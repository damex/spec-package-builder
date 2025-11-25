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
BuildRequires: golang >= 1.25.0, golang < 1.26.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Kafka exporter for Prometheus.

%prep
%setup -q -n kafka_exporter-%{version}

%build
cd %{_builddir}/kafka_exporter-%{version}
export GOFLAGS=-buildvcs=false
go install
go build -o $(pwd)/kafka-exporter

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -d %{buildroot}%{_sysconfdir}/default
%{__install} -m 755 kafka-exporter %{buildroot}%{_bindir}/kafka-exporter
cat <<EOF > %{buildroot}%{_unitdir}/kafka-exporter.service
[Unit]
Description=Prometheus Kafka Exporter
Documentation=%{url}

[Service]
Restart=always
User=prometheus
Group=prometheus
EnvironmentFile=%{_sysconfdir}/default/kafka-exporter
ExecStart=%{_bindir}/kafka-exporter \$ARGUMENTS
ExecReload=%{_bindir}/kill -HUP \$MAINPID
SendSIGKILL=no
LimitNOFILE=65536
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

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin \
    -c "Prometheus daemon" prometheus

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
