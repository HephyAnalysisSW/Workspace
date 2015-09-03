#!/bin/sh 
########Spring15###############

python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=TToLeptons_sch_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=TToLeptons_tch_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=TBar_tWch_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=T_tWch_25ns
