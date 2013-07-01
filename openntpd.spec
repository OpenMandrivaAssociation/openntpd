Summary:	- NTP Time Synchronization Client/Server 
Name:		openntpd
Version:	3.9p1
Release:	%mkrel 8
License:	BSD
Group:		System/Servers
URL:		http://www.openntpd.org
Source0:	ftp://ftp.openbsd.org/pub/OpenBSD/OpenNTPD/%{name}-%{version}.tar.bz2
Source1:	openntpd.init
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
OpenNTPD is a FREE, easy to use implementation of the Network Time
Protocol. It provides the ability to sync the local clock to
remote NTP servers and can act as NTP server itself,
redistributing the local clock. 

%prep

%setup -q -n %{name}-%{version}

cp %{SOURCE1} openntpd.init

%build

%configure2_5x \
    --disable-strip \
    --with-privsep-user=ntp \
    --with-privsep-path=%{_var}/empty \
    --with-ssl-dir=%{_prefix}
	      
%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_initrddir}

%makeinstall_std

mv openntpd.init %{buildroot}%{_initrddir}/ntpd

%pre
%_pre_useradd ntp %{_var}/empty /bin/false
/usr/sbin/usermod -d %{_var}/empty ntp

%post
%_post_service ntpd

%preun
%_preun_service ntpd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CREDITS ChangeLog README*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ntpd.conf
%attr(0755,root,root) %{_initrddir}/ntpd
%attr(0755,root,root) %{_sbindir}/*
%attr(0644,root,root) %{_mandir}/man*/*


%changelog
* Mon Oct 17 2011 Leonardo Coelho <leonardoc@mandriva.com> 3.9p1-8mdv2012.0
+ Revision: 704979
- fix the copy from init file

* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 3.9p1-7mdv2011.0
+ Revision: 613540
- rebuild

* Fri Apr 16 2010 Funda Wang <fwang@mandriva.org> 3.9p1-6mdv2010.1
+ Revision: 535263
- rebuild

* Sun Apr 04 2010 Emmanuel Andry <eandry@mandriva.org> 3.9p1-5mdv2010.1
+ Revision: 531391
- fix conflict

* Sat Mar 20 2010 Emmanuel Andry <eandry@mandriva.org> 3.9p1-4mdv2010.1
+ Revision: 525507
- provides ntp (#58028)

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 3.9p1-3mdv2010.0
+ Revision: 430213
- rebuild

* Sun Jul 20 2008 Oden Eriksson <oeriksson@mandriva.com> 3.9p1-2mdv2009.0
+ Revision: 239100
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 3.9p1-1mdv2008.0
+ Revision: 39281
- fix deps
- fix #28330


* Wed May 17 2006 Oden Eriksson <oeriksson@mandriva.com> 3.9p1-1mdk
- 3.9p1

* Fri Mar 17 2006 Oden Eriksson <oeriksson@mandriva.com> 3.7p1-4mdk
- rebuilt against openssl-0.9.8a

* Tue Oct 18 2005 Emmanuel Blindauer <blindauer@mandriva.org> 3.7p1-3mdk
- Fix the startup script to add the -s option to force ajusting the time if
  the clock screw is greater than 180s

* Fri Aug 05 2005 Oden Eriksson <oeriksson@mandriva.com> 3.7p1-2mdk
- fix deps
- use the %%mkrel macro
- from Leonardo C. Filho <chiquitto@conectiva.com.br>:
  - use /var/empty as home directory instead of /var/empty/ntpd
    (it's better to have /var/empty empty)

* Mon Jun 06 2005 Oden Eriksson <oeriksson@mandriva.com> 3.7p1-1mdk
- 3.7p1 (Minor feature enhancements)

* Fri Jan 21 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 3.6.1p1-1mdk
- initial mandrake package, used parts of the provided spec file

