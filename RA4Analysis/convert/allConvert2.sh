#!/bin/sh
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=0   --toPercentage=20 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=20  --toPercentage=40 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=40  --toPercentage=60 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=60  --toPercentage=80 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=80  --toPercentage=100 &
