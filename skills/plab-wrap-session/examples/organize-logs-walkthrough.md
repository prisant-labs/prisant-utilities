# Worked example: `--organize`

A real run of `scripts/organize-logs.py` against a six-log store. Every block below is actual
captured output, not an illustration.

The run is pinned to `--today 2026-08-18`, so the hot window is **2026-08** (current) and **2026-07**
(previous). Everything older is filed.

Commands are shown relative to this skill's directory, which is how the skill invokes them wherever the
plugin is installed. The store argument is relative to the project being wrapped. All output below is
verbatim.

## Before

```
_local/_session-logs/2026-05-19_14-30_claude_skill-audit.md
_local/_session-logs/2026-06-02_11-15_codex_guide-pdf-toolchain.md
_local/_session-logs/2026-06-30_09-40_claude_capture-lite-hook.md
_local/_session-logs/2026-07-21_16-05_claude_release-v011.md
_local/_session-logs/2026-08-04_10-12_codex_ai-review-close-pass.md
_local/_session-logs/2026-08-18_13-44_claude_marketplace-ssh-to-https-fix.md
_local/_session-logs/_capture/2026-08.jsonl
_local/_session-logs/notes.md
```

Two things in there are not session logs: the `_capture/` hook records and a stray `notes.md`.
Both survive untouched.

## Step 1: dry run

The script is dry run by default. Nothing moves.

```console
$ python scripts/organize-logs.py _local/_session-logs
Would file 3 log(s) into 2 month folder(s): 2026-05, 2026-06
  2026-05-19_14-30_claude_skill-audit.md -> 2026-05/2026-05-19_14-30_claude_skill-audit.md
  2026-06-02_11-15_codex_guide-pdf-toolchain.md -> 2026-06/2026-06-02_11-15_codex_guide-pdf-toolchain.md
  2026-06-30_09-40_claude_capture-lite-hook.md -> 2026-06/2026-06-30_09-40_claude_capture-lite-hook.md
Kept hot (3): the current and previous month are never filed.
Left in place, name does not match the log pattern (1): notes.md

Dry run. Re-run with --apply to perform these moves.
```

Three logs move, three stay hot, `notes.md` is reported and left alone.

## Step 2: apply

`/plab-wrap-session --organize` shows the plan above, asks once, and only then runs this.

```console
$ python scripts/organize-logs.py _local/_session-logs --apply
Filed 3 log(s) into 2 month folder(s): 2026-05, 2026-06
  2026-05-19_14-30_claude_skill-audit.md -> 2026-05/2026-05-19_14-30_claude_skill-audit.md
  2026-06-02_11-15_codex_guide-pdf-toolchain.md -> 2026-06/2026-06-02_11-15_codex_guide-pdf-toolchain.md
  2026-06-30_09-40_claude_capture-lite-hook.md -> 2026-06/2026-06-30_09-40_claude_capture-lite-hook.md
Kept hot (3): the current and previous month are never filed.
Left in place, name does not match the log pattern (1): notes.md
```

## After

```
_local/_session-logs/2026-05/2026-05-19_14-30_claude_skill-audit.md
_local/_session-logs/2026-06/2026-06-02_11-15_codex_guide-pdf-toolchain.md
_local/_session-logs/2026-06/2026-06-30_09-40_claude_capture-lite-hook.md
_local/_session-logs/2026-07-21_16-05_claude_release-v011.md
_local/_session-logs/2026-08-04_10-12_codex_ai-review-close-pass.md
_local/_session-logs/2026-08-18_13-44_claude_marketplace-ssh-to-https-fix.md
_local/_session-logs/_capture/2026-08.jsonl
_local/_session-logs/notes.md
```

Filenames are unchanged. `_capture/` and `notes.md` are exactly where they were.

`/plab-continue-session` 1.3.0+ still resumes from
`2026-08-18_13-44_claude_marketplace-ssh-to-https-fix.md`, because it pools the flat store and the
month folders and sorts on the filename alone.

## Step 3: run it again

Idempotent. A second `--apply` moves nothing and exits 0.

```console
$ python scripts/organize-logs.py _local/_session-logs --apply
Nothing to file. Every log is already filed or still hot.
Kept hot (3): the current and previous month are never filed.
Already filed: 3 log(s) in existing month folders.
Left in place, name does not match the log pattern (1): notes.md
```

## Machine-readable form

`--json` emits the same plan for the hygiene sweep's Check 5, which calls it in dry run to decide
whether there is anything worth proposing.

```console
$ python scripts/organize-logs.py _local/_session-logs --json
{
  "moves": [
    {
      "from": "2026-05-19_14-30_claude_skill-audit.md",
      "to": "2026-05/2026-05-19_14-30_claude_skill-audit.md"
    },
    {
      "from": "2026-06-02_11-15_codex_guide-pdf-toolchain.md",
      "to": "2026-06/2026-06-02_11-15_codex_guide-pdf-toolchain.md"
    },
    {
      "from": "2026-06-30_09-40_claude_capture-lite-hook.md",
      "to": "2026-06/2026-06-30_09-40_claude_capture-lite-hook.md"
    }
  ],
  "hot": [
    "2026-07-21_16-05_claude_release-v011.md",
    "2026-08-04_10-12_codex_ai-review-close-pass.md",
    "2026-08-18_13-44_claude_marketplace-ssh-to-https-fix.md"
  ],
  "unmatched": [
    "notes.md"
  ],
  "collisions": [],
  "archived": 0,
  "applied": false
}
```

Check 5 flags on a non-empty `moves` list, stays silent when it is empty, and routes a non-empty
`collisions` list to Waiting on You instead of the proposal queue.

## What it will not do

| Situation | Behavior |
|---|---|
| Log from the current or previous month | Never filed |
| Target filename already exists in the month folder | Skipped, reported as `SKIPPED`, exit code 1, nothing overwritten |
| File whose name is not `YYYY-MM-DD_HH-MM_<llm>_<title>.md` | Left in place, reported |
| Any subdirectory that is not `YYYY-MM` | Never entered |
| Legacy stores (`_agent-context/session-log/`, `AGENTS/session-log/`) | Never touched |
| Anything at all | Never deleted; moves only |

## Reproducing this

`scripts/test-organize-logs.py` builds throwaway fixtures like this one and asserts all of the above
across 34 checks, with the date pinned so results do not drift as the calendar moves.

```console
$ python scripts/test-organize-logs.py
34/34 checks passed.
ALL PASS
```
