import copy, os, sys
allSamples = []

path = os.path.abspath('../../HEPHYCommonTools/python')
if not path in sys.path:
    sys.path.insert(1, path)
del path
from createPUReweightingHisto import getPUReweightingUncertainty

S10rwHisto = getPUReweightingUncertainty("S10", dataFile = "/data/schoef/results2012/PU/MyDataPileupHistogram_Run2012ABCD_60max_true_pixelcorr_Sys0.root")
S10rwPlusHisto = getPUReweightingUncertainty("S10", dataFile = "/data/schoef/results2012/PU/MyDataPileupHistogram_Run2012ABCD_60max_true_pixelcorr_SysPlus5.root")
S10rwMinusHisto = getPUReweightingUncertainty("S10", dataFile = "/data/schoef/results2012/PU/MyDataPileupHistogram_Run2012ABCD_60max_true_pixelcorr_SysMinus5.root")

data={}
data["name"]     = "data";
data["dirname"] = "/data/mhickel/pat_130531/"
data["bins"]    = ["MET-Run2012A-13Jul2012","MET-Run2012B-13Jul2012","MET-Run2012C-Aug24ReReco","MET-Run2012C-PromptReco-v2", "MET-Run2012D-PromptReco"]
data["Chain"] = "Events"
data["Counter"] = "bool_EventCounter_passed_PAT.obj"
allSamples.append(data)

mc={}
mc["name"]     = "mc";
mc["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/mhickel/pat_130527"
mc["Chain"] = "Events"
#mc["reweightingHistoFile"]          = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S10-Run2012ABCD_60max_true_pixelcorr_Sys0.root"
#mc["reweightingHistoFileSysPlus"]   = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S10-Run2012ABCD_60max_true_pixelcorr_SysPlus5.root"
#mc["reweightingHistoFileSysMinus"]  = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S10-Run2012ABCD_60max_true_pixelcorr_SysMinus5.root"

QCD_Bins = \
  ["8TeV-QCD-Pt1000-MuEnrichedPt5", "8TeV-QCD-Pt120to170-MuEnrichedPt5", "8TeV-QCD-Pt170to300-MuEnrichedPt5",\
   "8TeV-QCD-Pt20to30-MuEnrichedPt5", "8TeV-QCD-Pt300to470-MuEnrichedPt5", "8TeV-QCD-Pt30to50-MuEnrichedPt5",\
   "8TeV-QCD-Pt470to600-MuEnrichedPt5", "8TeV-QCD-Pt50to80-MuEnrichedPt5",\
   "8TeV-QCD-Pt600to800-MuEnrichedPt5", "8TeV-QCD-Pt800to1000-MuEnrichedPt5", "8TeV-QCD-Pt80to120-MuEnrichedPt5"]

WJets_Bins = ["8TeV-WJets-HT250to300", "8TeV-WJets-HT300to400", "8TeV-WJets-HT400"]
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
ttbar['reweightingHistoFile'] = S10rwHisto
ttbar['reweightingHistoFileSysPlus'] = S10rwPlusHisto
ttbar['reweightingHistoFileSysMinus'] = S10rwMinusHisto
#
#ttbarPowHeg = copy.deepcopy(mc)
#ttbarPowHeg["dirname"] = "/data/mhickel/pat_130328/"
#ttbarPowHeg["bins"] = ["8TeV-TTJets-powheg-v1+2"]
#ttbarPowHeg["name"] = "TTJets-PowHeg" 

wjets = copy.deepcopy(mc)
wjets["bins"] = WJets_Bins 
wjets["name"] = "WJetsHT250" 
wjets['reweightingHistoFile'] = S10rwHisto
wjets['reweightingHistoFileSysPlus'] = S10rwPlusHisto
wjets['reweightingHistoFileSysMinus'] = S10rwMinusHisto

#wjets["dirname"] = "/data/mhickel/pat_120917_S10/mc8TeV/"
wjetsInc = copy.deepcopy(wjets)
wjetsInc["bins"] = ["8TeV-WJetsToLNu-3"] 
wjetsInc["name"] = "WJetsToLNu" 
wjetsInc['reweightingHistoFile'] = S10rwHisto
wjetsInc['reweightingHistoFileSysPlus'] = S10rwPlusHisto
wjetsInc['reweightingHistoFileSysMinus'] = S10rwMinusHisto

w1jets = copy.deepcopy(wjets)
w1jets["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_131028" 
w1jets["bins"] = ["8TeV-W1JetsToLNu"] 
w1jets["name"] = "W1JetsToLNu"
w1jets['reweightingHistoFile'] = S10rwHisto
w1jets['reweightingHistoFileSysPlus'] = S10rwPlusHisto
w1jets['reweightingHistoFileSysMinus'] = S10rwMinusHisto

w2jets = copy.deepcopy(w1jets)
w2jets["bins"] = ["8TeV-W2JetsToLNu"] 
w2jets["name"] = "W2JetsToLNu"
w2jets['reweightingHistoFile'] = S10rwHisto
w2jets['reweightingHistoFileSysPlus'] = S10rwPlusHisto
w2jets['reweightingHistoFileSysMinus'] = S10rwMinusHisto

w3jets = copy.deepcopy(w1jets)
w3jets["bins"] = ["8TeV-W3JetsToLNu"] 
w3jets["name"] = "W3JetsToLNu"
w3jets['reweightingHistoFile'] = S10rwHisto
w3jets['reweightingHistoFileSysPlus'] = S10rwPlusHisto
w3jets['reweightingHistoFileSysMinus'] = S10rwMinusHisto

w4jets = copy.deepcopy(w1jets)
w4jets["bins"] = ["8TeV-W4JetsToLNu"] 
w4jets["name"] = "W4JetsToLNu"
w4jets['reweightingHistoFile'] = S10rwHisto
w4jets['reweightingHistoFileSysPlus'] = S10rwPlusHisto
w4jets['reweightingHistoFileSysMinus'] = S10rwMinusHisto

wbbjets = copy.deepcopy(wjets)
wbbjets["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140212"
wbbjets["bins"]=["8TeV-WbbJetsToLNu"]
wbbjets["name"] = "WbbJets"
wbbjets['reweightingHistoFile'] = S10rwHisto
wbbjets['reweightingHistoFileSysPlus'] = S10rwPlusHisto
wbbjets['reweightingHistoFileSysMinus'] = S10rwMinusHisto
 
dy = copy.deepcopy(mc)
dy["bins"] = DY_Bins 
dy["name"] = "DY"
dy['reweightingHistoFile'] = S10rwHisto
dy['reweightingHistoFileSysPlus'] = S10rwPlusHisto
dy['reweightingHistoFileSysMinus'] = S10rwMinusHisto

zinv = copy.deepcopy(mc)
zinv["bins"] = ZJetsInv_Bins 
zinv["name"] = "ZJetsInv"
zinv['reweightingHistoFile'] = S10rwHisto
zinv['reweightingHistoFileSysPlus'] = S10rwPlusHisto
zinv['reweightingHistoFileSysMinus'] = S10rwMinusHisto

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

#
#wjetsCombined = copy.deepcopy(wjets)
#wjetsCombined["bins"]+=wjetsInc["bins"]
#wjetsCombined["name"] = "WJetsCombined"
#wjetsCombined["additionalCut"] = {"8TeV-WJetsToLNu":"ht<325", "8TeV-WJets-HT250to300":"ht>=325"}
#wjetsCombined["scaleFac"] = {"8TeV-WJetsToLNu":0.8851333125242441}
#
#wbbjetsCombined = copy.deepcopy(wjets)
#wbbjetsCombined["bins"]+=["8TeV-WbbJetsToLNu"]
#wbbjetsCombined["name"] = "WbbJetsCombined"
#wbbjetsCombined["additionalCut"] = {"8TeV-WbbJetsToLNu":"nbjets>0&&ht>300", "8TeV-WJets-HT250to300":"nbjets==0", "8TeV-WJets-HT300to400":"nbjets==0", "8TeV-WJets-HT400":"nbjets==0"}
#
#
#
#####
#sigTest = copy.deepcopy(mc)
#sigTest["dirname"] = "/data/imikulec/testmc/"
#sigTest["bins"] = ["8TeV-stop300-LSP270"]
#sigTest["name"] = "S300N270"
#
#sigFullSimTest = copy.deepcopy(mc)
#sigFullSimTest["dirname"] = "/data/schoef/pat_131021/"
#sigFullSimTest["bins"] = ["8TeV-stop300-LSP270-FullSim"]
#sigFullSimTest["name"] = "S300N270FullSim"
#####

stop200lsp170g100FastSim = copy.deepcopy(mc)
stop200lsp170g100FastSim["dirname"] = "/data/schoef/monoJetSignals/SUSYTupelizer/FastSim"
stop200lsp170g100FastSim["bins"] = ["8TeV-stop200lsp170g100"]
stop200lsp170g100FastSim["name"] = "stop200lsp170g100FastSim"

stop300lsp240g150FastSim = copy.deepcopy(mc)
stop300lsp240g150FastSim["dirname"] = "/data/schoef/monoJetSignals/SUSYTupelizer/FastSim"
stop300lsp240g150FastSim["bins"] = ["8TeV-stop300lsp240g150"]
stop300lsp240g150FastSim["name"] = "stop300lsp240g150FastSim"

stop300lsp270g175FastSim = copy.deepcopy(mc)
stop300lsp270g175FastSim["dirname"] = "/data/schoef/monoJetSignals/SUSYTupelizer/FastSim"
stop300lsp270g175FastSim["bins"] = ["8TeV-stop300lsp270g175"]
stop300lsp270g175FastSim["name"] = "stop300lsp270g175FastSim"

stop300lsp270FastSim = copy.deepcopy(mc)
stop300lsp270FastSim["dirname"] = "/data/schoef/monoJetSignals/SUSYTupelizer/FastSim"
stop300lsp270FastSim["bins"] = ["8TeV-stop300lsp270"]
stop300lsp270FastSim["name"] = "stop300lsp270FastSim"

stop300lsp270g200FastSim = copy.deepcopy(mc)
stop300lsp270g200FastSim["dirname"] = "/data/schoef/monoJetSignals/SUSYTupelizer/FastSim"
stop300lsp270g200FastSim["bins"] = ["8TeV-stop300lsp270g200"]
stop300lsp270g200FastSim["name"] = "stop300lsp270g200FastSim"

stop200lsp170g100FullSim = copy.deepcopy(mc)
stop200lsp170g100FullSim["dirname"] = "/data/schoef/monoJetSignals/SUSYTupelizer/FullSim"
stop200lsp170g100FullSim["bins"] = ["8TeV-stop200lsp170g100"]
stop200lsp170g100FullSim["name"] = "stop200lsp170g100FullSim"

stop300lsp240g150FullSim = copy.deepcopy(mc)
stop300lsp240g150FullSim["dirname"] = "/data/schoef/monoJetSignals/SUSYTupelizer/FullSim"
stop300lsp240g150FullSim["bins"] = ["8TeV-stop300lsp240g150"]
stop300lsp240g150FullSim["name"] = "stop300lsp240g150FullSim"

stop300lsp270g175FullSim = copy.deepcopy(mc)
stop300lsp270g175FullSim["dirname"] = "/data/schoef/monoJetSignals/SUSYTupelizer/FullSim"
stop300lsp270g175FullSim["bins"] = ["8TeV-stop300lsp270g175"]
stop300lsp270g175FullSim["name"] = "stop300lsp270g175FullSim"

stop300lsp270FullSim = copy.deepcopy(mc)
stop300lsp270FullSim["dirname"] = "/data/schoef/monoJetSignals/SUSYTupelizer/FullSim"
stop300lsp270FullSim["bins"] = ["8TeV-stop300lsp270"]
stop300lsp270FullSim["name"] = "stop300lsp270FullSim"

stop300lsp270g200FullSim = copy.deepcopy(mc)
stop300lsp270g200FullSim["dirname"] = "/data/schoef/monoJetSignals/SUSYTupelizer/FullSim"
stop300lsp270g200FullSim["bins"] = ["8TeV-stop300lsp270g200"]
stop300lsp270g200FullSim["name"] = "stop300lsp270g200FullSim"

for s in [stop200lsp170g100FastSim, stop300lsp240g150FastSim, stop300lsp270g175FastSim, stop300lsp270FastSim, stop300lsp270g200FastSim, stop200lsp170g100FullSim, stop300lsp240g150FullSim, stop300lsp270g175FullSim, stop300lsp270FullSim, stop300lsp270g200FullSim]:
  s['reweightingHistoFile'] = S10rwHisto
  s['reweightingHistoFileSysPlus'] = S10rwPlusHisto
  s['reweightingHistoFileSysMinus'] = S10rwMinusHisto
