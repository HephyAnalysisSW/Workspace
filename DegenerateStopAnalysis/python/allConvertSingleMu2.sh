#!/bin/sh
python convert.py --samples=$1 --chmode=copyMu --fromPercentage=50 --toPercentage=55 &
python convert.py --samples=$1 --chmode=copyMu --fromPercentage=55 --toPercentage=60 &
python convert.py --samples=$1 --chmode=copyMu --fromPercentage=60 --toPercentage=65 &
python convert.py --samples=$1 --chmode=copyMu --fromPercentage=65 --toPercentage=70 &
python convert.py --samples=$1 --chmode=copyMu --fromPercentage=70 --toPercentage=75 &
python convert.py --samples=$1 --chmode=copyMu --fromPercentage=75 --toPercentage=80 &
python convert.py --samples=$1 --chmode=copyMu --fromPercentage=80 --toPercentage=85 &
python convert.py --samples=$1 --chmode=copyMu --fromPercentage=85 --toPercentage=90 &
python convert.py --samples=$1 --chmode=copyMu --fromPercentage=90 --toPercentage=95 &
python convert.py --samples=$1 --chmode=copyMu --fromPercentage=95 --toPercentage=100 &
