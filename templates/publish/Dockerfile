# Toolchain do /prumo.publish: PlantUML (C4) -> SVG -> PDF (vetor) + LaTeX -> PDF.
# Base enxuta (não o texlive-full): só o necessário para o template solution.tex.
FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      default-jre-headless \
      graphviz \
      librsvg2-bin \
      latexmk \
      lmodern \
      texlive-latex-recommended \
      texlive-latex-extra \
      texlive-fonts-recommended \
      texlive-lang-portuguese \
      wget ca-certificates fontconfig \
 && rm -rf /var/lib/apt/lists/*

# plantuml.jar pinado e recente (traz a stdlib C4 via "!include <C4/...>",
# sem depender de internet no render).
ARG PLANTUML_VERSION=1.2024.7
RUN wget -qO /opt/plantuml.jar \
      "https://github.com/plantuml/plantuml/releases/download/v${PLANTUML_VERSION}/plantuml-${PLANTUML_VERSION}.jar"
ENV PLANTUML_JAR=/opt/plantuml.jar

WORKDIR /work
