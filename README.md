# Adeptus Necroneerium

Adeptus Necroneerium is a strictly on-demand Codex plugin and coding skill for completing substantial software requests through hierarchical, revisable code drafts and evidence-based review.

It exists to test whether a structured run can deliver better quality, evolvability, review honesty, and total token efficiency than plain Codex—especially by reducing architectural drift, rework, false PASS claims, and user reprompting.

The canonical project doctrine and hierarchy diagram are in [the manifesto](docs/manifesto.md).

## Invocation

The skill must never activate implicitly. Use it only when the user explicitly requests Adeptus Necroneerium, writes `adeptus_necroneerium`, or invokes `@adeptus-necroneerium` (the native `$adeptus-necroneerium` form is also recognized).

The registered skill name is `adeptus-necroneerium`; the repository and prompt alias may use `adeptus_necroneerium`.

## Core model

Codex is the orchestrator. Role names identify responsibilities and do not require separate personalities, roleplay, or agent contexts.

- **One Lich** reads the complete request and drafts the whole-project strategic topology, acceptance coverage, integration seams, and Vampire scope graph.
- **Many Vampires** may each draft one coherent tactical subsystem, including contracts, tests, and Skeleton assignments.
- **Many Skeletons** may each implement one bounded unit, usually a file and all relevant stubs or a tightly coupled implementation-and-test unit.
- **Shade** reviews Skeleton items, integrated Vampire scopes, phase gates, and the final project; routes failures backward; and may recall retired Vampires when direct evidence requires it.

Responsibility forms a hierarchy. Software dependencies may form a DAG that Codex schedules from the current drafts.

## Drafts, not decrees

Lich and Vampire outputs guide downstream work but are not immutable requirements. Lower responsibilities may revise them without routine parent approval when implementation evidence supports a safer, simpler, or more correct design.

Material changes must be propagated to affected contracts, tests, dependencies, siblings, and validation state. User requirements, explicit acceptance criteria, safety constraints, and phase gates remain binding.

A normal draft revision is not a retry. Shade rejection of a critical judged finding begins its isolated retry sequence.

## Mechanical completion guard

The plugin packages a session-scoped completion ledger and [Codex Stop hook](https://learn.chatgpt.com/docs/hooks). Explicit invocation activates the guard. The hook adds the ledger and state-tool paths to Codex context before target writes and rejects a final response until one of these conditions is mechanically evidenced:

- **PASS:** every binding acceptance item and required phase gate is passed with direct evidence, with no unresolved critical finding or open blocker;
- **BLOCKED:** a recorded open external blocker covers every unfinished item and unresolved critical finding, and names the narrowest unblock action;
- **FAIL:** the same stable critical finding has evidenced rejections at attempt 0, retry 1, and retry 2.

An ordinary Codex session creates no ledger and its Stop event is untouched. Active state lives under the plugin data directory, not in the target repository. A successful terminal check seals that session ledger. The user can explicitly cancel a run with `@adeptus-necroneerium abort`; disabling the hook through `/hooks` is the administrative escape hatch.

Installing or enabling the plugin does not automatically trust its executable hooks. After each new or changed hook definition, open `/hooks`, review both plugin-bundled hooks, and explicitly trust them before starting the test in a new thread. Codex skips an untrusted hook, so an invocation is not proven active unless the injected context names the session ledger and state tool. A successful activation also writes `activation-receipt.json` beside the session ledger in the plugin data directory for diagnosis outside the target.

Before an expensive run, submit exactly `@adeptus-necroneerium probe` in a disposable fresh thread. A working `UserPromptSubmit` hook injects `ADEPTUS COMPLETION GUARD PROBE PASSED`, writes a probe receipt in plugin data, and deliberately leaves the completion ledger and Stop guard inactive. If that message is absent, inspect `/hooks` rather than starting product work.

The hook is a lifecycle guard, not a substitute for implementation judgment. Codex still has to construct the complete acceptance inventory, update it honestly, execute work, and gather direct evidence. Hook source should be reviewed before enabling the plugin, as with any executable repository content.

## Forward construction and backward review

Codex normally activates one dependency-ready Vampire at a time. Its Skeleton army implements the tactical draft, Shade reviews the items and integrated subsystem, and Codex retires the Vampire after PASS before activating the next ready scope.

Passing a Skeleton, Vampire, milestone, or phase is intermediate progress when requested work remains. Codex must continue without asking a parent responsibility for an already-known next action.

Shade routes critical findings to the lowest responsible level:

- Skeleton implementation;
- Vampire tactical contract or subsystem design;
- Lich strategic topology or decomposition;
- user requirement or external dependency.

Retired Vampires are inactive, not sealed. Shade may recall one for a verified tactical or integration defect; Lich may require recall after a strategic revision. Recalls preserve scope identity, finding identity, retry state, and unaffected sibling work.

## Retry rule

Initial judged work is attempt 0. The first Shade rejection triggers retry 1. Rejection of retry 1 triggers retry 2. Rejection after retry 2 for the same finding terminates the entire project.

Counters are isolated by stable finding and scope path. They are never pooled across siblings, Vampires, phases, test suites, or the project. An upstream repair reruns only affected descendants and integration seams.

## Cost discipline

> Working code over comprehensive agent artifacts.

Quality and total token efficiency matter more than speed. The hierarchy is justified only when it reduces rework, missed requirements, drift, false claims, or user intervention.

Use Direct or Tactical mode for smaller tasks. In Adeptus mode, keep Lich and Vampire drafts compact, pass only relevant context downward, combine tiny Skeleton assignments, keep Shade reports evidence-dense, and preserve unaffected passed work.

Do not save tokens by omitting necessary code, tests, or verification. Save them by eliminating repeated interpretation, full-context reloads, ceremonial reports, needless handoffs, and broad reruns.

## Repository

- `skills/adeptus-necroneerium/SKILL.md`: installed skill entrypoint and complete operating rules.
- `skills/adeptus-necroneerium/roles/`: focused role references.
- `skills/adeptus-necroneerium/templates/spec.md`: optional working-state template for substantial runs.
- `docs/manifesto.md`: project doctrine and hierarchy diagram.
- `docs/charter.md`: purpose, boundaries, and success criteria.
- `docs/skill-outline.md`: design reference for the nested lifecycle.
- `.codex-plugin/plugin.json`: plugin manifest.
- `hooks/hooks.json` and `hooks/adeptus_hook.py`: opt-in activation and terminal enforcement.
- `scripts/adeptus_state.py`: atomic ledger updates and terminal-policy validation.
- `tests/test_completion_guard.py`: executable policy and hook tests.

## Development verification

From the repository root, run:

```text
python3 -m unittest discover -s tests -v
python3 -m compileall -q hooks scripts tests
```

On Windows, `py -3` may replace `python3`. Plugin maintainers should also run the current plugin and skill validators supplied with their Codex development environment.

## Success criterion

Adeptus Necroneerium matters only if controlled practical tests show a meaningful advantage over plain Codex. If it cannot improve delivered quality, evolvability, review accuracy, or total interaction cost, simplify or abandon it.
