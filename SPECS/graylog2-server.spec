%define debug_package %{nil}
%define base_install_dir %{_javadir}{%name}
%define __jar_repack %{nil
}
Name:           graylog2-server
Version:        0.20.2
Release:        1%{?dist}
Summary:        graylog2-server

Group:          System Environment/Daemons
License:        ASL 2.0
URL:            http://www.graylog2.org
Source0:        graylog2-server-0.20.2.tgz
Source1:        init.d-%{name}
Source2:        sysconfig-%{name}
Source3:        log4j.xml
Source4:	logrotate-%{name}
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       jpackage-utils
Requires:       java-1.7.0-openjdk
Requires: 	logrotate

Requires(post): chkconfig initscripts
Requires(pre):  chkconfig initscripts
Requires(pre):  shadow-utils

%description
A distributed, highly available, RESTful search engine

%prep
%setup -q -n graylog2-server-0.20.2
#we have to use a specific name here until graylog starts using real version number

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
%{__install} -m 644 graylog2.conf.example %{buildroot}%{_sysconfdir}/graylog2/server.conf


# logs
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/graylog2/web
%{__mkdir} -p %{buildroot}/opt/graylog2/server/log
%{__install} -p -m 644 %{SOURCE3} %{buildroot}/opt/graylog2/server/log4j.xml

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
%{__install} -m 644 %{SOURCE4}  %{buildroot}%{_sysconfdir}/logrotate.d/%name

#Docs and other stuff
%{__install} -p -m 644 COPYING %{buildroot}/opt/graylog2/server
%{__install} -p -m 644 build_date %{buildroot}/opt/graylog2/server
%{__install} -p -m 644 README.markdown %{buildroot}/opt/graylog2/server
%{__mkdir} -p %{buildroot}/var/run/graylog2
%pre
# create graylog2 group
if ! getent group graylog2 >/dev/null; then
        groupadd -r graylog2
fi

# create graylog2 user
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
%config(noreplace) %{_sysconfdir}/graylog2/server.conf
%config(noreplace) %{_sysconfdir}/graylog2
%config(noreplace) %{_sysconfdir}/logrotate.d/%name
%doc README.markdown
%defattr(-,graylog2,graylog2,-)
/opt/graylog2/server/graylog2-server.jar
/opt/graylog2/server/bin/graylog2ctl
/opt/graylog2/server/log4j.xml
/opt/graylog2/server/COPYING
/opt/graylog2/server/build_date
/opt/graylog2/server/README.markdown
/var/run/graylog2
%dir %{_localstatedir}/log/graylog2

%changelog
* Mon Jun 02 2014 lee@leebriggs.co.uk 0.20.2
- adding logrotate config
* Wed Feb 26 2014 lee@leebriggs.co.uk 0.20.1
- bugfix release 0.20.1
* Wed Feb 19 2014 lee@leebriggs.co.uk 0.20.0
- final release
- added option for JAVA_EXTRA_ARGS
* Fri Feb 14 2014 lee@leebriggs.co.uk 0.20.0-rc3
- bump for new release
* Mon Feb 10 2014 lee@leebriggs.co.uk 0.20.0-rc2
- Some changes to the init script
- Bumping for new release
* Tue Jan 21 2014 lee@leebriggs.co.uk 0.20.0-rc1.1
- Updating for Rc1.1 release
* Tue Jan 14 2014 lee@leebriggs.co.uk 0.20.0-rc1
- New GL 2 release
- fixing the version numbering
* Fri Dec 13 2013 lee@leebriggs.co.uk 0.20.0.08-1
- updating for new GL2 release
- updated comments
* Wed Dec 04 2013 lee@leebriggs.co.uk 0.20.0.07-1
- Initial RPM

