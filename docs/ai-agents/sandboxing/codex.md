---
title: Codex's sandbox
description: The Codex CLI's two knobs, sandbox_mode and approval_policy, and how each platform implements them
type: explanation
tags: [ai-agents, codex, sandbox]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://developers.openai.com/codex/security
  - https://github.com/openai/codex
---

Codex splits the problem into two independent knobs: `sandbox_mode` decides what commands can do, `approval_policy` decides when to ask a human.

## sandbox_mode

| Mode | Writes | Network | Use |
| --- | --- | --- | --- |
| `read-only` | Nowhere | Off | Read-only analysis |
| `workspace-write` | Working directory, `$TMPDIR`, `/tmp`, plus `writable_roots`; protected paths such as `.git` and `.codex` stay read-only | Off by default | Everyday coding |
| `danger-full-access` | Unrestricted | Unrestricted | Already inside a container or VM |

```toml
# ~/.codex/config.toml
sandbox_mode = "workspace-write"
approval_policy = "on-request"

[sandbox_workspace_write]
network_access = false
writable_roots = ["/home/<user>/.cache/pip"]
exclude_tmpdir_env_var = false
exclude_slash_tmp = false
```

## approval_policy

| Policy | Behaviour |
| --- | --- |
| `untrusted` | Only known-safe read-only commands run automatically; everything else asks |
| `on-request` | Runs inside the sandbox without asking; when the model decides it must cross the boundary (write outside, use the network) it requests escalation, and an approved command runs outside the sandbox |
| `never` | Never asks; failures go back to the model |
| `on-failure` | Older option, no longer recommended |

Common combinations: `--full-auto` is `workspace-write` + `on-request`; `--yolo` (`--dangerously-bypass-approvals-and-sandbox`) means no sandbox and no questions.

## Implementation

| Platform | Mechanism |
| --- | --- |
| macOS | `/usr/bin/sandbox-exec` with a built-in [Seatbelt](../../macos/seatbelt.md) base profile, extended with writable roots and network settings |
| Linux (current) | [bubblewrap](../../linux/bubblewrap.md): `--unshare-user`, `--unshare-net`, `--ro-bind` of the root then writable directories bound back; plus [seccomp](../../linux/seccomp.md) |
| Linux (legacy) | [Landlock](../../linux/landlock.md) + seccomp via `codex-linux-sandbox`; kept as a fallback (`use_legacy_landlock`) |
| Windows | A restricted-token / separate-account design, or the Linux approach inside WSL |

The Linux details were checked against the codex-cli 0.166.0 binary, which also contains managed-network settings such as `network_proxy` and `allowed_domains`: Codex is adding domain allowlisting much like an [egress proxy](egress-proxy.md).

Sandboxed child processes see `CODEX_SANDBOX_NETWORK_DISABLED=1` (and `CODEX_SANDBOX=seatbelt` on macOS), so tests can skip network cases.

## Try it

```sh
codex sandbox -- touch ./ok.txt ~/outside.txt
codex sandbox -- curl -sI https://github.com
codex sandbox -c 'sandbox_workspace_write.network_access=true' -- curl -sI https://github.com
```

Older versions used `codex sandbox linux|macos` or `codex debug seatbelt|landlock`; check `codex sandbox --help`. Don't run it inside another sandbox; see [pitfalls](pitfalls.md).

## Related

- [Claude Code's sandbox](claude-code.md)
- [Comparison](claude-code-vs-codex.md)
