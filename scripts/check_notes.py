#!/usr/bin/env python3
"""Check that every page exists in both languages with matching metadata.

- docs/**/foo.md (English) and docs/**/foo.zh.md (Chinese) must both exist.
- Both need `title` and `description`.
- Notes (every page except index.md and tags.md) also need type, tags,
  created and updated, and the two languages must agree on type, tags,
  created, updated and sources.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
TYPES = {"explanation", "how-to", "reference", "tutorial", "case-study"}
SHARED = ("type", "tags", "created", "updated", "sources")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def front_matter(path: pathlib.Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    data, key = {}, None
    for line in m.group(1).splitlines():
        if re.match(r"^\s+-\s", line) and key:
            data.setdefault(key, []).append(line.split("-", 1)[1].strip())
            continue
        k, _, v = line.partition(":")
        key, v = k.strip(), v.strip()
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
        data[key] = v if v != "" else []
    return data


def main() -> int:
    errors = []
    pages = sorted(DOCS.rglob("*.md"))
    english = {p for p in pages if not p.name.endswith(".zh.md")}
    chinese = {p for p in pages if p.name.endswith(".zh.md")}

    for zh in chinese:
        if zh.with_name(zh.name[: -len(".zh.md")] + ".md") not in english:
            errors.append(f"{zh.relative_to(ROOT)}: no English page")
    for en in sorted(english):
        rel = en.relative_to(ROOT)
        zh = en.with_name(en.stem + ".zh.md")
        if zh not in chinese:
            errors.append(f"{rel}: no Chinese page ({zh.name})")
            continue
        fe, fz = front_matter(en), front_matter(zh)
        for lang, fm in (("en", fe), ("zh", fz)):
            for k in ("title", "description"):
                if not fm.get(k):
                    errors.append(f"{rel} [{lang}]: missing {k}")
        if en.name in ("index.md", "tags.md"):
            continue
        for lang, fm in (("en", fe), ("zh", fz)):
            for k in ("type", "tags", "created", "updated"):
                if k not in fm:
                    errors.append(f"{rel} [{lang}]: missing {k}")
            if fm.get("type") and fm["type"] not in TYPES:
                errors.append(f"{rel} [{lang}]: type must be one of {sorted(TYPES)}")
            for k in ("created", "updated"):
                if fm.get(k) and not DATE.fullmatch(str(fm[k])):
                    errors.append(f"{rel} [{lang}]: {k} must be YYYY-MM-DD")
        for k in SHARED:
            if fe.get(k) != fz.get(k):
                errors.append(f"{rel}: {k} differs between languages ({fe.get(k)!r} vs {fz.get(k)!r})")

    for e in errors:
        print(e)
    print(f"{len(english)} pages checked, {len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
