# Find The Binding Constraint

Before designing anything, compute the candidate bottlenecks, identify the single
one that actually binds, and let it drive the architecture. State what is fine at
low scale and exactly why it breaks at high scale.

## When To Use
- A system has a scale or load target and you must justify the structure, not just sketch it.
- More than one resource could plausibly be the limit (bandwidth, CPU, storage, throughput, memory, IOPS, fan-out) and it is not obvious which dominates.
- You are about to choose a topology (replicas vs shards, batch vs stream, push vs pull) and the right choice depends on which resource runs out first.

## When Not To Use
- The scale is trivial / single-box and no resource is near a limit — naming a "binder" is theater.
- The constraint is already established and agreed (e.g. a prior step computed it); don't recompute for ceremony.
- There is no numeric target at all and none can be assumed — get the target first.

## Preconditions
- Approximate inputs: request rate, object/record size, total data volume, read:write ratio, retention/time window.
- Per-unit costs for each candidate resource (a request costs X CPU, a stored item costs Y bytes, a transfer costs Z bandwidth).
- Capacity of one unit of the relevant building block (one machine/node: its cores, NIC bandwidth, disk, memory).

## Order Of Operations
The constraint-finding procedure. PRINCIPLE first; the arithmetic below is one MATERIALIZATION.

1. **List the candidates.** Enumerate the resources that could run out: bandwidth, CPU, storage, throughput (QPS), memory, IOPS, connection/fan-out count. Don't pre-judge.
2. **Estimate each candidate independently.** Back-of-the-envelope, one line each:
   - Storage = volume × size × replication × retention.
   - Bandwidth = rate × payload size (in and out separately).
   - CPU = rate × work-per-request, converted to cores/machines.
   - Throughput = required QPS vs per-node QPS ceiling.
   - Memory / IOPS / fan-out by the same shape.
   Compute the order of magnitude, not a precise figure.
3. **Convert to a common unit.** Express each as "how many machines/nodes does this resource alone demand" (or "what fraction of one node"). This makes them comparable.
4. **Pick the binder.** The candidate demanding the most capacity is the binding constraint. Name it explicitly with a one-word label (storage-bound, core-bound, read-bound, bandwidth-bound, write-bound).
5. **Sanity-check the margin.** If the top two candidates are within ~2x, treat both as binding and design for the pair; only commit to one when it clearly dominates.
6. **Reason by scale regime.** State the threshold: what is fine at low scale, and the specific resource that breaks first as scale rises, and at roughly what point. The breaking resource should equal the binder from step 4 — if it doesn't, an estimate is wrong.
7. **Let the binder drive the architecture.** Make the first structural decision the one that relieves the named constraint (e.g. read-bound → replicas; storage-bound → partition/tier/compress; core-bound → horizontal compute). Defer decisions that fight a non-binding resource.

## Test Checklist
- [ ] Every candidate resource was estimated, not assumed away.
- [ ] Each estimate is reduced to a comparable unit (machines / fraction of a node).
- [ ] Exactly one binder is named with a one-word label — or a tie is explicitly declared.
- [ ] The scale regime is stated: fine below threshold T, breaks above it, on resource R.
- [ ] R (the resource that breaks) matches the named binder.
- [ ] The first architectural move addresses the binder, not a different resource.
- [ ] No part of the design pays to optimize a resource that is not binding.

## Anti-Patterns
- **Assumed constraint.** Skipping the back-of-the-envelope and declaring the bottleneck by reflex or habit.
- **Wrong binder.** Designing hard for a resource that is not the one that actually runs out first (e.g. optimizing throughput on a storage-bound system).
- **No regime.** Asserting "it scales" or "it breaks" without the threshold and the specific resource that fails.
- **Premature multi-constraint.** Designing for every candidate at once instead of the dominant one, when one clearly dominates.
- **Unconverted units.** Comparing raw bytes against raw QPS against raw cores without a common denominator, then guessing.

## Provenance
MP5 — "Find the binding constraint and design for it." Appears in 4 of the 8
build-set videos (provenance 4/8). Patterns with a build-set count are treated as
technique and promoted to skills.
