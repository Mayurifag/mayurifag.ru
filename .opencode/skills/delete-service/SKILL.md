---
name: delete-service
description: Use ONLY for /delete-service, deleting a service from this repo, destructive cleanup, service removal, or removing a role/app from Ansible and production hosts.
---

# Delete Service

Deleting a service/role/app is destructive. Before editing or mutating servers, present a concrete plan and wait for explicit user approval.

Approved deletion plan must cover:

- Remove all repo references: playbooks, roles, defaults, inventory vars, templates, docs, scripts, tests.
- Preserve inventory parity between sample and my-provision files.
- Run repo validation, usually `make ci`.
- Clean leftovers on both production hosts: stop/remove containers, remove service data dirs, remove service Docker images, deployed config references, and service-specific UFW rules.
- Deploy affected roles after config/template removals, for example `make deploy HOST=<inventory-alias> <role>`.
- Verify both hosts have no service containers, images, data dirs, deployed config references, exposed ports, or stale UFW allow rules left.
- Never delete unrelated shared/persistent data unless the user explicitly names it in the approved plan.
