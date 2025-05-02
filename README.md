# Ansible playbook for provisioning mayurifag.ru

[![Linters](https://github.com/Mayurifag/mayurifag.ru/actions/workflows/lint.yml/badge.svg)](https://github.com/Mayurifag/mayurifag.ru/actions/workflows/lint.yml)

## Description

**DONT USE THIS REPOSITORY NO MATTER WHAT** due to security reasons (i.e. there
is no firewall rules, no custom fail2ban rules and it uses docker).

Playbook is fine only for my personal opinionated usage!

## Requires

### VPS

* `A` record for your TLD + wildcard/subdomain configuration in Cloudflare or
  your favourite DNS provider.
* Debian 10-12 (Ubuntu works, though requires A LOT of interventions)
* ssh authorization key for root user (Done by VPS or
`ssh-copy-id root@mayurifag.ru`)
* Be sure that you have open ports for needed applications (some vps providers
  have default blocked ports or blocked them all)
* (optionally) Large folder for docker data if you need it (might be done via
  connecting some disk to your vps or ask your vps provider about some GB)

### Your PC

* Ansible `python3 -m pip install --user ansible`
* (only MacOS) - passlib `python3 -m pip install --user passlib` (to use crypto
module from ansible)

## Instructions

### Initial setup

```sh
git clone https://github.com/Mayurifag/mayurifag.ru.git
cd mayurifag.ru
cp -rfp inventories/sample inventories/my-provision
# ... change my-provision ...
ansible-galaxy install -r requirements.yml
```

### Production deployment

#### TL;DR

Maybe first you'll need to ssh and exec:

```sh
apt-get --allow-releaseinfo-change update
# or
do-release-upgrade
```

```sh
make deploy-prod
# or
make deploy-tag netdata # or other tag
```

#### Optional in-before steps

* Remove old remote host identification

<!-- markdownlint-disable line-length -->
```sh
ssh-keygen -R mayurifag.ru ; ssh-keygen -R $(host mayurifag.ru | awk '/has address/ {print $4}')
```

* Generate new ssh key and add it to your inventory vars file

```sh
ssh-keygen -t rsa -b 4096 -C "Mayurifag@mayurifag.ru" -f ~/Desktop/mayurifag.ru # rsa here, but you can use ed25519
xclip -sel clip < ~/Desktop/mayurifag.ru.pub
vi inventories/my-provision/group_vars/sample.yml # add key here in section
keepassxc # Make new ssh agent entry
```

<!-- markdownlint-enable line-length -->

* Make new ssh config section. You need to change it after deploy.

```sh
vi ~/.ssh/config

# ~/.ssh/config
Host *
    Protocol 2
    ServerAliveInterval 120
    ServerAliveCountMax 2

[...]

Host mayurifag-prod
    HostName mayurifag.ru
    User root # Change user
    Port 22
```

## Applications List

<!-- markdownlint-disable line-length -->

| Name                    | Default endpoint                             | App. Port   | Watchtower updates |
| ----------------------- | -------------------------------------------- | ----------- | ------------------ |
| 3proxy                  | <socks5://mayurifag.local:1080> or 3128      | 1080/3128   | ✅                 |
| Blocky                  | [DNS] -> ip:53                               | 53          |                    |
| Dockovpn                | <http://dockovpn.mayurifag.local>            | 1194/8080   |                    |
| Gitea                   | <http://git.mayurifag.local>                 | 3000/222    |                    |
| Hemmelig                | <http://secret.mayurifag.local>              | 3000        |                    |
| mayurifag.github.io     | <http://mayurifag.local>                     | 8005        | ✅                 |
| Navidrome               | <http://mus.mayurifag.local>                 | 80          |                    |
| Netdata                 | <http://netdata.mayurifag.local>             | 19999       |                    |
| Nextcloud All-in-One    | <http://nextcloud.mayurifag.local>           | 11000       |                    |
| Portainer               | <http://portainer.mayurifag.local>           | 9000        | ✅                 |
| Shadowsocks-rust        | <https://ss.mayurifag.local/xray> (uses TLS) | 1080        |                    |
| Traefik Dashboard       | <http://traefik.mayurifag.local>             | 8080        |                    |
| Vaultwarden             | <http://pw.mayurifag.local>                  | 80          |                    |
| Watchtower              | <http://watchtower.mayurifag.local>          | 8080        |                    |
| Wireguard-Easy          | <http://wg.mayurifag.local>                  | 58172       |                    |

<!-- markdownlint-enable line-length -->

## TODO

### Work is not in progress

The work is not in progress now, because I am okay with current implementation,
but still I think there are some things existing for further development if I'll
need to deploy my services once again.

### High priority

* [ ] [Max log for systemctl journal](https://unix.stackexchange.com/questions/130786/can-i-remove-files-in-var-log-journal-and-var-cache-abrt-di-usr)
* [x] Proxy to be http and socks5 in single container
* [x] Sync time with ntp automatically. I need it for some of my time-sensitive
  services.
* [x] Some strange things with Traefik config. If problem with
  "secure-headers@file" -> return "secure-headers@file"
* [x] Log rotation for docker containers - or default settings after install
* [ ] ~~<https://github.com/alexta69/metube>~~
* [x] Add cleaning up apt-get to get extra 1GB
* [x] Think how to rotate logs easily for docker (takes all the space in a
  year or more)
* [ ] ~~Ssh configuration: change port and make the sshd configuration cheatsheet
  with Readme~~
* [x] Comment out ports sections on containers and try to work with them
* [x] Add Dozzle <https://github.com/amir20/dozzle>
* [ ] ~~Uptime Kuma~~
* [x] Blocky DNS
* [ ] ~~Add systemd services - do I need them or I'm fine~~
* [ ] Migrate to dashboard which is easy maintainable: <https://gethomepage.dev>
  * [ ] Should have docker labels services configuration and use authelia or
    other auth cookies/etc. - documented
* [ ] Add Authentik / Remove baseauth
* [ ] ~~Add Cloudflare companion tiredofit/traefik-cloudflare-companion:latest docker~~
* [ ] ~~Add Vikunja <https://vikunja.io/docs/full-docker-example/>~~
* [ ] Move this section to issues and kanban
* [ ] ~~Add zswap~~
* [ ] ~~<https://github.com/pglombardo/PasswordPusher>~~
* [x] Migrate from mysql to postgres for nextcloud. Look other perfomance
  boosters. cron at docker for nextcloud. bump versions
  * [x] <https://github.com/ReinerNippes/nextcloud_on_docker>
  * [x] <https://help.nextcloud.com/t/howto-ubuntu-docker-nextcloud-talk-collabora/76430>
  * [x] <https://docs.nextcloud.com/server/18/admin_manual/configuration_server/caching_configuration.html>
  * [x] <https://docs.nextcloud.com/server/18/admin_manual/installation/server_tuning.html>

### Medium priority

* [x] <https://github.com/epoupon/lms>
* [ ] ~~Add automatic backup solution (duplicati?). Do I need anything more than/data/docker_data?~~
* [ ] Add ufw with rules + make docker respect the rules. geerligguy.firewall
* [x] Add pastebin - done via hemmelig
* [ ] ~~Make traefik to write logs to file + logrotate them~~
* [ ] Suggest if I need more fail2ban jail rules
  * [ ] ~~<https://shadowsocks.org/en/wiki/Setup-fail2ban.html>~~
  * [ ] fail2ban plugin for traefik?!
* [ ] Add motd.txt to server
  * [ ] About lazydocker
  * [ ] Aliases
* [ ] ~~<https://github.com/EmbarkStudios/wg-ui>~~
* [x] Navidrome
* [x] Doku <https://github.com/tborychowski/self-hosted-cookbook/blob/master/apps/docker/doku.md>
* [ ] ~~<https://github.com/tborychowski/self-hosted-cookbook/blob/master/apps/other/firefox.md>~~
* [x] FileRun
* [x] Simple proxy server in docker
* [x] Makefiles + info to launch only specified tags
* [x] Make traefik dashboard available from internet
* [ ] <https://github.com/usememos/memos>

### Low priority

* [x] Ssh hardening:
  * [ ] ~~If I change port on installation -- what I have to change then?~~
  * [x] Check if current config is okay without changes done already by playbook
  * [x] PubkeyAuthentication yes
  * [x] AllowUsers root, admin_username
  * [x] AllowTcpForwarding no
  * [x] PermitEmptyPasswords no
  * [x] X11Forwarding no
* [ ] Add zsh
* [x] Make CI working (decided not to have full e2e test suite, so fine for now)
* [x] Add instructions for requirements and deployment
* [x] Try to make deploy from zero to hero. Add instructions if needed.
* [x] Add lightweight filesharing nextcloud alternative (FileRun?)
* [ ] ~~Add web analytics (matomo?)~~
* [ ] ~~Add rocket.chat~~
* [ ] ~~Add url shortener~~
* [ ] Add wiki - do I need it? Research first
* [x] Add Git (gitea/gitlab/else)
* [ ] Add ci/cd runner for selfhosted git
* [x] Add ~~bitwarden~~ Vaultwarden
* [ ] Check security <https://github.com/docker/docker-bench-security>
  <https://github.com/quay/clair>
* [ ] Make connection to docker through proxy fluencelabs/docker-socket-proxy
* [x] Migrate from dante to something docker based
  * [x] <https://hub.docker.com/r/serjs/go-socks5-proxy/>
  * [x] <https://github.com/schors/tgdante2>
* [x] Migrate from shadowsocks-rust + v2ray to shadowsocks2-go + x-ray / maybe docker
  * [x] <https://github.com/dmirubtsov/ss-xray-docker>
  * [x] <https://habr.com/ru/post/358126/>
* [ ] <https://hub.docker.com/r/linuxserver/librespeed>
* [ ] <https://github.com/alexjustesen/speedtest-tracker> - check if compatible
  with other providers + with homepage.dev + with traefik + with authelia
* [x] Rename `my-headers` to `secure-headers` in traefik config and all
  containers
* [ ] research simple selfhosted pinger

## Older implementation

There is branch `old-implementation-with-mailserver` without docker. I decided
to re-write roles from scratch with all XP I got so far and include docker
containers for better maintainability. But still there are some ideas I want to
migrate into newer implementation.

## Based on / inspired / helpful

* <https://github.com/davestephens/ansible-nas>
* <https://davidstephens.uk/ansible-nas/testing>
* <https://www.smarthomebeginner.com/traefik-2-docker-tutorial>
* <https://www.smarthomebeginner.com/cloudflare-settings-for-traefik-docker>
* <https://www.reddit.com/r/selfhosted/>
