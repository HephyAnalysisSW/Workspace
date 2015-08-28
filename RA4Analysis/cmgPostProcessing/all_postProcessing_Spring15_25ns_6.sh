#!/bin/sh 
########Spring15###############

python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=WZ_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=WWTo2L2Nu_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=ZZ_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=ZJetsToNuNu_HT200to400_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=ZJetsToNuNu_HT400to600_25ns
python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=ZJetsToNuNu_HT600toInf_25ns

