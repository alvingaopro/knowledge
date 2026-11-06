---
title: Namespaces
description: What Linux namespaces are, what each kind isolates, and why sandboxes and containers rely on them
type: explanation
tags: [linux, isolation, sandbox]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://man7.org/linux/man-pages/man7/namespaces.7.html
---

A namespace gives a group of processes a **private copy** of a kernel-wide resource. The process isn't forbidden from touching the host's resources; it simply can't see them.

## What it is

Many things in the kernel exist once per machine: the process list, the mounted file systems, network interfaces, the hostname. Put a process in a new namespace and it sees a different copy of that resource. Think of it as glasses that only show the part of the world you allow.

Containers (Docker, Podman) and agent sandboxes ([bubblewrap](bubblewrap.md)) both build on this; they differ only in how much they set up around it.

## The eight kinds

| Kind | Isolates | Typical use in a sandbox |
| --- | --- | --- |
| `mnt` | Mount points, i.e. what the file tree looks like | Rebuild the tree: root read-only, the working directory writable, sensitive directories covered with empty ones |
| `pid` | Process IDs and which processes are visible | Host processes are invisible and can't be killed; the first process is PID 1 |
| `net` | Network interfaces, routes, ports | Only the loopback interface `lo`; no direct route out |
| `user` | User IDs and who owns privileges | Lets an unprivileged user create the other namespaces; see [user namespaces](user-namespaces.md) |
| `uts` | Hostname and domain name | Rarely needed |
| `ipc` | System V shared memory and message queues | Prevents shared memory across the boundary |
| `cgroup` | The visible cgroup hierarchy | Common in containers; cgroups themselves limit CPU and memory |
| `time` | Offsets of monotonic clocks | Rarely needed |

## Creating and inspecting

- System calls: `clone(2)` with `CLONE_NEW*` flags, `unshare(2)` to leave the current namespaces, `setns(2)` to join an existing one.
- Command line: `unshare`, [`bwrap`](bubblewrap.md), `nsenter`.
- Inspecting: each entry under `/proc/<pid>/ns/` points at a namespace, with its ID in brackets; equal IDs mean the same namespace. See [inspecting through /proc](procfs-isolation-inspection.md).

```sh
# No root needed (relies on user namespaces)
unshare --user --map-root-user --pid --fork --mount-proc ps -ef   # only two processes
unshare --user --map-root-user --net ip link                      # only lo, and it is DOWN
```

## What it doesn't do

Namespaces decide what a process *sees*. Resource usage (CPU, memory, process count) is the job of cgroups; which system calls are allowed is [seccomp](seccomp.md)'s; whether the process holds privileges is a matter of [capabilities](capabilities.md).

## Related

- [User namespaces](user-namespaces.md)
- [bubblewrap](bubblewrap.md)
