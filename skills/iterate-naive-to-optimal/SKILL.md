# Iterate From Naive To Optimal

Reach a design by starting from the obvious-but-flawed approach and refining one defect at a time, instead of presenting a finished solution as if it were inevitable. The reasoning *is* the deliverable: each step earns the next by naming the specific defect it removes.

## When To Use
- A design decision has more than one plausible approach and the choice is not obvious.
- You must justify *why* the chosen approach beats the alternatives, not just state it.
- Explaining or teaching a design, where the trade-offs are the point.
- A reviewer or audience would otherwise ask "why not the simpler thing?"

## When Not To Use
- The decision is forced (one viable option) or trivially constrained — skip straight to it.
- The alternatives differ only cosmetically, with no disqualifying defect distinguishing them.
- Cost of enumerating options exceeds the cost of just building and revising.

## Preconditions
- You can articulate a naive baseline a reasonable person would try first.
- For each candidate, you can name a concrete, checkable defect (or confirm it has none).
- You have at least one decisive criterion that separates the candidates.

## Order Of Operations

PRINCIPLE — the loop:
1. **State the naive approach.** The simplest thing that plausibly works. Do not strawman it; make it genuinely tempting.
2. **Expose its failure mode.** Name the *specific* defect — the input, scale, or condition under which it breaks. Be concrete enough to verify ("breaks at N concurrent X", not "doesn't scale").
3. **Introduce the refinement that fixes exactly that defect** — and ideally only that defect, so the causal link is clear.
4. **Repeat.** Treat the refinement as the new baseline; find *its* defect. Stop when the remaining approach has no disqualifying defect for the stated requirements.
5. **Select explicitly.** When multiple candidates survive or compete in parallel, lay them side by side as a decision matrix and pick by a *single decisive criterion* — the one dimension that dominates the choice. Name that criterion out loud.

Invariant: every transition is justified by the named defect of the prior step. No step appears without a reason rooted in the previous one's flaw.

MATERIALIZATION (examples, swap for your medium):
- Linear prose: "Naive: X. Problem: under <condition> it <fails>. Fix: Y, which removes that. But Y now <fails> when… → Z."
- Decision matrix: rows = candidates, columns = criteria; mark the disqualifying defect per row; bold the decisive column; state the winner and why that column decides.
- One-word neutral example of a candidate set to refine across: *lookup* (scan → index → partitioned index).

## Test Checklist
- [ ] A naive baseline is stated before any refined approach.
- [ ] Each step names a *specific*, checkable defect — not a vague "won't scale."
- [ ] Each refinement is traceable to the exact defect of the prior step.
- [ ] The iteration stops at an approach with no disqualifying defect (not arbitrarily).
- [ ] When candidates compete, they are shown side by side.
- [ ] Selection is made by a single, explicitly named decisive criterion.
- [ ] The final choice's surviving trade-offs are acknowledged, not hidden.

## Anti-Patterns
- **Jumping to the final solution** without showing the trade-off or why-not of the alternatives — the choice looks asserted, not earned.
- **Alternatives without a decisive criterion** — listing options side by side but never naming the one dimension that selects among them.
- **Strawman baseline** — a naive approach so weak nobody would propose it; the failure mode then teaches nothing.
- **Unmotivated step** — a refinement that fixes a defect never stated, or fixes several at once so the cause is unclear.
- **Endless iteration** — refining past the point where the approach already satisfies requirements.

## Provenance
MP10 ("naive-first-then-refine"), 4/8 build-set videos; additionally corroborated in 2 held-out videos.
