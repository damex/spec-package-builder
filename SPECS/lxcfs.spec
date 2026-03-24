%define debug_package %{nil}
%global _build_id_links none
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/incus/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog

Name: lxcfs
Version: 6.0.6
Release: 1%{?dist}
Summary: FUSE filesystem for containers
License: LGPL-2.1-or-later
URL: https://linuxcontainers.org/lxcfs
Source: https://linuxcontainers.org/downloads/%{name}/%{name}-%{version}.tar.gz
BuildRequires: gcc
BuildRequires: fuse3-devel
BuildRequires: meson
BuildRequires: python3-jinja2
Requires: fuse3
%{?systemd_requires}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
LXCFS is a small FUSE filesystem that makes Linux containers feel more
like a virtual machine by providing container-aware /proc and /sys values.

%prep
%autosetup

%build
%meson \
        -D docs=false \
        -D init-script=systemd \
        -D runtime-path=%{_rundir} \
        -D tests=false \
        %{nil}
%meson_build

%install
%meson_install
%{__install} -d %{buildroot}%{_sharedstatedir}/%{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/%{name}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/lib%{name}.so
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/lxc.mount.hook
%{_datadir}/%{name}/lxc.reboot.hook
%{_unitdir}/%{name}.service
%dir %{_datadir}/lxc
%dir %{_datadir}/lxc/config
%dir %{_datadir}/lxc/config/common.conf.d
%{_datadir}/lxc/config/common.conf.d/00-lxcfs.conf
%dir %{_sharedstatedir}/%{name}
