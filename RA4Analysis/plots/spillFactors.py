import ROOT, pickle, os, sys
from array import array
from math import *
from Workspace.RA4Analysis.simplePlotsCommon import *
import numpy as np

small = False
SFsmall = False
makePlots = False
#subdir = "copyMET_JES+"
#subdir = "copyMET_JES-"
subdir = "copyMET"

allMCs = ["TTJets-PowHeg", "DY", "QCD", "singleTop",  "WJetsHT250", "TTWJets", "TTZJets"]
#allMCs = ["TTJets-PowHeg"]
vstr="v19"
prefix = "_fullMC_"+vstr+"_GluSplitFixed_small_new_"
if len(sys.argv)>1:
  allMCs = sys.argv[1:2]
  vstr="v20"
  prefix="_fullMC_"+vstr+"_GluSplitFixed_small_new_only"+sys.argv[1]+"_"
  print "allMCs",allMCs

cMC = {}
cMCTotal = ROOT.TChain("Events")
for mc in allMCs:
  cMC[mc] = ROOT.TChain("Events")
  print "Adding", mc
  cMC[mc].Add("/data/schoef/convertedTuples_"+vstr+"/"+subdir+"/Mu/"+mc+"/histo_"+mc+".root")
  cMC[mc].Add("/data/schoef/convertedTuples_"+vstr+"/"+subdir+"/Ele/"+mc+"/histo_"+mc+".root")
  cMCTotal.Add("/data/schoef/convertedTuples_"+vstr+"/"+subdir+"/Mu/"+mc+"/histo_"+mc+".root")
  cMCTotal.Add("/data/schoef/convertedTuples_"+vstr+"/"+subdir+"/Ele/"+mc+"/histo_"+mc+".root")
  print mc,"has",cMC[mc].GetEntries(), "Events"

cData = ROOT.TChain("Events")
cData.Add("/data/schoef/convertedTuples_v16/copyMET/Mu/data/histo_data.root")
cData.Add("/data/schoef/convertedTuples_v16/copyMET/Ele/data/histo_data.root")

htvals = [\
#    [400,450  ],
#    [450,500  ],
#    [500,550  ],
#    [550,600  ],
#    [600,650  ],
#    [650,700  ],
#    [700,750  ],
#    [750,800  ],
#    [800,1000 ],
#    [1000,1200],
#    [1200,1500],
#    [1500,2500]
  ]

additionalHTIntervals = [[400,750], [400,2500], [500,2500], [750, 2500], [1000,2500]]
metbins = [\
    [150, 250],
    [250, 350],
    [350, 450],
    [450, 2500],
    [150,2500],
    [250,2500],
#    [250, 275],
#    [275, 300],
#    [300, 350],
#    [150, 175],
#    [175, 200],
#    [200, 225],
#    [225, 250]
    ]
#njetbins = [[3,3], [4,4],[5,5], [6,99], [3,5]]
njetbins = [[6,99], [3,5]]


#prefix = "_minimal_UCSB_test_"
##prefix = ""
#htvals = [\
#  ]
#additionalHTIntervals = [[400,750], [500,2500], [750, 2500], [1000,2500], [400,2500]]
#metbins = [\
#    [150, 250],
#    [250, 350],
#    [350, 450],
#    [450, 2500],
#    [150,2500],
#    [250,2500],
#    [250, 275],
#    [275, 300],
#    [300, 350],
#    [150, 175],
#    [175, 200],
#    [200, 225],
#    [225, 250]]
#
#njetbins = [[3,5], [6,99]]

if small:
  prefix = "_small_"
  htvals = [  [750, 2500  ] ]
  additionalHTIntervals = []
  metbins = [ [150, 250] ] 
  njetbins = [[6,99]]

#njetbins = range(3,8)+[-1]
#if small:

#get njet reweighting histograms
preSelCut="njets>=3 && met>=150&&ht>=400&&((singleMuonic&&nvetoElectrons==0&&nvetoMuons==1)||(singleElectronic&&nvetoElectrons==1&&nvetoMuons==0))"
if not globals().has_key("njetWeightHisto"):
  njetWeightHisto={}
  for htb in htvals+additionalHTIntervals:
    sigCut="ht>="+str(htb[0])+"&&ht<"+str(htb[1])+"&&"+preSelCut
    cMCTotal.Draw("njets>>hNJetMC(10,0,10)", "weight*("+sigCut+")", "goff")
    mcNJHisto =  ROOT.gDirectory.Get("hNJetMC").Clone()
    mcNJHisto.Scale(1./mcNJHisto.Integral())
    cData.Draw("njets>>hNJetData(10,0,10)", sigCut, "goff")
    dataNJHisto =  ROOT.gDirectory.Get("hNJetData").Clone()
    dataNJHisto.Scale(1./dataNJHisto.Integral())
    dataNJHisto.Divide(mcNJHisto) 
    njetWeightHisto[tuple(htb)]=dataNJHisto.Clone("njetRWHisto_ht_"+str(htb[0])+"_"+str(htb[1]))

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
sys = ['GluSplitUp', 'GluSplitDown', 'cFracUp', 'cFracDown', 'TTV_Up', 'TTV_Down', 'PUPlus', 'PUMinus']
#sys = ['cFracUp', 'TTV_Up', 'TTV_Down']

if SFsmall:
  SFSys = []
  sys = ['cFracUp', 'cFracDown']

if subdir.count("JES"):
  sys=[]


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
        if sfk=='PUPlus':
          weightFac = c.GetLeaf("weightPUSysPlus").GetValue()/c.GetLeaf("weight").GetValue()
        if sfk=='PUMinus':
          weightFac = c.GetLeaf("weightPUSysMinus").GetValue()/c.GetLeaf("weight").GetValue()
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
      res[sfk]["nEvents"] = len(weights1[sfk])
  return res 

#Either load or calculate SpF
#SpF_small =   pickle.load(file("/data/schoef/results2012/jackKnifeSpF_SFsmall.pkl"))

filename = "/data/schoef/results2012/"+subdir+prefix+"jackKnifeSpF.pkl"
if os.path.isfile(filename):
  SpF =   pickle.load(file(filename))

print filename

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
        sigCut="njets>="+str(njb[0])+"&&njets<="+str(njb[1])+"&&met>="+str(metb[0])+"&&met<"+str(metb[1])+"&&ht>="+str(htb[0])+"&&ht<"+str(htb[1])+"&&"+preSelCut
        res3po2 = getJackKnifeSpillFactor(cMC, sigCut, bt1='3p', bt2='2', njetReweightingHist=njetWeightHisto[tuple(htb)])
  #      res1o2 = getJackKnifeSpillFactor(cMC, sigCut, bt1='2', bt2='1', njetReweightingHist=njetWeightHisto[tuple(htb)])
        for sFk in SFSys+sys:
          SpF[tuple(htb)][tuple(metb)][tuple(njb)][sFk] = {}
          SpF[tuple(htb)][tuple(metb)][tuple(njb)][sFk]["3po2"] = res3po2[sFk]
   #       SpF[tuple(htb)][tuple(metb)][njb][sFk]["1o2"] = res1o2[sFk]
  if not small:
    pickle.dump(SpF, file(filename, "w"))
  else:
    print "No saving when small!"

#make plots
for inclData in [True, False]:
  if (not makePlots) or small:break
  htbins = [h[0] for h in htvals] + [htvals[-1][1]]
  ROOT.TH1F().SetDefaultSumw2()
  for metb in metbins:
    for njb in njetbins:
      l = ROOT.TLegend(0.6,0.55,1,1)
      l.SetFillColor(0)
      l.SetBorderSize(1)

      c1  =ROOT.TCanvas()
      SpFData_3po2 = ROOT.TH1F("SpF_3po2_Data","SpF", len(htbins) - 1, array('d',htbins))
      SpFData_2 = ROOT.TH1F("SpF_2_Data","SpF", len(htbins) - 1, array('d',htbins))
      SpFData_3 = ROOT.TH1F("SpF_3_Data","SpF", len(htbins) - 1, array('d',htbins))
      SpF_3po2 = {}
      for sFk in SFSys+sys:
        SpF_3po2[sFk] = ROOT.TH1F("SpF_3po2","SpF_"+sFk, len(htbins) - 1, array('d',htbins))
        SpF_3po2[sFk].SetLineColor(ROOT.kRed) 
        SpF_3po2[sFk].SetMarkerColor(ROOT.kRed) 

      for htb in htvals:
        print "\nHT bin", htb
        cut="njets>="+str(njb[0])+"&&njets<="+str(njb[1])+"&&met>"+str(metb[0])+"&&met<"+str(metb[1])+"&&ht>"+str(htb[0])+"&&ht<"+str(htb[1])+"&&"+preSelCut
        n_bt2 = cData.GetEntries(cut+"&&nbtags==2")
        n_bt3p = cData.GetEntries(cut+"&&nbtags>=3")
        SpFData_2.Fill(htb[0], n_bt2)
        SpFData_3.Fill(htb[0], n_bt3p)
        print htb, n_bt3p, n_bt2
        if n_bt2>0 and n_bt3p>0:
          r = n_bt3p/float(n_bt2)
          r_err = r*sqrt(1./n_bt3p+1./n_bt2)
          SpFData_3po2.SetBinContent(SpFData_3po2.FindBin(htb[0]), r)
          SpFData_3po2.SetBinError(SpFData_3po2.FindBin(htb[0]), r_err)
        for sFk in SFSys+sys:
          b = SpF_3po2[sFk].FindBin(htb[0])
          spf = SpF[tuple(htb)][tuple(metb)][tuple(njb)][sFk]
#          if sFk.count("cFrac"):
#            spf = SpF_small[tuple(htb)][tuple(metb)][tuple(njb)][sFk]
          spf = SpF[tuple(htb)][tuple(metb)][tuple(njb)][sFk]
          val = spf['3po2']['rForData']
          valErr = spf['3po2']['sigmaForData']
          if val<float('inf') and valErr<float('inf'): 
            SpF_3po2[sFk].SetBinContent(b, spf['3po2']['rForData'] )
            SpF_3po2[sFk].SetBinError(b, spf['3po2']['sigmaForData'])

      SpFData_3po2_TGA = ROOT.TGraphAsymmErrors(SpFData_3, SpFData_2, 'pois')

      SpF_3po2["SF"].GetYaxis().SetRangeUser(0,2.5*SpF_3po2['SF'].GetMaximum())
      SpF_3po2["SF"].GetXaxis().SetTitle("H_{T} (GeV)")
      SpF_3po2["SF"].GetYaxis().SetTitle("R_{32}")

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
#        SpFData_3po2_TGA.SetMarkerStyle(20)
#        SpFData_3po2_TGA.Draw("Psame")
#        l.AddEntry( SpFData_3po2_TGA, "Data")
        SpFData_3po2.Draw("same")
        l.AddEntry( SpFData_3po2, "Data")
      l.AddEntry( SpF_3po2["SF"], "MC (SF)")
      l.AddEntry( SpF_3po2["SF_b_Up"], "MC (SF) #pm 1 #sigma b.eff.")
      l.AddEntry( SpF_3po2["SF_light_Up"], "MC (SF) #pm 1 #sigma l.eff.")
      l.AddEntry( SpF_3po2["GluSplitUp"], "MC (SF) #pm 50% g split")
      l.AddEntry( SpF_3po2["cFracUp"], "MC (SF) #pm 1 #sigma c frac.")
      l.Draw()
      if inclData:
        pprefix = prefix+"withData_"
      else:
        pprefix = prefix+"noData_"
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/spillFactors/SpF_metb_"+subdir+pprefix+str(metb[0])+"_"+str(metb[1])+"_nj"+str(njb[0])+"-"+str(njb[1])+".png")
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/spillFactors/SpF_metb_"+subdir+pprefix+str(metb[0])+"_"+str(metb[1])+"_nj"+str(njb[0])+"-"+str(njb[1])+".pdf")
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/spillFactors/SpF_metb_"+subdir+pprefix+str(metb[0])+"_"+str(metb[1])+"_nj"+str(njb[0])+"-"+str(njb[1])+".root")

filenameCentral = "/data/schoef/results2012/"+subdir+"_fullMC_jackKnifeSpF.pkl"
SpFc = pickle.load(file(filenameCentral))
for njb in [(3,5), (6,99)]:
  if small: break
  for htb in [(500,2500), (750,2500), (1000,2500)]:
      for metb in [(150,250),(250,350),(350,450),(450,2500)]:
          print njb, htb, metb, round(SpFc[htb][metb][njb]['SF']['3po2']['rForData'],5),"+/-",round(SpFc[htb][metb][njb]['SF']['3po2']['sigmaForData'],5),"(stat.)",\
          "+/-",round(0.5*(SpF[htb][metb][njb]['SF_b_Up']['3po2']['rForData'] - SpF[htb][metb][njb]['SF_b_Down']['3po2']['rForData']),5),"(SFb)",\
          "+/-",round(0.5*(SpF[htb][metb][njb]['SF_light_Up']['3po2']['rForData'] - SpF[htb][metb][njb]['SF_light_Down']['3po2']['rForData']),5),"(SFl)",\
          "+/-",round(0.5*(SpF[htb][metb][njb]['cFracUp']['3po2']['rForData'] - SpF[htb][metb][njb]['cFracDown']['3po2']['rForData']),5),"(cFrac)",\
          "+/-",round(0.5*(SpF[htb][metb][njb]['GluSplitUp']['3po2']['rForData'] - SpF[htb][metb][njb]['GluSplitDown']['3po2']['rForData']),5),"(GluSplit)"

