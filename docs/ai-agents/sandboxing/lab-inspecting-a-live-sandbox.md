---
title: Inspecting a live sandbox
description: Run inspection commands inside Claude Code's Linux sandbox and explain each result
type: tutorial
tags: [ai-agents, claude-code, sandbox, linux]
created: 2026-11-06
updated: 2026-11-06
---

With Claude Code's sandbox on, have it run the commands below through Bash. The output comes from a real session in 2026-11 (Linux, Claude Code with sandbox-runtime), with personal details and credentials removed. The method is in [inspecting through /proc](../../linux/procfs-isolation-inspection.md).

## 1. Process list

```console
$ ps -eo pid,args
PID COMMAND
  1 apply-seccomp /usr/bin/zsh -c …
  2 /usr/bin/zsh -c …
  3 ps -eo pid,args
```

- Only our own command chain is visible: we're in a new pid [namespace](../../linux/namespaces.md).
- PID 1 is `apply-seccomp`, a small sandbox-runtime program: it installs the [seccomp](../../linux/seccomp.md) filter, starts zsh as its child (PID 2), and stays as process 1. Every later command inherits the filter.
- **Meaning**: commands can't see or kill host processes such as your editor or browser.

## 2. Namespaces

```console
$ ls -l /proc/self/ns
cgroup -> cgroup:[4026531835]
ipc    -> ipc:[4026531839]
mnt    -> mnt:[4026533631]
net    -> net:[4026533029]
pid    -> pid:[4026533632]
time   -> time:[4026531834]
user   -> user:[4026533630]
uts    -> uts:[4026531838]
```

- cgroup, ipc, time and uts fall in the initial namespaces' fixed range `4026531834`–`4026531839`: shared with the host.
- user, mnt and pid are consecutive new IDs: created together. net is also new, as the next step shows.

## 3. Network interfaces

```console
$ cat /proc/net/dev
Inter-|   Receive …
 face |bytes …
    lo:       0 …
```

Only `lo`, no `eth0`: no direct way out, only the [egress proxy](egress-proxy.md).

## 4. Identity

```console
$ id
uid=1000(<user>) gid=1000(<user>) …
$ cat /proc/self/uid_map
      1000       1000          1
```

Still yourself, not root; files created inside belong to you on the host. See [user namespaces](../../linux/user-namespaces.md).

## 5. Privileges and filters

```console
$ grep -E 'Cap|NoNewPrivs|Seccomp' /proc/self/status
CapInh: 0000000000000000
CapPrm: 0000000000000000
CapEff: 0000000000000000
CapBnd: 000001ffffffffff
CapAmb: 0000000000000000
NoNewPrivs:      1
Seccomp:         2
Seccomp_filters: 2
```

- No effective [capabilities](../../linux/capabilities.md); `CapBnd` is only a ceiling, irrelevant when you hold none.
- [NoNewPrivs](../../linux/no-new-privs.md) is set: `sudo` can't escalate.
- `Seccomp: 2` is filter mode, with two filters stacked.

## 6. Network settings

```console
$ env | grep -i _proxy | sed 's/=.*@/=***@/'
HTTPS_PROXY=***@127.0.0.1:3128
ALL_PROXY=***@127.0.0.1:3128
…
```

Every kind of proxy variable points at a local port inside the sandbox; `GIT_SSH_COMMAND` makes ssh go through the proxy too. The variables carry one-time proxy credentials: don't print or commit them unredacted.

## 7. Hitting the walls

```sh
touch ./ok.txt                   # succeeds
touch ~/outside.txt              # Read-only file system
echo x >> .claude/settings.json  # denied even inside the working directory
ls ~/.ssh                        # denied or invisible
curl -sI https://github.com      # succeeds if allowlisted
curl -sI https://example.org     # refused by the proxy, or prompts
python3 -c "import socket;socket.create_connection(('1.1.1.1',53),3)"  # no interface: fails
```

## 8. Nested sandboxes

```console
$ codex sandbox -- true
bwrap: No permissions to create new namespace …
```

The outer sandbox forbids creating another [user namespace](../../linux/user-namespaces.md), so the inner bwrap fails. Run Codex experiments in an ordinary terminal.
