WIP: Ansible role for provisioning mayurifag.ru

DONT USE THIS REPOSITORY NO MATTER WHAT due to security reasons (for ex. there is no role for ufw right now)

requires:
- debian 9 (probably wont work anywhere else)
- large /data folder for nextcloud (/data is default on my cheap vps)
- shell provisioning for python (look an example at Vargrantfile)

TODO:
- acme.sh refactoring — think about issue cert task
- dnsmasq.d — caching dns resolving / maybe adblocking
- ufw
- maybe openvpn (i dont need it though)

DNS: https://thomas-leister.de/en/mailserver-debian-stretch/
Spam learning: https://words.bombast.net/rspamd-with-postfix-dovecot-debian-stretch/

https://123qwe.com/tutorial/#example-dns-zone-files
https://matt.sh/email2018#_jump-into-it
