#!/bin/sh

python convert.py --samples=ttbarPowHeg    --chmode=$1 --newMETCollection --fromPercentage=0 --toPercentage=20   &
python convert.py --samples=ttbarPowHeg    --chmode=$1 --newMETCollection --fromPercentage=20 --toPercentage=40  &
python convert.py --samples=ttbarPowHeg    --chmode=$1 --newMETCollection --fromPercentage=40 --toPercentage=60  &
python convert.py --samples=ttbarPowHeg    --chmode=$1 --newMETCollection --fromPercentage=60 --toPercentage=80  &
python convert.py --samples=ttbarPowHeg    --chmode=$1 --newMETCollection --fromPercentage=80 --toPercentage=100 &
