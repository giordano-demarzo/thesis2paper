#!/usr/bin/env python3
"""Claude Code status line for thesis2paper: project · stage/round · GPU budget · jobs · pending decision."""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    data = json.load(sys.stdin)
except Exception:  # noqa: BLE001
    data = {}
model = (data.get("model") or {}).get("display_name", "")
project = os.environ.get("T2P_PROJECT")
D, B, Y, G, C, X = "\033[2m", "\033[1m", "\033[33m", "\033[32m", "\033[36m", "\033[0m"
if not project:
    print(f"{B}t2p{X} · lab {D}· {model}{X}")
    sys.exit()
try:
    import importlib.util
    from importlib.machinery import SourceFileLoader

    import yaml
    from t2p_run import all_runs
    root = Path(__file__).resolve().parent.parent
    p = root / "projects" / project
    cfg = yaml.safe_load((p / "project.yaml").read_text())
    st = cfg.get("state", {})
    rnd = st.get("round", 0)
    runs = all_runs(p)
    used = sum(r["gpu_hours"] for r in runs if r.get("round") == rnd)
    budget = cfg.get("compute", {}).get("gpu_hours_budget_per_round", "?")
    running = sum(r["state"] == "running" for r in runs)
    failed = sum(r["state"] in ("failed", "timeout", "lost") for r in runs if r.get("round") == rnd)
    loader = SourceFileLoader("t2pcli", str(root / "scripts" / "t2p"))
    t2p = importlib.util.module_from_spec(importlib.util.spec_from_loader("t2pcli", loader))
    loader.exec_module(t2p)
    pend = t2p.pending_decision(p)
    parts = [f"{B}t2p{X} {C}{project}{X}", f"{st.get('stage')} r{rnd}", f"GPU {used:.1f}/{budget}h"]
    if running:
        parts.append(f"{G}{running} running{X}")
    if failed:
        parts.append(f"{Y}{failed} failed{X}")
    if pend:
        parts.append(f"{Y}⏳ {pend.removesuffix('.md')}{X}")
    print(" · ".join(parts) + f" {D}· {model}{X}")
except Exception as e:  # noqa: BLE001
    print(f"t2p {project} · status unavailable ({type(e).__name__})")
