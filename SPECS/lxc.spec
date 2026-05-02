%define debug_package %{nil}
%global _build_id_links none
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/incus/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog

Name: lxc
Version: 7.0.0
Release: 2%{?dist}
Summary: Linux Resource Containers
License: LGPLv2.1+
URL: https://linuxcontainers.org/lxc
Source: https://linuxcontainers.org/downloads/%{name}/%{name}-%{version}.tar.gz
BuildRequires: gcc-c++
BuildRequires: dbus-devel
BuildRequires: libcap-devel
BuildRequires: libseccomp-devel
BuildRequires: libselinux-devel
BuildRequires: liburing-devel
BuildRequires: meson
BuildRequires: openssl-devel
BuildRequires: pam-devel
BuildRequires: systemd-devel
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-templates%{?_isa} = %{version}-%{release}

%package -n %{name}-libs
Summary: runtime library files for LXC
Requires: rsync
%{?systemd_requires}

%package -n %{name}-devel
Summary: development files for LXC
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%package -n %{name}-templates
Summary: templates for %{name}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

%description -n %{name}-libs
Runtime library files for LXC, providing process and resource isolation
without the overhead of full virtualization.

%description -n %{name}-devel
Development headers and pkg-config files for building against liblxc.

%description -n %{name}-templates
Templates for creating LXC containers.

%prep
%autosetup

%build
%meson \
        -D apparmor=false \
        -D capabilities=true \
        -D commands=true \
        -D dbus=true \
        -D distrosysconfdir=sysconfig \
        -D examples=false \
        -D init-script=systemd \
        -D io-uring-event-loop=true \
        -D man=false \
        -D memfd-rexec=true \
        -D openssl=true \
        -D pam-cgroup=true \
        -D runtime-path=%{_rundir} \
        -D seccomp=true \
        -D selinux=true \
        -D systemd-unitdir=%{_unitdir} \
        -D tests=false \
        -D thread-safety=true \
        -D tools=true \
        %{nil}
%meson_build

%install
%meson_install
%{__rm} %{buildroot}%{_libdir}/liblxc.a
%{__rm} %{buildroot}%{_libexecdir}/%{name}/%{name}-apparmor-load
%{__rm} %{buildroot}%{_datadir}/%{name}/%{name}-patch.py

%post -n %{name}-libs
%systemd_post %{name}-net.service
%systemd_post %{name}.service
%systemd_post %{name}-monitord.service

%preun -n %{name}-libs
%systemd_preun %{name}-net.service
%systemd_preun %{name}.service
%systemd_preun %{name}-monitord.service

%postun -n %{name}-libs
%systemd_postun %{name}-net.service
%systemd_postun %{name}.service
%systemd_postun %{name}-monitord.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}-attach
%{_bindir}/%{name}-autostart
%{_bindir}/%{name}-cgroup
%{_bindir}/%{name}-checkconfig
%{_bindir}/%{name}-checkpoint
%{_bindir}/%{name}-config
%{_bindir}/%{name}-console
%{_bindir}/%{name}-copy
%{_bindir}/%{name}-create
%{_bindir}/%{name}-destroy
%{_bindir}/%{name}-device
%{_bindir}/%{name}-execute
%{_bindir}/%{name}-freeze
%{_bindir}/%{name}-info
%{_bindir}/%{name}-ls
%{_bindir}/%{name}-monitor
%{_bindir}/%{name}-snapshot
%{_bindir}/%{name}-start
%{_bindir}/%{name}-stop
%{_bindir}/%{name}-top
%{_bindir}/%{name}-unfreeze
%{_bindir}/%{name}-unshare
%{_bindir}/%{name}-update-config
%{_bindir}/%{name}-usernsexec
%{_bindir}/%{name}-wait
%{_datadir}/bash-completion/completions/_%{name}
%{_datadir}/bash-completion/completions/%{name}-attach
%{_datadir}/bash-completion/completions/%{name}-autostart
%{_datadir}/bash-completion/completions/%{name}-cgroup
%{_datadir}/bash-completion/completions/%{name}-checkpoint
%{_datadir}/bash-completion/completions/%{name}-config
%{_datadir}/bash-completion/completions/%{name}-console
%{_datadir}/bash-completion/completions/%{name}-copy
%{_datadir}/bash-completion/completions/%{name}-create
%{_datadir}/bash-completion/completions/%{name}-destroy
%{_datadir}/bash-completion/completions/%{name}-device
%{_datadir}/bash-completion/completions/%{name}-execute
%{_datadir}/bash-completion/completions/%{name}-freeze
%{_datadir}/bash-completion/completions/%{name}-info
%{_datadir}/bash-completion/completions/%{name}-ls
%{_datadir}/bash-completion/completions/%{name}-monitor
%{_datadir}/bash-completion/completions/%{name}-snapshot
%{_datadir}/bash-completion/completions/%{name}-start
%{_datadir}/bash-completion/completions/%{name}-stop
%{_datadir}/bash-completion/completions/%{name}-top
%{_datadir}/bash-completion/completions/%{name}-unfreeze
%{_datadir}/bash-completion/completions/%{name}-unshare
%{_datadir}/bash-completion/completions/%{name}-usernsexec
%{_datadir}/bash-completion/completions/%{name}-wait
%{_datadir}/%{name}/%{name}.functions

%files -n %{name}-libs
%defattr(-,root,root,-)
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/default.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sbindir}/init.%{name}
%{_libdir}/liblxc.so.1
%{_libdir}/liblxc.so.1.9.0
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/rootfs
%{_libdir}/%{name}/rootfs/README
%{_libdir}/security/pam_cgfs.so
%dir %{_libexecdir}/%{name}
%dir %{_libexecdir}/%{name}/hooks
%{_libexecdir}/%{name}/hooks/unmount-namespace
%{_libexecdir}/%{name}/%{name}-containers
%{_libexecdir}/%{name}/%{name}-monitord
%{_libexecdir}/%{name}/%{name}-net
%{_libexecdir}/%{name}/%{name}-user-nic
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}@.service
%{_unitdir}/%{name}-net.service
%{_unitdir}/%{name}-monitord.service
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/config
%dir %{_datadir}/%{name}/hooks
%{_datadir}/%{name}/hooks/clonehostname
%{_datadir}/%{name}/hooks/dhclient
%{_datadir}/%{name}/hooks/dhclient-script
%{_datadir}/%{name}/hooks/mountecryptfsroot
%{_datadir}/%{name}/hooks/nvidia
%{_datadir}/%{name}/hooks/squid-deb-proxy-client
%{_datadir}/%{name}/hooks/ubuntu-cloud-prep
%dir %{_datadir}/%{name}/selinux
%{_datadir}/%{name}/selinux/%{name}.if
%{_datadir}/%{name}/selinux/%{name}.te
%license COPYING
%dir %{_sharedstatedir}/%{name}
%dir %{_localstatedir}/cache/%{name}

%files -n %{name}-devel
%defattr(-,root,root,-)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/attach_options.h
%{_includedir}/%{name}/lxccontainer.h
%{_includedir}/%{name}/version.h
%{_libdir}/liblxc.so
%{_libdir}/pkgconfig/%{name}.pc

%files -n %{name}-templates
%defattr(-,root,root,-)
%dir %{_datadir}/%{name}/templates
%{_datadir}/%{name}/templates/%{name}-busybox
%{_datadir}/%{name}/templates/%{name}-download
%{_datadir}/%{name}/templates/%{name}-local
%{_datadir}/%{name}/templates/%{name}-oci
%dir %{_datadir}/%{name}/config/common.conf.d
%{_datadir}/%{name}/config/common.conf
%{_datadir}/%{name}/config/common.conf.d/README
%{_datadir}/%{name}/config/common.seccomp
%{_datadir}/%{name}/config/nesting.conf
%{_datadir}/%{name}/config/oci.common.conf
%{_datadir}/%{name}/config/userns.conf
