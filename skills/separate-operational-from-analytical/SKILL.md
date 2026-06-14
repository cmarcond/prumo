# separate-operational-from-analytical

Keep analytical, training, and large-scan work off the operational serving store. The operational store answers low-latency point and range queries for live traffic. Analytical work (group-by, full scans, ETL, model training) runs against a separate analytical store fed asynchronously. Mixing the two lets heavy analytical queries contend for resources on the serving path, spiking latency and failing live requests.

This is the PRINCIPLE: one store sized and tuned for low-latency live serving, a physically separate store for heavy read-mostly scans, with asynchronous propagation between them. The specific MATERIALIZATION (how you replicate, what the analytical store is) is interchangeable and marked as examples below.

## When To Use

- A single store serves both live point/range lookups and heavy aggregate or scan workloads.
- You observe (or anticipate) serving-latency spikes correlated with reporting jobs, exports, or batch runs.
- You need full-table scans, group-by/aggregation, joins across large datasets, ETL, or model-training reads.
- Analytical demand is read-mostly and can tolerate seconds-to-minutes of staleness.
- You want to scale serving capacity and analytical capacity independently.

## When Not To Use

- The dataset is small enough that any query is cheap on the serving store and contention is impossible.
- Analytical consumers require strict read-your-writes consistency with the operational store (no staleness budget).
- There is no measurable contention and no realistic growth path that would create it (avoid premature split).
- The workload is purely operational with no scan/aggregate access pattern at all.

## Preconditions

- Workloads are classified: each access pattern is labeled operational (low-latency point/range) or analytical (scan/aggregate/ETL/training).
- A staleness budget exists for analytical consumers (how fresh must analytical data be).
- An asynchronous propagation mechanism is chosen and its lag is bounded and observable.
- The analytical store's schema/model is shaped for scans/aggregation, not copied verbatim from the serving schema.
- Serving latency SLOs are defined and measured before the split, to confirm the win after.

## Order Of Operations

1. Inventory access patterns; tag each as operational or analytical.
2. Set the staleness budget for analytical reads and the serving latency SLO.
3. Provision a separate analytical store sized for scans/aggregation.
   *(Materialization examples: a columnar warehouse, a data lake, a read replica reserved for analytics.)*
4. Establish asynchronous propagation from operational to analytical store.
   *(Materialization example: change-data-capture streaming the operational write log; periodic snapshot/export as a simpler alternative.)*
5. Repoint all analytical consumers (reports, exports, ETL, training) to the analytical store.
6. Verify no analytical query path touches the operational store.
7. Monitor propagation lag against the staleness budget and serving latency against the SLO.

## Test Checklist

- [ ] Run the heaviest analytical query (full scan / large group-by) and confirm serving latency stays within SLO during it.
- [ ] Confirm analytical consumers connect only to the analytical store (no operational credentials/endpoints in their config).
- [ ] Measure propagation lag under load; confirm it stays within the staleness budget.
- [ ] Kill/pause propagation and confirm serving is unaffected (decoupling holds).
- [ ] Load-test concurrent live traffic plus a batch job; confirm no failed live requests.
- [ ] Verify analytical results match the operational source within the staleness window.
- [ ] Confirm the analytical store can be rebuilt/backfilled from the operational source.

## Anti-Patterns

- Running full-table scans, group-by/aggregation, ETL, or model-training reads directly against the production operational store.
- Using a single store for both serving and analytics "to keep things simple," then watching batch jobs spike serving latency.
- Pointing reporting/export tools at the live operational database, causing page loads to slow or fail during report runs.
- Treating a synchronous read replica of the serving store as an analytical store without isolating its resource budget.
- Copying the operational schema verbatim into the analytical store, leaving it unfit for scans/aggregation.
- Letting analytical consumers hold long-running transactions or locks on the operational store.

## Provenance

Synthesized from a recurring pattern across approximately 6 system-design sources. Backs gate **G-OLTP-OLAP**: analytical/scan/aggregate/ETL/training workloads must not execute against the operational serving store; they run against a separate analytical store fed asynchronously, with bounded, observable propagation lag and a serving latency SLO that holds under concurrent analytical load.

Neutral example workload referenced for illustration only: *reporting*.
