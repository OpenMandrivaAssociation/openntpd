Summary:	OpenNTPD - NTP Time Synchronization Client/Server 
Name:		openntpd
Version:	3.9p1
Release:	%mkrel 1
License:	BSD
Group:		System/Servers
URL:		http://www.openntpd.org
Source0:	ftp://ftp.openbsd.org/pub/OpenBSD/OpenNTPD/%{name}-%{version}.tar.bz2
Source1:	openntpd.init.bz2
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	openssl-devel
Conflicts:	ntp ntp-client
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
OpenNTPD is a FREE, easy to use implementation of the Network Time
Protocol. It provides the ability to sync the local clock to
remote NTP servers and can act as NTP server itself,
redistributing the local clock. 

%prep

%setup -q -n %{name}-%{version}

bzcat %{SOURCE1} > openntpd.init

%build

%configure2_5x \
    --disable-strip \
    --with-privsep-user=ntp \
    --with-privsep-path=%{_var}/empty \
    --with-ssl-dir=%{_prefix}
	      
%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_initrddir}

%makeinstall_std

install -m0755 openntpd.init %{buildroot}%{_initrddir}/ntpd

%pre
%_pre_useradd ntp %{_var}/empty /bin/false
/usr/sbin/usermod -d %{_var}/empty ntp

%post
%_post_service ntpd

%preun
%_preun_service ntpd

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CREDITS ChangeLog README*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ntpd.conf
%attr(0755,root,root) %{_initrddir}/ntpd
%attr(0755,root,root) %{_sbindir}/*
%attr(0644,root,root) %{_mandir}/man*/*

