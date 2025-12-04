# Ansible playbook for provisioning mayurifag.ru

[![Linters](https://github.com/Mayurifag/mayurifag.ru/actions/workflows/lint.yml/badge.svg)](https://github.com/Mayurifag/mayurifag.ru/actions/workflows/lint.yml)

## Requires

### VPS

* DNS `A` records for your TLD and wildcard (`*`)
* Debian 12+
* (optionally) Check that VPS provider has open ports for apps you use
* (optionally) Check that you have correct storage setup

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
# Tag by tag, and there is make deploy-prod available to deploy all-in-once
make deploy-tag "traefik,mus"
```

#### Optional steps

* Generate new ssh key and add it to your inventory vars file

```sh
ssh-keygen -t ed25519 -C "Mayurifag@mayurifag.ru" -f ~/Desktop/mayurifag.ru
xclip -sel clip < ~/Desktop/mayurifag.ru.pub
vi inventories/my-provision/group_vars/sample.yml # add key here in section
keepassxc # Make new ssh agent entry if you use keepassxc ssh agent
```

* Make new ssh config section. You need to change it after deploy.

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

| Name                 | Default endpoint                         | Port(s)   | Autoupdate | Auth |
| -------------------- | ---------------------------------------- | --------- | ---------- | ---- |
| 3proxy               | <socks5://mayurifag.local:1080> or 3128  | 1080/3128 | ✅          | app  |
| 3x-ui                | <http://threexui.mayurifag.local>        | 2053/2096 |            | app  |
| Blocky               | <http://dns.mayurifag.local> / TLS :853  | 853/4000  |            | -    |
| Gitea                | <http://git.mayurifag.local>             | 3000/222  |            | app  |
| Hemmelig             | <http://secret.mayurifag.local>          | 3000      |            | app  |
| mayurifag.github.io  | <http://mayurifag.local>                 | 8005      | ✅          | ldap |
| mus                  | <http://mus.mayurifag.local>             | 8000      | ✅          | ldap |
| lldap                | <http://ldap.mayurifag.local>            | 17170     | ✅          | ✅    |
| Netdata              | <http://netdata.mayurifag.local>         | 19999     |            |      |
| Nextcloud            | <http://nextcloud.mayurifag.local>       | 11000     |            |      |
| Obsidian LiveSync db | <http://couchdbobsidian.mayurifag.local> | 5984      |            |      |
| Portainer            | <http://portainer.mayurifag.local>       | 9000      | ✅          |      |
| Traefik dashboard    | <http://traefik.mayurifag.local>         | 8080      |            |      |
| Tinyauth             | <http://auth.mayurifag.local>            | 3000      | ✅          |
| Vaultwarden          | <http://pw.mayurifag.local>              | 80        |            |      |
| Watchtower           | <http://watchtower.mayurifag.local>      | 8080      |            |      |

<!-- markdownlint-enable line-length -->

## TODO

### Work is not in progress

The work is not in progress now, because I am okay with current implementation,
but still I think there are some things existing for further development if I'll
need to deploy my services once again.

### List

* [ ] LDAP via <https://github.com/lldap/lldap>
  * [x] Create users through GraphQL scripting on deployment / bootstrap script
  * [x] Activate in tinyauth
  * [ ] Activate in apps (i.e. Nextcloud and others)
* [ ] Portainer - auto add user and env
  * [ ] <https://docs.portainer.io/admin/environments/add/api>
* [ ] Check 3x-ui/Remnawave - working
* [ ] Migrate <https://gethomepage.dev>
  * [ ] Make a service
  * [ ] Make labels on all services I have
* [ ] Blocky readme - DNS over encrypted things
* [ ] OCIS - POSIX fs

### Non priority for now

* [ ] Refactor dynamic configs for traefik - some are static, some need to be
  moved to the services themself
  * [ ] Crowdsec will be after traefik
* [ ] Crowdsec webui dashboard and readme section about that
* [ ] Firewall
  * [ ] ufw - for docker too <https://github.com/chaifeng/ufw-docker> - each role
  * [ ] Crowdsec iptables firewall
    * [ ] <https://www.crowdsec.net/blog/secure-docker-compose-stacks-with-crowdsec>
* [ ] maybe finance app - deprecated, so research alternatives.
  * [ ] Has to support crypto, ibkr, russian brokers
  * [ ] <https://github.com/we-promise/sure>
* [ ] VPS security
  * [ ] <https://madaidans-insecurities.github.io/guides/linux-hardening.html>
  * [ ] (wait for update) <https://github.com/docker/docker-bench-security>
  * [ ] (not sure) <https://github.com/quay/clair>
  * [ ] Make connection to docker through proxy fluencelabs/docker-socket-proxy
* [ ] Status page on some free service
* [ ] <https://github.com/binwiederhier/ntfy>
* [ ] docker image of mayurifag.github.io has to be in ghcr
* [ ] watchtowerrr - use config.json for auth to dockerhub to prevent limits
* [ ] traefik observability tests

## Based on / inspired / helpful

* <https://github.com/davestephens/ansible-nas>
* <https://davidstephens.uk/ansible-nas/testing>
* <https://www.smarthomebeginner.com/traefik-2-docker-tutorial>
* <https://www.smarthomebeginner.com/cloudflare-settings-for-traefik-docker>
* <https://www.reddit.com/r/selfhosted/>
