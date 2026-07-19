---
name: adeptus-necroneerium
description: Strictly on-demand coding workflow for large or structurally complex implementation tasks. Use only when the user explicitly requests Adeptus Necroneerium, writes adeptus_necroneerium, or invokes @adeptus-necroneerium. Codex orchestrates one whole-project Lich draft, multiple Vampire tactical scopes, bounded Skeleton implementation assignments, evidence-based Shade review, and mechanically guarded terminal conditions.
---

# Adeptus Necroneerium

## Mission

Complete substantial coding requests with high quality and reasonable total token cost by giving implementation a revisable strategic and tactical frame.

The goal is fewer user reprompts, less architectural drift, less rework, and more honest verification. Speed and maximum parallelism are not primary goals.

## Invocation boundary

This skill is strictly opt-in. Run it only when the user explicitly requests Adeptus Necroneerium by name, writes `adeptus_necroneerium`, or invokes `@adeptus-necroneerium`. The native `$adeptus-necroneerium` form is equivalent.

Never self-invoke based on complexity, file count, ambiguity, prior drift, or a failed direct attempt. Those traits affect mode selection only after explicit invocation.

## Mechanical completion guard

The installed plugin activates a session-scoped ledger on explicit invocation. Hook context supplies absolute paths for the ledger and `adeptus_state.py`. This state belongs to plugin data, not the target repository.

After read-only preflight and whole-request inspection, but before target writes:

1. Build the complete binding acceptance inventory, including every requested phase and gate.
2. Write a temporary inventory JSON object with `request_title`, `current_phase`, `acceptance`, `phase_gates`, and optional `lich_revision` and `vampire_scopes`.
3. Give every acceptance and gate record a unique stable `id`, observable `description`, optional `phase`, `state` (initially `pending`), and `evidence` list.
4. Initialize the injected ledger:

```text
python <adeptus-state-script> init --state <session-ledger> --inventory <inventory-json>
```

Keep it current with the tool rather than editing it by hand:

```text
python <adeptus-state-script> set-item --state <session-ledger> --id <id> --status passed --evidence <direct-result>
python <adeptus-state-script> set-gate --state <session-ledger> --id <id> --status passed --evidence <direct-result>
python <adeptus-state-script> advance-phase --state <session-ledger> --gate <gate-id> --to <next-phase>
```

Use `record-finding --help` and `record-blocker --help` for routed failures and genuine external blockers. Finding IDs and attempt evidence are immutable across retries. A blocker must be external, directly evidenced, name an unblock action, and cover every unfinished acceptance or gate ID plus every unresolved critical finding ID.

Immediately before final output, propose exactly one terminal outcome:

```text
python <adeptus-state-script> propose --state <session-ledger> --outcome PASS
python <adeptus-state-script> propose --state <session-ledger> --outcome BLOCKED --blocker-id <id>
python <adeptus-state-script> propose --state <session-ledger> --outcome FAIL --finding-id <id>
```

An invalid proposal exits nonzero and is nonterminal. Any later ledger mutation invalidates a prior proposal. The Stop hook also rechecks the state: it permits final output only for a certified outcome and otherwise supplies a continuation reason for the next turn.

The user may explicitly end an active run with `@adeptus-necroneerium abort`. Hook unavailability or corruption is not permission to improvise a terminal claim; either repair it before target work or report the genuine external limitation without writing the target.

## Prime directive

Working code over comprehensive agent artifacts.

Every meaningful output must either:

- become code or a code-adjacent draft used by downstream implementation;
- become a test or executable validation step;
- become an embedded contract, schema, or docstring;
- update the compact orchestration state needed to finish the request;
- or identify a blocker that prevents code from proceeding.

Do not create ceremonial reports, repeated task summaries, or planning documents that downstream work will not use.

## Operating model

Codex is the orchestrator and retains responsibility for the complete user request, work state, dependency order, recalls, phase gates, and terminal outcome.

The named roles are execution responsibilities, not personalities or mandatory separate agent calls:

- **Lich**: one strategic responsibility over the complete requested outcome.
- **Vampire**: one tactical responsibility per coherent subsystem; a Lich may define many Vampire scopes.
- **Skeleton**: one bounded implementation responsibility; each Vampire may define many Skeleton assignments.
- **Shade**: review, integration judgment, backward routing, and recall authority at Skeleton, Vampire, phase, and project gates.

Do not create a separate context merely because a role has a name. When a separate subagent is justified, give it only the context its scope needs. Codex remains the orchestrator.

Responsibility is a hierarchy, but implementation dependencies may form a DAG. The Lich drafts cross-Vampire seams and dependencies; Codex schedules scopes accordingly.

## Binding requirements and revisable drafts

The user's requested outcomes, explicit constraints, acceptance criteria, safety requirements, and phase gates are binding unless the user changes them.

Lich topology, Vampire contracts, Skeleton plans, internal APIs, file boundaries, and generated tests are **drafts**. They guide downstream work but are not immutable requirements.

Lower responsibilities are free to revise an upstream draft when implementation evidence reveals a safer, simpler, or more correct design. They do not need permission or a routine return to the parent responsibility. They must:

- make material changes explicit;
- update affected contracts, tests, and orchestration state;
- identify affected siblings or consumers;
- revalidate invalidated work;
- preserve unrelated passed work.

Free to revise does not mean free to ignore without cause. A draft must materially guide downstream work or it is waste.

A normal evidence-driven draft revision is not a retry. A retry begins only when Shade rejects a judged item as a critical finding.

Shade judges the product against the user request and observed behavior, not merely against an upstream draft or tests written from that draft.

## Mode selection

Choose the lightest safe mode after explicit invocation.

### Direct mode

Use for tiny or mechanical work where hierarchy would cost more than it prevents.

1. Inspect the necessary context.
2. Implement.
3. Add or update relevant tests.
4. Validate directly.
5. Report evidence.

### Tactical mode

Use when topology is obvious but contracts or coordinated implementation matter.

1. Establish the binding acceptance criteria.
2. Create one Vampire tactical draft.
3. Execute its Skeleton assignments.
4. Apply Skeleton and Vampire Shade gates.
5. Report only after the requested outcome passes.

### Adeptus mode

Use for large, phased, multi-subsystem, structurally ambiguous, or evolution-heavy work.

Run the complete hierarchy below. Do not terminate after the first working subsystem.

## Adeptus hierarchy and lifecycle

### 1. Lich: whole-project strategic draft

The singular Lich reads the complete user request and all supplied specifications before decomposing implementation.

It drafts the entire requested outcome in breadth, including later phases, while avoiding premature private implementation detail. Its compact output must cover:

- acceptance coverage across the complete request;
- proposed repository, package, file, and module topology;
- major data flow, dependency direction, and public integration seams;
- a set of coherent Vampire scopes;
- dependencies and likely activation order among those scopes;
- phase and compatibility gates that must remain binding;
- high-risk seams that need early executable evidence.

The Lich may reorganize implementation order when that improves development, but it may not violate explicit user gates. Awareness of future phases should prevent dead-end architecture, not justify speculative implementation.

A broad request is not by itself a blocker. Decomposing broad work is the Lich's responsibility. Block only for irreducible ambiguity, conflicting binding requirements, missing authority, or unavailable external dependencies.

### 2. Codex: activate a Vampire scope

Codex selects the next dependency-ready Vampire scope from the Lich draft. Prefer one active Vampire at a time for context and coordination efficiency. Overlap scopes only when it materially improves quality or reduces risk enough to justify coordination cost.

A Vampire scope remains a stable identity even if its implementation context is later retired and recalled.

### 3. Vampire: tactical subsystem draft

The active Vampire reads its relevant Lich context and drafts the complete tactical frame for one coherent subsystem:

- files or tightly related code areas;
- types, signatures, schemas, exceptions, and behavioral contracts;
- relevant test intent and falsification cases;
- cross-scope interfaces inherited from or proposed back to the Lich draft;
- bounded Skeleton assignments and their dependency order;
- subsystem acceptance conditions and integration checks.

The Vampire should remove ambiguity for Skeleton work without implementing the whole subsystem or inventing speculative abstractions.

### 4. Skeleton army: bounded implementation

Codex executes the Vampire's Skeleton assignments in dependency order. A Skeleton owns one cohesive implementation unit, usually one file and all relevant stubs, but it may span tightly coupled implementation and test files when splitting them would create incomplete behavior.

Each Skeleton:

- implements all behavior in its assignment;
- completes the relevant tests;
- runs focused validation;
- may revise drafts under the rules above;
- leaves no placeholder behavior presented as complete.

Do not create an agent call per function. Merge tiny adjacent assignments when separation would add handoff cost without improving review.

### 5. Shade: Skeleton gate

Shade judges each Skeleton result against its assignment, affected user acceptance criteria, current contracts, and direct evidence.

A Skeleton PASS is intermediate state. Codex marks the item complete and executes the next ready Skeleton assignment without returning to Lich or Vampire for an already-known decision.

### 6. Shade: Vampire gate and retirement

After all required Skeleton items for the active scope pass, Shade reviews the integrated Vampire subsystem, including its cross-scope seams and directly relevant documentation.

On PASS, Codex retires the Vampire context, preserves its current draft and evidence, and activates the next ready Vampire. Retirement means inactive, not immutable or permanently unavailable.

### 7. Continue until the full request is covered

Codex continues through every required Vampire scope. A working subsystem, vertical slice, milestone, or phase checkpoint is never project PASS when requested work remains.

If a phase gate is binding, record its direct evidence and proceed automatically to the next requested phase unless user input is genuinely required.

### 8. Shade: phase and project gates

At each required phase gate and at final completion, Shade independently checks the integrated product against the complete acceptance inventory.

Required review includes, where relevant:

- executable behavior at real claimed boundaries;
- full and focused tests with exact results;
- public API, CLI, UI, persistence, concurrency, restart, and process behavior;
- backward compatibility and retained fixtures;
- README commands run verbatim from documented working directories;
- documentation claims compared with actual behavior;
- final filesystem cleanup scanned after the last tool that can regenerate debris;
- direct acknowledgment of anything not verified.

Passing generated unit tests is not sufficient evidence for a boundary those tests bypass.

## Shade backward routing and Vampire recall

Shade assigns each critical finding to the lowest responsible scope:

- **Skeleton**: implementation defect, failed test, placeholder, missing edge case, or behavior contradicting the current contract.
- **Vampire**: incorrect or incomplete tactical contract, test intent, subsystem decomposition, or cross-scope interface.
- **Lich**: incorrect project topology, dependency direction, subsystem boundary, public seam, or whole-request decomposition.
- **Requirement/User**: conflicting binding requirements, missing decision or authority, or unavailable dependency.

Shade may recall an active or retired Vampire when direct review evidence identifies that tactical scope as responsible. Lich may require Vampire recalls after a strategic revision invalidates tactical assumptions. Codex executes and tracks all recalls.

A current Vampire may report a sibling conflict but does not independently reopen that sibling. Shade adjudicates a tactical or integration finding; Lich handles a strategic conflict.

When a separate Vampire context must be reestablished, Codex supplies a compact recall packet containing:

- stable Vampire scope identity;
- relevant current Lich draft and previous Vampire draft;
- finding ID, direct evidence, and retry state when applicable;
- changed assumptions or integration contracts;
- affected files, tests, Skeleton assignments, and invalidated passes;
- acceptance conditions for retirement;
- unrelated sibling scopes that must remain untouched.

Do not reload unrelated project history merely to recall a scope.

## Finding identity and isolated retries

Each critical finding receives a stable finding ID, scope path, judged item, root defect, and isolated retry counter. Do not pool retries across files, siblings, Vampires, phases, test suites, or the project.

Initial judged construction is attempt 0:

- The first Shade rejection immediately triggers retry 1.
- Rejection of retry 1 for the same finding immediately triggers retry 2.
- Rejection after retry 2 for that finding terminates the entire project as FAIL.

Renaming, rerouting, recalling a context, or discovering another symptom of the same root defect does not reset the counter.

Rerun only the affected branch from the responsible level:

- Skeleton finding: affected Skeleton work, then its Shade gate.
- Vampire finding: recalled or active Vampire draft, affected Skeleton descendants, Vampire gate, and implicated integration seam.
- Lich finding: Lich draft, affected Vampire scopes and descendants, then affected phase/project gates.
- Requirement/User finding: BLOCKED without consuming an implementation retry until input becomes available.

Upstream repair is intentionally more expensive because it invalidates more downstream assumptions. Unaffected siblings retain their passed state and counters.

## Orchestration state and completion accounting

For Adeptus mode, Codex maintains compact hierarchical work state linked to the mandatory session completion ledger. Together they contain:

- the complete requested outcomes and binding gates;
- the current Lich draft revision;
- all Vampire scopes, dependencies, and states;
- Skeleton assignments and states for active or recalled scopes;
- invalidated work requiring revalidation;
- Shade findings and isolated retry histories.

The plugin ledger is mandatory and remains outside the target. Use existing planning state for richer Lich, Vampire, and Skeleton detail when sufficient. Create another temporary or repository artifact only when it materially prevents state loss, and do not ship ceremonial process debris with the product.

When one item passes, schedule the next known ready item. Do not ask a parent responsibility a question whose answer is already in the current work state.

If requested work remains but no scope is ready, diagnose a dependency deadlock, missing decomposition, or external blocker. Do not silently stop.

Project PASS is allowed only when every binding acceptance item and required phase/project gate has passed with evidence and the ledger certifies PASS. Otherwise continue, certify a genuine BLOCKED state, or certify terminal retry failure; never present an honest partial foundation as completion.

## Token discipline

Spend tokens to prevent rework, not to describe work.

The hierarchy must remain proportional to task complexity:

- use Direct or Tactical mode when full hierarchy would be waste;
- read the full request at Lich level, then pass only relevant context downward;
- avoid repeating the complete specification in every handoff;
- keep Lich and Vampire drafts compact and actionable;
- combine tiny Skeleton assignments;
- keep Shade reports evidence-dense and short;
- preserve unaffected passed work and rerun only invalidated descendants;
- avoid repeated full-repository rereads;
- do not optimize token cost by omitting necessary code, tests, or verification.

For large tasks, a reasonable initial framing cost is justified only when it reduces user reprompting, architectural drift, missed requirements, or later rework. If hierarchy dominates the work without producing those benefits, collapse levels or simplify the process.

## Review outcomes

### Item or scope PASS

Include short reasoning, direct validation evidence, and trivial notes. Mark the item complete and continue orchestration if requested work remains.

### Routed FAIL

Include stable finding ID, scope path, judged item, root defect, responsible level, direct evidence, required repair, triggered retry number, and affected branch to rerun. Then continue the required repair automatically.

### Terminal FAIL

Use only when the same finding remains rejected after retry 2 and the ledger certifies FAIL. Include its complete attempt history and stop the project.

### BLOCKED

Use only when progress requires unavailable user input, authority, or an external dependency and the ledger certifies that it covers all unfinished work. Include what is missing, direct evidence, why safe progress cannot continue, and the narrowest action that would unblock it.

## Anti-patterns

Do not:

- let the Lich see only the next vertical slice of a larger request;
- confuse a Skeleton, Vampire, milestone, or phase PASS with project PASS;
- treat Lich or Vampire drafts as immutable requirements;
- silently disregard upstream drafts without propagating consequences;
- return to a parent responsibility for an already-known next action;
- stop after building a partial foundation when requested work remains;
- block merely because a request is broad enough to require decomposition;
- create an agent per role, file, or function without a real benefit;
- recall a Vampire for a trivial or speculative concern;
- restart unaffected sibling scopes after a local repair;
- pool or reset retry counters;
- accept tests, documentation, cleanup, UI, CLI, or process claims without checking the claimed boundary;
- spend more effort narrating the hierarchy than implementing and verifying the product.
