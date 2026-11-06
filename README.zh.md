# Knowledge

[English](README.md) | 中文

个人技术知识库：一条笔记只讲一个概念，笔记之间互相链接；案例研究记录一个主题是怎么研究出来的。每个页面都有英文和中文两个版本。

**站点：**<https://alvingaopro.github.io/knowledge/>（按浏览器语言打开对应版本，也可以用语言菜单切换）

## 目录

| 路径 | 内容 |
| --- | --- |
| `docs/<领域>/` | 按领域分的笔记，例如 `linux/`、`macos/`、`ai-agents/` |
| `docs/<领域>/index.md` | 该领域的入口页：列出笔记和阅读顺序 |
| `docs/case-studies/` | 完整研究过程的记录，链接到研究中产生的笔记 |
| `docs/**/foo.md`、`foo.zh.md` | 每个页面的英文版和中文版 |
| `templates/` | 两种语言的笔记模板 |
| `scripts/new_note.py` | 按模板同时创建中英文笔记 |
| `scripts/check_notes.py` | 检查两种语言都存在且元数据一致 |
| `CONTRIBUTING.zh.md` | 写作与组织约定 |
| `AGENTS.md` | 给更新本仓库的 coding agent 的说明 |

## 从这里开始读

- [coding agent 沙箱](docs/ai-agents/sandboxing/index.zh.md)
- [案例研究：coding agent 如何给命令套沙箱](docs/case-studies/coding-agent-sandboxes.zh.md)

## 本地预览

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve                 # http://127.0.0.1:8000/knowledge/
python3 scripts/check_notes.py         # 两种语言都在且一致
.venv/bin/mkdocs build --strict        # 坏链接、坏锚点会让构建失败
npx markdownlint-cli2 "**/*.md"
```

## 发布

`.github/workflows/docs.yml` 在每次推送和 PR 上运行检查；当仓库变量 `PAGES_ENABLED` 为 `true`、且 Pages 来源设为 GitHub Actions 时，从 `main` 部署到 GitHub Pages。
