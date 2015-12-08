#!/bin/sh 
########Spring15###############

python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250"  --samples=TToLeptons_sch
python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250"  --samples=TToLeptons_tch
python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250"  --samples=TBar_tWch
python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250"  --samples=T_tWch

python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250"  --samples=TTWJetsToLNu_25ns
python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250"  --samples=TTWJetsToQQ_25ns
python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250"  --samples=TTZToLLNuNu_25ns
python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250"  --samples=TTZToQQ_25ns
#
#
#python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250"  --samples=TBar_tWch_DS
#python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250"  --samples=T_tWch_DS
#python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250"  --samples=TToLeptons_tch_amcatnlo
#python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250"  --samples=TToLeptons_tch_amcatnlo_ext




