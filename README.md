[![patchelf](https://copr.fedorainfracloud.org/coprs/gsauthof/epel/package/patchelf/status_image/last_build.png)][5]

This repository contains [Fedora][2] RPM source packages that aren't
available in the Fedora [EPEL repository][3], yet.

The source packages are built using the Fedora [COPR service][4]
and the resulting binary RPM packages are thus available in the
corresponding COPR repository:
https://copr.fedorainfracloud.org/coprs/gsauthof/epel/

2017, Georg Sauthoff <mail@gms.tf>

## Notable Packages

- [patchelf][1] - useful for displaying and setting link related
  attributes (like `RPATH`, `SONAME`, ...) of an
  executable/shared-library

## Design Decisions

The repository contains `.copr/Makefile` for building the SRPM
from the `.spec` inside the COPR-Environment. Choosing the
[makefile build method][7] over the default [rpkg one][8] has the following
reasons:

1. rpkg auto-downloads all referenced sources without
   verification - this has the obvious [security implications][6],
   especially for HTTP sources
2. rpkg doesn't properly substitute custom macros (Example: ghex
   spec file)

[1]: http://nixos.org/patchelf.html
[2]: https://en.wikipedia.org/wiki/Fedora_(operating_system)
[3]: https://fedoraproject.org/wiki/EPEL
[4]: https://copr.fedorainfracloud.org/coprs/
[5]: https://copr.fedorainfracloud.org/coprs/gsauthof/epel/
[6]: https://bugzilla.redhat.com/show_bug.cgi?id=1536846
[7]: https://docs.pagure.org/copr.copr/user_documentation.html#make-srpm
[8]: https://docs.pagure.org/copr.copr/user_documentation.html#scm
