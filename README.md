# prisant-utilities

Five agent skills for the work around the work: closing and resuming coding sessions, turning raw thinking into a decision-ready brief, producing guide bundles, and getting a second model to review a document.

Works with Claude Code and Codex.

## Skills

_Inventory populated as skills land. See `AGENTS.md` for the agent-facing index._

## Install

Via the prisant-labs marketplace:

```
/plugin marketplace add prisant-labs/agent-plugins
/plugin install prisant-utilities@agent-plugins
```

## Conventions

Generated artifacts are written to `_output/<skill-name>/` relative to your working directory, and each skill accepts an explicit destination to override that.

## License

MIT. See `LICENSE`.
