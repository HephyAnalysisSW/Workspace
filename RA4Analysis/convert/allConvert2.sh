#!/bin/sh
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=0   --toPercentage=2 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=2   --toPercentage=4 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=4   --toPercentage=6 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=6   --toPercentage=8 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=8   --toPercentage=10 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=90   --toPercentage=92 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=92   --toPercentage=94 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=94   --toPercentage=96 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=96   --toPercentage=98 &
python convert.py --samples=$1     --chmode=$2 $3 --fromPercentage=98   --toPercentage=100 &
