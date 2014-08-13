import ROOT
from array import array
from math import *
import os, copy, sys
from helpers import wRecoPt
ROOT.TH1F().SetDefaultSumw2()

from Workspace.HEPHYPythonTools.helpers import getObjFromFile, passPUJetID, getISRweight, minDeltaRLeptonJets

from Workspace.RA4Analysis.simplePlotsCommon import *
#from monoJetFuncs import *
#from monoJetEventShapeVars import circularity2D, foxWolframMoments, thrust

from Workspace.HEPHYPythonTools.xsec import xsec
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
presel = "refSelNoNJet"
ver = "v5"
region = "refSel-njetGr2"
preprefix = region+"_"+ver
if region == "preSel":
  #isrjet>350, met>250, mT<70
  additionalCut = "(1)"
  addData = True
  addSignals = False
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "signal":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>750&&type1phiMet>350&&njets>=4)"
  addData = False
  addSignals = False
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "signal34jht500-750":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>400&&ht<600&&type1phiMet>350&&njets>=3&&njets<=4)"
  addData = True
  addSignals = False
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "signal5jht400-750":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>400&&ht<750&&type1phiMet>350&&njets>=5)"
  addData = False
  addSignals = False
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "signal2j":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>750&&type1phiMet>350&&njets==2)"
  addData = True 
  addSignals = False
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "signal23j":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>750&&type1phiMet>350&&njets>=2&&njets<=3)"
  addData = True 
  addSignals = False
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "refSel-njetGr2":
  #isrjet>350, met>250, mT<70
  additionalCut = "(njets>=2)"
  addData = True 
  addSignals = False
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "signal3j":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>750&&type1phiMet>350&&njets==3)"
  addData = True
  addSignals = False
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "signal4j":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>750&&type1phiMet>350&&njets==4)"
  addData = False
  addSignals = False
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "signal5j":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>750&&type1phiMet>350&&njets>=5)"
  addData = False
  addSignals = False
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "signalHTFLS04":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>750&&type1phiMet>350)&&htThrustLepSideRatio>0.4"
  addData = False
  addSignals = False
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "signalCosMLPhi":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>750&&type1phiMet>350)&&cos(leptonPhi-type1phiMetphi)<0.8"
  addData = False
  addSignals = False
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "signalCosMLPhi2j":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>750&&type1phiMet>350)&&cos(leptonPhi-type1phiMetphi)<0.8&&njets==2"
  addData = False
  addSignals = False
  normalizeToData = False
  normalizeSignalToMCSum = False
if region == "signalCosMLPhi3j":
  #isrjet>350, met>250, mT<70
  additionalCut = "(ht>750&&type1phiMet>350)&&cos(leptonPhi-type1phiMetphi)<0.8&&njets==3"
  addData = False
  addSignals = False
  normalizeToData = False
  normalizeSignalToMCSum = False

subdir = "/pngT5LNu/"

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

prefix = "T5Lnu_"+preprefix+"_"+presel+"_"+chmode+"_"

def getT5LNu(mgl, mn, color = ROOT.kBlue):
  res = {} 
  res["dirname"] = ["/data/schoef/convertedTuples_v22/copy/"]
  res["bins"] = ["T5LNu_"+str(mgl)+"_"+str(mn)]
  res["hasWeight"] = True
  res["weight"] = "weight"
  res["color"] = color
  res["name"] = res["bins"][0]
  return res


signals=[getT5LNu(1000,100, ROOT.kBlue + 3), getT5LNu(1000, 600, ROOT.kRed + 3)]
if addSignals:
  allSamples += signals

for sample in allSamples:
  sample["Chain"] = chainstring
  sample["dirname"] = "/data/schoef/convertedTuples_v22/"+chmode+"/"
for sample in allSamples[1:]:
  sample["weight"] = "puWeight"

def getStack(varstring, binning, cutstring, signals, varfunc = "", addData=True, additionalCutFunc = "", symmetrizeSignalCharge = False):
  DATA          = variable(varstring, binning, cutstring,additionalCutFunc=additionalCutFunc, binningIsExplicit = True)
  DATA.sample   = data
#  DATA.color    = ROOT.kGray
  DATA.color    = dataColor
  DATA.legendText="Data"

  MC_WJETS                     = variable(varstring, binning, cutstring, additionalCutFunc=additionalCutFunc, binningIsExplicit = True) 
  MC_WJETS.sample              = wjetsSample
  MC_TTJETS                    = variable(varstring, binning, cutstring, additionalCutFunc=additionalCutFunc, binningIsExplicit = True)
  MC_TTJETS.sample             = ttJetsPowHeg
  MC_STOP                      = variable(varstring, binning, cutstring, additionalCutFunc=additionalCutFunc, binningIsExplicit = True) 
  MC_STOP.sample               = singleTop
  MC_Z                         = variable(varstring, binning, cutstring, additionalCutFunc=additionalCutFunc, binningIsExplicit = True) 
  MC_Z.sample                  = dy
  MC_VV                        = variable(varstring, binning, cutstring, additionalCutFunc=additionalCutFunc, binningIsExplicit = True) 
  MC_VV.sample                 = vv
  MC_QCD                       = variable(varstring, binning, cutstring, additionalCutFunc=additionalCutFunc, binningIsExplicit = True)
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

  res = [MC_WJETS, MC_TTJETS, MC_STOP, MC_Z, MC_VV, MC_QCD]
  for v in res:
#    v.reweightVar = "ngoodVertices"
#    v.reweightHisto = simplePUreweightHisto 
    v.legendCoordinates=[0.61,0.95 - 0.08*5,.98,.95]
#  for signal in signals:
#    if symmetrizeSignalCharge:
#      MC_SIGNAL                    = variable(varstring, binning, cutstring.replace("&&leptonPdg<0","").replace("&&leptonPdg>0",""),additionalCutFunc=additionalCutFunc, binningIsExplicit=True)
#    else:
#      MC_SIGNAL                    = variable(varstring, binning, cutstring,additionalCutFunc=additionalCutFunc, binningIsExplicit=True)
#    MC_SIGNAL.sample             = copy.deepcopy(signal)
#    MC_SIGNAL.legendText         = signal["name"]
#    MC_SIGNAL.style              = "l02"
#    MC_SIGNAL.color              = signal['color']
#    if symmetrizeSignalCharge: 
#      MC_SIGNAL.scale              = 0.5
#    MC_SIGNAL.add = []
#    MC_SIGNAL.reweightVar = lambda c:getISRweight(c, mode='Central')
#    res.append(MC_SIGNAL)
#    if normalizeSignalToMCSum:
#      MC_SIGNAL.normalizeTo = res[0]
 
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


binning = range(0,700,100)+[800, 1200]

wRecoPt_stack = getStack(":XXX;p_{T,W} (GeV);Number of Events / 100 GeV",binning,  commoncf, signals, addData = addData, varfunc = wRecoPt)
wRecoPt_stack[0].addOverFlowBin = "upper"
allStacks.append(wRecoPt_stack)
wPosPdgRecoPt_stack = getStack(":XXX;p_{T,W} (GeV);Number of Events / 100 GeV",binning,  commoncf+"&&leptonPdg>0", signals, addData = addData, varfunc = wRecoPt)
wPosPdgRecoPt_stack[0].addOverFlowBin = "upper"
allStacks.append(wPosPdgRecoPt_stack)
wNegPdgRecoPt_stack = getStack(":XXX;p_{T,W} (GeV);Number of Events / 100 GeV",binning,  commoncf+"&&leptonPdg<0", signals, addData = addData, varfunc = wRecoPt)
wNegPdgRecoPt_stack[0].addOverFlowBin = "upper"
allStacks.append(wNegPdgRecoPt_stack)


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

drawNMStacks(1,1,[wRecoPt_stack],              subdir+prefix+"wRecoPt", False)
drawNMStacks(1,1,[wPosPdgRecoPt_stack],              subdir+prefix+"wPosPdgRecoPt", False)
drawNMStacks(1,1,[wNegPdgRecoPt_stack],              subdir+prefix+"wNegPdgRecoPt", False)
