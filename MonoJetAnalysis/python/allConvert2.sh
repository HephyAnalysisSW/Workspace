#!/bin/sh
python convert.py --samples=wjetsInc  --chmode=$1 $2 --fromPercentage=0 --toPercentage=20 &
python convert.py --samples=wjetsInc  --chmode=$1 $2 --fromPercentage=20 --toPercentage=40 &
python convert.py --samples=wjetsInc  --chmode=$1 $2 --fromPercentage=40 --toPercentage=60 &
python convert.py --samples=wjetsInc  --chmode=$1 $2 --fromPercentage=60 --toPercentage=80 &
python convert.py --samples=wjetsInc  --chmode=$1 $2 --fromPercentage=80 --toPercentage=100 &
python convert.py --samples=dy        --chmode=$1 $2 --fromPercentage=0 --toPercentage=20 &
python convert.py --samples=dy        --chmode=$1 $2 --fromPercentage=20 --toPercentage=40 &
python convert.py --samples=dy        --chmode=$1 $2 --fromPercentage=40 --toPercentage=60 &
python convert.py --samples=dy        --chmode=$1 $2 --fromPercentage=60 --toPercentage=80 &
python convert.py --samples=dy        --chmode=$1 $2 --fromPercentage=80 --toPercentage=100 &
