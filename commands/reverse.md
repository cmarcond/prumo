# /prumo.reverse — Reverse engineering: existing project → seed (problem + Problem Gates)

An auxiliary entry point to the flow. Instead of starting from a prompt, it starts from
**finished code** and reconstructs the *seed* that, given to `/prumo.init`, would
regenerate this system's design. Precondition: `.prumo/` installed + the **path of a
target project**. Output (in the **root of the results project**): the seed ready to
paste into `/prumo.init` — optionally `questions.md` (the answered Problem Gates) and a
thin `intent.json`, to shorten the init.

> **Paths:** the framework (`gates/`, `skills/`, `templates/`) is read from `.prumo/`;
> the results go in the **root**. Full convention in `/prumo.init`.

> Altitude rule: prumo projects the project onto the **system design** axis — scale,
> components, guarantees. The *features/craft/TDD* story is NOT its job (it belongs to
> catraca). If the target project is CRUD with no scale challenge, the seed comes out
> lean — and that is fine.

## Step 0 — Mode and target
- Receive the **path of the target project**. Guided mode (default) or automatic mode.
- Re-read `manifesto.md` and `gates/gates.md`: the design you are going to invert has to
  be defensible by the same gates, so it is through them that you read the code.

## Step 1 — Reverse architect's reading (map the materialized solution)
Read, in this order, what reveals the **design already made**: README; infra/deploy
(`docker-compose*`, `k8s/*.yaml`, `*.tf`, Helm, Procfile); the choice of datastores,
caches, queues, load balancers; replica/scaling/partitioning configs; metrics,
SLAs, alerts, dashboards. Identify the **real components + edges** — this is the
`design.json` already materialized in the project (do not write it yet; it is an input to
the inversion).

## Step 2 — Invert to the Problem Gates (suggest from the evidence)
Read the questions from the **template** `.prumo/gates/questions.md` (blank — do NOT edit
it) and, for each gate (A→E / P1–P10), **infer** the answer from the evidence in the
code, citing the file/excerpt that supports it. Examples of the reverse reasoning:
- 3x replication on the datastore → high durability (P7); a cache on the hot path +
  read replicas → read-heavy and a tight latency SLA (P3, P7); a queue/broker →
  asynchronous fan-out and peaks (P4); a uniqueness index/transaction → uniqueness
  required (P5). Mark what cannot be inferred as `[assumed YYYY-MM-DD]`. Write it to
  `./questions.md` (root). In guided mode, present the inferences and ask for confirmation.

## Step 3 — Distill the thin `intent.json` (no solution)
From Gate A, write the intent: `problem`, `goal`, `scope_in[]`/`scope_out[]`,
qualitative `context_assumptions[]`. Two barriers, now inverted:
- **intent/solution**: NO component/technology/pattern from Step 1 enters the
  problem statement (Redis/Kafka/sharding belong to P8 "mandatory tech" or to the design,
  not to the problem);
- **intent/derivation**: do not enumerate the functional list or numbers — that is
  `/prumo.requirements`.
Run a **clean-context adversarial review** (in Claude Code, a Task subagent)
that hunts for solution leakage in the problem statement — if it finds technology in
`problem`, move it to P8 and rewrite. Schema: `templates/schemas/intent.schema.json`.

## Step 4 — Emit the seed
Assemble a **`SEED FOR /prumo.init`** block = problem statement (Step 3) + Problem Gates
answered with evidence (Step 2) + a `leak-check` confirming that the problem statement
does not name technology. This block is the **extracted prompt**. In automatic mode, also
write `intent.json` and `questions.md` so that the init can go straight on.

## Step 5 — Round-trip validation (recommended)
Run the seed through `/prumo.requirements` → `/prumo.design` and **compare** the generated
`design.json` with the real components/edges from Step 1. Each divergence is a **gap in
the seed** (a guarantee or number the problem did not capture) — address it and re-emit.
Convergence = the seed reconstructs the project.
