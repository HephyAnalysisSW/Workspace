#!/bin/sh 
########Spring15###############

#python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=WJetsToLNu_HT100to200_25ns
#python cmgPostProcessing.py --overwrite --calcbtagweights --skim="HT500ST250" --samples=WJetsToLNu_HT100to200_25ns
#python cmgPostProcessing.py --overwrite --calcbtagweights --skim="HT500ST250"  --samples=WJetsToLNu_HT200to400
#python cmgPostProcessing.py --overwrite --calcbtagweights --skim="HT500ST250"  --samples=WJetsToLNu_HT400to600
#python cmgPostProcessing.py --overwrite --calcbtagweights --skim="HT500ST250"  --samples=WJetsToLNu_HT600to800
python cmgPostProcessing.py --overwrite --calcbtagweights --skim="HT500ST250"  --samples=WJetsToLNu_HT800to1200
python cmgPostProcessing.py --overwrite --calcbtagweights --skim="HT500ST250"  --samples=WJetsToLNu_HT1200to2500
python cmgPostProcessing.py --overwrite --calcbtagweights --skim="HT500ST250"  --samples=WJetsToLNu_HT2500toInf

#python cmgPostProcessing.py --overwrite --skim="HT500ST250" --calcbtagweights --samples=WJetsToLNu
