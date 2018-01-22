#!/bin/bash

set -eux

env

name=gdlmm
short_version=3.7
patch_version=3
version=$short_version.$patch_version
filename=$name-$version.tar.xz
url=http://ftp.gnome.org/pub/GNOME/sources/$name/$short_version/$filename
checksum=e280ed9233877b63ad0a0c8fb04d2c35dc6a29b3312151ee21a15b5932fef79b

. ../build.sh
