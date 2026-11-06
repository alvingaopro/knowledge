---
title: Landlock
description: 让普通进程自己按路径限制能访问的文件和端口的 Linux 安全模块
type: explanation
tags: [linux, security, sandbox]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://docs.kernel.org/userspace-api/landlock.html
---

Landlock 是 Linux 5.13 起加入的安全模块：普通进程不需要 root，就能给自己和子进程声明“只能访问这些路径”。

## 和其他机制的区别

| 机制 | 按什么限制 | 需要特权吗 |
| --- | --- | --- |
| [mount namespace](namespaces.md) | 重新拼一棵文件树 | 需要 [user namespace](user-namespaces.md) |
| [seccomp](seccomp.md) | 系统调用编号和数值参数，不能看路径 | 不需要（配合 NoNewPrivs） |
| Landlock | 文件路径层级；新版本还能限制 TCP 端口 | 不需要 |
| SELinux / AppArmor | 管理员写的全局策略 | 需要 root 配置 |

Landlock 的优点是不用建 namespace，在禁止 user namespace 的环境里也能用；缺点是能力随内核版本（ABI 版本）逐步增加，旧内核上可能只能部分生效。

## 怎么用

三个系统调用：`landlock_create_ruleset` 声明要管哪些操作，`landlock_add_rule` 为路径添加允许规则，`landlock_restrict_self` 生效。生效后不可撤销，并遗传给子进程。

## 在 agent 沙箱里的用途

Codex 的 Linux 沙箱早期用 Landlock + [seccomp](seccomp.md) 实现；新版本改为默认 [bubblewrap](bubblewrap.md)，Landlock 保留为回退。见 [Codex 的沙箱](../ai-agents/sandboxing/codex.md)。

## 相关

- [seccomp](seccomp.md)
- [bubblewrap](bubblewrap.md)
