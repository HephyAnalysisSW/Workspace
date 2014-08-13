import ROOT
from array import array
from math import *
import os, copy, sys

ROOT.TH1F().SetDefaultSumw2()

from Workspace.HEPHYPythonTools.helpers import getObjFromFile, passPUJetID, getISRweight, minDeltaRLeptonJets

from Workspace.RA4Analysis.simplePlotsCommon import *
#from monoJetFuncs import *
#from monoJetEventShapeVars import circularity2D, foxWolframMoments, thrust

from Workspace.HEPHYPythonTools.xsec import xsec
from Workspace.HEPHYPythonTools.xsecSMS import gluino8TeV_NLONLL, gluino13TeV_NLONLL
small = False

targetLumi = 19700.

from defaultConvertedTuples import * 

wjetsSample = wJetsHT150v2 
allSamples = [data, dy, ttJetsPowHeg, wjetsSample, singleTop, vv, qcd]

allVars=[]
allStacks=[]

## plots for studying preselection 
minimum=10**(-2.5)

chmode = "copy"
presel = "refSel"
ver = "v5"
region = "signal6j"
scaleTo13TeV = True
preprefixes=[]
if scaleTo13TeV:
  preprefixes.append("scaleTo13TeV")
preprefixes += [region, ver]

preprefix="_".join(preprefixes)
if region == "preSel":
  #isrjet>350, met>250, mT<70
  additionalCut = "(1)"
  addData = True
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "signal":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>750&&type1phiMet>350&&njets>=4)"
  addData = False
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "signal34jht500-750":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>400&&ht<600&&type1phiMet>350&&njets>=3&&njets<=4)"
  addData = True
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "signal5jht400-750":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>400&&ht<750&&type1phiMet>350&&njets>=5)"
  addData = False
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "signal2j":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>750&&type1phiMet>350&&njets==2)"
  addData = True 
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "signal23j":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>750&&type1phiMet>350&&njets>=2&&njets<=3)"
  addData = True 
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "refSel2j":
  #isrjet>350, met>250, mT<70
  additionalCut = "(njets==2)"
  addData = True 
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "signal3j":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>750&&type1phiMet>350&&njets==3)"
  addData = True
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "signal4j":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>750&&type1phiMet>350&&njets==4)"
  addData = False
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "signal5j":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>750&&type1phiMet>350&&njets>=5)"
  addData = False
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "signal6j":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>750&&type1phiMet>350&&njets>=6)"
  addData = False
  addSignals = True
  normalizeToData = False
  normalizeSignalToMCSum = False

subdir = "/pngT5Full/"
doAnalysisVars            = True 
doAllDiscriminatingVars   = False  
doOtherVars               = False  
doMTPlots                 = False

chainstring = "Events"
commoncf = "(0)"
prefix="empty_"
if presel == "refSel":
  commoncf="type1phiMet>150&&njets>=4&&ht>400&&nTightMuons+nTightElectrons==1&&nbtags==0"
if presel == "refSelNoNJet":
  commoncf="type1phiMet>150&&ht>400&&nTightMuons+nTightElectrons==1&&nbtags==0"
if presel == "refSelTauNoNJet":
  commoncf="type1phiMet>150&&ht>400&&nTightMuons+nTightElectrons==1&&nbtags==0&&Sum$(taPt>20)==0"

if additionalCut!="":
  commoncf+="&&"+additionalCut

prefix = "T5Full_"+preprefix+"_"+presel+"_"+chmode+"_"
T5Full_1100_200_100['color'] = ROOT.kBlue + 3
T5Full_1100_800_600['color'] = ROOT.kRed + 3

signals=[T5Full_1100_200_100, T5Full_1100_800_600]
for s in [T5Full_1100_200_100, T5Full_1100_800_600]:
  s['kFac13TeV'] = gluino13TeV_NLONLL[1100]/gluino8TeV_NLONLL[1100]
if addSignals:
  allSamples += signals
for sample in allSamples:
  sample["Chain"] = chainstring
  sample["dirname"] = "/data/schoef/convertedTuples_v22/"+chmode+"/"
for sample in allSamples[1:]:
#  sample["weight"] = "puWeight"
  sample["weight"] = "weight"

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
  MC_STOP.add                  = [MC_Z]
  MC_STOP.color                = ROOT.kOrange + 4
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

  if scaleTo13TeV:
    MC_TTJETS.scale = 3.31
    MC_WJETS.scale  = 1.663
    MC_Z.scale      = 1.65
    MC_STOP.scale   = 2.
    MC_VV.scale     = 2.
    MC_QCD.scale    = 2.

  res = [MC_WJETS, MC_TTJETS, MC_STOP, MC_Z, MC_VV, MC_QCD]
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
    if scaleTo13TeV:
      MC_SIGNAL.scale = signal['kFac13TeV'] 
    res.append(MC_SIGNAL)
    if normalizeSignalToMCSum:
      MC_SIGNAL.normalizeTo = res[0]
 
  getLinesForStack(res, targetLumi)
  nhistos = len(res)
  if addData:
    res.append(DATA)
    res[0].dataMCRatio = [DATA, res[0]]
#  else:
#    res[0].dataMCRatio = [MC_SIGNAL, res[0]]
#    res[0].ratioVarName = "SUS/SM" 
  if varfunc!="":
    for var in res:
      var.varfunc = varfunc
  return res

def cosDeltaPhiLepW(chain):
  lPt = getVarValue(chain, "leptonPt")
  lPhi = getVarValue(chain, "leptonPhi")
  metphi = getVarValue(chain, "type1phiMetphi")
  met = getVarValue(chain, "type1phiMet")
  cosLepPhi = cos(lPhi)
  sinLepPhi = sin(lPhi)
  mpx = met*cos(metphi)
  mpy = met*sin(metphi)
  pW = sqrt((lPt*cosLepPhi + mpx)**2 + (lPt*sinLepPhi + mpy)**2)

  return ((lPt*cosLepPhi + mpx)*cosLepPhi + (lPt*sinLepPhi + mpy)*sinLepPhi )/pW

#def dHtOrth(c):
#  htf=0.
#  for i in range(c.njetCount):
#    htf+=c.jetPt[i]*abs(cos(c.type1phiMetphi+pi/2.-c.jetPhi[i]))
#  return htf/c.ht

if doAnalysisVars:
#  dHtOrth_stack = getStack(":xxx;dHtOrth;Number of Events",[25,0,1], commoncf, signals, varfunc = dHtOrth, addData = addData)
#  dHtOrth_stack[0].addOverFlowBin = "upper"
#  allStacks.append(dHtOrth_stack)

#  njetsNoNJetCut_stack = getStack(":njets;n_{jet};Number of Events",[10,0,10], commoncf.replace('&&njets>=4',''), signals, addData = addData)
#  njetsNoNJetCut_stack[0].addOverFlowBin = "upper"
#  allStacks.append(njetsNoNJetCut_stack)

#  cosPhiLepJet0_stack = getStack(":xxx;cosPhiLepJet0;Number of Events",[25,-1,1], commoncf, signals, varfunc = lambda c:cos(c.leptonPhi - c.jetPhi[0]), addData = addData)
#  cosPhiLepJet0_stack[0].addOverFlowBin = "upper"
#  allStacks.append(cosPhiLepJet0_stack)
#  cosPhiLepJet1_stack = getStack(":xxx;cosPhiLepJet1;Number of Events",[25,-1,1], commoncf, signals, varfunc = lambda c:cos(c.leptonPhi - c.jetPhi[1]), addData = addData)
#  cosPhiLepJet1_stack[0].addOverFlowBin = "upper"
#  allStacks.append(cosPhiLepJet1_stack)
#  cosPhiMETJet0_stack = getStack(":xxx;cosPhiMETJet0;Number of Events",[25,-1,1], commoncf, signals, varfunc = lambda c:cos(c.type1phiMetphi - c.jetPhi[0]), addData = addData)
#  cosPhiMETJet0_stack[0].addOverFlowBin = "upper"
#  allStacks.append(cosPhiMETJet0_stack)
#  cosPhiMETJet1_stack = getStack(":xxx;cosPhiMETJet1;Number of Events",[25,-1,1], commoncf, signals, varfunc = lambda c:cos(c.type1phiMetphi - c.jetPhi[1]), addData = addData)
#  cosPhiMETJet1_stack[0].addOverFlowBin = "upper"
#  allStacks.append(cosPhiMETJet1_stack)
#
#  htThrustLepSideRatio_stack = getStack(":htThrustLepSideRatio;htThrustLepSideRatio;Number of Events",[25,0,1], commoncf, signals, addData = addData)
#  htThrustLepSideRatio_stack[0].addOverFlowBin = "upper"
#  allStacks.append(htThrustLepSideRatio_stack)
#
#  htThrustMetSideRatio_stack = getStack(":htThrustMetSideRatio;htThrustMetSideRatio;Number of Events",[25,0,1], commoncf, signals, addData = addData)
#  htThrustMetSideRatio_stack[0].addOverFlowBin = "upper"
#  allStacks.append(htThrustMetSideRatio_stack)
#
#  htThrustWSideRatio_stack = getStack(":htThrustWSideRatio;htThrustWSideRatio;Number of Events",[25,0,1], commoncf, signals, addData = addData)
#  htThrustWSideRatio_stack[0].addOverFlowBin = "upper"
#  allStacks.append(htThrustWSideRatio_stack)
#
  mT_stack  = getStack(":mT;m_{T} (GeV);Number of Events / 10 GeV",[41,0,410], commoncf, signals, addData = addData)
  mT_stack[0].addOverFlowBin = "upper"
  allStacks.append(mT_stack)

  mTCoarse_stack  = getStack(":mT;m_{T} (GeV);Number of Events / 100 GeV",[10,20,1020], commoncf, signals, addData = addData)
  mTCoarse_stack[0].addOverFlowBin = "upper"
  allStacks.append(mTCoarse_stack)

  met_stack = getStack(":type1phiMet;#slash{E}_{T} (GeV);Number of Events / 50 GeV",[18,150,1050], commoncf, signals, addData = addData)
  met_stack[0].addOverFlowBin = "upper"
  allStacks.append(met_stack)

  metphi_stack = getStack(":type1phiMetphi;#slash{E}_{T} (GeV);Number of Events / 50 GeV",[18,-pi,pi], commoncf, signals, addData = addData)
  metphi_stack[0].addOverFlowBin = "upper"
  allStacks.append(metphi_stack)

  metNoMET_stack = getStack(":type1phiMet;#slash{E}_{T} (GeV);Number of Events / 50 GeV",[18,150,1050], commoncf.replace('type1phiMet>350&&',''), signals, addData = addData)
  metNoMET_stack[0].addOverFlowBin = "upper"
  allStacks.append(metNoMET_stack)

  njets_stack = getStack(":njets;n_{jet};Number of Events",[15,0,15], commoncf, signals, addData = addData)
  njets_stack[0].addOverFlowBin = "upper"
  allStacks.append(njets_stack)

  njetsNoNJet_stack = getStack(":njets;n_{jet};Number of Events",[15,0,15], commoncf.replace('&&njets>=4','').replace('&&njets>=5','').replace('&&njets>=6',''), signals, addData = addData)
  njetsNoNJet_stack[0].addOverFlowBin = "upper"
  allStacks.append(njetsNoNJet_stack)

  nbtags_stack = getStack(":nbtags;n_{b-tags};Number of Events",[10,0,10], commoncf, signals, addData = addData)
  nbtags_stack[0].addOverFlowBin = "upper"
  allStacks.append(nbtags_stack)

  ht_stack                          = getStack(":ht;H_{T} (GeV);Number of Events / 100 GeV",[31,0,2600 ], commoncf, signals, addData = addData)
  ht_stack[0].addOverFlowBin = "upper"
  allStacks.append(ht_stack)

  htNoHT_stack                          = getStack(":ht;H_{T} (GeV);Number of Events / 100 GeV",[26,0,2600 ], commoncf.replace('ht>750&&','').replace('ht>400&&',''), signals, addData = addData)
  htNoHT_stack[0].addOverFlowBin = "upper"
  allStacks.append(htNoHT_stack)


if doAllDiscriminatingVars:

#  cosPhiMetJet_stack = getStack(":xxx;cos(#phi(#slash{E}_{T}, ISR-jet));Number of Events",[20,-1,1], commoncf, signals, addData = addData, varfunc = lambda c: cos(getVarValue(c, 'isrJetPhi') - getVarValue(c, 'leptonPhi')))
#  cosPhiMetJet_stack[0].addOverFlowBin = "both"
#  allStacks.append(cosPhiMetJet_stack)

  FWMT1_stack = getStack(":FWMT1;FMWT1 (jets,lep,MET);Number of Events",[20,0,1], commoncf, signals, addData = addData)
  FWMT1_stack[0].addOverFlowBin = "upper"
  allStacks.append(FWMT1_stack)

  FWMT2_stack = getStack(":FWMT2;FMWT2 (jets,lep,MET);Number of Events",[20,0,1], commoncf, signals, addData = addData)
  FWMT2_stack[0].addOverFlowBin = "upper"
  allStacks.append(FWMT2_stack)

  FWMT3_stack = getStack(":FWMT3;FMWT3 (jets,lep,MET);Number of Events",[20,0,1], commoncf, signals, addData = addData)
  FWMT3_stack[0].addOverFlowBin = "upper"
  allStacks.append(FWMT3_stack)

  FWMT4_stack = getStack(":FWMT4;FMWT4 (jets,lep,MET);Number of Events",[20,0,1], commoncf, signals, addData = addData)
  FWMT4_stack[0].addOverFlowBin = "upper"
  allStacks.append(FWMT4_stack)


  c2D_stack = getStack(":C2D;C2D (jets,lep,MET);Number of Events",[20,0,1], commoncf, signals, addData = addData)
  c2D_stack[0].addOverFlowBin = "upper"
  allStacks.append(c2D_stack)

  linC2D_stack = getStack(":linC2D;linC2D (jets,lep,MET);Number of Events",[20,0,1], commoncf, signals, addData = addData)
  linC2D_stack[0].addOverFlowBin = "upper"
  allStacks.append(linC2D_stack)

  thrust_stack = getStack(":thrust;thrust;Number of Events",[20,0.6,1], commoncf, signals, addData = addData)
  thrust_stack[0].addOverFlowBin = "upper"
  allStacks.append(thrust_stack)

#  sTlep_stack  = getStack(":XXX;S_{T, lep.} (GeV);Number of Events / 50 GeV",[21,0,1050], commoncf, signals, lambda c: c.GetLeaf('leptonPt').GetValue() + c.GetLeaf('type1phiMet').GetValue() , addData = addData)
#  sTlep_stack[0].addOverFlowBin = "upper"
#  allStacks.append(sTlep_stack)

  cosDeltaPhiLepMET_stack  = getStack(":xxx;cos(#Delta #phi(l, #slash{E}_{T}));Number of Events",[22,-1.1,1.1], commoncf, signals, lambda c: cos(c.GetLeaf('leptonPhi').GetValue() - c.GetLeaf('type1phiMetphi').GetValue()), addData = addData)
  allStacks.append(cosDeltaPhiLepMET_stack)

  cosDeltaPhiLepW_stack  = getStack(":cosDeltaPhi;cos(#Delta #phi(l, W));Number of Events",[22,-1.1,1.1], commoncf, signals, addData = addData)
  allStacks.append(cosDeltaPhiLepW_stack)

if doMTPlots:
  mTReco_PosCharge_stack  = getStack(":mT;m_{T} (GeV);Number of Events / 100 GeV",[8,20,820], commoncf+"&&leptonPdg<0", signals, addData = addData)
  mTReco_PosCharge_stack[0].addOverFlowBin = "upper"
  allStacks.append(mTReco_PosCharge_stack)
  mTReco_NegCharge_stack  = getStack(":mT;m_{T} (GeV);Number of Events / 100 GeV",[8,20,820], commoncf+"&&leptonPdg>0", signals, addData = addData)
  mTReco_NegCharge_stack[0].addOverFlowBin = "upper"
  allStacks.append(mTReco_NegCharge_stack)
  mTReco_stack  = getStack(":mT;m_{T} (GeV);Number of Events / 100 GeV",[8,20,820], commoncf, signals, addData = addData)
  mTReco_stack[0].addOverFlowBin = "upper"
  allStacks.append(mTReco_stack)

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
    stack[0].maximum = 2*10**2 *stack[0].data_histo.GetMaximum()
  stack[0].logy = True
  stack[0].minimum = minimum
#  stack[0].legendCoordinates=[0.76,0.95 - 0.3,.98,.95]
#  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS preliminary}"], [0.2,0.85,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 7 TeV"]]
  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS Collaboration}"], [0.2,0.85,str(int(round(targetLumi/10.))/100.)+" fb^{-1},  #sqrt{s} = 8 TeV"]]

if doAnalysisVars:
#  drawNMStacks(1,1,[njetsNoNJetCut_stack],             subdir+prefix+"njetsNoNJetCut", False)

#  drawNMStacks(1,1,[cosPhiLepJet0_stack],             subdir+prefix+"cosPhiLepJet0", False)
#  drawNMStacks(1,1,[cosPhiLepJet1_stack],             subdir+prefix+"cosPhiLepJet1", False)
#  drawNMStacks(1,1,[cosPhiMETJet0_stack],             subdir+prefix+"cosPhiMETJet0", False)
#  drawNMStacks(1,1,[cosPhiMETJet1_stack],             subdir+prefix+"cosPhiMETJet1", False)
#  htThrustMetSideRatio_stack[0].maximum = 6*10**5 *htThrustMetSideRatio_stack[0].data_histo.GetMaximum()
#  drawNMStacks(1,1,[htThrustMetSideRatio_stack],             subdir+prefix+"htThrustMetSideRatio", False)
##  drawNMStacks(1,1,[dHtOrth_stack],             subdir+prefix+"dHtOrth", False)
#  htThrustLepSideRatio_stack[0].maximum = 6*10**5 *htThrustLepSideRatio_stack[0].data_histo.GetMaximum()
#  drawNMStacks(1,1,[htThrustLepSideRatio_stack],             subdir+prefix+"htThrustLepSideRatio", False)
#  htThrustWSideRatio_stack[0].maximum = 6*10**5 *htThrustWSideRatio_stack[0].data_histo.GetMaximum()
#  drawNMStacks(1,1,[htThrustWSideRatio_stack],             subdir+prefix+"htThrustWSideRatio", False)
  drawNMStacks(1,1,[mT_stack],              subdir+prefix+"mT", False)
  drawNMStacks(1,1,[mTCoarse_stack],              subdir+prefix+"mTCoarse", False)

  drawNMStacks(1,1,[met_stack],             subdir+prefix+"met", False)
  drawNMStacks(1,1,[metphi_stack],             subdir+prefix+"metphi", False)
  drawNMStacks(1,1,[metNoMET_stack],             subdir+prefix+"metNoMET", False)
  drawNMStacks(1,1,[njets_stack],             subdir+prefix+"njets", False)
  drawNMStacks(1,1,[njetsNoNJet_stack],             subdir+prefix+"njetsNoNJet", False)
  drawNMStacks(1,1,[nbtags_stack],             subdir+prefix+"nbtags", False)
  drawNMStacks(1,1,[ht_stack],              subdir+prefix+"ht", False)
  drawNMStacks(1,1,[htNoHT_stack],             subdir+prefix+"htNoHT", False)
if doAllDiscriminatingVars:
#  drawNMStacks(1,1,[closestMuJetMass_stack] ,             subdir+prefix+"closestMuJetMass_stack", False)
#  drawNMStacks(1,1,[closestMuJetDeltaR_stack] ,        subdir+prefix+"closestMuJetDeltaR_stack", False)
#  drawNMStacks(1,1,[closestMuJetDeltaR_zoomed_stack] ,        subdir+prefix+"closestMuJetDeltaR_zoomed_stack", False)
  FWMT2_stack[0].maximum = 6*10**4 *FWMT2_stack[0].data_histo.GetMaximum()
  FWMT3_stack[0].maximum = 6*10**3 *FWMT3_stack[0].data_histo.GetMaximum()
  FWMT4_stack[0].maximum = 6*10**4 *FWMT4_stack[0].data_histo.GetMaximum()
#  cosPhiMetJet_stack[0].maximum = 6*10**3 *cosPhiMetJet_stack[0].data_histo.GetMaximum()
#  thrust_stack[0].maximum = 6*10**4 *thrust_stack[0].data_histo.GetMaximum()
#  drawNMStacks(1,1,[cosPhiMetJet_stack], subdir+prefix+"cosPhiMetJet", False)
  drawNMStacks(1,1,[FWMT1_stack],             subdir+prefix+"FWMT1", False)
  drawNMStacks(1,1,[FWMT2_stack],             subdir+prefix+"FWMT2", False)
  drawNMStacks(1,1,[FWMT3_stack],             subdir+prefix+"FWMT3", False)
  drawNMStacks(1,1,[FWMT4_stack],             subdir+prefix+"FWMT4", False)
  drawNMStacks(1,1,[c2D_stack],             subdir+prefix+"c2D", False)
  drawNMStacks(1,1,[linC2D_stack],             subdir+prefix+"linC2D", False)
  drawNMStacks(1,1,[thrust_stack],             subdir+prefix+"thrust", False)
#  drawNMStacks(1,1,[sTlep_stack],             subdir+prefix+"sTlep", False)
  drawNMStacks(1,1,[cosDeltaPhiLepW_stack],             subdir+prefix+"cosDeltaPhiLepW", False)
  drawNMStacks(1,1,[cosDeltaPhiLepMET_stack],             subdir+prefix+"cosDeltaPhiLepMET", False)

if doMTPlots:
  drawNMStacks(1,1,[mTReco_PosCharge_stack], subdir+prefix+"mTReco_PosCharge", False)
  drawNMStacks(1,1,[mTReco_NegCharge_stack], subdir+prefix+"mTReco_NegCharge", False)
  drawNMStacks(1,1,[mTReco_stack], subdir+prefix+"mTReco", False)
