---
title: User namespaces
description: Why an unprivileged user can build a sandbox without sudo, and why that sometimes fails
type: explanation
tags: [linux, isolation, sandbox]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://man7.org/linux/man-pages/man7/user_namespaces.7.html
---

A user namespace lets an unprivileged user create a small world in which they are an administrator, so they can create the other [namespaces](namespaces.md). Those privileges mean nothing on the host.

## Why it's needed

Creating mnt, net or pid namespaces normally requires `CAP_SYS_ADMIN`, that is, root. User namespaces are the exception: any user can create one, and its creator holds every [capability](capabilities.md) inside it. With those in-namespace privileges it can go on to create other namespaces and mount file systems.

This is why [bubblewrap](bubblewrap.md) needs neither setuid nor sudo.

## ID mapping

IDs inside a user namespace map to host IDs, recorded in `/proc/<pid>/uid_map`. The three columns are: first ID inside, first ID on the host, count.

```text
1000  1000  1      # inside 1000 is host 1000, one ID mapped: you're still yourself
   0  1000  1      # unshare --map-root-user: shows as root inside, really host 1000
```

So `unshare --user --map-root-user id` prints `uid=0(root)`, yet `touch /etc/x` is still denied: to host files, you are still 1000.

## Why it fails

`No permissions to create new namespace` or `Operation not permitted` usually means one of:

- You're already inside another sandbox, which forbids creating user namespaces (nested sandboxes).
- The distribution disables unprivileged user namespaces, e.g. `kernel.unprivileged_userns_clone=0`, or Ubuntu 24.04's AppArmor restriction `kernel.apparmor_restrict_unprivileged_userns=1`.
- A container runtime's default seccomp profile blocks the relevant `unshare`/`clone` flags.

## The security cost

User namespaces let unprivileged users reach kernel code paths that used to be root-only, and they have been the entry point for many privilege-escalation bugs. That's why some distributions restrict them by default.

## Related

- [Namespaces](namespaces.md)
- [Capabilities](capabilities.md)
