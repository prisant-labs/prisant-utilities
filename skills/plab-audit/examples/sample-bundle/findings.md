# Findings: example-plugin

Three findings. Each carries a severity, a file path, and a line number where the finding is line-scoped. Candidates withdrawn after reconciliation against the repository's own recorded decisions are listed at the end, because a withdrawn candidate is a result and deleting it invites the next audit to raise it again.

## F-01 - Medium: the CI gate enumerates its checks and globs nothing

`.github/workflows/gate.yml:44-58` lists each check as its own named `run:` step. A check added to `scripts/` is therefore not run by CI until someone also edits the workflow, and nothing reports the omission. The failure is silent in the direction that matters: the check exists, passes locally, and never runs on a pull request.

**Severity rationale.** Medium rather than High because the enumeration is deliberate and legible; the risk is a future omission, not a present hole.

**Reconciliation.** No decision record addresses this. Not withdrawn.

## F-02 - Medium: a generated manifest is writable and carries no generated-file marker

`.claude-plugin/plugin.json` is produced by the generator named in `AGENTS.md`, but the file itself says nothing about that. An agent reading it in isolation has no way to know a hand-edit will be overwritten on the next regeneration.

**Severity rationale.** Medium. The convention is documented centrally, so the information exists; it is just not reachable from the file where the mistake is made.

**Reconciliation.** Checked against the repository's decision records. None covers file-level markers. Not withdrawn.

## F-03 - Low: the usage README requirement is enforced but not stated

`scripts/version-parity-check.py:184-207` requires every skill to carry `docs/skills/<name>/README.md` with exactly one `**Version:**` line, and fails the build when one is missing. `AGENTS.md` does not mention the requirement, so the first time an author learns of it is a red pull request.

**Severity rationale.** Low. The gate message is clear and the fix is a one-file addition.

**Reconciliation.** Not withdrawn.

## Withdrawn candidates

- **"The plugin should pin its Standard version."** Withdrawn. The repository tested a pin and recorded the result against it; raising it again would recommend a change already rejected on measured evidence.
- **"No contributor onboarding guide."** Withdrawn against the stated design frame in `AGENTS.md`, which excludes adoption affordances by standing decision.
