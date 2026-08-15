# File Lifecycle & Naming Conventions

The review document is named `_reviewed-by-<reviewer>` from creation. This name describes the document's purpose and persists through all phases - no renames during the workflow.

---

## File Naming

| Phase | File | Actor | Content |
|-------|------|-------|---------|
| Source | `doc.md` | Requestor LLM | Original document |
| Review request | `doc_reviewed-by-codex.md` | Requestor LLM (--review) | Template with placeholders |
| Reviewer fills in | `doc_reviewed-by-codex.md` | Reviewer LLM | Findings added per section |
| Requestor synthesis | `doc_reviewed-by-codex.md` | Requestor LLM (--respond) | Assessment, analysis, decisions, actions added |
| Archive original | `_archive/doc_original.md` | User | Snapshot of source before updates |
| Source updated | `doc.md` | Requestor LLM | Approved changes applied |
| Archive review | `_archive/doc_original_reviewed-by-codex.md` | User | Completed review moved to archive |

## LLM Identifiers in Filenames

Use lowercase: `codex`, `gpt`, `gemini`, `claude`, `grok`, `mistral`, `local-<model>`

---

## Archive Convention

The `_archive/` directory sits alongside the source document:

```
project/
├── doc.md                              # Updated source
└── _archive/
    ├── doc_original.md                 # Pre-update snapshot
    └── doc_original_reviewed-by-codex.md  # Completed review artifact
```

Naming:
- `_archive/<basename>_original.md` - snapshot of source before updates
- `_archive/<basename>_original_reviewed-by-<reviewer>.md` - completed review artifact

---

## Workflow (User Perspective)

```
1. /plab-ai-review doc.md --reviewer codex
   → Creates doc_reviewed-by-codex.md

2. Copy doc_reviewed-by-codex.md contents into Codex / target LLM
   → Reviewer fills in findings per section
   → Paste reviewer output back into doc_reviewed-by-codex.md

3. /plab-ai-review doc_reviewed-by-codex.md --respond
   → Adds: Reviewer Assessment, Requestor Analysis, inline responses,
     structured decisions, recommendations, proposed actions

4. Review the completed document
   → Resolve open decisions (update Status in summary table)
   → Approve or modify Proposed Actions table

5. Archive and update - **automated by `--close` (see `SKILL.md`); the steps below are the manual equivalent:**
   a. Copy doc.md → _archive/doc_original.md
   b. Ask requestor LLM to apply approved updates to doc.md
   c. Move doc_reviewed-by-codex.md → _archive/doc_original_reviewed-by-codex.md
```
