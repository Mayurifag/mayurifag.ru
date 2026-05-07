# Repo Rules

## Debug on servers

`debug on <name>` = read-only ssh inspection on host reachable via `ssh <name>`. Run diagnostic commands only (logs, status, configs). Never mutate server state. For changes, edit ansible files in repo and deploy via `make deploy <role>`.

## Inventory parity

`inventories/sample/group_vars/all.yml` and `inventories/my-provision/group_vars/all.yml` must stay structurally identical (same keys, order, comments). Only values differ: sample uses `change_this`/placeholders, my-provision holds real production values. When editing one, mirror the change in the other and dont forget to encrypt file back.
