import ROOT, pickle
from array import array
from math import *
from Workspace.RA4Analysis.simplePlotsCommon import *
import numpy as np

small = False
SFsmall = False

#subdir = "copyMET_JES+"
#subdir = "copyMET_JES-"
subdir = "copyMET50"

allMCs = ["TTJets-PowHeg", "DY", "QCD", "singleTop",  "WJetsHT250", "TTWJets", "TTZJets"]
#allMCs = ["TTJets-PowHeg"]
cMC = {}
cMCTotal = ROOT.TChain("Events")
for mc in allMCs:
  cMC[mc] = ROOT.TChain("Events")
  print "Adding", mc
  cMC[mc].Add("/data/schoef/convertedTuples_v19/"+subdir+"/Mu/"+mc+"/histo_"+mc+".root")
  cMC[mc].Add("/data/schoef/convertedTuples_v19/"+subdir+"/Ele/"+mc+"/histo_"+mc+".root")
  cMCTotal.Add("/data/schoef/convertedTuples_v19/"+subdir+"/Mu/"+mc+"/histo_"+mc+".root")
  cMCTotal.Add("/data/schoef/convertedTuples_v19/"+subdir+"/Ele/"+mc+"/histo_"+mc+".root")
  print mc,"has",cMC[mc].GetEntries(), "Events"


cData = ROOT.TChain("Events")
cData.Add("/data/schoef/convertedTuples_v18/copyMET50/Mu/singleMuData/histo_singleMuData.root")
cData.Add("/data/schoef/convertedTuples_v18/copyMET50/Ele/singleEleData/histo_singleEleData.root")

prefix = "_minimal_"
metbins = [\
    [100,250]]
additionalHTIntervals = []
htvals = [ [0, 400] ]
njetbins = [ [5,5] , [6,99]]
#htvals = [ [200,250 ], [250, 300], [300, 350], [350, 400] ]
#njetbins = [ [5,5]]
#htvals = [ [200,225 ],[225,250], [250, 275], [275,300], [300, 325], [325,350], [350, 400] ]
#njetbins = [ [4,4]]

leptonCut="leptonPt>30&&((singleMuonic&&nvetoElectrons==0&&nvetoMuons==1)||(singleElectronic&&nvetoElectrons==1&&nvetoMuons==0))"
##get njet reweighting histograms
#if not globals().has_key("njetWeightHisto"):
#  njetWeightHisto={}
#  for htb in htvals+additionalHTIntervals:
#    sigCut="ht>="+str(htb[0])+"&&ht<"+str(htb[1])+"&&"+leptonCut
#    cPow.Draw("njets>>hNJetMC(10,0,10)", sigCut, "goff")
#    mcNJHisto =  ROOT.gDirectory.Get("hNJetMC").Clone()
#    mcNJHisto.Scale(1./mcNJHisto.Integral())
#    cData.Draw("njets>>hNJetData(10,0,10)", sigCut, "goff")
#    dataNJHisto =  ROOT.gDirectory.Get("hNJetData").Clone()
#    dataNJHisto.Scale(1./dataNJHisto.Integral())
#    dataNJHisto.Divide(mcNJHisto)
#    njetWeightHisto[tuple(htb)]=dataNJHisto.Clone("njetRWHisto_ht_"+str(htb[0])+"_"+str(htb[1]))



#def jackKnifeSum(w1, i):#make sum without i-th component
#  sw1 = float('nan')
#  if i<len(w1):
#    sw1 = sum(w1[:i])+sum(w1[i+1:])
#  return sw1

def jackKnifeRatios(w1, w2):
  n = len(w1)
  if not n==len(w2): print "Length not equal!"; return float('nan')
  sw1 = sum(w1)
  sw2 = sum(w2)
  if sw2==0.:
    return [float('nan')]
  try:
    res = [n*(sw1/sw2) - (n-1)*((sw1 - w1[i])/(sw2 - w2[i])) for i in range(len(w1))] #This is the vector of n=1 jacknife estimates according to http://www.math.wustl.edu/~sawyer/handouts/Jackknife.pdf 
#    res = [n*(sw1/sw2) - (n-1)*(jackKnifeSum(w1, i)/jackKnifeSum(w2, i)) for i in range(len(w1))] #This is the vector of n=1 jacknife estimates according to http://www.math.wustl.edu/~sawyer/handouts/Jackknife.pdf 
  except ZeroDivisionError:
    res = [float('nan')]
  return res

def jackNifeEstimate(w1, w2): #Calculate jacknifeEstimate of ratios sum(w1)/sum(w2)
  jnf = jackKnifeRatios(w1, w2) #Get vector of n=1 jacknife estimates
  n=float(len(jnf))
  res={}
  if n==0.:
    res['mean'] = float('nan'); res['sigma'] = float('nan')
  else:
    res['mean'] = sum(jnf)/n
  if n==1.:
     res['sigma'] = float('nan')
  else:
    res['sigma']= sqrt(1./(n*(n-1))*sum([(jnf[i] - res['mean'])**2 for i in range(len(jnf))]))
  return res 


SFSys = ['', 'SF', 'SF_b_Up', 'SF_b_Down', 'SF_light_Up', 'SF_light_Down']
#SFSys = []
sys = ['GluSplitUp', 'GluSplitDown', 'cFracUp', 'cFracDown', 'TTV_Up', 'TTV_Down']
#sys = ['cFracUp', 'TTV_Up', 'TTV_Down']

def getJackKnifeSpillFactor(cDict, cut, bt1='3p', bt2='2', njetReweightingHist=""):
  weights1={}
  weights2={}
  weightsnj1={}
  weightsnj2={}
  for sfk in SFSys+sys:
    weights1[sfk] = []
    weights2[sfk] = []
    weightsnj1[sfk] = []
    weightsnj2[sfk] = []
  for k in cDict.keys():
    c = cDict[k]
    c.Draw(">>eList",cut, "goff")
    eList = ROOT.gDirectory.Get("eList")
    nEvents = int(eList.GetN())
    for i in range(nEvents):
      if not i%100:print i,"/",nEvents
      c.GetEntry(eList.GetEntry(i))
      for sfk in SFSys:
        if sfk=='':
          weightVal1=c.GetLeaf("weightBTag"+bt1).GetValue()
          weightVal2=c.GetLeaf("weightBTag"+bt2).GetValue()
        else:
          weightVal1=c.GetLeaf("weightBTag"+bt1+"_"+sfk).GetValue()
          weightVal2=c.GetLeaf("weightBTag"+bt2+"_"+sfk).GetValue()
        if njetReweightingHist!="":
          njetReWeight = njetReweightingHist.GetBinContent(njetReweightingHist.FindBin(c.GetLeaf("njets").GetValue()))
          weightsnj1[sfk].append(njetReWeight*weightVal1)
          weightsnj2[sfk].append(njetReWeight*weightVal2)
        weights1[sfk].append(weightVal1)
        weights2[sfk].append(weightVal2)
      weightVal1=c.GetLeaf("weightBTag"+bt1+"_SF").GetValue()
      weightVal2=c.GetLeaf("weightBTag"+bt2+"_SF").GetValue()
      numBPartons = c.GetLeaf("numBPartons").GetValue()
      numCPartons = c.GetLeaf("numCPartons").GetValue()
      singleC     = numCPartons==1
      if k=="TTJets-PowHeg":
        top0WDaughter1Pdg = c.GetLeaf("top0WDaughter1Pdg").GetValue()
        top0WDaughter0Pdg = c.GetLeaf("top0WDaughter0Pdg").GetValue()
        top1WDaughter1Pdg = c.GetLeaf("top1WDaughter1Pdg").GetValue()
        top1WDaughter0Pdg = c.GetLeaf("top1WDaughter0Pdg").GetValue()
        wDecaysToC = abs(top0WDaughter1Pdg)==4 or abs(top0WDaughter0Pdg)==4 or abs(top1WDaughter1Pdg)==4 or abs(top1WDaughter0Pdg)==4
      else:
        wDecaysToC = False
      mcGluonSplit  = c.GetLeaf("hasGluonSplitting").GetValue()==1
      gluonSplit = mcGluonSplit or  (numBPartons>2) or (wDecaysToC and numCPartons>1) or ((not wDecaysToC) and numCPartons>=1)
      for sfk in sys:
        weightFac = 1.
        if sfk.count('GluSplit') and gluonSplit:
          if sfk.count('Up'):
            weightFac = 1.5
          if sfk.count('Down'):
            weightFac = 0.5
        if sfk.count('cFrac') and singleC:
          if sfk.count('Up'):
            weightFac = 1.57
          if sfk.count('Down'):
            weightFac = 1. - 0.57
        if sfk.count('TTV_') and (k=="TTWJets" or k=="TTZJets"):
          if sfk.count('Up'):
            weightFac = 1.50
          if sfk.count('Down'):
            weightFac = 1. - 0.50
        weightVal1_=weightVal1*weightFac
        weightVal2_=weightVal2*weightFac
        weights1[sfk].append(weightVal1_)
        weights2[sfk].append(weightVal2_)
        if njetReweightingHist!="":
          njetReWeight = njetReweightingHist.GetBinContent(njetReweightingHist.FindBin(c.GetLeaf("njets").GetValue()))
          weightsnj1[sfk].append(njetReWeight*weightVal1_)
          weightsnj2[sfk].append(njetReWeight*weightVal2_)
#        print sfk, sum(weights1[sfk]), sum(weights2[sfk])
    del eList
  res={}
  for sfk in SFSys+sys:
#    print sfk, sum(weights1[sfk]), sum(weights2[sfk])
    jnfsp = jackNifeEstimate(weights1[sfk], weights2[sfk])
    res[sfk] = {"rTrue":jnfsp['mean'],"rTrueSigma":jnfsp['sigma']}
#    print sfk, "rTrue",jnfsp['mean']
    if njetReweightingHist!="":
      jnfsp = jackNifeEstimate(weightsnj1[sfk], weightsnj2[sfk])
      res[sfk]["rForData"] = jnfsp['mean']
      res[sfk]["sigmaForData"] = jnfsp['sigma']
  return res


#def getJackKnifeSpillFactor(c, cut, bt1='3p', bt2='2', njetReweightingHist=""):
#  c.Draw(">>eList",cut, "goff")
#  eList = ROOT.gDirectory.Get("eList")
#  nEvents = int(eList.GetN())
#  weights1={}
#  weights2={}
#  weightsnj1={}
#  weightsnj2={}
#  for sfk in SFSys+sys:
#    weights1[sfk] = [] 
#    weights2[sfk] = [] 
#    weightsnj1[sfk] = [] 
#    weightsnj2[sfk] = [] 
#
#  for i in range(nEvents):
#    if not i%100:print i,"/",nEvents
#    c.GetEntry(eList.GetEntry(i))
#    for sfk in SFSys:
#      if sfk=='':
#        weightVal1=c.GetLeaf("weightBTag"+bt1).GetValue()
#        weightVal2=c.GetLeaf("weightBTag"+bt2).GetValue()
#      else:
#        weightVal1=c.GetLeaf("weightBTag"+bt1+"_"+sfk).GetValue()
#        weightVal2=c.GetLeaf("weightBTag"+bt2+"_"+sfk).GetValue()
#      if njetReweightingHist!="":
#        njetReWeight = njetReweightingHist.GetBinContent(njetReweightingHist.FindBin(c.GetLeaf("njets").GetValue()))
#        weightsnj1[sfk].append(njetReWeight*weightVal1)
#        weightsnj2[sfk].append(njetReWeight*weightVal2)
#      weights1[sfk].append(weightVal1)
#      weights2[sfk].append(weightVal2)
#    for sfk in sys:
#      weightVal1=c.GetLeaf("weightBTag"+bt1+"_SF").GetValue()
#      weightVal2=c.GetLeaf("weightBTag"+bt2+"_SF").GetValue()
##      numBPartons = c.GetLeaf("numBPartons").GetValue()
##      numCPartons = c.GetLeaf("numCPartons").GetValue()
#
##      singleC     = numCPartons==1
#      gluonSplit  = c.GetLeaf("hasGluonSplitting").GetValue() 
#      weightFac = 1.
#      if sfk.count('GluSplit') and gluonSplit:
#        if sfk.count('Up'):
#          weightFac = 1.5
#        if sfk.count('Down'):
#          weightFac = 0.5
##      if sfk.count('cFrac') and singleC:
##        if sfk.count('Up'):
##          weightFac = 1.57
##        if sfk.count('Down'):
##          weightFac = 1. - 0.57
#      weightVal1=weightVal1*weightFac
#      weightVal2=weightVal2*weightFac
#      if njetReweightingHist!="":
#        njetReWeight = njetReweightingHist.GetBinContent(njetReweightingHist.FindBin(c.GetLeaf("njets").GetValue()))
#        weightsnj1[sfk].append(njetReWeight*weightVal1)
#        weightsnj2[sfk].append(njetReWeight*weightVal2)
#      weights1[sfk].append(weightVal1)
#      weights2[sfk].append(weightVal2)
#
#  del eList
#  res={}
#  for sfk in SFSys+sys:
#    jnfsp = jackNifeEstimate(weights1[sfk], weights2[sfk])
#    res[sfk] = {"rTrue":jnfsp['mean'],"rTrueSigma":jnfsp['sigma']}
#    if njetReweightingHist!="":
#      jnfsp = jackNifeEstimate(weightsnj1[sfk], weightsnj2[sfk])
#      res[sfk]["rForData"] = jnfsp['mean']
#      res[sfk]["sigmaForData"] = jnfsp['sigma']
#  return res 

#Either load or calculate SpF
#SpF_small =   pickle.load(file("/data/schoef/results2012/jackKnifeSpF_SFsmall.pkl"))
#filename = "/data/schoef/results2012/"+subdir+prefix+"jackKnifeSpF.pkl"
#SpF =   pickle.load(file(filename))
#if SFsmall:
#  filename = "/data/schoef/results2012/jackKnifeSpF_SFsmall.pkl"
if not globals().has_key("SpF"):
  SpF = {}
  for htb in htvals+additionalHTIntervals:
    SpF[tuple(htb)] = {}
    for metb in metbins:
      SpF[tuple(htb)][tuple(metb)] = {}
      for njb in njetbins:
        print htb, metb, njb
        SpF[tuple(htb)][tuple(metb)][tuple(njb)] = {}
        sigCut="event%4==0&&njets>="+str(njb[0])+"&&njets<="+str(njb[1])+"&&met>="+str(metb[0])+"&&met<"+str(metb[1])+"&&ht>="+str(htb[0])+"&&ht<"+str(htb[1])+"&&"+leptonCut
#        res3po2 = getJackKnifeSpillFactor(cPow, sigCut, bt1='3p', bt2='2', njetReweightingHist=njetWeightHisto[tuple(htb)])
        res3po2 = getJackKnifeSpillFactor(cMC, sigCut, bt1='3p', bt2='2', njetReweightingHist="")
        for sFk in SFSys+sys:
          SpF[tuple(htb)][tuple(metb)][tuple(njb)][sFk] = {}
          SpF[tuple(htb)][tuple(metb)][tuple(njb)][sFk]["3po2"] = res3po2[sFk]
   #       SpF[tuple(htb)][tuple(metb)][njb][sFk]["1o2"] = res1o2[sFk]
#  if not small:
#    pickle.dump(SpF, file(filename, "w"))
#  else:
#    print "No saving when small!"

#make plots
for inclData in [True]:#, False]:
  htbins = [h[0] for h in htvals] + [htvals[-1][1]]
  ROOT.TH1F().SetDefaultSumw2()
  for metb in metbins:
    for njb in njetbins:
      l = ROOT.TLegend(0.6,0.55,1,1)
      l.SetFillColor(0)
      l.SetBorderSize(1)

      c1  =ROOT.TCanvas()
      SpFData_3po2 = ROOT.TH1F("SpF_3po2_Data","SpF", len(htbins) - 1, array('d',htbins))
      SpF_3po2 = {}
      for sFk in SFSys+sys:
        SpF_3po2[sFk] = ROOT.TH1F("SpF_3po2","SpF_"+sFk, len(htbins) - 1, array('d',htbins))
        SpF_3po2[sFk].SetLineColor(ROOT.kRed) 
        SpF_3po2[sFk].SetMarkerColor(ROOT.kRed) 

      for htb in htvals:
        print "\nHT bin", htb
        cut="njets>="+str(njb[0])+"&&njets<="+str(njb[1])+"&&met>"+str(metb[0])+"&&met<"+str(metb[1])+"&&ht>"+str(htb[0])+"&&ht<"+str(htb[1])+"&&"+leptonCut
        n_bt2 = cData.GetEntries(cut+"&&nbtags==2")
        n_bt3p = cData.GetEntries(cut+"&&nbtags>=3")
        print htb, n_bt3p, n_bt2
        SpFData_3po2.SetBinContent(SpFData_3po2.FindBin(htb[0]), n_bt3p/float(n_bt2))
        SpFData_3po2.SetBinError(SpFData_3po2.FindBin(htb[0]), n_bt3p/float(n_bt2)*sqrt(1./n_bt3p + 1./n_bt2))
        for sFk in SFSys+sys:
          b = SpF_3po2[sFk].FindBin(htb[0])
          spf = SpF[tuple(htb)][tuple(metb)][tuple(njb)][sFk]
#          if sFk.count("cFrac"):
#            spf = SpF_small[tuple(htb)][tuple(metb)][tuple(njb)][sFk]
          spf = SpF[tuple(htb)][tuple(metb)][tuple(njb)][sFk]
          val = spf['3po2']['rTrue']
          valErr = spf['3po2']['rTrueSigma']
          if val<float('inf') and valErr<float('inf'): 
            SpF_3po2[sFk].SetBinContent(b, val )
            SpF_3po2[sFk].SetBinError(b, valErr)
#      SpFData_3po2.SetDefaultSumw2()
#      SpFData_3po2.Divide(SpFData_2)
      SpF_3po2["SF"].GetYaxis().SetRangeUser(0.04,0.8)
      SpF_3po2["SF"].GetXaxis().SetTitle("H_{T} (GeV)")
      SpF_3po2["SF"].GetYaxis().SetTitle("spillFactor #geq 3 / ==2")

      SpF_3po2["SF"].Draw()
      SpF_3po2["SF_b_Up"]  .SetLineColor(ROOT.kBlue) 
      SpF_3po2["SF_b_Down"].SetLineColor(ROOT.kBlue) 
      SpF_3po2["SF_light_Up"]  .SetLineColor(ROOT.kRed) 
      SpF_3po2["SF_light_Down"].SetLineColor(ROOT.kRed) 
      SpF_3po2["GluSplitDown"].SetLineColor(ROOT.kGreen) 
      SpF_3po2["GluSplitUp"].SetLineColor(ROOT.kGreen) 
      SpF_3po2["cFracDown"].SetLineColor(ROOT.kMagenta) 
      SpF_3po2["cFracUp"].SetLineColor(ROOT.kMagenta) 
      SpF_3po2["SF_b_Up"]  .SetMarkerColor(ROOT.kBlue) 
      SpF_3po2["SF_b_Down"].SetMarkerColor(ROOT.kBlue) 
      SpF_3po2["SF_light_Up"]  .SetMarkerColor(ROOT.kRed) 
      SpF_3po2["SF_light_Down"].SetMarkerColor(ROOT.kRed) 
      SpF_3po2["GluSplitDown"].SetMarkerColor(ROOT.kGreen) 
      SpF_3po2["GluSplitUp"].SetMarkerColor(ROOT.kGreen) 
      SpF_3po2["cFracDown"].SetMarkerColor(ROOT.kMagenta) 
      SpF_3po2["cFracUp"].SetMarkerColor(ROOT.kMagenta) 
      SpF_3po2["SF_b_Up"]       .SetMarkerSize(0) 
      SpF_3po2["SF_b_Down"]     .SetMarkerSize(0) 
      SpF_3po2["SF_light_Up"]   .SetMarkerSize(0)
      SpF_3po2["SF_light_Down"] .SetMarkerSize(0)
      SpF_3po2["GluSplitDown"].SetMarkerSize(0)
      SpF_3po2["GluSplitUp"].SetMarkerSize(0)
      SpF_3po2["cFracDown"].SetMarkerSize(0)
      SpF_3po2["cFracUp"].SetMarkerSize(0)
      SpF_3po2["SF_b_Up"]       .SetMarkerStyle(0) 
      SpF_3po2["SF_b_Down"]     .SetMarkerStyle(0) 
      SpF_3po2["SF_light_Up"]   .SetMarkerStyle(0)
      SpF_3po2["SF_light_Down"] .SetMarkerStyle(0)
      SpF_3po2["GluSplitDown"].SetMarkerStyle(0)
      SpF_3po2["GluSplitUp"].SetMarkerStyle(0)
      SpF_3po2["cFracDown"].SetMarkerStyle(0)
      SpF_3po2["cFracUp"].SetMarkerStyle(0)
      SpF_3po2["SF_b_Up"]      .Draw("histsame") 
      SpF_3po2["SF_b_Down"]    .Draw("histsame") 
      SpF_3po2["SF_light_Up"]  .Draw("histsame")
      SpF_3po2["SF_light_Down"].Draw("histsame") 
      SpF_3po2["GluSplitDown"].Draw("histsame")
      SpF_3po2["GluSplitUp"].Draw("histsame")
      SpF_3po2["cFracDown"].Draw("histsame")
      SpF_3po2["cFracUp"].Draw("histsame")
      if inclData:
        SpFData_3po2.Draw("same")
        l.AddEntry( SpFData_3po2, "Data")
      l.AddEntry( SpF_3po2["SF"], "MC (SF)")
      l.AddEntry( SpF_3po2["SF_b_Up"], "MC (SF) #pm 1 #sigma b.eff.")
      l.AddEntry( SpF_3po2["SF_light_Up"], "MC (SF) #pm 1 #sigma l.eff.")
      l.AddEntry( SpF_3po2["GluSplitUp"], "MC (SF) #pm 50% g split")
      l.AddEntry( SpF_3po2["cFracUp"], "MC (SF) #pm 1 #sigma c frac.")
      l.Draw()
      if inclData:
        prefix = "withData"
      else:
        prefix = "noData"
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/spillFactors/SpF_control_metb_"+subdir+"_"+prefix+"_"+str(metb[0])+"_"+str(metb[1])+"_nj"+str(njb[0])+"-"+str(njb[1])+".png")
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/spillFactors/SpF_control_metb_"+subdir+"_"+prefix+"_"+str(metb[0])+"_"+str(metb[1])+"_nj"+str(njb[0])+"-"+str(njb[1])+".pdf")
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/spillFactors/SpF_control_metb_"+subdir+"_"+prefix+"_"+str(metb[0])+"_"+str(metb[1])+"_nj"+str(njb[0])+"-"+str(njb[1])+".root")
