---
title: Claude Code 的沙箱
description: Claude Code 如何用 sandbox-runtime 限制 Bash 命令的文件和网络访问，以及相关配置
type: explanation
tags: [ai-agents, claude-code, sandbox]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://docs.claude.com/en/docs/claude-code/sandboxing
  - https://www.anthropic.com/engineering/claude-code-sandboxing
  - https://github.com/anthropic-experimental/sandbox-runtime
---

Claude Code 用开源的 `@anthropic-ai/sandbox-runtime`（命令行 `srt`）把每条 Bash 命令单独包进 OS 沙箱：写只限工作目录和临时目录，网络只能经代理访问白名单域名。

## 实现

| 平台 | 机制 |
| --- | --- |
| Linux | [bubblewrap](../../linux/bubblewrap.md) 建 user / mnt / pid / net [namespace](../../linux/namespaces.md)；[seccomp](../../linux/seccomp.md) 禁止新建 Unix socket；`socat` 把流量桥接到沙箱外的[出网代理](egress-proxy.md)。依赖 `bwrap` 和 `socat` |
| macOS | `sandbox-exec` 加按配置动态生成的 [Seatbelt](../../macos/seatbelt.md) 规则 |

每条命令单独套一层，不是整个会话进一个容器。

## 文件系统

| 操作 | 默认 | 说明 |
| --- | --- | --- |
| 读 | 几乎都能读，只拒绝列出的路径 | 拒绝名单来自权限规则里的 `Read(...)` deny 和沙箱配置 |
| 写 | 只能写当前工作目录和临时目录 | 其中再挖掉 `.claude/settings.json`、hooks、skills 等，防止 agent 改自己的配置给自己放权 |

## 配置

`settings.json` 的 `sandbox` 段：

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "allowUnsandboxedCommands": false,
    "excludedCommands": ["docker *"],
    "network": {
      "allowedDomains": ["github.com", "registry.npmjs.org"],
      "allowUnixSockets": []
    },
    "filesystem": { "allowWrite": [], "denyWrite": [] }
  }
}
```

| 键 | 作用 |
| --- | --- |
| `enabled` | 打开沙箱；交互式里也可以用 `/sandbox` |
| `autoAllowBashIfSandboxed` | 沙箱内的 Bash 命令不再弹权限确认 |
| `allowUnsandboxedCommands` | 是否允许模型通过 Bash 工具的 `dangerouslyDisableSandbox` 参数请求在沙箱外重跑；设为 `false` 彻底关掉这条路 |
| `excludedCommands` | 这些命令在沙箱外运行，回到普通权限审批 |
| `network.allowedDomains` | 出网白名单 |
| `network.allowUnixSockets` | 允许连接的 Unix socket，例如 `docker.sock`；放开等于给出宿主控制权 |
| `filesystem.allowWrite` / `denyWrite` | 增减可写路径 |

配置名以[官方文档](https://docs.claude.com/en/docs/claude-code/sandboxing)为准，版本迭代较快。

## 和权限系统的关系

沙箱只包 Bash 工具。Read、Edit、WebFetch、MCP 工具仍走权限规则。见[两道闸](permissions-vs-sandbox.md)。

## 相关

- [Codex 的沙箱](codex.md)
- [对比](claude-code-vs-codex.md)
- [解读一个正在运行的沙箱](lab-inspecting-a-live-sandbox.md)
