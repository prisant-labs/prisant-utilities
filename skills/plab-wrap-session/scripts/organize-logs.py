#!/usr/bin/env python3
"""Archive plab session logs into YYYY-MM month folders.

Dry run by default. Pass --apply to perform the moves.

The month comes from the filename prefix, never from mtime: mtime is wrong
after any copy, sync, or restore, and the filename is the log's identity.

The current month and the previous month are never filed, so recent logs stay
flat where /plab-continue-session reads them first.

Layout rules are defined once, in
skills/plab-continue-session/references/log-discovery.md.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

# YYYY-MM-DD_HH-MM_<llm>_<brief-kebab-title>.md
LOG_NAME = re.compile(r"^(\d{4}-\d{2})-\d{2}_\d{2}-\d{2}_[^_]+_.+\.md$")
MONTH_DIR = re.compile(r"^\d{4}-\d{2}$")
DEFAULT_STORE = Path("_local/_session-logs")


def hot_months(today: dt.date) -> set[str]:
    """The current month and the previous one. Never archived."""
    first = today.replace(day=1)
    previous = (first - dt.timedelta(days=1)).replace(day=1)
    return {first.strftime("%Y-%m"), previous.strftime("%Y-%m")}


def build_plan(store: Path, today: dt.date) -> dict:
    """Classify every top-level entry. Never descends into subdirectories."""
    plan: dict = {"moves": [], "hot": [], "unmatched": [], "collisions": [], "archived": 0}
    if not store.is_dir():
        return plan

    hot = hot_months(today)
    for entry in sorted(store.iterdir()):
        if entry.is_dir():
            # Month folders are already-filed logs. Everything else in the store
            # is deliberately outside the corpus and is never entered.
            if MONTH_DIR.match(entry.name):
                plan["archived"] += len(list(entry.glob("*.md")))
            continue
        if entry.suffix != ".md":
            continue
        match = LOG_NAME.match(entry.name)
        if not match:
            plan["unmatched"].append(entry.name)
            continue
        month = match.group(1)
        if month in hot:
            plan["hot"].append(entry.name)
            continue
        if (store / month / entry.name).exists():
            plan["collisions"].append(entry.name)
            continue
        plan["moves"].append({"from": entry.name, "to": f"{month}/{entry.name}"})
    return plan


def apply_plan(store: Path, plan: dict) -> None:
    """Move every planned log. Creates month folders as needed. Never deletes."""
    for move in plan["moves"]:
        target = store / move["to"]
        target.parent.mkdir(parents=True, exist_ok=True)
        (store / move["from"]).rename(target)


def render(plan: dict, applied: bool) -> str:
    lines = []
    if plan["moves"]:
        months = sorted({move["to"].split("/")[0] for move in plan["moves"]})
        verb = "Filed" if applied else "Would file"
        lines.append(
            f"{verb} {len(plan['moves'])} log(s) into {len(months)} month folder(s): "
            + ", ".join(months)
        )
        for move in plan["moves"]:
            lines.append(f"  {move['from']} -> {move['to']}")
    else:
        lines.append("Nothing to file. Every log is already filed or still hot.")

    if plan["hot"]:
        lines.append(
            f"Kept hot ({len(plan['hot'])}): the current and previous month are never filed."
        )
    if plan["archived"]:
        lines.append(f"Already filed: {plan['archived']} log(s) in existing month folders.")
    if plan["unmatched"]:
        lines.append(
            f"Left in place, name does not match the log pattern ({len(plan['unmatched'])}): "
            + ", ".join(plan["unmatched"])
        )
    if plan["collisions"]:
        lines.append(
            f"SKIPPED, target already exists ({len(plan['collisions'])}): "
            + ", ".join(plan["collisions"])
        )
    if not applied and plan["moves"]:
        lines.append("")
        lines.append("Dry run. Re-run with --apply to perform these moves.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Archive session logs into YYYY-MM month folders."
    )
    parser.add_argument(
        "store", nargs="?", default=str(DEFAULT_STORE),
        help="session-log store (default: _local/_session-logs)",
    )
    parser.add_argument("--apply", action="store_true",
                        help="perform the moves (default: dry run)")
    parser.add_argument("--today", help="override today's date as YYYY-MM-DD (for testing)")
    parser.add_argument("--json", action="store_true", help="emit the plan as JSON")
    args = parser.parse_args(argv)

    store = Path(args.store)
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()

    plan = build_plan(store, today)
    if args.apply:
        apply_plan(store, plan)

    if args.json:
        print(json.dumps({**plan, "applied": args.apply}, indent=2))
    else:
        print(render(plan, args.apply))

    # A collision means a target filename already exists in its month folder.
    # Nothing was overwritten; the anomaly is worth a non-zero exit.
    return 1 if plan["collisions"] else 0


if __name__ == "__main__":
    sys.exit(main())
