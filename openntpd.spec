Summary:	OpenNTPD - NTP Time Synchronization Client/Server 
Name:		openntpd
Version:	3.9p1
Release:	11
License:	BSD
Group:		System/Servers
URL:		http://www.openntpd.org
Source0:	ftp://ftp.openbsd.org/pub/OpenBSD/OpenNTPD/%{name}-%{version}.tar.bz2
Source1:	openntpd.service
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	openssl-devel
BuildRequires:	bison
BuildRequires:	byacc
BuildRequires:	groff-for-man
Conflicts:	ntp-client
Provides:	ntp

%description
OpenNTPD is a FREE, easy to use implementation of the Network Time
Protocol. It provides the ability to sync the local clock to
remote NTP servers and can act as NTP server itself,
redistributing the local clock. 

%prep

%setup -q -n %{name}-%{version}

cp %{SOURCE1} openntpd.service

%build

%configure2_5x \
    --disable-strip \
    --with-privsep-user=ntp \
    --with-privsep-path=%{_var}/empty \
    --with-ssl-dir=%{_prefix}
	      
%make

%install

install -d %{buildroot}%{_unitdir}

%makeinstall_std

mv openntpd.service %{buildroot}%{_unitdir}/%{name}.service

%pre
%_pre_useradd ntp %{_var}/empty /bin/false
/usr/sbin/usermod -d %{_var}/empty ntp

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%clean

%files
%doc CREDITS ChangeLog README*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ntpd.conf
%attr(0755,root,root) %{_unitdir}/*service
%attr(0755,root,root) %{_sbindir}/*
%attr(0644,root,root) %{_mandir}/man*/*
