Name:           cnx-fsw-application-curl
Version:        1.10.12
Release:        2%{?dist}
Summary:        mod_curl up to date for FreeSWITCH 1.10.6

%define         company   connectics
%define         _package_ %{name}-%{version}

Group:          System/Libraries
License:        Proprietary
URL:            http://github.com/INTERACT-IV/cnx-api-proxy

%description
Provide FreeSWITCH dialplan access to CURL

%prep

%build

%install

# Copy files into their folder
mkdir -p $RPM_BUILD_ROOT/usr/lib64/freeswitch/mod
cp %{gitdir}/src/mod/applications/mod_curl/.libs/mod_curl.so $RPM_BUILD_ROOT/usr/lib64/freeswitch/mod

%post

%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/lib64/freeswitch/mod

%changelog

