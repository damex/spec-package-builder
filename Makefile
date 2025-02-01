ifndef SPEC_FILE
$(error SPEC_FILE is not defined. Please define SPEC_FILE as a spec file you want to build using this Makefile.)
endif

BUILD_DEPENDENCIES := rpmdevtools rpm-build dnf-utils
SOURCES_DIR := $(shell pwd)/SOURCES

default: install_build_dependencies get_spec_sources install_spec_build_dependencies build_package

install_build_dependencies:
	dnf --assumeyes install $(BUILD_DEPENDENCIES)

get_spec_sources:
	spectool --get-files --directory $(SOURCES_DIR) $(SPEC_FILE)

install_spec_build_dependencies:
	yum-builddep --assumeyes $(SPEC_FILE)

build_package:
	rpmbuild -bb --define "_topdir $(shell pwd)" $(SPEC_FILE)
