ifeq ($(OS),Windows_NT)
sync-watchtower-secrets: SHELL := cmd.exe
endif

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
