---
title: Claude Code 与 Codex 沙箱对比
description: 两家 coding agent 沙箱在机制、默认边界、网络和审批上的异同
type: reference
tags: [ai-agents, claude-code, codex, sandbox]
created: 2026-11-06
updated: 2026-11-06
---

| | [Claude Code](claude-code.md) | [Codex](codex.md) |
| --- | --- | --- |
| 包住什么 | Bash 工具的命令；文件工具走权限规则 | agent 执行的命令；补丁写入按 writable roots 检查 |
| Linux | bubblewrap + seccomp + socat | bubblewrap + seccomp（旧版 Landlock） |
| macOS | Seatbelt（动态生成规则） | Seatbelt（内置基础规则） |
| 读 | 默认全可读，按名单拒绝 | 默认全可读 |
| 写 | 工作目录 + 临时目录，可增减 | 按模式；`workspace-write` 下 `.git` 只读 |
| 网络 | 只经[代理](egress-proxy.md)，域名白名单 | 默认全关，开关式；新版加入代理白名单 |
| 免确认 | `autoAllowBashIfSandboxed` | `approval_policy = "on-request"` |
| 跳出沙箱 | `dangerouslyDisableSandbox`、`excludedCommands` | 提权请求、`danger-full-access`、`--yolo` |
| 开源实现 | `anthropic-experimental/sandbox-runtime` | `openai/codex` 的 `codex-rs` |

## 共同点

- 都不是虚拟机，不限制 CPU、内存。
- 都是“先隔离，再只对越界的事审批”，见[两道闸](permissions-vs-sandbox.md)。
- Linux 上都依赖非特权 [user namespace](../../linux/user-namespaces.md)。

## 主要差别

- **网络**：Claude Code 从一开始就是“没有网卡 + 代理白名单”；Codex 以“开或关”起步。
- **`.git`**：Codex 的 `workspace-write` 默认把 `.git` 设为只读，agent 不能自己提交；Claude Code 默认可写工作目录里的 `.git`。
- **审批粒度**：Claude Code 的审批规则按工具和命令模式写；Codex 用一个策略枚举控制整体行为。
