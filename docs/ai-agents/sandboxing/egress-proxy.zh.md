---
title: 出网代理
description: 没有网卡的沙箱如何通过沙箱外的代理按域名白名单访问网络
type: explanation
tags: [ai-agents, sandbox, networking]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://github.com/anthropic-experimental/sandbox-runtime
---

沙箱里的命令没有网卡，所有流量只能交给沙箱外的代理，由代理按域名白名单决定放不放行。

## 为什么不用防火墙

防火墙按 IP 过滤，而 `github.com`、`registry.npmjs.org` 背后是 CDN，IP 会变、还和别的网站共用。HTTP 代理能看到目标**域名**（HTTPS 的 `CONNECT github.com:443`），按域名放行更准确，也不需要 root 去改防火墙。

## Linux 上的数据路径

```mermaid
flowchart LR
  subgraph 沙箱内["沙箱内（新的 net namespace，只有 lo）"]
    C["curl / git / npm<br/>读 HTTPS_PROXY=127.0.0.1:3128"] --> S["socat<br/>监听 127.0.0.1:3128"]
  end
  S -->|Unix socket| P["沙箱外的 HTTP / SOCKS 代理"]
  P -->|域名在白名单| I["互联网"]
  P -.->|不在白名单| X["拒绝或询问用户"]
```

1. 新的 [net namespace](../../linux/namespaces.md) 里只有 `lo`，命令无法直连任何外部地址。
2. 沙箱给命令设置 `HTTP_PROXY`、`HTTPS_PROXY`、`ALL_PROXY` 等环境变量，指向沙箱内的一个本地端口。
3. 沙箱内的 `socat` 把这个端口转发到一个 Unix socket；这个 socket 文件挂载进了沙箱，另一端连着沙箱外的代理。
4. 代理检查目标域名，在白名单内就转发。
5. [seccomp](../../linux/seccomp.md) 禁止命令自己新建 Unix socket，防止它绕过代理去连宿主上的其他 socket。

macOS 上不需要 socat：[Seatbelt](../../macos/seatbelt.md) 规则直接只允许连本机代理端口。

## 后果

- 不认代理环境变量的程序（自己开裸 TCP 的工具）连不出去。
- Git over SSH 不是 HTTP，需要改用 HTTPS remote，或用 `GIT_SSH_COMMAND` 让 ssh 通过代理的 `CONNECT` 建立连接。
- 代理凭据通常放在环境变量里，属于敏感信息，不要打印到日志。

## 相关

- [Claude Code 的沙箱](claude-code.md)
- [常见的坑](pitfalls.md)
