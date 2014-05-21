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
SFb_err={}
for i in range(len(ptBorders)-1):
  ptBins.append([ptBorders[i], ptBorders[i+1]])
  SFb_err[tuple(ptBins[i])] = SFb_errors[i]

#from defaultMu2012Samples import ttbar, ttbarPowHeg
#def getBTagMCTruthEfficiencies(small=True, sample=ttbar, cut=""):
#
#  print sample, cut
#
#  c = ROOT.TChain("Events")
#  for b in sample["bins"]:
#    if small:
#      c.Add(sample["dirname"] + "/"+b+"/h*_10_*.root")
#    else:
#      c.Add(sample["dirname"] + "/"+b+"/h*.root")
#  mceff = {}
#  if cut!="":
#    commoncf=cut+"&&"
#  else:
#    commoncf=cut
#
#  for ptBin in ptBins+[[670,-1]]:
#    mceff[tuple(ptBin)] = {}
#    for etaBin in etaBins:
#      mceff[tuple(ptBin)][tuple(etaBin)] = {}
#      #c.Draw("Sum$(jetsBtag>0.679&&jetsParton==5&&jetsPt>40&&jetsPt<50&&abs(jetsEta)>0&&abs(jetsEta)<1)/Sum$(jetsParton==5&&jetsPt>40&&jetsPt<50&&abs(jetsEta)>0&&abs(jetsEta)<1)")
#      etaCut = "abs(jetsEta)>"+str(etaBin[0])+"&&abs(jetsEta)<"+str(etaBin[1])
#      ptCut = "abs(jetsPt)>"+str(ptBin[0])
#      if ptBin[1]>0:
#        ptCut += "&&abs(jetsPt)<"+str(ptBin[1])
#      c.Draw(commoncf+"(jetsBtag>0.679)>>hbQuark(100,-1,2)",commoncf+"abs(jetsParton)==5&&                     "+etaCut+"&&"+ptCut)
#      c.Draw(commoncf+"(jetsBtag>0.679)>>hcQuark(100,-1,2)",commoncf+"abs(jetsParton)==4&&                     "+etaCut+"&&"+ptCut)
#      c.Draw(commoncf+"(jetsBtag>0.679)>>hOther(100,-1,2)" ,commoncf+"(abs(jetsParton) < 4  || abs(jetsParton) > 5)&&  "+etaCut+"&&"+ptCut)
#      hbQuark = ROOT.gDirectory.Get("hbQuark")
#      hcQuark = ROOT.gDirectory.Get("hcQuark")
#      hOther = ROOT.gDirectory.Get("hOther")
#      mceff[tuple(ptBin)][tuple(etaBin)]["b"]     = hbQuark.GetMean()
#      mceff[tuple(ptBin)][tuple(etaBin)]["c"]     = hcQuark.GetMean()
#      mceff[tuple(ptBin)][tuple(etaBin)]["other"] = hOther.GetMean()
#      print "Eta",etaBin,etaCut,"Pt",ptBin,ptCut,"Found b/c/other", mceff[tuple(ptBin)][tuple(etaBin)]["b"], mceff[tuple(ptBin)][tuple(etaBin)]["c"], mceff[tuple(ptBin)][tuple(etaBin)]["other"]
#      del hbQuark, hcQuark, hOther
#  return mceff

#pickle.dump(getBTagMCTruthEfficiencies(False, ttbar53X, ""), file("btagEff/mceff.pkl", "w"))
#from defaultMu2012Samples import ttbarPowHeg
#mcEffPowHeg = getBTagMCTruthEfficiencies(False, ttbar53X, "")
#pickle.dump(getBTagMCTruthEfficiencies(False, ttbar53X, ""), file("btagEff/mceff.pkl", "w"))

#mcEff = pickle.load(file("btagEff/mceff_mod2.pkl"))
#mcEff = pickle.load(file("/data/schoef/results2012/btagEff/mceff.pkl"))
bTagEffFile = "/data/schoef/results2012/btagEff/btagEffPowHegHT400MET150_Moriond2013.pkl"
print "Loading", bTagEffFile
mcEff = pickle.load(file(bTagEffFile))
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

def getTagWeightDict(effs, maxConsideredBTagWeight):
  zeroTagWeight = 1.
  for e in effs:
    zeroTagWeight*=(1-e)
#  print "\n","zeroTagWeight", zeroTagWeight, "effs",effs
  tagWeight={}
  for i in range(min(len(effs), maxConsideredBTagWeight)+1):
    tagWeight[i]=zeroTagWeight
    combinations = list(itertools.combinations(effs, i))
#    print "Calculating weight for ",i,"bjets"
    twfSum = 0.
    for tagged in combinations:
      twf=1.
      for fac in [x/(1-x) for x in tagged]:
        twf*=fac
      twfSum+=twf
#      print "tagged",tagged,"twf",twf,"twfSum now",twfSum
    tagWeight[i]*=twfSum
#  print "tagWeight",tagWeight,"\n"
  for i in range(maxConsideredBTagWeight+1):
    if not tagWeight.has_key(i):
      tagWeight[i] = 0.
  return tagWeight

ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/SFlightFuncs_Moriond2013.C+")
ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/FSimCorr_UCSB.C+")
SFlightMean = {}
SFlightMin = {}
SFlightMax = {}
for etaB in etaBins:
  SFlightMean[tuple(etaB)] =   ROOT.GetSFlmean( "CSV" , "M", etaB[0], etaB[1], "ABCD")
  SFlightMin [tuple(etaB)] =   ROOT.GetSFlmin ( "CSV" , "M", etaB[0], etaB[1], "ABCD")
  SFlightMax [tuple(etaB)] =   ROOT.GetSFlmax ( "CSV" , "M", etaB[0], etaB[1], "ABCD")

def getSF(parton, pt, eta, year = 2012):
  if abs(parton)==5:#SF_b
    highPtErrFac=1.
    lowPtErrShift = 0.
    if pt<30:
      pt=30
      lowPtErrShift = 0.12
    if pt>=670:
      pt=670
      highPtErrFac = 2.
    sfb_err = -1.
    for bin in ptBins:
      if pt>=bin[0] and pt<=bin[1]:
        sfb_err = SFb_err[tuple(bin)]
    if sfb_err<0:
      print "Warning! no SFb_err found for jet pt",pt
      return None
#    sfb = 0.6981*((1.+(0.414063*pt))/(1.+(0.300155*pt)))
    sfb = 0.726981*((1.+(0.253238*pt))/(1.+(0.188389*pt)));
    yearFac = 1.
#    if year==2012:
#      yearFac = 1.5
#    print sfb_err
    return {"SF":sfb , "SF_down":sfb - yearFac*(sfb_err + lowPtErrShift)*highPtErrFac, "SF_up":sfb + yearFac*(sfb_err + lowPtErrShift)*highPtErrFac}

  if abs(parton)==4: #SF_c; vary correlated with SF_b
    sfb = getSF(5, pt, 0.)
    return {"SF":sfb["SF"], "SF_down":sfb["SF"] + 2.*(sfb["SF_down"] - sfb["SF"]),"SF_up":sfb["SF"] + 2.*(sfb["SF_up"] - sfb["SF"])}

  doubleUnc = False #SFLight
  if pt<20:
    pt=20
  if pt>670:
    pt=670
    doubleUnc = True
  for bin in etaBins:
    if abs(eta)>=bin[0] and abs(eta)<=bin[1]:
      min = SFlightMin[tuple(bin)].Eval(pt)
      max = SFlightMax[tuple(bin)].Eval(pt)
      mean = SFlightMean[tuple(bin)].Eval(pt)
      yearFac = 1.
#      if year==2012:
#        yearFac= 1.10422 - 0.000523856*pt + 1.14251e-06*pt*pt
      if doubleUnc:
        return {"SF":yearFac*mean, "SF_down":yearFac*mean + 2.*yearFac*(min-mean), "SF_up":yearFac*mean +2.*yearFac*(max-mean)}
      else: 
        return {"SF":yearFac*mean, "SF_down":yearFac*mean  +   yearFac*(min-mean), "SF_up":yearFac*mean +   yearFac*(max-mean)}

