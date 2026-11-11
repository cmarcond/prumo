# How Catraca works — a study for Prumo

A summary of the architecture of `catraca` (the spec-driven TDD/Clean
Architecture framework, this one's sibling) and what Prumo inherits, adapts or replaces.

## What catraca is
A stack of text artifacts installed into `.catraca/` in the target project. The
host agent executes; the framework **guides with text**. Installation is by an
idempotent `install.py` (create / skip identical / keep divergent as `.new`).

## Pieces
- **`MANIFESTO.md`** — the constitution: 11 principles that hold for every project and
  are not asked about (TDD red-green-refactor, dependencies point inward, libraries
  behind an adapter, errors at the edge, coverage is a gate, automatic gates not
  discipline…).
- **`skills/` + `index.yaml`** — 13 skills, each with When To Use / When Not /
  Preconditions / Order Of Operations / **Test Checklist** (where the acceptance
  criteria come from) / **Anti-Patterns** (what fails in the rubric).
- **`templates/questions.md`** — the **User Feedback Gates** (A product, B
  platform, C method, D evaluation, E per-feature). In guided mode the agent
  asks one gate at a time and records the answer; in automatic mode it records defaults
  with `[assumed]`. They calibrate the **rigor**, never the principles.
- **`commands/`** — the flow: `init` (gates → product/architecture/method),
  `plan` (roadmap + tasks), `implement` (red→green→refactor per behavior),
  `evaluate` (rubric + audit + ratchet), `status` (reconcile).
- **Quality pipeline (feature 000)** — before any product feature, it
  installs the automatic gates (lint, type-check, coverage) as hooks that
  reject commit/push. Each gate **seen to fail** a provoked violation.
- **`evaluate` + `ratchet.json`** — a rubric with evidence per line; a **clean-context
  audit** (a subagent that tries to knock scores down, re-running and
  **mutating** the code to see whether any test breaks); the ratchet in
  warn/block/**repair** mode (it appends tasks R1, R2… and re-evaluates).

## Catraca's deterministic ground
Catraca's "red" is **run and fail**: test, linter, coverage, mutation.
All of it mechanically verifiable. That is what Prumo needs to recreate — and it is the
point where system design diverges.

## What Prumo inherits, adapts, replaces

| Catraca | Prumo (system design) |
|---|---|
| Constitution (`MANIFESTO`) | inherited, rewritten for design (see `MANIFESTO.md`) |
| Skills with Anti-Patterns | inherited — the design-method skills in `skills/` (listed in `skills/index.yaml`) |
| User Feedback Gates (questions) | **Problem Gates** (`gates/questions.md`): scope, scale, consistency×availability, SLA, budget |
| Pipeline of automatic gates (lint/coverage) | **Design Gates** (`gates/gates.md`): lints over the graph + arithmetic (DET) and adversarial verifiers (ADV) |
| red→green→refactor of code | red→green→refactor of the **design**: v1→v2→…, a gate fails → refine → simplify |
| Mutation of the code (testing the test) | Mutation of the **design** (inject an anti-pattern, confirm the gate goes RED) — the analogue of chaos engineering |
| Clean-context audit | identical: scorer/critic with no access to the ground truth |
| Ratchet per feature | Ratchet per **design** (a floor per reproduction dimension) |
| `implement` executes TDD tasks | `design` runs the versioned design loop |

## The essential difference
Code is proven by **running it**; a design is proven by **structured inspection +
arithmetic + adversarial refutation**. That is why Prumo leans as much as it can on the
deterministic ground that exists (lints over the annotated `design.json` + capacity/
amplification calculations) and uses sub-agents only for what cannot be mechanized.
The **meta-gate** is blind reproduction against the instructor's ground truth: if intent +
skills + gates reproduce the instructor's design, the set works; where it diverges, a
gate or skill is missing (the gap becomes the next gate).
