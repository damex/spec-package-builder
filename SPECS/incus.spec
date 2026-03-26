%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/incus/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog

Name: incus
Version: 6.22.0
Release: 4%{?dist}
Summary: powerful system container and virtual machine manager
License: ASL 2.0
URL: https://github.com/lxc/incus
Source: https://github.com/lxc/incus/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%{?systemd_requires}
Requires(pre): shadow-utils
Requires: %{name}-client = %{version}-%{release}
Requires: attr
Requires: ca-certificates
Requires: dnsmasq
Requires: e2fsprogs
Requires: fuse3
Requires: gdisk
Requires: genisoimage
Requires: hwdata
Requires: iproute
Requires: iptables
Requires: iputils
Requires: kmod
Requires: lshw
Requires: nftables
Requires: rsync
Requires: squashfs-tools
Requires: tar
Requires: xdelta
Requires: xz
Requires: %{name}-agent = %{version}-%{release}
Requires: edk2-ovmf
Requires: qemu-img
Requires: qemu-kvm-core
Recommends: lxcfs
Recommends: btrfs-progs
Recommends: ceph-common
Recommends: lvm2
Recommends: xfsprogs
Recommends: zfs
BuildRequires: golang >= 1.25.0, golang < 1.26.0
BuildRequires: cowsql-devel
BuildRequires: libacl-devel
BuildRequires: libcap-devel
BuildRequires: libseccomp-devel
BuildRequires: lxc-devel
BuildRequires: raft-devel
BuildRequires: sqlite-devel
BuildRequires: systemd-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%package -n %{name}-client
Summary: command line client for Incus

%package -n %{name}-tools
Summary: extra tools for Incus

%package -n %{name}-agent
Summary: Incus virtual machine guest agent

%description
Incus provides the ability to run containers and virtual machines locally
along with very flexible networking and storage akin to what's offered
in a public cloud environment.

%description -n %{name}-client
Incus provides the ability to run containers and virtual machines locally
along with very flexible networking and storage akin to what's offered
in a public cloud environment. This package contains the command line client.

%description -n %{name}-tools
Incus provides the ability to run containers and virtual machines locally
along with very flexible networking and storage akin to what's offered
in a public cloud environment. This package contains additional command line tools.

%description -n %{name}-agent
Incus provides the ability to run containers and virtual machines locally
along with very flexible networking and storage akin to what's offered
in a public cloud environment. This package contains the virtual machine guest agent.

%prep
%autosetup

%build
export GOFLAGS=-buildvcs=false
export CGO_LDFLAGS_ALLOW="(-Wl,-wrap,pthread_create)|(-Wl,-z,now)"
go mod download
go build -tags libsqlite3 -o $(pwd)/incusd ./cmd/incusd
go build -tags libsqlite3 -o $(pwd)/incus-user ./cmd/incus-user
go build -tags libsqlite3 -o $(pwd)/lxd-to-incus ./cmd/lxd-to-incus
go build -o $(pwd)/incus ./cmd/incus
go build -o $(pwd)/fuidshift ./cmd/fuidshift
go build -o $(pwd)/incus-benchmark ./cmd/incus-benchmark
go build -o $(pwd)/lxc-to-incus ./cmd/lxc-to-incus
CGO_ENABLED=0 go build -tags netgo -o $(pwd)/incus-migrate ./cmd/incus-migrate
GOARCH=amd64 CGO_ENABLED=0 go build -tags "agent,netgo" -o $(pwd)/incus-agent.linux.x86_64 ./cmd/incus-agent
GOARCH=386 CGO_ENABLED=0 go build -tags "agent,netgo" -o $(pwd)/incus-agent.linux.i686 ./cmd/incus-agent
GOARCH=arm64 CGO_ENABLED=0 go build -tags "agent,netgo" -o $(pwd)/incus-agent.linux.aarch64 ./cmd/incus-agent
GOARCH=amd64 GOOS=windows CGO_ENABLED=0 go build -tags "agent,netgo" -o $(pwd)/incus-agent.windows.x86_64 ./cmd/incus-agent
GOARCH=386 GOOS=windows CGO_ENABLED=0 go build -tags "agent,netgo" -o $(pwd)/incus-agent.windows.i686 ./cmd/incus-agent
GOARCH=arm64 GOOS=windows CGO_ENABLED=0 go build -tags "agent,netgo" -o $(pwd)/incus-agent.windows.aarch64 ./cmd/incus-agent
GOARCH=amd64 GOOS=darwin CGO_ENABLED=0 go build -tags "agent,netgo" -o $(pwd)/incus-agent.macos.x86_64 ./cmd/incus-agent
GOARCH=arm64 GOOS=darwin CGO_ENABLED=0 go build -tags "agent,netgo" -o $(pwd)/incus-agent.macos.aarch64 ./cmd/incus-agent

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -d %{buildroot}%{_sysconfdir}/default
%{__install} -d %{buildroot}%{_sysconfdir}/dnsmasq.d
%{__install} -d -m 0711 %{buildroot}%{_sharedstatedir}/incus
%{__install} -d -m 0700 %{buildroot}%{_localstatedir}/cache/incus
%{__install} -d -m 0700 %{buildroot}%{_localstatedir}/log/incus
%{__install} -m 755 incusd %{buildroot}%{_bindir}/incusd
%{__install} -m 755 incus-user %{buildroot}%{_bindir}/incus-user
%{__install} -m 755 incus %{buildroot}%{_bindir}/incus
%{__install} -m 755 fuidshift %{buildroot}%{_bindir}/fuidshift
%{__install} -m 755 incus-benchmark %{buildroot}%{_bindir}/incus-benchmark
%{__install} -m 755 incus-migrate %{buildroot}%{_bindir}/incus-migrate
%{__install} -m 755 lxc-to-incus %{buildroot}%{_bindir}/lxc-to-incus
%{__install} -m 755 lxd-to-incus %{buildroot}%{_bindir}/lxd-to-incus
%{__install} -d %{buildroot}%{_datadir}/incus/agent
%{__install} -m 755 incus-agent.linux.x86_64 %{buildroot}%{_datadir}/incus/agent/incus-agent.linux.x86_64
%{__install} -m 755 incus-agent.linux.i686 %{buildroot}%{_datadir}/incus/agent/incus-agent.linux.i686
%{__install} -m 755 incus-agent.linux.aarch64 %{buildroot}%{_datadir}/incus/agent/incus-agent.linux.aarch64
%{__install} -m 755 incus-agent.windows.x86_64 %{buildroot}%{_datadir}/incus/agent/incus-agent.windows.x86_64
%{__install} -m 755 incus-agent.windows.i686 %{buildroot}%{_datadir}/incus/agent/incus-agent.windows.i686
%{__install} -m 755 incus-agent.windows.aarch64 %{buildroot}%{_datadir}/incus/agent/incus-agent.windows.aarch64
%{__install} -m 755 incus-agent.macos.x86_64 %{buildroot}%{_datadir}/incus/agent/incus-agent.macos.x86_64
%{__install} -m 755 incus-agent.macos.aarch64 %{buildroot}%{_datadir}/incus/agent/incus-agent.macos.aarch64
cat <<EOF > %{buildroot}%{_unitdir}/incus.socket
[Unit]
Description=Incus - Container and Virtual Machine Manager (unix socket)

[Socket]
ListenStream=%{_rundir}/incus/unix.socket
SocketMode=0660
SocketGroup=incus-admin
Service=incus.service

[Install]
WantedBy=sockets.target
EOF
cat <<EOF > %{buildroot}%{_unitdir}/incus.service
[Unit]
Description=Incus - Container and Virtual Machine Manager
After=network-online.target incus.socket
Requires=incus.socket
Documentation=https://linuxcontainers.org/incus

[Service]
EnvironmentFile=%{_sysconfdir}/default/incus
ExecStart=%{_bindir}/incusd \$ARGUMENTS
ExecStartPost=%{_bindir}/incusd waitready --timeout=600
KillMode=process
Restart=on-failure
TimeoutStartSec=600s
TimeoutStopSec=330s
LimitNOFILE=1048576
LimitNPROC=infinity
LimitCORE=infinity
TasksMax=infinity
Delegate=yes
OOMScoreAdjust=-999

[Install]
WantedBy=multi-user.target
Also=incus.socket
Also=incus-startup.service
EOF
cat <<EOF > %{buildroot}%{_unitdir}/incus-startup.service
[Unit]
Description=Incus - Container and Virtual Machine Manager (Startup)
After=incus.socket incus.service
Requires=incus.socket

[Service]
Type=oneshot
ExecStart=%{_bindir}/incusd activateifneeded
ExecStop=%{_bindir}/incusd shutdown
TimeoutStartSec=600s
TimeoutStopSec=600s
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF
cat <<EOF > %{buildroot}%{_unitdir}/incus-user.socket
[Unit]
Description=Incus - Container and Virtual Machine Manager (User unix socket)

[Socket]
ListenStream=%{_rundir}/incus/unix.socket.user
SocketMode=0660
SocketGroup=incus
Service=incus-user.service

[Install]
WantedBy=sockets.target
EOF
cat <<EOF > %{buildroot}%{_unitdir}/incus-user.service
[Unit]
Description=Incus - Container and Virtual Machine Manager (User)
After=incus.service
Requires=incus.service

[Service]
EnvironmentFile=%{_sysconfdir}/default/incus-user
ExecStart=%{_bindir}/incus-user \$ARGUMENTS
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
Also=incus-user.socket
EOF
cat <<EOF > %{buildroot}%{_sysconfdir}/default/incus
ARGUMENTS="--group incus-admin"
INCUS_AGENT_PATH=%{_datadir}/incus/agent
EOF
cat <<EOF > %{buildroot}%{_sysconfdir}/default/incus-user
ARGUMENTS="--group incus"
EOF
cat <<EOF > %{buildroot}%{_sysconfdir}/dnsmasq.d/incus.conf
except-interface=incusbr0
EOF
%{__install} -d %{buildroot}%{_sysusersdir}
cat <<EOF > %{buildroot}%{_sysusersdir}/incus.conf
g incus-admin -
u incus - "Incus daemon user" %{_sharedstatedir}/incus /sbin/nologin
EOF
%{__install} -d %{buildroot}%{_tmpfilesdir}
cat <<EOF > %{buildroot}%{_tmpfilesdir}/incus.conf
d /var/cache/incus 0700 root root - -
d /var/log/incus 0700 root root - -
d /var/lib/incus 0711 root root - -
d /run/incus 0711 root root - -
EOF
%{__install} -d %{buildroot}%{_sysctldir}
cat <<EOF > %{buildroot}%{_sysctldir}/10-incus-inotify.conf
fs.aio-max-nr = 16777216
fs.inotify.max_queued_events = 1048576
fs.inotify.max_user_instances = 1048576
fs.inotify.max_user_watches = 1048576
kernel.keys.maxbytes = 2000000
kernel.keys.maxkeys = 2000
net.ipv4.fib_sync_mem = 33554432
net.ipv4.neigh.default.gc_thresh3 = 8192
net.ipv6.neigh.default.gc_thresh3 = 8192
vm.max_map_count = 262144
EOF

%pre
%sysusers_create_compat %{_sysusersdir}/incus.conf

%post
%systemd_post incus.socket
%systemd_post incus.service
%systemd_post incus-startup.service
%systemd_post incus-user.socket
%systemd_post incus-user.service

%preun
%systemd_preun incus.socket
%systemd_preun incus.service
%systemd_preun incus-startup.service
%systemd_preun incus-user.socket
%systemd_preun incus-user.service

%postun
%systemd_postun incus.socket
%systemd_postun incus.service
%systemd_postun incus-startup.service
%systemd_postun incus-user.socket
%systemd_postun incus-user.service

%files
%defattr(-,root,root,-)
%{_bindir}/incusd
%{_bindir}/incus-user
%{_unitdir}/incus.socket
%{_unitdir}/incus.service
%{_unitdir}/incus-startup.service
%{_unitdir}/incus-user.socket
%{_unitdir}/incus-user.service
%config(noreplace) %{_sysconfdir}/default/incus
%config(noreplace) %{_sysconfdir}/default/incus-user
%config(noreplace) %{_sysconfdir}/dnsmasq.d/incus.conf
%{_sysusersdir}/incus.conf
%{_tmpfilesdir}/incus.conf
%{_sysctldir}/10-incus-inotify.conf
%dir %attr(711, root, root) %{_sharedstatedir}/incus
%dir %attr(700, root, root) %{_localstatedir}/cache/incus
%dir %attr(700, root, root) %{_localstatedir}/log/incus

%files -n %{name}-client
%defattr(-,root,root,-)
%{_bindir}/incus

%files -n %{name}-tools
%defattr(-,root,root,-)
%{_bindir}/fuidshift
%{_bindir}/incus-benchmark
%{_bindir}/incus-migrate
%{_bindir}/lxc-to-incus
%{_bindir}/lxd-to-incus

%files -n %{name}-agent
%defattr(-,root,root,-)
%dir %{_datadir}/incus
%dir %{_datadir}/incus/agent
%{_datadir}/incus/agent/incus-agent.linux.x86_64
%{_datadir}/incus/agent/incus-agent.linux.i686
%{_datadir}/incus/agent/incus-agent.linux.aarch64
%{_datadir}/incus/agent/incus-agent.windows.x86_64
%{_datadir}/incus/agent/incus-agent.windows.i686
%{_datadir}/incus/agent/incus-agent.windows.aarch64
%{_datadir}/incus/agent/incus-agent.macos.x86_64
%{_datadir}/incus/agent/incus-agent.macos.aarch64
