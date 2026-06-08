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
- Clean leftovers on both production hosts, `nnnnn` and `mayurifag`: stop/remove containers, remove service data dirs, remove service Docker images, and remove deployed config references.
- Deploy affected roles after config/template removals, for example `make deploy HOST=nnnnn <role>` and `make deploy HOST=mayurifag <role>`.
- Verify both hosts have no service containers, images, data dirs, or deployed config references left.
- Never delete unrelated shared/persistent data unless the user explicitly names it in the approved plan.
