# Knowledge

English | [中文](README.zh.md)

A personal technical knowledge base: one concept per note, notes linked to each other, and case studies that tell how a topic was researched. Every page exists in English and Chinese.

**Site:** <https://alvingaopro.github.io/knowledge/> (opens in your browser's language; switch with the language menu)

## Layout

| Path | Contents |
| --- | --- |
| `docs/<domain>/` | Notes by domain, e.g. `linux/`, `macos/`, `ai-agents/` |
| `docs/<domain>/index.md` | The domain's entry page: lists its notes and a reading order |
| `docs/case-studies/` | Write-ups of whole investigations, linking to the notes they produced |
| `docs/**/foo.md`, `foo.zh.md` | Each page in English and in Chinese |
| `templates/` | Note templates in both languages |
| `scripts/new_note.py` | Creates a note in both languages from the templates |
| `scripts/check_notes.py` | Checks both languages exist and their metadata agree |
| `CONTRIBUTING.md` | Writing and organisation conventions |
| `AGENTS.md` | Instructions for coding agents that update this repository |

## Start reading

- [Coding agent sandboxes](docs/ai-agents/sandboxing/index.md)
- [Case study: how coding agents sandbox their commands](docs/case-studies/coding-agent-sandboxes.md)

## Local preview

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve                 # http://127.0.0.1:8000/knowledge/
python3 scripts/check_notes.py         # both languages present and consistent
.venv/bin/mkdocs build --strict        # broken links or anchors fail the build
npx markdownlint-cli2 "**/*.md"
```

## Publishing

`.github/workflows/docs.yml` runs the checks on every push and pull request, and deploys to GitHub Pages from `main` when the repository variable `PAGES_ENABLED` is `true` and Pages' source is set to GitHub Actions.
