---
title: Inspecting isolation through /proc
description: Use ps, /proc/self/ns, /proc/self/status and friends to tell whether you're sandboxed and how
type: how-to
tags: [linux, sandbox, debugging]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://man7.org/linux/man-pages/man5/proc.5.html
---

`/proc` is a virtual directory provided by the kernel; its "files" are live information about processes, and `/proc/self` is the current process. Together, the commands below tell you whether a shell is sandboxed and what it's restricted from.

## The checks

```sh
ps -eo pid,args | head                    # how many processes are visible, who is PID 1
ls -l /proc/self/ns                       # which namespaces we're in
cat /proc/self/uid_map                    # how user IDs are mapped
cat /proc/net/dev                         # which network interfaces exist
grep -E 'Cap|NoNewPrivs|Seccomp' /proc/self/status
env | grep -i _proxy                      # is traffic steered to a proxy
```

## Reading the output

### Process list

A host usually runs hundreds of processes. If you only see your own command chain, and PID 1 isn't `systemd`/`init`, you're in a new pid [namespace](namespaces.md).

### `/proc/self/ns`

```text
cgroup -> cgroup:[4026531835]
ipc    -> ipc:[4026531839]
mnt    -> mnt:[4026533631]
pid    -> pid:[4026533632]
user   -> user:[4026533630]
uts    -> uts:[4026531838]
```

The bracketed number is the namespace ID; equal IDs mean the same namespace. The kernel gives the boot-time (initial) user, pid, uts, ipc, cgroup and time namespaces fixed IDs `4026531834`–`4026531839`. A number in that range means shared with the host; anything else is new. The initial mnt and net IDs are allocated dynamically, so judge those by other evidence (such as the interface list).

### `uid_map`

Three columns: first ID inside, first ID on the host, count. `1000 1000 1` means you're still yourself in the sandbox, not root. See [user namespaces](user-namespaces.md).

### `/proc/net/dev`

Only `lo` means a new net namespace with no interface that reaches outside.

### `/proc/self/status`

| Field | Typical in a sandbox | Meaning |
| --- | --- | --- |
| `CapEff` / `CapPrm` | `0` | No privileges at all; see [capabilities](capabilities.md) |
| `NoNewPrivs` | `1` | setuid programs can't escalate; see [NoNewPrivs](no-new-privs.md) |
| `Seccomp` | `2` | A system call filter is installed; see [seccomp](seccomp.md) |
| `Seccomp_filters` | `≥1` | How many filters are stacked |

No single field proves much (an ordinary shell's `CapEff` is also 0); read them together.

## Worked example

[Inspecting a live agent sandbox](../ai-agents/sandboxing/lab-inspecting-a-live-sandbox.md) runs these commands inside Claude Code's sandbox and explains each result.
