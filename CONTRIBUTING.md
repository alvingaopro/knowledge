# 写作与组织约定

## 原则

1. **原子化**：一条笔记只回答一个问题、只讲一个概念。超过一屏半、或者出现第二个可以独立成题的概念时，拆开。
2. **链接优于重复**：需要用到别的概念时，链接过去，不要再解释一遍。
3. **入口页（MOC）负责组织**：笔记本身不关心自己在哪个“章节”；阅读顺序、主题分组写在 `index.md` 里。
4. **可验证**：写清来源（`sources`），实测类内容注明环境和版本，避免过期知识被当成现状。

## 目录与命名

- 一级目录是**领域**（`linux/`、`macos/`、`ai-agents/`……），领域下可以再按主题建一级子目录（如 `ai-agents/sandboxing/`）。不要超过三级。
- 新建目录时同时建 `index.md` 作为入口页。
- 文件名用英文 kebab-case，表达概念本身：`seccomp.md`、`user-namespaces.md`。不要带日期、序号。
- 移动或改名文件后，运行 `mkdocs build --strict` 确认没有断链。

## Front matter

每条笔记都以下面的元数据开头。用脚本从模板创建，日期和路径检查都会自动完成：

```sh
python3 scripts/new_note.py docs/linux/landlock.md "Landlock" --type explanation --tags linux,security
```

元数据格式：

```yaml
---
title: seccomp                     # 页面标题
description: 一句话说明这条笔记回答什么   # 用于搜索结果和链接预览
type: explanation                  # 见下表
tags: [linux, security]            # 小写英文，复用已有标签
created: 2026-11-06
updated: 2026-11-06
sources:                           # 可选：权威出处
  - https://man7.org/linux/man-pages/man2/seccomp.2.html
---
```

`type` 借用 [Diátaxis](https://diataxis.fr/) 的四类，帮助判断一条笔记该怎么写：

| type | 回答的问题 | 写法 |
| --- | --- | --- |
| `explanation` | 为什么、是什么 | 讲原理和取舍 |
| `how-to` | 怎么做到某件事 | 步骤，目标明确 |
| `reference` | 有哪些选项、参数 | 表格、清单，少叙述 |
| `tutorial` | 跟着做一遍来学会 | 可复现的实验 |

## 写作

- 正文从 H2（`##`）开始，H1 由 `title` 生成。
- 链接用相对路径并带 `.md`：`[seccomp](../linux/seccomp.md)`。这样在 GitHub 和站点上都能跳转。
- 提示、警告用 admonition：`!!! note` / `!!! warning`。
- 图优先用 Mermaid（` ```mermaid `），不要提交截图形式的图表。
- 不要写入密码、token、代理凭据、内网地址、个人主目录路径；用 `<user>`、`example.com` 代替。

## 提交前检查

```sh
.venv/bin/mkdocs build --strict
npx markdownlint-cli2 "**/*.md"
```

CI 会跑同样的检查。
