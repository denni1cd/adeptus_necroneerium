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

### Tactical layer

Responsible for code contracts:

- function signatures,
- class/dataclass/enum definitions,
- data contracts,
- docstrings,
- expected exceptions,
- test names and test intent,
- edge cases.

The tactical layer should make implementation easier and safer without overdesigning.

### Worker layer

Responsible for implementation:

- fill function bodies,
- complete tests,
- add private helpers where justified,
- wire modules together,
- run validation,
- patch failures.

Workers should not silently change public contracts. If a skeleton or contract is wrong, explain the contract change and keep the change local and justified.

### Review layer

Responsible for verification:

- confirm tests pass,
- confirm acceptance criteria are satisfied,
- check implementation against contracts,
- check for placeholder code,
- patch clear failures when possible.

Preferred review output is short: PASS, PASS with minor notes, FAIL with specific fixes, or BLOCKED with the missing information.

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
