# Prumo — an agentic framework for system design

*Prumo* is Portuguese for **plumb line**: the weighted string that checks whether
something is aligned against a true reference. Here the reference is what the
system has to satisfy; the **gates** check whether the design is "plumb".

Prumo is the sibling of [`catraca`](https://github.com/cmarcond/catraca) (spec-driven TDD):
the same philosophy (text artifacts that guide an agent; the agent executes),
applied to system design. It is a layer of Markdown/YAML files (gates, skills,
commands, schemas) installed into `.prumo/`; the host agent executes. The gates
and skills were distilled from a real corpus of system-design interviews; see
`docs/method-patterns.md` and `docs/catraca-study.md`.

## The idea in one sentence
Instead of letting the agent spit out a zero-shot design (which tends toward the
"neutral baseline"), the agent designs in **versions** (v1 → v2 → …), with
**design-reasoning gates** failing each version until it is green: the same
red → green → refactor loop as catraca, only applied to the design. A **ratchet**
(*catraca*, in Portuguese) locks in the best result.

## The pieces
| Piece | File | Role |
|---|---|---|
| Constitution | `MANIFESTO.md` | principles that are not negotiable |
| Problem Gates | `gates/questions.md` | what the **owner** decides (scope, scale, guarantees, cost) |
| Design Gates | `gates/gates.md` | what **fails** a design (DET lints + ADV verifiers) |
| Skills | `skills/` + `index.yaml` | **how** to design well (each skill repairs the gate it backs) |
| Commands | `commands/` | `init` → `requirements` → `design` → `evaluate` → `publish` |
| Memory | `templates/ratchet.json` | a quality floor that only goes up |
| Schemas | `templates/schemas/` | the format of requirements / design / scores |

## Layout in the project — framework vs. results
The installer creates `.prumo/` in the target project. The separation is:

- **`.prumo/` = framework/method** (MANIFESTO, `gates/`, `skills/`, `templates/`,
  `commands/`, `docs/`). Shared across projects; it changes only **deliberately**,
  when a new gate/skill is promoted. That change belongs to the *method* and goes
  back to this repo (`prumo`); it is not a by-product of a problem.
- **Project root = results** of the problem, written by the commands:
  `questions.md` (the answered Problem Gates), `intent.json`, `requirements.json`,
  `requirements-critique.md`, `design/v1..vN/` + `design/v_final`, `evaluation/`,
  `ratchet.json`.

```
project/
├── questions.md            # Problem Gate answers (result)
├── intent.json             # result
├── requirements.json       # result
├── requirements-critique.md
├── design/ v1.. v_final/   # result
├── evaluation/             # result
├── ratchet.json            # result (quality floor)
└── .prumo/                 # FRAMEWORK (method): gates, skills, templates, …
```

The template `.prumo/gates/questions.md` stays **blank**; `init` reads it and writes
the answers to `./questions.md`. References to `gates/…`, `skills/…`, `templates/…`
in the commands mean `.prumo/…`, for **reading**.

## Flow
1. `/prumo.init` — Problem Gates (the agent **suggests**, the owner confirms) → a
   **thin** `intent.json` (problem + the owner's scope + qualitative context; no
   derived list).
2. `/prumo.requirements` — **expands** the thin intent into rich requirements
   (implicit functional requirements, relationships, invariants, NFRs derived from
   the workload, numbers), with the completeness gate `G-REQ-COMPLETENESS`.
   Deriving well is a skill, not an input.
3. `/prumo.design` — the versioned loop: v1 → gate critique (red) → refine (green) →
   simplify (refactor) → mutation (proves the gates).
4. `/prumo.evaluate` — rubric + clean-context audit + ratchet. In benchmark mode,
   it compares against the instructor's ground truth (the meta-gate).
5. `/prumo.publish` — a teaching document for the solution: it decomposes
   `design/v_final` into C4 figures (context→container→component) + sequences +
   scenarios, assembles a LaTeX document and generates `doc/solution.pdf` in a
   Docker container (LaTeX+PlantUML). Gates `G-DOC-LEGIBLE` / `G-DOC-PEDAGOGIC`.

> The benchmark feeds the agent **only the thin intent** (or a generic prompt),
> never the finished requirements. Deriving the requirements is part of what is
> measured.

**Auxiliary entry point.** `/prumo.reverse` goes the other way: it starts from an
**existing project** (a path) and reconstructs the *seed* (problem statement +
Problem Gates) that, given to `/prumo.init`, would regenerate that design. Validate
it by round-trip: run the seed through the flow and compare the `design.json` with
the project's real components.

## Installation
```
python3 install.py /path/to/target-project
```
Idempotent; creates `.prumo/` in the target + `/prumo.*` shortcuts in
`.claude/commands/prumo/`.

## Status
v0, distilled from a pilot of 10 videos. Blind reproduction of held-out problems
(intent + skills + gates) rises from ~0.63 (zero-shot) to ~0.75 (versioned with
gates). The DET gates still depend on annotations in `design.json`; the
loop-until-green is currently a command script, not an automated runner. Next:
automate the loop, thicken the gates/skills with the full corpus (82 videos),
triangulate the evaluation.

## License

MIT. See [LICENSE](LICENSE).
