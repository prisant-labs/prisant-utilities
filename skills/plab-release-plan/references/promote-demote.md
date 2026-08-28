# Promote / Demote

Atomicity rules, frontmatter side effects, and failure modes for the two move operations.

## Atomicity

Per AC-2 of the spec (non-functional requirements): a promote or demote either completes fully or fails with no partial state. The contract:

**A successful promote of S-07:**

1. The folder `release-plans/_unassigned/S-07_<slug>/` no longer exists.
2. The folder `release-plans/plan_NN_<slug>/S-07_<slug>/` exists with all the original contents (`spec.md`, `implementation-plan.md` if it was present, `supporting/` if it was present).
3. `release-plans/plan_NN_<slug>/S-07_<slug>/spec.md` frontmatter has `target-release: vX.Y.Z` and `linked-release: docs/internal/release-plans/plan_NN_<slug>/plan.md`.
4. If `implementation-plan.md` exists in the folder, its `linked-release` is set to the same path.
5. The release plan's `plan.md` frontmatter `includes:` list contains the effort id.

**A failed promote of S-07** (e.g., disk write error mid-way):

1. `release-plans/_unassigned/S-07_<slug>/` still exists with original contents.
2. `release-plans/plan_NN_<slug>/S-07_<slug>/` does NOT exist (or is rolled back to non-existence).
3. The spec's frontmatter is unchanged.
4. The release plan's `includes:` is unchanged.

**Implementation guidance** (for an agent driving the moves):

```
# Pseudocode for --promote S-07:
1. Verify source folder exists and contains expected files
2. Read spec.md frontmatter (capture before)
3. Move folder: src -> dst
4. Update dst/spec.md frontmatter
5. Update dst/implementation-plan.md frontmatter (if exists)
6. Update plan.md includes: list
7. Run --update to refresh aggregation

# If any step 3-7 fails:
- If step 3 failed: nothing to roll back
- If step 4+ failed: move folder back (dst -> src); restore spec frontmatter
- Report the specific failure to the user
```

The "atomic move" guarantee is achieved by treating the folder as the unit; intermediate states are not exposed to subsequent reads (e.g., the aggregation table reflects either the old or the new state, never a half-move).

## Frontmatter side effects

### On promote `--from _unassigned --to vX.Y.Z S-07`:

| File | Field | Before | After |
|------|-------|--------|-------|
| `<S-07_slug>/spec.md` | `target-release` | (none or `null`) | `vX.Y.Z` |
| `<S-07_slug>/spec.md` | `linked-release` | `null` | `docs/internal/release-plans/plan_NN_<slug>/plan.md` |
| `<S-07_slug>/spec.md` | `updated` | (some date) | today's date |
| `<S-07_slug>/implementation-plan.md` (if exists) | `linked-release` | `null` | `docs/internal/release-plans/plan_NN_<slug>/plan.md` |
| `<S-07_slug>/implementation-plan.md` (if exists) | `updated` | (some date) | today's date |
| `plan.md` | `includes` | `[...]` | `[..., S-07]` (sorted) |
| `plan.md` | `status` | `draft` | `in-progress` (if was `draft` and this is the first promote) |
| `plan.md` | `updated` | (some date) | today's date |

### On demote `--from vX.Y.Z [--to _unassigned] S-07`:

| File | Field | Before | After |
|------|-------|--------|-------|
| `<S-07_slug>/spec.md` | `target-release` | `vX.Y.Z` | `null` |
| `<S-07_slug>/spec.md` | `linked-release` | `docs/internal/release-plans/plan_NN_<slug>/plan.md` | `null` |
| `<S-07_slug>/spec.md` | `updated` | (some date) | today's date |
| `<S-07_slug>/implementation-plan.md` (if exists) | `linked-release` | (path) | `null` |
| `<S-07_slug>/implementation-plan.md` (if exists) | `updated` | (some date) | today's date |
| `plan.md` | `includes` | `[..., S-07]` | `[...]` (S-07 removed) |
| `plan.md` | `status` | `in-progress` | `draft` (if `includes` becomes empty after the demote; otherwise unchanged) |
| `plan.md` | `updated` | (some date) | today's date |

## Failure modes

| Failure | Detection | Resolution |
|---------|-----------|-----------|
| Source folder missing | `Test-Path src` before moving | Refuse; report which id has no folder in `_unassigned/` |
| Destination already exists | `Test-Path dst` before moving | Refuse; report id collision; ask user to investigate |
| Disk write error mid-move | OS exception | Roll back: restore source folder if dest partially created; report I/O error with paths |
| Spec frontmatter unparseable | YAML parse failure | Refuse; report the unparseable file path; don't silently skip |
| `plan.md` does not exist | `Test-Path plan` after `--create` requirement | Refuse `--promote` / `--demote`; instruct to run `--create` first |
| `--to vX.Y.Z` references a non-existent release | Same | Same: refuse, instruct to `--create` |
| Effort id in promote list not in `_unassigned/` | Folder scan | Refuse the whole batch; report which id is missing |
| Effort id in demote list not in source release | Folder scan | Same |

The skill always refuses on partial-success: if 3 of 5 promotes would succeed and 2 would fail, the whole batch is refused. Either explicitly do the 3 valid promotes in a follow-up invocation, or fix the 2 problems first.

## What promote / demote do NOT do

- **Do not modify the spec body** (the `## Acceptance Criteria` section etc.). Frontmatter only.
- **Do not modify the implementation plan body.** Frontmatter only.
- **Do not change `status` on the spec or plan.** Only the release plan's `status` and the frontmatter fields listed above change.
- **Do not git-commit anything.** The maintainer commits when ready. (The skill never auto-commits, per hard constraint.)
- **Do not modify other releases.** A promote `--to v1.4.0` does not touch `v1.5.0` or other releases, even if the effort had previously been in one. (If the effort was in another release, that's a structural inconsistency the user fixes manually.)
- **Do not validate that the spec is "ready."** That's gate (a)'s job, run via `--gate`, not at promote time.

## When in doubt, run `--update`

`--update` is idempotent and read-mostly: it reconciles the release plan's aggregation and `includes:` list with the actual folder contents. If promote / demote left anything in a suspicious state, `--update` is the first thing to run to surface the truth.
