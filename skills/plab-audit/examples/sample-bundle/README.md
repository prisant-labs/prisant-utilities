# Audit: example-plugin

**Repository:** `example-plugin/` (illustrative target, not a real repository)
**Audited:** 2026-09-20, `main` at `0000000`, clean worktree
**Type detected:** `agent-plugin`, from `library.json` and `.claude-plugin/plugin.json`
**Mode:** read-only. Nothing in the audited repository was modified
**Auditor:** hand-run

**What this bundle is.** It is the committed sample that `.github/workflows/gate.yml` runs `bundle-check.py` against on every push and pull request. It is deliberately small, and it is deliberately complete: every structural rule the checker enforces is exercised here, so a rule that stops working fails CI on this sample instead of failing silently on real output months later.

**It is not a real audit.** The target is illustrative. Trimmed from the Phase 2 fixture, which audited a real repository; that fixture stays out of this public tree because its findings belong to that repository and its evidence carried machine-specific paths.

## The bundle

| File | What it answers |
|------|-----------------|
| `appraise.md` | What this repository is, and what it is worth |
| `findings.md` | What is wrong with it, with a file path on every finding |
| `roadmap.md` | What to do next, ranked, with a speculation break |
| `evidence.md` | What was actually run and read, and what was not |

## Why the sample must stay complete

`bundle-check.py` rule R3 requires `evidence.md` to carry a `Decision records consulted` section. A sample cut down to the bare minimum would fail CI on the sample rather than on any real output, and a job that fails for reasons nobody believes is a job everybody learns to ignore. Rule R6 checks a per-item property, so this sample keeps more than one rank-numbered roadmap item; with a single item, half of R6 would never run.
