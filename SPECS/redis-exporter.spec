%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/prometheus/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog

Name: redis-exporter
Version: 1.82.0
Release: 1%{?dist}
Summary: Prometheus Valkey & Redis Metrics Exporter
License: MIT
URL: https://github.com/oliver006/redis_exporter
Source: https://github.com/oliver006/redis_exporter/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%{?systemd_requires}
Requires(pre): shadow-utils
BuildRequires: golang >= 1.26.0, golang < 1.27.0

%description
Prometheus exporter for Valkey metrics (Redis-compatible).
Supports Valkey and Redis 2.x, 3.x, 4.x, 5.x, 6.x, and 7.x

%prep
%autosetup -n redis_exporter-%{version}

%build
cd %{_builddir}/redis_exporter-%{version}
export GOFLAGS=-buildvcs=false
go mod download
go build -o $(pwd)/redis-exporter

%install
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -d %{buildroot}%{_sysconfdir}/default
%{__install} -m 755 redis-exporter %{buildroot}%{_bindir}/redis-exporter
cat <<EOF > %{buildroot}%{_unitdir}/redis-exporter.service
[Unit]
Description=Prometheus Valkey & Redis Metrics Exporter
Documentation=%{url}

[Service]
User=prometheus
Group=prometheus
EnvironmentFile=%{_sysconfdir}/default/redis-exporter
ExecStart=%{_bindir}/redis-exporter \$ARGUMENTS
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
cat <<EOF > %{buildroot}%{_sysconfdir}/default/redis-exporter
ARGUMENTS=""
EOF
%{__install} -d %{buildroot}%{_sysusersdir}
cat <<EOF > %{buildroot}%{_sysusersdir}/%{name}.conf
u prometheus - "Prometheus daemon" %{_sharedstatedir}/prometheus /sbin/nologin
EOF

%pre
%sysusers_create_compat %{_sysusersdir}/%{name}.conf

%post
%systemd_post redis-exporter.service

%preun
%systemd_preun redis-exporter.service

%postun
%systemd_postun redis-exporter.service

%files
%defattr(-,root,root,-)
%{_bindir}/redis-exporter
%{_unitdir}/redis-exporter.service
%config(noreplace) %{_sysconfdir}/default/redis-exporter
%{_sysusersdir}/%{name}.conf
