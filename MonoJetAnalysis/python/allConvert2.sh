#!/bin/sh
python convert.py $1 w1jets  &
python convert.py $1 w2jets  &
python convert.py $1 w3jets  &
python convert.py $1 w4jets  &
python convert.py $1 wjets  &
python convert.py $1 qcd1  &
python convert.py $1 qcd2 &
python convert.py $1 qcd3 &

