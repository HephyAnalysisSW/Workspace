#!/bin/sh
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=0   --toPercentage=10 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=10  --toPercentage=20 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=20  --toPercentage=30 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=30  --toPercentage=40 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=40  --toPercentage=50 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=50  --toPercentage=60 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=60  --toPercentage=70 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=70  --toPercentage=80 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=80  --toPercentage=90 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=90  --toPercentage=100 &
