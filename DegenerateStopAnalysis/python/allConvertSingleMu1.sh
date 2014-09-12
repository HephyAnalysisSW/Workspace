#!/bin/sh
python convert.py --samples=$1 --chmode=copyMu --fromPercentage=0  --toPercentage=5 &
python convert.py --samples=$1 --chmode=copyMu --fromPercentage=5  --toPercentage=10 &
python convert.py --samples=$1 --chmode=copyMu --fromPercentage=10 --toPercentage=15 &
python convert.py --samples=$1 --chmode=copyMu --fromPercentage=15 --toPercentage=20 &
python convert.py --samples=$1 --chmode=copyMu --fromPercentage=20 --toPercentage=25 &
python convert.py --samples=$1 --chmode=copyMu --fromPercentage=25 --toPercentage=30 &
python convert.py --samples=$1 --chmode=copyMu --fromPercentage=30 --toPercentage=35 &
python convert.py --samples=$1 --chmode=copyMu --fromPercentage=35 --toPercentage=40 &
python convert.py --samples=$1 --chmode=copyMu --fromPercentage=40 --toPercentage=45 &
python convert.py --samples=$1 --chmode=copyMu --fromPercentage=45 --toPercentage=50 &
