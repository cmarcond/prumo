# Method Patterns — pattern library (full corpus: 82 videos)

Provenance = the number of videos in the corpus (out of 82) whose heuristics/anti-patterns/decisions
show the pattern (keyword bucketing over the per-video observation files, which are not part of
this repo; it is a floor, not exact). **Technique** patterns become a skill + gate; **style** patterns are
only recorded (they inform fidelity, they do not become a gate).

## Tier 1 — almost universal (>50/82)
| pattern | /82 | essence | skill / gate |
|---|---|---|---|
| async-propagate | **78** | persist+ack immediately, propagate async; decouple through a broker; explicit push-vs-pull; no synchronous fan-out before the ack | `decouple-with-async-propagation`, `persist-before-external-visibility` / G-ASYNC, G-PERSIST-BEFORE-VISIBLE |
| datastore-by-access | **72** | choose the DB/index by the read:write ratio and the shape of the query; the simplest technology that fits (B-tree/Dynamo read-heavy; LSM/Cassandra write-heavy) | `choose-datastore-by-access-pattern` / G-FREETEXT |
| staleness-lever | **63** | exploit what the problem tolerates (staleness/approximation) as the key move: batch, precompute, TTL | `exploit-tolerated-weakness` / G-LEVER |

## Tier 2 — strong (40–46/82)
| pattern | /82 | essence | skill / gate |
|---|---|---|---|
| partition/hot-partition | **46** | partition key without skew; avoid scatter-gather; read-heavy hotspot → replicas | `partition-keys-and-hot-partitions` / G-HOTPART |
| ml-method | **46** | ML method: approach derived from the requirement, two-stage (candidate→rank), persist the model, train/serve parity, the label comes from the action, normalize features, metric by cost of error, baseline before complexity | `ml-system-design` / G-TWO-STAGE-RANK, G-MODEL-PERSIST, **G-ML-FEATURE-ENG**, **G-COLD-START** |
| oltp-olap | **41** | take analytical reads/training off the operational store; analytics via CDC→warehouse; no dual writes | `separate-operational-from-analytical` / G-OLTP-OLAP, **G-NO-DUAL-WRITES** |
| idempotency/partial-failure | **41** | enumerate partial failures; persist the key before the call; order with the least-bad failure; the ladder let-it-fail→idempotent retry→2PC→consensus | `design-for-partial-failure` / G-IDEMPOTENT, G-UNIQUENESS, G-ORDERING |

## Tier 3 — recurring (30–36/82)
| pattern | /82 | essence | skill / gate |
|---|---|---|---|
| payload-off-path | **36** | blobs via object store/URL, never through the app servers | `keep-large-payloads-out-of-path` / G-PAYLOAD |
| naive-first | **34** | naive → expose the failure → refine; enumerate by axes of variation and rank | `iterate-naive-to-optimal` / G-NO-REINVENT, G-NAIVE-FIRST |
| workload-classify | **34** | classify the workload (read/write/total-ordering) first; the fork chooses the architecture | **`classify-workload-first`** (new) |
| binding-constraint | **33** | compute the bottleneck candidates and design for the dominant one; translate it into a number of machines | `find-the-binding-constraint` / G-AMPLIFICATION, G-CAPACITY |
| scope-blackbox | **31** | sub-problem → a named black box; do not roll your own consensus/crypto; build the core before collapsing into managed | `scope-defer-and-blackbox` |

## Tier 4 — present (13–22/82)
| pattern | /82 | essence | skill / gate |
|---|---|---|---|
| client-trust | **22** | security/correctness enforcement is server-side; never filter sensitive data / choose the id/shard in the browser | **`enforce-on-the-server`** (new) / **G-NO-CLIENT-TRUST** |
| hot-key (≠ hot-partition) | **17** | distinguish a hot partition (→ consistent hashing) from a hot key (→ CDN/cache/sharded counter) | `partition-keys-and-hot-partitions` (to refine) |
| invariant-data | **15** | invariants in the model (exact money, guarded counts, timestamp vs boolean); deltas, not state | `model-invariants-in-data` / G-INVARIANT-IN-DATA, G-DELTA-NOT-STATE |
| entry-exit-diagram | **14** | start the diagram from the entry/exit points and translate requirements into boxes | **`diagram-from-dataflow`** (new, process) |
| append-only | **13** | prefer append-only/event sourcing; avoid in-place update/delete; reconstruct state from events; stay away from tombstones | **`append-only-event-sourcing`** (new) / **G-APPEND-ONLY** |

## Gates surfaced by the evaluation (gaps that every arm missed)
- **G-NO-OVERENGINEER-REALTIME** — do not add real-time/stateful machinery (WebSocket) when access is intermittent (use polling/reload).
- **G-CACHE-POPULAR-NOT-ALL** — cache/CDN only the popular subset (via a popularity batch); do not push everything to the CDN.

## STYLE (recorded, does not become a gate)
| pattern | /82 | note |
|---|---|---|
| cite-sources | 39 | anchors on DDIA/Alex Xu/Grokking/production experience — a credibility tell |
| number-pedagogy | 10 | adjusts numbers "to keep it interesting" — relevant for fidelity, not a method to reproduce |

## Reading
His method is dominated by **3 reflexes** (decouple async, match the store to the access,
exploit staleness) + a core of ~9 patterns, with a **strong ML** branch (46/82) and a
tail of niche but real patterns. It converged early (~30 videos); the 82 gave the
provenance and the tail (client-trust, append-only, hot-key, invariants).
