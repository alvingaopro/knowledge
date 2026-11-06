---
title: 从 /proc 观察进程的隔离状态
description: 用 ps、/proc/self/ns、/proc/self/status 等判断自己是否在沙箱里、被限制了什么
type: how-to
tags: [linux, sandbox, debugging]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://man7.org/linux/man-pages/man5/proc.5.html
---

`/proc` 是内核提供的虚拟目录，里面的“文件”是进程的实时信息；`/proc/self` 指当前进程自己。下面几条命令合起来，就能判断一个 shell 是否在沙箱里、被限制了什么。

## 一组检查命令

```sh
ps -eo pid,args | head                    # 看得到多少进程，PID 1 是谁
ls -l /proc/self/ns                       # 属于哪些 namespace
cat /proc/self/uid_map                    # 用户编号怎么映射
cat /proc/net/dev                         # 有哪些网卡
grep -E 'Cap|NoNewPrivs|Seccomp' /proc/self/status
env | grep -i _proxy                      # 网络是否被导向代理
```

## 怎么读

### 进程列表

宿主上通常有几百个进程。如果只看到自己这条命令链上的几个，并且 PID 1 不是 `systemd`/`init`，说明在新的 pid [namespace](namespaces.md) 里。

### `/proc/self/ns`

```text
cgroup -> cgroup:[4026531835]
ipc    -> ipc:[4026531839]
mnt    -> mnt:[4026533631]
pid    -> pid:[4026533632]
user   -> user:[4026533630]
uts    -> uts:[4026531838]
```

方括号里是 namespace 编号，相同即同一个 namespace。内核给“开机时那一份”（初始 namespace）中的 user、pid、uts、ipc、cgroup、time 分配了固定编号 `4026531834`–`4026531839`。看到这个范围的数，就是和宿主共用；其他编号说明是新建的。mnt 和 net 的初始编号是动态分配的，要靠别的证据判断（例如网卡列表）。

### `uid_map`

三列：namespace 内起始编号、宿主起始编号、数量。`1000 1000 1` 表示沙箱里仍是你本人，不是 root。见 [user namespace](user-namespaces.md)。

### `/proc/net/dev`

只有 `lo` 说明在新的 net namespace 里，没有直连外网的网卡。

### `/proc/self/status`

| 字段 | 沙箱里常见值 | 含义 |
| --- | --- | --- |
| `CapEff` / `CapPrm` | `0` | 没有任何特权能力，见 [capability](capabilities.md) |
| `NoNewPrivs` | `1` | 无法通过 setuid 程序提权，见 [NoNewPrivs](no-new-privs.md) |
| `Seccomp` | `2` | 装了系统调用过滤器，见 [seccomp](seccomp.md) |
| `Seccomp_filters` | `≥1` | 叠了几层过滤器 |

单独一项说明不了问题（普通 shell 的 `CapEff` 也是 0），要几项一起看。

## 实例

[解读一个正在运行的 agent 沙箱](../ai-agents/sandboxing/lab-inspecting-a-live-sandbox.md)用这套命令逐条分析了 Claude Code 的沙箱。
