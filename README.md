# Ansible playbook for provisioning mayurifag.ru

[![Linters](https://github.com/Mayurifag/mayurifag.ru/actions/workflows/lint.yml/badge.svg)](https://github.com/Mayurifag/mayurifag.ru/actions/workflows/lint.yml)

## Requires

### VPS

* DNS `A` records for your TLD and wildcard (`*`)
* Debian 12+
* Open ports on server provider' side

### Mac/PC

* Ansible `python3 -m pip install --user ansible`
* (only MacOS) - passlib `python3 -m pip install --user passlib` (to use crypto
  module from ansible)
* Setup inventory (if key not added, be prepared to add ansible_ssh_pass and
  that after general server setup)

## Instructions

### Initial setup

~~~sh
git clone https://github.com/Mayurifag/mayurifag.ru.git
cd mayurifag.ru
cp -rfp inventories/sample inventories/my-provision
# Now you are required to change my-provision files.
# or ln from some place like that:
# ln -s /Volumes/exfat/OpenCloud/Personal/Software/dotfiles/my-provision/ inventories/my-provision
# Dont forget you are required to generate ssh key and copy public into provision
ansible-galaxy install -r requirements.yml
~~~

### Production deployment

#### TL;DR

~~~sh
make boostrap # run once, its cleaning known_hosts and makes ssh configuration
make deploy "traefik,mus" # or make deploy-all if you are sure
~~~

#### Optional steps

* Make new ssh config section for convenience and using tmux by default

~~~sh
# ~/.ssh/config
Host change_that
    HostName change.that
    User admin_user # Change user
    Port 2222 # change port
    RequestTTY yes
    RemoteCommand tmux attach -d || tmux new-session -s main
~~~

## Applications List

This list changed a lot through years, I'm trying to remove things I do not use.

<!-- markdownlint-disable line-length -->

| Name                | Subdomain    | Auth | Watchtower |
| :------------------ | :----------- | ---- | ---------- |
| 3proxy              |              | app  | +          |
| 3x-ui               | `3x`         | app  |            |
| BentoPDF            | `pdf`        | ldap | +          |
| ConvertX            | `convert`    | ldap | +          |
| Gitea               | `git`        | todo |            |
| Homepage.dev        | `home`       | ldap | +          |
| MkDocs              | `docs`       | ldap | +          |
| Mini-QR             | `qr`         | ldap | +          |
| mayurifag.github.io | `<TLD>`      | ldap | +          |
| mus                 | `mus`        | ldap | +          |
| Navidrome           | `navidrome`  | app  | +          |
| lldap               | `ldap`       | ldap | +          |
| OpenCloud           | `cloud`      | ldap |            |
| Portainer           | `portainer`  | app  | +          |
| TG AI Manager       | `tg`         | ldap | +          |
| Traefik / Crowdsec  | `traefik`    | ldap |            |
| Tinyauth            | `auth`       | ldap | +          |
| Watchtower HTTP API | `watchtower` | app  | +          |

<!-- markdownlint-enable line-length -->

Refer to [POST_INSTALL.md](./POST_INSTALL.md) for after deployment info.

## TODO

### Work is not in progress

The work is not in progress now, because I am okay with current implementation,
but still I think there are some things existing for further development if I'll
need to deploy my services once again.

### List

* [ ] <https://github.com/we-promise/sure> - or its alternatives
  * [ ] Has to support crypto, ibkr, russian brokers
  * [ ] Is it possible to have data in opencloud?
* [ ] Bentopdf to stirlingpdf? Something which easily makes edits.
  * [ ] Check locally first before deploy on some pdf invoice
* [ ] Crowdsec iptables firewall - remediation component.
  * [ ] traefik and crowdsec have to be in a single role - too much connected
  * [ ] Crowdsec has to be inside traefik role
  * [ ] <https://www.crowdsec.net/blog/secure-docker-compose-stacks-with-crowdsec>
  * [ ] see if there is solution to unban false positive and if not, add smth

### Thinking if I need it / On hold / probably wont do - ideas / notes

* [ ] Add simple secret sharing app
  * [ ] Hemmelig - too much things, analytics and so on
  * [ ] also maybe url shorten like <https://github.com/anhostfr/nah.pet>
* [ ] <https://github.com/pranshuparmar/witr> - wait debian repos to include it
* [ ] Bandwhich - will require downloading binary to root - wait for deb repo
* [ ] When Tinyauth will be an OIDC provider
  * [ ] make it work for opencloud
  * [ ] Portainer - setup automatic LDAP
* [ ] Watchtowerrr
  * [ ] use config.json for auth to dockerhub to prevent limits
  * [ ] use metrics for homepage <https://gethomepage.dev/widgets/services/watchtower/>
* [ ] VPS security
  * [ ] Kernel params to have less /var/log/syslog noise - add to crowdsec btw
  * [ ] <https://madaidans-insecurities.github.io/guides/linux-hardening.html>
  * [ ] (wait for update) <https://github.com/docker/docker-bench-security>
  * [ ] (not sure) <https://github.com/quay/clair>
  * [ ] Make connection to docker through proxy fluencelabs/docker-socket-proxy
  * [ ] <https://github.com/imthenachoman/How-To-Secure-A-Linux-Server>
* [ ] Homepage.dev ideas
  * [ ] redesign
  * [ ] Stocks SPY/QQQ - requires finnhub api key
  * [ ] World clock? moscow time
  * [ ] For crowdsec - link to <https://app.crowdsec.net/>
* [ ] Status page for services
  * [ ] Has to be free and allow deploy from ansible via API
  * [ ] maybe just main website check and self service to report docker unhealth
  * [ ] <https://beszel.dev/>
* [ ] tmux
  * [ ] add dracula disk usage (used/total) or totally redesign it
  * [ ] tmux with `nice` priority <https://x.com/SA5280/status/2001732941639282759>
* [ ] Traefik
  * [ ] Update 3.6.4 was breaking change, test with opencloud
  * [ ] tracing/observability tests with my apps
  * [ ] No AI Bots Middleware with robots.txt - plugin install
* [ ] ufw
  * [ ] Waiting for <https://github.com/shinebayar-g/ufw-docker-automated>
  * [ ] Problem for docker is that on server reboot or else address of docker
        container is changing so rules have to be updated
  * [ ] Block everything. There are a lot of exceptions: ssh/web/dns/dhcp/ntp
  * [ ] open port if needed in each ansible role
  * [ ] IP Masquerading ?
  * [ ] research <https://github.com/capnspacehook/whalewall> (not updated though)
* [ ] zerobyte - webapp for restic backups - wait until developed
