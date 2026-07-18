# Skill Outline: Adeptus Necroneerium

## Purpose

Adeptus Necroneerium is a coding execution skill for producing working, tested code while minimizing non-code process waste.

The skill is not an agent framework by default. It is a workflow that can be used by a human, Codex, ChatGPT, or another coding agent when direct one-shot coding is too likely to drift but a full planning bureaucracy would be too expensive.

## One-sentence definition

Use the lightest effective path from request to working validated code by moving through code topology, contracts, implementation, and review only when each step directly helps the codebase.

## Operating principle

Working code over comprehensive agent artifacts.

Every meaningful output must either:

- become code,
- become a test,
- become an embedded contract or docstring,
- become an executable validation step,
- or identify a blocker that prevents code from proceeding.

## Invocation boundary

This skill is strictly opt-in. Use it only when the user explicitly requests Adeptus Necroneerium by name, writes `adeptus_necroneerium`, or invokes `@adeptus-necroneerium`.

Never infer invocation from task complexity, file count, ambiguity, prior drift, or a failed direct attempt. Without an explicit request, use the ordinary Codex workflow.

After explicit invocation, the following traits help choose Tactical or Adeptus mode:

- new modules or files,
- public function/class/data contracts,
- multiple files,
- validation logic,
- meaningful tests,
- prior implementation drift,
- unclear module boundaries,
- a failed direct coding attempt.

Choose Direct mode within the invoked skill for tiny obvious fixes, pure documentation edits, simple config changes, or mechanical edits where direct implementation is the shortest safe path.

## Workflow modes

### Direct mode

Use when the shape is obvious.

1. Implement the change.
2. Add or update tests if relevant.
3. Run validation.
4. Report result.

### Tactical mode

Use when contracts matter but repo structure is mostly obvious.

1. Identify the current milestone or acceptance criteria.
2. Draft the minimal function/class/data/test skeleton required by the milestone.
3. Implement the skeleton.
4. Run validation.
5. Review critical/trivial findings.

### Adeptus mode

Use when the change affects structure, multiple files, or public interfaces.

1. Strategic topology: define or update the minimal file/module structure for the next vertical slice.
2. Tactical skeleton: define the necessary function signatures, data contracts, docstrings, and tests for the current milestone.
3. Worker implementation: fill behavior, complete tests, and wire the slice.
4. Review: validate behavior, classify findings, patch clear failures, and route unresolved issues backward only as far as necessary.

## Layer responsibilities

### Strategic layer: code topology

Produces repository or module structure needed for the next working slice.

Allowed outputs:

- file tree changes,
- module boundaries,
- dependency direction,
- public entry points,
- data-flow boundaries,
- structural patch.

Must avoid:

- long strategy prose,
- speculative architecture,
- implementation logic,
- structures not required by the current milestone.

May push back if the request is too unclear, broad, contradictory, or cannot be decomposed into a working vertical slice.

### Tactical layer: contracts and skeletons

Produces the minimal contracts needed to satisfy the strategic milestone.

Allowed outputs:

- function signatures,
- class/dataclass/enum definitions,
- data contracts,
- docstrings,
- expected exceptions,
- test names,
- test intent,
- edge cases.

Must satisfy the milestone, no more and no less.

Must avoid:

- overdesign,
- speculative APIs,
- future-proofing not required by the milestone,
- full implementation,
- unrelated refactors.

May push back if the milestone is insufficient, overbroad, internally inconsistent, or would require unjustified abstractions.

### Worker layer: implementation

Produces working behavior.

Allowed outputs:

- completed function bodies,
- completed tests,
- private helpers,
- wiring between modules,
- validation runs,
- focused patches for failures.

Must avoid:

- silent public contract changes,
- expanding scope,
- replacing architecture without explanation,
- broad unrelated changes.

May push back if the contract cannot be implemented safely with the information provided.

### Review layer: verification and routing

Checks the result against acceptance criteria and contracts.

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

Review failure must route to the lowest responsible layer.

- Worker: implementation bug, failed test, placeholder code, missing edge case, behavior contradicts contract.
- Tactical: wrong function contract, missing data shape, wrong exception behavior, tests prove the wrong behavior, skeleton is over/under-specified.
- Strategic: wrong file/module boundary, wrong dependency direction, wrong public entry point, topology prevents the vertical slice from working.
- Requirement/User: ambiguous acceptance criteria, conflicting goals, missing decision, external blocker.

Do not restart the full chain unless the failure requires it.

Assign each critical finding a stable identity and its own retry counter. The initial construction and first rejection are not retries. Each finding receives retry 1 and retry 2. Rewording, rerouting, or discovering another symptom of the same root defect does not reset the counter; unrelated findings have independent counters.

Rerun from the responsible layer forward:

- Worker finding: Worker, then Review.
- Tactical finding: Tactical, then Worker, then Review.
- Strategic finding: Strategic, then Tactical, then Worker, then Review.
- Requirement/User finding: BLOCKED without consuming implementation retries.

If the same finding remains after retry 2, terminate the entire project as FAIL and report its full attempt history.

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

- stable finding ID,
- critical finding,
- responsible layer,
- required fix,
- next retry number, 1 or 2,
- downstream layers that must rerun.

A same-finding failure after retry 2 is terminal FAIL for the entire project.

### BLOCKED

Use when progress requires user input, a requirement decision, or an unavailable dependency. Do not use BLOCKED after retry 2; that outcome is terminal FAIL.

Include:

- blocker,
- likely failure layer,
- what was tried,
- recommended next action.

## Minimal skill loop

1. Decide whether Direct, Tactical, or Adeptus mode is needed.
2. Build the smallest useful vertical slice.
3. Keep outputs code-adjacent.
4. Validate.
5. Review with critical/trivial classification.
6. Assign stable IDs and isolated two-retry budgets to critical findings.
7. Rerun each repair from the responsible layer through every affected downstream layer.
8. Pass with reasoning, block for missing external input, or terminate if the same finding fails retry 2.

## Non-goals

This skill is not trying to:

- create a new heavy agent bureaucracy,
- create an agent per function,
- force strategic/tactical layers onto tiny fixes,
- maximize documentation,
- replace direct coding where direct coding is best,
- hide failure behind endless retries.

## First experiment target

The first practical experiment should be small but non-trivial: enough to require contracts and tests, but not enough to justify a large framework.

A good first experiment should compare:

- raw direct coding,
- tactical mode,
- Adeptus mode.

The project should only continue adding structure if the experiment shows a real advantage in working-code quality, reduced drift, or reduced wasted process.
