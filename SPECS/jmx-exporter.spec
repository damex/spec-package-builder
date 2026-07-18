%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/prometheus/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog

Name: jmx-exporter
Version: 1.6.0
Release: 1%{?dist}
Summary: JMX Exporter (Standalone)
License: ASL 2.0
URL: https://github.com/prometheus/jmx_exporter
Source: https://github.com/prometheus/jmx_exporter/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%{?systemd_requires}
Requires(pre): shadow-utils
BuildRequires: java-21-openjdk-devel
Requires: java

%package -n jmx-exporter-agent
Summary: JMX Exptorter (Agent)

%description
The JMX Exporter is a collector to capture JMX MBean values.

%description -n jmx-exporter-agent
The JMX Exporter is a collector to capture JMX MBean values.

%prep
%autosetup -n jmx_exporter-%{version}

%build
cd %{_builddir}/jmx_exporter-%{version}
./mvnw clean package -Dparamixel.skipTests=true

%install
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -d %{buildroot}%{_sysconfdir}/default
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}-agent
%{__install} -d %{buildroot}%{_sharedstatedir}
%{__install} -d %{buildroot}%{_sharedstatedir}/%{name}
%{__install} -m 755 jmx_prometheus_standalone/target/jmx_prometheus_standalone-%{version}.jar %{buildroot}%{_sharedstatedir}/%{name}/%{name}.jar
%{__install} -m 755 jmx_prometheus_javaagent/target/jmx_prometheus_javaagent-%{version}.jar %{buildroot}%{_sharedstatedir}/%{name}/%{name}-agent.jar
cat <<EOF > %{buildroot}%{_unitdir}/%{name}.service
[Unit]
Description=JMX Exporter
Documentation=%{url}

[Service]
User=prometheus
Group=prometheus
EnvironmentFile=%{_sysconfdir}/default/%{name}
ExecStart=%{_bindir}/java -jar %{_sharedstatedir}/%{name}/%{name}.jar %{_sysconfdir}/%{name}/%{name}.yml
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
cat <<EOF > %{buildroot}%{_sysconfdir}/default/%{name}
EOF
cat <<EOF > %{buildroot}%{_sysconfdir}/%{name}/%{name}.yml
EOF
cat <<EOF > %{buildroot}%{_sysconfdir}/%{name}-agent/%{name}-agent.yml
EOF
%{__install} -d %{buildroot}%{_sysusersdir}
cat <<EOF > %{buildroot}%{_sysusersdir}/%{name}.conf
u prometheus - "Prometheus daemon" %{_sharedstatedir}/prometheus /sbin/nologin
EOF

%pre
%sysusers_create_compat %{_sysusersdir}/%{name}.conf

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%{_sharedstatedir}/%{name}/%{name}.jar
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.yml
%{_sysusersdir}/%{name}.conf

%files -n jmx-exporter-agent
%defattr(-,root,root,-)
%{_sharedstatedir}/%{name}/jmx-exporter-agent.jar
%config(noreplace) %{_sysconfdir}/%{name}-agent/%{name}-agent.yml
