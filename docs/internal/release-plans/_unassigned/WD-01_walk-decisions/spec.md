---
id: WD-01
title: "plab-walk-decisions: the in-session decision and question walk"
type: spec
status: draft
created: 2026-10-05
updated: 2026-10-05
linked-effort: "the maintainer's private walk-decisions strategy brief, 2026-10-04"
linked-plan: null
linked-release: null
ac-count: 16
source-count: 6
requires-human-review: true
priority: P2
---

# Spec: plab-walk-decisions, the in-session decision and question walk

## Task Summary

**Status:** draft
**Last updated:** 2026-10-05 by claude (Sonnet 5), on initial draft
**Linked plan:** not yet planned
**Open questions:** 7 (6 carried from the design brief as Proposed working defaults, not yet ratified by the maintainer, and 1 Needs info; see Open Questions / Decisions)
**Revisions:** 0

### Acceptance Criteria Fulfillment

- [ ] **AC-1** - Gathering is limited to the conversation and documents touched this session
- [ ] **AC-2** - Items are presented as Q or D, with lettered options and a recommendation on D items
- [ ] **AC-3** - Every sourced item names its source document and that document's own item id
- [ ] **AC-4** - Every Q item states its default if skipped; a D item states none
- [ ] **AC-5** - A one-line answer parses to the exact item and option or text it names
- [ ] **AC-6** - A skipped D item is left untouched; a skipped Q item proceeds on its stated default
- [ ] **AC-7** - A bare accept-all answer is explicit, never inferred from silence
- [ ] **AC-8** - Write-back touches only the three documented surfaces and never the item's own body
- [ ] **AC-9** - A source document on another branch is never written; its edit is reported as text
- [ ] **AC-10** - Every walk produces a walk record naming every item, its answer, and where it landed
- [ ] **AC-11** - The walk record defaults to `_local/decisions/`, or an existing repository convention
- [ ] **AC-12** - ADR promotion for an architectural decision is offered, never performed automatically
- [ ] **AC-13** - The only GitHub action is printing a ready command and body, never filing it
- [ ] **AC-14** - The skill is auto-invocable, with do-NOT-fire clauses for three named cases
- [ ] **AC-15** - Applying answers needs no extra confirmation; only outward actions do
- [ ] **AC-16** - The skill's own description names the deferred future work rather than omitting it

### Currently In Progress

None.

---

## Purpose

`plab-walk-decisions` turns a request the maintainer already types by hand, roughly a dozen times since early September 2026, into a dependable command [S1]. Given the current conversation, the skill finds every pending question and decision inside it, lists each one with context and a recommendation, and accepts the maintainer's answer as a single line of chat.

This spec covers only the first of two planned slices: the in-session walk, including writing each answer back to where its question came from. A second slice, the backlog `--sitting` mode, is explicitly out of scope here, following the design brief's own decision on which slice comes first, D2 (first slice) [S1]. It is named in Non-Goals below.

The format this skill reads and writes is not new. `references/decisions-section.md` already defines the lettered-option, recommendation, and maintainer-block structure this skill operates on, and the maintainer has already hand-run an equivalent walk at least once over a different project's backlog [S2, S4]. This spec packages that existing design into one skill, rather than inventing a new format.

## Scope

### In Scope

1. Gathering pending items from exactly two sources: the current conversation's own unresolved questions and decisions, and the "Open Questions / Decisions" section of any document the session has read or edited.
2. Presenting gathered items in two numbered series: Q, a question whose answer only the maintainer has, and D, a decision carrying two to four lettered options and a recommendation with a stated confidence level.
3. Naming, for every item drawn from a source document, that document and the item's own id there.
4. Accepting a single-line maintainer answer such as "D1 A, D2 B, Q1: the NAS" and parsing each token against the item it names.
5. Writing an answered decision's choice into its source document's maintainer decision block, updating the three surfaces `references/decisions-section.md` defines for a status change, and leaving that item's own body untouched.
6. Writing a walk record for every walk, holding every item, whether answered, skipped, or sourceless, and, for a sourced item, where its answer landed.
7. Writing to a document's maintainer block only when that document's own working-tree branch matches the walk's current branch; otherwise reporting the intended edit as text, never writing it.
8. Offering, never performing, promotion to a MADR architecture decision record for a decided item that meets `references/decisions-section.md`'s own architectural bar.
9. Printing a ready `gh issue create` command and body for a decision where GitHub tracking applies, and never invoking that command.
10. Running from an explicit walk request rather than a manual-only command, carrying a description with do-NOT-fire clauses for three named cases.
11. Treating a skipped decision item and a skipped question item differently: a decision left unanswered is left exactly as found, while a question left unanswered proceeds on its own stated default, recorded in the walk record as assumed rather than decided.
12. Recognizing a bare "ok" or "accept all" answer as an explicit instruction to accept every item's recommendation or default, never inferring acceptance from an answer line's silence.

### Non-Goals

1. The `--sitting` backlog mode: gathering across a repository's specs, plans, session logs, and any tracker of open items; sorting the result into tiers; writing a standalone sitting file. This is slice 2, deferred to its own future spec.
2. Automatically filing a GitHub issue, or managing a GitHub Projects board, for any item.
3. Adding a "Decision" GitHub issue type to any organization's settings. This spec depends on no such type existing.
4. Applying any default to a skipped decision item. Only a skipped question gets a stated default; a skipped decision is left exactly as found (see In Scope item 11).
5. Gathering across more than the current repository, or across more than the current session's own documents.
6. A published web-page rendering of a walk.
7. A persistent, fleet-wide view of open items, such as a redesigned options board for a resume-style skill, or a living status document a wrap-style skill might write in place. The design brief's own decision D8 (overlap with the options board and the living status document) stages this: slice 1, this spec, reads nothing from either surface, and a future `--sitting` slice is where they are expected to merge, because a sitting and either surface would otherwise gather the same "waiting on the maintainer" material twice.

## Users / Actors

| Actor | Role | Interaction |
|---|---|---|
| Maintainer | The only human reader and the only person who answers a walk | Types the walk request, reads the presented items, types the one-line answer, confirms any outward action |
| Running agent (Claude Code or Codex) | Executes the skill | Gathers items, presents them, parses the answer, writes back, writes the walk record |

## Requirements

1. Gathering is limited to two sources: the current conversation's own unresolved items, and the Open Questions / Decisions section of any document the session has read or edited. This is a deliberately narrow slice of a broader gathering design already written for a repository's specs, plans, and session logs; that broader design stays reserved for the `--sitting` mode, outside this spec (see Non-Goals). [S1, S3]
2. A document counts as touched when the current session has read it or written to it. The design brief itself notes that what counts as pending inside a session is not defined anywhere, so this definition is this spec's own judgment call. [S1, model-inference]
3. Every gathered item is presented under one of two series: Q, a question only the maintainer can answer, or D, a decision carrying two to four lettered options and exactly one recommendation with a stated confidence level. [S1, S2]
4. An item drawn from a source document names that document and the item's own id there. An item with no source document is marked as having none, never given a fabricated one. [S1]
5. Every Q item states the default the skill will assume if the maintainer does not answer it. A D item carries no such default, and an unanswered D item is left exactly as found. [S1]
6. The maintainer's answer arrives as one line, such as "D1 A, D2 B, Q1: the NAS". Each token in that line resolves to exactly the item and option, or free text, it names. [S1, S4]
7. A bare answer such as "ok" or "accept all" is recognized as an explicit instruction accepting every item's recommendation or default. Such acceptance is never inferred from an answer line's silence about an item. [S1, model-inference]
8. For a D item with a source document, write-back updates exactly the three surfaces `references/decisions-section.md` defines for a status change: the summary-table row, the subsection header's status, and the maintainer decision block. The item's own Summary, Context, Desired outcome, Options, and Recommendation text is never rewritten. [S2]
9. Write-back to a source document never happens when that document's own working-tree branch differs from the walk's current branch. The walk instead reports the intended edit as text, under the branch it would have targeted. [S1]
10. Every walk produces one walk record, regardless of outcome, naming every presented item, the answer or assumed default each received, and, for a sourced item, where its write-back landed. [S1]
11. The walk record's default location is `_local/decisions/`. When the current repository already defines its own folder for decision or sitting records, the walk record follows that convention instead. [S1]
12. For a decided item meeting `references/decisions-section.md`'s own architectural bar, the skill offers promotion to a MADR architecture decision record; it never performs that promotion without the offer being accepted. [S2]
13. The skill's only GitHub-facing action, for any item, is printing a ready `gh issue create` command and an issue body stating that item's options in full. It never runs the command itself. [S1]
14. The skill carries no `disable-model-invocation` setting and fires from its own description. That description carries explicit do-NOT-fire clauses for a code-walkthrough request, a single standalone decision question, and a status question. [S1, S5, S6]
15. Applying the maintainer's answer line, including write-back to current-branch documents and writing the walk record, happens in the same pass that reads the answer line, without an added confirmation step. [S1, S4]
16. A confirmation step is required only before an action that deletes, pushes, merges, posts externally, or edits a document outside the current repository or the current branch. [S1, S4]
17. The skill's own description and documentation name the `--sitting` backlog mode, automatic GitHub filing, a GitHub Projects board, cross-repository gathering, and a published web-page rendering as deferred or separate work, rather than omitting any of them silently. [S1]

## Acceptance Criteria

**AC-1:** Gathering is limited to exactly two sources per walk: the current conversation's own unresolved items, and the "Open Questions / Decisions" section of a document the session has read or edited. [S1, S3]

**AC-2:** Every gathered item is presented under one of two series, Q for a question only the maintainer can answer, or D for a decision carrying two to four lettered options and exactly one recommendation with a stated confidence level. [S1, S2]

**AC-3:** An item drawn from a source document names that document and the item's own id there, for example "D4, from the WD-01 spec's D1." An item with no source document is marked as having none. [S1]

**AC-4:** Every Q item states the default the skill will assume if the maintainer skips it. A D item states no default, and an unanswered D item is left exactly as found. [S1]

**AC-5:** A one-line answer parses to the exact item, and the option or text, it names. [S1, S4]
  Given: an answer line reading "D1 A, D2 B, Q1: the NAS"
  When: the skill reads it
  Then: D1 resolves to option A, D2 resolves to option B, and Q1's free text is captured verbatim, with no other item changed.

**AC-6:** A skipped item is handled differently by series. [S1]
  Given: an answer line that omits D3 and Q2
  When: the walk applies the given answers
  Then: D3's source document is not written to and D3's status is unchanged, while Q2 proceeds on its own stated default, and the walk record marks Q2's value as assumed rather than decided.

**AC-7:** A bare answer such as "ok" or "accept all" is treated as an explicit instruction accepting every presented item's recommendation or default. Such acceptance is never inferred from an answer line's silence about an item. [S1, model-inference]

**AC-8:** Write-back to a sourced item's document updates only the three surfaces `references/decisions-section.md` names for a status change: the summary-table row, the subsection header's status, and the maintainer decision block. The item's own Summary, Context, Desired outcome, Options, and Recommendation text is never rewritten. [S2]

**AC-9:** A branch mismatch blocks the write. [S1]
  Given: a source document whose own working-tree branch differs from the walk's current branch
  When: the walk applies an answer targeting that document
  Then: no write happens to that document, and the walk's output reports the intended edit as text, naming the branch it would have targeted.

**AC-10:** Every walk produces one walk record, regardless of outcome, naming every presented item, the answer or assumed default it received, and, for a sourced item, where its write-back landed. [S1]

**AC-11:** The walk record's default location is `_local/decisions/`. When the current repository already defines its own folder for decision or sitting records, the walk record is written there instead. [S1]

**AC-12:** For a decided item meeting `references/decisions-section.md`'s own architectural bar, the skill offers promotion to a MADR architecture decision record. It never performs that promotion without the offer being accepted. [S2]

**AC-13:** For any item, the skill's only GitHub-facing action is printing a ready `gh issue create` command and an issue body stating that item's options in full. It never runs the command itself. [S1]

**AC-14:** The skill carries no `disable-model-invocation` setting and fires from a trigger matching an explicit walk request. Its description carries do-NOT-fire clauses for a code-walkthrough request, a single standalone decision question, and a status question. [S1, S5, S6]

**AC-15:** Applying the maintainer's answer line, including write-back to current-branch documents and writing the walk record, happens in the same pass that reads the answer line. A confirmation step is required only before an action that deletes, pushes, merges, posts externally, or edits a document outside the current repository or the current branch. [S1, S4]

**AC-16:** The skill's own description and documentation name the `--sitting` backlog mode, automatic GitHub filing, a GitHub Projects board, cross-repository gathering, and a published web-page rendering as deferred or separate, rather than omitting any of them silently. [S1]

## Behavior / Examples

### Example 1: A walk with one decision and one question (grounds AC-2, AC-5, AC-8, AC-10)

The maintainer asks for a walk mid-session. The skill finds one open decision in a spec the session edited earlier, and one question with no source document, drawn from the conversation itself. It presents:

```
D1 (sync authority), from the WD-07 spec's D2. Options A/B/C. Recommendation: A.
Q1 (deploy target). No source document. Default if skipped: staging.
```

The maintainer answers "D1 A, Q1: production". The skill writes D1's choice into the WD-07 spec's maintainer decision block, updating its table row, its subsection header's status, and the maintainer block itself, and leaves the rest of that item's body untouched. It writes a walk record noting Q1's answer as production, decided rather than assumed, and noting where D1's answer landed.

### Example 2: A branch mismatch (grounds AC-9)

A gathered decision's source document lives on a branch other than the one currently checked out. The maintainer answers it along with two other items. The skill writes the other two answers normally, and for this one prints the intended maintainer-block edit as text, naming the branch the document actually lives on, with nothing written to disk.

### Example 3: Silence versus an explicit skip (grounds AC-6, AC-7)

A walk presents D1 through D3 and Q1. The maintainer answers "D2 B, Q1: the NAS, accept the rest". D1 and D3 each already carry a stated recommendation, and "accept the rest" explicitly applies each one. The skill writes D1 and D3 back as their recommended options because the answer said so, not merely because the line left them unmentioned.

## Non-Functional Requirements

| Category | Requirement | Source |
|---|---|---|
| Portability | The one-line maintainer answer format, such as "D1 A, Q1: free text", is the contract that works in both Claude Code and Codex. A structured prompt such as Claude Code's own multiple-choice tool may present the same items, but the skill's correctness never depends on one being available. | [S1] |
| Safety | Any tracked output this skill ever writes, including a promoted architecture decision record or a printed GitHub issue body, cites no path under `_local/` and no path outside the current repository, matching this plugin's own public-repository convention. | [S1, S6] |

## Revisions

| Date | Author | Type | Description |
|------|--------|------|-------------|
| 2026-10-05 | claude | added | Initial draft created |

## Sources & Evidence

- **[S1]** The maintainer's private walk-decisions strategy brief, 2026-10-04. Maintainer-local, gitignored, exists on disk. Class A; the primary design source for this spec, read in full.
- **[S2]** `references/decisions-section.md` (this repository). Class A, read in full; defines the item format, the three-surface write-back rule, and the ADR-promotion lifecycle this skill reuses.
- **[S3]** A private toolchain design document in the maintainer's own working notes, its section on the decision and task layer, 2026-08-26. Maintainer-local, gitignored, exists on disk. Class A, read in full; the source for the finding that gathering signals from specs, plans, and session logs is already designed, and for the caution against surfacing every open item at once.
- **[S4]** A hand-built decision-sitting document in the maintainer's own private planning project, 2026-10-03. Maintainer-local, outside this repository, exists on disk. Class A; its opening instructions and its "Answer sheet" section were read directly, and are the precedent for the one-line batch-answer format and for confirming only outward actions.
- **[S5]** `skills/plab-continue-session/SKILL.md` (this repository). Class A; precedent for a narrowed description carrying a do-NOT-fire clause for a status question, rather than disabling model invocation.
- **[S6]** `AGENTS.md` (this repository). Class A; records the design frame favoring a narrowed description over a manual-only flag, and the convention that a tracked document in this repository cites no gitignored path.

### Unverified Claims

- "A document counts as touched when the current session has read it or written to it." Appears in Requirements item 2. The design brief names the gap this definition fills, but does not itself define it.
- "A bare answer such as 'ok' or 'accept all' is recognized as an explicit instruction accepting every item." Appears in Requirements item 7 and AC-7. The exact trigger wording is this spec's own choice.

### Gaps

- Whether Codex exposes a structured multiple-choice prompt equivalent to Claude Code's own tool is unverified. The plain-text answer line (Requirements item 6) is the contract this spec relies on regardless of the answer. [S1]
- How reliably the skill locates and edits the correct maintainer decision block, when another session edits the same file at the same time, is untested. This spec's branch guard (AC-9) narrows that risk without removing it. [S1]

## Open Questions / Decisions

**What these statuses mean.** `Proposed` marks an answer this spec adopted as a working default, drawn directly from the design brief's own recommendation, so that this document could be written; the maintainer has not seen or ratified it. `Needs info` marks a question only the maintainer can answer. Nothing in this section carries maintainer approval. Ratify or overturn every `Proposed` row, and answer the `Needs info` row, before this spec's status moves past `draft`. Two further decisions the design brief raised, D2 (first slice) and D8 (overlap with the options board and the living status document), are not repeated here: D2 is already settled in Scope above, and D8's resolution is recorded as a Non-Goal above rather than as an open row, because this spec does not touch either surface it would otherwise weigh against.

| ID | Title | Resolution | Status | Updated |
|----|-------|------------|--------|---------|
| D1 | Skill name | (none) | Proposed | 2026-10-05 |
| D3 | Numbering and item types | (none) | Proposed | 2026-10-05 |
| D4 | Where answers are recorded | (none) | Proposed | 2026-10-05 |
| D5 | Where the walk record lives | (none) | Proposed | 2026-10-05 |
| D6 | GitHub issues | (none) | Proposed | 2026-10-05 |
| D7 | Invocation | (none) | Proposed | 2026-10-05 |
| Q1 | What happened to past walk answers | (none) | Needs info | (none) |

### D1: Skill name (Proposed)

**Summary.** What this skill should be called.

**Context.** An earlier proposal for the same functionality used a different name. The maintainer's own recent phrasing favors "walk decisions," and the name is also this skill's strongest trigger phrase. [S1]

**Desired outcome.** The name matches words the maintainer already types, and covers both this spec's in-session walk and a later backlog mode.

**Options / approaches.**

* **Option A:** `plab-walk-decisions`. Matches the maintainer's own phrasing and this plugin's verb-first naming pattern.
* **Option B:** `plab-decision-sitting`. Matches the earlier proposal and a hand-built precedent, but names the rarer backlog case.
* **Option C:** `plab-decisions`. Short and neutral, but reads as a record viewer rather than an action.

**Recommendation.** Option A, which this spec adopts throughout as its working default.

**Confidence:** Medium.

---

> **Maintainer decision:** _(pending ratification)_
>
> * **Status:** Proposed as this spec's working default; NOT yet ratified
> * **Choice (proposed):** Option A, `plab-walk-decisions`
> * **Reasoning:** Matches the phrasing the maintainer already uses, which is the strongest trigger a description can carry.
> * **Proposed by / date:** claude, drafting session 2026-10-05. No maintainer input has been received on this item.

### D3: Numbering and item types (Proposed)

**Summary.** How items inside a walk should be numbered and typed.

**Context.** Earlier hand-built walks used three different numbering schemes, and one of them let a group letter collide with an option letter. [S1]

**Desired outcome.** Every answer is unambiguous when typed as one line in chat.

**Options / approaches.**

* **Option A:** Two series, Q for maintainer-only information and D for a lettered decision, uppercase options, no group letters; a clarification counts as a Q.
* **Option B:** One D series only, with a question marked by the Needs info status instead of its own series.
* **Option C:** A section letter plus a number, with lowercase options, matching an existing hand-built precedent.

**Recommendation.** Option A, which this spec adopts throughout Scope, Requirements, and Acceptance Criteria above.

**Confidence:** High.

---

> **Maintainer decision:** _(pending ratification)_
>
> * **Status:** Proposed as this spec's working default; NOT yet ratified
> * **Choice (proposed):** Option A, the Q and D series with uppercase options
> * **Reasoning:** Matches the maintainer's own prompt, and this section is itself a working test of the scheme.
> * **Proposed by / date:** claude, drafting session 2026-10-05. No maintainer input has been received on this item.

### D4: Where answers are recorded (Proposed)

**Summary.** Where an answer goes once the maintainer gives it.

**Context.** `references/decisions-section.md` already makes a source document's maintainer block the authoritative record for a sourced item. A separate walk record is still useful for an item with no source document. [S1, S2]

**Desired outcome.** An answer sits beside its own question, and a whole walk can still be reviewed later as one record.

**Options / approaches.**

* **Option A:** Write back to the source document's maintainer block for a sourced item, and keep one walk record covering every item, including where each sourced item's answer landed.
* **Option B:** Keep one walk record only, and leave every source document untouched.
* **Option C:** Write a MADR architecture decision record for every decided item.

**Recommendation.** Option A, which is this spec's write-back and walk-record design above (Requirements items 8 and 10).

**Confidence:** Medium, because write-back reliability stays the open implementation risk (see Gaps above).

---

> **Maintainer decision:** _(pending ratification)_
>
> * **Status:** Proposed as this spec's working default; NOT yet ratified
> * **Choice (proposed):** Option A
> * **Reasoning:** Reuses the standard's own maintainer-block rule for sourced items, and covers the common in-session case where no source document exists.
> * **Proposed by / date:** claude, drafting session 2026-10-05. No maintainer input has been received on this item.

### D5: Where the walk record lives (Proposed)

**Summary.** Whether the walk record is tracked or local, and where it is written.

**Context.** A walk record can carry candid notes, similar to a session log, and this repository is public. [S1]

**Desired outcome.** Nothing private ships by accident, and the record stays findable by a later session.

**Options / approaches.**

* **Option A:** Default to `_local/decisions/`; follow an existing decision or sitting-record folder convention instead, when the current repository already has one.
* **Option B:** Always tracked, under a documented decisions folder in the repository.
* **Option C:** Always local, with no repository-convention override.

**Recommendation.** Option A, which this spec adopts as AC-11.

**Confidence:** High.

---

> **Maintainer decision:** _(pending ratification)_
>
> * **Status:** Proposed as this spec's working default; NOT yet ratified
> * **Choice (proposed):** Option A
> * **Reasoning:** Mirrors the same reasoning that already put session logs under `_local/`, and respects a convention the maintainer's own other planning project already follows.
> * **Proposed by / date:** claude, drafting session 2026-10-05. No maintainer input has been received on this item.

### D6: GitHub issues (Proposed)

**Summary.** What role GitHub issues play in a walk.

**Context.** No "Decision" issue type exists in the maintainer's GitHub organization today, and this repository has never filed an issue. [S1]

**Desired outcome.** GitHub becomes part of the workflow only once the maintainer's own behavior shows it is a place they look.

**Options / approaches.**

* **Option A:** The skill prints a ready `gh issue create` command and body per item; it never files on its own.
* **Option B:** A flag files the issue directly once the maintainer confirms.
* **Option C:** Leave GitHub out of this skill entirely.

**Recommendation.** Option A, which this spec adopts as AC-13.

**Confidence:** Medium, because it depends on a usage test that has not yet run.

---

> **Maintainer decision:** _(pending ratification)_
>
> * **Status:** Proposed as this spec's working default; NOT yet ratified
> * **Choice (proposed):** Option A
> * **Reasoning:** Costs almost nothing, keeps the option open, and avoids adding a sixth design to an already-undecided tracking question.
> * **Proposed by / date:** claude, drafting session 2026-10-05. No maintainer input has been received on this item.

### D7: Invocation (Proposed)

**Summary.** Whether the skill can start itself from the model's own reading of the conversation, or only by an explicit command.

**Context.** Two sibling skills in this plugin run only by explicit command. Two others moved from that mode to automatic invocation guarded by an explicit do-NOT-fire clause, which this plugin's own documentation records as the better instrument. [S1, S5, S6]

**Desired outcome.** The skill fires on a genuine walk request, and never on a code walkthrough, a single standalone decision question, or a status question.

**Options / approaches.**

* **Option A:** Automatic invocation, with a do-NOT-fire clause for those three cases.
* **Option B:** Manual only, requiring an explicit command every time.

**Recommendation.** Option A, which this spec adopts as AC-14.

**Confidence:** Medium, because trigger accuracy is only provable after real use.

---

> **Maintainer decision:** _(pending ratification)_
>
> * **Status:** Proposed as this spec's working default; NOT yet ratified
> * **Choice (proposed):** Option A
> * **Reasoning:** The trigger phrase is distinctive and used weekly, so the description cost is worth paying.
> * **Proposed by / date:** claude, drafting session 2026-10-05. No maintainer input has been received on this item.

### Q1: What happened to past walk answers (Needs info)

**Summary.** After roughly a dozen earlier in-session walks the maintainer typed by hand, did any answer ever need to be found again later, or was each one acted on at once and then forgotten?

**Context.** This decides whether write-back genuinely belongs in this first slice, or whether a lighter, format-only skill would already have been enough. [S1]

**Default if skipped.** This spec assumes an answer mattered later at least some of the time, so write-back and the walk record both stay in this slice's scope (Requirements items 8 through 11).

---

> **Maintainer decision:** _(pending)_
>
> * **Status:** Needs info
> * **Choice:** (none)
> * **Reasoning:** (none)
> * **Decided by / date:** (none)
