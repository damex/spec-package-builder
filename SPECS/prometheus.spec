%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/prometheus/%{disttype}/%{distnum}

Name: prometheus
Version: 3.2.0
Release: 1%{?dist}
Summary: monitoring system and time series database
License: ASL 2.0
URL: https://prometheus.io
Source: https://github.com/prometheus/prometheus/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%{?systemd_requires}
Requires: prometheus-promtool
Requires(pre): shadow-utils
BuildRequires: golang >= 1.22.0, golang < 1.23.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%package -n prometheus-promtool
Summary: Tooling for the Prometheus monitoring system

%description
Prometheus, a Cloud Native Computing Foundation project, is a systems and service monitoring system.
It collects metrics from configured targets at given intervals, evaluates rule expressions, displays the results, and can trigger alerts if some condition is observed to be true.

%description -n prometheus-promtool
Tooling for the Prometheus monitoring system

%prep
%setup -q -n prometheus-%{version}

%build
cd %{_builddir}/prometheus-%{version}
go install -C cmd/prometheus
go build -C cmd/prometheus -o $(pwd)/prometheus
go install -C cmd/promtool
go build -C cmd/promtool -o $(pwd)/promtool

%install
%{__rm} -rf %{buildroot}
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
LimitNOFILE=65536
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

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin \
    -c "Prometheus daemon" prometheus
exit 0

%post
%systemd_post prometheus.service

%preun
%systemd_preun prometheus.service

%postun
%systemd_postun prometheus.service

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/prometheus
%config(noreplace) %{_sysconfdir}/prometheus/prometheus.yml
%{_unitdir}/prometheus.service
%config(noreplace) %{_sysconfdir}/default/prometheus
%dir %attr(755, prometheus, prometheus)%{_sharedstatedir}/prometheus

%files -n prometheus-promtool
%{_bindir}/promtool
