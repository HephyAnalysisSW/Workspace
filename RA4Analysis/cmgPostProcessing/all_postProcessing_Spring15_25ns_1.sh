#!/bin/sh 
########Spring15###############

#python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=TTJets_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim="HT400ST200"  --samples=TTJets_LO_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim="HT400ST200"  --samples=TTJets_LO_HT600to800_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim="HT400ST200"  --samples=TTJets_LO_HT800to1200_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim="HT400ST200"  --samples=TTJets_LO_HT1200to2500_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim="HT400ST200"  --samples=TTJets_LO_HT2500toInf_25ns
