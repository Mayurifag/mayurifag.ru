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
| BentoPDF            | `pdf`        | ldap | +          |
| ConvertX            | `convert`    | ldap | +          |
| Gitea               | `git`        | todo |            |
| Homepage.dev        | `home`       | ldap | +          |
| Linkding            | `bookmarks`  | app  | +          |
| Mini-QR             | `qr`         | ldap | +          |
| mayurifag.github.io | `<TLD>`      | ldap | +          |
| mus                 | `mus`        | ldap | +          |
| lldap               | `ldap`       | ldap | +          |
| OpenCloud           | `cloud`      | ldap |            |
| Portainer           | `portainer`  | app  | +          |
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

* [ ] ufw
  * [ ] ufw - for docker too <https://github.com/HexmosTech/udwall>
  * [ ] Block everything except ssh. Check ufw status and allowances
  * [ ] open port if needed in each ansible role
  * [ ] IP Masquerading ?
* [ ] Replace 3x-ui with remnawave completely
  * [ ] Make sure subscription is working
  * [ ] Information about client apps (win/linux/macos/android/ios)
  * [ ] How can I easily deploy nodes to multiple servers with current setup?
  * [ ] Scripts to automate setup
* [ ] Homepage has to contain processes monitoring - glances?
* [ ] maybe finance app - deprecated, so research alternatives.
  * [ ] Has to support crypto, ibkr, russian brokers
  * [ ] <https://github.com/we-promise/sure>
  * [ ] Is it possible to have data in opencloud?
* [ ] Bentopdf to stirlingpdf? Something which easily makes edits.
* [ ] Crowdsec iptables firewall - remediation component.
  * [ ] traefik and crowdsec have to be in a single role - too much connected
  * [ ] Crowdsec has to be inside traefik role
  * [ ] <https://www.crowdsec.net/blog/secure-docker-compose-stacks-with-crowdsec>
  * [ ] see if there is solution to unban false positive and if not, add smth

### Thinking if I need it / probably wont do ideas / notes

* [ ] Add simple secret sharing app
  * [ ] Hemmelig - too much things, analytics and so on
* [ ] <https://github.com/pranshuparmar/witr> - from official repos
* [ ] general role has too much things inside it, split it
* [ ] When Tinyauth will be an OIDC provider
  * [ ] make it work for opencloud
  * [ ] Portainer - setup automatic LDAP
  * [ ] Linkding
* [ ] Traefik
  * [ ] Update 3.6.4 was breaking change, test with opencloud
  * [ ] tracing/observability tests with my apps
  * [ ] No AI Bots Middleware with robots.txt - plugin install
  * [ ] To use LDAP auth onto opencloud and so on I have to use
        <https://github.com/wiltonsr/ldapAuth> though I dont want to commit that
* [ ] Watchtowerrr
  * [ ] use config.json for auth to dockerhub to prevent limits
  * [ ] use metrics for homepage <https://gethomepage.dev/widgets/services/watchtower/>
  * [ ] actually maybe migrate <https://getwud.github.io/wud> but it will
        require to change webhook on mayurifag.github.io and mus. But more
        maintained and includes nice web ui
* [ ] <https://github.com/binwiederhier/ntfy>
* [ ] docker image of mayurifag.github.io has to be in ghcr like mus
* [ ] VPS security
  * [ ] Kernel params to have less /var/log/syslog noise - add to crowdsec btw
  * [ ] <https://madaidans-insecurities.github.io/guides/linux-hardening.html>
  * [ ] (wait for update) <https://github.com/docker/docker-bench-security>
  * [ ] (not sure) <https://github.com/quay/clair>
  * [ ] Make connection to docker through proxy fluencelabs/docker-socket-proxy
  * [ ] <https://github.com/imthenachoman/How-To-Secure-A-Linux-Server>
* [ ] DNS and Blocky changes
  * [ ] Leave only DNS-over-HTTPS (plain DNS might be used in DDOS, DoT useless)
  * [ ] Revisit all blocklists
  * [ ] POST_INSTALL DNS over HTTPS setup on clients
  * [ ] <https://www.youtube.com/watch?v=UjqZPLL0UvM>
  * [ ] Do I want my own blocks? 🏴‍☠️
  * [ ] Perhaps I wont need dynamic config also if I get rid of 53 port
* [ ] Homepage.dev ideas
  * [ ] Stocks SPY/QQQ - requires finnhub api key
  * [ ] World clock? moscow time
  * [ ] For crowdsec - link to <https://app.crowdsec.net/>
* [ ] url shorten <https://github.com/anhostfr/nah.pet>
* [ ] Email 💩
  * [ ] research something super simple. Preferably single docker container
  * [ ] Parsedmarc app
* [ ] Status page for services
  * [ ] Has to be free and allow deploy from ansible via API
  * [ ] maybe just main website check and self service to report docker unhealth
  * [ ] <https://beszel.dev/>
* [ ] Bandwhich - will require downloading binary to root - wait for deb repo
* [ ] tmux
  * [ ] add dracula disk usage (used/total) or totally redesign it
  * [ ] tmux with `nice` priority <https://x.com/SA5280/status/2001732941639282759>
* [ ] Linkeding to smth else supported in floccus when helium browser fixed for them
