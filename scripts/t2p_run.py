#!/usr/bin/env python3
"""Experiment runner for thesis2paper. Every experiment goes through here so that commit, spec,
outputs and GPU-hours are recorded and the per-round budget is enforced.

Usage:
  python scripts/t2p_run.py launch <project> <exp-id> [--dry-run] [--force-budget]
  python scripts/t2p_run.py status <project> [exp-id ...]
  python scripts/t2p_run.py wait   <project> <exp-id> [...] [--poll 60]
  python scripts/t2p_run.py budget <project>

Spec file: projects/<project>/experiments/<exp-id>.yaml
  id: E1
  title: "Robustness of C1 to network size"
  hypothesis: "..."
  claims: [C1]
  round: 1
  command: "python train.py --config configs/e1.yaml --out $T2P_OUT"   # run from work/repo/<workdir>
  # OR notebook: notebooks/fig3.ipynb  (+ optional parameters: {...}; uses papermill if installed)
  workdir: .
  gpus: 1                 # 0 for CPU-only
  est_gpu_hours: 2.0
  timeout_hours: 12
  expected_outputs: [metrics.json]
  success_criterion: "..."

The job gets env vars T2P_OUT (absolute run dir — write results there), T2P_EXP, CUDA_VISIBLE_DEVICES.
Outputs land in projects/<project>/raw/runs/<exp-id>[-rN]/ and must not be edited afterwards.
"""
import argparse
import datetime as dt
import json
import os
import shlex
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def now():
    return dt.datetime.now().isoformat(timespec="seconds")


def load_project(name):
    proj = ROOT / "projects" / name
    if not (proj / "project.yaml").exists():
        sys.exit(f"no such project: {name}")
    return proj, yaml.safe_load((proj / "project.yaml").read_text())


def pid_alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, TypeError):
        return False
    except PermissionError:
        return True


def run_state(run_dir: Path) -> dict:
    meta = json.loads((run_dir / "run.json").read_text())
    ec_file = run_dir / "exit_code"
    if ec_file.exists():
        code = int(ec_file.read_text().strip() or -1)
        meta["state"] = "done" if code == 0 else ("timeout" if code == 124 else "failed")
        meta["exit_code"] = code
        end = dt.datetime.fromtimestamp(ec_file.stat().st_mtime)
    elif pid_alive(meta.get("pid")):
        meta["state"] = "running"
        end = dt.datetime.now()
    else:
        meta["state"] = "lost"   # process gone without writing exit_code (killed / reboot)
        end = dt.datetime.fromtimestamp((run_dir / "stdout.log").stat().st_mtime)
    hours = (end - dt.datetime.fromisoformat(meta["started"])).total_seconds() / 3600
    meta["wall_hours"] = round(hours, 3)
    meta["gpu_hours"] = round(hours * max(len(meta.get("gpu_ids", [])), 0), 3)
    return meta


def all_runs(proj: Path):
    runs_dir = proj / "raw" / "runs"
    if not runs_dir.exists():
        return []
    return [run_state(d) for d in sorted(runs_dir.iterdir()) if (d / "run.json").exists()]


def gpus_in_use():
    used = set()
    for proj in (ROOT / "projects").iterdir():
        if proj.name.startswith("_") or not proj.is_dir():
            continue
        for r in all_runs(proj):
            if r["state"] == "running":
                used.update(r.get("gpu_ids", []))
    return used


def nvidia_busy(threshold_mb=1000):
    """GPUs with more than threshold MB used by anyone (other users, notebooks)."""
    if not shutil.which("nvidia-smi"):
        return set()
    out = subprocess.run(["nvidia-smi", "--query-gpu=index,memory.used", "--format=csv,noheader,nounits"],
                         text=True, capture_output=True).stdout
    busy = set()
    for line in out.strip().splitlines():
        idx, mem = [x.strip() for x in line.split(",")]
        if int(mem) > threshold_mb:
            busy.add(int(idx))
    return busy


def round_usage(proj, rnd):
    return sum(r["gpu_hours"] for r in all_runs(proj) if r.get("round") == rnd)


def cmd_launch(a):
    proj, cfg = load_project(a.project)
    comp = cfg.get("compute", {})
    spec_path = proj / "experiments" / f"{a.exp}.yaml"
    if not spec_path.exists():
        sys.exit(f"missing spec {spec_path}")
    spec = yaml.safe_load(spec_path.read_text())
    rnd = spec.get("round", 1)
    n_gpu = int(spec.get("gpus", 0))

    # budget
    budget = comp.get("gpu_hours_budget_per_round")
    used = round_usage(proj, rnd)
    est = float(spec.get("est_gpu_hours", 0))
    if budget is not None and used + est > budget and not a.force_budget:
        sys.exit(f"BUDGET: round {rnd} used {used:.1f} + est {est:.1f} > budget {budget} GPU-h. "
                 f"Raise it at a checkpoint or pass --force-budget.")

    # parallelism
    running = [r for r in all_runs(proj) if r["state"] == "running"]
    if len(running) >= comp.get("max_parallel_jobs", 2):
        sys.exit(f"WAIT: {len(running)} jobs already running (max_parallel_jobs).")

    # gpu allocation
    gpu_ids = []
    if n_gpu > 0:
        allowed = comp.get("gpu_ids") or []
        free = [g for g in allowed if g not in gpus_in_use() | nvidia_busy()]
        if len(free) < n_gpu:
            sys.exit(f"WAIT: need {n_gpu} GPU(s); free among {allowed}: {free}")
        gpu_ids = free[:n_gpu]

    # run dir (never overwrite)
    runs_dir = proj / "raw" / "runs"
    run_id, k = a.exp, 1
    while (runs_dir / run_id).exists():
        k += 1
        run_id = f"{a.exp}-r{k}"
    run_dir = runs_dir / run_id

    if "worktree" not in (cfg.get("repo") or {}):
        sys.exit("project has no worktree configured (project.yaml → repo); was it created with new_project.py?")
    work = proj / cfg["repo"]["worktree"]
    cwd = (work / spec.get("workdir", ".")).resolve()
    sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=work, text=True, capture_output=True).stdout.strip()
    diff = subprocess.run(["git", "diff", "HEAD"], cwd=work, text=True, capture_output=True).stdout

    if "notebook" in spec:
        nb = shlex.quote(spec["notebook"])
        out_nb = shlex.quote(str(run_dir / Path(spec["notebook"]).name))
        if shutil.which("papermill"):
            params = " ".join(f"-p {shlex.quote(str(k))} {shlex.quote(str(v))}" for k, v in (spec.get("parameters") or {}).items())
            command = f"papermill {nb} {out_nb} {params}"
        else:
            command = f"jupyter nbconvert --to notebook --execute {nb} --output {out_nb} --ExecutePreprocessor.timeout=-1"
    else:
        command = spec["command"]

    timeout = int(float(spec.get("timeout_hours", comp.get("default_timeout_hours", 24))) * 3600)
    if a.dry_run:
        print(f"[dry-run] {run_id}: cwd={cwd}\n  gpus={gpu_ids} commit={sha[:10]} dirty={bool(diff)}\n  $ {command}\n"
              f"  budget round {rnd}: used {used:.1f} + est {est:.1f} / {budget}")
        return

    run_dir.mkdir(parents=True)
    shutil.copy2(spec_path, run_dir / "spec.yaml")
    if diff:
        (run_dir / "uncommitted.patch").write_text(diff)
        print("  ! worktree has uncommitted changes; saved as uncommitted.patch (commit before launching next time)")

    env = os.environ.copy()
    env.update(T2P_OUT=str(run_dir), T2P_EXP=run_id,
               CUDA_VISIBLE_DEVICES=",".join(map(str, gpu_ids)) if n_gpu > 0 else "")
    wrapper = (f"timeout {timeout} bash -c {shlex.quote(command)} "
               f"> {shlex.quote(str(run_dir / 'stdout.log'))} 2> {shlex.quote(str(run_dir / 'stderr.log'))}; "
               f"echo $? > {shlex.quote(str(run_dir / 'exit_code'))}")
    proc = subprocess.Popen(["bash", "-c", wrapper], cwd=cwd, env=env,
                            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            start_new_session=True)
    meta = dict(run_id=run_id, exp=a.exp, round=rnd, claims=spec.get("claims", []), pid=proc.pid,
                started=now(), host=socket.gethostname(), commit=sha, dirty=bool(diff),
                gpu_ids=gpu_ids, command=command, cwd=str(cwd), timeout_s=timeout)
    (run_dir / "run.json").write_text(json.dumps(meta, indent=2))

    with open(proj / "wiki" / "log.md", "a") as f:
        f.write(f"\n## [{now()[:16].replace('T', ' ')}] run | launched {run_id}\n- {spec.get('title', '')}\n"
                f"- commit {sha[:10]}{' (dirty)' if diff else ''}, gpus {gpu_ids}, est {est} GPU-h\n")
    print(f"launched {run_id} pid={proc.pid} gpus={gpu_ids} -> {run_dir.relative_to(ROOT)}")


def cmd_status(a):
    proj, _ = load_project(a.project)
    runs = all_runs(proj)
    if a.exp:
        runs = [r for r in runs if r["exp"] in a.exp or r["run_id"] in a.exp]
    if not runs:
        print("no runs")
        return
    print(f"{'run':<12}{'state':<9}{'round':<6}{'gpus':<8}{'wall_h':<8}{'gpu_h':<8}claims")
    for r in runs:
        print(f"{r['run_id']:<12}{r['state']:<9}{r['round']:<6}{','.join(map(str, r['gpu_ids'])) or '-':<8}"
              f"{r['wall_hours']:<8}{r['gpu_hours']:<8}{','.join(r['claims'])}")
        if r["state"] in ("failed", "timeout", "lost"):
            err = proj / "raw" / "runs" / r["run_id"] / "stderr.log"
            tail = err.read_text().strip().splitlines()[-5:] if err.exists() else []
            for line in tail:
                print(f"    | {line}")


def cmd_wait(a):
    proj, _ = load_project(a.project)
    while True:
        runs = [r for r in all_runs(proj) if r["exp"] in a.exp or r["run_id"] in a.exp]
        pending = [r["run_id"] for r in runs if r["state"] == "running"]
        if not pending:
            break
        time.sleep(a.poll)
    cmd_status(a)


def cmd_budget(a):
    proj, cfg = load_project(a.project)
    budget = cfg.get("compute", {}).get("gpu_hours_budget_per_round")
    rounds = sorted({r["round"] for r in all_runs(proj)} | {cfg.get("state", {}).get("round", 0)})
    for rnd in rounds:
        print(f"round {rnd}: {round_usage(proj, rnd):.2f} / {budget} GPU-h")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("launch"); p.add_argument("project"); p.add_argument("exp")
    p.add_argument("--dry-run", action="store_true"); p.add_argument("--force-budget", action="store_true")
    p.set_defaults(fn=cmd_launch)
    p = sub.add_parser("status"); p.add_argument("project"); p.add_argument("exp", nargs="*")
    p.set_defaults(fn=cmd_status)
    p = sub.add_parser("wait"); p.add_argument("project"); p.add_argument("exp", nargs="+")
    p.add_argument("--poll", type=int, default=60); p.set_defaults(fn=cmd_wait)
    p = sub.add_parser("budget"); p.add_argument("project"); p.set_defaults(fn=cmd_budget)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
