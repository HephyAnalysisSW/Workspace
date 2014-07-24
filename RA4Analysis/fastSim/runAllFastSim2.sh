#!/bin/sh
#/data/schoef/lhe/decayed_stop200lsp170g100.lhe
#/data/schoef/lhe/decayed_stop300lsp240g150.lhe
#/data/schoef/lhe/decayed_stop300lsp270g175.lhe
#/data/schoef/lhe/decayed_stop300lsp270g200.lhe


python runFastSim.py $1 200000  225000 &
python runFastSim.py $1 225000  250000 &
python runFastSim.py $1 250000  275000 &
python runFastSim.py $1 275000  300000 &
python runFastSim.py $1 300000  325000 &
python runFastSim.py $1 325000  350000 &
python runFastSim.py $1 350000  375000 &
python runFastSim.py $1 375000  400000 &

