#!/bin/bash

set -eux

env

name=gtksourceviewmm
short_version=3.18
patch_version=0
version=$short_version.$patch_version
filename=$name-$version.tar.xz
url=http://ftp.gnome.org/pub/GNOME/sources/$name/$short_version/$filename
checksum=51081ae3d37975dae33d3f6a40621d85cb68f4b36ae3835eec1513482aacfb39

. ../build.sh
