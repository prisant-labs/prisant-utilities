# Decisions / Open Questions Section Standard

Canonical definition of the **decisions section**: the one structural pattern any `prisant-utilities` document uses for a section that captures open questions or decisions (strategy briefs, peer-review documents, and other documents that surface unresolved choices).

This reference is the single source of truth. Skills and docs cite this file rather than redefining the pattern. The pattern originates in `plab-ai-review`'s review template, the most evolved exemplar in this plugin.

## When to use it

Use it in any document that has to record a question awaiting a maintainer decision, or a decision the maintainer has made, with the analysis that led to it. The section heading in the host document is:

```markdown
## Open Questions / Decisions
```

If there are no open items, write "None at this time." under the heading.

## Structure

Three required parts, in this order:

1. **A summary table** - one row per item, status and outcome at a glance.
2. **A subsection per item** - structured fields covering the question and the agent's analysis. The subsection header carries the item's status.
3. **A visually separated maintainer decision block** - the human's response, unambiguous and unmistakable.

### Part A: Summary table

```markdown
## Open Questions / Decisions

| ID | Title | Resolution | Status | Updated |
|----|-------|------------|--------|---------|
| D1 | <short handle for the question> | (none) | Open | (none) |
| D2 | <short handle> | <short outcome, e.g. "Option B"> | Decided | 2026-06-16 |
| D3 | <short handle> | <when / why> | Deferred | 2026-06-10 |
```

**Columns.**

| Column | Contents |
|--------|----------|
| `ID` | Stable item id, `D` prefix by default (`D1`, `D2`, ...). Keyed to the subsection below and cited from commits, other docs, and the maintainer block. Always paired with the Title so the id is never bare. |
| `Title` | One-line human-readable handle for the question. |
| `Resolution` | Short outcome once decided (the chosen option, or when/why deferred). `(none)` while open. |
| `Status` | One of the status vocabulary below. |
| `Updated` | ISO `YYYY-MM-DD` of the last status change. `(none)` while never touched. |

**Status vocabulary.**

| Status | Meaning |
|--------|---------|
| `Open` | Awaiting maintainer decision. Default for a newly added item. |
| `Decided` | Maintainer has chosen. Outcome and reasoning recorded in the maintainer block. |
| `Deferred` | Intentionally postponed. The decision is to not decide yet; note when to revisit. |
| `Needs info` | Blocked on clarification. Usually triggers a re-run of the producing skill. |
| `Withdrawn` | No longer relevant. Keep the row for traceability; do not delete history. |

### Part B: Per-item subsection

The subsection header restates the id and title and **carries the status in a trailing parenthetical** so the reader sees it in the body without scrolling back to the table.

```markdown
### D1: <Title> (Open)

**Summary.** One-line restatement of the question.

**Context.** Why this is open, the background facts, why it matters. 2-4 sentences,
no more than a short paragraph.

**Desired outcome.** What good looks like, independent of which option wins. One or
two sentences. The criteria the chosen option must satisfy.

**Options / approaches.**

* **Option A:** <description, including the most important trade-off>
* **Option B:** <description, including the most important trade-off>
* **Option C:** <description, including the most important trade-off>

**Recommendation.** <The agent's pick plus a 1 to 3 sentence rationale. The agent
always recommends; never "it depends".>
```

Two options is the minimum, three is common, four is the upper bound. If there are more, group them into families first.

### Part C: Visually separated maintainer decision block

A `>` blockquote preceded by a `---` horizontal rule. Together they create a strong visual break that is unambiguous on GitHub. This block is the **authoritative record** of the answer; the table and the subheader status mirror it.

```markdown
---

> **Maintainer decision:** _(pending)_
>
> * **Status:** Open
> * **Choice:** (none)
> * **Reasoning:** (none)
> * **Decided by / date:** (none)
```

When the maintainer decides, the block fills:

```markdown
---

> **Maintainer decision:** Decided 2026-06-16 by jp
>
> * **Status:** Decided
> * **Choice:** Option B with the addition from Option C
> * **Reasoning:** B preserves the round-trip integrity; C's auto-detection
>   resolves the staleness concern without adding a manual step.
> * **Decided by / date:** jp / 2026-06-16
```

Optionally, a clarification request can follow the decision block when the maintainer is blocked on a question for the agent:

```markdown
---

> **Maintainer clarification request:** _(if blocked)_
>
> jp's question here.

**Agent response** (claude, 2026-06-16):

> Agent's answer here.
```

## Lifecycle

* When an item's status changes, update **three surfaces in sync**: the summary-table row (`Resolution`, `Status`, `Updated`), the subsection header's trailing `(status)`, and the maintainer block. The maintainer block is the source of truth; the other two mirror it.
* Do **not** rewrite the per-item body (Summary, Context, Desired outcome, Options, Recommendation) when a status flips. The analysis stays as the historical record of what was on the table.
* When a decision becomes architectural (alternatives considered, hard to reverse, looks wrong without context), copy or move the resolved item to a MADR v4 ADR in `docs/internal/decisions/` and reference the ADR from the source document.
