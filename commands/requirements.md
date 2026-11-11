# /prumo.requirements — Expand the thin intent into rich requirements (gated)

The phase that was missing. `init` produces a **thin intent** (problem + the owner's
scope + qualitative context). Here the agent **derives** the rich requirements — and
deriving well is a skill under test, not a given input. Precondition: `intent.json`.
Output (in the **project root**): `requirements.json` (rich) + `requirements-critique.md`.

> **Paths:** results go in the **root**; the framework (`gates/`, `skills/`,
> `templates/`) is read from `.prumo/`. Full convention in `/prumo.init`.

> Golden rule (anti-leakage): `intent.json` does NOT contain the detailed functional
> list or the numbers — if it does, that is leakage of the derivation. This phase is
> where the list is born.

## Step 1 — Derive (skill `elicit-requirements-from-intent`)
From the thin intent, derive:
- **Functional requirements**: walk through the entities, actions, **relationships** and
  **edge cases** that the domain implies — including the non-obvious ones (e.g.
  distinguishing types of relationship; lifecycle/deletion; what happens on a
  conflict/duplicate).
- **Invariants**: uniqueness, monotonicity (upgrade-only), ordering,
  idempotency — what the domain requires never to be violated.
- **Non-functional requirements**: derive them from the **shape of the workload**
  (read:write → consistency/latency; fan-out → amplification; volume → durability) —
  each NFR tied to its why.
- **Scale**: do the back-of-the-envelope calculation (skill `find-the-binding-constraint`):
  the numbers the owner fixed + the ones you estimate, with the calculation.
Write `requirements.json` per `templates/schemas/requirements.schema.json`.

## Step 2 — Completeness gate (`G-REQ-COMPLETENESS`, ADV)
Run a clean-context critic that **enumerates the implicit surface** of the
problem (the expected entities/actions/relationships/invariants/NFRs) and checks whether
the requirements cover it — and marks what is **missing** as RED. It does NOT draw a
solution; it only checks completeness and whether each NFR is anchored in the workload.
Write `requirements-critique.md`.

## Step 3 — Iterate until green
Address each RED (derive what was missing). Re-run the gate. Stop when complete.
Do not invent a requirement the domain does not ask for (over-spec is also a finding).

## Output
Announce `/prumo.design`. In automatic mode, go straight on. The design consumes THESE
requirements, not the intent.
