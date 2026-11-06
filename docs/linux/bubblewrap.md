---
title: bubblewrap
description: How bwrap builds a lightweight, rootless sandbox out of namespaces and mounts
type: explanation
tags: [linux, sandbox, tools]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://github.com/containers/bubblewrap
---

bubblewrap (command `bwrap`) is a small tool: one command sets up [namespaces](namespaces.md), assembles a file tree and drops privileges for a target program, and the sandbox disappears when the program exits. Flatpak, Claude Code and Codex all use it on Linux.

## What it does

1. Creates a [user namespace](user-namespaces.md) and briefly holds every [capability](capabilities.md) in it.
2. Creates mnt, pid, net and other namespaces as requested.
3. Mounts, one argument at a time, the file tree the program will see inside the new mnt namespace.
4. Drops all capabilities, sets [NoNewPrivs](no-new-privs.md), and optionally installs a [seccomp](seccomp.md) filter.
5. Executes the target command.

It needs no image and no daemon, and it doesn't limit CPU or memory.

## Minimal example

```sh
bwrap --ro-bind / / \
      --bind "$PWD" "$PWD" \
      --tmpfs /tmp \
      --dev /dev --proc /proc \
      --unshare-user --unshare-pid --unshare-net \
      --die-with-parent \
      bash -c 'touch ok; touch ~/no; curl -sI https://example.com'
# ok is written; ~/no fails with Read-only file system; curl reaches nothing
```

## Common options

| Option | Effect |
| --- | --- |
| `--ro-bind SRC DEST` | Read-only mount |
| `--bind SRC DEST` | Writable mount |
| `--tmpfs DEST` | Mount an empty in-memory file system, often to hide a sensitive directory |
| `--dev /dev`, `--proc /proc` | A minimal device directory and a `/proc` matching the new pid namespace |
| `--unshare-user/-pid/-net/-ipc/-uts` | Create that namespace; `--unshare-all` creates them all |
| `--die-with-parent` | End the sandbox when the parent exits |
| `--seccomp FD` | Read a compiled seccomp filter from a file descriptor |

Options apply in order: `--ro-bind / /` first, then `--bind` writable directories back, then `--tmpfs` over paths to hide.

## Limits

- It depends on unprivileged user namespaces; if they're disabled, or you're nested inside another sandbox, it fails outright.
- With no network, allowing specific domains needs a separate [egress proxy](../ai-agents/sandboxing/egress-proxy.md).

## Related

- [Namespaces](namespaces.md)
- [Claude Code's sandbox](../ai-agents/sandboxing/claude-code.md)
- [Codex's sandbox](../ai-agents/sandboxing/codex.md)
