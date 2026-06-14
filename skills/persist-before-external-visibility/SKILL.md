# persist-before-external-visibility

Make an effect durable BEFORE you make it visible to others. Commit to the
durable store first; only then broadcast, fan-out, publish, or return a success
that implies durability.

## When To Use

- An effect (write, state change, value) will be observed by other actors —
  other users, other services, downstream consumers.
- A success response (200/ack) signals to the caller that the effect is durable.
- You are coupling a persist step with a notify/broadcast/enqueue step and a
  crash between them would drop or expose uncommitted state.
- Example domain: bid.

## When Not To Use

- The effect is local and never observed externally before the next durable
  write (no cross-actor visibility window).
- Best-effort, lossy-by-design signals (telemetry, metrics, hints) where loss is
  acceptable and no consumer treats them as durable.
- Read-only paths with no state change.

## Preconditions

- A durable store with a defined commit point (the write is acknowledged
  durable, not merely buffered).
- A clear definition of "visible": what other actors can observe and when.
- Identified crash window: the interval between persist and publish where a
  failure must not drop or expose data.

## Order Of Operations

PRINCIPLE (always):
1. Compute the effect.
2. Persist to the durable store and wait for the commit acknowledgement.
3. Only after commit: broadcast / fan-out / publish / return success.

Never reorder to "broadcast then persist" or "ack then persist". Never expose a
value to other actors before its commit point.

MATERIALIZATION (when persist and publish must be decoupled):
- Transactional outbox (example): write the business state and the
  outbound-event record in the SAME transaction. A separate relay reads
  committed outbox rows and publishes them. Persist and the intent-to-publish
  are atomic; the publish itself is at-least-once and idempotent downstream.
- Broker (example, only as a relay step): a broker may carry the event, but it
  is not the durable store. Pair it with a consumer that durably copies the data
  out; publishing from a broker with no durable consumer is not persistence.

## Test Checklist

- Kill the process AFTER persist but BEFORE publish: on restart the effect is
  recoverable and eventually published; nothing is silently lost.
- Kill the process BEFORE the commit point: no other actor ever observed the
  effect, and no success was returned implying durability.
- The success/ack response is never sent before the commit acknowledgement.
- Replays / at-least-once delivery are idempotent for downstream consumers.
- No path lets another actor read a value before its commit point.
- Outbox (if used): event row and business row commit or roll back together —
  never one without the other.

## Anti-Patterns

- Broadcasting or showing a value to other actors before it is committed.
- Writing to the store, THEN to a queue, so a crash between the two drops the
  event.
- Returning 200/ack that implies durability before the write lands.
- Publishing from a broker with no consumer that durably copies the data out.
- Treating a buffered/in-flight write as if it were committed.

## Provenance

Pattern observed across ~4 independent system-design sources. Backs gate
G-PERSIST-BEFORE-VISIBLE.
