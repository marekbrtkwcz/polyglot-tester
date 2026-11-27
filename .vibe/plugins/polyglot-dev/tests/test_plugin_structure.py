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


def test_skill_descriptions_within_vibe_limit():
    # Vibe refuses to load a skill whose description exceeds 1024 characters.
    for d in skill_dirs():
        description = parse_frontmatter(d / "SKILL.md")["description"]
        assert len(description) <= 1024, (
            f"{d.name}: description is {len(description)} chars, Vibe limit is 1024"
        )


def test_skill_descriptions_are_written_as_triggers():
    # The README convention: a description is a trigger sentence from the
    # user's point of view — "Load this skill when/for/to ...".
    for d in skill_dirs():
        description = parse_frontmatter(d / "SKILL.md")["description"]
        assert description.startswith("Load this skill "), (
            f"{d.name}: description should start with 'Load this skill ...': {description[:60]}"
        )


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


READ_ONLY_AGENTS = {
    "code-reviewer",
    "explorer",
    "onboarder",
    "performance-profiler",
    "planner",
    "security-auditor",
    "test-runner",
}


def test_read_only_agents_have_approved_bash():
    # A read-only agent without bash cannot map an unknown repo (the
    # onboarder regression): every read-only agent gets bash with
    # permission "ask" and a denylist of state-changing commands.
    for f in agent_files():
        if f.stem not in READ_ONLY_AGENTS:
            continue
        data = tomllib.loads(f.read_text(encoding="utf-8"))
        assert "bash" in data.get("enabled_tools", []), f"{f.name}: bash not enabled"
        assert "bash" not in data.get("disabled_tools", []), f"{f.name}: bash disabled"
        bash_cfg = data.get("tools", {}).get("bash", {})
        assert bash_cfg.get("permission") == "ask", f"{f.name}: bash must be ask"
        assert bash_cfg.get("denylist"), f"{f.name}: bash denylist missing"


def test_agent_instructions_cover_global_plugin_path():
    # With a global install the plugin lives in ~/.vibe/plugins/polyglot-dev/;
    # instructions pointing at plugin files must name both locations.
    for f in agent_files():
        text = f.read_text(encoding="utf-8")
        if "plugin directory" in text or "knowledge folders" in text:
            assert "~/.vibe/plugins/polyglot-dev/" in text, (
                f"{f.name}: instructions must mention the global plugin path"
            )


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


def _hooks():
    data = tomllib.loads((VIBE_DIR / "hooks.toml").read_text(encoding="utf-8"))
    return data.get("hooks", [])


def test_pre_tool_hooks_cover_whole_tool_class():
    # A hook guarding a tool class must cover every variant of that class,
    # or it is bypassable: shell calls arrive as `bash`, Windows
    # `git_bash`/`powershell`, and background `process_start`; file writes
    # arrive as `write_file` and `edit`.
    classes = {
        "shell": ("bash", "git_bash", "powershell", "process_start"),
        "file writes": ("write_file", "edit"),
    }
    for hook in _hooks():
        if hook.get("type") != "pre_tool":
            continue
        match = hook.get("match", "")
        for cls_name, tools in classes.items():
            if any(tool in match for tool in tools):
                for tool in tools:
                    assert tool in match, (
                        f"{hook.get('name')}: match covers {cls_name} "
                        f"only partially: missing {tool}"
                    )


def test_one_process_guard_hooks():
    # One Python process per tool call: a single hook for ALL shell tools
    # via guard_all.py, plus one for file writes via guard_secrets.py (a
    # call is either a shell command or a file write, never both). Each
    # hook's match must cover its whole tool class.
    pre_tool = [h for h in _hooks() if h.get("type") == "pre_tool"]
    assert len(pre_tool) == 2, (
        f"expected one shell hook + one write hook, got {[h.get('name') for h in pre_tool]}"
    )
    shell = next(h for h in pre_tool if "bash" in h.get("match", ""))
    writes = next(h for h in pre_tool if "write_file" in h.get("match", ""))
    assert "guard_all.py" in shell["command"], shell["command"]
    for tool in ("bash", "git_bash", "powershell", "process_start"):
        assert tool in shell["match"], f"{shell.get('name')}: match missing {tool}"
    assert "guard_secrets.py" in writes["command"], writes["command"]
    for tool in ("write_file", "edit"):
        assert tool in writes["match"], f"{writes.get('name')}: match missing {tool}"


def test_hook_commands_fallback_to_python3():
    # macOS and modern Linux ship `python3` only. With `strict = true`,
    # a command that names just `python` fails to spawn there and
    # escalates to denying every guarded shell call.
    for hook in _hooks():
        command = hook.get("command", "")
        assert "|| python3 " in command, (
            f"{hook.get('name')}: command lacks a python3 fallback: {command}"
        )


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
