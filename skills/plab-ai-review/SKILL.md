---
name: plab-ai-review
description: "Generate and synthesize structured AI peer reviews. Three modes: --review
  generates a self-contained review request for a second LLM (Codex, GPT, Gemini);
  --respond adds requestor synthesis after the reviewer completes findings (auto-detects
  pending clarifications on re-run); --close archives the source + review, applies
  accepted changes, and writes unresolved decisions to a user-specified backlog.
  Supports document types: plan, brief, spec/prd, rfc, or doc (generic). Triggers
  on 'review this with codex/gpt', 'ai-review', 'get a second opinion', 'peer review
  this', 'close this review'."
version: "1.2.1"
updated: 2026-07-04
argument-hint: "<doc.md> [--reviewer codex|gpt|gemini] [--respond]"
license: MIT
---

# AI Review

Generate structured, self-contained review requests for cross-LLM peer review. The reviewer LLM receives a document with everything needed to critique independently - context, targeted questions, severity framework, and response templates. After the reviewer completes findings, add requestor synthesis with inline responses, structured decisions, and proposed actions.

## Modes

### `--review` (Generate Review Request)

```
/plab-ai-review doc.md --reviewer codex
```

1. Read the source document fully
2. Auto-detect document type (or use `--type`): plan, brief, spec, rfc, doc
3. Select review dimensions from type preset (5-7 sections); confirm with user for `doc` type
4. Generate self-contained review document with:
   - Reviewer Assessment + Requestor Analysis placeholders
   - Structured Decisions placeholder
   - Anti-sycophancy reviewer instructions (see `references/attribution-guide.md`)
   - Source document (embed if < 200 lines, else summarize key claims + reference path)
   - Review sections - each with context line + reviewer/requestor attribution placeholders
   - Proposed Actions placeholder
5. Write to `<basename>_reviewed-by-<reviewer>.md` (same directory as source)
6. Tell user: paste into reviewer LLM, bring back findings, run `--respond`

### `--respond` (Requestor Synthesis)

```
/plab-ai-review doc_reviewed-by-codex.md --respond
```

1. Read the reviewed document with reviewer findings
2. Write **Reviewer Assessment** - summarize reviewer's overall findings, fill severity table
3. Write **Requestor Analysis** - agreement/disagreement, proposed action count
4. Write **inline responses** per section, scaled by severity:
   - Blocker/Major: full paragraph with evidence and proposed change
   - Minor/Note: one-liner ("Agree. [action]." or "Noted. Deferring.")
5. Write **Structured Decisions** - summary table + per-decision sections. **Every Blocker and every Major finding MUST generate a per-decision section.** Minor and Note findings may generate sections when the requestor judges they need human attention.
6. Write **Recommendations** - top 3 most impactful actions
7. Write **Proposed Actions** table - consolidated Update/Defer rows

### `--close` (Post-Review Lifecycle Automation)

```
/plab-ai-review doc_reviewed-by-<reviewer>.md --close [--backlog path/to/backlog.md]
```

Automates the post-review lifecycle documented in `references/file-lifecycle.md` Step 5:

1. Copy `doc.md` → `_archive/doc_original.md`. Creates `_archive/` if missing.
2. Apply changes from the reviewed-by document back into `doc.md`. **The Proposed Actions table is the source of truth** - every row where `Action = Update` gets applied. Pre-flight check: if any decision has `Status = Rejected` or `Deferred` while its triggered Proposed Actions row is still `Update`, the confirmation prompt flags the divergence (warn-not-block).
3. Move `doc_reviewed-by-<reviewer>.md` → `_archive/doc_original_reviewed-by-<reviewer>.md`.
4. Append unresolved items (Status ∈ Open / Deferred / Needs info) to the file at `--backlog` using `references/backlog-entry-format.md`. Accepted and Rejected decisions are closed - they stay in the archive and are not written to the backlog.

**Before any file operation, print this summary and require `y` confirmation:**

```
--close will:
  - Archive source:  doc.md → _archive/doc_original.md
  - Apply N accepted changes to doc.md
  - Archive review:  doc_reviewed-by-<reviewer>.md → _archive/doc_original_reviewed-by-<reviewer>.md
  - Append M unresolved items to path/to/backlog.md

Proceed? (y/n)
```

If the pre-flight check found rows flagged for decision/action divergence, list them under the "Apply N accepted changes" line so JP sees them before confirming.

**`--backlog <path>` flag:**

- Required when the review has at least one unresolved decision (Status ∈ Open / Deferred / Needs info). Missing flag → skill errors out before any file operation.
- Optional when there are zero unresolved items; silently ignored if provided anyway.
- If `<path>` does not exist, `--close` creates it with a standard header (see `references/backlog-entry-format.md`).
- Existing files are appended to under a new dated heading - never overwritten.

**Edge cases:**

- **Existing `_archive/doc_original.md`:** skill errors out; names the existing archive path in the error; no file operation. JP resolves manually.
- **Missing Proposed Actions table in the reviewed-by doc:** Step 2 applies no changes and surfaces a warning in the confirmation prompt.

### Auto-detect

`/plab-ai-review doc_reviewed-by-codex.md` (no flag) - detect reviewer findings present, confirm with user: "This review has findings. Want me to add my response?" Proceed as `--respond`.

On a reviewed-by file where initial synthesis is already filled in, `--respond` auto-detects pending clarifications: scans for `**Maintainer Clarification Request**` sub-blocks containing content but no filled `**Requestor Response - **` below. If any are found, prompts: *"Found N pending clarification(s). Address them?"* On confirm, fills only those sub-blocks; does not modify resolved decisions or the initial synthesis.

## Phase Model

| Phase | Actor | What happens |
|-------|-------|--------------|
| **P2** | `--review` | Generates the template with placeholders. |
| **P3** | Reviewer LLM (Codex/GPT/etc.) | Fills findings per section. JP pastes reviewer output back into the file. |
| **P4** | `--respond` first pass | Writes Reviewer Assessment, Requestor Analysis, inline responses, per-decision sections (Part 1 populated, Parts 2/3 left as placeholders), summary table with `Status = Open`, Proposed Actions table. |
| **P5** | JP (manual) | Fills Maintainer Response per decision (Status / Reasoning / free-form notes); optionally writes Clarification questions; updates Final Decision and Last Updated columns. |
| **P6** | `--respond` second pass | Answers pending clarifications only. Leaves resolved decisions and initial synthesis untouched. |

P1 is intentionally unused (historical gap from an earlier draft); do not renumber the others.

## Document Types

Types are optional - the skill auto-detects and proposes dimensions. Use `--type` to skip the proposal step.

| Type | Focus | Sections |
|------|-------|----------|
| **plan** | Executability - can this be built as written? | 7 |
| **brief** | Decision quality - is the thinking rigorous? | 7 |
| **spec** | Completeness - is this testable and unambiguous? | 6 |
| **rfc** | Technical soundness - is the proposal correct? | 7 |
| **doc** | Generic - LLM proposes 5-7 custom dimensions | varies |

`spec` and `prd` are synonyms. See `references/section-presets.md` for default dimensions per type.

## LLM Identifiers

`claude` | `codex` | `gpt` | `gemini` | `grok` | `mistral` | `local-<model>`

## Output

Use the template in `references/review-template.md`. File naming and archive workflow per `references/file-lifecycle.md`.

- **`--review`**: Write `<basename>_reviewed-by-<reviewer>.md` in same directory as source
- **`--respond`**: Update existing `_reviewed-by-` file in place (fill placeholders)
- **`--close`**: Archive source + reviewed-by to `_archive/`, apply accepted changes to source, append unresolved items to `--backlog` file (see edge cases in `--close` section)

## Constraints

- **Every Blocker finding and every Major finding MUST generate a corresponding per-decision section.** Requestor LLM retains judgment for Minor and Note findings. Silent drops of Blocker/Major findings are a skill violation.
- Review document must be **self-contained** - reviewer needs nothing beyond this document
- Every review section must have a **specific question**, not "what do you think?"
- Every finding must **cite specific evidence** (sections, quotes, file paths)
- Do **not** call the reviewer LLM - user handles the handoff
- All LLM content **attributed** with role + LLM name + date (see `references/attribution-guide.md`)
- Reviewer Assessment and Requestor Analysis are **separate** top-level sections
- Proposed Actions is a **single table** at the bottom - no per-section update lines
- Response depth **scales with severity** - Blockers get paragraphs, Notes get one-liners
- Review should be **shorter than the source** - focused, not exhaustive
