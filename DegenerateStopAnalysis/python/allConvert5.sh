#!/bin/sh

python convert.py --samples=wjetsToLNuPtW180      --chmode=$1 $2 &
python convert.py --samples=wjetsToLNuPtW50       --chmode=$1 $2 &
python convert.py --samples=wMinusToLNu           --chmode=$1 $2 &
python convert.py --samples=wPlusToLNu            --chmode=$1 $2 &
python convert.py --samples=dyJetsToLLPtZ180      --chmode=$1 $2 &
python convert.py --samples=dyJetsToLLPtZ50       --chmode=$1 $2 &
python convert.py --samples=dyJetsToLLPtZ50Ext    --chmode=$1 $2 &
python convert.py --samples=zJetsToNuNuHT50       --chmode=$1 $2 &
python convert.py --samples=zJetsToNuNuHT50Ext    --chmode=$1 $2 &
