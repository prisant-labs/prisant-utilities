# plab-ai-review

**Version:** 1.2.1
**Source:** [`skills/plab-ai-review/`](../../../skills/plab-ai-review/)

Generate and synthesize structured AI peer reviews. Create a self-contained review request for a second LLM, add requestor synthesis once the reviewer files findings, then close the review: archive the pair, apply the accepted changes, and send unresolved decisions to a backlog.

---

## Getting Started

### Quick Start

```
/plab-ai-review path/to/document.md --reviewer codex
```

This generates a structured review request at `path/to/document_reviewed-by-codex.md`. The document includes everything the reviewer LLM needs - context, targeted questions, severity framework, and response templates.

### Full Workflow

```
1. /plab-ai-review doc.md --reviewer codex        # Generate review request
2. Copy contents into Codex                   # Reviewer fills in findings
3. Paste reviewer output back into file       # Replace placeholders
4. /plab-ai-review doc_reviewed-by-codex.md --respond  # Add synthesis
5. Review decisions and proposed actions       # Human resolves
```

### Installation

Install via the prisant-labs marketplace:

```bash
/plugin marketplace add prisant-labs/agent-plugins
/plugin install prisant-utilities@agent-plugins
```

Or symlink into a project:

```bash
ln -s /path/to/prisant-utilities/skills/plab-ai-review .claude/skills/plab-ai-review
```

---

## When to Use

- You want a second LLM to independently critique a plan, spec, brief, or design doc
- You say "review this with codex/gpt", "get a second opinion", "peer review this"
- You have a high-stakes document where rubber-stamping is worse than no review
- The document has enough substance to review (>500 words, real decisions)

## When NOT to Use

- Trivial documents (< 500 words, low-stakes, no decisions)
- Code review (use git-based review tools)
- Documents you want validated, not challenged (plab-ai-review is adversarial by design)
- When you need the review done automatically (the user handles the LLM handoff)

---

## Three Modes

### `--review` (Generate Review Request)

Reads the source document, auto-detects the document type, selects 5-7 review dimensions, and generates a self-contained review request.

**Input:**
- Document path (required)
- `--reviewer <name>` - target reviewer LLM (required): `codex`, `gpt`, `gemini`, `claude`, `grok`, `mistral`, `local-<model>`
- `--type <type>` - optional override: `plan`, `brief`, `spec`, `rfc`, `doc`

**Output:** `<basename>_reviewed-by-<reviewer>.md` in the same directory as the source.

### `--respond` (Requestor Synthesis)

Reads the reviewed document (with reviewer findings filled in), then adds:
- Reviewer Assessment summary with severity counts
- Requestor Analysis with agreement/disagreement
- Inline responses per section (depth scales with severity)
- Structured Decisions for items needing human judgment
- Top 3 Recommendations
- Proposed Actions table

**Input:** The `_reviewed-by-` file with reviewer findings filled in.

**Output:** Updates the same file in place.

### `--close` (Post-Review Lifecycle)

```
/plab-ai-review doc_reviewed-by-codex.md --close --backlog path/to/backlog.md
```

Runs the archive workflow for you once the decisions are settled:

- Snapshots the source to `_archive/doc_original.md`, creating `_archive/` if it is missing.
- Applies every Proposed Actions row marked `Update` back into the source. That table is the source of truth. If a decision reads Rejected or Deferred while its action row still says `Update`, the divergence is flagged in the confirmation prompt rather than blocking the run.
- Moves the `_reviewed-by-` file into `_archive/`.
- Appends unresolved decisions (Open, Deferred, Needs info) to the `--backlog` file under a dated heading. Accepted and Rejected items are closed; they stay in the archive and never reach the backlog.

Nothing is touched until it prints all four steps and you answer `y`.

**`--backlog <path>`** is required when the review has at least one unresolved decision, and ignored when it has none. A missing file is created with a standard header; an existing one is appended to under a new dated heading, never overwritten.

**It stops rather than guesses.** An existing `_archive/doc_original.md` is an error, not an overwrite: the skill names the path it found and leaves every file alone.

**Input:** The `_reviewed-by-` file with decisions resolved.

**Output:** Updated source, two files in `_archive/`, and appended backlog entries.

### Auto-detect

Running `/plab-ai-review doc_reviewed-by-codex.md` (no flag) detects reviewer findings and asks: "This review has findings. Want me to add my response?"

---

## Document Types

| Type | Focus | Default Sections |
|------|-------|-----------------|
| **plan** | Executability - can this be built as written? | 7 (traceability, completeness, dependencies, decisions, file inventory, success criteria, scope risks) |
| **brief** | Decision quality - is the thinking rigorous? | 7 (framing, evidence, viability, recommendations, stakeholders, risks, assumptions) |
| **spec** | Completeness - is this testable and unambiguous? | 6 (requirements, acceptance criteria, scope, dependencies, priorities, user stories) |
| **rfc** | Technical soundness - is the proposal correct? | 7 (problem, architecture, trade-offs, edge cases, integration, migration, open questions) |
| **doc** | Generic - LLM proposes custom dimensions | varies (5-7, confirmed with user) |

`spec` and `prd` are synonyms. See `references/section-presets.md` for the full preset definitions.

---

## Output Shape

The skill produces a single cross-LLM review document named `<basename>_reviewed-by-<reviewer>.md`, built up in phases: `--review` generates the structure with placeholders, the reviewer LLM fills findings, `--respond` adds synthesis, and `--close` archives the source plus review and applies accepted changes. The document includes (in order):

| Section / Element | Purpose |
|-------------------|---------|
| Metadata header | Document path, type, date, and the three actors (Requestor LLM, Reviewer LLM, Human) |
| `## Reviewer Assessment` | Reviewer's independent 2-3 sentence headline plus a severity-count table (Blocker / Major / Minor / Note) |
| `## Requestor Analysis & Proposed Actions` | Requestor's agreement/disagreement summary, top-3 `### Recommendations`, and the `### Decisions for JP` summary table |
| Per-decision sections (`#### D1`, `D2`, ...) | One per decision: context, proposed options, recommendation, a visually-separated `**Maintainer Response**` block (Status / Reasoning), and an optional `**Maintainer Clarification Request**` with the requestor's reply. Every Blocker and Major finding generates one |
| `## Instructions for Reviewer` | Anti-sycophancy guidance, source-document table, finding format, severity definitions |
| `## Document Under Review` | Source embedded (if under 200 lines) or summarized with key claims plus a path reference |
| `## Findings` | 5-7 review dimensions; each carries a reviewer finding then a severity-scaled requestor response |
| `## Proposed Actions` | Single consolidated table of Update / Defer rows, with target and triggering finding |

Canonical structure with phase annotations lives in [`references/review-template.md`](../../../skills/plab-ai-review/references/review-template.md).

---

## Examples

### Example 1: Review an Implementation Plan

```
/plab-ai-review docs/plans/checkout-rewrite.md --reviewer codex
```

The skill:
1. Reads the plan, detects type `plan`
2. Selects 7 review dimensions (Plan Traceability, Work Item Completeness, etc.)
3. Generates `plan_v1_init-project_reviewed-by-codex.md` with:
   - Reviewer instructions including anti-sycophancy guidance
   - The plan embedded (or summarized if >200 lines)
   - 7 review sections with targeted questions
   - Attribution placeholders for both reviewer and requestor

### Example 2: Get a Second Opinion on a Strategy Brief

```
/plab-ai-review docs/strategy_tooling-migration.md --reviewer gpt --type brief
```

Generates a review targeting the 7 brief dimensions (Problem Framing, Evidence Quality, Approach Viability, etc.).

### Example 3: Synthesize After Review

After Codex fills in findings:

```
/plab-ai-review plan_v1_init-project_reviewed-by-codex.md --respond
```

The skill reads Codex's findings and adds:
- Severity summary (e.g., 1 Blocker, 2 Major, 3 Minor, 1 Note)
- Inline responses: paragraphs for Blockers, one-liners for Notes
- 2 structured Decisions (where requestor and reviewer disagree)
- Proposed Actions table with 5 Update rows and 2 Defer rows

---

## Review Document Structure

The generated document follows this layout:

```
# AI Review: [Title]
  Header (document, type, date, actors)

## Reviewer Assessment           ← reviewer's independent summary
## Requestor Analysis            ← requestor's response + recommendations + decisions

## Instructions for Reviewer     ← anti-sycophancy, finding format, severity defs
## Document Under Review         ← embedded or summarized source

## Findings
  ### [Dimension 1]              ← reviewer findings, then requestor response
  ### [Dimension 2]
  ...

## Proposed Actions              ← consolidated Update/Defer table
```

Full template: `references/review-template.md`

---

## Reference Files

| File | Purpose | When to Read |
|------|---------|-------------|
| `references/review-template.md` | Canonical document template with phase annotations | When customizing the review format |
| `references/section-presets.md` | Default review dimensions per document type | When overriding or understanding type presets |
| `references/attribution-guide.md` | Finding format, severity definitions, anti-sycophancy, structured decisions | When the attribution or finding format needs clarification |
| `references/file-lifecycle.md` | File naming, archive workflow, user-facing steps | When managing review artifacts |
| `references/backlog-entry-format.md` | Shape of the entries `--close` appends to a backlog file | When reading or reformatting backlog output |

---

## Key Concepts

**Self-contained reviews.** The reviewer LLM receives everything it needs in one document - no conversation context, no back-and-forth. This is what makes cross-LLM review possible.

**Anti-sycophancy.** Every review document includes explicit instructions: "Your role is to find problems, not to validate. If you find nothing wrong, that's suspicious."

**Severity-scaled responses.** Requestor responses match the severity of findings. Blockers get full paragraphs with evidence and proposed changes. Notes get one-liners. This prevents over-responding to minor issues and under-responding to critical ones.

**Three actors.** Reviewer finds problems. Requestor analyzes and proposes actions. Human decides. No single actor does everything - this prevents both rubber-stamping and analysis paralysis.

**Role-labeled attribution.** Every LLM contribution is tagged with role, name, and date (`**Reviewer - Codex (2026-04-08):**`). No ambiguity about who wrote what.

---

## Archive Workflow

This is what `--close` automates. The steps are documented because you can also run them by hand, and because
knowing them makes the confirmation prompt readable. After resolving decisions and applying updates:

```
1. Copy doc.md -> _archive/doc_original.md           # Snapshot before updates
2. Apply approved updates to doc.md                    # Requestor applies changes
3. Move reviewed-by file -> _archive/doc_original_reviewed-by-codex.md
```

The `_archive/` directory sits alongside the source document.

---

## Improvement Ideas

- **Custom section override via CLI** - let users specify review dimensions instead of using presets
- **Multi-reviewer protocol** - 2-3 independent reviewers on the same document, then cross-comparison
- **Review quality tracking** - which findings get accepted vs. rejected over time, per reviewer LLM
- **LLM pairing recommendations** - empirical data on which LLM pairs produce the best reviews
- **Automated citation verification** - script that checks whether cited sections/quotes actually exist in the source

---

## Constraints

- Review document must be self-contained
- Every finding must cite specific evidence
- Does not call the reviewer LLM (user handles the handoff)
- All LLM content attributed with role + name + date
- Reviewer Assessment and Requestor Analysis are separate sections
- Response depth scales with severity
- Review should be shorter than the source
