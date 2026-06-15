%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/prometheus/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog

Name: blackbox-exporter
Version: 0.28.0
Release: 1%{?dist}
Summary: Prometheus Blackbox Exporter
License: ASL 2.0
URL: https://github.com/prometheus/blackbox_exporter
Source: https://github.com/prometheus/blackbox_exporter/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%{?systemd_requires}
Requires(pre): shadow-utils
BuildRequires: golang >= 1.26.0, golang < 1.27.0

%description
The blackbox exporter allows blackbox probing of endpoints over HTTP, HTTPS, DNS, TCP and ICMP.

%prep
%autosetup -n blackbox_exporter-%{version}

%build
cd %{_builddir}/blackbox_exporter-%{version}
export GOFLAGS=-buildvcs=false
go mod download
go build -o $(pwd)/blackbox-exporter

%install
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -d %{buildroot}%{_sysconfdir}/blackbox-exporter
%{__install} -d %{buildroot}%{_sysconfdir}/default
%{__install} -m 755 blackbox-exporter %{buildroot}%{_bindir}/blackbox-exporter
cat <<EOF > %{buildroot}%{_unitdir}/blackbox-exporter.service
[Unit]
Description=Prometheus blackbox Exporter
Documentation=%{url}

[Service]
User=prometheus
Group=prometheus
EnvironmentFile=%{_sysconfdir}/default/blackbox-exporter
ExecStart=%{_bindir}/blackbox-exporter \$ARGUMENTS
ExecReload=%{_bindir}/kill -HUP \$MAINPID
SendSIGKILL=no
LimitNOFILE=65535
OOMScoreAdjust=-1000
Restart=always
RestartSec=5s
StartLimitInterval=0
StartLimitBurst=0
AmbientCapabilities=CAP_NET_RAW

[Install]
WantedBy=multi-user.target
EOF
cat <<EOF > %{buildroot}%{_sysconfdir}/blackbox-exporter/blackbox-exporter.yml
---
EOF
cat <<EOF > %{buildroot}%{_sysconfdir}/default/blackbox-exporter
ARGUMENTS="--config.file=%{_sysconfdir}/blackbox-exporter/blackbox-exporter.yml"
EOF
%{__install} -d %{buildroot}%{_sysusersdir}
cat <<EOF > %{buildroot}%{_sysusersdir}/%{name}.conf
u prometheus - "Prometheus daemon" %{_sharedstatedir}/prometheus /sbin/nologin
EOF

%pre
%sysusers_create_compat %{_sysusersdir}/%{name}.conf

%post
%systemd_post blackbox-exporter.service

%preun
%systemd_preun blackbox-exporter.service

%postun
%systemd_postun blackbox-exporter.service

%files
%defattr(-,root,root,-)
%{_bindir}/blackbox-exporter
%{_unitdir}/blackbox-exporter.service
%dir %{_sysconfdir}/blackbox-exporter
%config(noreplace) %{_sysconfdir}/blackbox-exporter/blackbox-exporter.yml
%config(noreplace) %{_sysconfdir}/default/blackbox-exporter
%{_sysusersdir}/%{name}.conf
