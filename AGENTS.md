# AGENTS.md

Agent navigation entrypoint for the `prisant-utilities` plugin.

## What this is

Eight general-purpose agent skills for the work around the work: scaffolding a repository for agent-assisted development, closing and resuming coding sessions, turning raw thinking into a decision-ready brief, producing guide bundles, getting a second model to review a document, and carrying a feature from written specification through to a taggable release plan.

One of the eight ships with `disable-model-invocation: true` and runs only when invoked by name: `plab-init-project`. It scaffolds files into a repository root, its trigger phrases ("init", "initialize", "set up") are among the most common words in ordinary conversation, and it is run once per repository rather than routinely.

`plab-spec` and `plab-release-plan` carried the same flag through v0.4.3 and no longer do. Their descriptions now carry explicit do-NOT-fire clauses instead, which is the mechanism that took `plab-continue-session` from over-triggering to correct: a narrowed description is a better instrument than a binary gate, because it can distinguish a request from a mention.

## Design frame

**This plugin is built for its maintainer's own use.** The repository is public because there is no reason for it not to be, not because the skills target an adoption curve. Where a general-purpose choice and a personally-useful choice diverge, the personally-useful one wins.

Practical consequences for anyone proposing or changing a skill here:

- Do not add configurability, onboarding affordances, or compatibility shims for hypothetical third-party users.
- Skill descriptions still matter enormously, and arguably more. The description is the trigger mechanism for the one user who matters; a skill that does not fire is a skill that does not exist.
- Always-on context cost is paid by one person in every session, forever. A rarely-used skill should justify its description budget or ship with model invocation disabled so it runs only on explicit command.
- A skill that goes unused has no value at all. There is no second user to rescue it.

Conventions an agent should follow in this repo:

- Every skill name carries the `plab-` prefix and matches its directory name exactly.
- Skills load shared utilities from the plugin root: `references/` for authoring guidance, `lib/` for executable helpers.
- Generated artifacts go to `_output/<skill-name>/`, which is gitignored. The three planning skills are the
  exception: `plab-spec` and `plab-release-plan` write into `docs/internal/release-plans/`, and
  `plab-init-project` writes into the repository it scaffolds.
- Never write em-dashes (U+2014) or en-dashes (U+2013). Use " - " or restructure.

## Skills

### plab-wrap-session

Document and close agentic coding sessions with structured session logs. Deep mode is the default: a full log with an evidence index, a pre-wrap hygiene sweep (remote divergence, release state, doc drift, working-tree reconciliation, unfiled session logs, all with per-action confirmation), a mandatory "waiting on you" section with file links, and a verbose copy-paste-ready continuation prompt in every mode. Writes to `_local/_session-logs/`, which is expected to be gitignored. `--organize` runs instead of a wrap and files logs from closed months into `YYYY-MM/` subfolders via `skills/plab-wrap-session/scripts/organize-logs.py`, leaving the current and previous month flat.

**Trigger:** `/plab-wrap-session`, "wrap up", "end of session", "session log", "close out"

---

### plab-continue-session

Resume an interrupted work session by replaying its recorded handoff. The read-side companion to `/plab-wrap-session`. Reads the most recent session log, leads with what is blocked on the maintainer, surfaces the outstanding work and the named next action, and confirms before acting. Discovery pools the flat store with its `YYYY-MM/` month folders and the legacy locations, newest filename wins. Does not fire on status questions; those get answered directly.

**Trigger:** `/plab-continue-session`, "continue", "resume", "pick up where we left off"

---

### plab-strategy-brief

Transform messy thinking into a structured, decision-ready analysis document. Use when someone provides raw, unstructured thoughts and wants them organised, expanded, and turned into an actionable artifact. Not for summarising already-structured documents or for pure research queries with no raw thinking supplied.

**Trigger:** `/plab-strategy-brief`, "help me think through", "brain dump", "make sense of this", "strategy primer"

---

### plab-guide

Generate a paired guide bundle for any topic: a standard Markdown guide, an ADHD-formatted variant, a quick-reference HTML page, and a 1-2 page PDF operator card. Accepts a repository URL, a tool name, or a concept.

**Trigger:** `/plab-guide`, "create a guide", "build a cheat sheet", "explain X with a quick reference"

---

### plab-ai-review

Generate and synthesise structured peer reviews across models. Three modes: `--review` produces a self-contained review request for a second LLM, `--respond` adds requestor synthesis once the reviewer has filed findings, and `--close` archives the source and review, applies accepted changes, and writes unresolved decisions to a backlog. Designed to be run in a different harness from the one that produced the document under review.

**Trigger:** `/plab-ai-review`, "review this with a second model", "get a second opinion", "peer review this"

---

### plab-spec

Create a feature specification: the contract between intent and implementation. Writes a `spec.md` into a per-effort folder under `docs/internal/release-plans/`, carrying frontmatter, an agent-updated Task Summary block, numbered acceptance criteria each cited to a source, and links to the related effort and plan. Lands in `_unassigned/` by default, or straight into a release folder with `--target-release vX.Y.Z`. Defines WHAT to build; `/superpowers:writing-plans` defines HOW and `/plab-strategy-brief` explores WHY. Refuses to write implementation steps.

**Invocation:** auto-discoverable as of 1.3.0. Fires on an explicit request to write a spec or turn requirements into acceptance criteria. Its description carries a do-NOT-fire clause for passing mentions of the word "spec", questions about an existing spec, and requests to implement one.

---

### plab-release-plan

Aggregate every spec and implementation plan in scope of a release into one self-contained folder, and gate the tag on hygiene checks plus a doc-update checklist. Five subcommands: `--create` scaffolds the release folder and plan document, `--promote` and `--demote` move whole per-effort folders between `_unassigned/` and a release, `--update` regenerates the aggregation table from disk, `--gate` reports readiness read-only. The aggregation table is generated, never hand-edited. Refuses to add or modify acceptance criteria; those live in specs.

**Invocation:** auto-discoverable as of 1.4.0. Fires on release scoping, promoting or demoting efforts, and release-readiness checks. Its description carries a do-NOT-fire clause for general planning talk, release-notes or changelog requests, and questions about what already shipped.

---

### plab-init-project

Initialize agent development infrastructure in a repository: `AGENTS.md`, `CLAUDE.md`, gitignored `_local/_session-logs/`, and MADR v4 decision records. Three profiles: `minimal`, `standard`, `public`. Non-destructive and idempotent, so it is safe to run against a repository that already has some of this. Pairs with `plab-wrap-session` and `plab-continue-session`, which write and read the session logs it scaffolds.

**Invocation:** manual only (`disable-model-invocation: true`). `/plab-init-project`.

---

## Build and validate

- Conformance gate: `node <agent-skills-toolkit>/scripts/check.mjs .`
- CI runs the same gate automatically: `.github/workflows/gate.yml` grades against the Advanced Skill Library Standard on every pull request and every push to `main`, and runs `scripts/check-dashes.py` repo-wide. CI reports; it never fixes, bumps, or tags. The two toolkit-internal scripts it deliberately skips are named and explained in the workflow header.
- The canonical manifest is `library.json`. `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` are generated from it; do not hand-edit them.
- Regenerate native manifests: `node <agent-skills-toolkit>/scripts/generators/gen-manifest.mjs . --write --target=all`

## License

MIT. See `LICENSE`.
