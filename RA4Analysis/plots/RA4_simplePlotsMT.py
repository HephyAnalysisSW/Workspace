import ROOT
from array import array
from math import *
import os, copy
from simpleStatTools import niceNum
from simplePlotsCommon import *
from funcs import *

import xsec
small = False
useConvertedTuples = True
mode = "Mu"

from defaultMu2012Samples import *

if useConvertedTuples:
  ttbarPowHeg["bins"] = ["TTJets-PowHeg"]
  wjets["bins"] = ["WJetsHT250"]
  data["bins"] = ["data"]
  stop["bins"] = ["singleTop"]
  dy["bins"]  = ["DY"]
  qcd["bins"] = ["QCD"]
  mc["bins"] = ["TTJets-PowHeg", "WJetsHT250", "singleTop", "DY", "QCD"]
#allSamples = [ttbar, wjets, dy, stop, qcd, data, mc]
thisSample = ttbarPowHeg

#thisSample = wjets 

allSamples = [thisSample]

defWeight = "weight"

if useConvertedTuples:
  for sample in allSamples:
    sample["dirname"] = "/data/schoef/convertedTuples_v16/copyMET/"+mode+"/"
    sample["hasWeight"] = True
    if sample['name'].lower().count('data'):
      sample["weight"] = "weight"
    else:
      sample["weight"] = defWeight

targetLumi = 20000.

allVars=[]
allStacks=[]
    
signalColors = [ROOT.kBlack, ROOT.kBlue + 1, ROOT.kGreen + 2, ROOT.kOrange + 2]

## plots for studying preselection 
minimum=0.7 
    
    
presel = "pf-4j40"
preprefix     = mode+"-met100-coarseHT"
additionalCut = "met>100"

subdir = "/MT/"

doOnlyMET = False
normalizeToData = False

chainstring = "empty"
commoncf = "(0)"
prefix="empty_"

if presel == "pf-4j40":
  chainstring = "Events"
  if mode=="Mu":
    commoncf = "jet3pt>40&&leptonPt>20&&singleMuonic&&nvetoMuons==1&&nvetoElectrons==0"
  if mode=="Ele":
    commoncf = "jet3pt>40&&leptonPt>20&&singleElectronic&&nvetoElectrons==1&&nvetoMuons==0"

if additionalCut!="":
  commoncf+="&&"+additionalCut

prefix= "RA4_"+presel+"_"
if preprefix!="":
  prefix = preprefix+"_"+presel+"_"
if useConvertedTuples:
  if defWeight=="weight":
    prefix = "converted_"+prefix
  else:
    prefix = "converted_"+defWeight+"_"+prefix

for sample in allSamples:
  sample["Chain"] = chainstring


def legendName(varname, cutlow, cuthigh = -1):
  if cuthigh>0:
    return str(cutlow)+"< "+varname+" <"+str(cuthigh)
  else:
    return str(cutlow)+"< "+varname

def varBin(cutlow, cuthigh = -1, var = "ht"):
  if cuthigh>0:
    return "&&("+var+">="+str(cutlow)+")&&("+var+"<"+str(cuthigh)+")"
  else:
    return "&&("+var+">="+str(cutlow)+")"

def nJetBin(cutn = -1):
  if cutn>=0:
    return "&&(njets=="+str(cutn)+")"
  else:
    return "&&(1)"

#def getNJetStack(varstring, binning, cutstring, thisSample, njetBins, topIsLargest = False):
#  DATA          = variable(varstring, binning, cutstring)
#  DATA.sample   = data
##  DATA.color    = ROOT.kGray
#  DATA.color    = dataColor
#  DATA.legendText="Data"
#  MC_QCD                       = variable(varstring, binning, cutstring)
#  MC_QCD.minimum               = 5*10**(-1)
#  MC_QCD.sample                = qcd 
#  MC                    = copy.deepcopy(MC_QCD)
#  MC.sample             = ttjets 
#  MC_WJETS                     = copy.deepcopy(MC_QCD)
#  MC_WJETS.sample              = wjets 
#  MC_DY                     = copy.deepcopy(MC_QCD)
#  MC_DY.sample              = dy 
#
#  MC.legendText         = "TTJets"
#  MC.style              = "f"
#  MC.color              = ROOT.kRed - 3
#  MC.add                = [MC_WJETS]
#  MC_WJETS.legendText          = "WJets"
#  MC_WJETS.style               = "f"
#  MC_WJETS.add                 = [MC_QCD]
#  MC_WJETS.color               = ROOT.kYellow
#  MC_QCD.color                 = myBlue
#  MC_QCD.legendText            = "QCD"
#  MC_QCD.style                 = "f"
#  MC_QCD.add                   = [MC_DY]
#  MC_DY.legendText          = "ZJets"
#  MC_DY.style               = "f"
#  MC_DY.color               = ROOT.kGreen + 3
##  res = [MC_WJETS, MC_QCD, MC_DY, MC, DATA, ISO_DATA]
#  res = [MC, MC_WJETS, MC_QCD, MC_DY]
#
#  for ibin in range(len(njetBins)):
#    print cutstring + nJetBin(njetBins[ibin])
#    shape = variable(varstring, binning, cutstring + nJetBin(njetBins[ibin]))
#    shape.minimum = 5*10**(-1)
#    shape.sample = mc
#    shape.normalizeTo = res[0]
#    shape.legendText = "njet=="+str(njetBins[ibin])
#    shape.style="e"
#    shape.color = shapeColors[ibin]
#    res.append(shape)
#  res[0].legendCoordinates=[0.62,0.5,.98,.95]
#  getLinesForStack(res, targetLumi)
#  return res

#def getHTBinStack(varstring, binning, cutstring, thisSample, htbins, varfunc = ""):
#  DATA          = variable(varstring, binning, cutstring)
#  DATA.sample   = data
##  DATA.color    = ROOT.kGray
#  DATA.color    = dataColor
#  DATA.legendText="Data"
#  MC_QCD                       = variable(varstring, binning, cutstring)
#  MC_QCD.minimum               = minimum 
#  MC_QCD.sample                = qcd 
#  MC                    = copy.deepcopy(MC_QCD)
#  MC.sample             = ttbarPowHeg 
#  MC_WJETS                     = copy.deepcopy(MC_QCD)
#  MC_WJETS.sample              = wjets 
#  MC_DY                     = copy.deepcopy(MC_QCD)
#  MC_DY.sample              = dy 
#
#  MC.legendText         = "TTJets"
#  MC.style              = "f"
#  MC.color              = ROOT.kRed - 3
#  MC.add                = [MC_WJETS]
#  MC_WJETS.legendText          = "WJets"
#  MC_WJETS.style               = "f"
#  MC_WJETS.add                 = [MC_QCD]
#  MC_WJETS.color               = ROOT.kYellow
#  MC_QCD.color                 = myBlue
#  MC_QCD.legendText            = "QCD"
#  MC_QCD.style                 = "f"
#  MC_QCD.add                   = [MC_DY]
#  MC_DY.legendText          = "DY + Jets"
#  MC_DY.style               = "f"
#  MC_DY.color               = ROOT.kGreen + 3
##  res = [MC_WJETS, MC_QCD, MC_DY, MC, DATA, ISO_DATA]
#  res = [MC, MC_WJETS, MC_QCD, MC_DY]
#
#  for ibin in range(len(htbins)):
#    print cutstring + htBin(*(htbins[ibin]))
#    shape = variable(varstring, binning, cutstring + htBin(*(htbins[ibin])))
#    shape.minimum = minimum
#    shape.sample = mc
#    shape.normalizeTo = res[0]
#    shape.legendText = legendName("HT", *(htbins[ibin])) 
#    shape.style="e"
#    shape.color = ROOT_colors[ibin] 
#    res.append(shape)
#    
#  getLinesForStack(res, targetLumi)
#  res[0].legendCoordinates=[0.62,0.5,.98,.95]
#  for var in res:
#    if varfunc!="":
#        var.varfunc = varfunc
#
#  return res

def getTTbarBinStack(varstring, binning, cutstring, thisSample, bins, bvar="ht", varfunc=""):
  MC                       = variable(varstring, binning, cutstring)
  MC.minimum               = minimum
  MC.sample                = thisSample 

  MC.legendText         = thisSample["name"]
  MC.style              = "f"
  MC.color              = ROOT.kRed - 3
  res = [MC]

  for ibin in range(len(bins)):
    print cutstring + varBin(*(bins[ibin]), var=bvar)
    shape = variable(varstring, binning, cutstring + varBin(*(bins[ibin]), var=bvar))
    shape.minimum = minimum
    shape.sample = MC.sample
    shape.normalizeTo = res[0]
    shape.legendText = legendName(bvar, *(bins[ibin])) 
    shape.style="e"
    shape.color = ROOT_colors[ibin] 
    res.append(shape)
    
  getLinesForStack(res, targetLumi)
  res[0].legendCoordinates=[0.62,0.5,.98,.95]
  getLinesForStack(res, targetLumi)
  
  if varfunc!="":
    for var in res:
      var.varfunc = varfunc
  return res

#met_stack = getStack(":RA4Events.met;#slash{E}_{T} [GeV];Number of Events / 5 GeV",[77,0,385], commoncf, thisSample, topIsLargest)
#allStacks.append(met_stack)
if mode=="Mu":
  singleGenLepCut = "antinuMu+nuMu==1&&antinuE+nuE+antinuTau+nuTau==0"
if mode=="Ele":
  singleGenLepCut = "antinuE+nuE==1&&antinuMu+nuMu+antinuTau+nuTau==0"

#bins = [ [0,400], [400,500], [500,600], [600,700], [700,800], [800,-1] ]
#bins = [ [0,400], [400,800], [800,-1] ]
#mtFunc = matchedMTtrue

#mTGenMet_zoomed_stack  = getTTbarBinStack(":xx;genMet -> m_{T} [GeV];Number of Events / 20 GeV",[15,0,300], commoncf+"&&"+singleGenLepCut, thisSample, htBins, mTGenMet)
#allStacks.append(mTGenMet_zoomed_stack)
#
#mTGenMet_stack  = getTTbarBinStack(":xx;genMet -> m_{T} [GeV];Number of Events / 50 GeV",[21,0,1050], commoncf+"&&"+singleGenLepCut, thisSample, htBins,  mTGenMet)
#allStacks.append(mTGenMet_stack)
#

#binVar = "met"
##bins = [ [100,150], [150,200], [200,250], [250,350], [350,450], [450,-1] ]
#bins = [ [100,200], [200,300], [300, -1] ]
binVar = "ht"
bins = [ [300, 400], [400,800], [800,-1] ]


mTGenFunc = getMTGenFunc(mode, thisSample["name"])
mTGen_stack = getTTbarBinStack(":xx;gen m_{T} [GeV];Number of Events / 50 GeV",[21,0,1050], commoncf+"&&"+singleGenLepCut, thisSample, bins, binVar, mTGenFunc)
allStacks.append(mTGen_stack)

mTGen_zoomed_stack = getTTbarBinStack(":xx;gen m_{T} [GeV];Number of Events / 20 GeV",[15,0,300], commoncf+"&&"+singleGenLepCut, thisSample, bins, binVar, mTGenFunc)
allStacks.append(mTGen_zoomed_stack)

mTGen_zoomed2_stack = getTTbarBinStack(":xx;gen m_{T} [GeV];Number of Events / 3 GeV",[40,35,155], commoncf+"&&"+singleGenLepCut, thisSample, bins, binVar, mTGenFunc)
allStacks.append(mTGen_zoomed2_stack)

mTGen_zoomed3_stack = getTTbarBinStack(":xx;gen m_{T} [GeV];Number of Events / 5 GeV",[22,35,155], commoncf+"&&"+singleGenLepCut, thisSample, bins, binVar, mTGenFunc)
allStacks.append(mTGen_zoomed3_stack)

mTGen_zoomed4_stack = getTTbarBinStack(":xx;gen m_{T} [GeV];Number of Events / 10 GeV",[11,35,155], commoncf+"&&"+singleGenLepCut, thisSample, bins, binVar, mTGenFunc)
allStacks.append(mTGen_zoomed4_stack)

##htBins = [ [0,400], [400,500], [500,600], [600,700], [700,800], [800,-1] ] #fine
#mGenFunc = getMGenFunc(mode)
#
#mGen_stack  = getTTbarBinStack(":xx;gen m [GeV];Number of Events / 50 GeV",[21,0,1050], commoncf+"&&"+singleGenLepCut, thisSample, bins, binVar,   mGenFunc)
#allStacks.append(mGen_stack)
#
#mGen_zoomed_stack  = getTTbarBinStack(":xx;gen m [GeV];Number of Events / 20 GeV",[15,0,300], commoncf+"&&"+singleGenLepCut, thisSample, bins, binVar,  mGenFunc)
#allStacks.append(mGen_zoomed_stack)
#
#mGen_zoomed2_stack  = getTTbarBinStack(":xx;gen m [GeV];Number of Events / 3 GeV",[40,35,155], commoncf+"&&"+singleGenLepCut, thisSample, bins, binVar,  mGenFunc)
#allStacks.append(mGen_zoomed2_stack)
#
#mGen_zoomed3_stack  = getTTbarBinStack(":xx;gen m [GeV];Number of Events / 5 GeV",[22,35,155], commoncf+"&&"+singleGenLepCut, thisSample, bins, binVar,  mGenFunc)
#allStacks.append(mGen_zoomed3_stack)
#
#mGen_zoomed4_stack  = getTTbarBinStack(":xx;gen m [GeV];Number of Events / 10 GeV",[11,35,155], commoncf+"&&"+singleGenLepCut, thisSample, bins, binVar,  mGenFunc)
#allStacks.append(mGen_zoomed4_stack)

#
#mT_stack  = getTTbarBinStack(":mT;m_{T} [GeV];Number of Events / 50 GeV",[21,0,1050], commoncf+"&&"+singleGenLepCut, thisSample, htBins)
#allStacks.append(mT_stack)
#
#mT_zoomed_stack  = getTTbarBinStack(":mT;m_{T} [GeV];Number of Events / 20 GeV",[15,0,300], commoncf+"&&"+singleGenLepCut, thisSample, htBins)
#allStacks.append(mT_zoomed_stack)


  
#njetbins = [2,3,4,5]
#mT_htStacks=[]
#for bin in htBins:
#  mT_stack_ht  = getNJetStack(":RA4Events.mT;m_{T} [GeV];Number of Events / 5 GeV",[77,0,385], commoncf + htBin(*bin), thisSample, njetbins,  topIsLargest)
#  allStacks.append(mT_stack_ht)
#  mT_htStacks.append(mT_stack_ht)

execfile("simplePlotsLoopKernel.py")
for stack in allStacks:
  stack[0].maximum = 3*10**4 
  stack[0].minimum = stack[0].minimum 

#drawNMStacks(1,1,[mT_stack],              subdir+"/"+prefix+"mT.png", False)
#drawNMStacks(1,1,[mT_zoomed_stack],              subdir+"/"+prefix+"zoomed_mT.png", False)
#drawNMStacks(1,1,[mTGenMet_stack],              subdir+"/"+prefix+"mTGenMet.png", False)
#drawNMStacks(1,1,[mTGenMet_zoomed_stack],              subdir+"/"+prefix+"zoomed_mTGenMet.png", False)

drawNMStacks(1,1,[mTGen_stack],                      subdir+"/"+prefix+"_"+thisSample["name"]+"_mTGen.png", False)
drawNMStacks(1,1,[mTGen_zoomed_stack],               subdir+"/"+prefix+"_"+thisSample["name"]+"_zoomed_mTGen.png", False)
drawNMStacks(1,1,[mTGen_zoomed2_stack],              subdir+"/"+prefix+"_"+thisSample["name"]+"_zoomed2_mTGen.png", False)
drawNMStacks(1,1,[mTGen_zoomed3_stack],              subdir+"/"+prefix+"_"+thisSample["name"]+"_zoomed3_mTGen.png", False)
drawNMStacks(1,1,[mTGen_zoomed4_stack],              subdir+"/"+prefix+"_"+thisSample["name"]+"_zoomed4_mTGen.png", False)
#drawNMStacks(1,1,[mGen_stack],              subdir+"/"+prefix+"mGen.png", False)
#drawNMStacks(1,1,[mGen_zoomed_stack],              subdir+"/"+prefix+"zoomed_mGen.png", False)
#drawNMStacks(1,1,[mGen_zoomed2_stack],              subdir+"/"+prefix+"zoomed2_mGen.png", False)
#drawNMStacks(1,1,[mGen_zoomed3_stack],              subdir+"/"+prefix+"zoomed3_mGen.png", False)
#drawNMStacks(1,1,[mGen_zoomed4_stack],              subdir+"/"+prefix+"zoomed4_mGen.png", False)
#for i in range(5):
#  drawNMStacks(1,1,[mT_jetStacks[i]],     "pngPAT/"+prefix+"mT_njet_"+str(i)+".png", False)
#for i in range(len(htBins)):
#  drawNMStacks(1,1,[mT_htStacks[i]],     "pngPAT/"+prefix+"mT_njet__ht_"+str(htBins[i][0])+"_"+str(htBins[i][1])+".png", False)

