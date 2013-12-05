%define debug_package %{nil}
%define base_install_dir %{_javadir}{%name}

Name:           graylog2-server
Version:        0.20.0.07
Release:        1%{?dist}
Summary:        graylog2-server

Group:          System Environment/Daemons
License:        ASL 2.0
URL:            http://www.graylog2.org
Source0:        graylog2-server-0.20.0-preview.7.tgz
Source1:        init.d-%{name}
Source2:        sysconfig-%{name}
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       jpackage-utils
Requires:       jre >= 1.6.0

Requires(post): chkconfig initscripts
Requires(pre):  chkconfig initscripts
Requires(pre):  shadow-utils

%description
A distributed, highly available, RESTful search engine

%prep
%setup -q -n graylog2-server-0.20.0-preview.7
#we have to use a specific name here until graylog starts using real version number
#%setup -q -n %{name}-%{version}

%build
true

%install
rm -rf $RPM_BUILD_ROOT
# I know we can use -p to create the root directory, but this is more to
# keep track of the required dir
%{__mkdir} -p %{buildroot}/opt/graylog2/server
%{__mkdir} -p %{buildroot}/opt/graylog2/server/bin
%{__install} -p -m 755 graylog2-server.jar %{buildroot}/opt/graylog2/server
%{__install} -p -m 755 bin/graylog2ctl %{buildroot}/opt/graylog2/server/bin/

# config
%{__mkdir} -p %{buildroot}%{_sysconfdir}/graylog2
%{__install} -m 644 graylog2.conf.example %{buildroot}%{_sysconfdir}/graylog2/graylog2.conf


# logs
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/graylog2/web
%{__mkdir} -p %{buildroot}/opt/graylog2/server/log

# plugins
%{__mkdir} -p %{buildroot}/opt/graylog2/server/plugin/alarm_callbacks
%{__mkdir} -p %{buildroot}/opt/graylog2/server/plugin/filters
%{__mkdir} -p %{buildroot}/opt/graylog2/server/plugin/initializers
%{__mkdir} -p %{buildroot}/opt/graylog2/server/plugin/inputs
%{__mkdir} -p %{buildroot}/opt/graylog2/server/plugin/ouput
%{__mkdir} -p %{buildroot}/opt/graylog2/server/plugin/transports

# sysconfig and init
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysconfig
%{__mkdir} -p %{buildroot}%{_sysconfdir}/init.d
%{__install} -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/%{name}
%{__install} -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

#Docs and other stuff
%{__install} -p -m 644 COPYING %{buildroot}/opt/graylog2/server
%{__install} -p -m 644 build_date %{buildroot}/opt/graylog2/server
%{__install} -p -m 644 README.markdown %{buildroot}/opt/graylog2/server

%pre
# create elasticsearch group
if ! getent group graylog2 >/dev/null; then
        groupadd -r graylog2
fi

# create elasticsearch user
if ! getent passwd graylog2 >/dev/null; then
        useradd -r -g graylog2 -d %{_javadir}/%{name} \
            -s /sbin/nologin -c "Party Gorilla" graylog2
fi

%post
/sbin/chkconfig --add graylog2-server

%preun
if [ $1 -eq 0 ]; then
  /sbin/service/graylog2 stop >/dev/null 2>&1
  /sbin/chkconfig --del graylog2-server
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_sysconfdir}/init.d/graylog2-server
%config(noreplace) %{_sysconfdir}/sysconfig/graylog2-server
%dir /opt/graylog2/server
%dir /opt/graylog2/server/bin
%dir /opt/graylog2/server/log
%dir /opt/graylog2/server/plugin
/opt/graylog2/server/graylog2-server.jar
/opt/graylog2/server/bin/graylog2ctl
/opt/graylog2/server/COPYING
/opt/graylog2/server/build_date
/opt/graylog2/server/README.markdown
%{_sysconfdir}/graylog2/graylog2.conf
%config(noreplace) %{_sysconfdir}/graylog2
%doc README.markdown
%defattr(-,graylog2,graylog2,-)
%dir %{_localstatedir}/log/graylog2

%changelog
* Wed Nov 04 2013 lee@leebriggs.co.uk 0.20.0.07-1
- Initial RPM

