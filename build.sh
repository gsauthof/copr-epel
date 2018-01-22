#!/bin/bash

# to be included from a build.sh located in a subdirectory
# input variables: filename, url, checksum

outdir=$1
# equals $PWD
specdir=$2
specfile=$(ls *.spec)

if [ ${url#https} = $url ]; then
  just_https=""
else
  just_https="--proto-redir =https"
fi
curl $just_https --silent --show-error --fail -L -O $url
sha256sum "$filename"
echo "$checksum  $filename" | sha256sum -c -

rpmbuild \
 --define "_sourcedir $PWD" \
 --define "_specdir $PWD" \
 --define "_rpmdir $outdir" \
 --define "_srcrpmdir $outdir" \
 -bs $specfile
