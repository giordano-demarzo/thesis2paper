#!/usr/bin/env python3
"""Create a new thesis2paper project from projects/_template.

Usage:
  python scripts/new_project.py <name> --repo <git URL or local path> [--thesis path] [--venue pnas] [--papers ...]

Inbox convention (so you don't have to pass paths): put the material in inbox/<name>/
  inbox/<name>/            thesis PDF and/or LaTeX source (anything here except the items below)
  inbox/<name>/papers/     optional context papers
  inbox/<name>/repo.txt    optional: the repo URL (then --repo can be omitted)

- Copies the template to projects/<name>/
- Copies the thesis into raw/thesis/ (and papers into raw/papers/), extracts text from PDFs
- Repo: a URL is cloned into source/repo (pristine, never edited); a local path is used in place.
  A git worktree of it is created at work/repo on branch t2p/<name> — all edits happen there.
  (Non-git local folders are copied and snapshotted.)
- Records the repo, URL and base commit in project.yaml
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


def is_url(s: str) -> bool:
    return s.startswith(("http://", "https://", "git@", "ssh://", "file://")) or s.endswith(".git")


def clone(url: str, proj: Path) -> Path:
    dst = proj / "source" / "repo"
    dst.parent.mkdir(parents=True, exist_ok=True)
    print(f"  cloning {url} ...")
    res = sh(["git", "clone", "--recurse-submodules", url, str(dst)], check=False)
    if res.returncode != 0 and "github.com" in url and shutil.which("gh"):
        slug = url.split("github.com")[-1].lstrip(":/").removesuffix(".git")
        res = sh(["gh", "repo", "clone", slug, str(dst), "--", "--recurse-submodules"], check=False)
    if res.returncode != 0:
        raise RuntimeError(f"clone failed (private repo? run `gh auth login` or add an SSH key):\n{res.stderr.strip()}")
    if (dst / ".gitattributes").exists() and "filter=lfs" in (dst / ".gitattributes").read_text():
        if shutil.which("git-lfs"):
            sh(["git", "lfs", "pull"], cwd=dst, check=False)
        else:
            print("  ! repo uses Git LFS but git-lfs is not installed; large files are pointers only")
    return dst


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
    ap.add_argument("--thesis", type=Path, help="default: inbox/<name>/")
    ap.add_argument("--repo", help="git URL or local path; default: inbox/<name>/repo.txt")
    ap.add_argument("--venue", default="undecided")
    ap.add_argument("--papers", nargs="*", type=Path, default=[])
    args = ap.parse_args()

    proj = ROOT / "projects" / args.name
    if proj.exists():
        sys.exit(f"{proj} already exists")
    inbox = ROOT / "inbox" / args.name
    if args.repo is None and (inbox / "repo.txt").exists():
        args.repo = (inbox / "repo.txt").read_text().strip().splitlines()[0].strip()
    if not args.repo:
        sys.exit("no repo: pass --repo <URL or path> or write the URL in inbox/<name>/repo.txt")
    if args.thesis is None:
        thesis_items = [f for f in inbox.iterdir() if f.name not in {"papers", "repo.txt", ".gitkeep"}] \
            if inbox.exists() else []
        if not thesis_items:
            sys.exit(f"no thesis: put it in {inbox.relative_to(ROOT)}/ or pass --thesis <path>")
        args.thesis_items = thesis_items
        if (inbox / "papers").is_dir():
            args.papers += sorted((inbox / "papers").iterdir())
    else:
        args.thesis_items = [args.thesis]
    local = [*args.thesis_items, *args.papers] + ([] if is_url(args.repo) else [Path(args.repo)])
    for p in local:
        if not Path(p).exists():
            sys.exit(f"not found: {p}")

    shutil.copytree(ROOT / "projects" / "_template", proj)
    try:
        build(proj, args)
    except BaseException as e:
        shutil.rmtree(proj, ignore_errors=True)
        sys.exit(f"setup failed, removed {proj}: {e}")
    print(f"created {proj}")


def build(proj, args):
    for t in args.thesis_items:
        copy_into(Path(t).resolve(), proj / "raw" / "thesis")
    for p in args.papers:
        copy_into(Path(p).resolve(), proj / "raw" / "papers")
    extract_pdfs(proj / "raw")

    if is_url(args.repo):
        repo_info = setup_repo(clone(args.repo, proj), proj, args.name)
        repo_info["url"] = args.repo
        repo_info["path"] = "source/repo"
    else:
        repo_info = setup_repo(Path(args.repo).resolve(), proj, args.name)

    cfg_path = proj / "project.yaml"
    cfg = yaml.safe_load(cfg_path.read_text())
    cfg["name"] = args.name
    cfg["created"] = dt.date.today().isoformat()
    cfg["target"]["venue"] = args.venue
    cfg["repo"] = repo_info
    cfg_path.write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True))

    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(proj / "wiki" / "log.md", "a") as f:
        f.write(f"\n## [{now}] setup | project created\n- thesis: {', '.join(Path(t).name for t in args.thesis_items)}\n- repo: {args.repo} "
                f"@ {repo_info['base_commit'][:10]} ({repo_info['kind']})\n")
    print(f"repo -> {proj / 'work' / 'repo'} ({repo_info['kind']}, base {repo_info['base_commit'][:10]}, "
          f"branch {repo_info.get('branch', '-')})")


if __name__ == "__main__":
    main()
