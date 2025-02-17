%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/prometheus/%{disttype}/%{distnum}

Name: node-exporter
Version: 1.9.0
Release: 1%{?dist}
Summary: Prometheus Node Exporter
License: ASL 2.0
URL: https://github.com/prometheus/node_exporter
Source: https://github.com/prometheus/node_exporter/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%{?systemd_requires}
Requires(pre): shadow-utils
BuildRequires: golang >= 1.22.0, golang < 1.23.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Prometheus exporter for hardware and OS metrics exposed by *NIX kernels, written in Go with pluggable metric collectors.

%prep
%setup -q -n node_exporter-%{version}

%build
cd %{_builddir}/node_exporter-%{version}
go install
go build -o $(pwd)/node-exporter

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -d %{buildroot}%{_sysconfdir}/default
%{__install} -m 755 node-exporter %{buildroot}%{_bindir}/node-exporter
cat <<EOF > %{buildroot}%{_unitdir}/node-exporter.service
[Unit]
Description=Prometheus Node Exporter
Documentation=%{url}

[Service]
Restart=always
User=prometheus
Group=prometheus
EnvironmentFile=%{_sysconfdir}/default/node-exporter
ExecStart=%{_bindir}/node-exporter \$ARGUMENTS
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
cat <<EOF > %{buildroot}%{_sysconfdir}/default/node-exporter
ARGUMENTS=""
EOF

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin \
    -c "Prometheus daemon" prometheus

%post
%systemd_post node-exporter.service

%preun
%systemd_preun node-exporter.service

%postun
%systemd_postun node-exporter.service

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/node-exporter
%{_unitdir}/node-exporter.service
%config(noreplace) %{_sysconfdir}/default/node-exporter
