# Adding a New Service (AI Assistant Guide)

This document serves as a reference guide for the AI assistant on the preferred structure and standards when adding a new Dockerized application/service to this Ansible repository.

## 1. Create Ansible Role

A new application requires a dedicated Ansible role.

- **Example** of directory structure: `roles/<app_name>/defaults/main.yml`, `roles/<app_name>/tasks/main.yml`, and optionally `roles/<app_name>/templates/`.
- Add the new role to `provisioning.yml` in the `Provisioning` block, ensuring it has an appropriate tag and `when` condition.

## 2. Role Variables (`defaults/main.yml`)

Define all configuration variables here. The following are **examples** of required variables:

- `app_name_enabled`: Boolean to enable/disable the app (e.g., `true`).
- `app_name_subdomain`: The subdomain for the service (e.g., `"app"`).
- `app_name_image`: The Docker image to use (e.g., `"user/image:latest"`).
- `app_name_memory`: The container memory limit (e.g., `"512m"`).
- `app_name_data_directory`: The host path for persistent data (e.g., `"{{ docker_home }}/<app_name>"`).

## 3. Main Tasks (`tasks/main.yml`)

This file contains the deployment logic.

- **Directory Creation**: Ensure necessary host directories (e.g., `app_name_data_directory`) are created.
- **Docker Container**: Use `community.docker.docker_container`.
  - Set `name`, `image`, `pull: true`, `recreate: true`, `restart_policy: unless-stopped`.
  - Configure `volumes` and `memory`.
  - **Networking**: Containers exposed by Traefik **must** be connected to the `web` network: `networks: [ { name: "web" } ]`. This is the designated network for Traefik routing.

## 4. Traefik Labels

All web-facing applications must be configured with Traefik labels in the `docker_container` task.

- `traefik.enable: "true"`
- `traefik.http.routers.<app_name>.rule`: `Host(\`{{ app_name_subdomain }}.{{ server_hostname }}\`)`
- `traefik.http.services.<app_name>.loadbalancer.server.port`: The internal port of the container.
- **Middlewares**: At minimum, include `secure-headers@file`. If the service is meant for authenticated users, include `tinyauth@docker`.
  - Example: `traefik.http.routers.<app_name>.middlewares: "tinyauth@docker,secure-headers@file"`
- `com.centurylinklabs.watchtower.enable: "true"` - you may add it only if service does not requires too much hussle on update. 100% if it is stateless or it is not very important or complex.

## 5. Global File Updates

- `inventories/sample/group_vars/sample.yml`: Add/uncomment the `<app_name>_enabled: true` and any required `app_name_*` variables.
- `README.md`: Update the **Applications List** table.
