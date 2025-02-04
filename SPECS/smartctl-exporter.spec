%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/prometheus/%{disttype}/%{distnum}

Name: smartctl-exporter
Version: 0.13.0
Release: 1%{?dist}
Summary: prometheus smartctl exporter
License: ASL 2.0
URL: https://github.com/prometheus-community/smartctl_exporter
Source: https://github.com/prometheus-community/smartctl_exporter/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%{?systemd_requires}
Requires: smartmontools >= 1:7.0
BuildRequires: golang >= 1.22.0, golang < 1.23.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Export smartctl statistics to prometheus

%prep
%setup -q -n smartctl_exporter-%{version}

%build
cd %{_builddir}/smartctl_exporter-%{version}
go install
go build -o $(pwd)/smartctl-exporter

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -d %{buildroot}%{_sysconfdir}/default
%{__install} -m 755 smartctl-exporter %{buildroot}%{_bindir}/smartctl-exporter
cat <<EOF > %{buildroot}%{_unitdir}/smartctl-exporter.service
[Unit]
Description=prometheus smartctl exporter
Documentation=%{url}

[Service]
User=root
Group=root
EnvironmentFile=%{_sysconfdir}/default/smartctl-exporter
ExecStart=%{_bindir}/smartctl-exporter \$ARGUMENTS
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
cat <<EOF > %{buildroot}%{_sysconfdir}/default/smartctl-exporter
ARGUMENTS=""
EOF

%post
%systemd_post smartctl-exporter.service

%preun
%systemd_preun smartctl-exporter.service

%postun
%systemd_postun smartctl-exporter.service

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/smartctl-exporter
%{_unitdir}/smartctl-exporter.service
%config(noreplace) %{_sysconfdir}/default/smartctl-exporter
