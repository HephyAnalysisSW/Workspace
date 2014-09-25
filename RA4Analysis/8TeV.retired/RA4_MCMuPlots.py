import ROOT
from array import array
from math import *
import os, copy

from Workspace.RA4Analysis.simplePlotsCommon import *
from funcs import *

import xsec
small = False

from defaultMuSamples import *

allVars=[]
allStacks=[]

signalColors = [ROOT.kBlack, ROOT.kBlue + 1, ROOT.kGreen + 2, ROOT.kOrange + 2]

## plots for studying preselection 
topIsLargest = True
minimum=10**(-0.5)
signalNumbers = []

#preprefix="noWscale"
#WJETS_scale = 1.

## pre-selection plots with met>25
#preprefix=""
#WJETS_scale = 1.34068264918  #met>25
#presel = "pf-4j30"
#subdir = "/pngFit/Mu-met25/"
#additionalCut = "met>25"
#floatWJets = False

#ABCD plots with ht>300
#preprefix="PromptReco-Mu-_ht300-met100"
#targetLumi = 884
#preprefix="May10ReReco-Mu-ht200-lpt35"
#signalNumbers = [0, 1]
#signalNumbers = [1,8]
preprefix="MC-Mu-ht300"
additionalCut = "ht>300"
#WJETS_scale = 1.78226347114  #met>25
WJETS_scale = 1.
TTJETS_scale = 1.
presel = "pf-3j40"
subdir = "/pngMC/"


doOnlyMET = False
floatWJets = False
floatTTJets = False

chainstring = "empty"
commoncf = "(0)"
prefix="empty_"

if presel == "4j30":
  chainstring = "RA4Analyzer/Events"
  commoncf = "jet1pt>30&&jet3pt>30&&lepton_pt>20&&singleMuonic&&nvetoMuons==1&&nvetoElectrons==0"
if presel == "pf-4j30":                                                                         
  chainstring = "pfRA4Analyzer/Events"                                                          
  commoncf = "jet1pt>30&&jet3pt>30&&lepton_pt>20&&singleMuonic&&nvetoMuons==1&&nvetoElectrons==0"
if presel == "pf-ex3j30":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "jet1pt>30&&jet2pt>30&&(!(jet3pt>30))&&lepton_pt>20&&singleMuonic&&nvetoMuons==1&&nvetoElectrons==0"
if presel == "pf-3j40":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "jet1pt>40&&jet2pt>40&&lepton_pt>20&&singleMuonic&&nvetoMuons==1&&nvetoElectrons==0"
if presel == "pf-4j40":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "jet1pt>40&&jet3pt>40&&lepton_pt>20&&singleMuonic&&nvetoMuons==1&&nvetoElectrons==0"
if presel == "pf-2j40":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "jet1pt>40&&lepton_pt>20&&singleMuonic&&nvetoMuons==1&&nvetoElectrons==0"

if additionalCut!="":
  commoncf+="&&"+additionalCut

prefix= "RA4_"+presel+"_"
if preprefix!="":
  prefix = preprefix+"_"+presel+"_"

for sample in allSamples:
  sample["Chain"] = chainstring

def getStack(varstring, binning, cutstring, signalNumbers, topIsLargest = False, varfunc = ""):

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
  MC_TTJETS.style              = "f0"
  MC_TTJETS.color              = ROOT.kRed - 3
  if floatTTJets:
    MC_TTJETS.floating            = "scaleByNEvents"
  else:
    MC_TTJETS.scale               = TTJETS_scale
  MC_ZJETS.legendText          = "DY + Jets"
  MC_ZJETS.style               = "f0"
  MC_ZJETS.add                 = [MC_TTJETS]
  MC_ZJETS.color               = ROOT.kGreen + 3
  MC_STOP.legendText          = "single Top"
  MC_STOP.style               = "f0"
  MC_STOP.add                 = [MC_ZJETS]
  MC_STOP.color               = ROOT.kOrange + 4
  MC_QCD.color                 = myBlue
  MC_QCD.legendText            = "QCD"
  MC_QCD.style                 = "f0"
  MC_QCD.add                   = [MC_STOP]
  MC_WJETS.legendText          = "W + Jets"
  MC_WJETS.style               = "f0"
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
  if varfunc!="":
    for var in res:
      var.varfunc = varfunc
  return res

genmet_stack = getStack(":genmet;#slash{E}_{T} (GeV);Number of Events / 25 GeV",[41,0,1025], commoncf, signalNumbers, topIsLargest)
genmet_stack[0].addOverFlowBin = "upper"
allStacks.append(genmet_stack)

genmetstacks = {}
htvals = [[300,10000],[400,10000],[500,10000],[600,10000],[700,10000],[800,10000],[900,10000],[1000,10000],[1200,10000]]
for htval in  htvals:
  stack = getStack(":genmet;#slash{E}_{T} (GeV);Number of Events / 25 GeV",[41,0,1025], commoncf+"&&ht>"+str(htval[0])+"&&ht<"+str(htval[1]), signalNumbers, topIsLargest)
  stack[0].addOverFlowBin = "upper"
  allStacks.append(stack)
  genmetstacks[str(htval[0])] = stack

for stack in allStacks:
  stack[0].minimum = minimum


reweightingHistoFile = "reweightingHisto_Summer2011.root"
#reweightingHistoFile = ""
execfile("simplePlotsLoopKernel.py")
#execfile("simplePlotsKernel.py")

for key in genmetstacks.keys():
  myfunc = ROOT.TF1("g","[0]*exp([1]*x)",0,1000)
  myfunc.SetParameters(100,-0.01)
  genmetstacks[key][0].data_histo.Fit(myfunc,"","",100, 1000)


for stack in allStacks:
  stack[0].maximum = 10.*stack[0].data_histo.GetMaximum()
  stack[0].logy = True
  stack[0].minimum = minimum
#  stack[0].legendCoordinates=[0.76,0.95 - 0.3,.98,.95]
#  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS preliminary}"], [0.2,0.85,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 7 TeV"]]
  stack[0].legendCoordinates=[0.61,0.95 - 0.08*5,.98,.95]
  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS preliminary}"], [0.2,0.85,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 7 TeV"]]
  if globals().has_key("lepton_eta_stack"):
    lepton_eta_stack[0].maximum = 90.*lepton_eta_stack[-1].data_histo.GetMaximum()

drawNMStacks(1,1,[genmet_stack],             subdir+prefix+"genmet.png", False)
for htval in htvals:
  drawNMStacks(1,1,[genmetstacks[str(htval[0])]], subdir+prefix+"genmet_ht_"+str(htval[0])+"_"+str(htval[1])+".png", False)

for stack in allStacks:
  stack[0].maximum = 1.3*stack[0].data_histo.GetMaximum()
  stack[0].logy = False
  stack[0].minumum=0
  

drawNMStacks(1,1,[genmet_stack],             subdir+prefix+"genmet_lin.png", False)
for htval in htvals:
  drawNMStacks(1,1,[genmetstacks[str(htval[0])]], subdir+prefix+"genmet_ht_"+str(htval[0])+"_"+str(htval[1])+"_lin.png", False)

