# AGENTS.md

## Project mission

Adeptus Necroneerium explores Layered Agile Coding: a workflow where strategic, tactical, worker, and review layers each contribute directly to working software instead of producing large planning artifacts.

The project exists to test whether progressive code construction can outperform raw one-shot coding on practical tasks without becoming another token-heavy process.

## Primary principle

Working code over comprehensive agent artifacts.

Every output should either:

- become code,
- become a test,
- become an embedded contract or docstring,
- become an executable validation step,
- or identify a blocker that prevents code from proceeding.

Avoid ceremonial planning, repeated restatement, long implementation reports, and unused documentation.

## Layer model

Use the layer model only when it helps produce working code.

### Strategic layer

Responsible for code topology:

- repository structure,
- file/module boundaries,
- dependency direction,
- public entry points,
- major data flow.

The strategic layer should not produce long prose strategy documents. Its output should usually be a compact repo/file shape or a concrete structural patch.

Strategic work may push back when the requested goal is unclear, contradictory, too broad, or cannot be decomposed into a useful working-code slice.

### Tactical layer

Responsible for code contracts:

- function signatures,
- class/dataclass/enum definitions,
- data contracts,
- docstrings,
- expected exceptions,
- test names and test intent,
- edge cases.

The tactical layer must satisfy the current strategic milestone: no more and no less. Tactical design should be necessary and sufficient for the milestone, not speculative future-proofing.

The tactical layer should make implementation easier and safer without overdesigning. It may push back when the milestone is insufficient, overbroad, internally inconsistent, or would require unjustified abstractions.

### Worker layer

Responsible for implementation:

- fill function bodies,
- complete tests,
- add private helpers where justified,
- wire modules together,
- run validation,
- patch failures.

Workers should not silently change public contracts. If a skeleton or contract is wrong, explain the contract change and keep the change local and justified.

Workers may push back when the skeleton or contract cannot be implemented safely with the information provided.

### Review layer

Responsible for verification:

- confirm tests pass,
- confirm acceptance criteria are satisfied,
- check implementation against contracts,
- check for placeholder code,
- patch clear failures when possible.

Preferred review output is short: PASS, PASS with trivial notes, FAIL with specific fixes, or BLOCKED with the missing information.

All reviews must classify findings as critical or trivial.

Critical findings block a pass. They must be resolved, explicitly downgraded with justification, or escalated as blocked. Examples include failing tests, unmet acceptance criteria, silent public contract drift, data loss risk, placeholder code, implementation that contradicts the tactical contract, tactical contracts that fail the strategic milestone, or structure that prevents the slice from working.

Trivial findings do not block a pass. They may be noted, deferred, or ignored. Examples include naming preferences, minor readability improvements, non-blocking documentation, or optional refactors.

All passes must include short reasoning. A pass should explain why acceptance criteria are satisfied, why no critical findings remain, and what validation evidence supports the result.

## Backward review flow

Review can move backward, but construction should move forward.

On review failure, classify each critical finding by the lowest responsible layer:

- Worker-level failure: implementation bug, missing edge case, placeholder code, failed test, or behavior that does not match the contract.
- Tactical-level failure: wrong function contract, missing data shape, wrong exception behavior, tests proving the wrong behavior, or over/under-specified skeleton.
- Strategic-level failure: wrong file/module boundary, wrong dependency direction, wrong entry point, or a topology that prevents the vertical slice from working.
- Requirement-level failure: ambiguous acceptance criteria, conflicting user goals, missing decision, or external blocker.

Route fixes only as far backward as necessary. Do not restart the full process unless the failure truly requires it.

Maximum autonomous repair attempts after a failed review: two. After the second failed repair attempt, stop, report honest failure, identify the likely failure layer, summarize what was tried, and recommend the next human decision or redesign.

## Cost discipline

Do not reduce cost by truncating useful code, tests, or functions.

Reduce cost by eliminating waste:

- repeated task restatement,
- agent identity setup,
- long planning artifacts,
- unused documentation,
- review theater,
- excessive handoffs,
- full-context reloads,
- planning detached from executable output.

## Workflow guidance

Prefer vertical slices. A useful slice proves behavior end to end:

1. input,
2. processing,
3. output,
4. test,
5. validation.

Do not build a huge abstract skeleton before proving any behavior works.

Skip the layered process for tiny fixes. Use direct implementation when the shape is obvious.

Escalate to layered coding when the task involves new modules, public contracts, multiple files, validation logic, or previous implementation drift.

## Current project status

This repository is in concept/design phase. Do not create a large framework until the smallest useful workflow has been defined and tested on real coding tasks.
