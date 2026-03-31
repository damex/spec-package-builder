%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/zfs/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog

Name: damex-zfs-release
Version: 0.1.0
Release: 1%{?dist}
Summary: damex zfs repository configuration
License: MIT
URL: https://yum-repositories.damex.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description

%prep

%build

%install
%{__install} -d %{buildroot}%{_sysconfdir}/yum.repos.d
cat <<EOF > %{buildroot}%{_sysconfdir}/yum.repos.d/damex-zfs.repo
[damex-zfs]
name = damex-zfs
baseurl = https://yum-repositories.damex.org/zfs/%{disttype}/%{distnum}/%{_arch}
gpgcheck = 1
gpgkey = https://yum-repositories.damex.org/zfs/yum-repositories-2035-11-30.asc
EOF

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/yum.repos.d/damex-zfs.repo
