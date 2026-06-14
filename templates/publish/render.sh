#!/usr/bin/env bash
# Roda no HOST: builda a imagem (cacheada) e gera o PDF do documento da solução.
# Uso (a partir da raiz do projeto):  bash .prumo/templates/publish/render.sh [DOC_DIR]
set -euo pipefail

DOC_DIR="${1:-doc}"
IMAGE="${PRUMO_LATEX_IMAGE:-prumo-latex:latest}"
PROJECT_DIR="$(pwd)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

command -v docker >/dev/null || { echo "erro: docker não encontrado"; exit 1; }
[ -d "$PROJECT_DIR/$DOC_DIR" ] || { echo "erro: $DOC_DIR/ não existe na raiz do projeto"; exit 1; }

echo ">> build da imagem $IMAGE (cacheado após a 1ª vez)"
docker build -t "$IMAGE" "$SCRIPT_DIR"

echo ">> render em container"
docker run --rm -v "$PROJECT_DIR":/work -w /work "$IMAGE" \
  bash .prumo/templates/publish/build.sh "$DOC_DIR"

echo ">> pronto: $DOC_DIR/solution.pdf"
