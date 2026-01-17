%define debug_package %{nil}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}
%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define _rpmdir %{_topdir}/RPMS/pocket-id/%{disttype}/%{distnum}
%undefine source_date_epoch_from_changelog

Name: pocket-id
Version: 2.2.0
Release: 1%{?dist}
Summary: A simple OIDC provider for passwordless authentication
License: ASL 2.0
URL: https://github.com/pocket-id/pocket-id
Source: https://github.com/pocket-id/pocket-id/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%{?systemd_requires}
BuildRequires: nodejs
BuildRequires: nodejs-npm
BuildRequires: golang >= 1.25.0, golang < 1.26.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Pocket ID is a simple OIDC provider that allows users to authenticate with their passkeys to your services.

%prep
%setup -q

%build
export GOFLAGS=-buildvcs=false
npm install -g pnpm@latest-10
pnpm --filter pocket-id-frontend install
pnpm --filter pocket-id-frontend build
go install -C backend/cmd
go build -C backend/cmd -o $(pwd)/pocket-id

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -d %{buildroot}%{_sysconfdir}/default
%{__install} -m 755 pocket-id %{buildroot}%{_bindir}/pocket-id
cat <<EOF > %{buildroot}%{_unitdir}/pocket-id.service
[Unit]
Description=pocket-id
Documentation=%{url}

[Service]
User=pocket-id
Group=pocket-id
EnvironmentFile=%{_sysconfdir}/default/pocket-id
ExecStart=%{_bindir}/pocket-id
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
cat <<EOF > %{buildroot}%{_sysconfdir}/default/pocket-id
ENCRYPTION_KEY="$(openssl rand -base64 32)"
PUID="808"
PGID="808"
EOF

%pre
getent group pocket-id >/dev/null || groupadd -r -g 808 pocket-id
getent passwd pocket-id >/dev/null || \
  useradd -r -u 808 -g pocket-id -d %{_sharedstatedir}/pocket-id -s /sbin/nologin \
    -c "PocketID daemon" pocket-id
exit 0

%post
%systemd_post pocket-id.service

%preun
%systemd_preun pocket-id.service

%postun
%systemd_postun pocket-id.service

%files
%defattr(-,root,root,-)
%{_bindir}/pocket-id
%{_unitdir}/pocket-id.service
%config(noreplace) %{_sysconfdir}/default/pocket-id
