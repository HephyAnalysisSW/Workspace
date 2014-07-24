#!/bin/sh
python convert.py --samples=data         $1 --chmode=copy --fromPercentage=0  --toPercentage=20  &
python convert.py --samples=data         $1 --chmode=copy --fromPercentage=20 --toPercentage=40  &
python convert.py --samples=data         $1 --chmode=copy --fromPercentage=40 --toPercentage=60  &
python convert.py --samples=data         $1 --chmode=copy --fromPercentage=60 --toPercentage=80  &
python convert.py --samples=data         $1 --chmode=copy --fromPercentage=80 --toPercentage=100 &
python convert.py --samples=dataSingleMu $1 --chmode=copyMu --fromPercentage=0  --toPercentage=20  &
python convert.py --samples=dataSingleMu $1 --chmode=copyMu --fromPercentage=20 --toPercentage=40  &
python convert.py --samples=dataSingleMu $1 --chmode=copyMu --fromPercentage=40 --toPercentage=60  &
python convert.py --samples=dataSingleMu $1 --chmode=copyMu --fromPercentage=60 --toPercentage=80  &
python convert.py --samples=dataSingleMu $1 --chmode=copyMu --fromPercentage=80 --toPercentage=100 &
