#!/bin/bash

set -eux

env

name=maildrop
version=2.8.5
filename=$name-$version.tar.bz2
url=http://prdownloads.sourceforge.net/courier/$name/$version/$name-$version.tar.bz2
checksum=c21174ef882aeb169031bb5886b55959687074415153232f4c60695405fcddb1

. ../build.sh
