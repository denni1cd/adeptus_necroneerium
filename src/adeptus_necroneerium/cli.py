"""Command-line interface for Layered Agile Coding spec validation."""

import argparse
from collections.abc import Sequence
from pathlib import Path

from .spec_validation import validate_file


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a Layered Agile Coding spec markdown file."
    )
    parser.add_argument("spec", type=Path, help="path to the markdown spec")
    args = parser.parse_args(argv)

    try:
        result = validate_file(args.spec)
    except OSError as error:
        print(f"FAIL: {error}")
        return 1

    if result.is_valid:
        print("PASS")
        return 0

    print("FAIL")
    for section in result.missing_sections:
        print(f"- missing section: {section}")
    for section in result.empty_sections:
        print(f"- empty section: {section}")
    return 1
