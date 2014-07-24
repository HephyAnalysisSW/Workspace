#!/bin/sh

python convert.py --samples=wjetsHT150v2    --chmode=$1       $2  --fromPercentage=0 --toPercentage=10 &
python convert.py --samples=wjetsHT150v2    --chmode=$1       $2  --fromPercentage=10 --toPercentage=20 &
python convert.py --samples=wjetsHT150v2    --chmode=$1       $2  --fromPercentage=20 --toPercentage=30 &
python convert.py --samples=wjetsHT150v2    --chmode=$1       $2  --fromPercentage=30 --toPercentage=40 &
python convert.py --samples=wjetsHT150v2    --chmode=$1       $2  --fromPercentage=40 --toPercentage=50 &
python convert.py --samples=wjetsHT150v2    --chmode=$1       $2  --fromPercentage=50 --toPercentage=60 &
python convert.py --samples=wjetsHT150v2    --chmode=$1       $2  --fromPercentage=60 --toPercentage=70 &
python convert.py --samples=wjetsHT150v2    --chmode=$1       $2  --fromPercentage=70 --toPercentage=80 &
python convert.py --samples=wjetsHT150v2    --chmode=$1       $2  --fromPercentage=80 --toPercentage=90 &
python convert.py --samples=wjetsHT150v2    --chmode=$1       $2  --fromPercentage=90 --toPercentage=100 &
#python convert.py --samples=wjetsToLNuPtW100   --chmode=$1 $2  --fromPercentage=0 --toPercentage=20 &
#python convert.py --samples=wjetsToLNuPtW100   --chmode=$1 $2  --fromPercentage=20 --toPercentage=40 &
#python convert.py --samples=wjetsToLNuPtW100   --chmode=$1 $2  --fromPercentage=40 --toPercentage=60 &
#python convert.py --samples=wjetsToLNuPtW100   --chmode=$1 $2  --fromPercentage=60 --toPercentage=80 &
#python convert.py --samples=wjetsToLNuPtW100   --chmode=$1 $2  --fromPercentage=80 --toPercentage=100 &
