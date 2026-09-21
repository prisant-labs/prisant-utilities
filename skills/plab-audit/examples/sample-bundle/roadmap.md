# Roadmap: example-plugin

Ranked 2026-09-20 from the findings in `findings.md`. Every item above the break cites the finding it comes from and names the rung it should be pushed to. Nothing above the break is invented: an item that does not trace to a finding belongs below the break instead.

Ranking uses the standing calibration: token economy, deterministic enforcement over remembering, documentation that agents read, evidence and reversibility, cross-harness durability, session continuity. Contributor onboarding, community growth and external backwards compatibility are unweighted, which is why nothing here is justified by a hypothetical contributor.

## 1. Make the CI gate refuse to skip a check it does not know about

Traces to F-01. **Rung: deterministic enforcement.** Add a step that lists `scripts/*.py` and fails when one is absent from the workflow's enumerated steps. The enumeration stays, because it is legible and ordered; what changes is that leaving a script out becomes loud instead of silent.

Effort: under an hour. Reversible: delete the step.

## 2. Mark every generated file as generated, in the file

Traces to F-02. **Rung: documentation an agent reads.** A `"_generated"` key naming the generator, written by the generator itself, so the warning lives where the mistake is made rather than only in `AGENTS.md`.

Effort: a generator change plus one regeneration. Reversible.

## 3. State the usage-README requirement where an author will meet it

Traces to F-03. **Rung: documentation an agent reads.** One line in `AGENTS.md` naming the requirement and the gate that enforces it. The gate already works; this only moves the discovery earlier than the failed build.

Effort: minutes.

---

## Below the break: speculation

Nothing here traces to a finding. These are ideas, recorded so that the next audit does not have to rediscover them, and explicitly not recommendations.

- **A release-notes generator that reads the changelog.** Plausible, and unevidenced: no measurement here shows the current release step costs enough to be worth automating.
- **Splitting the reference tree per skill.** Would reduce always-on context if the tree grows. It has not grown yet, so the premise is untested.
- **A dashboard over gate history.** Appealing and almost certainly not worth it at this size.
