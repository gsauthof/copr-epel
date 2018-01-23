#!/bin/bash

set -eux

env

name=nemiver
short_version=0.9
patch_version=6
version=${short_version}.${patch_version}
filename=$name-$version.tar.xz
url=http://ftp.gnome.org/pub/GNOME/sources/$name/$short_version/$filename
# checksum of the tar.xz included in the SRPM
#checksum=331ae34f2d18166199a7012dc777fbc5899e01f3e28909502957fcb6bef6963f
# great, the checksum doesn't match current available downloads ...
# ... a diff of both un-tarred versions doesn't show any differences, though
checksum=85ab8cf6c4f83262f441cb0952a6147d075c3c53d0687389a3555e946b694ef2

. ../build.sh
