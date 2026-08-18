# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2] - 2026-08-18

Correctness and bookkeeping. No new capability, but two of these change day-to-day behaviour.

**What changes for you.** Asking "what did we do?" or "where were we?" no longer risks launching a
session-log write or a resume ritual. Both skills listed those status questions as triggers, so a request
for an answer could be answered with a procedure instead. You now get the answer. Separately, quick-mode
and blocked-mode wraps stop producing logs that the wrap skill's own self-check rejects, so the fast path
is usable rather than quietly emitting output that fails its own gate. The wrap skill's description is 34
characters shorter, which is context you stop paying for in every session.

**What does not change.** No mode, section, template structure, or output format moved. A log written by
1.4.0 reads identically to one written by 1.4.1, and `/plab-continue-session` parses both the same way.
Nothing you have already written needs migrating.

### Fixed

- `plab-continue-session` 1.2.1: the skill body listed "where were we" and "what were we doing" as
  triggers, contradicting its own description, which refuses to fire on status questions. A narrowed
  description stops the skill firing; a stale body told it to proceed once it had. Both now agree.
- `plab-wrap-session` 1.4.1: dropped "what did we do" from the trigger list. It is a request for an
  answer, not a request to write a session log, and it is the same over-trigger class already removed
  from `plab-continue-session`. The description is shorter as a result.
- `plab-wrap-session` 1.4.1: the Quick and Blocked session-log templates omitted `machine:`, and the
  SKILL.md frontmatter block omitted `type:`, both of which the frontmatter schema places in Tier 1 and
  the skill's own self-check requires in every mode. An agent following either light template produced a
  log the skill would reject.
- Usage documentation for `plab-continue-session` opened with a description two rewrites out of date and
  documented a field list that predated the 1.2.0 extraction changes.
- Removed ten dangling references to `/jp-init-project`, `jp-implementation-plan`, and `jp-skill-builder`
  across both skills' usage docs. None of the three ships in this plugin. The v0.1.1 sweep looked for
  private folder paths and did not look for private skill names.

### Notes

`plab-continue-session`'s description was rewritten on 2026-08-17 in commit `38a75f0` and shipped inside
v0.1.1 with no version bump, no history entry, and no changelog line. Its 1.2.1 history entry records that
retroactively. The hygiene check that would have caught it is one-directional and is scheduled for a
later release.

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
