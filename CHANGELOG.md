# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2026-08-17

### Fixed

- Removed four dangling references to a private development folder (`docs/internal/agent-skills-published/...`) that the migration's mechanical rename had rewritten rather than deleted. Affected `plab-guide`'s theme reference and regression script, and the `plab-guide` and `plab-ai-review` usage docs.
- `scripts/regression-test.sh` no longer points at a path that cannot exist in this repository. Baseline bundles are not shipped; the script now accepts your own via `PLAB_GUIDE_EXAMPLES_DIR` and exits 2 with a clear message when absent.
- `references/quick-ref-theme.md` described two source-of-truth templates kept in sync, when only one ships here.

## [0.1.0] - 2026-08-17

### Added

- Initial public release with five skills: `plab-wrap-session` 1.4.0, `plab-continue-session` 1.2.0, `plab-strategy-brief` 1.1.1, `plab-guide` 2.2.1, `plab-ai-review` 1.2.1.
- Shared plugin-root utilities: `lib/render-mermaid.py`, `references/diagrams.md`, `references/decisions-section.md`.
- Per-skill usage documentation under `docs/skills/`.
- `library.json` as the canonical manifest, with native Claude Code and Codex manifests generated from it.

### Notes

Skills were previously developed in a private library and carry their version numbers forward unchanged. Per-skill `HISTORY.md` files start at the migrated version and record what changed for public release; earlier history remains private.

The default output root for generated artifacts is `_output/<skill-name>/`, replacing a brand-named folder used privately.
