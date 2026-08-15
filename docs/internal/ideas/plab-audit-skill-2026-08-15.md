---
title: "plab-audit: a repo appraisal and roadmap skill"
type: strategy-brief
status: draft
created: 2026-08-15
audience: public
generated-by: strategy-brief
---

# plab-audit: Appraising a Repository, Not Just Grading It

## 1. What I Understand

The proposal is a new skill for this plugin that takes a repository as input and returns two things:

1. **A summary of the repository's value.** What this codebase is, what it is worth, what it is actually for. Not a file listing.
2. **A prioritized roadmap.** Improvements, new features, and innovations, ordered so a maintainer knows what to do on Monday.

Three sub-threads are bundled in that ask, and they are genuinely different jobs:

- **Audit** asks *what is wrong here*. Findings, severity, evidence.
- **Appraisal** asks *what is this worth, and to whom*. A judgment about value, maturity, and fit.
- **Ideation** asks *what should exist next*. Generative, not diagnostic.

Most tools in this space do only the first. Deterministic linters, conformance gates, and security scanners all produce findings. Very few produce an appraisal, and almost none produce a roadmap that ranks a *new feature idea* against a *hygiene fix* on one list.

Assumptions I am making, flagged so they can be corrected:

- The primary user is a solo maintainer or a very small team, not an enterprise audit function.
- "Repository" means any repo, not only agent-skill plugins. A skill that only audits plugins is a much smaller idea.
- The output is a durable document, consistent with how this plugin's other producing skills behave.
- Cost matters. A skill that burns a large token budget per run will be used once and abandoned.

**Gap in the input:** the ask does not say whether this is meant to run on *your own* repositories, on *unfamiliar* repositories you are evaluating, or both. That distinction changes the design substantially, and Section 7 treats it as the top open question.

## 2. Problem Space

### Why now

The audit workflow already exists. It has been performed by hand at least three times over recent months, each time reproducing the same shape from scratch: scope the repository, fan out evidence gathering, collect findings with file and line citations, verify the high-severity claims independently, then write a verdict with a prioritized recommendation set.

Each run produced a genuinely useful artifact. Each run also re-derived the method from nothing, which is the classic signal that a workflow is ready to become a skill. A prior backlog captured this observation and accepted it as a proposal; this brief is the design pass that proposal was waiting for.

Two of those hand-run audits changed a real decision. One of them reversed a planned course of action entirely. That is a strong argument that the artifact has value; it is not yet an argument that the *skill* will get used, and Section 3 treats that gap honestly.

### What "solved" looks like

A maintainer points the skill at a repository and, within one session, has a document they would actually send to a collaborator. It says what the repository is good at, what is rotting, what is missing, and what the next three things to build are, in order, with reasons. Every claim in it can be traced to a file and a line.

The failure state is a document full of true, generic observations. "Add more tests." "Improve documentation." "Consider CI." A repository audit that could have been written without reading the repository is worse than no audit, because it consumes attention and produces the feeling of progress.

### Who is affected

- **The maintainer of an active repository** wants to know what to fix next and whether the thing they are worried about is actually the problem.
- **Someone inheriting a repository** wants orientation: what is this, is it healthy, where are the landmines.
- **Someone evaluating a dependency or an acquisition target** wants an appraisal they can defend.

These three want the same document at different weightings. The first wants the roadmap. The second wants the value summary. The third wants the evidence.

### Adjacent problems this does not solve

Deliberately out of scope, because each is already served:

- **Conformance grading for skill libraries.** A deterministic gate already exists for that, and it is model-free, which is a genuine advantage this skill cannot match. Reimplementing it would be strictly worse.
- **Security review of a diff.** Harness-native review commands cover changed code.
- **Cross-model review of a single document.** That is what this plugin's peer-review skill already does, and the why-gate question in Section 3 asks whether audit is really a mode of it.

## 3. Analysis

### Strengths

**The method is proven, not speculative.** This is not a skill designed from an idea of what auditing should be. It codifies a procedure that has been executed by hand, repeatedly, with results that changed decisions. Skills built from a real repeated workflow have a far better adoption record than skills built from an appealing concept.

**The evidence discipline is the differentiator.** Findings that carry a file and a line are checkable. Findings that do not are opinions. The hand-run precedent already enforced this, and it is the single practice most likely to make output trustworthy rather than plausible.

**Adversarial verification has already earned its keep.** In one hand-run audit, an independent verification pass over the initial findings materially corrected a headline claim (an undercount that was wrong by more than an order of magnitude) and surfaced several whole categories the first pass had missed. That is direct evidence that a single analysis pass is insufficient for this artifact, and that a critic pass is not ceremony.

**The value summary is underserved.** Plenty of tools produce findings. Very few will tell you what a repository is worth and why. That is the part a maintainer cannot easily get elsewhere, and it is the part most likely to be forwarded to another person.

### Weaknesses

**Three jobs in one skill is a real risk.** Audit, appraisal, and ideation use different muscles and produce different artifacts. Bundling them can yield a document that does all three shallowly. The modes design in Approach A is the mitigation, but the risk does not disappear.

**Repository size destroys naive designs.** A skill that reads everything will exhaust context on any serious repository. Every viable design must be a sampling strategy with an explicit, stated coverage claim. An audit that silently examined 6% of a repository while sounding comprehensive is actively harmful.

**Ideation is the weakest leg.** "New features and innovations" is where a language model is most likely to produce confident, generic, unhelpful output. Recommending "add a plugin system" to a repository that should not have one is worse than silence.

### Risks

**Adoption risk is the dominant one, and the evidence is unfriendly.** A prior portfolio audit of a comparable skill collection found that seven of ten skills had zero confirmed invocations. The single strongest predictor of a skill going unused was not quality; it was that the maintainer already had a working manual habit and never switched. This skill is being built precisely on top of a working manual habit. That is both its best evidence and its biggest threat.

**Cost risk.** The hand-run precedent used multi-agent fan-out and consumed a substantial token budget per audit. If that becomes the default, the skill is reserved for special occasions and never becomes routine. Routine use is what would make it valuable.

**Scope-creep risk.** "Audit a repo" invites every check anyone has ever wanted. Without a firm boundary, this becomes a meta-skill that duplicates linters, security scanners, and conformance gates, all of which do their narrow job better.

### Open questions

- Is this a skill or a *mode* of the existing peer-review skill? Both take an artifact, apply structured dimensions, produce findings with severity, and end with prioritized actions. The shapes rhyme closely enough that the why-gate must be answered explicitly rather than assumed.
- Does it run on unfamiliar repositories, or only ones the maintainer knows? Unfamiliar repositories need far more orientation work and cannot rely on the user to correct wrong assumptions.
- Is the roadmap opinionated or optioned? A ranked list implies the skill knows the maintainer's goals. It does not.

### Concerns

The deepest concern is **calibration**. A roadmap ranks items against each other, which requires knowing what the maintainer is optimizing for: shipping speed, correctness, contributor onboarding, cost. Absent that, the ranking is a guess wearing the costume of an analysis. Any credible design has to either elicit the objective up front or present the ranking as conditional on a stated objective.

### Situational lens: token economy

Every skill in a plugin pays an always-on cost, because its description sits in context for every session whether it fires or not. A skill used four times a year still bills you continuously. This argues for one skill with modes rather than three skills, and it argues for a tight description. It is also a reason to consider whether this belongs in a general-purpose utility plugin at all, or in a separate plugin a maintainer installs only when doing this kind of work.

### Situational lens: reversibility

An audit is a read-only act. Nothing it does is destructive, and a bad audit costs attention rather than data. That makes this a low-risk skill to ship early and iterate on, which meaningfully lowers the bar for a first version.

## 4. Approaches

### Approach A: One skill, three modes

`--appraise` (what is this worth), `--audit` (what is wrong), `--roadmap` (what next). Modes compose: running all three is the default full report, and each can be run alone.

- **Pros.** One description to pay for. Matches the modal pattern already used elsewhere in this plugin, where a peer-review skill carries three modes and a release skill carries five subcommands rather than fragmenting into separate skills. Lets a user take the cheap part (`--appraise`) without paying for the expensive part.
- **Cons.** A three-mode skill is harder to describe well, and description quality is the strongest predictor of whether a skill fires at all.
- **Risks.** Modes that are never used individually are just complexity.
- **Effort.** Moderate. The mode boundary is the main design work.

### Approach B: Deterministic-first, judgment-second

The skill runs whatever objective tooling the repository already supports (tests, linters, conformance gates, dependency audits, git history statistics), then confines the model to interpreting those results and to the judgments no tool can make.

- **Pros.** Strongest possible grounding. Every hygiene finding traces to a tool exit code rather than an opinion. Dramatically cheaper, because the model reads summaries rather than source. Naturally avoids duplicating existing gates, since it *invokes* them.
- **Cons.** Coverage is hostage to what the repository already has. A repository with no tests and no linter yields almost nothing from the deterministic layer, and those are exactly the repositories most in need of an audit.
- **Risks.** Tempting to over-trust green checks. A repository can pass every gate and still be a bad codebase.
- **Effort.** Moderate, with real per-ecosystem work to detect and invoke the right tools.

### Approach C: Multi-agent fan-out with adversarial verification

Codify the hand-run precedent directly: parallel scouts over different dimensions, a synthesis pass, then an independent critic that tries to refute the high-severity findings and hunts for missed categories.

- **Pros.** This is the design with demonstrated results. The critic pass has already caught a materially wrong headline claim and several missed categories in practice. It scales to large repositories because scouts each hold a narrow slice.
- **Cons.** Expensive per run. Needs a harness that can fan out, which limits portability across agents. Most repositories do not warrant it.
- **Risks.** Building the heavyweight version first and discovering it gets used twice a year. This is the specific failure the dormancy evidence warns about.
- **Effort.** High.

### Approach D: Thin single-pass

One analysis pass over a sampled slice, producing a short document. No fan-out, no tool invocation, no critic.

- **Pros.** Cheap, fast, portable, trivially easy to build.
- **Cons.** This is the design most likely to produce the generic output that Section 2 names as the failure state. Without a critic pass, there is nothing to catch a confident wrong claim.
- **Risks.** Ships, disappoints once, is never used again. The worst outcome, because it also poisons appetite for a better version.
- **Effort.** Low.

## 5. The 80/20 Recommendation

**Build Approach A's mode structure on Approach B's deterministic spine, and make Approach C's fan-out an explicit opt-in flag rather than the default. Do not build Approach D.**

The reasoning is about sequencing rather than preference. The fan-out design is the one with proven results, but proven for *occasional, high-stakes* audits. The thing that does not exist yet, and would be used far more often, is a cheap audit a maintainer runs on a normal Tuesday. Deterministic-first is what makes that cheap version credible: it grounds hygiene findings in tool output instead of model opinion, and it keeps the model doing only what tools cannot.

Modes matter because they let cost track intent. `--appraise` on a repository should be minutes and pennies. `--audit --deep` on the same repository can be expensive, because the maintainer chose it.

**Next steps, in order:**

1. **Answer the why-gate before writing any file.** Is this a skill, or a mode of the existing peer-review skill? Write the answer down either way. If it is a mode, this brief becomes an enhancement proposal instead, and that is a perfectly good outcome.
2. **Hand-run the target output once more, deliberately, on a repository that is not this plugin.** Produce the exact document the skill should produce. That artifact becomes the specification and the test fixture. Do not write `SKILL.md` before this exists.
3. **Design the coverage statement first.** Decide how the skill declares what it examined and what it skipped, before designing anything else. This is the constraint that keeps the output honest, and retrofitting it is painful.

**Explicitly defer:**

- The fan-out implementation. Ship the single-pass deterministic version, use it on real repositories, and let demand justify the expensive path.
- Ecosystem breadth. Support one ecosystem well rather than five shallowly.
- The ideation leg. Ship `--appraise` and `--audit` first. "New features and innovations" is the weakest leg and benefits most from seeing what the first two modes actually surface.

**Confidence: medium-high on the artifact, medium-low on adoption.**

High on the artifact because the method is proven and the output has already changed decisions. Low on adoption because the dormancy evidence is specifically unkind to skills that formalize an existing manual habit, and because this skill would be built by someone who is already good at doing it by hand. The mitigation is a dogfood gate: no feature work beyond v1 until one real end-to-end run exists on a repository the maintainer did not write. That pattern has been applied to other skills in this family and should apply here too, with no exemption for being the newest idea.

## 6. Evidence and Source Map

| Claim | Source | Strength |
|---|---|---|
| The audit workflow has been hand-run at least three times with the same shape | Maintainer's private working records, recent months | Strong, first-hand |
| An independent verification pass materially corrected a headline finding and surfaced missed categories | One of those hand-run audits, where the corrected figure was wrong by more than an order of magnitude | Strong, specific |
| Seven of ten skills in a comparable collection had zero confirmed invocations | A prior portfolio audit of that collection | Strong, and the basis for the adoption concern |
| Bundling modes beats fragmenting into skills | Existing skills in this plugin use three modes and five subcommands respectively, rather than splitting | Moderate, internal precedent |
| A skill's description quality predicts whether it fires | Prior audit finding that a skill's own misconfigured description was a plausible cause of its non-adoption across seven later opportunities | Moderate, single case but a mechanism |
| Deterministic gates outperform model judgment on conformance | Existing model-free conformance tooling in this ecosystem | Strong for that narrow scope |
| Repositories exceed usable context | General, uncontroversial | Strong |

**Evidence gaps, stated plainly.** There is no data on how a comparable skill performs for someone who is *not* the maintainer, no cost measurement for the proposed cheap path, and no evidence at all on the ideation leg, which has never been hand-run as a distinct exercise. The adoption estimate in Section 5 is reasoning from one adjacent dataset, not measurement of this skill.

## 7. Uncertainties and Open Items

**Top open question, blocking.** Own repositories, unfamiliar repositories, or both? Auditing an unfamiliar repository requires an orientation phase and cannot lean on the user to catch wrong assumptions. Auditing a known repository can skip most of that and go straight to judgment. Building for both without deciding produces a skill that is mediocre at each. *Requires human judgment; nothing here can settle it.*

**The why-gate, blocking.** Skill or mode of the existing peer-review skill? Genuinely uncertain. The shapes rhyme, but the inputs differ (a document versus a tree) and so does the cross-model requirement. *Recommend answering via the backlog intake gate rather than by intuition.*

**Calibration, high uncertainty.** How does the skill learn what the maintainer is optimizing for? Options include asking once at invocation, reading a declared objective from repository configuration, or presenting the roadmap as conditional on two or three named objectives. The third is the most honest and the least convenient.

**Where it lives, medium uncertainty.** A general-purpose utility plugin, or a separate plugin installed only when this kind of work is happening? The always-on description cost argues for the latter if the skill is genuinely occasional.

**Output convention, low uncertainty.** Default to this plugin's standard generated-artifact root under the skill's own name, with an explicit destination flag for cases where the audit should be tracked in the repository under review. The prior backlog proposal suggested a different default; the plugin-wide convention should win for consistency.

**Naming, low uncertainty.** "Audit" undersells it, since the value summary and roadmap are the differentiated parts and neither is an audit. Worth one minute of thought before the name is locked, because renaming a shipped skill is expensive.

---

**Suggested follow-ups.** This brief can become a component proposal for backlog intake (which is where the why-gate gets answered), or a specification once the two blocking questions are settled. The recommended next artifact is neither: it is the hand-run example document from Section 5, step 2, because it converts every design argument here into something checkable.
