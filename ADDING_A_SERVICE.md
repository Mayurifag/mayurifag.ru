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

## 5. Homepage Integration

The service should be discoverable and linkable on the Homepage dashboard via Docker labels.

- `homepage.group`: A meaningful group name (e.g., "Services", "Infrastructure").
- `homepage.name`: Display name of the service.
- `homepage.href`: Full URL, typically `https://{{ app_name_subdomain }}.{{ server_hostname }}`.
- `homepage.icon`: **CRITICAL: Icon Policy**
  - The icon name **must** be one of the following:
    - A filename (e.g., `vaultwarden.svg`) that exists in the **Homarr Dashboard Icons** repository: [https://github.com/homarr-labs/dashboard-icons/tree/main/svg](https://github.com/homarr-labs/dashboard-icons/tree/main/svg).
    - A Material Design Icon (MDI) name prefixed with `mdi-`. Use the search tool at [https://dashboardicons.com/](https://dashboardicons.com/) to find the name (look for MDI icons).
      - **Example 1 (Existing Icon)**: `homepage.icon: "netdata.svg"`
      - **Example 2 (MDI Icon)**: `homepage.icon: "mdi-cloud-outline"` (for a generic cloud app if no dedicated icon exists).
  - **Do not use** a custom file name (e.g., `app_name.png`) unless it is explicitly an approved Homarr/Homepage icon name.

## 6. Global File Updates

- `inventories/sample/group_vars/sample.yml`: Add/uncomment the `<app_name>_enabled: true` and any required `app_name_*` variables.
- `README.md`: Update the **Applications List** table.
