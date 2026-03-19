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
BuildRequires: golang >= 1.25.0, golang < 1.26.0
BuildRequires: nodejs
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Alert dashboard for Prometheus Alertmanager.

%prep
%setup -q

%build
export GOFLAGS=-buildvcs=false
make

%install
%{__rm} -rf %{buildroot}
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

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin \
    -c "Prometheus daemon" prometheus
exit 0

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
