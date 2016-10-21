%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%define version %{getenv:VERSION}
%define release %{getenv:RELEASE}

Name:             vsm-deploy
%if 0%{?suse_version}
Version:          2.0.0
Release:          217
%else
Version:          %{version}
Release:          %{release}
%endif
Summary:          Deployment tool for VSM

Group:            Deploy/VSM
License:          Intel
URL:              http://intel.com
Source:           %{name}-%{version}.tar.gz
BuildArch:        noarch
%if 0%{?suse_version}
BuildRequires:    shadow
Requires:         shadow
%endif

#TODO Add ceph rpms.
%description
Intel VSM Storage System Tools Kit.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for VSM Deploy Tools Kit.
Group:            Documentation

%description      doc
OpenStack Tools Kit (codename VSM) provides services to manage and
access block storage services for use by Virtual Machine instances.

This package contains documentation files for vsm.
%endif

%prep
%setup -q -n %{name}-%{version}

%build


%install
#---------------------------
# usr/bin/
#---------------------------
install -d -m 755 %{buildroot}%{_sysconfdir}/manifest/
install -p -D -m 755 tools/etc/vsm/cluster.manifest %{buildroot}%{_sysconfdir}/manifest/cluster.manifest
install -p -D -m 755 tools/etc/vsm/server.manifest %{buildroot}%{_sysconfdir}/manifest/server.manifest

install -d -m 755 %{buildroot}%{_usr}/local/bin/
install -d -m 755 %{buildroot}%{_usr}/local/bin/tools

install -p -D -m 755 admin-token %{buildroot}%{_bindir}/admin-token
install -p -D -m 755 agent-token %{buildroot}%{_bindir}/agent-token

%if 0%{?suse_version}
install -p -D -m 755 cluster_manifest %{buildroot}%{_usr}/bin/cluster_manifest
install -p -D -m 755 server_manifest  %{buildroot}%{_usr}/bin/server_manifest
install -p -D -m 755 getip  %{buildroot}%{_usr}/bin/getip
install -p -D -m 755 usr/bin/vsm-controller %{buildroot}%{_usr}/bin/vsm-controller
install -p -D -m 755 usr/bin/vsm-storage %{buildroot}%{_usr}/bin/vsm-storage
install -p -D -m 755 usr/bin/populate-servermanifest %{buildroot}%{_usr}/bin/populate-servermanifest
install -p -D -m 755 usr/bin/partition-drives %{buildroot}%{_usr}/bin/partition-drives
install -p -D -m 755 usr/bin/vsm-installer %{buildroot}%{_usr}/bin/vsm-installer
install -p -D -m 755 usr/bin/vsm-node %{buildroot}%{_usr}/bin/vsm-node
install -d -m 755 %{buildroot}%{_sysconfdir}/systemd/system
install -p -D -m 755 etc/systemd/system/epmd.socket %{buildroot}%{_sysconfdir}/systemd/system
install -p -D -m 755 restart-all %{buildroot}%{_usr}/bin/restart-all
install -p -D -m 755 replace-str %{buildroot}%{_usr}/bin/replace-str
#install -p -D -m 755 tools/hooks/add_disk.sh %{buildroot}%{_bindir}/add_disk

install -p -D -m 755 clean-data %{buildroot}%{_usr}/bin/clean-data
install -p -D -m 755 __clean-data %{buildroot}%{_usr}/bin/__clean-data
install -p -D -m 755 ec-profile %{buildroot}%{_usr}/bin/ec-profile
install -p -D -m 755 vsm-update %{buildroot}%{_usr}/bin/vsm-update

install -p -D -m 755 vsm-checker %{buildroot}%{_usr}/bin/vsm-checker
install -d -m 755 %{buildroot}%{_usr}/lib/vsm
cp -rf keys  %{buildroot}%{_usr}/lib/vsm/
cp -rf tools/ %{buildroot}%{_usr}/lib/vsm/
cp -rf usr/bin/keys  %{buildroot}%{_usr}/lib/vsm/
cp -rf usr/bin/tools/ %{buildroot}%{_usr}/lib/vsm/
%else
install -p -D -m 755 cluster_manifest %{buildroot}%{_usr}/local/bin/cluster_manifest
install -p -D -m 755 server_manifest  %{buildroot}%{_usr}/local/bin/server_manifest
install -p -D -m 755 getip  %{buildroot}%{_usr}/local/bin/getip
install -p -D -m 755 vsm-controller %{buildroot}%{_usr}/local/bin/vsm-controller
install -p -D -m 755 vsm-installer %{buildroot}%{_usr}/local/bin/vsm-installer
install -p -D -m 755 vsm-node %{buildroot}%{_usr}/local/bin/vsm-node
install -p -D -m 755 restart-all %{buildroot}%{_usr}/local/bin/restart-all
install -p -D -m 755 replace-str %{buildroot}%{_usr}/local/bin/replace-str

install -p -D -m 755 clean-data %{buildroot}%{_usr}/local/bin/clean-data
install -p -D -m 755 __clean-data %{buildroot}%{_usr}/local/bin/__clean-data
install -p -D -m 755 preinstall %{buildroot}%{_usr}/local/bin/preinstall
install -p -D -m 755 ec-profile %{buildroot}%{_usr}/local/bin/ec-profile
install -p -D -m 755 vsm-update %{buildroot}%{_usr}/local/bin/vsm-update

install -p -D -m 755 vsm-checker %{buildroot}%{_usr}/local/bin/vsm-checker

cp -rf keys  %{buildroot}%{_usr}/local/bin/
cp -rf tools %{buildroot}%{_usr}/local/bin/
%endif


%pre
getent group vsm >/dev/null || groupadd -r vsm --gid 165
if ! getent passwd vsm >/dev/null; then
  useradd -u 165 -r -g vsm -G vsm,nobody -d %{_sharedstatedir}/vsm -s /sbin/nologin -c "Vsm Storage Services" vsm
fi
exit 0

%files
%defattr(-,root,root,-)
%if 0%{?suse_version}
%dir %{_sysconfdir}/systemd
%dir %{_sysconfdir}/systemd/system
%attr(-, root, root) %{_usr}/bin/cluster_manifest
%attr(-, root, root) %{_usr}/bin/server_manifest
%attr(-, root, root) %{_bindir}/admin-token
%attr(-, root, root) %{_bindir}/agent-token
%attr(-, root, root) %{_usr}/bin/getip
%attr(-, root, root) %{_usr}/bin/vsm-storage
%attr(-, root, root) %{_usr}/bin/partition-drives
%attr(-, root, root) %{_usr}/bin/populate-servermanifest
%attr(-, root, root) %{_usr}/bin/vsm-controller
%attr(-, root, root) %{_usr}/bin/restart-all
%attr(-, root, root) %{_usr}/bin/replace-str
%attr(-, root, root) %{_usr}/bin/vsm-node
%attr(-, root, root) %{_usr}/bin/clean-data
%attr(-, root, root) %{_usr}/bin/__clean-data
%attr(-, root, root) %{_usr}/bin/vsm-installer
%attr(-, root, root) %{_usr}/bin/ec-profile
%attr(-, root, root) %{_usr}/bin/vsm-update
%attr(-, root, root) %{_usr}/bin/vsm-checker
%dir %{_usr}/lib/vsm
%attr(-, root, root) %{_usr}/lib/vsm/*
#%dir %{_usr}/lib/vsm/keys
#%attr(-, root, root) %{_usr}/lib/vsm/keys/*

%dir %{_sysconfdir}/manifest
%config(noreplace) %attr(-, root, root) %{_sysconfdir}/manifest/server.manifest
%config(noreplace) %attr(-, root, root) %{_sysconfdir}/manifest/cluster.manifest
%{_sysconfdir}/systemd/system/epmd.socket
%else
%config(noreplace) %attr(-, root, vsm) %{_usr}/local/bin/cluster_manifest
%config(noreplace) %attr(-, root, vsm) %{_usr}/local/bin/server_manifest
%config(noreplace) %attr(-, root, vsm) %{_bindir}/admin-token
%config(noreplace) %attr(-, root, vsm) %{_bindir}/agent-token
%config(noreplace) %attr(-, root, vsm) %{_usr}/local/bin/getip
%config(noreplace) %attr(-, root, vsm) %{_usr}/local/bin/vsm-controller
%config(noreplace) %attr(-, root, vsm) %{_usr}/local/bin/restart-all
%config(noreplace) %attr(-, root, vsm) %{_usr}/local/bin/replace-str
%config(noreplace) %attr(-, root, vsm) %{_usr}/local/bin/vsm-node
%config(noreplace) %attr(-, root, vsm) %{_usr}/local/bin/clean-data
%config(noreplace) %attr(-, root, vsm) %{_usr}/local/bin/__clean-data
%config(noreplace) %attr(-, root, vsm) %{_usr}/local/bin/vsm-installer
%config(noreplace) %attr(-, root, vsm) %{_usr}/local/bin/preinstall
%config(noreplace) %attr(-, root, vsm) %{_usr}/local/bin/ec-profile
%config(noreplace) %attr(-, root, vsm) %{_usr}/local/bin/vsm-update

%config(noreplace) %attr(-, root, vsm) %{_usr}/local/bin/vsm-checker

%dir %{_usr}/local/bin/keys
%config(noreplace) %attr(-, root, vsm) %{_usr}/local/bin/keys/*

%dir %{_usr}/local/bin/tools
%config(noreplace) %attr(-, root, vsm) %{_usr}/local/bin/tools/*

%dir %{_sysconfdir}/manifest
%config(noreplace) %attr(-, root, vsm) %{_sysconfdir}/manifest/server.manifest
%config(noreplace) %attr(-, root, vsm) %{_sysconfdir}/manifest/cluster.manifest
%endif

