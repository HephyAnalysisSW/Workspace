jetdata={}
jetdata["name"]     = "Jet Data";
jetdata["dirname"] = "/scratch/schoef/pat_110927/Jet/"
jetdata["bins"]    = [ 'Run2011A-May10ReReco', 'Run2011A-Prompt-v4', 'Run2011A-Aug5ReReco-v1', 'Run2011A-Prompt-v6', 'Run2011B-Prompt-v1']
jetdata["specialCuts"] = []

HTdata={}
HTdata["name"]     = "HT Data";
HTdata["dirname"] = "/data/schoef/pat_111108/HT/"
HTdata["bins"]    = [ 'Run2011A-May10ReReco', 'Run2011A-Prompt-v4', 'Run2011A-Aug5ReReco-v1', 'Run2011A-Prompt-v6', 'Run2011B-Prompt-v1']
HTdata["Chain"] = "Events"
HTdata["Counter"] = "bool_EventCounter_passed_PAT.obj"
HTdata["specialCuts"] = []

qcdHad={}
qcdHad["name"]     = "QCD had.";
qcdHad["dirname"] = "/scratch/schoef/pat_110924/Had/"
qcdHad["specialCuts"] = []
qcdHad["bins"] = ["QCD_Pt_120to170", "QCD_Pt_15to30", "QCD_Pt_1800", "QCD_Pt_30to50", "QCD_Pt_50to80", "QCD_Pt_600to800", "QCD_Pt_80to120", "QCD_Pt_1000to1400", "QCD_Pt_1400to1800", "QCD_Pt_170to300", "QCD_Pt_300to470", "QCD_Pt_470to600", "QCD_Pt_800to1000"]

zToNuNu={}
zToNuNu["name"] = "ZToNuNu"
zToNuNu["dirname"] = "/data/mhickel/pat_130714/"
zToNuNu["specialCuts"] = []
zToNuNu["bins"] = ["8TeV-ZJetsToNuNu-HT100to200", "8TeV-ZJetsToNuNu-HT200to400", "8TeV-ZJetsToNuNu-HT400",  "8TeV-ZJetsToNuNu-HT50to100"]
 


#QCD_Bins = ["QCD_Pt-20to30_MuPt5Enriched",  "QCD_Pt-30to50_MuPt5Enriched", "QCD_Pt-50to80_MuPt5Enriched",  "QCD_Pt-80to120_MuPt5Enriched", "QCD_Pt-120to150_MuPt5Enriched", "QCD_Pt-150_MuPt5Enriched"]
#
#WJets_Bins = ["WJetsToLNu"]
#
#ZJets_Bins = ["DYtoEE-M20", "DYtoMuMu-M20", "DYtoTauTau-M20"]
#
#singleTop_Bins = ["T-t", "T-s", "T-tW", "Tbar-t", "Tbar-s", "Tbar-tW"]
#
#mc["bins"] =  ["TTJets"]
#mc["bins"].extend(QCD_Bins)
#mc["bins"].extend(WJets_Bins)
#mc["bins"].extend(ZJets_Bins)
#mc["bins"].extend(singleTop_Bins)
#allSamples.append(mc)
#
#ttbar = copy.deepcopy(mc)
#ttbar["bins"] = ["TTJets"] 
#wjets = copy.deepcopy(mc)
#wjets["bins"] = WJets_Bins 
#zjets = copy.deepcopy(mc)
#zjets["bins"] = ZJets_Bins 
#stop = copy.deepcopy(mc)
#stop["bins"] = singleTop_Bins 
#qcd = copy.deepcopy(mc)
#qcd["bins"] = QCD_Bins 
#dy = copy.deepcopy(mc)
#dy["bins"] = ZJets_Bins

