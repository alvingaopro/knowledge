# 贡献约定

[English](CONTRIBUTING.md) | 中文

## 原则

1. **原子化**：一条笔记只回答一个问题、只讲一个概念。超过一屏半，或者出现第二个能独立成题的概念时，拆开。
2. **链接优于重复**：需要别的概念时链接过去，不要再解释一遍。
3. **入口页负责组织**：笔记不关心自己在哪个“章节”；分组和阅读顺序写在各目录的 `index.md` 里。
4. **可验证**：写清来源；实测内容注明环境和版本。
5. **双语**：每个页面都有 `foo.md`（英文）和 `foo.zh.md`（中文），两者同步更新。

## 笔记与案例研究

| 类型 | 位置 | 内容 |
| --- | --- | --- |
| 笔记 | `docs/<领域>/[<主题>/]` | 一个概念，尽量不随时间过期 |
| 案例研究 | `docs/case-studies/` | 一次研究：问题、方法、发现、未验证的部分、产出的笔记 |

案例研究链接到笔记；可复用的解释写进笔记，不写在案例里。

## 目录与命名

- 一级目录是**领域**（`linux/`、`macos/`、`ai-agents/`……），可以再有一级主题（`ai-agents/sandboxing/`），不再更深。
- 新目录要同时建 `index.md` 和 `index.zh.md` 作为入口页。
- 文件名用英文 kebab-case，表达概念本身：`seccomp.md`、`user-namespaces.md`。不带日期、序号。
- 移动或改名后运行检查，确认没有断链。

## Front matter

用脚本创建笔记，日期和路径检查会自动完成：

```sh
python3 scripts/new_note.py docs/linux/landlock.md "Landlock" "Landlock" --type explanation --tags linux,security
```

`type`、`tags`、`created`、`updated`、`sources` 两种语言必须一致。`type` 沿用 [Diátaxis](https://diataxis.fr/) 的四类，另加案例研究：

| type | 回答的问题 | 写法 |
| --- | --- | --- |
| `explanation` | 为什么、是什么 | 讲原理和取舍 |
| `how-to` | 怎么做到某件事 | 面向目标的步骤 |
| `reference` | 有哪些选项 | 表格、清单 |
| `tutorial` | 跟着做一遍来学会 | 可复现的实验 |
| `case-study` | 这是怎么研究出来的 | 一次研究的叙述 |

## 写作

- 正文从 `##` 开始，标题来自 front matter。
- 链接用相对路径并带 `.md`：`[seccomp](../linux/seccomp.md)`。两种语言都链接英文文件名，站点会自动换成读者所用语言的页面。
- 提示用 `!!! note` / `!!! warning`，图用 Mermaid。
- 不写密码、token、代理凭据、内网地址、个人路径；用 `<user>`、`example.com` 代替。

## 检查

```sh
python3 scripts/check_notes.py
.venv/bin/mkdocs build --strict
npx markdownlint-cli2 "**/*.md"
```

CI 跑同样的检查。
