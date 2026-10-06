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
| `effectiveSeverity: "off"` | The repository's profile turns the rule off. Under `profile: "plain-plugin"`, set in `askit.config.json`, the toolkit switches off its house conventions: U1, U2, U5, U16 and the whole S and G series. This is not a tier-ceiling marker |
| `suppressed: true` with a `ceiling` object | A migration ceiling, usually `{pinned, from, to, due}`, holding a graduated rule at a lower severity because of the repository's declared `standard` |
| `suppressionReason` | Present when the repository configured the suppression itself. **Read it in full.** Truncating it is how the fixture audit's first draft went wrong |

**The tier ceiling carries no per-finding marker. A profile does, and the two are easy to confuse.** Until 2026-10-06 this pack said that the tier-ceiling marker varied with the toolkit version. It does not. On the same toolkit commit, `549eb32` (`v1.20.0-2`), `prisant-utilities` returned 35 above-tier findings, all at `effectiveSeverity: "error"` with `suppressed: false` and `ceiling: null`. `nonfiction-studio` returned 150 at `"off"`. The difference is the profile: `prisant-utilities` runs the default `askit-library` profile, which keeps every rule's declared severity, and `nonfiction-studio` sets `plain-plugin`, which the toolkit's `scripts/lib/profiles.mjs` uses to switch the house conventions off. The fixture's "off" findings came from the same profile.

Under either profile, only three things reveal the tier ceiling: `errorCount: 0` against a non-empty `findings` array, the `tierReport` object, and `reqId` values from a series above the declared tier, such as G4 to G10 under a `universal` declaration. Read all three before concluding that a finding is live. Record `config.profile` from the JSON, because it says which rubric the repository chose to be graded against. Record the toolkit version with `git -C <agent-skills-toolkit> describe --tags`, because CI may pin a different one.

Record `findings.length`, the breakdown by `check`, and the breakdown by `effectiveSeverity`. A repository reporting zero errors while holding a hundred findings is a fact worth stating, whether or not any of them is actionable.

`--strict` disables the ceiling, which is useful for seeing what the pin is deferring. Run it only if you intend to report on the pin.

### 2. The repository's own gate scripts

**Run these before reaching for anything external.** A repository that ships its own checks has encoded what it believes about itself, and those checks are both a tool and a document.

Find them in `scripts/`, `bin/`, or the `scripts` block of `package.json`. Run each, record the exit code.

**Read each script's header before running it.** Most carry a usage line, and an argument you guessed is how you generate a false finding: on the fixture, invoking a release-tag checker with `.` where it wanted a tag produced a spurious exit 1 and three manifest "mismatches" that did not exist.

### 3. Vendored-versus-upstream comparison, if the repository vendors a toolchain

A repository that vendors its validation spine has taken on an obligation to track the delta. Two different questions apply, and each needs its own baseline:

- **A. Was the vendored copy edited?** Compare it against the upstream commit it was copied from, the pin.
- **B. How far behind upstream is it?** Compare it against upstream `HEAD`.

Start with the attribution file, usually `scripts/ATTRIBUTION.md`, which records the pin and the copy date. Then extract both baselines to a scratch folder outside the target. `git archive` reads the toolkit at any commit without touching its worktree:

```bash
pin=<commit recorded in the target's attribution file>
mkdir -p <scratch>/pinned <scratch>/head
git -C <agent-skills-toolkit> archive "$pin" scripts | tar -x -C <scratch>/pinned
git -C <agent-skills-toolkit> archive HEAD scripts | tar -x -C <scratch>/head

# A. Edited? Content differences against the pin, per vendored folder
diff -rq --strip-trailing-cr <scratch>/pinned/scripts/checks <target>/scripts/checks
diff -rq --strip-trailing-cr <scratch>/pinned/scripts/lib <target>/scripts/lib

# B. Stale? Upstream checks the copy does not carry
comm -13 <(ls <target>/scripts/checks/ | sort) <(ls <scratch>/head/scripts/checks/ | sort)
```

**Never report a B result as an A finding.** Until 2026-10-06 this step diffed the target against the toolkit's current files and nothing else. That comparison answers B but reads like A, and the fixture audit's highest-ranked finding, "vendored spine modified", was a B result reported as A. Against its pin, `nonfiction-studio`'s vendored `checks/` and `lib/` folders show 0 content differences. Against upstream `HEAD`, the same `checks/` comparison shows 22.

**`--strip-trailing-cr` is required on a Windows checkout.** With `core.autocrlf=true` the working tree carries CRLF line endings, and without the flag the same comparison against the pin reported 49 false differences.

In A's output, `Only in <target>` lines are files the repository added inside the vendored folders, and `Only in <pinned>` lines are upstream files it chose not to vendor. Ask of the attribution file whether it records both, and whether it records the modifications it promises to record.

**Checks present upstream and absent from the fork cannot run in that repository's CI.** Name them, and name what is therefore unchecked. On the fixture this was how a live divergence from the declared Standard stayed invisible: the check that would have caught it was one of the five the fork did not carry.

### 4. Description scoring, with its caveat

```bash
node --input-type=module -e '
import { pathToFileURL } from "node:url";
const [tk, target] = process.argv.slice(1);
const lib = (p) => import(pathToFileURL(`${tk}/scripts/${p}`).href);
const { loadPlugin } = await lib("lib/load-plugin.mjs");
const s = await lib("checks/description-score.mjs");
for (const k of loadPlugin(target).skills) {
  const d = k.frontmatter?.description ?? "";
  const v = s.englishDensity(d) < s.READABLE_FLOOR ? "NOT SCORED" : s.scoreDescription(d).toFixed(2);
  console.log(`${v}  ${k.name ?? k.dir}`);
}' <agent-skills-toolkit> <target>
```

**Do not run `description-score.mjs` directly.** It is a library module with no command-line entry point, so `node .../checks/description-score.mjs <target>` loads it, does nothing, prints nothing and exits 0. This pack named exactly that command until 2026-10-05, when its first real run caught it. The command above builds the context with the toolkit's own loader and calls the module's exported scorer, so it prints one line per skill. **If it prints nothing, it did not run.** Record that as a coverage gap, never as a clean result. `check.mjs` also runs this check as U5, but only reports scores below the threshold, so its silence does not tell you what the scores were.

`NOT SCORED` is the toolkit declining to score a description its English lexicon cannot read (ADR 0049). It is not a pass and not a failure.

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
