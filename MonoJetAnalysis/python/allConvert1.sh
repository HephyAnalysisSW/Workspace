#!/bin/sh
python convert.py $1 data  &
python convert.py $1 ttbar  &
python convert.py $1 ww  &
python convert.py $1 singleTop  &
python convert.py $1 wjetsInc  &
python convert.py $1 dy  &
python convert.py $1 zinv  &

