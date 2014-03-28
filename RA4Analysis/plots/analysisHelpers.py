import ROOT
from math import *
import os
ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
metNormReg = [150, 250] #low MEt normalization region
verbose = False

htbins = [\
    [400,450   ],
    [450,500   ],
    [500,550   ],
    [550,600   ],
    [600,650   ],
    [650,700   ],
    [700,750   ],
    [750,800   ],
    [800,1000  ],
    [1000,1200 ],
    [1200,1500 ],
    [1500,2500 ]
  ]

#
# return list of individual ht bins covering the HT range
#   defined by htb
#
def getHtList (htb):
  htList = [ ]
  for h in htbins:
    if h[0]>=htb[0] and h[1]<=htb[1]:
      htList.append(h)
  if len(htList)==0 or htList[0][0]!=htb[0] or htList[-1][1]!=htb[1]:
    return None
  return htList

def getObjFromFile(fname, hname):
  f = ROOT.TFile(fname)
  assert not f.IsZombie()
  f.cd()
  htmp = f.Get(hname)
  if not htmp:  return htmp
  ROOT.gDirectory.cd('PyROOT:/')
  res = htmp.Clone()
  f.Close()
  return res

def tGraphIntegral(tgr, low, high="None"):
  int = 0.
  var = 0.
  xc = tgr.GetX()
  yc = tgr.GetY()
  yl = tgr.GetEYlow()
  yh = tgr.GetEYhigh()

  for i in range(tgr.GetN()):
    if xc[i]>=low and (high=="None" or xc[i]<high):
      int += yc[i]
      var += (.5*(yl[i] + yh[i]))**2
  return {"res":int,"sigma":sqrt(var)}

def histIntegral(h, xmin, xmax): #Rene Brun http://root.cern.ch/root/roottalk/roottalk03/2211.html
  axis = h.GetXaxis();
  bmin = axis.FindBin(xmin)
  bmax = axis.FindBin(xmax)
  integral = h.Integral(bmin,bmax)
#  print bmin, bmax, integral
  integral -= h.GetBinContent(bmin)*(xmin-axis.GetBinLowEdge(bmin))/axis.GetBinWidth(bmin)
  integral -= h.GetBinContent(bmax)*(axis.GetBinUpEdge(bmax)-xmax)/axis.GetBinWidth(bmax)
  return integral

#retrieve MC truth yield for any given region. 
#syntax: 
btbCut={'2p':"nbtags>=2", '2':"nbtags==2", '1':'nbtags==1', '0':'nbtags==0', 2:"nbtags==2", 1:'nbtags==1', 0:'nbtags==0', 'ex2':"nbtags==2", '3':"nbtags>=3", 3:"nbtags>=3", 'none':"(1)"}
leptonCut = "((singleMuonic&&nvetoMuons==1&&nvetoElectrons==0)||(singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))"
defMetBinning = [(1500-150)/25,150,1500]

def getRefChain(dir = "/data/schoef/convertedTuples_v19/copyMET/", mode = "MC", onlyTT = False):
  if mode.lower()=="mc":
    cMC   = ROOT.TChain("Events")
    cMC.Add(dir+"/Mu/TTJets-PowHeg/histo_TTJets-PowHeg.root")
    cMC.Add(dir+"/Ele/TTJets-PowHeg/histo_TTJets-PowHeg.root")
    if onlyTT:
      return cMC
    cMC.Add(dir+"/Mu/DY/histo_DY.root")
    cMC.Add(dir+"/Ele/DY/histo_DY.root")
    cMC.Add(dir+"/Mu/QCD/histo_QCD.root")
    cMC.Add(dir+"/Ele/QCD/histo_QCD.root")
#    cMC.Add(dir+"/Mu/WJetsHT250/histo_WJetsHT250.root")
#    cMC.Add(dir+"/Ele/WJetsHT250/histo_WJetsHT250.root")
    cMC.Add(dir+"/Mu/WJetsCombined/histo_WJetsCombined.root")
    cMC.Add(dir+"/Ele/WJetsCombined/histo_WJetsCombined.root")
    cMC.Add(dir+"/Mu/singleTop/histo_singleTop.root")
    cMC.Add(dir+"/Ele/singleTop/histo_singleTop.root")
    return cMC
  else:
    cData   = ROOT.TChain("Events")
    cData.Add(dir+"/Mu/data/histo_data.root")
    cData.Add(dir+"/Ele/data/histo_data.root")
    return cData

def getRefYield(btb, htb, metb, metvar, minNJet, chain, weight = "weight", additionalCut = "(1)", addError = False):
  leptonCut = metvar+">=150&&njets>="+str(minNJet)+"&&ht>=400&&((singleMuonic&&nvetoMuons==1&&nvetoElectrons==0)||(singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))&&"+additionalCut
  cut =  leptonCut+"&&ht>="+str(htb[0])+"&&ht<"+str(htb[1])+"&&"+metvar+">="+str(metb[0])+"&&"+metvar+"<"+str(metb[1])
  if btb>=0:
    cut+="&&"+btbCut[btb]
  cut = weight+"*("+cut+")"
  if addError and not ROOT.TH1.GetDefaultSumw2():
    ROOT.TH1.SetDefaultSumw2()
  chain.Draw("1>>htmp(1,0.5,1.5)", cut, "goff")
  htmp =  ROOT.gDirectory.Get("htmp")
  res = htmp.GetBinContent(1)
  eres = htmp.GetBinError(1)
  del htmp
  if not addError:
    return res
  else:
    return ( res, eres )

def getSignalYield(btb, htb, metb, metvar, minNJet, varX, varY, sms,  dir = '/data/adamwo/convertedTuples_v19/copyMET/', weight = "weight", correctForFastSim = False):

  if sms == "T1tttt" or sms=="T1tttt-madgraph":
    fstringMu  = dir+"/Mu/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
    fstringEle = dir+"/Ele/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
  if sms == "T1t1t":
    fstringMu  = dir+"/Mu/"+sms+"_"+str(varY)+"_"+str(varX)+"/histo_"+sms+"_"+str(varY)+"_"+str(varX)+".root"
    fstringEle = dir+"/Ele/"+sms+"_"+str(varY)+"_"+str(varX)+"/histo_"+sms+"_"+str(varY)+"_"+str(varX)+".root"
  if sms == "T5tttt":
    fstringMu  = dir+"/Mu/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
    fstringEle = dir+"/Ele/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
  if not (os.path.isfile(fstringMu) and os.path.isfile(fstringEle)):
    print "[getSignalYield] File missing!", fstringMu,fstringEle
    return 
  c = ROOT.TChain("Events")
  c.Add(fstringMu)
  c.Add(fstringEle)
  if c.GetEntries()==0:
    print "[getSignalYield] Files empty!"
    return 

  leptonCut = metvar+">=150&&njets>="+str(minNJet)+"&&ht>=400&&((singleMuonic&&nvetoMuons==1&&nvetoElectrons==0)||(singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))"
  cut =  leptonCut+"&&ht>="+str(htb[0])+"&&ht<"+str(htb[1])+"&&"+metvar+">="+str(metb[0])+"&&"+metvar+"<"+str(metb[1])
  if btb>=0:
    cut+="&&"+btbCut[btb]

  gluinoSystemPt = "sqrt( (gluino0Pt*cos(gluino0Phi) + gluino1Pt*cos(gluino1Phi))**2 + (gluino0Pt*sin(gluino0Phi) + gluino1Pt*sin(gluino1Phi))**2)"
  ISRRefWeight  = "(1.*("+gluinoSystemPt+"<120) + "+".95*( "+gluinoSystemPt+">120&&"+gluinoSystemPt+"<150) + "+".90*( "+gluinoSystemPt+">150&&"+gluinoSystemPt+"<250) + "+".80*( "+gluinoSystemPt+">250))"

  leptonAndHadWeight = "(0.98*(0.95*singleMuonic + singleElectronic*(0.86*(abs(leptonEta)>1.552) + 0.98*(abs(leptonEta)<=1.552) )))"
  leptonTriggerEff = "(0.96*singleElectronic + singleMuonic*( (abs(leptonEta)<0.9)*0.98 + (abs(leptonEta)>0.9)*0.84) )"

  cut = weight+"*("+cut+")"
  print cut
  if correctForFastSim:
    cut = ISRRefWeight+"*"+leptonAndHadWeight+"*"+leptonTriggerEff+"*"+cut
#    cut = leptonAndHadWeight+"*"+cut
    print "[getSignalYield] Correcting ISR and lepton weight"
  c.Draw(metvar+">>htmp(1,0,2500)", cut, "goff")
  htmp =  ROOT.gDirectory.Get("htmp")
  res = htmp.Integral()
  del c
  del htmp
  return res

def getBkgChain(dir = "/data/schoef/convertedTuples_v19/copyMET/", samples=None):
  if (not samples) or not ( type(samples)==type("") or type(samples)==type([]) or type(samples)==type(()))  :return
  if type(samples)==type(""):
    samples=[samples]
  cMC   = ROOT.TChain("Events")
  for s in samples:
    for l in ["Mu","Ele"]:
      fname = dir+"/"+l+"/"+s+"/histo_"+s+".root"
      if os.path.isfile(fname):
        print "Adding",fname
        cMC.Add(fname)
      else:
        print fname,"not found!"
  return cMC


def getSignalChain(varX, varY, sms,  dir = '/data/schoef/convertedTuples_v19/copyMET/'):
  if sms == "T1tttt" or sms=="T1tttt-madgraph":
    fstringMu  = dir+"/Mu/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
    fstringEle = dir+"/Ele/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
  if sms == "T1t1t":
    fstringMu  = dir+"/Mu/"+sms+"_"+str(varY)+"_"+str(varX)+"/histo_"+sms+"_"+str(varY)+"_"+str(varX)+".root"
    fstringEle = dir+"/Ele/"+sms+"_"+str(varY)+"_"+str(varX)+"/histo_"+sms+"_"+str(varY)+"_"+str(varX)+".root"
  if sms == "T5tttt":
    fstringMu  = dir+"/Mu/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
    fstringEle = dir+"/Ele/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
  if not (os.path.isfile(fstringMu) and os.path.isfile(fstringEle)):
    print "[getSignalYield] File missing!", fstringMu,fstringEle
    return 
  c = ROOT.TChain("Events")
  print "Adding",fstringMu
  c.Add(fstringMu)
  print "Adding",fstringEle
  c.Add(fstringEle)
  
  if c.GetEntries()==0:
    print "[getSignalYield] Files empty!"
    return 
  return c

def getCutSignalYield(c, cut,  weight = "weight", correctForFastSim = True, mtcut = None) :

  if correctForFastSim:
    gluinoSystemPt = "sqrt( (gluino0Pt*cos(gluino0Phi) + gluino1Pt*cos(gluino1Phi))**2 + (gluino0Pt*sin(gluino0Phi) + gluino1Pt*sin(gluino1Phi))**2)"
    ISRRefWeight  = "(1.*("+gluinoSystemPt+"<120) + "+".95*( "+gluinoSystemPt+">120&&"+gluinoSystemPt+"<150) + "+".90*( "+gluinoSystemPt+">150&&"+gluinoSystemPt+"<250) + "+".80*( "+gluinoSystemPt+">250))"

    leptonAndHadWeight = "(0.98*(0.95*singleMuonic + singleElectronic*(0.86*(abs(leptonEta)>1.552) + 0.98*(abs(leptonEta)<=1.552) )))"
    leptonTriggerEff = "(0.96*singleElectronic + singleMuonic*( (abs(leptonEta)<0.9)*0.98 + (abs(leptonEta)>0.9)*0.84) )"
    weight = ISRRefWeight+"*"+leptonAndHadWeight+"*"+leptonTriggerEff+"*("+weight+")"
#    cut = leptonAndHadWeight+"*"+cut
    print "[getSignalYield] Correcting ISR and lepton weight"

  weight = weight+"*("+cut+")"
  if mtcut:
    from funcs import type1phiMT
    mTVar = "sqrt(2.*(leptonPt*(type1phiMet - type1phiMetpx*cos(leptonPhi) - type1phiMetpy*sin(leptonPhi) )))"
    weight = weight+"*("+cut+")*("+mTVar+">="+str(mtcut[0])+"&&"+mTVar+"<"+str(mtcut[1])+")"
#  print weight
  htmp = ROOT.TH1F("htmp","htmp",1,0,2500)
  htmp.Sumw2()
  c.Draw("1>>htmp", weight, "goff")
#  htmp =  ROOT.gDirectory.Get("htmp")
  res = htmp.GetBinContent(1)
  err = htmp.GetBinError(1)
  del c
  del htmp
  return {'res':res, 'err':err}


def getRefMetHisto(chain, cut, binning=defMetBinning, metVar="type1phiMet", weight="weight"):
  wCut = weight+"*("+cut+")"
  print "[getMetHisto] Using binning", binning,"cut",wCut
  chain.Draw(metVar+">>hTMP("+str(binning[0])+","+str(binning[1])+","+str(binning[2])+")", wCut, "goff")
  h = ROOT.gDirectory.Get("hTMP").Clone()
  return h

defInDir = '/afs/hephy.at/user/s/schoefbeck/www/FitRes2012/Results_copyMET_dontFold_constrainParetoShape_convertedTuples_v16_with_weight_weight_fitMC_MuonElectron_jet5pt40__bt1_150.0-met-1500.0__bt2_150.0-met-400.0__bt1_400.0-ht-2500.0__bt2_400.0-ht-750.0_intLumi-20p0_130304_1440/err_sampling_750_ht_2500/'

def getNormRegYield(inDir, btb, htb):
  if type(btb)==type(0):
    btb = str(btb)
  hname = 'h_metnorm_yield_sumpdf_bt'+btb+"_"+str(htb[0])+'_ht_'+str(htb[1])
  ifile = inDir+"/"+hname+".root"
  if os.path.exists(ifile):
    htbs = [ htb ]
  else:
    htbs = getHtList(htb)
  sumyield = 0.
  sumyieldVar = 0.
  for iht,htbb in enumerate(htbs):
    hname = 'h_metnorm_yield_sumpdf_bt'+btb+"_"+str(htbb[0])+'_ht_'+str(htbb[1])
    ifile = inDir.replace("err_sampling_"+str(htb[0])+"_ht_"+str(htb[1]),"err_sampling_"+str(htbb[0])+"_ht_"+str(htbb[1]))
    ifile += "/"+hname+".root"
    normyield    = getObjFromFile(ifile, hname).GetBinContent(1)
    normyieldErr = getObjFromFile(ifile, hname).GetBinError(1)
    sumyield += normyield
    sumyieldVar += normyieldErr*normyieldErr
  return sumyield, sqrt(sumyieldVar)

def getInputMetShape(inDir, btb, htb):
  if type(btb)==type(0):
    btb = str(btb)
  hname = "h_data_yield_bt"+btb+"_"+str(htb[0])+"_ht_"+str(htb[1])
  ifile = inDir+"/"+hname+".root"
  print hname
  data_hist =   getObjFromFile(ifile, hname)
  return data_hist

def getPredictedMetShapes(inDir, btb, htb):
  if type(btb)==type(0):
    btb = str(btb)
  hname = "h_central_bt"+btb+"_"+str(htb[0])+"_ht_"+str(htb[1])+"__type1phiMet"
  ifile = inDir+"/err_sampling_"+str(htb[0])+"_ht_"+str(htb[1])+"/"+hname
  if os.path.exists(ifile+".root"):
    htbs = [ htb ]
  else:
    htbs = getHtList(htb)
  result = { }
  for iht,htbb in enumerate(htbs):
    hname = "h_central_bt"+btb+"_"+str(htbb[0])+"_ht_"+str(htbb[1])+"__type1phiMet"
    ifile = inDir+"/err_sampling_"+str(htbb[0])+"_ht_"+str(htbb[1])+"/"+hname
    h_central = getObjFromFile(ifile+".root", hname)
    h_varDown = getObjFromFile(ifile+"_varDown.root", hname+"_varDown")
    h_varUp = getObjFromFile(ifile+"_varUp.root", hname+"_varUp")
    h_varMedian = getObjFromFile(ifile+"_varMedian.root", hname+"_varMedian")
    if iht==0:
      result["central"] = h_central
      result["varDown"] = h_varDown
      result["varUp"] = h_varUp
      result["varMedian"] = h_varMedian
    else:
      result["central"].Add(h_central)
      result["varDown"].Add(h_varDown)
      result["varUp"].Add(h_varUp)
      result["varMedian"].Add(h_varMedian)
  return result
  
def getSampledMetShapePrediction(inDir, btb, htb, n=100):
  if type(btb)==type(0):
    btb = str(btb)
  ifile = inDir+"err_sampling_"+str(htb[0])+"_ht_"+str(htb[1])+"/sampled_histo.root"
  if os.path.exists(ifile):
    htbs = [ htb ]
  else:
    htbs = getHtList(htb)
  res = []
  for iht,htbb in enumerate(htbs):
    ifile = inDir+"err_sampling_"+str(htbb[0])+"_ht_"+str(htbb[1])+"/sampled_histo.root"
    i = 0
    while i < n:
#  for i in range(n):
      hname = "h_variation"+str(i)+"_bt"+btb+"_"+str(htbb[0])+"_ht_"+str(htbb[1])+"__type1phiMet"
      h = getObjFromFile(ifile,hname)
      if not h: break
      if iht==0:
        res.append(h.Clone())
      else:
        res[i].Add(h)
      i += 1
#  print "Found ",len(res)," histograms"
  return res

def convertMatrixToRoot(l):
  n=len(l)
  m=len(l[0])
  rm = ROOT.TMatrixD(n,m)
  for i in range(n):
    for j in range(m):
      rm[i][j] = l[i][j]
  return rm

defRegions = [\
  {'btb':'2',"htb":[750,2500], "metb":[250,350]},  
  {'btb':'2',"htb":[750,2500], "metb":[350,450]},  
  {'btb':'2',"htb":[750,2500], "metb":[450,2500]},  
  {'btb':'2',"htb":[400,750], "metb":[250,2500]},
#  {'btb':'2',"htb":[400,750], "metb":[350,450]},  
#  {'btb':'2',"htb":[400,750], "metb":[450,2500]},  
  ]

testInDir = '/data/kwolf/RA4Fit2012_6j/output/Res_copyMET_separateBTagWeights_constrPareto_fitData_MuonElectron_jet5pt40__bt1_150.0-met-1500.0__bt2_150.0-met-400.0__bt1_400.0-ht-2500.0__bt2_400.0-ht-750.0_intLumi-20p0_130404_1603/'

def getSamplingCovrianceMatrix(inDir, regions, n=100, sumUpSingleBins = True ):
  if sumUpSingleBins:
    htbinsConsidered = htbins
  else:
    htbinsConsidered = list(set([tuple(r['htb']) for r in regions]))
  dim = len(regions)
  for htb in htbinsConsidered:
    for r in regions:
      if sumUpSingleBins and ( not (htb[0]>=r['htb'][0] and htb[1]<=r['htb'][1])): continue  
      if (not sumUpSingleBins) and ( not (htb[0]==r['htb'][0] and htb[1]==r['htb'][1])): continue
#      print "sumUpSingleBins", sumUpSingleBins,"adding",htb,"for",r['htb'],r['metb'],r['btb']
      histos = getSampledMetShapePrediction(inDir, r['btb'], htb,n)
      if not r.has_key("samplingRes"):
        r["samplingRes"] = [histos]
      else:
        r["samplingRes"].append(histos)
  for i in range(dim): #Transpose
    regions[i]['samplingRes'] =   zip(*(regions[i]['samplingRes']))

  for r in regions:
    r['samplingInt'] = []
    for s in r['samplingRes']:
      res = 0.
      for h in s:
        res+=histIntegral(h, r['metb'][0], r['metb'][1]) 
      r['samplingInt'].append(res)
    r.pop('samplingRes', None)

  for r in regions:
    r['mean'] = sum(r['samplingInt'])/float(len(r['samplingInt']))

  cov={}
  for i1, r1 in enumerate(regions):
    cov[i1]={}
    for i2, r2 in enumerate(regions):
      if i1<=i2:
        covi1i2=0.
        for k in range(len(r1['samplingInt'])):
          covi1i2+=(r1['samplingInt'][k] - r1['mean'])*(r2['samplingInt'][k] - r2['mean'])
        cov[i1][i2]=covi1i2/float(len(r1['samplingInt']))
      else:
        cov[i1][i2] = cov[i2][i1]
  
  covM = [[] for i in range(dim)]
  corM = [[] for i in range(dim)]
  for i1 in range(dim):
    for i2 in range(dim):
#      mk1 = tuple(mb1); mk2 = tuple(mb2)
      covM[i1].append(cov[i1][i2]) 
      norm = sqrt(cov[i1][i1]*cov[i2][i2])
      if norm>0:
        corM[i1].append(cov[i1][i2]/norm) 
  ratioCovM = covM
  for i1 in range(dim):
    for i2 in range(dim):
      ratioCovM[i1][i2]/=(regions[i1]['mean']*regions[i2]['mean'])
  for r in regions:
    r.pop('samplingRes', None)
  return {'covM':convertMatrixToRoot(covM), 'corM':convertMatrixToRoot(corM), 'ratioCovM':convertMatrixToRoot(ratioCovM),'means':[r['mean'] for r in regions]}

def getSampledMetYieldPrediction(inDir, btb, htb, metb, n=100, matrixFormat="list"):
  fitResult = getPredictedMetShapes(inDir, btb, htb)
  if not type(metb[0])==type([]):
    metbins = [metb]
  else:
    metbins = metb
#  print "met-Bins",metbins

  histos = getSampledMetShapePrediction(inDir, btb, htb, n)
  res={}
  mean={}
  central={}
  for mb in metbins:
    res[tuple(mb)] = [histIntegral(x, mb[0], mb[1]) for x in histos]
    mean[tuple(mb)] = sum(res[tuple(mb)])/float(len(res[tuple(mb)]))
    central[tuple(mb)] = histIntegral(fitResult['central'], mb[0], mb[1]) 

  cov={}
  for i1, mb1 in enumerate(metbins):
    cov[i1]={}
    for i2, mb2 in enumerate(metbins):
      if i1<=i2:
        covi1i2=0.
        for k in range(len(res[tuple(mb1)])):
          covi1i2+=(res[tuple(mb1)][k] - mean[tuple(mb1)])*(res[tuple(mb2)][k] - mean[tuple(mb2)])
        cov[i1][i2]=covi1i2/float(len(res[tuple(mb1)]))
      else:
        cov[i1][i2] = cov[i2][i1]

  covM = [[] for i in range(len(cov.keys()))]
  corM = [[] for i in range(len(cov.keys()))]
  for i1, mb1 in enumerate(metbins):
    for i2, mb2 in enumerate(metbins):
#      mk1 = tuple(mb1); mk2 = tuple(mb2)
      covM[i1].append(cov[i1][i2]) 
      norm = sqrt(cov[i1][i1]*cov[i2][i2])
      if norm>0:
        corM[i1].append(cov[i1][i2]/norm) 

  resDicts = {}
  for mb in metbins:
    res[tuple(mb)].sort()
    ivar_qdown = int(round(0.16*(len(res[tuple(mb)])-1)))
    ivar_qmedian = int(round(0.5*(len(res[tuple(mb)])-1)))
    ivar_qup = int(round(0.84*(len(res[tuple(mb)])-1)))
    resDicts[tuple(mb)] =  {"varDown":res[tuple(mb)][ivar_qdown], "varMedian":res[tuple(mb)][ivar_qmedian], "varUp":res[tuple(mb)][ivar_qup], "samplingMean":mean[tuple(mb)],\
                            "central":central[tuple(mb)]}
  if matrixFormat.lower()=="root":
    covM = convertMatrixToRoot(covM)
    corM = convertMatrixToRoot(corM)
  return {"results":resDicts, "covMatrix":covM, "corMatrix":corM}

#def getNormRegYieldFromSamplingDirectory(inDir, btb, htb):
#  hname = 'h_metnorm_yield_sumpdf_bt'+str(btb)+"_"+str(htb[0])+"_ht_"+str(htb[1])
#  ifile = inDir+"/err_sampling_"+str(htb[0])+"_ht_"+str(htb[1])+"/"+hname
#  normyield    = getObjFromFile(ifile+".root", hname).GetBinContent(1)
#  normyieldErr = getObjFromFile(ifile+".root", hname).GetBinError(1)
#  return normyield, normyieldErr
#
#def getDataMetShapeFromSamplingDirectory(inDir, btb, htb):
#  ifile = inDir+"/err_sampling_"+str(htb[0])+"_ht_"+str(htb[1])+"/c_sum_model_bt"+str(btb)+"_"+str(htb[0])+"_ht_"+str(htb[1])+".root"
#  canv_name = "c_sum_model_bt"+str(btb)+"_"+str(htb[0])+"_ht_"+str(htb[1])
#  canv =   getObjFromFile(ifile, canv_name)
#  data_hist = canv.GetPrimitive("plot_data_bt"+str(btb)+"_ht_"+str(htb[0])+"_"+str(htb[1])).Clone()
#  return data_hist

#def getDataMetShape(inDir, btb, htb):
#  ifile = inDir+"/c_metfit_ht"+"_"+str(htb[0])+"_"+str(htb[1])+"_bt_"+str(btb)+"_MuonElectron_plusminus.root"
#  canv_name = "c_metfit_ht"+"_"+str(htb[0])+"_"+str(htb[1])+"_bt_"+str(btb)+"_MuonElectron_plusminus"
#  canv =   getObjFromFile(ifile, canv_name)
#  for item in canv.GetListOfPrimitives():
#    if isinstance(item,ROOT.RooHist):
##      print item.GetName()
##      print item.GetMarkerColor(),item.GetLineColor()
#      if item.GetMarkerColor()==1 and item.GetLineColor()==1:
##        print "Going to return ",type(item)
#        return item.Clone()
#  print "[getDataMetShape] Failed"
#  return None
#
#def getNormRegYieldFromSamplingDirectory(inDir, btb, htb):
#  hname = 'h_metnorm_yield_sumpdf_bt'+str(btb)+"_"+str(htb[0])+"_ht_"+str(htb[1])
#  ifile = inDir+"/err_sampling_"+str(htb[0])+"_ht_"+str(htb[1])+"/"+hname
#  normyield    = getObjFromFile(ifile+".root", hname).GetBinContent(1)
#  normyieldErr = getObjFromFile(ifile+".root", hname).GetBinError(1)
#  return normyield, normyieldErr
#
#def getPredictionFromSamplingDirectory(inDir, btb, htb, metb, metvar = "met", blowUpStatErr = 1):
#  ifile = inDir+"/err_sampling_"+str(htb[0])+"_ht_"+str(htb[1])+"/h_central_bt"+str(btb)+"_"+str(htb[0])+"_ht_"+str(htb[1])+"__"+metvar
#  if verbose: print "[getPredictionFromSamplingDirectory] Using",ifile
#
#  #Load fit result
#  hname = 'h_central_bt'+str(btb)+"_"+str(htb[0])+"_ht_"+str(htb[1])+"__"+metvar
#  centralShape = getObjFromFile(ifile+".root", hname)                                   #Get the central shape (i.e. fit result)
#  centralShapeNormRegYield  = histIntegral(centralShape, metNormReg[0], metNormReg[1])  #intgrate in normalization and signal region
#  centralShapeSigRegYield   = histIntegral(centralShape, metb[0], metb[1])
#
#  #Load the median and the quantil shapes and calculate the yields in the signal region
#  if verbose: print ifile+"_varMedian.root", hname
#  medianShape  = getObjFromFile(ifile+"_varMedian.root", hname+"_varMedian")
#  medianShapeSigRegYield   = histIntegral(medianShape, metb[0], metb[1])
#  varUpShape = getObjFromFile(ifile+"_varUp.root", hname+"_varUp")
#  varUpShapeSigRegYield   = histIntegral(varUpShape, metb[0], metb[1])
#  varDownShape = getObjFromFile(ifile+"_varDown.root", hname+"_varDown")
#  varDownShapeSigRegYield   = histIntegral(varDownShape, metb[0], metb[1])
#
#  #retrieve the normalization yield. This is just the MC yield in the low MET control region (can checked inedpendently with getMCTruthYield)
#  normYield, normYieldErr = getNormRegYieldFromSamplingDirectory(inDir, btb, htb) 
#
#  #calculate the central value and the model error. We take the asymmetric model error wrt. the median and use it for the fitres. 
#  #This works if the fit converged well, otherwise the high-MET tail sampling distribution can become very skew and the central value might leave the 68% conf. interv. of the sampling distribution.
#  res     = normYield/centralShapeNormRegYield*centralShapeSigRegYield
#  resUp   = normYield/centralShapeNormRegYield*(varUpShapeSigRegYield    - medianShapeSigRegYield  + centralShapeSigRegYield)
#  resDown = normYield/centralShapeNormRegYield*(varDownShapeSigRegYield  - medianShapeSigRegYield  + centralShapeSigRegYield)
#  #Calculate combined errors, including SumW2 or Poissonian fluctuation of the normalization yield
#  sigmaUp   = resUp   - res
#  sigmaDown = resDown - res
#  combinedUncertaintySumW2Plus  = res + sqrt(res**2*normYieldErr**2/normYield**2 + sigmaUp**2)
#  combinedUncertaintySumW2Minus = res - sqrt(res**2*normYieldErr**2/normYield**2 + sigmaDown**2)
#  combinedUncertaintyPoissonianPlus  = res + sqrt(res**2/normYield + sigmaUp**2)
#  combinedUncertaintyPoissonianMinus = res - sqrt(res**2/normYield + sigmaDown**2)
#
#  #make sure the shapes are normalized correctly
#  scaleFac = normYield/centralShapeNormRegYield
#  print "[getPredictionFromSamplingDirectory] Using scaleFac",scaleFac
#  centralShape.Scale(scaleFac)
#  medianShape .Scale(scaleFac)
#  varUpShape  .Scale(scaleFac)
#  varDownShape.Scale(scaleFac)
#
#  #Write y(x) = n*f(x) and propagate error on n into y. The error on n can be SumW2 or Poissonian. Formulae for  y+-sigma(y), sigma(y)(x)=sqrt(sigma(n)**2*y(x)**2/n**2 + sigma(y)(x)**2) ~ sqrt(1/n y**2 + var(y))
#  #calculate sigma(f)(x) shapes: sigma(f)+/- = f(+/-) - median + central
#  sigmaShapePlus   = varUpShape.Clone()
#  sigmaShapeMinus  = varDownShape.Clone()
#  sigmaShapePlus.Scale(-1.)
#  sigmaShapeMinus.Scale(-1.)
#  sigmaShapePlus.Add(medianShape) 
#  sigmaShapeMinus.Add(medianShape) 
#  sigmaShapePlus.Scale(-1.)
#  sigmaShapeMinus.Scale(-1.)
#  sigmaShapePlus.Add(centralShape) 
#  sigmaShapeMinus.Add(centralShape) 
#
#  combinedUncertaintyShapeSumW2Plus  =  sigmaShapePlus.Clone("combinedUncertaintyShapeSumW2Plus")
#  combinedUncertaintyShapeSumW2Plus.Reset()
#  combinedUncertaintyShapeSumW2Minus     =  combinedUncertaintyShapeSumW2Plus.Clone("combinedUncertaintyShapeSumW2Minus")
#  combinedUncertaintyShapePoissonianPlus =  combinedUncertaintyShapeSumW2Plus.Clone("combinedUncertaintyShapePoissonianPlus")
#  combinedUncertaintyShapePoissonianMinus=  combinedUncertaintyShapeSumW2Plus.Clone("combinedUncertaintyShapePoissonianMinus")
#  for i in range(sigmaShapePlus.GetNbinsX()+1):
#    y = centralShape.GetBinContent(i)
#    sigmaShapePlus_y   = sigmaShapePlus.GetBinContent(i) - centralShape.GetBinContent(i)
#    sigmaShapeMinus_y  = sigmaShapeMinus.GetBinContent(i) - centralShape.GetBinContent(i)
#    combinedUncertaintyShapeSumW2Plus        .SetBinContent(i, y + sqrt(blowUpStatErr**2*y**2*normYieldErr**2/normYield**2 + sigmaShapePlus_y**2))
#    combinedUncertaintyShapeSumW2Minus       .SetBinContent(i, y - sqrt(blowUpStatErr**2*y**2*normYieldErr**2/normYield**2 + sigmaShapeMinus_y**2))
#    combinedUncertaintyShapePoissonianPlus   .SetBinContent(i, y + sqrt(blowUpStatErr**2*y**2/normYield + sigmaShapePlus_y**2))
#    combinedUncertaintyShapePoissonianMinus  .SetBinContent(i, y - sqrt(blowUpStatErr**2*y**2/normYield + sigmaShapeMinus_y**2))
#  data_hist = getDataMetShapeFromSamplingDirectory(inDir, btb, htb)
#  dataYield = tGraphIntegral(data_hist, metb[0], metb[1])
##  ifile = inDir+"/err_sampling_"+str(htb[0])+"_ht_"+str(htb[1])+"/c_sum_model_bt"+str(btb)+"_"+str(htb[0])+"_ht_"+str(htb[1])+".root"
##  canv_name = "c_sum_model_bt"+str(btb)+"_"+str(htb[0])+"_ht_"+str(htb[1])
##  canv =   getObjFromFile(ifile, canv_name)
##  data_hist = canv.GetPrimitive("plot_data_bt"+str(btb)+"_ht_"+str(htb[0])+"_"+str(htb[1])).Clone()
#
#  resDict = {"predictedYield":res, "predictedYield_Uncertainty_Model_Up":resUp, "predictedYield_Uncertainty_Model_Down":resDown, "normRegYield":normYield, "normRegYieldErr":normYieldErr, \
#             "predictedYield_Uncertainty_CombinedSumW2_Up":combinedUncertaintySumW2Plus, "predictedYield_Uncertainty_CombinedSumW2_Down":combinedUncertaintySumW2Minus, 
#             "predictedYield_Uncertainty_CombinedPoissonian_Up":combinedUncertaintyPoissonianPlus, "predictedYield_Uncertainty_CombinedPoissonian_Down":combinedUncertaintyPoissonianMinus,
#             "predictedShape":centralShape,"dataShape":data_hist,"dataYield":dataYield,
#             "predictedShape_Uncertainty_Model_Up":sigmaShapePlus, "predictedShape_Uncertainty_Model_Down":sigmaShapeMinus,
#             "predictedShape_Uncertainty_CombinedSumW2_Up":combinedUncertaintyShapeSumW2Plus, "predictedShape_Uncertainty_CombinedSumW2_Down":combinedUncertaintyShapeSumW2Minus, 
#             "predictedShape_Uncertainty_CombinedPoissonian_Up":combinedUncertaintyShapePoissonianPlus, "predictedShape_Uncertainty_CombinedPoissonian_Down":combinedUncertaintyShapePoissonianMinus
#              }
#  return resDict
#
#def getUncertaintyFromSamplingDirectory(refDir, plusDir, minusDir, plotRefHisto, btb, htb, metb, metvar = "met"):
#  fname = "/err_sampling_"+str(htb[0])+"_ht_"+str(htb[1])+"/h_central_bt"+str(btb)+"_"+str(htb[0])+"_ht_"+str(htb[1])+"__"+metvar
#  ifilePlus    = plusDir+"/"+fname+".root"
#  ifileMinus   = minusDir+"/"+fname+".root"
#  ifileReference  = refDir+"/"+fname+".root"
##  ifilePlotReference  = plotRefDir+"/"+fname+".root"
#  if verbose: print "[getUncertaintyFromSamplingDirectory] using:\n","Plus   :",ifilePlus,"\n","Minus  :",ifileMinus,"\n","Ref    :",ifileReference,"\n"#,"plotRef:",ifilePlotReference
#
#  #load fit result
#  hname = 'h_central_bt'+str(btb)+"_"+str(htb[0])+"_ht_"+str(htb[1])+"__"+metvar
#  plusShape = getObjFromFile(ifilePlus, hname)                                   #get the central shape for Plus 
#  minusShape = getObjFromFile(ifileMinus, hname)                                 #get the central shape for Minus 
#  referenceShape = getObjFromFile(ifileReference, hname)                               #get the central shape for Reference 
##  plotReferenceShape = getObjFromFile(ifilePlotReference, hname)                               #get the central shape for Reference 
#
#  referenceNormregyield     = histIntegral(referenceShape, metNormReg[0], metNormReg[1])  #intgrate in normalization and signal region
##  plotReferenceNormregyield     = histIntegral(plotReferenceShape, metNormReg[0], metNormReg[1])  #intgrate in normalization and signal region
#  referenceSigregyield      = histIntegral(referenceShape, metb[0], metb[1])
#  plusNormregyield       = histIntegral(plusShape, metNormReg[0], metNormReg[1])  #intgrate in normalization and signal region
#  plusSigregyield        = histIntegral(plusShape, metb[0], metb[1])
#  minusNormregyield      = histIntegral(minusShape, metNormReg[0], metNormReg[1])  #intgrate in normalization and signal region
#  minusSigregyield       = histIntegral(minusShape, metb[0], metb[1])
#
#  #retrieve the normalization yield. this is just the mc yield in the low met control region (can checked inedpendently with getmctruthyield)
#  normYield, normYieldErr                   = getNormRegYieldFromSamplingDirectory(refDir, btb, htb) 
#  normYieldPlus, normYieldPlusErr     = getNormRegYieldFromSamplingDirectory(plusDir, btb, htb) 
#  normYieldMinus, normYieldMinusErr   = getNormRegYieldFromSamplingDirectory(minusDir, btb, htb) 
#
#  #calculate the central value and the model error. we take the asymmetric model error wrt. the median and use it for the fitres. 
#  #this works if the fit converged well, otherwise the high-met tail sampling distribution can become very skew and the central value might leave the 68% conf. interv. of the sampling distribution.
#  res_ref       = normYield         /referenceNormregyield*referenceSigregyield
#  res_plus      = normYieldPlus  /plusNormregyield  *plusSigregyield
#  res_minus     = normYieldMinus /minusNormregyield *minusSigregyield
#  true_ref      = tGraphIntegral(getDataMetShapeFromSamplingDirectory(refDir, btb, htb), metb[0], metb[1])
#  true_plus     = tGraphIntegral(getDataMetShapeFromSamplingDirectory(plusDir, btb, htb), metb[0], metb[1]) 
#  true_minus    = tGraphIntegral(getDataMetShapeFromSamplingDirectory(minusDir, btb, htb), metb[0], metb[1])
#
#  relSysDRPlus   = res_plus/true_plus['res'] / (res_ref / true_ref['res'])
#  relSysDRMinus =  res_minus/true_minus['res'] / (res_ref / true_ref['res'])
#  relAbsSysDR = max(abs(1.-relSysDRPlus),abs(1.-relSysDRMinus))
#  relAbsSysSR = abs((res_plus - res_minus)/(res_minus + res_plus))
#  print "res: +/-",res_plus, res_minus,"true+/-", true_plus['res'], true_minus['res'], true_ref['res']
#  # relSysDRPlus, relSysDRMinus, relAbsSysDR 
#  #make sure the shapes are normalized correctly. #shapes are normalized wrt. to the control region of the central value because the normalization effect cancels out in the sys. uncert. of integrated yields
#  referenceShape.Scale(normYield/referenceNormregyield)  
##  plotReferenceShape.Scale(normYield/plotReferenceNormregyield)  
#  plusShape  .Scale(normYield/plusNormregyield)  
#  minusShape .Scale(normYield/minusNormregyield)  
#  
#  ErrorShape = plotRefHisto.Clone()
#  for i in range(ErrorShape.GetNbinsX()+1):
#    if referenceShape.GetBinContent(i)>0:
#      ErrorShape.SetBinError(i, (plotRefHisto.GetBinContent(i)/referenceShape.GetBinContent(i))*max(abs(plusShape.GetBinContent(i) - referenceShape.GetBinContent(i)), abs(minusShape.GetBinContent(i) - referenceShape.GetBinContent(i))))
##    print ErrorShape.GetBinError(i)
#  return {\
#          "predictedYield_Reference":res_ref, "predictedYield_Plus":res_plus, "predictedYield_Minus":res_minus, 
#          "trueYield_Reference":true_ref, "trueYield_Plus":true_plus, "trueYield_Minus":true_minus, 
#          "refShape":referenceShape, "plusShape":plusShape, "minusShape":minusShape,
#          "refShapeWithError":ErrorShape,
#          "relSysDRPlus" : relSysDRPlus, 
#          "relSysDRMinus" : relSysDRMinus,
#          "relAbsSysDR" : relAbsSysDR, "relAbsSysSR":relAbsSysSR,
#          "tmp":getDataMetShapeFromSamplingDirectory(plusDir, btb, htb)
#         }
#
#def getUncertainty(refDir, plusDir, minusDir, plotRefHisto, btb, htb, metb, metvar = "met", patchRef = False):
#  res_sum_ref = 0.
#  res_sum_plus = 0.
#  res_sum_minus = 0.
#  true_sum_ref = 0.
#  true_sum_plus = 0.
#  true_sum_minus = 0.
#
#  if type(btb)==list:
#    btbins = btb
#  else:
#    btbins = [ btb ]
#    
#  htbinslow = None
#  htbinshigh = None 
#  for htbin in htbins:
#    if not ( htbin[0]>=htb[0] and htbin[1]<=htb[1] ): continue
#    if htbinslow==None or htbin[0]<htbinslow:  htbinslow = htbin[0]
#    if htbinshigh==None or htbin[1]>htbinshigh:  htbinshigh = htbin[1]
#    for btb in btbins:
#      fname = "h_conv_sumcharge_sumpdf_met_ht_" + str(htbin[0]) + "_" + str(htbin[1]) + "_bt" + str(btb) + "__met"
#      ifilePlus    = plusDir+"/"+fname+".root"
#      ifileMinus   = minusDir+"/"+fname+".root"
#      ifileReference  = refDir+"/"+fname+".root"
#    #  ifilePlotReference  = plotRefDir+"/"+fname+".root"
#      if verbose: print "[getUncertainty] using:\n","Plus   :",ifilePlus,"\n","Minus  :",ifileMinus,"\n","Ref    :",ifileReference,"\n"#,"plotRef:",ifilePlotReference
#
#      #load fit result
#    #  hname = "h_conv_sumcharge_sumpdf_met_ht_" + str(htbin[0]) + "_" + str(htbin[1]) + "_bt" + str(btb) + "__met"
#      hname = fname
#      plusShape = getObjFromFile(ifilePlus, hname)                                   #get the central shape for Plus 
#      minusShape = getObjFromFile(ifileMinus, hname)                                 #get the central shape for Minus 
#      referenceShape = getObjFromFile(ifileReference, hname)                               #get the central shape for Reference 
#
#      referenceNormregyield     = histIntegral(referenceShape, metNormReg[0], metNormReg[1])  #intgrate in normalization and signal region
#    #  plotReferenceNormregyield     = histIntegral(plotReferenceShape, metNormReg[0], metNormReg[1])  #intgrate in normalization and signal region
#      referenceSigregyield      = histIntegral(referenceShape, metb[0], metb[1])
#      plusNormregyield       = histIntegral(plusShape, metNormReg[0], metNormReg[1])  #intgrate in normalization and signal region
#      plusSigregyield        = histIntegral(plusShape, metb[0], metb[1])
#      minusNormregyield      = histIntegral(minusShape, metNormReg[0], metNormReg[1])  #intgrate in normalization and signal region
#      minusSigregyield       = histIntegral(minusShape, metb[0], metb[1])
#
#      #retrieve the normalization yield. this is just the mc yield in the low met control region (can checked inedpendently with getmctruthyield)
#      normYield, normYieldErr                   = getNormRegYield(refDir, btb, htbin) 
#      normYieldPlus, normYieldPlusErr     = getNormRegYield(plusDir, btb, htbin) 
#      normYieldMinus, normYieldMinusErr   = getNormRegYield(minusDir, btb, htbin) 
#
#      #calculate the central value and the model error. we take the asymmetric model error wrt. the median and use it for the fitres. 
#      #this works if the fit converged well, otherwise the high-met tail sampling distribution can become very skew and the central value might leave the 68% conf. interv. of the sampling distribution.
#      res_ref       = normYield         /referenceNormregyield*referenceSigregyield
#      res_plus      = normYieldPlus  /plusNormregyield  *plusSigregyield
#      res_minus     = normYieldMinus /minusNormregyield *minusSigregyield
#      true_ref      = tGraphIntegral(getDataMetShape(refDir, btb, htbin), metb[0], metb[1])
#      true_plus     = tGraphIntegral(getDataMetShape(plusDir, btb, htbin), metb[0], metb[1]) 
#      true_minus    = tGraphIntegral(getDataMetShape(minusDir, btb, htbin), metb[0], metb[1])
#
#      res_sum_ref += res_ref
#      res_sum_plus += res_plus
#      res_sum_minus += res_minus
#      true_sum_ref += true_ref['res']
#      true_sum_plus += true_plus['res']
#      true_sum_minus += true_minus['res']
#
#  assert htbinslow==htb[0] and htbinshigh==htb[1]
#
## temporary patch for WPol systs without matching ref
#  if patchRef:
#    res_sum_ref = (res_sum_plus+res_sum_minus)/2.
#    true_sum_ref = (true_sum_plus+true_sum_minus)/2.
#  
#  relSysDPredPlus = (res_sum_plus-res_sum_ref)/res_sum_ref
#  relSysDPredMinus = (res_sum_minus-res_sum_ref)/res_sum_ref
#  relSysDTruePlus = (true_sum_plus-true_sum_ref)/true_sum_ref
#  relSysDTrueMinus = (res_sum_minus-res_sum_ref)/res_sum_ref
#  relSysDRPlus   = res_sum_plus/true_sum_plus / (res_sum_ref / true_sum_ref)
#  relSysDRMinus =  res_sum_minus/true_sum_minus / (res_sum_ref / true_sum_ref)
#  relAbsSysDR = max(abs(1.-relSysDRPlus),abs(1.-relSysDRMinus))
#  relSysSRPlus   = res_sum_plus/res_sum_ref-1
#  relSysSRMinus   = res_sum_minus/res_sum_ref-1
#  relAbsSysSR = max(abs(relSysSRPlus),abs(relSysSRMinus))
##  relAbsSysSR = abs((res_sum_plus - res_sum_minus)/(res_sum_minus + res_sum_plus))
##  print plusDir
#  print "res_sum: +/-",res_sum_plus, res_sum_minus,res_sum_ref, "true+/-", true_sum_plus, true_sum_minus, true_sum_ref
##        relSysDRPlus, relSysDRMinus, relAbsSysDR 
#  #make sure the shapes are normalized correctly. #shapes are normalized wrt. to the control region of the central value because the normalization effect cancels out in the sys. uncert. of integrated yields
#  referenceShape.Scale(normYield/referenceNormregyield)  
##  plotReferenceShape.Scale(normYield/plotReferenceNormregyield)  
#  plusShape  .Scale(normYield/plusNormregyield)  
#  minusShape .Scale(normYield/minusNormregyield)  
#  
#  ErrorShape = plotRefHisto.Clone()
#  for i in range(ErrorShape.GetNbinsX()+1):
#    if referenceShape.GetBinContent(i)>0:
#      ErrorShape.SetBinError(i, (plotRefHisto.GetBinContent(i)/referenceShape.GetBinContent(i))*max(abs(plusShape.GetBinContent(i) - referenceShape.GetBinContent(i)), abs(minusShape.GetBinContent(i) - referenceShape.GetBinContent(i))))
##    print ErrorShape.GetBinError(i)
#  return {\
#          "predictedYield_Reference":res_sum_ref, "predictedYield_Plus":res_sum_plus, "predictedYield_Minus":res_sum_minus, 
#          "trueYield_Reference":true_sum_ref, "trueYield_Plus":true_sum_plus, "trueYield_Minus":true_sum_minus, 
#          "refShape":referenceShape, "plusShape":plusShape, "minusShape":minusShape,
#          "refShapeWithError":ErrorShape,
#          "relSysDRPlus" : relSysDRPlus, "relSysDRMinus" : relSysDRMinus,
#          "relSysSRPlus" : relSysSRPlus, "relSysSRMinus" : relSysSRMinus,
#          "relAbsSysDR" : relAbsSysDR, "relAbsSysSR":relAbsSysSR,
#          "relSysDPredPlus" : relSysDPredPlus, "relSysDPredMinus" : relSysDPredMinus, 
#          "relSysDTruePlus" : relSysDTruePlus, "relSysDTrueMinus" : relSysDTrueMinus
##          ,"tmp":getDataMetShapeFromSamplingDirectory(plusDir, btb, htb)
#         }
#
#goodDirectories = {\
##"MC_central"    : "/data/schoef/RA4Fit2012/output/Results_copyMET_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121212_1204/",
##"data_central"  : "/data/schoef/RA4Fit2012/output/Results_copyMET_separateBTagWeights_fitData_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121211_1113/",
#"MC_central" : "/data/kwolf/RA4Fit2012/output/Results_copyMET_convertedTuples_v14_new_with_weight_weight_fitMC_MuonElectron_jet3pt40_150.0-met-600.0_400.0-ht-750.0_intLumi-20p0_130115_1544/",
#"data_central" : "/data/kwolf/RA4Fit2012/output/Results_copyMET_separateBTagWeights_convertedTuples_v14_new_with_weight_weight_fitData_MuonElectron_jet3pt40_150.0-met-600.0_400.0-ht-750.0_intLumi-12p0_130115_1559/",
#"JESRef"  : "/data/schoef/RA4Fit2012/output/Results_copyMET_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121206_0916/",
#"JESPlus" : "/data/schoef/RA4Fit2012/output/Results_copyMET_JES+_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121206_1531/",
#"JESMinus": "/data/schoef/RA4Fit2012/output/Results_copyMET_JES-_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121206_1531/",
#"BTag_SF_b_Up":       "/data/schoef/RA4Fit2012/output/Results_copyMET_separateBTagWeights_BTag_SF_b_Up_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121206_2148/",
#"BTag_SF_b_Down":     "/data/schoef/RA4Fit2012/output/Results_copyMET_separateBTagWeights_BTag_SF_b_Down_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121206_1557",
#"BTag_SF_light_Up":   "/data/schoef/RA4Fit2012/output/Results_copyMET_separateBTagWeights_BTag_SF_light_Up_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121206_1557/",
#"BTag_SF_light_Down": "/data/schoef/RA4Fit2012/output/Results_copyMET_separateBTagWeights_BTag_SF_light_Down_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121211_1016/", #FIXME: sampling aborted after HT400
#"BTag_SF":            "/data/schoef/RA4Fit2012/output/Results_copyMET_separateBTagWeights_BTag_SF_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121206_1556/",
#
#"DiLepRef"  : "/data/schoef/RA4Fit2012/output/Results_copyMET_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121212_1204/",
#"DiLepMinus":"/data/schoef/RA4Fit2012/output/Results_copyMET_weightDiLepMinus15_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121212_1514",
#"DiLepPlus" :"/data/schoef/RA4Fit2012/output/Results_copyMET_weightDiLepPlus15_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121212_1514",
#
#"PURef"    : "/data/schoef/RA4Fit2012/output/Results_copyMET_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121212_1204/",
#"PUMinus"  :"/data/schoef/RA4Fit2012/output/Results_copyMET_weightPUSysMinus_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121212_1516",
#"PUPlus"   :"/data/schoef/RA4Fit2012/output/Results_copyMET_weightPUSysPlus_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121212_1515",
#
#"TTPolRef"  : "/data/schoef/RA4Fit2012/output/Results_copyMET_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121212_1204/",
#"TTPolMinus":"/data/schoef/RA4Fit2012/output/Results_copyMET_weightTTPolMinus5_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121212_1512",
#"TTPolPlus" :"/data/schoef/RA4Fit2012/output/Results_copyMET_weightTTPolPlus5_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121212_1513",
#
#"TTXSecRef": "/data/schoef/RA4Fit2012/output/Results_copyMET_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121212_1204/",
#"TTXSecMinus":"/data/schoef/RA4Fit2012/output/Results_copyMET_weightTTxsecMinus30_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121211_1025",
#"TTXSecPlus": "/data/schoef/RA4Fit2012/output/Results_copyMET_weightTTxsecPlus30_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121211_1023",
#
#"WPol1Ref"  : "/data/schoef/RA4Fit2012/output/Results_copyMET_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121212_1204/",
#"WPol1Minus": "/data/schoef/RA4Fit2012/output/Results_copyMET_weightWPol1Minus10_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121119_1158",
#"WPol1Plus": "/data/schoef/RA4Fit2012/output/Results_copyMET_weightWPol1Minus10_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121119_1158",
#
#"WPol2MinusRef"  : "/data/schoef/RA4Fit2012/output/Results_copyMET_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121212_1204/",
#"WPol2MinusMinus": "/data/schoef/RA4Fit2012/output/Results_copyMET_weightWPol2MinusMinus5_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121119_2014",
#"WPol2MinusPlus": "/data/schoef/RA4Fit2012/output/Results_copyMET_weightWPol2MinusPlus5_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121119_2013",
#
#"WPol2PlusRef"  : "/data/schoef/RA4Fit2012/output/Results_copyMET_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121212_1204/",
#"WPol2PlusMinus": "/data/schoef/RA4Fit2012/output/Results_copyMET_weightWPol2PlusMinus5_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121119_2016",
#"WPol2PlusPlus": "/data/schoef/RA4Fit2012/output/Results_copyMET_weightWPol2PlusPlus5_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121119_2009",
#
#"WPol3Ref"  : "/data/schoef/RA4Fit2012/output/Results_copyMET_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121212_1204/",
#"WPol3Minus": "/data/schoef/RA4Fit2012/output/Results_copyMET_weightWPol3Minus10_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121119_2020",
#"WPol3Plus": "/data/schoef/RA4Fit2012/output/Results_copyMET_weightWPol3Plus10_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121119_2021",
#
#}
#
#def allUncertaintiesFromSamplingDirectory ( htb = [400,2500], metb = [250, 2500], btb = 2 ):
#  result = { }
#  res = getPredictionFromSamplingDirectory(goodDirectories['MC_central'], btb = btb, htb = htb, metb = metb, metvar = "met")
#  result['stat'] = res
#  result['JES'] = getUncertaintyFromSamplingDirectory(goodDirectories["JESRef"], goodDirectories["JESPlus"], goodDirectories["JESMinus"], \
#                                 res['predictedShape'], btb = btb, htb = htb, metb = metb, metvar = "met")
#  result['btag_SF_b'] = getUncertaintyFromSamplingDirectory(goodDirectories["BTag_SF"], goodDirectories["BTag_SF_b_Up"], goodDirectories["BTag_SF_b_Down"], \
#                                       res["predictedShape"], btb = btb, htb = htb, metb = metb, metvar = "met")
#  result['btag_SF_light'] = getUncertaintyFromSamplingDirectory(goodDirectories["BTag_SF"], goodDirectories["BTag_SF_light_Up"], goodDirectories["BTag_SF_light_Down"], \
#                                           res["predictedShape"], btb = btb, htb = htb, metb = metb, metvar = "met")
#  result['DiLep'] = getUncertaintyFromSamplingDirectory(goodDirectories["DiLepRef"], goodDirectories["DiLepPlus"], goodDirectories["DiLepMinus"], \
#                                   res["predictedShape"], btb = btb, htb = htb, metb = metb, metvar = "met")
#  result['PU'] = getUncertaintyFromSamplingDirectory(goodDirectories["PURef"], goodDirectories["PUPlus"], goodDirectories["PUMinus"], \
#                                res["predictedShape"], btb = btb, htb = htb, metb = metb, metvar = "met")
#  result['TTPol'] = getUncertaintyFromSamplingDirectory(goodDirectories["TTPolRef"], goodDirectories["TTPolPlus"], goodDirectories["TTPolMinus"], \
#                                   res["predictedShape"], btb = btb, htb = htb, metb = metb, metvar = "met")
#  result['TTXSec'] = getUncertaintyFromSamplingDirectory(goodDirectories["TTXSecRef"], goodDirectories["TTXSecPlus"], goodDirectories["TTXSecMinus"], \
#                                    res["predictedShape"], btb = btb, htb = htb, metb = metb, metvar = "met")
#
#  return result
#
#def allUncertainties ( htb = [400,2500], metb = [250, 2500], btb = 2 ):
#  result = { }
#  res = getPredictionFromSamplingDirectory(goodDirectories['MC_central'], btb = btb, htb = htb, metb = metb, metvar = "met")
#  result['stat'] = res
#  result['JES'] = getUncertainty(goodDirectories["JESRef"], goodDirectories["JESPlus"], goodDirectories["JESMinus"], \
#                                 res['predictedShape'], btb = btb, htb = htb, metb = metb, metvar = "met", patchRef = True )
#  result['btag_SF_b'] = getUncertainty(goodDirectories["BTag_SF"], goodDirectories["BTag_SF_b_Up"], goodDirectories["BTag_SF_b_Down"], \
#                                       res["predictedShape"], btb = btb, htb = htb, metb = metb, metvar = "met", patchRef = True )
#  result['btag_SF_light'] = getUncertainty(goodDirectories["BTag_SF"], goodDirectories["BTag_SF_light_Up"], goodDirectories["BTag_SF_light_Down"], \
#                                           res["predictedShape"], btb = btb, htb = htb, metb = metb, metvar = "met", patchRef = True )
#  result['DiLep'] = getUncertainty(goodDirectories["DiLepRef"], goodDirectories["DiLepPlus"], goodDirectories["DiLepMinus"], \
#                                   res["predictedShape"], btb = btb, htb = htb, metb = metb, metvar = "met", patchRef = True )
#  result['PU'] = getUncertainty(goodDirectories["PURef"], goodDirectories["PUPlus"], goodDirectories["PUMinus"], \
#                                res["predictedShape"], btb = btb, htb = htb, metb = metb, metvar = "met", patchRef = True )
#  result['TTPol'] = getUncertainty(goodDirectories["TTPolRef"], goodDirectories["TTPolPlus"], goodDirectories["TTPolMinus"], \
#                                   res["predictedShape"], btb = btb, htb = htb, metb = metb, metvar = "met", patchRef = True )
#  result['TTXSec'] = getUncertainty(goodDirectories["TTXSecRef"], goodDirectories["TTXSecPlus"], goodDirectories["TTXSecMinus"], \
#                                    res["predictedShape"], btb = btb, htb = htb, metb = metb, metvar = "met", patchRef = True )
#  result['WPol1'] = getUncertainty(goodDirectories["WPol1Ref"], goodDirectories["WPol1Plus"], goodDirectories["WPol1Minus"], \
#                                   res["predictedShape"], btb = btb, htb = htb, metb = metb, metvar = "met", patchRef = True )
#  result['WPol2Minus'] = getUncertainty(goodDirectories["WPol2MinusRef"], goodDirectories["WPol2MinusPlus"], goodDirectories["WPol2MinusMinus"], \
#                                        res["predictedShape"], btb = btb, htb = htb, metb = metb, metvar = "met", patchRef = True )
#  result['WPol2Plus'] = getUncertainty(goodDirectories["WPol2PlusRef"], goodDirectories["WPol2PlusPlus"], goodDirectories["WPol2PlusMinus"], \
#                                       res["predictedShape"], btb = btb, htb = htb, metb = metb, metvar = "met", patchRef = True )
#  result['WPol3'] = getUncertainty(goodDirectories["WPol3Ref"], goodDirectories["WPol3Plus"], goodDirectories["WPol3Minus"], \
#                                   res["predictedShape"], btb = btb, htb = htb, metb = metb, metvar = "met", patchRef = True )
#
#  return result
#
#def printUncertainties ( htb = [400,2500], metb = [250, 2500], btb = 2 ):
#  allressampling = allUncertaintiesFromSamplingDirectory(htb, metb, btb)
#  allres = allUncertainties(htb, metb, btb)
##  res               = getPredictionFromSamplingDirectory(goodDirectories['MC_central'], btb = btb, htb = htb, metb = metb, metvar = "met")
##  resJes            = getUncertainty(goodDirectories["JESRef"], goodDirectories["JESPlus"], goodDirectories["JESMinus"], res['predictedShape'], btb = btb, htb = htb, metb = metb, metvar = "met")
##  btag_SF_b_res     = getUncertainty(goodDirectories["BTag_SF"], goodDirectories["BTag_SF_b_Up"]     , goodDirectories["BTag_SF_b_Down"]    , res["predictedShape"] , btb = btb, htb = htb, metb = metb, metvar = "met")
##  btag_SF_light_res = getUncertainty(goodDirectories["BTag_SF"], goodDirectories["BTag_SF_light_Up"] , goodDirectories["BTag_SF_light_Down"], res["predictedShape"] , btb = btb, htb = htb, metb = metb, metvar = "met")
##  DiLep_res         = getUncertainty(goodDirectories["DiLepRef"], goodDirectories["DiLepPlus"] , goodDirectories["DiLepMinus"], res["predictedShape"] , btb = btb, htb = htb, metb = metb, metvar = "met")
##  PU_res            = getUncertainty(goodDirectories["PURef"], goodDirectories["PUPlus"] , goodDirectories["PUMinus"], res["predictedShape"] , btb = btb, htb = htb, metb = metb, metvar = "met")
##  TTPol_res         = getUncertainty(goodDirectories["TTPolRef"], goodDirectories["TTPolPlus"] , goodDirectories["TTPolMinus"], res["predictedShape"] , btb = btb, htb = htb, metb = metb, metvar = "met")
##  TTXSec_res        = getUncertainty(goodDirectories["TTXSecRef"], goodDirectories["TTXSecPlus"] , goodDirectories["TTXSecMinus"], res["predictedShape"] , btb = btb, htb = htb, metb = metb, metvar = "met")
##  WPol1_res         = getUncertainty(goodDirectories["WPol1Ref"], goodDirectories["WPol1Plus"] , goodDirectories["WPol1Minus"], res["predictedShape"] , btb = btb, htb = htb, metb = metb, metvar = "met")
##  WPol2Minus_res         = getUncertainty(goodDirectories["WPol2MinusRef"], goodDirectories["WPol2MinusPlus"] , goodDirectories["WPol2MinusMinus"], res["predictedShape"] , btb = btb, htb = htb, metb = metb, metvar = "met")
##  WPol2Plus_res         = getUncertainty(goodDirectories["WPol2PlusRef"], goodDirectories["WPol2PlusPlus"] , goodDirectories["WPol2PlusMinus"], res["predictedShape"] , btb = btb, htb = htb, metb = metb, metvar = "met")
##  WPol3_res         = getUncertainty(goodDirectories["WPol3Ref"], goodDirectories["WPol3Plus"] , goodDirectories["WPol3Minus"], res["predictedShape"] , btb = btb, htb = htb, metb = metb, metvar = "met")
##  print "BTagSFb"
##  BTagSFb_res =  getUncertainty(goodDirectories["BTag_SF"], goodDirectories["BTag_SF_b_Up"] , goodDirectories["BTag_SF_b_Down"], res["predictedShape"] , btb = btb, htb = htb, metb = metb, metvar = "met")
##  print "BTagSFlight"
##  BTagSFlight_res =  getUncertainty(goodDirectories["BTag_SF"], goodDirectories["BTag_SF_light_Up"] , goodDirectories["BTag_SF_light_Down"], res["predictedShape"] , btb = btb, htb = htb, metb = metb, metvar = "met")
#
#  print "btb/htb/metb", btb, htb, metb
#  print "pred", allres["stat"]['predictedYield'], "obs.", allres["stat"]['dataYield']['res'] , ' +- ', allres["stat"]['dataYield']['sigma']
#
#  print "Model+stat.", abs(allres["stat"]['predictedYield_Uncertainty_CombinedSumW2_Down'] - allres["stat"]['predictedYield_Uncertainty_CombinedSumW2_Up'])/(allres["stat"]['predictedYield_Uncertainty_CombinedSumW2_Down'] + allres["stat"]['predictedYield_Uncertainty_CombinedSumW2_Up'])
#  print "Model+stat.", abs(allres["stat"]['predictedYield_Uncertainty_CombinedPoissonian_Down'] - allres["stat"]['predictedYield_Uncertainty_CombinedPoissonian_Up'])/(allres["stat"]['predictedYield_Uncertainty_CombinedPoissonian_Down'] + allres["stat"]['predictedYield_Uncertainty_CombinedPoissonian_Up'])
#  print "JES" , "DR",allressampling["JES"]['relAbsSysDR']             ,"SR",  allressampling["JES"]['relAbsSysSR']
#  print "JES" , "DR",allres["JES"]['relAbsSysDR']             ,"SR",  allres["JES"]['relAbsSysSR']
#  print "SFb" , "DR",allressampling["btag_SF_b"]['relAbsSysDR']      ,"SR",  allressampling["btag_SF_b"]['relAbsSysSR']
#  print "SFb" , "DR",allres["btag_SF_b"]['relAbsSysDR']      ,"SR",  allres["btag_SF_b"]['relAbsSysSR']
#  print "SFl" , "DR",allressampling["btag_SF_light"]['relAbsSysDR']  ,"SR",  allressampling["btag_SF_light"]['relAbsSysSR']
#  print "SFl" , "DR",allres["btag_SF_light"]['relAbsSysDR']  ,"SR",  allres["btag_SF_light"]['relAbsSysSR']
#  print "TTPol","DR",allressampling["TTPol"]['relAbsSysDR']          ,"SR",  allressampling["TTPol"]['relAbsSysSR']
#  print "TTPol","DR",allres["TTPol"]['relAbsSysDR']          ,"SR",  allres["TTPol"]['relAbsSysSR']
#  print "TTXSec","DR",allressampling["TTXSec"]['relAbsSysDR']          ,"SR",  allressampling["TTXSec"]['relAbsSysSR']
#  print "TTXSec","DR",allres["TTXSec"]['relAbsSysDR']          ,"SR",  allres["TTXSec"]['relAbsSysSR']
##  print "WPol1","DR",allres["WPol1"]['relAbsSysDR']          ,"SR",  allres["WPol1"]['relAbsSysSR']
##  print "WPol2Minus","DR",allres["WPol2Minus"]['relAbsSysDR']          ,"SR",  allres["WPol2Minus"]['relAbsSysSR']
##  print "WPol2Plus","DR",allres["WPol2Plus"]['relAbsSysDR']          ,"SR",  allres["WPol2Plus"]['relAbsSysSR']
##  print "WPol3","DR",allres["WPol3"]['relAbsSysDR']          ,"SR",  allres["WPol3"]['relAbsSysSR']
#  print "PU",   "DR",allressampling["PU"]['relAbsSysDR']             ,"SR",  allressampling["PU"]['relAbsSysSR']
#  print "PU",   "DR",allres["PU"]['relAbsSysDR']             ,"SR",  allres["PU"]['relAbsSysSR']
#  print "DiLep","DR",allressampling["DiLep"]['relAbsSysDR']          ,"SR",  allressampling["DiLep"]['relAbsSysSR']
#  print "DiLep","DR",allres["DiLep"]['relAbsSysDR']          ,"SR",  allres["DiLep"]['relAbsSysSR']
#
#
#  print "btag_SF_b","DR",allres["btag_SF_b"]['relAbsSysDR']          ,"SR",  allres["btag_SF_b"]['relAbsSysSR'], \
#        "relUp", allres["btag_SF_b"]['relSysDRPlus']-1, "relDown", allres["btag_SF_b"]['relSysDRMinus']-1
#  print "   relUpTrue", allres["btag_SF_b"]['relSysDTruePlus'], "relDownTrue", allres["btag_SF_b"]['relSysDTrueMinus']
#  print "btag_SF_light","DR",allres["btag_SF_light"]['relAbsSysDR']          ,"SR",  allres["btag_SF_light"]['relAbsSysSR'], \
#        "relUp", allres["btag_SF_light"]['relSysDRPlus']-1, "relDown", allres["btag_SF_light"]['relSysDRMinus']-1
#  print "   relUpTrue", allres["btag_SF_light"]['relSysDTruePlus'], "relDownTrue", allres["btag_SF_light"]['relSysDTrueMinus']
#
#  datares               = getPredictionFromSamplingDirectory(goodDirectories['data_central'], btb = btb, htb = htb, metb = metb, metvar = "met")
#  print "pred", datares['predictedYield'], "obs.", datares['dataYield']['res'], ' +- ', datares['dataYield']['sigma']
#
##printUncertainties()
#
#stuff=[]  
#def makeNicePlot(goodDirectories, btb, htb, metb, metvar = "met", option = "MC", blowUpStatErr = 1):
#  l = ROOT.TLegend(0.52,0.55,.95,.95)
#  l.SetFillColor(0)
#  l.SetShadowColor(ROOT.kWhite)
#  l.SetBorderSize(1)
#
#  if option.lower()=="mc":
#    centralKey = "MC_central"
#    option="MC"
#  else:
#    centralKey = "data_central"
#    option = "Data"
#
#  uncertaintyShapes = []
#    
#  res = getPredictionFromSamplingDirectory(goodDirectories[centralKey], btb, htb, metb, metvar = "met", blowUpStatErr = 1)
#  jesRes            = getUncertaintyFromSamplingDirectory(goodDirectories["JESRef"],  goodDirectories["JESPlus"]          , goodDirectories["JESMinus"]          , res["predictedShape"] , btb = btb, htb = htb, metb = metb, metvar = "met")
#  uncertaintyShapes.append(jesRes['refShapeWithError'])
#  btag_SF_b_res     = getUncertaintyFromSamplingDirectory(goodDirectories["BTag_SF"], goodDirectories["BTag_SF_b_Up"]     , goodDirectories["BTag_SF_b_Down"]    , res["predictedShape"] , btb = btb, htb = htb, metb = metb, metvar = "met")
#  uncertaintyShapes.append(btag_SF_b_res['refShapeWithError'])
#  btag_SF_light_res = getUncertaintyFromSamplingDirectory(goodDirectories["BTag_SF"], goodDirectories["BTag_SF_light_Up"] , goodDirectories["BTag_SF_light_Down"], res["predictedShape"] , btb = btb, htb = htb, metb = metb, metvar = "met")
#  uncertaintyShapes.append(btag_SF_light_res['refShapeWithError'])
#
#  c1 = ROOT.TCanvas()
#  c1.SetLogy()
#  h = res["predictedShape"]
#  res["predictedShape"].GetYaxis().SetTitle("Events / 25 GeV")
#  res["predictedShape"].GetYaxis().SetRangeUser(10**-.5, 10**.7*h[h.GetMaximumBin()])
#  res["predictedShape"].GetXaxis().SetRangeUser(150, 1500)
#  res["predictedShape"].Draw()
#  l.AddEntry(res["predictedShape"], "prediction")
##  res["predictedShape_Uncertainty_Model_Up"]                .Draw("Lsame")
##  res["predictedShape_Uncertainty_Model_Down"]              .Draw("Lsame")
#  res["predictedShape_Uncertainty_CombinedPoissonian_Up"]   .SetLineColor(ROOT.kGreen)
#  res["predictedShape_Uncertainty_CombinedPoissonian_Down"] .SetLineColor(ROOT.kGreen)
#  res["predictedShape_Uncertainty_CombinedPoissonian_Up"]   .Draw("Lsame")
#  res["predictedShape_Uncertainty_CombinedPoissonian_Down"] .Draw("Lsame")
#  #res["predictedShape_Uncertainty_CombinedSumW2_Up"]   .SetLineColor(ROOT.kMagenta)
#  #res["predictedShape_Uncertainty_CombinedSumW2_Down"] .SetLineColor(ROOT.kMagenta)
#  #res["predictedShape_Uncertainty_CombinedSumW2_Up"]   .Draw("same")
#  #res["predictedShape_Uncertainty_CombinedSumW2_Down"] .Draw("same")
#  res["predictedShape"].Draw("same")
#
#  h = jesRes['refShapeWithError']
#  h.GetYaxis().SetTitle("Events / 25 GeV")
#  h.GetYaxis().SetRangeUser(10**-2.5, 10**.7*h[h.GetMaximumBin()])
#  h.GetXaxis().SetRangeUser(150, 1500)
#  h.SetLineColor(ROOT.kBlack)
#  #jesRes['minusShape'].SetLineColor(ROOT.kRed)
#  #jesRes['plusShape'].SetLineColor(ROOT.kBlue)
##  jesRes['refShape'].Draw()
#  #jesRes['minusShape'].Draw("same")           
#  #jesRes['plusShape'].Draw("same")
#
#  jesRes['refShapeWithError'].SetFillColor(ROOT.kBlue)
#  jesRes['refShapeWithError'].SetFillStyle(3001)
#  jesRes['refShapeWithError'].Draw("sameE3")
#  l.AddEntry(jesRes['refShapeWithError'], "JES Uncertainty")
#
#  btag_SF_b_res['refShapeWithError'].SetFillColor(ROOT.kRed)
#  btag_SF_b_res['refShapeWithError'].SetFillStyle(3001)
#  btag_SF_b_res['refShapeWithError'].Draw("sameE3")
#  l.AddEntry(btag_SF_b_res['refShapeWithError'], "b-tag SF Uncertainty")
#
#  btag_SF_light_res['refShapeWithError'].SetFillColor(ROOT.kGreen)
#  btag_SF_light_res['refShapeWithError'].SetFillStyle(3001)
#  btag_SF_light_res['refShapeWithError'].Draw("sameE3")
#  l.AddEntry(btag_SF_light_res['refShapeWithError'], "mis-b-tag SF Uncertainty")
#  for i in range(res["dataShape"].GetN()+1):
#    if res["dataShape"].GetY()[i]<10**(-10):
#      res["dataShape"].SetPoint(i, res["dataShape"].GetX()[i], 10**(-10))
#  res["dataShape"].Draw("psame")
#  tmpDataHist = ROOT.TH1F("tmp", "tmp", (150-1500)/25, 150, 1500)
#  for i in range(res["dataShape"].GetN()):
#    bin = tmpDataHist.FindBin(res["dataShape"].GetX()[i])
#    y = res["dataShape"].GetY()[i] 
#    err = .5*(res["dataShape"].GetEYlow()[i] + res["dataShape"].GetEYhigh()[i] )
#    tmpDataHist.SetBinContent(bin, y)
#    tmpDataHist.SetBinError  (bin, err)
#  if option.lower()=="mc":
#    l.AddEntry(tmpDataHist, "MC truth")
#  else:
#    l.AddEntry(tmpDataHist, "Data")
#
#  totalErrorUp    = res["predictedShape"].Clone() 
#  totalErrorDown  = res["predictedShape"].Clone() 
#
#  for i in range(totalErrorUp.GetNbinsX()+1):
#    central = res["predictedShape"].GetBinContent(i)
#    sigmaModelPoissonianUp    = res["predictedShape_Uncertainty_CombinedPoissonian_Up"].GetBinContent(i) - central
#    sigmaModelPoissonianDown  = res["predictedShape_Uncertainty_CombinedPoissonian_Down"].GetBinContent(i) - central
#    var = 0
#    for uncertaintyShape in uncertaintyShapes:
#      var+= uncertaintyShape.GetBinError(i)**2
##    print central, sigmaModelPoissonianUp, sigmaModelPoissonianDown, sigmaJES
#    totalErrorUp    .SetBinContent(i, central + sqrt(sigmaModelPoissonianUp**2          + var))
#    totalErrorDown  .SetBinContent(i, max(0, central - sqrt(sigmaModelPoissonianDown**2 + var)))
#
#  totalErrorUp.Draw("lsame")
#  totalErrorDown.Draw("lsame")
#  l.AddEntry(totalErrorUp, "total uncertainty")
#  l.Draw()
##  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngModelResults2012/"+option+"_btb_"+str(btb)+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_metb_"+str(metb[0])+"_"+str(metb[0])+".png")
##  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngModelResults2012/"+option+"_btb_"+str(btb)+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_metb_"+str(metb[0])+"_"+str(metb[0])+".pdf")
##  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngModelResults2012/"+option+"_btb_"+str(btb)+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_metb_"+str(metb[0])+"_"+str(metb[0])+".root")
#  stuff.append([res, jesRes, btag_SF_b_res, btag_SF_light_res, totalErrorUp, totalErrorDown, l, tmpDataHist])
#  return c1
#
###Test: makeNicePlot
##for btb in [0,1,2]:
##  for htb in [[400,2500], [500,2500], [750, 2500]]:
##    for metb in [[150, 2500], [250, 2500], [350, 3500], [450, 2500]]:
##      c1 = makeNicePlot(goodDirectories, btb, htb, metb, option = "data")
##      c1 = makeNicePlot(goodDirectories, btb, htb, metb, option = "mc")
#
##for btb in [0,1,2]:
##  for htb in [[400,2500], [500,2500], [750, 2500]]:
##    for metb in [[150, 2500], [250, 2500], [350, 3500], [450, 2500]]:
#
##for btb in [2]:
##  for htb in [[400,2500], [750, 2500]]:
##    for metb in [[150, 2500], [250, 2500], [350, 3500]]:
##      for dataOrMC in ['MC', 'data']:
##        res              = getPredictionFromSamplingDirectory(goodDirectories[dataOrMC+"_central"],btb,htb,metb,metvar="met",blowUpStatErr=1)
##        jesRes           = getUncertaintyFromSamplingDirectory(goodDirectories["JESRef"],goodDirectories["JESPlus"],goodDirectories["JESMinus"],res["predictedShape"],btb=btb,htb=htb,metb=metb,metvar="met")
##        btag_SF_b_res    = getUncertaintyFromSamplingDirectory(goodDirectories["BTag_SF"],goodDirectories["BTag_SF_b_Up"],goodDirectories["BTag_SF_b_Down"],res["predictedShape"],btb=btb,htb=htb,metb=metb,metvar="met")
##        btag_SF_light_res= getUncertaintyFromSamplingDirectory(goodDirectories["BTag_SF"],goodDirectories["BTag_SF_light_Up"],goodDirectories["BTag_SF_light_Down"],res["predictedShape"],btb=btb,htb=htb,metb=metb,metvar="met")
##        print dataOrMC,"htb",htb,"metb",metb,res['dataYield']['res'], res["predictedYield"], jesRes["relAbsSysDR"], btag_SF_b_res["relAbsSysDR"], btag_SF_light_res["relAbsSysDR"]
#
##getPredictionFromSamplingDirectory(goodDirectories["data_central"],2,[400,2500],[500,2500],metvar="met",blowUpStatErr=1)
#
##samplingInputDir = "/data/kwolf/RA4Fit2012/output/Results_copyMET_JES-_fitGenMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121123_1133"
##def getPredictionFromSampling(inDir, btb, htb, metb, metvar = "met"):
##  ifile = inDir+"/err_sampling_"+str(htb[0])+"_ht_"+str(htb[1])+"/h_central_bt"+str(btb)+"_"+str(htb[0])+"_ht_"+str(htb[1])+"__"+metvar
##  print "Using",ifile
##  hname = 'h_central_bt'+str(btb)+"_"+str(htb[0])+"_ht_"+str(htb[1])+"__"+metvar
##  centralShape = getObjFromFile(ifile+".root", hname)
###  centralShapeNormRegYield  = centralShape.Integral(centralShape.FindBin(metNormReg[0]), centralShape.FindBin(metNormReg[1]))
###  centralShapeSigRegYield   = centralShape.Integral(centralShape.FindBin(metb[0]), centralShape.FindBin(metb[1]))
##  centralShapeNormRegYield  = histIntegral(centralShape, metNormReg[0], metNormReg[1])
##  centralShapeSigRegYield   = histIntegral(centralShape, metb[0], metb[1])
##  print ifile+"_varMedian.root", hname
##  medianShape  = getObjFromFile(ifile+"_varMedian.root", hname+"_varMedian")
###  medianShapeSigRegYield   = medianShape.Integral(medianShape.FindBin(metb[0]), medianShape.FindBin(metb[1]))
##  medianShapeSigRegYield   = histIntegral(medianShape, metb[0], metb[1])
##  varUpShape = getObjFromFile(ifile+"_varUp.root", hname+"_varUp")
###  varUpShapeSigRegYield   = varUpShape.Integral(varUpShape.FindBin(metb[0]), varUpShape.FindBin(metb[1]))
##  varUpShapeSigRegYield   = histIntegral(varUpShape, metb[0], metb[1])
##  varDownShape = getObjFromFile(ifile+"_varDown.root", hname+"_varDown")
###  varDownShapeSigRegYield   = varDownShape.Integral(varDownShape.FindBin(metb[0]), varDownShape.FindBin(metb[1]))
##  varDownShapeSigRegYield   = histIntegral(varDownShape, metb[0], metb[1])
##
##  hname = 'h_metnorm_yield_sumpdf_bt'+str(btb)+"_"+str(htb[0])+"_ht_"+str(htb[1])
##  ifile = inDir+"/err_sampling_"+str(htb[0])+"_ht_"+str(htb[1])+"/h_metnorm_yield_sumpdf_bt"+str(btb)+"_"+str(htb[0])+"_ht_"+str(htb[1])
##  normYield = getObjFromFile(ifile+".root", hname).GetBinContent(1)
##
##  res     = normYield*centralShapeSigRegYield/centralShapeNormRegYield
##  resUp   = normYield*(varUpShapeSigRegYield    - medianShapeSigRegYield  + centralShapeSigRegYield)/centralShapeNormRegYield
##  resDown = normYield*(varDownShapeSigRegYield  - medianShapeSigRegYield  + centralShapeSigRegYield)/centralShapeNormRegYield
##
##  ifile = inDir+"/err_sampling_"+str(htb[0])+"_ht_"+str(htb[1])+"/c_sum_model_bt"+str(btb)+"_"+str(htb[0])+"_ht_"+str(htb[1])+".root"
##  canv_name = "c_sum_model_bt"+str(btb)+"_"+str(htb[0])+"_ht_"+str(htb[1])
##  canv =   getObjFromFile(ifile, canv_name)
##  data_hist = canv.GetPrimitive("plot_data_bt"+str(btb)+"_ht_"+str(htb[0])+"_"+str(htb[1])).Clone()
##  dataYield =  tGraphIntegral(h, metb[0], metb[1])
##
##  resDict = {"predictedYield":res, "normRegYield":normYield, "predictedYield_Model_Up":resUp, "predictedYield_Model_Down":resDown, "dataYield":dataYield['res'], "dataYieldSigma":dataYield['sigma']}
##  return resDict
##
###binnedInputDir = "/data/schoef/RA4Fit2012/output/Results_copyMET_JES-_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121118_1510"
###binnedInputDir = "/data/schoef/RA4Fit2012/output/Results_copyMET_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121116_1732"
##binnedInputDir = "/data/schoef/RA4Fit2012/output/Results_copyMET_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121118_1658"
###binnedInputDir = "/data/schoef/RA4Fit2012/output/Results_copyMET_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121119_1253"
##
##def getPredictionFromBinnedHistos(inDir, btb, htb, metb, metvar = "met"):
##  metNormReg = [150, 250]
##  print "Using",inDir
##  relevantHTBins = []
##  allhtvals = []
##  for thtb in htbins:
##    if thtb[0]>=htb[0] and thtb[1]<=htb[1]:
##      relevantHTBins.append(thtb)
##      allhtvals+=thtb
##  newhtb = [min(allhtvals), max(allhtvals)]
##  if newhtb!=htb:
##    print "Warning! Can't make HT val.",htb,"will use",newhtb ,"instead"
##    htb=newhtb
##  print "Will sum HT bins:", relevantHTBins
##  ifile = inDir
##  res = 0.
##  for htval in relevantHTBins:
##    ifile = inDir+"/h_metnorm_yield_sumcharge_sumpdf_met_ht_"+str(htval[0])+"_"+str(htval[1])+"_bt"+str(btb)+".root"
##    hnorm = getObjFromFile(ifile,"h_metnorm_yield_sumcharge_sumpdf_met_ht_"+str(htval[0])+"_"+str(htval[1])+"_bt"+str(btb) )
##    normYield = hnorm.GetBinContent(1)
##
##    ifile = inDir+"/h_conv_sumcharge_sumpdf_"+metvar+"_ht_"+str(htval[0])+"_"+str(htval[1])+"_bt"+str(btb)+"__"+metvar+".root"
##
###    print "h_conv_sumcharge_sumpdf_"+metvar+"_ht_"+str(htval[0])+"_"+str(htval[1])+"_bt"+str(btb)+"__"+metvar
##    metshape = getObjFromFile(ifile,"h_conv_sumcharge_sumpdf_"+metvar+"_ht_"+str(htval[0])+"_"+str(htval[1])+"_bt"+str(btb)+"__"+metvar )
###    metshapeNormRegYield  = metshape.Integral(metshape.FindBin(metNormReg[0]), metshape.FindBin(metNormReg[1]))
###    metshapeSigRegYield   = metshape.Integral(metshape.FindBin(metb[0]), metshape.FindBin(metb[1]))
##    metshapeNormRegYield  = histIntegral(metshape, metNormReg[0], metNormReg[1])
##    metshapeSigRegYield   = histIntegral(metshape, metb[0], metb[1])
###    print normYield,"*",metshapeSigRegYield,"/",metshapeNormRegYield 
##    res += normYield*metshapeSigRegYield/metshapeNormRegYield
##  return res 
###  print "Using",ifile
###  hname = 'h_central_bt'+str(btb)+"_"+str(htb[0])+"_ht_"+str(htb[1])+"__"+metvar
###  centralShape = getObjFromFile(ifile+".root", hname)
###  centralShapeNormRegYield  = centralShape.Integral(centralShape.FindBin(metNormReg[0]), centralShape.FindBin(metNormReg[1]))
###  centralShapeSigRegYield   = centralShape.Integral(centralShape.FindBin(metb[0]), centralShape.FindBin(metb[1]))
###  print ifile+"_varMedian.root", hname
###  medianShape  = getObjFromFile(ifile+"_varMedian.root", hname+"_varMedian")
###  medianShapeSigRegYield   = medianShape.Integral(medianShape.FindBin(metb[0]), medianShape.FindBin(metb[1]))
###  varUpShape = getObjFromFile(ifile+"_varUp.root", hname+"_varUp")
###  varUpShapeSigRegYield   = varUpShape.Integral(varUpShape.FindBin(metb[0]), varUpShape.FindBin(metb[1]))
###  varDownShape = getObjFromFile(ifile+"_varDown.root", hname+"_varDown")
###  varDownShapeSigRegYield   = varDownShape.Integral(varDownShape.FindBin(metb[0]), varDownShape.FindBin(metb[1]))
###
###  hname = 'h_metnorm_yield_sumpdf_bt'+str(btb)+"_"+str(htb[0])+"_ht_"+str(htb[1])
###  ifile = inDir+"/err_sampling_"+str(htb[0])+"_ht_"+str(htb[1])+"/h_metnorm_yield_sumpdf_bt"+str(btb)+"_"+str(htb[0])+"_ht_"+str(htb[1])
###  normYield = getObjFromFile(ifile+".root", hname).GetBinContent(1)
###
###  res     = normYield*centralShapeSigRegYield/centralShapeNormRegYield
###  resUp   = normYield*(varUpShapeSigRegYield    - medianShapeSigRegYield  + centralShapeSigRegYield)/centralShapeNormRegYield
###  resDown = normYield*(varDownShapeSigRegYield  - medianShapeSigRegYield  + centralShapeSigRegYield)/centralShapeNormRegYield
###  
###
###  ifile = inDir+"/err_sampling_"+str(htb[0])+"_ht_"+str(htb[1])+"/c_sum_model_bt"+str(btb)+"_"+str(htb[0])+"_ht_"+str(htb[1])+".root"
###  canv_name = "c_sum_model_bt"+str(btb)+"_"+str(htb[0])+"_ht_"+str(htb[1])
###  canv =   getObjFromFile(ifile, canv_name)
###  data_hist = canv.GetPrimitive("plot_data_bt"+str(btb)+"_ht_"+str(htb[0])+"_"+str(htb[1])).Clone()
###  dataYield =  tGraphIntegral(h, metb[0], metb[1])
###
###  resDict = {"predictedYield":res, "normRegYield":normYield, "predictedYield_Model_Up":resUp, "predictedYield_Model_Down":resDown, "dataYield":dataYield['res'], "dataYieldSigma":dataYield['sigma']}
###  return resDict
