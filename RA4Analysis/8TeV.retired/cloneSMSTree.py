import ROOT, os, sys

small = False

c = ROOT.TChain("Events")
allFiles=[]
for subdir in ["8TeV-T1tttt", "8TeV-T1tttt_2J_mGo-775to1075_mLSP-25to500", "8TeV-T1tttt_2J_mGo-775to1075_mLSP-525to875"]:
  files = os.listdir("/data/mhickel/pat_130426/"+subdir+"/")
  for f in files:
    allFiles.append("/data/mhickel/pat_130426/"+subdir+"/"+f)

allFiles.sort()
first = int(sys.argv[1])
last = int(sys.argv[2])
for f in allFiles[first:last]:
  c.Add(f)


variables = ["event", "run", "lumi", "met", "type1phiMet", "type1phiMetpx", "type1phiMetpy", "metpx", "metpy", "metphi", "mT", "barepfmet" ,"ht", "btag0", "btag1", "btag2", "btag3","rawMetpx", "rawMetpy", "m3", "mht", "singleMuonic", "singleElectronic",  "leptonPt", "leptonEta", "leptonPhi", "leptonPdg", "njets", "nbtags", "nbjets", "jet0pt", "jet1pt", "jet2pt", "jet3pt", "nvetoMuons", "nvetoElectrons", "ngoodMuons", "ngoodElectrons", "nTrueGenVertices", "ngoodVertices", "btag0pt", "btag1pt", "btag0eta", "btag1eta", "genmet", "genmetpx","genmetpy", "btag0parton", "btag1parton", "btag2parton", "btag3parton", "antinuMu", "antinuE", "antinuTau", "nuMu", "nuE", "nuTau", "nuMuFromTausFromWs", "nuEFromTausFromWs", "nuTauFromTausFromWs", "gluino0Pt", "gluino0Eta", "gluino0Phi", "gluino0Pdg", "gluino1Pt", "gluino1Eta", "gluino1Phi", "gluino1Pdg", "osetMgl", "osetMN"]

variables+= ["jetsPt", "jetsPtUncorr", "jetsEta", "jetsPhi", "jetsParton", "jetsBtag", "jetsUnc", "jetsEleCleaned", "jetsMuCleaned", "jetsID", "hasGluonSplitting", "nsoftJets"]
#nc = 0; isample=0;
#
#structString = "struct MyStruct_"+str(nc)+"_"+str(isample)+"{ULong64_t event;"
#for var in variables:
#  structString +="Float_t "+var+";"
#structString   +="};"
#ROOT.gROOT.ProcessLine(structString)
#
#exec("from ROOT import MyStruct_"+str(nc)+"_"+str(isample))
#exec("s = MyStruct_"+str(nc)+"_"+str(isample)+"()")
c.GetEntry()
c.SetBranchStatus("*", 0) 
#c.SetBranchStatus("*met*", 1)
#c.SetBranchStatus("*_met_PAT", 1)
for var in variables:
  c.SetBranchStatus(c.GetAlias(var)[:-3]+"*", 1) 
#  c.SetBranchStatus(var+"*", 1) 
  
d = c.CloneTree()
for var in variables:
  d.SetAlias(var, c.GetAlias(var))

print "Cloned ...  now saving"

f = ROOT.TFile("/data/schoef/pat_130501/8TeV-T1tttt-redux/histo_T1tttt_file_"+str(first)+"_"+str(last)+".root", "recreate")
d.Write()
f.Close()
