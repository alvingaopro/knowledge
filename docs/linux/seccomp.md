---
title: seccomp
description: Checking every system call a process makes with a BPF filter
type: explanation
tags: [linux, security, sandbox]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://man7.org/linux/man-pages/man2/seccomp.2.html
  - https://docs.kernel.org/userspace-api/seccomp_filter.html
---

seccomp (secure computing) lets a process install a small filter program that every system call passes through first: allow it, return an error, or kill the process.

## System calls first

To do anything real (open a file, make a network connection, start a program) a program must ask the kernel. That request is a system call (syscall), e.g. `openat`, `connect`, `execve`, `socket`. Stop the system call and you stop the action, whatever language the program is in and however the command was written.

## Two modes

| `Seccomp` in `/proc/<pid>/status` | Meaning |
| --- | --- |
| `0` | Off |
| `1` | Strict mode: only `read`, `write`, `exit`, `sigreturn` |
| `2` | Filter mode: a custom BPF filter is installed |

`Seccomp_filters: N` is how many filters are stacked; each system call goes through all of them and the strictest result wins.

## Properties of a filter

- It checks the system call number and the **numeric values** of its arguments (e.g. whether `socket`'s first argument is `AF_UNIX`). It can't dereference pointers, so it can't filter by file path; path restrictions need a [mount namespace](namespaces.md) or [Landlock](landlock.md).
- Filters can only be added, never removed.
- They're inherited through `fork` and `execve`.
- An unprivileged process must set [NoNewPrivs](no-new-privs.md) first.

## Use in agent sandboxes

Claude Code's Linux sandbox uses seccomp to block creating new Unix sockets. A Unix socket is a "socket file" processes on one machine use to talk to each other. Without the block, a command could bypass the [egress proxy](../ai-agents/sandboxing/egress-proxy.md) and connect straight to host sockets like `docker.sock`, gaining control outside the sandbox.

Docker also installs a default seccomp profile that blocks over forty dangerous system calls.

## Related

- [NoNewPrivs](no-new-privs.md)
- [bubblewrap](bubblewrap.md)
