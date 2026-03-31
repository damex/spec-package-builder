%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/prometheus/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog

Name: postgresql-exporter
Version: 0.19.1
Release: 1%{?dist}
Summary: Prometheus PostgreSQL Metrics Exporter
License: ASL 2.0
URL: https://github.com/prometheus-community/postgres_exporter
Source: https://github.com/prometheus-community/postgres_exporter/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%{?systemd_requires}
Requires(pre): shadow-utils
BuildRequires: golang >= 1.25.0, golang < 1.26.0

%description
Prometheus exporter for PostgreSQL server metrics.

%prep
%autosetup -n postgres_exporter-%{version}

%build
cd %{_builddir}/postgres_exporter-%{version}
export GOFLAGS=-buildvcs=false
go mod download
go build -C cmd/postgres_exporter -o $(pwd)/postgresql-exporter

%install
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -d %{buildroot}%{_sysconfdir}/default
%{__install} -d %{buildroot}%{_sharedstatedir}/prometheus
%{__install} -m 755 postgresql-exporter %{buildroot}%{_bindir}/postgresql-exporter
cat <<EOF > %{buildroot}%{_unitdir}/postgresql-exporter.service
[Unit]
Description=Prometheus PostgreSQL Metrics Exporter
Documentation=%{url}

[Service]
User=prometheus
Group=prometheus
EnvironmentFile=%{_sysconfdir}/default/postgresql-exporter
ExecStart=%{_bindir}/postgresql-exporter \$ARGUMENTS
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
cat <<EOF > %{buildroot}%{_sysconfdir}/default/postgresql-exporter
DATA_SOURCE_NAME="user=postgres host=/var/run/postgresql sslmode=disable"
ARGUMENTS="--extend.query-path=%{_sharedstatedir}/prometheus/postgresql-exporter-queries.yml"
EOF
cat <<EOF > %{buildroot}%{_sharedstatedir}/prometheus/postgresql-exporter-queries.yml
---
EOF

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin \
    -c "Prometheus daemon" prometheus
exit 0

%post
%systemd_post postgresql-exporter.service

%preun
%systemd_preun postgresql-exporter.service

%postun
%systemd_postun postgresql-exporter.service

%files
%defattr(-,root,root,-)
%{_bindir}/postgresql-exporter
%{_unitdir}/postgresql-exporter.service
%config(noreplace) %{_sysconfdir}/default/postgresql-exporter
%config(noreplace) %{_sharedstatedir}/prometheus/postgresql-exporter-queries.yml
%dir %attr(755, prometheus, prometheus)%{_sharedstatedir}/prometheus
