# Notes for coding agents

This repository is a personal knowledge base: atomic Markdown notes under
`docs/`, built into a static site with MkDocs Material and (optionally)
deployed to GitHub Pages. You will usually be asked to **add knowledge from a
conversation** or **update an existing note**. This file is the whole
procedure; `CONTRIBUTING.md` is the human-facing version of the same rules.

## Repository map

| Path | What |
| --- | --- |
| `docs/index.md` | Site home: the table of domains. Add a row when you add a domain. |
| `docs/<domain>/index.md` | Domain entry page (MOC): groups notes, gives a reading order. |
| `docs/<domain>/<topic>/index.md` | Optional topic entry page, same role, one level down. |
| `docs/<domain>/[<topic>/]<slug>.md` | One note. |
| `docs/tags.md` | Generated tag index (`<!-- material/tags -->`). Don't edit by hand. |
| `templates/note.md` | Note template. |
| `scripts/new_note.py` | Creates a note from the template with today's date and validates the path. |
| `mkdocs.yml` | Site config. No hand-written `nav`: navigation comes from folders. |
| `requirements.txt` | Pinned build dependencies. |
| `.markdownlint-cli2.yaml` | Lint rules. |
| `.github/workflows/docs.yml` | CI: lint + `mkdocs build --strict` on every push/PR; Pages deploy only when the repo variable `PAGES_ENABLED` is `true`. |

Current domains: `linux/`, `macos/`, `ai-agents/` (topic: `sandboxing/`).

## Setup and checks

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs build --strict          # must pass: broken links/anchors fail
npx --yes markdownlint-cli2 "**/*.md"    # must pass
.venv/bin/mkdocs serve                   # optional preview at :8000
```

Run both checks before every commit. CI runs the same two.

## Adding knowledge: the procedure

1. **Split into atomic notes.** One note answers one question about one
   concept. If a draft explains two things that could each be linked to on
   their own (e.g. "seccomp" and "NoNewPrivs"), make two notes. Aim for well
   under ~150 lines per note.
2. **Search before writing.** `grep -ril "<concept>" docs/` — if a note
   exists, extend or correct it instead of creating a duplicate. Bump its
   `updated:` date.
3. **Place it.** Domain = the field the concept belongs to, not the project
   that made you learn it. Kernel mechanisms go in `linux/` even when learned
   while studying Claude Code; product behaviour goes in `ai-agents/`. Create
   a new domain only if no existing one fits; max depth is
   `docs/<domain>/<topic>/<note>.md`.
4. **Create it** with
   `python3 scripts/new_note.py docs/<domain>/<slug>.md "标题" --type explanation --tags linux,security`.
   File names: kebab-case English naming the concept (`user-namespaces.md`),
   no dates or numbers.
5. **Write it** (see conventions below).
6. **Link it.** Add it to the nearest `index.md`; link to it from related
   notes' "相关" section and link out from it. A new domain also needs its
   own `index.md` and a row in `docs/index.md`.
7. **Check and commit.** Both checks pass; one commit per logical change,
   imperative message (`Add note on Landlock`, `Update Codex sandbox for 0.170`).

## Note conventions

- Language: Chinese prose; code, commands, file names, tags in English.
- Front matter (all fields required in notes; `index.md` pages need only
  `title` and `description`):

  ```yaml
  ---
  title: seccomp
  description: One sentence: what question this note answers
  type: explanation        # explanation | how-to | reference | tutorial (Diátaxis)
  tags: [linux, security]  # lowercase English; reuse existing tags (see below)
  created: 2026-11-06
  updated: 2026-11-06
  sources:                 # authoritative URLs; may be [] for first-hand material
    - https://man7.org/linux/man-pages/man2/seccomp.2.html
  ---
  ```

- Body starts with a one- or two-sentence conclusion, then `##` sections.
  Never write a `#` heading; the title comes from front matter.
- End with `## 相关` listing related notes.
- Links: relative paths with the `.md` extension
  (`[seccomp](../../linux/seccomp.md)`). They work both on GitHub and on the
  site, and `--strict` catches breakage. No wiki links, no absolute site URLs.
- Diagrams: ` ```mermaid ` blocks. Callouts: `!!! note` / `!!! warning`.
- Tables for comparisons and options; prose for reasons.
- Version-sensitive facts (CLI flags, config keys, default behaviour) must
  name the version or date they were checked against, and cite a source.
  Prefer "checked against codex-cli 0.166.0" over unqualified claims.
- Observed output (labs) must be real. Don't invent output.

Existing tags: `linux`, `macos`, `security`, `isolation`, `privileges`,
`sandbox`, `networking`, `debugging`, `tools`, `ai-agents`, `claude-code`,
`codex`. Add a new tag only when none fits.

## Hard rules

- **No secrets or private data.** No tokens, passwords, proxy credentials,
  internal hostnames, private repo names, employer-internal details, or
  personal home paths. Use `<user>`, `example.com`, `/home/<user>`. The site
  may be public even though the repo is private.
- Don't add hand-written `nav` to `mkdocs.yml`; don't add plugins or
  dependencies without pinning them in `requirements.txt`.
- Don't edit `docs/tags.md` or the generated `site/`.
- Moving or renaming a note: update every link to it (`grep -rn "old-name.md" docs/`)
  and rebuild with `--strict`.
- Keep GitHub Actions pinned to commit SHAs (Dependabot updates them).

## Toolchain notes

- Material for MkDocs is in maintenance until its end of life on 2027-05-05;
  its successor, Zensical, reads this `mkdocs.yml` as is (checked with
  zensical 0.1.0: `zensical build --strict` passes on this repo). When
  migrating, swap the dependency and the CI build command; the notes don't
  change. Until then, keep the pinned MkDocs stack.
