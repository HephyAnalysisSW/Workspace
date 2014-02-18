#!/bin/sh
python convert.py --samples=w1jets  --chmode=$1 --jesmode=$2 &
python convert.py --samples=w2jets  --chmode=$1 --jesmode=$2 &
python convert.py --samples=w3jets  --chmode=$1 --jesmode=$2 &
python convert.py --samples=w4jets  --chmode=$1 --jesmode=$2 &
python convert.py --samples=wjets   --chmode=$1 --jesmode=$2 &
python convert.py --samples=qcd1    --chmode=$1 --jesmode=$2 &
python convert.py --samples=qcd2    --chmode=$1 --jesmode=$2 &
python convert.py --samples=qcd3    --chmode=$1 --jesmode=$2 &

