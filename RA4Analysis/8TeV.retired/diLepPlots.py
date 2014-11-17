import ROOT
from array import array
from math import *
import os, copy, sys

from Workspace.RA4Analysis.simplePlotsCommon import *
from funcs import *

import xsec
#xsec.xsec["WJets-HT300"] = 51.4
small = False

from defaultMu2012Samples import *

#def addSamples(s1, s2, newname):
#  res = copy.deepcopy(s1)
#  res["bins"] = s1["bins"] + s2["bins"]
#  res["name"] = newname
#  return res

mode = "OSDL"
signalRegion = "None"
lmodes =  ["doubleMu", "doubleEle", "eleMu"]
msq=175; mN=0

if len(sys.argv)>2:
  msq = int(sys.argv[1])
  mN = int(sys.argv[2])
  print "Using signal",msq, mN



allVars=[]
allStacks=[]

signalColors = [ROOT.kBlack, ROOT.kBlue + 1, ROOT.kGreen + 2, ROOT.kOrange + 2]

## plots for studying preselection 
topIsLargest = True
minimum=10**(-0.5)


presel = None 
#if mode=="JZB":
#  presel = "pf-3j40-mLL30-40"
#  presel = "pf-3j40-mLL80-100"
#  presel = "pf-3j40-mLL20-nbtags2"
#  presel = "pf-3j40-mLL20"
#  presel = "pf-3j40-mLL20-70"
#  presel = "pf-3j40-mLL70-110"
#  presel = "pf-3j40-mLL110"
if mode=="OSDL":
#highMET
#  presel = "pf-2j40-met150-mLL110"
#  presel = "pf-2j40-met150-mLL70-110"
#  presel = "pf-2j40-met150-mLL20-70"
#  presel = "pf-2j40-met150-mLL20"
#lowMET
#  presel = "pf-3j40-met100-mLL20"
#  presel = "pf-3j40-met100-mLL20-70"
#  presel = "pf-3j40-met100-mLL70-110"
#  presel = "pf-3j40-met100-mLL110"
  presel = "pf-3j40-met100-mLL20-Run2012ABC"
#  presel = "pf-3j40-met100-mLL20-70-Run2012ABC"
#  presel = "pf-3j40-met100-mLL70-110-Run2012ABC"
#  presel = "pf-3j40-met100-mLL110-Run2012ABC"
  if len(sys.argv)>3:
    presel = sys.argv[3]
    print "presel",presel
  if presel.count("pf-3j40-met100-mLL"):
    signalRegion = "lowMET"
  if presel.count("pf-2j40-met150-mLL"):
    signalRegion = "highMET"

preprefix     = mode
additionalCut = ""

#subdir = "/DiLep53X/"+signalRegion+"/"+mode+"/"
#subdir = "/DiLep53XSignal/"+signalRegion+"/"+mode+"/"
subdir = "/DiLep53XSignal_T6bbzz_v13/"+signalRegion+"/"

doOnlyMET = False
normalizeToData = False

commoncf = "(0)"
prefix="empty_"

if  presel == "pf-2j40-met150-mLL20-70-Run2012ABC-typeIMET":
  commoncf = "jet2pt>40&&type1met>100&&deltaRLL>0.3&&mLL>20&&mLL<70"
  targetLumi =  11000
if  presel == "pf-2j40-met150-mLL70-110-Run2012ABC-typeIMET":
  commoncf = "jet2pt>40&&type1met>100&&deltaRLL>0.3&&mLL>70&&mLL<110"
  targetLumi =  11000
if  presel == "pf-2j40-met150-mLL20-Run2012ABC-typeIMET":
  commoncf = "jet2pt>40&&type1met>100&&deltaRLL>0.3&&mLL>20"
  targetLumi =  11000
if  presel == "pf-2j40-met150-mLL110-Run2012ABC-typeIMET":
  commoncf = "jet2pt>40&&type1met>100&&deltaRLL>0.3&&mLL>110"
  targetLumi =  11000


if  presel == "pf-3j40-met100-mLL20-70-Run2012ABC-typeIMET":
  commoncf = "jet2pt>40&&type1met>100&&deltaRLL>0.3&&mLL>20&&mLL<70"
  targetLumi =  11000
if  presel == "pf-3j40-met100-mLL70-110-Run2012ABC-typeIMET":
  commoncf = "jet2pt>40&&type1met>100&&deltaRLL>0.3&&mLL>70&&mLL<110"
  targetLumi =  11000
if  presel == "pf-3j40-met100-mLL20-Run2012ABC-typeIMET":
  commoncf = "jet2pt>40&&type1met>100&&deltaRLL>0.3&&mLL>20"
  targetLumi =  11000
if  presel == "pf-3j40-met100-mLL110-Run2012ABC-typeIMET":
  commoncf = "jet2pt>40&&type1met>100&&deltaRLL>0.3&&mLL>110"
  targetLumi =  11000

if  presel == "pf-2j40-met150-mLL20-70-Run2012ABC":
  commoncf = "jet2pt>40&&met>100&&deltaRLL>0.3&&mLL>20&&mLL<70"
  targetLumi =  11000
if  presel == "pf-2j40-met150-mLL70-110-Run2012ABC":
  commoncf = "jet2pt>40&&met>100&&deltaRLL>0.3&&mLL>70&&mLL<110"
  targetLumi =  11000
if  presel == "pf-2j40-met150-mLL20-Run2012ABC":
  commoncf = "jet2pt>40&&met>100&&deltaRLL>0.3&&mLL>20"
  targetLumi =  11000
if  presel == "pf-2j40-met150-mLL110-Run2012ABC":
  commoncf = "jet2pt>40&&met>100&&deltaRLL>0.3&&mLL>110"
  targetLumi =  11000


if  presel == "pf-3j40-met100-mLL20-70-Run2012ABC":
  commoncf = "jet2pt>40&&met>100&&deltaRLL>0.3&&mLL>20&&mLL<70"
  targetLumi =  11000
if  presel == "pf-3j40-met100-mLL70-110-Run2012ABC":
  commoncf = "jet2pt>40&&met>100&&deltaRLL>0.3&&mLL>70&&mLL<110"
  targetLumi =  11000
if  presel == "pf-3j40-met100-mLL20-Run2012ABC":
  commoncf = "jet2pt>40&&met>100&&deltaRLL>0.3&&mLL>20"
  targetLumi =  11000
if  presel == "pf-3j40-met100-mLL110-Run2012ABC":
  commoncf = "jet2pt>40&&met>100&&deltaRLL>0.3&&mLL>110"
  targetLumi =  11000


if additionalCut!="":
  commoncf+="&&"+additionalCut

if preprefix!="":
  prefix = preprefix+"_"+presel+"_"


data={}
stop={}
dy={}
ttbar={}
wjets={}
lm6={}
T6bbzzv13Sig={}
allSamples = []
for lmode in lmodes:
  data[lmode] = {}
  data[lmode]["name"]     = "Data " + lmode;
  data[lmode]["dirname"] = "/data/schoef/convertedTuples_v11/"+mode+"_"+lmode+"/"+signalRegion+"/"
  data[lmode]["bins"]    = [ lmode+'Data']
  data[lmode]["Chain"] = "Events"
  data[lmode]["specialCuts"] = []
  data[lmode]["hasWeight"] = True
  allSamples.append(data[lmode])
#  stop[lmode]=copy.deepcopy(data[lmode])
#  stop[lmode]["name"]     = "single Top " + lmode;
#  stop[lmode]["dirname"] = "/data/schoef/convertedTuples_v9/"+mode+"_"+lmode+"/"+signalRegion+"/"
#  stop[lmode]["bins"]    = [ "singleTop" ]
#  allSamples.append(stop[lmode])
#
#  dy[lmode]=copy.deepcopy(stop[lmode])
#  dy[lmode]["name"]     = "Drell Yan " + lmode;
#  dy[lmode]["bins"]    = [ "DY-M20",  "DY-M50" ]
#  allSamples.append(dy[lmode])
#
#  ttbar[lmode]=copy.deepcopy(stop[lmode])
#  ttbar[lmode]["name"]     = "TTJets "+lmode;
#  ttbar[lmode]["bins"]    = [ "TTJets-S6" ]
#  allSamples.append(ttbar[lmode])
#
#  wjets[lmode]=copy.deepcopy(stop[lmode])
#  wjets[lmode]["name"]     = "WJets "+lmode;
#  wjets[lmode]["bins"]    = [ "WJets" ]
#  allSamples.append(wjets[lmode])
  T6bbzzv13Sig[lmode]=copy.deepcopy(data[lmode])
  sigName = "T6bbzzv13_"+str(msq)+"_"+str(mN)
  T6bbzzv13Sig[lmode]["name"]     = sigName+lmode;
  T6bbzzv13Sig[lmode]["bins"]    = [ sigName ]
  T6bbzzv13Sig[lmode]["hasWeight"]    = True
  allSamples.append(T6bbzzv13Sig[lmode])


def getStack(lmode, varstring, binning, cutstring, signals, topIsLargest = False, varfunc = ""):
  DATA          = variable(varstring, binning, cutstring)
  DATA.sample   = data[lmode]
#  DATA.color    = ROOT.kGray
  DATA.color    = dataColor
  DATA.legendText="Data ("+lmode+")"

  MC_STOP                       = variable(varstring, binning, cutstring)
  MC_STOP.minimum               = minimum
#  MC_STOP.sample                = stop[lmode]
#
#  MC_WJETS                     = copy.deepcopy(MC_STOP)
#  MC_WJETS.sample              = wjets[lmode]
#
#  MC_TTJETS                    = copy.deepcopy(MC_STOP)
#  MC_TTJETS.sample             = ttbar[lmode]
#
#  MC_DY                     = copy.deepcopy(MC_STOP)
#  MC_DY.sample              = dy[lmode]
#
#  MC_DY.legendText          = "DY + Jets" 
#  MC_DY.style               = "f0"
#  MC_DY.add                 = [MC_TTJETS]
#  MC_DY.color               = ROOT.kGreen + 3
#
#  MC_TTJETS.legendText         = "t#bar{t} + Jets"
#  MC_TTJETS.style              = "f0"
#  MC_TTJETS.color              = ROOT.kRed - 3
#  MC_TTJETS.add                = [MC_STOP]
#
#
  MC_STOP.legendText          = "single Top"
  MC_STOP.style               = "f0"
#  MC_STOP.add                 = [MC_WJETS]
#  MC_STOP.color               = ROOT.kOrange + 4
#
#  MC_WJETS.legendText          = "W + Jets"
#  MC_WJETS.style               = "f0"
#  MC_WJETS.add                 = []
#  MC_WJETS.color               = ROOT.kYellow
#
#  res = [MC_DY, MC_TTJETS, MC_STOP, MC_WJETS]
#  getLinesForStack(res, targetLumi)
#  nhistos = len(res)
  res = []
  for s in signals:
    MC_SIGNAL                    = copy.deepcopy(MC_STOP) 
    MC_SIGNAL.sample             = s[lmode] 
    MC_SIGNAL.legendText         = s[lmode]["bins"][0]
    MC_SIGNAL.style              = "l02"
    MC_SIGNAL.color              = ROOT.kBlue 
    MC_SIGNAL.add = []
    res.append(MC_SIGNAL)

  res.append(DATA)
  if varfunc!="":
    for var in res:
      var.varfunc = varfunc
  for var in res:
    var.legendCoordinates=[0.61,0.95 - 0.08*3,.98,.95]
  return res
#

ngoodVertices_stack = {}
met_stack = {}
jet0_pt_stack = {}
jet1_pt_stack = {}
jet2_pt_stack = {}
jet3_pt_stack = {}
kinMetSig_stack = {}
mLL_stack = {}
ptZ_stack = {}
jzb_stack = {}
ht_stack = {}
ngoodElectrons_stack = {}
nvetoElectrons_stack = {}
ngoodMuons_stack = {}
nvetoMuons_stack = {}
nbtags_stack = {}
btag0pt_stack = {}
btag1pt_stack = {}
njets_stack = {}
minLepMetIso_stack = {}
minJetsMetIso_stack = {}
minbJetsMetIso_stack = {}
minLepbJetIso_stack = {}
minLepJetIso_stack = {}
deltaPhibb_stack = {}
deltaEtabb_stack = {}
deltaRbb_stack = {}
deltaPhiLL_stack = {}
deltaEtaLL_stack = {}
deltaRLL_stack = {}
mbl_stack = {}
mbb_stack = {}
deltaHT_stack = {}
deltaHT2_stack = {}
mbl1MinDeltaHT_stack = {}
mbl2MinDeltaHT_stack = {}
mllbb_stack = {}

signals = [T6bbzzv13Sig]

for lmode in lmodes:
  ngoodVertices_stack[lmode]= getStack(lmode, ":ngoodVertices;Number of Vertices;Number of Events",[51,0,51], commoncf, signals, topIsLargest)
  ngoodVertices_stack[lmode][0].addOverFlowBin = "upper"
  allStacks.append(ngoodVertices_stack[lmode])

  met_stack[lmode]= getStack(lmode, ":met;#slash{E}_{T} (GeV);Number of Events / 30 GeV",[31,0,930], commoncf, signals, topIsLargest)
  met_stack[lmode][0].addOverFlowBin = "upper"
  allStacks.append(met_stack[lmode])

  if not doOnlyMET:

    jet0_pt_stack[lmode]= getStack(lmode, ":jet0pt;p_{T} of leading jet (GeV);Number of Events / 100 GeV",[11,40,1140], commoncf, signals, topIsLargest)
    jet0_pt_stack[lmode][0].addOverFlowBin = "upper"
    allStacks.append(jet0_pt_stack[lmode])
    jet1_pt_stack[lmode]= getStack(lmode, ":jet1pt;p_{T} of 2^{nd} leading jet (GeV);Number of Events / 100 GeV",[11,40,1140], commoncf, signals, topIsLargest)
    jet1_pt_stack[lmode][0].addOverFlowBin = "upper"
    allStacks.append(jet1_pt_stack[lmode])
    jet2_pt_stack[lmode]= getStack(lmode, ":jet2pt;p_{T} of 3^{rd} leading jet (GeV);Number of Events / 100 GeV",[11,40,1140], commoncf, signals, topIsLargest)
    jet2_pt_stack[lmode][0].addOverFlowBin = "upper"
    allStacks.append(jet2_pt_stack[lmode])
    jet3_pt_stack[lmode]= getStack(lmode, ":jet3pt;p_{T} of 4^{th} leading jet (GeV);Number of Events / 100 GeV",[11,40,1140], commoncf+"&&jet3pt>0", signals, topIsLargest)
    jet3_pt_stack[lmode][0].addOverFlowBin = "upper"
    allStacks.append(jet3_pt_stack[lmode])

    kinMetSig_stack[lmode]= getStack(lmode, ":kinMetSig;S_{MET};Number of Events",[25,0,25], commoncf, signals, topIsLargest, kinMetSig)
    kinMetSig_stack[lmode][0].addOverFlowBin = "upper"
    allStacks.append(kinMetSig_stack[lmode])

    mLLBinning = [26, 0, 260]
    mLL_stack[lmode]= getStack(lmode, ":mLL;m_{ll};Number of Events / "+str(int((mLLBinning[2] - mLLBinning[1])/mLLBinning[0]))+" GeV", mLLBinning, commoncf, signals, topIsLargest)
    mLL_stack[lmode][0].addOverFlowBin = "upper"
    allStacks.append(mLL_stack[lmode])

    jzb_stack[lmode]= getStack(lmode, ":jzb;JZB;Number of Events / 40 GeV",[30,-400,800], commoncf, signals, topIsLargest)
    jzb_stack[lmode][0].addOverFlowBin = "both"
    allStacks.append(jzb_stack[lmode])

    ptZ_stack[lmode]= getStack(lmode, ":ptZ;ptZ;Number of Events / 30 GeV",[11,0,330], commoncf, signals, topIsLargest)
    ptZ_stack[lmode][0].addOverFlowBin = "upper"
    allStacks.append(ptZ_stack[lmode])

    ht_stack[lmode]= getStack(lmode, ":ht;H_{T} (GeV);Number of Events / 50 GeV",[36,0-10,1750-10], commoncf, signals, topIsLargest)
    ht_stack[lmode][0].addOverFlowBin = "upper"
    allStacks.append(ht_stack[lmode])


    nbtags_stack[lmode]= getStack(lmode, ":nbtags;Number of b-tagged Jets;Number of Events",[10,0,10], commoncf, signals, topIsLargest)
    nbtags_stack[lmode][0].addOverFlowBin = "upper"
    allStacks.append(nbtags_stack[lmode])

    btag0pt_stack[lmode]= getStack(lmode, ":btag0pt;p_{T} of leading b-jet (GeV);Number of Events / 100 GeV",[11,40,1140], commoncf, signals, topIsLargest)
    btag0pt_stack[lmode][0].addOverFlowBin = "upper"
    allStacks.append(btag0pt_stack[lmode])

    btag1pt_stack[lmode]= getStack(lmode, ":btag1pt;p_{T} of 2^{nd.} leading b-jet (GeV);Number of Events / 100 GeV",[11,40,1140], commoncf, signals, topIsLargest)
    btag1pt_stack[lmode][0].addOverFlowBin = "upper"
    allStacks.append(btag1pt_stack[lmode])

    njets_stack[lmode]= getStack(lmode, ":njets;Number of Jets;Number of Events",[10,0,10], commoncf, signals, topIsLargest)
    njets_stack[lmode][0].addOverFlowBin = "upper"
    allStacks.append(njets_stack[lmode])

    minLepMetIso_stack[lmode]     =   getStack(lmode, ":minLepMetIso;min ||#phi(l, #slash{E}_{T})| - #pi|;Number of Events", [10,0,pi], commoncf, signals, topIsLargest)
    minLepMetIso_stack[lmode][0].addOverFlowBin = "both"
    allStacks.append(minLepMetIso_stack[lmode])

    minJetsMetIso_stack[lmode]    =   getStack(lmode, ":minJetsMetIso;min ||#phi(jets, #slash{E}_{T})| - #pi|;Number of Events", [10,0,pi], commoncf, signals, topIsLargest)
    minJetsMetIso_stack[lmode][0].addOverFlowBin = "both"
    allStacks.append(minJetsMetIso_stack[lmode])

    minbJetsMetIso_stack[lmode]   =   getStack(lmode, ":minbJetsMetIso;min #phi(b-jets, #slash{E}_{T});Number of Events", [10,0,pi], commoncf, signals, topIsLargest)
    minbJetsMetIso_stack[lmode][0].addOverFlowBin = "both"
    allStacks.append(minbJetsMetIso_stack[lmode])

    minLepbJetIso_stack[lmode]    =   getStack(lmode, ":minLepbJetIso;min #phi(l, b-jets);Number of Events", [10,0,pi], commoncf, signals, topIsLargest)
    allStacks.append(minLepbJetIso_stack[lmode])

    minLepJetIso_stack[lmode]     =   getStack(lmode, ":minLepJetIso;min #phi(l, jets);Number of Events", [10,0,pi], commoncf, signals, topIsLargest)
    allStacks.append(minLepJetIso_stack[lmode])

    deltaPhibb_stack[lmode]            =   getStack(lmode, ":deltaPhibb;#Delta#phi(bb);Number of Events", [10,0,pi], commoncf, signals, topIsLargest)
    allStacks.append(deltaPhibb_stack[lmode])
    deltaEtabb_stack[lmode]            =   getStack(lmode, ":deltaEtabb;#Delta#eta(bb);Number of Events", [20,-5,5], commoncf, signals, topIsLargest)
    allStacks.append(deltaEtabb_stack[lmode])
    deltaRbb_stack[lmode]            =   getStack(lmode, ":deltaRbb;#Delta R(bb);Number of Events", [20,0,5], commoncf, signals, topIsLargest)
    allStacks.append(deltaRbb_stack[lmode])
    deltaPhiLL_stack[lmode]            =   getStack(lmode, ":deltaPhiLL;#Delta#phi(LL);Number of Events", [10,0,pi], commoncf, signals, topIsLargest)
    allStacks.append(deltaPhiLL_stack[lmode])
    deltaEtaLL_stack[lmode]            =   getStack(lmode, ":deltaEtaLL;#Delta#eta(LL);Number of Events", [20,-5,5], commoncf, signals, topIsLargest)
    allStacks.append(deltaEtaLL_stack[lmode])
    deltaRLL_stack[lmode]            =   getStack(lmode, ":deltaRLL;#Delta R(LL);Number of Events", [20,0,5], commoncf, signals, topIsLargest)
    allStacks.append(deltaRLL_stack[lmode])

    mbl_stack[lmode]              =   getStack(lmode, ":mbl;m(b,l);Number of Events / 20 GeV", [31,0,620], commoncf, signals, topIsLargest)
    allStacks.append(mbl_stack[lmode])

    mbb_stack[lmode]              =   getStack(lmode, ":mbb;m(b,b);Number of Events / 50 GeV", [13,0,650], commoncf, signals, topIsLargest)
    allStacks.append(mbb_stack[lmode])

    deltaHT_stack[lmode]              =   getStack(lmode, ":minDeltaHT;min #Delta (l+b)_{T};Number of Events / 50 GeV", [13,0,650], commoncf, signals, topIsLargest)
    allStacks.append(deltaHT_stack[lmode])

    deltaHT2_stack[lmode]              =   getStack(lmode, ":minDeltaHT;min #Delta (l+b)_{T};Number of Events / 20 GeV", [13,0,260], commoncf, signals, topIsLargest)
    allStacks.append(deltaHT2_stack[lmode])

    mbl1MinDeltaHT_stack[lmode]              =   getStack(lmode, ":mbl1MinDeltaHT;m(leading-b,l);Number of Events / 50 GeV", [14,0,700], commoncf, signals, topIsLargest)
    allStacks.append(mbl1MinDeltaHT_stack[lmode])

    mbl2MinDeltaHT_stack[lmode]              =   getStack(lmode, ":mbl2MinDeltaHT;m(leading-b,l);Number of Events / 50 GeV", [14,0,700], commoncf, signals, topIsLargest)
    allStacks.append(mbl2MinDeltaHT_stack[lmode])

    mllbb_stack[lmode]              =   getStack(lmode, ":mllbb;m(llbb);Number of Events / 50 GeV", [31,0,1550], commoncf, signals, topIsLargest)
    allStacks.append(mllbb_stack[lmode])
  #  metiso_stack[lmode]= getStack(lmode, ":metiso;MET Iso from jets;Number of Events",[40,0,3.1415], commoncf, signals, topIsLargest)
  #  metiso_stack[lmode][0].addOverFlowBin = "upper"
  #  allStacks.append(metiso_stack[lmode])


for stack in allStacks:
  stack[0].minimum = minimum

#for stack in allStacks:
#  for var in stack:
#    var.addOverFlowBin = "both"

#reweightingHistoFile = "reweightingHisto_Summer2011.root"
#reweightingHistoFile = "Summer11_reweightingHisto-official.root"
#reweightingHistoFile = "reweightingHisto_Summer12.root"
#reweightingHistoFile = "reweightingHisto_Summer2012Private.root"
reweightingHistoFile = ""
execfile("simplePlotsLoopKernel.py")

if normalizeToData:
  for stack in allStacks:
    for var in stack[:-1]:
      var.normalizeTo = stack[-1]
      var.normalizeWhat = stack[0]
    stack[-1].normalizeTo=""
    stack[-1].normalizeWhat=""
else:
  for stack in allStacks:
    for var in stack:
      var.normalizeTo = ""
      var.normalizeWhat = "" 

def getOFSubtractedStack(stackDict, normalized = "eff", pos = -1):
  d1=copy.deepcopy(stackDict['doubleMu'][pos])
  d2=copy.deepcopy(stackDict['doubleEle'][pos])
  d3=copy.deepcopy(stackDict['eleMu'][pos])
  d1.addOverFlowBin = stackDict['doubleMu'][0].addOverFlowBin
  d3.addOverFlowBin = stackDict['doubleMu'][0].addOverFlowBin
  d1.data_histo.Add(d2.data_histo)
  if pos==-1:
    d1.legendText = 'Data SF'
    d3.legendText = 'Data OF'
  if pos==-2:
    d1.legendText = 'Signal SF'
    d3.legendText = 'Signal OF'
  d3.color = myBlue
  d3.style = "l12"
  if normalized=="eff":
    r_mue = 1.24
    eEE = 93.0; eEMu = 92.5; eMuMu = 94.4;
    fac = 0.5* (r_mue + 1./r_mue) * sqrt( eEE * eMuMu) / eEMu
    errScaleFac = abs(1-1./r_mue**2)/(1+1./r_mue**2)*0.1
#    for ibin in range(d3.data_histo.GetNbinsX()+1):
#      d3.data_histo.SetBinError(ibin, d3.data_histo.GetBinError(ibin)*(1.+errScaleFac))
    d3.data_histo.Scale(fac)
  if normalized=="area":
    y = d1.data_histo.Integral()
    x = d3.data_histo.Integral()
    if x>0:
      d3.data_histo.Scale(y/x)

  maximum = max([d3.data_histo.GetMaximum(), d1.data_histo.GetMaximum() ])

  if stackDict['doubleMu'][0].logy:
    d3.maximum = 10*maximum
    d1.maximum = 10*maximum
    d3.minimum = 10**(-.3)
    d1.minimum = 10**(-.3)
  else:
    d3.maximum = 1.4*maximum
    d1.maximum = 1.4*maximum
    d3.minimum =0.
    d1.minimum =0.
  d3.dataMCRatio = [d1, d3]
  d3.ratioVarName = "SF / OF"
  return [d3, d1]

def getOFSubtractedWithSignal(stack):
  print stack
  stackData = getOFSubtractedStack(stack[0], normalized="eff")
  stackSignal = getOFSubtractedStack(stack[0], normalized="eff", pos=-2)
  dSig = copy.deepcopy(stackData[0])
  dSig.data_histo.Add(stackSignal[1].data_histo)
  stackSignal[0].data_histo.Scale(-1)
  dSig.data_histo.Add(stackSignal[0].data_histo)
  dSig.legendText = "Data OF + Sig(SF-OF)"
  dSig.style = "l12"
  dSig.color = ROOT.kRed + 3
  stackData[0].dataMCRatio = [stackData[1], dSig]
  stackData[0].ratioVarName = "SF / OF"
  return stackData+[dSig]

stacksToDraw = [\
  [ngoodVertices_stack, "ngoodVertices"],
  [met_stack, "met"]
  ]
if not doOnlyMET:
  stacksToDraw+=[\
  [kinMetSig_stack, "kinMetSig"],
  [ht_stack, "ht"],
  [jzb_stack, "jzb"],
  [mLL_stack, "mLL"],
  [ptZ_stack, "ptZ"],
  [jet0_pt_stack, "jet0_pt"],
  [jet1_pt_stack, "jet1_pt"],
  [jet2_pt_stack, "jet2_pt"],
  [jet3_pt_stack, "jet3_pt"],
#  [ngoodElectrons_stack, "ngoodElectrons"],
#  [ngoodMuons_stack, "ngoodMuons"],
#  [nvetoElectrons_stack, "nvetoElectrons"],
#  [nvetoMuons_stack, "nvetoMuons"],
  [nbtags_stack, "nbtags"],
  [btag0pt_stack, "btag0pt"],
  [btag1pt_stack, "btag1pt"],
  [njets_stack, "njets"],
  [minLepMetIso_stack, "minLepMetIso"],
  [minJetsMetIso_stack, "minJetsMetIso"],
  [minbJetsMetIso_stack, "minbJetsMetIso"],
  [minLepbJetIso_stack, "minLepbJetIso"],
  [minLepJetIso_stack, "minLepJetIso"],
  [deltaPhibb_stack, "deltaPhibb"],
  [deltaEtabb_stack, "deltaEtabb"],
  [deltaRbb_stack, "deltaRbb"],
  [deltaPhiLL_stack, "deltaPhiLL"],
  [deltaEtaLL_stack, "deltaEtaLL"],
  [deltaRLL_stack, "deltaRLL"],
  [mbl_stack, "mbl"],
  [mbb_stack, "mbb"],
  [deltaHT_stack, "minDeltaHT"],
  [deltaHT2_stack, "minDeltaHT_zoomed"],
  [mbl1MinDeltaHT_stack, "mbl1"],
  [mbl2MinDeltaHT_stack, "mbl2"],
  [mllbb_stack, "mllbb"]
]

for stack in stacksToDraw:
  for lmode in lmodes:
    maximum = max([stack[0][lmode][0].data_histo.GetMaximum(), stack[0][lmode][-1].data_histo.GetMaximum() ])
    stack[0][lmode][0].maximum = 10*maximum # 10.*stack[-1].data_histo.GetMaximum()
    stack[0][lmode][0].logy = True
    stack[0][lmode][-1].logy = True
    stack[0][lmode][0].minimum = 10**(-.3)
    for var in stack[0][lmode]:
      var.lines = [[0.2, 0.9, "#font[22]{CMS Collaboration}"], [0.2,0.85,str(int(round(targetLumi/10.))/100.)+" fb^{-1},  #sqrt{s} = 8 TeV"]]
      var.legendCoordinates=[0.61,0.95 - 0.08*3,.98,.95]
#    drawNMStacks(1,1,[stack[0][lmode]],             subdir+"/"+lmode+"/"+prefix+stack[1], False)
#  drawNMStacks(1,1,[getOFSubtractedStack(stack[0], normalized = "eff")],             subdir+"/OFSub/"+prefix+stack[1]+"_normalized", False)
  ofSubtractedStacklWithSignal = getOFSubtractedWithSignal(stack)
  ofSubSignalFileName = subdir+"/OFSub/"+prefix+stack[1]+"_signal_T6bbzzv13_"+str(msq)+"_"+str(mN)+"_normalized"
  signalStack = getOFSubtractedStack(stack[0], normalized = "eff", pos=-2)

  drawNMStacks(3,1,[ofSubtractedStacklWithSignal, getOFSubtractedStack(stack[0], normalized = "eff"), signalStack],\
                    ofSubSignalFileName+".png", False)

  tf = ROOT.TFile(defaultWWWPath+"/"+ofSubSignalFileName+"_histos.root", "recreate")
  ofSubtractedStacklWithSignal[0].data_histo.SetName("DataOF")
  ofSubtractedStacklWithSignal[1].data_histo.SetName("DataSF")
  ofSubtractedStacklWithSignal[2].data_histo.SetName("DataOFPlusSig")
  ofSubtractedStacklWithSignal[0].data_histo.Write()
  ofSubtractedStacklWithSignal[1].data_histo.Write()
  ofSubtractedStacklWithSignal[2].data_histo.Write()
  signalStack[0].data_histo.SetName("SignalOF")
  signalStack[1].data_histo.SetName("SignalSF")
  signalStack[0].data_histo.Write()
  signalStack[1].data_histo.Write()
  print "Written", defaultWWWPath+"/"+ofSubSignalFileName+"_histos.root"
  tf.Close()
#  drawNMStacks(1,1,[getOFSubtractedStack(stack[0], normalized = "area")],             subdir+"/OFSub/"+prefix+stack[1]+"_areanormalized", False)

#  for lmode in lmodes:
#    maximum = max([stack[0][lmode][0].data_histo.GetMaximum(), stack[0][lmode][-1].data_histo.GetMaximum() ])
#    stack[0][lmode][0].maximum = 0.7*maximum
#    stack[0][lmode][0].logy = False
#    stack[0][lmode][-1].logy = False
#    stack[0][lmode][0].minumum=0
#    drawNMStacks(1,1,[stack[0][lmode]],             subdir+"/"+lmode+"/"+prefix+stack[1]+"_lin", False)
#  drawNMStacks(1,1,[getOFSubtractedStack(stack[0])],             subdir+"/OFSub/"+prefix+stack[1]+"_lin", False)
#  drawNMStacks(1,1,[getOFSubtractedStack(stack[0], normalized = "area")],             subdir+"/OFSub/"+prefix+stack[1]+"_areanormalized_lin", False)
