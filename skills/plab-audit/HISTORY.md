# History - plab-audit

| Version | Date | Release | Type | Summary |
|---|---|---|---|---|
| 1.0.0 | 2026-09-20 | unreleased | added | First version. Three composable modes, three type packs, one docs lens, a coverage statement, and a canary-proven bundle self-check. |

## 1.0.0 - 2026-09-20

**Added: the skill, specified by a hand-run audit rather than by a design.**

The workflow this codifies had been run by hand at least four times before it became a skill, most recently against `prisant-utilities` on 2026-08-29 and against `nonfiction-studio` on 2026-09-20. Each run re-derived the method from nothing, which is the signal that a workflow is ready to become a skill.

The parent brief, `docs/internal/ideas/plab-audit-skill-2026-08-15.md`, stalled at its own step 1 for 35 days: whether audit was a skill or a mode of `plab-ai-review`. The maintainer closed it on 2026-09-19 in these words: "plab-ai-review is more about a general review that an ai writes. my audit goal is a more holistic audit."

**What ships:** three modes, `--appraise`, `--audit` and `--roadmap`, composable and defaulting to all three. Three type packs, `agent-plugin`, `tauri` and `generic`, detected from disk with a `--type` override. One lens, `--lens=docs`. A five-file output bundle to a gitignored per-run folder. A coverage statement on every run, in every mode. A labelled break in `roadmap.md` separating evidenced items from speculation.

**The one rule the skill is built around, and the reason it exists:** the deterministic layer produces candidates, not findings. A candidate becomes a finding only after being reconciled against what the audited repository has already decided, in its decision records, suppression configuration, release notes, changelog and any prior audit.

That rule was not in the original specification. It was added as AC-15 on 2026-09-20, after the fixture run that specified this skill produced 15 candidates and published 8. All seven withdrawals came from that single step. Two were the highest-ranked findings of the first draft. One of them recommended converting a manifest's component list to a different shape, which the audited repository's own suppression config records as already tested and rejected, with the measured result: it clears the warnings and produces 28 errors from a competing check that requires the opposite shape.

A skill built without that step would have shipped that recommendation, with a severity label on it.

**Explicit invocation only,** by maintainer ruling of 2026-09-19. This makes `plab-audit` the second skill carrying `disable-model-invocation: true`, alongside `plab-init-project`. The parent brief argued the opposite, on the grounds that a skill built to displace a working manual habit cannot displace it if it only runs when named. That argument is recorded rather than re-fought, with one consequence noted: if the skill goes unused, a weak description is no longer a candidate cause, so the dogfood gate becomes the only adoption signal available.

**`scripts/bundle-check.py` is the skill's own gate.** Three states, 0 clean, 1 findings, 2 broken, because two states cannot distinguish a well-formed bundle from a checker that has stopped working. Seven rules, each proved against a canary that must fail, plus a well-formed anti-canary, a legitimate appraise-only partial, and an absent-directory case that must report broken rather than findings.

Two corrections to its specification were made while writing it. The plan said it should assert that all five bundle files exist; that is wrong for a mode-composable skill, because `--appraise` legitimately writes two, so the mode is inferred from what is present and each file is checked against its own rules. And rule 6 resolves a cited finding identifier against the headings in `findings.md` rather than pattern-matching something finding-shaped, because a roadmap citing `F-12` in a bundle whose findings stop at `F-08` is precisely the defect the rule exists to catch.

**Deliberately not in 1.0.0**, each with its reason:

- **`--lens=publish-readiness`**, cut on 2026-09-19. Both design briefs attribute it to a backlog proposal whose source document is not in this repository and was not located. Building it would mean guessing at a design from a second-hand summary.
- **`--deep` multi-agent fan-out**, described in the parent brief and never designed to an executable specification.
- **`--ideate` as a formal chain** to `plab-strategy-brief`. The mechanism exists and was verified, but it requires a scope amendment to that skill. Speculation ships instead as a labelled section at the foot of `roadmap.md`, which preserves the epistemic separation without the amendment.
- **A persistent committed audit file that diffs across runs.** A v2 candidate.
