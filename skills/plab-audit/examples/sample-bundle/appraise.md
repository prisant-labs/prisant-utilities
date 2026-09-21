# Appraisal: example-plugin

## What it is

An agent-skill plugin distributed to two harnesses from one manifest. `library.json` is the canonical source; the native manifests under `.claude-plugin/` and `.codex-plugin/` are generated from it. Four skills, one shared reference tree, one conformance gate in CI.

## What it is worth

**The generated-manifest discipline is the asset.** One source of truth, two targets, a generator that refuses to be hand-edited. A plugin that maintained three manifests by hand would drift within two releases; this one cannot drift without the generator being bypassed, and the gate notices when it is.

**The gate is real.** `.github/workflows/gate.yml` runs the conformance check on every pull request and blocks the merge. It reports and never fixes, which keeps the authority over content with the maintainer rather than with a formatter.

## What it is not

Not a product. `AGENTS.md` states the design frame plainly: the repository is public because there is no reason for it not to be, not because it targets adopters. Findings below are scored against that frame, so "no contributor onboarding guide" is not a defect here and does not appear.

## Confidence

Moderate. The manifest and CI claims are directly verified against files read in full; see `evidence.md`. The claim about drift resistance is a judgment from the generator's design, not a measurement over release history.
