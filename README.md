# prisant-utilities

Eight agent skills for the work around the work: scaffolding a repository for agent-assisted development, closing and resuming coding sessions, turning raw thinking into a decision-ready brief, producing guide bundles, getting a second model to review a document, and carrying a feature from written specification through to a taggable release plan.

Works with Claude Code and Codex.

## Skills

| Skill | What it does | Version |
|---|---|---|
| [`plab-wrap-session`](docs/skills/plab-wrap-session/README.md) | Close a coding session with a structured log: hygiene sweep, evidence index, and a copy-paste-ready continuation prompt for next time | 1.6.0 |
| [`plab-continue-session`](docs/skills/plab-continue-session/README.md) | Resume from the most recent session log and pick up the named next action | 1.3.0 |
| [`plab-strategy-brief`](docs/skills/plab-strategy-brief/README.md) | Turn a brain dump into a structured, decision-ready analysis document | 1.1.1 |
| [`plab-guide`](docs/skills/plab-guide/README.md) | Generate a guide bundle: standard Markdown, an ADHD-formatted variant, a quick-reference HTML page, and a 1-2 page PDF | 2.2.2 |
| [`plab-ai-review`](docs/skills/plab-ai-review/README.md) | Run a structured peer review of a document with a second model, then synthesise the findings | 1.2.1 |
| [`plab-spec`](docs/skills/plab-spec/README.md) **&sup1;** | Write a feature spec: numbered acceptance criteria, each cited to a source, in a per-effort folder | 1.2.1 |
| [`plab-release-plan`](docs/skills/plab-release-plan/README.md) **&sup1;** | Scope a release, promote efforts into it, and gate the tag on hygiene checks and a doc-update checklist | 1.3.0 |
| [`plab-init-project`](docs/skills/plab-init-project/README.md) **&sup1;** | Scaffold agent infrastructure into a repository: AGENTS.md, CLAUDE.md, session logs, decision records | 1.3.0 |

**&sup1; Manual invocation only.** These three ship with `disable-model-invocation: true`. They never fire on their own; type `/plab-spec`, `/plab-release-plan` or `/plab-init-project` to run them. Their trigger phrases ("spec", "init", "plan the release") are too common in ordinary conversation to be safe auto-matches, and all three write files into your repository.

The session pair is a contract: `plab-wrap-session` writes the log that `plab-continue-session` reads. They are versioned and released together.

The document trio is a pipeline: `plab-spec` writes the acceptance criteria, `/superpowers:writing-plans` writes the implementation plan beside it, and `plab-release-plan` aggregates whole effort folders into a release and decides whether it can ship.

## Install

```
/plugin marketplace add prisant-labs/agent-plugins
/plugin install prisant-utilities@agent-plugins
```

Then invoke any skill by name, for example `/plab-wrap-session`.

## Conventions

**Generated artifacts** are written to `_output/<skill-name>/` relative to your working directory. Every producing skill accepts an explicit destination to override that. Add `_output/` to your `.gitignore`.

That applies to the content-producing skills. The three planning skills write where their artifacts belong instead: `plab-spec` and `plab-release-plan` into per-effort folders under `docs/internal/release-plans/`, and `plab-init-project` into the repository it is scaffolding, with its dry-run and onboarding reports under `_local/plab-init-project/`.

**Session logs** are written to `_local/_session-logs/`, which is expected to be gitignored. They are local working notes and are not intended to be committed. Once a store has been running a while, `/plab-wrap-session --organize` files logs from closed months into `YYYY-MM/` subfolders; `/plab-continue-session` reads the flat store and those month folders as one set, so resume keeps working either way.

**Toolchain.** `plab-guide` shells out to headless Chrome for PDF rendering, and optionally to `pdfinfo` and `mmdc` (Mermaid CLI). It reports what is missing and degrades gracefully rather than failing. Run `skills/plab-guide/scripts/check-toolchain.sh` to see the current state.

## Provenance

These skills were developed in a private library and carry their version numbers forward. Each one's `HISTORY.md` starts at the version it was migrated at and records what changed for public release.

## License

MIT. See [`LICENSE`](LICENSE).
