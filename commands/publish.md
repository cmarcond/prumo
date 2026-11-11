# /prumo.publish — Teaching document for the solution (PlantUML/C4 → LaTeX → PDF)

The **publishing** phase, after `evaluate`. It turns `design/v_final` into a
PDF that teaches the solution: requirements in plain language (with emphasis on the
capacity/demand NFRs), the system design decisions, and a set of legible figures
(high level → zooms → sequences → scenarios). Precondition:
`/prumo.evaluate` has run (`design/v_final` and `evaluation/` exist).

Outputs (in the **project root**):
`doc/figures/*.puml`, `doc/solution.tex`, `doc/solution.pdf`.

> **Paths:** the results go in the **root** (`doc/`); the framework, including the
> toolchain templates (`templates/publish/`), is read from `.prumo/`. Full
> convention in `/prumo.init`.

## Step 0 — Inputs
Read: `design/v_final/design.json` (annotated components/edges), `requirements.json`
(numbers, invariants, binder), `design/v_final/critique.md` and the design's
`approaches`/`tech_choices` (decisions + rejected alternatives), `evaluation/<slug>.md`,
`intent.json`.

## Step 1 — Decompose into figures (skill `decompose-diagram-for-teaching`)
Generate the `.puml` files in `doc/figures/` using **C4-PlantUML from the stdlib**
(`!include <C4/C4_Context>` / `<C4/C4_Container>` / `<C4/C4_Component>`) and sequences
in plain PlantUML. Mirror the examples in `.prumo/templates/publish/figures-example/`.
Name them in reading order:
- `00-context.puml` — context (actors + the system as a black box).
- `10-containers.puml` — the big blocks and the flow of the data (≤ ~10 boxes).
- `20-component-<part>.puml` — one **zoom** per axis of variation of the problem
  (e.g. ingestion, serving). Promote to a zoom whatever exceeds the legibility ceiling.
- `seq-<flow>.puml` — one **sequence** diagram per main path (show
  order and asynchrony: ack before the fan-out, persist before visible).
- `scenario-<name>.puml` — one figure per **scenario** (partial failure, peak/viral,
  concurrency). Only the components the scenario exercises.

Component `type` → C4 macro: `service→Container`, `datastore→ContainerDb`,
`broker→ContainerQueue`, `cache`/`cdn`/`load_balancer`→a labelled `Container`.

## Step 2 — Assemble the document (`doc/solution.tex`)
Copy `.prumo/templates/publish/solution.tex.template` to `doc/solution.tex` and
fill in the `% >>> PRUMO:... <<<` blocks. Mandatory structure, in this order:
1. **Requirements in plain language** — the problem and the functional requirements
   without jargon.
2. **Capacity and demand (NFR)** — EXPLAIN each scale number in plain
   language (what it means in the real world, where the calculation came from), **name
   the binder** (the binding constraint) and fill in the sizing table.
3. **Design decisions** — one subsection per big decision: which pressure it relieves,
   what the **rejected naive alternative** is, and the trade-off.
4. **Figures** — use the macro `\prumofig{file}{caption}{explanation}`: first the
   context view, then containers, then the zooms, then the sequences,
   then the scenarios. **Each figure followed by prose that reads it.**

## Step 3 — Document gate (red) — `G-DOC-LEGIBLE` + `G-DOC-PEDAGOGIC` (ADV)
Delegate to a clean-context sub-agent (which sees only `doc/`): it checks
- **legibility**: there is a context view; no figure has more than ~10 boxes;
  there is a sequence for each main flow;
- **pedagogy**: the capacity NFRs are explained in plain language with the
  binder named; each decision has a rejected alternative; no figure is an orphan.
RED → fix it (break the dense figure into a zoom; add the missing text) and re-run.

## Step 4 — Generate the PDF (Docker)
Run, from the project root:
```
bash .prumo/templates/publish/render.sh doc
```
It builds the image (`templates/publish/Dockerfile`: LaTeX + PlantUML + Graphviz +
librsvg) and runs the pipeline `.puml → SVG → PDF (vector) → solution.pdf`. If the
LaTeX build fails, read the `latexmk` log, fix the `.tex` and re-run. If there is no
Docker, report the command for the user to run.

## Output
Announce the path of `doc/solution.pdf` and list the generated figures. End of the Prumo
flow: `init → requirements → design → evaluate → publish`.
