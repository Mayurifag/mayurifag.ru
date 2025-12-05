# Post Install Instructions

This document outlines the manual steps required to configure services after
the Ansible deployment is complete.

## CrowdSec

If you provided a valid `crowdsec_enroll_key` in `group_vars`, the deployment
should automatically enroll your instance to the
[CrowdSec Console](https://app.crowdsec.net/).

## 3x-ui (Xray)

### 1. Default Credentials

By default, the 3x-ui panel is deployed with insecure credentials.

* **Username**: `admin`
* **Password**: `admin`

**Action Required**:

1. Log in to the panel (default URL: `https://3x.mayurifag.local`).
2. Go to **Settings** (or Panel Settings).
3. Change the Username and Password immediately.
4. Restart the panel if prompted.

### 2. VLESS Reality XTLS Setup

To enable the stealth proxy that works behind Traefik on port 443, follow these
steps strictly.

**Panel Configuration**:

Navigate to **Inbounds** -> **Add Inbound**.

Configure the inbound with these specific settings:

* **Remark**: `Reality-TCP`
* **Protocol**: `vless`
* **Listening Port**: `443`
* **Network**: `tcp`
* **Security**: `reality`
* **Dest**: `learn.microsoft.com:443` (from `threexui_reality_domain`).
* **Server Names**: `learn.microsoft.com` (Must match `Dest` domain).
* **uTLS**: `chrome`.
* **Private Key**: Click **Get New Key**.
* **Flow**: `xtls-rprx-vision`.
