%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/prometheus/%{disttype}/%{distnum}

Name: damex-prometheus-release
Version: 0.1.0
Release: 1%{?dist}
Summary: damex prometheus repository configuration
License: MIT
URL: https://yum-repositories.damex.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description

%prep

%build

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_sysconfdir}/yum.repos.d
cat <<EOF > %{buildroot}%{_sysconfdir}/yum.repos.d/damex-prometheus.repo
[damex-prometheus]
name = damex-prometheus
baseurl = https://yum-repositories.damex.org/prometheus/%{disttype}/%{distnum}
gpgcheck = 0
EOF

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/yum.repos.d/damex-prometheus.repo
