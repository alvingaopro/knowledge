---
title: Capabilities
description: How Linux splits root's power into pieces, and how to read the capability bitmaps in /proc
type: explanation
tags: [linux, security, privileges]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://man7.org/linux/man-pages/man7/capabilities.7.html
---

Capabilities split root's privileges into some forty independent pieces, so a process can hold just the ones it needs instead of all or nothing.

## What they are

For example:

| Capability | Allows |
| --- | --- |
| `CAP_SYS_ADMIN` | Mounting file systems and many other admin operations (often called "the new root") |
| `CAP_NET_ADMIN` | Changing interfaces, routes, firewall rules |
| `CAP_NET_BIND_SERVICE` | Listening on ports below 1024 |
| `CAP_DAC_OVERRIDE` | Ignoring file read/write permissions |
| `CAP_SETUID` | Switching to any user ID |

## The five sets

`/proc/<pid>/status` has five lines, each a hexadecimal bitmap with one bit per capability:

| Field | Meaning |
| --- | --- |
| `CapEff` | Effective: what the kernel checks right now |
| `CapPrm` | Permitted: the ceiling Effective can draw from |
| `CapInh` | Inheritable: what may carry over when executing a new program |
| `CapBnd` | Bounding: the ceiling for the whole process tree; can only shrink |
| `CapAmb` | Ambient: kept even when executing ordinary programs |

`capsh --decode=000001ffffffffff` translates a bitmap into names.

## In a sandbox

[bubblewrap](bubblewrap.md) briefly holds every capability inside its [user namespace](user-namespaces.md) while setting up, then drops them all before running the target command. So inside a sandbox you typically see:

```text
CapPrm: 0000000000000000
CapEff: 0000000000000000
CapBnd: 000001ffffffffff
```

An all-ones `CapBnd` is fine: Permitted and Effective are empty, and with [NoNewPrivs](no-new-privs.md) there's no way to get them back.

Note that an ordinary user's shell on the host also has `CapEff` of 0. This line alone doesn't prove you're sandboxed; read it together with [namespaces](namespaces.md) and [seccomp](seccomp.md).

## Related

- [NoNewPrivs](no-new-privs.md)
- [Inspecting through /proc](procfs-isolation-inspection.md)
