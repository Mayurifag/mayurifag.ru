# Post Install Instructions

This document outlines the manual steps required to configure services after
the Ansible deployment is complete.

## DNS / Email Routing

DNS is managed by the `traefik` role (subtag `dns`). It owns:

- `A @` and `A *` (DNS-only, points at server IP)
- `TXT @` SPF: `v=spf1 include:_spf.mx.cloudflare.net -all`
  (CF Email Routing forwards only; everyone else hard-rejected)
- `TXT _dmarc` (patched in place: enforces `p=reject; sp=reject` + strict
  alignment, preserves CF-generated rua UUID)
- Cloudflare Email Routing enable + catch-all `*@domain` -> `admin_email`

Cloudflare auto-manages MX and DKIM records (the role never touches them).
DMARC Management owns the rua UUID; the role only patches the policy fields
around it. Posture: domain receives mail via CF Routing, sends nothing.

Note: SPF task uses `solo: true` on `@` — any other apex TXT will be
deleted. Place unrelated verifications (Google site, etc.) under
different subdomains.

### Required Cloudflare API token scopes

Token at <https://dash.cloudflare.com/profile/api-tokens>:

- Zone    : DNS                     : Edit (LE DNS-01 + A/DMARC records)
- Zone    : Email Routing Rules     : Edit (catch-all rule)
- Account : Email Routing Addresses : Edit (destination state)

## NetBird with Tinyauth

NetBird's embedded identity provider remains the issuer for its dashboard and
clients. Tinyauth is an external login option; creating a Tinyauth OIDC client
alone does not register it with NetBird. Additional apps can use another entry
in `tinyauth_oidc_clients`; Google sign-in remains configured once in Tinyauth.

1. Deploy `traefik`, `tinyauth`, and `netbird` on the target host. Finish
   NetBird's initial owner setup through its dashboard if needed.
2. In NetBird, open **Settings → Identity Providers → Add Identity Provider**.
   Choose **Generic OIDC**. Use name `Tinyauth`, client ID from
   `tinyauth_oidc_clients.netbird.client_id`, issuer
   `https://{{ tinyauth_subdomain }}.{{ server_hostname }}`, and client secret
   stored on the host at
   `{{ tinyauth_data_directory }}/netbird-oidc-client-secret`.
3. Copy the exact callback URL shown by NetBird into
   `tinyauth_oidc_clients.netbird.redirect_uri` in production inventory. For
   `nnnnn.cfd`, it is `https://netbird.nnnnn.cfd/oauth2/callback`.
4. `netbird_local_auth_disabled: true` removes email login. With one external
   provider, NetBird redirects directly to Tinyauth. Ensure a Tinyauth user has
   **Owner** access before applying this to an existing NetBird installation.

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
