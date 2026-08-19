# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-08-18

Session-log stores can now be archived by month without breaking resume.

**What changes for you.** `/plab-wrap-session --organize` files logs from closed months into
`YYYY-MM/` subfolders, so a store that has been running for a year is browsable again. The current
and previous month stay flat, nothing moves without your confirmation on that specific plan, and
nothing is ever deleted. You do not have to remember the command exists: deep and final wraps now
report unfiled logs and offer to file them, the same way they already offer to push a commit or fix
a stale version line. Resume keeps working throughout, because `/plab-continue-session` reads the
flat store and the month folders as one set ordered by filename.

**What does not change.** New logs are still written flat to
`_local/_session-logs/YYYY-MM-DD_HH-MM_<llm>_<title>.md`. No mode, section, template, or frontmatter
field moved, and nothing you have already written needs migrating. Archiving is opt-in and
reversible: the organizer only ever moves files.

**One ordering note.** The reader had to learn month folders before anything could be filed into
one, so both skills ship together in this release. A store organized by this version and opened by an
older install would read as empty; that case now reports the version skew and points at
`/plugin update` rather than offering to start fresh.

### Added

- `plab-wrap-session` 1.5.0: `--organize` mode, backed by
  `skills/plab-wrap-session/scripts/organize-logs.py`. Dry run by default, idempotent, move-only,
  never deleting. The month comes from the filename prefix rather than mtime, because mtime is wrong
  after any copy or restore and the filename is the log's identity. Collisions skip the file and exit
  non-zero instead of overwriting.
- `plab-wrap-session` 1.5.0: hygiene sweep Check 5 reports unfiled logs and proposes filing them
  under the existing per-action confirmation protocol. The check calls the organizer in dry run, so
  the sweep's read-only detection phase and the operation it proposes are one code path.
- `plab-wrap-session` 1.5.0: `skills/plab-wrap-session/scripts/test-organize-logs.py`, 34 fixture
  checks with a pinned date covering dry-run inertness, the hot window across a year boundary,
  idempotence, `_capture/` isolation, collision safety, a missing store, and the discovery contract
  itself.
- `plab-wrap-session` 1.5.0: a worked example with real captured output at
  `skills/plab-wrap-session/examples/organize-logs-walkthrough.md`.
- `plab-continue-session` 1.3.0: discovery reads `YYYY-MM/` month folders alongside the flat store as
  one pooled corpus. It is a date-shaped allowlist exactly one level deep, never a recursive walk, so
  `_capture/` and any future deliberately-hidden subdirectory stay outside the corpus.
- `plab-continue-session` 1.3.0: an empty top level with month folders present is now reported as
  version skew, naming `/plugin update`, instead of "no prior session log found".

### Fixed

- `plab-continue-session` 1.3.0: a stray Markdown file in the log store could be resumed from.
  Selection globbed `*.md` and took the lexically last name, so a `README.md` or `notes.md` outranked
  every dated log. Both shell pipelines now match the `YYYY-MM-DD_` prefix. Latent until now;
  `--organize` makes it reachable by establishing that the store may hold non-log Markdown.

### Changed

- `plab-wrap-session` 1.5.0: session logs are cited by filename, never by directory-qualified path,
  in `resumed-from:` and in prose alike. A path-qualified reference breaks when the log is archived;
  a filename does not, which is why archiving needs no link-rewriting step.

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
