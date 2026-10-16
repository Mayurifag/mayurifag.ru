# Homelab

Proxmox on the ThinkPad, with Home Assistant OS (VM 100) and Immich on Debian (VM 101).
Guests use `vmbr0`, `10.10.10.0/24`, and routed NAT through Wi-Fi. Gateway/DNS: `10.10.10.1`.

## Applications

- [Proxmox](https://proxmox.home.mayurifag.ru): host HTTPS on `8006`.
- [Home Assistant](https://ha.home.mayurifag.ru): `10.10.10.20:80`.
- [Immich](https://immich.home.mayurifag.ru): `10.10.10.30:80`; machine learning disabled.
- [Qwen](https://qwen.home.mayurifag.ru): Open WebUI on the Strix Halo NetBird peer; start it with `qwen`.

Native Traefik handles HTTPS on Proxmox. Wildcard DNS points to its NetBird address.
Clients need NetBird and membership in `remote-admins`. LAN-only access needs a local DNS override.
Certificates use Cloudflare DNS-01; no WAN forwarding is needed.
Start Qwen before deploying `homelab_proxy` when its route is enabled.

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
- `homelab_netbird`: only NetBird policies, including proxy-only Qwen backend access on TCP 3000.
- `homelab_host`: laptop power policy, guest DHCP/DNS, private LAN DNS, VM resources and startup.
- `homelab_proxy`: Traefik, private firewall access, DNS and TLS.
- `homelab_monitoring`: guest private DNS and HA-only HTTPS access; deploy on the hypervisor without changing VM resources or requiring Qwen to be running.
- `home_assistant`: YAML from `homelab/home-assistant/`; validates before restart and rolls back failures.
- `immich`: requires the existing database/library; recreates containers only when needed. Do not also use Compose.
- Reboot: `make deploy homelab_reboot HOST='<host>'`. Create/restore VMs through Proxmox.

## Apple Home

- HomeKit Bridge exports only the two Antikomarinka scenario switches from `homelab/home-assistant/configuration.yaml`; raw plugs and technical controls stay in Home Assistant.
- `make deploy homelab_homekit HOST='<host>'` configures LAN-only TCP `21063` forwarding and an Avahi `_hap._tcp` reflector between Wi-Fi and `vmbr0`.
- Reserve the Proxmox Wi-Fi address in router DHCP. HomeKit `advertise_ip` must match `homelab_proxy_lan_address`.
- Pair through Apple Home using the QR code in Home Assistant notifications. Do not add a second UI-created bridge.
- Antikomarinka scenario switches use each plug's native eight-hour countdown, not a volatile script delay. Their state follows the plug and countdown after Home Assistant restarts.

## Home Dashboard

- `/homelab-dashboard/overview` is the owner's landing page. `Slate Studio` is a native dark-only theme; both preferences are saved in frontend user data, not just browser storage.
- Service checks poll once per minute with TLS validation: Proxmox web UI and Immich API ping. They do not assert VM/database health. Qwen is an on-demand link, not an always-on health check.
- Resource tiles use native Supervisor diagnostics: Core CPU/RAM and HA OS data-disk total/used/free. Enable these entities in the entity registry; they describe VM 100, not physical Proxmox resources.
- Guest DNS shares the LAN override for the private domain. Private HTTPS permits the HA guest's single IP (`10.10.10.20/32`); no public port is opened.
- Unknown automatic-backup times and the offline cabinet plug remain visible. The dashboard does not start backups, update software, or toggle plugs automatically.

## Robot Vacuum

- Xiaomi S20 uses Xiaomi Miot in Singapore (`sg`) cloud mode, assigned to Home Assistant's Kitchen area. Account credentials and integration state stay outside Git.
- The `home_assistant` role manages the pinned upstream revision and checksum, without HACS. The pin includes PR #2948's verification signing fix, absent from release `v1.1.5`.
- `/vacuum-dashboard/s20` provides a saved map, status, settings, and room scripts. Positional labels follow the diagram: Upper Right = `10`, Middle Right = `11`, Left / Lower = `12`; the dock borders `12`. Recheck IDs after remapping. Live maps remain in Xiaomi Home.
- The map snapshot is encrypted at `inventories/my-provision/files/s20-room-map.png` and deployed to `/media/s20-room-map.png`. The dashboard uses native authenticated media storage, not public `/local` files. This snapshot is not auto-updated.
- Firmware rejects direct room-name lookup. Existing encrypted map uploads can supply names and outlines through `/v2/home/get_interim_file_url_pro` with object `<owner_uid>/<did>/0` (or slot `1`), decoded with the Ijai parser. Keep signed URLs and floorplans private; do not trigger map uploads just to read metadata.

## Data and configuration

- Immich library: `/srv/immich/library` on its mounted photo disk. Database: `/var/lib/immich/postgres`.
- Traefik certificates: `/var/lib/traefik-home/acme.json`. Keep backups outside Git and off the laptop.
- Home Assistant UI state, integrations and secrets stay outside Git. Reconcile UI-created YAML before deploying.
- Core and the owner's saved frontend language are Russian (`ru`). Profile locale is server-side `frontend` user data under key `language`; browser-only `selectedLanguage` is not sufficient. Vacuum dashboard labels and the private map snapshot are also localized.
- Guest SSH uses `ProxyCommand` through Proxmox; NetBird SSH does not support `ProxyJump`. Pin guest host keys in inventory.
- Home Assistant uses Terminal & SSH on port `2222` with key authentication. The role keeps `python3` in its `apks` list.

## Local quirks

- Home Assistant serves HTTP on **80**. HTTP proxy settings live in Settings > System > Network, not YAML.
- LAN dnsmasq maps `*.home.mayurifag.ru` to the reserved Proxmox Wi-Fi IP. Configure router DHCP to advertise that IP as its only DNS server; router remains the DHCP server.
- DNS interception requires the production Traefik propagation override: 30-second delay, local checks disabled.
- Proxmox owns firewall-file permissions. Create missing `host.fw` through `pvesh`; do not chmod it.
