# Ansible role for provisioning mayurifag.ru

## Description

DONT USE THIS REPOSITORY NO MATTER WHAT due to security reasons (i.e. there
is no role for ufw right now). Playbook is fine only for my personal usage.

## Requires

### VPS

* Debian 10
* Large folder for docker data (Done by VPS via /data folder)
* ssh authorization key for root user (Done by VPS)
* hostname <mayurifag.ru> (Done by VPS)

### Local development

* Vagrant + VirtualBox
* Ansible

## Instructions

### Local deployment

```sh
vagrant destroy -f ; vagrant up --provision
```

### Production deployment

```sh
ansible-playbook -i inventories/my-ansible-nas/inventory provisioning.yml -b -K
```

## After production deploy

1. You should go to Homer' URL and review services working. Several ones need
additional configuration. For example, you probably want to change
wallabag:wallabag user:password on the obvious service.
2. You probably want to change ssh port and make additional sshd config

## Working on

Check if sslabs A+ working

## Applications List

| Name                | Docker             | Default endpoint                              | Port        |
| ------------------- | ------------------ | --------------------------------------------- | ----------- |
| Dante proxy         | :x:                | <socks5://mayurifag.local:7777> (+auth)       | 7777        |
| Glances             | :heavy_check_mark: | <http://glances.mayurifag.local>              | 61208/61209 |
| Homer               | :heavy_check_mark: | <http://homer.mayurifag.local>                | 10080:8080  |
| Lazydocker          | :x:                |                                               |             |
| Mayurifag.github.io | :heavy_check_mark: | <http://mayurifag.local>                      | 8005        |
| Netdata             | :heavy_check_mark: | <http://netdata.mayurifag.local>              | 19999       |
| Nextcloud           | :heavy_check_mark: | <http://nextcloud.mayurifag.local>            | 8081:80     |
| Portainer           | :heavy_check_mark: | <http://portainer.mayurifag.local>            | 9000        |
| Shadowsocks + V2ray | :x:                | <mayurifag.local:8888> (+v2ray config)        | 8888        |
| Traefik Dashboard   | :heavy_check_mark: | <http://traefik.mayurifag.local/dashboard/#/> |             |
| Wallabag            | :heavy_check_mark: | <http://wallabag.mayurifag.local>             | 7780:80     |
| Watchtower          | :heavy_check_mark: |                                               |             |
| Wireguard           | :x:                | <mayurifag.local:58172>                       | 58172       |

## TODO

### High priority

- [ ] Add motd.txt to server
- [ ] Comment out ports sections on containers and try to work with them
- [ ] Add Dozzle <https://github.com/amir20/dozzle>
- [ ] Add Statping <https://github.com/statping/statping>
- [ ] Add Authelia <https://github.com/authelia/authelia> / Remove baseauth
- [ ] Add Cloudflare companion tiredofit/traefik-cloudflare-companion:latest docker
- [ ] Move this section to issues and kanban
- [ ] Ssh configuration: change port and make the sshd configuration cheatsheet with Readme

### Medium priority

- [ ] Add Backup solution (duplicati?)
- [ ] Add ufw with rules + make docker respect the rules
- [ ] Add pastebin
- [ ] Make traefik to write logs to file + logrotate them
- [ ] Suggest if I need more fail2ban jail rules

### Low priority

- [ ] Add instructions for requirements and deployment (ansible-nas mostly ones)
- [ ] Add web analytics (matomo?)
- [ ] Add rocket.chat
- [ ] Add url shortener
- [ ] Add wiki
- [ ] Add ci/cd runner for gitlab/github
- [ ] Add bitwarden
- [ ] Add Git (gitea/gitlab)
- [ ] Check security <https://github.com/docker/docker-bench-security> <https://github.com/quay/clair>
- [ ] Make connection to docker through proxy fluencelabs/docker-socket-proxy

## Based on

<https://github.com/davestephens/ansible-nas>
<https://davidstephens.uk/ansible-nas/testing>
<https://www.smarthomebeginner.com/traefik-2-docker-tutorial>
<https://www.smarthomebeginner.com/cloudflare-settings-for-traefik-docker>
