%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/kubernetes/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog

Name: kubernetes
Version: %{kubernetes_version}
Release: 1%{?dist}
Summary: open-source container orchestration system
License: ASL 2.0
URL: https://kubernetes.io
Source: https://github.com/kubernetes/kubernetes/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires: golang >= 1.25.0, golang < 1.26.0
BuildRoot: %{_tmppath}/%{name}-%{kubernetes_version}-%{release}-buildroot

%package -n kube-apiserver
Summary: services REST operations and provides the frontend to the cluster's shared state through which all other components interact
%{?systemd_requires}
Requires(pre): shadow-utils

%package -n kube-controller-manager
Summary: kube-controller-manager
%{?systemd_requires}
Requires(pre): shadow-utils

%package -n kube-proxy
Summary: The Kubernetes network proxy
%{?systemd_requires}
Requires(pre): shadow-utils

%package -n kube-scheduler
Summary: kube-scheduler
%{?systemd_requires}
Requires(pre): shadow-utils

%package -n kubelet
Summary: the primary node agent
%{?systemd_requires}
Requires(pre): shadow-utils

%package -n kubectl
Summary: command line tool for communicating with a Kubernetes cluster's control plane, using the Kubernetes API

%package -n kubectl-convert
Summary: command line tool for converting config files between different Kubernetes API versions

%description
%description -n kube-apiserver
%description -n kube-controller-manager
%description -n kube-proxy
%description -n kube-scheduler
%description -n kubelet
%description -n kubectl
%description -n kubectl-convert

%prep
%autosetup

%build
export GOFLAGS=-buildvcs=false
go mod download
go build -C cmd/kube-apiserver -o $(pwd)/kube-apiserver
go build -C cmd/kube-controller-manager -o $(pwd)/kube-controller-manager
go build -C cmd/kube-proxy -o $(pwd)/kube-proxy
go build -C cmd/kube-scheduler -o $(pwd)/kube-scheduler
go build -C cmd/kubelet -o $(pwd)/kubelet
go build -C cmd/kubectl -o $(pwd)/kubectl
go build -C cmd/kubectl-convert -o $(pwd)/kubectl-convert

%install
%{__install} -d %{buildroot}%{_sharedstatedir}/kubernetes
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_sysconfdir}/default
%{__install} -d %{buildroot}%{_sysconfdir}/kubernetes
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 755 kube-apiserver %{buildroot}%{_bindir}/kube-apiserver
%{__install} -m 755 kube-controller-manager %{buildroot}%{_bindir}/kube-controller-manager
%{__install} -m 755 kube-proxy %{buildroot}%{_bindir}/kube-proxy
%{__install} -m 755 kube-scheduler %{buildroot}%{_bindir}/kube-scheduler
%{__install} -m 755 kubelet %{buildroot}%{_bindir}/kubelet
%{__install} -m 755 kubectl %{buildroot}%{_bindir}/kubectl
%{__install} -m 755 kubectl-convert %{buildroot}%{_bindir}/kubectl-convert
cat <<EOF > %{buildroot}%{_unitdir}/kube-apiserver.service
[Unit]
Description=Kubernetes API server
Documentation=https://kubernetes.io

[Service]
User=kubernetes
Group=kubernetes
RuntimeDirectory=kubernetes
EnvironmentFile=%{_sysconfdir}/default/kube-apiserver
ExecStart=%{_bindir}/kube-apiserver \$ARGUMENTS
OOMScoreAdjust=-1000
Restart=always
RestartSec=5s
StartLimitInterval=0
StartLimitBurst=0
Type=notify
LimitNOFILE=65535
Slice=kubernetes.slice

[Install]
WantedBy=multi-user.target
EOF

cat <<EOF > %{buildroot}%{_unitdir}/kube-controller-manager.service
[Unit]
Description=kube-controller-manager
Documentation=https://kubernetes.io

[Service]
User=kubernetes
Group=kubernetes
EnvironmentFile=%{_sysconfdir}/default/kube-controller-manager
ExecStart=%{_bindir}/kube-controller-manager \$ARGUMENTS
OOMScoreAdjust=-1000
Restart=always
RestartSec=5s
StartLimitInterval=0
StartLimitBurst=0
LimitNOFILE=65535
Slice=kubernetes.slice

[Install]
WantedBy=multi-user.target
EOF

cat <<EOF > %{buildroot}%{_unitdir}/kube-proxy.service
[Unit]
Description=Kubernetes network proxy
Documentation=https://kubernetes.io

[Service]
EnvironmentFile=%{_sysconfdir}/default/kube-proxy
ExecStart=%{_bindir}/kube-proxy \$ARGUMENTS
OOMScoreAdjust=-1000
Restart=always
RestartSec=5s
StartLimitInterval=0
StartLimitBurst=0
LimitNOFILE=65535
Slice=kubernetes.slice

[Install]
WantedBy=multi-user.target
EOF

cat <<EOF > %{buildroot}%{_unitdir}/kube-scheduler.service
[Unit]
Description=kube-scheduler
Documentation=https://kubernetes.io

[Service]
User=kubernetes
Group=kubernetes
EnvironmentFile=%{_sysconfdir}/default/kube-scheduler
ExecStart=%{_bindir}/kube-scheduler \$ARGUMENTS
OOMScoreAdjust=-1000
Restart=always
RestartSec=5s
StartLimitInterval=0
StartLimitBurst=0
LimitNOFILE=65535
Slice=kubernetes.slice

[Install]
WantedBy=multi-user.target
EOF

cat <<EOF > %{buildroot}%{_unitdir}/kubelet.service
[Unit]
Description=the primary node agent
Documentation=https://kubernetes.io

[Service]
EnvironmentFile=%{_sysconfdir}/default/kubelet
ExecStart=%{_bindir}/kubelet \$ARGUMENTS
OOMScoreAdjust=-1000
Restart=always
RestartSec=5s
StartLimitInterval=0
StartLimitBurst=0
LimitNOFILE=65535
Slice=kubernetes.slice

[Install]
WantedBy=multi-user.target
EOF

cat <<EOF > %{buildroot}%{_sysconfdir}/default/kube-apiserver
ARGUMENTS=""
EOF

cat <<EOF > %{buildroot}%{_sysconfdir}/default/kube-controller-manager
ARGUMENTS=""
EOF

cat <<EOF > %{buildroot}%{_sysconfdir}/default/kube-proxy
ARGUMENTS="--config=/etc/kubernetes/kube-proxy.yml"
EOF

cat <<EOF > %{buildroot}%{_sysconfdir}/default/kube-scheduler
ARGUMENTS=""
EOF

cat <<EOF > %{buildroot}%{_sysconfdir}/default/kubelet
ARGUMENTS="--config=/etc/kubernetes/kubelet.yml"
EOF

cat <<EOF > %{buildroot}%{_sysconfdir}/kubernetes/kube-proxy.yml
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
EOF

cat <<EOF > %{buildroot}%{_sysconfdir}/kubernetes/kubelet.yml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
EOF
%{__install} -d %{buildroot}%{_sysusersdir}
cat <<EOF > %{buildroot}%{_sysusersdir}/kube-apiserver.conf
u kubernetes - "kubernetes" %{_sharedstatedir}/kubernetes /sbin/nologin
EOF
cat <<EOF > %{buildroot}%{_sysusersdir}/kube-controller-manager.conf
u kubernetes - "kubernetes" %{_sharedstatedir}/kubernetes /sbin/nologin
EOF
cat <<EOF > %{buildroot}%{_sysusersdir}/kube-proxy.conf
u kubernetes - "kubernetes" %{_sharedstatedir}/kubernetes /sbin/nologin
EOF
cat <<EOF > %{buildroot}%{_sysusersdir}/kube-scheduler.conf
u kubernetes - "kubernetes" %{_sharedstatedir}/kubernetes /sbin/nologin
EOF
cat <<EOF > %{buildroot}%{_sysusersdir}/kubelet.conf
u kubernetes - "kubernetes" %{_sharedstatedir}/kubernetes /sbin/nologin
EOF

%pre -n kube-apiserver
%sysusers_create_compat %{_sysusersdir}/kube-apiserver.conf

%pre -n kube-controller-manager
%sysusers_create_compat %{_sysusersdir}/kube-controller-manager.conf

%pre -n kube-proxy
%sysusers_create_compat %{_sysusersdir}/kube-proxy.conf

%pre -n kube-scheduler
%sysusers_create_compat %{_sysusersdir}/kube-scheduler.conf

%pre -n kubelet
%sysusers_create_compat %{_sysusersdir}/kubelet.conf

%post -n kube-apiserver
%systemd_post kube-apiserver.service

%preun -n kube-apiserver
%systemd_preun kube-apiserver.service

%postun -n kube-apiserver
%systemd_postun kube-apiserver.service

%post -n kube-controller-manager
%systemd_post kube-controller-manager.service

%preun -n kube-controller-manager
%systemd_preun kube-controller-manager.service

%postun -n kube-controller-manager
%systemd_postun kube-controller-manager.service

%post -n kube-proxy
%systemd_post kube-proxy.service

%preun -n kube-proxy
%systemd_preun kube-proxy.service

%postun -n kube-proxy
%systemd_postun kube-proxy.service

%post -n kube-scheduler
%systemd_post kube-scheduler.service

%preun -n kube-scheduler
%systemd_preun kube-scheduler.service

%postun -n kube-scheduler
%systemd_postun kube-scheduler.service

%post -n kubelet
%systemd_post kubelet.service

%preun -n kubelet
%systemd_preun kubelet.service

%postun -n kubelet
%systemd_postun kubelet.service

%files -n kube-apiserver
%defattr(-,root,root,-)
%{_sysusersdir}/kube-apiserver.conf
%dir %attr(755, kubernetes, kubernetes)%{_sharedstatedir}/kubernetes
%config(noreplace) %{_sysconfdir}/default/kube-apiserver
%{_unitdir}/kube-apiserver.service
%{_bindir}/kube-apiserver

%files -n kube-controller-manager
%defattr(-,root,root,-)
%{_sysusersdir}/kube-controller-manager.conf
%dir %attr(755, kubernetes, kubernetes)%{_sharedstatedir}/kubernetes
%config(noreplace) %{_sysconfdir}/default/kube-controller-manager
%{_unitdir}/kube-controller-manager.service
%{_bindir}/kube-controller-manager

%files -n kube-proxy
%defattr(-,root,root,-)
%{_sysusersdir}/kube-proxy.conf
%dir %attr(755, kubernetes, kubernetes)%{_sharedstatedir}/kubernetes
%config(noreplace) %{_sysconfdir}/default/kube-proxy
%dir %{_sysconfdir}/kubernetes
%config(noreplace) %{_sysconfdir}/kubernetes/kube-proxy.yml
%{_unitdir}/kube-proxy.service
%{_bindir}/kube-proxy

%files -n kube-scheduler
%defattr(-,root,root,-)
%{_sysusersdir}/kube-scheduler.conf
%dir %attr(755, kubernetes, kubernetes)%{_sharedstatedir}/kubernetes
%config(noreplace) %{_sysconfdir}/default/kube-scheduler
%{_unitdir}/kube-scheduler.service
%{_bindir}/kube-scheduler

%files -n kubelet
%defattr(-,root,root,-)
%{_sysusersdir}/kubelet.conf
%dir %attr(755, kubernetes, kubernetes)%{_sharedstatedir}/kubernetes
%config(noreplace) %{_sysconfdir}/default/kubelet
%dir %{_sysconfdir}/kubernetes
%config(noreplace) %{_sysconfdir}/kubernetes/kubelet.yml
%{_unitdir}/kubelet.service
%{_bindir}/kubelet

%files -n kubectl
%defattr(-,root,root,-)
%{_bindir}/kubectl

%files -n kubectl-convert
%defattr(-,root,root,-)
%{_bindir}/kubectl-convert
