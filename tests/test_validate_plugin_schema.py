"""Unit tests for scripts/validate_plugin_schema.py (schema fetch mocked)."""

import importlib.util
import io
import json
from pathlib import Path
from unittest import mock

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "validate_plugin_schema.py"

spec = importlib.util.spec_from_file_location("validate_plugin_schema", SCRIPT)
vps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vps)

SCHEMA = {
    "type": "object",
    "required": ["name", "version"],
    "properties": {
        "name": {"type": "string"},
        "version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
    },
}


def run_main(plugin_doc, schema=SCHEMA):
    fake_response = io.BytesIO(json.dumps(schema).encode())
    fake_response.__enter__ = lambda s: s
    fake_response.__exit__ = lambda s, *a: False
    with (
        mock.patch.object(vps.urllib.request, "urlopen", return_value=fake_response),
        mock.patch.object(
            vps,
            "PLUGIN_JSON",
            mock.Mock(read_text=lambda encoding="utf-8": json.dumps(plugin_doc)),
        ),
    ):
        return vps.main()


def test_valid_plugin_passes():
    assert run_main({"name": "polyglot-dev", "version": "1.3.0"}) == 0


@pytest.mark.parametrize(
    "plugin_doc",
    [
        {"name": "polyglot-dev"},  # missing version
        {"version": "1.3.0"},  # missing name
        {"name": "polyglot-dev", "version": "1.3"},  # bad semver
        {"name": 42, "version": "1.3.0"},  # wrong type
    ],
)
def test_invalid_plugin_fails(plugin_doc):
    assert run_main(plugin_doc) == 1


def test_real_plugin_json_is_valid_against_minimal_schema():
    """The shipped plugin.json satisfies the required-fields contract."""
    real = json.loads(
        (REPO_ROOT / ".vibe/plugins/polyglot-dev/plugin.json").read_text(
            encoding="utf-8"
        )
    )
    assert run_main(real) == 0
