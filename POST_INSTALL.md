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
