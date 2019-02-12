Name:		memtester
Version:	4.3.0
Release:	13%{?dist}
Summary:	Utility to test for faulty memory subsystem

Group:		System Environment/Base
License:	GPLv2
URL:		http://pyropus.ca/software/memtester/
Source0:	http://pyropus.ca/software/memtester/old-versions/%{name}-%{version}.tar.gz
Patch0:		memtester-4.0.8-debuginfo.patch

BuildRequires:  gcc
BuildRequires:	dos2unix
#Requires:	

%description
memtester is a utility for testing the memory subsystem in a computer to
determine if it is faulty.



%prep
%setup -q
%patch0 -p1 -b .debuginfo


%build
make %{?_smp_mflags} -e OPT="%{optflags}"


%install
rm -rf $RPM_BUILD_ROOT
mv README README.iso88591
iconv -o README -f iso88591 -t utf8 README.iso88591
touch -r README.iso88591 README
rm -f README.iso88591
dos2unix -k BUGS
make -e INSTALLPATH=$RPM_BUILD_ROOT%{_prefix} install
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
#fix location of manual
mv $RPM_BUILD_ROOT%{_prefix}/man/man8/memtester.8.gz $RPM_BUILD_ROOT%{_mandir}/man8



%files
%doc BUGS CHANGELOG COPYING README README.tests
%{_bindir}/memtester
%{_mandir}/man8/memtester.8.gz



%changelog
* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 4.3.0-13
- Rebuild with fixed binutils

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Oct 14 2012 Lucian Langa <cooly@gnome.eu.org> - 4.3.0-1
- new upstream release

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 31 2011 Lucian Langa <cooly@gnome.eu.org> - 4.2.2-1
- new upstream release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 30 2010 Lucian Langa <cooly@gnome.eu.org> - 4.2.1-1
- new upstream release

* Thu Aug 12 2010 Lucian Langa <cooly@gnome.eu.org> - 4.2.0-1
- new upstream release

* Mon Mar 01 2010 Lucian Langa <cooly@gnome.eu.org> - 4.1.3-1
- new upstream release

* Sat Aug 01 2009 Lucian Langa <cooly@gnome.eu.org> - 4.1.2-1
- new upstream release

* Sun Jul 26 2009 Lucian Langa <cooly@gnome.eu.org> - 4.1.1-1
- misc cleanups
- new upstream release

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 29 2008 Lucian Langa <cooly@gnome.eu.org> - 4.0.8-2
- preserve timestamps
- fix patch

* Sat Sep 27 2008 Lucian Langa <cooly@gnome.eu.org> - 4.0.8-1
- initial specfile


