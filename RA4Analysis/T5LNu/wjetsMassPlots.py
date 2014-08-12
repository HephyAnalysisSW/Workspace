import ROOT
from array import array
from math import *
import os, copy, sys
from helpers import wRecoPt, wGenPt
ROOT.TH1F().SetDefaultSumw2()

from Workspace.HEPHYPythonTools.helpers import getObjFromFile, passPUJetID, getISRweight, minDeltaRLeptonJets#, findClosestObjectDR, invMass 

from Workspace.RA4Analysis.simplePlotsCommon import *
#from monoJetFuncs import *
#from monoJetEventShapeVars import circularity2D, foxWolframMoments, thrust

from Workspace.HEPHYPythonTools.xsec import xsec
small = False

targetLumi = 19700.

from defaultConvertedTuples import * 

wjetsSample = wJetsHT150v2 
allSamples = [dy, ttJetsPowHeg, wjetsSample, singleTop, vv, qcd]

allVars=[]
allStacks=[]

## plots for studying preselection 
minimum=10**(-2.5)

chmode = "copy"
presel = "refSelNoNJet"
ver = "v5"
preprefix = ver
addData = False
addSignals = True
normalizeToData = False
normalizeSignalToMCSum = False

#if region == "signal3j":
#  #isrjet>350, met>250, mT<70
#  additionalCut = "(ht>750&&type1phiMet>350)"

subdir = "/pngT5LNu/"

chainstring = "Events"
commoncf = "(0)"
prefix="empty_"
if presel == "refSelNoNJet":
  commoncf="ht>400&&nTightMuons+nTightElectrons==1&&nbtags==0&&type1phiMet>150"

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

signals=[]
#signals=[getT5LNu(1000,100, ROOT.kBlue + 3), getT5LNu(1000, 600, ROOT.kRed + 3)]
#if addSignals:
#  allSamples += signals

for sample in allSamples:
  sample["Chain"] = chainstring
  sample["dirname"] = "/data/schoef/convertedTuples_v22/"+chmode+"/"
for sample in allSamples:
  sample["weight"] = "puWeight"

def getStack(varstring, binning, cutstring, signals, varfunc = None, addData=True, additionalCutFunc = "", onlyW = False, reweightFunc=None):
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

  res = [MC_WJETS, MC_TTJETS, MC_STOP, MC_Z, MC_VV, MC_QCD]
  if onlyW:
    MC_WJETS.add                 = []
    res = [MC_WJETS]
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
    res[0].dataMCRatio = [DATA, res[0]]
#  else:
#    res[0].dataMCRatio = [MC_SIGNAL, res[0]]
#    res[0].ratioVarName = "SUS/SM" 
  if varfunc:
    for var in res:
      var.varfunc = varfunc
  if reweightFunc:
    for var in res:
      var.reweightVar = reweightFunc
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

def wGenMass(c):
  res=[]
  for i in range(c.ngp):
    if abs(c.gpPdg[i])==24:
      res.append(c.gpM[i])
  if len(res)>0:
    return max(res)
  else:
    return float('nan') 


def wGenMT(c):
  for i in range(c.ngp):
    if abs(c.gpPdg[i])==24:
      pos = int(c.gpDa1[i])
      return sqrt(2.*c.gpPt[pos]*c.gpPt[pos+1]*(1-cos(c.gpPhi[pos] - c.gpPhi[pos+1]))) 
  return float('nan') 

def wGenMT(c):
  for i in range(c.ngp):
    if abs(c.gpPdg[i])==24:
      pos = int(c.gpDa1[i])
      return sqrt(2.*c.gpPt[pos]*c.gpPt[pos+1]*(1-cos(c.gpPhi[pos] - c.gpPhi[pos+1]))) 
  return float('nan') 

def getCut(var, bin):
  res= var+'>='+str(bin[0])
  if var=='njets':
    res+="&&"+var+"<="+str(bin[1])
  else:
    if bin[1]>0:
      res+="&&"+var+"<"+str(bin[1])
  return res
def getCutName(var, bin):
  res= var+str(bin[0])
  if bin[1]>0:
    res+="-"+str(bin[1])
  return res

def getNiceName(var, bin):
  res= str(bin[0]) + ' #leq ' + var
  if var=='njets':
    res+=" #leq "+str(bin[1])
  else:
    if bin[1]>0:
      res+=" < "+str(bin[1])
  return res

htBins =  [[400, 750], [500, 750], [750, -1]]
metBins = [[150, 350], [350, -1] ]
njetBins = [[2,2], [3,3], [4,4], [5,99]]
njetCRBins = [[2,2], [3,3], [4,4]]

#htBins =  [[750, -1]]
#metBins = [[350, -1] ]
#njetBins = [[2,2], [5,99]]
#njetCRBins = [[2,2]]
       
def getPTRWFunc(h, ptFunc):
  def rwf(c):
    return h.GetBinContent(h.FindBin(ptFunc(c)))
  return rwf

wGenMass_stacks={} 
wPlusGenMass_stacks={} 
wMinusGenMass_stacks={} 
wGenMT_stacks={} 
wPlusGenMT_stacks={} 
wMinusGenMT_stacks={} 
wGenMT_genPtRW_stacks={} 
wPlusGenMT_genPtRW_stacks={} 
wMinusGenMT_genPtRW_stacks={} 
wGenPt_genPtRW_stacks={} 
wPlusGenPt_genPtRW_stacks={} 
wMinusGenPt_genPtRW_stacks={} 
wRecoMT_stacks={} 
wPlusRecoMT_stacks={} 
wMinusRecoMT_stacks={} 
wRecoMT_recoPtRW_stacks={} 
wPlusRecoMT_recoPtRW_stacks={} 
wMinusRecoMT_recoPtRW_stacks={} 
wRecoPt_recoPtRW_stacks={} 
wPlusRecoPt_recoPtRW_stacks={} 
wMinusRecoPt_recoPtRW_stacks={} 
for metb in metBins:
  nameMetb=getCutName('met', metb)
  cutMetb=getCut('type1phiMet', metb)
  for htb in htBins:
    nameHTb = getCutName('ht', htb)
    cutHTb = getCut('ht', htb)
    for njetb in njetBins:
      nameNJetb =getCutName('njets', njetb)
      cutNJetb = getCut('njets', njetb)
      cut = '&&'.join([cutMetb, cutHTb, cutNJetb ])
      name = '_'.join([nameMetb, nameHTb, nameNJetb ])
      print name, cut
      thisCut = commoncf+"&&"+cut
      if njetb in njetCRBins:
        wGenMT_genPtRW_stacks[name] = getStack(":XXX;gen. m_{T} (GeV);Number of Events", binning, thisCut, signals, varfunc = wGenMT, addData = addData, onlyW = True, reweightFunc = getPTRWFunc(wGenPt_rwHisto[name], wGenPt))
        wGenMT_genPtRW_stacks[name][0].addOverFlowBin = "upper"
        allStacks.append(wGenMT_genPtRW_stacks[name])
        wPlusGenMT_genPtRW_stacks[name] = getStack(":XXX;gen. m_{T} (GeV);Number of Events", binning, thisCut+"&&Max$((abs(gpPdg)==24)*gpPdg)==24", signals, varfunc = wGenMT, addData = addData, onlyW = True, reweightFunc =  getPTRWFunc(wPlusGenPt_rwHisto[name], wGenPt))
        wPlusGenMT_genPtRW_stacks[name][0].addOverFlowBin = "upper"
        allStacks.append(wPlusGenMT_genPtRW_stacks[name])
        wMinusGenMT_genPtRW_stacks[name] = getStack(":XXX;gen. m_{T} (GeV);Number of Events", binning, thisCut+"&&Min$((abs(gpPdg)==24)*gpPdg)==-24", signals, varfunc = wGenMT, addData = addData, onlyW = True, reweightFunc =  getPTRWFunc(wMinusGenPt_rwHisto[name], wGenPt))
        wMinusGenMT_genPtRW_stacks[name][0].addOverFlowBin = "upper"
        allStacks.append(wMinusGenMT_genPtRW_stacks[name])

        wRecoMT_recoPtRW_stacks[name] = getStack(":mT;reco m_{T} (GeV);Number of Events", binning, thisCut, signals, addData = addData, onlyW = True, reweightFunc = getPTRWFunc(wRecoPt_rwHisto[name], wRecoPt))
        wRecoMT_recoPtRW_stacks[name][0].addOverFlowBin = "upper"
        allStacks.append(wRecoMT_recoPtRW_stacks[name])
        wPlusRecoMT_recoPtRW_stacks[name] = getStack(":mT;reco m_{T} (GeV);Number of Events", binning, thisCut+"&&Max$((abs(gpPdg)==24)*gpPdg)==24", signals, addData = addData, onlyW = True, reweightFunc =  getPTRWFunc(wPlusRecoPt_rwHisto[name], wRecoPt))
        wPlusRecoMT_recoPtRW_stacks[name][0].addOverFlowBin = "upper"
        allStacks.append(wPlusRecoMT_recoPtRW_stacks[name])
        wMinusRecoMT_recoPtRW_stacks[name] = getStack(":mT;reco m_{T} (GeV);Number of Events", binning, thisCut+"&&Min$((abs(gpPdg)==24)*gpPdg)==-24", signals, addData = addData, onlyW = True, reweightFunc =  getPTRWFunc(wMinusRecoPt_rwHisto[name], wRecoPt))
        wMinusRecoMT_recoPtRW_stacks[name][0].addOverFlowBin = "upper"
        allStacks.append(wMinusRecoMT_recoPtRW_stacks[name])

        wGenPt_genPtRW_stacks[name] = getStack(":XXX;gen. p_{T} (GeV);Number of Events", binningWPt, thisCut, signals, varfunc = wGenPt, addData = addData, onlyW = True, reweightFunc = getPTRWFunc(wGenPt_rwHisto[name], wGenPt))
        wGenPt_genPtRW_stacks[name][0].addOverFlowBin = "upper"
        allStacks.append(wGenPt_genPtRW_stacks[name])
        wPlusGenPt_genPtRW_stacks[name] = getStack(":XXX;gen. p_{T} (GeV);Number of Events", binningWPt, thisCut+"&&Max$((abs(gpPdg)==24)*gpPdg)==24", signals, varfunc = wGenPt, addData = addData, onlyW = True, reweightFunc = getPTRWFunc(wPlusGenPt_rwHisto[name], wGenPt))
        wPlusGenPt_genPtRW_stacks[name][0].addOverFlowBin = "upper"
        allStacks.append(wPlusGenPt_genPtRW_stacks[name])
        wMinusGenPt_genPtRW_stacks[name] = getStack(":XXX;gen. p_{T} (GeV);Number of Events", binningWPt, thisCut+"&&Min$((abs(gpPdg)==24)*gpPdg)==-24", signals, varfunc = wGenPt, addData = addData, onlyW = True, reweightFunc = getPTRWFunc(wMinusGenPt_rwHisto[name], wGenPt))
        wMinusGenPt_genPtRW_stacks[name][0].addOverFlowBin = "upper"
        allStacks.append(wMinusGenPt_genPtRW_stacks[name])

        wRecoPt_recoPtRW_stacks[name] = getStack(":XXX;reco p_{T} (GeV);Number of Events", binningWPt, thisCut, signals, varfunc = wRecoPt, addData = addData, onlyW = True, reweightFunc = getPTRWFunc(wRecoPt_rwHisto[name], wRecoPt))
        wRecoPt_recoPtRW_stacks[name][0].addOverFlowBin = "upper"
        allStacks.append(wRecoPt_recoPtRW_stacks[name])
        wPlusRecoPt_recoPtRW_stacks[name] = getStack(":XXX;reco p_{T} (GeV);Number of Events", binningWPt, thisCut+"&&Max$((abs(gpPdg)==24)*gpPdg)==24", signals, varfunc = wRecoPt, addData = addData, onlyW = True, reweightFunc = getPTRWFunc(wPlusRecoPt_rwHisto[name], wRecoPt))
        wPlusRecoPt_recoPtRW_stacks[name][0].addOverFlowBin = "upper"
        allStacks.append(wPlusRecoPt_recoPtRW_stacks[name])
        wMinusRecoPt_recoPtRW_stacks[name] = getStack(":XXX;reco p_{T} (GeV);Number of Events", binningWPt, thisCut+"&&Min$((abs(gpPdg)==24)*gpPdg)==-24", signals, varfunc = wRecoPt, addData = addData, onlyW = True, reweightFunc = getPTRWFunc(wMinusRecoPt_rwHisto[name], wRecoPt))
        wMinusRecoPt_recoPtRW_stacks[name][0].addOverFlowBin = "upper"
        allStacks.append(wMinusRecoPt_recoPtRW_stacks[name])

      wGenMT_stacks[name] = getStack(":XXX;gen. m_{T} (GeV);Number of Events", binning, thisCut, signals, varfunc = wGenMT, addData = addData, onlyW = True)
      wGenMT_stacks[name][0].addOverFlowBin = "upper"
      allStacks.append(wGenMT_stacks[name])
      wPlusGenMT_stacks[name] = getStack(":XXX;gen. m_{T} (GeV);Number of Events", binning, thisCut+"&&Max$((abs(gpPdg)==24)*gpPdg)==24", signals, varfunc = wGenMT, addData = addData, onlyW = True)
      wPlusGenMT_stacks[name][0].addOverFlowBin = "upper"
      allStacks.append(wPlusGenMT_stacks[name])
      wMinusGenMT_stacks[name] = getStack(":XXX;gen. m_{T} (GeV);Number of Events", binning, thisCut+"&&Min$((abs(gpPdg)==24)*gpPdg)==-24", signals, varfunc = wGenMT, addData = addData, onlyW = True)
      wMinusGenMT_stacks[name][0].addOverFlowBin = "upper"
      allStacks.append(wMinusGenMT_stacks[name])

      wRecoMT_stacks[name] = getStack(":mT;reco m_{T} (GeV);Number of Events", binning, thisCut, signals, addData = addData, onlyW = True)
      wRecoMT_stacks[name][0].addOverFlowBin = "upper"
      allStacks.append(wRecoMT_stacks[name])
      wPlusRecoMT_stacks[name] = getStack(":mT;reco m_{T} (GeV);Number of Events", binning, thisCut+"&&Max$((abs(gpPdg)==24)*gpPdg)==24", signals, addData = addData, onlyW = True)
      wPlusRecoMT_stacks[name][0].addOverFlowBin = "upper"
      allStacks.append(wPlusRecoMT_stacks[name])
      wMinusRecoMT_stacks[name] = getStack(":mT;reco m_{T} (GeV);Number of Events", binning, thisCut+"&&Min$((abs(gpPdg)==24)*gpPdg)==-24", signals, addData = addData, onlyW = True)
      wMinusRecoMT_stacks[name][0].addOverFlowBin = "upper"
      allStacks.append(wMinusRecoMT_stacks[name])

#      wGenMass_stacks[name] = getStack(":XXX;gen. m_{W} (GeV);Number of Events", binning, thisCut, signals, varfunc = wGenMass, addData = addData, onlyW = True)
#      wGenMass_stacks[name][0].addOverFlowBin = "upper"
#      allStacks.append(wGenMass_stacks[name])
#      wPlusGenMass_stacks[name] = getStack(":XXX;gen. m_{W} (GeV);Number of Events", binning, thisCut+"&&Max$((abs(gpPdg)==24)*gpPdg)==24", signals, varfunc = wGenMass, addData = addData, onlyW = True)
#      wPlusGenMass_stacks[name][0].addOverFlowBin = "upper"
#      allStacks.append(wPlusGenMass_stacks[name])
#      wMinusGenMass_stacks[name] = getStack(":XXX;gen. m_{W} (GeV);Number of Events", binning, thisCut+"&&Min$((abs(gpPdg)==24)*gpPdg)==-24", signals, varfunc = wGenMass, addData = addData, onlyW = True)
#      wMinusGenMass_stacks[name][0].addOverFlowBin = "upper"
#      allStacks.append(wMinusGenMass_stacks[name])
#
#      wGenMT_stacks[name] = getStack(":XXX;gen. m_{T} (GeV);Number of Events", binning, thisCut, signals, varfunc = wGenMT, addData = addData, onlyW = True)
#      wGenMT_stacks[name][0].addOverFlowBin = "upper"
#      allStacks.append(wGenMT_stacks[name])
#      wPlusGenMT_stacks[name] = getStack(":XXX;gen. m_{T} (GeV);Number of Events", binning, thisCut+"&&Max$((abs(gpPdg)==24)*gpPdg)==24", signals, varfunc = wGenMT, addData = addData, onlyW = True)
#      wPlusGenMT_stacks[name][0].addOverFlowBin = "upper"
#      allStacks.append(wPlusGenMT_stacks[name])
#      wMinusGenMT_stacks[name] = getStack(":XXX;gen. m_{T} (GeV);Number of Events", binning, thisCut+"&&Min$((abs(gpPdg)==24)*gpPdg)==-24", signals, varfunc = wGenMT, addData = addData, onlyW = True)
#      wMinusGenMT_stacks[name][0].addOverFlowBin = "upper"
#      allStacks.append(wMinusGenMT_stacks[name])
#
#      wRecoMT_stacks[name] = getStack(":mT;reco m_{T} (GeV);Number of Events", binning, thisCut, signals, addData = addData, onlyW = True)
#      wRecoMT_stacks[name][0].addOverFlowBin = "upper"
#      allStacks.append(wRecoMT_stacks[name])
#      wPlusRecoMT_stacks[name] = getStack(":mT;reco m_{T} (GeV);Number of Events", binning, thisCut+"&&leptonPdg<0", signals, addData = addData, onlyW = True)
#      wPlusRecoMT_stacks[name][0].addOverFlowBin = "upper"
#      allStacks.append(wPlusRecoMT_stacks[name])
#      wMinusRecoMT_stacks[name] = getStack(":mT;reco m_{T} (GeV);Number of Events", binning, thisCut+"&&leptonPdg>0", signals, addData = addData, onlyW = True)
#      wMinusRecoMT_stacks[name][0].addOverFlowBin = "upper"
#      allStacks.append(wMinusRecoMT_stacks[name])

execfile("../../RA4Analysis/plots/simplePlotsLoopKernel.py")

for stack in allStacks:
  stack[0].logy = True
  stack[0].minimum = minimum
  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS Collaboration}"], [0.2,0.85,str(int(round(targetLumi/10.))/100.)+" fb^{-1},  #sqrt{s} = 8 TeV"]]

colors = [ROOT.kBlack, ROOT.kBlue, ROOT.kGreen, ROOT.kRed]
for metb in metBins:
#for metb in [[350,-1] ]:
  nameMetb=getCutName('met', metb)
  for htb in htBins:
#  for htb in [ [750, -1]]:
    nameHTb = getCutName('ht', htb)
    for sname, stacks, fac in [
#                          ["wGenMass", wGenMass_stacks, 6], ["wPlusGenMass", wPlusGenMass_stacks, 6], ["wMinusGenMass", wMinusGenMass_stacks, 6], \
                          ["wGenPt", wGenPt_stacks, 60], ["wPlusGenPt", wPlusGenPt_stacks, 60], ["wMinusGenPt", wMinusGenPt_stacks, 60], \
                          ["wRecoPt", wRecoPt_stacks, 60], ["wPlusRecoPt", wPlusRecoPt_stacks, 60], ["wMinusRecoPt", wMinusRecoPt_stacks, 60], \
                          ["wGenMT", wGenMT_stacks, 6], ["wPlusGenMT", wPlusGenMT_stacks, 6], ["wMinusGenMT", wMinusGenMT_stacks, 6],
                          ["wRecoMT", wRecoMT_stacks, 6], ["wPlusRecoMT", wPlusRecoMT_stacks, 6], ["wMinusRecoMT", wMinusRecoMT_stacks, 6]
                        ]:
      for ic, njetb in enumerate(njetBins):
        key = '_'.join([nameMetb, nameHTb, getCutName('njets', njetb)])
        refkey = '_'.join([nameMetb, nameHTb, getCutName('njets', [5,99])])
        stacks[key][0].style = 'l12' 
        stacks[key][0].color = colors[ic] 
        stacks[key][0].data_histo.Scale(stacks[refkey][0].data_histo.Integral()/stacks[key][0].data_histo.Integral())
        stacks[key][0].maximum = fac*stacks[key][-1].data_histo.GetMaximum() 
        stacks[key][0].minimum = 10**-5 * stacks[key][0].maximum
        stacks[key][0].legendText = getNiceName('njets', njetb)
      njb_stack = [stacks['_'.join([nameMetb, nameHTb, getCutName('njets', njetb)])][0] for njetb in njetBins]
      drawNMStacks(1,1, [njb_stack],             subdir+prefix+'_'.join([nameMetb, nameHTb])+"_njb_"+sname, False)
    for sname, stacks, fac, refstack in [
                          ["wGenMT_genPtRW", wGenMT_genPtRW_stacks, 6, wGenMT_stacks], ["wPlusGenMT_genPtRW", wPlusGenMT_genPtRW_stacks, 6, wPlusGenMT_stacks], ["wMinusGenMT_genPtRW", wMinusGenMT_genPtRW_stacks, 6, wMinusGenMT_stacks],
                          ["wGenPt_genPtRW", wGenPt_genPtRW_stacks, 6, wGenPt_stacks], ["wPlusGenPt_genPtRW", wPlusGenPt_genPtRW_stacks, 6, wPlusGenPt_stacks], ["wMinusGenPt_genPtRW", wMinusGenPt_genPtRW_stacks, 6, wMinusGenPt_stacks],
                          ["wRecoMT_recoPtRW", wRecoMT_recoPtRW_stacks, 6, wRecoMT_stacks], ["wPlusRecoMT_recoPtRW", wPlusRecoMT_recoPtRW_stacks, 6, wPlusRecoMT_stacks], ["wMinusRecoMT_recoPtRW", wMinusRecoMT_recoPtRW_stacks, 6, wMinusRecoMT_stacks],
                          ["wRecoPt_recoPtRW", wRecoPt_recoPtRW_stacks, 6, wRecoPt_stacks], ["wPlusRecoPt_recoPtRW", wPlusRecoPt_recoPtRW_stacks, 6, wPlusRecoPt_stacks], ["wMinusRecoPt_recoPtRW", wMinusRecoPt_recoPtRW_stacks, 6, wMinusRecoPt_stacks],
                        ]:
      for ic, njetb in enumerate(njetCRBins):
#      for ic, njetb in enumerate([[2,2]]):
        key = '_'.join([nameMetb, nameHTb, getCutName('njets', njetb)])
        refkey = '_'.join([nameMetb, nameHTb, getCutName('njets', [5,99])])
        stacks[key][0].style = 'l12' 
        stacks[key][0].color = colors[ic] 
        stacks[key][0].data_histo.Scale(refstack[refkey][0].data_histo.Integral()/stacks[key][0].data_histo.Integral())
        stacks[key][0].maximum = fac*stacks[key][-1].data_histo.GetMaximum() 
        stacks[key][0].minimum = 10**-5 * stacks[key][0].maximum
        stacks[key][0].legendText = getNiceName('njets', njetb) +' (rew.)'
  #      stacks[key][0].data_histo.Rebin(4)
      njb_stack = [stacks['_'.join([nameMetb, nameHTb, getCutName('njets', njetb)])][0] for njetb in njetCRBins]
#      njb_stack = [stacks['_'.join([nameMetb, nameHTb, getCutName('njets', njetb)])][0] for njetb in [[2,2]]]
      njb_stack += refstack[refkey]
      drawNMStacks(1,1, [njb_stack],             subdir+prefix+'_'.join([nameMetb, nameHTb])+"_njb_"+sname, False)

