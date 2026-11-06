---
title: Landlock
description: A Linux security module that lets an unprivileged process restrict its own access to paths and ports
type: explanation
tags: [linux, security, sandbox]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://docs.kernel.org/userspace-api/landlock.html
---

Landlock, in Linux since 5.13, lets an ordinary process, without root, declare "only these paths" for itself and its children.

## Compared with other mechanisms

| Mechanism | Restricts by | Needs privileges? |
| --- | --- | --- |
| [mount namespace](namespaces.md) | Rebuilding a file tree | Needs a [user namespace](user-namespaces.md) |
| [seccomp](seccomp.md) | System call numbers and numeric arguments; can't see paths | No (with NoNewPrivs) |
| Landlock | File path hierarchies; newer versions also TCP ports | No |
| SELinux / AppArmor | System-wide policy written by an administrator | Root to configure |

Landlock needs no namespaces, so it works where user namespaces are disabled. The catch is that its abilities grow with kernel versions (ABI versions), so on older kernels it may only partly apply.

## How it's used

Three system calls: `landlock_create_ruleset` declares which operations are governed, `landlock_add_rule` allows paths, `landlock_restrict_self` applies it. Once applied it can't be undone and is inherited by children.

## Use in agent sandboxes

Codex's Linux sandbox originally used Landlock plus [seccomp](seccomp.md); newer versions default to [bubblewrap](bubblewrap.md) and keep Landlock as a fallback. See [Codex's sandbox](../ai-agents/sandboxing/codex.md).

## Related

- [seccomp](seccomp.md)
- [bubblewrap](bubblewrap.md)
