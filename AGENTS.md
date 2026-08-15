# AGENTS.md

Agent navigation entrypoint for the `prisant-utilities` plugin.

## What this is

Five general-purpose agent skills for the work around the work: closing and resuming coding sessions, turning raw thinking into a decision-ready brief, producing guide bundles, and getting a second model to review a document.

Conventions an agent should follow in this repo:

- Every skill name carries the `plab-` prefix and matches its directory name exactly.
- Skills load shared utilities from the plugin root: `references/` for authoring guidance, `lib/` for executable helpers.
- Generated artifacts go to `_output/<skill-name>/`, which is gitignored.
- Never write em-dashes (U+2014) or en-dashes (U+2013). Use " - " or restructure.

## Components

- **Skills:** see the `## Skills` section below.

## Skills

_Populated as skills land._

## Build and validate

- Conformance gate: `node <agent-skills-toolkit>/scripts/check.mjs .`
- The canonical manifest is `library.json`. `.claude-plugin/plugin.json` mirrors its `name` and `description`; they must not drift.

## License

MIT. See `LICENSE`.
