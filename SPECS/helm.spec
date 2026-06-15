%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/kubernetes/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog

Name: helm
Version: 3.20.1
Release: 1%{?dist}
Summary: The package manager for Kubernetes
License: ASL 2.0
URL: https://helm.sh
Source: https://github.com/helm/helm/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires: golang >= 1.26.0, golang < 1.27.0

%description
Helm is a tool for managing Charts. Charts are packages of pre-configured Kubernetes resources.

%prep
%autosetup

%build
export GOFLAGS=-buildvcs=false
go mod download
go build -C cmd/helm -o $(pwd)/helm

%install
%{__install} -d %{buildroot}%{_bindir}
%{__install} -m 755 helm %{buildroot}%{_bindir}/helm

%files
%defattr(-,root,root,-)
%{_bindir}/helm
