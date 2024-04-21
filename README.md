# Ansible playbook for provisioning mayurifag.ru

## Description

**DONT USE THIS REPOSITORY NO MATTER WHAT** due to security reasons (i.e. there
is no firewall rules, not much services monitoring, no fail2ban rules and most
important: it uses docker).

Playbook is fine only for my personal usage.

## Requires

### DNS

Obviously, `A` record for your TLD + wildcard/subdomain configuration in
Cloudflare or your favourite DNS provider.

### VPS

- Debian 10-11 (maybe works fine on other `apt` distros)
- Large folder for docker data (Done by VPS via large disk)
- ssh authorization key for root user (Done by VPS or
`ssh-copy-id root@mayurifag.ru`)

### Your PC

- Ansible `python3 -m pip install --user ansible`
- (only MacOS) - passlib `python3 -m pip install --user passlib` (to use crypto
module from ansible)
- Vagrant 2.2.19 (latest) + VirtualBox (for testing)

## Instructions

```sh
git clone https://github.com/Mayurifag/mayurifag.ru.git
cd mayurifag.ru
cp -rfp inventories/sample inventories/my-provision
# ... change my-provision ...
ansible-galaxy install -r requirements.yml
```

### Local test deployment

```sh
# maybe if something wrong -- rm -rf .vagrant on repo folder
vagrant destroy -f ; vagrant up --provision
```

### Production deployment

#### TL;DR

```sh
ansible-playbook -i inventories/my-provision/inventory provisioning.yml
```

Maybe first you'll need to ssh and exec:

```sh
apt-get --allow-releaseinfo-change update
```

#### Optional in-before steps

- Remove old remote host identification

```sh
ssh-keygen -R mayurifag.ru ; ssh-keygen -R $(host mayurifag.ru | awk '/has address/ {print $4}')
```

- Generate new ssh key and add it to your inventory vars file

```sh
ssh-keygen -t rsa -b 4096 -C "Mayurifag@mayurifag.ru" -f ~/Desktop/mayurifag.ru
xclip -sel clip < ~/Desktop/mayurifag.ru.pub
vi inventories/my-provision/group_vars/sample.yml # add key here in section
keepassxc # Make new ssh agent entry
```

- Make new ssh config section. You need to change it after deploy.

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
    User root # Change user and port
    Port 22   # after deployment
```

## Applications List

| Name                    | Default endpoint                             | App. Port   |
| ----------------------- | -------------------------------------------- | ----------- |
| Blocky                  | -                                            | -           |
| Doku                    | <http://doku.mayurifag.local>                | 9090        |
| Dozzle                  | <http://dozzle.mayurifag.local>              | 8080        |
| Filebrowser             | <http://fb.mayurifag.local>                  | 80          |
| Glances                 | <http://glances.mayurifag.local>             | 61208/61209 |
| Go-socks5-proxy         | <socks5://mayurifag.local:7777> (+auth)      | 1080        |
| Homer                   | <http://homer.mayurifag.local>               | 8080        |
| Hemmelig                | <http://secret.mayurifag.local>              | 3000        |
| LMS                     | <http://lms.mayurifag.local>                 | 5082        |
| mayurifag.github.io     | <http://mayurifag.local>                     | 8005        |
| Navidrome               | <http://mus.mayurifag.local>                 | 80          |
| Netdata                 | <http://netdata.mayurifag.local>             | 19999       |
| Owncloud Infinite Scale | <http://ocis.mayurifag.local>                | 9200        |
| Portainer               | <http://portainer.mayurifag.local>           | 9000        |
| SFTPGo                  | <https://sftp.mayurifag.local>               | 8080        |
| Shadowsocks-rust        | <https://ss.mayurifag.local/xray> (uses TLS) | 1080        |
| Syncthing [WebUI]       | <https://st.mayurifag.local>                 | 8384        |
| Wallabag                | <http://wallabag.mayurifag.local>            | 80          |
| Watchtower              | -                                            | -           |
| Webdav [SFTPGo]         | <http://webdav.mayurifag.ru>                 | 10080       |
| Wireguard-Easy          | <http://wg.mayurifag.local>                  | 58172       |
| Whattocommit            | <http://commit.mayurifag.local>              | 8080        |

## TODO

### WIP

The work is not in progress now, because I'm okay with current implementation,
but still I think there are some things existing for further development if I'll
need to deploy my services once again.

### High priority

- [x] Some strange things with Traefik config. If problem with "my-headers@file" ->
  return "my-headers@file"
- [ ] Log rotation for docker containers
- [ ] ~~https://github.com/alexta69/metube~~
- [ ] ~~Add cleaning up apt-get to get extra 1GB~~
- [ ] ~~Think how to rotate logs easily for docker (takes all the space in a year or more)~~
- [ ] Ssh configuration: change port and make the sshd configuration cheatsheet with Readme
- [x] Comment out ports sections on containers and try to work with them
- [x] Add Dozzle <https://github.com/amir20/dozzle>
- [ ] Uptime Kuma
- [x] Blocky DNS
- [ ] Add systemd services
- [ ] Migrate to dashboard which is easy maintainable: flame (with labels)
- [ ] Add Authentik / Remove baseauth
- [ ] Add Cloudflare companion tiredofit/traefik-cloudflare-companion:latest docker
- [ ] Add Vikunja <https://vikunja.io/docs/full-docker-example/>
- [ ] Move this section to issues and kanban
- [ ] Add zswap
- [ ] ~~<https://github.com/pglombardo/PasswordPusher>~~
- [x] Migrate from mysql to postgres for nextcloud. Look other perfomance boosters. cron at docker for nextcloud. bump versions
  - [x] <https://github.com/ReinerNippes/nextcloud_on_docker>
  - [x] <https://help.nextcloud.com/t/howto-ubuntu-docker-nextcloud-talk-collabora/76430>
  - [x] <https://docs.nextcloud.com/server/18/admin_manual/configuration_server/caching_configuration.html>
  - [x] <https://docs.nextcloud.com/server/18/admin_manual/installation/server_tuning.html>

### Medium priority

- [ ] https://github.com/epoupon/lms
- [ ] Add automatic backup solution (duplicati?). Do I need anything more than
      /data/docker_data?
- [ ] Add ufw with rules + make docker respect the rules
- [ ] Add pastebin
- [ ] ~~Make traefik to write logs to file + logrotate them~~
- [ ] Suggest if I need more fail2ban jail rules
  - [ ] <https://shadowsocks.org/en/wiki/Setup-fail2ban.html>
- [ ] Add motd.txt to server
  - [ ] About lazydocker
  - [ ] Aliases
- [ ] ~~<https://github.com/EmbarkStudios/wg-ui>~~
- [x] Navidrome
- [x] Doku https://github.com/tborychowski/self-hosted-cookbook/blob/master/apps/docker/doku.md
- [ ] ~~<https://github.com/tborychowski/self-hosted-cookbook/blob/master/apps/other/firefox.md>~~
- [x] FileRun
- [x] Simple proxy server in docker
- [x] Makefiles + info to launch only specified tags
- [ ] Librespeed

### Low priority

- [ ] Add zsh
- [ ] Make CI working
- [x] Add instructions for requirements and deployment
- [ ] Try to make deploy from zero to hero. Add instructions if needed.
- [x] Add lightweight filesharing nextcloud alternative (FileRun?)
- [ ] Add web analytics (matomo?)
- [ ] Add rocket.chat
- [ ] Add url shortener
- [ ] Add wiki
- [ ] Add ci/cd runner for gitlab/github
- [ ] Add bitwarden
- [ ] Add Git (gitea/gitlab)
- [ ] Check security <https://github.com/docker/docker-bench-security> <https://github.com/quay/clair>
- [ ] Make connection to docker through proxy fluencelabs/docker-socket-proxy
- [x] Migrate from dante to something docker based
  - [x] <https://hub.docker.com/r/serjs/go-socks5-proxy/>
  - [x] <https://github.com/schors/tgdante2>
- [x] Migrate from shadowsocks-rust + v2ray to shadowsocks2-go + x-ray / maybe docker
  - [x] <https://github.com/dmirubtsov/ss-xray-docker>
  - [x] <https://habr.com/ru/post/358126/>
- [ ] https://hub.docker.com/r/linuxserver/librespeed

## Older implementation

There is branch `old-implementation-with-mailserver` without docker. I decided
to re-write roles from scratch with all XP I got so far and include docker
containers for better maintainability. But still there are some ideas I want to
migrate into newer implementation.

## Based on / inspired / helpful

- <https://github.com/davestephens/ansible-nas>
- <https://davidstephens.uk/ansible-nas/testing>
- <https://www.smarthomebeginner.com/traefik-2-docker-tutorial>
- <https://www.smarthomebeginner.com/cloudflare-settings-for-traefik-docker>
- <https://www.reddit.com/r/selfhosted/>
