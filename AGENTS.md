# AGENTS.md

Agent navigation entrypoint for the `prisant-utilities` plugin.

## What this is

Five general-purpose agent skills for the work around the work: closing and resuming coding sessions, turning raw thinking into a decision-ready brief, producing guide bundles, and getting a second model to review a document.

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
- Generated artifacts go to `_output/<skill-name>/`, which is gitignored.
- Never write em-dashes (U+2014) or en-dashes (U+2013). Use " - " or restructure.

## Skills

### plab-wrap-session

Document and close agentic coding sessions with structured session logs. Deep mode is the default: a full log with an evidence index, a pre-wrap hygiene sweep (remote divergence, release state, doc drift, working-tree reconciliation with per-action confirmation), a mandatory "waiting on you" section with file links, and a verbose copy-paste-ready continuation prompt in every mode. Writes to `_local/_session-logs/`, which is expected to be gitignored.

**Trigger:** `/plab-wrap-session`, "wrap up", "end of session", "session log", "close out"

---

### plab-continue-session

Resume an interrupted work session by replaying its recorded handoff. The read-side companion to `/plab-wrap-session`. Reads the most recent session log, leads with what is blocked on the maintainer, surfaces the outstanding work and the named next action, and confirms before acting. Legacy log locations are also searched, newest wins. Does not fire on status questions; those get answered directly.

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

## Build and validate

- Conformance gate: `node <agent-skills-toolkit>/scripts/check.mjs .`
- The canonical manifest is `library.json`. `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` are generated from it; do not hand-edit them.
- Regenerate native manifests: `node <agent-skills-toolkit>/scripts/generators/gen-manifest.mjs . --write --target=all`

## License

MIT. See `LICENSE`.
