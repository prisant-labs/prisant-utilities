---
name: plab-release-plan
description: "Manage a version-scoped release plan. Creates the release folder with the plan
  document inside; promotes per-effort folders (spec + implementation plan + supporting) from
  _unassigned/ into the release; auto-generates an aggregation table from the folder contents;
  enforces hygiene gates and a doc-update checklist that gates the tag. Use when scoping a release,
  moving efforts in or out of one, or checking whether a version can be tagged yet. Explicit
  invocation only: run /plab-release-plan with one of five subcommands - --create, --promote,
  --demote, --update, --gate; it does not fire on its own. Refuses to invent or modify acceptance
  criteria - AC live in specs written by /plab-spec; the release plan only aggregates."
argument-hint: "--create vX.Y.Z [--theme <text>] | --promote --from _unassigned --to vX.Y.Z S-NN ... | --demote --from vX.Y.Z [--to _unassigned] S-NN | --update vX.Y.Z | --gate vX.Y.Z"
disable-model-invocation: true
license: MIT
metadata:
  version: "1.3.0"
  updated: 2026-08-24
---

# Release Plan

Aggregate every spec and implementation plan in scope of a release into one self-contained folder. Own the `_unassigned/` -> `plan_vX.Y.Z/` promotion ceremony. Gate the tag on hygiene checks + doc-update checklist.

## Subcommand Selection

| Subcommand | When to use |
|-----------|------------|
| `--create vX.Y.Z` | Start a new release plan. Creates the folder, writes the plan document with empty aggregation, scaffolds doc-update checklist + hygiene gates section. |
| `--promote --from _unassigned --to vX.Y.Z S-07 S-09 ...` | Move named per-effort folders into the release. Updates spec frontmatter on each. Refreshes aggregation. |
| `--demote --from vX.Y.Z [--to _unassigned] S-NN` | Reverse of promote. Moves the effort folder back. Clears spec `target-release` / `linked-release`. Default `--to` is `_unassigned`. |
| `--update vX.Y.Z` | Refresh the aggregation table and dynamic frontmatter fields after promotions or spec/plan status changes. Leaves authored sections (theme, decisions, checklist state) untouched. |
| `--gate vX.Y.Z` | Read-only readiness report. Walks hygiene gates and checklist; reports current pass/fail. Does not modify anything. |

## When NOT to Use This Skill

- You're writing the spec or plan itself (use `/plab-spec` or `/superpowers:writing-plans`)
- You're tagging or pushing (the skill blesses readiness; tagging is a manual human action)
- You're trying to add an AC (refuse; redirect to `/plab-spec --revise`)
- You're modifying CHANGELOG / README / HISTORY content (the skill only manages the *checklist* of what to update, not the content)
- You're auto-promoting based on heuristics (no; explicit human choice required)

## Input Contract (per subcommand)

### `--create vX.Y.Z`

| Input | Required | Notes |
|-------|----------|-------|
| `vX.Y.Z` | Yes | Semver release version. The folder `plan_vX.Y.Z/` is created at `docs/internal/release-plans/`; the plan document at `plan_vX.Y.Z/plan_vX.Y.Z.md` |
| `--theme <text>` | No | One-line release theme for the plan document header |
| `--target-date <YYYY-MM-DD>` | No | Optional target ship date for frontmatter |

### `--promote --from _unassigned --to vX.Y.Z S-NN ...`

| Input | Required | Notes |
|-------|----------|-------|
| `--from _unassigned` | Yes (v1) | Source. v1 only supports `_unassigned`; cross-release promote out of scope |
| `--to vX.Y.Z` | Yes | Target release. Must exist (run `--create` first) |
| Effort IDs | Yes | One or more `S-NN`. Each must exist as a folder in `_unassigned/<id>_<slug>/` |

### `--demote --from vX.Y.Z [--to _unassigned] S-NN`

| Input | Required | Notes |
|-------|----------|-------|
| `--from vX.Y.Z` | Yes | Source release |
| `--to _unassigned` | No (defaults to `_unassigned`) | v1 supports only `_unassigned`; direct release-to-release demote out of scope |
| Effort IDs | Yes | One or more `S-NN` currently in the named release |

### `--update vX.Y.Z` and `--gate vX.Y.Z`

| Input | Required | Notes |
|-------|----------|-------|
| `vX.Y.Z` | Yes | Release to refresh or check |

## Output

Per subcommand:

| Subcommand | Writes | Reads |
|-----------|--------|-------|
| `--create` | `plan_vX.Y.Z/` folder + `plan_vX.Y.Z.md` | release-checklist.yaml (if present, for checklist extension) |
| `--promote` | Moves effort folders; updates spec frontmatter; refreshes plan's aggregation + dynamic fields | Each effort's `spec.md` (for frontmatter update) |
| `--demote` | Moves effort folders back; clears spec frontmatter fields; refreshes plan | Same |
| `--update` | Aggregation table + dynamic frontmatter (`spec-count`, `plan-count`, `checklist-complete`) | Every effort folder in the release |
| `--gate` | Nothing (read-only) | Plan, every effort's spec + plan, checklist |

## Workflow

### `--create vX.Y.Z`

1. Verify `plan_vX.Y.Z/plan_vX.Y.Z.md` does not already exist. If it does, refuse without `--update`.
2. Create `docs/internal/release-plans/plan_vX.Y.Z/` if missing.
3. Write `plan_vX.Y.Z.md` inside it (template at `references/plan-template.md`):
   - Frontmatter per `references/frontmatter-schema.md`
   - Release theme line (from `--theme` or `"<release version> release"`)
   - Empty aggregation table (no efforts yet)
   - Hygiene gates section with default gates listed (all marked N/A while folder is empty)
   - Doc-update checklist with built-in defaults + any items from `docs/internal/release-plans/release-checklist.yaml` `add:` list (see `references/checklist-extension.md`)
4. Report: created path, checklist item count, "next: run `--promote`".

### `--promote --from _unassigned --to vX.Y.Z S-NN ...`

1. Verify each effort id resolves to a folder in `_unassigned/`. Refuse if any are missing.
2. Verify `plan_vX.Y.Z/` exists. Refuse if not (instruct to run `--create` first).
3. For each effort:
   - Move `release-plans/_unassigned/<id>_<slug>/` -> `release-plans/plan_vX.Y.Z/<id>_<slug>/` (whole folder, atomic per `references/promote-demote.md`)
   - Read the moved `spec.md` frontmatter; set `target-release: vX.Y.Z` and `linked-release: docs/internal/release-plans/plan_vX.Y.Z/plan_vX.Y.Z.md`
   - If the folder contains `implementation-plan.md`, update its `linked-release` field to match
4. Run `--update vX.Y.Z` to refresh the aggregation table and dynamic frontmatter fields.
5. Report: per-effort moves, frontmatter updates, current aggregation state.

Per D1 (spec section 9): promote ALLOWS specs with `status: draft`; the hygiene gate (AC-5(a)) catches drafts before tag rather than blocking at promote.

### `--demote --from vX.Y.Z [--to _unassigned] S-NN`

1. Verify each effort id resolves to a folder in `plan_vX.Y.Z/`. Refuse if missing.
2. For each effort:
   - Move `release-plans/plan_vX.Y.Z/<id>_<slug>/` -> `release-plans/_unassigned/<id>_<slug>/`
   - Clear the spec's `target-release` (set to null) and `linked-release` (set to null)
   - If `implementation-plan.md` exists, clear its `linked-release` too
3. Run `--update vX.Y.Z` to refresh the (now-shrunk) aggregation.
4. Report: per-effort moves, frontmatter clears, current aggregation.

Per D2: `--to` defaults to `_unassigned` when omitted. Direct release-to-release demote and `_shelved/` target are out of scope for v1.

### `--update vX.Y.Z`

1. Read `plan_vX.Y.Z/plan_vX.Y.Z.md`.
2. Walk `plan_vX.Y.Z/` for per-effort subfolders matching `<id>_<slug>/`. For each: read `spec.md` frontmatter (status, ac-count, title); if `implementation-plan.md` exists, read its frontmatter (status, ac-coverage, phase-count).
3. Regenerate the aggregation table (columns: `id`, `title`, `spec-status`, `plan-status`, `AC-coverage`, `has-plan?`).
4. Update dynamic frontmatter fields: `spec-count`, `plan-count`, `checklist-complete` (computed from the checklist's checkbox state).
5. Leave all other sections (theme, decisions, doc-update checklist text, hygiene gates section) untouched.
6. Report: efforts found, aggregation diff vs previous.

### `--gate vX.Y.Z`

Read-only. Walks:

0. **Emptiness check (precondition).** Count the efforts in scope for the release. If the count is zero, report the release as `INCONCLUSIVE` and do NOT emit PASS lines for gates (a) through (e): those gates iterate per-effort artifacts, so with nothing to iterate they would each report a vacuous PASS that reads as a clean bill of health. State explicitly that (a)-(e) are *unevaluated*, not passing. Still evaluate gate (f) and the doc-update checklist, which do not depend on efforts. See the "Emptiness guard" section of `references/hygiene-gates.md`.
1. Hygiene gates (a) through (f) per `references/hygiene-gates.md`. Report each as PASS / FAIL with the specific cause when FAIL.
2. Doc-update checklist: count checked vs total.
3. Release readiness: READY only when there is at least one effort in scope AND every gate passes AND every checklist item is checked.

Output: structured report; no file modification. An empty release is never READY; it is `INCONCLUSIVE` until efforts are in scope. If a release is intentionally tracked outside the spec chain (as v1.4.0 and v1.5.0 were), gate on (f) plus the checklist alone and record that choice in the plan's Decisions section. The skill never sets `status: released` automatically (the maintainer does that after tagging).

## Hard Constraints

1. **AC live in specs, not in the release plan.** If user input attempts to add an AC, refuse and redirect: "AC belong in the spec. Edit the linked spec or run `/plab-spec --revise`."
2. **Atomicity of promote/demote.** A folder move either completes (spec + plan + supporting all moved, frontmatter updated) or fails with no partial state. See `references/promote-demote.md`.
3. **Aggregation is generated, not authored.** `--update` regenerates the table; never hand-edit aggregation rows. The skill is the only writer of that section.
4. **Status flows up from evidence.** Never auto-set `status: released`. The skill reports readiness; the human acts on it.
5. **Checklist is a gate, not a reminder.** `--gate` reports unchecked items as FAIL. Tag time requires every item checked.
6. **Folder is self-contained.** `plan_vX.Y.Z.md` lives INSIDE `plan_vX.Y.Z/`, not as a sibling. The release folder is the unit of release-time freeze.

## Pairings

- **`/plab-spec`** writes `spec.md` into `_unassigned/<id>_<slug>/` (or directly into `plan_vX.Y.Z/<id>_<slug>/` if `--target-release` is passed).
- **`/superpowers:writing-plans`** writes `implementation-plan.md` into the same per-effort folder as its spec.
- **`/plab-release-plan --promote`** moves committed efforts from `_unassigned/` into the release. The promotion is the explicit commitment to ship.
- **`/plab-release-plan --gate`** is the pre-tag sanity check.

## References

| File | Purpose | Load when |
|------|---------|-----------|
| `references/plan-template.md` | Full output template for `plan_vX.Y.Z.md` (frontmatter + theme + aggregation + checklist + gates) | `--create` |
| `references/frontmatter-schema.md` | `type: release-plan` frontmatter fields, types, validation | `--create`, `--update` |
| `references/aggregation-table.md` | The aggregation table format and what to read from each effort folder | `--update`, `--gate` |
| `references/hygiene-gates.md` | The five default hygiene gates (a)-(e); how each is computed | `--gate` |
| `references/checklist-extension.md` | `release-checklist.yaml` schema and merge rules with built-in defaults | `--create`, `--update` |
| `references/promote-demote.md` | Atomicity rules; frontmatter side effects; failure modes | `--promote`, `--demote` |

