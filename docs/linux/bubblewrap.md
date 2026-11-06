---
title: bubblewrap
description: bwrap 如何用 namespace 和挂载拼出一个无需 root 的轻量沙箱
type: explanation
tags: [linux, sandbox, tools]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://github.com/containers/bubblewrap
---

bubblewrap（命令 `bwrap`）是一个小工具：一条命令就为目标程序建好 [namespace](namespaces.md)、拼好文件树、丢掉特权，程序结束沙箱也随之消失。Flatpak、Claude Code 和 Codex 的 Linux 沙箱都用它。

## 它做了什么

1. 创建 [user namespace](user-namespaces.md)，在里面临时拥有全部 [capability](capabilities.md)。
2. 按参数创建 mnt、pid、net 等 namespace。
3. 在新的 mnt namespace 里按参数一项项挂载，拼出程序能看到的文件树。
4. 丢掉全部 capability，打开 [NoNewPrivs](no-new-privs.md)，可选地装上 [seccomp](seccomp.md) 过滤器。
5. 执行目标命令。

它不需要镜像、不需要守护进程，也不限制 CPU 和内存。

## 最小例子

```sh
bwrap --ro-bind / / \
      --bind "$PWD" "$PWD" \
      --tmpfs /tmp \
      --dev /dev --proc /proc \
      --unshare-user --unshare-pid --unshare-net \
      --die-with-parent \
      bash -c 'touch ok; touch ~/no; curl -sI https://example.com'
# ok 写成功；~/no 报 Read-only file system；curl 连不上任何地址
```

## 常用参数

| 参数 | 作用 |
| --- | --- |
| `--ro-bind SRC DEST` | 只读挂载 |
| `--bind SRC DEST` | 可写挂载 |
| `--tmpfs DEST` | 挂一个空的内存文件系统，常用来“盖住”敏感目录 |
| `--dev /dev`、`--proc /proc` | 提供最小的设备目录和与新 pid namespace 匹配的 `/proc` |
| `--unshare-user/-pid/-net/-ipc/-uts` | 创建对应 namespace；`--unshare-all` 全部创建 |
| `--die-with-parent` | 父进程退出时沙箱一起结束 |
| `--seccomp FD` | 从文件描述符读入编译好的 seccomp 过滤器 |

参数按顺序生效：先 `--ro-bind / /`，再把可写目录 `--bind` 回来，最后用 `--tmpfs` 盖住要隐藏的路径。

## 局限

- 依赖非特权 user namespace，被禁用时直接失败，嵌套在另一个沙箱里也常失败。
- 没有网络之后若要按域名放行，需要另外搭[出网代理](../ai-agents/sandboxing/egress-proxy.md)。

## 相关

- [Namespace](namespaces.md)
- [Claude Code 的沙箱](../ai-agents/sandboxing/claude-code.md)
- [Codex 的沙箱](../ai-agents/sandboxing/codex.md)
