#!/usr/bin/env python3
"""Instalador do Prumo — framework agêntico de System Design.

Copia constituição, gates, skills, comandos e templates para `.prumo/` num
projeto alvo. Idempotente: nunca destrói conteúdo existente.

Regras por arquivo de destino:
- não existe        -> cria
- existe, idêntico  -> pula
- existe, diferente -> preserva o existente e grava a nova versão como `<nome>.new`
                       (com --force: move o existente para `<nome>.bak`)

Uso:
    python3 install.py /caminho/do/projeto-alvo [--force] [--no-claude]
"""
from __future__ import annotations
import argparse, filecmp, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMANDS = ["init", "requirements", "design", "evaluate", "status"]
# top-level files + trees copiados para .prumo/
FILES = ["MANIFESTO.md"]
TREES = ["gates", "skills", "commands", "templates", "docs"]


class Report:
    def __init__(self): self.created=[]; self.skipped=[]; self.conflicted=[]; self.backed_up=[]
    def summary(self):
        out=[f"criados: {len(self.created)}", f"pulados (idênticos): {len(self.skipped)}"]
        if self.backed_up: out += [f"sobrescritos c/ .bak: {len(self.backed_up)}"]+[f"  - {p}" for p in self.backed_up]
        if self.conflicted: out += [f"conflitos (existente preservado, nova em .new): {len(self.conflicted)}"]+[f"  - {p}" for p in self.conflicted]
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
    ap = argparse.ArgumentParser(description="Instala o Prumo num projeto.")
    ap.add_argument("target", type=Path)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-claude", action="store_true")
    args = ap.parse_args(argv)

    if not (ROOT/"commands").is_dir() or not (ROOT/"skills").is_dir():
        print("erro: rode a partir de um checkout completo do prumo", file=sys.stderr); return 2

    target = args.target.resolve(); target.mkdir(parents=True, exist_ok=True)
    prumo = target / ".prumo"; r = Report()

    for f in FILES:
        install_file(ROOT/f, prumo/f, args.force, r)
    for t in TREES:
        install_tree(ROOT/t, prumo/t, args.force, r)
    if not args.no_claude:
        # atalhos /prumo.<cmd>
        for c in COMMANDS:
            src = ROOT/"commands"/f"{c}.md"
            if src.is_file():
                install_file(src, target/".claude"/"commands"/"prumo"/f"{c}.md", args.force, r)

    print(f"Prumo instalado em {prumo}")
    print(r.summary())
    print("\nPróximo passo: abra o agente no projeto e rode /prumo.init "
          "(.prumo/commands/init.md). O fluxo é init → design → evaluate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
