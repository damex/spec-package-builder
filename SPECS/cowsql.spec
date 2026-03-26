%define debug_package %{nil}
%global _build_id_links none
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/incus/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog

Name: cowsql
Version: 1.15.9
Release: 1%{?dist}
Summary: Embeddable, replicated and fault tolerant SQL engine
License: LGPL-3.0-only WITH LGPL-3.0-linking-exception
URL: https://github.com/cowsql/cowsql
Source: %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: libtool
BuildRequires: libuv-devel
BuildRequires: raft-devel
BuildRequires: sqlite-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%package -n %{name}-devel
Summary: Development files for cowsql
Requires: %{name}%{?_isa} = %{version}-%{release}

%description
cowsql is a C library that implements an embeddable and replicated SQL database
engine with high availability and automatic failover.

%description -n %{name}-devel
Development headers and library for cowsql.

%prep
%autosetup
autoreconf -i

%build
%configure --disable-static
%make_build

%install
%make_install
%{__rm} %{buildroot}%{_libdir}/libcowsql.la

%ldconfig_scriptlets

%files
%defattr(-,root,root,-)
%license LICENSE
%{_libdir}/libcowsql.so.0
%{_libdir}/libcowsql.so.0.0.1

%files -n %{name}-devel
%defattr(-,root,root,-)
%{_includedir}/cowsql.h
%{_libdir}/libcowsql.so
%{_libdir}/pkgconfig/%{name}.pc
