#!/bin/sh 
########Spring15###############
python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=WZ_50ns
python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=WWTo2L2Nu_50ns
python cmgPostProcessing.py --leptonSelection=hard --skim=HT400ST200  --samples=ZZ_50ns
