# Knowledge

个人技术知识库：一条笔记只讲一个概念，用链接把它们连起来。源文件是 `docs/` 下的 Markdown，在 GitHub 上可以直接读，也能用 [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) 构建成静态站点，发布到 GitHub Pages。

## 目录

| 路径 | 内容 |
| --- | --- |
| `docs/<领域>/` | 按领域分的笔记，例如 `linux/`、`macos/`、`ai-agents/` |
| `docs/<领域>/index.md` | 该领域的入口（MOC，Map of Content）：列出笔记和建议的阅读顺序 |
| `docs/tags.md` | 自动生成的标签索引 |
| `templates/note.md` | 新笔记模板 |
| `CONTRIBUTING.md` | 写作与组织约定（新增笔记前先读） |

## 本地预览

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve          # http://127.0.0.1:8000
.venv/bin/mkdocs build --strict # 与 CI 相同：坏链接、坏锚点都会失败
```

## 发布到 GitHub Pages

`.github/workflows/docs.yml` 在每次推送和 PR 上都会检查 Markdown 并严格构建站点。部署这一步默认关闭，打开方法：

1. 仓库 Settings → Pages → Source 选 **GitHub Actions**
2. Settings → Secrets and variables → Actions → Variables，新建 `PAGES_ENABLED` = `true`

注意：私有仓库使用 Pages 需要付费账户，并且发布出去的站点是公开的。
