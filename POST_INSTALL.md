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

Be absolutely sure the domain you picked SNI into is fine with that. Sometimes
that just wont work, i.e. you cant use <live.vkvideo.ru> as SNI target now.

### 1. Default Credentials

By default, the 3x-ui panel is deployed with insecure credentials.

- **Username**: `admin`
- **Password**: `admin`

**Action Required**:

- Log in to the panel (default URL: `https://3x.mayurifag.local`).
- Go to **Panel Settings**.
- **Authentication** -> Change the Username and Password immediately.
- **Subscription** -> `Reverse Proxy URI` to `https://3x.mayurifag.local/sub/`

### 2. VLESS Reality XTLS Setup

**Panel Configuration**:

Navigate to **Inbounds** -> **Add Inbound**.

Configure the inbound with these specific settings:

- **Protocol**: `vless`
- **Listening Port**: `443`
- **Security**: `reality`
- Client -> Email: `username`; **Flow**: `xtls-rprx-vision`.
- **Transmission**: `XHTTP`
- **Target**: `learn.microsoft.com:443` (from `threexui_reality_domain`).
- **SNI**: `learn.microsoft.com` (Must match `Dest` domain).
- **Private Key**: Click **Get New Key**.
- **Save**.

Then just use subscription with [Happ](https://www.happ.su/main/).

There is also some
[tuning](https://vc.ru/id206643/2149746-nastroika-3x-ui-bez-oshibok) available.
