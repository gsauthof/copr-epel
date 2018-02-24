#!/bin/bash

set -eux

env

name=maildrop
version=2.8.3.20151220
filename=$name-$version.tar.bz2
url=http://prdownloads.sourceforge.net/courier/$name/$version/$name-$version.tar.bz2
checksum=ff2c8018510129e9b3681e73717f8628e7c0310c0d8f74919a7cfab6aadab857

. ../build.sh
