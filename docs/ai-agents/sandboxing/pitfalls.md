---
title: Common sandbox pitfalls
description: Typical failures inside agent sandboxes, their causes and fixes
type: reference
tags: [ai-agents, sandbox, debugging]
created: 2026-11-06
updated: 2026-11-06
---

| Symptom | Cause | Fix |
| --- | --- | --- |
| Committing in a git worktree fails with `index.lock: Read-only file system` | A worktree's index and refs live in the main repository's `.git`, outside the working directory | Make the repository's common git directory writable, but keep its `config` and `hooks` read-only so nothing can plant code that runs outside the sandbox |
| Commit identity, `pushInsteadOf` and similar settings silently vanish | Git silently skips an `[include]` it can't read; the included file is on the read deny list | Put needed config somewhere readable, or pass it through environment variables (`GIT_AUTHOR_NAME` …) |
| `git push` over SSH fails | SSH isn't HTTP and doesn't go through the [egress proxy](egress-proxy.md) | Use an HTTPS remote, or `GIT_SSH_COMMAND` through the proxy's `CONNECT`, or exclude the command from the sandbox |
| Can't reach `docker.sock`, ssh-agent or a database socket | [seccomp](../../linux/seccomp.md) blocks new Unix sockets, and those paths aren't mounted | Allow that specific socket; remember `docker.sock` equals root on the host |
| `bwrap: No permissions to create new namespace` | Nested in another sandbox, or unprivileged [user namespaces](../../linux/user-namespaces.md) disabled | Run outside; check settings such as `kernel.apparmor_restrict_unprivileged_userns` |
| One tool can't reach the network though curl can | The tool ignores `HTTPS_PROXY` and friends | Use the tool's own proxy setting |
| Tests pass, real tasks fail | Tests ran only in a temporary directory, which is writable anyway | Test with the same directory layout as real use |
| Assuming file tools are isolated too | Only shell commands are sandboxed; built-in file tools, MCP and hooks aren't | Restrict those with permission rules; see [two gates](permissions-vs-sandbox.md) |
| A command saturates the machine | The sandbox doesn't limit CPU, memory or process count | Add cgroup limits, e.g. `systemd-run --user -p MemoryMax=` |
