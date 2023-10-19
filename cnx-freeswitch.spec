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
Requires:	net-snmp

%define BINDIR 		/usr/bin
%define LIBDIR		/usr/lib64
%define MODINSTDIR 	/usr/lib64/freeswitch/mod
%define DATADIR 	/usr/share/freeswitch
%define SYSCONFDIR 	/etc/freeswitch
%define GITDIR		%{_topdir}/..

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
mkdir -p $RPM_BUILD_ROOT%{BINDIR}
mkdir -p $RPM_BUILD_ROOT%{MODINSTDIR}
mkdir -p $RPM_BUILD_ROOT%{DATADIR}
mkdir -p $RPM_BUILD_ROOT%{SYSCONFDIR}
install -m 664 %{GITDIR}/src/mod/loggers/mod_console/.libs/mod_console.so -t $RPM_BUILD_ROOT%{MODINSTDIR}
install -m 664 %{GITDIR}/src/mod/loggers/mod_logfile/.libs/mod_logfile.so -t $RPM_BUILD_ROOT%{MODINSTDIR}
install -m 664 %{GITDIR}/src/mod/loggers/mod_graylog2/.libs/mod_graylog2.so -t $RPM_BUILD_ROOT%{MODINSTDIR}

install -m 664 %{GITDIR}/src/mod/event_handlers/mod_cdr_csv/.libs/mod_cdr_csv.so -t $RPM_BUILD_ROOT%{MODINSTDIR}
install -m 664 %{GITDIR}/src/mod/event_handlers/mod_event_socket/.libs/mod_event_socket.so -t $RPM_BUILD_ROOT%{MODINSTDIR}
install -m 664 %{GITDIR}/src/mod/event_handlers/mod_snmp/.libs/mod_snmp.so -t $RPM_BUILD_ROOT%{MODINSTDIR}

install -m 664 %{GITDIR}/src/mod/endpoints/mod_sofia/.libs/mod_sofia.so -t $RPM_BUILD_ROOT%{MODINSTDIR}

install -m 664 %{GITDIR}/src/mod/applications/mod_dptools/.libs/mod_dptools.so -t $RPM_BUILD_ROOT%{MODINSTDIR}
install -m 664 %{GITDIR}/src/mod/applications/mod_commands/.libs/mod_commands.so -t $RPM_BUILD_ROOT%{MODINSTDIR}
install -m 664 %{GITDIR}/src/mod/applications/mod_distributor/.libs/mod_distributor.so -t $RPM_BUILD_ROOT%{MODINSTDIR}
install -m 664 %{GITDIR}/src/mod/applications/mod_translate/.libs/mod_translate.so -t $RPM_BUILD_ROOT%{MODINSTDIR}
install -m 664 %{GITDIR}/src/mod/applications/mod_hash/.libs/mod_hash.so -t $RPM_BUILD_ROOT%{MODINSTDIR}

install -m 664 %{GITDIR}/src/mod/dialplans/mod_dialplan_xml/.libs/mod_dialplan_xml.so -t $RPM_BUILD_ROOT%{MODINSTDIR}

install -m 664 %{GITDIR}/src/mod/languages/mod_lua/.libs/mod_lua.so -t $RPM_BUILD_ROOT%{MODINSTDIR}


%pre 
if ! /usr/bin/id freeswitch &>/dev/null; then
       /usr/sbin/useradd -r -g daemon -s /bin/false -c "The FreeSWITCH Open Source Voice Platform" -d %{LOCALSTATEDIR} freeswitch || \
                %logmsg "Unexpected error adding user \"freeswitch\". Aborting installation."
fi

%post
%{?run_ldconfig:%run_ldconfig}

chown freeswitch:daemon /var/log/freeswitch /var/run/freeswitch

%files
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

