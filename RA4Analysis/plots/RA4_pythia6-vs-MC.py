import ROOT
from array import array
from math import *
import os, copy

from simplePlotsCommon import *
from funcs import *

import xsec
small = False

from defaultMuSamples import *


allVars=[]
allStacks=[]

signalColors = [ROOT.kBlack, ROOT.kBlue + 1, ROOT.kGreen + 2, ROOT.kOrange + 2]

## plots for studying pythia MC 
topOrW = False
doOnlyMET = False
normalizeToPYTHIA = True

preprefix="pythia6-vs-MC-Mu-ht300-genmet50"
if topOrW:
  preprefix="TT_"+preprefix
else:
  preprefix="W_"+preprefix

if topOrW:
  allSamples = [pythia6TT, ttbar]
  pythia6TT["Chain"] = "RA4MCAnalyzer/Events"
  ttbar["Chain"] = "RA4MCAnalyzer/Events"
  ttbar["name"] = "TT-Jets MG"
  
else:
  allSamples = [pythia6W, wjets]
  pythia6W["Chain"] = "RA4MCAnalyzer/Events"
  wjets["Chain"] = "RA4MCAnalyzer/Events"
  wjets["name"] = "W-Jets MG"

additionalCut = "ht>300&&genmet>50"
#WJETS_scale = 1.78226347114  #met>25
presel = "pf-3j40"
subdir = "/pngMC/"
minimum=10**(-0.5)


commoncf = "(0)"
prefix="empty_"

if presel == "pf-3j40":
  commoncf = "jet1pt>40&&jet2pt>40&&lepton_pt>20&&singleMuonic"

if additionalCut!="":
  commoncf+="&&"+additionalCut

prefix= "RA4_"+presel+"_"
if preprefix!="":
  prefix = preprefix+"_"+presel+"_"


def getStack(varstring, binning, cutstring, topOrW = True, varfunc = ""):
  pythiaSample = pythia6W
  MCSample = wjets
  if topOrW:
    pythiaSample = pythia6TT
    MCSample = ttbar

  PYTHIA          = variable(varstring, binning, cutstring)
  PYTHIA.sample   = pythiaSample 
  PYTHIA.color    = dataColor
  PYTHIA.legendText= pythiaSample["name"]
  PYTHIA.style              = "l02"

  MC                       = variable(varstring, binning, cutstring)
  MC.minimum               = 5*10**(-1)
  MC.sample                = MCSample 
  MC.color                 = myBlue
  MC.legendText            = MCSample["name"]
  MC.style                 = "f0"

  res=[MC, PYTHIA]
  res[0].dataMCRatio = [PYTHIA, res[0]]

  nhistos = len(res)
  for var in res:
    var.legendCoordinates=[0.61,0.95 - 0.08*2,.98,.95]
  if varfunc!="":
    for var in res:
      var.varfunc = varfunc
  return res

genmet_stack = getStack(":genmet;#slash{E}_{T} (GeV);Number of Events / 25 GeV",[21,0,525], commoncf, topOrW)
genmet_stack[0].addOverFlowBin = "upper"
allStacks.append(genmet_stack)

if not doOnlyMET:

  jet0_pt_stack                     = getStack(":jet0pt;p_{T} of leading jet (GeV);Number of Events / 30 GeV",[27,10,820], commoncf, topOrW)
  jet0_pt_stack[0].addOverFlowBin = "upper"
  allStacks.append(jet0_pt_stack)
  jet1_pt_stack                     = getStack(":jet1pt;p_{T} of 2^{nd} leading jet (GeV);Number of Events / 30 GeV",[27,10,810], commoncf, topOrW)
  jet1_pt_stack[0].addOverFlowBin = "upper"
  allStacks.append(jet1_pt_stack)
  jet2_pt_stack                     = getStack(":jet2pt;p_{T} of 3^{rd} leading jet (GeV);Number of Events / 30 GeV",[27,10,810], commoncf, topOrW)
  jet2_pt_stack[0].addOverFlowBin = "upper"
  allStacks.append(jet2_pt_stack)
  jet3_pt_stack                     = getStack(":jet3pt;p_{T} of 4^{th} leading jet (GeV);Number of Events / 30 GeV",[27,10,810], commoncf+"&&jet3pt>0", topOrW)
  jet3_pt_stack[0].addOverFlowBin = "upper"
  allStacks.append(jet3_pt_stack)

  kinMetSig_stack                   = getStack(":kinMetSig;S_{MET};Number of Events",[25,0,25], commoncf, topOrW)
  kinMetSig_stack[0].addOverFlowBin = "upper"
  allStacks.append(kinMetSig_stack)

  mT_stack  = getStack(":mT;m_{T} (GeV);Number of Events / 20 GeV",[27,0,540], commoncf, topOrW)
  mT_stack[0].addOverFlowBin = "upper"
  allStacks.append(mT_stack)

  ht_stack                          = getStack(":ht;H_{T} (GeV);Number of Events / 50 GeV",[35,0,1750], commoncf, topOrW)
  ht_stack[0].addOverFlowBin = "upper"
  allStacks.append(ht_stack)

  m3_stack = getStack(":m3;M_{3} (GeV);Number of Events / 30 GeV",[51,0,1530], commoncf, topOrW)
  m3_stack[0].addOverFlowBin = "upper"
  allStacks.append(m3_stack)

  lepton_pt_stack = getStack("p_{T} (GeV):lepton_pt;p_{T,lep.} (GeV);Number of Events / 20 GeV",[26,0,520], commoncf, topOrW)
  lepton_pt_stack[0].addOverFlowBin = "upper"
  allStacks.append(lepton_pt_stack)

  lepton_eta_stack                  = getStack(":lepton_eta;|#eta^{#mu}|;Number of Events",[62,-3.1,3.1], commoncf, topOrW)
  lepton_eta_stack[0].addOverFlowBin = "both"
  allStacks.append(lepton_eta_stack)
  
  ngoodElectrons_stack = getStack("ngoodElectrons :ngoodElectrons;Number of electrons;Number of Events",[5,0,5], commoncf.replace("singleMuonic&&nvetoMuons==1&&nvetoElectrons==0", "ngoodMuons==1&&nvetoMuons==1"), topOrW)
  ngoodElectrons_stack[0].addOverFlowBin = "upper"
  allStacks.append(ngoodElectrons_stack)

  ngoodMuons_stack = getStack("ngoodMuons :ngoodMuons;Number of muons;Number of Events",[5,0,5], commoncf.replace("singleMuonic&&nvetoMuons==1", "ngoodMuons>0"), topOrW)
  ngoodMuons_stack[0].addOverFlowBin = "upper"
  allStacks.append(ngoodMuons_stack)



for stack in allStacks:
  stack[0].minimum = minimum

execfile("simplePlotsKernel.py")

if normalizeToPYTHIA:
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

for stack in allStacks:
#  stack[0].maximum = 10.*stack[-1].data_histo.GetMaximum()
  stack[0].logy = True
  stack[0].minimum = minimum
#  stack[0].legendCoordinates=[0.76,0.95 - 0.3,.98,.95]
#  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS preliminary}"], [0.2,0.85,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 7 TeV"]]
  stack[0].legendCoordinates=[0.61,0.95 - 0.08*2,.98,.95]
  stack[0].lines = []

drawNMStacks(1,1,[genmet_stack],             subdir+prefix+"genmet.png", False)

if not doOnlyMET:
  drawNMStacks(1,1,[mT_stack],              subdir+prefix+"mT.png", False)
  drawNMStacks(1,1,[kinMetSig_stack],       subdir+prefix+"kinMetSig.png", False)
  drawNMStacks(1,1,[ht_stack],              subdir+prefix+"ht.png", False)
#  drawNMStacks(1,1,[ht2had_stack],          subdir+prefix+"ht2had.png", False)
#  drawNMStacks(1,1,[ht2_stack],             subdir+prefix+"ht2.png", False)
  drawNMStacks(1,1,[jet0_pt_stack],         subdir+prefix+"jet0_pt.png", False)
  drawNMStacks(1,1,[jet1_pt_stack],         subdir+prefix+"jet1_pt.png", False)
  drawNMStacks(1,1,[jet2_pt_stack],         subdir+prefix+"jet2_pt.png", False)
  drawNMStacks(1,1,[jet3_pt_stack],         subdir+prefix+"jet3_pt.png", False)
  drawNMStacks(1,1,[m3_stack],              subdir+prefix+"m3.png", False)
  drawNMStacks(1,1,[lepton_pt_stack],       subdir+prefix+"lepton_pt.png", False)
  drawNMStacks(1,1,[lepton_eta_stack],                  subdir+prefix+"lepton_eta.png", False)
  drawNMStacks(1,1,[ngoodElectrons_stack],  subdir+prefix+"ngoodElectrons.png", False)
  drawNMStacks(1,1,[ngoodMuons_stack],  subdir+prefix+"ngoodMuons.png", False)


for stack in allStacks:
#  stack[0].maximum = 1.3*stack[-1].data_histo.GetMaximum()
  stack[0].logy = False
  stack[0].minimum=0
  
drawNMStacks(1,1,[genmet_stack],             subdir+prefix+"genmet_lin.png", False)

if not doOnlyMET:
  drawNMStacks(1,1,[mT_stack],              subdir+prefix+"mT_lin.png", False)
  drawNMStacks(1,1,[kinMetSig_stack],       subdir+prefix+"kinMetSig_lin.png", False)
  drawNMStacks(1,1,[ht_stack],              subdir+prefix+"ht_lin.png", False)
  drawNMStacks(1,1,[jet0_pt_stack],         subdir+prefix+"jet0_pt_lin.png", False)
  drawNMStacks(1,1,[jet1_pt_stack],         subdir+prefix+"jet1_pt_lin.png", False)
  drawNMStacks(1,1,[jet2_pt_stack],         subdir+prefix+"jet2_pt_lin.png", False)
  drawNMStacks(1,1,[jet3_pt_stack],         subdir+prefix+"jet3_pt_lin.png", False)
  drawNMStacks(1,1,[m3_stack],              subdir+prefix+"m3_lin.png", False)
  drawNMStacks(1,1,[lepton_pt_stack],       subdir+prefix+"lepton_pt_lin.png", False)
  drawNMStacks(1,1,[lepton_eta_stack],                  subdir+prefix+"lepton_eta_lin.png", False)
  drawNMStacks(1,1,[ngoodElectrons_stack],  subdir+prefix+"ngoodElectrons_lin.png", False)
  drawNMStacks(1,1,[ngoodMuons_stack],  subdir+prefix+"ngoodMuons_lin.png", False)
