import copy, os, sys
allSamples = []

from Workspace.HEPHYPythonTools.createPUReweightingHisto import getPUReweightingUncertainty

S10rwHisto = getPUReweightingUncertainty("S10", dataFile = "/data/schoef/tools/PU/MyDataPileupHistogram_Run2012ABCD_60max_true_pixelcorr_Sys0.root")
S10rwPlusHisto = getPUReweightingUncertainty("S10", dataFile = "/data/schoef/tools/PU/MyDataPileupHistogram_Run2012ABCD_60max_true_pixelcorr_SysPlus5.root")
S10rwMinusHisto = getPUReweightingUncertainty("S10", dataFile = "/data/schoef/tools/PU/MyDataPileupHistogram_Run2012ABCD_60max_true_pixelcorr_SysMinus5.root")

data={}
data["name"]     = "data";
data['newMETCollection'] = True
data["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140314/"
data["bins"]    = ["MuHad-Run2012A-22Jan2013", "MuHad-Run2012B-22Jan2013", "MuHad-Run2012C-22Jan2013", "MuHad-Run2012D-22Jan2013"]
data["bins"]    += ["ElectronHad-Run2012A-22Jan2013", "ElectronHad-Run2012B-22Jan2013", "ElectronHad-Run2012C-22Jan2013-2", "ElectronHad-Run2012D-22Jan2013-2"]
data["Chain"] = "Events"
data["Counter"] = "bool_EventCounter_passed_PAT.obj"
allSamples.append(data)


dataSingleMu={}
dataSingleMu["name"]     = "data";
dataSingleMu['newMETCollection'] = True
dataSingleMu["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140314/"
dataSingleMu["bins"]    = ["SingleMu-Run2012A-22Jan2013", "SingleMu-Run2012B-22Jan2013", "SingleMu-Run2012C-22Jan2013", "SingleMu-Run2012D-22Jan2013"]
dataSingleMu["Chain"] = "Events"
dataSingleMu["Counter"] = "bool_EventCounter_passed_PAT.obj"
allSamples.append(dataSingleMu)


T5Full_1100_200_100={}
T5Full_1100_200_100['reweightingHistoFile'] = S10rwHisto 
T5Full_1100_200_100['reweightingHistoFileSysPlus'] = S10rwPlusHisto
T5Full_1100_200_100['reweightingHistoFileSysMinus'] = S10rwMinusHisto
T5Full_1100_200_100["name"]     = "T5Full_1100_200_100"
T5Full_1100_200_100['newMETCollection'] = True
T5Full_1100_200_100["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_160514/"
T5Full_1100_200_100["bins"]    = ["T5Full_1100_200_100-4"]
T5Full_1100_200_100["Chain"] = "Events"
T5Full_1100_200_100["Counter"] = "bool_EventCounter_passed_PAT.obj"

T5Full_1100_800_600={}
T5Full_1100_800_600['reweightingHistoFile'] = S10rwHisto 
T5Full_1100_800_600['reweightingHistoFileSysPlus'] = S10rwPlusHisto
T5Full_1100_800_600['reweightingHistoFileSysMinus'] = S10rwMinusHisto
T5Full_1100_800_600["name"]     = "T5Full_1100_800_600"
T5Full_1100_800_600['newMETCollection'] = True
T5Full_1100_800_600["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_160514/"
T5Full_1100_800_600["bins"]    = ["T5Full_1100_800_600-4"]
T5Full_1100_800_600["Chain"] = "Events"
T5Full_1100_800_600["Counter"] = "bool_EventCounter_passed_PAT.obj"

mc={}
mc["name"]     = "mc";
mc["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/mhickel/pat_130527"
mc['newMETCollection'] = False
mc["Chain"] = "Events"
#mc["reweightingHistoFile"]          = "/data/schoef/tools/PU/reweightingHisto_Summer2012-S10-Run2012ABCD_60max_true_pixelcorr_Sys0.root"
#mc["reweightingHistoFileSysPlus"]   = "/data/schoef/tools/PU/reweightingHisto_Summer2012-S10-Run2012ABCD_60max_true_pixelcorr_SysPlus5.root"
#mc["reweightingHistoFileSysMinus"]  = "/data/schoef/tools/PU/reweightingHisto_Summer2012-S10-Run2012ABCD_60max_true_pixelcorr_SysMinus5.root"

QCD_Bins = \
  ["8TeV-QCD-Pt1000-MuEnrichedPt5", "8TeV-QCD-Pt120to170-MuEnrichedPt5", "8TeV-QCD-Pt170to300-MuEnrichedPt5",\
   "8TeV-QCD-Pt20to30-MuEnrichedPt5", "8TeV-QCD-Pt300to470-MuEnrichedPt5", "8TeV-QCD-Pt30to50-MuEnrichedPt5",\
   "8TeV-QCD-Pt470to600-MuEnrichedPt5", "8TeV-QCD-Pt50to80-MuEnrichedPt5",\
   "8TeV-QCD-Pt600to800-MuEnrichedPt5", "8TeV-QCD-Pt800to1000-MuEnrichedPt5", "8TeV-QCD-Pt80to120-MuEnrichedPt5"]

#WJets_Bins = ["8TeV-WJets-HT250to300", "8TeV-WJets-HT300to400", "8TeV-WJets-HT400"]
#
DY_Bins = ["8TeV-DYJetsToLL-M10to50", "8TeV-DYJetsToLL-M50"]
#ZJets_Bins = DY_Bins
ZJetsInv_Bins = ["8TeV-ZJetsToNuNu-HT100to200", "8TeV-ZJetsToNuNu-HT200to400",\
                 "8TeV-ZJetsToNuNu-HT400", "8TeV-ZJetsToNuNu-HT50to100"]
#
singleTop_Bins = ["8TeV-T-t", "8TeV-T-s", "8TeV-T-tW", "8TeV-Tbar-t", "8TeV-Tbar-s", "8TeV-Tbar-tW"]

ttbar = copy.deepcopy(mc)
ttbar['reweightingHistoFile'] = S10rwHisto 
ttbar['reweightingHistoFileSysPlus'] = S10rwPlusHisto
ttbar['reweightingHistoFileSysMinus'] = S10rwMinusHisto
ttbar["bins"] = ["8TeV-TTJets"]
ttbar["name"] = "TTJets" 

ttbarPowHeg = copy.deepcopy(mc)
ttbarPowHeg['reweightingHistoFile'] = S10rwHisto 
ttbarPowHeg['reweightingHistoFileSysPlus'] = S10rwPlusHisto
ttbarPowHeg['reweightingHistoFileSysMinus'] = S10rwMinusHisto
ttbarPowHeg["bins"] = [["8TeV-TTJets-powheg-v1+2", ["8TeV-TTJets-powheg-v1", "8TeV-TTJets-powheg-v2"]]]
ttbarPowHeg["name"] = "TTJetsPowHeg" 
#
#ttbarPowHeg = copy.deepcopy(mc)
#ttbarPowHeg["dirname"] = "/data/mhickel/pat_130328/"
#ttbarPowHeg["bins"] = ["8TeV-TTJets-powheg-v1+2"]
#ttbarPowHeg["name"] = "TTJets-PowHeg" 

#wjets = copy.deepcopy(mc)
#wjets["bins"] = WJets_Bins 
#wjets["name"] = "WJetsHT250" 
#wjets['reweightingHistoFile'] = S10rwHisto
#wjets['reweightingHistoFileSysPlus'] = S10rwPlusHisto
#wjets['reweightingHistoFileSysMinus'] = S10rwMinusHisto

#wjets["dirname"] = "/data/mhickel/pat_120917_S10/mc8TeV/"
wjetsInc = copy.deepcopy(mc)
wjetsInc["bins"] = ["8TeV-WJetsToLNu-3"] 
wjetsInc["name"] = "WJetsToLNu" 
wjetsInc['reweightingHistoFile'] = S10rwHisto
wjetsInc['reweightingHistoFileSysPlus'] = S10rwPlusHisto
wjetsInc['reweightingHistoFileSysMinus'] = S10rwMinusHisto

w1jets = copy.deepcopy(mc)
w1jets["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140314/" 
w1jets['newMETCollection'] = True
w1jets["bins"] = ["8TeV-W1JetsToLNu"] 
w1jets["name"] = "W1JetsToLNu"
w1jets['reweightingHistoFile'] = S10rwHisto
w1jets['reweightingHistoFileSysPlus'] = S10rwPlusHisto
w1jets['reweightingHistoFileSysMinus'] = S10rwMinusHisto

w2jets = copy.deepcopy(w1jets)
w2jets["bins"] = ["8TeV-W2JetsToLNu"] 
w2jets['newMETCollection'] = True
w2jets["name"] = "W2JetsToLNu"
w2jets['reweightingHistoFile'] = S10rwHisto
w2jets['reweightingHistoFileSysPlus'] = S10rwPlusHisto
w2jets['reweightingHistoFileSysMinus'] = S10rwMinusHisto

w3jets = copy.deepcopy(w1jets)
w3jets["bins"] = ["8TeV-W3JetsToLNu"] 
w3jets['newMETCollection'] = True
w3jets["name"] = "W3JetsToLNu"
w3jets['reweightingHistoFile'] = S10rwHisto
w3jets['reweightingHistoFileSysPlus'] = S10rwPlusHisto
w3jets['reweightingHistoFileSysMinus'] = S10rwMinusHisto

w4jets = copy.deepcopy(w1jets)
w4jets["bins"] = ["8TeV-W4JetsToLNu"] 
w4jets['newMETCollection'] = True
w4jets["name"] = "W4JetsToLNu"
w4jets['reweightingHistoFile'] = S10rwHisto
w4jets['reweightingHistoFileSysPlus'] = S10rwPlusHisto
w4jets['reweightingHistoFileSysMinus'] = S10rwMinusHisto

wbbjets = copy.deepcopy(w1jets)
wbbjets["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140212"
wbbjets['newMETCollection'] = True
wbbjets["bins"]=["8TeV-WbbJetsToLNu"]
wbbjets["name"] = "WbbJets"
wbbjets['reweightingHistoFile'] = S10rwHisto
wbbjets['reweightingHistoFileSysPlus'] = S10rwPlusHisto
wbbjets['reweightingHistoFileSysMinus'] = S10rwMinusHisto


wjetsHT150v2 = copy.deepcopy(mc)
wjetsHT150v2["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140314"
wjetsHT150v2['newMETCollection'] = True
wjetsHT150v2["bins"] = ["8TeV-WJetsToLNu_HT-150To200", "8TeV-WJetsToLNu_HT-200To250", "8TeV-WJetsToLNu_HT-250To300", "8TeV-WJetsToLNu_HT-300To400", "8TeV-WJetsToLNu_HT-400ToInf"] 
wjetsHT150v2["name"] = "WJetsHT150v2" 
wjetsHT150v2['reweightingHistoFile'] = S10rwHisto
wjetsHT150v2['reweightingHistoFileSysPlus'] = S10rwPlusHisto
wjetsHT150v2['reweightingHistoFileSysMinus'] = S10rwMinusHisto

wjetsHT150PDF = copy.deepcopy(mc)
wjetsHT150PDF["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_270414"
wjetsHT150PDF['newMETCollection'] = True
wjetsHT150PDF["bins"] = ["8TeV-WJetsToLNu_HT-150To200-2", "8TeV-WJetsToLNu_HT-200To250-2", "8TeV-WJetsToLNu_HT-250To300-2", "8TeV-WJetsToLNu_HT-300To400-2", "8TeV-WJetsToLNu_HT-400ToInf-2"] 
wjetsHT150PDF["name"] = "WJetsHT150PDF" 
wjetsHT150PDF['reweightingHistoFile'] = S10rwHisto
wjetsHT150PDF['reweightingHistoFileSysPlus'] = S10rwPlusHisto
wjetsHT150PDF['reweightingHistoFileSysMinus'] = S10rwMinusHisto


wjetsToLNuPtW100 = copy.deepcopy(mc)
wjetsToLNuPtW100["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140314"
wjetsToLNuPtW100['newMETCollection'] = True
wjetsToLNuPtW100["bins"] = ["8TeV-WJetsToLNu_PtW-100_TuneZ2star_8TeV_ext-madgraph-tarball"] 
wjetsToLNuPtW100["name"] = "WJetsToLNu_PtW-100_TuneZ2star_8TeV_ext-madgraph-tarball" 
wjetsToLNuPtW100['reweightingHistoFile'] = S10rwHisto
wjetsToLNuPtW100['reweightingHistoFileSysPlus'] = S10rwPlusHisto
wjetsToLNuPtW100['reweightingHistoFileSysMinus'] = S10rwMinusHisto

wjetsToLNuPtW180 = copy.deepcopy(mc)
wjetsToLNuPtW180["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140314"
wjetsToLNuPtW180['newMETCollection'] = True
wjetsToLNuPtW180["bins"] = ["8TeV-WJetsToLNu_PtW-180_TuneZ2star_8TeV-madgraph-tarball"] 
wjetsToLNuPtW180["name"] = "WJetsToLNu_PtW-180_TuneZ2star_8TeV-madgraph-tarball" 
wjetsToLNuPtW180['reweightingHistoFile'] = S10rwHisto
wjetsToLNuPtW180['reweightingHistoFileSysPlus'] = S10rwPlusHisto
wjetsToLNuPtW180['reweightingHistoFileSysMinus'] = S10rwMinusHisto

wjetsToLNuPtW50 = copy.deepcopy(mc)
wjetsToLNuPtW50["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140314"
wjetsToLNuPtW50['newMETCollection'] = True
wjetsToLNuPtW50["bins"] = ["8TeV-WJetsToLNu_PtW-50To70_TuneZ2star_8TeV-madgraph", "8TeV-WJetsToLNu_PtW-70To100_TuneZ2star_8TeV-madgraph", "8TeV-WJetsToLNu_PtW-100_TuneZ2star_8TeV-madgraph"] 
wjetsToLNuPtW50["name"] = "WJetsToLNu_PtW-50_TuneZ2star_8TeV-madgraph" 
wjetsToLNuPtW50['reweightingHistoFile'] = S10rwHisto
wjetsToLNuPtW50['reweightingHistoFileSysPlus'] = S10rwPlusHisto
wjetsToLNuPtW50['reweightingHistoFileSysMinus'] = S10rwMinusHisto


wMinusToLNu = copy.deepcopy(mc)
wMinusToLNu["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140314"
wMinusToLNu['newMETCollection'] = True
wMinusToLNu["bins"] = ["8TeV-WminusToENu", "8TeV-WminusToMuNu", "8TeV-WminusToTauNu-tauola"] 
wMinusToLNu["name"] = "WminusToLNu" 
wMinusToLNu['reweightingHistoFile'] = S10rwHisto
wMinusToLNu['reweightingHistoFileSysPlus'] = S10rwPlusHisto
wMinusToLNu['reweightingHistoFileSysMinus'] = S10rwMinusHisto

wPlusToLNu = copy.deepcopy(mc)
wPlusToLNu["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140314"
wPlusToLNu['newMETCollection'] = True
wPlusToLNu["bins"] = ["8TeV-WplusToENu", "8TeV-WplusToMuNu", "8TeV-WplusToTauNu-tauola"] 
wPlusToLNu["name"] = "WplusToLNu" 
wPlusToLNu['reweightingHistoFile'] = S10rwHisto
wPlusToLNu['reweightingHistoFileSysPlus'] = S10rwPlusHisto
wPlusToLNu['reweightingHistoFileSysPlus'] = S10rwPlusHisto

dy = copy.deepcopy(mc)
dy["bins"] = DY_Bins 
dy["name"] = "DY"
dy['reweightingHistoFile'] = S10rwHisto
dy['reweightingHistoFileSysPlus'] = S10rwPlusHisto
dy['reweightingHistoFileSysMinus'] = S10rwMinusHisto

dyJetsToLLPtZ180 = copy.deepcopy(mc)
dyJetsToLLPtZ180["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140314"
dyJetsToLLPtZ180['newMETCollection'] = True
dyJetsToLLPtZ180["bins"] = ["8TeV-DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball"] 
dyJetsToLLPtZ180["name"] = "DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball" 
dyJetsToLLPtZ180['reweightingHistoFile'] = S10rwHisto
dyJetsToLLPtZ180['reweightingHistoFileSysPlus'] = S10rwPlusHisto
dyJetsToLLPtZ180['reweightingHistoFileSysMinus'] = S10rwMinusHisto

dyJetsToLLPtZ50 = copy.deepcopy(mc)
dyJetsToLLPtZ50["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140314"
dyJetsToLLPtZ50['newMETCollection'] = True
dyJetsToLLPtZ50["bins"] = ["8TeV-DYJetsToLL_PtZ-50To70_TuneZ2star_8TeV-madgraph-tarball", "8TeV-DYJetsToLL_PtZ-70To100_TuneZ2star_8TeV-madgraph-tarball", "8TeV-DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph"] 
dyJetsToLLPtZ50["name"] = "DYJetsToLL_PtZ-50_TuneZ2star_8TeV-madgraph-tarball" 
dyJetsToLLPtZ50['reweightingHistoFile'] = S10rwHisto
dyJetsToLLPtZ50['reweightingHistoFileSysPlus'] = S10rwPlusHisto
dyJetsToLLPtZ50['reweightingHistoFileSysMinus'] = S10rwMinusHisto

dyJetsToLLPtZ50Ext = copy.deepcopy(mc)
dyJetsToLLPtZ50Ext['newMETCollection'] = True
dyJetsToLLPtZ50Ext["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140314"
dyJetsToLLPtZ50Ext["bins"] = ["8TeV-DYJetsToLL_PtZ-50To70_TuneZ2star_8TeV_ext-madgraph-tarball", "8TeV-DYJetsToLL_PtZ-70To100_TuneZ2star_8TeV_ext-madgraph-tarball", "8TeV-DYJetsToLL_PtZ-100_TuneZ2star_8TeV_ext-madgraph-tarball"] 
dyJetsToLLPtZ50Ext["name"] = "8TeV-DYJetsToLL_PtZ-50_TuneZ2star_8TeV_ext-madgraph-tarball" 
dyJetsToLLPtZ50Ext['reweightingHistoFile'] = S10rwHisto
dyJetsToLLPtZ50Ext['reweightingHistoFileSysPlus'] = S10rwPlusHisto
dyJetsToLLPtZ50Ext['reweightingHistoFileSysMinus'] = S10rwMinusHisto


zinv = copy.deepcopy(mc)
zinv["bins"] = ZJetsInv_Bins 
zinv["name"] = "ZJetsInv"
zinv['reweightingHistoFile'] = S10rwHisto
zinv['reweightingHistoFileSysPlus'] = S10rwPlusHisto
zinv['reweightingHistoFileSysMinus'] = S10rwMinusHisto

zJetsToNuNuHT50 = copy.deepcopy(mc)
zJetsToNuNuHT50["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140314"
zJetsToNuNuHT50['newMETCollection'] = True
zJetsToNuNuHT50["bins"] = ["8TeV-ZJetsToNuNu_50_HT_100_TuneZ2Star_8TeV_madgraph", "8TeV-ZJetsToNuNu_100_HT_200_TuneZ2Star_8TeV_madgraph", "8TeV-ZJetsToNuNu_200_HT_400_TuneZ2Star_8TeV_madgraph", "8TeV-ZJetsToNuNu_400_HT_inf_TuneZ2Star_8TeV_madgraph"] 
zJetsToNuNuHT50["name"] = "8TeV-ZJetsToNuNu_50_TuneZ2Star_8TeV_madgraph" 
zJetsToNuNuHT50['reweightingHistoFile'] = S10rwHisto
zJetsToNuNuHT50['reweightingHistoFileSysPlus'] = S10rwPlusHisto
zJetsToNuNuHT50['reweightingHistoFileSysMinus'] = S10rwMinusHisto

zJetsToNuNuHT50Ext = copy.deepcopy(mc)
zJetsToNuNuHT50Ext["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140314"
zJetsToNuNuHT50Ext['newMETCollection'] = True
zJetsToNuNuHT50Ext["bins"] = ["8TeV-ZJetsToNuNu_50_HT_100_TuneZ2Star_8TeV_madgraph_ext", "8TeV-ZJetsToNuNu_100_HT_200_TuneZ2Star_8TeV_madgraph_ext", "8TeV-ZJetsToNuNu_200_HT_400_TuneZ2Star_8TeV_madgraph_ext", "8TeV-ZJetsToNuNu_400_HT_inf_TuneZ2Star_8TeV_madgraph_ext"] 
zJetsToNuNuHT50Ext["name"] = "8TeV-ZJetsToNuNu_50_TuneZ2Star_8TeV_madgraph_ext" 
zJetsToNuNuHT50Ext['reweightingHistoFile'] = S10rwHisto
zJetsToNuNuHT50Ext['reweightingHistoFileSysPlus'] = S10rwPlusHisto
zJetsToNuNuHT50Ext['reweightingHistoFileSysMinus'] = S10rwMinusHisto

singleTop = copy.deepcopy(mc)
singleTop["bins"] = singleTop_Bins 
singleTop["name"] = "singleTop"
singleTop['reweightingHistoFile'] = S10rwHisto
singleTop['reweightingHistoFileSysPlus'] = S10rwPlusHisto
singleTop['reweightingHistoFileSysMinus'] = S10rwMinusHisto

qcd = copy.deepcopy(mc)
qcd["bins"] = QCD_Bins 
qcd["name"] = "QCD"
qcd['reweightingHistoFile'] = S10rwHisto
qcd['reweightingHistoFileSysPlus'] = S10rwPlusHisto
qcd['reweightingHistoFileSysMinus'] = S10rwMinusHisto
#
qcd1 = copy.deepcopy(mc)
qcd1["bins"] = ["8TeV-QCD-Pt20to30-MuEnrichedPt5", "8TeV-QCD-Pt30to50-MuEnrichedPt5",\
                "8TeV-QCD-Pt50to80-MuEnrichedPt5", "8TeV-QCD-Pt80to120-MuEnrichedPt5",\
		"8TeV-QCD-Pt120to170-MuEnrichedPt5", "8TeV-QCD-Pt170to300-MuEnrichedPt5",\
		"8TeV-QCD-Pt300to470-MuEnrichedPt5", "8TeV-QCD-Pt470to600-MuEnrichedPt5"]
qcd1["name"] = "QCD20to600"
qcd1['reweightingHistoFile'] = S10rwHisto
qcd1['reweightingHistoFileSysPlus'] = S10rwPlusHisto
qcd1['reweightingHistoFileSysMinus'] = S10rwMinusHisto
#
qcd1a = copy.deepcopy(mc)
qcd1a["bins"] = ["8TeV-QCD-Pt20to30-MuEnrichedPt5", "8TeV-QCD-Pt30to50-MuEnrichedPt5",\
                "8TeV-QCD-Pt50to80-MuEnrichedPt5", "8TeV-QCD-Pt80to120-MuEnrichedPt5",\
                "8TeV-QCD-Pt120to170-MuEnrichedPt5", "8TeV-QCD-Pt170to300-MuEnrichedPt5"]
qcd1a["name"] = "QCD20to300"
qcd1a['reweightingHistoFile'] = S10rwHisto
qcd1a['reweightingHistoFileSysPlus'] = S10rwPlusHisto
qcd1a['reweightingHistoFileSysMinus'] = S10rwMinusHisto
#
qcd1b = copy.deepcopy(mc)
qcd1b["bins"] = ["8TeV-QCD-Pt300to470-MuEnrichedPt5", "8TeV-QCD-Pt470to600-MuEnrichedPt5"]
qcd1b["name"] = "QCD300to600"
qcd1b['reweightingHistoFile'] = S10rwHisto
qcd1b['reweightingHistoFileSysPlus'] = S10rwPlusHisto
qcd1b['reweightingHistoFileSysMinus'] = S10rwMinusHisto
#
qcd2 = copy.deepcopy(mc)
qcd2["bins"] = ["8TeV-QCD-Pt600to800-MuEnrichedPt5", "8TeV-QCD-Pt800to1000-MuEnrichedPt5"]
qcd2["name"] = "QCD600to1000"
qcd2['reweightingHistoFile'] = S10rwHisto
qcd2['reweightingHistoFileSysPlus'] = S10rwPlusHisto
qcd2['reweightingHistoFileSysMinus'] = S10rwMinusHisto
#
qcd3 = copy.deepcopy(mc)
qcd3["bins"] = ["8TeV-QCD-Pt1000-MuEnrichedPt5"]
qcd3["name"] = "QCD1000"
qcd3['reweightingHistoFile'] = S10rwHisto
qcd3['reweightingHistoFileSysPlus'] = S10rwPlusHisto
qcd3['reweightingHistoFileSysMinus'] = S10rwMinusHisto
#####
#iqcd1 = copy.deepcopy(mc)
#iqcd1["bins"] = ["8TeV-QCD_Pt-30to50", "8TeV-QCD_Pt-50to80", "8TeV-QCD_Pt-80to120",\
#                 "8TeV-QCD_Pt-120to170", "8TeV-QCD_Pt-170to300"]
#iqcd1["name"] = "iQCD30to300"
##
#iqcd2 = copy.deepcopy(mc)
#iqcd2["bins"] = ["8TeV-QCD_Pt-300to470", "8TeV-QCD_Pt-470to600"]
#iqcd2["name"] = "iQCD300to600"
##
#iqcd3 = copy.deepcopy(mc)
#iqcd3["bins"] = ["8TeV-QCD_Pt-600to800", "8TeV-QCD_Pt-800to1000"]
#iqcd3["name"] = "iQCD600to1000"
##
#iqcd4 = copy.deepcopy(mc)
#iqcd4["bins"] = ["8TeV-QCD_Pt-1000to1400", "8TeV-QCD_Pt-1400to1800", "8TeV-QCD_Pt-1800"]
#iqcd4["name"] = "iQCD1000"
#
ww = copy.deepcopy(mc)
ww["bins"] = ["8TeV-WW"]
ww["name"] = "WW"
ww['reweightingHistoFile'] = S10rwHisto
ww['reweightingHistoFileSysPlus'] = S10rwPlusHisto
ww['reweightingHistoFileSysMinus'] = S10rwMinusHisto

wz = copy.deepcopy(mc)
wz["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140314/"
wz['newMETCollection'] = True
wz["bins"] = ["8TeV-WZ"]
wz["name"] = "WZ"
wz['reweightingHistoFile'] = S10rwHisto
wz['reweightingHistoFileSysPlus'] = S10rwPlusHisto
wz['reweightingHistoFileSysMinus'] = S10rwMinusHisto

zz = copy.deepcopy(mc)
zz["bins"] = ["8TeV-ZZ"]
zz['newMETCollection'] = True
zz["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140314/"
zz["name"] = "ZZ"
zz['reweightingHistoFile'] = S10rwHisto
zz['reweightingHistoFileSysPlus'] = S10rwPlusHisto
zz['reweightingHistoFileSysMinus'] = S10rwMinusHisto

ttw = copy.deepcopy(mc)
ttw["bins"] = ["8TeV-TTWJets"]
ttw["name"] = "TTWJets"
ttw['reweightingHistoFile'] = S10rwHisto
ttw['reweightingHistoFileSysPlus'] = S10rwPlusHisto
ttw['reweightingHistoFileSysMinus'] = S10rwMinusHisto

