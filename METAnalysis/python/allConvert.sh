#!/bin/sh
python convert.py $1 dataZmumu &
python convert.py $1 ttbar_mumu &
python convert.py $1 wjets_mumu &
python convert.py $1 drellYan_mumu &
python convert.py $1 singleTop_mumu &
python convert.py $1 diboson_mumu &

