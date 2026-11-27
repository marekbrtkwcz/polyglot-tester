"""Check that every plugin skill is documented in README.md (and no stale entries).

Each skills/<name>/SKILL.md must appear in README.md as `polyglot-dev:<name>`,
and every `polyglot-dev:<name>` entry in README must match an existing skill.
Exits non-zero and lists the drift. Used by the tests CI job.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / ".vibe/plugins/polyglot-dev/skills"
README = REPO_ROOT / "README.md"
ENTRY_RE = re.compile(r"`polyglot-dev:([a-z0-9-]+)`")


def skill_names(skills_dir=SKILLS_DIR):
    """Return the set of skill names from SKILL.md frontmatter (name field)."""
    names = set()
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        for line in skill_md.read_text(encoding="utf-8").splitlines():
            if line.startswith("name:"):
                names.add(line.split(":", 1)[1].strip())
                break
    return names


def readme_entries(readme=README):
    """Return skill names from README table rows marked as Skill (| Skill | ...)."""
    text = readme.read_text(encoding="utf-8")
    rows = (line for line in text.splitlines() if line.startswith("| Skill |"))
    return set(name for row in rows for name in ENTRY_RE.findall(row))


def check(skills_dir=SKILLS_DIR, readme=README):
    """Return (missing_in_readme, stale_in_readme) as sorted lists."""
    on_disk = skill_names(skills_dir)
    in_readme = readme_entries(readme)
    return sorted(on_disk - in_readme), sorted(in_readme - on_disk)


def main():
    missing, stale = check(SKILLS_DIR, README)
    ok = True
    for name in missing:
        sys.stderr.write(f"skill missing from README.md: polyglot-dev:{name}\n")
        ok = False
    for name in stale:
        sys.stderr.write(f"README.md references unknown skill: polyglot-dev:{name}\n")
        ok = False
    if ok:
        print(f"README.md documents all {len(skill_names())} skills, no stale entries")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
