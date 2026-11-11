# /prumo.design — Versioned design loop (red → green → refactor)

The heart of Prumo. It produces the design in **versions**, with the Design Gates
failing between them, until green. Precondition: `intent.json` (from `/prumo.init`) +
a rich and complete `requirements.json` (from **`/prumo.requirements`**, already past
the G-REQ-COMPLETENESS gate). Outputs (in the **project root**):
`design/v1..vN/{requirements.json,design.json,design.mmd,critique.md}` and a
symbolic `design/v_final` pointing to the best version.

> **Paths:** `design/` goes in the **root**; the framework (`gates/`, `skills/`,
> `templates/`) is read from `.prumo/`. Full convention in `/prumo.init`.

## Principle
Never produce the final design in one go (zero-shot tends toward the "neutral
baseline" and loses the move that distinguishes a good design). Iterate naive →
optimal, as the `iterate-naive-to-optimal` skill requires.

## Step 0 — Axes of variation (skill `enumerate-variations`)
Before drawing, name the problem's **axes of variation** (strong×eventual
consistency, fixed×dynamic deadline, exact×approximate, continuous×intermittent access,
read-heavy×write-heavy regime). For each axis with architectural impact, decide:
draw the distinct variation, or collapse it with a justification. Gate `G-ENUMERATE-VARIATIONS`.

## Step 1 — v1 (first version)
Applying the skills (`skills/index.yaml`), produce:
- a complete `requirements.json` — **do the back-of-the-envelope calculation** (skill
  `find-the-binding-constraint`): estimate the bottleneck candidates and name the one
  that limits. Do not skip the calculation.
- `design.json` (components + edges, per `templates/schemas/design.schema.json`)
  and `design.mmd` (Mermaid built from the nodes/edges).

## Step 2 — Gate critique (red)
Run ALL the gates in `gates/gates.md` against the current version:
- **DET** (lints over the graph + arithmetic): compute concretely
  (post-fan-out amplification, summed capacity vs demand, skewed partition key,
  idempotency before an external call, blob kept off the app server…). Check
  against `design.json` (annotate `consistency`/`partition_key`/`payload`/`idempotent`
  on the elements to make the lint mechanical).
- **ADV** (adversarial verifiers): for each non-functional requirement, a
  sub-agent tries to **refute** that the design meets it (it finds the load/failure/sequence
  that breaks it). RED if the majority refute.
Write `critique.md` (gate | verdict RED/AMBER/GREEN | issue | fix + skill).

## Step 3 — vN+1 (green)
If there is any RED: refine the version, addressing **each** RED by applying the skill
that does the repair (the gate's "skill" column / `backs_gates` in the index). Changing
the architecture is allowed when a gate demands it (drop a redundant store, re-key a log,
swap the engine to fit the shape of the workload). Re-run Step 2.

## Step 4 — Convergence and refactor
Stop when all the gates are GREEN (or after K iterations with no new RED).
Then **refactor**: simplify (fewer components) while keeping everything green.

## Step 4b — Tech materialization (skill `materialize-tech-choices`)
With the structure stable, **name the concrete technology of each component**,
justified by the shape of the access (write-heavy+scans→LSM/Cassandra; read-heavy
point lookup→DynamoDB/B-tree; stream→Kafka; etc.), in `tech_choices`. No component
may be left as a generic abstraction. Non-obvious choices cite 1 rejected alternative.
Gate `G-MATERIALIZE-TECH`. Then mark the version as `v_final`.

## Step 5 — Mutation (prove the gates)
For the gates that are critical to the problem, inject the anti-pattern into `design.json`
(swap a strong store for an eventual one; a skewed partition key; remove the idempotency
persist) and confirm that the corresponding gate goes RED. A gate that does not catch the
mutation is not installed — record it.

## Output
Announce `/prumo.evaluate` (rubric + ratchet). In automatic mode, go straight on.
