#!/usr/bin/env bash
# Roda DENTRO do container (ver render.sh). Pipeline:
#   .puml --(plantuml -tsvg)--> .svg --(rsvg-convert)--> .pdf (vetor) --> LaTeX --> solution.pdf
# Uso: bash build.sh [DOC_DIR]   (default: doc)
set -euo pipefail

DOC_DIR="${1:-doc}"
FIG="$DOC_DIR/figures"
PLANTUML_JAR="${PLANTUML_JAR:-/opt/plantuml.jar}"

[ -d "$FIG" ] || { echo "erro: não achei $FIG (gere os .puml antes)"; exit 1; }
[ -f "$DOC_DIR/solution.tex" ] || { echo "erro: não achei $DOC_DIR/solution.tex"; exit 1; }

echo ">> [1/3] PlantUML -> SVG"
mkdir -p "$FIG/svg"
java -jar "$PLANTUML_JAR" -tsvg -charset UTF-8 -o "svg" "$FIG"/*.puml

echo ">> [2/3] SVG -> PDF (vetor)"
mkdir -p "$FIG/pdf"
for f in "$FIG"/svg/*.svg; do
  base="$(basename "$f" .svg)"
  rsvg-convert -f pdf -o "$FIG/pdf/$base.pdf" "$f"
done

echo ">> [3/3] LaTeX -> PDF"
( cd "$DOC_DIR" && latexmk -pdf -interaction=nonstopmode -halt-on-error solution.tex >/dev/null )

echo "OK -> $DOC_DIR/solution.pdf"
