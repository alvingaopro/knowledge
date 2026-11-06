---
title: NoNewPrivs
description: 一个让进程及其子孙永远无法通过 setuid 程序提权的标志
type: explanation
tags: [linux, security, privileges]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://docs.kernel.org/userspace-api/no_new_privs.html
---

NoNewPrivs 是进程上的一个标志：打开后，这个进程和它所有的子孙在执行新程序时都不能获得额外权限，而且无法关闭。

## 解决什么问题

`sudo`、`su`、`passwd` 这类 setuid 程序执行时会变成文件属主（通常是 root）的身份；带文件 capability 的程序执行时会获得那些能力。沙箱里如果还留着这条路，前面的限制就可能被绕过。

打开 NoNewPrivs 之后：

- setuid / setgid 位被忽略，`sudo` 无法变成 root。
- 文件 capability 不生效。
- 标志遗传给所有子进程，`fork` 和 `execve` 都去不掉。

## 怎么设置和查看

```c
prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
```

```sh
grep NoNewPrivs /proc/self/status   # 1 表示已打开
setpriv --no-new-privs bash         # 命令行设置
```

## 和 seccomp 的关系

内核规定：没有 `CAP_SYS_ADMIN` 的进程，必须先打开 NoNewPrivs 才能安装 [seccomp](seccomp.md) 过滤器。否则一个进程可以先装一个让系统调用行为异常的过滤器，再去执行 setuid 程序，诱导它出错。所以沙箱里这两项几乎总是一起出现。

## 相关

- [Capability](capabilities.md)
- [seccomp](seccomp.md)
