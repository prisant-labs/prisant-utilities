# Appraisal: example-plugin

Appraised 2026-09-20 against `main` at `0000000`. Illustrative: `example-plugin` is not a real repository, as `README.md` explains. This document answers what the repository is and what it is worth. What is wrong with it is in `findings.md`; what to do next is in `roadmap.md`.

## 1. What this is

An agent-skill plugin distributed to two harnesses from one manifest. `library.json` is the canonical source, and the native manifests under `.claude-plugin/` and `.codex-plugin/` are generated from it. Four skills, one shared reference tree, one conformance gate in CI.

The organising idea is a single source of truth with generated targets: an author edits one file, and a generator produces everything a harness reads. `docs/decisions/0002-generated-manifests.md` records the choice.

It is not a product. `AGENTS.md` states the design frame plainly: the repository is public because there is no reason for it not to be, not because it targets adopters. The findings are scored against that frame, so "no contributor onboarding guide" is not a defect here and does not appear.

## 2. Current status

| Item | Observed |
|---|---|
| Version | `1.2.0` in `library.json`. The four documentation locations that claim it agree, by `scripts/version-parity-check.py`, exit 0 |
| Last release | `1.2.0`, the newest dated entry in `CHANGELOG.md`. Tags were not listed |
| Last commit | `0000000`, `HEAD` of `main` |
| Open pull requests | Not queried. Local clone only |
| Branches in flight | Not queried |
| Working tree | Clean |
| Skills | 4 |
| Conformance | Universal tier, 0 errors, 0 warnings, by `check.mjs`, exit 0 |
| Dependency scanning | Not assessed. `cargo audit` is not installed, exit 127; see `evidence.md` |

## 3. Recent history

This section reads `CHANGELOG.md`, because git history beyond `HEAD` was skipped. The unit is the release, since the changelog dates each one.

**1.2.0 added the fourth skill.** **1.1.0 moved the native manifests to generation from `library.json`**, which is the change `docs/decisions/0002-generated-manifests.md` records. Every release since then has shipped its manifests from the generator rather than by hand.

## 4. What it is good at

- **The generated-manifest discipline is the asset.** One source of truth, two targets, and a generator that refuses to be hand-edited. A plugin that maintained three manifests by hand would drift within two releases. This one cannot drift without the generator being bypassed, and the gate notices when it is. This is a judgment from the generator's design, not a measurement over release history, and `evidence.md` rates it accordingly.
- **The gate is real.** `.github/workflows/gate.yml` runs the conformance check on every pull request and blocks the merge. It reports and never fixes, which keeps authority over content with the maintainer rather than with a formatter.
- **Version claims are checked, not trusted.** `scripts/version-parity-check.py` compares every documented version with the declared one and fails the build on a disagreement, so a stale version string cannot reach `main` through a green pull request.

## 5. What the repository declares as next

The only planning artifact in the tracked tree is the `## [Unreleased]` section of `CHANGELOG.md`. It lists one item: every skill now has a usage README under `docs/skills/`. No release plan or roadmap file is tracked. If one exists outside the tree, this audit could not see it.

## 6. Declared plans against observed state

Two comparisons, and both agree. Agreement is a result, so it is reported as plainly as a disagreement would be.

**Agreement: the unreleased usage READMEs.** `CHANGELOG.md` lists them as landed and unreleased. Four skills have four usage READMEs, and `scripts/version-parity-check.py`, which requires one per skill, exits 0. No tag follows the entry, so "landed but unreleased" is exactly the observed state.

**Agreement: the version.** The changelog's newest dated release, `1.2.0`, is the version `library.json` declares.

## 7. Standing back

This is a small plugin whose engineering lives mostly in one decision: an author edits one file, and everything a harness reads is generated from it. That decision is recorded, enforced by a gate on every pull request, and it is why every version claim this audit looked at agrees.

The constraint is not a missing rule. It is where the rules are stated. Each of the three findings is a rule that exists and is enforced, but is announced one step away from the place an author meets it. F-01: which checks CI runs is decided in the workflow file, not where a check is added. F-02: a manifest's generated status is stated in `AGENTS.md`, not in the manifest. F-03: the usage-README requirement is stated by a failing build, not by `AGENTS.md`. That shared cause is why every item in `roadmap.md` is small: each one makes an existing rule visible, or loud, at the place where it is broken.
