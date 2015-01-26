import copy
allSamples = []

data={}
data["name"]     = "Data";
data["dirname"] = "/scratch/schoef/pat_110924/Mu/"
#data["bins"]    = ['Run2010A-Dec22ReReco','Run2010B-Dec22ReReco', 'Run2010B-Dec22ReReco-2e32', 'Run2011A-PromptReco', 'Run2011A-PromptReco-v2'] #110519
#data["bins"]    = ['Run2010A-Apr21ReReco','Run2010B-Apr21ReReco', 'Run2010B-Apr21ReReco-2e32', 'Run2011A-May10ReReco', 'Run2011A-PromptReco-v4']
data["bins"]    = [ 'Run2011A-May10ReReco', 'Run2011A-Prompt-v4', 'Run2011A-Aug5ReReco-v1', 'Run2011A-Prompt-v6', 'Run2011B-Prompt-v1']

data["specialCuts"] = []
allSamples.append(data)
#targetLumi = 2.98 + 14.16 + 17.71 +5.07 + 185.10 #pat_110519 
#targetLumi = 3.17 + 13.25 + 16.67 + 189.81 + 497.63 #pat_110711 
targetLumi = 204.7 + 883.3 + 361.7 + 624.8 + 334.9 #pat_110924 

#data={}
#data["name"]     = "Data";
#data["dirname"] = "/scratch/schoef/pat_110406/Mu/"
#data["bins"]    = ['Run2011A-PromptReco']
#
#data["specialCuts"] = []
#allSamples.append(data)
#targetLumi = 5.0 


mc={}
mc["name"]     = "MC";
mc["dirname"] = "/scratch/schoef/pat_110924/Mu/"
mc["specialCuts"] = []
#QCD_Bins =  ["QCD_Pt-15to30_bEnriched","QCD_Pt-30to50_bEnriched","QCD_Pt-50to150_bEnriched","QCD_Pt-150_bEnriched"]
QCD_Bins = ["QCD_Pt-20to30_MuPt5Enriched",  "QCD_Pt-30to50_MuPt5Enriched", "QCD_Pt-50to80_MuPt5Enriched",  "QCD_Pt-80to120_MuPt5Enriched", "QCD_Pt-120to150_MuPt5Enriched", "QCD_Pt-150_MuPt5Enriched"]

#WJets_Bins = ["W1Jets_ptW-0to100","W1Jets_ptW-100to300","W1Jets_ptW-300to800","W1Jets_ptW-800to1600","W2Jets_ptW-0to100","W2Jets_ptW-100to300","W2Jets_ptW-300to800","W2Jets_ptW-800to1600","W3Jets_ptW-0to100","W3Jets_ptW-100to300","W3Jets_ptW-300to800","W3Jets_ptW-800to1600","W4Jets_ptW-0to100","W4Jets_ptW-100to300","W4Jets_ptW-300to800","W4Jets_ptW-800to1600","W5Jets_ptW-0to100","W5Jets_ptW-100to300","W5Jets_ptW-300to800","W5Jets_ptW-800to1600"]

WJets_Bins = ["WJetsToLNu"]

#ZJets_Bins = ["ZJetToMuMu_Pt_0to15","ZJetToMuMu_Pt_120to170","ZJetToMuMu_Pt_15to20","ZJetToMuMu_Pt_170to230","ZJetToMuMu_Pt_20to30","ZJetToMuMu_Pt_230to300","ZJetToMuMu_Pt_300","ZJetToMuMu_Pt_30to50","ZJetToMuMu_Pt_50to80","ZJetToMuMu_Pt_80to120"]
#ZJets_Bins = ["DYtoEE-M20", "DYtoMuMu-M20", "DYtoTauTau-M20"]
ZJets_Bins = ["DYtoEE-M20", "DYtoMuMu-M20", "DYtoTauTau-M20"]

#singleTop_Bins = ["single-Top-tW", "single-Top-s", "single-Top-t"]
singleTop_Bins = ["T-t", "T-s", "T-tW", "Tbar-t", "Tbar-s", "Tbar-tW"]
#["single-Top-tW", "single-Top-s", "single-Top-t"]

#https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
mc["bins"] =  ["TTJets"]
mc["bins"].extend(QCD_Bins)
mc["bins"].extend(WJets_Bins)
mc["bins"].extend(ZJets_Bins)
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
  signal["name"]      = "LM"+str(n);
  signal["dirname"]   = "/scratch/schoef/pat_110924/Mu/"
  signal["bins"] = [signal["name"]]
  return signal

signals = {}
for i in range(0,10):
  sig = getSignal(i)
  allSamples.append(sig)
  signals[str(i)] = sig

pythia6TT={}
pythia6TT["name"]     = "TT-Jets pythia6";
pythia6TT["dirname"] = "/scratch/schoef/pat_110924/pythia6/"
pythia6TT["specialCuts"] = []
pythia6TT["bins"]=["TTJets-met50"]
pythia6TT["hasCountingHLTFilter"]=False

pythia6W={}
pythia6W["name"]     = "W-Jets pythia6";
pythia6W["dirname"] = "/scratch/schoef/pat_110924/pythia6/"
pythia6W["specialCuts"] = []
pythia6W["bins"]=["WJets-met50"]
pythia6W["hasCountingHLTFilter"]=False
