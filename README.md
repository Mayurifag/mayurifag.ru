WIP: Ansible role for provisioning mayurifag.ru

DONT USE THIS REPOSITORY NO MATTER WHAT due to security reasons (i.e. there
is no role for ufw right now)

requires:
- debian 9 (probably wont work anywhere else)
- large /data folder for nextcloud (/data is default on my cheap vps)
- shell provisioning for python (look an example at Vargrantfile)

I use secret file as git diff because im just too lazy to write all the things
you have to change to make this working for your purpose

TODO:
- acme.sh refactoring — think about issue cert task
- dnsmasq.d — caching dns resolving / maybe adblocking
- ufw
- monitoring and alerting (not enough netdata)
- maybe openvpn (i dont need it though)
- handlers for services: see if services are active! -- error otherwise

DNS: https://thomas-leister.de/en/mailserver-debian-stretch/
Spam learning: https://words.bombast.net/rspamd-with-postfix-dovecot-debian-stretch/

https://123qwe.com/tutorial/#example-dns-zone-files
https://matt.sh/email2018#_jump-into-it

original https://github.com/ajgon/self-hosted-mailserver/
