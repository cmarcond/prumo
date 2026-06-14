# Diagram From Dataflow

A method for building an architecture diagram by starting at the system's edges
(clients/actors and their request/response flows) and working inward, turning
each requirement into a component as you trace the data through it.

## When To Use

- You are drawing an architecture diagram from a set of functional requirements.
- You need to reason about where load concentrates and where data is stored.
- You want the diagram to be defensible: every box justified by a traced flow.
- You are explaining a design and must show how a request becomes a response.

## When Not To Use

- The architecture is already fixed and you are only annotating an existing
  diagram.
- The task is a pure data-model or schema exercise with no request/response
  surface.
- You are reverse-documenting a running system from code/telemetry rather than
  designing one.

## Preconditions

- The entry points are known: which actors/clients initiate interactions.
- The exit points are known: what each interaction returns or emits.
- The functional requirements are enumerated, each phrased as something the
  system must do.
- For each requirement you can state whether it primarily reads or writes data.

## Order Of Operations

1. List the actors/clients and place them at the edges of the canvas.
2. For each actor, draw its request flow inward and its response flow outward.
3. Take the first requirement; place the minimum component needed to satisfy it
   on the path the request already traces. Do not add components the flow does
   not yet reach.
4. Annotate every arrow with DATA direction (read vs write), not merely request
   direction. A request arrow pointing inward may carry a write or trigger a
   read; mark which.
5. Follow the data: where writes accumulate, place the store; where reads
   repeat, mark the candidate for caching/replication.
6. Repeat per requirement, extending inward only along paths an actual flow
   demands.
7. Stop when every requirement maps to a box and every box sits on a traced
   request-and-data path.

## Test Checklist

- Every actor has both a request-in and a response-out (or emit-out) flow.
- Every component lies on at least one traced flow; none float unconnected.
- Every arrow is labeled with data direction (read/write), distinct from request
  direction.
- Every requirement maps to at least one component reached by tracing.
- Storage sits where writes converge; caches/replicas sit where reads converge.
- No component exists that no requirement or flow justifies.

## Anti-Patterns

- Starting from the middle or the database and guessing the edges afterward.
- Drawing components with no traced request or data flow attached to them.
- Conflating request direction with data direction (assuming an inbound request
  means inbound data, or that a response means a read).
- Adding components for completeness or convention rather than for a requirement.

## Provenance

14/82 (process skill, no hard gate).
