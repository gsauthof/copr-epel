#!/bin/bash

set -eux

env

name=nemiver
short_version=0.9
patch_version=6
version=${short_version}.${patch_version}
filename=$name-$version.tar.xz
url=http://ftp.gnome.org/pub/GNOME/sources/$name/$short_version/$filename
checksum=331ae34f2d18166199a7012dc777fbc5899e01f3e28909502957fcb6bef6963f

. ../build.sh
