import copy
allSamples=[]

data={}
data["name"]     = "Data";
data["dirname"] = "/data/schoef/pat_111201/EG/"
data["specialCuts"] = []
#data["bins"] = ["Run2010A-133320-140058","Run2010A-140059-143962","Run2010A-143963-144114","Run2010B-146428-147116","Run2010B-147117", "Run2011A-May10ReReco", "Run2011A-Prompt-v4"]
data["bins"]    = [ 'Run2011A-May10ReReco', 'Run2011A-Prompt-v4', 'Run2011A-Aug5ReReco-v1', 'Run2011A-Prompt-v6', 'Run2011B-Prompt-v1']
data["Chain"] = "Events"
data["Counter"] = "bool_EventCounter_passed_PAT.obj"
allSamples.append(data)
#targetLumi = 0.07 + 1.25 + 0.3 + 3.31 + 25.37 + 168.98 + 435.03#pat_110711
#targetLumi = 1.1*(0.09 + 2.17 + 0.6 + 4.27 + 24.45 + 191.12 + 508.21) #pat_110711
#targetLumi = 211 + 930 + 371 + 663 + 330 #pat_110924 
#targetLumi = 216 + 930 + 368 + 658 + 2484 #451 + 1660 #FULL 658 + 2526 #pat_111107
targetLumi = 4700 

mc={}
mc["name"]     = "mc";
mc["dirname"] = "/data/schoef/pat_111201/EG/"
mc["Chain"] = "Events"
mc["Counter"] = "bool_EventCounter_passed_PAT.obj"
mc["specialCuts"] = []
#WJets_Bins = ["W1Jets_ptW-0to100","W1Jets_ptW-100to300","W1Jets_ptW-300to800","W1Jets_ptW-800to1600","W2Jets_ptW-0to100","W2Jets_ptW-100to300","W2Jets_ptW-300to800","W2Jets_ptW-800to1600","W3Jets_ptW-0to100","W3Jets_ptW-100to300","W3Jets_ptW-300to800","W3Jets_ptW-800to1600","W4Jets_ptW-0to100","W4Jets_ptW-100to300","W4Jets_ptW-300to800","W4Jets_ptW-800to1600","W5Jets_ptW-0to100","W5Jets_ptW-100to300","W5Jets_ptW-300to800","W5Jets_ptW-800to1600"]
#WJets_Bins = ["WJetsToLNu"]
WJets_Bins = ["WJets-HT300"]

#ZJets_Bins = ["ZJetToEE_Pt_0to15", "ZJetToEE_Pt_120to170", "ZJetToEE_Pt_15to20", "ZJetToEE_Pt_170to230", "ZJetToEE_Pt_20to30", "ZJetToEE_Pt_230to300", "ZJetToEE_Pt_300", "ZJetToEE_Pt_30to50", "ZJetToEE_Pt_50to80", "ZJetToEE_Pt_80to120"]
#ZJets_Bins = ["DYtoEE-M20", "DYtoMuMu-M20", "DYtoTauTau-M20"]
ZJets_Bins = ["DYtoLL-M50"]

QCD_Bins =  ["QCD_BCtoE_Pt20to30", "QCD_BCtoE_Pt30to80", "QCD_BCtoE_Pt80to170", "QCD_EMEnriched_Pt20to30", "QCD_EMEnriched_Pt30to80", "QCD_EMEnriched_Pt80to170", "QCD_Pt1000to1400", "QCD_Pt1400to1800", "QCD_Pt170to300", "QCD_Pt1800", "QCD_Pt300to470", "QCD_Pt470to600", "QCD_Pt600to800","QCD_Pt800to1000"]
#singleTop_Bins = ["single-Top-tW", "single-Top-s", "single-Top-t"]
singleTop_Bins = ["T-t", "T-s", "T-tW", "Tbar-t", "Tbar-s", "Tbar-tW"]

mc["bins"] =  ["TTJets"]
mc["bins"].extend(WJets_Bins)
mc["bins"].extend(ZJets_Bins)
mc["bins"].extend(QCD_Bins)
mc["bins"].extend(singleTop_Bins)
allSamples.append(mc) 

ttbar = copy.deepcopy(mc)
ttbar["bins"] = ["TTJets"]
wjets = copy.deepcopy(mc)
wjets["bins"] = WJets_Bins 
zjets = copy.deepcopy(mc)
zjets["bins"] = ZJets_Bins 
stop = copy.deepcopy(mc)
stop["bins"] = singleTop_Bins 
qcd = copy.deepcopy(mc)
qcd["bins"] = QCD_Bins    
dy = copy.deepcopy(mc)
dy["bins"] = ZJets_Bins

def getSignal(n):
  signal={}
  signal["name"]     = "LM"+str(n);
  signal["dirname"] = "/data/schoef/pat_111201/EG/"
  signal["bins"] = [signal["name"]]
  signal["Chain"] = "Events"
  signal["Counter"] = "bool_EventCounter_passed_PAT.obj"
  return signal
signals = {}
for i in range(0,10):
  sig = getSignal(i)
  allSamples.append(sig)
  signals[str(i)] = sig

