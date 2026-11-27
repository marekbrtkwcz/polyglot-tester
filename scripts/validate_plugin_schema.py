"""Validate plugin.json against the official Agent Plugins 1.0 schema.

Fetches the schema from agent-plugins.org and validates with jsonschema.
Exits non-zero on any validation error. Used by the plugin-schema CI job.
"""

import json
import sys
import urllib.request
from pathlib import Path

import jsonschema

SCHEMA_URL = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
PLUGIN_JSON = Path(__file__).resolve().parents[1] / ".vibe/plugins/polyglot-dev/plugin.json"


def main():
    with urllib.request.urlopen(SCHEMA_URL, timeout=30) as response:  # noqa: S310 - fixed official URL
        schema = json.loads(response.read().decode())

    plugin = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
    try:
        jsonschema.validate(plugin, schema)
    except jsonschema.ValidationError as exc:
        sys.stderr.write(f"plugin.json schema violation: {exc.message}\n  at: {list(exc.absolute_path)}\n")
        return 1
    print(f"plugin.json valid against {SCHEMA_URL}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
