%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/prometheus/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog

Name: kafka-exporter
Version: 1.9.0
Release: 1%{?dist}
Summary: Prometheus Kafka Exporter
License: ASL 2.0
URL: https://github.com/danielqsj/kafka_exporter
Source: https://github.com/danielqsj/kafka_exporter/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%{?systemd_requires}
Requires(pre): shadow-utils
BuildRequires: golang >= 1.25.0, golang < 1.26.0

%description
Kafka exporter for Prometheus.

%prep
%autosetup -n kafka_exporter-%{version}

%build
cd %{_builddir}/kafka_exporter-%{version}
export GOFLAGS=-buildvcs=false
go mod download
go build -o $(pwd)/kafka-exporter

%install
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -d %{buildroot}%{_sysconfdir}/default
%{__install} -m 755 kafka-exporter %{buildroot}%{_bindir}/kafka-exporter
cat <<EOF > %{buildroot}%{_unitdir}/kafka-exporter.service
[Unit]
Description=Prometheus Kafka Exporter
Documentation=%{url}

[Service]
User=prometheus
Group=prometheus
EnvironmentFile=%{_sysconfdir}/default/kafka-exporter
ExecStart=%{_bindir}/kafka-exporter \$ARGUMENTS
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
cat <<EOF > %{buildroot}%{_sysconfdir}/default/kafka-exporter
ARGUMENTS=""
EOF
%{__install} -d %{buildroot}%{_sysusersdir}
cat <<EOF > %{buildroot}%{_sysusersdir}/%{name}.conf
u prometheus - "Prometheus daemon" %{_sharedstatedir}/prometheus /sbin/nologin
EOF

%pre
%sysusers_create_compat %{_sysusersdir}/%{name}.conf

%post
%systemd_post kafka-exporter.service

%preun
%systemd_preun kafka-exporter.service

%postun
%systemd_postun kafka-exporter.service

%files
%defattr(-,root,root,-)
%{_bindir}/kafka-exporter
%{_unitdir}/kafka-exporter.service
%config(noreplace) %{_sysconfdir}/default/kafka-exporter
%{_sysusersdir}/%{name}.conf
