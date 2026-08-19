#!/usr/bin/env python3
"""Fixture tests for organize-logs.py. No test framework required.

Run: python skills/plab-wrap-session/scripts/test-organize-logs.py

Every case builds a throwaway store in a temp directory, so the tests never
touch a real session-log store. The date is pinned with --today so results do
not drift as the calendar moves.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "organize-logs.py"
TODAY = "2026-08-18"

HOT = [
    "2026-08-18_09-09_claude_hot-one.md",
    "2026-07-02_11-00_codex_hot-two.md",
]
COLD = [
    "2026-06-01_10-00_claude_cold-one.md",
    "2026-05-14_16-30_codex_cold-two.md",
    "2025-12-31_23-59_claude_year-boundary.md",
]
JUNK = ["README.md", "notes.md"]

results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, ok, detail))
    suffix = f"  |  {detail}" if detail and not ok else ""
    print(f"{'PASS' if ok else 'FAIL'}  {name}{suffix}")


def make_store(root: Path) -> Path:
    store = root / "_local" / "_session-logs"
    (store / "_capture").mkdir(parents=True)
    (store / "_capture" / "2026-08.jsonl").write_text("{}\n", encoding="utf-8")
    for name in HOT + COLD + JUNK:
        (store / name).write_text(f"# {name}\n", encoding="utf-8")
    return store


def run(store: Path, *args: str, today: str = TODAY) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(store), "--today", today, *args],
        capture_output=True, text=True,
    )


def discover(store: Path) -> list[str]:
    """The discovery contract from log-discovery.md, in Python.

    Date-prefixed names only, exactly one level deep, month folders pooled with
    the flat top level, sorted by basename descending.
    """
    log = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]_*.md"
    pooled = list(store.glob(log)) + list(store.glob(f"[0-9][0-9][0-9][0-9]-[0-9][0-9]/{log}"))
    return [p.name for p in sorted(pooled, key=lambda p: p.name, reverse=True)]


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)

        # 1. Dry run is the default and touches nothing.
        store = make_store(root / "dry")
        before = sorted(p.name for p in store.iterdir())
        dry = run(store)
        after = sorted(p.name for p in store.iterdir())
        check("dry run moves nothing", before == after, f"{before} != {after}")
        check("dry run exits 0", dry.returncode == 0, dry.stderr)
        check("dry run names --apply as the next step", "--apply" in dry.stdout, dry.stdout)

        # 2. Apply files only closed months.
        store = make_store(root / "apply")
        applied = run(store, "--apply")
        check("apply exits 0", applied.returncode == 0, applied.stderr)
        for name in HOT:
            check(f"hot kept flat: {name}", (store / name).exists(), applied.stdout)
        for name in COLD:
            month = name[:7]
            check(f"cold filed: {name}", (store / month / name).exists(), applied.stdout)
            check(f"cold left top level: {name}", not (store / name).exists())

        # 3. Files that are not logs are left alone and reported.
        for name in JUNK:
            check(f"unmatched left in place: {name}", (store / name).exists())
        check("unmatched reported in output",
              "does not match the log pattern" in applied.stdout, applied.stdout)

        # 4. Non-date subdirectories are never entered or created into.
        check("_capture untouched", (store / "_capture" / "2026-08.jsonl").exists())
        check("no month folder created inside _capture",
              not (store / "_capture" / "2026-08").exists())

        # 5. Idempotence: a second apply is a no-op.
        second = run(store, "--apply")
        check("second apply exits 0", second.returncode == 0, second.stderr)
        check("second apply moves nothing", "Nothing to file" in second.stdout, second.stdout)

        # 6. Discovery still finds every log, newest first, ignoring _capture and junk.
        names = discover(store)
        check("discovery pools flat and archived",
              len(names) == len(HOT) + len(COLD), str(names))
        check("newest wins across placement",
              names[0] == "2026-08-18_09-09_claude_hot-one.md", str(names[:2]))
        check("discovery ignores _capture",
              all(not n.endswith(".jsonl") for n in names), str(names))
        check("discovery ignores non-log markdown",
              not any(n in JUNK for n in names), str(names))

        # 7. Archived-newer-than-hot: ordering is independent of directory.
        ordering = root / "ordering" / "_local" / "_session-logs" / "2026-06"
        ordering.mkdir(parents=True)
        (ordering / "2026-06-30_23-00_claude_newest.md").write_text("x\n", encoding="utf-8")
        (ordering.parent / "2026-05-01_08-00_claude_older-hot.md").write_text("x\n",
                                                                             encoding="utf-8")
        order_names = discover(ordering.parent)
        check("archived log outranks older hot log",
              order_names[0] == "2026-06-30_23-00_claude_newest.md", str(order_names))

        # 8. Year boundary: the previous month of 2026-01 is 2025-12.
        jan = make_store(root / "jan")
        jan_run = run(jan, "--apply", today="2026-01-15")
        check("year boundary keeps 2025-12 hot",
              (jan / "2025-12-31_23-59_claude_year-boundary.md").exists(), jan_run.stdout)

        # 9. Collisions skip the file, never overwrite, and exit non-zero.
        collide = make_store(root / "collide")
        (collide / "2026-06").mkdir()
        (collide / "2026-06" / COLD[0]).write_text("existing\n", encoding="utf-8")
        clash = run(collide, "--apply")
        check("collision exits non-zero", clash.returncode != 0, clash.stdout)
        check("collision leaves the original in place", (collide / COLD[0]).exists())
        check("collision does not overwrite the target",
              (collide / "2026-06" / COLD[0]).read_text(encoding="utf-8") == "existing\n")
        check("collision is reported", "SKIPPED" in clash.stdout, clash.stdout)

        # 10. A missing store is not an error.
        absent = run(root / "does-not-exist")
        check("missing store exits 0", absent.returncode == 0, absent.stderr)
        check("missing store reports nothing to do",
              "Nothing to file" in absent.stdout, absent.stdout)

        # 11. --json emits a parseable plan.
        import json as _json
        js = run(make_store(root / "json"), "--json")
        try:
            parsed = _json.loads(js.stdout)
            check("--json emits valid JSON", True)
            check("--json plan lists the cold logs",
                  len(parsed["moves"]) == len(COLD), js.stdout)
            check("--json reports applied=false on dry run",
                  parsed["applied"] is False, js.stdout)
        except _json.JSONDecodeError as exc:
            check("--json emits valid JSON", False, f"{exc}: {js.stdout[:200]}")

    failed = [name for name, ok, _ in results if not ok]
    print()
    print(f"{len(results) - len(failed)}/{len(results)} checks passed.")
    if failed:
        print("FAILED: " + ", ".join(failed))
        return 1
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
