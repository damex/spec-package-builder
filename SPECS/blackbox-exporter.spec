%define debug_package %{nil}

Name: blackbox-exporter
Version: 0.25.0
Release: 1%{?dist}
Summary: Prometheus Blackbox Exporter
License: ASL 2.0
URL: https://github.com/prometheus/blackbox_exporter
Source: https://github.com/prometheus/blackbox_exporter/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%{?systemd_requires}
BuildRequires: golang >= 1.22.0, golang < 1.23.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The blackbox exporter allows blackbox probing of endpoints over HTTP, HTTPS, DNS, TCP and ICMP.

%prep
%setup -q -n blackbox_exporter-%{version}

%build
cd %{_builddir}/blackbox_exporter-%{version}
go install
go build -o $(pwd)/blackbox-exporter

%install
%{__rm} -rf %{buildroot}
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
User=root
Group=root
EnvironmentFile=%{_sysconfdir}/default/blackbox-exporter
ExecStart=%{_bindir}/blackbox-exporter \$ARGUMENTS
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
cat <<EOF > %{buildroot}%{_sysconfdir}/blackbox-exporter/blackbox-exporter.yml
---
EOF
cat <<EOF > %{buildroot}%{_sysconfdir}/default/blackbox-exporter
ARGS="--config.file=%{_sysconfdir}/blackbox-exporter/blackbox-exporter.yml"
EOF

%post
%systemd_post blackbox-exporter.service

%preun
%systemd_preun blackbox-exporter.service

%postun
%systemd_postun blackbox-exporter.service

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/blackbox-exporter
%{_unitdir}/blackbox-exporter.service
%config(noreplace) %{_sysconfdir}/blackbox-exporter/blackbox-exporter.yml
%config(noreplace) %{_sysconfdir}/default/blackbox-exporter
