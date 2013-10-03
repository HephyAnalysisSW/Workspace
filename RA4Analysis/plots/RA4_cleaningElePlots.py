import ROOT
from array import array
from math import *
import os, copy

from simplePlotsCommon import *

import xsec
small = False

from defaultEleSamples import *
targetLumi = 36.
allVars=[]
allStacks=[]

signalColors = [ROOT.kBlack, ROOT.kBlue + 1, ROOT.kGreen + 2, ROOT.kOrange + 2]

## plots for studying preselection 
topIsLargest = True
minimum=10**(-0.5)

#WJETS_scale = 1.34068264918  #met>25
WJETS_scale = 1.0
subdir = "/png2011/"
presel = "pf-4j30"
#additionalCut = "ht>900"
#preprefix = "ht900"
#additionalCut = "ht>300&&ht<900"
#preprefix = "ht300-900"
#additionalCut = "kinMetSig>9"
#preprefix = "kMs9"
#additionalCut = "kinMetSig>2.5&&kinMetSig<9"
#preprefix = "kMs2.5-9"
#additionalCut = "kinMetSig>2.5&&ht>300"
#preprefix = "kMs2.5ht300-oldRA4-Ele"
additionalCut = ""
preprefix = "oldRA4-Ele"
#additionalCut = ""
#preprefix = ""
signalNumbers = []

floatWJets = False

doOnlyMET = False
#floatWJets = True

chainstring = "empty"
commoncf = "(0)"
prefix="empty_"


if presel == "pf-4j30":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "jet3pt>30&&lepton_pt>20&&singleElectronic"
if presel == "3j50":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "jet2pt>50&&lepton_pt>20&&singleElectronic"
if presel == "2j80+1j50":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "jet1pt>80&&jet2pt>50&&lepton_pt>20&&singleElectronic"
if presel == "2j80+2j50":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "jet1pt>80&&jet3pt>50&&lepton_pt>20&&singleElectronic"
if presel == "120_80_50":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "jet0pt>120&&jet1pt>80&&jet2pt>50&&lepton_pt>20&&singleElectronic"

if additionalCut!="":
  commoncf+="&&"+additionalCut

prefix= "RA4_"+presel+"_"
if preprefix!="":
  prefix = preprefix+"_"+presel+"_"

for sample in allSamples:
  sample["Chain"] = chainstring

def getStack(varstring, binning, cutstring, signalNumbers, topIsLargest = False):
  DATA          = variable(varstring, binning, cutstring)
  DATA.sample   = data
#  DATA.color    = ROOT.kGray
  DATA.color    = dataColor
  DATA.legendText="Data"

  MC_QCD                       = variable(varstring, binning, cutstring)
  MC_QCD.minimum               = 10**(-1)

  MC_TTJETS                    = copy.deepcopy(MC_QCD)
  MC_WJETS                     = copy.deepcopy(MC_QCD)
  MC_ZJETS                     = copy.deepcopy(MC_QCD)
  MC_STOP                      = copy.deepcopy(MC_QCD)

  MC_QCD                       = variable(varstring, binning, cutstring)
  MC_QCD.minimum               = 5*10**(-1)
  MC_QCD.sample                = copy.deepcopy(mc)
  MC_QCD.sample["bins"]        = QCD_Bins
  MC_TTJETS                    = copy.deepcopy(MC_QCD)
  MC_TTJETS.sample             = copy.deepcopy(mc)
  MC_TTJETS.sample["bins"]     = ["TTJets"]
  MC_WJETS                     = copy.deepcopy(MC_QCD)
  MC_WJETS.sample              = copy.deepcopy(mc)
  MC_WJETS.sample["bins"]      = WJets_Bins

  if floatWJets:
    MC_WJETS.floating            = "scaleByNEvents"
  else:
    MC_WJETS.scale               = WJETS_scale
  MC_ZJETS                     = copy.deepcopy(MC_QCD)
  MC_ZJETS.sample              = copy.deepcopy(mc)
  MC_ZJETS.sample["bins"]      = ZJets_Bins
  MC_STOP                     = copy.deepcopy(MC_QCD)
  MC_STOP.sample              = copy.deepcopy(mc)
  MC_STOP.sample["bins"]      = singleTop_Bins

  MC_TTJETS.legendText         = "t#bar{t} + Jets"
  MC_TTJETS.style              = "f"
  MC_TTJETS.color              = ROOT.kRed - 3
  MC_ZJETS.legendText          = "DY + Jets"
  MC_ZJETS.style               = "f"
  MC_ZJETS.add                 = [MC_TTJETS]
  MC_ZJETS.color               = ROOT.kGreen + 3
  MC_STOP.legendText          = "single Top"
  MC_STOP.style               = "f"
  MC_STOP.add                 = [MC_ZJETS]
  MC_STOP.color               = ROOT.kOrange + 4
  MC_QCD.color                 = myBlue
  MC_QCD.legendText            = "QCD"
  MC_QCD.style                 = "f"
  MC_QCD.add                   = [MC_STOP]
  MC_WJETS.legendText          = "W + Jets"
  MC_WJETS.style               = "f"
  MC_WJETS.add                 = [MC_QCD]
  MC_WJETS.color               = ROOT.kYellow
  res=[]
  if topIsLargest:
    res = [MC_TTJETS, MC_WJETS, MC_QCD, MC_STOP, MC_ZJETS]
    MC_TTJETS.add=[MC_WJETS]
    MC_ZJETS.add=[]
  else:
    res = [MC_WJETS, MC_QCD, MC_STOP, MC_ZJETS, MC_TTJETS]
  for i in range(len(signalNumbers)):
    MC_SIGNAL                    = copy.deepcopy(MC_QCD)
    MC_SIGNAL.sample             = copy.deepcopy(signals[str(signalNumbers[i])])
    MC_SIGNAL.legendText         = signals[str(signalNumbers[i])]["name"]
    MC_SIGNAL.style              = "l"
    MC_SIGNAL.color              = signalColors[i]
    MC_SIGNAL.add = []
    res.append(MC_SIGNAL)

  getLinesForStack(res, targetLumi)
  nhistos = len(res)
  for var in res:
    var.legendCoordinates=[0.61,0.95 - 0.08*5,.98,.95]
#    var.legendCoordinates=[0.64,0.95 - 0.05*nhistos,.98,.95] #for signalnumbers = [0,1]
  res.append(DATA)
  return res


nvetoElectrons_stack = getStack(":nvetoElectrons;nvetoElectrons;Number of Events ",[7,0,7], commoncf, signalNumbers, topIsLargest)
allStacks.append(nvetoElectrons_stack)
nvetoMuons_stack = getStack(":nvetoMuons;nvetoMuons;Number of Events ",[7,0,7], commoncf, signalNumbers, topIsLargest)
allStacks.append(nvetoMuons_stack)
ngoodPhotons_stack = getStack(":ngoodPhotons;ngoodPhotons;Number of Events ",[7,0,7], commoncf, signalNumbers, topIsLargest)
allStacks.append(ngoodPhotons_stack)
metIso_stack = getStack(":metiso;metIso;Number of Events ",[20,0,1.57], commoncf, signalNumbers, topIsLargest)
allStacks.append(metIso_stack)

for stack in allStacks:
  stack[0].minimum = minimum

execfile("simplePlotsKernel.py")

for stack in allStacks:
  stack[0].maximum = 3.*stack[0].data_histo.GetMaximum()
  stack[0].logy = True
  stack[0].minimum = minimum
  stack[0].legendCoordinates=[0.61,0.95 - 0.08*5,.98,.95]
#  stack[0].lines = [[0.61, 0.48, "#font[22]{CMS preliminary}"], [0.61,0.43,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 7 TeV"]]
  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS preliminary}"], [0.2,0.85,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 7 TeV"]]

drawNMStacks(1,1,[nvetoElectrons_stack],             subdir+prefix+"nvetoElectrons", False)
drawNMStacks(1,1,[nvetoMuons_stack],             subdir+prefix+"nvetoMuons", False)
drawNMStacks(1,1,[ngoodPhotons_stack],             subdir+prefix+"ngoodPhotons", False)
drawNMStacks(1,1,[metIso_stack],             subdir+prefix+"metIso", False)

