.PHONY: bootstrap
bootstrap:
	@echo "==> Target host: [$(HOST)]"
	ansible-playbook -i $(INVENTORY) clean_hosts.yml --limit $(HOST)
	@IP=$$(ansible-inventory -i $(INVENTORY) --host $(HOST) | python3 -c "import json,sys; print(json.load(sys.stdin)['ansible_host'])"); \
	HN=$$(ansible-inventory -i $(INVENTORY) --host $(HOST) | python3 -c "import json,sys; print(json.load(sys.stdin)['server_hostname'])"); \
	echo "-----------------------------------------------------------------------"; \
	echo "Cleanup complete for [$(HOST)] -> $$HN ($$IP)."; \
	echo ""; \
	echo "ACTION REQUIRED:"; \
	echo "1. SSH into your server manually now: 'ssh root@$$IP'"; \
	echo "2. Accept the host key (type 'yes')."; \
	echo "3. Make everything your provider required to do interactively - cant automate that with ansible"; \
	echo "4. Exit the SSH session."; \
	echo ""; \
	echo "Then run 'make sshconfig HOST=$(HOST)'"; \
	echo "-----------------------------------------------------------------------"

.PHONY: sshconfig
sshconfig:
	@echo "==> Target host: [$(HOST)]"
	ansible-playbook -i $(INVENTORY) sshconfig.yml --limit $(HOST)
