# /prumo.init — Problem Gates → intent + requirements skeleton

Initialization script. Precondition: `.prumo/` installed. Outputs (in the **project
root**): a filled-in `questions.md`, `intent.json`, `requirements.json` (skeleton).

> **Path convention — framework vs. results.** `.prumo/` holds the
> **framework/method** (MANIFESTO, `gates/`, `skills/`, `templates/`, `docs/`),
> shared across projects: it changes only **deliberately**, when a new gate/skill
> is promoted (a change to the *method*, which goes back to the Prumo repo) — never
> as a by-product of a problem. The **results** of this problem go in the **project
> root**: `questions.md`, `intent.json`, `requirements.json`,
> `requirements-critique.md`, `design/`, `evaluation/`, `ratchet.json`. The answers
> to the Problem Gates are written in `./questions.md` (root), **not** in the template
> `.prumo/gates/questions.md` (which stays blank). References to `gates/…`, `skills/…`,
> `templates/…` for **reading** mean `.prumo/…`.

## Step 0 — Mode and constitution
- Guided mode (default) or automatic mode (if the user asks for it).
- Re-read `manifesto.md` (the principles already hold — do not ask whether the user
  "wants to find the bottleneck": that is constitution) and `gates/gates.md` (the
  Design Gates that will govern the design).

## Step 0.5 — Reading of the problem (so that you can SUGGEST)
Before asking anything, do a quick architect's reading of the problem (even if the
prompt is generic, e.g. "design a social graph"): what the likely usage pattern is,
what dominates (reads? writes? fan-out?), which guarantees the domain really demands,
a plausible order of magnitude. This reading is the basis for the gate **proposals** —
the user does not need to arrive knowing scale or consistency.

## Step 1 — Problem Gates (A→E): suggest, do not interrogate
The user may be **generic**. Read the questions from the **template**
`.prumo/gates/questions.md` (blank — do NOT edit it) and write the answers to
`./questions.md` in the **root**. For EACH gate, the agent **proposes** an answer
derived from Step 0.5, with one line of justification, and asks only for confirmation —
it never leaves the question open for the user to fill in from scratch. Rules:
- **Guided**: one gate at a time. Present the proposal ("I suggest read-heavy ~100:1
  because searches/views ≫ new connections; ok?"). The user confirms, adjusts
  or asks for alternatives. Record it with origin `proposed` (confirmed) or `user`
  (if the user changed it) or `prompt` (if the user had already fixed it in the prompt).
- **Automatic**: record the proposal itself as the answer, marked
  `[assumed YYYY-MM-DD]`, and go on.
- What the user fixed in the prompt is a proposal to confirm (origin `prompt`), not a
  question. What the user did NOT fix, you propose — you do not ask it as an open question.

## Step 2 — `intent.json` (the seed, **thin**, no solution)
From Gate A: `problem`, `goal`, **high-level** `scope_in[]` / `scope_out[]` **(what the
OWNER decides to include/exclude)**, `context_assumptions[]` (qualitative).
**Keep it thin**: the intent does NOT carry the detailed functional list, nor invariants,
nor numbers — that is **derivation**, and it is born in the `/prumo.requirements` phase
(putting it here leaks the work that will be tested). Two barriers:
- **intent/solution**: the intent does not name a component/technology/pattern;
- **intent/derivation**: the intent does not enumerate derived requirements (relationships,
  edge cases, invariants, metrics) — only the scope the owner fixes.
Run an adversarial review (clean context) that hunts for leakage of solution **and** of
derivation before accepting it. Schema: `templates/schemas/intent.schema.json`.

## Step 3 — Wrap-up
- Confirm consistency (problem × the owner's scope × the gate answers).
- Next phase: **`/prumo.requirements`** (expands the thin intent into rich requirements,
  with the completeness gate), and only then `/prumo.design`.
