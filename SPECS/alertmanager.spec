%define debug_package %{nil}
%define _rpmdir %{_topdir}/RPMS/prometheus

Name: alertmanager
Version: 0.28.0
Release: 1%{?dist}
Summary: The Alertmanager handles alerts sent by client applications such as the Prometheus server.
License: ASL 2.0
URL: https://prometheus.io
Source: https://github.com/prometheus/alertmanager/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%{?systemd_requires}
Requires(pre): shadow-utils
Requires: alertmanager-amtool
BuildRequires: golang >= 1.22.0, golang < 1.23.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%package -n alertmanager-amtool
Summary: Tooling for the Alertmanager

%description
The Alertmanager handles alerts sent by client applications such as the Prometheus server.
It takes care of deduplicating, grouping, and routing them to the correct receiver integrations such as email,
PagerDuty, or OpsGenie. It also takes care of silencing and inhibition of alerts.

%description -n alertmanager-amtool
Tooling for the Alertmanager

%prep
%setup -q -n alertmanager-%{version}

%build
cd %{_builddir}/alertmanager-%{version}
go install -C cmd/alertmanager
go build -C cmd/alertmanager -o $(pwd)/alertmanager
go install -C cmd/amtool
go build -C cmd/amtool -o $(pwd)/amtool

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_sharedstatedir}/alertmanager
%{__install} -d %{buildroot}%{_sysconfdir}/default
%{__install} -d %{buildroot}%{_sysconfdir}/alertmanager
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 755 alertmanager %{buildroot}%{_bindir}/alertmanager
%{__install} -m 755 amtool %{buildroot}%{_bindir}/amtool
%{__install} -m 644 examples/ha/alertmanager.yml %{buildroot}%{_sysconfdir}/alertmanager/alertmanager.yml
cat <<EOF > %{buildroot}%{_unitdir}/alertmanager.service
[Unit]
Description=Alertmanager handles alerts sent by client applications such as the Prometheus server.
Documentation=https://prometheus.io/docs/alerting/latest/alertmanager/

[Service]
User=prometheus
Group=prometheus
EnvironmentFile=%{_sysconfdir}/default/alertmanager
ExecStart=%{_bindir}/alertmanager \$ARGUMENTS
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
cat <<EOF > %{buildroot}%{_sysconfdir}/default/alertmanager
ARGUMENTS="--config.file=%{_sysconfdir}/alertmanager/alertmanager.yml --storage.path=%{_sharedstatedir}/alertmanager"
EOF

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin \
    -c "Prometheus daemon" prometheus
exit 0

%post
%systemd_post alertmanager.service

%preun
%systemd_preun alertmanager.service

%postun
%systemd_postun alertmanager.service

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/alertmanager
%config(noreplace) %{_sysconfdir}/alertmanager/alertmanager.yml
%{_unitdir}/alertmanager.service
%config(noreplace) %{_sysconfdir}/default/alertmanager
%dir %attr(755, prometheus, prometheus)%{_sharedstatedir}/alertmanager

%files -n alertmanager-amtool
%{_bindir}/amtool
