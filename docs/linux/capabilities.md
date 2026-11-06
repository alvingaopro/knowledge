---
title: Capability
description: Linux 把 root 权限拆成的小块，以及如何读 /proc 里的能力位图
type: explanation
tags: [linux, security, privileges]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://man7.org/linux/man-pages/man7/capabilities.7.html
---

Capability 把 root 的特权拆成四十来个独立的能力；进程只拿到需要的那几个，而不是全有或全无。

## 是什么

例如：

| 能力 | 允许做什么 |
| --- | --- |
| `CAP_SYS_ADMIN` | 挂载文件系统等大量管理操作（常被称为“新的 root”） |
| `CAP_NET_ADMIN` | 修改网卡、路由、防火墙 |
| `CAP_NET_BIND_SERVICE` | 监听 1024 以下端口 |
| `CAP_DAC_OVERRIDE` | 无视文件读写权限 |
| `CAP_SETUID` | 任意切换用户编号 |

## 五组集合

`/proc/<pid>/status` 里有五行，每行是十六进制位图，每一位代表一种能力：

| 字段 | 含义 |
| --- | --- |
| `CapEff` | Effective，此刻真正生效、内核检查的那组 |
| `CapPrm` | Permitted，允许拥有的上限，Eff 只能从这里取 |
| `CapInh` | Inheritable，执行新程序时可以继承的 |
| `CapBnd` | Bounding，整个进程树的天花板，只能缩小 |
| `CapAmb` | Ambient，普通程序执行时也能保留的 |

用 `capsh --decode=000001ffffffffff` 可以把位图翻译成能力名。

## 在沙箱里怎么用

[bubblewrap](bubblewrap.md) 在 [user namespace](user-namespaces.md) 里搭笼子时临时拥有全部能力，搭完后全部丢掉，再执行目标命令。所以沙箱内常见：

```text
CapPrm: 0000000000000000
CapEff: 0000000000000000
CapBnd: 000001ffffffffff
```

`CapBnd` 全是 1 没关系：Prm 和 Eff 都是 0，再配合 [NoNewPrivs](no-new-privs.md)，拿不回来。

注意：宿主上普通用户的 shell `CapEff` 本来也是 0。这一行本身不能证明在沙箱里，要结合 [namespace](namespaces.md) 和 [seccomp](seccomp.md) 一起看。

## 相关

- [NoNewPrivs](no-new-privs.md)
- [从 /proc 观察](procfs-isolation-inspection.md)
