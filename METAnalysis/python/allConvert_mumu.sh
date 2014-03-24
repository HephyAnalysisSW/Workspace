#!/bin/sh
python convert.py Zmumu data_mumu &
python convert.py Zmumu ttbar_mumu &
python convert.py Zmumu wjets_mumu &
python convert.py Zmumu drellYan_mumu &
python convert.py Zmumu singleTop_mumu &
python convert.py Zmumu diboson_mumu &

