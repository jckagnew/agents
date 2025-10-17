#!/usr/bin/env python3
"""
add_future_upgrade.py

Usage:
  python scripts/add_future_upgrade.py \
      --name "Claude Skills" \
      --status "Keep Watching" \
      --summary "Claude Code feature for template-driven SOP execution" \
      --triggers "Revisit if >1 collaborator adopts Claude Code or Anthropic exposes Skills via API" \
      --owner "Jack" \
      --notes "Research Anthropic skill examples before piloting"

The script maintains docs/potential-factory-upgrades.md as a markdown table.
Existing entries are updated in place; new entries are appended.
"""

import argparse
import datetime as dt
import csv
import io
from pathlib import Path
from textwrap import dedent

FACTORY_DOC = Path("docs/potential-factory-upgrades.md")
STATUS_CHOICES = [
    "Keep Watching",
    "Prototype",
    "Adopt",
    "Parked",
]

HEADER = dedent(
    """\
    # Potential Future Upgrades

    We track emerging tools and capabilities here without immediately committing build time.
    Review this list during monthly factory planning or whenever a customer/project need changes.

    | Name | Status | Summary | Trigger Conditions | Owner | Last Reviewed | Notes |
    |------|--------|---------|-------------------|-------|---------------|-------|
    """
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add or update a potential factory upgrade entry.")
    parser.add_argument("--name", required=True, help="Name of the capability/tool (e.g., 'Claude Skills').")
    parser.add_argument(
        "--status",
        required=True,
        choices=STATUS_CHOICES,
        help="Tracking status (e.g., 'Keep Watching').",
    )
    parser.add_argument("--summary", required=True, help="One-line description of the capability.")
    parser.add_argument(
        "--triggers",
        default="Define trigger conditions before next review.",
        help="Conditions that would move this item forward (default: generic reminder).",
    )
    parser.add_argument(
        "--owner",
        default="Unassigned",
        help="Person responsible for monitoring the item (default: Unassigned).",
    )
    parser.add_argument(
        "--notes",
        default="",
        help="Optional extra context or links.",
    )
    return parser.parse_args()


def ensure_doc() -> None:
    FACTORY_DOC.parent.mkdir(parents=True, exist_ok=True)
    if not FACTORY_DOC.exists():
        FACTORY_DOC.write_text(HEADER)


def load_entries():
    ensure_doc()
    lines = FACTORY_DOC.read_text().splitlines()
    table_rows = []
    for line in lines:
        if line.startswith("|") and not line.startswith("|------"):
            table_rows.append(line)
    # Skip header row if present
    if table_rows and table_rows[0].startswith("| Name"):
        table_rows = table_rows[1:]

    entries = {}
    order = []
    for row in table_rows:
        row_buffer = io.StringIO(row.strip("| \n"))
        reader = csv.reader([row_buffer.getvalue()], delimiter="|")
        cells = next(reader)
        cells = [cell.strip() for cell in cells]
        if len(cells) < 7:
            # Pad missing cells for older entries
            cells += [""] * (7 - len(cells))
        name, status, summary, triggers, owner, last_reviewed, notes = cells[:7]
        entries[name.lower()] = {
            "Name": name,
            "Status": status,
            "Summary": summary,
            "Trigger Conditions": triggers,
            "Owner": owner,
            "Last Reviewed": last_reviewed,
            "Notes": notes,
        }
        order.append(name.lower())
    return entries, order


def save_entries(entries, order):
    # Rebuild the markdown file
    rows = []
    for key in order:
        entry = entries[key]
        rows.append(
            "| {Name} | {Status} | {Summary} | {Trigger Conditions} | "
            "{Owner} | {Last Reviewed} | {Notes} |".format(**entry)
        )
    doc_body = HEADER + "\n".join(rows) + "\n"
    FACTORY_DOC.write_text(doc_body)


def main():
    args = parse_args()
    entries, order = load_entries()

    today = dt.date.today().isoformat()
    name_key = args.name.lower()

    new_entry = {
        "Name": args.name,
        "Status": args.status,
        "Summary": args.summary,
        "Trigger Conditions": args.triggers,
        "Owner": args.owner,
        "Last Reviewed": today,
        "Notes": args.notes,
    }

    if name_key in entries:
        entries[name_key].update(new_entry)
        # keep existing order
    else:
        entries[name_key] = new_entry
        order.append(name_key)

    save_entries(entries, order)
    print(f"✅ Recorded upgrade '{args.name}' with status '{args.status}'.")


if __name__ == "__main__":
    main()
