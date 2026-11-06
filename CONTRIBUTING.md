# Contributing

English | [中文](CONTRIBUTING.zh.md)

## Principles

1. **Atomic.** A note answers one question about one concept. When a note passes about a screen and a half, or a second concept could stand on its own, split it.
2. **Link, don't repeat.** When a note needs another concept, link to it instead of explaining it again.
3. **Entry pages organise.** Notes don't know which "chapter" they're in; grouping and reading order live in each folder's `index.md`.
4. **Verifiable.** Cite sources; for observed output, say which environment and version it came from.
5. **Bilingual.** Every page exists as `foo.md` (English) and `foo.zh.md` (Chinese), kept in step.

## Notes and case studies

| Kind | Where | What |
| --- | --- | --- |
| Note | `docs/<domain>/[<topic>/]` | One concept, timeless as far as possible |
| Case study | `docs/case-studies/` | One investigation: question, method, findings, what's unverified, notes produced |

A case study links to notes; any reusable explanation goes into a note, not the case study.

## Folders and names

- Top-level folders are **domains** (`linux/`, `macos/`, `ai-agents/` …), optionally with one topic level (`ai-agents/sandboxing/`). No deeper.
- A new folder gets `index.md` and `index.zh.md` as its entry pages.
- File names are kebab-case English naming the concept: `seccomp.md`, `user-namespaces.md`. No dates or numbers.
- After moving or renaming, run the checks to catch broken links.

## Front matter

Create notes with the script, which fills dates and checks the path:

```sh
python3 scripts/new_note.py docs/linux/landlock.md "Landlock" "Landlock" --type explanation --tags linux,security
```

```yaml
---
title: seccomp
description: One sentence on the question this note answers
type: explanation
tags: [linux, security]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://man7.org/linux/man-pages/man2/seccomp.2.html
---
```

`type`, `tags`, `created`, `updated` and `sources` must match between the two languages. `type` follows [Diátaxis](https://diataxis.fr/), plus case studies:

| type | Answers | Style |
| --- | --- | --- |
| `explanation` | Why, what | Principles and trade-offs |
| `how-to` | How do I achieve X | Steps toward a goal |
| `reference` | What options exist | Tables and lists |
| `tutorial` | Learn by doing it once | Reproducible experiment |
| `case-study` | How was this researched | Narrative of one investigation |

## Writing

- Body starts at `##`; the title comes from front matter.
- Links are relative with `.md`: `[seccomp](../linux/seccomp.md)`. Link to the English file name from both languages; the site resolves it to the reader's language.
- Callouts: `!!! note` / `!!! warning`. Diagrams: Mermaid.
- No passwords, tokens, proxy credentials, internal hostnames or personal paths; use `<user>`, `example.com`.

## Checks

```sh
python3 scripts/check_notes.py
.venv/bin/mkdocs build --strict
npx markdownlint-cli2 "**/*.md"
```

CI runs the same checks.
