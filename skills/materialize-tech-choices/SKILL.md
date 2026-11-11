# Materialize Tech Choices

Once the structure of the design (components + edges) is green, **materialize**:
name the concrete technology of each component and justify it by the shape of the access.
The manifesto separates principle (what the component does) from materialization (the tech
that realizes it) — this skill is the materialization step, and it closes gap no. 1 measured
in the 15 runs (33% of the nuances ended up "right principle, tech not named").

## When To Use
- Always, when finalizing the design — each component needs a named tech.
- When a tech choice is not obvious (cite 1 alternative and why it lost).

## When Not To Use
- In a throwaway spike. In a phase where the structure is still unstable (materialize after the topology stops changing).

## Preconditions
- `design.json` with components/edges, and the shape of the workload (read:write, consistency, payload) known.

## Order Of Operations
1. For each component, write `tech_choices[{component, choice, rationale}]`: the concrete tech + one line tying it to the access characteristic (e.g. "write-heavy + scans → Cassandra/LSM"; "read-heavy point lookup → DynamoDB/B-tree"; "event stream → Kafka").
2. Where the choice is non-obvious, record `alternatives_considered` and the reason for the rejection.
3. Do not leave any component as a generic abstraction ("a durable log", "an object store") with no named tech.
4. Roll-from-scratch vs managed: decide explicitly (avoid lock-in where the level of the problem calls for the lower-level one).

## Test Checklist
- [ ] Every component in `design.json` has a named `tech_choice`.
- [ ] Each choice cites the access characteristic that justifies it (it is not a catalogue).
- [ ] Non-obvious choices have ≥1 alternative considered, with a reason.

## Anti-Patterns
- Components as generic abstractions with no named tech.
- Naming a tech without tying it to the access pattern.
- Vendor lock-in where rolling from scratch is what is expected (or the reverse).

## Provenance
Derived from the analysis of the 15 runs: the largest share of the missed nuances were
partials for lack of a concrete materialization of technology. Backs gate **G-MATERIALIZE-TECH**.
