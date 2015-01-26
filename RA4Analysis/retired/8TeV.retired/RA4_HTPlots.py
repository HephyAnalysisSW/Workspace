import ROOT
from array import array
from math import *
import os, copy

from Workspace.RA4Analysis.simplePlotsCommon import *
from funcs import *

import xsec
small = False

from defaultMu2012Samples import *
targetLumi = 19400

ttbar["bins"] = ["TTJets-PowHeg"]
wjets["bins"] = ["WJetsHT250"]
data["bins"] = ["data"]

allSamples = [ttbar, wjets, dy, stop, qcd, data]
ttbar_CombWeight = {}
wjets_CombWeight = {}
for btb in [0,1,2]:
  ttbar_CombWeight[btb] =copy.deepcopy(ttbar) 
  wjets_CombWeight[btb] =copy.deepcopy(wjets) 
  ttbar_CombWeight[btb]["weight"]="weight"
  wjets_CombWeight[btb]["weight"]="weight"
  ttbar_CombWeight[btb]["weight"]+="BTag"+str(btb)
  wjets_CombWeight[btb]["weight"]+="BTag"+str(btb)
  ttbar_CombWeight[btb]["name"]+="_BTag"+str(btb)
  wjets_CombWeight[btb]["name"]+="_BTag"+str(btb)
  allSamples+=[wjets_CombWeight[btb], ttbar_CombWeight[btb]]

for sample in allSamples:
  sample["dirname"] = ["/data/schoef/convertedTuples_v16/copyMET/Ele/", "/data/schoef/convertedTuples_v16/copyMET/Mu/"]
  sample["hasWeight"] = True

allVars=[]
allStacks=[]

signalColors = [ROOT.kBlack, ROOT.kBlue + 1, ROOT.kGreen + 2, ROOT.kOrange + 2]

## plots for studying preselection 
topIsLargest = True
minimum=10**(-0.5)

preprefix = "met150"
WJETS_scale = 1.
TTJETS_scale = 1.
presel = "pf-6j40"
subdir = "/pngHT/"


chainstring = "Events"

prefix= "RA4_"+presel+"_"
if preprefix!="":
  prefix = preprefix+"_"+presel+"_"

for sample in allSamples:
  sample["Chain"] = chainstring

def getStack(varstring, binning, cutstring,  sample, dataSample, varfunc = "", useCombWeight = False):
  if not useCombWeight:
    MC0                       = variable(varstring, binning, cutstring+"&&(!(btag0>0.679))")
  else:
    MC0                       = variable(varstring, binning, cutstring)

  MC0.minimum               = 5*10**(-1)
  if sample=="TT":
    MC0.sample                = ttbar 
  if sample=="W":
    MC0.sample                = wjets
  if useCombWeight:
    if sample=="TT":
      MC0.sample                = ttbar_CombWeight[0] 
    if sample=="W":
      MC0.sample                = wjets_CombWeight[0]
  MC0.color                 = ROOT.kBlack
  MC0.legendText            = "==0 b-jets (MC)"
  MC0.style                 = "e12"
  if not useCombWeight:
    MC1                     = variable(varstring, binning, cutstring+"&&(btag0>0.679&&(!(btag1>0.679)))")
  else:
    MC1                     = variable(varstring, binning, cutstring)
  MC1.minimum               = 5*10**(-1)
  if sample=="TT":
    MC1.sample                = ttbar 
  if sample=="W":
    MC1.sample                = wjets
  if useCombWeight:
    if sample=="TT":
      MC1.sample                = ttbar_CombWeight[1] 
    if sample=="W":
      MC1.sample                = wjets_CombWeight[1]
  MC1.color                 = ROOT.kBlue
  MC1.legendText            = "==1 b-jets (MC)"
  MC1.style                 = "e12"
  if not useCombWeight: 
    MC2                       = variable(varstring, binning, cutstring+"&&(btag1>0.679)")
  else:
    MC2                       = variable(varstring, binning, cutstring)
  MC2.minimum               = 5*10**(-1)
  if sample=="TT":
    MC2.sample                = ttbar 
  if sample=="W":
    MC2.sample                = wjets
  if useCombWeight:
    if sample=="TT":
      MC2.sample                = ttbar_CombWeight[2] 
    if sample=="W":
      MC2.sample                = wjets_CombWeight[2]
  MC2.color                 = ROOT.kRed
  MC2.legendText            = "==2 b-jets (MC)"
  MC2.style                 = "e12"
  
  if sample == "W":
    data                       = variable(varstring, binning, cutstring+"&&(!(btag0>0.679))")
    data.minimum               = 5*10**(-1)
    data.sample                = dataSample
    data.color                 = ROOT.kBlack
    data.legendText            = "==0 bjets (Data)"
    data.style = "l12"

    MC0.style                 = "e12"
    MC0.dataMCRatio = [MC0, MC1]
    MC0.ratioVarName = "==0 / ==1"
    return [MC0, MC1, data]
  else:
    data                       = variable(varstring, binning, cutstring+"&&(btag1>0.679)")
    data.minimum               = 5*10**(-1)
    data.sample                = dataSample
    data.color                 = ROOT.kBlack
    data.legendText            = "==2 bjets (Data)"
    data.style = "l12"
    MC0.dataMCRatio = [MC0, MC2]
    MC0.ratioVarName = "==0 / ==2"
    return [MC0, MC1, MC2, data]

leptonCut = "((singleMuonic&&nvetoMuons==1&&nvetoElectrons==0)||(singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))"
useCombWeight = True
tt_stack =  getStack(":ht;H_{T} (GeV);Number of Events / 100 GeV", [17,400,2100]  , "ht>400&&type1phiMet>150&&njets>=6&&"+leptonCut, "TT", data, useCombWeight = useCombWeight)
allStacks.append(tt_stack)
w_stack =   getStack(":ht;H_{T} (GeV);Number of Events / 100 GeV", [17,400,2100]  , "ht>400&&type1phiMet>150&&njets>=6&&"+leptonCut, "W", data, useCombWeight = useCombWeight)
allStacks.append(w_stack)

for stack in allStacks:
  stack[0].minimum = minimum

execfile("simplePlotsLoopKernel.py")

for stack in allStacks:
  for var in stack[1:]:
#    var.data_histo.Scale(stack[0].data_histo.Integral(stack[0].data_histo.FindBin(400), -1)/ var.data_histo.Integral(stack[0].data_histo.FindBin(400), -1))
    var.normalizeTo = stack[0]
    var.normalizeWhat = ""

for stack in allStacks:
  stack[0].maximum = 10.*stack[0].data_histo.GetMaximum()
  stack[0].logy = True
  stack[0].data_histo.GetXaxis().SetLabelSize(0.035)
  stack[0].minimum = minimum
  stack[0].legendCoordinates=[0.61,0.95 - 0.08*5,.98,.95]
  stack[0].lines = [[0.25, 0.85, "#font[22]{CMS preliminary}"], [0.25,0.80,str(int(round(targetLumi/100.))/10.)+" fb^{-1},  #sqrt{s} = 8 TeV"]]

drawNMStacks(1,1, [tt_stack],                 subdir+prefix+"tt", False)
drawNMStacks(1,1, [w_stack],              subdir+prefix+"wjets", False)
