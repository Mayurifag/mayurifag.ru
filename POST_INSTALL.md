# Post Install Instructions

This document outlines the manual steps required to configure services after
the Ansible deployment is complete.

## CrowdSec

If you provided a valid `crowdsec_enroll_key` in `group_vars`, the deployment
should automatically enroll your instance to the
[CrowdSec Console](https://app.crowdsec.net/).

## OpenCloud

Make sure that Personal space is generated. Things I have to restore:

- Obsidian (also update in docs)
- ejson folder ln
- my-provision folder ln
- Windows Portable apps shortcuts
- Windows - Available offline for Personal space
- Webdav requires token for now. Restore mobiles

## 3x-ui (Xray)

Reality SNI target may stop working over time (e.g. `live.vkvideo.ru`
is dead). Pick another if so.

### 1. Login

Default `admin` / `admin` at
`https://{{ threexui_panel_subdomain }}.{{ server_hostname }}`.

- Change credentials.
- **Subscription -> Reverse Proxy URI:**
  `https://{{ threexui_panel_subdomain }}.{{ server_hostname }}/sub/`.

### 2. VLESS Reality (TCP/443)

**Inbounds -> Add Inbound**:

- Protocol `vless`, Port `443`, Security `reality`.
- Flow `xtls-rprx-vision`, Transmission `XHTTP`.
- Target + SNI: `{{ threexui_reality_domain }}`.
- Get new private key. Save.

### 3. Hysteria 2 (UDP/`{{ threexui_hysteria2_port }}`)

Verify dumped certs:

~~~bash
docker exec 3x-ui ls /root/cert/certs /root/cert/private
~~~

Expect `{{ server_hostname }}.crt` in `certs/` and `.key` in `private/`. If
missing: check `docker logs traefik-certs-dumper` and
`docker logs traefik | grep acme`.

**Inbounds -> Add Inbound**:

- Protocol `hysteria2`, Port `{{ threexui_hysteria2_port }}`.
- Client -> Email -> set something
- Stream Settings -> Final Mask -> UDP Masks -> `+` -> Type `salamander`,
  password = random 16+ chars.
- Masquerade `proxy`, URL `https://{{ server_hostname }}`,
  rewriteHost `true`.
- Cert `/root/cert/certs/{{ server_hostname }}.crt`,
  key `/root/cert/private/{{ server_hostname }}.key`,
  SNI `{{ server_hostname }}`.
- Bandwidth: leave default. Don't crank Brutal.
- Save.

Subscribe in [Happ](https://www.happ.su/main/). Both inbounds in one sub.

## Gitea

Requires setup after installation:

- Create admin user
- Add SSH and GPG keys
