#!/bin/sh 
########Spring15###############
python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=TTJets_50ns
python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=DYJetsToLL_M_10to50_50ns
