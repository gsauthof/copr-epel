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

[1]: http://nixos.org/patchelf.html
[2]: https://en.wikipedia.org/wiki/Fedora_(operating_system)
[3]: https://fedoraproject.org/wiki/EPEL
[4]: https://copr.fedorainfracloud.org/coprs/
