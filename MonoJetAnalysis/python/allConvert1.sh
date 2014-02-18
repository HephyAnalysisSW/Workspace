#!/bin/sh
python convert.py --samples=data      --chmode=$1 --jesmode=$2&
python convert.py --samples=ttbar     --chmode=$1 --jesmode=$2&
python convert.py --samples=ww        --chmode=$1 --jesmode=$2&
python convert.py --samples=singleTop --chmode=$1 --jesmode=$2&
python convert.py --samples=wjetsInc  --chmode=$1 --jesmode=$2&
python convert.py --samples=dy        --chmode=$1 --jesmode=$2&
python convert.py --samples=zinv      --chmode=$1 --jesmode=$2&

