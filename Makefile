ifndef SPEC_FILE
$(error SPEC_FILE is not defined. Please define SPEC_FILE as a spec file you want to build using this Makefile.)
endif

BUILD_DEPENDENCIES := rpmdevtools rpm-build dnf-utils
LINT_DEPENDENCIES := rpmlint
SOURCES_DIRECTORY := $(shell pwd)/SOURCES
DOCKER_IMAGE_NAME := almalinux
DOCKER_IMAGE_TAG := 9
DOCKER_WORK_DIRECTORY := /srv

define run_in_docker
	docker run \
		--mount "type=bind,source=$(shell pwd),target=$(DOCKER_WORK_DIRECTORY)" \
		--workdir "$(DOCKER_WORK_DIRECTORY)" \
		--rm \
		--tty \
		$(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG) \
		sh -c "dnf --assumeyes install make && make SPEC_FILE=$(SPEC_FILE) $(1)"
endef

default: build

build: install_build_dependencies get_spec_sources install_spec_build_dependencies build_package

build_in_docker:
	@$(call run_in_docker, build)

lint: install_lint_dependencies lint_spec

lint_in_docker:
	@$(call run_in_docker, lint)

install_build_dependencies:
	dnf --assumeyes install $(BUILD_DEPENDENCIES)

install_lint_dependencies:
	dnf --assumeyes install $(LINT_DEPENDENCIES)

lint_spec:
	rpmlint $(SPEC_FILE)

get_spec_sources:
	spectool --get-files --directory $(SOURCES_DIRECTORY) $(SPEC_FILE)

install_spec_build_dependencies:
	yum-builddep --assumeyes $(SPEC_FILE)

build_package:
	rpmbuild -bb --define "_topdir $(shell pwd)" $(SPEC_FILE)
