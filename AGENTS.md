# Instructions

## General Repo Rules

Docker-published ports must bind to loopback with `127.0.0.1:host:container`
unless intentionally public. Public exceptions require a matching UFW allow rule;
current baseline public ports are SSH, Traefik `80/tcp`, `443/tcp`, `443/udp`,
and 3x-ui Hysteria2 UDP.

Add `no_log: true` to Ansible tasks that include API tokens, passwords, bearer
tokens, private keys, or generated secrets in module arguments.

`debug on <name>` = read-only ssh inspection on host reachable via `ssh <name>`. Run diagnostic commands only (logs, status, configs). Never mutate server state. For changes, edit ansible files in repo and deploy via `make deploy <role>`. You maybe need to override `RemoteCommand=none`.

Do not expose real SSH host aliases in instructions, skills, docs, or examples. Use placeholders like `<host>` or `<production-host>`; discover concrete aliases from inventory only when executing commands.

`inventories/sample/group_vars/all.yml` and `inventories/my-provision/group_vars/all.yml` must stay structurally identical (same keys, order, comments). Only values differ: sample uses `change_this`/placeholders, my-provision holds real production values. When editing one, mirror the change in the other and dont forget to encrypt file back.

Use lazy loading for detailed repo-specific rules. When a task matches one of the references below, read only the relevant file before acting. Treat loaded rules as mandatory repo instructions.

Load these files only when relevant:

- OpenCloud config, POSIX storage, NATS state -> `./airules/opencloud.md`
- Docker daemon options, live restore -> `./airules/docker.md`
- Traefik CrowdSec plugin and Traefik startup warnings -> `./airules/traefik.md`

If several areas apply, load all matching files. Do not preemptively load unrelated rule files.

## sshconfig bootstrap general VPS server to needed state

`make sshconfig` is first-bootstrap only for hosts still on provider SSH. Never run it on a ready host; use the inventory SSH port and a narrowly scoped Ansible deploy for ready-host SSH changes. It is meant to only run once per server as first ansible setup run.

Do not edit `sshconfig.yml` unless the user explicitly asks. It must stay minimal: only enough setup to make the main Ansible provisioning applicable.
