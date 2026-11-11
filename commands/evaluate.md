# /prumo.evaluate — Rubric + clean-context audit + ratchet

Evaluates the final design of a problem. Precondition: `/prumo.design` has converged
(gates green). Outputs (in the **project root**): `evaluation/<slug>.md` +
an updated `ratchet.json`.

> **Paths:** `evaluation/` and `ratchet.json` go in the **root**; the framework
> (`gates/`, `skills/`, `templates/`) is read from `.prumo/`. Full convention in
> `/prumo.init`. Deliberate exception: promoting a gate/skill (Step 4) **edits** the
> framework in `.prumo/gates/gates.md` or `.prumo/skills/` — it is a change to the
> *method*, which must go back to the Prumo repo, not a result of the problem.

## Two modes
- **Benchmark** (the instructor's ground truth exists): compare `design/v_final` against
  the reference `requirements.json` + `design.json`, on the dimensions below. This is the
  **meta-gate** — it measures whether intent + skills + gates reproduce the instructor.
- **Standalone** (no ground truth): score by the gates alone (how many are green,
  how many needed how many iterations) + the clean audit. There is no "match", but there
  is "passed the gates and survived refutation".

## Step 1 — Rubric (with evidence per line)
Dimensions (0..1), per `templates/schemas/scores.schema.json`:
- `requirements_coverage` — functional + non-functional requirements covered.
- `estimation_fidelity` — numbers in the right order of magnitude / correct reasoning.
- `design_match` — semantic match of components/edges/decisions (benchmark)
  **or** coverage of the applicable gates (standalone).
- `criteria_coverage` — the method heuristics show up (bottleneck found, rejected
  naive alternative named, tolerance used as a lever…).
- `baseline_gap` — where the design diverges from the architect's neutral baseline (the
  non-obvious move). With no evidence, 0.

## Step 2 — Clean-context audit
Delegate to a subagent **with no access to whoever generated the design** (and, in the
benchmark, that did not see the ground truth while designing): re-run the DET gates (redo
the calculations), and **mutate the design** (inject an anti-pattern) to confirm that the
gate catches it. It reports findings; you either accept them (adjust the score) or refute
them with a justification. Record mutations applied × mutations that survived.

## Step 3 — Ratchet
Compare each score with `ratchet.json` (key = the problem's slug). Higher → the floor
rises. Lower than `floor - buffer` → regression:
- `warn` ⇒ an alert in the rubric;
- `block` ⇒ HALT, report to the user;
- `repair` ⇒ go back to `/prumo.design` with the REDs/differences as refinement items
  (a new version), re-evaluate once; recovered ⇒ carry on, otherwise ⇒ HALT.
Keep the progression of versions (v1→vN) and the floor per dimension.

## Step 4 — Wrap-up
Summarize: verdict, scores per dimension, gates that needed iteration, and (if
benchmark) the divergences from the instructor — each divergence is a candidate for a
**new gate** (`.prumo/gates/gates.md`) or a new skill (`.prumo/skills/`). A gap becomes
incorporated knowledge. Promoting is a change **to the method** (it goes back to the
Prumo repo), distinct from the results in the root; do it deliberately, not silently.
