%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/prometheus/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog

Name: memcached-exporter
Version: 0.15.5
Release: 1%{?dist}
Summary: Prometheus Memcached Metrics Exporter
License: ASL 2.0
URL: https://github.com/prometheus/memcached_exporter
Source: https://github.com/prometheus/memcached_exporter/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%{?systemd_requires}
Requires(pre): shadow-utils
BuildRequires: golang >= 1.25.0, golang < 1.26.0

%description
Prometheus exporter for Memcached server metrics.

%prep
%autosetup -n memcached_exporter-%{version}

%build
cd %{_builddir}/memcached_exporter-%{version}
export GOFLAGS=-buildvcs=false
go mod download
go build -C cmd/memcached_exporter -o $(pwd)/memcached-exporter

%install
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -d %{buildroot}%{_sysconfdir}/default
%{__install} -m 755 memcached-exporter %{buildroot}%{_bindir}/memcached-exporter
cat <<EOF > %{buildroot}%{_unitdir}/memcached-exporter.service
[Unit]
Description=Prometheus Memcached Metrics Exporter
Documentation=%{url}

[Service]
User=prometheus
Group=prometheus
EnvironmentFile=%{_sysconfdir}/default/memcached-exporter
ExecStart=%{_bindir}/memcached-exporter \$ARGUMENTS
ExecReload=%{_bindir}/kill -HUP \$MAINPID
SendSIGKILL=no
LimitNOFILE=65535
OOMScoreAdjust=-1000
Restart=always
RestartSec=5s
StartLimitInterval=0
StartLimitBurst=0

[Install]
WantedBy=multi-user.target
EOF
cat <<EOF > %{buildroot}%{_sysconfdir}/default/memcached-exporter
ARGUMENTS=""
EOF
%{__install} -d %{buildroot}%{_sysusersdir}
cat <<EOF > %{buildroot}%{_sysusersdir}/%{name}.conf
u prometheus - "Prometheus daemon" %{_sharedstatedir}/prometheus /sbin/nologin
EOF

%pre
%sysusers_create_compat %{_sysusersdir}/%{name}.conf

%post
%systemd_post memcached-exporter.service

%preun
%systemd_preun memcached-exporter.service

%postun
%systemd_postun memcached-exporter.service

%files
%defattr(-,root,root,-)
%{_bindir}/memcached-exporter
%{_unitdir}/memcached-exporter.service
%config(noreplace) %{_sysconfdir}/default/memcached-exporter
%{_sysusersdir}/%{name}.conf
