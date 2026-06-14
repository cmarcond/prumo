# append-only-event-sourcing

Prefer append-only / event-sourced writes over in-place update/delete when you need auditability, point-in-time reconstruction, or you are on an LSM-tree store. Treat the event log as the source of truth; derive current state by folding events.

## When To Use

- You need an audit trail: every change must be attributable and replayable, not overwritten.
- You need point-in-time reconstruction: "what did state look like at time T" must be answerable.
- You are on an LSM-tree store (e.g. Cassandra, RocksDB, ScyllaDB) where in-place updates and deletes create tombstones that cause read-amplification.
- Concurrent writers benefit from append-only semantics (no read-modify-write contention on a shared row).

## When Not To Use

- Pure key-value cache or ephemeral state with no audit or history requirement.
- The store is a B-tree / page-oriented engine and in-place update cost is acceptable, and you never need history.
- Read latency on current state dominates and you cannot afford folding or maintaining a materialized snapshot.
- Strong cross-entity transactional invariants are required that an event log alone cannot enforce without added coordination.

## Preconditions

- Events are immutable and append-only once written; no in-place edits to past events.
- Each event carries a stable ordering key (sequence number, logical timestamp, or partition-local offset) sufficient to fold deterministically.
- The fold (reducer) is deterministic: same event sequence always yields the same state.
- Events are self-describing and versioned so the reducer can evolve without rewriting history.
- A retention / compaction policy exists so the log does not grow unbounded.

## Order Of Operations

Separate the principle (events are the truth) from the materialization (how current state is served).

1. Define the event schema and the ordering key. Decide partitioning so a single entity's events are co-located and ordered.
2. Write path: append a new event. Never update or delete prior events.
3. Read path (principle): reconstruct current state by folding the entity's events in order.
4. Materialization (optimization): maintain a snapshot/projection so reads do not re-fold the full log every time.
   - Build snapshots by replaying events, not by locking or full-scanning the live table.
   - Persist `(snapshot, last_event_offset)`; on read, fold only events after the snapshot offset.
   - Rebuild projections by replaying from the log; they are derived and disposable.
5. Compaction: collapse or archive events older than a checkpoint once a durable snapshot covers them, per the retention policy.

## Test Checklist

- Folding the full event sequence reproduces current state exactly.
- Point-in-time query: folding events up to T reproduces the historical state at T.
- Snapshot + tail-fold equals full-fold (snapshot correctness).
- Replacing a logical "delete" with a tombstone/end event still folds to the correct absent state.
- Reducer is deterministic across repeated runs and across reordering-tolerant inputs (idempotent replay).
- Schema evolution: an old event version and a new one fold correctly under the current reducer.
- Snapshot rebuild does not lock or full-scan the live table; it replays from the log.

## Anti-Patterns

- In-place update/delete on an LSM/Cassandra store: each mutation writes a tombstone, and reads must scan past accumulated tombstones (read-amplification) until compaction.
- Needing point-in-time or audit state but keeping only mutable current rows, so history is unrecoverable.
- Rebuilding a snapshot by locking or full-scanning the live table instead of replaying events.
- Treating a derived projection as the source of truth and mutating it directly.
- Mutating or back-dating past events to "fix" state instead of appending a corrective event.

## Provenance

Provenance 13/82. Backs gate G-APPEND-ONLY.
