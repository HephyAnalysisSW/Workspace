#!/bin/sh 
########Spring15###############

python cmgPostProcessing.py --overwrite  --skim="HT500ST250" --samples=QCD_HT300to500_25ns
python cmgPostProcessing.py --overwrite  --skim="HT500ST250" --samples=QCD_HT500to700_25ns
python cmgPostProcessing.py --overwrite  --skim="HT500ST250" --samples=QCD_HT700to1000_25ns
python cmgPostProcessing.py --overwrite  --skim="HT500ST250" --samples=QCD_HT1000to1500_25ns
python cmgPostProcessing.py --overwrite  --skim="HT500ST250" --samples=QCD_HT1500to2000_25ns
python cmgPostProcessing.py --overwrite  --skim="HT500ST250" --samples=QCD_HT2000toInf_25ns
#
