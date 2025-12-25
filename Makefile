ifndef SPEC_FILE
$(error SPEC_FILE is not defined. Please define SPEC_FILE as a spec file you want to build using this Makefile.)
endif

BUILD_DEPENDENCIES := dnf-utils rpmdevtools rpm-build rpm-sign
LINT_DEPENDENCIES := rpmlint
PUBLISH_DEPENDENCIES := createrepo gnupg redhat-rpm-config rpm-sign s3cmd
SOURCES_DIRECTORY := $(shell pwd)/SOURCES
DOCKER_IMAGE_NAME := ghcr.io/almalinux/9-base
DOCKER_IMAGE_TAG := 9
DOCKER_WORK_DIRECTORY := /srv
REDHAT_DISTRIBUTION_TYPE ?= $(shell /usr/lib/rpm/redhat/dist.sh --disttype)
REDHAT_DISTRIBUTION_VERSION ?= $(shell /usr/lib/rpm/redhat/dist.sh --distnum)
REDHAT_DISTRIBUTION_ARCHITECTURE ?= $(shell /usr/bin/arch)
GPG_PUBLIC_KEY := yum-repositories-2035-11-30.gpg
GPG_ASCII_PUBLIC_KEY := yum-repositories-2035-11-30.asc
GPG_KEY_ID := 9E0EBF3C3BD6B9B0

define run_in_docker
	docker run \
		--mount "type=bind,source=$(shell pwd),target=$(DOCKER_WORK_DIRECTORY)" \
		--workdir "$(DOCKER_WORK_DIRECTORY)" \
		--rm \
		--tty \
		$(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG) \
		sh -c "dnf --assumeyes install make && make $(MAKEFLAGS) $(1)"
endef

define run_in_podman
	podman run \
		--mount "type=bind,source=$(shell pwd),target=$(DOCKER_WORK_DIRECTORY)" \
		--workdir "$(DOCKER_WORK_DIRECTORY)" \
		--rm \
		--tty \
		$(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG) \
		sh -c "dnf --assumeyes install make && make $(MAKEFLAGS) $(1)"
endef

default: build

build: install_build_dependencies get_spec_sources install_spec_build_dependencies build_package sign_rpm_packages verify_rpm_packages

build_in_docker:
	@$(call run_in_docker, build)

build_in_podman:
	@$(call run_in_podman, build)

lint: install_lint_dependencies lint_spec

lint_in_docker:
	@$(call run_in_docker, lint)

lint_in_podman:
	@$(call run_in_podman, lint)

publish: install_publish_dependencies create_yum_repository sign_yum_repository verify_yum_repository publish_yum_repository_to_s3

publish_in_docker:
	@$(call run_in_docker, publish)

publish_in_podman:
	@$(call run_in_podman, publish)

install_build_dependencies:
	dnf --assumeyes install $(BUILD_DEPENDENCIES)

install_lint_dependencies:
	dnf --assumeyes install epel-release
	dnf --assumeyes install $(LINT_DEPENDENCIES)

install_publish_dependencies:
	dnf --assumeyes install epel-release
	dnf --assumeyes install $(PUBLISH_DEPENDENCIES)

lint_spec:
	rpmlint $(SPEC_FILE)

get_spec_sources:
	spectool --get-files --directory $(SOURCES_DIRECTORY) $(SPEC_FILE)

install_spec_build_dependencies:
	yum-builddep --assumeyes $(SPEC_FILE)

build_package:
	rpmbuild -bb --define "_topdir $(shell pwd)" $(SPEC_FILE)

sign_rpm_packages:
	printf '%s' "$${GPG_PRIVATE_KEY}" | base64 --decode | gpg --batch --yes --import
	echo "unlock" | gpg --batch --yes --passphrase ${GPG_PASSPHRASE} --pinentry-mode loopback --sign --output /dev/null
	for rpm_package_to_sign in RPMS/$(YUM_REPOSITORY_NAME)/$(REDHAT_DISTRIBUTION_TYPE)/$(REDHAT_DISTRIBUTION_VERSION)/$(REDHAT_DISTRIBUTION_ARCHITECTURE)/*.rpm; do rpmsign --key-id="$(GPG_KEY_ID)" --addsign "$${rpm_package_to_sign}"; done

verify_rpm_packages:
	rpmkeys --import ./$(GPG_ASCII_PUBLIC_KEY)
	for rpm_package_to_verify in RPMS/$(YUM_REPOSITORY_NAME)/$(REDHAT_DISTRIBUTION_TYPE)/$(REDHAT_DISTRIBUTION_VERSION)/$(REDHAT_DISTRIBUTION_ARCHITECTURE)/*.rpm; do rpmkeys --checksig "$${rpm_package_to_verify}"; done

create_yum_repository:
	createrepo --verbose RPMS/$(YUM_REPOSITORY_NAME)/$(REDHAT_DISTRIBUTION_TYPE)/$(REDHAT_DISTRIBUTION_VERSION)/$(REDHAT_DISTRIBUTION_ARCHITECTURE)

sign_yum_repository:
	printf '%s' "$${GPG_PRIVATE_KEY}" | base64 --decode | gpg --batch --yes --import
	gpg --batch --yes --passphrase ${GPG_PASSPHRASE} --pinentry-mode loopback --detach-sign --armor RPMS/$(YUM_REPOSITORY_NAME)/$(REDHAT_DISTRIBUTION_TYPE)/$(REDHAT_DISTRIBUTION_VERSION)/$(REDHAT_DISTRIBUTION_ARCHITECTURE)/repodata/repomd.xml

verify_yum_repository:
	gpgv --keyring ./$(GPG_PUBLIC_KEY) RPMS/$(YUM_REPOSITORY_NAME)/$(REDHAT_DISTRIBUTION_TYPE)/$(REDHAT_DISTRIBUTION_VERSION)/$(REDHAT_DISTRIBUTION_ARCHITECTURE)/repodata/repomd.xml.asc RPMS/$(YUM_REPOSITORY_NAME)/$(REDHAT_DISTRIBUTION_TYPE)/$(REDHAT_DISTRIBUTION_VERSION)/$(REDHAT_DISTRIBUTION_ARCHITECTURE)/repodata/repomd.xml
	cp $(GPG_ASCII_PUBLIC_KEY) $(GPG_PUBLIC_KEY) RPMS/$(YUM_REPOSITORY_NAME)

publish_yum_repository_to_s3:
	s3cmd sync \
		--host=$(YUM_REPOSITORIES_S3_ENDPOINT) \
		--host-bucket="%(bucket)s.${YUM_REPOSITORIES_S3_ENDPOINT}" \
		--access_key=${YUM_REPOSITORIES_ACCESS_KEY} \
		--secret_key=${YUM_REPOSITORIES_SECRET_KEY} \
		--acl-public \
		--verbose \
		RPMS/$(YUM_REPOSITORY_NAME) \
		s3://${YUM_REPOSITORIES_BUCKET_NAME}/
