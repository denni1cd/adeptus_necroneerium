# Adeptus Necroneerium Spec

Use this template only when it helps implementation or review. Skip it for tiny Direct mode work.

## Request

<!-- Short statement of the requested change. -->

## Acceptance criteria

<!-- Observable outcomes required for the work to pass. -->

- 

## Selected mode

<!-- Direct, Tactical, or Adeptus. Explain briefly why. -->

Mode: 
Reason: 

## Current milestone

<!-- The smallest useful working-code slice. Tactical design must satisfy this milestone, no more and no less. -->

## Non-goals

<!-- Explicitly list things that should not be built or changed in this slice. -->

- 

## Lich: strategic topology

Use only if structure is not obvious.

### Files/modules

<!-- Files to create/change and their responsibility boundaries. -->

- 

### Dependency direction

<!-- Any dependency rules needed to keep the slice clean. -->

## Vampire: tactical contracts

Use only if contracts are needed.

### Types / data contracts

<!-- Dataclasses, enums, schemas, payload fields, validation rules. -->

### Functions / methods

<!-- Signatures, behavior, exceptions, side effects. -->

### Tests

<!-- Test names and intent. -->

- 

## Skeleton: implementation plan

<!-- Concrete implementation notes. Keep this code-adjacent; do not write a prose plan if code is clearer. -->

## Validation plan

<!-- Commands or checks required to verify the work. -->

- 

## Shade: review route

### Critical findings

<!-- Must be resolved, downgraded with justification, or escalated. -->

- 

### Trivial findings

<!-- Non-blocking notes only. -->

- 

### Finding repair ledger

<!-- Keep one stable row per critical finding. Initial work is attempt 0; first rejection triggers retry 1. -->

| Scope path | Finding ID | Judged item / acceptance criterion | Responsible layer | Triggered retry | Retry result | Status |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

First rejection triggers retry 1; rejection of retry 1 triggers retry 2; rejection of retry 2 terminates the entire project as FAIL. Do not pool counters across parent, child, sibling, or unrelated findings. Rerun only the affected descendant branch.

### Final outcome

<!-- PASS, FAIL, or BLOCKED. Pass requires short reasoning and validation evidence. -->

Outcome: 
Reasoning: 
Validation evidence: 
