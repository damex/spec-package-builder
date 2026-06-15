%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/prometheus/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog

Name: karma
Version: 0.126
Release: 1%{?dist}
Summary: Alert dashboard for Prometheus Alertmanager
License: ASL 2.0
URL: https://karma-dashboard.io
Source: https://github.com/prymitive/karma/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%{?systemd_requires}
Requires(pre): shadow-utils
BuildRequires: golang >= 1.26.0, golang < 1.27.0
BuildRequires: nodejs
BuildRequires: %{?el9:npm}%{!?el9:nodejs-npm}

%description
Alert dashboard for Prometheus Alertmanager.

%prep
%autosetup

%build
export GOFLAGS=-buildvcs=false
make

%install
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_sysconfdir}/default
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 755 karma %{buildroot}%{_bindir}/karma
cat <<EOF > %{buildroot}%{_unitdir}/karma.service
[Unit]
Description=%{summary}
Documentation=%{url}

[Service]
User=prometheus
Group=prometheus
EnvironmentFile=%{_sysconfdir}/default/karma
ExecStart=%{_bindir}/karma \$ARGUMENTS
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
cat <<EOF > %{buildroot}%{_sysconfdir}/default/karma
ARGUMENTS=""
EOF
%{__install} -d %{buildroot}%{_sysusersdir}
cat <<EOF > %{buildroot}%{_sysusersdir}/%{name}.conf
u prometheus - "Prometheus daemon" %{_sharedstatedir}/prometheus /sbin/nologin
EOF

%pre
%sysusers_create_compat %{_sysusersdir}/%{name}.conf

%post
%systemd_post karma.service

%preun
%systemd_preun karma.service

%postun
%systemd_postun karma.service

%files
%defattr(-,root,root,-)
%{_bindir}/karma
%{_unitdir}/karma.service
%config(noreplace) %{_sysconfdir}/default/karma
%{_sysusersdir}/%{name}.conf
