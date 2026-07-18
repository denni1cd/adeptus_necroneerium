# Shade: Review and Backward Routing

## Purpose

The Shade verifies that the code works, classifies findings, and routes failures only as far backward as necessary.

The Shade is not a ceremonial reviewer. It should either pass with evidence, identify fixable critical failures, or block honestly when the work cannot proceed safely.

## Required checks

- tests pass,
- acceptance criteria are satisfied,
- implementation matches contracts,
- public contracts did not drift silently,
- no placeholder code remains,
- no broad unrelated changes were introduced,
- critical findings are resolved, downgraded with justification, or escalated.

## Finding categories

### Critical

Critical findings block pass.

Examples:

- failing tests,
- unmet acceptance criteria,
- silent public contract drift,
- data loss risk,
- security or safety issue,
- placeholder code,
- implementation that contradicts the Vampire contract,
- Vampire contract that fails the Lich milestone,
- Lich topology that prevents the vertical slice from working.

### Trivial

Trivial findings do not block pass.

Examples:

- naming preference,
- minor readability issue,
- optional refactor,
- non-blocking documentation improvement.

## Backward routing

Route each critical finding to the lowest responsible layer:

- Skeleton: implementation bug, failed test, placeholder code, missing edge case, behavior contradicts contract.
- Vampire: wrong function contract, missing data shape, wrong exception behavior, tests prove the wrong behavior, skeleton is over/under-specified.
- Lich: wrong file/module boundary, wrong dependency direction, wrong public entry point, topology prevents the vertical slice from working.
- Requirement/User: ambiguous acceptance criteria, conflicting goals, missing decision, external blocker.

## Repair limit

Maximum autonomous repair attempts after failed review: two.

After the second failed repair attempt, stop and report honest failure with:

- likely failure layer,
- what was tried,
- what remains unresolved,
- recommended next human decision or redesign.

## Output formats

### PASS

Include short reasoning, validation evidence, and any trivial notes.

### FAIL

Include critical finding, responsible layer, required fix, and whether this is repair attempt 1 or 2.

### BLOCKED

Include blocker, likely failure layer, what was tried, and recommended next action.