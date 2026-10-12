#!/usr/bin/env python3
"""Ledger tools for thesis2paper.

  python scripts/t2p_ledger.py check  <project>   # validate ledger, evidence paths, numbers, citations
  python scripts/t2p_ledger.py macros <project>   # write paper/generated/results.tex from the ledger
  python scripts/t2p_ledger.py table  <project>   # compact markdown view of claims (for 1-pagers / chat)

Evidence `source` forms (relative to the project folder):
  raw/runs/E1/metrics.json#/acc/sparse   -> file must exist; JSON pointer resolved and compared to `value`
  raw/thesis/thesis.pdf#p42              -> file must exist (fragment is a human hint)
  work/repo@<sha>:path/to/file.py        -> file must exist in the worktree git history at <sha>
  lab:refs.bib#key / bib:key             -> key must exist in a bib file
Exit code 1 if there are errors (warnings don't fail).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ROLES = {"headline", "supporting", "methodological", "context"}
STATUSES = {"thesis-only", "reproduced", "verified", "discrepancy", "weak", "missing", "dropped"}
KINDS = {"number", "figure", "table", "script", "thesis", "literature"}
MACRO_RE = re.compile(r"^[A-Za-z]+$")


def load(project):
    proj = ROOT / "projects" / project
    led = yaml.safe_load((proj / "ledger.yaml").read_text()) or {}
    return proj, led.get("claims") or []


def bib_keys(proj):
    keys = set()
    for bib in [ROOT / "lab" / "refs.bib", proj / "paper" / "refs.bib"]:
        if bib.exists():
            keys |= set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", bib.read_text()))
    return keys


def json_pointer(obj, ptr):
    for part in [p for p in ptr.split("/") if p]:
        part = part.replace("~1", "/").replace("~0", "~")
        obj = obj[int(part)] if isinstance(obj, list) else obj[part]
    return obj


def close(a, b, rtol=1e-3):
    try:
        a, b = float(a), float(b)
    except (TypeError, ValueError):
        return str(a) == str(b)
    return abs(a - b) <= rtol * max(1.0, abs(a), abs(b))


def check_source(proj, ev, keys, errs, warns, where):
    src = str(ev.get("source", ""))
    if not src:
        errs.append(f"{where}: evidence without source")
        return
    if src.startswith(("bib:", "lab:refs.bib#")):
        key = src.split(":", 1)[1].split("#")[-1]
        if key not in keys:
            errs.append(f"{where}: bib key '{key}' not in any refs.bib")
        return
    m = re.match(r"^(work/repo)@([0-9a-f]{6,40}):(.+)$", src)
    if m:
        res = subprocess.run(["git", "cat-file", "-e", f"{m[2]}:{m[3]}"], cwd=proj / m[1], capture_output=True)
        if res.returncode != 0:
            errs.append(f"{where}: {m[3]} not found at commit {m[2]} in worktree")
        return
    path, _, frag = src.partition("#")
    f = proj / path
    if not f.exists():
        errs.append(f"{where}: missing file {path}")
        return
    if f.suffix == ".json" and frag.startswith("/"):
        try:
            got = json_pointer(json.loads(f.read_text()), frag)
        except Exception as e:  # noqa: BLE001
            errs.append(f"{where}: JSON pointer {frag} failed in {path}: {e!r}")
            return
        if "value" in ev and not close(got, ev["value"]):
            errs.append(f"{where}: ledger value {ev['value']} != source value {got} ({src})")


def validate(project):
    proj, claims = load(project)
    errs, warns = [], []
    keys = bib_keys(proj)
    ids, macros = set(), set()
    for i, c in enumerate(claims):
        cid = c.get("id", f"#{i}")
        if cid in ids:
            errs.append(f"{cid}: duplicate id")
        ids.add(cid)
        if not c.get("statement"):
            errs.append(f"{cid}: empty statement")
        if c.get("role") not in ROLES:
            errs.append(f"{cid}: role '{c.get('role')}' not in {sorted(ROLES)}")
        if c.get("status") not in STATUSES:
            errs.append(f"{cid}: status '{c.get('status')}' not in {sorted(STATUSES)}")
        for j, ev in enumerate(c.get("evidence") or []):
            where = f"{cid}.evidence[{j}]"
            if ev.get("kind") not in KINDS:
                errs.append(f"{where}: kind '{ev.get('kind')}' not in {sorted(KINDS)}")
            check_source(proj, ev, keys, errs, warns, where)
            if ev.get("macro"):
                if not MACRO_RE.match(ev["macro"]):
                    errs.append(f"{where}: macro '{ev['macro']}' must be letters only")
                if ev["macro"] in macros:
                    errs.append(f"{where}: duplicate macro '{ev['macro']}'")
                macros.add(ev["macro"])
                if "value" not in ev:
                    errs.append(f"{where}: macro without value")
        for e in c.get("experiments") or []:
            if not (proj / "experiments" / f"{e}.yaml").exists():
                warns.append(f"{cid}: experiment {e} has no spec file")
        if c.get("role") == "headline" and c.get("status") in {"thesis-only", "discrepancy", "missing", "weak"}:
            warns.append(f"{cid}: HEADLINE claim has status '{c.get('status')}'")
        if c.get("status") in {"reproduced", "verified"} and not any(
                str(ev.get("source", "")).startswith(("raw/runs/", "work/repo@")) for ev in c.get("evidence") or []):
            warns.append(f"{cid}: status '{c['status']}' but no evidence from raw/runs or the worktree")

    # paper checks
    paper = proj / "paper"
    for tex in sorted(paper.glob("*.tex")) if paper.exists() else []:
        txt = re.sub(r"(?<!\\)%.*", "", tex.read_text())
        for group in re.findall(r"\\cite[a-z]*\*?(?:\[[^\]]*\])*\{([^}]*)\}", txt):
            for k in [k.strip() for k in group.split(",") if k.strip()]:
                if k not in keys:
                    errs.append(f"{tex.name}: \\cite{{{k}}} not in refs.bib")
        n = len(re.findall(r"\\needcite\{", txt))
        if n:
            warns.append(f"{tex.name}: {n} \\needcite placeholder(s)")
        gen = paper / "generated" / "results.tex"
        defined = set(re.findall(r"\\newcommand\{\\(\w+)\}", gen.read_text())) if gen.exists() else set()
        stale = macros - defined
        if stale and tex.name == "main.tex":
            warns.append(f"results.tex is stale (missing {sorted(stale)[:5]}...); run `macros`")
    return claims, errs, warns


def cmd_check(project):
    claims, errs, warns = validate(project)
    for w in warns:
        print(f"WARN  {w}")
    for e in errs:
        print(f"ERROR {e}")
    print(f"{len(claims)} claims, {len(errs)} errors, {len(warns)} warnings")
    sys.exit(1 if errs else 0)


def cmd_macros(project):
    _, errs, _ = validate(project)
    if errs:
        sys.exit(f"ledger has {len(errs)} error(s); fix them first (run `check`). No macros written.")
    proj, claims = load(project)
    out = proj / "paper" / "generated" / "results.tex"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = ["% AUTO-GENERATED from ledger.yaml by scripts/t2p_ledger.py macros. Do not edit.", ""]
    for c in claims:
        for ev in c.get("evidence") or []:
            if ev.get("macro"):
                lines.append(f"% {c['id']} [{c.get('status')}] {ev.get('source', '')}")
                lines.append(f"\\newcommand{{\\{ev['macro']}}}{{{ev['value']}}}")
    out.write_text("\n".join(lines) + "\n")
    print(f"wrote {out.relative_to(ROOT)} ({sum(1 for l in lines if l.startswith(chr(92)))} macros)")


def cmd_table(project):
    _, claims = load(project)
    print("| id | role | status | statement | gaps | exps |\n|---|---|---|---|---|---|")
    for c in claims:
        print(f"| {c.get('id')} | {c.get('role')} | {c.get('status')} | {c.get('statement', '')} | "
              f"{'; '.join(c.get('gaps') or [])} | {', '.join(c.get('experiments') or [])} |")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in {"check", "macros", "table"}:
        sys.exit(__doc__)
    {"check": cmd_check, "macros": cmd_macros, "table": cmd_table}[sys.argv[1]](sys.argv[2])
