from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from adeptus_state import (
    advance_phase,
    evaluate_terminal,
    initialize_inventory,
    new_state,
    save_state,
    session_state_path,
)


class TerminalPolicyTests(unittest.TestCase):
    @staticmethod
    def complete_state() -> dict[str, object]:
        state = new_state("session", "/target")
        state.update(
            {
                "inventory_initialized": True,
                "acceptance": [
                    {"id": "A1", "state": "passed", "evidence": ["test exited 0"]},
                ],
                "phase_gates": [
                    {"id": "G1", "state": "passed", "evidence": ["checkpoint"]},
                ],
            }
        )
        return state

    def test_unfinished_inventory_refuses_stop(self) -> None:
        state = new_state("session", "/target")
        state.update(
            {
                "inventory_initialized": True,
                "acceptance": [
                    {"id": "A1", "state": "pending", "evidence": []},
                ],
                "proposed_outcome": "PASS",
            }
        )
        decision = evaluate_terminal(state)
        self.assertFalse(decision["allow_stop"])
        self.assertEqual(decision["unfinished"], ["A1"])

    def test_evidenced_complete_inventory_allows_pass(self) -> None:
        state = self.complete_state()
        state["proposed_outcome"] = "PASS"
        decision = evaluate_terminal(state)
        self.assertTrue(decision["allow_stop"])
        self.assertEqual(decision["outcome"], "PASS")

    def test_pass_rejects_claim_without_direct_evidence(self) -> None:
        state = self.complete_state()
        state["acceptance"][0]["evidence"] = []
        state["proposed_outcome"] = "PASS"
        self.assertFalse(evaluate_terminal(state)["allow_stop"])

    def test_external_blocker_must_cover_every_unfinished_id(self) -> None:
        state = self.complete_state()
        state["acceptance"].append({"id": "A2", "state": "pending", "evidence": []})
        state.update(
            {
                "proposed_outcome": "BLOCKED",
                "terminal_blocker_id": "B1",
                "blockers": [
                    {
                        "id": "B1",
                        "state": "open",
                        "external": True,
                        "reason": "required service is unavailable",
                        "unblock_action": "restore the service",
                        "evidence": ["service probe failed from the required environment"],
                        "blocks": [],
                    }
                ],
            }
        )
        decision = evaluate_terminal(state)
        self.assertFalse(decision["allow_stop"])
        self.assertEqual(decision["unfinished"], ["A2"])
        state["blockers"][0]["blocks"] = ["A2"]
        self.assertTrue(evaluate_terminal(state)["allow_stop"])

    def test_internal_difficulty_is_not_a_blocker(self) -> None:
        state = self.complete_state()
        state["acceptance"][0].update({"state": "pending", "evidence": []})
        state.update(
            {
                "proposed_outcome": "BLOCKED",
                "terminal_blocker_id": "B1",
                "blockers": [
                    {
                        "id": "B1",
                        "state": "open",
                        "external": False,
                        "reason": "work is large",
                        "unblock_action": "continue decomposing it",
                        "evidence": ["the request contains multiple subsystems"],
                        "blocks": ["A1"],
                    }
                ],
            }
        )
        self.assertFalse(evaluate_terminal(state)["allow_stop"])

    def test_fail_requires_three_evidenced_attempts_for_same_finding(self) -> None:
        state = self.complete_state()
        state.update(
            {
                "proposed_outcome": "FAIL",
                "terminal_finding_id": "F1",
                "findings": [
                    {
                        "id": "F1",
                        "critical": True,
                        "scope_path": "V1/S1",
                        "judged_item": "critical behavior",
                        "root_defect": "stable defect",
                        "state": "rejected_after_retry_2",
                        "retry_count": 2,
                        "attempts": [
                            {"attempt": 0, "evidence": "first rejection"},
                            {"attempt": 1, "evidence": "second rejection"},
                        ],
                    }
                ],
            }
        )
        self.assertFalse(evaluate_terminal(state)["allow_stop"])
        state["findings"][0]["attempts"].append(
            {"attempt": 2, "evidence": "third rejection"}
        )
        self.assertTrue(evaluate_terminal(state)["allow_stop"])

    def test_phase_cannot_advance_before_its_items_and_gate_pass(self) -> None:
        state = new_state("session", "/target")
        initialize_inventory(
            state,
            {
                "request_title": "two phase test",
                "current_phase": "phase-1",
                "acceptance": [
                    {
                        "id": "A1",
                        "description": "phase one behavior",
                        "phase": "phase-1",
                    }
                ],
                "phase_gates": [
                    {
                        "id": "G1",
                        "description": "phase one checkpoint",
                        "state": "passed",
                        "evidence": ["direct checkpoint evidence"],
                    }
                ],
            },
        )
        with self.assertRaisesRegex(ValueError, "unfinished phase acceptance"):
            advance_phase(state, "G1", "phase-2")
        state["acceptance"][0].update(
            {"state": "passed", "evidence": ["phase one test exited 0"]}
        )
        advance_phase(state, "G1", "phase-2")
        self.assertEqual(state["current_phase"], "phase-2")

    def test_blocked_must_cover_an_open_critical_finding_too(self) -> None:
        state = self.complete_state()
        state["acceptance"][0].update({"state": "pending", "evidence": []})
        state.update(
            {
                "proposed_outcome": "BLOCKED",
                "terminal_blocker_id": "B1",
                "findings": [{"id": "F1", "critical": True, "state": "open"}],
                "blockers": [
                    {
                        "id": "B1",
                        "state": "open",
                        "external": True,
                        "reason": "external runner unavailable",
                        "unblock_action": "restore the runner",
                        "evidence": ["runner probe failed"],
                        "blocks": ["A1"],
                    }
                ],
            }
        )
        decision = evaluate_terminal(state)
        self.assertFalse(decision["allow_stop"])
        self.assertEqual(decision["unfinished"], ["F1"])
        state["blockers"][0]["blocks"].append("F1")
        self.assertTrue(evaluate_terminal(state)["allow_stop"])

    def test_inventory_rejects_duplicate_ids(self) -> None:
        state = new_state("session", "/target")
        with self.assertRaisesRegex(ValueError, "duplicate ledger ID"):
            initialize_inventory(
                state,
                {
                    "request_title": "bad inventory",
                    "acceptance": [{"id": "X", "description": "one"}],
                    "phase_gates": [{"id": "X", "description": "duplicate"}],
                },
            )


class StopHookPrototypeTests(unittest.TestCase):
    def run_hook(self, plugin_data: str, payload: dict[str, object]) -> dict[str, object]:
        environment = os.environ.copy()
        environment.update({"PLUGIN_ROOT": str(ROOT), "PLUGIN_DATA": plugin_data})
        result = subprocess.run(
            [sys.executable, str(ROOT / "hooks" / "adeptus_hook.py")],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            env=environment,
            check=True,
        )
        return json.loads(result.stdout)

    def test_stop_hook_blocks_then_allows_a_certified_pass(self) -> None:
        with tempfile.TemporaryDirectory() as plugin_data:
            path = session_state_path(plugin_data, "s-1")
            state = new_state("s-1", "/target")
            state.update(
                {
                    "inventory_initialized": True,
                    "acceptance": [{"id": "A1", "state": "pending", "evidence": []}],
                    "proposed_outcome": "PASS",
                }
            )
            save_state(path, state)
            payload = {"hook_event_name": "Stop", "session_id": "s-1", "cwd": "/target"}
            blocked = self.run_hook(plugin_data, payload)
            self.assertEqual(blocked["decision"], "block")

            state["acceptance"][0].update(
                {"state": "passed", "evidence": ["direct boundary check exited 0"]}
            )
            save_state(path, state)
            allowed = self.run_hook(plugin_data, payload)
            self.assertEqual(allowed, {})
            self.assertFalse(json.loads(path.read_text(encoding="utf-8"))["active"])

    def test_non_adeptus_stop_is_untouched(self) -> None:
        with tempfile.TemporaryDirectory() as plugin_data:
            result = self.run_hook(
                plugin_data,
                {"hook_event_name": "Stop", "session_id": "ordinary", "cwd": "/target"},
            )
            self.assertEqual(result, {})

    def test_continuation_turn_remains_blocked_until_state_changes(self) -> None:
        with tempfile.TemporaryDirectory() as plugin_data:
            path = session_state_path(plugin_data, "persistent")
            state = new_state("persistent", "/target")
            state.update(
                {
                    "inventory_initialized": True,
                    "acceptance": [{"id": "A1", "state": "pending", "evidence": []}],
                }
            )
            save_state(path, state)
            result = self.run_hook(
                plugin_data,
                {
                    "hook_event_name": "Stop",
                    "session_id": "persistent",
                    "cwd": "/target",
                    "stop_hook_active": True,
                },
            )
            self.assertEqual(result["decision"], "block")
            self.assertIn("Continue executing", result["reason"])

    def test_explicit_invocation_activates_but_discussion_does_not(self) -> None:
        with tempfile.TemporaryDirectory() as plugin_data:
            discussion = self.run_hook(
                plugin_data,
                {
                    "hook_event_name": "UserPromptSubmit",
                    "session_id": "discussion",
                    "cwd": "/target",
                    "prompt": "Why did Adeptus Necroneerium stop early?",
                },
            )
            self.assertEqual(discussion, {})
            invocation = self.run_hook(
                plugin_data,
                {
                    "hook_event_name": "UserPromptSubmit",
                    "session_id": "invoked",
                    "cwd": "/target",
                    "prompt": "Use @adeptus-necroneerium to implement the request.",
                },
            )
            self.assertIn("ADEPTUS COMPLETION GUARD IS ACTIVE", invocation["additionalContext"])
            self.assertTrue(session_state_path(plugin_data, "invoked").exists())

    def test_explicit_abort_disables_an_active_guard(self) -> None:
        with tempfile.TemporaryDirectory() as plugin_data:
            common = {
                "hook_event_name": "UserPromptSubmit",
                "session_id": "abortable",
                "cwd": "/target",
            }
            self.run_hook(plugin_data, {**common, "prompt": "adeptus_necroneerium build it"})
            aborted = self.run_hook(
                plugin_data, {**common, "prompt": "@adeptus-necroneerium abort"}
            )
            self.assertIn("explicitly aborted", aborted["additionalContext"])
            stopped = self.run_hook(
                plugin_data,
                {"hook_event_name": "Stop", "session_id": "abortable", "cwd": "/target"},
            )
            self.assertEqual(stopped, {})

    def test_corrupt_active_state_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as plugin_data:
            path = session_state_path(plugin_data, "corrupt")
            path.parent.mkdir(parents=True)
            path.write_text("{not json", encoding="utf-8")
            result = self.run_hook(
                plugin_data,
                {"hook_event_name": "Stop", "session_id": "corrupt", "cwd": "/target"},
            )
            self.assertEqual(result["decision"], "block")
            self.assertIn("unreadable", result["reason"])

    def test_packaged_platform_hook_command_executes_verbatim(self) -> None:
        configuration = json.loads(
            (ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8")
        )
        hook = configuration["hooks"]["UserPromptSubmit"][0]["hooks"][0]
        command_key = "commandWindows" if os.name == "nt" else "command"
        command = hook[command_key]
        with tempfile.TemporaryDirectory() as plugin_data:
            environment = os.environ.copy()
            environment.update({"PLUGIN_ROOT": str(ROOT), "PLUGIN_DATA": plugin_data})
            result = subprocess.run(
                command,
                input=json.dumps(
                    {
                        "hook_event_name": "UserPromptSubmit",
                        "session_id": "packaged-command",
                        "cwd": "/target",
                        "prompt": "Use @adeptus-necroneerium now.",
                    }
                ),
                text=True,
                capture_output=True,
                env=environment,
                shell=True,
                check=True,
            )
            output = json.loads(result.stdout)
            self.assertIn("ADEPTUS COMPLETION GUARD IS ACTIVE", output["additionalContext"])


class StateCliTests(unittest.TestCase):
    def run_state(self, *arguments: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "adeptus_state.py"), *arguments],
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, expected, result.stderr or result.stdout)
        return result

    def initialized_state(
        self, directory: str, acceptance: list[dict[str, object]], gates: list[dict[str, object]]
    ) -> Path:
        state_path = Path(directory) / "completion-state.json"
        inventory_path = Path(directory) / "inventory.json"
        save_state(state_path, new_state("cli-session", "/target"))
        inventory_path.write_text(
            json.dumps(
                {
                    "request_title": "CLI policy test",
                    "current_phase": "phase-1",
                    "acceptance": acceptance,
                    "phase_gates": gates,
                }
            ),
            encoding="utf-8",
        )
        self.run_state(
            "init", "--state", str(state_path), "--inventory", str(inventory_path)
        )
        return state_path

    def test_cli_runs_two_phases_and_certifies_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state = self.initialized_state(
                directory,
                [
                    {"id": "A1", "description": "phase one", "phase": "phase-1"},
                    {"id": "A2", "description": "phase two", "phase": "phase-2"},
                ],
                [
                    {"id": "G1", "description": "phase one checkpoint"},
                    {"id": "G2", "description": "project gate"},
                ],
            )
            self.run_state(
                "set-item", "--state", str(state), "--id", "A1", "--status", "passed",
                "--evidence", "phase one boundary exited 0",
            )
            self.run_state(
                "set-gate", "--state", str(state), "--id", "G1", "--status", "passed",
                "--evidence", "untouched checkpoint archived",
            )
            self.run_state(
                "advance-phase", "--state", str(state), "--gate", "G1", "--to", "phase-2"
            )
            for identifier in ("A2", "G2"):
                command = "set-item" if identifier == "A2" else "set-gate"
                self.run_state(
                    command, "--state", str(state), "--id", identifier, "--status", "passed",
                    "--evidence", f"{identifier} direct verification exited 0",
                )
            proposed = self.run_state(
                "propose", "--state", str(state), "--outcome", "PASS"
            )
            self.assertEqual(json.loads(proposed.stdout)["outcome"], "PASS")
            self.run_state("check", "--state", str(state))

    def test_cli_certifies_only_an_evidenced_external_blocker(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state = self.initialized_state(
                directory,
                [{"id": "A1", "description": "requires external service"}],
                [],
            )
            self.run_state(
                "record-blocker", "--state", str(state), "--id", "B1", "--external",
                "--reason", "required service is unavailable", "--evidence",
                "service health probe failed", "--unblock-action", "restore the service",
                "--blocks", "A1", "--status", "open",
            )
            proposed = self.run_state(
                "propose", "--state", str(state), "--outcome", "BLOCKED", "--blocker-id", "B1"
            )
            self.assertEqual(json.loads(proposed.stdout)["outcome"], "BLOCKED")

    def test_cli_requires_attempt_zero_and_both_retries_for_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state = self.initialized_state(
                directory,
                [{"id": "A1", "description": "critical behavior"}],
                [],
            )
            for attempt, status in ((0, "open"), (1, "open"), (2, "rejected_after_retry_2")):
                self.run_state(
                    "record-finding", "--state", str(state), "--id", "F1", "--critical",
                    "--scope-path", "V1/S1", "--judged-item", "critical behavior",
                    "--root-defect", "stable implementation defect", "--attempt", str(attempt),
                    "--evidence", f"attempt {attempt} direct failure", "--status", status,
                )
            proposed = self.run_state(
                "propose", "--state", str(state), "--outcome", "FAIL", "--finding-id", "F1"
            )
            self.assertEqual(json.loads(proposed.stdout)["outcome"], "FAIL")


if __name__ == "__main__":
    unittest.main()
