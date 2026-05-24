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

Do not delete `/var/lib/opencloud/nats` or disable NATS KV persistence for OpenCloud POSIX storage. The ID cache is
required to resolve existing spaces after restarts.

## Docker live restore

`docker_daemon_options.live-restore=true` keeps containers running across Docker daemon restarts. After daemon option
changes, containers with published ports may still need explicit relaunch/recreate for new networking behavior to apply.

## Traefik CrowdSec

Keep the Traefik CrowdSec middleware as the real plugin and keep `/plugins-storage` persistent. Do not replace it with a
permanent no-op fallback; only use no-op live config as a temporary emergency recovery step.
