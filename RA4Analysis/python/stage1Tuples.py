import copy, os, sys

debug={}
debug["name"]     = "debug"
debug["Chain"]     = "Events"
debug["bins"] = [{'dir':"/afs/hephy.at/scratch/s/schoefbeck/CMS/CMSSW_7_0_6_patch1/src/Workspace/HEPHYPythonTools/crab/pickEvents/miniAOD/",'dbsName':None}]

ttJetsCSA1425ns={}
ttJetsCSA1425ns["name"]     = "ttJetsCSA1425ns"
ttJetsCSA1425ns["Chain"] = "Events"
ttJetsCSA1425ns["bins"] = [{'dir':"/data/schoef/stage1CSA14/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_Spring14miniaod-PU20bx25_POSTLS170_V5-v1__2", 
                        'dbsName':'/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM'}]

#ttJetsCSA1450ns={}
#ttJetsCSA1450ns["name"]     = "ttJetsCSA1450ns"
#ttJetsCSA1450ns["Chain"] = "Events"
##ttJetsCSA1450ns['reweightingHistoFile'] = S10rwHisto 
##ttJetsCSA1450ns['reweightingHistoFileSysPlus'] = S10rwPlusHisto
##ttJetsCSA1450ns['reweightingHistoFileSysMinus'] = S10rwMinusHisto
#ttJetsCSA1450ns["bins"] = [{'dir':"/dpm/oeaw.ac.at/home/cms/store/user/schoef/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/crab_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_Spring14miniaod-PU_S14_POSTLS170_V6-v1_MINIAODSIM/140817_063637/0000", 
#                        'dbsName':'/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU_S14_POSTLS170_V6-v1/MINIAODSIM'}]

ttJetsCSA1450ns={}
ttJetsCSA1450ns["name"]     = "ttJetsCSA1450ns"
ttJetsCSA1450ns["Chain"] = "Events"
ttJetsCSA1450ns["bins"] = [{'dir':"/dpm/oeaw.ac.at/home/cms/store/user/easilar/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/crab_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_Spring14miniaod-PU_S14_POSTLS170_V6-v1_MINIAODSIM/140814_095845/0000", 
                        'dbsName':'/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU_S14_POSTLS170_V6-v1/MINIAODSIM'}]

WJetsToLNu25ns={}
WJetsToLNu25ns["name"]   = "WJetsToLNu25ns"
WJetsToLNu25ns["Chain"] = "Events"
WJetsToLNu25ns["bins"] = [{'dir':"/dpm/oeaw.ac.at/home/cms/store/user/easilar/WJetsToLNu_13TeV-madgraph-pythia8-tauola/crab_WJetsToLNu_13TeV-madgraph-pythia8-tauola_Spring14miniaod-PU20bx25_POSTLS170_V5-v1_MINIAODSIM/140814_112652/0000",
                       'dbsName':'/WJetsToLNu_13TeV-madgraph-pythia8-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM'}] 

WJetsHTToLNu={}
WJetsHTToLNu["name"]   = "WJetsHTToLNu"
WJetsHTToLNu["Chain"] = "Events"
WJetsHTToLNu["bins"] = [
                        {'dir':"/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_310814/WJetsToLNu_HT-100to200_Tune4C_13TeV-madgraph-tauola/schoef-WJetsToLNu_HT-100to200_Tune4C_13TeV-madgraph-tauola_Spring14dr-PU_S14_POSTLS170_V6-v1",
                        'dbsName':'/WJetsToLNu_HT-100to200_Tune4C_13TeV-madgraph-tauola/Spring14dr-PU_S14_POSTLS170_V6-v1/AODSIM'},
                        {'dir':"/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_310814/WJetsToLNu_HT-200to400_Tune4C_13TeV-madgraph-tauola/schoef-WJetsToLNu_HT-200to400_Tune4C_13TeV-madgraph-tauola_Spring14dr-PU_S14_POSTLS170_V6-v1",
                        'dbsName':'/WJetsToLNu_HT-200to400_Tune4C_13TeV-madgraph-tauola/Spring14dr-PU_S14_POSTLS170_V6-v1/AODSIM'},
                        {'dir':"/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_310814/WJetsToLNu_HT-400to600_Tune4C_13TeV-madgraph-tauola/schoef-WJetsToLNu_HT-400to600_Tune4C_13TeV-madgraph-tauola_Spring14dr-PU_S14_POSTLS170_V6-v1",
                        'dbsName':'/WJetsToLNu_HT-400to600_Tune4C_13TeV-madgraph-tauola/Spring14dr-PU_S14_POSTLS170_V6-v1/AODSIM'},
                        {'dir':"/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_310814/WJetsToLNu_HT-600toInf_Tune4C_13TeV-madgraph-tauola/schoef-WJetsToLNu_HT-600toInf_Tune4C_13TeV-madgraph-tauola_Spring14dr-PU_S14_POSTLS170_V6-v1",
                        'dbsName':'/WJetsToLNu_HT-600toInf_Tune4C_13TeV-madgraph-tauola/Spring14dr-PU_S14_POSTLS170_V6-v1/AODSIM'},
                        ] 
T5Full_1200_1000_800={}
T5Full_1200_1000_800["name"]     = "T5Full_1200_1000_800"
T5Full_1200_1000_800["Chain"] = "Events"
T5Full_1200_1000_800["bins"] = [{'dir':"/dpm/oeaw.ac.at/home/cms/store/user/schoef/stage1_031014/T5Full-1200-1000-800", 
                        'dbsName':'/T5Full_T5Full-1200-1000-800-Decay-MGMMatch50/schoef-T5Full_T5Full-1200-1000-800-Decay-MGMMatch50-miniAOD-92bfc1aa0ef8c674e0edabb945b19298/USER'}]
T5Full_1500_800_100={}
T5Full_1500_800_100["name"]     = "T5Full_1500_800_100"
T5Full_1500_800_100["Chain"] = "Events"
T5Full_1500_800_100["bins"] = [{'dir':"/dpm/oeaw.ac.at/home/cms/store/user/schoef/stage1_031014/T5Full-1500-800-100", 
                        'dbsName':'/T5Full_T5Full-1500-800-100-Decay-MGMMatch50/schoef-T5Full_T5Full-1500-800-100-Decay-MGMMatch50-miniAOD-92bfc1aa0ef8c674e0edabb945b19298/USER'}]



testSample={}
testSample["name"]     = "tmp"
testSample["dirname"] = "/afs/hephy.at/scratch/s/schoefbeck/CMS/CMSSW_7_0_6_patch1/src/Workspace/"
testSample["Chain"] = "Events"
testSample["bins"] = [{'dir':'/afs/hephy.at/scratch/s/schoefbeck/CMS/CMSSW_7_0_6_patch1/src/Workspace/tmp','dbsName':None}]



#from Workspace.HEPHYPythonTools.createPUReweightingHisto import getPUReweightingUncertainty
#
#S10rwHisto = getPUReweightingUncertainty("S10", dataFile = "/data/schoef/tools/PU/MyDataPileupHistogram_Run2012ABCD_60max_true_pixelcorr_Sys0.root")
#S10rwPlusHisto = getPUReweightingUncertainty("S10", dataFile = "/data/schoef/tools/PU/MyDataPileupHistogram_Run2012ABCD_60max_true_pixelcorr_SysPlus5.root")
#S10rwMinusHisto = getPUReweightingUncertainty("S10", dataFile = "/data/schoef/tools/PU/MyDataPileupHistogram_Run2012ABCD_60max_true_pixelcorr_SysMinus5.root")

