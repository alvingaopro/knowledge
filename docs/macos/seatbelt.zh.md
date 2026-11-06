---
title: Seatbelt
description: macOS 用 SBPL 规则文件限制进程访问文件、网络和系统服务的沙箱机制
type: explanation
tags: [macos, security, sandbox]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://github.com/anthropic-experimental/sandbox-runtime
  - https://github.com/openai/codex
---

Seatbelt 是 macOS 内核里的沙箱机制，App Sandbox 就建立在它上面。命令行用 `/usr/bin/sandbox-exec -p <规则> <命令>` 让一个命令在指定规则下运行。

## 规则长什么样

规则语言叫 SBPL（Sandbox Profile Language），是 Scheme 风格的 S 表达式：

```scheme
(version 1)
(deny default)                                   ; 默认全部拒绝
(allow process-exec process-fork)
(allow file-read*)                               ; 允许读
(allow file-write* (subpath "/Users/me/project")); 只允许写项目目录
(allow network-outbound (remote ip "localhost:3128")) ; 只能连本机代理
```

规则按操作类型（`file-read*`、`file-write*`、`network-outbound`、`mach-lookup` 等）和过滤条件（`subpath`、`literal`、`regex`、`remote ip`）组合。

## 和 Linux 方案的对应

| Linux | macOS |
| --- | --- |
| [mount namespace](../linux/namespaces.md) 重拼文件树 | `file-read*` / `file-write*` 路径规则 |
| net namespace + [出网代理](../ai-agents/sandboxing/egress-proxy.md) | 只允许 `network-outbound` 到本机代理端口 |
| [seccomp](../linux/seccomp.md) | 按操作类型拒绝，如 `mach-lookup` |

区别在于 Seatbelt 不隔离“看到什么”：沙箱里的进程仍能看到其他进程，只是规则禁止的操作会失败。

## 现状

`sandbox-exec` 在手册里早已标为弃用，但至今仍随系统提供并被广泛使用，Claude Code 和 Codex 的 macOS 沙箱都依赖它。

## 相关

- [Claude Code 的沙箱](../ai-agents/sandboxing/claude-code.md)
- [Codex 的沙箱](../ai-agents/sandboxing/codex.md)
