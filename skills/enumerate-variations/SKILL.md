# Enumerate Variations

Many problems have **distinct regimes** that call for distinct architectures (e.g.
fixed vs sliding deadline; strong vs eventual consistency; read-heavy vs
write-heavy regime). The instructor almost always **enumerates the variations** and draws
the relevant ones, instead of committing to a single one. This skill brings that reflex;
it closes gap no. 2 of the 15 runs ("made one design, did not enumerate the variations").

## When To Use
- At the start of the design, to name the problem's axes of variation.
- Whenever the problem has 2+ regimes that change the architecture.

## When Not To Use
- A genuinely single-regime problem (record that you checked and there is no variation).

## Preconditions
- Intent + requirements (the axes come out of the requirements: consistency, deadline, scale, access pattern).

## Order Of Operations
1. Name the problem's **axes of variation** (strong×eventual consistency, fixed×dynamic, exact×approximate, continuous×intermittent).
2. For each relevant axis, **draw the distinct variation** (or justify collapsing into a single one because the others do not change the architecture).
3. Record the naive→chosen progression with the **named failure** of the rejected alternative (complements G-NAIVE-FIRST).
4. Make explicit which variation is the main path and why.

## Test Checklist
- [ ] The problem's axes of variation are named.
- [ ] Each axis with architectural impact has its variation drawn or a recorded reason for collapsing it.
- [ ] There is ≥1 rejected alternative with its failure named.

## Anti-Patterns
- Committing to one architecture without exposing the axes of variation.
- Presenting a single design where the problem clearly has 2+ regimes (e.g. real-time only when there are continuous watchers).

## Provenance
Derived from the 15 runs: partials/misses were concentrated in "built one design, the
instructor explored variations". Backs gate **G-ENUMERATE-VARIATIONS** (complements G-NAIVE-FIRST).
