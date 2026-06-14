# Design For Partial Failure

Treat partial failure as the primary input to the design, not an afterthought.
Enumerate failure scenarios first, locate exactly where each failure can occur,
and make every retriable side effect idempotent and reversible. Combines
failure-driven ordering with persist-before-call idempotency.

## When To Use

- A request crosses a boundary you do not control: network call, external
  provider, separate service, queue, or process that can crash mid-step.
- An operation has a side effect that costs something if duplicated or left
  half-done (a charge, a dispense, an email, a state mutation).
- Multiple steps must happen in sequence and any step can fail independently.
- Clients or infrastructure may retry, and you cannot assume the happy path.

## When Not To Use

- A pure, read-only, or trivially repeatable operation with no side effect
  (running it twice is indistinguishable from running it once).
- A self-contained local computation with no boundary crossing.
- The cost of a duplicated or partial action is genuinely zero.

## Preconditions

- You can enumerate the discrete steps and the boundaries between them.
- You have (or can introduce) durable storage for pending state and retry keys.
  Volatile cache does not count as durable.
- For each retriable call you can attach a stable identifier the callee can
  deduplicate on.
- For each irreversible action you can identify whether a reserve/undo form
  exists (authorize vs. commit, reserve vs. consume).

## Order Of Operations

The procedure has two layers. Keep the PRINCIPLE separate from any specific
MATERIALIZATION.

### 1. Enumerate failure scenarios first

- Before drawing the solution, list the ways each step can fail.
- For every boundary crossing, distinguish WHERE the failure lands:
  - request lost (the callee never acted) — a retry is safe;
  - response lost (the callee may have acted, but you did not hear back) — a
    naive retry may duplicate the side effect.
- This distinction decides whether a retry is safe and whether idempotency is
  mandatory.

### 2. Order steps by least-bad failure mode

- When steps can be sequenced more than one way, compare the failure mode of
  each ordering and pick the one whose worst outcome is least harmful.
- PRINCIPLE: prefer leaving a recoverable/refundable state over an
  unrecoverable one; prefer "did nothing" over "did half".
- MATERIALIZATION (one-word neutral example, *dispensing*): reserve, then
  perform the irreversible action, then commit — so a crash leaves a reservation
  to release rather than a committed action with nothing delivered.

### 3. Persist the retry identifier before the call (store-then-call)

- PRINCIPLE: write the retry key / pending record to durable storage BEFORE
  issuing the retriable or external call. On retry, the key already exists, so
  the operation is recognized as a duplicate.
- Never issue the external call before persisting the key — a lost response
  then leaves you unable to tell whether the action happened.
- Store pending state durably, never only in a volatile cache.

### 4. Reuse identifiers across boundaries

- Thread the same identifier through each stage of a multi-step operation so
  later stages can correlate with, and deduplicate against, earlier ones.

### 5. Reserve, do not commit, when an action may be undone

- PRINCIPLE: if a later step can fail, take a reversible hold first (authorize /
  reserve) and only finalize (commit / consume) once dependent steps succeed.
- Do not perform an irreversible commit before the step that depends on it
  has succeeded.

## Test Checklist

- [ ] Failure scenarios were listed before the design was fixed.
- [ ] For each boundary crossing, request-lost vs. response-lost is identified.
- [ ] Every retriable side-effecting call is idempotent (duplicate request with
      the same key produces no extra effect).
- [ ] The retry key is persisted to durable storage strictly before the call.
- [ ] Identifiers are reused across the steps of a multi-step operation.
- [ ] Step ordering was chosen by comparing failure modes, not the happy path.
- [ ] Irreversible actions use reserve-then-commit; nothing irreversible is
      committed before its dependent step succeeds.
- [ ] No critical pending state lives only in a volatile cache.
- [ ] A crash between any two steps leaves a recoverable state.

## Anti-Patterns

- Non-idempotent retry on a side-effecting call: a lost response triggers a
  retry that duplicates the effect (e.g. a double commit).
- Issuing the external call before persisting the retry key.
- Committing an irreversible action before the dependent step succeeds
  (finalizing before delivering).
- Storing critical pending state in a volatile cache instead of durable storage.
- Assuming the happy path and bolting on error handling afterward.

## Provenance

Distilled from the method-pattern build-set: MP3 *failure-driven design* (3/8)
and MP4 *idempotency: persist-before-call* (3/8). Counts are the number of
build-set videos in which each pattern was observed. See
`meta/method-patterns/patterns.md`.
