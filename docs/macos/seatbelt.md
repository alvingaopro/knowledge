---
title: Seatbelt
description: The macOS sandbox that restricts files, network and system services with SBPL profiles
type: explanation
tags: [macos, security, sandbox]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://github.com/anthropic-experimental/sandbox-runtime
  - https://github.com/openai/codex
---

Seatbelt is the sandbox mechanism in the macOS kernel; App Sandbox is built on it. On the command line, `/usr/bin/sandbox-exec -p <profile> <command>` runs a command under a given profile.

## What a profile looks like

The language is SBPL (Sandbox Profile Language), Scheme-style S-expressions:

```scheme
(version 1)
(deny default)                                   ; deny everything by default
(allow process-exec process-fork)
(allow file-read*)                               ; allow reads
(allow file-write* (subpath "/Users/me/project")); writes only in the project
(allow network-outbound (remote ip "localhost:3128")) ; only the local proxy
```

Rules combine an operation (`file-read*`, `file-write*`, `network-outbound`, `mach-lookup` …) with filters (`subpath`, `literal`, `regex`, `remote ip`).

## Mapping to the Linux approach

| Linux | macOS |
| --- | --- |
| [mount namespace](../linux/namespaces.md) rebuilds the file tree | `file-read*` / `file-write*` path rules |
| net namespace + [egress proxy](../ai-agents/sandboxing/egress-proxy.md) | `network-outbound` allowed only to the local proxy port |
| [seccomp](../linux/seccomp.md) | Denying operation types such as `mach-lookup` |

The difference: Seatbelt doesn't change what a process *sees*. A sandboxed process can still see other processes; operations the profile forbids just fail.

## Status

`sandbox-exec` has long been marked deprecated in its man page, yet it still ships with macOS and is widely used; both Claude Code and Codex rely on it.

## Related

- [Claude Code's sandbox](../ai-agents/sandboxing/claude-code.md)
- [Codex's sandbox](../ai-agents/sandboxing/codex.md)
