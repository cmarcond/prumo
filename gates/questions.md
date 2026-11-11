# Problem Gates — initial questions (the owner's decisions)

> A living record of the decisions about the **problem**. The user may be
> **generic**: the agent **suggests** each answer from a reading of the problem
> (init, Step 0.5) and the user only confirms/adjusts. A gate is a
> proposal-to-confirm, not an open question: nobody needs to arrive knowing
> scale or consistency. The "Answer" column receives the final answer; "Origin"
> records where it came from (`proposed` = suggestion confirmed · `user` = the
> user changed it · `prompt` = already fixed in the prompt · `[assumed]` =
> automatic mode). These decisions are NOT design decisions: they are what the
> owner fixes, and what the Design Gates (`gates.md`) check the design against.
> Output: `intent.json` (no solution) + a skeleton of `requirements.json`.

## Gate A — Problem and scope
| # | Question | Answer (proposed→confirmed) | Origin |
|---|---|---|---|
| P1 | What system are we designing, in terms of the problem (not the solution)? Who uses it and what can they do? | | |
| P2 | What is **in** scope (capabilities) and what is **out** (variants we will NOT handle)? | | |

## Gate B — Scale and shape of the workload
| # | Question | Answer (proposed→confirmed) | Origin |
|---|---|---|---|
| P3 | Order of magnitude: users/items, and the **read:write** ratio? (read-heavy? write-heavy? balanced?) | | |
| P4 | Is there fan-out / write amplification (one event generates N writes)? Peaks/seasonality? | | |

## Gate C — Guarantees (what the problem demands and what it tolerates)
| # | Question | Answer (proposed→confirmed) | Origin |
|---|---|---|---|
| P5 | **Consistency × availability** priority on the critical path? Is there a uniqueness / exactly-once requirement? | | |
| P6 | How much **staleness** is tolerated on reads? Where is an approximate count acceptable? | | |
| P7 | **Latency** targets (SLA, P99) and **durability** targets (can data be lost? which data)? | | |

## Gate D — Constraints and cost
| # | Question | Answer (proposed→confirmed) | Origin |
|---|---|---|---|
| P8 | Cost/infra constraints, multi-region, compliance, or mandatory/forbidden technologies? | | |

## Gate E — Rigor and ratchet
| # | Question | Answer (proposed→confirmed) | Origin |
|---|---|---|---|
| P9 | Strict, pedagogical or pragmatic evaluation? | | |
| P10 | On a score regression, does the ratchet alert (`warn`), block (`block`) or repair (`repair`)? | | |

## Defaults of the canonical profile (automatic mode)
Explicit minimal scope · read:write ratio declared (if unknown, assume
read-heavy and mark it) · availability > consistency unless there is a
uniqueness requirement · staleness tolerated when nothing says otherwise · P99
as the target · no multi-region unless requested · pedagogical evaluation ·
ratchet in `repair`.

> Iron rule: **method is never a question; problem is never an unmarked default.**
> What the user fixes explicitly gets the origin "prompt", not `[assumed]`.
