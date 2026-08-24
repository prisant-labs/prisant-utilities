# Acceptance Criteria Format

The AC are the spec's load-bearing column. If they're weak, the spec is useless. These rules are constraints - pressure tests do not relax them.

## The Rules

### 1. Numbered as AC-N

```
AC-1: <outcome>
AC-2: <outcome>
```

Stable IDs. AC-3 is always AC-3, even after revisions. Superseded ACs keep their number with a strikethrough or `(superseded)` marker.

### 2. One observable outcome per AC

If the AC contains "and" between two observable outcomes, split it.

**Bad:**
```
AC-1: Skill produces frontmatter and validates required fields and rejects invalid input.
```

**Good:**
```
AC-1: Skill produces frontmatter with all required fields.
AC-2: Skill validates required fields against the schema.
AC-3: Skill rejects input missing required fields with a specific error message.
```

### 3. Testable phrasing

Future agents (or reviewers) must be able to verify the AC. Vague language fails this test.

**Bad:**
- "Skill produces high-quality output"
- "User experience is good"
- "Performance is acceptable"

**Good:**
- "Skill produces output passing `bash scripts/lint-skills-frontmatter.sh`"
- "Skill response within 200ms for inputs under 10kb (measured at p95)"
- "Skill rejects malformed input with non-zero exit code and an error on stderr"

If you can't articulate how it would be verified, the AC isn't ready.

### 4. Cited

Every AC has a citation: an inline `[Sn]` referencing Sources & Evidence, or a `[model-inference]` marker.

```
AC-1: Spec produces frontmatter with all required fields. [S1]
AC-2: Spec rejects input missing required fields. [S1, S3]
AC-3: Spec includes a Task Summary block at top. [model-inference]
```

If you can't cite, mark `[model-inference]` and set `requires-human-review: true` in frontmatter. Don't fabricate a source.

### 5. Optional Given/When/Then for behavior-heavy AC

For AC where preconditions and triggers matter, expand into G/W/T:

```
AC-2: Spec rejects input missing required fields. [S1]
  Given: a spec input with no `id` field
  When: plab-spec runs in dry-run mode
  Then: the skill prints "ERROR: id is required" and exits non-zero before writing any file
```

Keep G/W/T short. If it's longer than the AC statement, the AC is too vague.

### 6. Numbered fulfillment, not narrative

The Task Summary block has a checkbox per AC. AC text appears once (here, in this section), then is restated one-line in the Task Summary block. Don't repeat AC details in Behavior, NFR, or elsewhere.

## What Counts as an AC vs What Doesn't

| Type | Example | Where it lives |
|------|---------|----------------|
| **AC** | "Skill produces frontmatter with required fields" | This section |
| **NFR** | "Skill response time under 200ms" | Non-Functional Requirements |
| **Behavior detail** | "When the user provides --dry-run, the skill prints the would-write report" | Behavior / Examples |
| **Implementation step** | "Use yaml.safe_load to parse frontmatter" | The plan, NOT the spec |
| **Test case** | "test_required_fields_present()" | Test code, NOT the spec |

If you're tempted to write an implementation step or test case as an AC, stop. Those belong in the plan or test suite.

## Common AC Smells

- **Multi-clause AC** ("and", "or", commas listing distinct outcomes) → split
- **Aspirational AC** ("should ideally", "tries to", "aims for") → reword as binary
- **Subjective AC** ("intuitive", "elegant", "reasonable") → restate as observable
- **Implementation AC** ("uses YAML library", "stores in PostgreSQL") → move to plan
- **Untestable AC** ("works correctly", "handles edge cases") → name the actual edge cases as AC-N+1, AC-N+2
- **Source-less AC** with no `[S]` or `[model-inference]` → not allowed; cite or mark

## Counting

`ac-count` in frontmatter equals the number of `AC-N:` entries. Including superseded ones (they still take a number; just marked).

## Revising AC

Never silently rewrite a committed AC. Rules:

1. Mark the original AC with `(superseded YYYY-MM-DD)`:
   ```
   AC-3: ~~<original text>~~ (superseded 2026-04-20 - see AC-8)
   ```
2. Add a new AC at the end with a fresh number (do not reuse AC-3 for new content).
3. Append to the Revisions table:
   | YYYY-MM-DD | <author> | superseded | AC-3 superseded by AC-8: <reason> |

Stable IDs let plans, tests, and PRs reference the same AC across revisions.

## Examples of Good AC

```
AC-1: Skill produces frontmatter with `id`, `title`, `type`, `status`, `created`, `updated`, `linked-effort`, `ac-count`. [S1]

AC-2: Skill includes Task Summary block as the first section after the H1 title. [S1, S2]

AC-3: When user input lacks `--effort`, skill prompts for it instead of inventing an id. [S1]

AC-4: Skill rejects re-runs that would overwrite an existing spec, unless `--revise` is passed. [S2]

AC-5: Every requirement and AC in the output carries an inline citation or `[model-inference]` marker. [S1, S3]
  Given: a spec input where one requirement has no source
  When: plab-spec writes the output
  Then: the requirement appears with `[model-inference]` and frontmatter `requires-human-review` is set to true

AC-6: Output passes the validation checks in Phase 6 of the skill workflow. [S1]
```

If your draft AC don't read like these, revise before committing.
