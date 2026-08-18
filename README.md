# prisant-utilities

Five agent skills for the work around the work: closing and resuming coding sessions, turning raw thinking into a decision-ready brief, producing guide bundles, and getting a second model to review a document.

Works with Claude Code and Codex.

## Skills

| Skill | What it does | Version |
|---|---|---|
| [`plab-wrap-session`](docs/skills/plab-wrap-session/README.md) | Close a coding session with a structured log: hygiene sweep, evidence index, and a copy-paste-ready continuation prompt for next time | 1.4.1 |
| [`plab-continue-session`](docs/skills/plab-continue-session/README.md) | Resume from the most recent session log and pick up the named next action | 1.2.1 |
| [`plab-strategy-brief`](docs/skills/plab-strategy-brief/README.md) | Turn a brain dump into a structured, decision-ready analysis document | 1.1.1 |
| [`plab-guide`](docs/skills/plab-guide/README.md) | Generate a guide bundle: standard Markdown, an ADHD-formatted variant, a quick-reference HTML page, and a 1-2 page PDF | 2.2.1 |
| [`plab-ai-review`](docs/skills/plab-ai-review/README.md) | Run a structured peer review of a document with a second model, then synthesise the findings | 1.2.1 |

The session pair is a contract: `plab-wrap-session` writes the log that `plab-continue-session` reads. They are versioned and released together.

## Install

```
/plugin marketplace add prisant-labs/agent-plugins
/plugin install prisant-utilities@agent-plugins
```

Then invoke any skill by name, for example `/plab-wrap-session`.

## Conventions

**Generated artifacts** are written to `_output/<skill-name>/` relative to your working directory. Every producing skill accepts an explicit destination to override that. Add `_output/` to your `.gitignore`.

**Session logs** are written to `_local/_session-logs/`, which is expected to be gitignored. They are local working notes and are not intended to be committed.

**Toolchain.** `plab-guide` shells out to headless Chrome for PDF rendering, and optionally to `pdfinfo` and `mmdc` (Mermaid CLI). It reports what is missing and degrades gracefully rather than failing. Run `skills/plab-guide/scripts/check-toolchain.sh` to see the current state.

## Provenance

These skills were developed in a private library and carry their version numbers forward. Each one's `HISTORY.md` starts at the version it was migrated at and records what changed for public release.

## License

MIT. See [`LICENSE`](LICENSE).
