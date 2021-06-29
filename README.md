# Init

based:
https://github.com/davestephens/ansible-nas
https://davidstephens.uk/ansible-nas/testing/

instructions:
ansible-playbook -i inventories/my-ansible-nas/inventory provisioning.yml -b -K
vagrant destroy -f ; vagrant up --provision

Todo:
ssh ignore deprecated rules
sslabs A+
add motd.txt
backuping
ci/cd runner
rocket.chat
web analytics # matomo or something else
pastebin/files share/url shortener
bitwarden (?)
git (gitea or gitlab)

Readme:
list of apps with links and ports
wallabag:wallabag - change pass
change ssh listen port
sshd_config

check:

* base auths
* traefik dashboard https://www.leonpahole.com/2020/05/traefik-basic-setup.html
