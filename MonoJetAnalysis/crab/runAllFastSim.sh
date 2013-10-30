#!/bin/sh
#/data/schoef/lhe/decayed_stop200lsp170g100.lhe
#/data/schoef/lhe/decayed_stop300lsp240g150.lhe
#/data/schoef/lhe/decayed_stop300lsp270g175.lhe
#/data/schoef/lhe/decayed_stop300lsp270g200.lhe


python runFastSim.py $1 0       50000  &
python runFastSim.py $1 50000   100000 &
python runFastSim.py $1 100000  150000 &
python runFastSim.py $1 150000  200000 &
python runFastSim.py $1 200000  250000 &
python runFastSim.py $1 250000  300000 &
python runFastSim.py $1 300000  350000 &
python runFastSim.py $1 350000  400000 &

