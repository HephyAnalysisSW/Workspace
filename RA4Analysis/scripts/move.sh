#/bin/env bash


CMDDIR=$LCG_LOCATION/bin/dpm
[ "$LCG_LOCATION" == "/opt/lcg" ] && CMDDIR=$LCG_LOCATION/bin

ROOT=/dpm/oeaw.ac.at/home/cms/store/user/$USER

echo "$CMDDIR/rfrename $ROOT/$1 $ROOT/$2/$1"
$CMDDIR/rfrename $ROOT/$1 $ROOT/$2/$1
