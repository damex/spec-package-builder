%define debug_package %{nil}
%global _build_id_links none
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/zfs/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog
%global _dracutdir %(pkg-config --variable=dracutdir dracut)

Name: zfs
Version: 2.4.1
Release: 1%{?dist}
Summary: OpenZFS file system user utilities
License: CDDL-1.0
URL: https://openzfs.github.io/openzfs-docs/
Source0: https://github.com/openzfs/zfs/releases/download/zfs-%{version}/zfs-%{version}.tar.gz
ExclusiveArch: x86_64 aarch64
%{?systemd_requires}
BuildRequires: dracut
BuildRequires: gcc
BuildRequires: libaio-devel
BuildRequires: libattr-devel
BuildRequires: libblkid-devel
BuildRequires: libtirpc-devel
BuildRequires: libuuid-devel
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: pam-devel
BuildRequires: systemd-devel
BuildRequires: systemd-rpm-macros
BuildRequires: zlib-devel
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: openssl
Requires: python3
Requires: sysstat
Requires: util-linux
Requires: zfs-dkms = %{version}

%package -n %{name}-libs
Summary: OpenZFS shared libraries

%package -n %{name}-devel
Summary: Development files for OpenZFS
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%package -n %{name}-dracut
Summary: OpenZFS dracut module
Requires: %{name} = %{version}-%{release}
Requires: dracut

%package -n %{name}-pam
Summary: OpenZFS PAM module for encryption
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
OpenZFS userspace utilities including zfs, zpool, zdb, zed, and related tools.

%description -n %{name}-libs
Shared libraries for OpenZFS required by userspace utilities.

%description -n %{name}-devel
Development headers and pkg-config files for building against OpenZFS libraries.

%description -n %{name}-dracut
Dracut module for mounting ZFS datasets during boot.

%description -n %{name}-pam
PAM module for automatic unlocking of ZFS encrypted datasets at login.

%prep
%autosetup -n %{name}-%{version}

%build
%configure \
    --with-config=user \
    --with-mounthelperdir=%{_sbindir} \
    --with-udevdir=%{_prefix}/lib/udev \
    --with-udevruledir=%{_udevrulesdir} \
    --with-dracutdir=%{_dracutdir} \
    --with-pammoduledir=%{_libdir}/security \
    --with-pamconfigsdir=%{_datadir}/pam-configs \
    --with-pkgconfigdir=%{_libdir}/pkgconfig \
    --with-python=%{__python3} \
    --enable-systemd \
    --disable-sysvinit \
    --disable-static \
    --disable-pyzfs
%make_build

%install
# bashcompletiondir is hardcoded to /etc/bash_completion.d in configure
%make_install bashcompletiondir=%{_datadir}/bash-completion/completions
%{__rm} %{buildroot}%{_libdir}/libnvpair.la
%{__rm} %{buildroot}%{_libdir}/libuutil.la
%{__rm} %{buildroot}%{_libdir}/libzfs.la
%{__rm} %{buildroot}%{_libdir}/libzfs_core.la
%{__rm} %{buildroot}%{_libdir}/libzfsbootenv.la
%{__rm} %{buildroot}%{_libdir}/libzpool.la
%{__rm} -f %{buildroot}%{_libdir}/security/pam_zfs_key.la
%{__rm} -f %{buildroot}%{_sysconfdir}/%{name}/zfs-functions
%{__rm} -f %{buildroot}%{_sysconfdir}/default/zfs
%{__rm} -f %{buildroot}%{_sysconfdir}/sysconfig/zfs
%{__rm} -rf %{buildroot}%{_sysconfdir}/init.d
%{__rm} -f %{buildroot}%{_sysconfdir}/sudoers.d/zfs
%{__rm} -rf %{buildroot}%{_datadir}/initramfs-tools
%{__rm} -rf %{buildroot}%{_datadir}/pam-configs
%{__rm} -rf %{buildroot}%{_datadir}/%{name}/zfs-tests
%{__rm} -rf %{buildroot}%{_datadir}/%{name}/test-runner
%{__rm} -rf %{buildroot}%{_datadir}/%{name}/runfiles
%{__rm} -f %{buildroot}%{_datadir}/%{name}/zfs-helpers.sh
%{__rm} -f %{buildroot}%{_datadir}/%{name}/zfs-tests.sh
%{__rm} -f %{buildroot}%{_datadir}/%{name}/zfs.sh
%{__rm} -f %{buildroot}%{_datadir}/%{name}/zimport.sh
%{__rm} -f %{buildroot}%{_datadir}/%{name}/zloop.sh
%{__rm} -f %{buildroot}%{_mandir}/man1/test-runner.1*

%ldconfig_scriptlets -n %{name}-libs

%post
%systemd_post zfs-import-cache.service zfs-import-scan.service zfs-import.target zfs-mount.service zfs-share.service zfs-volume-wait.service zfs-zed.service zfs.target zfs-volumes.target

%preun
%systemd_preun zfs-import-cache.service zfs-import-scan.service zfs-import.target zfs-mount.service zfs-share.service zfs-volume-wait.service zfs-zed.service zfs.target zfs-volumes.target

%postun
%systemd_postun zfs-import-cache.service zfs-import-scan.service zfs-import.target zfs-mount.service zfs-share.service zfs-volume-wait.service zfs-zed.service zfs.target zfs-volumes.target

%files
%defattr(-,root,root,-)
%license LICENSE COPYRIGHT NOTICE
%{_sbindir}/fsck.zfs
%{_sbindir}/mount.zfs
%{_sbindir}/zdb
%{_sbindir}/zed
%{_sbindir}/zfs
%{_sbindir}/zfs_ids_to_path
%{_sbindir}/zgenhostid
%{_sbindir}/zhack
%{_sbindir}/zinject
%{_sbindir}/zpool
%{_sbindir}/zstream
%{_sbindir}/zstreamdump
%{_sbindir}/ztest
%{_bindir}/raidz_test
%{_bindir}/zvol_wait
%{_bindir}/zarcsummary
%{_bindir}/zarcstat
%{_bindir}/dbufstat
%{_bindir}/zilstat
# systemd units
%{_unitdir}/zfs-import-cache.service
%{_unitdir}/zfs-import-scan.service
%{_unitdir}/zfs-import.service
%{_unitdir}/zfs-import.target
%{_unitdir}/zfs-load-key.service
%{_unitdir}/zfs-mount.service
%{_unitdir}/zfs-mount@.service
%{_unitdir}/zfs-scrub-monthly@.timer
%{_unitdir}/zfs-scrub-weekly@.timer
%{_unitdir}/zfs-scrub@.service
%{_unitdir}/zfs-share.service
%{_unitdir}/zfs-trim-monthly@.timer
%{_unitdir}/zfs-trim-weekly@.timer
%{_unitdir}/zfs-trim@.service
%{_unitdir}/zfs-volume-wait.service
%{_unitdir}/zfs-volumes.target
%{_unitdir}/zfs-zed.service
%{_unitdir}/zfs.target
%{_presetdir}/50-zfs.preset
%{_systemdgeneratordir}/zfs-mount-generator
%{_modulesloaddir}/zfs.conf
# udev
%{_prefix}/lib/udev/vdev_id
%{_prefix}/lib/udev/zvol_id
%{_udevrulesdir}/60-zvol.rules
%{_udevrulesdir}/69-vdev.rules
%{_udevrulesdir}/90-zfs.rules
# /etc/zfs config
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/vdev_id.conf.alias.example
%config(noreplace) %{_sysconfdir}/%{name}/vdev_id.conf.multipath.example
%config(noreplace) %{_sysconfdir}/%{name}/vdev_id.conf.sas_direct.example
%config(noreplace) %{_sysconfdir}/%{name}/vdev_id.conf.sas_switch.example
%config(noreplace) %{_sysconfdir}/%{name}/vdev_id.conf.scsi.example
# /etc/zfs/zed.d config
%dir %{_sysconfdir}/%{name}/zed.d
%config(noreplace) %{_sysconfdir}/%{name}/zed.d/zed-functions.sh
%config(noreplace) %{_sysconfdir}/%{name}/zed.d/zed.rc
%config(noreplace) %{_sysconfdir}/%{name}/zed.d/all-syslog.sh
%config(noreplace) %{_sysconfdir}/%{name}/zed.d/data-notify.sh
%config(noreplace) %{_sysconfdir}/%{name}/zed.d/deadman-sync-slot_off.sh
%config(noreplace) %{_sysconfdir}/%{name}/zed.d/history_event-zfs-list-cacher.sh
%config(noreplace) %{_sysconfdir}/%{name}/zed.d/pool_import-sync-led.sh
%config(noreplace) %{_sysconfdir}/%{name}/zed.d/resilver_finish-notify.sh
%config(noreplace) %{_sysconfdir}/%{name}/zed.d/resilver_finish-start-scrub.sh
%config(noreplace) %{_sysconfdir}/%{name}/zed.d/scrub_finish-notify.sh
%config(noreplace) %{_sysconfdir}/%{name}/zed.d/statechange-notify.sh
%config(noreplace) %{_sysconfdir}/%{name}/zed.d/statechange-sync-led.sh
%config(noreplace) %{_sysconfdir}/%{name}/zed.d/statechange-sync-slot_off.sh
%config(noreplace) %{_sysconfdir}/%{name}/zed.d/vdev_attach-sync-led.sh
%config(noreplace) %{_sysconfdir}/%{name}/zed.d/vdev_clear-sync-led.sh
# /etc/zfs/zpool.d config
%dir %{_sysconfdir}/%{name}/zpool.d
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/ata_err
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/cmd_to
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/defect
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/dm-deps
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/enc
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/encdev
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/fault_led
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/health
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/hours_on
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/iostat
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/iostat-10s
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/iostat-1s
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/label
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/locate_led
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/lsblk
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/media
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/model
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/nonmed
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/nvme_err
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/off_ucor
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/pend_sec
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/pwr_cyc
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/r_proc
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/r_ucor
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/realloc
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/rep_ucor
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/serial
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/ses
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/size
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/slot
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/smart
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/smart_test
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/smartx
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/temp
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/test_ended
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/test_progress
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/test_status
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/test_type
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/upath
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/vendor
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/w_proc
%config(noreplace) %{_sysconfdir}/%{name}/zpool.d/w_ucor
# libexec
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/zfs_prepare_disk
%{_libexecdir}/%{name}/zpool_influxdb
%dir %{_libexecdir}/%{name}/zed.d
%{_libexecdir}/%{name}/zed.d/all-debug.sh
%{_libexecdir}/%{name}/zed.d/all-syslog.sh
%{_libexecdir}/%{name}/zed.d/data-notify.sh
%{_libexecdir}/%{name}/zed.d/deadman-sync-slot_off.sh
%{_libexecdir}/%{name}/zed.d/generic-notify.sh
%{_libexecdir}/%{name}/zed.d/history_event-zfs-list-cacher.sh
%{_libexecdir}/%{name}/zed.d/pool_import-sync-led.sh
%{_libexecdir}/%{name}/zed.d/resilver_finish-notify.sh
%{_libexecdir}/%{name}/zed.d/resilver_finish-start-scrub.sh
%{_libexecdir}/%{name}/zed.d/scrub_finish-notify.sh
%{_libexecdir}/%{name}/zed.d/statechange-notify.sh
%{_libexecdir}/%{name}/zed.d/statechange-sync-led.sh
%{_libexecdir}/%{name}/zed.d/statechange-sync-slot_off.sh
%{_libexecdir}/%{name}/zed.d/trim_finish-notify.sh
%{_libexecdir}/%{name}/zed.d/vdev_attach-sync-led.sh
%{_libexecdir}/%{name}/zed.d/vdev_clear-sync-led.sh
%dir %{_libexecdir}/%{name}/zpool.d
%{_libexecdir}/%{name}/zpool.d/ata_err
%{_libexecdir}/%{name}/zpool.d/cmd_to
%{_libexecdir}/%{name}/zpool.d/defect
%{_libexecdir}/%{name}/zpool.d/dm-deps
%{_libexecdir}/%{name}/zpool.d/enc
%{_libexecdir}/%{name}/zpool.d/encdev
%{_libexecdir}/%{name}/zpool.d/fault_led
%{_libexecdir}/%{name}/zpool.d/health
%{_libexecdir}/%{name}/zpool.d/hours_on
%{_libexecdir}/%{name}/zpool.d/iostat
%{_libexecdir}/%{name}/zpool.d/iostat-10s
%{_libexecdir}/%{name}/zpool.d/iostat-1s
%{_libexecdir}/%{name}/zpool.d/label
%{_libexecdir}/%{name}/zpool.d/locate_led
%{_libexecdir}/%{name}/zpool.d/lsblk
%{_libexecdir}/%{name}/zpool.d/media
%{_libexecdir}/%{name}/zpool.d/model
%{_libexecdir}/%{name}/zpool.d/nonmed
%{_libexecdir}/%{name}/zpool.d/nvme_err
%{_libexecdir}/%{name}/zpool.d/off_ucor
%{_libexecdir}/%{name}/zpool.d/pend_sec
%{_libexecdir}/%{name}/zpool.d/pwr_cyc
%{_libexecdir}/%{name}/zpool.d/r_proc
%{_libexecdir}/%{name}/zpool.d/r_ucor
%{_libexecdir}/%{name}/zpool.d/realloc
%{_libexecdir}/%{name}/zpool.d/rep_ucor
%{_libexecdir}/%{name}/zpool.d/serial
%{_libexecdir}/%{name}/zpool.d/ses
%{_libexecdir}/%{name}/zpool.d/size
%{_libexecdir}/%{name}/zpool.d/slot
%{_libexecdir}/%{name}/zpool.d/smart
%{_libexecdir}/%{name}/zpool.d/smart_test
%{_libexecdir}/%{name}/zpool.d/smartx
%{_libexecdir}/%{name}/zpool.d/temp
%{_libexecdir}/%{name}/zpool.d/test_ended
%{_libexecdir}/%{name}/zpool.d/test_progress
%{_libexecdir}/%{name}/zpool.d/test_status
%{_libexecdir}/%{name}/zpool.d/test_type
%{_libexecdir}/%{name}/zpool.d/upath
%{_libexecdir}/%{name}/zpool.d/vendor
%{_libexecdir}/%{name}/zpool.d/w_proc
%{_libexecdir}/%{name}/zpool.d/w_ucor
# compatibility data
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/common.sh
%dir %{_datadir}/%{name}/compatibility.d
%{_datadir}/%{name}/compatibility.d/2018
%{_datadir}/%{name}/compatibility.d/2019
%{_datadir}/%{name}/compatibility.d/2020
%{_datadir}/%{name}/compatibility.d/2021
%{_datadir}/%{name}/compatibility.d/compat-2018
%{_datadir}/%{name}/compatibility.d/compat-2019
%{_datadir}/%{name}/compatibility.d/compat-2020
%{_datadir}/%{name}/compatibility.d/compat-2021
%{_datadir}/%{name}/compatibility.d/freebsd-11.0
%{_datadir}/%{name}/compatibility.d/freebsd-11.1
%{_datadir}/%{name}/compatibility.d/freebsd-11.2
%{_datadir}/%{name}/compatibility.d/freebsd-11.3
%{_datadir}/%{name}/compatibility.d/freebsd-11.4
%{_datadir}/%{name}/compatibility.d/freebsd-12.0
%{_datadir}/%{name}/compatibility.d/freebsd-12.1
%{_datadir}/%{name}/compatibility.d/freebsd-12.2
%{_datadir}/%{name}/compatibility.d/freebsd-12.3
%{_datadir}/%{name}/compatibility.d/freebsd-12.4
%{_datadir}/%{name}/compatibility.d/freebsd-13.0
%{_datadir}/%{name}/compatibility.d/freebsd-13.1
%{_datadir}/%{name}/compatibility.d/freebsd-13.2
%{_datadir}/%{name}/compatibility.d/freenas-9.10.2
%{_datadir}/%{name}/compatibility.d/freenas-11.0
%{_datadir}/%{name}/compatibility.d/freenas-11.1
%{_datadir}/%{name}/compatibility.d/freenas-11.2
%{_datadir}/%{name}/compatibility.d/freenas-11.3
%{_datadir}/%{name}/compatibility.d/grub2
%{_datadir}/%{name}/compatibility.d/grub2-2.06
%{_datadir}/%{name}/compatibility.d/grub2-2.12
%{_datadir}/%{name}/compatibility.d/openzfs-2.0-freebsd
%{_datadir}/%{name}/compatibility.d/openzfs-2.0-linux
%{_datadir}/%{name}/compatibility.d/openzfs-2.1-freebsd
%{_datadir}/%{name}/compatibility.d/openzfs-2.1-linux
%{_datadir}/%{name}/compatibility.d/openzfs-2.2
%{_datadir}/%{name}/compatibility.d/openzfs-2.2-freebsd
%{_datadir}/%{name}/compatibility.d/openzfs-2.2-linux
%{_datadir}/%{name}/compatibility.d/openzfs-2.3
%{_datadir}/%{name}/compatibility.d/openzfs-2.3-freebsd
%{_datadir}/%{name}/compatibility.d/openzfs-2.3-linux
%{_datadir}/%{name}/compatibility.d/openzfs-2.4
%{_datadir}/%{name}/compatibility.d/openzfs-2.4-freebsd
%{_datadir}/%{name}/compatibility.d/openzfs-2.4-linux
%{_datadir}/%{name}/compatibility.d/openzfsonosx-1.7.0
%{_datadir}/%{name}/compatibility.d/openzfsonosx-1.8.1
%{_datadir}/%{name}/compatibility.d/openzfsonosx-1.9.3
%{_datadir}/%{name}/compatibility.d/openzfsonosx-1.9.4
%{_datadir}/%{name}/compatibility.d/truenas-12.0
%{_datadir}/%{name}/compatibility.d/ubuntu-18.04
%{_datadir}/%{name}/compatibility.d/ubuntu-20.04
%{_datadir}/%{name}/compatibility.d/ubuntu-22.04
%{_datadir}/%{name}/compatibility.d/zol-0.6.1
%{_datadir}/%{name}/compatibility.d/zol-0.6.4
%{_datadir}/%{name}/compatibility.d/zol-0.6.5
%{_datadir}/%{name}/compatibility.d/zol-0.7
%{_datadir}/%{name}/compatibility.d/zol-0.8
# bash completions
%{_datadir}/bash-completion/completions/zfs
%{_datadir}/bash-completion/completions/zpool
# man1
%{_mandir}/man1/zarcstat.1*
%{_mandir}/man1/zhack.1*
%{_mandir}/man1/ztest.1*
%{_mandir}/man1/raidz_test.1*
%{_mandir}/man1/zvol_wait.1*
# man4
%{_mandir}/man4/spl.4*
%{_mandir}/man4/zfs.4*
# man5
%{_mandir}/man5/vdev_id.conf.5*
# man7
%{_mandir}/man7/vdevprops.7*
%{_mandir}/man7/zfsconcepts.7*
%{_mandir}/man7/zfsprops.7*
%{_mandir}/man7/zpool-features.7*
%{_mandir}/man7/zpoolconcepts.7*
%{_mandir}/man7/zpoolprops.7*
# man8
%{_mandir}/man8/fsck.zfs.8*
%{_mandir}/man8/mount.zfs.8*
%{_mandir}/man8/vdev_id.8*
%{_mandir}/man8/zdb.8*
%{_mandir}/man8/zed.8*
%{_mandir}/man8/zfs.8*
%{_mandir}/man8/zfs-allow.8*
%{_mandir}/man8/zfs-bookmark.8*
%{_mandir}/man8/zfs-change-key.8*
%{_mandir}/man8/zfs-clone.8*
%{_mandir}/man8/zfs-create.8*
%{_mandir}/man8/zfs-destroy.8*
%{_mandir}/man8/zfs-diff.8*
%{_mandir}/man8/zfs-get.8*
%{_mandir}/man8/zfs-groupspace.8*
%{_mandir}/man8/zfs-hold.8*
%{_mandir}/man8/zfs-inherit.8*
%{_mandir}/man8/zfs-list.8*
%{_mandir}/man8/zfs-load-key.8*
%{_mandir}/man8/zfs-mount.8*
%{_mandir}/man8/zfs-mount-generator.8*
%{_mandir}/man8/zfs-program.8*
%{_mandir}/man8/zfs-project.8*
%{_mandir}/man8/zfs-projectspace.8*
%{_mandir}/man8/zfs-promote.8*
%{_mandir}/man8/zfs-receive.8*
%{_mandir}/man8/zfs-recv.8*
%{_mandir}/man8/zfs-redact.8*
%{_mandir}/man8/zfs-release.8*
%{_mandir}/man8/zfs-rename.8*
%{_mandir}/man8/zfs-rewrite.8*
%{_mandir}/man8/zfs-rollback.8*
%{_mandir}/man8/zfs-send.8*
%{_mandir}/man8/zfs-set.8*
%{_mandir}/man8/zfs-share.8*
%{_mandir}/man8/zfs-snapshot.8*
%{_mandir}/man8/zfs-unallow.8*
%{_mandir}/man8/zfs-unload-key.8*
%{_mandir}/man8/zfs-unmount.8*
%{_mandir}/man8/zfs-unzone.8*
%{_mandir}/man8/zfs-upgrade.8*
%{_mandir}/man8/zfs-userspace.8*
%{_mandir}/man8/zfs-wait.8*
%{_mandir}/man8/zfs-zone.8*
%{_mandir}/man8/zfs_ids_to_path.8*
%{_mandir}/man8/zfs_prepare_disk.8*
%{_mandir}/man8/zgenhostid.8*
%{_mandir}/man8/zinject.8*
%{_mandir}/man8/zpool.8*
%{_mandir}/man8/zpool-add.8*
%{_mandir}/man8/zpool-attach.8*
%{_mandir}/man8/zpool-checkpoint.8*
%{_mandir}/man8/zpool-clear.8*
%{_mandir}/man8/zpool-create.8*
%{_mandir}/man8/zpool-ddtprune.8*
%{_mandir}/man8/zpool-destroy.8*
%{_mandir}/man8/zpool-detach.8*
%{_mandir}/man8/zpool-events.8*
%{_mandir}/man8/zpool-export.8*
%{_mandir}/man8/zpool-get.8*
%{_mandir}/man8/zpool-history.8*
%{_mandir}/man8/zpool-import.8*
%{_mandir}/man8/zpool-initialize.8*
%{_mandir}/man8/zpool-iostat.8*
%{_mandir}/man8/zpool-labelclear.8*
%{_mandir}/man8/zpool-list.8*
%{_mandir}/man8/zpool-offline.8*
%{_mandir}/man8/zpool-online.8*
%{_mandir}/man8/zpool-prefetch.8*
%{_mandir}/man8/zpool-reguid.8*
%{_mandir}/man8/zpool-remove.8*
%{_mandir}/man8/zpool-reopen.8*
%{_mandir}/man8/zpool-replace.8*
%{_mandir}/man8/zpool-resilver.8*
%{_mandir}/man8/zpool-scrub.8*
%{_mandir}/man8/zpool-set.8*
%{_mandir}/man8/zpool-split.8*
%{_mandir}/man8/zpool-status.8*
%{_mandir}/man8/zpool-sync.8*
%{_mandir}/man8/zpool-trim.8*
%{_mandir}/man8/zpool-upgrade.8*
%{_mandir}/man8/zpool-wait.8*
%{_mandir}/man8/zpool_influxdb.8*
%{_mandir}/man8/zstream.8*
%{_mandir}/man8/zstreamdump.8*

%files -n %{name}-libs
%defattr(-,root,root,-)
%license LICENSE
%{_libdir}/libnvpair.so.3
%{_libdir}/libnvpair.so.3.1.0
%{_libdir}/libuutil.so.3
%{_libdir}/libuutil.so.3.0.0
%{_libdir}/libzfs.so.7
%{_libdir}/libzfs.so.7.0.0
%{_libdir}/libzfs_core.so.3
%{_libdir}/libzfs_core.so.3.0.0
%{_libdir}/libzfsbootenv.so.1
%{_libdir}/libzfsbootenv.so.1.0.0
%{_libdir}/libzpool.so.7
%{_libdir}/libzpool.so.7.0.0

%files -n %{name}-devel
%defattr(-,root,root,-)
%license LICENSE
%{_libdir}/libnvpair.so
%{_libdir}/libuutil.so
%{_libdir}/libzfs.so
%{_libdir}/libzfs_core.so
%{_libdir}/libzfsbootenv.so
%{_libdir}/libzpool.so
%{_libdir}/pkgconfig/libzfs.pc
%{_libdir}/pkgconfig/libzfs_core.pc
%{_libdir}/pkgconfig/libzfsbootenv.pc
%{_includedir}/libspl/*.h
%{_includedir}/libspl/rpc/*.h
%{_includedir}/libspl/sys/*.h
%{_includedir}/libspl/sys/dktp/*.h
%{_includedir}/libspl/sys/ia32/*.h
%{_includedir}/libzfs/*.h
%{_includedir}/libzfs/sys/*.h
%{_includedir}/libzfs/sys/crypto/*.h
%{_includedir}/libzfs/sys/fm/*.h
%{_includedir}/libzfs/sys/fm/fs/*.h
%{_includedir}/libzfs/sys/fs/*.h
%{_includedir}/libzfs/sys/lua/*.h
%{_includedir}/libzfs/sys/sysevent/*.h
%{_includedir}/libzfs/sys/zstd/*.h

%files -n %{name}-dracut
%defattr(-,root,root,-)
%license LICENSE
%dir %{_dracutdir}/modules.d/02zfsexpandknowledge
%{_dracutdir}/modules.d/02zfsexpandknowledge/module-setup.sh
%dir %{_dracutdir}/modules.d/90zfs
%{_dracutdir}/modules.d/90zfs/export-zfs.sh
%{_dracutdir}/modules.d/90zfs/import-opts-generator.sh
%{_dracutdir}/modules.d/90zfs/module-setup.sh
%{_dracutdir}/modules.d/90zfs/mount-zfs.sh
%{_dracutdir}/modules.d/90zfs/parse-zfs.sh
%{_dracutdir}/modules.d/90zfs/zfs-env-bootfs.service
%{_dracutdir}/modules.d/90zfs/zfs-generator.sh
%{_dracutdir}/modules.d/90zfs/zfs-lib.sh
%{_dracutdir}/modules.d/90zfs/zfs-load-key.sh
%{_dracutdir}/modules.d/90zfs/zfs-needshutdown.sh
%{_dracutdir}/modules.d/90zfs/zfs-nonroot-necessities.service
%{_dracutdir}/modules.d/90zfs/zfs-rollback-bootfs.service
%{_dracutdir}/modules.d/90zfs/zfs-snapshot-bootfs.service
%{_mandir}/man7/dracut.zfs.7*

%files -n %{name}-pam
%defattr(-,root,root,-)
%license LICENSE
%{_libdir}/security/pam_zfs_key.so
