#!/bin/sh 
########Spring15###############

python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=TToLeptons_sch_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=TToLeptons_tch_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=TBar_tWch_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=T_tWch_25ns
