# Evidence: example-plugin

Read-only. Nothing in the audited repository was modified. Every command below is recorded with its exit code, including the ones that failed, because a tool that was absent or broke is a coverage gap and not a silence.

## Repository snapshot

| Field | Value |
|-------|-------|
| Path | `example-plugin/` (illustrative) |
| Branch | `main` at `0000000`, clean worktree |
| Type detected | `agent-plugin`, from `library.json` and `.claude-plugin/plugin.json` |
| Skills | 4 |

## Validation commands and outcomes

| Command | Exit | Outcome |
|---------|------|---------|
| `node <agent-skills-toolkit>/scripts/check.mjs . ` | 0 | Universal tier, 0 errors, 0 warnings |
| `python3 scripts/version-parity-check.py` | 0 | All four claim locations agree |
| `python3 scripts/check-dashes.py` | 0 | Canary proved, no banned characters |
| `cargo audit` | 127 | **Not installed. Coverage gap, not a clean result.** No dependency-scanning claim is made anywhere in this bundle |

The `cargo audit` row is the one that matters most in a sample. A missing tool degrades to a recorded gap with its exit code; it never degrades to a passing check and never to generic advice standing in for a real one.

## Decision records consulted

Every candidate finding was reconciled against the repository's own recorded decisions before publication. Consulting these is what separates a finding from a candidate.

| Record | Bearing on this audit | Result |
|--------|----------------------|--------|
| `AGENTS.md`, design frame | Excludes adoption affordances by standing decision | Withdrew the contributor-onboarding candidate |
| `docs/decisions/0001-standard-pin.md` | Records a tested and rejected Standard pin | Withdrew the version-pin candidate |
| `docs/decisions/0002-generated-manifests.md` | Establishes the generator as canonical | Sharpened F-02; did not withdraw it |
| Release-cadence record | Absent | Recorded as absent rather than assumed permissive |

Seven of ten candidates survived reconciliation. The three withdrawn are listed in `findings.md` rather than deleted, so the next audit does not raise them again.

## What was read in full

- `library.json`
- `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`
- `.github/workflows/gate.yml`
- `AGENTS.md`
- `scripts/version-parity-check.py`

## What was sampled

- `skills/*/SKILL.md`: frontmatter of all four read; bodies of two read in full, two skimmed for structure only.
- `docs/decisions/`: the two records bearing on open candidates read in full; the remaining records read by title only.

## What was skipped, and why

- **Git history beyond `HEAD`.** Out of scope for a structural audit; no finding depends on it.
- **The generated manifests' byte-level agreement with `library.json`.** The generator's own parity gate covers it, and duplicating that check here would report a second opinion with no more evidence behind it.
- **Any runtime behaviour.** Nothing was executed from the audited repository.

## Limits and confidence

High confidence on every claim traceable to a file read in full. Moderate on the drift-resistance judgment in `appraise.md`, which reasons from the generator's design rather than from observed release history. No claim here rests on a tool that did not run.
