# Backlog Entry Format

When `--close` is invoked with `--backlog <path>`, unresolved decisions (Status ∈ Open / Deferred / Needs info) are appended to `<path>` under a dated heading.

## Section header per close run

Under the file at `<path>`, each close operation appends:

```
## From AI Review - YYYY-MM-DD
```

All unresolved items from that review fall under this heading.

## Entry template

```markdown
### D1: [Title] - [Status]

**Source:** `_archive/<basename>_original_reviewed-by-<reviewer>.md` (reviewed YYYY-MM-DD)

**Context:** [Context paragraph from the decision section - copied verbatim]

**Options considered:**
- **A:** [one-line summary]
- **B:** [one-line summary]

**Reviewer recommendation:** [What the requestor LLM recommended]

**Maintainer notes:** [JP's Reasoning field from Maintainer Response; empty bullet if unfilled]
```

## Omissions

- `Options considered` is omitted when the decision had one option or was effectively yes/no. Empty ceremony is removed.
- `Maintainer notes` is kept with an empty bullet (`- `) when the Reasoning field is unfilled - signals "unresolved without commentary" rather than silently dropping the field.

## Backlog file bootstrap

If the file at `--backlog <path>` does not exist, `--close` creates it with this header before appending the first dated section:

```markdown
# Backlog

_Unresolved items appended from ai-review close operations._
```

Existing files are never overwritten - only appended to.

## Why this format

- **Self-contained.** Readers do not need to open the archived review to understand the item: title, source link, context, options, recommendation, and maintainer notes are all present.
- **Source-linked.** Every entry points to the archived `_reviewed-by-*` file and the review date. JP can drill into the full review when deeper context is needed.
- **Medium fidelity.** Options are one-line summaries, not full pros/cons. Full detail lives in the archive where it does not compete for attention in a growing backlog.
