"""Pure validation logic for Layered Agile Coding markdown specs."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

REQUIRED_SECTIONS = (
    "Request",
    "Acceptance criteria",
    "Selected mode",
    "Current milestone",
    "Non-goals",
    "Validation plan",
    "Shade: review route",
)

_HEADING = re.compile(r"^##\s+(.+?)\s*#*\s*$", re.MULTILINE)
_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_SUBHEADING = re.compile(r"^#{1,6}\s+.*$", re.MULTILINE)
_BARE_LIST_MARKER = re.compile(r"^\s*(?:[-+*]|\d+[.)])\s*$", re.MULTILINE)
_BLANK_TEMPLATE_FIELD = re.compile(
    r"^\s*(?:Mode|Reason|Reasoning|Outcome|Validation evidence):\s*$",
    re.MULTILINE | re.IGNORECASE,
)
_DEFAULT_REPAIR_COUNT = re.compile(
    r"^\s*Attempt count:\s*0\s*/\s*2\s*$", re.MULTILINE | re.IGNORECASE
)


@dataclass(frozen=True)
class ValidationResult:
    """The missing and present-but-empty required sections in a spec."""

    missing_sections: tuple[str, ...] = ()
    empty_sections: tuple[str, ...] = ()

    @property
    def is_valid(self) -> bool:
        return not self.missing_sections and not self.empty_sections


def validate_spec(markdown: str) -> ValidationResult:
    """Validate required level-two sections in spec markdown content."""
    sections = _extract_sections(markdown)
    required_by_key = {name.casefold(): name for name in REQUIRED_SECTIONS}

    missing = tuple(
        name for key, name in required_by_key.items() if key not in sections
    )
    empty = tuple(
        name
        for key, name in required_by_key.items()
        if key in sections and not _has_useful_content(sections[key])
    )
    return ValidationResult(missing_sections=missing, empty_sections=empty)


def validate_file(path: str | Path) -> ValidationResult:
    """Read and validate a UTF-8 Layered Agile Coding spec file."""
    return validate_spec(Path(path).read_text(encoding="utf-8"))


def _extract_sections(markdown: str) -> dict[str, str]:
    matches = list(_HEADING.finditer(markdown))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        sections[match.group(1).strip().casefold()] = markdown[match.end() : end]
    return sections


def _has_useful_content(content: str) -> bool:
    content = _COMMENT.sub("", content)
    content = _SUBHEADING.sub("", content)
    content = _BARE_LIST_MARKER.sub("", content)
    content = _BLANK_TEMPLATE_FIELD.sub("", content)
    content = _DEFAULT_REPAIR_COUNT.sub("", content)
    return bool(re.search(r"[A-Za-z0-9]", content))
