# Choose Datastore And Index By Access Pattern

Select the datastore and its index from the read:write ratio and the shape of the query, then pick the **simplest technology that fits** the access pattern and justify it explicitly against the fancier specialized alternative.

## When To Use

- You are choosing persistence for a new component or service.
- You can estimate (even roughly) the read:write ratio and the dominant query shapes (point lookup, range scan, geospatial/nearest-neighbor, full-text, aggregation over time, etc.).
- Multiple storage technologies could "work," and you need a defensible choice.
- A default datastore or index is in place but no one has checked it against the actual queries.

## When Not To Use

- The access pattern is genuinely unknown and unbounded; defer the choice (prototype, instrument, then return) rather than guessing.
- The storage decision is dictated by a hard external constraint (regulatory, existing platform mandate, single-vendor environment) that removes real choice.
- The dataset is trivially small and short-lived, where any store fits and the analysis cost outweighs the benefit.

## Preconditions

- An estimate of read:write ratio for the data in question.
- An enumeration of the query shapes the data must serve, including the most demanding one (the query that, if unsupported, breaks the design).
- A rough volume / growth estimate (so write-heavy + high-volume regimes are visible).
- A short list of candidate technologies, including at least one "simple/general" option and one "fancy/specialized" option to justify against.

## Order Of Operations

1. **State the access pattern.** Write down the read:write ratio and the set of query shapes. Mark the single most demanding query.
2. **Match the index to the query shape.** Choose the index structure that natively serves the demanding query, not the default one.
   - Point/range queries on a sortable key → a balanced-tree index (*example: B-tree*).
   - Multi-dimensional / nearest-neighbor / geospatial queries → a spatial index (*examples: quad-tree, R-tree*). A default sortable-key index does **not** serve k-nearest in 2D.
   - Full-text / relevance ranking → an inverted index (*example: a search engine*).
3. **Match the engine to the read:write ratio and volume.**
   - Balanced read/write → a read-optimized engine with a tree index (*example: B-tree-backed store*).
   - Strongly write-heavy (e.g. on the order of 1:100 read:write) → a write-optimized engine (*example: LSM-tree-backed store*).
   - Read-heavy and rarely written → a relational store with leader/follower replication.
   - Very high write volume at large scale → a horizontally scalable NoSQL store.
   - Continuous events needing low-latency processing → a stream processor.
   - Time-stamped metrics with time-range aggregation → a time-series store.
   - Frequently changing, user-configurable logic → a rules engine rather than hardcoding.
4. **Pick the simplest technology that satisfies steps 2 and 3.** Prefer a general-purpose store with the right index over a dedicated specialized system when the general one meets the requirement. (*Example: a relational store with a spatial index can outperform and outsimplify a separate search-engine deployment for geo queries.*)
5. **Justify against the fancier option.** Explicitly name the specialized alternative you did not pick and state why the simpler choice is sufficient (lower operational cost, fewer moving parts, adequate performance at the projected scale). If the fancier option wins, the same justification proves it.
6. **Record the assumption that anchors the choice.** Note which ratio/volume/query-shape value the decision depends on, so the choice can be revisited if that value moves.

## Test Checklist

- [ ] The read:write ratio and the demanding query shape are written down, not implied.
- [ ] The chosen index natively serves the demanding query (no full scans or post-filtering for the hot path).
- [ ] The engine choice corresponds to the stated ratio/volume regime.
- [ ] The simpler-vs-fancier comparison is explicit: the rejected specialized option is named with a reason.
- [ ] No default index/DB was carried over without checking it against the access pattern.
- [ ] The decision cites the specific assumption it rests on and what would invalidate it.

## Anti-Patterns

- Using a default index or default database without matching it to the actual access pattern (e.g. keeping a sortable-key index for a nearest-neighbor query).
- Reaching for the fancier specialized system when a simpler general-purpose store with the right index fits the access pattern.
- Choosing the engine from familiarity or hype rather than from the read:write ratio and volume regime.
- Hardcoding logic that the requirements say will change often, instead of using a configurable engine.
- Declaring a choice without justifying it against the alternative, leaving the trade-off invisible.

## Provenance

MP1 — observed in 5 of 8 build-set videos.
