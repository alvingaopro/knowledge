---
title: Namespace
description: Linux namespace 是什么，每种隔离什么，为什么沙箱和容器都依赖它
type: explanation
tags: [linux, isolation, sandbox]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://man7.org/linux/man-pages/man7/namespaces.7.html
---

Namespace 给一组进程发一份内核全局资源的**私有副本**。进程不是被禁止访问宿主的东西，而是根本看不到它们。

## 是什么

内核里很多东西原本全机只有一份：进程列表、挂载好的文件系统、网卡、主机名。把进程放进新的 namespace，它看到的就是这份资源的另一个副本。可以想成给进程戴一副眼镜，镜片里只显示允许它看到的那部分世界。

容器（Docker、Podman）和 agent 沙箱（[bubblewrap](bubblewrap.md)）用的都是这套机制，区别只在于搭得多重。

## 八种 namespace

| 类型 | 隔离什么 | 在沙箱里的典型用途 |
| --- | --- | --- |
| `mnt` | 挂载点，也就是文件树长什么样 | 重新拼文件树：根目录只读挂载，工作目录可写，敏感目录用空目录盖住 |
| `pid` | 进程编号和可见的进程 | 看不到、也杀不了宿主进程；第一个进程编号是 1 |
| `net` | 网卡、路由表、端口 | 只剩回环网卡 `lo`，无法直连外网 |
| `user` | 用户编号和权限归属 | 让普通用户有资格创建其他 namespace，见 [user namespace](user-namespaces.md) |
| `uts` | 主机名、域名 | 很少需要 |
| `ipc` | System V 共享内存、消息队列 | 防止跨沙箱共享内存 |
| `cgroup` | 能看到的 cgroup 层级 | 容器常用；cgroup 本身才负责限 CPU、内存 |
| `time` | 单调时钟的偏移 | 很少需要 |

## 怎么创建和观察

- 系统调用：`clone(2)` 创建子进程时带上 `CLONE_NEW*` 标志，或用 `unshare(2)` 让当前进程脱离原 namespace，`setns(2)` 加入已有的。
- 命令行：`unshare`、[`bwrap`](bubblewrap.md)、`nsenter`。
- 观察：`/proc/<pid>/ns/` 下每一项指向一个 namespace，方括号里是编号；编号相同即同一个 namespace。详见[从 /proc 观察](procfs-isolation-inspection.md)。

```sh
# 不需要 root（依赖 user namespace）
unshare --user --map-root-user --pid --fork --mount-proc ps -ef   # 只看到两个进程
unshare --user --map-root-user --net ip link                      # 只有 lo，且是 DOWN
```

## 它不管什么

Namespace 只决定“看到什么”。资源用量（CPU、内存、进程数）归 cgroup 管；能调用哪些系统调用归 [seccomp](seccomp.md) 管；有没有特权归 [capability](capabilities.md) 管。

## 相关

- [User namespace](user-namespaces.md)
- [bubblewrap](bubblewrap.md)
