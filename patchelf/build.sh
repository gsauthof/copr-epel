#!/bin/bash

set -eux

env

name=patchelf
version=0.9
filename=$name-$version.tar.bz2
url=http://releases.nixos.org/$name/$name-$version/$filename
checksum=a0f65c1ba148890e9f2f7823f4bedf7ecad5417772f64f994004f59a39014f83

. ../build.sh
