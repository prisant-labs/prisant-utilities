---
id: D-10
title: Make derive-log-facts.py's output the single log-format contract
type: spec
status: draft
created: 2026-08-23
updated: 2026-08-23
linked-effort: _local/skill-roadmaps/2026-08-18/pair-defects.md
linked-plan: implementation-plan.md
ac-count: 7
source-count: 12
requires-human-review: false
target-release: v0.6.0
linked-release: docs/internal/release-plans/plan_v0.6.0/plan_v0.6.0.md
priority: P2
---

# Spec: Make derive-log-facts.py's output the single log-format contract

## Task Summary

**Status:** Draft
**Last updated:** 2026-08-23
**Linked plan:** `implementation-plan.md`
**Open questions:** 4 items, all decided and recorded below (see Open Questions / Decisions); none genuinely open
**Revisions:** Initial draft created 2026-08-23

### Acceptance Criteria Fulfillment

- [ ] AC-1: "hostname" derivation text confined to the script, not scattered across reference docs
- [ ] AC-2: `frontmatter-schema.md`'s own example matches its own Tier 1 table
- [ ] AC-3: The stale "18-field" claim appears nowhere in the skill's shipped documentation
- [ ] AC-4: Continue's Phase 2 field list no longer independently hand-enumerated
- [ ] AC-5: The versioned-together pairing claim, in one of its two current wordings, asserted in exactly one shipped file
- [ ] AC-6: Docs README's per-section descriptions defer to `SKILL.md` rather than restating it
- [ ] AC-7: This effort does not start before W-02 ships and wires the script

### Currently In Progress

None.

## Purpose

D-10 (the source roadmap's own numbering; no zero-padding transformation is needed since the source already writes it as two digits) is named as the structural cause under four already-diagnosed defects: D-1 (trigger narrowing reached the router but not the program), D-2 (a behavior change shipped with no version trail), D-5 (same-arc superseding logs have no mechanism), and D-8 (the wrap skill fails its own gate, inside its own references). All four are instances of one disease: the wrap and continue session-log format has no single source of truth. [S1]

The template lives in wrap's references, the parsing expectations live in continue's references, the frontmatter schema is a third document, and a claim that the two skills "move and version together" is asserted more than once with nothing checking it. [S1] This spec depends on W-02 (Derive session-log facts from git instead of model recall, `docs/internal/release-plans/plan_v0.6.0/W-02_derived-log-facts/spec.md`): once `derive-log-facts.py` exists, its actual output becomes the contract for every field it derives, and this effort's job is to make every other document defer to it and delete what they used to restate independently, rather than to build a new shared-schema artifact. [S1, S11]

## Scope

### In Scope

1. Rewrite `skills/plab-wrap-session/references/frontmatter-schema.md`: for every field `derive-log-facts.py` produces, replace hand-written derivation-method text with a pointer to the script; keep the tiering rationale and the guidance for fields the model still authors; fix the Example Frontmatter block's self-contradiction (it currently omits `type` and `machine`, both required by its own Tier 1 table) or replace the block with a pointer to the script's own real output.
2. Rewrite `skills/plab-wrap-session/references/session-log-template.md`: per-field inline comments for derived fields point at the script instead of restating the derivation method (today "# hostname" appears three times, once per mode).
3. Rewrite `skills/plab-continue-session/SKILL.md` Phase 2 and `skills/plab-continue-session/references/handoff-display.md`: state the field list once, deferring to the same contract, following the cross-skill-deferral pattern already shipped at `skills/plab-wrap-session/SKILL.md:104`.
4. Rewrite `docs/skills/plab-wrap-session/README.md`: remove the stale field-count claim and the independently restated Tier table and Output Shape field enumeration; point at the single reference instead.
5. Rewrite `docs/skills/plab-continue-session/README.md` wherever it independently restates fields or the pairing claim.
6. Consolidate the versioned-together pairing claim (today in `skills/plab-continue-session/HISTORY.md:69` and root `README.md:17`) to exactly one location.
7. Bump `plab-continue-session` to 1.6.0: `SKILL.md` `metadata.version`, a new `HISTORY.md` entry, a `CHANGELOG.md` bullet, continue's `version` field in `library.json`, continue's row in root `README.md`'s skill table, and a regeneration of the derived manifests.

### Non-Goals

1. Does not modify `derive-log-facts.py` or any file under `skills/plab-wrap-session/scripts/`. That script belongs to W-02, which must already have shipped and been wired into wrap's `SKILL.md` before this effort starts (AC-7).
2. Does not modify `skills/plab-wrap-session/SKILL.md`'s Evidence Gathering or Frontmatter sections. W-02 owns wrap's own consumption of the script; re-touching that file here would let two specs claim the same edit.
3. Does not add a new automated CI check or drift detector for future contract drift. The source is explicit that a shared schema should not be built as a separate artifact; a new detector here would be the same mistake in code form. D-3 (the hygiene sweep's one-directional documentation-drift check, gaining its missing direction) and D-11 (three-state gate canaries) already own that territory and are sequenced into v0.4.0, ahead of this release.
4. Does not change any session log's actual runtime shape. No field is renamed and no mode's output changes; this is a documentation and reference consolidation, not a format change.
5. Does not touch `AGENTS.md`. Neither skill is renamed, no trigger phrase changes, and neither skill's one-paragraph blurb there restates the frontmatter contract in enough detail to be part of this defect.

## Users / Actors

| Actor | Role | Interaction |
|---|---|---|
| Maintainer (JP) | Reads reference docs when auditing or extending either skill | Benefits from one place to check the contract instead of four or five |
| Agent (Claude Code or Codex running either skill) | Loads reference files at runtime | Pays the token cost of every restatement it reads, and risks loading a stale copy when restatements disagree |

## Requirements

1. For every field `derive-log-facts.py` produces, its derivation method must be asserted in exactly one place. `frontmatter-schema.md` and `session-log-template.md` must stop independently restating "hostname," "git diff --name-only," "git describe," and similar derivation phrases that the script itself already encodes. [S1, S2, S3]
2. `frontmatter-schema.md`'s own worked example must not contradict its own Tier 1 table. Today it omits `type` and `machine`, both of which the same document's table two paragraphs above marks as always-include. [S2]
3. Any hardcoded field count (today "18-field," which undercounts the actual 23 fields across the three tier tables) must not appear anywhere in the skill's shipped documentation. A reader who wants the count should be pointed at the authoritative source, not handed a number to trust. This effort's own working documents are exempt from that check, since they name the stale string as the thing being removed; AC-3's verification is scoped accordingly. [S6]
4. `skills/plab-continue-session/SKILL.md`'s Phase 2 field list and `references/handoff-display.md`'s parallel description of what a log's frontmatter and sections contain must stop independently restating a shape that can drift from `frontmatter-schema.md`'s tables, as Phase 2 already has: it lists `status`, `session-type`, `model`, and `agent`, but omits the Tier 1 fields `type`, `machine`, and `files-changed`. [S4, S5, S2]
5. The claim that the two skills move and version together must be asserted in exactly one shipped file, keeping one of its two current wordings verbatim rather than a freshly invented third phrasing. Today it is asserted independently in `skills/plab-continue-session/HISTORY.md:69` ("move and version together") and, in different words, in root `README.md:17` ("versioned and released together"). [S7, S8]
6. `docs/skills/plab-wrap-session/README.md`'s per-section purpose descriptions, and `docs/skills/plab-continue-session/README.md`'s own restatement of the pairing relationship and field expectations, must defer to the single-source documents rather than independently re-describing them a second time. [S6, S10, S9]
7. This effort must not start before `derive-log-facts.py` exists and is wired into wrap's `SKILL.md`; there is nothing to defer to before that point. [S1, S11]

## Acceptance Criteria

**AC-1:** The string "hostname" as a derivation-method comment or table cell appears nowhere in `skills/plab-wrap-session/references/frontmatter-schema.md` or `skills/plab-wrap-session/references/session-log-template.md` after this effort ships; both instead point at `derive-log-facts.py` for how derived fields are produced. Verified by `grep -rn hostname skills/plab-wrap-session/references/` returning no matches. [S1, S2, S3]

**AC-2:** `frontmatter-schema.md`'s worked example includes every field its own Tier 1 table marks as always-include, or the hand-maintained example is removed in favor of a pointer to the script's real output so no hand-written example can drift from the table again. Verified by reading the Example Frontmatter block and confirming `type:` and `machine:` are present, or that the block no longer exists as independent prose. [S2]

**AC-3:** The literal string "18-field" appears nowhere in this skill's shipped documentation after this effort ships. Verified by `grep -rn "18-field" skills/ docs/skills/ README.md CHANGELOG.md` returning zero matches. The scope deliberately excludes `docs/internal/release-plans/`, where this spec and its plan name the stale string as the thing being removed; a repo-wide grep would make the check unsatisfiable forever once these documents exist. [S6]

**AC-4:** `skills/plab-continue-session/SKILL.md`'s Phase 2 no longer hand-enumerates a frontmatter field list that duplicates `frontmatter-schema.md`'s tables; it instead names the fields it reads by deferring to that reference. Verified by reading Phase 2 and confirming the phrase "Extract from frontmatter:" is no longer followed by an independently maintained field list. [S4, S2]

**AC-5:** The claim that `plab-wrap-session` and `plab-continue-session` move and version together is asserted in exactly one shipped file after this effort ships, using one of its two current wordings verbatim rather than a newly invented third phrasing. Verified by `grep -rlnE "version together|versioned and released together" skills/ docs/skills/ README.md CHANGELOG.md` returning exactly one file. The scope deliberately excludes `docs/internal/release-plans/`, where this spec and its plan name both current wordings; a repo-wide grep would also count this spec itself as a second match. [S7, S8]

**AC-6:** `docs/skills/plab-wrap-session/README.md`'s per-section purpose descriptions defer to `SKILL.md`'s Body Sections prose rather than independently re-describing each section's purpose a second time. Verified by reading the "Output Shape" table and confirming it references the source instead of carrying its own parallel prose for what each section contains. [S6, S9]

**AC-7:** This effort's implementation plan does not begin until `skills/plab-wrap-session/scripts/derive-log-facts.py` exists and `skills/plab-wrap-session/SKILL.md`'s Evidence Gathering section references it. Verified by confirming both conditions before Phase 1 of the implementation plan starts. [S1, S11]

## Behavior / Examples

### Example 1: The "hostname" consolidation

Before this effort (and after W-02, which already removes wrap's own copy): `grep -rn hostname skills/plab-wrap-session/` matches `references/frontmatter-schema.md:15` and `references/session-log-template.md:13`, `:106`, and `:140`, three per-mode blocks. After this effort, the same grep, scoped to `references/`, returns nothing; the only remaining matches for "hostname" anywhere under `skills/plab-wrap-session/` are inside `scripts/derive-log-facts.py` and its test file, where the word legitimately names the implementation rather than restating it a second time.

### Example 2: Continue's Phase 2, before and after

Before: "Extract from frontmatter: `date`, `repo`, `branch`, `summary`, `status`, `session-type`, `model`, `agent`," a hand-typed list that already omits `type`, `machine`, and `files-changed`, three Tier 1 fields. After: Phase 2 states that it reads Tier 1 and Tier 2 fields per the single named reference, with no independently maintained list left to drift a second time.

### Example 3: The dependency gate in practice

An agent picking up this effort's implementation plan first checks two things: does `skills/plab-wrap-session/scripts/derive-log-facts.py` exist, and does `SKILL.md`'s Evidence Gathering section reference it? If either answer is no, the agent stops and reports that W-02 has not shipped yet, rather than guessing at what the eventual contract will look like and consolidating documents around a guess.

## Non-Functional Requirements

| Category | Requirement | Source |
|---|---|---|
| Token cost | Fewer independently authored restatements means fewer tokens spent loading redundant reference content at skill-load time, across both skills. | [S1] |
| Maintainability / auditability | Every AC in this spec is verifiable by grep or direct reading, so a future agent or the maintainer can re-check the contract's single-source property without re-deriving it from scratch. | [S1] |
| Compatibility | Consolidating the contract must not change any field name or log shape mid-stream; a log written the day before this effort ships must still parse the same way the day after. | [S1] |

## Revisions

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Initial draft created | agent |

## Sources & Evidence

- [S1] `_local/skill-roadmaps/2026-08-18/pair-defects.md`, section "D-10. The structural cause under D-1, D-2, D-5, and D-8." Maintainer-local, gitignored, exists on disk. Credibility A (primary design source for this effort).
- [S2] `skills/plab-wrap-session/references/frontmatter-schema.md`. Repo file, credibility A, read in full.
- [S3] `skills/plab-wrap-session/references/session-log-template.md`. Repo file, credibility A, read in full.
- [S4] `skills/plab-continue-session/SKILL.md`. Repo file, credibility A, read in full.
- [S5] `skills/plab-continue-session/references/handoff-display.md`. Repo file, credibility A, read in full.
- [S6] `docs/skills/plab-wrap-session/README.md`. Repo file, credibility A, read in full.
- [S7] `skills/plab-continue-session/HISTORY.md`. Repo file, credibility A, read in full.
- [S8] `README.md` (repository root). Repo file, credibility A, read in full.
- [S9] `skills/plab-wrap-session/SKILL.md`. Repo file, credibility A, read in full. Cited here for the existing cross-skill-deferral precedent at line 104, and for the Body Sections prose at lines 132-165 that other documents restate.
- [S10] `docs/skills/plab-continue-session/README.md`. Repo file, credibility A, read in full.
- [S11] `docs/internal/release-plans/plan_v0.6.0/W-02_derived-log-facts/spec.md`. This session's own prior artifact, written before this document and verified by direct reading.
- [S12] `AGENTS.md`. Repo file, credibility A, read in full. Cited for the "personally useful, not maximal" design frame this spec applies when deciding to retain `frontmatter-schema.md` rather than delete it.

### Unverified Claims

None.

## Open Questions / Decisions

| ID | Item | Status |
|---|---|---|
| D1 | Whether `frontmatter-schema.md` is deleted outright or retained for agent-authored fields only | Decided, see below |
| D2 | The source's "both HISTORY files" framing for the pairing claim | Decided, correcting the source, see below |
| D3 | Whether to build a generator or regeneration pipeline for the consolidated contract | Decided, see below |
| D4 | The task briefing's instruction to record the W-02 dependency via a `spec-dependencies` field | Decided, flagging a conflict, see below |

**D1.** `frontmatter-schema.md` is retained, not deleted, because it still legitimately documents fields the script does not produce: `session-type`, `model`, `model-settings`, `agent`, `status`, `skills-used`, `resumed-from`, the Tier 3 fields, and the tiering rationale itself (why three tiers exist at all). What changes is narrower: the document stops independently asserting the derivation method for fields the script does produce, and its own worked example stops contradicting its own table. This is a smaller change than deleting the file and matches this repo's stated design frame that a personally-useful choice wins over a maximal one. [S2, S12]

**D2.** The task briefing that produced this spec, and `pair-defects.md`'s own D-10 section, both describe the versioned-together claim as appearing in "both HISTORY files." Direct verification found it in only one: `skills/plab-continue-session/HISTORY.md:69`. `skills/plab-wrap-session/HISTORY.md` does not contain this phrase or a close paraphrase anywhere; it was read in full to confirm this. The second live instance found is not a HISTORY file at all; it is root `README.md:17`. AC-5 targets what was actually found, two files, one of which is not a HISTORY file, rather than the two-HISTORY-files framing the source used. The underlying diagnosis, an unchecked claim duplicated across files with nothing checking it, still holds; only the specific file list changes. [S7, S8]

**D3.** The source is explicit that a shared schema should not be built as a separate artifact. This spec reads that as ruling out a generated or regenerated markdown file, which would still be a second artifact needing its own build step to stay in sync, and instead treats deletion of the duplicate prose, plus a pointer to the script itself, as the correct minimal-machinery resolution. No regeneration pipeline is proposed here. [S1]

**D4.** The task briefing said to record the W-02 dependency using "spec-dependencies." No such frontmatter field exists in the conventions' closed `spec.md` schema, which states plainly that frontmatter fields must not be invented and that the schema is closed; the same conventions document warns that deviating from the exact shape produces documents its release gate cannot parse. This spec resolves the conflict in favor of the more explicit, harder constraint: the dependency is recorded in prose instead, here in Purpose, in Requirement 7, and as AC-7's explicit gate, rather than as a new structured field. If a structured dependency field is wanted going forward, that is a change for the conventions document itself to make, not a call for an individual spec to make unilaterally. This is flagged in the final report for the maintainer's attention.
