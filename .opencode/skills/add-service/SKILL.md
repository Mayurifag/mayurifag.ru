---
name: add-service
description: Use ONLY for adding a new Dockerized service/app role to this Ansible repo, including /add-service requests.
---

# Add Service

When adding a new service, implement it through Ansible only. Do not live-edit production hosts.

Required repo changes:

- Create `roles/<service>/defaults/main.yml` and `roles/<service>/tasks/main.yml`; add `templates/` only when needed.
- Add the role to `provisioning.yml` with a tag and `when: <service>_enabled`.
- Define defaults: `<service>_enabled`, `<service>_subdomain`, `<service>_image`, `<service>_memory`, `<service>_data_directory`, and service-specific config.
- In tasks, create persistent directories before starting containers.
- Use `community.docker.docker_container` with `pull: true`, `recreate: true`, `restart_policy: unless-stopped`, volumes, memory, and labels.
- Exposed HTTP services must join Docker network `web` for Traefik.
- Add Traefik labels: `traefik.enable`, router host rule, service port, and middlewares.
- Use `secure-headers@file` for web services; add `tinyauth@docker` for private services.
- Add `com.centurylinklabs.watchtower.enable: "true"` only for low-risk/stateless or simple-update services.
- Update both inventory group vars with identical keys/order/comments when new global vars are needed.
- Update `README.md` application list.
- Run repo validation, usually `make ci`.

Respect repo rules: keep sample and real inventory structures identical, encrypt real inventory back if changed, and deploy via `make deploy <role>` only after repo changes are validated.
