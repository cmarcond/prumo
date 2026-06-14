# model-invariants-in-data

Encode domain invariants and scale behavior in the DATA MODEL, so the storage layer enforces them, instead of relying on application code to do the right thing on every path.

## When To Use

- A value has an exact-arithmetic requirement (e.g. money) where rounding error is unacceptable.
- A counter, quota, or balance must respect a bound (≥ 0, ≤ capacity) under concurrent writers.
- You need to detect whether something is stale, recent, or expired — not just on/off.
- State is replicated to many consumers and the volume of full-state pushes is becoming the bottleneck.
- A correctness rule currently lives only in a check scattered across handlers and can be bypassed by a new code path.

## When Not To Use

- The data is genuinely a transient cache where loss/skew has no correctness consequence.
- A boolean flag is the actual domain fact (e.g. a feature toggle) with no staleness dimension.
- Single-writer, low-volume contexts where a race is structurally impossible and full state is cheap — added machinery is dead weight.
- The invariant depends on external systems the store cannot see; enforce at the boundary instead.

## Preconditions

- The storage engine supports the primitive you need: exact numeric types, atomic conditional updates / CAS, unique or check constraints, server-assigned timestamps.
- You can name the invariant as a single predicate over stored values (the thing that must always be true).
- You know the read pattern (who consumes the state, how often, how large) before choosing delta vs. full state.

## Order Of Operations

1. State the invariant as a predicate over data, separate from any code that maintains it. PRINCIPLE = "remaining ≥ 0"; MATERIALIZATION = the column type + constraint + atomic update that makes it hold.
2. Choose the exact representation. Money and any exact quantity: integer minor units, decimal, or string — never a float. Pick the type before writing logic against it.
3. Put the bound on the data, not the caller. Express the constraint as a check constraint, a conditional/atomic update (decrement-if-remaining>0), or by oversetting capacity rather than permitting a negative — so a race cannot violate it.
4. For "is it current?" questions, store a timestamp (last_seen / last_heartbeat / updated_at) and derive freshness at read time, instead of a boolean that loses the staleness dimension.
5. At scale, propagate DELTAS (the change) rather than re-broadcasting constant full state. Replay/fold deltas to reconstruct.
6. For large payloads, push an id + version and let consumers refetch, instead of routing the payload itself through the broker.
7. Verify the invariant holds under concurrency, not just in a single-threaded path.

## Test Checklist

- [ ] Exact-value fields use an exact type; assert no float appears anywhere in the value's lifecycle (storage, transport, arithmetic).
- [ ] Bounded counter: concurrent writers driving it past the bound is rejected at the data layer (the over-decrement fails / over-increment is capped), proven with a parallel test.
- [ ] Staleness: a consumer can distinguish fresh from stale purely from stored timestamps; advancing a clock flips the derived state with no extra write.
- [ ] Delta stream: applying the deltas in order reconstructs the same state as a full snapshot; an out-of-order or missing delta is detectable.
- [ ] Large-payload path carries an id/version, not the payload; consumer refetch resolves to the correct version.
- [ ] The invariant predicate is enforced even when exercised through a path that bypasses the normal application code.

## Anti-Patterns

- Money (or any exact quantity) stored or computed as a float — accumulates rounding error and fails equality.
- A counter that can go negative under concurrency because the guard is an application-level read-then-write with no atomic/conditional update.
- A plain boolean where a timestamp is needed — it answers "is it set?" but throws away "how long ago?", killing staleness detection.
- Broadcasting constant full state (or heartbeats) to a large group when only the delta changed — bandwidth scales with group size for no new information.
- Routing large payloads through the broker so every hop pays the size, instead of passing an id and refetching on demand.
- Encoding the invariant only in hopeful application code, leaving the stored data able to represent an illegal state.

## Provenance

Synthesized from ~5 system-design walkthroughs. Backs gates:

- **G-INVARIANT-IN-DATA** — domain invariants (exact types, bounded counters, timestamp-over-boolean) are materialized in the data model and enforced by the store, not assumed by application code.
- **G-DELTA-NOT-STATE** — at scale, changes are propagated as deltas and large payloads are referenced by id + refetch, rather than broadcasting constant full state through the broker.
