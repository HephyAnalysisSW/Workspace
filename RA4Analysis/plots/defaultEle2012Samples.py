import copy
allSamples=[]

data={}
data["name"]     = "data";
data["dirname"] = "/data/mhickel/pat_130412/"
data["bins"]    = ["ElectronHad-Run2012A-13Jul2012","ElectronHad-Run2012B-13Jul2012","ElectronHad-Run2012C-Aug24ReReco","ElectronHad-Run2012C-PromptReco-v2", "ElectronHad-Run2012D-PromptReco"]
data["Chain"] = "Events"
data["Counter"] = "bool_EventCounter_passed_PAT.obj"
allSamples.append(data)

data11fb={}
data11fb["name"]     = "data";
data11fb["dirname"] = "/data/mhickel/pat_121207/data8TeV/"
data11fb["bins"]    = ['ElectronHad-Run2012A-13Jul2012', 'ElectronHad-Run2012B-13Jul2012', 'ElectronHad-Run2012C-PromptReco-v2', 'ElectronHad-Run2012C-PromptReco']
data11fb["Chain"] = "Events"
data11fb["Counter"] = "bool_EventCounter_passed_PAT.obj"

singleLeptonData={}
singleLeptonData["name"]     = "singleEleData";
singleLeptonData["dirname"] = "/data/mhickel/pat_121207/"
singleLeptonData["bins"]    = [  'SingleElectron-Run2012A-13Jul2012', 'SingleElectron-Run2012B-13Jul2012', 'SingleElectron-Run2012C-PromptReco-v2', 'SingleElectron-Run2012C-Aug24ReReco', 'SingleElectron-Run2012D-PromptReco']
singleLeptonData["Chain"] = "Events"
singleLeptonData["Counter"] = "bool_EventCounter_passed_PAT.obj"


doubleEleData={}
doubleEleData["name"]     = "doubleEleData";
doubleEleData["dirname"] = "/data/schoef/pat_120816/data8TeV/"
doubleEleData["bins"]    = [ 'DoubleElectron-Run2012A-PromptReco', 'DoubleElectron-Run2012B-PromptReco']
doubleEleData["Chain"] = "Events"
doubleEleData["Counter"] = "bool_EventCounter_passed_PAT.obj"

allSamples.append(data)
mc={}
mc["name"]     = "mc";
mc["dirname"] = "/data/schoef/pat_130517/"
mc["Chain"] = "Events"
mc["Counter"] = "bool_EventCounter_passed_PAT.obj"
mc["specialCuts"] = []

QCD_Bins =  ["8TeV-QCD_BCtoE_Pt_170_250", "8TeV-QCD_BCtoE_Pt_20_30", "8TeV-QCD_BCtoE_Pt_250_350", "8TeV-QCD_BCtoE_Pt_30_80", "8TeV-QCD_BCtoE_Pt_350", "8TeV-QCD_BCtoE_Pt_80_170", "8TeV-QCD_EMEnriched_Pt_170_250", "8TeV-QCD_EMEnriched_Pt_20_30", "8TeV-QCD_EMEnriched_Pt_250_350", "8TeV-QCD_EMEnriched_Pt_30_80", "8TeV-QCD_EMEnriched_Pt_350", "8TeV-QCD_EMEnriched_Pt_80_170"]

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
wjetsCombined["scaleFac"] = {"8TeV-WJetsToLNu":0.87565035713284523}

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

#c.Add("/data/schoef/convertedTuples_v16/copyMET/Ele/WJetsHT250/h*.root")
#d.Add("/data/schoef/convertedTuples_v16/copyMET/Ele/WJetsToLNu/histo_WJetsToLNu.root")
#c.Draw("met>>h250","weight*(ht>325)","same")
#d.Draw("met>>hInc","weight*(ht>325)","same")
#
#ROOT.h250.Integral(ROOT.h250.FindBin(150), -1)
#25918.655519843102
#ROOT.hInc.Integral(ROOT.h250.FindBin(150), -1)
#29282.205463409424
#
#sF = 25918.655519843102/29282.205463409424

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
