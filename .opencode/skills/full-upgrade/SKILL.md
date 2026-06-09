---
name: full-upgrade
description: Use ONLY for /full-upgrade or full Docker service/container upgrades across this repo's production servers.
---

# Full Upgrade

A request to fully upgrade Docker containers across servers is high-risk. Do not mutate servers before an explicit approved plan.

Discovery phase:

- Inspect every production host read-only over SSH: running containers, images, compose/Ansible source, pinned tags, Watchtower labels, healthchecks, restart counts, current versions, resource usage, recent logs, kernel/OS/package versions, and non-container software managed by Ansible.
- Distinguish auto-updated components from components that are not auto-updated. Produce a per-host list with service/component name, current version/tag/digest, latest upstream stable version/tag/digest, owning role, update mechanism, and risk notes.
- A full Docker/service upgrade means checking every configured image tag/version and every configured plugin/extension/package/software version in the repo, then updating Ansible defaults/tasks/templates to newer upstream stable versions when they exist. This includes Traefik plugins such as the CrowdSec bouncer plugin, app-specific plugins/extensions, downloaded binaries, apt packages pinned by repo configuration, kernel/OS upgrade paths, and other non-Watchtower-managed software. Do not treat "current digest for the existing tag" as enough.
- It is normal for some roles/services to be deployed only on specific hosts. Use each host's effective inventory variables and runtime state to decide whether a service is expected there; do not mark a role missing on one host as anomalous just because it exists elsewhere in the repo.
- Do not include already-current images in the upgrade-candidate list. Mention them only if they have risk notes, health anomalies, or explain why no action is needed for a user-visible question.
- Use subagents per server when useful. Each subagent must inspect only its assigned server and return findings, unknowns, and proposed service order.
- Research every non-auto-updated service before planning changes. Check upstream release notes/changelogs, migration guides, breaking changes, deprecations, image/tag changes, config/env changes, database/storage migrations, and relevant GitHub issues/discussions.

Host aliases and read-only debug commands:

- Use inventory aliases as canonical host names, but do not write real aliases in notes or examples.
- Prefer Ansible inventory lookup before raw SSH when host details are unknown: `make hosts`.
- Raw SSH debug must be read-only and use `RemoteCommand=none`; derive concrete targets from inventory or SSH config only when executing commands.
- Container summary: `docker ps --all --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"`.
- Runtime/image/health summary: `docker inspect $(docker ps -aq) --format "{{.Name}} image={{.Config.Image}} imageID={{.Image}} restart={{.RestartCount}} state={{.State.Status}} health={{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}} watchtower={{index .Config.Labels \"com.centurylinklabs.watchtower.enable\"}}"`.
- Local image digests: `docker images --digests --format "{{.Repository}}:{{.Tag}} digest={{.Digest}} id={{.ID}} created={{.CreatedSince}}"`.
- Resource snapshot: `docker stats --no-stream --format "{{.Name}} cpu={{.CPUPerc}} mem={{.MemUsage}} net={{.NetIO}} block={{.BlockIO}}"` and `docker system df`.
- Recent logs: `for c in $(docker ps --format "{{.Names}}"); do printf "LOGS %s\n" "$c"; docker logs --since 2h --tail 80 "$c" 2>&1; done`.
- CrowdSec/Traefik bouncer diagnosis: `docker exec crowdsec cscli bouncers list`; `docker logs --since 30m traefik 2>&1 | grep -E "CrowdsecBouncer|crowdsec|appsec|403|unreachable"`; `docker logs --since 30m crowdsec 2>&1 | grep -E "7422|appsec|Crowdsec-Bouncer-Traefik|403"`.
- Remote tag check without pulling: `docker buildx imagetools inspect <image>:<tag>`.

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
