%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/prometheus/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog

Name: prometheus
Version: %{prometheus_version}
Release: 1%{?dist}
Summary: monitoring system and time series database
License: ASL 2.0
URL: https://prometheus.io
Source0: https://github.com/prometheus/prometheus/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1: https://github.com/prometheus/prometheus/releases/download/v%{version}/prometheus-web-ui-%{version}.tar.gz
%{?systemd_requires}
Requires: prometheus-promtool
Requires(pre): shadow-utils
BuildRequires: golang >= 1.26.0, golang < 1.27.0

%package -n prometheus-promtool
Summary: Tooling for the Prometheus monitoring system

%description
Prometheus, a Cloud Native Computing Foundation project, is a systems and service monitoring system.
It collects metrics from configured targets at given intervals, evaluates rule expressions, displays the results, and can trigger alerts if some condition is observed to be true.

%description -n prometheus-promtool
Tooling for the Prometheus monitoring system

%prep
%autosetup -a 1

%build
export GOFLAGS=-buildvcs=false
make build PREBUILT_ASSETS_STATIC_DIR=$(pwd)/static

%install
%{__install} -d %{buildroot}%{_sharedstatedir}/prometheus
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_sysconfdir}/default
%{__install} -d %{buildroot}%{_sysconfdir}/prometheus
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 755 prometheus %{buildroot}%{_bindir}/prometheus
%{__install} -m 755 promtool %{buildroot}%{_bindir}/promtool
%{__install} -m 644 documentation/examples/prometheus.yml %{buildroot}%{_sysconfdir}/prometheus/prometheus.yml
cat <<EOF > %{buildroot}%{_unitdir}/prometheus.service
[Unit]
Description=Monitoring system and time series database
Documentation=https://prometheus.io/docs/introduction/overview

[Service]
User=prometheus
Group=prometheus
EnvironmentFile=%{_sysconfdir}/default/prometheus
ExecStart=%{_bindir}/prometheus \$ARGUMENTS
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
cat <<EOF > %{buildroot}%{_sysconfdir}/default/prometheus
ARGUMENTS="--config.file=%{_sysconfdir}/prometheus/prometheus.yml --storage.tsdb.path=%{_sharedstatedir}/prometheus/data"
EOF
%{__install} -d %{buildroot}%{_sysusersdir}
cat <<EOF > %{buildroot}%{_sysusersdir}/%{name}.conf
u prometheus - "Prometheus daemon" %{_sharedstatedir}/prometheus /sbin/nologin
EOF

%pre
%sysusers_create_compat %{_sysusersdir}/%{name}.conf

%post
%systemd_post prometheus.service

%preun
%systemd_preun prometheus.service

%postun
%systemd_postun prometheus.service

%files
%defattr(-,root,root,-)
%{_bindir}/prometheus
%dir %{_sysconfdir}/prometheus
%config(noreplace) %{_sysconfdir}/prometheus/prometheus.yml
%{_unitdir}/prometheus.service
%config(noreplace) %{_sysconfdir}/default/prometheus
%{_sysusersdir}/%{name}.conf
%dir %attr(755, prometheus, prometheus)%{_sharedstatedir}/prometheus

%files -n prometheus-promtool
%defattr(-,root,root,-)
%{_bindir}/promtool
