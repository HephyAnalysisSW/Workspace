import copy
allSamples = []

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
#
#mc["bins"] =  ["8TeV-TTJets"]
#mc["bins"].extend(QCD_Bins)
#mc["bins"].extend(WJets_Bins)
#mc["bins"].extend(DY_Bins)
#mc["bins"].extend(singleTop_Bins)
#allSamples.append(mc)
#
ttbar = copy.deepcopy(mc)
ttbar["bins"] = ["8TeV-TTJets"]
ttbar["name"] = "TTJets" 
#
#ttbarPowHeg = copy.deepcopy(mc)
#ttbarPowHeg["dirname"] = "/data/mhickel/pat_130328/"
#ttbarPowHeg["bins"] = ["8TeV-TTJets-powheg-v1+2"]
#ttbarPowHeg["name"] = "TTJets-PowHeg" 
#

wjets = copy.deepcopy(mc)
wjets["bins"] = WJets_Bins 
wjets["name"] = "WJetsHT250" 

#wjets["dirname"] = "/data/mhickel/pat_120917_S10/mc8TeV/"
wjetsInc = copy.deepcopy(wjets)
wjetsInc["bins"] = ["8TeV-WJetsToLNu-3"] 
wjetsInc["name"] = "WJetsToLNu" 

w1jets = copy.deepcopy(wjets)
w1jets["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_131028" 
w1jets["bins"] = ["8TeV-W1JetsToLNu"] 
w1jets["name"] = "W1JetsToLNu"

w2jets = copy.deepcopy(w1jets)
w2jets["bins"] = ["8TeV-W2JetsToLNu"] 
w2jets["name"] = "W2JetsToLNu"

w3jets = copy.deepcopy(w1jets)
w3jets["bins"] = ["8TeV-W3JetsToLNu"] 
w3jets["name"] = "W3JetsToLNu"

w4jets = copy.deepcopy(w1jets)
w4jets["bins"] = ["8TeV-W4JetsToLNu"] 
w4jets["name"] = "W4JetsToLNu"
 
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
#wbbjets = copy.deepcopy(wjets)
#wbbjets["bins"]=["8TeV-WbbJetsToLNu"]
#wbbjets["name"] = "WbbJets"
#
#
dy = copy.deepcopy(mc)
dy["bins"] = DY_Bins 
dy["name"] = "DY"

zinv = copy.deepcopy(mc)
zinv["bins"] = ZJetsInv_Bins 
zinv["name"] = "ZJetsInv"

tops = copy.deepcopy(mc)
tops["bins"] = singleTop_Bins 
tops["name"] = "singleTop"

qcd = copy.deepcopy(mc)
qcd["bins"] = QCD_Bins 
qcd["name"] = "QCD"
#
qcd1 = copy.deepcopy(mc)
qcd1["bins"] = ["8TeV-QCD-Pt20to30-MuEnrichedPt5", "8TeV-QCD-Pt30to50-MuEnrichedPt5",\
                "8TeV-QCD-Pt50to80-MuEnrichedPt5", "8TeV-QCD-Pt80to120-MuEnrichedPt5",\
		"8TeV-QCD-Pt120to170-MuEnrichedPt5", "8TeV-QCD-Pt170to300-MuEnrichedPt5",\
		"8TeV-QCD-Pt300to470-MuEnrichedPt5", "8TeV-QCD-Pt470to600-MuEnrichedPt5"]
qcd1["name"] = "QCD20to600"
#
qcd1a = copy.deepcopy(mc)
qcd1a["bins"] = ["8TeV-QCD-Pt20to30-MuEnrichedPt5", "8TeV-QCD-Pt30to50-MuEnrichedPt5",\
                "8TeV-QCD-Pt50to80-MuEnrichedPt5", "8TeV-QCD-Pt80to120-MuEnrichedPt5",\
                "8TeV-QCD-Pt120to170-MuEnrichedPt5", "8TeV-QCD-Pt170to300-MuEnrichedPt5"]
qcd1a["name"] = "QCD20to300"
#
qcd1b = copy.deepcopy(mc)
qcd1b["bins"] = ["8TeV-QCD-Pt300to470-MuEnrichedPt5", "8TeV-QCD-Pt470to600-MuEnrichedPt5"]
qcd1b["name"] = "QCD300to600"
#
qcd2 = copy.deepcopy(mc)
qcd2["bins"] = ["8TeV-QCD-Pt600to800-MuEnrichedPt5", "8TeV-QCD-Pt800to1000-MuEnrichedPt5"]
qcd2["name"] = "QCD600to1000"
#
qcd3 = copy.deepcopy(mc)
qcd3["bins"] = ["8TeV-QCD-Pt1000-MuEnrichedPt5"]
qcd3["name"] = "QCD1000"
####
iqcd1 = copy.deepcopy(mc)
iqcd1["bins"] = ["8TeV-QCD_Pt-30to50", "8TeV-QCD_Pt-50to80", "8TeV-QCD_Pt-80to120",\
                 "8TeV-QCD_Pt-120to170", "8TeV-QCD_Pt-170to300"]
iqcd1["name"] = "iQCD30to300"
#
iqcd2 = copy.deepcopy(mc)
iqcd2["bins"] = ["8TeV-QCD_Pt-300to470", "8TeV-QCD_Pt-470to600"]
iqcd2["name"] = "iQCD300to600"
#
iqcd3 = copy.deepcopy(mc)
iqcd3["bins"] = ["8TeV-QCD_Pt-600to800", "8TeV-QCD_Pt-800to1000"]
iqcd3["name"] = "iQCD600to1000"
#
iqcd4 = copy.deepcopy(mc)
iqcd4["bins"] = ["8TeV-QCD_Pt-1000to1400", "8TeV-QCD_Pt-1400to1800", "8TeV-QCD_Pt-1800"]
iqcd4["name"] = "iQCD1000"
#
ww = copy.deepcopy(mc)
ww["bins"] = ["8TeV-WW"]
ww["name"] = "WW"
####
sigTest = copy.deepcopy(mc)
sigTest["dirname"] = "/data/imikulec/testmc/"
sigTest["bins"] = ["8TeV-stop300-LSP270"]
sigTest["name"] = "S300N270"

sigFullSimTest = copy.deepcopy(mc)
sigFullSimTest["dirname"] = "/data/schoef/pat_131021/"
sigFullSimTest["bins"] = ["8TeV-stop300-LSP270-FullSim"]
sigFullSimTest["name"] = "S300N270FullSim"
####

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

stop300lsp270g200FastSim = copy.deepcopy(mc)
stop300lsp270g200FastSim["dirname"] = "/data/schoef/monoJetSignals/SUSYTupelizer/FastSim"
stop300lsp270g200FastSim["bins"] = ["8TeV-stop300lsp270g200"]
stop300lsp270g200FastSim["name"] = "stop300lsp270g200FastSim"
