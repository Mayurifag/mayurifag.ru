Ansible role for provisioning mayurifag.ru

DONT USE THIS REPOSITORY NO MATTER WHAT due to security reasons (i.e. there
is no role for ufw right now). Playbook is fine only for my personal usage.

requires:
- clean debian 9 stretch (playbook wont work anywhere else)
- large /data folder for nextcloud (/data is default on my cheap vps)
- ssh auth keys + password on root user
- hostname + cloudflare dns provider + reverse dns settings
- to test: vagrant + vagrant-cachier + ansible

I use secret file as git diff because im just too lazy to write all the things
you have to change to make this working for your purpose

Services:
- Dante — simple socks5 proxy (for telegram idk)
- Shadowsocks + v2ray plugin — «anti-firewall» encrypted proxy
- Mailserver — via dovecot/postfix/rspamd/mysql
- Netdata — simple all-in-one plug-and-play dashboard monitoring solution
- Nextcloud — personal cloud
- Rainloop — web ui for email (you may still use nextcloud though or your fav
email client)
- Wireguard — faster OpenVPN alternative to use with Linux OS preferrably

Additional:
- Sysctl tweaks for security and perfomance
- Wildcard SSL certificate — via acme.sh and LetsEncrypt
- MySQL — used for mailserver and nextcloud
- PHP — used for nextcloud and roundcube
- Redis — used for nextcloud caching and rspamd
- Nginx — web proxy server for every service above
- OpenDKIM — DKIM for mailserver and cloudflare [it seems not working, lacks of postfix settings]

TODO:

* OpenDKIM / rspamd remake
* dnsmasq.d — caching dns resolving / maybe adblocking — look at streisand repo
* ufw
* monitoring and alerting (not enough netdata)
* maybe openvpn (i dont need it though)
* handlers for services: see if services are active! -- error otherwise
* check info.php google

deploy: `ansible-playbook -i ansible-inventory provisioning/setup.yml`

to test in vagrant your system needs some dns entries. Example of /etc/hosts:

```
172.16.100.2 mayurifag.local
172.16.100.2 nextcloud.mayurifag.local
172.16.100.2 netdata.mayurifag.local
172.16.100.2 rainloop.mayurifag.local
```

Ideas got from:


DNS: https://thomas-leister.de/en/mailserver-debian-stretch/

Spam learning: https://words.bombast.net/rspamd-with-postfix-dovecot-debian-stretch/

https://123qwe.com/tutorial/#example-dns-zone-files

https://matt.sh/email2018#_jump-into-it

original ideas https://github.com/ajgon/self-hosted-mailserver/
