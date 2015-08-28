#!/bin/sh 
########Spring15###############
#python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=DYJetsToLL_M_50_HT100to200_50ns
#python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=DYJetsToLL_M_50_HT200to400_50ns
python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=DYJetsToLL_M_50_HT400to600_50ns
python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=DYJetsToLL_M_50_HT600toInf_50ns
