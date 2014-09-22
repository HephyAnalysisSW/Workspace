import copy
HTdata={}
HTdata["name"]     = "HTData";
HTdata["dirname"] = "/data/mhickel/pat_121207/"
HTdata["bins"]    = ['HT-Run2012A-13Jul2012','JetHT-Run2012B-13Jul2012','JetHT-Run2012C-Aug24ReReco','JetHT-Run2012C-PromptReco-v2','JetHT-Run2012D-PromptReco']
HTdata["Chain"] = "Events"
HTdata["Counter"] = "bool_EventCounter_passed_PAT.obj"
HTdata["specialCuts"] = []
HTdata["hasWeight"] = False


QCDHad_Bins = ["8TeV-QCD_Pt-1000to1400","8TeV-QCD_Pt-120to170","8TeV-QCD_Pt-1400to1800","8TeV-QCD_Pt-170to300","8TeV-QCD_Pt-1800","8TeV-QCD_Pt-300to470","8TeV-QCD_Pt-30to50","8TeV-QCD_Pt-470to600","8TeV-QCD_Pt-50to80",
#  "8TeV-QCD_Pt-600to800",#FIXME
  "8TeV-QCD_Pt-800to1000","8TeV-QCD_Pt-80to120"]

qcdHad = copy.deepcopy(HTdata)
qcdHad["dirname"] = "/data/mhickel/pat_120917/mc8TeV/"
qcdHad["bins"] = QCDHad_Bins
qcdHad["name"] = "QCDHad"

mc={}
mc["name"]     = "mc";
mc["dirname"] = "/data/schoef/pat_130517/"
mc["Chain"] = "Events"
QCD_Bins = \
  ["8TeV-QCD-Pt1000-MuEnrichedPt5", "8TeV-QCD-Pt120to170-MuEnrichedPt5", "8TeV-QCD-Pt170to300-MuEnrichedPt5",
   "8TeV-QCD-Pt20to30-MuEnrichedPt5", "8TeV-QCD-Pt300to470-MuEnrichedPt5", "8TeV-QCD-Pt30to50-MuEnrichedPt5", "8TeV-QCD-Pt470to600-MuEnrichedPt5", "8TeV-QCD-Pt50to80-MuEnrichedPt5",
   "8TeV-QCD-Pt600to800-MuEnrichedPt5", "8TeV-QCD-Pt800to1000-MuEnrichedPt5", "8TeV-QCD-Pt80to120-MuEnrichedPt5"]

WJets_Bins = ["8TeV-WJets-HT250to300", "8TeV-WJets-HT300to400", "8TeV-WJets-HT400"]

DY_Bins = ["8TeV-DYJetsToLL-M10to50", "8TeV-DYJetsToLL-M50"]
ZJets_Bins = DY_Bins

singleTop_Bins = ["8TeV-T-t", "8TeV-T-s", "8TeV-T-tW", "8TeV-Tbar-t", "8TeV-Tbar-s", "8TeV-Tbar-tW"]

mc["bins"] =  ["8TeV-TTJets"]
mc["bins"].extend(QCD_Bins)
mc["bins"].extend(WJets_Bins)
mc["bins"].extend(DY_Bins)
mc["bins"].extend(singleTop_Bins)

ttbar = copy.deepcopy(mc)
ttbar["bins"] = ["8TeV-TTJets"]
ttbar["name"] = "TTJets"

ttbarPowHeg = copy.deepcopy(mc)
ttbarPowHeg["dirname"] = "/data/schoef/pat_130517/"
ttbarPowHeg["bins"] = ["8TeV-TTJets-powheg-v1+2"]
ttbarPowHeg["name"] = "TTJets-PowHeg"

wjets = copy.deepcopy(mc)
wjets["bins"] = WJets_Bins 
wjets["name"] = "WJetsHT250" 
wjets["dirname"] = "/data/schoef/pat_130517/"
wjetsInc = copy.deepcopy(wjets)
wjetsInc["bins"] = ["8TeV-WJetsToLNu"]
wjetsInc["name"] = "WJetsToLNu"

wjetsCombined = copy.deepcopy(wjets)
wjetsCombined["bins"]+=wjetsInc["bins"]
wjetsCombined["name"] = "WJetsCombined"
wjetsCombined["additionalCut"] = {"8TeV-WJetsToLNu":"ht<325", "8TeV-WJets-HT250to300":"ht>=325"}
wjetsCombined["scaleFac"] = {"8TeV-WJetsToLNu":0.8851333125242441}

wbbjetsCombined = copy.deepcopy(wjets)
wbbjetsCombined["bins"]+=["8TeV-WbbJetsToLNu"]
wbbjetsCombined["name"] = "WbbJetsCombined"
wbbjetsCombined["additionalCut"] = {"8TeV-WbbJetsToLNu":"nbjets>0&&ht>300", "8TeV-WJets-HT250to300":"nbjets==0", "8TeV-WJets-HT300to400":"nbjets==0", "8TeV-WJets-HT400":"nbjets==0"}


wbbjets = copy.deepcopy(wjets)
wbbjets["bins"]=["8TeV-WbbJetsToLNu"]
wbbjets["name"] = "WbbJets"

ttbarPowHeg = copy.deepcopy(mc)
ttbarPowHeg["dirname"] = "/data/schoef/pat_130517/"
ttbarPowHeg["bins"] = ["8TeV-TTJets-powheg-v1+2"]
ttbarPowHeg["name"] = "TTJets-PowHeg"

wjets = copy.deepcopy(mc)
wjets["bins"] = WJets_Bins
wjets["name"] = "WJetsHT250"
wjets["dirname"] = "/data/schoef/pat_130517/"
wjetsInc = copy.deepcopy(wjets)
wjetsInc["bins"] = ["8TeV-WJetsToLNu"]
wjetsInc["name"] = "WJetsToLNu"

wjetsCombined = copy.deepcopy(wjets)
wjetsCombined["bins"]+=wjetsInc["bins"]
wjetsCombined["name"] = "WJetsCombined"
wjetsCombined["additionalCut"] = {"8TeV-WJetsToLNu":"ht<325", "8TeV-WJets-HT250to300":"ht>=325"}
wjetsCombined["scaleFac"] = {"8TeV-WJetsToLNu":0.8851333125242441}

wbbjetsCombined = copy.deepcopy(wjets)
wbbjetsCombined["bins"]+=["8TeV-WbbJetsToLNu"]
wbbjetsCombined["name"] = "WbbJetsCombined"
wbbjetsCombined["additionalCut"] = {"8TeV-WbbJetsToLNu":"nbjets>0&&ht>300", "8TeV-WJets-HT250to300":"nbjets==0", "8TeV-WJets-HT300to400":"nbjets==0", "8TeV-WJets-HT400":"nbjets==0"}

wbbjets = copy.deepcopy(wjets)
wbbjets["bins"]=["8TeV-WbbJetsToLNu"]
wbbjets["name"] = "WbbJets"


dy = copy.deepcopy(mc)
dy["bins"] = DY_Bins
dy["name"] = "DY"
stop = copy.deepcopy(mc)
stop["bins"] = singleTop_Bins
stop["name"] = "singleTop"
qcd = copy.deepcopy(mc)
qcd["bins"] = QCD_Bins
qcd["name"] = "QCD"

ttwJets = copy.deepcopy(mc)
ttwJets["dirname"] = "/data/schoef/pat_130517/"
ttwJets["bins"] = ["8TeV-TTWJets"]
ttwJets["name"] = "TTWJets"

ttzJets = copy.deepcopy(mc)
ttzJets["dirname"] = "/data/schoef/pat_130517/"
ttzJets["bins"] = ["8TeV-TTZJets"]
ttzJets["name"] = "TTZJets"

ttvJets = copy.deepcopy(mc)
ttvJets["dirname"] = "/data/schoef/pat_130517/"
ttvJets["bins"] = ["8TeV-TTZJets", "8TeV-TTWJets"]
ttvJets["name"] = "TTVJets"

zToNuNu=copy.deepcopy(mc) 
zToNuNu["name"] = "ZToNuNu" 
zToNuNu["dirname"] = "/data/mhickel/pat_130714/" 
zToNuNu["specialCuts"] = [] 
zToNuNu["bins"] = ["8TeV-ZJetsToNuNu-HT100to200", "8TeV-ZJetsToNuNu-HT200to400", "8TeV-ZJetsToNuNu-HT400",  "8TeV-ZJetsToNuNu-HT50to100"] 

