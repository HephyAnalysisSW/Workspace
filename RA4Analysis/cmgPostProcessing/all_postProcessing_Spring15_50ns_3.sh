#!/bin/sh 
########Spring15###############
python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=WJetsToLNu_50ns
python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=TToLeptons_tch_50ns
python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=TBar_tWch_50ns
python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=T_tWch_50ns
