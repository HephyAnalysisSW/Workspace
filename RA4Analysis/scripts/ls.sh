#/bin/env bash


CMDDIR=$LCG_LOCATION/bin/dpm

[ "$LCG_LOCATION" == "/opt/lcg" ] && CMDDIR=$LCG_LOCATION/bin

ROOT=/dpm/oeaw.ac.at/home/cms/store/user/$USER

$CMDDIR/rfdir $ROOT/$1
