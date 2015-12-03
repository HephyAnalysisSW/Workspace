#!/bin/sh 
########Spring15###############

#python cmgPostProcessing.py --leptonSelection=hard --skim="HT500ST250" --overwrite --calcbtagweights --samples=TTJets_DiLepton_full
python cmgPostProcessing.py --leptonSelection=hard --skim="HT500ST250" --small --overwrite --manScaleFactor=1.044 --calcbtagweights --samples=TTJets_SingleLeptonFromT_full
#python cmgPostProcessing.py --leptonSelection=hard --skim="HT500ST250" --overwrite --calcbtagweights --samples=TTJets_SingleLeptonFromTbar_full
#python cmgPostProcessing.py --leptonSelection=hard --skim="HT500ST250" --overwrite --calcbtagweights --hadronicLeg --samples=TTJets_LO
#python cmgPostProcessing.py --leptonSelection=hard --skim="HT500ST250" --overwrite --calcbtagweights --hadronicLeg --samples=TTJets_LO_HT600to800_25ns
#python cmgPostProcessing.py --leptonSelection=hard --skim="HT500ST250" --overwrite --calcbtagweights --hadronicLeg --samples=TTJets_LO_HT800to1200_25ns
#python cmgPostProcessing.py --leptonSelection=hard --skim="HT500ST250" --overwrite --calcbtagweights --hadronicLeg --samples=TTJets_LO_HT1200to2500_25ns
#python cmgPostProcessing.py --leptonSelection=hard --skim="HT500ST250" --overwrite --calcbtagweights --hadronicLeg --samples=TTJets_LO_HT2500toInf_25ns
