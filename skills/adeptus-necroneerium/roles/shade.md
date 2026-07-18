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

## Finding identity

Record the finding's parent scope, judged item, and stable finding ID tied to the acceptance criterion, contract, or observable defect. Keep that identity when the wording changes, another symptom of the same root defect appears, or the responsible layer is corrected.

Scopes may branch: one Lich scope may govern many Vampire scopes, and one Vampire scope may govern many downstream Skeleton and Shade items. Do not combine parents, children, siblings, or unrelated findings into one repair counter. Do not reset a counter by renaming or rerouting the same finding.

## Isolated retry limit

Initial construction is attempt 0. The first rejection immediately triggers retry 1. Rejection of retry 1 immediately triggers retry 2.

- Retry 1 is triggered by the first rejection and reruns the affected descendant branch before Shade reviews again.
- Retry 2 is triggered by rejection of retry 1 and reruns that affected branch one final time.
- If the same finding remains after retry 2, stop the entire project immediately with terminal FAIL.
- A different finding starts its own two-retry budget.
- Sibling scopes retain their state and independent counters.

Required downstream reruns:

- Skeleton finding: Skeleton, then Shade.
- Vampire finding: Vampire, then affected Skeleton and Shade descendants.
- Lich finding: Lich, then affected Vampire, Skeleton, and Shade descendants.
- Requirement/User finding: BLOCKED without consuming a retry until the missing input is supplied.

## Output formats

### PASS

Include short reasoning, validation evidence, and any trivial notes.

### FAIL

For a routed repair, include scope path, stable finding ID, judged item, critical finding, responsible layer, triggered retry number, and affected descendant branch to rerun.

For terminal project failure, include the finding ID, responsible layer, initial failure, retry 1 result, retry 2 result, and unresolved defect.

### BLOCKED

Include blocker, likely failure layer, what was tried, and recommended next action. Do not use BLOCKED for a finding that failed retry 2; that outcome is terminal FAIL.
