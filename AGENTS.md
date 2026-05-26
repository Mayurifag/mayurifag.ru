# Debug on servers

`debug on <name>` = read-only ssh inspection on host reachable via `ssh <name>`. Run diagnostic commands only (logs,
status, configs). Never mutate server state. For changes, edit ansible files in repo and deploy via
`make deploy <role>`. You maybe need to override `RemoteCommand=none`.

## Inventory parity

`inventories/sample/group_vars/all.yml` and `inventories/my-provision/group_vars/all.yml` must stay structurally
identical (same keys, order, comments). Only values differ: sample uses `change_this`/placeholders, my-provision holds
real production values. When editing one, mirror the change in the other and dont forget to encrypt file back.

## OpenCloud storage

Keep `STORAGE_USERS_POSIX_WATCH_FS=true`: other services, including mus, write into the same files tree and OpenCloud
must notice external filesystem changes.

OpenCloud/Reva's default inotify watcher ignores `STORAGE_USERS_POSIX_WATCH_PATH` and watches `STORAGE_USERS_POSIX_ROOT`.
Current production preference is `STORAGE_USERS_POSIX_PROPAGATOR=async`; async writes `/storage/changes/*` inside the watched
root and can cause watcher churn/log spam, so revisit this first if those logs return.

Do not delete `/var/lib/opencloud/nats` or disable NATS KV persistence for OpenCloud POSIX storage. The ID cache is
required to resolve existing spaces after restarts.

OpenCloud config is stored in inventory files at `inventories/<inventory>/files/opencloud.yaml`. Deploys must run
`opencloud init --diff` against that inventory config before replacing the container and fail if OpenCloud wants to
change the config; update the inventory config with the full diff first.

## Docker live restore

`docker_daemon_options.live-restore=true` keeps containers running across Docker daemon restarts. After daemon option
changes, containers with published ports may still need explicit relaunch/recreate for new networking behavior to apply.

## SSH config

`make sshconfig` is first-bootstrap only for hosts still on provider SSH. Never run it on a ready host; use the inventory
SSH port and a narrowly scoped Ansible deploy for ready-host SSH changes.

## Traefik CrowdSec

Keep the Traefik CrowdSec middleware as the real plugin and keep `/plugins-storage` persistent. Do not replace it with a
permanent no-op fallback; only use no-op live config as a temporary emergency recovery step.

Traefik v3.7 prints the encoded-character startup warning unconditionally upstream; config cannot remove it. Do not hide it
by lowering log verbosity.
