%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/prometheus/%{disttype}/%{distnum}

Name: systemd-exporter
Version: 0.6.0
Release: 1%{?dist}
Summary: prometheus systemd exporter
License: ASL 2.0
URL: https://github.com/prometheus-community/systemd_exporter
Source: https://github.com/prometheus-community/systemd_exporter/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%{?systemd_requires}
BuildRequires: golang >= 1.22.0, golang < 1.23.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Prometheus exporter for systemd units, written in Go.

%prep
%setup -q -n systemd_exporter-%{version}

%build
cd %{_builddir}/systemd_exporter-%{version}
go install
go build -o $(pwd)/systemd-exporter

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -d %{buildroot}%{_sysconfdir}/default
%{__install} -m 755 systemd-exporter %{buildroot}%{_bindir}/systemd-exporter
cat <<EOF > %{buildroot}%{_unitdir}/systemd-exporter.service
[Unit]
Description=prometheus systemd exporter
Documentation=%{url}

[Service]
User=root
Group=root
EnvironmentFile=%{_sysconfdir}/default/systemd-exporter
ExecStart=%{_bindir}/systemd-exporter \$ARGUMENTS
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
cat <<EOF > %{buildroot}%{_sysconfdir}/default/systemd-exporter
ARGUMENTS=""
EOF

%post
%systemd_post systemd-exporter.service

%preun
%systemd_preun systemd-exporter.service

%postun
%systemd_postun systemd-exporter.service

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/systemd-exporter
%{_unitdir}/systemd-exporter.service
%config(noreplace) %{_sysconfdir}/default/systemd-exporter
