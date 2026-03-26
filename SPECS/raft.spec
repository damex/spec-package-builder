%define debug_package %{nil}
%global _build_id_links none
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/incus/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog

Name: raft
Version: 0.22.1
Release: 1%{?dist}
Summary: C implementation of the Raft consensus protocol
License: LGPL-3.0-only WITH LGPL-3.0-linking-exception
URL: https://github.com/cowsql/raft
Source: %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: libtool
BuildRequires: libuv-devel
BuildRequires: lz4-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%package -n %{name}-devel
Summary: Development files for raft
Requires: %{name}%{?_isa} = %{version}-%{release}

%description
Fully asynchronous C implementation of the Raft consensus protocol. It consists
of a core part that implements the core Raft algorithm logic and a pluggable
interface defining the I/O implementation for networking and disk persistence.

%description -n %{name}-devel
Development headers and library for raft.

%prep
%autosetup
autoreconf -i

%build
%configure --disable-static
%make_build

%install
%make_install
%{__rm} %{buildroot}%{_libdir}/libraft.la

%ldconfig_scriptlets

%files
%defattr(-,root,root,-)
%license LICENSE
%{_libdir}/libraft.so.0
%{_libdir}/libraft.so.0.0.0

%files -n %{name}-devel
%defattr(-,root,root,-)
%{_includedir}/raft.h
%dir %{_includedir}/raft
%{_includedir}/raft/fixture.h
%{_includedir}/raft/uv.h
%{_libdir}/libraft.so
%{_libdir}/pkgconfig/%{name}.pc
