import ROOT
from array import array
from math import *
import os, copy

from Workspace.RA4Analysis.simplePlotsCommon import *
from funcs import *

import xsec
small = False

from defaultEle2012Samples import *

targetLumi = 19400.
#lumiScale = 19.4/20.
lumiScale = 1.

ttbar["bins"] = ["TTJets-PowHeg"]
ttvJets["bins"] = ["TTZJets", "TTWJets"]
wjets["bins"] = ["WJetsHT250"]
data["bins"] = ["data"]
stop["bins"] = ["singleTop"]
dy["bins"]  = ["DY"]
qcd["bins"] = ["QCD"]
allSamples = [ttbar, wjets, dy, stop, qcd, ttvJets, data]

defWeight = "weight"

def getT1tttt(mgl, mn, cdir = "v21"):
  res = copy.deepcopy(mc)
  res["dirname"] = ["/data/schoef/convertedTuples_"+cdir+"/copyMET/Ele/", "/data/schoef/convertedTuples_"+cdir+"/copyMET/Mu/"]
  res["bins"] = ["T1tttt_"+str(mgl)+"_"+str(mn)]
  res["hasWeight"] = True
  res["weight"] = "weight"
  res["name"] = res["bins"][0]
  return res

for sample in allSamples:
  sample["dirname"] = ["/data/schoef/convertedTuples_v21/copyMET/Ele/", "/data/schoef/convertedTuples_v21/copyMET/Mu/"]
  sample["hasWeight"] = True
  if sample['name'].lower().count('data'):
    sample["weight"] = "weight"
  else:
    sample["weight"] = defWeight

signals = []
for mgl, mn in [ [1350, 800], [1300, 25]]:
  s = getT1tttt(mgl, mn)
  allSamples.append(s)
#  s["scaleFac"] = sf 
  signals.append(s)

allVars=[]
allStacks=[]

signalColors = [ ROOT.kBlue + 1, ROOT.kBlack, ROOT.kGreen + 2, ROOT.kOrange + 2]

## plots for studying preselection 
topIsLargest = True

minimum=10**(-0.5)

presel = "pf-4j40"
preprefix     = "ht750-met250-njets6-bt2"
additionalCut = "ht>750&&type1phiMet>250&&njets>=6&&nbtags>=2"

subdir = "/pngESV/"

doOnlyMET = False
floatWJets = False
floatTTJets = False
#normalizeToData = False
normalizeSignalToBkg = True

chainstring = "empty"
commoncf = "(0)"
prefix="empty_"

if presel == "pf-4j40":
  chainstring = "Events"
  commoncf = "njets>=4&&leptonPt>20&&(singleElectronic&&nvetoElectrons==1&&nvetoMuons==0||singleMuonic&&nvetoElectrons==0&&nvetoMuons==1)"
if presel == "pf-6j40":
  chainstring = "Events"
  commoncf =  "njets>=6&&leptonPt>20&&(singleElectronic&&nvetoElectrons==1&&nvetoMuons==0||singleMuonic&&nvetoElectrons==0&&nvetoMuons==1)"
if presel == "pf-3j40":
  chainstring = "Events"
  commoncf =  "njets>=3&&leptonPt>20&&(singleElectronic&&nvetoElectrons==1&&nvetoMuons==0||singleMuonic&&nvetoElectrons==0&&nvetoMuons==1)"
if presel == "pf-ex4j40":
  chainstring = "Events"
  commoncf =  "njets==4&&leptonPt>20&&(singleElectronic&&nvetoElectrons==1&&nvetoMuons==0||singleMuonic&&nvetoElectrons==0&&nvetoMuons==1)"

if presel == "pf-ex5j40":
  chainstring = "Events"
  commoncf = "njets==5&&leptonPt>20&&(singleElectronic&&nvetoElectrons==1&&nvetoMuons==0||singleMuonic&&nvetoElectrons==0&&nvetoMuons==1)"

if additionalCut!="":
  commoncf+="&&"+additionalCut

prefix= "RA4_"+presel+"_"
if preprefix!="":
  prefix = preprefix+"_"+presel+"_"
if defWeight=="weight":
  prefix = "converted_"+prefix
else:
  prefix = "converted_"+defWeight+"_"+prefix

for sample in allSamples:
  sample["Chain"] = chainstring


def getStack(varstring, binning, cutstring, signals, topIsLargest = False, varfunc = ""):
  DATA          = variable(varstring, binning, cutstring)
  DATA.sample   = data
#  DATA.color    = ROOT.kGray
  DATA.color    = dataColor
  DATA.legendText="Data"

  MC_QCD                       = variable(varstring, binning, cutstring)
  MC_QCD.minimum               = minimum
  MC_QCD.sample                = qcd
  MC_TTJETS                    = copy.deepcopy(MC_QCD)
  MC_TTJETS.sample             = ttbar
  MC_WJETS                     = copy.deepcopy(MC_QCD)
  MC_WJETS.sample              = wjets
  MC_ZJETS                     = copy.deepcopy(MC_QCD)
  MC_ZJETS.sample              = dy
  MC_STOP                      = copy.deepcopy(MC_QCD)
  MC_STOP.sample               = stop
  MC_TTVJETS                    = copy.deepcopy(MC_QCD)
  MC_TTVJETS.sample             = ttvJets

  MC_TTJETS.legendText         = "t#bar{t} + Jets"
  MC_TTJETS.style              = "f0"
  MC_TTJETS.color              = ROOT.kRed - 3
  MC_TTJETS.add                =  [MC_WJETS]
  MC_WJETS.legendText          = "W + Jets"
  MC_WJETS.style               = "f0"
  MC_WJETS.add                 = [MC_STOP]
  MC_WJETS.color               = ROOT.kYellow
  MC_STOP.legendText           = "single Top"
  MC_STOP.style                = "f0"
  MC_STOP.add                  = [MC_TTVJETS]
  MC_STOP.color                = ROOT.kOrange + 4
  MC_TTVJETS.legendText         = "TT+ Z/W + Jets"
  MC_TTVJETS.style              = "f0"
  MC_TTVJETS.add                = [MC_ZJETS]
  MC_TTVJETS.color              = ROOT.kCyan - 8
  MC_ZJETS.legendText          = "DY + Jets"
  MC_ZJETS.style               = "f0"
  MC_ZJETS.add                 = [MC_QCD]
  MC_ZJETS.color               = ROOT.kGreen + 3
  MC_QCD.color                 = myBlue
  MC_QCD.legendText            = "QCD"
  MC_QCD.style                 = "f0"
  MC_QCD.add                   = []

  res = [MC_TTJETS, MC_WJETS, MC_STOP, MC_TTVJETS, MC_ZJETS, MC_QCD]

  res[0].dataMCRatio = [DATA, res[0]]
  for i, signal in enumerate(signals):
    MC_SIGNAL                    = copy.deepcopy(MC_QCD)
    MC_SIGNAL.sample             = copy.deepcopy(signal)
    MC_SIGNAL.legendText         = signal["name"]
    if MC_SIGNAL.sample.has_key('scaleFac'):
      MC_SIGNAL.legendText       = str(int(MC_SIGNAL.sample['scaleFac']))+"*"+MC_SIGNAL.legendText
    MC_SIGNAL.style              = "l02"
    MC_SIGNAL.color              = signalColors[i]
    MC_SIGNAL.add = []
    if normalizeSignalToBkg:
      MC_SIGNAL.normalizeTo = res[0]
    res.append(MC_SIGNAL)
  getLinesForStack(res, targetLumi)
  nhistos = len(res)
  for var in res:
    var.legendCoordinates=[0.61,0.95 - 0.08*5,.98,.95]
    var.scale = lumiScale
#    var.legendCoordinates=[0.64,0.95 - 0.05*nhistos,.98,.95] #for signalnumbers = [0,1]
  res.append(DATA)
  if varfunc!="":
    for var in res:
      var.varfunc = varfunc
  return res

  getLinesForStack(res, targetLumi)
  nhistos = len(res)
  for var in res:
    var.legendCoordinates=[0.61,0.95 - 0.08*5,.98,.95]
#    var.legendCoordinates=[0.64,0.95 - 0.05*nhistos,.98,.95] #for signalnumbers = [0,1]
  res.append(DATA)
  if varfunc!="":
    for var in res:
      var.varfunc = varfunc
  return res

met_stack = getStack(":type1phiMet;#slash{E}_{T} (GeV);Number of Events / 50 GeV",[18,150,1050], commoncf, signals, topIsLargest)
met_stack[0].addOverFlowBin = "upper"
allStacks.append(met_stack)

if not doOnlyMET:
  ngoodVertices_stack = getStack(":ngoodVertices;Number of Vertices;Number of Events",[51,0,51], commoncf, signals, topIsLargest)
  ngoodVertices_stack[0].addOverFlowBin = "upper"
  allStacks.append(ngoodVertices_stack)

  ht_stack                          = getStack(":ht;H_{T} (GeV);Number of Events / 100 GeV",[26,400,3000], commoncf, signals, topIsLargest)
  ht_stack[0].addOverFlowBin = "upper"
  allStacks.append(ht_stack)

  njets_stack = getStack(":njets;Number of Jets;Number of Events",[10,4,14], commoncf.replace("jet2pt>40&&",""), signals, topIsLargest)
  njets_stack[0].addOverFlowBin = "upper"
  allStacks.append(njets_stack)

  thrust_stack = getStack(":thrust;transverse thrust;Number of Events",[30,0,1], commoncf, signals, topIsLargest)
  thrust_stack[0].addOverFlowBin = "both"
  allStacks.append(thrust_stack)

  htThrustLepSide_stack = getStack(":XXX;H_{T} frac. on lep. thrust hem.;Number of Events",[30,0,1], commoncf, signals, topIsLargest, htThrustLepRatio)
  htThrustLepSide_stack[0].addOverFlowBin = "both"
  allStacks.append(htThrustLepSide_stack)

  htThrustOppSide_stack = getStack(":XXX;H_{T} frac. on had. thrust hem.;Number of Events",[30,0,1], commoncf, signals, topIsLargest, htThrustOppRatio)
  htThrustOppSide_stack[0].addOverFlowBin = "both"
  allStacks.append(htThrustOppSide_stack)

  S3D_stack = getStack(":S3D;sphericity(3D);Number of Events",[30,0,1], commoncf, signals, topIsLargest)
  S3D_stack[0].addOverFlowBin = "both"
  allStacks.append(S3D_stack)

  C3D_stack = getStack(":C3D;circularity(3D);Number of Events",[30,0,1], commoncf, signals, topIsLargest)
  C3D_stack[0].addOverFlowBin = "both"
  allStacks.append(C3D_stack)

  C2D_stack = getStack(":C2D;trans. circularity (2D);Number of Events",[30,0,1], commoncf, signals, topIsLargest)
  C2D_stack[0].addOverFlowBin = "both"
  allStacks.append(C2D_stack)

  linS3D_stack = getStack(":linS3D; lin. spher. (3D);Number of Events",[30,0,1], commoncf, signals, topIsLargest)
  linS3D_stack[0].addOverFlowBin = "both"
  allStacks.append(linS3D_stack)

  linC3D_stack = getStack(":linC3D;lin. circ. (3D);Number of Events",[30,0,1], commoncf, signals, topIsLargest)
  linC3D_stack[0].addOverFlowBin = "both"
  allStacks.append(linC3D_stack)

  linC2D_stack = getStack(":linC2D;trans. lin. circ. (2D);Number of Events",[30,0,1], commoncf, signals, topIsLargest)
  linC2D_stack[0].addOverFlowBin = "both"
  allStacks.append(linC2D_stack)

  c2DLepMET_stack = getStack(":c2DLepMET;trans. circularity (2D, lmet);Number of Events",[30,0,1], commoncf, signals, topIsLargest)
  c2DLepMET_stack[0].addOverFlowBin = "both"
  allStacks.append(c2DLepMET_stack)

  linC2DLepMET_stack = getStack(":linC2DLepMET;trans. lin. circ. (2D, lmet);Number of Events",[30,0,1], commoncf, signals, topIsLargest)
  linC2DLepMET_stack[0].addOverFlowBin = "both"
  allStacks.append(linC2DLepMET_stack)

  FWMT1_stack = getStack(":FWMT1;FWMT1;Number of Events",[30,0,1], commoncf, signals, topIsLargest)
  FWMT1_stack[0].addOverFlowBin = "both"
  allStacks.append(FWMT1_stack)

  FWMT2_stack = getStack(":FWMT2;FWMT2;Number of Events",[30,0,1], commoncf, signals, topIsLargest)
  FWMT2_stack[0].addOverFlowBin = "both"
  allStacks.append(FWMT2_stack)

  FWMT3_stack = getStack(":FWMT3;FWMT3;Number of Events",[30,0,1], commoncf, signals, topIsLargest)
  FWMT3_stack[0].addOverFlowBin = "both"
  allStacks.append(FWMT3_stack)

  FWMT4_stack = getStack(":FWMT4;FWMT4;Number of Events",[30,0,1], commoncf, signals, topIsLargest)
  FWMT4_stack[0].addOverFlowBin = "both"
  allStacks.append(FWMT4_stack)

  FWMT1LepMET_stack = getStack(":FWMT1LepMET;FWMT1LepMET;Number of Events",[30,0,1], commoncf, signals, topIsLargest)
  FWMT1LepMET_stack[0].addOverFlowBin = "both"
  allStacks.append(FWMT1LepMET_stack)

  FWMT2LepMET_stack = getStack(":FWMT2LepMET;FWMT2LepMET;Number of Events",[30,0,1], commoncf, signals, topIsLargest)
  FWMT2LepMET_stack[0].addOverFlowBin = "both"
  allStacks.append(FWMT2LepMET_stack)

  FWMT3LepMET_stack = getStack(":FWMT3LepMET;FWMT3LepMET;Number of Events",[30,0,1], commoncf, signals, topIsLargest)
  FWMT3LepMET_stack[0].addOverFlowBin = "both"
  allStacks.append(FWMT3LepMET_stack)

  FWMT4LepMET_stack = getStack(":FWMT4LepMET;FWMT4LepMET;Number of Events",[30,0,1], commoncf, signals, topIsLargest)
  FWMT4LepMET_stack[0].addOverFlowBin = "both"
  allStacks.append(FWMT4LepMET_stack)

  htRatio_stack = getStack(":htRatio;htRatio;Number of Events",[30,0,1], commoncf, signals, topIsLargest)
  htRatio_stack[0].addOverFlowBin = "both"
  allStacks.append(htRatio_stack)

  minDeltaPhiOverPi_stack = getStack(":XXX;min #Delta#Phi(MET,j_{1,2})/#pi;Number of Events",[30,0,1], commoncf, signals, topIsLargest, minDeltaPhiOverPi)
  minDeltaPhiOverPi_stack[0].addOverFlowBin = "both"
  allStacks.append(minDeltaPhiOverPi_stack)

  cosDeltaPhiLepW_stack = getStack(":XXX;min #Delta#Phi(MET,j_{1,2})/#pi;Number of Events",[30,-1,1], commoncf, signals, topIsLargest, cosDeltaPhiLepW)
  cosDeltaPhiLepW_stack[0].addOverFlowBin = "both"
  allStacks.append(cosDeltaPhiLepW_stack)

for stack in allStacks:
  stack[0].minimum = minimum

#for stack in allStacks:
#  for var in stack:
#    var.addOverFlowBin = "both"
#reweightingHistoFile = "PU/reweightingHisto_Summer2012-S10-Run2012AB-Jul13ReReco.root"
reweightingHistoFile = ""

execfile("simplePlotsLoopKernel.py")

#if normalizeToData:
#  for stack in allStacks:
#    for var in stack[:-1]:
#      var.normalizeTo = stack[-1]
#      var.normalizeWhat = stack[0]
#    stack[-1].normalizeTo=""
#    stack[-1].normalizeWhat=""
#else:
#  for stack in allStacks:
#    for var in stack:
#      var.normalizeTo = ""
#      var.normalizeWhat = "" 

for stack in allStacks:
  stack[0].maximum = 4*10**4 # 10.*stack[-1].data_histo.GetMaximum()
  stack[0].logy = True
  stack[0].minimum = minimum
#  stack[0].legendCoordinates=[0.76,0.95 - 0.3,.98,.95]
#  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS preliminary}"], [0.2,0.85,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 7 TeV"]]
  stack[0].legendCoordinates=[0.61,0.95 - 0.08*5,.98,.95]
  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS Collaboration}"], [0.2,0.85,str(int(round(targetLumi/10.))/100.)+" fb^{-1},  #sqrt{s} = 8 TeV"]]

#discrimination={}
#for stack in allStacks:
#  disc = []
#  for v in stack:
#    if v.sample['name'].count('T1tttt'):
#       disc.append( bestSOverBBothSides( v.data_histo, stack[0].data_histo))
#  discrimination[stack[0].name] = {'value':min(disc),'allValues':disc}
#  print "Variable",stack[0].name,"min Disc. (S/B):",min(disc), "all", disc

drawNMStacks(1,1,[met_stack],             subdir+prefix+"met", False)
if not doOnlyMET:
  drawNMStacks(1,1,[ngoodVertices_stack],             subdir+prefix+"ngoodVertices", False)
  drawNMStacks(1,1,[ht_stack],              subdir+prefix+"ht", False)
  drawNMStacks(1,1,[njets_stack],             subdir+prefix+"njets", False)

  drawNMStacks(1,1,[thrust_stack], subdir+prefix+"thrust", False)
  drawNMStacks(1,1,[htThrustLepSide_stack], subdir+prefix+"htThrustLepSide", False)
  drawNMStacks(1,1,[htThrustOppSide_stack], subdir+prefix+"htThrustOppSide", False)
  drawNMStacks(1,1,[S3D_stack], subdir+prefix+"S3D", False)
  drawNMStacks(1,1,[C3D_stack], subdir+prefix+"C3D", False)
  drawNMStacks(1,1,[C2D_stack], subdir+prefix+"C2D", False)
  drawNMStacks(1,1,[linS3D_stack], subdir+prefix+"linS3D", False)
  drawNMStacks(1,1,[linC3D_stack], subdir+prefix+"linC3D", False)
  drawNMStacks(1,1,[linC2D_stack], subdir+prefix+"linC2D", False)
  drawNMStacks(1,1,[c2DLepMET_stack], subdir+prefix+"c2DLepMET", False)
  drawNMStacks(1,1,[linC2DLepMET_stack], subdir+prefix+"linC2DLepMET", False)
  drawNMStacks(1,1,[FWMT1_stack], subdir+prefix+"FWMT1", False)
  drawNMStacks(1,1,[FWMT2_stack], subdir+prefix+"FWMT2", False)
  drawNMStacks(1,1,[FWMT3_stack], subdir+prefix+"FWMT3", False)
  drawNMStacks(1,1,[FWMT4_stack], subdir+prefix+"FWMT4", False)
  drawNMStacks(1,1,[FWMT1LepMET_stack], subdir+prefix+"FWMT1LepMET", False)
  drawNMStacks(1,1,[FWMT2LepMET_stack], subdir+prefix+"FWMT2LepMET", False)
  drawNMStacks(1,1,[FWMT3LepMET_stack], subdir+prefix+"FWMT3LepMET", False)
  drawNMStacks(1,1,[FWMT4LepMET_stack], subdir+prefix+"FWMT4LepMET", False)
  drawNMStacks(1,1,[htRatio_stack], subdir+prefix+"htRatio", False)
  drawNMStacks(1,1,[minDeltaPhiOverPi_stack], subdir+prefix+"minDeltaPhiOverPi", False)
  drawNMStacks(1,1,[cosDeltaPhiLepW_stack], subdir+prefix+"cosDeltaPhiLepW", False)

#for stack in allStacks:
#  stack[0].maximum = 1.3*stack[-1].data_histo.GetMaximum()
#  stack[0].logy = False
#  stack[0].minumum=0
#
#drawNMStacks(1,1,[met_stack],             subdir+prefix+"met_lin", False)
#if not doOnlyMET:
#  drawNMStacks(1,1,[ngoodVertices_stack],             subdir+prefix+"ngoodVertices_lin", False)
#  drawNMStacks(1,1,[ht_stack],              subdir+prefix+"ht_lin", False)
#  drawNMStacks(1,1,[njets_stack],             subdir+prefix+"njets_lin", False)
#
#  drawNMStacks(1,1,[thrust_stack], subdir+prefix+"thrust_lin", False)
#  drawNMStacks(1,1,[htThrustLepSide_stack], subdir+prefix+"htThrustLepSide_lin", False)
#  drawNMStacks(1,1,[htThrustOppSide_stack], subdir+prefix+"htThrustOppSide_lin", False)
#  drawNMStacks(1,1,[S3D_stack], subdir+prefix+"S3D_lin", False)
#  drawNMStacks(1,1,[C3D_stack], subdir+prefix+"C3D_lin", False)
#  drawNMStacks(1,1,[C2D_stack], subdir+prefix+"C2D_lin", False)
#  drawNMStacks(1,1,[linS3D_stack], subdir+prefix+"linS3D_lin", False)
#  drawNMStacks(1,1,[linC3D_stack], subdir+prefix+"linC3D_lin", False)
#  drawNMStacks(1,1,[linC2D_stack], subdir+prefix+"linC2D_lin", False)
#  drawNMStacks(1,1,[c2DLepMET_stack], subdir+prefix+"c2DLepMET_lin", False)
#  drawNMStacks(1,1,[linC2DLepMET_stack], subdir+prefix+"linC2DLepMET_lin", False)
#  drawNMStacks(1,1,[FWMT1_stack], subdir+prefix+"FWMT1_lin", False)
#  drawNMStacks(1,1,[FWMT2_stack], subdir+prefix+"FWMT2_lin", False)
#  drawNMStacks(1,1,[FWMT3_stack], subdir+prefix+"FWMT3_lin", False)
#  drawNMStacks(1,1,[FWMT4_stack], subdir+prefix+"FWMT4_lin", False)
#  drawNMStacks(1,1,[FWMT1LepMET_stack], subdir+prefix+"FWMT1LepMET_lin", False)
#  drawNMStacks(1,1,[FWMT2LepMET_stack], subdir+prefix+"FWMT2LepMET_lin", False)
#  drawNMStacks(1,1,[FWMT3LepMET_stack], subdir+prefix+"FWMT3LepMET_lin", False)
#  drawNMStacks(1,1,[FWMT4LepMET_stack], subdir+prefix+"FWMT4LepMET_lin", False)
