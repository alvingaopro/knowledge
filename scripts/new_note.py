#!/usr/bin/env python3
"""Create a note in both languages from templates/note.md and templates/note.zh.md.

Usage:
  python3 scripts/new_note.py docs/<domain>/[<topic>/]<slug>.md "English title" "中文标题" \
      [--type explanation] [--tags a,b]

Writes <slug>.md (English) and <slug>.zh.md (Chinese).
"""
import argparse
import datetime
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TYPES = ("explanation", "how-to", "reference", "tutorial", "case-study")


def render(template: str, title: str, placeholder: str, kind: str, tags: list, today: str) -> str:
    text = (ROOT / "templates" / template).read_text(encoding="utf-8")
    text = text.replace(f"title: {placeholder}", f"title: {title}")
    text = text.replace("type: explanation", f"type: {kind}")
    text = text.replace("tags: []", f"tags: [{', '.join(tags)}]")
    return text.replace("YYYY-MM-DD", today)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("path", help="docs/<domain>/[<topic>/]<slug>.md")
    p.add_argument("title_en")
    p.add_argument("title_zh")
    p.add_argument("--type", default="explanation", choices=TYPES)
    p.add_argument("--tags", default="", help="comma-separated, lowercase English")
    a = p.parse_args()

    en = (ROOT / a.path).resolve()
    rel = en.relative_to(ROOT).as_posix()
    if not rel.startswith("docs/") or en.suffix != ".md" or en.name.endswith(".zh.md"):
        sys.exit("path must be docs/.../<slug>.md (the English file)")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", en.stem):
        sys.exit("file name must be kebab-case English, e.g. user-namespaces.md")
    if len(en.relative_to(ROOT / "docs").parts) > 3:
        sys.exit("at most docs/<domain>/<topic>/<note>.md")
    zh = en.with_name(en.stem + ".zh.md")
    for f in (en, zh):
        if f.exists():
            sys.exit(f"{f.relative_to(ROOT)} already exists")

    today = datetime.date.today().isoformat()
    tags = [t.strip() for t in a.tags.split(",") if t.strip()]
    en.parent.mkdir(parents=True, exist_ok=True)
    en.write_text(render("note.md", a.title_en, "Concept name", a.type, tags, today), encoding="utf-8")
    zh.write_text(render("note.zh.md", a.title_zh, "概念名", a.type, tags, today), encoding="utf-8")
    print(f"created {rel}\ncreated {zh.relative_to(ROOT).as_posix()}")
    index = en.parent / "index.md"
    where = en.parent.relative_to(ROOT).as_posix()
    if index.exists():
        print(f"next: link it from {where}/index.md and {where}/index.zh.md")
    else:
        print(f"note: {where}/index.md and index.zh.md don't exist yet; create them as the section's entry pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
