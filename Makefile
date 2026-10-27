.DEFAULT_GOAL := deploy

include makefiles/config.mk
include $(filter-out makefiles/config.mk makefiles/private.mk,$(wildcard makefiles/*.mk))

%:
	@:
