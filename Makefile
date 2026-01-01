ARGS = $(filter-out $@,$(MAKECMDGOALS))

%:
	@:

.PHONY: deploy
deploy:
	ansible-playbook -i inventories/my-provision/inventory provisioning.yml --tags "$(ARGS)"

.PHONY: deploy-all
deploy-all:
	ansible-playbook -i inventories/my-provision/inventory provisioning.yml

.PHONY: bootstrap
bootstrap:
	ansible-playbook -i inventories/my-provision/inventory clean_hosts.yml
	@IP=$$(grep "ansible_host=" inventories/my-provision/inventory | head -n 1 | sed -e 's/.*ansible_host=\([^ ]*\).*/\1/'); \
	echo "-----------------------------------------------------------------------"; \
	echo "Cleanup complete."; \
	echo ""; \
	echo "ACTION REQUIRED:"; \
	echo "1. SSH into your server manually now: 'ssh root@$$IP'"; \
	echo "2. Accept the host key (type 'yes')."; \
	echo "3. Make everything your provider required to do interactively - cant automate that with ansible"; \
	echo "4. Exit the SSH session."; \
	echo ""; \
	echo "Then run 'make sshconfig', you will be asked a password."; \
	echo "-----------------------------------------------------------------------"

.PHONY: sshconfig
sshconfig:
	ansible-playbook -i inventories/my-provision/inventory sshconfig.yml
