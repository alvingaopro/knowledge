---
title: NoNewPrivs
description: A flag that stops a process and its descendants from ever gaining privileges through setuid programs
type: explanation
tags: [linux, security, privileges]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://docs.kernel.org/userspace-api/no_new_privs.html
---

NoNewPrivs is a per-process flag: once set, neither the process nor any descendant can gain privileges when executing a new program, and it can't be unset.

## The problem it solves

Setuid programs such as `sudo`, `su` and `passwd` run as the file's owner (usually root); programs with file capabilities gain those capabilities when executed. If that path stays open inside a sandbox, the other restrictions can be bypassed.

With NoNewPrivs set:

- setuid and setgid bits are ignored, so `sudo` can't become root.
- File capabilities have no effect.
- The flag is inherited by every child; neither `fork` nor `execve` removes it.

## Setting and checking it

```c
prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
```

```sh
grep NoNewPrivs /proc/self/status   # 1 means set
setpriv --no-new-privs bash         # set it from the command line
```

## Relation to seccomp

A process without `CAP_SYS_ADMIN` must set NoNewPrivs before it may install a [seccomp](seccomp.md) filter. Otherwise it could install a filter that makes system calls misbehave and then execute a setuid program, tricking it into a mistake. That's why the two almost always appear together in a sandbox.

## Related

- [Capabilities](capabilities.md)
- [seccomp](seccomp.md)
