#!/bin/sh 
########Spring15###############

#python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=TTJets_25ns
#python cmgPostProcessing.py --leptonSelection=hard --skim="HT400ST200"  --samples=TTJets_LO_25ns
#python cmgPostProcessing.py --leptonSelection=hard --skim="HT400ST200"  --samples=TTJets_LO_HT600to800_25ns
#python cmgPostProcessing.py --leptonSelection=hard --skim="HT400ST200"  --samples=TTJets_LO_HT800to1200_25ns
#python cmgPostProcessing.py --leptonSelection=hard --skim="HT400ST200"  --samples=TTJets_LO_HT1200to2500_25ns
#python cmgPostProcessing.py --leptonSelection=hard --skim="HT400ST200"  --samples=TTJets_LO_HT2500toInf_25ns

#python cmgPostProcessing.py --overwrite --calcbtagweights --manScaleFactor=1.066 --skim="HT500ST250diLep" --samples=TTJets_DiLepton_full
python cmgPostProcessing.py --overwrite --calcbtagweights --manScaleFactor=2.05  --skim="HT500ST250semiLep" --samples=TTJets_SingleLeptonFromT_full
#python cmgPostProcessing.py --overwrite --calcbtagweights --manScaleFactor=1.025 --skim="HT500ST250semiLep" --samples=TTJets_SingleLeptonFromTbar_full
#python cmgPostProcessing.py --overwrite --calcbtagweights --manScaleFactor=1.    --skim="HT500ST250LHE_FullHadronic_inc" --samples=TTJets_LO
#python cmgPostProcessing.py --overwrite --calcbtagweights --manScaleFactor=0.953 --skim="HT500ST250LHE_FullHadronic" --samples=TTJets_LO_HT600to800_25ns
#python cmgPostProcessing.py --overwrite --calcbtagweights --manScaleFactor=0.953 --skim="HT500ST250LHE_FullHadronic" --samples=TTJets_LO_HT800to1200_25ns
#python cmgPostProcessing.py --overwrite --calcbtagweights --manScaleFactor=0.953 --skim="HT500ST250LHE_FullHadronic" --samples=TTJets_LO_HT1200to2500_25ns
#python cmgPostProcessing.py --overwrite --calcbtagweights --manScaleFactor=0.953 --skim="HT500ST250LHE_FullHadronic" --samples=TTJets_LO_HT2500toInf_25ns
#python cmgPostProcessing.py --overwrite --calcbtagweights --manScaleFactor=0.93  --skim="LHEHT1000" --samples=TTJets_LO_HT600to800_25ns
#python cmgPostProcessing.py --overwrite --calcbtagweights --manScaleFactor=0.93  --skim="LHEHT1000" --samples=TTJets_LO_HT800to1200_25ns
#python cmgPostProcessing.py --overwrite --calcbtagweights --manScaleFactor=0.93  --skim="LHEHT1000" --samples=TTJets_LO_HT1200to2500_25ns
#python cmgPostProcessing.py --overwrite --calcbtagweights --manScaleFactor=0.93  --skim="LHEHT1000" --samples=TTJets_LO_HT2500toInf_25ns




