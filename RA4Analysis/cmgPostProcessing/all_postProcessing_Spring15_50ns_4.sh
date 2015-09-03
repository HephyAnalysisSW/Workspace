#!/bin/sh 
########Spring15###############
python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=WZ_50ns
python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=WWTo2L2Nu_50ns
python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=ZZ_50ns
