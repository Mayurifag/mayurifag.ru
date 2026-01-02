# Post Install Instructions

This document outlines the manual steps required to configure services after
the Ansible deployment is complete.

## CrowdSec

If you provided a valid `crowdsec_enroll_key` in `group_vars`, the deployment
should automatically enroll your instance to the
[CrowdSec Console](https://app.crowdsec.net/).

## Linkding

Install the browser extension:

- [Chrome](https://chrome.google.com/webstore/detail/linkding-extension/beakmhbijpdhipnjhnclmhgjlddhidpe)
- [Firefox](https://addons.mozilla.org/en-US/firefox/addon/linkding-extension/).

It will require to setup token: `/admin/authtoken/tokenproxy/1/change/`

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
- Go to **Settings** (or Panel Settings).
- Change the Username and Password immediately.
- Set **Subscription**: `Proxy URL` to `https://3x.mayurifag.local/sub/`

### 2. VLESS Reality XTLS Setup

**Panel Configuration**:

Navigate to **Inbounds** -> **Add Inbound**.

Configure the inbound with these specific settings:

- **Protocol**: `vless`
- **Listening Port**: `443`
- **Security**: `reality`
- Client ->  **Flow**: `xtls-rprx-vision`.
- **Transmission**: `XHTTP`
- **Dest**: `learn.microsoft.com:443` (from `threexui_reality_domain`).
- **Server Names**: `learn.microsoft.com` (Must match `Dest` domain).
- **uTLS**: `chrome`.
- **Private Key**: Click **Get New Key**.
- **Save**.

Then just use subscription with [Happ](https://www.happ.su/main/)
