"""Structural validation of the polyglot-dev plugin.

Runs in CI next to the guard tests. Uses only the standard library so it
works on every Python in the CI matrix (3.11+ for tomllib).
"""

import json
import re
import tomllib
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = PLUGIN_ROOT / "skills"
VIBE_DIR = PLUGIN_ROOT / "ai.mistral.vibe"
AGENTS_DIR = VIBE_DIR / "agents"
KNOWLEDGE_DIR = VIBE_DIR / "knowledge"

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
FRONTMATTER_KEY_RE = re.compile(r"^([a-z_]+):\s*(.+)$")


def skill_dirs():
    return sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir())


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    assert lines and lines[0].strip() == "---", f"{path.name}: missing opening ---"
    fields = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        m = FRONTMATTER_KEY_RE.match(line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    raise AssertionError(f"{path.name}: unterminated frontmatter")


# --- skills ---------------------------------------------------------------

def test_every_skill_dir_has_skill_md():
    dirs = skill_dirs()
    assert dirs, "no skills found"
    missing = [d.name for d in dirs if not (d / "SKILL.md").is_file()]
    assert not missing, f"skill dirs without SKILL.md: {missing}"


def test_skill_frontmatter_has_name_and_description():
    for d in skill_dirs():
        fields = parse_frontmatter(d / "SKILL.md")
        assert fields.get("name"), f"{d.name}: frontmatter missing 'name'"
        assert fields.get("description"), f"{d.name}: frontmatter missing 'description'"


def test_skill_name_matches_directory():
    for d in skill_dirs():
        fields = parse_frontmatter(d / "SKILL.md")
        assert fields["name"] == d.name, (
            f"{d.name}: frontmatter name {fields['name']!r} != directory name"
        )


def test_skill_names_are_unique():
    names = [parse_frontmatter(d / "SKILL.md")["name"] for d in skill_dirs()]
    dupes = {n for n in names if names.count(n) > 1}
    assert not dupes, f"duplicate skill names: {dupes}"


def test_skill_names_are_kebab_case():
    for d in skill_dirs():
        assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", d.name), (
            f"{d.name}: not kebab-case"
        )


# --- plugin.json ----------------------------------------------------------

def test_plugin_json_is_valid():
    data = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
    assert data["name"] == "polyglot-dev"
    assert SEMVER_RE.match(data["version"]), data["version"]
    assert data.get("description")
    assert "ai.mistral.vibe" in data.get("extensions", {})


# --- agents ---------------------------------------------------------------

ALLOWED_AGENT_KEYS = {
    "schema_version",
    "agent_type",
    "display_name",
    "description",
    "safety",
    "instructions",
    "model",
    "enabled_tools",
    "disabled_tools",
    "tools",
}


def agent_files():
    return sorted(AGENTS_DIR.glob("*.toml"))


def test_agents_exist_and_parse():
    files = agent_files()
    assert files, "no agent TOML files found"
    for f in files:
        data = tomllib.loads(f.read_text(encoding="utf-8"))
        assert data.get("schema_version") == 1, f"{f.name}: schema_version"
        assert data.get("agent_type"), f"{f.name}: agent_type"


def test_agent_keys_are_snake_case():
    for f in agent_files():
        data = tomllib.loads(f.read_text(encoding="utf-8"))
        bad = [k for k in data if k not in ALLOWED_AGENT_KEYS or k != k.lower()]
        assert not bad, f"{f.name}: non-snake_case or unknown keys: {bad}"


# --- knowledge ------------------------------------------------------------

def test_every_knowledge_dir_has_knowledge_md():
    dirs = sorted(d for d in KNOWLEDGE_DIR.iterdir() if d.is_dir())
    assert dirs, "no knowledge folders found"
    missing = [d.name for d in dirs if not (d / "KNOWLEDGE.md").is_file()]
    assert not missing, f"knowledge dirs without KNOWLEDGE.md: {missing}"


# --- hooks ----------------------------------------------------------------

def test_hooks_toml_parseable_with_required_fields():
    data = tomllib.loads((VIBE_DIR / "hooks.toml").read_text(encoding="utf-8"))
    hooks = data.get("hooks", [])
    assert hooks, "no hooks defined"
    for hook in hooks:
        assert hook.get("name"), "hook missing name"
        assert hook.get("type"), f"{hook.get('name')}: missing type"
        assert hook.get("command"), f"{hook.get('name')}: missing command"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
