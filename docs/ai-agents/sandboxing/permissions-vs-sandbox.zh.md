---
title: 权限审批与 OS 沙箱
description: agent 的工具调用要过的两道检查，各自管什么、为什么需要两道
type: explanation
tags: [ai-agents, sandbox, security]
created: 2026-11-06
updated: 2026-11-06
---

agent 的一个工具调用从模型发出到真正执行，要过两道检查：应用层的**权限审批**看命令写了什么，内核层的 **OS 沙箱**看进程实际做了什么。

## 两道闸

```mermaid
flowchart LR
  M["模型<br/>Bash('rm -rf build')"] --> P["权限 / 审批<br/>读命令文本"]
  P -->|放行| S["OS 沙箱<br/>检查实际的系统调用"]
  S --> K["内核执行"]
```

| | 权限审批 | OS 沙箱 |
| --- | --- | --- |
| 位置 | agent 程序内部 | 操作系统内核 |
| 依据 | 命令文本、工具名、规则列表、hook | 进程发起的系统调用 |
| 弱点 | 命令可以换着花样写来绕过；看不懂就只能问人，打断频繁 | 只覆盖它包住的进程；配置过宽就形同虚设 |
| Claude Code | permissions（allow/deny 规则、hook） | sandbox（[bubblewrap](../../linux/bubblewrap.md) / [Seatbelt](../../macos/seatbelt.md)） |
| Codex | `approval_policy` | `sandbox_mode` |

## 为什么两道都要

只有审批：每条不认识的命令都要问人，用户很快就会无脑点“允许”。

有了沙箱：既然命令最多只能改工作目录、只能连白名单主机，笼子内的命令就可以自动放行，只对越界的事审批。这是两家产品共同的思路：**先隔离，再只对越界的事审批**。

## 沙箱不包什么

沙箱只包 shell 命令及其子进程。以 Claude Code 为例，Read / Edit / WebFetch 等内置工具、MCP server、hook 都不在 OS 沙箱里，仍然只靠权限规则。

## 相关

- [Claude Code 的沙箱](claude-code.md)
- [Codex 的沙箱](codex.md)
