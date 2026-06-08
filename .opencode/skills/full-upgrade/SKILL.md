---
name: full-upgrade
description: Use ONLY for /full-upgrade or full Docker service/container upgrades across this repo's production servers.
---

# Full Upgrade

A request to fully upgrade Docker containers across servers is high-risk. Do not mutate servers before an explicit approved plan.

Discovery phase:

- Inspect every production host read-only over SSH: running containers, images, compose/Ansible source, pinned tags, Watchtower labels, healthchecks, restart counts, current versions, resource usage, and recent logs.
- Distinguish auto-updated containers from containers that are not auto-updated. Produce a per-host list with service name, current image/tag/digest, latest upstream stable tag/digest, owning role, update mechanism, and risk notes.
- A full Docker upgrade means checking every configured image tag/version in the repo and updating the Ansible defaults/tasks to newer upstream stable tags when they exist. Do not treat "current digest for the existing tag" as enough.
- Use subagents per server when useful. Each subagent must inspect only its assigned server and return findings, unknowns, and proposed service order.
- Research every non-auto-updated service before planning changes. Check upstream release notes/changelogs, migration guides, breaking changes, deprecations, image/tag changes, config/env changes, database/storage migrations, and relevant GitHub issues/discussions.

Plan phase:

- Present the full upgrade plan and wait for explicit approval before editing repo files, deploying, restarting containers, or changing server state.
- Plan must go host-by-host from smaller/lower-risk server to bigger/higher-risk server, then service-by-service from least critical/stateless to most critical/stateful.
- Plan must include exact repo files to edit, deploy commands, rollback path, expected downtime, data backup/snapshot needs, and service-specific verification steps.

Execution after approval:

- Edit Ansible/inventory/templates in repo; do not live-edit containers or deployed configs except for read-only diagnosis.
- Run repo validation, usually `make ci`, before deployment unless the approved plan explicitly narrows validation.
- Deploy one service/role on one host at a time, starting with the smaller/lower-risk host.
- After each service deploy, verify container health/status, restart count, image version/digest, exposed ports, HTTP/TCP probes where applicable, dependent services, recent logs, Docker events, CPU, memory, disk, network, and host load.
- Watch for anomalies before continuing: crash loops, healthcheck failures, migration errors, auth failures, elevated 4xx/5xx, log spam, resource spikes, missing volumes, permission errors, or changed startup warnings.
- If an anomaly appears, stop rollout, diagnose, and either fix via repo/deploy or ask for approval to roll back. Do not continue to the next host or service while the current one is unhealthy.
- Keep notes of what changed and the observed post-deploy state for each service.
