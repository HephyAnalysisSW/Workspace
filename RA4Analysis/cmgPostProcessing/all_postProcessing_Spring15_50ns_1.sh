#!/bin/sh 
########Spring15###############
python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=TTJets_50ns
python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=DYJetsToLL_M_10to50_50ns
