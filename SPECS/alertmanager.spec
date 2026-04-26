%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/prometheus/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog
# HEAD as of 2025-12-11: includes GHC 9.4+/9.8 compat fixes (word8ToWord# in Data/Utf8.hs)
%define elm_compiler_commit cce7a8bbd8fe690fc83fa795f8d7e02505d1f25f

Name: alertmanager
Version: 0.32.0
Release: 1%{?dist}
Summary: The Alertmanager handles alerts sent by client applications such as the Prometheus server.
License: ASL 2.0
URL: https://prometheus.io
Source: https://github.com/prometheus/alertmanager/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# elm compiler built from source - no official arm64 binary, and HEAD has GHC 9.4+/9.8 fixes
Source1: https://github.com/elm/compiler/archive/%{elm_compiler_commit}.tar.gz#/elm-compiler-%{elm_compiler_commit}.tar.gz
%{?systemd_requires}
Requires(pre): shadow-utils
Requires: alertmanager-amtool
BuildRequires: golang >= 1.25.0, golang < 1.26.0
BuildRequires: nodejs
BuildRequires: %{?el9:npm}%{!?el9:nodejs-npm}
# elm
BuildRequires: ghc
BuildRequires: cabal-install
BuildRequires: gcc-c++

%package -n alertmanager-amtool
Summary: Tooling for the Alertmanager

%description
The Alertmanager handles alerts sent by client applications such as the Prometheus server.
It takes care of deduplicating, grouping, and routing them to the correct receiver integrations such as email,
PagerDuty, or OpsGenie. It also takes care of silencing and inhibition of alerts.

%description -n alertmanager-amtool
Tooling for the Alertmanager

%prep
%autosetup -a 1

%build
# build elm compiler from source
cd compiler-%{elm_compiler_commit}
cabal update
cabal v1-install --only-dependencies --disable-library-profiling
cabal v1-configure
cabal v1-build
cd ..
# skip elm download hook, place our compiled binary where npm package expects it
npm --prefix ui/app ci --ignore-scripts
%{__install} -m 755 compiler-%{elm_compiler_commit}/dist/build/elm/elm ui/app/node_modules/elm/bin/elm
# build elm UI assets
npm --prefix ui/app run build
export GOFLAGS=-buildvcs=false
go mod download
go build -C cmd/alertmanager -o $(pwd)/alertmanager
go build -C cmd/amtool -o $(pwd)/amtool

%install
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
LimitNOFILE=65535
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
%{__install} -d %{buildroot}%{_sysusersdir}
cat <<EOF > %{buildroot}%{_sysusersdir}/%{name}.conf
u prometheus - "Prometheus daemon" %{_sharedstatedir}/prometheus /sbin/nologin
EOF

%pre
%sysusers_create_compat %{_sysusersdir}/%{name}.conf

%post
%systemd_post alertmanager.service

%preun
%systemd_preun alertmanager.service

%postun
%systemd_postun alertmanager.service

%files
%defattr(-,root,root,-)
%{_bindir}/alertmanager
%dir %{_sysconfdir}/alertmanager
%config(noreplace) %{_sysconfdir}/alertmanager/alertmanager.yml
%{_unitdir}/alertmanager.service
%config(noreplace) %{_sysconfdir}/default/alertmanager
%{_sysusersdir}/%{name}.conf
%dir %attr(755, prometheus, prometheus)%{_sharedstatedir}/alertmanager

%files -n alertmanager-amtool
%defattr(-,root,root,-)
%{_bindir}/amtool
