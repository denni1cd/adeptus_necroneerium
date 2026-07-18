# Project Charter: Adeptus Necroneerium

## Status

Concept / design exploration.

This project is not currently an Adeptus Engineerium replacement. It is a separate coding-process experiment focused on reducing wasted agent overhead while improving code quality through progressive construction.

## Core idea

Traditional agentic coding systems often split work into strategic, tactical, and worker layers, but only the worker layer actually writes code. The upper layers tend to produce plans, summaries, reviews, or artifacts that may consume large amounts of tokens without directly advancing the codebase.

Adeptus Necroneerium shifts that model.

Each layer contributes a different resolution of code:

- Strategic layer creates or revises the draft file/module structure.
- Tactical layer creates function, class, data contract, and test skeletons.
- Worker layer implements the actual behavior.
- Review layer verifies that the result works and patches failures.

The goal is not more process. The goal is working code with less wasted non-code output.

## Guiding principle

Working code over comprehensive agent artifacts.

Every meaningful output should either:

- become code,
- become a test,
- become an embedded contract/docstring,
- become an executable validation step,
- or identify a blocker that prevents code from proceeding.

Standalone planning documents, ceremonial logs, and repeated summaries are considered waste unless they directly improve implementation or review.

## Core doctrine

- Adeptus Necroneerium is strictly on demand and must never be selected implicitly.
- Working code over artifacts.
- Each layer may push back when it cannot safely complete its responsibility with what was provided.
- Tactical scope is milestone-bound: no more and no less.
- Review moves backward only as far as necessary.
- Critical findings must be resolved, downgraded with justification, or escalated.
- Trivial findings must not block working code.
- Each critical finding has an isolated two-retry repair budget.
- Passes require short evidence-based reasoning.

## Layer responsibilities

### Strategic layer

The strategic layer works at repository and module level.

It may draft:

- file structure,
- package boundaries,
- module names,
- ownership of responsibilities,
- major data flow,
- dependency direction,
- public entry points.

It should avoid:

- detailed prose strategy documents,
- implementation logic,
- excessive justification,
- unnecessary architecture.

Its output should look like a codebase taking shape.

The strategic layer may push back if the requested goal is unclear, contradictory, too broad, or cannot be decomposed into a useful working-code slice.

### Tactical layer

The tactical layer works at interface and contract level.

It may draft:

- function signatures,
- class/dataclass/enum definitions,
- data contracts,
- docstrings,
- expected exceptions,
- test names,
- test intent,
- edge cases.

It should avoid:

- full implementation,
- redundant planning summaries,
- unrelated refactors,
- changing strategic structure without noting why,
- speculative future-proofing,
- abstractions not required by the current milestone.

Its output should make implementation easier and safer.

Tactical designs must satisfy the current strategic milestone, no more and no less. A tactical design is good when it is necessary and sufficient for the milestone as working code.

The tactical layer may push back if the milestone is insufficient, overbroad, internally inconsistent, or would require unjustified abstractions.

### Worker layer

The worker layer writes the implementation.

It may:

- fill function bodies,
- complete tests,
- add private helpers,
- wire modules together,
- run validation,
- fix failures.

It should avoid:

- silently changing public contracts,
- expanding scope,
- replacing the architecture with a different one,
- writing broad unrelated code.

If the worker discovers the skeleton is wrong, it should request or explain a contract change rather than drifting silently.

The worker layer may push back if the skeleton or contract cannot be implemented safely with the information provided.

### Review layer

The review layer verifies working behavior.

It checks:

- tests pass,
- implementation matches intended behavior,
- public contracts were not changed accidentally,
- no placeholder code remains,
- no broad unrelated changes were introduced,
- acceptance criteria are actually satisfied.

The review output should be short unless there is a real issue.

Preferred review outcomes:

- PASS
- PASS with trivial notes
- FAIL with specific patch/fix required
- BLOCKED with specific missing information

All review findings must be categorized as critical or trivial.

Critical findings block a pass. A critical finding must be resolved by patch, downgraded with justification, or escalated as blocked. Critical examples include failing tests, unmet acceptance criteria, silent public contract drift, data loss risk, security/safety issue, placeholder code, implementation that contradicts tactical contract, tactical contract that fails the strategic milestone, or strategic topology that prevents the vertical slice from working.

Trivial findings do not block a pass. Trivial examples include naming preferences, minor style/readability improvements, optional refactors, or non-blocking documentation improvements.

All passes must be justified with short reasoning. A pass should state why acceptance criteria are satisfied, why no critical findings remain, and what validation evidence supports the result.

## Backward review flow

Review can move backward, but construction should move forward.

When review fails, it should identify the lowest responsible layer for each critical finding:

- Worker-level failure: bug in implementation, missing edge case, failed test, placeholder code, or behavior that does not match the contract.
- Tactical-level failure: wrong function contract, missing data shape, wrong exception behavior, tests proving the wrong behavior, or an over/under-specified skeleton.
- Strategic-level failure: wrong file/module boundary, wrong dependency direction, wrong public entry point, or a topology that prevents the vertical slice from working.
- Requirement-level failure: ambiguous acceptance criteria, conflicting user goals, missing decision, or external blocker.

Route the fix only as far backward as necessary. Do not restart the full chain unless the failure actually requires it.

Assign each critical finding a stable identity tied to the judged item, acceptance criterion, contract, or observable defect. The initial construction and first rejection are not retries. Each finding then receives retry 1 and retry 2 independently of every other finding. Rewording, rerouting, or discovering another symptom of the same root defect does not reset its counter.

A repair reruns the responsible layer and every affected downstream layer:

- Worker failure: Worker, then Review.
- Tactical failure: Tactical, then Worker, then Review.
- Strategic failure: Strategic, then Tactical, then Worker, then Review.
- Requirement or external blocker: BLOCKED without consuming an implementation retry.

If the same finding remains after retry 2, stop the entire project and report terminal FAIL with the finding identity and full attempt history.

## Cost philosophy

The project does not attempt to save tokens by limiting code output.

Code, tests, and useful skeletons are not the enemy.

The cost problem is usually caused by:

- repeated task restatement,
- agent identity setup,
- long planning artifacts,
- unused documentation,
- review theater,
- excessive handoffs,
- full-context reloads,
- planning detached from executable output.

This project should reduce those costs by making each step directly code-adjacent.

## Agile interpretation

The system should prefer vertical slices.

A useful slice proves behavior end to end:

- input,
- processing,
- output,
- test,
- validation.

The project should avoid building huge abstract skeletons before any behavior works.

The preferred rhythm is:

1. shape a small piece,
2. implement it,
3. test it,
4. review it,
5. move to the next slice.

## Initial open questions

1. What is the smallest useful version of this process?
2. When should the strategic layer be skipped?
3. When should the tactical skeleton layer be skipped?
4. What is the right unit of work: module, feature slice, story, or function group?
5. How do we prevent tactical skeletons from overdesigning?
6. How do we prevent workers from drifting away from approved contracts?
7. What review output is actually useful versus ceremonial?
8. Can a local model help with low-risk skeleton drafting without hurting quality?
9. When is up-to-date/cloud-model knowledge actually needed?
10. How do we compare this against raw Codex fairly?
11. What evidence is enough to downgrade a review finding from critical to trivial?
12. What task classes are best suited for the Adeptus workflow versus direct coding?

## Success criteria

The project is successful only if it can produce working code with better cost/benefit than raw one-shot coding for at least some classes of tasks.

It should be judged by:

- fewer wasted artifacts,
- fewer failed implementation loops,
- clearer module boundaries,
- better tests,
- less drift,
- comparable or lower total token cost,
- faster path to working code.

If it cannot beat raw Codex on practical tasks, the process should be simplified or abandoned.

## Non-goals

This project is not trying to create another heavy agent bureaucracy.

It is not trying to maximize documentation.

It is not trying to assign an agent to every function.

It is not trying to replace all direct coding.

It is not trying to force strategic/tactical layers onto tiny fixes.

It is not currently an Adeptus Engineerium integration.
