# Debug on servers

`debug on <name>` = read-only ssh inspection on host reachable via `ssh <name>`. Run diagnostic commands only (logs,
status, configs). Never mutate server state. For changes, edit ansible files in repo and deploy via
`make deploy <role>`. You maybe need to override `RemoteCommand=none`.

## Inventory parity

`inventories/sample/group_vars/all.yml` and `inventories/my-provision/group_vars/all.yml` must stay structurally
identical (same keys, order, comments). Only values differ: sample uses `change_this`/placeholders, my-provision holds
real production values. When editing one, mirror the change in the other and dont forget to encrypt file back.

## OpenCloud NATS

OpenCloud uses external `opencloud-nats`; do not delete NATS storage in normal deploys. Inspect pressure with
`docker run --rm --network web natsio/nats-box:latest sh -lc 'nats --server nats://opencloud-nats:4222 stream report && nats --server nats://opencloud-nats:4222 consumer report main-queue'`.
`KV_ids-storage-users` is expected to dominate because POSIX watcher/id-cache writes inode mappings there.

Browser/app profile folders in OpenCloud storage are intentional. When debugging POSIX watcher/cache noise from volatile
profile files, prefer mitigations that keep those folders in OpenCloud instead of recommending removal as the primary
fix.
