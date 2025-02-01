%define debug_package %{nil}
%define _rpmdir %{_topdir}/RPMS/kubernetes

Name: helm
Version: 3.16.4
Release: 1%{?dist}
Summary: The package manager for Kubernetes
License: ASL 2.0
URL: https://helm.sh
Source: https://github.com/helm/helm/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires: golang >= 1.22.0, golang < 1.23.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Helm is a tool for managing Charts. Charts are packages of pre-configured Kubernetes resources.

%prep
%setup -q

%build
go install -C cmd/helm
go build -C cmd/helm -o $(pwd)/helm

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_bindir}
%{__install} -m 755 helm %{buildroot}%{_bindir}/helm

%files
%defattr(-,root,root,-)
%{_bindir}/helm
