---
title: Claude Code's sandbox
description: How Claude Code confines Bash commands' file and network access with sandbox-runtime, and how to configure it
type: explanation
tags: [ai-agents, claude-code, sandbox]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://docs.claude.com/en/docs/claude-code/sandboxing
  - https://www.anthropic.com/engineering/claude-code-sandboxing
  - https://github.com/anthropic-experimental/sandbox-runtime
---

Claude Code uses the open-source `@anthropic-ai/sandbox-runtime` (CLI `srt`) to wrap each Bash command in an OS sandbox: writes only in the working and temporary directories, network only to allowlisted domains through a proxy.

## Implementation

| Platform | Mechanism |
| --- | --- |
| Linux | [bubblewrap](../../linux/bubblewrap.md) creates user / mnt / pid / net [namespaces](../../linux/namespaces.md); [seccomp](../../linux/seccomp.md) blocks new Unix sockets; `socat` bridges traffic to the [egress proxy](egress-proxy.md) outside. Needs `bwrap` and `socat` |
| macOS | `sandbox-exec` with a [Seatbelt](../../macos/seatbelt.md) profile generated from the settings |

Each command gets its own sandbox; the session as a whole isn't in a container.

## File system

| Operation | Default | Notes |
| --- | --- | --- |
| Read | Almost everything, except listed paths | The deny list comes from `Read(...)` deny rules and sandbox settings |
| Write | Only the working directory and temporary directory | With `.claude/settings.json`, hooks, skills and similar carved out, so the agent can't edit its own configuration to grant itself more |

## Settings

The `sandbox` section of `settings.json`:

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "allowUnsandboxedCommands": false,
    "excludedCommands": ["docker *"],
    "network": {
      "allowedDomains": ["github.com", "registry.npmjs.org"],
      "allowUnixSockets": []
    },
    "filesystem": { "allowWrite": [], "denyWrite": [] }
  }
}
```

| Key | Effect |
| --- | --- |
| `enabled` | Turns the sandbox on; interactively, `/sandbox` too |
| `autoAllowBashIfSandboxed` | Sandboxed Bash commands no longer prompt for permission |
| `allowUnsandboxedCommands` | Whether the model may ask, via the Bash tool's `dangerouslyDisableSandbox` parameter, to rerun a command outside; `false` closes that door |
| `excludedCommands` | Run outside the sandbox and go back through normal permission checks |
| `network.allowedDomains` | The egress allowlist |
| `network.allowUnixSockets` | Unix sockets that may be reached, e.g. `docker.sock`; allowing one hands over control of the host |
| `filesystem.allowWrite` / `denyWrite` | Add or remove writable paths |

Key names follow the [official docs](https://docs.claude.com/en/docs/claude-code/sandboxing) as of 2026-11; they change between versions.

## Relation to permissions

Only the Bash tool is sandboxed. Read, Edit, WebFetch and MCP tools still go through permission rules. See [two gates](permissions-vs-sandbox.md).

## Related

- [Codex's sandbox](codex.md)
- [Comparison](claude-code-vs-codex.md)
- [Inspecting a live sandbox](lab-inspecting-a-live-sandbox.md)
