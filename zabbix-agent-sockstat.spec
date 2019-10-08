%define     main_version  4.0
%define     minor_version 12
%define     module_dir    src/modules

Name:       sockstat-zabbix-module
Version:    %{main_version}.%{minor_version}
Release:    1%{?dist}
Summary:    Agent module for zabbix for network sockets status

Group:      Applications/Internet
License:    GPLv2+
URL: 		https://github.com/vicendominguez/sockstat-zabbix-module
VCS:        git+git@github.com:vganyn-alarstudios/sockstat-zabbix-module.git#3d5d36a1bf80b98a5c9e85bf36b3506e112bb5ef:

Source1:    zbx_sockstat.c
Source2:    Makefile

Requires:   zabbix-agent >= 4.0.0, zabbix-agent < 4.1.0

BuildRequires: systemd, gcc
Requires(post):  systemd
Requires(preun): systemd

%description
Agent module to parse the /proc/net/sockstat info for Zabbix > 2.2.x agent.
Info: https://github.com/vicendominguez/sockstat-zabbix-module

%global debug_package %{nil}

%prep
%setup -q -n sockstat-zabbix-module
curl -o /tmp/zbx.rpm https://repo.zabbix.com/zabbix/%{main_version}/rhel/%{?rhel}/SRPMS/zabbix-%{version}-1.el%{?rhel}.src.rpm
rpm -i /tmp/zbx.rpm
%setup -qTcn zabbix-%{version}
tar --strip-components=1 -xf %{_topdir}/SOURCES/zabbix-%{version}.tar.gz
echo 'LoadModule=zbx_sockstat.so' > %{_topdir}/SOURCES/zbx_sockstat.conf

%build
%configure
mkdir -p %{module_dir}/%{name}
cp %{SOURCE1} %{SOURCE2} %{module_dir}/%{name}/
cd %{module_dir}/%{name}/
make

%install
install --directory %{buildroot}%{_libdir}/zabbix/modules/
install --directory %{buildroot}/etc/zabbix/zabbix_agentd.d

install -m 0755 %{_builddir}/zabbix-%{version}/%{module_dir}/%{name}/zbx_sockstat.so %{buildroot}%{_libdir}/zabbix/modules/
install -m 0644 %{_topdir}/SOURCES/zbx_sockstat.conf                             %{buildroot}/etc/zabbix/zabbix_agentd.d/

%clean
rm -rf %{buildroot}

%files
/%{_libdir}/zabbix/modules/
/etc/zabbix/zabbix_agentd.d/zbx_sockstat.conf

%post
/usr/bin/systemctl try-restart zabbix-agent.service >/dev/null 2>&1 || :

%postun
/usr/bin/systemctl try-restart zabbix-agent.service >/dev/null 2>&1 || :

%changelog
* Fri Feb 8  2019 Anatolii Vorona <vorona.tolik@gmail.com>    - 3.4
- Updated spec for EPEL7 and systemd

* Tue Jan 28 2014 Vicente Dominguez <twitter:@vicendominguez> - 2.00
- No malloc, random value solved and first production version

* Fri Jan 24 2014 Vicente Dominguez <twitter:@vicendominguez> - 0.99
- rpm for rhel6 (fast-way) 