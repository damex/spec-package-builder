%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/kubernetes/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog

Name: flannel
Version: 0.28.1
Release: 1%{?dist}
Summary: simple and easy way to configure a layer 3 network fabric designed for Kubernetes
License: ASL 2.0
URL: https://github.com/flannel-io/flannel
Source: https://github.com/flannel-io/flannel/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires: golang >= 1.25.0, golang < 1.26.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Flannel is a simple and easy way to configure a layer 3 network fabric designed for Kubernetes.

%prep
%setup -q

%build
export GOFLAGS=-buildvcs=false
go mod download
go build -o $(pwd)/flanneld

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_bindir}
%{__install} -m 755 flanneld %{buildroot}%{_bindir}/flanneld

%files
%defattr(-,root,root,-)
%{_bindir}/flanneld
