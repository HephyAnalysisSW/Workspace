#/bin/env bash

CMDDIR=$LCG_LOCATION/bin/dpm
[ "$LCG_LOCATION" == "/opt/lcg" ] && CMDDIR=$LCG_LOCATION/bin
ROOT=/dpm/oeaw.ac.at/home/cms/store/user/$USER

isFile=`echo $1 | grep root$ | wc -l`

R=""

[ "$isFile" -eq 0 ] && R="-r"

yes | $CMDDIR/rfrm $R $ROOT/$1
