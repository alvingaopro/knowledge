---
title: seccomp
description: 用 BPF 过滤器检查进程的每一次系统调用
type: explanation
tags: [linux, security, sandbox]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://man7.org/linux/man-pages/man2/seccomp.2.html
  - https://docs.kernel.org/userspace-api/seccomp_filter.html
---

seccomp（secure computing）让进程给自己装一段过滤程序，每次系统调用先经过它：放行、返回错误，或者杀掉进程。

## 先理解系统调用

程序要做任何实际的事，比如打开文件、建立网络连接、启动新程序，都必须请内核代办，这个请求就叫系统调用（syscall），例如 `openat`、`connect`、`execve`、`socket`。拦住系统调用，就拦住了程序能做的事，不论它用什么语言写、命令怎么拼。

## 两种模式

| `/proc/<pid>/status` 的 `Seccomp` | 含义 |
| --- | --- |
| `0` | 未启用 |
| `1` | strict 模式：只允许 `read`、`write`、`exit`、`sigreturn` |
| `2` | filter 模式：装了自定义的 BPF 过滤器 |

`Seccomp_filters: N` 表示叠了几层过滤器；每次系统调用要依次通过所有层，结果取最严格的那个。

## 过滤器的性质

- 检查的是系统调用编号和参数的**数值**（例如 `socket` 的第一个参数是不是 `AF_UNIX`），不能解引用指针，所以不能按文件路径过滤；按路径限制要靠 [mount namespace](namespaces.md) 或 [Landlock](landlock.md)。
- 只能叠加，不能卸载。
- 通过 `fork`、`execve` 遗传给所有子孙。
- 普通用户安装前必须先打开 [NoNewPrivs](no-new-privs.md)。

## 在 agent 沙箱里的用途

Claude Code 的 Linux 沙箱用 seccomp 禁止新建 Unix socket。Unix socket 是本机进程间通信用的“插座文件”。不禁止的话，命令可以绕过[出网代理](../ai-agents/sandboxing/egress-proxy.md)，直接连宿主上的 `docker.sock` 这类 socket，等于拿到笼外的控制权。

Docker 也默认装一份 seccomp 配置，禁掉四十多个危险系统调用。

## 相关

- [NoNewPrivs](no-new-privs.md)
- [bubblewrap](bubblewrap.md)
