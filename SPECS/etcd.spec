%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/kubernetes/%{disttype}/%{distnum}

Name: etcd
Version: 3.5.18
Release: 1%{?dist}
Summary: distributed key-value store
License: ASL 2.0
URL: https://etcd.io
Source: https://github.com/etcd-io/etcd/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%{?systemd_requires}
Requires(pre): shadow-utils
BuildRequires: golang >= 1.22.0, golang < 1.23.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%package -n etcd-etcdctl
Summary: Command line client for etcd

%package -n etcd-etcdutl
Summary: Command line administration utility for etcd

%package -n etcd-benchmark
Summary: Official benchmarking tool for etcd clusters

%package -n etcd-dump-db
Summary: Tool to inspect etcd db files

%package -n etcd-dump-logs
Summary: Tool to dump the log from data directory

%package -n etcd-dump-metrics
Summary: Provides metrics for the latest main branch, a given endpoint, or version

%description
%description -n etcd-etcdctl
%description -n etcd-etcdutl
%description -n etcd-benchmark
%description -n etcd-dump-db
%description -n etcd-dump-logs
%description -n etcd-dump-metrics

%prep
%setup -q

%build
cd %{_builddir}/etcd-%{version}
go install
go build -o $(pwd)/etcd
go install -C etcdctl
go build -C etcdctl -o $(pwd)/etcd-etcdctl
go install -C etcdutl
go build -C etcdutl -o $(pwd)/etcd-etcdutl
go install -C tools/benchmark
go build -C tools/benchmark -o $(pwd)/benchmark
go install -C tools/etcd-dump-db
go build -C tools/etcd-dump-db -o $(pwd)/etcd-dump-db
go install -C tools/etcd-dump-logs
go build -C tools/etcd-dump-logs -o $(pwd)/etcd-dump-logs
go install -C tools/etcd-dump-metrics
go build -C tools/etcd-dump-metrics -o $(pwd)/etcd-dump-metrics

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_sharedstatedir}/etcd
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_sysconfdir}/default
%{__install} -d %{buildroot}%{_sysconfdir}/etcd
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 755 etcd %{buildroot}%{_bindir}/etcd
%{__install} -m 755 etcd-etcdctl %{buildroot}%{_bindir}/etcdctl
%{__install} -m 755 etcd-etcdutl %{buildroot}%{_bindir}/etcdutl
%{__install} -m 755 benchmark %{buildroot}%{_bindir}/benchmark
%{__install} -m 755 etcd-dump-db %{buildroot}%{_bindir}/etcd-dump-db
%{__install} -m 755 etcd-dump-logs %{buildroot}%{_bindir}/etcd-dump-logs
%{__install} -m 755 etcd-dump-metrics %{buildroot}%{_bindir}/etcd-dump-metrics
cat <<EOF > %{buildroot}%{_unitdir}/etcd.service
[Unit]
Description=distributed key-value store
Documentation=https://etcd.io

[Service]
User=etcd
Group=etcd
EnvironmentFile=%{_sysconfdir}/default/etcd
ExecStart=%{_bindir}/etcd \$ARGUMENTS
ExecReload=%{_bindir}/kill -HUP \$MAINPID
SendSIGKILL=no
OOMScoreAdjust=-1000
Restart=always
RestartSec=5s
StartLimitInterval=0
StartLimitBurst=0

[Install]
WantedBy=multi-user.target
EOF
cat <<EOF > %{buildroot}%{_sysconfdir}/default/etcd
ARGUMENTS="--data-dir=%{_sharedstatedir}/etcd"
EOF
cat <<EOF > %{buildroot}%{_sysconfdir}/etcd/etcd.yml
ARGS=""
EOF

%pre
getent group etcd >/dev/null || groupadd -r etcd
getent passwd etcd >/dev/null || \
  useradd -r -g etcd -d %{_sharedstatedir}/etcd -s /sbin/nologin \
          -c "etcd" etcd/
exit 0

%post
%systemd_post etcd.service

%preun
%systemd_preun etcd.service

%postun
%systemd_postun etcd.service

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/etcd
%config(noreplace) %{_sysconfdir}/etcd/etcd.yml
%{_unitdir}/etcd.service
%config(noreplace) %{_sysconfdir}/default/etcd
%dir %attr(755, etcd, etcd)%{_sharedstatedir}/etcd

%files -n etcd-etcdctl
%defattr(-,root,root,-)
%{_bindir}/etcdctl

%files -n etcd-etcdutl
%defattr(-,root,root,-)
%{_bindir}/etcdutl

%files -n etcd-benchmark
%defattr(-,root,root,-)
%{_bindir}/benchmark

%files -n etcd-dump-db
%defattr(-,root,root,-)
%{_bindir}/etcd-dump-db

%files -n etcd-dump-logs
%defattr(-,root,root,-)
%{_bindir}/etcd-dump-logs

%files -n etcd-dump-metrics
%defattr(-,root,root,-)
%{_bindir}/etcd-dump-metrics
