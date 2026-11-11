# Toolchain for /prumo.publish: PlantUML (C4) -> SVG -> PDF (vector) + LaTeX -> PDF.
# Lean base (not texlive-full): only what the solution.tex template needs.
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
      wget ca-certificates fontconfig \
 && rm -rf /var/lib/apt/lists/*

# plantuml.jar pinned and recent (it ships the C4 stdlib via "!include <C4/...>",
# with no dependency on the internet at render time).
ARG PLANTUML_VERSION=1.2024.7
RUN wget -qO /opt/plantuml.jar \
      "https://github.com/plantuml/plantuml/releases/download/v${PLANTUML_VERSION}/plantuml-${PLANTUML_VERSION}.jar"
ENV PLANTUML_JAR=/opt/plantuml.jar

WORKDIR /work
