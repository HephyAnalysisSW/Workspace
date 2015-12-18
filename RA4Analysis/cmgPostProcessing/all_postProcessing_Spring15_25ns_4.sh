#!/bin/sh 
########Spring15###############

#python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=TToLeptons_sch_25ns
#python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=TToLeptons_tch_25ns
#python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=TBar_tWch_25ns
#python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=T_tWch_25ns

python cmgPostProcessingAntiSelectionV2.py --overwrite --leptonSelection=none --samples=TToLeptons_sch
python cmgPostProcessingAntiSelectionV2.py --overwrite --leptonSelection=none --samples=TToLeptons_tch
python cmgPostProcessingAntiSelectionV2.py --overwrite --leptonSelection=none --samples=TBar_tWch
python cmgPostProcessingAntiSelectionV2.py --overwrite --leptonSelection=none --samples=T_tWch

python cmgPostProcessingAntiSelectionV2.py --overwrite --leptonSelection=none --samples=TTWJetsToLNu_25ns
python cmgPostProcessingAntiSelectionV2.py --overwrite --leptonSelection=none --samples=TTWJetsToQQ_25ns
python cmgPostProcessingAntiSelectionV2.py --overwrite --leptonSelection=none --samples=TTZToLLNuNu_25ns
python cmgPostProcessingAntiSelectionV2.py --overwrite --leptonSelection=none --samples=TTZToQQ_25ns
