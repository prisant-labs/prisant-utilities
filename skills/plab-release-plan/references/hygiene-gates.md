# Hygiene Gates

The release-blocking conditions enforced by `--gate`. A release is READY only when it has at least one effort in scope and all six gates PASS (see the Emptiness guard below for why the effort count is a precondition, not just an input).

Gates (a) through (e) are about the **efforts** in the release: are their specs frozen, planned, covered, done, and current. Gate (f) is about the **repo** shipping them: do the plugin manifests actually declare the version you are about to tag.

## Gate (a): Spec status

**Condition.** Every effort's `spec.md` has `status: committed` or `status: fulfilled`. No `draft` allowed at tag time.

**Why.** A draft spec means the AC are not frozen; shipping work whose contract is still in flux is the canonical "spec drift" failure mode.

**Computation.**
```
for folder in plan_NN_<slug>/<id>_<slug>/:
    spec = read folder/spec.md
    if spec.frontmatter.status in (draft, superseded):
        FAIL with reason "S-07 spec status is draft (must be committed or fulfilled)"
```

**Per D1 in spec section 9:** promote does NOT enforce this; promote allows draft. Gate (a) is where the enforcement bites.

## Gate (b): Coupled plan

**Condition.** Every effort folder contains an `implementation-plan.md`, OR the effort id appears in `gate-waivers:` with `gate: b` and a reason.

**Why.** Implementation plan is the HOW; shipping a spec without a plan means there's no audit trail of how the AC were met.

**Computation.**
```
for folder in plan_NN_<slug>/<id>_<slug>/:
    if not exists(folder/implementation-plan.md):
        if not (effort_id in gate-waivers with gate=b):
            FAIL with reason "S-07 has no implementation-plan.md (and not waived)"
```

**Waiver example (rare):** a one-line README fix that shipped via direct commit, where decomposing into a plan would be theater.

## Gate (c): AC coverage

**Condition.** Every `implementation-plan.md` has `ac-coverage: complete` in frontmatter.

**Why.** `partial` means some spec AC are not addressed by any phase; `unmapped` means none are. Either way, the plan does not deliver the spec's contract.

**Computation.**
```
for folder in plan_NN_<slug>/<id>_<slug>/:
    plan = read folder/implementation-plan.md (skip if absent; gate (b) handles that)
    if plan.frontmatter.ac-coverage != complete:
        FAIL with reason "S-07 implementation-plan ac-coverage is partial (gaps: AC-4, AC-8)"
```

If the plan has waived AC (rare; would be documented in the plan's body), the spec author should waive them in `gate-waivers` for gate (c) too. Otherwise, expect this to FAIL until AC are mapped.

## Gate (d): Phases done

**Condition.** Every implementation plan's completion-status table shows every phase as `Status: Done`.

**Why.** A `Done` phase means its work is verified per the phase's Verification subsection. The phase contributes to AC fulfillment. Until every phase is done, the spec's contract is not yet met.

**Computation.**
```
for folder in plan_NN_<slug>/<id>_<slug>/:
    plan = read folder/implementation-plan.md (skip if absent)
    parse the completion-status table (markdown table with columns: Phase, Goal, Fulfills AC, Owner, Status)
    if any row.Status != Done:
        FAIL with reason "S-07 plan: P2 In progress, P3 Not started, P4 Blocked"
```

The completion-status table is the source of truth; the plan's frontmatter `status: complete` is downstream of this gate.

## Gate (e): Staleness

**Condition.** For every effort folder, `spec.md`'s file mtime is NOT newer than the sibling `implementation-plan.md`'s file mtime.

**Why.** If the spec was edited after the plan was last written, the plan may be stale (the AC may have changed since the plan was decomposed). At tag time, the plan must reflect the current spec.

**Computation.**
```
for folder in plan_NN_<slug>/<id>_<slug>/:
    spec_mtime = mtime(folder/spec.md)
    plan_path = folder/implementation-plan.md
    if exists(plan_path):
        plan_mtime = mtime(plan_path)
        if spec_mtime > plan_mtime:
            FAIL with reason "S-07 spec was edited 2026-05-30 after plan was last edited 2026-05-28; revise implementation-plan.md against the spec"
```

Skip the check when there's no implementation plan (gate (b) handles that case).

## Gate (f): Manifest version

**Condition.** `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` both declare `version: X.Y.Z` matching the `vX.Y.Z` release being gated.

**Why.** The tag is the only input to the self-pinning marketplace (`.github/workflows/pin-marketplace.yml`). Tagging `v1.6.0` while the manifests still say `1.5.0` makes the marketplace advertise a release that does not exist in the plugin it serves: consumers install from `ref: v1.6.0` and receive a `plugin.json` claiming `1.5.0`.

The repo's other checks do not catch this. `scripts/validate-plugin-manifests.py` compares the two `plugin.json` files **against each other** (invariant 2) and the marketplace `ref` against the **marketplace's own** version (invariant 5), but nothing bridges the two. The workflow now refuses to pin on a mismatch, so the bad state cannot reach consumers - but that failure happens **after** the tag is already pushed, and recovery means deleting a public tag and re-cutting it.

This gate moves the catch to before the tag exists, where it costs nothing.

**Computation.**
```
target = the vX.Y.Z of the release being gated
claude_version = read .claude-plugin/plugin.json    -> .version
codex_version  = read .codex-plugin/plugin.json     -> .version

if claude_version != target.version or codex_version != target.version:
    FAIL with reason "manifests declare 1.5.0 but the release is v1.6.0;
                      bump both plugin.json files and merge to main before tagging"
```

Skip this gate (report `PASS (n/a)`) when the repo has no `.claude-plugin/plugin.json`, i.e. the project is not a plugin. The gate is plugin-repo-specific and must not block releases in ordinary projects.

Do **not** extend this gate to `.claude-plugin/marketplace.json`. Between the manifest-bump commit and the tag that follows it, the marketplace legitimately still points at the previous release; the pin workflow advances it on the tag push. Asserting marketplace equality here would fail a normal intermediate state.

## Emptiness guard

Gates (a) through (e) iterate the efforts in the release. With zero efforts, every loop body is skipped, no FAIL is emitted, and each gate reports PASS. That is a vacuous truth: the report reads as a clean bill of health when nothing was actually checked. A gate that cannot tell *healthy* from *empty* gives false assurance at the exact moment a human is deciding whether to tag - and today every release in this repo is empty of per-effort folders, so `--gate` would report all-PASS on all of them.

`--gate` therefore checks emptiness first. If the release has no efforts in scope:

- Report the release as **INCONCLUSIVE**, not READY and not a row of PASSes.
- Do **not** print per-gate PASS lines for (a) through (e). State that they are *unevaluated* - there is nothing to evaluate - not passing.
- Still evaluate gate (f) (manifest version) and the doc-update checklist. Neither depends on efforts, so both remain meaningful for an otherwise-empty release.
- Offer the escape hatch: a release intentionally tracked outside the spec chain can legitimately gate on (f) plus the checklist alone, provided that choice is recorded in the plan's Decisions section.

Report for an empty release:

```
Aggregation: 0 efforts, 0 plans, 0 AC across the release.

INCONCLUSIVE - no efforts in scope for v1.6.0.
Gates (a)-(e) evaluate per-effort artifacts and cannot run with zero efforts.
They are NOT passing; they are unevaluated.

  (f) plugin manifests declare v1.6.0 ........... PASS

Doc-update checklist: 3 of 8 checked.

NOT READY TO SHIP. Either bring efforts into scope for this release, or - if
this release is intentionally tracked outside the spec chain - record that in
the plan's Decisions section and gate on (f) plus the checklist alone.
```

## Reporting from `--gate`

For a populated release, every gate evaluates normally:

```
Aggregation: 2 efforts, 1 plan, 12 AC across the release.

Hygiene gates:
  (a) spec status committed/fulfilled .......... FAIL (S-05 is draft)
  (b) every effort has coupled plan ............ FAIL (S-05 has no plan; not waived)
  (c) implementation plan ac-coverage complete . PASS (1 of 1)
  (d) every phase Done ......................... FAIL (S-07: P3 In progress, P4 Not started)
  (e) no spec edited after plan ................ PASS
  (f) plugin manifests declare v1.6.0 .......... FAIL (both plugin.json say 1.5.0)

Doc-update checklist: 0 of 8 checked.

NOT READY TO SHIP. Resolve the 4 failed gates and check the 8 doc-update items, then re-run --gate.
```

## Waiver semantics

A waiver is a row in `gate-waivers:` frontmatter:

```yaml
gate-waivers:
  - id: S-05
    gate: b
    reason: "v1.2.0 zone removal; implementation plan deferred until decomposition stabilizes."
```

Waivers:

- **Must include a reason.** Empty reasons are rejected (warn the maintainer).
- **Apply per-gate.** `gate: b` waives only the coupled-plan gate for that effort. Other gates still apply.
- **Are visible in the report.** `--gate` shows waived items with a `(waived: <reason>)` annotation so the deferred check stays visible.
- **Are not silent passes.** A waived gate reports `PASS (waived)`, not just `PASS`.

Use waivers sparingly. Each waiver is a decision the maintainer is explicitly making to ship despite a missing safeguard. Document why.
