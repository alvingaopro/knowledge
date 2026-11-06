---
title: User namespace
description: 为什么普通用户不用 sudo 也能创建沙箱，以及它为什么会失败
type: explanation
tags: [linux, isolation, sandbox]
created: 2026-11-06
updated: 2026-11-06
sources:
  - https://man7.org/linux/man-pages/man7/user_namespaces.7.html
---

User namespace 让普通用户建一个“小世界”，在里面拥有管理员权限，从而能创建其他 [namespace](namespaces.md)；这些权限对宿主无效。

## 为什么需要它

创建 mnt、net、pid namespace 原本需要 `CAP_SYS_ADMIN`，也就是 root。User namespace 是例外：普通用户就能创建，而且创建者在新 namespace 里自动拥有全部 [capability](capabilities.md)。有了这份“小世界里的特权”，就能继续创建其他 namespace、做挂载。

这正是 [bubblewrap](bubblewrap.md) 不需要 setuid 或 sudo 的原因。

## 用户编号的映射

User namespace 内的 uid 要映射到宿主的 uid，记录在 `/proc/<pid>/uid_map`，三列分别是：namespace 内起始编号、宿主上起始编号、数量。

```text
1000  1000  1      # 内部 1000 就是宿主 1000，只映射一个：沙箱里还是你本人
   0  1000  1      # unshare --map-root-user：内部显示为 root，实际是宿主的 1000
```

所以 `unshare --user --map-root-user id` 会显示 `uid=0(root)`，但 `touch /etc/x` 仍然被拒绝：对宿主文件，你依旧是 1000。

## 为什么会失败

报错 `No permissions to create new namespace` 或 `Operation not permitted`，常见原因：

- 已经在另一个沙箱里，外层禁止再建 user namespace（嵌套沙箱）。
- 发行版关闭了非特权 user namespace，例如 `kernel.unprivileged_userns_clone=0`，或 Ubuntu 24.04 起的 AppArmor 限制 `kernel.apparmor_restrict_unprivileged_userns=1`。
- 容器运行时的默认 seccomp 配置禁止 `unshare`/`clone` 的相关标志。

## 安全上的代价

User namespace 让普通用户能接触到原本只有 root 才能触发的内核代码路径，历史上是不少提权漏洞的入口。这也是部分发行版默认收紧它的原因。

## 相关

- [Namespace](namespaces.md)
- [Capability](capabilities.md)
