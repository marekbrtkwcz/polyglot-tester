"""Unit tests for scripts/check_readme_skills.py."""

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "check_readme_skills.py"

spec = importlib.util.spec_from_file_location("check_readme_skills", SCRIPT)
crs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(crs)


def make_skill(root, name):
    skill_dir = root / "skills" / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: test skill {name}\n---\n",
        encoding="utf-8",
    )


def test_repo_readme_matches_skills_on_disk():
    missing, stale = crs.check()
    assert missing == [], f"skills missing from README: {missing}"
    assert stale == [], f"stale README entries: {stale}"


def test_missing_skill_detected(tmp_path):
    make_skill(tmp_path, "alpha")
    readme = tmp_path / "README.md"
    readme.write_text("nothing here\n", encoding="utf-8")
    missing, stale = crs.check(tmp_path / "skills", readme)
    assert missing == ["alpha"]
    assert stale == []


def test_stale_readme_entry_detected(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text("| Skill | `polyglot-dev:ghost` | removed skill |\n", encoding="utf-8")
    missing, stale = crs.check(tmp_path / "skills", readme)
    assert missing == []
    assert stale == ["ghost"]


def test_both_directions_at_once(tmp_path):
    make_skill(tmp_path, "present")
    readme = tmp_path / "README.md"
    readme.write_text(
        "| Skill | `polyglot-dev:present` | ok |\n| Skill | `polyglot-dev:old-one` | stale |\n",
        encoding="utf-8",
    )
    missing, stale = crs.check(tmp_path / "skills", readme)
    assert missing == []
    assert stale == ["old-one"]


def test_main_returns_nonzero_on_drift(tmp_path, capsys):
    make_skill(tmp_path, "undocumented")
    readme = tmp_path / "README.md"
    readme.write_text("", encoding="utf-8")
    import unittest.mock as mock

    with (
        mock.patch.object(crs, "SKILLS_DIR", tmp_path / "skills"),
        mock.patch.object(crs, "README", readme),
    ):
        assert crs.main() == 1
    assert "undocumented" in capsys.readouterr().err
