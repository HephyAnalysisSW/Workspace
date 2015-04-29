import copy, os, sys

#[TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_Phys14DR-PU20bx25_PHYS14_25_V1-v1_AODSIM]
#cmssw.datasetpath=/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM

DYJetsToLL_HT={}
DYJetsToLL_HT["name"]   = "DYJetsToLL_HT"
DYJetsToLL_HT["Chain"] = "Events"
DYJetsToLL_HT["bins"] = [
  {'dir':"/data/schoef/metTuple2/DYJetsToLL_M-50_HT-100to200_Tune4C_13TeV-madgraph-tauola_Phys14DR-PU20bx25_PHYS14_25_V1-v1_AODSIM",
  'dbsName':'/DYJetsToLL_M-50_HT-100to200_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM'},
  {'dir':"/data/schoef/metTuple2/DYJetsToLL_M-50_HT-200to400_Tune4C_13TeV-madgraph-tauola_Phys14DR-PU20bx25_PHYS14_25_V1-v1_AODSIM",
  'dbsName':'/DYJetsToLL_M-50_HT-200to400_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM'},
  {'dir':"/data/schoef/metTuple2/DYJetsToLL_M-50_HT-400to600_Tune4C_13TeV-madgraph-tauola_Phys14DR-PU20bx25_PHYS14_25_V1-v1_AODSIM",
  'dbsName':'/DYJetsToLL_M-50_HT-400to600_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM'},
  {'dir':"/data/schoef/metTuple2/DYJetsToLL_M-50_HT-600toInf_Tune4C_13TeV-madgraph-tauola_Phys14DR-PU20bx25_PHYS14_25_V1-v1_AODSIM",
  'dbsName':'/DYJetsToLL_M-50_HT-600toInf_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM'},
  ] 
TTJets={}
TTJets["name"]   = "TTJets"
TTJets["Chain"] = "Events"
TTJets["bins"] = [
  {'dir':"/data/schoef/metTuple2/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_Phys14DR-PU20bx25_PHYS14_25_V1-v1_AODSIM",
  'dbsName':'/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM'},
  ] 
DYJetsToLL={}
DYJetsToLL["name"]   = "DYJetsToLL"
DYJetsToLL["Chain"] = "Events"
DYJetsToLL["bins"] = [
  {'dir':"/data/schoef/metTuple2/DYJetsToLL_M-50_13TeV-madgraph-pythia8_Phys14DR-PU20bx25_PHYS14_25_V1-v1_AODSIM",
  'dbsName':'/DYJetsToLL_M-50_13TeV-madgraph-pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM'},
  ] 
