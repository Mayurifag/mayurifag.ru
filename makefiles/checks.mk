.PHONY: ci
ci:
	$(EDITORCONFIG_CHECKER)
	ansible-playbook -i inventories/sample/inventory provisioning.yml --syntax-check
	ansible-playbook -i inventories/sample/inventory clean_hosts.yml --syntax-check
	ansible-playbook -i inventories/sample/inventory sshconfig.yml --syntax-check
	ansible-lint
	yamllint .
	markdownlint-cli2 "**/*.{md,markdown}"
