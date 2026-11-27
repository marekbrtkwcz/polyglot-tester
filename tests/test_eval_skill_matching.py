"""Tests for scripts/eval_skill_matching.py (the mechanical eval baseline)."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "eval_skill_matching.py"

spec = importlib.util.spec_from_file_location("eval_skill_matching", SCRIPT)
esm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(esm)


def test_load_skills_reads_every_skill_description():
    skills = esm.load_skills()
    assert len(skills) == 79
    assert all(desc for desc in skills.values())
    assert "feature-workflow" in skills


def test_parse_cases_reads_both_case_files():
    activation = esm.parse_cases(esm.EVALS / "activation-cases.md")
    collision = esm.parse_cases(esm.EVALS / "collision-cases.md")
    assert len(activation) == 23
    assert len(collision) == 15
    assert activation[0]["winner"] == "feature-workflow"
    assert collision[0]["winner"] == "golang-error-handling"
    assert all(c["prompt"] and c["id"] for c in activation + collision)


def test_rank_puts_language_named_twin_on_top():
    skills = esm.load_skills()
    doc_freq = {}
    for desc in skills.values():
        for tok in set(esm.tokenize(desc)):
            doc_freq[tok] = doc_freq.get(tok, 0) + 1
    ranking = esm.rank(
        "N+1 queries from Prisma in the orders endpoint", skills, doc_freq
    )
    # the case-file prompts deliberately avoid description vocabulary, so the
    # mechanical matcher abstains (all zero) instead of guessing
    assert all(score == 0.0 for score, _, _ in ranking)
    ranking = esm.rank(
        "error handling in Go: wrapping with sentinel errors", skills, doc_freq
    )
    assert ranking[0][1] == "golang-error-handling"


def test_rank_ignores_single_shared_token():
    skills = {
        "a": "Load this skill when you need a thing",
        "b": "Load this skill for other stuff",
    }
    ranking = esm.rank("we need it", skills, {"need": 1})
    assert all(score == 0.0 for score, _, _ in ranking)


def test_main_outputs_valid_json_with_all_cases():
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--top", "1"],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(result.stdout)
    assert len(data) == 38
    assert all("mechanical_pick" in case and "winner_rank" in case for case in data)
