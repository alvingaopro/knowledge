#!/usr/bin/env python3
"""Create a note from templates/note.md.

Usage: python3 scripts/new_note.py docs/<domain>/[<topic>/]<slug>.md "标题" [--type explanation] [--tags a,b]
"""
import argparse
import datetime
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TYPES = ("explanation", "how-to", "reference", "tutorial")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("path", help="docs/<domain>/[<topic>/]<slug>.md")
    p.add_argument("title")
    p.add_argument("--type", default="explanation", choices=TYPES)
    p.add_argument("--tags", default="", help="comma-separated, lowercase")
    a = p.parse_args()

    path = (ROOT / a.path).resolve()
    rel = path.relative_to(ROOT).as_posix()
    if not rel.startswith("docs/") or path.suffix != ".md":
        sys.exit("path must be docs/.../<slug>.md")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", path.stem):
        sys.exit("file name must be kebab-case English, e.g. user-namespaces.md")
    if len(path.relative_to(ROOT / "docs").parts) > 3:
        sys.exit("at most docs/<domain>/<topic>/<note>.md")
    if path.exists():
        sys.exit(f"{rel} already exists")

    today = datetime.date.today().isoformat()
    tags = [t.strip() for t in a.tags.split(",") if t.strip()]
    text = (ROOT / "templates/note.md").read_text(encoding="utf-8")
    text = text.replace("title: 概念名", f"title: {a.title}")
    text = text.replace("type: explanation", f"type: {a.type}")
    text = text.replace("tags: []", f"tags: [{', '.join(tags)}]")
    text = text.replace("YYYY-MM-DD", today)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"created {rel}")
    if not (path.parent / "index.md").exists():
        print(f"note: {path.parent.relative_to(ROOT).as_posix()}/index.md does not exist yet; create it as the section's entry page")
    else:
        print(f"next: link it from {path.parent.relative_to(ROOT).as_posix()}/index.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
