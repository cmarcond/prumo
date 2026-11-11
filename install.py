#!/usr/bin/env python3
"""Prumo installer — an agentic framework for system design.

Copies the constitution, gates, skills, commands and templates into `.prumo/`
in a target project. Idempotent: it never destroys existing content.

Rules per destination file:
- does not exist     -> create it
- exists, identical  -> skip it
- exists, different  -> keep the existing file and write the new version as `<name>.new`
                        (with --force: move the existing file to `<name>.bak`)

Usage:
    python3 install.py /path/to/target-project [--force] [--no-claude]
"""
from __future__ import annotations
import argparse, filecmp, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMANDS = ["init", "requirements", "design", "evaluate", "publish", "status", "reverse"]
# top-level files + trees copied into .prumo/
FILES = ["MANIFESTO.md"]
TREES = ["gates", "skills", "commands", "templates", "docs"]


class Report:
    def __init__(self): self.created=[]; self.skipped=[]; self.conflicted=[]; self.backed_up=[]
    def summary(self):
        out=[f"created: {len(self.created)}", f"skipped (identical): {len(self.skipped)}"]
        if self.backed_up: out += [f"overwritten with .bak: {len(self.backed_up)}"]+[f"  - {p}" for p in self.backed_up]
        if self.conflicted: out += [f"conflicts (existing kept, new version in .new): {len(self.conflicted)}"]+[f"  - {p}" for p in self.conflicted]
        return "\n".join(out)


def install_file(src: Path, dest: Path, force: bool, r: Report):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        shutil.copy2(src, dest); r.created.append(str(dest)); return
    if filecmp.cmp(src, dest, shallow=False):
        r.skipped.append(str(dest)); return
    if force:
        shutil.copy2(dest, dest.with_name(dest.name+".bak")); shutil.copy2(src, dest)
        r.backed_up.append(str(dest)); return
    shutil.copy2(src, dest.with_name(dest.name+".new")); r.conflicted.append(str(dest))


def install_tree(src_dir: Path, dest_dir: Path, force: bool, r: Report):
    if not src_dir.is_dir(): return
    for src in sorted(src_dir.rglob("*")):
        if src.is_file():
            install_file(src, dest_dir / src.relative_to(src_dir), force, r)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Install Prumo into a project.")
    ap.add_argument("target", type=Path)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-claude", action="store_true")
    args = ap.parse_args(argv)

    if not (ROOT/"commands").is_dir() or not (ROOT/"skills").is_dir():
        print("error: run from a complete checkout of prumo", file=sys.stderr); return 2

    target = args.target.resolve(); target.mkdir(parents=True, exist_ok=True)
    prumo = target / ".prumo"; r = Report()

    for f in FILES:
        install_file(ROOT/f, prumo/f, args.force, r)
    for t in TREES:
        install_tree(ROOT/t, prumo/t, args.force, r)
    if not args.no_claude:
        # /prumo.<cmd> shortcuts
        for c in COMMANDS:
            src = ROOT/"commands"/f"{c}.md"
            if src.is_file():
                install_file(src, target/".claude"/"commands"/"prumo"/f"{c}.md", args.force, r)

    print(f"Prumo installed in {prumo}")
    print(r.summary())
    print("\nNext step: open the agent in the project and run /prumo.init "
          "(.prumo/commands/init.md). The flow is "
          "init → requirements → design → evaluate → publish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
