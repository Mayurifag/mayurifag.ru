.PHONY: deploy-tag
deploy-tag:
	ansible-playbook -i inventories/my-provision/inventory provisioning.yml --tags "$(ARGS)"

.PHONY: deploy
deploy: deploy-tag
