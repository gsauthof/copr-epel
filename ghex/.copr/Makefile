
$(info $(shell env))

.PHONY: srpm

srpm: ghex-3.18.3.tar.xz
	rpmbuild \
 --define '%{_sourcedir} $(PWD)' \
 --define '%{_specdir} $(PWD)' \
 --define '_rpmdir $(outdir)' \
 --define '_srcrpmdir $(outdir)' \
 -bs $(spec)


ghex-3.18.3.tar.xz:
	curl -L -O http://ftp.gnome.org/pub/GNOME/sources/ghex/3.18/ghex-3.18.3.tar.xz
	echo 'c67450f86f9c09c20768f1af36c11a66faf460ea00fbba628a9089a6804808d3  ghex-3.18.3.tar.xz' | sha256sum -c -
