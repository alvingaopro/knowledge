---
title: coding agent 如何给命令套沙箱
description: 从一个正在运行的沙箱内部，研究 Claude Code 和 Codex 怎样限制 shell 命令
type: case-study
tags: [ai-agents, claude-code, codex, sandbox, linux]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://docs.claude.com/en/docs/claude-code/sandboxing
  - https://github.com/anthropic-experimental/sandbox-runtime
  - https://github.com/openai/codex
---

**问题：**Claude Code 或 Codex 说命令“在沙箱里”运行时，究竟是什么阻止它碰到机器上的其他东西？

**简短回答：**两者都不用虚拟机。每条命令被包在内核机制里：Linux 上由 [bubblewrap](../linux/bubblewrap.md) 新建 [namespace](../linux/namespaces.md)、丢掉 [capability](../linux/capabilities.md)、打开 [NoNewPrivs](../linux/no-new-privs.md)、装上 [seccomp](../linux/seccomp.md)；macOS 上用 [Seatbelt](../macos/seatbelt.md)。网络要么经[出网代理](../ai-agents/sandboxing/egress-proxy.md)，要么关闭。正因为命令被关在里面，才可以不经审批就运行，只有越界才问人（[两道闸](../ai-agents/sandboxing/permissions-vs-sandbox.md)）。

## 背景

起因是在做一个无人值守运行 coding agent 的工具，需要决定 agent 的哪些命令要人来批准。要决定给沙箱放开什么，先得弄清沙箱本身已经做了什么。

## 研究过程

### 1. 从文档开始

厂商文档给出了模型：Claude Code 有 `sandbox.enabled`、允许的域名和可写路径（[笔记](../ai-agents/sandboxing/claude-code.md)）；Codex 有 `sandbox_mode` 和 `approval_policy`（[笔记](../ai-agents/sandboxing/codex.md)）。文档说明了**能配置什么**，没说明**怎么强制执行**。

### 2. 从内部观察一个沙箱

这次研究本身就运行在开着沙箱的 Claude Code 里，所以最省事的证据就是从里面看：`ps`、`/proc/self/ns`、`/proc/self/status`、`/proc/net/dev`、代理环境变量。每一行结果都能对应到一种机制；完整解读见[解读一个正在运行的沙箱](../ai-agents/sandboxing/lab-inspecting-a-live-sandbox.md)，通用方法见[从 /proc 观察](../linux/procfs-isolation-inspection.md)。

有两处需要内核背景才看得懂：

- namespace 编号 `4026531834`–`4026531839` 是宿主初始 namespace 的固定编号，一眼就能分出哪些是共用的、哪些是新建的。
- 笼内 PID 1 是 `apply-seccomp` 而不是 shell：过滤器先装好，之后的一切都继承它。

### 3. 查二进制，而不只是文档

很多文章说 Codex 在 Linux 上用 Landlock + seccomp。本机装的 codex-cli 0.166.0 却不是这样：对二进制跑 `strings`，能看到 bubblewrap 参数（`--unshare-net`、`--ro-bind`）、作为**回退**的 Landlock（`use_legacy_landlock`），以及托管网络配置（`network_proxy`、`allowed_domains`）。实现已经走在常见描述前面了。

### 4. 动手试，看它失败

在 Claude Code 的沙箱里运行 `codex sandbox`，报错 `bwrap: No permissions to create new namespace`。外层沙箱禁止新建 [user namespace](../linux/user-namespaces.md)，而所有基于 bubblewrap 的沙箱都依赖它。这次失败比成功更能证实机制。

## 发现

1. 两者都**只沙箱 shell 命令**。Claude Code 的文件工具、MCP server、hook 不在 OS 沙箱里。
2. Linux 上两者现在都用 bubblewrap；Claude Code 另加 socat 和按域名放行的代理，Codex 从“网络开或关”起步，正在加入代理。
3. 写入限制在工作目录和临时目录，并挖掉 agent 自己的配置，防止它给自己放权。
4. Codex 在 `workspace-write` 下保持 `.git` 只读；Claude Code 默认不这样。
5. 沙箱不是虚拟机：不限 CPU、内存，嵌套通常会失败。

并排对比见 [Claude Code 与 Codex](../ai-agents/sandboxing/claude-code-vs-codex.md)。

## 经验

- **以实际发布的东西为准。**对迭代很快的工具，二进制和 `--help` 比博客新，有时比文档还新。
- **在真实布局下测试。**git worktree 的 index 在工作目录之外，只放开工作目录的沙箱里提交会失败。只在临时目录里跑的测试（临时目录本来就可写）永远发现不了。更多见[常见的坑](../ai-agents/sandboxing/pitfalls.md)。
- **边查边脱敏。**观察时打印出的代理变量里带着有效凭据。从沙箱里复制到笔记的任何内容都要先清理。

## 没有验证的部分

- macOS：Seatbelt 的行为来自文档和源码，没有在这里实际运行。
- Codex 的 `network_proxy` / `allowed_domains`：在二进制里看到了，没有实际使用。
- 两层 seccomp 过滤器分别由哪个组件安装、具体拦截什么，没有导出来看。

## 产出的笔记

- Linux：[namespace](../linux/namespaces.md)、[user namespace](../linux/user-namespaces.md)、[capability](../linux/capabilities.md)、[NoNewPrivs](../linux/no-new-privs.md)、[seccomp](../linux/seccomp.md)、[Landlock](../linux/landlock.md)、[bubblewrap](../linux/bubblewrap.md)、[从 /proc 观察](../linux/procfs-isolation-inspection.md)
- macOS：[Seatbelt](../macos/seatbelt.md)
- Agent：[沙箱主题](../ai-agents/sandboxing/index.md)
