---
title: Codex 的沙箱
description: Codex CLI 的 sandbox_mode 与 approval_policy 两个旋钮，以及各平台的实现
type: explanation
tags: [ai-agents, codex, sandbox]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://developers.openai.com/codex/security
  - https://github.com/openai/codex
---

Codex 把问题拆成两个独立的旋钮：`sandbox_mode` 决定命令能做什么，`approval_policy` 决定什么时候问人。

## sandbox_mode

| 模式 | 写 | 网络 | 用途 |
| --- | --- | --- | --- |
| `read-only` | 哪都不能写 | 关 | 只读分析 |
| `workspace-write` | 工作目录、`$TMPDIR`、`/tmp`，加上 `writable_roots`；其中 `.git`、`.codex` 等受保护路径仍只读 | 默认关 | 日常写代码 |
| `danger-full-access` | 不限制 | 不限制 | 已经在容器或 VM 里 |

```toml
# ~/.codex/config.toml
sandbox_mode = "workspace-write"
approval_policy = "on-request"

[sandbox_workspace_write]
network_access = false
writable_roots = ["/home/<user>/.cache/pip"]
exclude_tmpdir_env_var = false
exclude_slash_tmp = false
```

## approval_policy

| 策略 | 行为 |
| --- | --- |
| `untrusted` | 只有已知安全的只读命令自动运行，其余都问 |
| `on-request` | 沙箱内自动运行；模型认为需要越界（写外面、联网）时发起提权请求，人批准后在沙箱外执行 |
| `never` | 从不问，失败就把错误交还模型 |
| `on-failure` | 旧选项，不再推荐 |

常用组合：`--full-auto` 等于 `workspace-write` + `on-request`；`--yolo`（`--dangerously-bypass-approvals-and-sandbox`）既不要沙箱也不问。

## 实现

| 平台 | 机制 |
| --- | --- |
| macOS | `/usr/bin/sandbox-exec` + 内置的 [Seatbelt](../../macos/seatbelt.md) 基础规则，按 writable roots 和网络设置拼接 |
| Linux（新版） | [bubblewrap](../../linux/bubblewrap.md)：`--unshare-user`、`--unshare-net`，`--ro-bind` 根目录后再挂回可写目录；外加 [seccomp](../../linux/seccomp.md) |
| Linux（旧版） | [Landlock](../../linux/landlock.md) + seccomp，由 `codex-linux-sandbox` 执行；新版保留为回退（`use_legacy_landlock`） |
| Windows | 受限 token / 独立账户方案，或在 WSL 里使用 Linux 方案 |

以上 Linux 部分核对自 codex-cli 0.166.0 的二进制，其中还有 `network_proxy`、`allowed_domains` 等托管网络配置，说明 Codex 也在加入类似 [出网代理](egress-proxy.md) 的按域名放行。

沙箱内的子进程能看到 `CODEX_SANDBOX_NETWORK_DISABLED=1`（macOS 上还有 `CODEX_SANDBOX=seatbelt`），测试代码可据此跳过联网用例。

## 自己试

```sh
codex sandbox -- touch ./ok.txt ~/outside.txt
codex sandbox -- curl -sI https://github.com
codex sandbox -c 'sandbox_workspace_write.network_access=true' -- curl -sI https://github.com
```

旧版本的子命令是 `codex sandbox linux|macos` 或 `codex debug seatbelt|landlock`，以 `codex sandbox --help` 为准。不要在另一个沙箱里运行，见[常见的坑](pitfalls.md)。

## 相关

- [Claude Code 的沙箱](claude-code.md)
- [对比](claude-code-vs-codex.md)
