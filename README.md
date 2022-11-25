# Ansible playbook for provisioning mayurifag.ru

## Description

**DONT USE THIS REPOSITORY NO MATTER WHAT** due to security reasons (i.e. there
is no role for ufw right now and it's docker based). Playbook is fine only for
my personal usage.

### Older implementation

There is branch `old-implementation-with-mailserver` without docker. I decided
to re-write roles from scratch with all XP I got so far and include docker
containers for better maintainability. But still there are some ideas I want to
migrate into newer implementation.

## Requires

### VPS

- Debian 10 / KVM virtualization / Linux 4.9+ kernel version
- Large folder for docker data (Done by VPS via /data folder)
- ssh authorization key for root user (Done by VPS)
- hostname <mayurifag.ru> (Done by VPS)

### Your PC

- Ansible
- Vagrant 2.2.19 (latest) + VirtualBox (for testing)

## Instructions

```sh
git clone https://github.com/Mayurifag/mayurifag.ru.git
cd mayurifag.ru
cp -rfp inventories/sample inventories/my-provision
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

| ------------------- | ------------------ | ----------------------------------------------- | ------------------ |
| Name                | Docker             | Default endpoint                                | App. Port          |
| ------------------- | ------------------ | ----------------------------------------------- | ------------------ |
| Dante proxy         | :heavy_minus_sign: | <socks5://mayurifag.local:7777> (+auth)         | 7777               |
| Dozzle              | :heavy_check_mark: | <http://dozzle.mayurifag.local>                 | 8080               |
| Filerun             | :heavy_check_mark: | <http://filerun.mayurifag.local>                | 80 [+3306 db]      |
| Glances             | :heavy_check_mark: | <http://glances.mayurifag.local>                | 61208/61209        |
| Homer               | :heavy_check_mark: | <http://homer.mayurifag.local>                  | 8080               |
| Lazydocker          | :heavy_minus_sign: | :heavy_minus_sign:                              | :heavy_minus_sign: |
| mayurifag.github.io | :heavy_check_mark: | <http://mayurifag.local>                        | 8005               |
| Netdata             | :heavy_check_mark: | <http://netdata.mayurifag.local>                | 19999              |
| Nextcloud           | :heavy_check_mark: | <http://nextcloud.mayurifag.local>              | 80                 |
| Portainer           | :heavy_check_mark: | <http://portainer.mayurifag.local>              | 9000               |
| Shadowsocks-rust    | :heavy_minus_sign: | <socks5://mayurifag.local:8888> (+v2ray config) | 8888               |
| Traefik Dashboard   | :heavy_check_mark: | <http://traefik.mayurifag.local/dashboard/#/>   | 8080 (?)           |
| Wallabag            | :heavy_check_mark: | <http://wallabag.mayurifag.local>               | 80                 |
| Watchtower          | :heavy_check_mark: | :heavy_minus_sign:                              | :heavy_minus_sign: |
| Wireguard           | :heavy_minus_sign: | <mayurifag.local:58172>                         | 58172              |
| ------------------- | ------------------ | ----------------------------------------------- | ------------------ |

## TODO

### WIP

The work is not in progress now, because I'm okay with current implementation,
but still I think there are some things existing for further development if I'll
need to deploy my services once again.

### High priority

- [ ] Ssh configuration: change port and make the sshd configuration cheatsheet with Readme
- [x] Comment out ports sections on containers and try to work with them
- [x] Add Dozzle <https://github.com/amir20/dozzle>
- [ ] Add Statping <https://github.com/statping/statping>
- [ ] Add Authelia <https://github.com/authelia/authelia> / Remove baseauth
- [ ] Add Cloudflare companion tiredofit/traefik-cloudflare-companion:latest docker
- [ ] Add Vikunja <https://vikunja.io/docs/full-docker-example/>
- [ ] Move this section to issues and kanban
- [x] Migrate from mysql to postgres for nextcloud. Look other perfomance boosters. cron at docker for nextcloud. bump versions
  - [x] <https://github.com/ReinerNippes/nextcloud_on_docker>
  - [x] <https://help.nextcloud.com/t/howto-ubuntu-docker-nextcloud-talk-collabora/76430>
  - [x] <https://docs.nextcloud.com/server/18/admin_manual/configuration_server/caching_configuration.html>
  - [x] <https://docs.nextcloud.com/server/18/admin_manual/installation/server_tuning.html>

### Medium priority

- [ ] Add automatic backup solution (duplicati?). Do I need anything more than
      /data/docker_data?
- [ ] Add ufw with rules + make docker respect the rules
- [ ] Add pastebin
- [ ] Make traefik to write logs to file + logrotate them
- [ ] Suggest if I need more fail2ban jail rules
  - [ ] <https://shadowsocks.org/en/wiki/Setup-fail2ban.html>
- [ ] Add motd.txt to server
  - [ ] About lazydocker
  - [ ] Aliases
- [ ] https://github.com/EmbarkStudios/wg-ui
- [x] FileRun

### Low priority

- [ ] Add zsh
- [ ] Make CI working
- [x] Add instructions for requirements and deployment
- [ ] Try to make deploy from zero to hero. Add instructions if needed.
- [ ] Add lightweight opensource filesharing nextcloud alternative (FileRun?)
- [ ] Add web analytics (matomo?)
- [ ] Add rocket.chat
- [ ] Add url shortener
- [ ] Add wiki
- [ ] Add ci/cd runner for gitlab/github
- [ ] Add bitwarden
- [ ] Add Git (gitea/gitlab)
- [ ] Check security <https://github.com/docker/docker-bench-security> <https://github.com/quay/clair>
- [ ] Make connection to docker through proxy fluencelabs/docker-socket-proxy
- [ ] Migrate from dante to something docker based
  - [ ] <https://hub.docker.com/r/serjs/go-socks5-proxy/>
  - [ ] <https://github.com/schors/tgdante2>
- [ ] Migrate from shadowsocks-rust + v2ray to shadowsocks2-go + x-ray / maybe docker
  - [ ] <https://github.com/dmirubtsov/ss-xray-docker>
  - [ ] <https://habr.com/ru/post/358126/>

```txt
ss-server[21509]: Installing the rng-utils/rng-tools, jitterentropy or haveged packages may help.
ss-server[21509]: On virtualized Linux environments, also consider using virtio-rng.
```

## Based on / inspired / helpful

- <https://github.com/davestephens/ansible-nas>
- <https://davidstephens.uk/ansible-nas/testing>
- <https://www.smarthomebeginner.com/traefik-2-docker-tutorial>
- <https://www.smarthomebeginner.com/cloudflare-settings-for-traefik-docker>
- <https://www.reddit.com/r/selfhosted/>
