#!/usr/bin/env python3
"""Persistent completion state and terminal-policy validation for Adeptus."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
ITEM_STATES = {"pending", "active", "passed", "invalidated", "blocked"}
FINDING_STATES = {"open", "resolved", "rejected_after_retry_2"}
BLOCKER_STATES = {"open", "resolved"}


def session_state_path(plugin_data: str | os.PathLike[str], session_id: str) -> Path:
    """Return a traversal-safe, session-specific state path."""
    digest = hashlib.sha256(session_id.encode("utf-8")).hexdigest()[:24]
    return Path(plugin_data) / "sessions" / digest / "completion-state.json"


def new_state(session_id: str, cwd: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "session_id": session_id,
        "cwd": cwd,
        "active": True,
        "inventory_initialized": False,
        "request_title": "",
        "current_phase": "",
        "acceptance": [],
        "phase_gates": [],
        "findings": [],
        "blockers": [],
        "proposed_outcome": None,
        "terminal_finding_id": None,
        "terminal_blocker_id": None,
        "transition_log": [],
    }


def load_state(path: str | os.PathLike[str]) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError("completion state must be a JSON object")
    return value


def save_state(path: str | os.PathLike[str], state: dict[str, Any]) -> None:
    """Atomically replace state without leaving a partial JSON file."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(state, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def _evidence_present(record: dict[str, Any]) -> bool:
    evidence = record.get("evidence")
    return isinstance(evidence, list) and any(
        isinstance(entry, str) and entry.strip() for entry in evidence
    )


def _records_by_id(state: dict[str, Any], key: str) -> dict[str, dict[str, Any]]:
    records = state.get(key, [])
    if not isinstance(records, list):
        return {}
    return {
        record["id"]: record
        for record in records
        if isinstance(record, dict) and isinstance(record.get("id"), str)
    }


def _continue(reason: str, unfinished: list[str] | None = None) -> dict[str, Any]:
    return {
        "allow_stop": False,
        "reason": reason,
        "unfinished": unfinished or [],
    }


def evaluate_terminal(state: dict[str, Any]) -> dict[str, Any]:
    """Decide whether a terminal response is justified by the ledger."""
    if state.get("schema_version") != SCHEMA_VERSION:
        return _continue("completion-state schema is missing or unsupported")
    try:
        _validate_unique_ids(state)
    except ValueError as error:
        return _continue(f"completion-state structure is invalid: {error}")
    if not state.get("inventory_initialized"):
        return _continue("the binding acceptance inventory has not been initialized")

    acceptance = _records_by_id(state, "acceptance")
    gates = _records_by_id(state, "phase_gates")
    if not acceptance:
        return _continue("the binding acceptance inventory is empty")

    all_required = {**acceptance, **gates}
    unfinished = sorted(
        identifier
        for identifier, record in all_required.items()
        if record.get("state") != "passed" or not _evidence_present(record)
    )
    outcome = state.get("proposed_outcome")
    if outcome is None:
        return _continue(
            "no terminal outcome has been proposed; continue the next executable work",
            unfinished,
        )

    if outcome == "PASS":
        if unfinished:
            return _continue(
                "PASS requires every acceptance item and phase gate to be passed with direct evidence",
                unfinished,
            )
        open_critical = sorted(
            finding.get("id", "<unnamed>")
            for finding in state.get("findings", [])
            if isinstance(finding, dict)
            and finding.get("critical") is True
            and finding.get("state") != "resolved"
        )
        if open_critical:
            return _continue(
                "PASS is barred by unresolved critical findings", open_critical
            )
        open_blockers = sorted(
            blocker.get("id", "<unnamed>")
            for blocker in state.get("blockers", [])
            if isinstance(blocker, dict) and blocker.get("state") == "open"
        )
        if open_blockers:
            return _continue("PASS is barred by open blockers", open_blockers)
        return {"allow_stop": True, "outcome": "PASS", "reason": "all gates passed"}

    if outcome == "BLOCKED":
        if not unfinished:
            return _continue("BLOCKED requires genuinely unfinished work")
        blocker_id = state.get("terminal_blocker_id")
        blockers = _records_by_id(state, "blockers")
        blocker = blockers.get(blocker_id)
        if not blocker:
            return _continue("BLOCKED requires a selected, recorded blocker", unfinished)
        if blocker.get("state") != "open" or blocker.get("external") is not True:
            return _continue("BLOCKED requires a genuine open external blocker", unfinished)
        if not str(blocker.get("reason", "")).strip() or not str(
            blocker.get("unblock_action", "")
        ).strip():
            return _continue(
                "BLOCKED requires both evidence and a concrete unblock action", unfinished
            )
        if not _evidence_present(blocker):
            return _continue("BLOCKED requires direct evidence of the external blocker", unfinished)
        blocked_ids = set(blocker.get("blocks", []))
        unresolved_findings = {
            finding.get("id")
            for finding in state.get("findings", [])
            if isinstance(finding, dict)
            and finding.get("critical") is True
            and finding.get("state") != "resolved"
        }
        required_blocks = set(unfinished) | unresolved_findings
        if not required_blocks.issubset(blocked_ids):
            return _continue(
                "BLOCKED is invalid while executable unfinished requirements or critical findings remain",
                sorted(required_blocks - blocked_ids),
            )
        return {
            "allow_stop": True,
            "outcome": "BLOCKED",
            "reason": f"external blocker {blocker_id} covers all unfinished work",
        }

    if outcome == "FAIL":
        finding_id = state.get("terminal_finding_id")
        finding = _records_by_id(state, "findings").get(finding_id)
        if not finding:
            return _continue("terminal FAIL requires a selected, stable critical finding")
        stable_fields = ("scope_path", "judged_item", "root_defect")
        if any(not str(finding.get(key, "")).strip() for key in stable_fields):
            return _continue(
                "terminal FAIL requires the finding's stable scope, judged item, and root defect"
            )
        attempts = finding.get("attempts", [])
        attempt_numbers = {
            attempt.get("attempt")
            for attempt in attempts
            if isinstance(attempt, dict)
            and isinstance(attempt.get("evidence"), str)
            and attempt.get("evidence", "").strip()
        }
        if (
            finding.get("critical") is not True
            or finding.get("state") != "rejected_after_retry_2"
            or finding.get("retry_count") != 2
            or attempt_numbers != {0, 1, 2}
        ):
            return _continue(
                "terminal FAIL requires the same critical finding to be evidenced at attempt 0, retry 1, and retry 2"
            )
        return {
            "allow_stop": True,
            "outcome": "FAIL",
            "reason": f"critical finding {finding_id} remained after retry 2",
        }

    return _continue(f"unsupported terminal outcome: {outcome!r}", unfinished)


def _required_text(record: dict[str, Any], key: str, label: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} requires non-empty {key}")
    return value.strip()


def _validate_unique_ids(state: dict[str, Any]) -> None:
    seen: set[str] = set()
    for key in ("acceptance", "phase_gates", "findings", "blockers"):
        records = state.get(key, [])
        if not isinstance(records, list):
            raise ValueError(f"{key} must be a list")
        for record in records:
            if not isinstance(record, dict):
                raise ValueError(f"every {key} entry must be an object")
            identifier = _required_text(record, "id", key)
            if identifier in seen:
                raise ValueError(f"duplicate ledger ID: {identifier}")
            seen.add(identifier)


def initialize_inventory(state: dict[str, Any], inventory: dict[str, Any]) -> None:
    """Install a complete inventory while preserving hook-owned session metadata."""
    if not isinstance(inventory, dict):
        raise ValueError("inventory must be a JSON object")
    title = _required_text(inventory, "request_title", "inventory")
    acceptance = inventory.get("acceptance")
    gates = inventory.get("phase_gates", [])
    if not isinstance(acceptance, list) or not acceptance:
        raise ValueError("inventory acceptance must be a non-empty list")
    if not isinstance(gates, list):
        raise ValueError("inventory phase_gates must be a list")

    normalized_acceptance = []
    for record in acceptance:
        if not isinstance(record, dict):
            raise ValueError("every acceptance entry must be an object")
        normalized_acceptance.append(
            {
                **record,
                "id": _required_text(record, "id", "acceptance entry"),
                "description": _required_text(
                    record, "description", "acceptance entry"
                ),
                "state": record.get("state", "pending"),
                "evidence": record.get("evidence", []),
            }
        )
    normalized_gates = []
    for record in gates:
        if not isinstance(record, dict):
            raise ValueError("every phase gate entry must be an object")
        normalized_gates.append(
            {
                **record,
                "id": _required_text(record, "id", "phase gate"),
                "description": _required_text(record, "description", "phase gate"),
                "state": record.get("state", "pending"),
                "evidence": record.get("evidence", []),
            }
        )
    for record in normalized_acceptance + normalized_gates:
        if record["state"] not in ITEM_STATES:
            raise ValueError(f"invalid state for {record['id']}: {record['state']}")
        if not isinstance(record["evidence"], list):
            raise ValueError(f"evidence for {record['id']} must be a list")

    state.update(
        {
            "inventory_initialized": True,
            "request_title": title,
            "current_phase": inventory.get("current_phase", ""),
            "lich_revision": inventory.get("lich_revision", 1),
            "vampire_scopes": inventory.get("vampire_scopes", []),
            "acceptance": normalized_acceptance,
            "phase_gates": normalized_gates,
            "findings": [],
            "blockers": [],
            "proposed_outcome": None,
            "terminal_finding_id": None,
            "terminal_blocker_id": None,
            "transition_log": ["binding inventory initialized"],
        }
    )
    _validate_unique_ids(state)


def _record(state: dict[str, Any], collection: str, identifier: str) -> dict[str, Any]:
    record = _records_by_id(state, collection).get(identifier)
    if record is None:
        raise ValueError(f"unknown {collection} ID: {identifier}")
    return record


def _invalidate_proposal(state: dict[str, Any], log_entry: str) -> None:
    state["proposed_outcome"] = None
    state["terminal_finding_id"] = None
    state["terminal_blocker_id"] = None
    log = state.setdefault("transition_log", [])
    if isinstance(log, list):
        log.append(log_entry)
        if len(log) > 100:
            del log[:-100]


def set_required_item(
    state: dict[str, Any],
    collection: str,
    identifier: str,
    item_state: str,
    evidence: list[str],
) -> None:
    if item_state not in ITEM_STATES:
        raise ValueError(f"unsupported item state: {item_state}")
    record = _record(state, collection, identifier)
    existing = record.setdefault("evidence", [])
    if not isinstance(existing, list):
        raise ValueError(f"evidence for {identifier} is not a list")
    existing.extend(entry.strip() for entry in evidence if entry.strip())
    if item_state == "passed" and not _evidence_present(record):
        raise ValueError(f"passing {identifier} requires direct evidence")
    record["state"] = item_state
    _invalidate_proposal(state, f"{identifier} -> {item_state}")


def record_finding(state: dict[str, Any], args: argparse.Namespace) -> None:
    findings = state.setdefault("findings", [])
    finding = _records_by_id(state, "findings").get(args.id)
    if finding is None:
        finding = {
            "id": args.id,
            "critical": args.critical,
            "scope_path": args.scope_path,
            "judged_item": args.judged_item,
            "root_defect": args.root_defect,
            "state": "open",
            "retry_count": 0,
            "attempts": [],
        }
        findings.append(finding)
    else:
        for key, value in (
            ("scope_path", args.scope_path),
            ("judged_item", args.judged_item),
            ("root_defect", args.root_defect),
        ):
            if value and value != finding.get(key):
                raise ValueError(
                    f"finding {args.id} changed stable {key}; create a new finding ID"
                )
        if args.critical and finding.get("critical") is not True:
            raise ValueError(f"finding {args.id} changed critical identity")
    if args.attempt < 0 or args.attempt > 2:
        raise ValueError("attempt must be 0, 1, or 2")
    attempts = finding.setdefault("attempts", [])
    replacement = {"attempt": args.attempt, "evidence": args.evidence.strip()}
    if not replacement["evidence"]:
        raise ValueError("finding attempt requires direct evidence")
    previous = next(
        (attempt for attempt in attempts if attempt.get("attempt") == args.attempt), None
    )
    if previous is None:
        attempts.append(replacement)
    elif previous.get("evidence") != replacement["evidence"]:
        raise ValueError(
            f"finding {args.id} attempt {args.attempt} evidence is immutable"
        )
    finding["retry_count"] = max(finding.get("retry_count", 0), args.attempt)
    finding["state"] = args.status
    if args.status not in FINDING_STATES:
        raise ValueError(f"unsupported finding state: {args.status}")
    _validate_unique_ids(state)
    _invalidate_proposal(state, f"finding {args.id} attempt {args.attempt} -> {args.status}")


def record_blocker(state: dict[str, Any], args: argparse.Namespace) -> None:
    blockers = state.setdefault("blockers", [])
    blocker = _records_by_id(state, "blockers").get(args.id)
    value = {
        "id": args.id,
        "external": args.external,
        "state": args.status,
        "reason": args.reason.strip(),
        "unblock_action": args.unblock_action.strip(),
        "evidence": [entry.strip() for entry in args.evidence if entry.strip()],
        "blocks": sorted(set(args.blocks)),
    }
    if not value["reason"] or not value["unblock_action"] or not value["evidence"]:
        raise ValueError("blocker requires a reason, direct evidence, and unblock action")
    if value["state"] not in BLOCKER_STATES:
        raise ValueError(f"unsupported blocker state: {value['state']}")
    if blocker is None:
        blockers.append(value)
    else:
        blocker.update(value)
    _validate_unique_ids(state)
    _invalidate_proposal(state, f"blocker {args.id} -> {args.status}")


def advance_phase(state: dict[str, Any], gate_id: str, next_phase: str) -> None:
    gate = _record(state, "phase_gates", gate_id)
    if gate.get("state") != "passed" or not _evidence_present(gate):
        raise ValueError(f"phase gate {gate_id} has not passed with direct evidence")
    current = state.get("current_phase")
    if not isinstance(current, str) or not current.strip():
        raise ValueError("current_phase must be set before advancing a phase")
    if not next_phase.strip() or next_phase == current:
        raise ValueError("next phase must be non-empty and different from current_phase")
    if gate.get("phase") not in (None, current):
        raise ValueError(f"phase gate {gate_id} does not govern {current}")
    current_records = [
        record
        for record in state.get("acceptance", [])
        if record.get("phase") == current
    ]
    if not current_records:
        raise ValueError(f"no acceptance items are assigned to current phase {current}")
    unfinished = [
        record["id"]
        for record in current_records
        if record.get("state") != "passed" or not _evidence_present(record)
    ]
    if unfinished:
        raise ValueError(
            f"cannot leave {current}; unfinished phase acceptance: {', '.join(unfinished)}"
        )
    state["current_phase"] = next_phase
    _invalidate_proposal(state, f"phase {current} -> {next_phase} through {gate_id}")


def propose_outcome(
    state: dict[str, Any], outcome: str, finding_id: str | None, blocker_id: str | None
) -> dict[str, Any]:
    state["proposed_outcome"] = outcome
    state["terminal_finding_id"] = finding_id
    state["terminal_blocker_id"] = blocker_id
    decision = evaluate_terminal(state)
    if not decision["allow_stop"]:
        state["proposed_outcome"] = None
        state["terminal_finding_id"] = None
        state["terminal_blocker_id"] = None
        raise ValueError(decision["reason"])
    state.setdefault("transition_log", []).append(f"terminal {outcome} certified")
    return decision


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Maintain and validate an Adeptus session completion ledger."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    initialize = commands.add_parser("init", help="initialize the binding inventory")
    initialize.add_argument("--state", required=True)
    initialize.add_argument("--inventory", required=True)

    for name, collection in (("set-item", "acceptance"), ("set-gate", "phase_gates")):
        command = commands.add_parser(name)
        command.set_defaults(collection=collection)
        command.add_argument("--state", required=True)
        command.add_argument("--id", required=True)
        command.add_argument("--status", choices=sorted(ITEM_STATES), required=True)
        command.add_argument("--evidence", action="append", default=[])

    finding = commands.add_parser("record-finding")
    finding.add_argument("--state", required=True)
    finding.add_argument("--id", required=True)
    finding.add_argument("--critical", action="store_true")
    finding.add_argument("--scope-path", required=True)
    finding.add_argument("--judged-item", required=True)
    finding.add_argument("--root-defect", required=True)
    finding.add_argument("--attempt", required=True, type=int)
    finding.add_argument("--evidence", required=True)
    finding.add_argument("--status", choices=sorted(FINDING_STATES), required=True)

    blocker = commands.add_parser("record-blocker")
    blocker.add_argument("--state", required=True)
    blocker.add_argument("--id", required=True)
    blocker.add_argument("--external", action="store_true")
    blocker.add_argument("--reason", required=True)
    blocker.add_argument("--unblock-action", required=True)
    blocker.add_argument("--evidence", action="append", required=True)
    blocker.add_argument("--blocks", action="append", default=[])
    blocker.add_argument("--status", choices=sorted(BLOCKER_STATES), required=True)

    phase = commands.add_parser("advance-phase")
    phase.add_argument("--state", required=True)
    phase.add_argument("--gate", required=True)
    phase.add_argument("--to", required=True)

    propose = commands.add_parser("propose")
    propose.add_argument("--state", required=True)
    propose.add_argument("--outcome", choices=("PASS", "BLOCKED", "FAIL"), required=True)
    propose.add_argument("--finding-id")
    propose.add_argument("--blocker-id")

    check = commands.add_parser("check")
    check.add_argument("--state", required=True)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        state = load_state(args.state)
        decision: dict[str, Any] | None = None
        if args.command == "init":
            with Path(args.inventory).open("r", encoding="utf-8") as stream:
                initialize_inventory(state, json.load(stream))
        elif args.command in {"set-item", "set-gate"}:
            set_required_item(state, args.collection, args.id, args.status, args.evidence)
        elif args.command == "record-finding":
            record_finding(state, args)
        elif args.command == "record-blocker":
            record_blocker(state, args)
        elif args.command == "advance-phase":
            advance_phase(state, args.gate, args.to)
        elif args.command == "propose":
            decision = propose_outcome(
                state, args.outcome, args.finding_id, args.blocker_id
            )
        elif args.command == "check":
            decision = evaluate_terminal(state)
            print(json.dumps(decision, indent=2, sort_keys=True))
            return 0 if decision["allow_stop"] else 2
        if args.command != "check":
            save_state(args.state, state)
            if decision is not None:
                print(json.dumps(decision, indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.exit(2, f"error: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
