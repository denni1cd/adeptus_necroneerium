# Adeptus Necroneerium Design Outline

## One-sentence definition

Codex completes a substantial coding request by orchestrating one whole-project Lich draft, multiple Vampire subsystem drafts, their Skeleton implementation assignments, and evidence-based Shade gates that route defects backward without discarding unaffected work.

## Invocation and modes

The plugin and skill are strictly opt-in. After explicit invocation, Codex chooses the lightest safe mode:

- **Direct:** obvious bounded implementation and direct validation.
- **Tactical:** one Vampire scope with one or more Skeleton assignments and Shade gates.
- **Adeptus:** one Lich, multiple Vampire scopes as warranted, nested Skeleton work, recalls, phase gates, and final integrated review.

Do not force Adeptus mode onto work whose risk does not justify the hierarchy.

## Authority model

Binding authority belongs to the user's requested outcomes, explicit constraints, acceptance criteria, safety requirements, and phase gates.

Internal outputs are revisable drafts:

- Lich drafts strategic topology and scope decomposition by creating or revising actual repository structure and strategic code seams.
- Vampire drafts tactical contracts and work decomposition by writing actual signatures, types, schemas, docstrings, exceptions, and test skeletons.
- Skeleton drafts and implements local details.
- Tests generated from internal drafts remain subject to Shade's independent comparison with user acceptance.

Lower responsibilities may revise upstream drafts without routine approval when evidence supports the change. They must propagate effects to the current shared design and revalidate invalidated work.

## Nested construction lifecycle

### Whole-project Lich pass

Read the complete request. Create a breadth-complete strategic draft containing acceptance coverage, proposed topology, public seams, Vampire scopes, dependency order, phase gates, and high-risk integration assumptions. Materialize it in the repository through strategic-resolution code structure rather than a prose-only plan.

The Lich must not stop at the next vertical slice. It anticipates future phases without implementing them before binding gates permit it.

### Vampire activation

Codex selects a dependency-ready Vampire scope, normally one at a time. The Vampire creates the complete tactical draft for that subsystem as executable skeleton code: files, contracts, tests, edge cases, cross-scope interfaces, Skeleton assignments, and retirement conditions.

### Skeleton execution

Codex executes cohesive Skeleton assignments in dependency order. A Skeleton normally owns one file and its relevant stubs, or a tightly coupled implementation-and-test unit. Tiny assignments should be combined when separation adds no quality.

Each item receives a focused Shade gate. A PASS marks intermediate progress and Codex immediately schedules the next known item.

### Vampire integration and retirement

After all required Skeleton items pass, Shade verifies the complete subsystem and implicated seams. Codex retires the Vampire after PASS and activates the next ready scope.

Retirement is reversible through evidence-based recall.

### Phase and project gates

Shade verifies each binding phase checkpoint and the final integrated product against the complete acceptance inventory. Codex continues automatically across requested phases unless genuinely blocked.

## Dependency model

The ownership structure is hierarchical, but implementation dependencies may form a DAG. The Lich drafts cross-scope seams. Codex tracks readiness and invalidation.

If work remains but nothing is dependency-ready, Codex diagnoses missing decomposition, a dependency cycle, or an external blocker rather than stopping silently.

## Draft revision

Free revision prevents early guesses from becoming expensive constraints. Propagation prevents free revision from becoming uncontrolled drift.

A material revision records only what downstream execution needs:

- evidence or reason;
- changed draft or contract;
- affected consumers or siblings;
- invalidated passed work;
- required revalidation.

Normal revision is not a retry. Shade rejection is.

## Shade gates and backward routing

Shade reviews:

1. each Skeleton implementation unit;
2. each integrated Vampire subsystem;
3. required phase checkpoints;
4. the final project.

Shade routes a critical finding to the lowest responsible level:

- Skeleton behavior;
- Vampire tactical contract or subsystem decomposition;
- Lich topology or whole-request decomposition;
- user requirement or external dependency.

Shade judges observed acceptance, not conformance to an internal draft alone.

## Vampire recall

Shade may recall an active or retired Vampire for a directly evidenced tactical or integration defect. Lich may require recall after strategic revision. Codex executes the recall with a compact packet containing stable scope identity, relevant current and previous drafts, finding evidence, retry state, invalidated descendants, preserved siblings, and retirement conditions.

A current Vampire may report a sibling conflict but does not reopen the sibling without Shade adjudication or Lich revision.

## Isolated retry semantics

Initial judged work is attempt 0. First rejection triggers retry 1. Rejection of retry 1 triggers retry 2. Rejection after retry 2 for the same finding terminates the project.

Every critical finding retains a stable ID, scope path, judged item, root defect, and independent counter. Recalls, reroutes, renamed symptoms, and new contexts never reset it.

Only the affected branch reruns:

- Skeleton finding: Skeleton and its Shade gate.
- Vampire finding: Vampire, invalidated Skeleton descendants, Vampire gate, and implicated seams.
- Lich finding: Lich, invalidated Vampire branches and descendants, then affected higher gates.
- Requirement finding: BLOCKED until input exists, without consuming an implementation retry.

## Completion accounting

Large Adeptus runs maintain compact orchestration state containing the complete acceptance inventory, Lich draft revision, Vampire graph, active Skeleton assignments, invalidated work, Shade findings, and retry histories.

The following are nonterminal while requested work remains:

- working vertical slice;
- Skeleton PASS;
- Vampire PASS;
- milestone PASS;
- phase PASS.

Project terminal outcomes are:

- PASS after every binding item and gate passes;
- BLOCKED for genuinely unavailable input, authority, or dependency covering all unfinished work and unresolved critical findings;
- terminal FAIL after rejection of retry 2 for one stable finding.

## Evidence standards

Shade verifies claims at the boundary claimed. Run README commands verbatim. Exercise real UI, CLI, API, storage, process, restart, scheduling, and concurrency behavior when claimed. Scan cleanup only after the last command capable of regenerating debris. State unverified requirements explicitly.

## Token discipline

Quality and total token efficiency outrank speed.

- Read the complete specification once at Lich level.
- Pass scoped context downward instead of restating the project.
- Keep drafts actionable and compact.
- Avoid an agent or report per function.
- Preserve passed work and rerun only invalidated descendants.
- Collapse to a lighter mode when hierarchy costs more than the risk it prevents.
- Never save tokens by omitting necessary code, tests, or direct verification.

The hierarchy succeeds only when its framing cost is repaid through reduced drift, rework, false claims, or user reprompting.
