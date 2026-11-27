"""Deterministic skill-selection matcher for the eval case files.

Reads the case tables in evals/activation-cases.md and evals/collision-cases.md,
parses every skill's frontmatter description, and ranks skills per case by
token overlap between the prompt and the description (stopwords removed,
description tokens weighted by inverse frequency across the collection so
rare, distinctive words count more).

This is NOT a model run: it is the reproducible mechanical baseline that the
manual run record in evals/runs/ is compared against. A disagreement between
this ranking and the model's actual selection is a description-vocabulary
finding, not a scoring artifact.

Usage: python scripts/eval_skill_matching.py [--top N]
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN = REPO_ROOT / ".vibe" / "plugins" / "polyglot-dev"
EVALS = PLUGIN / "evals"

STOPWORDS = set(
    "a an and are as at be but by for from has have in into is it its of on or "
    "our so that the their them they this to was we what when where which who "
    "will with you your not no do does did should can could than then just only "
    "some any all each other more most such over under again once per via".split()
)


def tokenize(text):
    return [
        t
        for t in re.findall(r"[a-z0-9]+", text.lower())
        if t not in STOPWORDS and len(t) > 2
    ]


def parse_frontmatter(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines and lines[0].strip() == "---", f"{path}: no frontmatter"
    fields = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^([a-z_]+):\s*(.+)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields


def load_skills():
    skills = {}
    for skill_md in sorted((PLUGIN / "skills").glob("*/SKILL.md")):
        fields = parse_frontmatter(skill_md)
        skills[fields["name"]] = fields.get("description", "")
    return skills


def parse_cases(path):
    """Rows of the case tables: | # | prompt | winner | must-not |."""
    cases = []
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and re.fullmatch(r"[A-C]?\d+", cells[0] or ""):
            cases.append(
                {
                    "id": cells[0],
                    "prompt": cells[1].strip('"'),
                    "winner": cells[2].strip("` "),
                    "must_not": cells[3].strip("` ") if len(cells) > 3 else "",
                }
            )
    return cases


def bigrams(tokens):
    return {f"{a} {b}" for a, b in zip(tokens, tokens[1:])}


def rank(prompt, skills, doc_freq):
    prompt_tokens = tokenize(prompt)
    prompt_token_set = set(prompt_tokens)
    prompt_bigrams = bigrams(prompt_tokens)
    scores = []
    for name, desc in skills.items():
        desc_tokens = tokenize(desc)
        if not desc_tokens:
            continue
        desc_token_set = set(desc_tokens)
        overlap = prompt_token_set & desc_token_set
        # a single shared word is noise; require substance
        if len(overlap) < 2 and not (prompt_bigrams & bigrams(desc_tokens)):
            scores.append((0.0, name, []))
            continue
        # idf weighting: rare description words signal a real match
        score = sum(1.0 / math.log(1 + doc_freq.get(tok, 1)) for tok in overlap)
        score += 3.0 * len(prompt_bigrams & bigrams(desc_tokens))
        scores.append((score, name, sorted(overlap)))
    scores.sort(reverse=True)
    return scores


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--top", type=int, default=3)
    args = parser.parse_args()

    skills = load_skills()
    # document frequency of each description token across the collection
    doc_freq = {}
    for desc in skills.values():
        for tok in set(tokenize(desc)):
            doc_freq[tok] = doc_freq.get(tok, 0) + 1

    cases = parse_cases(EVALS / "activation-cases.md") + parse_cases(
        EVALS / "collision-cases.md"
    )
    out = []
    for case in cases:
        ranking = rank(case["prompt"], skills, doc_freq)
        top = [
            {"skill": name, "score": round(score, 3), "shared": shared}
            for score, name, shared in ranking[: args.top]
        ]
        winner_rank = next(
            (i for i, (s, n, _) in enumerate(ranking) if n == case["winner"]), None
        )
        out.append(
            {
                **case,
                "mechanical_top": top,
                "winner_rank": winner_rank,
                "mechanical_pick": ranking[0][1] if ranking else None,
            }
        )

    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
