from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "adeptus-necroneerium"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class SkillContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = read("skills/adeptus-necroneerium/SKILL.md")
        cls.lich = read("skills/adeptus-necroneerium/roles/lich.md")
        cls.vampire = read("skills/adeptus-necroneerium/roles/vampire.md")
        cls.shade = read("skills/adeptus-necroneerium/roles/shade.md")

    def test_skill_remains_explicitly_opt_in(self) -> None:
        frontmatter = self.skill.split("---", 2)[1]
        self.assertIn("Use only when the user explicitly requests", frontmatter)
        self.assertIn("This skill is strictly opt-in", self.skill)
        self.assertIn("allow_implicit_invocation: false", read(
            "skills/adeptus-necroneerium/agents/openai.yaml"
        ))

    def test_lich_is_a_code_producing_layer(self) -> None:
        combined = f"{self.skill}\n{self.lich}".lower()
        for required in (
            "code-producing layer",
            "actual codebase",
            "package",
            "module",
            "public entry points",
            "major wiring seams",
        ):
            self.assertIn(required, combined)
        self.assertIn("prose-only architecture", combined)

    def test_vampire_is_a_code_producing_layer(self) -> None:
        combined = f"{self.skill}\n{self.vampire}".lower()
        for required in (
            "code-producing layer",
            "executable skeletons",
            "function and method signatures",
            "dataclasses",
            "exceptions",
            "test skeletons",
        ):
            self.assertIn(required, combined)
        self.assertIn("prose-only tactical plan", combined)

    def test_missing_control_context_cannot_block_implementation(self) -> None:
        self.assertIn(
            "Missing plugin, hook, or bookkeeping context is never by itself a reason "
            "to block implementation.",
            self.skill,
        )
        forbidden = (
            "mechanical completion guard",
            "mandatory session completion ledger",
            "adeptus_state.py",
            "hook context supplies",
            "ledger certifies",
        )
        installable_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in SKILL_ROOT.rglob("*")
            if path.is_file()
        ).lower()
        for phrase in forbidden:
            self.assertNotIn(phrase.lower(), installable_text)

    def test_guard_control_plane_is_absent(self) -> None:
        for relative in (
            "hooks/hooks.json",
            "hooks/adeptus_hook.py",
            "scripts/adeptus_state.py",
            "tests/test_completion_guard.py",
        ):
            self.assertFalse((ROOT / relative).exists(), relative)

    def test_pass_still_requires_complete_acceptance_evidence(self) -> None:
        self.assertIn(
            "Project PASS is allowed only when every binding acceptance item and required "
            "phase/project gate has passed with direct evidence.",
            self.skill,
        )
        self.assertIn("A local PASS is not project PASS", self.skill)

    def test_manifest_describes_progressive_code_construction(self) -> None:
        manifest = json.loads(read(".codex-plugin/plugin.json"))
        description = " ".join(
            (
                manifest["description"],
                manifest["interface"]["shortDescription"],
                manifest["interface"]["longDescription"],
            )
        ).lower()
        self.assertIn("lich shapes repository structure", description)
        self.assertIn("vampire writes executable contracts", description)
        self.assertNotRegex(description, re.compile(r"hook|ledger|mechanic|evidence-gated"))

    def test_repository_doctrine_contains_no_guard_dependency(self) -> None:
        doctrine = "\n".join(
            read(relative)
            for relative in (
                "AGENTS.md",
                "README.md",
                "docs/charter.md",
                "docs/manifesto.md",
                "docs/skill-outline.md",
            )
        ).lower()
        for phrase in (
            "completion guard",
            "session ledger",
            "stop hook",
            "injected context",
            "adeptus_state.py",
        ):
            self.assertNotIn(phrase, doctrine)

    def test_verifier_derives_expectations_from_the_repository(self) -> None:
        verifier = read("verify-adeptus-update.ps1")
        self.assertIn("repository-synchronized-v5", verifier)
        self.assertIn("HEAD matches origin/main", verifier)
        self.assertIn("Get-RelativeFiles", verifier)
        self.assertIn("Invoke-NativeCaptured", verifier)
        self.assertNotIn("& py -3 -m unittest", verifier)
        self.assertNotRegex(verifier, re.compile(r"\b[0-9a-f]{40}\b"))
        self.assertNotRegex(verifier, re.compile(r"\b[0-9a-f]{64}\b"))
        self.assertNotIn("[string]::Join", verifier)
        self.assertNotIn("C:\\Users\\Zero", verifier)

    def test_verifier_runs_tests_from_repository_root(self) -> None:
        verifier = read("verify-adeptus-update.ps1")
        self.assertIn("$startInfo.WorkingDirectory", verifier)
        self.assertIn("-WorkingDirectory $repositoryRoot", verifier)

    def test_verifier_has_explicit_bounded_repair_mode(self) -> None:
        verifier = read("verify-adeptus-update.ps1")
        self.assertIn("[switch]$Repair", verifier)
        self.assertIn("function Sync-InstallablePackage", verifier)
        self.assertIn("foreach ($relativeDirectory in @('.codex-plugin', 'skills'))", verifier)
        self.assertIn("Refusing repair because", verifier)
        self.assertIn("codex plugin add $PluginId --json", verifier)


if __name__ == "__main__":
    unittest.main()
