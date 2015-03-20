#!/bin/bash
files=$1
out=$2
var=$3
period=$4
tmp=~/tmp/$(basename $0)
mkdir -p $tmp
vfiles=""
failure=1
for file in $1 ; do
    tmp2=$tmp/$(basename $file)
    cdo seldate,${period/-/,} -selname,$var $file $tmp2  &&  vfiles+=" "$tmp2
done
if [ "$vfiles" ] ; then 
    tmp3=$tmp/$(basename $0).nc
    cdo copy $vfiles $tmp3            && rm $vfiles 
    cdo timavg $tmp3 $out             && rm $tmp3         && failure=0
fi
exit $failure
