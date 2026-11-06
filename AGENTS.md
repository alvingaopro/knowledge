# Notes for coding agents

This repository is a public, bilingual (English/Chinese) knowledge base:
atomic Markdown notes and case studies under `docs/`, built with MkDocs
Material + `mkdocs-static-i18n` and deployed to GitHub Pages at
<https://alvingaopro.github.io/knowledge/>. You will usually be asked to
**add knowledge from a conversation**, **write up an investigation as a case
study**, or **update an existing note**. This file is the whole procedure;
`CONTRIBUTING.md` / `CONTRIBUTING.zh.md` are the human-facing version.

## Repository map

| Path | What |
| --- | --- |
| `docs/index.md` / `index.zh.md` | Site home: domains table and case-study pointer. Add a row for a new domain. |
| `docs/<domain>/index[.zh].md` | Domain entry page (MOC): groups notes, gives a reading order. |
| `docs/<domain>/<topic>/index[.zh].md` | Optional topic entry page, one level down. |
| `docs/<domain>/[<topic>/]<slug>[.zh].md` | One note, in English (`.md`) and Chinese (`.zh.md`). |
| `docs/case-studies/index[.zh].md` | Table of case studies, newest first. |
| `docs/case-studies/<slug>[.zh].md` | One case study. |
| `docs/tags[.zh].md` | Generated tag index (`<!-- material/tags -->`). Don't edit. |
| `templates/note[.zh].md` | Note templates. |
| `scripts/new_note.py` | Creates both language files with today's date; validates the path. |
| `scripts/check_notes.py` | Fails if a page lacks its other language, or metadata differ. |
| `overrides/main.html` | Picks the language from the browser on arrival; a choice made in the language menu is remembered (`localStorage` key `knowledge.lang`). |
| `mkdocs.yml` | Site config. No hand-written `nav`: navigation comes from folders. |
| `requirements.txt` | Pinned build dependencies. |
| `.markdownlint-cli2.yaml` | Lint rules. |
| `.github/workflows/docs.yml` | CI: lint, `check_notes.py`, `mkdocs build --strict`; deploys `main` to Pages when the repo variable `PAGES_ENABLED` is `true`. |

Current domains: `linux/`, `macos/`, `ai-agents/` (topic `sandboxing/`).
Case studies: `coding-agent-sandboxes`.

## Setup and checks

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
python3 scripts/check_notes.py           # both languages, matching metadata
.venv/bin/mkdocs build --strict          # broken links/anchors fail
npx --yes markdownlint-cli2 "**/*.md"
.venv/bin/mkdocs serve                   # preview at http://127.0.0.1:8000/knowledge/
```

All three checks must pass before every commit. CI runs the same.

## Adding knowledge

1. **Split into atomic notes.** One note answers one question about one
   concept. If a draft explains two things that could each be linked to on
   their own (e.g. "seccomp" and "NoNewPrivs"), make two notes. Keep notes
   well under ~150 lines.
2. **Search first.** `grep -ril "<concept>" docs/`. If a note exists, extend
   or correct it (both languages) and bump `updated:` in both.
3. **Place it.** Domain = the field the concept belongs to, not the project
   that prompted it. Kernel mechanisms go in `linux/` even when learned while
   studying Claude Code; product behaviour goes in `ai-agents/`. New domain
   only if none fits; max depth `docs/<domain>/<topic>/<note>.md`.
4. **Create it:**
   `python3 scripts/new_note.py docs/<domain>/<slug>.md "English title" "中文标题" --type explanation --tags linux,security`.
   File names are kebab-case English naming the concept, no dates/numbers.
5. **Write both languages** (conventions below). Write the content once,
   carefully, then translate; the two must say the same thing. Don't leave
   one language as a stub.
6. **Link it.** Add it to the nearest `index.md` **and** `index.zh.md`; add
   it to related notes' "Related / 相关" sections in both languages. A new
   domain also needs both index files and a row in both home pages.
7. **Check and commit.** One commit per logical change, imperative message
   (`Add note on Landlock`, `Update Codex sandbox for 0.170`).

## Writing a case study

Use one when the user asks to record *how* something was researched, not just
the result.

- `type: case-study`, file `docs/case-studies/<slug>.md` + `.zh.md`
  (`new_note.py ... --type case-study`).
- Sections: question and short answer; context (generic: no employer,
  product or private-repo names); how it was researched, step by step,
  including dead ends and failures that taught something; findings; lessons;
  **not verified**; notes produced.
- Every reusable explanation goes into an atomic note, which the case study
  links to. Create or update those notes in the same change.
- Add a row to `docs/case-studies/index.md` and `index.zh.md`, newest first.

## Conventions

- Front matter, identical in both languages except `title` and
  `description` (index pages need only those two):

  ```yaml
  ---
  title: seccomp
  description: One sentence on what question this page answers
  type: explanation   # explanation | how-to | reference | tutorial | case-study
  tags: [linux, security]
  created: 2026-11-06
  updated: 2026-11-06
  sources:
    - https://man7.org/linux/man-pages/man2/seccomp.2.html
  ---
  ```

- Start with a one- or two-sentence conclusion, then `##` sections. Never a
  `#` heading. End notes with `## Related` / `## 相关`.
- Links: relative, with `.md`, always to the **English** file name, also
  from Chinese pages (`[seccomp](../linux/seccomp.md)`); the i18n plugin
  points it at the reader's language. No wiki links, no absolute site URLs.
- Chinese pages: Chinese prose; code, commands, file names and tags stay
  English. English pages: plain, direct English.
- Mermaid for diagrams; `!!! note` / `!!! warning` for callouts; tables for
  options and comparisons, prose for reasons.
- Version-sensitive facts (flags, config keys, defaults) name the version or
  date checked and cite a source ("checked against codex-cli 0.166.0").
- Observed output must be real; never invent it.

Existing tags: `linux`, `macos`, `security`, `isolation`, `privileges`,
`sandbox`, `networking`, `debugging`, `tools`, `ai-agents`, `claude-code`,
`codex`. Add a new one only when none fits.

## Hard rules

- **The repository and site are public.** No tokens, passwords, proxy
  credentials, internal hostnames, private repository or employer names,
  internal decision numbers, or personal home paths. Use `<user>`,
  `example.com`, `/home/<user>`. Scan before committing:
  `grep -rnE '/home/[a-z]|token|passw|secret' docs/`.
- Don't add `nav` to `mkdocs.yml`; pin any new dependency in
  `requirements.txt`; keep GitHub Actions pinned to commit SHAs (Dependabot
  updates them).
- Don't enable `navigation.instant`: it breaks the language menu's links to
  the same page in the other language.
- Don't edit `docs/tags*.md` or the generated `site/`.
- Moving or renaming: move both language files, update every link
  (`grep -rn "old-name.md" docs/`), rerun the checks.

## Toolchain notes

- Material for MkDocs is maintained until 2027-05-05; its successor Zensical
  reads `mkdocs.yml` (`zensical build --strict` passed on this repo before
  i18n was added, with zensical 0.1.0). Migration is blocked until Zensical
  supports a bilingual setup equivalent to `mkdocs-static-i18n`; re-check
  then. The notes themselves won't need to change.
