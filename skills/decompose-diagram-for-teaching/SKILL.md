# Decompose The Diagram For Teaching

A single diagram with every component is illegible and does not teach. Break the
design into a **sequence of figures** that goes from the high level to the detail, plus
flows (sequences) and scenarios — each figure legible on its own, each with text
that reads it for the reader.

## When To Use
- The `/prumo.publish` phase: turning `design/v_final` into a teaching document.
- Whenever a `design.json` has more than ~8–10 components (a single diagram becomes a
  tangle).

## When Not To Use
- A trivial design (≤ ~6 nodes, 1 flow): one context figure + one containers figure
  are enough; do not invent empty zooms.

## Preconditions
- `design/v_final/design.json` (annotated components + edges) and
  `requirements.json` (numbers, invariants), `critique.md` (decisions/alternatives).
- The problem's axes of variation (from `/prumo.design`, skill `enumerate-variations`)
  — they define which zooms and scenarios are worth having.

## Order Of Operations
1. **Map the design onto the C4 levels.** Context (actors + the system as a black
   box) → Containers (the big blocks: services, stores, broker, cdn) →
   Components (a zoom inside a subsystem). The component's `type` becomes the C4
   macro: `service→Container`, `datastore→ContainerDb`, `broker→ContainerQueue`,
   `cache/cdn→Container` with a label.
2. **Cut along an axis of variation, not arbitrarily.** Each zoom (component) is a
   cohesive subsystem — typically the same axes the design separated
   (ingestion×serving, write×read, hot×cold). One zoom per relevant axis.
3. **Legibility ceiling: ~10 boxes per figure.** If a level goes past that,
   promote a subset to a zoom of its own. The containers figure shows the
   skeleton; the details live in the zooms.
4. **Flows become sequence diagrams.** One per main path (e.g. upload,
   watch). The sequence is where you see the **order** and the **asynchrony** (ack before
   the fan-out; persist before visible) — things the block diagram hides.
5. **Scenarios become figures of their own.** Partial failure, peak/viral (cold-start),
   concurrency (deletion during a read): one cut per scenario, showing only the
   components it exercises.
6. **Each figure gets prose.** Below each figure, read it for the reader: what to
   look at, why that block exists, which pressure it relieves. A figure without text
   does not teach.

## Test Checklist
- [ ] There is a context figure (high level) before any detail.
- [ ] No figure has more than ~10 boxes; the dense ones became zooms.
- [ ] Each axis of variation of the problem has its zoom (or was collapsed with a reason).
- [ ] Each main path has a sequence diagram showing order/asynchrony.
- [ ] Each failure/peak/concurrency scenario has its figure.
- [ ] Every figure is followed by prose that explains it (it is not left an orphan).

## Anti-Patterns
- **Tangle diagram**: a single board with everything, illegible, "technically complete".
- **Empty zoom**: splitting for the sake of splitting, producing figures that add nothing.
- **Orphan figure**: an image with no text that reads it — pretty and mute.
- **Missing sequence**: only blocks, never the temporal order — it hides the asynchrony
  and the ordering, which are half of the design.
- **Overflowing the page**: a figure too big for the paper; the fix is to decompose it,
  not to shrink the font until it is illegible.

## Provenance
The `/prumo.publish` feature: `design.json` is the source of truth, but a human
learns the solution through a progression of views (C4: context→container→component)
+ flows + scenarios, each view legible and narrated. It mirrors the principle "the
artifact is the truth; the narration is context" applied to communicating the solution.
