# Partition Keys And Hot Partitions

Choose a partition/shard key whose values spread load evenly so no single key
becomes a hot partition. When a hotspot is read-heavy, scale reads (replicas)
instead of changing the partitioning scheme. When the infrastructure self-shards,
let it pick its own keys.

## When To Use
- You must split a dataset or stream across nodes and need to pick the key that
  decides placement.
- One key value is suspected to carry a disproportionate share of traffic
  (skew), or a hotspot has already appeared and you must resolve it.
- You are about to hand-pick a sharding key for a component that can shard itself.

## When Not To Use
- The dataset fits one node and partitioning is premature.
- The hotspot is **write-heavy** — replicas do not absorb writes; that needs a
  different move (split the key, buffer/aggregate, or back-pressure), out of
  scope here.
- Skew is intrinsic and unavoidable for the access pattern (e.g. a global
  counter); treat it as a dedicated design problem, not a key choice.

## Preconditions
- You know the read:write ratio of the workload.
- You can estimate the distribution of candidate key values (which values are
  hot, how heavy the tail is) — not just assume uniformity.
- You know which components are managed/self-sharding versus self-operated.

## Order Of Operations
1. List candidate partition keys drawn from the access pattern.
2. For each candidate, estimate the load distribution across its values. Reject
   any key where a single value (or few values) concentrates load — that is a
   hot partition waiting to happen.
3. Prefer a key with high cardinality and even spread (a composite or
   synthetic key if no natural attribute qualifies).
4. If a hotspot still appears, classify it:
   - **Read-heavy** -> add read replicas of the hot partition; route reads to
     them. Do not reshard, do not switch to hash + scatter-gather.
   - **Write-heavy** -> out of scope (see When Not To Use).
5. If the component self-shards, do not supply a key — let it manage placement;
   only feed it a well-distributed input.

## Test Checklist
- [ ] Largest key value's share of load is bounded (no single value dominates).
- [ ] The chosen key has enough distinct values for the node count to grow into.
- [ ] Adding nodes rebalances load (no value pins traffic to one node).
- [ ] Read-heavy hotspots are handled by replicas, not by resharding or
      scatter-gather across all nodes.
- [ ] No manual key is imposed on a self-sharding component.

## Anti-Patterns
- Partitioning by a skewed attribute (one dominant id: a single active
  entity, a heavy producer, a popular item) -> that value's partition runs hot.
- "Fixing" a read-heavy hot partition with hash partitioning + scatter-gather:
  spreading every query to every node makes **all** nodes hot instead of one.
- Hand-picking a sharding key for a system designed to self-shard — fights the
  infrastructure and forfeits its rebalancing.
- Assuming uniform distribution without checking the actual value frequencies.

## Provenance
MP2, 5/8 build-set videos.

---
PRINCIPLE: spread load evenly via the key; scale read hotspots with replicas;
defer to self-sharding infrastructure.
MATERIALIZATION (examples only, not the rule): read replicas behind a hot
partition; a log/stream broker that shards its own topics; a key-value or
document store that rebalances by key range or hash.
