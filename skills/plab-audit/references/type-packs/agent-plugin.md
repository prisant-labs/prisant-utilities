# Type pack: agent-plugin

**Detected by:** `library.json` or `.claude-plugin/plugin.json` at the repository root.

**What this covers:** a repository whose product is skills, agents, hooks or commands loaded by an agent harness. Claude Code plugins, Codex plugins, and skill libraries.

**Provenance.** This pack is written from the hand-run fixture audit of nonfiction-studio, 2026-09-20, not from a list drawn up in advance. Where the two disagreed, the fixture won. The specific correction: the implementation plan named five `prisant-utilities` Python scripts as the primary tools, and four of them turned out not to apply to any other repository. That is recorded below rather than quietly fixed, because the same mistake is available to anyone extending this pack.

## Tools, in order

### 1. The conformance gate, in machine mode

```bash
node <agent-skills-toolkit>/scripts/check.mjs <target> --json
```

**Use `--json`. Never rely on the human output.** This is the single most important line in this pack.

On the fixture, the human output was four lines ending `0 error(s), 0 warning(s).` with no finding lines at all. The same command with `--json` returned **152 findings**, every one `severity: "error"`. The two suppression mechanisms that produced the discrepancy are both legitimate, and neither is visible in the human summary:

| Field | What it means |
|---|---|
| `effectiveSeverity: "off"` | The requirement sits above the repository's declared tier, so the tier ceiling switches it off |
| `suppressed: true` with a `ceiling` object | A migration ceiling, usually `{pinned, from, to, due}`, holding a graduated rule at a lower severity because of the repository's declared `standard` |
| `suppressionReason` | Present when the repository configured the suppression itself. **Read it in full.** Truncating it is how the fixture audit's first draft went wrong |

Record `findings.length`, the breakdown by `check`, and the breakdown by `effectiveSeverity`. A repository reporting zero errors while holding a hundred findings is a fact worth stating, whether or not any of them is actionable.

`--strict` disables the ceiling, which is useful for seeing what the pin is deferring. Run it only if you intend to report on the pin.

### 2. The repository's own gate scripts

**Run these before reaching for anything external.** A repository that ships its own checks has encoded what it believes about itself, and those checks are both a tool and a document.

Find them in `scripts/`, `bin/`, or the `scripts` block of `package.json`. Run each, record the exit code.

**Read each script's header before running it.** Most carry a usage line, and an argument you guessed is how you generate a false finding: on the fixture, invoking a release-tag checker with `.` where it wanted a tag produced a spurious exit 1 and three manifest "mismatches" that did not exist.

### 3. Vendored-versus-upstream comparison, if the repository vendors a toolchain

A repository that vendors its validation spine has taken on an obligation to track the delta. Check whether it has:

```bash
diff <target>/scripts/check.mjs <agent-skills-toolkit>/scripts/check.mjs
comm -13 <(ls <target>/scripts/checks/ | sort) <(ls <agent-skills-toolkit>/scripts/checks/ | sort)
comm -23 <(ls <target>/scripts/checks/ | sort) <(ls <agent-skills-toolkit>/scripts/checks/ | sort)
```

Look for an attribution file, usually `scripts/ATTRIBUTION.md`, recording the upstream commit and copy date. Two questions: how old is the pin, and does the file record the modifications it promises to record.

**Checks present upstream and absent from the fork cannot run in that repository's CI.** Name them, and name what is therefore unchecked. On the fixture this was how a live divergence from the declared Standard stayed invisible: the check that would have caught it was one of the five the fork did not carry.

### 4. Description scoring, with its caveat

```bash
node <agent-skills-toolkit>/scripts/checks/description-score.mjs <target>
```

`THRESHOLD = 0.7`. **A score of exactly 0.65 is checked before it is called a defect.** ADR 0049 in the toolkit documents that a description whose `WHEN` pattern the English lexicon cannot match caps at 0.65 and cannot pass at any quality. A 0.65 is therefore a likely tool artifact rather than a bad description, and reporting it as a defect wastes a rewrite.

### 5. Always-on context measurement

Extract `name` plus `description` from every `SKILL.md` frontmatter block, collapse whitespace, and total the characters. This is the floor of what the plugin costs before it does anything.

Report the number and the per-skill average. **Do not attach it to a budget the repository is not under.** Check `agent-targets` in `library.json` first: the 8,000-character fallback skill-list budget is a Codex constraint, and a Claude-only plugin is not subject to it. The fixture's 8,563 characters would have been "107% of budget" under the wrong yardstick and is in fact an unremarkable per-skill average across more skills.

### 6. Component inventory against disk

Compare what the manifests enumerate against what exists in `skills/`, `agents/`, `hooks/` and `commands/`. Both directions: catalogued but missing, and present but uncatalogued.

**Verify the consequence before repeating it.** A registration check asserting that an unregistered skill "ships but is invisible to installers" is asserting something testable. Claude Code discovers skills from the `skills/` directory on disk, and a control repository whose manifest enumerates no components while its skills demonstrably load refutes the claim in one comparison. Find a control before publishing a delivery failure.

## What this pack deliberately does not run

Recorded because the alternative is a future extender re-adding them.

**`prisant-utilities`' own Python gates do not apply to other repositories.** `frontmatter-check.py`, `doc-lifecycle-check.py`, `version-parity-check.py` and `gen-release-index.py` validate against schemas, a release-plan corpus and a series legend specific to that repository. Run against any other agent-plugin repo they report the absence of a structure it never claimed to have. `check-dashes.py` is repo-wide but enforces a house style other repositories have not adopted.

**`path-citation-check.py` is never invoked.** It false-positives on every markdown inline link and its fix is an open item awaiting maintainer approval. Note it in the coverage statement as unavailable-pending-fix rather than running it and recording noise.

**Third-party plugin validators are optional accelerators only.** `plugin-dev:plugin-validator` and its kin are useful when installed and absent when not; the superpowers plugin was disabled on 2026-09-01 and any installed plugin can vanish the same way. Never make one a required step, and state the fallback wherever one is named.

## Judgment questions

The deterministic layer cannot answer these. They are the reason a model runs this and not a shell script.

1. **Is there a front door?** Does a root `AGENTS.md` exist, and does it carry the conventions an agent would otherwise have to recover by reading source? Is there a `CLAUDE.md` bridging to it, given that Claude Code does not load `AGENTS.md` on its own?
2. **Where does this repository record decisions, and is that place reachable from the root?** Trace one non-obvious convention back to where it is written down and count the hops.
3. **Does each skill's description distinguish it from its siblings?** Two skills that would both plausibly fire on the same request are one skill with a configuration flag, or a boundary that needs stating in both descriptions.
4. **Is anything enforced twice or zero times?** A rule in a skill's prose and a gate that checks it is good. A rule in prose with no gate, or two gates checking the same thing differently, is not.
5. **What does the repository declare as next, and does the tree agree?** A changelog describing one change in two tenses, a stalled branch named in a current plan, a roadmap citation that resolves to nothing tracked.
6. **What is the release posture, and is it stated?** Tags, releases, and whether an untagged repository says anywhere that it means to be.

## Snapshot rows for this type

Beyond the standard snapshot: declared standard and tier, declared agent targets, skill count on disk against manifest count, agent count, hook event count, CLI count, total name-plus-description characters, presence of root `AGENTS.md` and `CLAUDE.md`, and whether the validation spine is vendored.
