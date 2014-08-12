import ROOT
from array import array
from math import *
import os, copy, sys

ROOT.TH1F().SetDefaultSumw2()

from monoJetEventShapeVars import thrust, foxWolframMoments, circularity2D
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, passPUJetID, getISRweight, minDeltaRLeptonJets#, findClosestObjectDR, invMass 
#simplePUreweightHisto = getObjFromFile('/data/schoef/monoJetStuff/simpPUreweighting.root', "ngoodVertices_Data")
from Workspace.RA4Analysis.mvaFuncs import cosDeltaPhiLepW
from Workspace.RA4Analysis.simplePlotsCommon import *
small = False

targetLumi = 19700.

from Workspace.MonoJetAnalysis.defaultConvertedTuples import * 

#wjetsSample = wJetsToLNuInc
#wjetsSample = wJetsHT150v2
wjetsSample = wJetsToLNu
#allSamples = [data, dy_and_ww, ttJets, zJetsInv, wJetsToLNu, singleTop, ww, qcd]
allSamples = [data, dy, ttJetsPowHeg, zJetsInv, wjetsSample, singleTop, vv, qcd]
#allSamples = [data, dy,  zJetsInv, wJetsToLNu, singleTop, qcd]
#prepreprefix = "wJetsToLNu"
#prepreprefix = "wJetsHT150v2"
prepreprefix = ""
allVars=[]
allStacks=[]

## plots for studying preselection 

minimum=10**(-0.5)

chmode = "copy"
presel = "refSel"
ver = "v6"
#region = "preSelHT200"
region = "preSel"
#region = "negCh_pmuboost3d_below_45"
#region = "negCh_isrJetPt350"
#region = "highMETlowISRJetPtCR"
#region = "lowMETlowISRJetPtCR"
#region = "SR23NoMT"
#region = "SR23MTPeak"
#region = "SR23MTPeakNegPdg"
#region = "SR23MTPeakPosPdg"
#region = "SR23MTPeakPosPdg"
#region = "CR23NoMTPosCharge"
#region = "CR23NoMTNegCharge"
#region = "CR23NoMTPosChargeLowRI"
#region = "CR23NoMTNegChargeLowRI"
#region = "CR23NoMTPosChargeISRJetPt200"
#region = "CR23NoMTNegChargeISRJetPt200"
#region = "CR23NoMTPosChargeHighMT"
#region = "CR23NoMTNegChargeHighMT"
#region = "CR23NoMTPosChargenbtag1"
#region = "CR23NoMTNegChargenbtag1"
preprefix = region+"_"+ver
if prepreprefix!="":
  preprefix = prepreprefix+"_"+preprefix
if region == "SR1":
  #isrjet>350, met>250, mT<70
  additionalCut = "type1phiMet>300&&isrJetPt>325&&Sum$(jetBtag>0.679&&jetPt>60)==0&&nbtags>0"
  addData = False
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "SR2":
  additionalCut = "type1phiMet>300&&ht>400&&nbtags==0&&softIsolatedMuPdg>0&&abs(softIsolatedMuEta)<1.5&&softIsolatedMT<60."
  addData = False
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "SR3":
  additionalCut = "type1phiMet>300&&ht>400&&nbtags==0&&softIsolatedMuPdg>0&&abs(softIsolatedMuEta)<1.5&&softIsolatedMT>88."
  addData = False
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "SR23MTPeak":
  additionalCut = "type1phiMet>300&&ht>400&&nbtags==0&&abs(softIsolatedMuEta)<1.5&&softIsolatedMT<88.&&softIsolatedMT>60"
  addData =True
  addSignals = False
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "SR23MTPeakPosPdg":
  additionalCut = "type1phiMet>300&&ht>400&&nbtags==0&&abs(softIsolatedMuEta)<1.5&&softIsolatedMT<88.&&softIsolatedMT>60&&softIsolatedMuPdg>0"
  addData =True
  addSignals = False
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "SR23MTPeakNegPdg":
  additionalCut = "type1phiMet>300&&ht>400&&nbtags==0&&abs(softIsolatedMuEta)<1.5&&softIsolatedMT<88.&&softIsolatedMT>60&&softIsolatedMuPdg<0"
  addData =True
  addSignals = False
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "SR23MTPeakPosPdgLowSlice50":
  additionalCut = "type1phiMet>250&&type1phiMet<300&&ht>350&&ht<400&&nbtags==0&&abs(softIsolatedMuEta)<1.5&&softIsolatedMT<88.&&softIsolatedMT>60&&softIsolatedMuPdg>0"
  addData =True
  addSignals = False
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "SR23NoMT":
  additionalCut = "type1phiMet>300&&ht>400&&nbtags==0&&softIsolatedMuPdg>0&&abs(softIsolatedMuEta)<1.5"
  addData = False
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "CR23NoMTNegCharge":
  additionalCut = "type1phiMet>200&&type1phiMet<300&&nbtags==0&&softIsolatedMuPdg>0&&abs(softIsolatedMuEta)<1.5"
  addData = True
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "CR23NoMTPosCharge":
  additionalCut = "type1phiMet>200&&type1phiMet<300&&nbtags==0&&softIsolatedMuPdg<0&&abs(softIsolatedMuEta)<1.5"
  addData = True
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "CR23NoMTNegChargeLowRI":
  additionalCut = "type1phiMet>200&&type1phiMet<300&&nbtags==0&&softIsolatedMuPdg>0&&abs(softIsolatedMuEta)<1.5&&softIsolatedMuRelIso<0.1"
  addData = True
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "CR23NoMTPosChargeLowRI":
  additionalCut = "type1phiMet>200&&type1phiMet<300&&nbtags==0&&softIsolatedMuPdg<0&&abs(softIsolatedMuEta)<1.5&&softIsolatedMuRelIso<0.1"
  addData = True
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "CR23NoMTNegChargenbtag1":
  additionalCut = "type1phiMet>200&&type1phiMet<300&&nbtags>=1&&softIsolatedMuPdg>0&&abs(softIsolatedMuEta)<1.5"
  addData = True
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "CR23NoMTPosChargenbtag1":
  additionalCut = "type1phiMet>200&&type1phiMet<300&&nbtags>=1&&softIsolatedMuPdg<0&&abs(softIsolatedMuEta)<1.5"
  addData = True
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "CR23NoMTNegChargeHighMT":
  additionalCut = "type1phiMet>200&&type1phiMet<300&&nbtags==0&&softIsolatedMuPdg>0&&abs(softIsolatedMuEta)<1.5&&softIsolatedMT>90"
  addData = True
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "CR23NoMTPosChargeHighMT":
  additionalCut = "type1phiMet>200&&type1phiMet<300&&nbtags==0&&softIsolatedMuPdg<0&&abs(softIsolatedMuEta)<1.5&&softIsolatedMT>90"
  addData = True
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "CR23NoMTNegChargeISRJetPt200":
  additionalCut = "type1phiMet>200&&type1phiMet<300&&nbtags==0&&softIsolatedMuPdg>0&&abs(softIsolatedMuEta)<1.5&&isrJetPt>200"
  addData = True
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "CR23NoMTPosChargeISRJetPt200":
  additionalCut = "type1phiMet>200&&type1phiMet<300&&nbtags==0&&softIsolatedMuPdg<0&&abs(softIsolatedMuEta)<1.5&&isrJetPt>200"
  addData = True
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
#if region == "lowMEThighISRJetPtCR":
#  additionalCut = "type1phiMet>150&&type1phiMet<=250&&isrJetPt>350&&softIsolatedMT<70&&softIsolatedMuPdg>0"
#  addData = True
#  addSignals = True
#  normalizeToData = False
#  normalizeSignalToMCSum = False
#if region == "highMETlowISRJetPtCR":
#  additionalCut = "type1phiMet>250&&isrJetPt<=350&&softIsolatedMT<70&&softIsolatedMuPdg>0"
#  addData = True
#  addSignals = True
#  normalizeToData = False
#  normalizeSignalToMCSum = False
#if region == "lowMETlowISRJetPtCR":
#  additionalCut = "type1phiMet<=250&&isrJetPt<=350&&softIsolatedMT<70&&softIsolatedMuPdg>0"
#  addData = True
#  addSignals = True
#  normalizeToData = False
#  normalizeSignalToMCSum = False
if region == "preSel":
  #isrjet>350, met>250, mT<70
  additionalCut = "(1)"
  addData = True
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "preSelHT200":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>200)"
  addData = True
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
#if region == "negCh_isrJetPt350":
#  additionalCut = "softIsolatedMuPdg>0&&isrJetPt>350"
#  addData = False
#  addSignals = True
#  normalizeToData = False
#  normalizeSignalToMCSum = False
#if region == "negCh_isrJetPt500":
#  additionalCut = "softIsolatedMuPdg>0&&isrJetPt>500"
#  addData = False
#  addSignals = True
#  normalizeToData = False
#  normalizeSignalToMCSum = False
#if region == "negCh_pmuboost3d_below_45":
#  additionalCut = "softIsolatedMuPdg>0&&softIsolatedpmuboost3d<45"
#  addData = False
#  addSignals = True
#  normalizeToData = False
#  normalizeSignalToMCSum = False

subdir = "/pngDegStopPreSel/"
doOnlyOne=True
doAnalysisVars            = True
doAllDiscriminatingVars   = False 
doSoftIsolatedVars        = False 
doISRJetVars              = True
doOtherVars               = True 

chainstring = "Events"
commoncf = "(0)"
prefix="empty_"
if presel == "refSel":
  commoncf="isrJetPt>110&&type1phiMet>200&&isrJetBTBVetoPassed&&softIsolatedMuPt>5&&nHardElectrons+nHardMuonsRelIso02+nHardTaus==0&&njet60<=2"
if presel == "refSelNoBTB":
  commoncf="isrJetPt>110&&type1phiMet>200&&softIsolatedMuPt>5&&nHardElectrons+nHardMuonsRelIso02+nHardTaus==0&&njet60<=2"
if presel == "refSelNoTau":
  commoncf="isrJetPt>110&&type1phiMet>200&&isrJetBTBVetoPassed&&softIsolatedMuPt>5&&nHardElectrons+nHardMuonsRelIso02==0&&njet60<=2"
if presel == "inc":
  commoncf="(1)"
if presel == "incMu":
  commoncf="softIsolatedMuPt>5&&nHardElectrons+nHardMuonsRelIso02==0"
#  commoncf="njet<=3"
if presel == "inclusive":
  commoncf="(1)"
#  commoncf="njet<=3"

if additionalCut!="":
  commoncf+="&&"+additionalCut

prefix = "DegStop_"+preprefix+"_"+presel+"_"+chmode+"_"

stop300lsp270FullSim["legendText"]  = "m_{#tilde t} = 300, m_{LSP} = 270 (Fulls.)"
stop300lsp270FullSim["color"]  = ROOT.kRed + 3 
stop300lsp240g150FullSim["legendText"]  = "m_{#tilde t} = 300, m_{LSP} = 240 (Fulls.)"
stop300lsp240g150FullSim["color"]  = ROOT.kBlue + 3 
stop300lsp270FastSim["legendText"]  = "m_{#tilde t} = 300, m_{LSP} = 270 (Fasts.)"
stop300lsp270FastSim["color"]  = ROOT.kRed + 3 
stop300lsp240g150FastSim["legendText"]  = "m_{#tilde t} = 300, m_{LSP} = 240 (Fasts.)"
stop300lsp240g150FastSim["color"]  = ROOT.kBlue + 3 

signals=[stop300lsp270FullSim, stop300lsp240g150FullSim, stop300lsp270FastSim]
signals=[stop300lsp270FullSim, stop300lsp240g150FullSim]
if addSignals:
  allSamples += signals

for sample in allSamples:
  sample["Chain"] = chainstring
  sample["dirname"] = "/data/schoef/monoJetTuples_"+ver+"/"+chmode+"/"
for sample in allSamples[1:]:
  sample["weight"] = "puWeight"

def getStack(varstring, binning, cutstring, signals, varfunc = "", addData=True, additionalCutFunc = ""):
  DATA          = variable(varstring, binning, cutstring,additionalCutFunc=additionalCutFunc)
  DATA.sample   = data
#  DATA.color    = ROOT.kGray
  DATA.color    = dataColor
  DATA.legendText="Data"

  MC_WJETS                     = variable(varstring, binning, cutstring, additionalCutFunc=additionalCutFunc) 
  MC_WJETS.sample              = wjetsSample
  MC_TTJETS                    = variable(varstring, binning, cutstring, additionalCutFunc=additionalCutFunc)
  MC_TTJETS.sample             = ttJetsPowHeg
  MC_STOP                      = variable(varstring, binning, cutstring, additionalCutFunc=additionalCutFunc) 
  MC_STOP.sample               = singleTop
  MC_ZJETSINV                  = variable(varstring, binning, cutstring, additionalCutFunc=additionalCutFunc) 
  MC_ZJETSINV.sample           = zJetsInv
  MC_Z                         = variable(varstring, binning, cutstring, additionalCutFunc=additionalCutFunc) 
  MC_Z.sample                  = dy
  MC_VV                        = variable(varstring, binning, cutstring, additionalCutFunc=additionalCutFunc) 
  MC_VV.sample                 = vv
  MC_QCD                       = variable(varstring, binning, cutstring, additionalCutFunc=additionalCutFunc)
  MC_QCD.sample                = qcd

  MC_WJETS.legendText          = "W + Jets"
  MC_WJETS.style               = "f0"
  MC_WJETS.add                 = [MC_TTJETS]
  MC_WJETS.color               = ROOT.kYellow
  MC_TTJETS.legendText         = "t#bar{t} + Jets"
  MC_TTJETS.style              = "f0"
  MC_TTJETS.color              = ROOT.kRed - 3
  MC_TTJETS.add                =  [MC_STOP]
  MC_STOP.legendText           = "single Top"
  MC_STOP.style                = "f0"
  MC_STOP.add                  = [MC_ZJETSINV]
  MC_STOP.color                = ROOT.kOrange + 4
  MC_ZJETSINV.legendText       = "Z to Inv."
  MC_ZJETSINV.style            = "f0"
  MC_ZJETSINV.add              = [MC_Z]
  MC_ZJETSINV.color            = ROOT.kCyan - 8
  MC_Z.legendText             = "DY + Jets"
  MC_Z.style                  = "f0"
  MC_Z.add                    = [MC_VV]
  MC_Z.color                  = ROOT.kGreen + 3
  MC_VV.legendText          = "VV (WZ,WW,ZZ)"
  MC_VV.style               = "f0"
  MC_VV.add                 = [MC_QCD]
  MC_VV.color               = ROOT.kViolet + 8

  MC_QCD.color                 = myBlue
  MC_QCD.legendText            = "QCD"
  MC_QCD.style                 = "f0"
  MC_QCD.add                   = []

  res = [MC_WJETS, MC_TTJETS, MC_STOP,MC_ZJETSINV, MC_Z, MC_VV, MC_QCD]
  for v in res:
#    v.reweightVar = "ngoodVertices"
#    v.reweightHisto = simplePUreweightHisto 
    v.legendCoordinates=[0.61,0.95 - 0.08*5,.98,.95]
  for signal in signals:
    MC_SIGNAL                    = variable(varstring, binning, cutstring,additionalCutFunc=additionalCutFunc)
    MC_SIGNAL.sample             = copy.deepcopy(signal)
    MC_SIGNAL.legendText         = signal["name"]
    MC_SIGNAL.style              = "l02"
    MC_SIGNAL.color              = signal['color'] 
    MC_SIGNAL.add = []
    MC_SIGNAL.reweightVar = lambda c:getISRweight(c, mode='Central')
    res.append(MC_SIGNAL)
    if normalizeSignalToMCSum:
      MC_SIGNAL.normalizeTo = res[0]
 
  getLinesForStack(res, targetLumi)
  nhistos = len(res)
  if addData:
    res.append(DATA)
#    res[0].dataMCRatio = [DATA, res[0]]
#  else:
#    res[0].dataMCRatio = [MC_SIGNAL, res[0]]
#    res[0].ratioVarName = "SUS/SM" 
  if varfunc!="":
    for var in res:
      var.varfunc = varfunc
  return res

def lp(c):
  ptl = getVarValue(c, 'softIsolatedMuPt')
  phil = getVarValue(c, 'softIsolatedMuPhi')
  met = getVarValue(c, 'type1phiMet')
  metphi = getVarValue(c, 'type1phiMetphi')
  pxL = ptl*cos(phil)
  pyL = ptl*sin(phil)
  pxW = met*cos(metphi) + pxL
  pyW = met*sin(metphi) + pyL
  return (pxW*pxL+pyW*pyL)/(pxW**2+pyW**2)

if doAnalysisVars:
  isrJetPt_stack = getStack(":isrJetPt;p_{T} of ISR jet;Number of Events / 20 GeV",[50,0,1000], commoncf, signals, addData = addData)
  isrJetPt_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetPt_stack)

  lp_stack = getStack(":XXX;L_{P};Number of Events",[40,-.1,.1], commoncf, signals, addData = addData, varfunc = lp)
  lp_stack[0].addOverFlowBin = "upper"
  allStacks.append(lp_stack)

  minDeltaRLepJets_stack = getStack(":XXX;min(#DeltaR(l, j));Number of Events",[10,0,4], commoncf, signals, addData = addData, varfunc = minDeltaRLeptonJets)
  minDeltaRLepJets_stack[0].addOverFlowBin = "upper"
  allStacks.append(minDeltaRLepJets_stack)

  isrJetEta_stack = getStack(":isrJetEta;#eta of ISR jet;Number of Events",[20,-5,5], commoncf, signals, addData = addData)
  isrJetEta_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetEta_stack)

  softIsolatedMuPt_stack = getStack(":softIsolatedMuPt;p_{T} of soft isolated muon;Number of Events / 1 GeV",[25,0,25], commoncf, signals, addData = addData)
  softIsolatedMuPt_stack[0].addOverFlowBin = "upper"
  allStacks.append(softIsolatedMuPt_stack)

  mT_stack  = getStack(":softIsolatedMT;m_{T} (GeV);Number of Events / 10 GeV",[21,0,210], commoncf, signals, addData = addData)
  mT_stack[0].addOverFlowBin = "upper"
  allStacks.append(mT_stack)

  met_stack = getStack(":type1phiMet;#slash{E}_{T} (GeV);Number of Events / 50 GeV",[18,150,1050], commoncf, signals, addData = addData)
  met_stack[0].addOverFlowBin = "upper"
  allStacks.append(met_stack)

  metNoMETCut_stack = getStack(":type1phiMet;#slash{E}_{T} (GeV);Number of Events / 50 GeV",[18,150,1050], commoncf.replace('&&type1phiMet>200','').replace('&&type1phiMet<300','').replace('&&type1phiMet>300',''), signals, addData = addData)
  metNoMETCut_stack[0].addOverFlowBin = "upper"
  allStacks.append(metNoMETCut_stack)

  njet_stack = getStack(":njet;n_{jet};Number of Events",[10,0,10], commoncf, signals, addData = addData)
  njet_stack[0].addOverFlowBin = "upper"
  allStacks.append(njet_stack)

  njet60_stack = getStack(":njet60;n_{jet};Number of Events",[10,0,10], commoncf.replace('&&njet60<=2',''), signals, addData = addData)
  njet60_stack[0].addOverFlowBin = "upper"
  allStacks.append(njet60_stack)
  
  nbtags_stack = getStack(":nbtags;n_{b-tags};Number of Events",[10,0,10], commoncf, signals, addData = addData)
  nbtags_stack[0].addOverFlowBin = "upper"
  allStacks.append(nbtags_stack)

  ht_stack                          = getStack(":ht;H_{T} (GeV);Number of Events / 50 GeV",[31,0,1550 ], commoncf, signals, addData = addData)
  ht_stack[0].addOverFlowBin = "upper"
  allStacks.append(ht_stack)

  softIsolatedMuEta_stack = getStack(":softIsolatedMuEta;#eta of soft isolated muon;Number of Events",[20,-4,4], commoncf, signals, addData = addData)
  softIsolatedMuEta_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuEta_stack)

  softIsolatedMuCharge_stack = getStack(":XXX;charge of soft isolated muon;Number of Events",[3,-1,2], commoncf, signals, lambda c: -c.GetLeaf('softIsolatedMuPdg').GetValue()/abs(c.GetLeaf('softIsolatedMuPdg').GetValue()), addData = addData)
  softIsolatedMuCharge_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuCharge_stack)



if doAllDiscriminatingVars:
  def htThrustMetSideFunc(c):
    t = thrust(c)['htThrustMetSide']
    if t>0.7: print c.GetLeaf('run').GetValue(), c.GetLeaf('lumi').GetValue(), c.GetLeaf('event').GetValue()
    return t

  htThrustMetSide_stack = getStack(":xxx;htThrustMetSide;Number of Events",[50,0,1], commoncf, signals, addData = addData, varfunc = htThrustMetSideFunc)
  htThrustMetSide_stack[0].addOverFlowBin = "upper"
  allStacks.append(htThrustMetSide_stack)

#  closestMuJetMass_stack = getStack(":xxx;closestMuJetMass;Number of Events",[50,0,500], commoncf, signals, addData = addData, varfunc = closestMuJetMass)
#  closestMuJetMass_stack[0].addOverFlowBin = "upper"
#  allStacks.append(closestMuJetMass_stack)
#
#  closestMuJetDeltaR_stack = getStack(":xxx;closestMuJetDeltaR;Number of Events",[50,0,7], commoncf, signals, addData = addData, varfunc = closestMuJetDeltaR)
#  closestMuJetDeltaR_stack[0].addOverFlowBin = "upper"
#  allStacks.append(closestMuJetDeltaR_stack)
#
#  closestMuJetDeltaR_zoomed_stack = getStack(":xxx;closestMuJetDeltaR;Number of Events",[50,0,1], commoncf, signals, addData = addData, varfunc = closestMuJetDeltaR)
#  closestMuJetDeltaR_zoomed_stack[0].addOverFlowBin = "upper"
#  allStacks.append(closestMuJetDeltaR_zoomed_stack)

  cosPhiMetJet_stack = getStack(":xxx;cos(#phi(#slash{E}_{T}, ISR-jet));Number of Events",[20,-1,1], commoncf, signals, addData = addData, varfunc = lambda c: cos(getVarValue(c, 'isrJetPhi') - getVarValue(c, 'softIsolatedMuPhi')))
  cosPhiMetJet_stack[0].addOverFlowBin = "both"
  allStacks.append(cosPhiMetJet_stack)

  FWMT1_stack = getStack(":xxx;FMWT1 (jets,lep,MET);Number of Events",[20,0,1], commoncf, signals, addData = addData, varfunc = lambda c:foxWolframMoments(c)['FWMT1'])
  FWMT1_stack[0].addOverFlowBin = "upper"
  allStacks.append(FWMT1_stack)

  FWMT2_stack = getStack(":xxx;FMWT2 (jets,lep,MET);Number of Events",[20,0,1], commoncf, signals, addData = addData, varfunc = lambda c:foxWolframMoments(c)['FWMT2'])
  FWMT2_stack[0].addOverFlowBin = "upper"
  allStacks.append(FWMT2_stack)

  FWMT3_stack = getStack(":xxx;FMWT3 (jets,lep,MET);Number of Events",[20,0,1], commoncf, signals, addData = addData, varfunc = lambda c:foxWolframMoments(c)['FWMT3'])
  FWMT3_stack[0].addOverFlowBin = "upper"
  allStacks.append(FWMT3_stack)

  FWMT4_stack = getStack(":xxx;FMWT4 (jets,lep,MET);Number of Events",[20,0,1], commoncf, signals, addData = addData, varfunc = lambda c:foxWolframMoments(c)['FWMT4'])
  FWMT4_stack[0].addOverFlowBin = "upper"
  allStacks.append(FWMT4_stack)


  c2D_stack = getStack(":xxx;c2D (jets,lep,MET);Number of Events",[20,0,1], commoncf, signals, addData = addData, varfunc = lambda c:circularity2D(c)['c2D'])
  c2D_stack[0].addOverFlowBin = "upper"
  allStacks.append(c2D_stack)

  linC2D_stack = getStack(":xxx;linC2D (jets,lep,MET);Number of Events",[20,0,1], commoncf, signals, addData = addData, varfunc = lambda c:circularity2D(c)['linC2D'])
  linC2D_stack[0].addOverFlowBin = "upper"
  allStacks.append(linC2D_stack)

  thrust_stack = getStack(":xxx;thrust;Number of Events",[20,0.6,1], commoncf, signals, addData = addData, varfunc = lambda c: thrust(c)['thrust'])
  thrust_stack[0].addOverFlowBin = "upper"
  allStacks.append(thrust_stack)

  htThrustLepSide_stack = getStack(":xxx;htThrustLepSide;Number of Events",[50,0,1], commoncf, signals, addData = addData, varfunc = lambda c: thrust(c)['htThrustLepSide'])
  htThrustLepSide_stack[0].addOverFlowBin = "upper"
  allStacks.append(htThrustLepSide_stack)

  sTlep_stack  = getStack(":XXX;S_{T, lep.} (GeV);Number of Events / 50 GeV",[21,0,1050], commoncf, signals, lambda c: c.GetLeaf('softIsolatedMuPt').GetValue() + c.GetLeaf('type1phiMet').GetValue() , addData = addData)
  sTlep_stack[0].addOverFlowBin = "upper"
  allStacks.append(sTlep_stack)

  cosDeltaPhiLepMET_stack  = getStack(":xxx;cos(#Delta #phi(l, #slash{E}_{T}));Number of Events",[30,-1.1,1.1], commoncf, signals, lambda c: cos(c.GetLeaf('softIsolatedMuPhi').GetValue() - c.GetLeaf('type1phiMetphi').GetValue()), addData = addData)
  allStacks.append(cosDeltaPhiLepMET_stack)

  cosDeltaPhiLepW_stack  = getStack(":xxx;cos(#Delta #phi(l, #slash{E}_{T}));Number of Events",[30,-1.1,1.1], commoncf, signals, cosDeltaPhiLepW, addData = addData)
  allStacks.append(cosDeltaPhiLepW_stack)

#  ptw_stack = getStack(":sqrt((metpx + leptonPt*cos(lepton_phi))**2 + (metpy + leptonPt*sin(lepton_phi))**2);(l+#slash{E})_{T}; Number of Events / 25 GeV",[21,0,525], commoncf, signals, addData = addData)
#  ptw_stack[0].addOverFlowBin = "upper"
#  allStacks.append(ptw_stack)


if doSoftIsolatedVars:

  softIsolatedMuPhi_stack = getStack(":softIsolatedMuPhi;#phi of soft isolated muon;Number of Events",[20,-4,4], commoncf, signals, addData = addData)
  softIsolatedMuPhi_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuPhi_stack)

  softIsolatedMuRelIso_stack = getStack(":softIsolatedMuRelIso;I_{rel.} of soft isolated muon;Number of Events",[24,0,1.2], commoncf, signals, addData = addData)
  softIsolatedMuRelIso_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuRelIso_stack)

  softIsolatedMuAbsIso_stack = getStack(":XXX;I_{abs.} of soft isolated muon;Number of Events",[30,0,12], commoncf, signals, lambda c: c.GetLeaf('softIsolatedMuRelIso').GetValue()*c.GetLeaf('softIsolatedMuPt').GetValue(), addData = addData)
  softIsolatedMuAbsIso_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuAbsIso_stack)

  softIsolatedMuDxy_stack = getStack(":softIsolatedMuDxy;d_{xy} of soft isolated muon;Number of Events",[40,0,.08], commoncf, signals, addData = addData)
  softIsolatedMuDxy_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuDxy_stack)

  softIsolatedMuNormChi2_stack = getStack(":softIsolatedMuNormChi2;#chi^{2} of global muon track;Number of Events",[30,0,30], commoncf, signals)
  softIsolatedMuNormChi2_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuNormChi2_stack)

  softIsolatedMuNValMuonHits_stack = getStack(":softIsolatedMuNValMuonHits;valid hits;Number of Events",[60,0,60], commoncf, signals)
  softIsolatedMuNValMuonHits_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuNValMuonHits_stack)

  softIsolatedMuNumMatchedStations_stack = getStack(":softIsolatedMuNumMatchedStations;matched stations;Number of Events",[8,0,8], commoncf, signals)
  softIsolatedMuNumMatchedStations_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuNumMatchedStations_stack)

  softIsolatedMuPixelHits_stack = getStack(":softIsolatedMuPixelHits;Pixel hits;Number of Events",[10,0,10], commoncf, signals)
  softIsolatedMuPixelHits_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuPixelHits_stack)

  softIsolatedMuPixelHits_lowDz_stack = getStack(":softIsolatedMuPixelHits;Pixel hits;Number of Events",[10,0,10], commoncf+"&&softIsolatedMuDz<0.2", signals)
  softIsolatedMuPixelHits_lowDz_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuPixelHits_lowDz_stack)

  softIsolatedMuPixelHits_highDz_stack = getStack(":softIsolatedMuPixelHits;Pixel hits;Number of Events",[10,0,10], commoncf+"&&softIsolatedMuDz>=0.2", signals)
  softIsolatedMuPixelHits_highDz_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuPixelHits_highDz_stack)

  softIsolatedMuNumtrackerLayerWithMeasurement_stack = getStack(":softIsolatedMuNumtrackerLayerWithMeasurement;tracker layer w. meas.;Number of Events",[20,0,20], commoncf, signals)
  softIsolatedMuNumtrackerLayerWithMeasurement_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuNumtrackerLayerWithMeasurement_stack)

  softIsolatedMuIsGlobal_stack = getStack(":softIsolatedMuIsGlobal;isGlobal;Number of Events",[2,0,2], commoncf, signals)
  softIsolatedMuIsGlobal_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuIsGlobal_stack)

  softIsolatedMuIsTracker_stack = getStack(":softIsolatedMuIsTracker;isTracker;Number of Events",[2,0,2], commoncf, signals)
  softIsolatedMuIsTracker_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuIsTracker_stack)

  softIsolatedMuDz_stack = getStack(":softIsolatedMuDz;d_{z} of soft isolated muon;Number of Events",[40,0,20], commoncf, signals)
  softIsolatedMuDz_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuDz_stack)

  softIsolatedMuDz_zoomed_stack = getStack(":softIsolatedMuDz;d_{z} of soft isolated muon;Number of Events",[40,0,2], commoncf, signals)
  softIsolatedMuDz_zoomed_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuDz_zoomed_stack)

  softIsolatedMuDz_noPixelHits_stack = getStack(":softIsolatedMuDz;d_{z} of soft isolated muon;Number of Events",[40,0,2], commoncf+"&&softIsolatedMuPixelHits==0", signals)
  softIsolatedMuDz_noPixelHits_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuDz_noPixelHits_stack)

  softIsolatedMuDz_onePixelHit_stack = getStack(":softIsolatedMuDz;d_{z} of soft isolated muon;Number of Events",[40,0,2], commoncf+"&&softIsolatedMuPixelHits>=1", signals)
  softIsolatedMuDz_onePixelHit_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuDz_onePixelHit_stack)

  softIsolatedMuDz_twoPixelHits_stack = getStack(":softIsolatedMuDz;d_{z} of soft isolated muon;Number of Events",[40,0,2], commoncf+"&&softIsolatedMuPixelHits>=2", signals)
  softIsolatedMuDz_twoPixelHits_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuDz_twoPixelHits_stack)


if doISRJetVars:

  isrJetPhi_stack = getStack(":isrJetPhi;#phi of ISR jet;Number of Events",[20,-pi,pi], commoncf, signals, addData = addData)
  isrJetPhi_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetPhi_stack)

  isrJetBtag_stack = getStack(":isrJetBtag;CSV b-tag of ISR jet;Number of Events",[20,-1,1], commoncf, signals, addData = addData)
  isrJetBtag_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetBtag_stack)

  isrJetChef_stack = getStack(":isrJetChef;Chef of ISR jet;Number of Events",[20,0,1], commoncf, signals, addData = addData)
  isrJetChef_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetChef_stack)

  isrJetNhef_stack = getStack(":isrJetNhef;Nhef of ISR jet;Number of Events",[20,0,1], commoncf, signals, addData = addData)
  isrJetNhef_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetNhef_stack)

  isrJetCeef_stack = getStack(":isrJetCeef;Ceef of ISR jet;Number of Events",[20,0,1], commoncf, signals, addData = addData)
  isrJetCeef_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetCeef_stack)

  isrJetNeef_stack = getStack(":isrJetNeef;Neef of ISR jet;Number of Events",[20,0,1], commoncf, signals, addData = addData)
  isrJetNeef_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetNeef_stack)

  isrJetHFhef_stack = getStack(":isrJetHFhef;HFhef of ISR jet;Number of Events",[20,0,1], commoncf, signals, addData = addData)
  isrJetHFhef_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetHFhef_stack)

  isrJetHFeef_stack = getStack(":isrJetHFeef;HFeef of ISR jet;Number of Events",[20,0,1], commoncf, signals, addData = addData)
  isrJetHFeef_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetHFeef_stack)

  isrJetMuef_stack = getStack(":isrJetMuef;Muef of ISR jet;Number of Events",[20,0,1], commoncf, signals, addData = addData)
  isrJetMuef_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetMuef_stack)

  isrJetElef_stack = getStack(":isrJetElef;Elef of ISR jet;Number of Events",[20,0,1], commoncf, signals, addData = addData)
  isrJetElef_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetElef_stack)

  isrJetPhef_stack = getStack(":isrJetPhef;Phef of ISR jet;Number of Events",[20,0,1], commoncf, signals, addData = addData)
  isrJetPhef_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetPhef_stack)

if doOtherVars:
  type1phiMetphi_stack = getStack(":type1phiMetphi;#phi(#slash{E}_{T});Number of Events",[40,-pi,pi], commoncf, signals, addData = addData)
  type1phiMetphi_stack[0].addOverFlowBin = "upper"
  allStacks.append(type1phiMetphi_stack)

  ngoodVertices_stack = getStack(":ngoodVertices;Number of Vertices;Number of Events",[61,0,61], commoncf, signals, addData = addData)
  ngoodVertices_stack[0].addOverFlowBin = "upper"
  allStacks.append(ngoodVertices_stack)

  njetWOjetCut_stack = getStack(":njet;n_{jet};Number of Events",[10,0,10], commoncf.replace('&&njet60<=2',''), signals, addData = addData)
  njetWOjetCut_stack[0].addOverFlowBin = "upper"
  allStacks.append(njetWOjetCut_stack)
  

#  isrJetFull53XPUJetIDTight_stack = getStack(":isrJetFull53XPUJetIDTight;isrJetFull53XPUJetIDTight;Number of Events",[2,0,2], commoncf, signals,lambda c: passPUJetID(int(c.GetLeaf('isrJetFull53XPUJetIDFlag').GetValue()),'Tight'), addData = addData)
#  allStacks.append(isrJetFull53XPUJetIDTight_stack)
#  isrJetFull53XPUJetIDMedium_stack = getStack(":isrJetFull53XPUJetIDMedium;isrJetFull53XPUJetIDMedium;Number of Events",[2,0,2], commoncf, signals,lambda c: passPUJetID(int(c.GetLeaf('isrJetFull53XPUJetIDFlag').GetValue()),'Medium'), addData = addData)
#  allStacks.append(isrJetFull53XPUJetIDMedium_stack)
#  isrJetFull53XPUJetIDLoose_stack = getStack(":isrJetFull53XPUJetIDLoose;isrJetFull53XPUJetIDLoose;Number of Events",[2,0,2], commoncf, signals,lambda c: passPUJetID(int(c.GetLeaf('isrJetFull53XPUJetIDFlag').GetValue()),'Loose'), addData = addData)
#  allStacks.append(isrJetFull53XPUJetIDLoose_stack)
#  
#  isrJetMET53XPUJetIDTight_stack = getStack(":isrJetMET53XPUJetIDTight;isrJetMET53XPUJetIDTight;Number of Events",[2,0,2], commoncf, signals,lambda c: passPUJetID(int(c.GetLeaf('isrJetMET53XPUJetIDFlag').GetValue()),'Tight'), addData = addData)
#  allStacks.append(isrJetMET53XPUJetIDTight_stack)
#  isrJetMET53XPUJetIDMedium_stack = getStack(":isrJetMET53XPUJetIDMedium;isrJetMET53XPUJetIDMedium;Number of Events",[2,0,2], commoncf, signals,lambda c: passPUJetID(int(c.GetLeaf('isrJetMET53XPUJetIDFlag').GetValue()),'Medium'), addData = addData)
#  allStacks.append(isrJetMET53XPUJetIDMedium_stack)
#  isrJetMET53XPUJetIDLoose_stack = getStack(":isrJetMET53XPUJetIDLoose;isrJetMET53XPUJetIDLoose;Number of Events",[2,0,2], commoncf, signals,lambda c: passPUJetID(int(c.GetLeaf('isrJetMET53XPUJetIDFlag').GetValue()),'Loose'), addData = addData)
#  allStacks.append(isrJetMET53XPUJetIDLoose_stack)
#  
#  isrJetCutBasedPUJetIDTight_stack = getStack(":isrJetCutBasedPUJetIDTight;isrJetCutBasedPUJetIDTight;Number of Events",[2,0,2], commoncf, signals,lambda c: passPUJetID(int(c.GetLeaf('isrJetCutBasedPUJetIDFlag').GetValue()),'Tight'), addData = addData)
#  allStacks.append(isrJetCutBasedPUJetIDTight_stack)
#  isrJetCutBasedPUJetIDMedium_stack = getStack(":isrJetCutBasedPUJetIDMedium;isrJetCutBasedPUJetIDMedium;Number of Events",[2,0,2], commoncf, signals,lambda c: passPUJetID(int(c.GetLeaf('isrJetCutBasedPUJetIDFlag').GetValue()),'Medium'), addData = addData)
#  allStacks.append(isrJetCutBasedPUJetIDMedium_stack)
#  isrJetCutBasedPUJetIDLoose_stack = getStack(":isrJetCutBasedPUJetIDLoose;isrJetCutBasedPUJetIDLoose;Number of Events",[2,0,2], commoncf, signals,lambda c: passPUJetID(int(c.GetLeaf('isrJetCutBasedPUJetIDFlag').GetValue()),'Loose'), addData = addData)
#  allStacks.append(isrJetCutBasedPUJetIDLoose_stack)
#  
#  isrJetMET53XPUJetIDTightVetoed_softIsolatedMuDz_stack = getStack(":softIsolatedMuDz;softIsolatedMuDz;Number of Events",[40,0,20], commoncf, signals, addData=addData, additionalCutFunc = lambda c: not  passPUJetID(int(c.GetLeaf('isrJetMET53XPUJetIDFlag').GetValue()),'Tight'))
#  allStacks.append(isrJetMET53XPUJetIDTightVetoed_softIsolatedMuDz_stack)
#  isrJetMET53XPUJetIDMediumVetoed_softIsolatedMuDz_stack = getStack(":softIsolatedMuDz;softIsolatedMuDz;Number of Events",[40,0,20], commoncf, signals, addData=addData, additionalCutFunc = lambda c: not  passPUJetID(int(c.GetLeaf('isrJetMET53XPUJetIDFlag').GetValue()),'Medium'))
#  allStacks.append(isrJetMET53XPUJetIDMediumVetoed_softIsolatedMuDz_stack)
#  isrJetMET53XPUJetIDLooseVetoed_softIsolatedMuDz_stack = getStack(":softIsolatedMuDz;softIsolatedMuDz;Number of Events",[40,0,20], commoncf, signals, addData=addData, additionalCutFunc = lambda c: not  passPUJetID(int(c.GetLeaf('isrJetMET53XPUJetIDFlag').GetValue()),'Loose'))
#  allStacks.append(isrJetMET53XPUJetIDLooseVetoed_softIsolatedMuDz_stack)
#  
#  isrJetFull53XPUJetIDTightVetoed_softIsolatedMuDz_stack = getStack(":softIsolatedMuDz;softIsolatedMuDz;Number of Events",[40,0,20], commoncf, signals, addData=addData, additionalCutFunc = lambda c: not  passPUJetID(int(c.GetLeaf('isrJetFull53XPUJetIDFlag').GetValue()),'Tight'))
#  allStacks.append(isrJetFull53XPUJetIDTightVetoed_softIsolatedMuDz_stack)
#  isrJetFull53XPUJetIDMediumVetoed_softIsolatedMuDz_stack = getStack(":softIsolatedMuDz;softIsolatedMuDz;Number of Events",[40,0,20], commoncf, signals, addData=addData, additionalCutFunc = lambda c: not  passPUJetID(int(c.GetLeaf('isrJetFull53XPUJetIDFlag').GetValue()),'Medium'))
#  allStacks.append(isrJetFull53XPUJetIDMediumVetoed_softIsolatedMuDz_stack)
#  isrJetFull53XPUJetIDLooseVetoed_softIsolatedMuDz_stack = getStack(":softIsolatedMuDz;softIsolatedMuDz;Number of Events",[40,0,20], commoncf, signals, addData=addData, additionalCutFunc = lambda c: not  passPUJetID(int(c.GetLeaf('isrJetFull53XPUJetIDFlag').GetValue()),'Loose'))
#  allStacks.append(isrJetFull53XPUJetIDLooseVetoed_softIsolatedMuDz_stack)
#  
#  isrJetCutBasedPUJetIDTightVetoed_softIsolatedMuDz_stack = getStack(":softIsolatedMuDz;softIsolatedMuDz;Number of Events",[40,0,20], commoncf, signals, addData=addData, additionalCutFunc = lambda c: not  passPUJetID(int(c.GetLeaf('isrJetCutBasedPUJetIDFlag').GetValue()),'Tight'))
#  allStacks.append(isrJetCutBasedPUJetIDTightVetoed_softIsolatedMuDz_stack)
#  isrJetCutBasedPUJetIDMediumVetoed_softIsolatedMuDz_stack = getStack(":softIsolatedMuDz;softIsolatedMuDz;Number of Events",[40,0,20], commoncf, signals, addData=addData, additionalCutFunc = lambda c: not  passPUJetID(int(c.GetLeaf('isrJetCutBasedPUJetIDFlag').GetValue()),'Medium'))
#  allStacks.append(isrJetCutBasedPUJetIDMediumVetoed_softIsolatedMuDz_stack)
#  isrJetCutBasedPUJetIDLooseVetoed_softIsolatedMuDz_stack = getStack(":softIsolatedMuDz;softIsolatedMuDz;Number of Events",[40,0,20], commoncf, signals, addData=addData, additionalCutFunc = lambda c: not  passPUJetID(int(c.GetLeaf('isrJetCutBasedPUJetIDFlag').GetValue()),'Loose'))
#  allStacks.append(isrJetCutBasedPUJetIDLooseVetoed_softIsolatedMuDz_stack)
#  
#  
#  isrJetMET53XPUJetIDTightPassed_softIsolatedMuDz_stack = getStack(":softIsolatedMuDz;softIsolatedMuDz;Number of Events",[40,0,20], commoncf, signals, addData=addData, additionalCutFunc = lambda c: passPUJetID(int(c.GetLeaf('isrJetMET53XPUJetIDFlag').GetValue()),'Tight'))
#  allStacks.append(isrJetMET53XPUJetIDTightPassed_softIsolatedMuDz_stack)
#  isrJetMET53XPUJetIDMediumPassed_softIsolatedMuDz_stack = getStack(":softIsolatedMuDz;softIsolatedMuDz;Number of Events",[40,0,20], commoncf, signals, addData=addData, additionalCutFunc = lambda c: passPUJetID(int(c.GetLeaf('isrJetMET53XPUJetIDFlag').GetValue()),'Medium'))
#  allStacks.append(isrJetMET53XPUJetIDMediumPassed_softIsolatedMuDz_stack)
#  isrJetMET53XPUJetIDLoosePassed_softIsolatedMuDz_stack = getStack(":softIsolatedMuDz;softIsolatedMuDz;Number of Events",[40,0,20], commoncf, signals, addData=addData, additionalCutFunc = lambda c: passPUJetID(int(c.GetLeaf('isrJetMET53XPUJetIDFlag').GetValue()),'Loose'))
#  allStacks.append(isrJetMET53XPUJetIDLoosePassed_softIsolatedMuDz_stack)
#  
#  isrJetFull53XPUJetIDTightPassed_softIsolatedMuDz_stack = getStack(":softIsolatedMuDz;softIsolatedMuDz;Number of Events",[40,0,20], commoncf, signals, addData=addData, additionalCutFunc = lambda c: passPUJetID(int(c.GetLeaf('isrJetFull53XPUJetIDFlag').GetValue()),'Tight'))
#  allStacks.append(isrJetFull53XPUJetIDTightPassed_softIsolatedMuDz_stack)
#  isrJetFull53XPUJetIDMediumPassed_softIsolatedMuDz_stack = getStack(":softIsolatedMuDz;softIsolatedMuDz;Number of Events",[40,0,20], commoncf, signals, addData=addData, additionalCutFunc = lambda c: passPUJetID(int(c.GetLeaf('isrJetFull53XPUJetIDFlag').GetValue()),'Medium'))
#  allStacks.append(isrJetFull53XPUJetIDMediumPassed_softIsolatedMuDz_stack)
#  isrJetFull53XPUJetIDLoosePassed_softIsolatedMuDz_stack = getStack(":softIsolatedMuDz;softIsolatedMuDz;Number of Events",[40,0,20], commoncf, signals, addData=addData, additionalCutFunc = lambda c: passPUJetID(int(c.GetLeaf('isrJetFull53XPUJetIDFlag').GetValue()),'Loose'))
#  allStacks.append(isrJetFull53XPUJetIDLoosePassed_softIsolatedMuDz_stack)
#  
#  isrJetCutBasedPUJetIDTightPassed_softIsolatedMuDz_stack = getStack(":softIsolatedMuDz;softIsolatedMuDz;Number of Events",[40,0,20], commoncf, signals, addData=addData, additionalCutFunc = lambda c: passPUJetID(int(c.GetLeaf('isrJetCutBasedPUJetIDFlag').GetValue()),'Tight'))
#  allStacks.append(isrJetCutBasedPUJetIDTightPassed_softIsolatedMuDz_stack)
#  isrJetCutBasedPUJetIDMediumPassed_softIsolatedMuDz_stack = getStack(":softIsolatedMuDz;softIsolatedMuDz;Number of Events",[40,0,20], commoncf, signals, addData=addData, additionalCutFunc = lambda c: passPUJetID(int(c.GetLeaf('isrJetCutBasedPUJetIDFlag').GetValue()),'Medium'))
#  allStacks.append(isrJetCutBasedPUJetIDMediumPassed_softIsolatedMuDz_stack)
#  isrJetCutBasedPUJetIDLoosePassed_softIsolatedMuDz_stack = getStack(":softIsolatedMuDz;softIsolatedMuDz;Number of Events",[40,0,20], commoncf, signals, addData=addData, additionalCutFunc = lambda c: passPUJetID(int(c.GetLeaf('isrJetCutBasedPUJetIDFlag').GetValue()),'Loose'))
#  allStacks.append(isrJetCutBasedPUJetIDLoosePassed_softIsolatedMuDz_stack)
#


for stack in allStacks:
  stack[0].minimum = minimum
  
execfile("../../RA4Analysis/plots/simplePlotsLoopKernel.py")

if normalizeToData:
  for stack in allStacks:
    for var in stack[:-1]:
      var.normalizeTo = stack[-1]
      var.normalizeWhat = stack[0]
    stack[-1].normalizeTo=""
    stack[-1].normalizeWhat=""
#else:
#  for stack in allStacks:
#    for var in stack:
#      var.normalizeTo = ""
#      var.normalizeWhat = "" 
#
for stack in allStacks:
  if addData:
    stack[0].maximum = 6*10**2 *stack[-1].data_histo.GetMaximum()
  else:
    stack[0].maximum = 6*10**2 *stack[0].data_histo.GetMaximum()
  stack[0].logy = True
  stack[0].minimum = minimum
#  stack[0].legendCoordinates=[0.76,0.95 - 0.3,.98,.95]
#  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS preliminary}"], [0.2,0.85,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 7 TeV"]]
  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS Collaboration}"], [0.2,0.85,str(int(round(targetLumi/10.))/100.)+" fb^{-1},  #sqrt{s} = 8 TeV"]]

if doAnalysisVars:
  drawNMStacks(1,1,[isrJetPt_stack],             subdir+prefix+"isrJetPt", False)
  drawNMStacks(1,1,[lp_stack],             subdir+prefix+"lp", False)
  drawNMStacks(1,1,[minDeltaRLepJets_stack],             subdir+prefix+"minDeltaRLepJets", False)
#  drawNMStacks(1,1,[pmuboost3d_stack],      subdir+prefix+"pmuboost3d", False)
  drawNMStacks(1,1,[isrJetEta_stack],             subdir+prefix+"isrJetEta", False)
  drawNMStacks(1,1,[mT_stack],              subdir+prefix+"mT", False)
  drawNMStacks(1,1,[softIsolatedMuPt_stack],            subdir+prefix+"softIsolatedMuPt", False)
  mT_stack[0].logY = False
  drawNMStacks(1,1,[mT_stack],              subdir+prefix+"mT_lin", False)
  drawNMStacks(1,1,[met_stack],             subdir+prefix+"met", False)
  drawNMStacks(1,1,[metNoMETCut_stack], subdir+prefix+"metNoMETCut", False)
  drawNMStacks(1,1,[njet_stack],             subdir+prefix+"njet", False)
  drawNMStacks(1,1,[njet60_stack],             subdir+prefix+"njet60", False)
  drawNMStacks(1,1,[nbtags_stack],             subdir+prefix+"nbtags", False)
  drawNMStacks(1,1,[ht_stack],              subdir+prefix+"ht", False)
  softIsolatedMuEta_stack[0].maximum = 6*10**3 *softIsolatedMuEta_stack[0].data_histo.GetMaximum()
  drawNMStacks(1,1,[softIsolatedMuEta_stack],            subdir+prefix+"softIsolatedMuEta", False)
  softIsolatedMuCharge_stack[0].maximum = 6*10**3 *softIsolatedMuCharge_stack[0].data_histo.GetMaximum()
  drawNMStacks(1,1,[softIsolatedMuCharge_stack],            subdir+prefix+"softIsolatedMuCharge", False)
if doAllDiscriminatingVars:
  htThrustMetSide_stack[0].maximum = 6*10**5 *htThrustMetSide_stack[0].data_histo.GetMaximum()
  drawNMStacks(1,1,[htThrustMetSide_stack],             subdir+prefix+"htThrustMetSide", False)
#  drawNMStacks(1,1,[closestMuJetMass_stack] ,             subdir+prefix+"closestMuJetMass_stack", False)
#  drawNMStacks(1,1,[closestMuJetDeltaR_stack] ,        subdir+prefix+"closestMuJetDeltaR_stack", False)
#  drawNMStacks(1,1,[closestMuJetDeltaR_zoomed_stack] ,        subdir+prefix+"closestMuJetDeltaR_zoomed_stack", False)
  FWMT2_stack[0].maximum = 6*10**4 *FWMT2_stack[0].data_histo.GetMaximum()
  FWMT3_stack[0].maximum = 6*10**3 *FWMT3_stack[0].data_histo.GetMaximum()
  FWMT4_stack[0].maximum = 6*10**4 *FWMT4_stack[0].data_histo.GetMaximum()
  cosPhiMetJet_stack[0].maximum = 6*10**3 *cosPhiMetJet_stack[0].data_histo.GetMaximum()
  thrust_stack[0].maximum = 6*10**4 *thrust_stack[0].data_histo.GetMaximum()
  htThrustLepSide_stack[0].maximum = 6*10**5 *htThrustLepSide_stack[0].data_histo.GetMaximum()
  drawNMStacks(1,1,[cosPhiMetJet_stack], subdir+prefix+"cosPhiMetJet", False)
  drawNMStacks(1,1,[FWMT1_stack],             subdir+prefix+"FWMT1", False)
  drawNMStacks(1,1,[FWMT2_stack],             subdir+prefix+"FWMT2", False)
  drawNMStacks(1,1,[FWMT3_stack],             subdir+prefix+"FWMT3", False)
  drawNMStacks(1,1,[FWMT4_stack],             subdir+prefix+"FWMT4", False)
  drawNMStacks(1,1,[c2D_stack],             subdir+prefix+"c2D", False)
  drawNMStacks(1,1,[linC2D_stack],             subdir+prefix+"linC2D", False)
  drawNMStacks(1,1,[thrust_stack],             subdir+prefix+"thrust", False)
  drawNMStacks(1,1,[htThrustLepSide_stack],             subdir+prefix+"htThrustLepSide", False)
  drawNMStacks(1,1,[sTlep_stack],             subdir+prefix+"sTlep", False)
  drawNMStacks(1,1,[cosDeltaPhiLepW_stack],             subdir+prefix+"cosDeltaPhiLepW", False)
  drawNMStacks(1,1,[cosDeltaPhiLepMET_stack],             subdir+prefix+"cosDeltaPhiLepMET", False)
if doSoftIsolatedVars:
  drawNMStacks(1,1,[softIsolatedMuPhi_stack],            subdir+prefix+"softIsolatedMuPhi", False)
  drawNMStacks(1,1,[softIsolatedMuRelIso_stack],            subdir+prefix+"softIsolatedMuRelIso", False)
  drawNMStacks(1,1,[softIsolatedMuAbsIso_stack],            subdir+prefix+"softIsolatedMuAbsIso", False)
  drawNMStacks(1,1,[softIsolatedMuDxy_stack],            subdir+prefix+"softIsolatedMuDxy", False)
  drawNMStacks(1,1,[softIsolatedMuDz_stack],            subdir+prefix+"softIsolatedMuDz", False)
  drawNMStacks(1,1,[softIsolatedMuNormChi2_stack                       ]   , subdir+prefix+"softIsolatedMuNormChi2", False)
  drawNMStacks(1,1,[softIsolatedMuNValMuonHits_stack                   ]   , subdir+prefix+"softIsolatedMuNValMuonHits", False)
  softIsolatedMuNumMatchedStations_stack[0].maximum = 10**4 *softIsolatedMuNumMatchedStations_stack[0].data_histo.GetMaximum()
  drawNMStacks(1,1,[softIsolatedMuNumMatchedStations_stack             ]   , subdir+prefix+"softIsolatedMuNumMatchedStations", False)
  drawNMStacks(1,1,[softIsolatedMuPixelHits_stack                      ]   , subdir+prefix+"softIsolatedMuPixelHits", False)
  drawNMStacks(1,1,[softIsolatedMuPixelHits_lowDz_stack                      ]   , subdir+prefix+"softIsolatedMuPixelHits_lowDz", False)
  drawNMStacks(1,1,[softIsolatedMuPixelHits_highDz_stack                      ]   , subdir+prefix+"softIsolatedMuPixelHits_highDz", False)
  softIsolatedMuNumtrackerLayerWithMeasurement_stack[0].maximum = 10**4 *softIsolatedMuNumtrackerLayerWithMeasurement_stack[0].data_histo.GetMaximum()
  drawNMStacks(1,1,[softIsolatedMuNumtrackerLayerWithMeasurement_stack ]   , subdir+prefix+"softIsolatedMuNumtrackerLayerWithMeasurement", False)
  softIsolatedMuIsGlobal_stack[0].maximum = 10**4 *softIsolatedMuIsGlobal_stack[0].data_histo.GetMaximum()
  drawNMStacks(1,1,[softIsolatedMuIsGlobal_stack                       ]   , subdir+prefix+"softIsolatedMuIsGlobal", False)
  softIsolatedMuIsTracker_stack[0].maximum = 10**4 *softIsolatedMuIsTracker_stack[0].data_histo.GetMaximum()
  drawNMStacks(1,1,[softIsolatedMuIsTracker_stack                       ]   , subdir+prefix+"softIsolatedMuIsTracker", False)
  drawNMStacks(1,1,[softIsolatedMuDz_stack],            subdir+prefix+"softIsolatedMuDz", False)
  drawNMStacks(1,1,[softIsolatedMuDz_zoomed_stack],            subdir+prefix+"softIsolatedMuDz_zoomed", False)
  drawNMStacks(1,1,[softIsolatedMuDz_noPixelHits_stack],            subdir+prefix+"softIsolatedMuDz_noPixelHits", False)
  drawNMStacks(1,1,[softIsolatedMuDz_onePixelHit_stack],            subdir+prefix+"softIsolatedMuDz_onePixelHit", False)
  drawNMStacks(1,1,[softIsolatedMuDz_twoPixelHits_stack],            subdir+prefix+"softIsolatedMuDz_twoPixelHits", False)
if doISRJetVars:
  drawNMStacks(1,1,[isrJetPhi_stack],             subdir+prefix+"isrJetPhi", False)
  drawNMStacks(1,1,[isrJetBtag_stack],            subdir+prefix+"isrJetBtag", False)
  drawNMStacks(1,1,[isrJetChef_stack],            subdir+prefix+"isrJetChef", False)
  drawNMStacks(1,1,[isrJetNhef_stack],            subdir+prefix+"isrJetNhef", False)
  drawNMStacks(1,1,[isrJetCeef_stack],            subdir+prefix+"isrJetCeef", False)
  drawNMStacks(1,1,[isrJetNeef_stack],            subdir+prefix+"isrJetNeef", False)
  drawNMStacks(1,1,[isrJetHFhef_stack],           subdir+prefix+"isrJetHFhef", False)
  drawNMStacks(1,1,[isrJetHFeef_stack],           subdir+prefix+"isrJetHFeef", False)
  drawNMStacks(1,1,[isrJetMuef_stack],            subdir+prefix+"isrJetMuef", False)
  drawNMStacks(1,1,[isrJetElef_stack],            subdir+prefix+"isrJetElef", False)
  drawNMStacks(1,1,[isrJetPhef_stack],            subdir+prefix+"isrJetPhef", False)
if doOtherVars:
  drawNMStacks(1,1,[ngoodVertices_stack],             subdir+prefix+"ngoodVertices", False)
  drawNMStacks(1,1,[type1phiMetphi_stack],             subdir+prefix+"type1phiMetphi", False)
  drawNMStacks(1,1,[njetWOjetCut_stack],             subdir+prefix+"njetWOJetCut", False)



#  drawNMStacks(1,1,[isrJetFull53XPUJetIDTight_stack], subdir+prefix+"isrJetFull53XPUJetIDTight", False)
#  drawNMStacks(1,1,[isrJetFull53XPUJetIDMedium_stack], subdir+prefix+"isrJetFull53XPUJetIDMedium", False)
#  drawNMStacks(1,1,[isrJetFull53XPUJetIDLoose_stack], subdir+prefix+"isrJetFull53XPUJetIDLoose", False)
#  
#  drawNMStacks(1,1,[isrJetMET53XPUJetIDTight_stack], subdir+prefix+"isrJetMET53XPUJetIDTight", False)
#  drawNMStacks(1,1,[isrJetMET53XPUJetIDMedium_stack], subdir+prefix+"isrJetMET53XPUJetIDMedium", False)
#  drawNMStacks(1,1,[isrJetMET53XPUJetIDLoose_stack], subdir+prefix+"isrJetMET53XPUJetIDLoose", False)
#  
#  drawNMStacks(1,1,[isrJetCutBasedPUJetIDTight_stack], subdir+prefix+"isrJetCutBasedPUJetIDTight", False)
#  drawNMStacks(1,1,[isrJetCutBasedPUJetIDMedium_stack], subdir+prefix+"isrJetCutBasedPUJetIDMedium", False)
#  drawNMStacks(1,1,[isrJetCutBasedPUJetIDLoose_stack], subdir+prefix+"isrJetCutBasedPUJetIDLoose", False)
#  
#  drawNMStacks(1,1,[isrJetFull53XPUJetIDTightVetoed_softIsolatedMuDz_stack], subdir+prefix+"isrJetFull53XPUJetIDTightVetoed_softIsolatedMuDz", False)
#  drawNMStacks(1,1,[isrJetFull53XPUJetIDMediumVetoed_softIsolatedMuDz_stack], subdir+prefix+"isrJetFull53XPUJetIDMediumVetoed_softIsolatedMuDz", False)
#  drawNMStacks(1,1,[isrJetFull53XPUJetIDLooseVetoed_softIsolatedMuDz_stack], subdir+prefix+"isrJetFull53XPUJetIDLooseVetoed_softIsolatedMuDz", False)
#  
#  drawNMStacks(1,1,[isrJetMET53XPUJetIDTightVetoed_softIsolatedMuDz_stack], subdir+prefix+"isrJetMET53XPUJetIDTightVetoed_softIsolatedMuDz", False)
#  drawNMStacks(1,1,[isrJetMET53XPUJetIDMediumVetoed_softIsolatedMuDz_stack], subdir+prefix+"isrJetMET53XPUJetIDMediumVetoed_softIsolatedMuDz", False)
#  drawNMStacks(1,1,[isrJetMET53XPUJetIDLooseVetoed_softIsolatedMuDz_stack], subdir+prefix+"isrJetMET53XPUJetIDLooseVetoed_softIsolatedMuDz", False)
#  
#  drawNMStacks(1,1,[isrJetCutBasedPUJetIDTightVetoed_softIsolatedMuDz_stack], subdir+prefix+"isrJetCutBasedPUJetIDTightVetoed_softIsolatedMuDz", False)
#  drawNMStacks(1,1,[isrJetCutBasedPUJetIDMediumVetoed_softIsolatedMuDz_stack], subdir+prefix+"isrJetCutBasedPUJetIDMediumVetoed_softIsolatedMuDz", False)
#  drawNMStacks(1,1,[isrJetCutBasedPUJetIDLooseVetoed_softIsolatedMuDz_stack], subdir+prefix+"isrJetCutBasedPUJetIDLooseVetoed_softIsolatedMuDz", False)
#  
#  
#  drawNMStacks(1,1,[isrJetFull53XPUJetIDTightPassed_softIsolatedMuDz_stack], subdir+prefix+"isrJetFull53XPUJetIDTightPassed_softIsolatedMuDz", False)
#  drawNMStacks(1,1,[isrJetFull53XPUJetIDMediumPassed_softIsolatedMuDz_stack], subdir+prefix+"isrJetFull53XPUJetIDMediumPassed_softIsolatedMuDz", False)
#  drawNMStacks(1,1,[isrJetFull53XPUJetIDLoosePassed_softIsolatedMuDz_stack], subdir+prefix+"isrJetFull53XPUJetIDLoosePassed_softIsolatedMuDz", False)
#  
#  drawNMStacks(1,1,[isrJetMET53XPUJetIDTightPassed_softIsolatedMuDz_stack], subdir+prefix+"isrJetMET53XPUJetIDTightPassed_softIsolatedMuDz", False)
#  drawNMStacks(1,1,[isrJetMET53XPUJetIDMediumPassed_softIsolatedMuDz_stack], subdir+prefix+"isrJetMET53XPUJetIDMediumPassed_softIsolatedMuDz", False)
#  drawNMStacks(1,1,[isrJetMET53XPUJetIDLoosePassed_softIsolatedMuDz_stack], subdir+prefix+"isrJetMET53XPUJetIDLoosePassed_softIsolatedMuDz", False)
#  
#  drawNMStacks(1,1,[isrJetCutBasedPUJetIDTightPassed_softIsolatedMuDz_stack], subdir+prefix+"isrJetCutBasedPUJetIDTightPassed_softIsolatedMuDz", False)
#  drawNMStacks(1,1,[isrJetCutBasedPUJetIDMediumPassed_softIsolatedMuDz_stack], subdir+prefix+"isrJetCutBasedPUJetIDMediumPassed_softIsolatedMuDz", False)
#  drawNMStacks(1,1,[isrJetCutBasedPUJetIDLoosePassed_softIsolatedMuDz_stack], subdir+prefix+"isrJetCutBasedPUJetIDLoosePassed_softIsolatedMuDz", False)
