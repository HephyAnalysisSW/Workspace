#!/bin/sh 
########Spring15###############

#python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=DYJetsToLL_M_10to50_25ns
#python cmgPostProcessing.py --skim="HT500ST250"  --samples=DYJetsToLL_M_50_25ns
# --calcbtagweights removed!
#python cmgPostProcessing.py --overwrite --skim="HT500ST250" --calcbtagweights --samples=DYJetsToLL_M_50_amcatnloFXFX_25ns
#python cmgPostProcessing.py --overwrite --skim="HT500ST250" --calcbtagweights --samples=DYJetsToLL_M_50_madgraphMLM_25ns
python cmgPostProcessing.py --overwrite  --calcbtagweights --samples=DYJetsToLL_M_50_HT_100to200_25ns
#python cmgPostProcessing.py --overwrite  --calcbtagweights --samples=DYJetsToLL_M_50_HT_200to400_25ns
#python cmgPostProcessing.py --overwrite  --calcbtagweights --samples=DYJetsToLL_M_50_HT_400to600_25ns
#python cmgPostProcessing.py --overwrite  --calcbtagweights --samples=DYJetsToLL_M_50_HT_600toInf_25ns
