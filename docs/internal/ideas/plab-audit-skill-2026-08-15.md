---
title: "plab-audit: a repo appraisal and roadmap skill"
type: strategy-brief
status: draft
created: 2026-08-15
audience: maintainer
generated-by: strategy-brief
---

# plab-audit: Appraising a Repository, Not Just Grading It

> **Design frame.** This plugin is built for its maintainer's own use. The repository is public because there is no reason for it not to be, not because the skills are aimed at an adoption curve. Nothing below should be traded away to serve a hypothetical third-party user. Where a general-purpose choice and a personally-useful choice diverge, the personally-useful one wins.

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

- The only user is the maintainer. Not a team, not an adoption curve.
- "Repository" means any repo, not only agent-skill plugins. A skill that only audits plugins is a much smaller idea.
- The output is a durable document, consistent with how this plugin's other producing skills behave.
- Cost matters. A skill that burns a large token budget per run will be used once and abandoned.

**Gap in the input:** the ask does not say whether this runs on *your own* repositories, on *unfamiliar* ones you are sizing up, or both. That still changes the design, though a single-user frame narrows it: the honest answer is probably "mostly mine, occasionally not," which argues for optimising the known-repo path and letting the unfamiliar case degrade gracefully rather than being a first-class mode.

## 2. Problem Space

### Why now

The audit workflow already exists. It has been performed by hand at least three times over recent months, each time reproducing the same shape from scratch: scope the repository, fan out evidence gathering, collect findings with file and line citations, verify the high-severity claims independently, then write a verdict with a prioritized recommendation set.

Each run produced a genuinely useful artifact. Each run also re-derived the method from nothing, which is the classic signal that a workflow is ready to become a skill. A prior backlog captured this observation and accepted it as a proposal; this brief is the design pass that proposal was waiting for.

Two of those hand-run audits changed a real decision. One of them reversed a planned course of action entirely. That is a strong argument that the artifact has value; it is not yet an argument that the *skill* will get used, and Section 3 treats that gap honestly.

### What "solved" looks like

The maintainer points the skill at a repository and, within one session, has a document that changes what they do next. Not a document they would send to someone; a document that reorders their own queue. It says what the repository is good at, what is rotting, what is missing, and what the next three things to build are, in order, with reasons. Every claim in it can be traced to a file and a line.

The success test is behavioural and personal: **did the roadmap change the order of work?** A beautifully written audit that confirmed what the maintainer already believed has produced nothing.

The failure state is a document full of true, generic observations. "Add more tests." "Improve documentation." "Consider CI." A repository audit that could have been written without reading the repository is worse than no audit, because it consumes attention and produces the feeling of progress.

### Who is affected

One person: the maintainer, working across their own active repositories and the occasional unfamiliar one they are sizing up. That is the whole user base, and designing for it is a constraint worth using rather than apologising for.

What it buys: the objective function is knowable rather than guessed (see Calibration in Section 7), the ecosystems that matter are a short finite list, and no effort goes into onboarding, configurability, or graceful behaviour in situations that will never arise.

What it costs: there is no second user whose non-use would signal a problem. If the maintainer does not reach for this skill, it has no value at all. That makes adoption the dominant risk rather than one risk among several, which Section 3 treats accordingly.

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

**The value summary is underserved.** Plenty of tools produce findings. Very few will tell you what a repository is worth and why. That is the part a maintainer cannot easily get elsewhere, and on an unfamiliar repository it is the fastest route from nothing to orientation.

### Weaknesses

**Three jobs in one skill is a real risk.** Audit, appraisal, and ideation use different muscles and produce different artifacts. Bundling them can yield a document that does all three shallowly. The modes design in Approach A is the mitigation, but the risk does not disappear.

**Repository size destroys naive designs.** A skill that reads everything will exhaust context on any serious repository. Every viable design must be a sampling strategy with an explicit, stated coverage claim. An audit that silently examined 6% of a repository while sounding comprehensive is actively harmful.

**Ideation is the weakest leg.** "New features and innovations" is where a language model is most likely to produce confident, generic, unhelpful output. Recommending "add a plugin system" to a repository that should not have one is worse than silence.

### Risks

**Adoption is not a risk among several; with one user it is the entire risk.** A prior portfolio audit of a comparable collection found seven of ten skills with zero confirmed invocations. The strongest predictor of dormancy was not quality; it was that the maintainer already had a working manual habit and never switched. This skill would be built directly on top of a working manual habit, by the person who is already good at performing it by hand. That is simultaneously the best evidence that the artifact is valuable and the best evidence that the skill will sit unused.

The single-user frame makes this sharper, not softer. There is no population of other users to carry a skill the author neglects, and no external signal to notice the neglect. The mitigation has to be structural: make the cheap mode genuinely cheaper and faster than doing it by hand, because convenience is the only thing that displaces a working habit.

**Cost risk.** The hand-run precedent used multi-agent fan-out and consumed a substantial token budget per audit. If that becomes the default, the skill is reserved for special occasions and never becomes routine. Routine use is what would make it valuable, and with one user there is nobody else generating the usage that would justify the build.

**Scope-creep risk.** "Audit a repo" invites every check anyone has ever wanted. Without a firm boundary, this becomes a meta-skill that duplicates linters, security scanners, and conformance gates, all of which do their narrow job better.

### Open questions

- Is this a skill or a *mode* of the existing peer-review skill? Both take an artifact, apply structured dimensions, produce findings with severity, and end with prioritized actions. The shapes rhyme closely enough that the why-gate must be answered explicitly rather than assumed.
- Does it run on unfamiliar repositories, or only ones the maintainer knows? Unfamiliar repositories need far more orientation work and cannot rely on the user to correct wrong assumptions.
- Is the roadmap opinionated or optioned? A ranked list implies the skill knows the maintainer's goals. It does not.

### Concerns

The deepest concern was **calibration**: a roadmap ranks items against each other, which requires knowing what the maintainer is optimising for. Absent that, the ranking is a guess wearing the costume of an analysis.

The single-user frame largely dissolves this. With one known user, the objective function can be written down once, as a default the skill carries rather than a question it asks. Section 7 sketches what that default looks like. Contributor onboarding, for instance, can be dropped from the ranking entirely rather than weighted, because it is not an objective here.

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
- Ecosystem breadth. Support the two or three ecosystems actually in use, and let everything else fall back to language-agnostic checks (git history, structure, docs, dependency manifests). With one user this is a short finite list, not a product decision.
- The ideation leg. Ship `--appraise` and `--audit` first. "New features and innovations" is the weakest leg and benefits most from seeing what the first two modes actually surface.

**Confidence: medium-high on the artifact, medium-low on adoption.**

High on the artifact because the method is proven and the output has already changed decisions twice. Low on adoption because the dormancy evidence is specifically unkind to skills that formalise an existing manual habit, and because with one user there is no second party whose usage could rescue it.

The mitigation is a dogfood gate, and the single-user frame lets it be a sharper one than usual: **no feature work beyond v1 until the skill has produced one roadmap that actually reordered the maintainer's queue.** Not "until it has been run once", which is trivially satisfiable and proves nothing. The test is whether the output changed a decision, which is the same bar the two successful hand-run audits cleared. That pattern has been applied to other skills in this family and should apply here with no exemption for being the newest idea.

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

**Evidence gaps, stated plainly.** There is no cost measurement for the proposed cheap path, and no evidence at all on the ideation leg, which has never been hand-run as a distinct exercise. The adoption estimate in Section 5 reasons from one adjacent dataset rather than measuring this skill.

One gap that would matter for a general-purpose tool is deliberately not listed: how this performs for a user who is not the maintainer. Under the design frame, that is not a gap. It is out of scope.

## 7. Uncertainties and Open Items

**Top open question, no longer blocking.** Own repositories, unfamiliar repositories, or both? The single-user frame supplies a workable default: optimise the known-repo path, where the skill can skip orientation and go straight to judgment, and let the unfamiliar case degrade gracefully rather than being a co-equal mode. Worth confirming, but no longer a decision that has to precede design.

**The why-gate, blocking.** Skill or mode of the existing peer-review skill? Genuinely uncertain. The shapes rhyme, but the inputs differ (a document versus a tree) and so does the cross-model requirement. *Recommend answering via the backlog intake gate rather than by intuition.*

**Calibration, now low uncertainty and an opportunity.** With one known user the objective function can be a written default rather than a question. From observed working patterns, the ranking should weight:

1. **Token and cost economy.** Always-on context cost, per-run cost, and the cheapest model that does the job. Recommendations that add recurring cost need to earn it explicitly.
2. **Deterministic enforcement over remembering.** A rule enforced by a hook, a gate, or CI beats a rule written in a document. Prefer recommending the mechanism over the reminder.
3. **Evidence and reversibility.** Claims traceable to file and line; archive rather than delete; changes that can be undone.
4. **Cross-harness durability.** Things that work in more than one agent harness, not just the one in front of you.
5. **Session continuity.** Work that survives the gap between sessions without the maintainer holding state in their head.

Explicitly *not* weighted: contributor onboarding, community growth, backwards compatibility for external consumers. Those are real objectives for other repositories and noise for this one.

The remaining uncertainty is whether to hard-code that list, read it from a declared objectives file in the repository under audit, or both. Reading it is more general; hard-coding it is more useful on day one.

**Where it lives, medium uncertainty, and the single-user frame makes it sharper.** A general-purpose utility plugin, or a separate plugin installed only when this kind of work is happening? The always-on description cost is paid by exactly one person in every one of their sessions, forever, whether the skill fires or not. If audits are genuinely occasional, a separate plugin, or shipping it here with model invocation disabled so it only runs on explicit command, is the more honest trade. Both options keep it one command away.

**Output convention, low uncertainty.** Default to this plugin's standard generated-artifact root under the skill's own name, with an explicit destination flag for cases where the audit should be tracked in the repository under review. The prior backlog proposal suggested a different default; the plugin-wide convention should win for consistency.

**Naming, now near-irrelevant.** "Audit" undersells it, since the value summary and roadmap are the differentiated parts and neither is an audit. With no market to communicate to, the only cost of a mediocre name is that the description has to work harder to trigger correctly, and the description matters far more than the name. Spend the minute on the description instead.

---

**Suggested follow-ups.** This brief can become a component proposal for backlog intake (which is where the why-gate gets answered), or a specification once the why-gate is settled. The recommended next artifact is neither: it is the hand-run example document from Section 5, step 2, because it converts every design argument here into something checkable.
