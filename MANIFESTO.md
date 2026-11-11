# Prumo Manifesto — Constitutional Principles

> A *prumo* (Portuguese for **plumb line**) is the string that checks whether
> something is aligned against a true reference. Here the reference is what the
> system **has to** satisfy; the gates check whether the design is "plumb".
> These principles hold for **every** project that uses Prumo: they are not
> asked about, they do not depend on the prompt, and they are not negotiated
> per design. What the Problem Gates (the initial questions) calibrate is the
> **problem** (scope, scale, priorities), never whether the principles apply.
>
> The method is agnostic of domain and technology: the technology is a
> disposable example; the principle is what stays. Distilled from a real
> system-design corpus (see `docs/method-patterns.md`) and from the meta-method
> in `CORE_IDEA.md`.

## Principles

1. **Every design goes through the gates; a gate only counts once it has been
   seen to fail.** The design is checked against the reasoning gates
   (`gates/gates.md`). A gate is only installed after it has failed a provoked
   violation (mutation: inject the anti-pattern and watch the gate go RED).
   Configuring is not installing.
2. **Find the binding constraint before you draw, and design for it.**
   Bandwidth, CPU, storage, throughput, fan-out: compute the candidates and
   design for the one that actually limits. A number not computed is a decision
   not made.
3. **A requirement is intent; a skill is method; a gate is the floor.** The
   requirement says WHAT the system does and tolerates; the skill says HOW to
   design well; the gate fails whatever violates it. Do not mix them: an intent
   that names a component is leaking solution.
4. **Iterate from naive to optimal.** Every design names at least one rejected
   alternative together with the failure that brings it down. Red (a gate
   fails) → Green (refine until it passes) → Refactor (simplify while green).
   Versions: v1, v2, … until green.
5. **The artifact is the truth; the narration is context.** The diagram and the
   numbers win over the spoken explanation when they disagree.
6. **Do not pay for a guarantee the requirement does not demand.** Strong
   consistency, a live index, an exact count: if the problem tolerates less,
   the tolerance is a design lever, not a debt.
7. **Partial failure and idempotency first** on every path with a side effect
   or state: persist the key before the retriable call; order the steps so the
   irreversible action comes last; the least-bad failure wins.
8. **The ratchet only goes up.** The best score ever measured becomes the floor
   (`ratchet.json`); a regression is an explicit event (alert, block or
   repair), never silent decay.
9. **Automatic gates, not discipline.** Every check that can be run runs as a
   gate that fails: deterministic where possible (lints over the graph +
   arithmetic), adversarial (sub-agents that try to refute a requirement) where
   it is not.
10. **The owner decides the problem; the framework decides the design.** Scope,
    scale, the consistency-vs-availability priority, SLA and budget are the
    user's **Problem Gates**, recorded with their origin. Everything else the
    agent executes through the Design Gates until the next Problem Gate.

## The layers (they mirror CORE_IDEA)

| Layer | Artifact | Question |
|---|---|---|
| Constitution | `MANIFESTO.md` | What is never negotiated? |
| Knowledge | `skills/` | How is each thing designed well? |
| Decision | `gates/questions.md` | What is the owner's choice? (Problem Gates) |
| Verification | `gates/gates.md` | What fails a design? (Design Gates) |
| Execution | `commands/design.md` | What is the next verifiable version? (v1→vN) |
| Measurement | `commands/evaluate.md` | Was it done the right way? (rubric + clean audit) |
| Memory | `ratchet.json` | What has already been achieved? (quality floor) |
