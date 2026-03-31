%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/prometheus/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog

Name: unbound-exporter
Version: 0.5.0
Release: 1%{?dist}
Summary: Prometheus Unbound Exporter
License: ASL 2.0
URL: https://github.com/letsencrypt/unbound_exporter
Source: https://github.com/letsencrypt/unbound_exporter/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%{?systemd_requires}
Requires(pre): shadow-utils
BuildRequires: golang >= 1.25.0, golang < 1.26.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Prometheus exporter for Unbound metrics, written in Go with pluggable metric collectors. The metrics exporter converts Unbound metric names to Prometheus metric names and labels by using a set of regular expressions.

%prep
%autosetup -n unbound_exporter-%{version}

%build
cd %{_builddir}/unbound_exporter-%{version}
export GOFLAGS=-buildvcs=false
go mod download
go build -o $(pwd)/unbound-exporter

%install
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -d %{buildroot}%{_sysconfdir}/default
%{__install} -m 755 unbound-exporter %{buildroot}%{_bindir}/unbound-exporter
cat <<EOF > %{buildroot}%{_unitdir}/unbound-exporter.service
[Unit]
Description=Prometheus Unbound Exporter
Documentation=%{url}

[Service]
User=prometheus
Group=prometheus
EnvironmentFile=%{_sysconfdir}/default/unbound-exporter
ExecStart=%{_bindir}/unbound-exporter \$ARGUMENTS
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
cat <<EOF > %{buildroot}%{_sysconfdir}/default/unbound-exporter
ARGUMENTS="-bound.ca '' -unbound.cert '' -unbound.host 'unix:///run/unbound.ctl'"
EOF

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin \
    -c "Prometheus daemon" prometheus
exit 0

%post
%systemd_post unbound-exporter.service

%preun
%systemd_preun unbound-exporter.service

%postun
%systemd_postun unbound-exporter.service

%files
%defattr(-,root,root,-)
%{_bindir}/unbound-exporter
%{_unitdir}/unbound-exporter.service
%config(noreplace) %{_sysconfdir}/default/unbound-exporter
