---
title: Linux
description: Isolation and privilege mechanisms in the Linux kernel
---

The Linux kernel has no single feature called "sandbox". Sandboxes and containers combine the independent mechanisms below.

## Isolation: what a process can see

- [Namespaces](namespaces.md): a private process list, file tree and network
- [User namespaces](user-namespaces.md): let unprivileged users create the other namespaces

## Privilege: what a process can do

- [Capabilities](capabilities.md): root's power split into pieces
- [NoNewPrivs](no-new-privs.md): a process can never gain privileges again
- [seccomp](seccomp.md): a filter on system calls
- [Landlock](landlock.md): unprivileged, path-based file access restrictions

## Tools and inspection

- [bubblewrap](bubblewrap.md): a command-line tool that combines the above into a lightweight sandbox
- [Inspecting isolation through /proc](procfs-isolation-inspection.md)

## Suggested order

namespaces → user namespaces → capabilities → NoNewPrivs → seccomp → bubblewrap → inspecting with /proc.
