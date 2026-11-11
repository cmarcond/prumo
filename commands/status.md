# /prumo.status — Reconcile state

Use it after editing an answer in `./questions.md` (root) or when resuming work.

> **Paths:** the results (`questions.md`, `intent.json`, `requirements.json`,
> `design/`, `evaluation/`, `ratchet.json`) live in the **root**; the framework is read
> from `.prumo/`. Full convention in `/prumo.init`.

1. Re-read `./questions.md`, `./intent.json`, `./requirements.json` and the latest version
   in `./design/` (all in the root).
2. If a Problem Gate changed: mark the affected artifacts (intent/requirements/
   design) and propose the reconciliation (e.g. the read:write ratio changed → re-run the
   bottleneck and the capacity/amplification gates).
3. Report: which phase it is in (init / design vN / evaluate), pending gates, and the
   next action (`/prumo.init`, `/prumo.design` or `/prumo.evaluate`).
4. Never rewrite the owner's decisions without confirming; the agent executes the design,
   it does not redefine the problem.
