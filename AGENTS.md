# Repository Guidance

## Mission

This repository develops Adeptus Necroneerium, a strictly on-demand Codex coding skill. Its purpose is to test whether hierarchical, revisable code drafts improve quality and total token efficiency over plain Codex without creating process bloat.

The skill entrypoint is `skills/adeptus-necroneerium/SKILL.md`. Keep the repository alias `adeptus_necroneerium` and registered skill name `adeptus-necroneerium` distinct where syntax requires it.

## Invocation boundary

Never invoke the skill implicitly. It runs only when the user explicitly requests Adeptus Necroneerium, writes `adeptus_necroneerium`, or invokes `@adeptus-necroneerium`.

## Canonical model

Codex is the orchestrator.

- One Lich reads the complete request and creates a whole-project strategic draft.
- The Lich may define many Vampire tactical scopes.
- Each Vampire may define many Skeleton implementation assignments.
- Shade reviews at Skeleton, Vampire, phase, and project resolution and may route or recall work backward.

Roles are responsibility labels, not mandatory separate agents or personalities. Use separate contexts only when they materially help the task.

Responsibility is hierarchical; code dependencies may form a DAG.

## Draft authority

User requirements, explicit acceptance criteria, safety constraints, and phase gates are binding.

Lich and Vampire outputs are drafts. Lower responsibilities may revise them without routine permission when evidence supports the change. Material consequences must be propagated to affected contracts, tests, dependencies, siblings, and review state. Do not silently drift, but do not lock implementation behind parent approval.

## Repository consistency

When changing the process, update every affected source of doctrine rather than patching only the installed skill:

- `README.md`;
- `docs/manifesto.md`;
- `docs/charter.md`;
- `docs/skill-outline.md`;
- `skills/adeptus-necroneerium/SKILL.md`;
- relevant role guides and templates;
- `agents/openai.yaml` when invocation metadata changes.
- `.codex-plugin/plugin.json`, hook behavior, ledger tooling, and policy tests when terminal enforcement changes.

Search for contradictory legacy wording after edits. In particular, the Lich must never be reduced to planning only the next vertical slice, and a local PASS must never imply project completion.

## Working-code discipline

Every meaningful process output must become code, tests, embedded contracts, executable validation, compact orchestration state, or a genuine blocker. Avoid long unused plans, repeated restatement, identity setup, review theater, and reports that downstream work does not consume.

Quality and total token efficiency outrank speed. Use the lightest mode appropriate to the invoked task and do not manufacture role or agent boundaries for tiny work.

## Review discipline

Shade must test claims at the boundary being claimed. Generated tests do not prove UI, CLI, API, subprocess, persistence, restart, concurrency, documentation, or cleanup behavior when they bypass that boundary.

Run README commands verbatim. Perform cleanup scans after the final artifact-generating command. State unverified requirements honestly.

Critical findings keep stable IDs and isolated counters: attempt 0, retry 1 after first rejection, retry 2 after the second, and terminal project FAIL after rejection of retry 2. Recalls and reroutes never reset counters.

The session completion guard is part of the doctrine, not optional packaging. Keep invocation detection opt-in, state outside the target, writes atomic, non-Adeptus sessions untouched, and terminal PASS/BLOCKED/FAIL mechanically consistent with the installed skill.
