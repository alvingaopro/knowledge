---
title: How coding agents sandbox their commands
description: Researching how Claude Code and Codex confine shell commands, from inside a running sandbox
type: case-study
tags: [ai-agents, claude-code, codex, sandbox, linux]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://docs.claude.com/en/docs/claude-code/sandboxing
  - https://github.com/anthropic-experimental/sandbox-runtime
  - https://github.com/openai/codex
---

**Question:** when Claude Code or Codex runs a shell command "in a sandbox", what actually stops it from touching the rest of the machine?

**Short answer:** neither uses a VM. Each command is wrapped in kernel mechanisms: on Linux, [bubblewrap](../linux/bubblewrap.md) builds new [namespaces](../linux/namespaces.md), drops [capabilities](../linux/capabilities.md), sets [NoNewPrivs](../linux/no-new-privs.md) and installs [seccomp](../linux/seccomp.md); on macOS, [Seatbelt](../macos/seatbelt.md). Network access goes through an [egress proxy](../ai-agents/sandboxing/egress-proxy.md) or is off. Because commands are confined, they can run without approval; only boundary crossings ask a human ([two gates](../ai-agents/sandboxing/permissions-vs-sandbox.md)).

## Context

This came up while building a tool that runs coding agents unattended and decides which of their commands need a human. To decide what to grant a sandbox, we first had to know exactly what the sandbox already does.

## How it was researched

### 1. Start from the documentation

The vendors' docs give the model: Claude Code has `sandbox.enabled`, allowed domains and write paths ([notes](../ai-agents/sandboxing/claude-code.md)); Codex has `sandbox_mode` and `approval_policy` ([notes](../ai-agents/sandboxing/codex.md)). Docs say *what* is configurable, not *how* it's enforced.

### 2. Look at a sandbox from the inside

The research itself ran inside Claude Code with its sandbox on, so the cheapest evidence was to inspect the sandbox from within: `ps`, `/proc/self/ns`, `/proc/self/status`, `/proc/net/dev`, the proxy variables. Every line of the result maps to a mechanism; the full walk-through is in [inspecting a live sandbox](../ai-agents/sandboxing/lab-inspecting-a-live-sandbox.md), and the general method in [inspecting through /proc](../linux/procfs-isolation-inspection.md).

Two observations needed kernel background to read:

- Namespace IDs `4026531834`–`4026531839` are the fixed IDs of the host's initial namespaces, which tells shared from new at a glance.
- PID 1 inside was `apply-seccomp`, not a shell: the filter is installed first and inherited by everything after.

### 3. Check the binary, not just the docs

Many write-ups describe Codex on Linux as Landlock + seccomp. The installed codex-cli 0.166.0 said otherwise: `strings` on the binary showed bubblewrap arguments (`--unshare-net`, `--ro-bind`), a Landlock *fallback* (`use_legacy_landlock`), and managed-network settings (`network_proxy`, `allowed_domains`). The implementation had moved ahead of the commonly cited description.

### 4. Try it, and watch it fail

Running `codex sandbox` from inside Claude Code's sandbox failed with `bwrap: No permissions to create new namespace`. The outer sandbox forbids new [user namespaces](../linux/user-namespaces.md), and every bubblewrap-based sandbox depends on them. The failure confirmed the mechanism better than a success would have.

## Findings

1. Both agents sandbox **shell commands only**. Claude Code's file tools, MCP servers and hooks aren't in the OS sandbox.
2. On Linux both now use bubblewrap; Claude Code adds socat and a domain-allowlisting proxy, Codex started with network on/off and is adding a proxy.
3. Writes are confined to the working and temporary directories, minus the agent's own configuration, so it can't grant itself more.
4. Codex keeps `.git` read-only under `workspace-write`; Claude Code doesn't by default.
5. A sandbox is not a VM: no CPU or memory limits, and nesting usually fails.

Side by side: [Claude Code vs Codex](../ai-agents/sandboxing/claude-code-vs-codex.md).

## Lessons

- **Check the shipped artifact.** For fast-moving tools, the binary and its `--help` are more current than blog posts, and sometimes than the docs.
- **Test in the real layout.** A git worktree keeps its index outside the working directory, so commits fail in a sandbox that only allows the working directory. Tests that ran in a temporary directory, which is always writable, never saw it. More in [pitfalls](../ai-agents/sandboxing/pitfalls.md).
- **Redact as you go.** The proxy variables printed during inspection carried live credentials. Anything copied from a sandbox into notes needs scrubbing.

## Not verified

- macOS: Seatbelt behaviour is from documentation and source, not run here.
- Codex's `network_proxy` / `allowed_domains`: seen in the binary, not exercised.
- Which component installed each of the two stacked seccomp filters, and what exactly they block, wasn't dumped.

## Notes produced

- Linux: [namespaces](../linux/namespaces.md), [user namespaces](../linux/user-namespaces.md), [capabilities](../linux/capabilities.md), [NoNewPrivs](../linux/no-new-privs.md), [seccomp](../linux/seccomp.md), [Landlock](../linux/landlock.md), [bubblewrap](../linux/bubblewrap.md), [inspecting through /proc](../linux/procfs-isolation-inspection.md)
- macOS: [Seatbelt](../macos/seatbelt.md)
- Agents: [the sandboxing topic](../ai-agents/sandboxing/index.md)
