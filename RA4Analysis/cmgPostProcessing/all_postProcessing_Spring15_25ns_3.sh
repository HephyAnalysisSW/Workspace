#!/bin/sh 
########Spring15###############

python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=WJetsToLNu_HT100to200_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=WJetsToLNu_HT200to400_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=WJetsToLNu_HT400to600_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=WJetsToLNu_HT600toInf_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=WJetsToLNu_HT600to800_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=WJetsToLNu_HT800to1200_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=WJetsToLNu_HT1200to2500_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=WJetsToLNu_HT2500toInf_25ns
