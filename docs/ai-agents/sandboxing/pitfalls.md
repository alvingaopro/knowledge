---
title: 沙箱的常见坑
description: agent 沙箱里常见的失败现象、原因和处理办法
type: reference
tags: [ai-agents, sandbox, debugging]
created: 2026-11-06
updated: 2026-11-06
---

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| git worktree 里提交报 `index.lock: Read-only file system` | worktree 的 index 和 refs 在主仓库的 `.git` 目录，不在工作目录下 | 把主仓库的公共 git 目录加入可写路径，但保持它的 `config` 和 `hooks` 只读，防止植入在沙箱外执行的代码 |
| 提交身份、`pushInsteadOf` 等配置悄悄失效 | Git 读不到 `[include]` 的文件时静默跳过；被包含的文件在拒读名单里 | 把需要的配置放到可读位置，或用环境变量（`GIT_AUTHOR_NAME` 等）传入 |
| `git push` 走 SSH 失败 | SSH 不是 HTTP，默认不经过[出网代理](egress-proxy.md) | 改用 HTTPS remote，或用 `GIT_SSH_COMMAND` 让 ssh 通过代理 `CONNECT`，或把命令排除出沙箱 |
| 连不上 `docker.sock`、ssh-agent、数据库 socket | [seccomp](../../linux/seccomp.md) 禁止新建 Unix socket，且这些路径没挂进来 | 显式放开指定 socket；注意 `docker.sock` 等于宿主 root |
| `bwrap: No permissions to create new namespace` | 已在另一个沙箱里，或系统禁用了非特权 [user namespace](../../linux/user-namespaces.md) | 在外层运行；检查 `kernel.apparmor_restrict_unprivileged_userns` 等设置 |
| 某个工具连不上网，curl 却可以 | 该工具不读 `HTTPS_PROXY` 等环境变量 | 查工具自己的代理配置项 |
| 测试都过了，真实任务失败 | 测试只在临时目录里跑，临时目录本来就可写 | 用与真实环境相同的目录布局测试 |
| 以为文件工具也被隔离了 | 沙箱只包 shell 命令，内置文件工具、MCP、hook 不在其中 | 用权限规则约束这些工具，见[两道闸](permissions-vs-sandbox.md) |
| 命令把机器跑满 | 沙箱不限制 CPU、内存、进程数 | 需要时另外用 cgroup / `systemd-run --user -p MemoryMax=` |
