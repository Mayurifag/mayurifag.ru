WIP: Ansible role for provisioning mayurifag.ru

DONT USE THIS REPOSITORY NO MATTER WHAT due to security reasons (i.e. there
is no role for ufw right now)

requires:
- debian 9 (probably wont work anywhere else)
- large /data folder for nextcloud (/data is default on my cheap vps)
- ssh keys + password on root user

I use secret file as git diff because im just too lazy to write all the things
you have to change to make this working for your purpose

Services:
- Dante — simple socks5 proxy (for telegram idk)
- Shadowsocks + v2ray plugin — «anti-firewall» encrypted proxy
- Mailserver — via dovecot/postfix/rspamd/mysql
- Netdata — simple all-in-one plug-and-play dashboard monitoring solution
- Nextcloud — personal cloud
- Rainloop — web ui for email (you may still use nextcloud though or your fav email client)
- Wireguard — faster OpenVPN alternative to use with Linux OS preferrably

Additional:
- Sysctl tweaks for security and perfomance
- Wildcard SSL certificate — via acme.sh and LetsEncrypt
- MySQL — used for mailserver and nextcloud
- PHP — used for nextcloud and roundcube
- Redis — used for php caching, nextcloud, probably roundcube idk i have to google that later (TODO)
- Nginx — web proxy server for every service above
- OpenDKIM — DKIM for mailserver and cloudflare

TODO:
[] netdata auth basic at least or smth
[] change root password ??? why changed see and guess about that!
[] Fix mysql (root@localhost fail after 1st run) and nextcloud (default permission issues)
[] Global domain 1-2lvl setting — but still notice letsencrypt domain getting — switch to self-signed??
[] acme.sh refactoring — think about issue cert task
[] dnsmasq.d — caching dns resolving / maybe adblocking
[] ufw
[] monitoring and alerting (not enough netdata)
[] maybe openvpn (i dont need it though)
[] handlers for services: see if services are active! -- error otherwise

DNS: https://thomas-leister.de/en/mailserver-debian-stretch/
Spam learning: https://words.bombast.net/rspamd-with-postfix-dovecot-debian-stretch/

https://123qwe.com/tutorial/#example-dns-zone-files
https://matt.sh/email2018#_jump-into-it

original ideas https://github.com/ajgon/self-hosted-mailserver/

deploy: `ansible-playbook -i ansible-inventory provisioning/setup.yml`
