Name:		cnx-freeswitch
Version:	1.10.10.1
Release:	9%{?dist}
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
%define STATEDIR	/var/lib/freeswitch

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

%description application-distributor
Provides FreeSWITCH mod_distributor, a simple round-robin style distribution
to call gateways.

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

%description lua
Provides FreeSWITCH mod_lua.

%package config-minimal
Summary:        Minimial config for the FreeSWITCH Open Source telephone platform.
Group:          System/Libraries
Requires:	%{name} = %{version}-%{release}

%description config-minimal
Minimial config for the FreeSWITCH Open Source telephone platform.

%install
%{__mkdir} -p %{buildroot}%{BINDIR}
%{__mkdir} -p %{buildroot}%{MODINSTDIR}
%{__mkdir} -p %{buildroot}%{DATADIR}/scripts %{buildroot}%{DATADIR}/certs %{buildroot}%{DATADIR}/sounds %{buildroot}%{DATADIR}/htdocs %{buildroot}%{DATADIR}/fonts %{buildroot}%{DATADIR}/grammar
%{__mkdir} -p %{buildroot}%{SYSCONFDIR}/tls %{buildroot}%{SYSCONFDIR}/autoload_configs %{buildroot}%{SYSCONFDIR}/dialplan/public %{buildroot}%{SYSCONFDIR}/sip_profiles/external
%{__mkdir} -p %{buildroot}%{LOGDIR}
%{__mkdir} -p %{buildroot}%{RUNDIR}
%{__mkdir} -p %{buildroot}%{STATEDIR}/db %{buildroot}%{STATEDIR}/cache %{buildroot}%{STATEDIR}/images %{buildroot}%{STATEDIR}/recordings %{buildroot}%{STATEDIR}/storage

#
# Exécutables
#
%{__install} -D -m 755 %{GITDIR}/.libs/freeswitch %{buildroot}%{BINDIR}/freeswitch
%{__install} -D -m 755 %{GITDIR}/fs_cli %{buildroot}%{BINDIR}/fs_cli
%{__install} -D -m 755 %{GITDIR}/fs_ivrd %{buildroot}%{BINDIR}/fs_ivrd
%{__install} -D -m 755 %{GITDIR}/fs_encode %{buildroot}%{BINDIR}/fs_encode
%{__install} -D -m 755 %{GITDIR}/tone2wav %{buildroot}%{BINDIR}/tone2wav
%{__install} -D -m 755 %{GITDIR}/scripts/gentls_cert %{buildroot}%{BINDIR}/gentsl_cert
#
# Librairies
#
%{__install} -D -m 755 %{GITDIR}/.libs/libfreeswitch.so.1.0.0 %{buildroot}%{LIBDIR}/libfreeswitch.so.1.0.0
%{__cp} -P %{GITDIR}/.libs/libfreeswitch.so.1 %{buildroot}%{LIBDIR}/libfreeswitch.so.1
%{__cp} -P %{GITDIR}/.libs/libfreeswitch.so %{buildroot}%{LIBDIR}/libfreeswitch.so

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

#
# Config minimale
#

%{__install} -m 640 %{GITDIR}/conf/minimal/autoload_configs/acl.conf.xml 		%{buildroot}%{SYSCONFDIR}/autoload_configs/acl.conf.xml
%{__install} -m 640 %{GITDIR}/conf/minimal/autoload_configs/cdr_csv.conf.xml 	%{buildroot}%{SYSCONFDIR}/autoload_configs/cdr_csv.conf.xml
%{__install} -m 640 %{GITDIR}/conf/minimal/autoload_configs/conference.conf.xml %{buildroot}%{SYSCONFDIR}/autoload_configs/conference.conf.xml
%{__install} -m 640 %{GITDIR}/conf/minimal/autoload_configs/console.conf.xml 	%{buildroot}%{SYSCONFDIR}/autoload_configs/console.conf.xml
%{__install} -m 640 %{GITDIR}/conf/minimal/autoload_configs/db.conf.xml 		%{buildroot}%{SYSCONFDIR}/autoload_configs/db.conf.xml
%{__install} -m 640 %{GITDIR}/conf/minimal/autoload_configs/event_socket.conf.xml %{buildroot}%{SYSCONFDIR}/autoload_configs/event_socket.conf.xml
%{__install} -m 640 %{GITDIR}/conf/minimal/autoload_configs/logfile.conf.xml 	%{buildroot}%{SYSCONFDIR}/autoload_configs/logfile.conf.xml
%{__install} -m 640 %{GITDIR}/conf/minimal/autoload_configs/modules.conf.xml 	%{buildroot}%{SYSCONFDIR}/autoload_configs/modules.conf.xml
%{__install} -m 640 %{GITDIR}/conf/minimal/autoload_configs/sofia.conf.xml 		%{buildroot}%{SYSCONFDIR}/autoload_configs/sofia.conf.xml
%{__install} -m 640 %{GITDIR}/conf/minimal/autoload_configs/switch.conf.xml 	%{buildroot}%{SYSCONFDIR}/autoload_configs/switch.conf.xml
%{__install} -m 640 %{GITDIR}/conf/minimal/autoload_configs/xml_rpc.conf.xml 	%{buildroot}%{SYSCONFDIR}/autoload_configs/xml_rpc.conf.xml
%{__install} -m 640 %{GITDIR}/conf/minimal/autoload_configs/timezones.conf.xml 	%{buildroot}%{SYSCONFDIR}/autoload_configs/timezones.conf.xml
%{__install} -m 640 %{GITDIR}/conf/minimal/dialplan/default.xml 				%{buildroot}%{SYSCONFDIR}/dialplan/default.xml
%{__install} -m 640 %{GITDIR}/conf/minimal/dialplan/public.xml 					%{buildroot}%{SYSCONFDIR}/dialplan/public.xml
%{__install} -m 640 %{GITDIR}/conf/minimal/dialplan/public/00_stub.xml 			%{buildroot}%{SYSCONFDIR}/dialplan/public/00_stub.xml
%{__install} -m 640 %{GITDIR}/conf/minimal/freeswitch.xml 						%{buildroot}%{SYSCONFDIR}/freeswitch.xml
%{__install} -m 640 %{GITDIR}/conf/minimal/sip_profiles/external.xml 			%{buildroot}%{SYSCONFDIR}/sip_profiles/
%{__install} -m 640 %{GITDIR}/conf/minimal/sip_profiles/external/stub.xml 		%{buildroot}%{SYSCONFDIR}/sip_profiles/external/stub.xml
%{__install} -m 640 %{GITDIR}/conf/minimal/sip_profiles/internal.xml 			%{buildroot}%{SYSCONFDIR}/sip_profiles/internal.xml
%{__install} -m 640 %{GITDIR}/conf/minimal/vars.xml 							%{buildroot}%{SYSCONFDIR}/vars.xml

%files config-minimal

%config(noreplace) %attr(0640, freeswitch, daemon) %{SYSCONFDIR}/autoload_configs/acl.conf.xml
%config(noreplace) %attr(0640, freeswitch, daemon) %{SYSCONFDIR}/autoload_configs/cdr_csv.conf.xml
%config(noreplace) %attr(0640, freeswitch, daemon) %{SYSCONFDIR}/autoload_configs/conference.conf.xml
%config(noreplace) %attr(0640, freeswitch, daemon) %{SYSCONFDIR}/autoload_configs/console.conf.xml
%config(noreplace) %attr(0640, freeswitch, daemon) %{SYSCONFDIR}/autoload_configs/db.conf.xml
%config(noreplace) %attr(0640, freeswitch, daemon) %{SYSCONFDIR}/autoload_configs/event_socket.conf.xml
%config(noreplace) %attr(0640, freeswitch, daemon) %{SYSCONFDIR}/autoload_configs/logfile.conf.xml
%config(noreplace) %attr(0640, freeswitch, daemon) %{SYSCONFDIR}/autoload_configs/modules.conf.xml
%config(noreplace) %attr(0640, freeswitch, daemon) %{SYSCONFDIR}/autoload_configs/sofia.conf.xml
%config(noreplace) %attr(0640, freeswitch, daemon) %{SYSCONFDIR}/autoload_configs/switch.conf.xml
%config(noreplace) %attr(0640, freeswitch, daemon) %{SYSCONFDIR}/autoload_configs/xml_rpc.conf.xml
%config(noreplace) %attr(0640, freeswitch, daemon) %{SYSCONFDIR}/autoload_configs/timezones.conf.xml
%config(noreplace) %attr(0640, freeswitch, daemon) %{SYSCONFDIR}/dialplan/default.xml
%config(noreplace) %attr(0640, freeswitch, daemon) %{SYSCONFDIR}/dialplan/public.xml
%config(noreplace) %attr(0640, freeswitch, daemon) %{SYSCONFDIR}/dialplan/public/00_stub.xml
%config(noreplace) %attr(0640, freeswitch, daemon) %{SYSCONFDIR}/freeswitch.xml
%config(noreplace) %attr(0640, freeswitch, daemon) %{SYSCONFDIR}/sip_profiles/external.xml
%config(noreplace) %attr(0640, freeswitch, daemon) %{SYSCONFDIR}/sip_profiles/external/stub.xml
%config(noreplace) %attr(0640, freeswitch, daemon) %{SYSCONFDIR}/sip_profiles/internal.xml
%config(noreplace) %attr(0640, freeswitch, daemon) %{SYSCONFDIR}/vars.xml


%pre 
if ! /usr/bin/id freeswitch &>/dev/null; then
       /usr/sbin/useradd -r -g daemon -s /bin/false -c "The FreeSWITCH Open Source Voice Platform" -d %{STATEDIR} freeswitch || \
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
%{LIBDIR}/libfreeswitch.so.1.0.0
%{LIBDIR}/libfreeswitch.so.1
%{LIBDIR}/libfreeswitch.so

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

