#!/bin/sh 
########Spring15###############

#python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=TToLeptons_sch_25ns
#python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=TToLeptons_tch_25ns
#python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=TBar_tWch_25ns
#python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=T_tWch_25ns

#python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT400ST200"  --samples=TToLeptons_sch
#python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT400ST200"  --samples=TToLeptons_tch
#python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT400ST200"  --samples=TBar_tWch
#python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT400ST200"  --samples=T_tWch

#python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT400ST200"  --samples=TTWJetsToLNu_25ns
python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT400ST200"  --samples=TTWJetsToQQ_25ns
#python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT400ST200"  --samples=TTZToLLNuNu_25ns
#python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT400ST200"  --samples=TTZToQQ_25ns
