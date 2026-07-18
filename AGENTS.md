# AGENTS.md

## Project mission

Adeptus Necroneerium is a coding workflow where strategic, tactical, worker, and review responsibilities each contribute directly to working software instead of producing large planning artifacts.

The project exists to test whether progressive code construction can outperform raw one-shot coding on practical tasks without becoming another token-heavy process.

This is not a council or debate project. It is a Codex coding skill focused on getting from request to working, validated code.

## Codex skill entrypoint

This repository treats `skills/adeptus-necroneerium/SKILL.md` as the Codex skill entrypoint for Adeptus Necroneerium. The repository and prompt alias is `adeptus_necroneerium`; the registered skill name is `adeptus-necroneerium` because Codex skill names require hyphen-case.

This skill is strictly on demand. Never invoke it automatically from task complexity, file count, ambiguity, implementation drift, or a failed direct coding attempt. Use it only when the user explicitly requests Adeptus Necroneerium by name, writes `adeptus_necroneerium`, or invokes `@adeptus-necroneerium`.

After explicit invocation, choose the lightest safe mode. Direct implementation remains appropriate for tiny or obvious fixes even inside an Adeptus Necroneerium run.

Do not create extra artifacts simply because the skill exists. The skill is a code execution workflow, not a documentation workflow.

## Named roles

The project uses lightweight necromantic role names to make the layers memorable:

- **Lich** = Strategic topology
- **Vampire** = Tactical contracts
- **Skeleton** = Worker implementation
- **Shade** = Review and backward routing

These names are responsibility labels, not a reason to create separate agent contexts or perform roleplay. Use them to clarify which layer owns a decision.

## Spec template

Use `skills/adeptus-necroneerium/templates/spec.md` only when a lightweight spec will reduce ambiguity for Tactical or Adeptus mode work.

Skip the spec for Direct mode tasks where it would become process waste.

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

### Lich: Strategic topology

Responsible for code topology:

- repository structure,
- file/module boundaries,
- dependency direction,
- public entry points,
- major data flow.

The Lich should not produce long prose strategy documents. Its output should usually be a compact repo/file shape or a concrete structural patch.

The Lich may push back when the requested goal is unclear, contradictory, too broad, or cannot be decomposed into a useful working-code slice.

### Vampire: Tactical contracts

Responsible for code contracts:

- function signatures,
- class/dataclass/enum definitions,
- data contracts,
- docstrings,
- expected exceptions,
- test names and test intent,
- edge cases.

The Vampire must satisfy the current strategic milestone: no more and no less. Tactical design should be necessary and sufficient for the milestone, not speculative future-proofing.

The Vampire should make implementation easier and safer without overdesigning. It may push back when the milestone is insufficient, overbroad, internally inconsistent, or would require unjustified abstractions.

### Skeleton: Worker implementation

Responsible for implementation:

- fill function bodies,
- complete tests,
- add private helpers where justified,
- wire modules together,
- run validation,
- patch failures.

The Skeleton should not silently change public contracts. If a skeleton or contract is wrong, explain the contract change and keep the change local and justified.

The Skeleton may push back when the skeleton or contract cannot be implemented safely with the information provided.

### Shade: Review and backward routing

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

On Shade review failure, classify each critical finding by the lowest responsible layer:

- Skeleton-level failure: implementation bug, missing edge case, placeholder code, failed test, or behavior that does not match the contract.
- Vampire-level failure: wrong function contract, missing data shape, wrong exception behavior, tests proving the wrong behavior, or over/under-specified skeleton.
- Lich-level failure: wrong file/module boundary, wrong dependency direction, wrong entry point, or a topology that prevents the vertical slice from working.
- Requirement-level failure: ambiguous acceptance criteria, conflicting user goals, missing decision, or external blocker.

Route fixes only as far backward as necessary. Do not restart the full process unless the failure truly requires it.

Assign each critical finding a stable ID and an isolated retry counter. The initial construction and first rejection are not retries. The responsible layer receives retry 1 and, if the same finding remains, retry 2. Rewording, rerouting, or finding another symptom of the same root defect does not reset the counter. Unrelated findings receive independent counters.

Rerun from the responsible layer forward: Skeleton then Shade; Vampire then Skeleton then Shade; or Lich then Vampire then Skeleton then Shade. If the same finding remains after retry 2, stop the entire project with terminal FAIL. Requirement or external-dependency findings are BLOCKED without consuming implementation retries.

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

Skip the Adeptus process for tiny fixes. Use direct implementation when the shape is obvious.

Without explicit user invocation, do not escalate into the Adeptus workflow. After invocation, task complexity may determine which mode to use, but it is never itself a trigger.

## Current project status

This repository is in concept/design phase. Do not create a large framework until the smallest useful workflow has been defined and tested on real coding tasks.
