from adeptus_necroneerium.cli import main
from adeptus_necroneerium.spec_validation import REQUIRED_SECTIONS, validate_spec


def make_spec(*, omit: str | None = None, empty: str | None = None) -> str:
    sections = []
    for name in REQUIRED_SECTIONS:
        if name == omit:
            continue
        body = "<!-- template guidance -->\n- \n" if name == empty else "Useful detail."
        sections.append(f"## {name}\n\n{body}")
    return "\n\n".join(sections)


def test_valid_spec_passes():
    result = validate_spec(make_spec())

    assert result.is_valid
    assert result.missing_sections == ()
    assert result.empty_sections == ()


def test_missing_required_section_fails():
    result = validate_spec(make_spec(omit="Non-goals"))

    assert not result.is_valid
    assert result.missing_sections == ("Non-goals",)


def test_empty_required_section_fails():
    result = validate_spec(make_spec(empty="Current milestone"))

    assert not result.is_valid
    assert result.empty_sections == ("Current milestone",)


def test_blank_template_scaffolding_is_not_useful_content():
    markdown = """## Selected mode

<!-- Direct, Tactical, or Layered. -->
Mode:
Reason:

## Shade: review route

### Critical findings
-
### Repair attempts
Attempt count: 0 / 2
### Final outcome
Outcome:
Reasoning:
Validation evidence:
"""

    result = validate_spec(markdown)

    assert "Selected mode" in result.empty_sections
    assert "Shade: review route" in result.empty_sections


def test_cli_returns_nonzero_on_invalid_spec(tmp_path, capsys):
    spec = tmp_path / "invalid.md"
    spec.write_text(make_spec(omit="Request"), encoding="utf-8")

    exit_code = main([str(spec)])

    assert exit_code != 0
    assert "FAIL" in capsys.readouterr().out
