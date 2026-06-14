# classify-workload-first

Classify the workload before choosing or drawing any architecture. The read/write/ordering profile and the access cadence determine the design; the design does not determine them.

## When To Use

- Starting any system-design task where the architecture is not yet fixed.
- Choosing between storage, caching, replication, or consistency strategies.
- Deciding whether updates must propagate to clients in real time.
- Evaluating an existing design that was committed to before its load profile was characterized.

## When Not To Use

- The workload profile is already established and agreed, and you are only refining a sub-component within fixed constraints.
- The task is a localized change that does not touch the data-flow or access model.

## Preconditions

- You can name the dominant operation mix: read-heavy, write-heavy, or total-ordering / strongly-sequenced.
- You can name the access cadence: continuous (clients need fresh state constantly) vs intermittent (clients access sporadically, tolerate staleness).
- You have the freedom to pick the architecture, not just decorate a pre-chosen one.

## Order Of Operations

1. State the read/write skew explicitly. Quantify if possible (ratio, ordering requirement).
2. State the access cadence: continuous vs intermittent; bounded staleness tolerance.
3. Derive the architectural class from 1 and 2 (e.g. read-heavy continuous favors replication/caching; write-heavy or total-ordering favors a serialized log / single-writer path; intermittent access favors pull over push).
4. Only now select concrete components and draw them.
5. Default to the simplest delivery mechanism the cadence allows; escalate to stateful/real-time machinery only when continuous access is a stated requirement.

## Test Checklist

- The workload classification (skew + cadence) is written down before any component appears.
- Each major component traces back to a classification decision, not to habit or familiarity.
- For data delivery: if access is intermittent, the design uses pull/refresh rather than a persistent stateful connection.
- Real-time / stateful machinery (if present) is justified by an explicit continuous-access requirement, not by "might be nice."
- Removing the classification would change the design — i.e. the design is actually driven by it.

## Anti-Patterns

- Committing to a design (drawing boxes, picking a database) before stating read/write skew.
- Treating every system as read-heavy-continuous by default and reaching for caches/replicas reflexively.
- Adding persistent stateful real-time transport when watchers are intermittent and periodic refresh would satisfy the staleness budget.
- Letting a familiar architecture dictate the workload assumptions instead of the reverse.

## Provenance

34/82; backs gate G-NO-OVERENGINEER-REALTIME.
