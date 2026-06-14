# Enforce On The Server

Enforce security and correctness on the server, never in the client. The client can be replayed, inspected, and tampered with, so authorization, rate-limiting, filtering of sensitive data, and the choice of security-relevant identifiers (shard keys, random ids, timestamps) must be decided server-side.

## When To Use

- A request from an untrusted party (browser, mobile app, third-party API caller) drives an action with a security or correctness consequence.
- You are designing authorization checks, rate limits, quotas, or abuse controls.
- A response could include data the caller is not entitled to see, requiring filtering or projection.
- A security-relevant value is being assigned: shard key, partition key, random id/token, timestamp, sequence number, or pricing/amount.
- An idempotency key, dedup key, or correlation id originates outside your trust boundary.

## When Not To Use

- The "client" is a trusted internal service inside your security boundary that you authenticate and control.
- The value is purely cosmetic or local (UI state, display formatting, optimistic rendering) with no server-side effect.
- Client-side checks are added only as a UX hint and the same check is also enforced server-side (defense in depth, not the source of truth).

## Preconditions

- A defined trust boundary: it is explicit which callers are untrusted.
- An authenticated principal on the server for each privileged request; identity is derived server-side from the session/token, not read from a client-supplied field.
- A server-side store or service capable of holding the authoritative state (counters for rate limits, id generator, clock).

## Order Of Operations

1. Authenticate the principal on the server from the session/token; never trust a client-supplied identity field.
2. Authorize the specific action against that principal before doing any work.
3. Apply rate limits and quotas against server-held counters keyed by the server-derived identity.
4. Generate security-relevant values server-side: random ids/tokens from a secure source, timestamps from the server clock, shard/partition keys by server policy.
5. Execute the operation, then filter the response server-side so only data the principal is entitled to leaves the boundary.
6. For idempotency from external parties, derive or namespace the key server-side rather than trusting the raw client value.

## Test Checklist

- Replaying an identical request does not bypass the rate limit (counter is server-side).
- A tampered or forged client identity field does not change who is authorized or counted.
- A response never contains fields the caller lacks entitlement for, even when the client requests them.
- A client cannot dictate the shard/partition key, random id, or timestamp used for a write.
- Two external callers supplying the same idempotency key cannot collide or overwrite each other's results.
- Removing or modifying client-side validation has no effect on enforced outcomes.

## Anti-Patterns

- Client-side rate limiting: the client can be replayed or modified, so the limit is not enforced.
- Filtering private or sensitive data in the browser: the unfiltered payload already crossed the boundary.
- Letting the client pick a shard/partition key, random id, or timestamp: spoofable and a hot-shard / DDoS vector.
- Trusting a client-supplied idempotency key from an external party: collisions and overwrites become attacker-controlled.
- Deriving identity, authorization, or pricing from a request body field instead of the authenticated principal.

## Provenance

Frequency 22/82. Backs gate G-NO-CLIENT-TRUST.
