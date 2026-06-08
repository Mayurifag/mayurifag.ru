# Instructions

## General Repo Rules

`debug on <name>` = read-only ssh inspection on host reachable via `ssh <name>`. Run diagnostic commands only (logs, status, configs). Never mutate server state. For changes, edit ansible files in repo and deploy via `make deploy <role>`. You maybe need to override `RemoteCommand=none`.

`inventories/sample/group_vars/all.yml` and `inventories/my-provision/group_vars/all.yml` must stay structurally identical (same keys, order, comments). Only values differ: sample uses `change_this`/placeholders, my-provision holds real production values. When editing one, mirror the change in the other and dont forget to encrypt file back.

`make sshconfig` is first-bootstrap only for hosts still on provider SSH. Never run it on a ready host; use the inventory SSH port and a narrowly scoped Ansible deploy for ready-host SSH changes.

Use lazy loading for detailed repo-specific rules. When a task matches one of the references below, read only the relevant file before acting. Treat loaded rules as mandatory repo instructions.

Load these files only when relevant:

- OpenCloud config, POSIX storage, NATS state -> `./airules/opencloud.md`
- Docker daemon options, live restore -> `./airules/docker.md`
- Traefik CrowdSec plugin and Traefik startup warnings -> `./airules/traefik.md`

If several areas apply, load all matching files. Do not preemptively load unrelated rule files.
