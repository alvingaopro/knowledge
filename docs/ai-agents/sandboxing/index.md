---
title: Coding agent sandboxes
description: Where to start learning how Claude Code and Codex sandbox commands, and in what order
---

Neither Claude Code nor Codex runs in a virtual machine. They wrap the **shell commands** an agent runs in restrictions the operating system kernel enforces: where it may write, what it may read, which hosts it may reach. Commands inside the limits run without asking; only crossing them needs a human.

## Reading order

1. [Permissions and the OS sandbox: two gates](permissions-vs-sandbox.md): what each layer is responsible for
2. Linux basics: [namespaces](../../linux/namespaces.md), [user namespaces](../../linux/user-namespaces.md), [capabilities](../../linux/capabilities.md), [NoNewPrivs](../../linux/no-new-privs.md), [seccomp](../../linux/seccomp.md), [bubblewrap](../../linux/bubblewrap.md); on macOS, [Seatbelt](../../macos/seatbelt.md)
3. [Egress proxy](egress-proxy.md): how a sandbox with no network interface reaches allowed domains
4. [Claude Code's sandbox](claude-code.md)
5. [Codex's sandbox](codex.md)
6. [Claude Code vs Codex](claude-code-vs-codex.md)
7. [Inspecting a live sandbox](lab-inspecting-a-live-sandbox.md): hands-on
8. [Common pitfalls](pitfalls.md)

The [case study](../../case-studies/coding-agent-sandboxes.md) tells how this was researched.

## Further reading

- [Claude Code docs: Sandboxing](https://docs.claude.com/en/docs/claude-code/sandboxing)
- [Anthropic engineering: Beyond permission prompts](https://www.anthropic.com/engineering/claude-code-sandboxing)
- [anthropic-experimental/sandbox-runtime](https://github.com/anthropic-experimental/sandbox-runtime): the open-source implementation behind Claude Code's sandbox
- [Codex docs: Security](https://developers.openai.com/codex/security)
- [openai/codex](https://github.com/openai/codex): `docs/sandbox.md`, `codex-rs/linux-sandbox`
