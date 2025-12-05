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

```sh
git clone https://github.com/Mayurifag/mayurifag.ru.git
cd mayurifag.ru
cp -rfp inventories/sample inventories/my-provision
# ... change my-provision ...
# or ln from some place like that:
# ln -s ~/Nextcloud/Software/dotfiles/my-provision inventories/my-provision
ansible-galaxy install -r requirements.yml
```

### Production deployment

#### TL;DR

```sh
make deploy-tag "traefik,mus"
```

#### Optional steps

* Generate new ssh key and add it to inventory vars file and password manager

```sh
ssh-keygen -t ed25519 -C "Mayurifag@mayurifag.ru" -f ~/Desktop/mayurifag.ru
xclip -sel clip < ~/Desktop/mayurifag.ru.pub
vi inventories/my-provision/group_vars/sample.yml # add key here in section
keepassxc # Make new ssh agent entry if you use keepassxc ssh agent
```

* Make new ssh config section for convenience

```sh
vi ~/.ssh/config

# ~/.ssh/config
Host *
    StrictHostKeyChecking ask
    UpdateHostKeys ask
    Protocol 2
    ServerAliveInterval 120
    ServerAliveCountMax 2

[...]

Host mayurifag-prod
    HostName mayurifag.ru
    User root # Change user
```

## Applications List

This list changed a lot through years, I'm trying to remove things I do not use.

<!-- markdownlint-disable line-length -->

| Name                 | Default endpoint                         | Port(s)   | Auth | Watchtower |
| -------------------- | ---------------------------------------- | --------- | ---- | ---------- |
| 3proxy               | <socks5://mayurifag.local:1080> or 3128  | 1080/3128 | app  | ✅          |
| 3x-ui panel          | <http://3x.mayurifag.local>              | 2053      | app  |            |
| 3x-ui subscriptions  | <http://3xsub.mayurifag.local>           | 2096      | app  |            |
| Blocky               | <http://dns.mayurifag.local> / TLS :853  | 853/4000  | app  |            |
| Gitea                | <http://git.mayurifag.local>             | 3000/222  | todo |            |
| Hemmelig.app         | <http://secret.mayurifag.local>          | 3000      | app  |            |
| Homepage.dev         | <http://home.mayurifag.local>            | 3000      | ldap | ✅          |
| mayurifag.github.io  | <http://mayurifag.local>                 | 8005      | ldap | ✅          |
| mus                  | <http://mus.mayurifag.local>             | 8000      | ldap | ✅          |
| lldap                | <http://ldap.mayurifag.local>            | 17170     | ldap | ✅          |
| Netdata              | <http://netdata.mayurifag.local>         | 19999     | ldap |            |
| Nextcloud            | <http://nextcloud.mayurifag.local>       | 11000     | todo |            |
| Obsidian LiveSync db | <http://couchdbobsidian.mayurifag.local> | 5984      | app  |            |
| OpenCloud            | <http://cloud.mayurifag.local>           | 9200      | ldap |            |
| Portainer            | <http://portainer.mayurifag.local>       | 9000      | app  | ✅          |
| Traefik dashboard    | <http://traefik.mayurifag.local>         | 8080      | ldap |            |
| Tinyauth             | <http://auth.mayurifag.local>            | 3000      | ldap | ✅          |
| Vaultwarden          | <http://pw.mayurifag.local>              | 80        | app  |            |
| Watchtower HTTP API  | <http://watchtower.mayurifag.local>      | 8080      | app  | ✅          |

<!-- markdownlint-enable line-length -->

Refer to [POST_INSTALL.md](./POST_INSTALL.md) for after deployment info.

## TODO

### Work is not in progress

The work is not in progress now, because I am okay with current implementation,
but still I think there are some things existing for further development if I'll
need to deploy my services once again.

### List

* [ ] (wait) Next deploy of 3x-ui
  * [ ] Make tinyauth defence and change keepassxc entry
  * [ ] Edit POST_INSTALL info with real information on adding inbound+client+qr
  * [ ] Information about client apps (win/linux/macos/android/ios)
* [ ] Firewall
  * [ ] ufw - for docker too <https://github.com/chaifeng/ufw-docker>
  * [ ] Block everything except ssh. Check ufw status and allowances
  * [ ] open port if needed in each ansible role
  * [ ] Crowdsec iptables firewall - remediation component.
  * [ ] <https://www.crowdsec.net/blog/secure-docker-compose-stacks-with-crowdsec>
  * [ ] see if there is solution to unban false positive and if not, add smth
* [ ] maybe finance app - deprecated, so research alternatives.
  * [ ] Has to support crypto, ibkr, russian brokers
  * [ ] <https://github.com/we-promise/sure>
  * [ ] Is it possible to have data in nextcloud?
* [ ] Status page for services
  * [ ] Has to be free and allow deploy from ansible via API
* [ ] pdf <https://github.com/alam00000/bentopdf>

### Thinking if I need it / probably wont do ideas / notes

* [ ] Traefik
  * [ ] tracing/observability tests with my apps
  * [ ] No AI Bots Middleware with robots.txt - plugin install
* [ ] Watchtowerrr
  * [ ] use config.json for auth to dockerhub to prevent limits
  * [ ] use metrics for homepage <https://gethomepage.dev/widgets/services/watchtower/>
* [ ] <https://github.com/binwiederhier/ntfy>
* [ ] docker image of mayurifag.github.io has to be in ghcr
* [ ] VPS security
  * [ ] Kernel params to have less /var/log/syslog noise - add to crowdsec btw
  * [ ] <https://madaidans-insecurities.github.io/guides/linux-hardening.html>
  * [ ] (wait for update) <https://github.com/docker/docker-bench-security>
  * [ ] (not sure) <https://github.com/quay/clair>
  * [ ] Make connection to docker through proxy fluencelabs/docker-socket-proxy
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
  * [ ] Parsedmarc
