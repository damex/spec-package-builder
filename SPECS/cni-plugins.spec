%define debug_package %{nil}
%define cni_bindir /opt/cni/bin
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/kubernetes/%{disttype}/%{distnum}

Name: cni-plugins
Version: 1.5.1
Release: 1%{?dist}
Summary: CNI network plugins
License: ASL 2.0
URL: https://github.com/containernetworking/plugins
Source: https://github.com/containernetworking/plugins/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Requires: cni-plugins-main = %{version}
Requires: cni-plugins-ipam = %{version}
Requires: cni-plugins-meta = %{version}
BuildRequires: golang >= 1.22.0, golang < 1.23.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%package -n cni-plugins-main
Summary: CNI network plugins (main)

%package -n cni-plugins-ipam
Summary: CNI network plugins (ipam)

%package -n cni-plugins-meta
Summary: CNI network plugins (meta)

%description
CNI network plugins

%description -n cni-plugins-main
CNI network plugins (main)

%description -n cni-plugins-ipam
CNI network plugins (ipam)

%description -n cni-plugins-meta
CNI network plugins (meta)

%prep
%setup -q -n plugins-%{version}

%build
cd %{_builddir}/plugins-%{version}
# main
go install -C plugins/main/bridge
go build -C plugins/main/bridge -o $(pwd)/bridge
go install -C plugins/main/dummy
go build -C plugins/main/dummy -o $(pwd)/dummy
go install -C plugins/main/host-device
go build -C plugins/main/host-device -o $(pwd)/host-device
go install -C plugins/main/ipvlan
go build -C plugins/main/ipvlan -o $(pwd)/ipvlan
go install -C plugins/main/loopback
go build -C plugins/main/loopback -o $(pwd)/loopback
go install -C plugins/main/macvlan
go build -C plugins/main/macvlan -o $(pwd)/macvlan
go install -C plugins/main/ptp
go build -C plugins/main/ptp -o $(pwd)/ptp
go install -C plugins/main/tap
go build -C plugins/main/tap -o $(pwd)/tap
go install -C plugins/main/vlan
go build -C plugins/main/vlan -o $(pwd)/vlan
# ipam
go install -C plugins/ipam/dhcp
go build -C plugins/ipam/dhcp -o $(pwd)/dhcp
go install -C plugins/ipam/host-local
go build -C plugins/ipam/host-local -o $(pwd)/host-local
go install -C plugins/ipam/static
go build -C plugins/ipam/static -o $(pwd)/static
# meta
go install -C plugins/meta/bandwidth
go build -C plugins/meta/bandwidth -o $(pwd)/bandwidth
go install -C plugins/meta/firewall
go build -C plugins/meta/firewall -o $(pwd)/firewall
go install -C plugins/meta/portmap
go build -C plugins/meta/portmap -o $(pwd)/portmap
go install -C plugins/meta/sbr
go build -C plugins/meta/sbr -o $(pwd)/sbr
go install -C plugins/meta/sbr
go build -C plugins/meta/sbr -o $(pwd)/sbr
go install -C plugins/meta/tuning
go build -C plugins/meta/tuning -o $(pwd)/tuning
go install -C plugins/meta/vrf
go build -C plugins/meta/vrf -o $(pwd)/vrf

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{cni_bindir}
# main
%{__install} -m 755 bridge %{buildroot}%{cni_bindir}/bridge
%{__install} -m 755 dummy %{buildroot}%{cni_bindir}/dummy
%{__install} -m 755 host-device %{buildroot}%{cni_bindir}/host-device
%{__install} -m 755 ipvlan %{buildroot}%{cni_bindir}/ipvlan
%{__install} -m 755 loopback %{buildroot}%{cni_bindir}/loopback
%{__install} -m 755 macvlan %{buildroot}%{cni_bindir}/macvlan
%{__install} -m 755 ptp %{buildroot}%{cni_bindir}/ptp
%{__install} -m 755 tap %{buildroot}%{cni_bindir}/tap
%{__install} -m 755 vlan %{buildroot}%{cni_bindir}/vlan
# ipam
%{__install} -m 755 dhcp %{buildroot}%{cni_bindir}/dhcp
%{__install} -m 755 host-local %{buildroot}%{cni_bindir}/host-local
%{__install} -m 755 static %{buildroot}%{cni_bindir}/static
# meta
%{__install} -m 755 bandwidth %{buildroot}%{cni_bindir}/bandwidth
%{__install} -m 755 firewall %{buildroot}%{cni_bindir}/firewall
%{__install} -m 755 portmap %{buildroot}%{cni_bindir}/portmap
%{__install} -m 755 sbr %{buildroot}%{cni_bindir}/sbr
%{__install} -m 755 tuning %{buildroot}%{cni_bindir}/tuning
%{__install} -m 755 vrf %{buildroot}%{cni_bindir}/vrf

%clean
%{__rm} -rf %{buildroot}

%files

%files -n cni-plugins-main
%defattr(-,root,root,-)
%{cni_bindir}/bridge
%{cni_bindir}/dummy
%{cni_bindir}/host-device
%{cni_bindir}/ipvlan
%{cni_bindir}/loopback
%{cni_bindir}/macvlan
%{cni_bindir}/ptp
%{cni_bindir}/tap
%{cni_bindir}/vlan

%files -n cni-plugins-ipam
%defattr(-,root,root,-)
%{cni_bindir}/dhcp
%{cni_bindir}/host-local
%{cni_bindir}/static

%files -n cni-plugins-meta
%defattr(-,root,root,-)
%{cni_bindir}/bandwidth
%{cni_bindir}/firewall
%{cni_bindir}/portmap
%{cni_bindir}/sbr
%{cni_bindir}/tuning
%{cni_bindir}/vrf
