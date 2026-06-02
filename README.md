# Ansible playbook for provisioning my servers

[![Linters](https://github.com/Mayurifag/mayurifag.ru/actions/workflows/lint.yml/badge.svg)](https://github.com/Mayurifag/mayurifag.ru/actions/workflows/lint.yml)

## Requirements

On VPS - Debian 12+.
On VPS provider - opened ports
On Cloudflare - token (DNS propagated during setup)
On PC - just `ansible`. For MacOS also `passlib` because of some `crypto` module.

## Instructions

### Initial setup

~~~sh
git clone https://github.com/Mayurifag/mayurifag.ru.git
cd mayurifag.ru
cp -rfp inventories/sample inventories/my-provision # and change it directly
ansible-galaxy install -r requirements.yml
~~~

### Production deployment

#### TL;DR

~~~sh
make boostrap hostname # run once, its cleaning known_hosts and makes ssh configuration
make deploy hostname "traefik,mus" # or make deploy-all if you are sure
~~~

#### Optional steps

* Make new ssh config section for convenience and using tssh' udp by default

~~~sh
# ~/.ssh/config
Host change_that_provider change_that_website.com
    HostName change.that
    User admin_user # Change user
    Port 2222 # change port
    #!! UdpMode KCP
    #!! TsshdPort 12345 # change this
~~~

## Applications List

This list changed a lot through years, I'm trying to remove things I do not use.

<!-- markdownlint-disable line-length -->

| Name                | Subdomain    | Auth | Watchtower |
| :------------------ | :----------- | ---- | ---------- |
| 3x-ui               | `3x`         | app  |            |
| BentoPDF            | `pdf`        | ldap | +          |
| Beszel              | `beszel`     | app  | +          |
| ConvertX            | `convert`    | ldap | +          |
| EchoIP              | `ip`         | none | +          |
| Gitea               | `git`        | app  |            |
| Dynacat             | `rss`        | ldap | +          |
| Mini-QR             | `qr`         | ldap | +          |
| mayurifag.github.io |              | none | +          |
| mus                 | `mus`        | ldap | +          |
| Navidrome           | `navidrome`  | app  | +          |
| lldap               | `ldap`       | ldap | +          |
| OpenCloud           | `cloud`      | ldap |            |
| Portainer           | `portainer`  | app  | +          |
| SnapOtter           | `images`     | ldap | +          |
| TG AI Manager       | `tg`         | ldap | +          |
| Traefik / Crowdsec  | `traefik`    | ldap |            |
| Tinyauth            | `auth`       | ldap | +          |
| Watchtower HTTP API | `watchtower` | app  | +          |

<!-- markdownlint-enable line-length -->

Refer to [POST_INSTALL.md](./POST_INSTALL.md) for after deployment info.

## TODO

* [ ] Migrate to debian 13
  * [ ] Upgrade everything
  * [ ] OpenSSH: add `PerSourcePenalties`, stricter other options
  * [ ] cheatsheet on ssh opening.
    * [ ] Output CPU/RAM/disk usage.
    * [ ] dumbfile size and aliases. Other useful aliases. What else?
  * [ ] dysk instead of default du dh??

### On hold

* [ ] <https://github.com/pranshuparmar/witr> - wait debian repos to include it
* [ ] Bandwhich - will require downloading binary to root - wait for deb repo
* [ ] When Tinyauth will be an OIDC provider
  * [ ] make it work for opencloud
  * [ ] Portainer - setup automatic LDAP
* [ ] zerobyte - webapp for restic backups - wait until developed stable version
* [ ] Track finances selfhosted
  * [ ] Has to support auto import crypto, ibkr, russian brokers, banks, georgian banks - no way today
  * [ ] Save data to opencloud
  * [ ] <https://github.com/we-promise/sure>
* [ ] ufw
  * [ ] Waiting for <https://github.com/shinebayar-g/ufw-docker-automated>
  * [ ] Problem for docker is that on server reboot or else address of docker container is changing so rules have to be
        updated
  * [ ] Block everything. There are a lot of exceptions: ssh/web/dns/dhcp/ntp
  * [ ] open port if needed in each ansible role
  * [ ] IP Masquerading ?
  * [ ] research <https://github.com/capnspacehook/whalewall> (not updated though)

### Thinking if I need it / probably wont do - ideas / notes

* [ ] try <https://dockhand.pro/manual/> for possible portainer alternative
  * [ ] For now i think no need until replaces watchtower API
* [ ] try <https://github.com/stalwartlabs/stalwart> for email
  * [ ] Extract dns into another role?
* [ ] Add simple secret sharing app
  * [ ] Hemmelig - too much things, analytics and so on
  * [ ] also maybe url shorten like <https://github.com/anhostfr/nah.pet>
  * [ ] I also might need to share files
  * [ ] <https://github.com/Luzifer/ots> seems fine
* [ ] Watchtowerrr
  * [ ] use config.json for auth to dockerhub to prevent limits
* [ ] VPS security
  * [ ] Kernel params to have less /var/log/syslog noise - add to crowdsec btw
  * [ ] <https://madaidans-insecurities.github.io/guides/linux-hardening.html>
  * [ ] (wait for update) <https://github.com/docker/docker-bench-security>
  * [ ] (not sure) <https://github.com/quay/clair>
  * [ ] Make connection to docker through proxy fluencelabs/docker-socket-proxy
  * [ ] <https://github.com/imthenachoman/How-To-Secure-A-Linux-Server>
* [ ] SSH tunnel/bastion
  * [ ] Cloudflare + tailscale ips only.
  * [ ] Is it compatible with ansible deployment then?
  * [ ] 443 traffic might be gone through cloudflare proxy then
  * [ ] Whitelist for cf/tailscale, more enforcing rules for spammers
  * [ ] cf rules for spammers?
  * [ ] proxies-cfg will work fine? ssh with proxies?
* [ ] Grimmory - for Kindle KOReader - sync progress and books download
