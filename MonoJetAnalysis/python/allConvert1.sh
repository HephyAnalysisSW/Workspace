#!/bin/sh
python convert.py --samples=ttbarPowHeg     --chmode=$1 $2 --fromPercentage=0 --toPercentage=20 &
python convert.py --samples=ttbarPowHeg     --chmode=$1 $2 --fromPercentage=20 --toPercentage=40 &
python convert.py --samples=ttbarPowHeg     --chmode=$1 $2 --fromPercentage=40 --toPercentage=60 &
python convert.py --samples=ttbarPowHeg     --chmode=$1 $2 --fromPercentage=60 --toPercentage=80 &
python convert.py --samples=ttbarPowHeg     --chmode=$1 $2 --fromPercentage=80 --toPercentage=100 &
python convert.py --samples=ww              --chmode=$1 $2 &
python convert.py --samples=wz              --chmode=$1 $2 &
python convert.py --samples=zz              --chmode=$1 $2 &
python convert.py --samples=singleTop       --chmode=$1 $2 &
python convert.py --samples=zinv            --chmode=$1 $2 --fromPercentage=0 --toPercentage=20   &
python convert.py --samples=zinv            --chmode=$1 $2 --fromPercentage=20 --toPercentage=40  &
python convert.py --samples=zinv            --chmode=$1 $2 --fromPercentage=40 --toPercentage=60  &
python convert.py --samples=zinv            --chmode=$1 $2 --fromPercentage=60 --toPercentage=80  &
python convert.py --samples=zinv            --chmode=$1 $2 --fromPercentage=80 --toPercentage=100 &
##
