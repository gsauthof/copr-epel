Name:		nemiver
Version:	0.9.6
Release:	8%{?dist}
Summary:	A GNOME C/C++ Debugger

Group:		Development/Debuggers
License:	GPLv2+
URL:		http://projects.gnome.org/nemiver

Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.9/%{name}-%{version}.tar.xz
# Backported from upstream
Patch0:		0001-Fix-compiliation-warnings-errors.patch
Patch1:		0001-Use-RefPtr-bool-operator-in-the-conditions.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

## The glibmm bits would normally be part of the dependency tree for
## gtksourceviewmm; but we're using GIO here (F9+) so we need to ensure that the
## the Glib/glibmm we're depending on also includes it (e.g., 2.16+)
##
## We specify the minimum version of gtkmm24 because we are now using
## the tooltip and treeview APIs of gtkmm 2.12.7.
BuildRequires:	boost-devel
BuildRequires:	boost-static
BuildRequires:	desktop-file-utils
BuildRequires:	gdb
BuildRequires:	gettext
#This is useful to get m4 macros from gsettings.m4, like GLIB_GSETTING
# Requiring glib2-devel >= 2.28 is equivalent to requiring the
# glib2-devel of Fedora 15.
BuildRequires:  glib2-devel >= 2.28
BuildRequires:	ghex-devel >= 3.10
BuildRequires:	glibmm24-devel >= 2.46
BuildRequires:	gtkmm30-devel >= 3.18
BuildRequires:	gdlmm-devel >= 3.2.1
BuildRequires:	yelp-tools >= 3.2.0
BuildRequires:	gtksourceviewmm3-devel >= 3.0.0
BuildRequires:	libgtop2-devel >= 2.14
BuildRequires:	libtool
BuildRequires:	perl(XML::Parser)
BuildRequires:	sqlite-devel >= 3.0
BuildRequires:	vte291-devel >= 0.41
BuildRequires:	intltool
BuildRequires:	libxml2-devel >= 2.6.22
BuildRequires:  gsettings-desktop-schemas-devel
BuildRequires:  dconf

Requires: gsettings-desktop-schemas

## Needs hicolor-icon-theme so that the parent %%_datadir/icons/hicolor
## and its subtree directories are properly owned.
Requires:	hicolor-icon-theme
Requires:	gdb
Provides: %{name}-devel = %{version}-%{release}
Provides: %{name}-headers = %{version}-%{release}

Obsoletes:	%{name}-devel < 0.5.4-1
Obsoletes:	%{name}-headers < 0.6.5-2

## Mostly taken from its site index... :]
%description
Nemiver is an ongoing effort to write a standalone graphical debugger that
integrates well in the GNOME desktop environment. It currently features a
backend which uses the well known GNU Debugger (gdb) to debug C/C++ programs.

The yelp package must be installed to make use of Nemiver's documentation.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure --disable-static --disable-schemas-install  --disable-scrollkeeper 
# Use system libtool to prevent build scripts from using RPATH hacks.
make %{?_smp_mflags} LIBTOOL=%{_bindir}/libtool


%install
rm -rf %{buildroot}
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}
desktop-file-install                                    \
	--dir %{buildroot}%{_datadir}/applications	\
	--remove-category=Application			\
	--delete-original				\
	%{buildroot}/%{_datadir}/applications/%{name}.desktop

# # Register as an application to be visible in the software center
# #
# # NOTE: It would be *awesome* if this file was maintained by the upstream
# # project, translated and installed into the right place during `make install`.
# #
# # See http://www.freedesktop.org/software/appstream/docs/ for more details.
# #
# mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
# cat > $RPM_BUILD_ROOT%{_datadir}/appdata/%{name}.appdata.xml <<EOF
# <?xml version="1.0" encoding="UTF-8"?>
# <!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
# <!--
# BugReportURL: https://bugzilla.gnome.org/show_bug.cgi?id=708754
# SentUpstream: 2014-09-22
# -->
# <application>
#   <id type="desktop">nemiver.desktop</id>
#   <metadata_license>CC0-1.0</metadata_license>
#   <description>
#     <p>
#       Nemiver is an on-going effort to write a standalone graphical debugger that
#       integrates well in the GNOME desktop environment.
#       It currently features a backend which uses the well known GNU Debugger gdb
#       to debug C / C++ programs.
#     </p>
#     <p>
#       We believe that Nemiver is mature and robust enough to just let you debug
#       your favorite C or C++ application in a pleasant way, as we use it daily
#       for our own debugging purposes.
#     </p>
#   </description>
#   <screenshots>
#     <screenshot type="default">https://projects.gnome.org/nemiver/images/nemiver-main-page.png</screenshot>
#   </screenshots>
#   <url type="homepage">https://projects.gnome.org/nemiver/</url>
#   <updatecontact>nemiver-list@gnome.org</updatecontact>
# </application>
# EOF

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
update-desktop-database -q
touch --no-create %{_datadir}/icons/hicolor ||:

%postun
/sbin/ldconfig
update-desktop-database -q
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING COPYRIGHT NEWS README TODO 
%exclude %{_includedir}/%{name}
%exclude %{_libdir}/%{name}/*.a
%exclude %{_libdir}/%{name}/*.la
%exclude %{_libdir}/%{name}/modules/*.a
%exclude %{_libdir}/%{name}/modules/*.la
%exclude %{_libdir}/%{name}/plugins/*/*.la
%exclude %{_libdir}/%{name}/plugins/*/*.a
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/glib-2.0/schemas/org.nemiver.gschema.xml
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}*.*
%{_datadir}/%{name}/
%{_datadir}/help/*
%{_mandir}/man?/%{name}.*

%changelog
* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 13 2017 Kalev Lember <klember@redhat.com> - 0.9.6-6
- Rebuilt for libgtop2 soname bump

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 0.9.6-3
- Rebuilt for Boost 1.60

* Thu Sep 24 2015 Dodji Seketeli <dodji@seketeli.org> - 0.9.6-2
- Re-build with vte291, version 0.41
- Use the appdata file from the tarball

* Wed Sep 23 2015 Dodji Seketeli <dodji@redhat.com> - 0.9.6-1
- Update to upstream 0.9.6 version
- There is no HighContrast icon distributed anymore
- Adjust files for the new nemiver-symbolic.svg icon
- Bump requirement of gtkmm-30-devel to 3.18

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 0.9.5-12
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-11
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.9.5-10
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.9.5-8
- Rebuilt for GCC 5 C++11 ABI change

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 0.9.5-7
- Add an AppData file for the software center

* Mon Jan 26 2015 Petr Machata <pmachata@redhat.com> - 0.9.5-6
- Rebuild for boost 1.57.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 0.9.5-3
- Rebuild for boost 1.55.0

* Thu May 01 2014 Kalev Lember <kalevlember@gmail.com> - 0.9.5-2
- Rebuilt for libgtop2 soname bump

* Sun Dec  8 2013 Dodji Seketeli <dodji@seketeli.org> - 0.9.5-1
- Update for upstream release 0.9.5
  - Package new high contrast icons: %%{_datadir}/icons/HighContrast/*/apps/nemiver.*
  - Bug fixed -- numbers are bug numbers in upstream bugzilla:
    - 680376 - Local variables in nested scopes don't get refreshed automatically
    - 697992 - fail to restart a program wrapped in libtool shell script
    - 687609 - nemiver should install a highcontrast app icon
    - 561239 - UI to select and copy text from source editor
    - 700248 - Support breakpoints with multiple locations
    - 701480 - Correctly flag a breakpoint pending state
    - 698371 - Run command is available even after detaching
    - Fix "restart loosing inferior argument" bug
    - Don't 'run' the inferior on startup when it has no 'main'
    - Continue execution upon (re)start with breakpoints set
    - Handle deleting all sub-breakpoints at once
    - Support modified-breakpoint async output from GDB
    - Allow disassembling from address 0
    - Fix continue action label
    - Fix menu typo

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 0.9.4-6
- Rebuild for boost 1.54.0

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 0.9.4-5
- Rebuilt for gtksourceview3 soname bump

* Wed Mar 20 2013 Kalev Lember <kalevlember@gmail.com> - 0.9.4-4
- Rebuilt for gdlmm soname bump

* Wed Mar  6 2013 Matthias Clasen <mclasen@redhat.com> - 0.9.4-3
- Drop the vendor prefix from the desktop file name

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 13 2013 Dodji Seketeli <dodji@seketeli.org> - 0.9.4-1
- Update to upstream 0.9.4 release
  - Bug fixed (upstream bugzilla):
    - 689338 - Sometimes current frame is wrongly set
    - 689458 - Crash when copying variable value
    - 684046 - nemiver.desktop conformance fix
    - 670439 - Nemiver doesn't handle well multi-threaded apps
    - 689575 - Freeze when local variable values are refreshed
    - Fix well form-ness of gl.po
    - Fix help browser launching
    - Fix French translation markup
    - Ensure workbench body is shown
    - Added a README.release.txt file
    - Various code cleanups
    - Added search keywords to .desktop file
    - Use new documentation infrastructure based on yelp-tools
  - Updated translations: French, Danish, British, Catalan,
    Traditional Chinese, Simplified Chinese, Spanish, Greek,
    Portuguese, Galician, Hungarian, Brazilian Portuguese, Uyghur,
    Norwegian bokmål, Czech, German, Slovenian, Japanese, Polish,
    Hindi, Slovak, Latvian, Korean, Russian
- Drop gnome-doc-utils build dependency
- Add new yelp-tools build dependency
- Drop %%{datadir}/gnome/help/* and %%{datadir}/omf/%%{name}.  Use
  %%{datadir}/help/* now.

* Thu Sep 27 2012 Kalev Lember <kalevlember@gmail.com> - 0.9.3-3
- Rebuilt for libgdl soname bump

* Wed Sep 19 2012 Kalev Lember <kalevlember@gmail.com> - 0.9.3-2
- Silence glib-compile-schemas scriplets

* Sun Aug 12 2012 Dodji Seketeli <dodji@seketeli.org> - 0.9.3-1
- Update to upstream 0.9.3 release
  Bugs fixed (upstream bugzilla):
  - #680934 - Fix --enable-debuggeronly
  - don't hardcode path to false (BSD)
  - build: unbreak on OpenBSD by including iostream (BSD)
  - Terminal portability fixes for BSDs
  - Code cleanups
  New features:
  - #542503 - Initial support for monitoring expressions
  - 665274 - Support --just-load command line
  - Save and restore tty attributes
  Many translation updates

* Mon Jul 23 2012 Kalev Lember <kalevlember@gmail.com> - 0.9.2-4
- Rebuilt for libgdl 3.5.4 soname bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 23 2012 Kalev Lember <kalevlember@gmail.com> - 0.9.2-2
- Rebuilt for libgdl 3.4.2 soname bump

* Wed Mar 28 2012 Richard Hughes <hughsient@gmail.com> - 0.9.2-1
- Update to 0.9.2

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-3
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 20 2011  <dodji@seketeli.org> - 0.9.1-1
- Update to upstream release 0.9.1

* Tue Sep 27 2011  <dodji@redhat.com> - 0.9.0-2
- Rebuild to link against gdlmm 3.1.90 and activate the Dynamic View
- Update the link to the upstream tarball
- Remove unnecessary --enable-gsettings from configure command line

* Fri Sep  9 2011  <dodji@seketeli.org> - 0.9.0-1
- Update upstream release 0.9.0
- Update ghex-devel dependency to 2.90
- Move to gtksourceviewmm3-devel >= 3.0.0 dep
- Move to vte3-devel >= 0.28.0

* Sat May  7 2011  <dodji@seketeli.org> - 0.8.2-1
- Update to upstream release 0.8.2
- Enable GSettings.  Remove usage of GConf.  Bump glibmm24 requirement
  to 2.25 (to support gsettings) Add build requirements for
  gsettings-desktop-schemas-devel, dconf and glib2-devel >= 2.28.
  Remove GConf schema from package.  Add gsettings schema.
- Remove use of scrollkeeper at long last.
- Cleanup and update scriplet snippets.
- Bump gtkmm24 build requirement to 2.20 as per what upstream
  requires.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan  9 2011  <dodji@seketeli.org> - 0.8.1-1
- Update to upstream release 0.8.1
- Change Source0 to point to the .gz tarball instead of the .bz

* Tue Oct 19 2010  <dodji@seketeli.org> - 0.8.0-1
- Update upstream release 0.8.0
- Drop patches 0001-Fix-build-with-gcc-4.5.patch and
  0001-More-GCC-4.5-fixes-611588.patch as they are now released upstream
- Remove libglademm and libgnome dependencies are they got removed upstream
- Add GConf2 dependency

* Wed Sep 29 2010 jkeating - 0.7.3-3
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010  <dodji@seketeli.org> - 0.7.3-2
- Fix source0 URL.
- 0001-Fix-build-with-gcc-4.5.patch and 0001-More-GCC-4.5-fixes-611588.patch:
  fix build breakage with GCC 4.5

* Sun Dec 06 2009 Dodji Seketeli <dodji@redhat.com> - 0.7.3-1
- Update to new upstream release (0.7.3)

* Sat Sep 12 2009 Dodji Seketeli <dodji@redhat.com> - 0.7.2-1
- Update to new upstream release (0.7.2)

* Sat Aug 01 2009 Dodji Seketeli <dodji@redhat.com> - 0.7.1-1
- Update to new upstream release (0.7.1)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 02 2009 Dodji Seketeli <dodji@redhat.com> - 0.7.0-2
- Fix typo (redhat.org -> redhat.com)

* Thu Jul 02 2009 Dodji Seketeli <dodji@redhat.com> - 0.7.0-1
- Update to new upstream release (0.7.0)

* Sat May 02 2009 Dodji Seketeli <dodji@redhat.com> - 0.6.7-1
- Update to new upstream release (0.6.7)

* Fri Apr 03 2009 Dodji Seketeli <dodji@redhat.com> - 0.6.6-1
- Update to new upstream release (0.6.6)
- Drop patch http://bugzilla.gnome.org/show_bug.cgi?id=574915
  as included in upstream release.

* Fri Mar 13 2009 Dodji Seketeli <dodji@redhat.com> - 0.6.5-2
- Add upstream patch http://bugzilla.gnome.org/show_bug.cgi?id=574915
  Fixes a "spinner not found" bug.
- Add boost-static in BuildRequires (required for nemiver tests)
- Remove more *.a files
- Do not ship nemiver-headers package
  Upstream can't garantee API/ABI stability yet and
  nobody uses this package yet anyway

* Sun Mar 01 2009 Dodji Seketeli <dodji@redhat.com> - 0.6.5-1
- Update to new upstream release (0.6.5)
- Drop include-stdint.patch as pushed upstream
- BuildRequire intltool

* Tue Feb 24 2009 Dodji Seketeli <dodji@redhat.com> - 0.6.4-2
- Rebuild against ghex 2.2.4. This should fix #571099
- Patch Nemiver to make it compile with gcc 4.3.3

* Sat Jan 17 2009 Denis Leroy <denis@poolshark.com> - 0.6.4-1
- Update to upstream 0.6.4
- Now build against gtksourceviewmm 2.2.0

* Sun Sep 28 2008 Peter Gordon <peter@thecodergeek.com> - 0.6.3-1
- Update to new upstream release (0.6.3).
- Set the minimum required version of gtkmm-24 to 2.12.7; and update the
  Summary field to reflect the current state of upstream, as recommended by
  Dodji Seketeli.
- Resolves: #464413 (Nemiver 0.6.3 has been released upstream)

* Sat Sep 13 2008 Peter Gordon <peter@thecodergeek.com> - 0.6.2-1
- Update to new upstream release (0.6.2).

* Wed Aug  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.6.1-3
- bump to rebuild against old libgtksourceviewmm

* Tue Aug  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.6.1-2
- rebuild for new libgtksourceviewmm

* Thu Jul 31 2008 Peter Gordon <peter@thecodergeek.com> - 0.6.1-1
- Update to new upstream release (0.6.1).

* Sat Jul 19 2008 Peter Gordon <peter@thecodergeek.com> - 0.5.5-0.1.svn889
- Update to new upstream snapshot (SVN 889): increased performance when
  stepping in big applications like WebKit, ability to call arbitrary functions
  in the inferior process being debugged and support for conditional
  breakpoints, and loads of bug-fixes. Sweet!
- Fix typo in previous %%changelog entry.

* Fri Jun 27 2008 Peter Gordon <peter@thecodergeek.com> - 0.5.4-1
- Update to new upstream release (0.5.4)
- Rename -devel subpackage to -headers and adjust the %%description
  accordingly. (It no longer contains any shared library symlinks or pkgconfig
  data; and thus would not be multilib-friendly. We can't put it in the main
  package due to its additional *-devel dependencies. Finally, upstream has
  said that nothing should really be using the libnemivercommon API yet
  anyway.)
- Drop the libnemiver global library patch (fixed upstream)
  - make-libnemivercommon-global-lib.patch

* Mon May 26 2008 Peter Gordon <peter@thecodergeek.com> - 0.5.3-1
- Update to new upstream release (0.5.3)
- Add upstream bug reference for make-libnemivercommon-global-lib patch. 

* Fri Apr 11 2008 Peter Gordon <peter@thecodergeek.com> - 0.5.2-1
- Update to new upstream release (0.5.2)
- Add patch to keep the nemivercommon shared library in the global  %%_libdir,
  rather that in a private directory therein. This allows other sources to
  properly build against it without using nasty RPATH hacks, and also makes RPM
  correctly add same-arch dependencies from the devel subpackage to the main
  package via that unversioned binary symlink:
  + make-libnemivercommon-global-lib.patch    
- Alphabetize dependency list (aesthetic-only change)

* Sat Mar 22 2008 Peter Gordon <peter@thecodergeek.com> - 0.5.1-1
- Update to new upstream release (0.5.1)
- Drop upstreamed GCC 4.3 and build-fix patches:
  - gcc43.patch
  - multiple-a_key-params.patch

* Sun Mar 09 2008 Peter Gordon <peter@thecodergeek.com> - 0.5.0-1
- Update to new upstream release (0.5.0)
- Rebuild for GCC 4.3
- Drop upstreamed patches:
  - setbreakpoint-glade-filename.patch
  - pid_t-fix-build.patch
- Add patch to fix build errors with GCC 4.3 reduced headers:
  + gcc43.patch
- Add patch to fix multiple a_key function parameters:
  + multiple-a_key-params.patch

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.4.0-5
- Autorebuild for GCC 4.3

* Wed Jan 30 2008 Peter Gordon <peter@thecodergeek.com> - 0.4.0-4
- Add patch to fix missing setbreakpoint.glade file error (should be
  setbreakpointdialog.glade). Fixes bug 430971 (missing glade file).
  + setbreakpoint-glade-filename.patch

* Thu Jan 10 2008 Peter Gordon <peter@thecodergeek.com> - 0.4.0-3
- Make GConf scriplets quieter (bug 426801: "unclean" rpm transaction).
- Add upstream patch to fix compile errors with casting from unsigned int*
  to pid_t* due to libgtop API change:
  + pid_t-fix-build.patch

* Tue Aug 21 2007 Peter Gordon <peter@thecodergeek.com> - 0.4.0-2
- Rebuild with BuildID-enabled binutils.
- Update License tag (GPLv2+)

* Sun Jun 03 2007 Peter Gordon <peter@thecodergeek.com> - 0.4.0-1
- Update to new upstream release (0.4.0)

* Sat Feb 17 2007 Peter Gordon <peter@thecodergeek.com> - 0.3.0-6
- Remove chcon invocation entirely; as it is not needed.
- Don't install libtool archives (.la files) of the plugins.

* Tue Feb 13 2007 Peter Gordon <peter@thecodergeek.com> - 0.3.0-5
- chcon call should be in %%post, not %%install

* Mon Feb 12 2007 Peter Gordon <peter@thecodergeek.com> - 0.3.0-4
- Mark the libdbgperspectiveplugin.so plugin with a textrel_shlib_t context to
  workaround SELinux execmod denials.
- Hardcoded RPATHs are bad (especially when they are simply repeats of the
  standard LIBDIR stuff); so get rid of them in the supplied libtool with a
  couple of sed incantantions from the packaging guidelines.

* Wed Jan 24 2007 Peter Gordon <peter@thecodergeek.com> - 0.3.0-3
- Another fix from Michael Schwendt: Don't mark installed GConf schemas as
  %%config. 

* Tue Jan 23 2007 Peter Gordon <peter@thecodergeek.com> - 0.3.0-2
- Fix issues noted in review comments (Thanks to Michael Schwendt, #223943):
  (1) Add %%defattr line to the -devel subpackage %%files list.
  (2) Fix consistency of schemas listing by not using a glob in the
      %%files list, since they are separate in the scriplets' gconftool-2
      calls.
  (3) Add gettext and perl(XML::Parser) BuildRequires to fix mock building.
  (4) Add and explicitly version the Requires for the -devel subpackage due
      to various dependencies in the installed .pc file: libxml2-devel,
      glibmm24-devel, gnome-vfs2-devel. (glib2-devel is also needed, but that
      is pulled in as as dependency of glibmm24-devel.) 

* Mon Jan 22 2007 Peter Gordon <peter@thecodergeek.com> - 0.3.0-1
- Initial packaging for Fedora Extras.
