DEPLOY_REMOTE ?=
DEPLOY_FORWARD_AGENT ?= no
REMOTE_DEPLOY = $(PYTHON) scripts/remote_deploy.py --remote "$(DEPLOY_REMOTE)" $(if $(filter yes,$(DEPLOY_FORWARD_AGENT)),--forward-agent)

ifeq ($(OS),Windows_NT)
USE_REMOTE = yes
# Git's sh cannot resolve Python .cmd shims reliably; use the native shell here.
deploy deploy-all remote-sync remote-ci: SHELL := cmd.exe
else
USE_REMOTE = $(if $(strip $(DEPLOY_REMOTE)),yes,)
endif

.PHONY: deploy
deploy:
ifneq ($(USE_REMOTE),)
	@$(REMOTE_DEPLOY) --action deploy --target "$(HOST)" --inventory "$(INVENTORY)" --tags "$(ARGS)"
else
	@echo "==> Target host: [$(HOST)]"
	ansible-playbook -i "$(INVENTORY)" provisioning.yml --limit "$(HOST)" --tags "$(ARGS)"
endif

.PHONY: deploy-all
deploy-all:
ifneq ($(USE_REMOTE),)
	@$(REMOTE_DEPLOY) --action deploy-all --target "$(HOST)" --inventory "$(INVENTORY)"
else
	@echo "==> Target host: [$(HOST)] (ALL roles)"
	ansible-playbook -i "$(INVENTORY)" provisioning.yml --limit "$(HOST)"
endif

.PHONY: remote-sync remote-ci
remote-sync:
	@$(REMOTE_DEPLOY) --action sync

remote-ci:
	@$(REMOTE_DEPLOY) --action ci
