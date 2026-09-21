# Calibration and the mechanization ladder

How roadmap items are ranked, and how far down each recommendation should be pushed.

This is a written default, not a question the skill asks. The maintainer has already answered it, and asking again at every run would be a worse use of their attention than getting the order slightly wrong occasionally.

## The weighted factors

In order. When two items compete, the one higher on this list wins.

1. **Token economy.** Always-on context is paid in every session, forever, by one person. A change that reduces what must be loaded before anything happens outranks a change of similar size elsewhere.
2. **Deterministic enforcement over remembering.** A rule a machine checks beats a rule a person remembers, every time. An item that converts a remembered intention into a gate is worth more than its line count suggests.
3. **Documentation that agents read.** Instruction files, decision records and conventions an agent loads. Distinct from documentation humans read, which is not unimportant but is not weighted here.
4. **Evidence and reversibility.** Can the change be shown to work, and can it be undone. A change with a proof attached outranks a larger change without one.
5. **Cross-harness durability.** Whether the thing survives a move between Claude Code, Codex and whatever comes next. Plain Markdown and committed scripts survive; harness-specific configuration does not.
6. **Session continuity.** Whether work survives a context reset, a machine change or a handoff to another agent.

## Explicitly unweighted

These are not oversights and they are not worth arguing for in a roadmap item.

- **Contributor onboarding.** The repositories this skill audits are built for their maintainer's own use. A second contributor is hypothetical.
- **Community growth.** Same reason.
- **External backwards compatibility.** There is no external consumer whose upgrade path constrains a decision.

**Do not justify an item by an unweighted factor.** If the only argument for a change is that a future contributor would find it easier, that argument does not rank here, and the item belongs below the speculation break if it belongs anywhere.

This does not mean such changes are wrong. It means the audit has no standing to rank them.

## The mechanization ladder

Every roadmap item above the break names the rung it should end at. Push each recommendation as far down the ladder as it will honestly go, and no further.

| Rung | What it is | When it is the right stopping point |
|---|---|---|
| **CI check** | Runs on every push or pull request, blocks on failure | The rule is objective, cheap to evaluate, and its violation matters enough to stop work |
| **Committed script** | Exists in the repository, run by hand or by a person's habit | The rule is objective but too slow, too expensive, or too situational to gate on |
| **Documented convention** | Written down where the person or agent doing the work will read it | The rule needs judgment to apply, or the cost of mechanizing exceeds the cost of the occasional miss |
| **Remembered practice** | Nothing written, nothing run | Almost never the right answer. Use it when writing the rule down would cost more attention than the rule saves |

### Two rules about the ladder

**A gate that cannot be shown failing is not a gate.** An item that recommends the CI-check rung is incomplete unless it also says how the check would be proven to fail when the rule it guards is removed. If no canary is possible, the honest rung is one higher.

**Do not mechanize a prose rule literally.** A rule that reads clearly because a human applies judgment can be under-specified in ways only mechanization exposes. The known instance in this corpus: a path-citation rule applied literally produced 13 flags with 11 false positives, worse than the gate it replaced, because separators appear in slash commands, repo slugs, git refs, globs, placeholders and URLs. Mechanize the structure, never the prose.

## Severity against rank

They are different axes and they disagree often.

**Severity** describes the consequence of leaving a finding alone. It belongs in `findings.md` and it is about the finding.

**Rank** describes the order to act. It belongs in `roadmap.md` and it is about the maintainer's next week.

A Medium finding that unblocks four others outranks a High finding that stands alone. A Critical finding whose remedy is a rewrite may rank below three one-paragraph fixes. When rank and severity disagree, say so in the item, in one sentence. The reader will notice the disagreement, and an unexplained one reads as an error.

## Estimating cost

Give an order of magnitude and nothing finer: one line, one paragraph, an hour, a day, a project. Do not produce hour estimates for work you have not scoped, and do not sum them into a total that implies precision the parts do not have.

Where a whole list is cheap, say so once, at the top. That is a result: it tells the maintainer the audit found no large problems, which is different from the audit finding nothing.
