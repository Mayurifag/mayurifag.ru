deploy-prod:
	ansible-playbook -i inventories/my-provision/inventory provisioning.yml

deploy-tag:
	ansible-playbook -i inventories/my-provision/inventory provisioning.yml --tags "$(ARGS)"

.PHONY: deploy-prod deploy-tag
