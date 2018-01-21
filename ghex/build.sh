#!/bin/bash

set -eux

env

name=ghex
short_version=3.18
patch_version=3
version=${short_version}.${patch_version}
filename=ghex-$version.tar.xz
url=http://ftp.gnome.org/pub/GNOME/sources/ghex/$short_version/$filename
checksum=c67450f86f9c09c20768f1af36c11a66faf460ea00fbba628a9089a6804808d3

outdir=$1
# equals $PWD
specdir=$2
specfile=$(ls *.spec)


curl -L -O $url
echo "$checksum  $filename" | sha256sum -c -

rpmbuild \
 --define "_sourcedir $PWD" \
 --define "_specdir $PWD" \
 --define "_rpmdir $outdir" \
 --define "_srcrpmdir $outdir" \
 -bs $specfile
