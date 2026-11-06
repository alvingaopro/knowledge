---
title: Claude Code vs Codex sandboxes
description: How the two coding agents' sandboxes compare in mechanism, default boundaries, network and approval
type: reference
tags: [ai-agents, claude-code, codex, sandbox]
created: 2026-11-06
updated: 2026-11-06
---

| | [Claude Code](claude-code.md) | [Codex](codex.md) |
| --- | --- | --- |
| What's wrapped | Bash tool commands; file tools go through permissions | Commands the agent runs; patch writes checked against writable roots |
| Linux | bubblewrap + seccomp + socat | bubblewrap + seccomp (legacy: Landlock) |
| macOS | Seatbelt (generated profile) | Seatbelt (built-in base profile) |
| Reads | Everything by default, deny list | Everything by default |
| Writes | Working + temporary directory, adjustable | Per mode; `.git` read-only under `workspace-write` |
| Network | Only through a [proxy](egress-proxy.md), domain allowlist | Off by default, on/off switch; newer versions add a proxy allowlist |
| No prompts | `autoAllowBashIfSandboxed` | `approval_policy = "on-request"` |
| Escape hatch | `dangerouslyDisableSandbox`, `excludedCommands` | Escalation requests, `danger-full-access`, `--yolo` |
| Source | `anthropic-experimental/sandbox-runtime` | `codex-rs` in `openai/codex` |

## In common

- Neither is a VM; neither limits CPU or memory.
- Both confine first and approve only boundary crossings; see [two gates](permissions-vs-sandbox.md).
- On Linux both depend on unprivileged [user namespaces](../../linux/user-namespaces.md).

## Main differences

- **Network**: Claude Code started with "no interface + allowlisting proxy"; Codex started with on or off.
- **`.git`**: Codex's `workspace-write` makes `.git` read-only by default, so the agent can't commit itself; Claude Code's default lets it write `.git` inside the working directory.
- **Approval granularity**: Claude Code's rules are per tool and command pattern; Codex controls overall behaviour with one policy value.
