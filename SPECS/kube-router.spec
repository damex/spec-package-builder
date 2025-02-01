%define debug_package %{nil}

Name: kube-router
Version: 2.4.1
Release: 1%{?dist}
Summary: a turnkey solution for Kubernetes networking
License: ASL 2.0
URL: https://www.kube-router.io
Source: https://github.com/cloudnativelabs/kube-router/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%{?systemd_requires}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Kube-router is a turnkey solution for Kubernetes networking with aim to provide operational simplicity and high performance.

%prep
%setup -q

%build
go install -C cmd/kube-router
go build -C cmd/kube-router -o $(pwd)/kube-router

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -d %{buildroot}%{_sysconfdir}/default
%{__install} -d %{buildroot}%{_sysconfdir}/kube-router
%{__install} -m 755 kube-router %{buildroot}%{_bindir}/kube-router
cat <<EOF > %{buildroot}%{_unitdir}/kube-router.service
[Unit]
Description=a turnkey solution for Kubernetes networking
Documentation=%{url}

[Service]
User=root
Group=root
EnvironmentFile=%{_sysconfdir}/default/kube-router
ExecStart=%{_bindir}/kube-router \$ARGUMENTS
LimitNOFILE=65536
Restart=always
RestartSec=5s
StartLimitInterval=0
StartLimitBurst=0
Slice=kubernetes.slice

[Install]
WantedBy=multi-user.target
EOF

cat <<EOF > %{buildroot}%{_sysconfdir}/default/kube-router
ARGUMENTS=""
EOF

%post
%systemd_post kube-router.service

%preun
%systemd_preun kube-router.service

%postun
%systemd_postun kube-router.service

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_sysconfdir}/kube-router
%{_bindir}/kube-router
%{_unitdir}/kube-router.service
%config(noreplace) %{_sysconfdir}/default/kube-router
