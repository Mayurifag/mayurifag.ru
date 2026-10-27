HOST ?= nnnnn
INVENTORY = inventories/my-provision/inventory
ARGS = $(filter-out $@,$(MAKECMDGOALS))
ifeq ($(OS),Windows_NT)
PYTHON ?= cmd /c python3
else
PYTHON ?= python3
endif
EDITORCONFIG_CHECKER ?= editorconfig-checker

-include makefiles/private.mk
