Summary: A library that performs asynchronous DNS operations
Name: c-ares
Version: 1.13.0
Release: 9%{?dist}.1
License: MIT
Group: System Environment/Libraries
URL: http://c-ares.haxx.se/
Source0: http://c-ares.haxx.se/download/%{name}-%{version}.tar.gz
# The license can be obtained at http://c-ares.haxx.se/license.html
Source1: LICENSE
Patch0: 0001-Use-RPM-compiler-options.patch
Patch1: 0002-fix-CVE-2021-3672.patch
Patch2: 0003-Add-str-len-check-in-config_sortlist-to-avoid-stack-.patch
Patch3: 0004-Merge-pull-request-from-GHSA-9g78-jv2r-p7vc.patch
Patch4: 0005-avoid-read-heap-buffer-overflow-332.patch
Patch5: 0006-Merge-pull-request-from-GHSA-x6mf-cxr9-8q6v.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool

%description
c-ares is a C library that performs DNS requests and name resolves 
asynchronously. c-ares is a fork of the library named 'ares', written 
by Greg Hudson at MIT.

%package devel
Summary: Development files for c-ares
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the header files and libraries needed to
compile applications or shared objects that use c-ares.

%prep
%setup -q
%patch0 -p1 -b .optflags
%patch1 -p1 -b .dns
%patch2 -p1 -b .sortlist
%patch3 -p1 -b .udp
%patch4 -p1 -b .buffer
%patch5 -p1 -b .underwrite

cp %{SOURCE1} .
f=CHANGES ; iconv -f iso-8859-1 -t utf-8 $f -o $f.utf8 ; mv $f.utf8 $f

%build
autoreconf -if
%configure --enable-shared --disable-static \
           --disable-dependency-tracking
%{__make} %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/libcares.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc README.cares CHANGES NEWS LICENSE
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/ares.h
%{_includedir}/ares_build.h
%{_includedir}/ares_dns.h
%{_includedir}/ares_rules.h
%{_includedir}/ares_version.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libcares.pc
%{_mandir}/man3/ares_*

%changelog
* Fri Oct  6 2023 Alexey Tikhonov <atikhono@redhat.com> - 1.13.0-9.1
- Resolves: RHEL-11931 - Buffer Underwrite in ares_inet_net_pton() [rhel-8.9.0.z]

* Mon Sep 11 2023 Alexey Tikhonov <atikhono@redhat.com> - 1.13.0-9
- Resolves: rhbz#2238293 - CVE-2020-22217 c-ares: read-heap-buffer-overflow in ares_parse_soa_reply [rhel-8] [rhel-8.9.0.z]

* Mon May 29 2023 Alexey Tikhonov <atikhono@redhat.com> - 1.13.0-8
- Resolves: rhbz#2209517 - CVE-2023-32067 c-ares: 0-byte UDP payload Denial of Service [rhel-8.9.0]

* Fri May 12 2023 Alexey Tikhonov <atikhono@redhat.com> - 1.13.0-7
- Resolves: rhbz#2170867 - c-ares: buffer overflow in config_sortlist() due to missing string length check [rhel-8]

* Fri Oct 15 2021 Alexey Tikhonov <atikhono@redhat.com> - 1.13.0-6
- Resolves: rhbz#1989425 - CVE-2021-3672 c-ares: missing input validation of host names may lead to Domain Hijacking [rhel-8]

* Mon Aug 13 2018 Jakub Hrozek <jhrozek@redhat.com> - 1.13.0-5
- Drop an unused patch

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 20 2017 Jakub Hrozek <jhrozek@redhat.com> - 1.13.0-1
- update to 1.13.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 29 2016 Tom Callaway <spot@fedoraproject.org> - 1.12.0-1
- update to 1.12.0

* Fri Feb 19 2016 Jakub Hrozek <jhrozek@redhat.com> - 1.11.0
- New upstream version 1.11.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.1-1
- New upstream release 1.10
- Obsolete upstreamed patches
- Amend the multilib patch, there's no need to patch configure since we
  are running autoreconf anyways
- https://raw.github.com/bagder/c-ares/cares-1_10_0/RELEASE-NOTES

* Thu Apr 11 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.1-6
- Apply an upstream patch to override AC_CONFIG_MACRO_DIR only conditionally

* Thu Apr 11 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.1-5
- Apply a patch by Stephen Gallagher to patch autoconf, not configure to
  allow optflags to be passed in by build environment
- Run autoreconf before configure
- git rm obsolete patches
- Apply upstream patch to stop overriding AC_CONFIG_MACRO_DIR

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 8 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.1-3
- Include URL to the license text

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Tom Callaway <spot@fedoraproject.org> - 1.9.1-1
- update to 1.9.1

* Sat Apr 28 2012 Tom Callaway <spot@fedoraproject.org> - 1.8.0-1
- update to 1.8.0
- fix multilib patch (thanks to Paul Howarth)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 17 2011 Jakub Hrozek <jhrozek@redhat.com> - 1.7.5-1
- New upstream release 1.7.5
- Obsoletes patch #2
- Rebase patch #1 (optflags) to match the 1.7.5 code
- Fixed Source0 URL to point at the upstream tarball

* Mon Apr 11 2011 Jakub Hrozek <jhrozek@redhat.com> - 1.7.4-3
- Apply upstream patch to fix rhbz#695424

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 10 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.7.4-1
- update to 1.7.4

* Wed Aug 25 2010 Jakub Hrozek <jhrozek@redhat.com> - 1.7.3-3
- Actually apply the patches

* Wed Aug 25 2010 Jakub Hrozek <jhrozek@redhat.com> - 1.7.3-2
- apply couple of patches from upstream

* Tue Jun 15 2010 Jakub Hrozek <jhrozek@redhat.com> - 1.7.3-1
- Upgrade to new upstream release 1.7.3 (obsoletes search/domain patch)
- Fix conflict of -devel packages on multilib architectures (#602880)

* Thu Jun 3 2010 Jakub Hrozek <jhrozek@redhat.com> - 1.7.1-2
- Use last instance of search/domain, not the first one (#597286)

* Tue Mar 23 2010 Jakub Hrozek <jhrozek@redhat.com> - 1.7.1-1
- update to 1.7.1 which contains the IPv6 nameserver patch

* Sun Mar  7 2010 Jakub Hrozek <jhrozek@redhat.com> - 1.7.0-3
- Change IPv6 nameserver patch according to upstream changes
  (upstream revisions 1199,1201,1202)

* Wed Mar  3 2010 Jakub Hrozek <jhrozek@redhat.com> - 1.7.0-2
- Add a patch to allow usage of IPv6 nameservers

* Tue Dec  1 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.7.0-1
- update to 1.7.0

* Sat Jul 25 2009 Ville Skyttä <ville.skytta at iki.fi> - 1.6.0-3
- Patch to make upstream build system honor our CFLAGS and friends.
- Don't bother building throwaway static libs.
- Disable autotools dependency tracking for cleaner build logs and possible
  slight build speedup.
- Convert docs to UTF-8.
- Update URLs.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6.0-1
- update to 1.6.0

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.5.3-1
- update to 1.5.3

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.5.1-2
- Autorebuild for GCC 4.3

* Tue Feb 19 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.1-1
- update to 1.5.1

* Thu Aug 23 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.4.0-2
- rebuild for ppc32

* Wed Jun 27 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.4.0-1
- bump to 1.4.0 (resolves bugzilla 243591)
- get rid of static library (.a)

* Wed Jan 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.2-1
- bump to 1.3.2

* Mon Sep 11 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.1-2
- FC-6 bump

* Mon Jul 10 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.1-1
- bump to 1.3.1

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.0-2
- bump for FC-5 rebuild

* Sun Sep  4 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.0-1
- include LICENSE text
- bump to 1.3.0

* Tue May 31 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.1-4
- use dist tag to prevent EVR overlap

* Fri Apr 22 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.1-2
- fix license (MIT, not LGPL)
- get rid of libcares.la

* Fri Apr 22 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.1-1
- initial package creation

