# Homelab

Proxmox on the ThinkPad, with Home Assistant OS (VM 100) and Immich on Debian (VM 101).
Guests use `vmbr0`, `10.10.10.0/24`, and routed NAT through Wi-Fi. Gateway/DNS: `10.10.10.1`.

## Applications

- [Proxmox](https://proxmox.home.mayurifag.ru): host HTTPS on `8006`.
- [Home Assistant](https://ha.home.mayurifag.ru): `10.10.10.20:80`.
- [Immich](https://immich.home.mayurifag.ru): `10.10.10.30:80`; machine learning disabled.

Native Traefik handles HTTPS on Proxmox. Wildcard DNS points to its NetBird address.
Clients need NetBird and membership in `remote-admins`. LAN-only access needs a local DNS override.
Certificates use Cloudflare DNS-01; no WAN forwarding is needed.

## Deployment

Inventory groups: `homelab`, `homelab_immich`, and `homelab_home_assistant`.
Unlock git-crypt first. Use inventory host names; never run VPS bootstrap on Proxmox.

~~~sh
make ci
make deploy homelab_access HOST='<host>'
make deploy homelab_host HOST='<host>'
make deploy homelab_proxy HOST='<host>'
make deploy home_assistant HOST='<ha-guest>'
make deploy immich HOST='<photo-guest>'
~~~

- `homelab_access`: NetBird HTTPS policy and Home Assistant trusted proxy.
- `homelab_host`: laptop power policy, DHCP/DNS, existing VM resources and startup.
- `homelab_proxy`: Traefik, private firewall access, DNS and TLS.
- `home_assistant`: YAML from `homelab/home-assistant/`; validates before restart and rolls back failures.
- `immich`: requires the existing database/library; recreates containers only when needed. Do not also use Compose.
- Reboot: `make deploy homelab_reboot HOST='<host>'`. Create/restore VMs through Proxmox.

## Data and configuration

- Immich library: `/srv/immich/library` on its mounted photo disk. Database: `/var/lib/immich/postgres`.
- Traefik certificates: `/var/lib/traefik-home/acme.json`. Keep backups outside Git and off the laptop.
- Home Assistant UI state, integrations and secrets stay outside Git. Reconcile UI-created YAML before deploying.
- Guest SSH uses `ProxyCommand` through Proxmox; NetBird SSH does not support `ProxyJump`. Pin guest host keys in inventory.
- Home Assistant uses Terminal & SSH on port `2222` with key authentication. The role keeps `python3` in its `apks` list.

## Local quirks

- Home Assistant serves HTTP on **80**. HTTP proxy settings live in Settings > System > Network, not YAML.
- DNS interception requires the production Traefik propagation override: 30-second delay, local checks disabled.
- Proxmox owns firewall-file permissions. Create missing `host.fw` through `pvesh`; do not chmod it.
