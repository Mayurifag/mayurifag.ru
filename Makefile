HOST ?= nnnnn
INVENTORY = inventories/my-provision/inventory
ARGS = $(filter-out $@,$(MAKECMDGOALS))
PYTHON ?= python3

%:
	@:

.PHONY: deploy
deploy:
	@echo "==> Target host: [$(HOST)]"
	ansible-playbook -i $(INVENTORY) provisioning.yml --limit $(HOST) --tags "$(ARGS)"

.PHONY: deploy-all
deploy-all:
	@echo "==> Target host: [$(HOST)] (ALL roles)"
	ansible-playbook -i $(INVENTORY) provisioning.yml --limit $(HOST)

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

.PHONY: hosts
hosts:
	@ansible-inventory -i $(INVENTORY) --list --yaml

.PHONY: sync-watchtower-secrets
sync-watchtower-secrets:
	@$(PYTHON) scripts/sync_watchtower_github_secrets.py --inventory "$(INVENTORY)"

.PHONY: install-deps
install-deps:
	ansible-galaxy install -r requirements.yml
	ansible-galaxy collection install -r collections/requirements.yml

.PHONY: ci
ci:
	editorconfig-checker
	ansible-playbook -i inventories/sample/inventory provisioning.yml --syntax-check
	ansible-playbook -i inventories/sample/inventory clean_hosts.yml --syntax-check
	ansible-playbook -i inventories/sample/inventory sshconfig.yml --syntax-check
	ansible-lint
	yamllint .
	markdownlint-cli2 "**/*.{md,markdown}"
