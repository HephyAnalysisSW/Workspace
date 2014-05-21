#!/bin/sh
#/data/schoef/lhe/decayed_stop200lsp170g100.lhe
#/data/schoef/lhe/decayed_stop300lsp240g150.lhe
#/data/schoef/lhe/decayed_stop300lsp270g175.lhe
#/data/schoef/lhe/decayed_stop300lsp270g200.lhe


python runFastSim.py $1 0       25000  &
python runFastSim.py $1 25000   50000  &
python runFastSim.py $1 50000   75000 &
python runFastSim.py $1 75000   100000 &
python runFastSim.py $1 100000  125000 &
python runFastSim.py $1 125000  150000 &
python runFastSim.py $1 150000  175000 &
python runFastSim.py $1 175000  200000 &
