ARGS = $(filter-out $@,$(MAKECMDGOALS))

%:
	@:

# No tags = deploy everything
.PHONY: deploy
deploy:
	ansible-playbook -i inventories/my-provision/inventory provisioning.yml --tags "$(ARGS)"

.PHONY: bootstrap
bootstrap:
	ansible-playbook -i inventories/my-provision/inventory bootstrap.yml
