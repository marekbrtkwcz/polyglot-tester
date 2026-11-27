---
name: git-workflow-polyglot
description: Load this skill for day-to-day git work in any project: commit conventions, branching, pull requests, rebases, bisect, and recovering from mistakes. Language-agnostic.
---

# Git Workflow (Polyglot)

## Commit messages

- One subject line, imperative mood, max ~72 chars: `Fix race in cache invalidation`.
- Body (optional) explains **why**, not what — the diff already shows what.
- Group related changes into one commit; unrelated changes never share one.
- Conventional prefixes when the repo already uses them (`feat:`, `fix:`, `chore:`); otherwise match the existing history (`git log --oneline`).

## Branching

- Short-lived feature branches off the default branch: `feature/short-name`, `fix/short-name`.
- Keep branches small; rebase onto the default branch before opening a PR, don't merge it in.
- Delete the branch after merge (local and remote).

## Pull requests

- PR title = the commit message the squash will produce.
- Description: what changed, why, how it was verified (commands + results), what is NOT verified.
- Keep PRs reviewable: if it spans unrelated areas, split it.

## Rebasing safely

- `git fetch origin && git rebase origin/main` on your feature branch.
- Never rebase commits already pushed to a shared branch (use merge there instead).
- After a conflicted rebase: resolve, `git add`, `git rebase --continue`; to bail out: `git rebase --abort`.

## Finding the breaking commit

- `git bisect start`, mark `bad`/`good`, let git drive; `git bisect run <script>` for automated checks.
- `git bisect reset` when done.

## Recovery

- Undo last commit, keep changes: `git reset --soft HEAD~1`.
- Discard unstaged changes to one file: `git restore <file>` (or `git checkout -- <file>`).
- Recover a deleted branch: `git reflog` → find the commit → `git branch <name> <sha>`.
- Stash before switching: `git stash push -m "wip: ..."`; `git stash pop` to return.

## Hygiene

- Never commit secrets, `.env` files, or build artifacts — check `.gitignore` first.
- `git status` before every commit; review the staged diff (`git diff --staged`).
- Push explicitly and deliberately; know which branch you are pushing to.
