# OpenCloud Rules

Keep `STORAGE_USERS_POSIX_WATCH_FS=true`: other services, including mus, write into the same files tree and OpenCloud must notice external filesystem changes.

OpenCloud/Reva's default inotify watcher ignores `STORAGE_USERS_POSIX_WATCH_PATH` and watches `STORAGE_USERS_POSIX_ROOT`. Current production preference is `STORAGE_USERS_POSIX_PROPAGATOR=sync`; async wrote `/storage/changes/*` inside the watched root and caused watcher churn/log spam.

Do not delete `/var/lib/opencloud/nats` or disable NATS KV persistence for OpenCloud POSIX storage during normal deploys. Use `opencloud_reset_state=true` only for a deliberate fresh-state repair.

OpenCloud config is stored in inventory files at `inventories/<inventory>/files/opencloud.yaml`. Deploys must run `opencloud init --diff` against that inventory config before replacing the container and fail if OpenCloud wants to change the config; update the inventory config with the full diff first.
