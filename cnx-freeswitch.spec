Name:		cnx-freeswitch
Version:	1.10.10.1
Release:	1%{?dist}
Summary:	Freeswitch 1.10.10 pour CNX
License:	MPL 1.1
Requires: curl >= 7.19
Requires: pcre
Requires: speex
Requires: sqlite >= 3.6.20
Requires: libtiff
Requires: libedit
Requires: openssl >= 1.0.1e
Requires: unixODBC
Requires: libjpeg
Requires: zlib
Requires: libxml2
Requires: libsndfile
# pour mod_snmp
Requires: net-snmp

%define BINDIR 		/usr/bin
%define LIBDIR		/usr/lib64
%define MODINSTDIR 	/usr/lib64/freeswitch/mod
%define DATADIR 	/usr/share/freeswitch
%define SYSCONFDIR 	/etc/freeswitch
%define GITDIR		%{_topdir}/..
%define LOGDIR		/var/log/freeswitch
%define RUNDIR		/var/run/freeswitch

%description
Freeswitch 1.10.10 patché pour Connectics

%package logger-graylog2
Summary:	GELF logger for Graylog2 and Logstash
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description logger-graylog2
GELF logger for Graylog2 and Logstash

%package event-snmp
Summary:	SNMP stats reporter for the FreeSWITCH open source telephony platform
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	net-snmp

%description event-snmp
SNMP stats reporter for the FreeSWITCH open source telephony platform

%package application-translate
Summary:	FreeSWITCH mod_translate
Group:          System/Libraries
Requires:       %{name} = %{version}-%{release}

%description application-translate
Provide an number translation to FreeSWITCH API calls

%package application-distributor
Summary:	FreeSWITCH mod_distributor
Group:          System/Libraries
Requires:       %{name} = %{version}-%{release}

%package application-hash
Summary:	FreeSWITCH mod_hash
Group:          System/Libraries
Requires:       %{name} = %{version}-%{release}

%description application-hash
Provides FreeSWITCH mod_hash, implements an API and application interface for 
manipulating a hash table. It also provides a limit backend. 

%package lua
Summary:	Lua support for the FreeSWITCH open source telephony platform
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description	lua

%description application-distributor
Provides FreeSWITCH mod_distributor, a simple round-robin style distribution
to call gateways.
%install
%{__mkdir} -p %{buildroot}%{BINDIR}
%{__mkdir} -p %{buildroot}%{MODINSTDIR}
%{__mkdir} -p %{buildroot}%{DATADIR}/scripts %{buildroot}%{DATADIR}/certs
%{__mkdir} -p %{buildroot}%{SYSCONFDIR}
%{__mkdir} -p %{buildroot}%{LOGDIR}
%{__mkdir} -p %{buildroot}%{RUNDIR}

#
# Exécutables
#
%{__install} -D -m 755 %{GITDIR}/freeswitch %{buildroot}%{BINDIR}/freeswitch
%{__install} -D -m 755 %{GITDIR}/fs_cli %{buildroot}%{BINDIR}/fs_cli
%{__install} -D -m 755 %{GITDIR}/fs_ivrd %{buildroot}%{BINDIR}/fs_ivrd
%{__install} -D -m 755 %{GITDIR}/fs_encode %{buildroot}%{BINDIR}/fs_encode
%{__install} -D -m 755 %{GITDIR}/tone2wav %{buildroot}%{BINDIR}/tone2wav
%{__install} -D -m 755 %{GITDIR}/scripts/gentls_cert %{buildroot}%{BINDIR}/gentsl_cert
#
# Fichiers systemd
#
%{__install} -Dpm 0644 %{GITDIR}/build/freeswitch.service %{buildroot}%{_unitdir}/freeswitch.service
%{__install} -Dpm 0644 %{GITDIR}/build/freeswitch-tmpfiles.conf %{buildroot}%{_tmpfilesdir}/freeswitch.conf
#
# Fichier sysconfig
#
%{__install} -D -m 744 %{GITDIR}/build/freeswitch.sysconfig %{buildroot}/etc/sysconfig/freeswitch
#
# Fichier monit
#
%{__install} -D -m 644 %{GITDIR}/build/freeswitch.monitrc %{buildroot}/etc/monit.d/freeswitch.monitrc

#
# Modules
#
%{__install} -m 664 %{GITDIR}/src/mod/loggers/mod_console/.libs/mod_console.so -t %{buildroot}%{MODINSTDIR}
%{__install} -m 664 %{GITDIR}/src/mod/loggers/mod_logfile/.libs/mod_logfile.so -t %{buildroot}%{MODINSTDIR}
%{__install} -m 664 %{GITDIR}/src/mod/loggers/mod_graylog2/.libs/mod_graylog2.so -t %{buildroot}%{MODINSTDIR}

%{__install} -m 664 %{GITDIR}/src/mod/event_handlers/mod_cdr_csv/.libs/mod_cdr_csv.so -t %{buildroot}%{MODINSTDIR}
%{__install} -m 664 %{GITDIR}/src/mod/event_handlers/mod_event_socket/.libs/mod_event_socket.so -t %{buildroot}%{MODINSTDIR}
%{__install} -m 664 %{GITDIR}/src/mod/event_handlers/mod_snmp/.libs/mod_snmp.so -t %{buildroot}%{MODINSTDIR}

%{__install} -m 664 %{GITDIR}/src/mod/endpoints/mod_sofia/.libs/mod_sofia.so -t %{buildroot}%{MODINSTDIR}

%{__install} -m 664 %{GITDIR}/src/mod/applications/mod_dptools/.libs/mod_dptools.so -t %{buildroot}%{MODINSTDIR}
%{__install} -m 664 %{GITDIR}/src/mod/applications/mod_commands/.libs/mod_commands.so -t %{buildroot}%{MODINSTDIR}
%{__install} -m 664 %{GITDIR}/src/mod/applications/mod_distributor/.libs/mod_distributor.so -t %{buildroot}%{MODINSTDIR}
%{__install} -m 664 %{GITDIR}/src/mod/applications/mod_translate/.libs/mod_translate.so -t %{buildroot}%{MODINSTDIR}
%{__install} -m 664 %{GITDIR}/src/mod/applications/mod_hash/.libs/mod_hash.so -t %{buildroot}%{MODINSTDIR}

%{__install} -m 664 %{GITDIR}/src/mod/dialplans/mod_dialplan_xml/.libs/mod_dialplan_xml.so -t %{buildroot}%{MODINSTDIR}

%{__install} -m 664 %{GITDIR}/src/mod/languages/mod_lua/.libs/mod_lua.so -t %{buildroot}%{MODINSTDIR}


%pre 
if ! /usr/bin/id freeswitch &>/dev/null; then
       /usr/sbin/useradd -r -g daemon -s /bin/false -c "The FreeSWITCH Open Source Voice Platform" -d %{LOCALSTATEDIR} freeswitch || \
                %logmsg "Unexpected error adding user \"freeswitch\". Aborting installation."
fi

%post
%{?run_ldconfig:%run_ldconfig}

chown freeswitch:daemon /var/log/freeswitch /var/run/freeswitch

%tmpfiles_create freeswitch
/usr/bin/systemctl -q enable freeswitch.service

%preun
%{?systemd_preun freeswitch.service}

%postun
%{?systemd_postun freeswitch.service}
%{?run_ldconfig:%run_ldconfig}
if [ $1 -eq 0 ]; then
    userdel freeswitch || %logmsg "User \"freeswitch\" could not be deleted."
fi

%files
%defattr(-,root,root)
%dir %attr(0750, freeswitch, daemon) %{SYSCONFDIR}
%dir %attr(0750, freeswitch, daemon) %{RUNDIR}
%dir %attr(0750, freeswitch, daemon) %{LOGDIR}
%{BINDIR}/freeswitch
%{BINDIR}/fs_cli
%{BINDIR}/fs_ivrd
%{BINDIR}/fs_encode
%{BINDIR}/gentsl_cert
%{BINDIR}/tone2wav

%{_unitdir}/freeswitch.service
%{_tmpfilesdir}/freeswitch.conf
%config(noreplace) %attr(0644,-,-) /etc/sysconfig/freeswitch
%config(noreplace) %attr(0644,-,-) /etc/monit.d/freeswitch.monitrc
%{MODINSTDIR}/mod_console.so
%{MODINSTDIR}/mod_logfile.so
%{MODINSTDIR}/mod_cdr_csv.so
%{MODINSTDIR}/mod_event_socket.so
%{MODINSTDIR}/mod_sofia.so
%{MODINSTDIR}/mod_dptools.so
%{MODINSTDIR}/mod_commands.so
%{MODINSTDIR}/mod_dialplan_xml.so

%files logger-graylog2
%{MODINSTDIR}/mod_graylog2.so*

%files event-snmp
%{MODINSTDIR}/mod_snmp.so*

%files application-distributor
%{MODINSTDIR}/mod_distributor.so*

%files application-translate
%{MODINSTDIR}/mod_translate.so*

%files application-hash
%{MODINSTDIR}/mod_hash.so*

%files lua
%{MODINSTDIR}/mod_lua*.so*

%changelog

