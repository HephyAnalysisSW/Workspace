import ROOT, pickle, itertools
## Tagger: CSVM within 30 < pt < 670 GeV, abs(eta) < 2.4, x = pt
## https://twiki.cern.ch/twiki/pub/CMS/BtagPOG/SFb-mujet_payload.txt
#
ptBorders = [30, 40, 50, 60, 70, 80, 100, 120, 160, 210, 260, 320, 400, 500, 670]
ptBins = []
etaBins = [[0,0.8], [0.8,1.6], [ 1.6, 2.4]]
# Moriond 2013 recommendations / approx. for last bin (using 500-600 for 500-670)
SFb_errors = [\
 0.0209663,
 0.0207019,
 0.0230073,
 0.0208719,
 0.0200453,
 0.0264232,
 0.0240102,
 0.0229375,
 0.0184615,
 0.0216242,
 0.0248119,
 0.0465748,
 0.0474666,
 0.0718173
]
#SFb_errors = [\
# 0.0295675,
# 0.0295095,
# 0.0210867,
# 0.0219349,
# 0.0227033,
# 0.0204062,
# 0.0185857,
# 0.0256242,
# 0.0383341,
# 0.0409675,
# 0.0420284,
# 0.0541299,
# 0.0578761,
# 0.0655432 ]
SFb_err={}
for i in range(len(ptBorders)-1):
  ptBins.append([ptBorders[i], ptBorders[i+1]])
  SFb_err[tuple(ptBins[i])] = SFb_errors[i]

from Workspace.MonoJetAnalysis.defaultConvertedTuples import wJetsHT150v2, ttJetsPowHeg
def getBTagMCTruthEfficiencies(small=True, sample=ttJetsPowHeg, cut=""):

  print sample, cut

  c = ROOT.TChain("Events")
  for b in sample["bins"]:
    c.Add(sample["dirname"] + "/"+b+"/h*.root")
  mceff = {}
  if cut!="":
    commoncf=cut+"&&"
  else:
    commoncf=cut

  for ptBin in ptBins+[[670,-1]]:
    mceff[tuple(ptBin)] = {}
    for etaBin in etaBins:
      mceff[tuple(ptBin)][tuple(etaBin)] = {}
      #c.Draw("Sum$(jetBtag>0.679&&jetPdg==5&&jetPt>40&&jetPt<50&&abs(jetEta)>0&&abs(jetEta)<1)/Sum$(jetPdg==5&&jetPt>40&&jetPt<50&&abs(jetEta)>0&&abs(jetEta)<1)")
      etaCut = "abs(jetEta)>"+str(etaBin[0])+"&&abs(jetEta)<"+str(etaBin[1])
      ptCut = "abs(jetPt)>"+str(ptBin[0])
      if ptBin[1]>0:
        ptCut += "&&abs(jetPt)<"+str(ptBin[1])
      c.Draw(commoncf+"(jetBtag>0.679)>>hbQuark(100,-1,2)",commoncf+"abs(jetPdg)==5&&                     "+etaCut+"&&"+ptCut)
      c.Draw(commoncf+"(jetBtag>0.679)>>hcQuark(100,-1,2)",commoncf+"abs(jetPdg)==4&&                     "+etaCut+"&&"+ptCut)
      c.Draw(commoncf+"(jetBtag>0.679)>>hOther(100,-1,2)" ,commoncf+"(abs(jetPdg) < 4  || abs(jetPdg) > 5)&&  "+etaCut+"&&"+ptCut)
      hbQuark = ROOT.gDirectory.Get("hbQuark")
      hcQuark = ROOT.gDirectory.Get("hcQuark")
      hOther = ROOT.gDirectory.Get("hOther")
      mceff[tuple(ptBin)][tuple(etaBin)]["b"]     = hbQuark.GetMean()
      mceff[tuple(ptBin)][tuple(etaBin)]["c"]     = hcQuark.GetMean()
      mceff[tuple(ptBin)][tuple(etaBin)]["other"] = hOther.GetMean()
      print "Eta",etaBin,etaCut,"Pt",ptBin,ptCut,"Found b/c/other", mceff[tuple(ptBin)][tuple(etaBin)]["b"], mceff[tuple(ptBin)][tuple(etaBin)]["c"], mceff[tuple(ptBin)][tuple(etaBin)]["other"]
      del hbQuark, hcQuark, hOther
  return mceff

pickle.dump(getBTagMCTruthEfficiencies(False, ttJetsPowHeg, ""), file("/data/schoef/results2014/btagEff/btagEff_ttJetsPowHeg.pkl", "w"))
pickle.dump(getBTagMCTruthEfficiencies(False, wJetsHT150v2, ""), file("/data/schoef/results2014/btagEff/btagEff_wJetsHT150v2.pkl", "w"))
#from defaultMu2012Samples import ttbarPowHeg
#mcEffPowHeg = getBTagMCTruthEfficiencies(False, ttbar53X, "")
#pickle.dump(getBTagMCTruthEfficiencies(False, ttbar53X, ""), file("btagEff/mceff.pkl", "w"))

#mcEff = pickle.load(file("btagEff/mceff_mod2.pkl"))
#mcEff = pickle.load(file("/data/schoef/results2012/btagEff/mceff.pkl"))
#bTagEffFile = "/data/schoef/results2014/btagEff/btagEffPowHegHT400MET150_Moriond2013.pkl"
#print "Loading", bTagEffFile
#mcEff = pickle.load(file(bTagEffFile))

def getMCEff(parton, pt, eta, year = 2012):
  for ptBin in ptBins+[[670,-1]]:
    if pt>=ptBin[0] and (pt<ptBin[1] or ptBin[1]<0):
      for etaBin in etaBins:
        if abs(eta)>=etaBin[0] and abs(eta)<etaBin[1]:
          res=getSF(parton, pt, eta, year)
#          print ptBin, etaBin      , mcEff[tuple(ptBin)][tuple(etaBin)]
          if abs(parton)==5:                  res["mcEff"] = mcEff[tuple(ptBin)][tuple(etaBin)]["b"]
          if abs(parton)==4:                  res["mcEff"] = mcEff[tuple(ptBin)][tuple(etaBin)]["c"]
          if abs(parton)>5 or abs(parton)<4:  res["mcEff"] = mcEff[tuple(ptBin)][tuple(etaBin)]["other"]
          return res 

