# Scope, Defer, And Black-Box Sub-Problems

Control scope deliberately: when a sub-problem is **self-contained** (its internals do not affect the rest of the design), name it as a black-box component and move on instead of rabbit-holing. When a sub-problem is the **core/interesting machinery** of the design, build it from scratch first to show how it works, **then** collapse it into a managed black-box equivalent to make the contrast explicit — do not reach for the managed black box at the very start.

PRINCIPLE: scope is a resource. Spend depth on the part that teaches or differentiates the design; spend a label on the part that is solved and decoupled.

## When To Use

- A design contains a sub-problem you could either expand or treat as a single named box.
- A sub-problem is **self-contained**: it has a clear interface, its internals do not change decisions elsewhere, and it has a known standard solution. (Defer it.)
- A sub-problem is the **core mechanic** the design exists to demonstrate or get right. (Build it first, then collapse it.)
- A managed/off-the-shelf service exists that could absorb a component, and you must decide whether and when to introduce it.

## When Not To Use

- Every sub-problem is genuinely central and small; there is nothing to defer and nothing routine to black-box.
- The "black box" hides a decision that actually drives the rest of the design (its interface, failure mode, or guarantees leak into other components) — it must be opened, not deferred.
- The audience/goal is purely an integration: the managed service is the deliverable and there is no core machinery worth building from scratch to contrast against.

## Preconditions

- An enumeration of the design's sub-problems.
- For each, a classification: **self-contained** (deferrable) vs **core** (build-first).
- For self-contained ones: a name for the box and its interface (inputs, outputs, guarantees) — enough to integrate without specifying internals.
- For core ones: knowledge of the from-scratch mechanism AND awareness of the managed equivalent it can collapse into.

## Order Of Operations

1. **Inventory the sub-problems.** List the distinct pieces the design must handle.
2. **Classify each piece.** Mark it *self-contained* (clear interface, internals don't affect other decisions, known standard answer) or *core* (the machinery the design is about, or whose internals change other decisions).
3. **Defer the self-contained pieces.** Give each a named black-box component and a minimal interface; explicitly state "this is its own problem, out of scope here" and integrate via the interface. Do not expand its internals. (*Example: id-generation.*)
4. **Build the core pieces from scratch first.** Show the explicit mechanism — the components, data flow, and why it works — before introducing any managed shortcut. This is where depth is spent.
5. **Then collapse the core into a managed equivalent.** After the from-scratch version is understood, show the managed/off-the-shelf service that does the same job, and state the contrast: what it abstracts away, what you trade for it (control, visibility, lock-in, cost) versus what you gain (operational simplicity, less code to own).
6. **Re-check the boxes for leaks.** Confirm each black box's interface and failure behavior do not silently dictate decisions elsewhere; if one does, reopen and treat it as core.

## Test Checklist

- [ ] Every sub-problem is classified as self-contained (deferred) or core (built first).
- [ ] Each deferred piece is a named box with a stated interface, explicitly marked out of scope — not expanded.
- [ ] No deferred box hides a decision that actually drives other components.
- [ ] The core machinery is shown from scratch before any managed service is introduced.
- [ ] The from-scratch-then-collapse contrast is explicit: what the managed box abstracts and the trade-off it carries.
- [ ] No managed black box was reached for at the very start in place of the part worth understanding.
- [ ] No time was sunk rabbit-holing a self-contained sub-problem that could have been a box.

## Anti-Patterns

- Reaching for a managed black box at the start of a design, skipping the from-scratch mechanism that is the part worth understanding.
- Rabbit-holing into a self-contained sub-problem (expanding its internals in depth) instead of naming it and deferring it.
- Black-boxing a piece whose interface, guarantees, or failure mode actually leak into and dictate the rest of the design.
- Collapsing the core into a managed service without stating the trade-off, so the contrast and what was abstracted away stay invisible.
- Treating scope as unlimited: expanding every sub-problem equally instead of spending depth on the differentiating one.

## Provenance

MP9 — observed in 4 of 8 build-set videos.
