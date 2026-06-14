# Decouple With Async Propagation

Persist the change durably and acknowledge the caller immediately; do the
propagation, replication, or fan-out afterward, asynchronously, decoupled
through a durable queue or log. Decide push-vs-pull explicitly for every link,
and use a lightweight task runner as a generic adapter to turn a pull-only
source into a push.

## When To Use
- A write must be acknowledged fast, but its side effects (replicate to other
  stores, notify N consumers, refresh a derived index, fan out a message) are
  slower or numerous.
- Downstream consumers are many, slow, flaky, or scale independently of the
  write path.
- One link speaks pull (a source you can only poll) but the consumer wants
  push, or vice versa, and you need an adapter between them.

## When Not To Use
- The caller genuinely needs the side effect to be complete before it returns
  (a strong end-to-end invariant) — then the work is synchronous by definition;
  do not fake an ack.
- The side effect is cheap, single-target, and in the same transaction boundary
  as the write — a queue adds latency and operational cost for no decoupling.
- Volume is tiny and a single process handles write + propagate well within the
  latency budget; defer the broker until scale demands it.

## Preconditions
- The write is made **durable before** the ack — the ack is a promise the
  system can keep after a crash, not a fire-and-forget.
- The propagated effect is idempotent or deduplicated, since async delivery
  implies at-least-once retries and reordering.
- The broker between producer and consumers is itself durable and can apply
  back-pressure (persist/lag) rather than silently dropping under load.
- For each link in the chain you know whether it is push or pull, and the
  push/pull boundary is named.

## Order Of Operations
1. Split the operation into the **caller-facing write** and the **downstream
   effects**.
2. On the write path: persist durably, then return the ack. Nothing more on the
   critical path.
3. Hand the effect to a durable, decoupling broker (a queue or an append log) —
   not an in-memory buffer at scale.
4. Drive each downstream effect from the broker, asynchronously, with retries
   and idempotent handling.
5. Walk the chain link by link and mark each as push or pull explicitly.
6. Where a pull-only source meets a push-wanting consumer (or the reverse),
   insert a lightweight task runner as a thin adapter that polls one side and
   emits to the other. Keep it a pure transport shim — business logic lives in
   a service, not in the adapter.

## Test Checklist
- [ ] Caller gets its ack after the durable write, before any fan-out.
- [ ] A crash after ack and before propagation loses no committed effect (it
      replays from the durable store/broker).
- [ ] The broker survives a slow/dead consumer by buffering or lagging, never
      by dropping data.
- [ ] Redelivery / duplicate effects are absorbed idempotently.
- [ ] Every link is annotated push or pull; each push/pull mismatch has exactly
      one adapter.
- [ ] The adapter contains transport only — no business rules to test inside it.

## Anti-Patterns
- Synchronous fan-out: replicating to all replicas or notifying all consumers
  before returning the response, coupling caller latency to the slowest
  downstream.
- Using an in-memory queue at large scale: under back-pressure it drops data
  instead of persisting or lagging.
- Stuffing heavy business logic into the adapter / task runner instead of a
  service — the shim becomes a hidden, untestable service.
- Acknowledging before the write is durable (ack is a lie a crash exposes).
- Leaving push-vs-pull implicit, so a pull source quietly stalls a consumer
  expecting push.

## Provenance
MP7, 4/8 build-set videos.

---
PRINCIPLE: persist + ack now, propagate later through a durable decoupling
channel; make push-vs-pull explicit; bridge pull->push with a thin adapter.
MATERIALIZATION (examples only, not the rule): a log-based broker or a managed
message queue as the decoupling channel; a cron/worker task runner as the
pull->push adapter; read replicas or a derived index refreshed off the log.
