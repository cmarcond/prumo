#!/usr/bin/env bash
# Runs on the HOST: builds the image (cached) and generates the PDF of the solution document.
# Usage (from the project root):  bash .prumo/templates/publish/render.sh [DOC_DIR]
set -euo pipefail

DOC_DIR="${1:-doc}"
IMAGE="${PRUMO_LATEX_IMAGE:-prumo-latex:latest}"
PROJECT_DIR="$(pwd)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

command -v docker >/dev/null || { echo "error: docker not found"; exit 1; }
[ -d "$PROJECT_DIR/$DOC_DIR" ] || { echo "error: $DOC_DIR/ does not exist in the project root"; exit 1; }

echo ">> building image $IMAGE (cached after the first time)"
docker build -t "$IMAGE" "$SCRIPT_DIR"

echo ">> rendering in a container"
docker run --rm -v "$PROJECT_DIR":/work -w /work "$IMAGE" \
  bash .prumo/templates/publish/build.sh "$DOC_DIR"

echo ">> done: $DOC_DIR/solution.pdf"
