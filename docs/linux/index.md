---
title: Linux
description: Linux 内核的隔离与权限机制
---

Linux 内核没有一个叫“沙箱”的功能。沙箱、容器都是把下面这些互相独立的机制拼起来用的。

## 隔离：进程能看到什么

- [Namespace](namespaces.md)：给进程一份自己的进程列表、文件树、网络
- [User namespace](user-namespaces.md)：让普通用户也能创建其他 namespace

## 权限：进程能做什么

- [Capability](capabilities.md)：被拆成小块的 root 权限
- [NoNewPrivs](no-new-privs.md)：禁止进程以后再变强
- [seccomp](seccomp.md)：给系统调用加过滤器
- [Landlock](landlock.md)：普通用户自己限制能访问的文件

## 工具与观察

- [bubblewrap](bubblewrap.md)：把以上机制组合成一个轻量沙箱的命令行工具
- [从 /proc 看一个进程的隔离状态](procfs-isolation-inspection.md)

## 建议阅读顺序

namespace → user namespace → capability → NoNewPrivs → seccomp → bubblewrap → 用 /proc 观察。
