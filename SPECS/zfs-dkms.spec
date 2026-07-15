%define debug_package %{nil}
%global _build_id_links none
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/zfs/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog
%global __brp_mangle_shebangs_exclude_from ^/usr/src/.*$

%define module zfs

Name: %{module}-dkms
Version: 2.4.3
Release: 1%{?dist}
Summary: OpenZFS DKMS kernel modules
License: CDDL-1.0
URL: https://openzfs.github.io/openzfs-docs/
Source0: https://github.com/openzfs/zfs/releases/download/zfs-%{version}/zfs-%{version}.tar.gz
ExclusiveArch: x86_64 aarch64
Requires: dkms
Requires: diffutils
Requires: perl

%description
OpenZFS DKMS kernel modules. Automatically builds and installs ZFS
kernel modules for each installed kernel.

%prep
%autosetup -n %{module}-%{version}

%build
scripts/dkms.mkconf -n %{module} -v %{version} -f dkms.conf

%install
%{__mkdir_p} %{buildroot}%{_usrsrc}
%{__cp} -rf %{_builddir}/%{module}-%{version} %{buildroot}%{_usrsrc}/

%pre
if [ -d /var/lib/dkms/%{module} ]; then
    cd /var/lib/dkms/%{module}
    for otherver in [[:digit:]]*; do
        [ -d "${otherver}" ] || continue
        if [ "${otherver}" != "%{version}" ]; then
            if [ $(dkms status -m %{module} -v "${otherver}" | grep -c %{module}) -gt 0 ]; then
                dkms remove -m %{module} -v "${otherver}" --all ||:
            fi
        fi
    done
fi
if [ $(dkms status -m %{module} -v %{version} | grep -c %{module}) -gt 0 ]; then
    dkms remove -m %{module} -v %{version} --all ||:
fi

%post
dkms add -m %{module} -v %{version} --rpm_safe_upgrade ||:
dkms install --force -m %{module} -v %{version} ||:

%preun
if [ "$1" -eq 0 ]; then
    if [ $(dkms status -m %{module} -v %{version} | grep -c %{module}) -gt 0 ]; then
        dkms remove -m %{module} -v %{version} --all --rpm_safe_upgrade ||:
    fi
fi

%files
%defattr(-,root,root,-)
%license LICENSE
%{_usrsrc}/%{module}-%{version}
