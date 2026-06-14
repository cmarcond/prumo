# /prumo.publish — Documento pedagógico da solução (PlantUML/C4 → LaTeX → PDF)

A fase de **publicação**, depois do `evaluate`. Transforma o `design/v_final` num
PDF que ensina a solução: requisitos em linguagem simples (com ênfase nos NFR de
capacidade/demanda), as decisões de system design, e um conjunto de figuras
legíveis (alto nível → zooms → sequências → cenários). Pré-condição:
`/prumo.evaluate` rodou (existe `design/v_final` e `evaluation/`).

Saídas (na **raiz do projeto**):
`doc/figures/*.puml`, `doc/solution.tex`, `doc/solution.pdf`.

> **Caminhos:** os resultados vão na **raiz** (`doc/`); o framework, incl. os
> templates de toolchain (`templates/publish/`), é lido de `.prumo/`. Convenção
> completa em `/prumo.init`.

## Passo 0 — Insumos
Leia: `design/v_final/design.json` (componentes/arestas anotadas), `requirements.json`
(números, invariantes, binder), `design/v_final/critique.md` e `approaches`/`tech_choices`
do design (decisões + alternativas rejeitadas), `evaluation/<slug>.md`, `intent.json`.

## Passo 1 — Decompor em figuras (skill `decompose-diagram-for-teaching`)
Gere os `.puml` em `doc/figures/` usando **C4-PlantUML da stdlib**
(`!include <C4/C4_Context>` / `<C4/C4_Container>` / `<C4/C4_Component>`) e sequências
em PlantUML puro. Espelhe os exemplos em `.prumo/templates/publish/figures-example/`.
Nomeie por ordem de leitura:
- `00-context.puml` — contexto (atores + sistema como caixa preta).
- `10-containers.puml` — os grandes blocos e o fluxo do dado (≤ ~10 caixas).
- `20-component-<parte>.puml` — um **zoom** por eixo de variação do problema
  (ex.: ingestão, serventia). Promova a zoom o que estourar o teto de legibilidade.
- `seq-<fluxo>.puml` — um diagrama de **sequência** por caminho principal (mostre
  ordem e assincronia: ack antes do fan-out, persist antes de visível).
- `scenario-<nome>.puml` — uma figura por **cenário** (falha parcial, pico/viral,
  concorrência). Só os componentes que o cenário exercita.

`type` do componente → macro C4: `service→Container`, `datastore→ContainerDb`,
`broker→ContainerQueue`, `cache`/`cdn`/`load_balancer`→`Container` rotulado.

## Passo 2 — Montar o documento (`doc/solution.tex`)
Copie `.prumo/templates/publish/solution.tex.template` para `doc/solution.tex` e
preencha os blocos `% >>> PRUMO:... <<<`. Estrutura obrigatória, nesta ordem:
1. **Requisitos em linguagem simples** — o problema e os funcionais sem jargão.
2. **Capacidade e demanda (NFR)** — EXPLIQUE cada número de escala em linguagem
   simples (o que significa no mundo real, de onde veio a conta), **nomeie o
   binder** (a restrição limitante) e preencha a tabela de dimensionamento.
3. **Decisões de projeto** — uma subseção por decisão grande: que pressão alivia,
   qual a **alternativa naive rejeitada** e o trade-off.
4. **Figuras** — use a macro `\prumofig{arquivo}{legenda}{explicação}`: primeiro a
   visão de contexto, depois containers, depois os zooms, depois as sequências,
   depois os cenários. **Cada figura seguida de prosa que a lê.**

## Passo 3 — Gate de documento (red) — `G-DOC-LEGIBLE` + `G-DOC-PEDAGOGIC` (ADV)
Delegue a um sub-agente de contexto limpo (que vê só `doc/`): ele verifica
- **legibilidade**: há vista de contexto; nenhuma figura passa de ~10 caixas;
  há sequência para cada fluxo principal;
- **pedagogia**: os NFR de capacidade estão explicados em linguagem simples com o
  binder nomeado; cada decisão tem alternativa rejeitada; nenhuma figura é órfã.
RED → conserte (quebre a figura densa em zoom; adicione o texto faltante) e re-rode.

## Passo 4 — Gerar o PDF (Docker)
Rode, da raiz do projeto:
```
bash .prumo/templates/publish/render.sh doc
```
Builda a imagem (`templates/publish/Dockerfile`: LaTeX + PlantUML + Graphviz +
librsvg) e roda o pipeline `.puml → SVG → PDF (vetor) → solution.pdf`. Se o build
LaTeX falhar, leia o log do `latexmk`, conserte o `.tex` e re-rode. Se não houver
Docker, reporte o comando para o usuário rodar.

## Saída
Anuncie o caminho de `doc/solution.pdf` e liste as figuras geradas. Fim do fluxo
Prumo: `init → requirements → design → evaluate → publish`.
