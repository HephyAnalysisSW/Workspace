import copy
allSamples = []

data={}
data["name"]     = "data";
data["dirname"] = "/data/mhickel/pat_130412/"
data["bins"]    = ["MuHad-Run2012A-13Jul2012","MuHad-Run2012B-13Jul2012","MuHad-Run2012C-Aug24ReReco","MuHad-Run2012C-PromptReco-v2", "MuHad-Run2012D-PromptReco"]
data["Chain"] = "Events"
data["Counter"] = "bool_EventCounter_passed_PAT.obj"
allSamples.append(data)

data11fb={}
data11fb["name"]     = "data";
data11fb["dirname"] = "/data/mhickel/pat_121207/data8TeV/"
data11fb["bins"]    = ['MuHad-Run2012A-13Jul2012', 'MuHad-Run2012B-13Jul2012', 'MuHad-Run2012C-Aug24ReReco', 'MuHad-Run2012C-PromptReco-v2']
data11fb["Chain"] = "Events"
data11fb["Counter"] = "bool_EventCounter_passed_PAT.obj"
allSamples.append(data)

singleLeptonData={}
singleLeptonData["name"]     = "singleMuData";
singleLeptonData["dirname"] = "/data/mhickel/pat_121207/"
singleLeptonData["bins"]    = [  'SingleMu-Run2012A-13Jul2012', 'SingleMu-Run2012B-13Jul2012', 'SingleMu-Run2012C-PromptReco-v2', 'SingleMu-Run2012C-Aug24ReReco', 'SingleMu-Run2012D-PromptReco']
singleLeptonData["Chain"] = "Events"
singleLeptonData["Counter"] = "bool_EventCounter_passed_PAT.obj"

#doubleMuData={}
#doubleMuData["name"]     = "doubleMuData";
#doubleMuData["dirname"] = "/data/schoef/pat_120816/data8TeV/"
#doubleMuData["bins"]    = [ 'DoubleMu-Run2012A-PromptReco', 'DoubleMu-Run2012B-PromptReco']
#doubleMuData["Chain"] = "Events"
#doubleMuData["Counter"] = "bool_EventCounter_passed_PAT.obj"

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
allSamples.append(mc)

ttbar = copy.deepcopy(mc)
ttbar["bins"] = ["8TeV-TTJets"]
ttbar["name"] = "TTJets" 

ttbarScaleDown = copy.deepcopy(mc)
ttbarScaleDown["dirname"] = "/data/mhickel/pat_120917/mc8TeV/"
ttbarScaleDown["bins"] = ["8TeV-TTJets_scaledown_TuneZ2star"]
ttbarScaleDown["name"] = "TTJetsScaleDown"
ttbarScaleUp = copy.deepcopy(mc)
ttbarScaleUp["dirname"] = "/data/mhickel/pat_120917/mc8TeV/"
ttbarScaleUp["bins"] = ["8TeV-TTJets_scaleup_TuneZ2star"]
ttbarScaleUp["name"] = "TTJetsScaleUp"
ttbarMatchingDown = copy.deepcopy(mc)
ttbarMatchingDown["dirname"] = "/data/mhickel/pat_120917/mc8TeV/"
ttbarMatchingDown["bins"] = ["8TeV-TTJets_matchingdown_TuneZ2star"]
ttbarMatchingDown["name"] = "TTJetsMatchingDown"
ttbarMatchingUp = copy.deepcopy(mc)
ttbarMatchingUp["dirname"] = "/data/mhickel/pat_120917/mc8TeV/"
ttbarMatchingUp["bins"] = ["8TeV-TTJets_matchingup_TuneZ2star"]
ttbarMatchingUp["name"] = "TTJetsMatchingUp"

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

