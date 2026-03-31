%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/prometheus/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog

Name: rsyslog-exporter
Version: 1.1.0
Release: 1%{?dist}
Summary: Prometheus Rsyslog Exporter
License: ASL 2.0
URL: https://github.com/prometheus-community/rsyslog_exporter
Source: https://github.com/prometheus-community/rsyslog_exporter/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires: golang >= 1.25.0, golang < 1.26.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Prometheus exporter for rsyslog server metrics.

%prep
%autosetup -n rsyslog_exporter-%{version}

%build
cd %{_builddir}/rsyslog_exporter-%{version}
export GOFLAGS=-buildvcs=false
go mod download
go build -o %{name}

%install
%{__install} -d %{buildroot}%{_bindir}
%{__install} -m 755 rsyslog-exporter %{buildroot}%{_bindir}/rsyslog-exporter

%files
%defattr(-,root,root,-)
%{_bindir}/rsyslog-exporter
