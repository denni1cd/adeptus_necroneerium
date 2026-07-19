#!/usr/bin/env python3
"""Codex hook that activates and enforces the Adeptus completion guard."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any


PLUGIN_ROOT = Path(os.environ.get("PLUGIN_ROOT", Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))

from adeptus_state import (  # noqa: E402
    evaluate_terminal,
    load_state,
    new_state,
    save_state,
    session_state_path,
)


INVOCATION = re.compile(
    r"[@$]adeptus-necroneerium\b|\badeptus_necroneerium\b|"
    r"^\s*(?:please\s+)?adeptus\s+necroneerium\b|"
    r"\b(?:use|invoke|run|activate|apply|with)\s+(?:the\s+)?adeptus\s+necroneerium\b",
    re.IGNORECASE,
)
ABORT = re.compile(
    r"^\s*(?:[@$]adeptus-necroneerium|adeptus_necroneerium)\s+abort\s*[.!]?\s*$",
    re.IGNORECASE,
)


def _emit(value: dict[str, Any]) -> None:
    json.dump(value, sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")


def _user_prompt_context(message: str) -> dict[str, Any]:
    """Return the current Codex UserPromptSubmit context envelope."""
    return {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": message,
        }
    }


def _read_input() -> dict[str, Any]:
    value = json.load(sys.stdin)
    if not isinstance(value, dict):
        raise ValueError("hook input must be an object")
    return value


def _state_path(payload: dict[str, Any]) -> Path | None:
    plugin_data = os.environ.get("PLUGIN_DATA")
    session_id = payload.get("session_id")
    if not plugin_data or not isinstance(session_id, str) or not session_id:
        return None
    return session_state_path(plugin_data, session_id)


def on_user_prompt(payload: dict[str, Any]) -> None:
    prompt = payload.get("prompt", "")
    state_path = _state_path(payload)
    if isinstance(prompt, str) and ABORT.match(prompt) and state_path is not None:
        if state_path.exists():
            state = load_state(state_path)
            state["active"] = False
            state["user_cancelled"] = True
            save_state(state_path, state)
        _emit(
            _user_prompt_context(
                "The user explicitly aborted the active Adeptus run. The completion "
                "guard is disabled for this session until a new explicit invocation."
            )
        )
        return
    if not isinstance(prompt, str) or not INVOCATION.search(prompt):
        _emit({})
        return
    if state_path is None:
        _emit(
            _user_prompt_context(
                "Adeptus invocation detected, but its session completion state "
                "could not be created. Do not begin target writes; report this hook failure."
            )
        )
        return
    if state_path.exists():
        state = load_state(state_path)
        if not state.get("active", True):
            state = new_state(payload["session_id"], payload.get("cwd", ""))
            save_state(state_path, state)
    else:
        state = new_state(payload["session_id"], payload.get("cwd", ""))
        save_state(state_path, state)
    receipt_path = state_path.with_name("activation-receipt.json")
    save_state(
        receipt_path,
        {
            "event": "UserPromptSubmit",
            "guard_active": True,
            "session_id": payload["session_id"],
            "state_path": str(state_path),
            "state_tool_path": str(PLUGIN_ROOT / "scripts" / "adeptus_state.py"),
        },
    )
    _emit(
        _user_prompt_context(
            "ADEPTUS COMPLETION GUARD IS ACTIVE. Its session ledger is "
            f"{state_path}, and its activation receipt is {receipt_path}. Before target "
            "writes, initialize the binding acceptance inventory with "
            f"{PLUGIN_ROOT / 'scripts' / 'adeptus_state.py'}. Keep it current as evidence, "
            "gates, findings, and blockers change. A Stop hook will reject final output "
            "unless PASS, BLOCKED, or terminal FAIL is mechanically justified by that ledger."
        )
    )


def on_stop(payload: dict[str, Any]) -> None:
    state_path = _state_path(payload)
    if state_path is None or not state_path.exists():
        _emit({})
        return
    try:
        state = load_state(state_path)
        if not state.get("active", True):
            _emit({})
            return
        decision = evaluate_terminal(state)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        _emit(
            {
                "decision": "block",
                "reason": (
                    "Adeptus completion state is unreadable. Repair the session ledger "
                    f"at {state_path} and continue. Error: {error}"
                ),
            }
        )
        return
    if decision["allow_stop"]:
        state["active"] = False
        state["terminal_certificate"] = decision
        save_state(state_path, state)
        _emit({})
        return
    unfinished = ", ".join(decision.get("unfinished", [])) or "not yet enumerated"
    _emit(
        {
            "decision": "block",
            "reason": (
                "Adeptus terminal conditions are not satisfied: "
                f"{decision['reason']}. Unfinished: {unfinished}. Continue executing "
                "the next feasible acceptance item; do not summarize this as a terminal result."
            ),
        }
    )


def main() -> None:
    payload = _read_input()
    event_name = payload.get("hook_event_name")
    try:
        if event_name == "UserPromptSubmit":
            on_user_prompt(payload)
        elif event_name == "Stop":
            on_stop(payload)
        else:
            _emit({})
    except (OSError, ValueError, json.JSONDecodeError) as error:
        if event_name == "Stop":
            _emit(
                {
                    "decision": "block",
                    "reason": (
                        "Adeptus completion guard failed closed. Repair or re-enable the "
                        f"guard before stopping. Error: {error}"
                    ),
                }
            )
        else:
            _emit(
                _user_prompt_context(
                    "Adeptus completion guard could not activate safely. Do not begin "
                    f"target writes. Repair the guard or report the external limitation. Error: {error}"
                )
            )


if __name__ == "__main__":
    main()
