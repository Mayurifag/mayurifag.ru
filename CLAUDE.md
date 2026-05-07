# Repo Rules

## Debug on servers

`debug on <name>` = read-only ssh inspection on host reachable via `ssh <name>`. Run diagnostic commands only (logs, status, configs). Never mutate server state. For changes, edit ansible files in repo and deploy via `make deploy <role>`.
