# Release plans

This folder holds the planned work for this plugin, one folder per release, with the specification
and implementation plan for every effort inside the release that will ship it.

If you are looking for what is currently released, read `CHANGELOG.md` at the repository root
instead. Nothing here has shipped; this is the plan.

## Start here

| Question | Read |
|---|---|
| What is coming next, and why? | `plan_v0.3.0/plan_v0.3.0.md`, then each later release plan in order |
| What exactly will change, and how will we know it worked? | The `spec.md` inside any effort folder |
| How will it actually get built? | The `implementation-plan.md` beside that spec |
| Can this release be tagged yet? | The Hygiene Gates table in the release plan |
| What documentation must be updated before the tag? | The Doc-Update Checklist in the release plan |

## The shape

```
docs/internal/release-plans/
    README.md                      this file
    release-checklist.yaml         project-specific doc-update rows, merged with the built-in defaults
    plan_v0.3.0/
        plan_v0.3.0.md             the release plan: theme, aggregation, gates, checklist, decisions
        D-07_waiting-on-blocker-contract/
            spec.md                WHAT will change, and the acceptance criteria that define done
            implementation-plan.md HOW it gets built, in phases, with verification per phase
        ...one folder per effort in the release
    plan_v0.4.0/
    ...
```

**The release folder is the unit of freeze.** Everything needed to understand and execute a release
sits inside it. An effort folder moves between releases as a whole, carrying its spec and plan
together, so scope changes never separate a contract from the work that fulfills it.

## The three document types

They answer different questions and must not absorb each other.

- **Release plan** (`plan_vX.Y.Z.md`) aggregates. It says what is in scope, whether the release can
  ship, and what documentation the tag depends on. It never contains acceptance criteria: those live
  in specs, and duplicating them here would create two versions that drift.
- **Spec** (`spec.md`) is the contract. Purpose, scope, non-goals, requirements, and numbered
  acceptance criteria, each one observable, testable, and cited to a source. The acceptance criteria
  are the durable artifact; they survive rewrites of the plan beneath them.
- **Implementation plan** (`implementation-plan.md`) is the route. Phases, files, steps, and a
  verification command per phase, plus a completion table mapping every phase to the acceptance
  criteria it fulfills.

A useful test when you are unsure where something belongs: if it states what "done" means, it is a
spec; if it states how to get there, it is a plan; if it states whether we can ship, it is the
release plan.

## Dependencies between efforts

Several efforts depend on others, sometimes across releases: the arc resume needs the aggregation
layer, the log-format consolidation needs the derivation script, and the blocker-promotion work needs
the blocked-since dates that an earlier release introduces.

Those dependencies are recorded **in prose**, not in a frontmatter field. Each dependent spec names
what it needs in its Purpose, carries it as a numbered requirement, and where the ordering is
load-bearing, adds an acceptance criterion that fails if the prerequisite is not actually in place.
An implementation plan whose prerequisite is missing should stop at its first phase rather than build
against something that is not there.

The tradeoff is deliberate. A machine-readable dependency field would let tooling sort the graph, but
nothing in this repository reads such a field today, and an unread field is a producer with no
consumer, which is a defect this plugin has already shipped once and is currently fixing. Prose that
a human and an agent both read is the cheaper contract until something needs to sort the graph.

## Effort IDs

Effort IDs are zero-padded (`D-07`, `W-02`, `C-05`) to satisfy the schema, while the source roadmaps
that define them use unpadded forms (`D-7`, `W-2`, `C-5`). Each spec states its own mapping. Always
pair an ID with a short handle in prose, for example "D-07 (the Waiting-on blocker contract)", since
a bare ID forces the reader to go hunting for what it refers to.

The source documents that define these efforts are maintainer-local and gitignored, under
`_local/skill-roadmaps/`. Each spec's `linked-effort` frontmatter names the exact file. If you are
reading this from a clone, those sources will not be present; the specs are written to stand alone.

## Status, and why so much of it says "draft"

Specs are born `draft` and are promoted to `committed` by a human, never by a tool. Until an effort is
actually executed, its release will fail hygiene gates (a) spec status, (d) phases done, and (f)
manifest version. That is the correct reading of unstarted work, not a defect in the plan. A release
plan reporting all gates green before the work exists would be a plan that cannot tell healthy from
empty.

## Working with these documents

The `/jp-release-plan` skill owns this folder's structure:

| Command | Effect |
|---|---|
| `--create vX.Y.Z` | Scaffold a new release folder and plan document |
| `--promote --from _unassigned --to vX.Y.Z <ids>` | Move effort folders into a release |
| `--demote --from vX.Y.Z <ids>` | Move them back out |
| `--update vX.Y.Z` | Regenerate the aggregation table and computed frontmatter from disk |
| `--gate vX.Y.Z` | Read-only readiness report against the hygiene gates and checklist |

Two rules that keep this folder honest:

1. **The Aggregation table is generated, never hand-edited.** It is rebuilt from the folder contents,
   so it cannot silently disagree with what is actually on disk.
2. **Acceptance criteria are never added or edited here.** Revise the spec instead, marking the
   original criterion superseded rather than rewriting it, so that plans and commits referencing it
   keep pointing at something stable.
