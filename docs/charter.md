# Project Charter: Adeptus Necroneerium

## Purpose

Adeptus Necroneerium is an experiment in hierarchical, draft-guided coding. It asks whether Codex can complete substantial software requests with higher quality and reasonable total token cost by shaping code at progressively finer resolution before implementation and reviewing failures backward at the lowest responsible level.

The target is not maximum speed. The target is fewer user corrections, less rework, better architecture, stronger verification, and honest completion claims.

## Scope

The project provides a strictly on-demand Codex plugin and skill. It is not a council, debate framework, roleplay system, or mandatory multi-agent runtime.

Codex is always the orchestrator. Named roles describe responsibility:

- one Lich for the complete strategic project draft;
- multiple Vampire scopes for coherent tactical subsystems;
- multiple Skeleton assignments within each Vampire scope;
- Shade review at implementation, subsystem, phase, and project resolution.

## Core commitments

- Working code over comprehensive agent artifacts.
- One Lich sees the complete request, including all phases.
- Broad work is decomposed rather than mistaken for a blocker.
- Strategic and tactical outputs are revisable drafts, not decrees.
- Lower responsibilities may improve drafts without routine approval and must propagate material consequences.
- User requirements and explicit acceptance gates outrank internal drafts.
- Codex advances known ready work without unnecessary parent callbacks.
- A local or phase PASS is not project PASS while requested work remains.
- Shade verifies real boundaries, routes failures backward, and may recall retired Vampires.
- Critical findings have stable identities and isolated two-retry budgets.
- A session-scoped Stop hook mechanically enforces terminal conditions after explicit invocation.
- Completion state is atomic, fails closed, and remains outside the target repository.
- Quality and total token efficiency outrank speed and maximum concurrency.
- The skill remains strictly opt-in.

## Structural model

The responsibility model is a tree: one Lich, many Vampires, and many Skeleton assignments under each Vampire. The implementation model may be a dependency DAG. Codex maintains both the hierarchy and dependency state.

The Lich drafts complete breadth without predicting private details. Vampires add subsystem depth just before implementation. Skeletons complete cohesive units. Shade evaluates each resolution against direct evidence and binding user outcomes.

## Draft governance

Drafts are strong defaults intended to save downstream reasoning. They are useful only when they materially guide implementation.

Lower responsibilities may revise them when code or tests reveal better information. No approval ceremony is required. The change must be explicit enough for Codex to update affected contracts, tests, dependencies, passed-state invalidation, and review coverage.

Normal draft evolution does not consume a retry. A critical Shade rejection does.

## Recall and repair

A Vampire becomes inactive after its integrated subsystem passes. Shade may recall it for a verified tactical or integration defect. Lich may require recall after a strategic revision. Codex reestablishes only the necessary context and preserves scope identity, retry history, unaffected siblings, and prior evidence.

Repairs rerun from the lowest responsible level through affected descendants only. Rejection after retry 2 for the same stable finding terminates the project.

## Terminal authority

Codex may propose PASS, BLOCKED, or terminal FAIL, but the plugin's completion validator decides whether the evidence permits the session to stop. PASS requires all acceptance items and gates. BLOCKED requires a genuine external condition that covers every unfinished item and unresolved critical finding. FAIL requires one stable critical finding rejected at attempt 0, retry 1, and retry 2.

Incomplete, corrupt, or stale active ledger state is nonterminal. The Stop hook returns a concrete continuation reason instead of allowing an honest partial implementation to become the terminal result. The user retains authority to abort explicitly or administratively disable hooks.

## Cost philosophy

The hierarchy may spend more tokens initially than direct coding only when that investment reasonably prevents later drift, rework, missed acceptance criteria, false claims, or user reprompting.

Cost savings must come from reducing waste—not truncating code, tests, or necessary verification. Avoid repeated specification restatement, tiny agent assignments, full-context reloads, narrative handoffs, and broad reruns of unaffected work.

## Evaluation

Compare Adeptus Necroneerium against plain Codex and useful ablations on realistic multi-stage tasks. Measure:

- acceptance coverage and functional correctness;
- preservation of existing behavior;
- architecture and evolvability;
- review honesty and false PASS rate;
- documentation and cleanup accuracy;
- user interventions and reprompts;
- rework and backward-routing cost;
- total token use relative to accepted functionality.

If the hierarchy cannot demonstrate practical value, simplify or abandon it.
