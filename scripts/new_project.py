#!/usr/bin/env python3
"""Create a new thesis2paper project from projects/_template.

Usage:
  python scripts/new_project.py <name> --thesis path/to/thesis.pdf --repo path/to/student/repo \
      [--venue pnas] [--papers p1.pdf p2.pdf ...]

- Copies the template to projects/<name>/
- Copies the thesis (file or folder) into raw/thesis/ and extracts text from PDFs (pdftotext)
- Creates a git worktree of the student repo at work/repo on branch t2p/<name>
  (falls back to a plain copy if the repo is not a git repo)
- Records the repo path and base commit in project.yaml
"""
import argparse
import datetime as dt
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def sh(cmd, cwd=None, check=True):
    return subprocess.run(cmd, cwd=cwd, check=check, text=True, capture_output=True)


def copy_into(src: Path, dst_dir: Path):
    dst_dir.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dst_dir / src.name, dirs_exist_ok=True)
    else:
        shutil.copy2(src, dst_dir / src.name)


def extract_pdfs(folder: Path):
    if not shutil.which("pdftotext"):
        print("  ! pdftotext not found; skipping text extraction (Claude can read PDFs directly)")
        return
    for pdf in folder.rglob("*.pdf"):
        txt = pdf.with_suffix(".txt")
        if not txt.exists():
            sh(["pdftotext", "-layout", str(pdf), str(txt)], check=False)


def setup_repo(repo: Path, proj: Path, name: str) -> dict:
    work = proj / "work" / "repo"
    work.parent.mkdir(parents=True, exist_ok=True)
    info = {"path": str(repo), "worktree": str(work.relative_to(proj))}
    is_git = sh(["git", "rev-parse", "--is-inside-work-tree"], cwd=repo, check=False).returncode == 0
    if is_git:
        sha = sh(["git", "rev-parse", "HEAD"], cwd=repo).stdout.strip()
        dirty = sh(["git", "status", "--porcelain"], cwd=repo).stdout.strip()
        if dirty:
            print("  ! student repo has uncommitted changes; the worktree is based on HEAD and will NOT include them")
        branch, k = f"t2p/{name}", 1
        while sh(["git", "rev-parse", "--verify", "--quiet", branch], cwd=repo, check=False).returncode == 0:
            k += 1
            branch = f"t2p/{name}-{k}"
        res = sh(["git", "worktree", "add", "-b", branch, str(work), sha], cwd=repo, check=False)
        if res.returncode != 0:
            raise RuntimeError(f"git worktree failed:\n{res.stderr}")
        info.update(kind="git-worktree", base_commit=sha, branch=branch, uncommitted_changes_at_start=bool(dirty))
    else:
        print("  ! repo is not a git repo; copying and initialising git in the copy")
        shutil.copytree(repo, work, ignore=shutil.ignore_patterns(".ipynb_checkpoints", "__pycache__"))
        sh(["git", "init", "-q"], cwd=work)
        sh(["git", "add", "-A"], cwd=work)
        sh(["git", "-c", "user.name=t2p", "-c", "user.email=t2p@local", "commit", "-qm", "snapshot of student repo"], cwd=work)
        sha = sh(["git", "rev-parse", "HEAD"], cwd=work).stdout.strip()
        info.update(kind="copy", base_commit=sha)
    return info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--thesis", required=True, type=Path)
    ap.add_argument("--repo", required=True, type=Path)
    ap.add_argument("--venue", default="undecided")
    ap.add_argument("--papers", nargs="*", type=Path, default=[])
    args = ap.parse_args()

    proj = ROOT / "projects" / args.name
    if proj.exists():
        sys.exit(f"{proj} already exists")
    for p in [args.thesis, args.repo, *args.papers]:
        if not p.exists():
            sys.exit(f"not found: {p}")

    shutil.copytree(ROOT / "projects" / "_template", proj)
    try:
        build(proj, args)
    except BaseException as e:
        shutil.rmtree(proj, ignore_errors=True)
        sys.exit(f"setup failed, removed {proj}: {e}")
    print(f"created {proj}")
    print("next: /t2p-intake " + args.name)


def build(proj, args):
    copy_into(args.thesis.resolve(), proj / "raw" / "thesis")
    for p in args.papers:
        copy_into(p.resolve(), proj / "raw" / "papers")
    extract_pdfs(proj / "raw")

    repo_info = setup_repo(args.repo.resolve(), proj, args.name)

    cfg_path = proj / "project.yaml"
    cfg = yaml.safe_load(cfg_path.read_text())
    cfg["name"] = args.name
    cfg["created"] = dt.date.today().isoformat()
    cfg["target"]["venue"] = args.venue
    cfg["repo"] = repo_info
    cfg_path.write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True))

    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(proj / "wiki" / "log.md", "a") as f:
        f.write(f"\n## [{now}] setup | project created\n- thesis: {args.thesis}\n- repo: {args.repo} "
                f"@ {repo_info['base_commit'][:10]} ({repo_info['kind']})\n")
    print(f"repo -> {proj / 'work' / 'repo'} ({repo_info['kind']}, base {repo_info['base_commit'][:10]}, "
          f"branch {repo_info.get('branch', '-')})")


if __name__ == "__main__":
    main()
