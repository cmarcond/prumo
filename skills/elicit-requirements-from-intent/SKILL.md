# Elicit Requirements From a Thin Intent

Derive a rich list of requirements from a generic problem statement. The intent
states the problem and the owner's scope; the requirements — functional (including the
implicit ones), invariants, non-functional and numbers — are **derived**, and deriving
is the work. Do not copy the words of the problem statement as if they were the requirements.

## When To Use
- Right after the intent is fixed and before any design.
- Whenever the problem statement is generic ("design an X in the style of Y") and the
  requirements surface does not exist yet.

## When Not To Use
- When the requirements already come given and verified by the owner (rare; even so,
  run the completeness checklist).
- For a throwaway spike that will not become a maintained design.

## Preconditions
- A thin `intent.json` (problem + the owner's in/out scope + qualitative context).
- The shape of the workload at least proposed (read:write, fan-out, volume).

## Order Of Operations
1. **Model the domain**: list the entities, the actions on them, and the
   **relationships** between entities. Relationships are where the forgotten
   requirements live (e.g. two types of relationship that look like one; a directional
   relationship).
2. **Walk the edge cases**: creation/update/deletion, conflict/duplicate,
   absence, limits (the largest/smallest case), concurrency. Each one tends to reveal
   a functional requirement or an invariant.
3. **Extract invariants**: what can NEVER be violated? uniqueness, monotonicity
   (upgrade-only), ordering, exactly-once, conservation. An invariant becomes an NFR and
   a gate later.
4. **Derive NFRs from the shape of the workload**: read-heavy → latency/reads and
   tolerable consistency; write/fan-out → amplification and durability; volume →
   retention. Each NFR tied to its why (the workload), not to a generic catalogue.
5. **Back-of-the-envelope**: the number the owner fixed + an estimate with the calculation
   (use `find-the-binding-constraint`).
6. **Review for completeness**: run `G-REQ-COMPLETENESS` and close the holes.

## Test Checklist
- [ ] Every relationship between entities became ≥1 requirement or was discarded with a reason.
- [ ] The edge cases (create/update/delete/conflict/limit) are covered.
- [ ] The domain invariants are explicit.
- [ ] Each NFR cites the workload characteristic that motivates it.
- [ ] The numbers have a calculation, not a guess; the likely bottleneck is named.
- [ ] Nothing is a literal copy of the problem statement without expansion.

## Anti-Patterns
- **Echo of the problem statement**: repeating the words of the prompt as "requirements", without deriving.
- **Forgotten relationship**: treating two types of relationship as one (e.g. follow ≠ connect).
- **Catalogue NFR**: listing "high availability, low latency" without tying it to the workload.
- **Implicit invariant**: assuming uniqueness/monotonicity without declaring it (it disappears in the design).
- **Over-spec**: inventing a requirement the domain does not ask for just to look complete.

## Provenance
Derived empirically: the clean-room benchmark showed that, starting from a generic
prompt, the derivation of requirements was the weak link (implicit relationships and
invariants were lost). Corroborated by the `requirements_method` observed in the
build-set (the instructor derives numbers with the calculation and distinguishes variants
of the problem).
