---
title: Coding agent 沙箱
description: Claude Code 和 Codex 沙箱的学习入口与阅读顺序
---

Claude Code 和 Codex 都不在虚拟机里跑。它们只给 agent 执行的 **shell 命令**套一层由操作系统内核强制执行的限制：能写哪里、能读哪里、能连哪里。限制以内的命令自动放行，越界才问人。

## 阅读顺序

1. [权限审批与 OS 沙箱：两道闸](permissions-vs-sandbox.md)：先分清两层各管什么
2. Linux 基础：[namespace](../../linux/namespaces.md)、[user namespace](../../linux/user-namespaces.md)、[capability](../../linux/capabilities.md)、[NoNewPrivs](../../linux/no-new-privs.md)、[seccomp](../../linux/seccomp.md)、[bubblewrap](../../linux/bubblewrap.md)；macOS 看 [Seatbelt](../../macos/seatbelt.md)
3. [出网代理](egress-proxy.md)：没有网卡的沙箱怎么按域名访问网络
4. [Claude Code 的沙箱](claude-code.md)
5. [Codex 的沙箱](codex.md)
6. [Claude Code 与 Codex 对比](claude-code-vs-codex.md)
7. [解读一个正在运行的沙箱](lab-inspecting-a-live-sandbox.md)：动手实验
8. [常见的坑](pitfalls.md)

## 延伸阅读

- [Claude Code 文档：Sandboxing](https://docs.claude.com/en/docs/claude-code/sandboxing)
- [Anthropic 工程博客：Beyond permission prompts](https://www.anthropic.com/engineering/claude-code-sandboxing)
- [anthropic-experimental/sandbox-runtime](https://github.com/anthropic-experimental/sandbox-runtime)：Claude Code 沙箱的开源实现
- [Codex 文档：Security](https://developers.openai.com/codex/security)
- [openai/codex](https://github.com/openai/codex)：`docs/sandbox.md`、`codex-rs/linux-sandbox`
