---
name: adeptus-necroneerium
description: Use when the user requests adeptus_necroneerium, Adeptus Necroneerium, or @adeptus-necroneerium, and for Codex coding tasks where direct one-shot implementation is likely to drift but heavy planning would waste tokens. Applies Lich strategic topology, Vampire tactical contracts, Skeleton implementation, and Shade backward review only as needed to reach working, validated code.
---

# Adeptus Necroneerium

## Mission

Produce working, tested code with the least useful process overhead.

This is a Codex skill for code execution. It is not a council, debate system, or separate agent framework by default. Use it to choose the lightest path from request to working validated code.

## Prime directive

Working code over comprehensive agent artifacts.

Every meaningful output must either:

- become code,
- become a test,
- become an embedded contract or docstring,
- become an executable validation step,
- or identify a blocker that prevents code from proceeding.

Do not create standalone planning artifacts, long summaries, or ceremonial reports unless they directly improve implementation or review.

## Role names

The skill uses lightweight named roles to make responsibilities memorable. The names are labels for execution responsibilities, not separate personalities or mandatory separate agent calls.

- **Lich**: strategic topology. Shapes repository/module structure for the next working slice.
- **Vampire**: tactical contracts. Extracts only the contracts, skeletons, and tests needed to satisfy the milestone.
- **Skeleton**: worker implementation. Fills in behavior, tests, wiring, and focused repairs.
- **Shade**: review and backward routing. Verifies behavior, classifies findings, and routes failures only as far backward as necessary.

Do not create a new context or agent call merely because a role has a name. Role separation is conceptual unless the task genuinely benefits from an explicit handoff.

## Spec template

For non-trivial work, use `skills/adeptus-necroneerium/templates/spec.md` as the lightweight spec format.

The spec is optional. Use it when it will reduce ambiguity for a Tactical or Adeptus task. Skip it for Direct mode tasks where it would become process waste.

A spec should be treated as a working-code guide, not a planning artifact. It should capture:

- acceptance criteria,
- selected mode,
- current milestone,
- strategic topology if needed,
- tactical contracts if needed,
- validation plan,
- review route and repair attempt count.

## Mode selection

Choose the lightest safe mode.

### Direct mode

Use for tiny or obvious changes.

1. Inspect only the files needed.
2. Implement the change.
3. Add or update tests if relevant.
4. Run the smallest meaningful validation.
5. Report result with evidence.

### Tactical mode

Use when the file structure is obvious but contracts matter.

1. Identify the milestone or acceptance criteria.
2. Have the Vampire draft the minimal function/class/data/test skeleton required by that milestone.
3. Have the Skeleton implement the skeleton.
4. Run validation.
5. Have the Shade review findings as critical or trivial.

### Adeptus mode

Use when the change affects repo structure, multiple files, public interfaces, or validation logic.

1. **Lich strategic topology**: create or revise the minimal file/module structure needed for the next vertical slice.
2. **Vampire tactical skeleton**: define the necessary signatures, data contracts, docstrings, exceptions, and tests for the current milestone.
3. **Skeleton worker implementation**: fill behavior, complete tests, wire modules, and patch failures.
4. **Shade review**: validate behavior, classify findings, and route unresolved issues backward only as far as necessary.

Skip Lich topology if the structure is already obvious. Skip Vampire skeletons if the implementation shape is obvious.

## Layer responsibilities

### Lich: strategic code topology

Purpose: shape the repository/module structure needed for the next working vertical slice.

Allowed outputs:

- file tree changes,
- module boundaries,
- dependency direction,
- public entry points,
- data-flow boundaries,
- structural patch.

Avoid:

- long strategy prose,
- speculative architecture,
- implementation logic,
- structures not required by the current milestone.

Push back if the request is unclear, contradictory, too broad, or cannot be decomposed into a useful working-code slice.

### Vampire: tactical contracts and skeletons

Purpose: create the minimum sufficient contracts required to satisfy the strategic milestone.

Allowed outputs:

- function signatures,
- class/dataclass/enum definitions,
- data contracts,
- docstrings,
- expected exceptions,
- test names and test intent,
- edge cases.

Tactical designs must satisfy the current strategic milestone, no more and no less.

Avoid:

- overdesign,
- speculative APIs,
- future-proofing not required by the milestone,
- full implementation,
- unrelated refactors.

Push back if the milestone is insufficient, overbroad, internally inconsistent, or would require unjustified abstractions.

### Skeleton: worker implementation

Purpose: produce working behavior.

Allowed outputs:

- completed function bodies,
- completed tests,
- private helpers,
- wiring between modules,
- validation runs,
- focused patches for failures.

Avoid:

- silent public contract changes,
- expanding scope,
- replacing architecture without explanation,
- broad unrelated changes.

If the approved skeleton or contract is wrong, make the contract change explicit and local. Do not drift silently.

Push back if the contract cannot be implemented safely with the information provided.

### Shade: review and backward routing

Purpose: verify code against acceptance criteria and contracts.

Required checks:

- tests pass,
- acceptance criteria are satisfied,
- implementation matches contracts,
- public contracts did not drift silently,
- no placeholder code remains,
- no broad unrelated changes were introduced.

Every finding must be critical or trivial.

Critical findings block pass and must be resolved, explicitly downgraded with justification, or escalated.

Trivial findings do not block pass and may be noted, deferred, or ignored.

All passes require short reasoning and validation evidence.

## Backward review flow

Review can move backward, but construction should move forward.

When Shade review fails, identify the lowest responsible layer for each critical finding:

- Skeleton: implementation bug, failed test, placeholder code, missing edge case, behavior contradicts contract.
- Vampire: wrong function contract, missing data shape, wrong exception behavior, tests prove the wrong behavior, skeleton is over/under-specified.
- Lich: wrong file/module boundary, wrong dependency direction, wrong public entry point, topology prevents the vertical slice from working.
- Requirement/User: ambiguous acceptance criteria, conflicting goals, missing decision, external blocker.

Route fixes only as far backward as necessary. Do not restart the full chain unless the failure actually requires it.

Maximum autonomous repair attempts after failed review: two.

After the second failed repair attempt, stop and report honest failure with:

- likely failure layer,
- what was tried,
- what remains unresolved,
- recommended next human decision or redesign.

## Review output format

### PASS

Use when no critical findings remain.

Include:

- short reasoning,
- validation evidence,
- any trivial notes.

### FAIL

Use when a critical finding is fixable within the current layer or a lower backward route.

Include:

- critical finding,
- responsible layer,
- required fix,
- whether this is repair attempt 1 or 2.

### BLOCKED

Use when progress requires user input, a requirement decision, an unavailable dependency, or redesign after two failed repair attempts.

Include:

- blocker,
- likely failure layer,
- what was tried,
- recommended next action.

## Minimal execution loop

1. Determine Direct, Tactical, or Adeptus mode.
2. Inspect only needed context.
3. Use the spec template only if it helps implementation or review.
4. Produce code-adjacent structure only when it helps implementation.
5. Implement working code and tests.
6. Run validation.
7. Review critical/trivial findings.
8. Patch at most two failed review attempts.
9. Pass with evidence or block honestly.

## Anti-patterns

Do not:

- create a new agent or full setup context per function,
- treat named roles as a council or debate system,
- generate long planning documents before code,
- write implementation reports that no later step uses,
- perform review theater,
- expand the task beyond the milestone,
- force the Adeptus process onto tiny fixes,
- keep repairing indefinitely after repeated failure.
