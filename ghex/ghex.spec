# first two digits of version
# this fails with rpkg - imported version uses awk, unimportant optimization
%global release_version %(echo %{version} | cut -d. -f1-2)

Name:           ghex
Version:        3.18.3
Release:        4%{?dist}
Summary:        Binary editor for GNOME

License:        GPLv2+
URL:            http://ftp.gnome.org/pub/GNOME/sources/ghex/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/ghex/%{release_version}/ghex-%{version}.tar.xz

BuildRequires:  gtk3-devel
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  itstool

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
GHex can load raw data from binary files and display them for editing in the
traditional hex editor view. The display is split in two columns, with
hexadecimal values in one column and the ASCII representation in the other.
A useful tool for working with raw data.


%package        libs
Summary:        GtkHex library

%description    libs
The %{name}-libs package contains the shared GtkHex library.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
%make_install
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/ghex.desktop

%find_lang %{name}-3.0 --all-name --with-gnome

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

    touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}-3.0.lang
%license COPYING COPYING-DOCS
%doc AUTHORS NEWS README
%{_bindir}/*
%{_datadir}/appdata/ghex.appdata.xml
%{_datadir}/applications/ghex.desktop
%{_datadir}/GConf/gsettings/ghex.convert
%{_datadir}/glib-2.0/schemas/org.gnome.GHex.gschema.xml
%{_datadir}/icons/hicolor/*/apps/*

%files libs
%license COPYING
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 12 2016 Kalev Lember <klember@redhat.com> - 3.18.3-1
- Update to 3.18.3
- Don't set group tags
- Don't manually require ldconfig

* Wed Jun 22 2016 Richard Hughes <rhughes@redhat.com> - 3.18.2-1
- Update to 3.18.2

* Wed May 11 2016 Kalev Lember <klember@redhat.com> - 3.18.1-1
- Update to 3.18.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 02 2016 Adel Gadllah <adel.gadllah@gmail.com> - 3.18.0-2
- Use %%global instead of %%define

* Wed Sep 23 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Mon Aug 31 2015 Kalev Lember <klember@redhat.com> - 3.17.91-1
- Update to 3.17.91
- Include new symbolic icons
- Use make_install macro
- Mark license files with the license macro
- Tighten -devel package deps with the _isa macro
- Split out the shared library to -libs subpackage

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 30 2015 Richard Hughes <rhughes@redhat.com> - 3.10.1-4
- Use better AppData screenshots

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 14 2014 Kalev Lember <kalevlember@gmail.com> - 3.10.1-1
- Update to 3.10.1

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.92-1
- Update to 3.9.92
- Include the appdata file

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Richard Hughes <rhughes@redhat.com> - 3.8.1-1
- Update to 3.8.1

* Mon Mar 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Tue Feb 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.90-1
- Update to 3.7.90

* Tue Feb 05 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.3-1
- Update to 3.7.3
- Add icon cache scriptlets for HighContrast icons

* Wed Jan 16 2013 Richard Hughes <hughsient@gmail.com> - 3.7.2-1
- Update to 3.7.2

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.1-1
- Update to 3.7.1
- Adjust buildrequires for the new documentation infrastructure

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Richard Hughes <hughsient@gmail.com> - 3.6.0-1
- Update to 3.6.0

* Wed Sep 19 2012 Richard Hughes <hughsient@gmail.com> - 3.5.91-1
- Update to 3.5.91

* Thu Aug 30 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.2-1
- Update to 3.5.2

* Tue May 15 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.1-2
- Use %%find_lang for help files

* Sat May 05 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.1-1
- Update to 3.5.1

* Mon Mar 26 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.0-1
- Update to 3.4.0
- Include HACKING in docs

* Tue Mar 06 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.91-1
- Update to 3.3.91
- Dropped manual gtk3-devel dependency from ghex-devel subpackage; it's
  automatically picked up by rpm pkgconfig depgen.

* Tue Feb 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.90-1
- Update to 3.3.90

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Sat Sep 10 2011 Kalev Lember <kalevlember@gmail.com> - 2.90.2-1
- Update to 2.90.2
- Switch to gsettings
- Updated description
- Don't require scrollkeeper
- Make sure files aren't listed twice in %%files
- Added icon cache scriplets

* Sat Aug 13 2011 Adel Gadllah <adel.gadllah@gmail.com> - 2.90.0-1
- Update to 2.90.0 - now uses GTK3
- Remove now obsolete patch

* Tue Feb 09 2010 Dodji Seketeli <dodji@redhat.com> - 2.24.0-5
- Add patch to fix building with --no-as-needed as linker option.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Dodji Seketeli <dodji@redhat.org> 2.24.0-2
- Use %{?dist} in the Release number

* Fri Feb 20 2009 Dodji Seketeli <dodji@redhat.org> 2.24.0-1
- Update to 2.24.0
- Use system libtool
- Explicitely exclude static libraries
- Added BuildRequires intltools,libtool

* Fri Apr 11 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.22.0-1
- Update to 2.22.0 (no code changes, just a late release for Gnome 2.22 with
  updated translations)

* Sun Mar 02 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.21.92-1
- Update to 2.21.92

* Fri Feb 08 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.21.90-1
- Update to 2.21.90

* Sat Dec 29 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.21.4-1
- Update to 2.21.4
- Pass --disable-static to configure
- remove obsolete rm -rf RPM_BUILD_ROOT/var/scrollkeeper from install section

* Fri Dec 14 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20.1-1
- Update to 2.20.1

* Fri Sep 21 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20.0-1
- Update to 2.20.0

* Fri Aug 31 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.19.91-1
- Update to 2.19.91

* Fri Aug 17 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.19.90-1
- Update to 2.19.90

* Thu Aug 09 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.19.0-1
- Update to 2.19.0 and drop patches (stuff got fixed upstream)
- use make isntall instread of %%makeinstall

* Fri Aug 03 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info>
- Update License field due to the "Licensing guidelines changes"

* Sun May 20 2007 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.8.2-5
- Update project URL (#240646)

* Tue Aug 29 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.8.2-4
- Add BR perl-XML-Parser

* Tue Aug 29 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.8.2-3
- Rebuild for devel

* Wed Aug 09 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> 2.8.2-2
- apply ghex-search-crash.patch from b.g.o #339055 -- fixes #175957 

* Sat Jul 15 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> 2.8.2-1
- Update to 2.8.2
- Don't use the libtool worksaroung anymore
- Rename ghex-2.8.0-no-scrollkeeper.patch to
  ghex-no-scrollkeeper.patch and and update it

* Mon Feb 13 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info>
- Rebuild for Fedora Extras 5

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Jan 09 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.8.1-2
- Use make param LIBTOOL=/usr/bin/libtool instead autoreconf -- fixes x86_64
  build

* Mon Dec 27 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.8.1-1
- Update to 2.8.1
- recreate autoconf & co data during pre; fixes build issues on x86_64

* Tue Dec 21 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.8.0-3
- Ran into the incomplete-removal-of-epoch trap. Fixed that.

* Wed Nov 10 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.8.0-2
- Add patch to prevent scrollkeeper-updates during %%install.
- Drop Epoch.

* Sun Oct 17 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:2.8.0-0.fdr.1
- Updated to 2.8.0.

* Fri Jun  4 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:2.6.1-0.fdr.1
- Updated to 2.6.1.
- Reenabled parallel make (fixed upstream).

* Mon May 17 2004 Mark A. Fonnemann <m.fonneman.n@bc.edu> - 0:2.6.0-0.fdr.1
- Updated to 2.6.0.
- Divided Requires(post, postun) into Requires(post) and Requires(postun) (thanks, Michael Schwendt).
- Added gtk2-devel and gail-devel to build requirements (thanks, Michael).
- Changed {_datadir}/path to {_datadir}/path/* (thanks again, Michael).

* Thu Oct 23 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:2.4.0.1-0.fdr.4
- Reverted previous change.
- Disabled parallell make.
- Added build req scrollkeeper.

* Sat Oct 11 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:2.4.0.1-0.fdr.3
- Remove sr@Latn locale from desktop file if old desktop-file-install.

* Thu Oct  9 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:2.4.0.1-0.fdr.2
- Post req GConf2.
- Split out devel package.
- Added URL.

* Wed Sep 24 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:2.4.0.1-0.fdr.1
- Initial RPM release.
