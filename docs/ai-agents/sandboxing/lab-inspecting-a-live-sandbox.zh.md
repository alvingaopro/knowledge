---
title: 解读一个正在运行的沙箱
description: 在 Claude Code 的 Linux 沙箱里逐条运行检查命令，并解释每一项输出
type: tutorial
tags: [ai-agents, claude-code, sandbox, linux]
created: 2026-11-06
updated: 2026-11-06
---

在 Claude Code 开启沙箱时，让它用 Bash 运行下面的命令。以下输出来自 2026-11 的一次真实会话（Linux，Claude Code + sandbox-runtime），个人信息和凭据已去掉。方法见[从 /proc 观察](../../linux/procfs-isolation-inspection.md)。

## 1. 进程列表

```console
$ ps -eo pid,args
PID COMMAND
  1 apply-seccomp /usr/bin/zsh -c …
  2 /usr/bin/zsh -c …
  3 ps -eo pid,args
```

- 只看到自己这条命令链：在新的 pid [namespace](../../linux/namespaces.md) 里。
- PID 1 是 `apply-seccomp`，sandbox-runtime 的小程序：装好 [seccomp](../../linux/seccomp.md) 过滤器后把 zsh 作为子进程（PID 2）启动，自己留下当 1 号进程。过滤器会遗传给之后的每条命令。
- **意味着**：命令看不到、也杀不了编辑器、浏览器等宿主进程。

## 2. Namespace

```console
$ ls -l /proc/self/ns
cgroup -> cgroup:[4026531835]
ipc    -> ipc:[4026531839]
mnt    -> mnt:[4026533631]
net    -> net:[4026533029]
pid    -> pid:[4026533632]
time   -> time:[4026531834]
user   -> user:[4026533630]
uts    -> uts:[4026531838]
```

- cgroup、ipc、time、uts 落在初始 namespace 的固定编号 `4026531834`–`4026531839` 内：与宿主共用。
- user、mnt、pid 是一组紧挨着的新编号：同时新建。net 也是新的，见下一步。

## 3. 网卡

```console
$ cat /proc/net/dev
Inter-|   Receive …
 face |bytes …
    lo:       0 …
```

只有 `lo`，没有 `eth0`：命令没有直连外网的路径，只能走[出网代理](egress-proxy.md)。

## 4. 身份

```console
$ id
uid=1000(<user>) gid=1000(<user>) …
$ cat /proc/self/uid_map
      1000       1000          1
```

沙箱里仍是你本人，不是 root；新建的文件在宿主上也属于你。见 [user namespace](../../linux/user-namespaces.md)。

## 5. 权限与过滤器

```console
$ grep -E 'Cap|NoNewPrivs|Seccomp' /proc/self/status
CapInh: 0000000000000000
CapPrm: 0000000000000000
CapEff: 0000000000000000
CapBnd: 000001ffffffffff
CapAmb: 0000000000000000
NoNewPrivs:      1
Seccomp:         2
Seccomp_filters: 2
```

- 没有任何生效的 [capability](../../linux/capabilities.md)；`CapBnd` 是上限，手里一个没有就无所谓。
- [NoNewPrivs](../../linux/no-new-privs.md) 已打开：`sudo` 无法提权。
- `Seccomp: 2` 是过滤模式，叠了两层过滤器。

## 6. 网络配置

```console
$ env | grep -i _proxy | sed 's/=.*@/=***@/'
HTTPS_PROXY=***@127.0.0.1:3128
ALL_PROXY=***@127.0.0.1:3128
…
```

各类代理变量都指向沙箱内的本地端口；`GIT_SSH_COMMAND` 也被设置成让 ssh 经代理连接。变量里带一次性代理凭据，不要原样打印或提交。

## 7. 撞墙实验

```sh
touch ./ok.txt                 # 成功
touch ~/outside.txt            # Read-only file system
echo x >> .claude/settings.json  # 工作目录内也被拒：防止 agent 改自己的配置
ls ~/.ssh                      # 被拒或看不到
curl -sI https://github.com    # 在白名单内则成功
curl -sI https://example.org   # 被代理拒绝或触发询问
python3 -c "import socket;socket.create_connection(('1.1.1.1',53),3)"  # 无网卡，失败
```

## 8. 嵌套沙箱

```console
$ codex sandbox -- true
bwrap: No permissions to create new namespace …
```

外层沙箱禁止再建 [user namespace](../../linux/user-namespaces.md)，内层的 bwrap 直接失败。Codex 的实验要在普通终端里做。
