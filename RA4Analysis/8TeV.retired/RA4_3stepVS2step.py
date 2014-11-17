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

## plots for studying pythia MC 
doOnlyMET = True
normalize = True


##WJets Comparison
#preprefix="WJetsToLnu-vs-WJetsHT300-ht400"
#additionalCut = "ht>300"
#wjetsHT300 = copy.deepcopy(wjets)
#wjetsHT300["bins"] = ["WJets-HT300"]
#wjetsHT300["name"] = "WJets-HT300"
#wjets["name"] = "WJets"
#allSamples = [wjets, wjetsHT300]

# TTJets 3-step/2-step comparison
preprefix="3-step-VS-2-step"
ttjets3step = copy.deepcopy(ttbar)
ttjets3step["name"] = "TTJets 3-step"
ttjets3step["dirname"] = "/scratch/schoef/pat_110924/Mu/"
ttjets3step["Chain"] = "pfRA4Analyzer/Events"
xsec.xsec['"TTJets 3-step"'] = xsec.xsec['TTJets']
ttjets2step = copy.deepcopy(ttbar)
ttjets2step["name"] = "TTJets 2-step"
ttjets2step["Chain"] = "Events"
ttjets2step["dirname"] = "/scratch/schoef/pat_111019/Mu/"
ttjets2step["hasCountingHLTFilter"] = False
#xsec.xsec['"TTJets 2-step"'] = xsec.xsec['TTJets']
sample1 = ttjets3step
sample2 = ttjets2step
allSamples = [sample1, sample2]
commoncfSample1 = "jet1pt>40&&jet2pt>40&&lepton_pt>20&&singleMuonic&&nvetoMuons==1&&nvetoElectrons==0"#&&ht>300&&barepfmet>300"
commoncfSample2 = "pfRA4Tupelizer_jet2pt>40&&pfRA4Tupelizer_singleMuonic&&pfRA4Tupelizer_nvetoMuons==1&&pfRA4Tupelizer_nvetoElectrons==0"#&&pfRA4Tupelizer_ht>300&&pfRA4Tupelizer_barepfmet>300"

### TTJets TotalKinematicsFilter comparison 
#preprefix="TKF"
#ttjetsTKF = copy.deepcopy(ttbar)
#ttjetsTKF["name"] = "TTJets TKF"
#ttjetsTKF["dirname"] = "/scratch/schoef/pat_111020/Mu/"
#ttjetsTKF["Chain"] = "Events"
#ttjetsTKF["hasCountingHLTFilter"] = False
#ttjets = copy.deepcopy(ttbar)
#ttjets["name"] = "TTJets"
#ttjets["Chain"] = "Events"
#ttjets["dirname"] = "/scratch/schoef/pat_111019/Mu/"
#ttjets["hasCountingHLTFilter"] = False
#sample1 = ttjetsTKF
#sample2 = ttjets
#allSamples = [sample1, sample2]
#commoncfSample1 = "pfRA4Tupelizer_jet2pt>40&&pfRA4Tupelizer_singleMuonic&&pfRA4Tupelizer_nvetoMuons==1&&pfRA4Tupelizer_nvetoElectrons==0"#&&pfRA4Tupelizer_ht>300&&pfRA4Tupelizer_barepfmet>300"
#commoncfSample2 = "pfRA4Tupelizer_jet2pt>40&&pfRA4Tupelizer_singleMuonic&&pfRA4Tupelizer_nvetoMuons==1&&pfRA4Tupelizer_nvetoElectrons==0"#&&pfRA4Tupelizer_ht>300&&pfRA4Tupelizer_barepfmet>300"

presel = "pf-3j40"
subdir = "/pngMC/"
minimum=10**(-1.5)

prefix = preprefix+"_"


def getStack(varstring1, varstring2, binning, cutstring1, cutstring2):#, varfunc = ""):

  SAMPLE2          = variable(varstring2, binning, cutstring2)
  SAMPLE2.sample   = sample2 
  SAMPLE2.color    = dataColor
  SAMPLE2.legendText=sample2["name"] 
  SAMPLE2.style              = "l12"

  SAMPLE1                       = variable(varstring1, binning, cutstring1)
  SAMPLE1.minimum               = minimum
  SAMPLE1.sample                = sample1 
  SAMPLE1.color                 = myBlue
  SAMPLE1.legendText            = sample1["name"]
  SAMPLE1.style                 = "f"

  res=[SAMPLE1, SAMPLE2]
  res[0].dataMCRatio = [SAMPLE1, res[1]]

  nhistos = len(res)
  for var in res:
    var.legendCoordinates=[0.61,0.95 - 0.08*2,.98,.95]
#  if varfunc!="":
#    for var in res:
#      var.varfunc = varfunc
  return res

lepton_deltaR_stack = getStack(":lepton_deltaR; #Delta_{R} ;Number of Events / 25 GeV","pfRA4Tupelizer_leptonDeltaR", [50,0,5], commoncfSample1,commoncfSample2)
lepton_deltaR_stack[0].addOverFlowBin = "upper"
allStacks.append(lepton_deltaR_stack)

lepton_deltaR_zoomed_stack = getStack(":lepton_deltaR; #Delta_{R} ;Number of Events / 25 GeV","pfRA4Tupelizer_leptonDeltaR", [50,0,1], commoncfSample1,commoncfSample2)
lepton_deltaR_zoomed_stack[0].addOverFlowBin = "upper"
allStacks.append(lepton_deltaR_zoomed_stack)

if not doOnlyMET:
  met_stack = getStack(":barepfmet;#slash{E}_{T} (GeV);Number of Events / 25 GeV","pfRA4Tupelizer_barepfmet", [25,0,625], commoncfSample1,commoncfSample2)
  met_stack[0].addOverFlowBin = "upper"
  allStacks.append(met_stack)

  genmet_stack = getStack(":genmet;generator #slash{E}_{T} (GeV);Number of Events / 25 GeV","pfRA4Tupelizer_genmet", [25,0,625], commoncfSample1,commoncfSample2)
  genmet_stack[0].addOverFlowBin = "upper"
  allStacks.append(genmet_stack)

  jet0_pt_stack                     = getStack(":jet0pt;p_{T} of leading jet (GeV);Number of Events / 30 GeV", "pfRA4Tupelizer_jet0pt",[27,10,820], commoncfSample1,commoncfSample2)
  jet0_pt_stack[0].addOverFlowBin = "upper"
  allStacks.append(jet0_pt_stack)
  jet1_pt_stack                     = getStack(":jet1pt;p_{T} of 2^{nd} leading jet (GeV);Number of Events / 30 GeV", "pfRA4Tupelizer_jet1pt",[27,10,810], commoncfSample1,commoncfSample2)
  jet1_pt_stack[0].addOverFlowBin = "upper"
  allStacks.append(jet1_pt_stack)
  jet2_pt_stack                     = getStack(":jet2pt;p_{T} of 3^{rd} leading jet (GeV);Number of Events / 30 GeV", "pfRA4Tupelizer_jet2pt",[27,10,810], commoncfSample1,commoncfSample2)
  jet2_pt_stack[0].addOverFlowBin = "upper"
  allStacks.append(jet2_pt_stack)
  jet3_pt_stack                     = getStack(":jet3pt;p_{T} of 4^{th} leading jet (GeV);Number of Events / 30 GeV", "pfRA4Tupelizer_jet3pt",[27,10,810], commoncfSample1+"&&jet3pt>0",commoncfSample2+"&&pfRA4Tupelizer_jet3pt>0")
  jet3_pt_stack[0].addOverFlowBin = "upper"
  allStacks.append(jet3_pt_stack)

  kinMetSig_stack                   = getStack(":kinMetSig;S_{MET};Number of Events", "pfRA4Tupelizer_kinMetSig", [25,0,25], commoncfSample1,commoncfSample2)
  kinMetSig_stack[0].addOverFlowBin = "upper"
  allStacks.append(kinMetSig_stack)

  mT_stack  = getStack(":mT;m_{T} (GeV);Number of Events / 20 GeV","pfRA4Tupelizer_mT", [27,0,540], commoncfSample1,commoncfSample2)
  mT_stack[0].addOverFlowBin = "upper"
  allStacks.append(mT_stack)

  ht_stack                          = getStack(":ht;H_{T} (GeV);Number of Events / 50 GeV","pfRA4Tupelizer_ht", [35,0,1750], commoncfSample1,commoncfSample2)
  ht_stack[0].addOverFlowBin = "upper"
  allStacks.append(ht_stack)

  m3_stack = getStack(":m3;M_{3} (GeV);Number of Events / 30 GeV","pfRA4Tupelizer_m3", [51,0,1530], commoncfSample1,commoncfSample2)
  m3_stack[0].addOverFlowBin = "upper"
  allStacks.append(m3_stack)

  lepton_pt_stack = getStack("p_{T} (GeV):lepton_pt;p_{T,lep.} (GeV);Number of Events / 20 GeV","pfRA4Tupelizer_leptonPt", [26,0,520], commoncfSample1,commoncfSample2)
  lepton_pt_stack[0].addOverFlowBin = "upper"
  allStacks.append(lepton_pt_stack)

  lepton_eta_stack                  = getStack(":lepton_eta;|#eta^{#mu}|;Number of Events","pfRA4Tupelizer_leptonEta", [62,-3.1,3.1], commoncfSample1,commoncfSample2)
  lepton_eta_stack[0].addOverFlowBin = "both"
  allStacks.append(lepton_eta_stack)
  
  ngoodElectrons_stack = getStack("ngoodElectrons :ngoodElectrons;Number of electrons;Number of Events","pfRA4Tupelizer_ngoodElectrons", [5,0,5],\
     commoncfSample1.replace("singleMuonic&&nvetoMuons==1&&nvetoElectrons==0", "ngoodMuons==1&&nvetoMuons==1"),
     commoncfSample2.replace("pfRA4Tupelizer_singleMuonic&&pfRA4Tupelizer_nvetoMuons==1&&pfRA4Tupelizer_nvetoElectrons==0", "pfRA4Tupelizer_ngoodMuons==1&&pfRA4Tupelizer_nvetoMuons==1"))
  ngoodElectrons_stack[0].addOverFlowBin = "upper"
  allStacks.append(ngoodElectrons_stack)

  ngoodMuons_stack = getStack("ngoodMuons :ngoodMuons;Number of muons;Number of Events","pfRA4Tupelizer_ngoodMuons", [5,0,5],\
     commoncfSample1.replace("singleMuonic&&nvetoMuons==1", "ngoodMuons>0"),
     commoncfSample2.replace("pfRA4Tupelizer_singleMuonic&&pfRA4Tupelizer_nvetoMuons==1", "pfRA4Tupelizer_ngoodMuons>0"))
  ngoodMuons_stack[0].addOverFlowBin = "upper"
  allStacks.append(ngoodMuons_stack)


for stack in allStacks:
  stack[0].minimum = minimum

execfile("simplePlotsKernel.py")

if normalize:
  for stack in allStacks:
#    for var in stack[:-1]:
#      var.normalizeTo = stack[-1]
#      var.normalizeWhat = stack[0]
    stack[-1].normalizeTo=stack[0]
    stack[-1].normalizeWhat=stack[-1]
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


drawNMStacks(1,1,[lepton_deltaR_stack],             subdir+prefix+"lepton_deltaR.png", False)
drawNMStacks(1,1,[lepton_deltaR_zoomed_stack],             subdir+prefix+"lepton_deltaR_zoomed.png", False)
if not doOnlyMET:
  drawNMStacks(1,1,[met_stack],             subdir+prefix+"met.png", False)
  drawNMStacks(1,1,[genmet_stack],             subdir+prefix+"genmet.png", False)
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

drawNMStacks(1,1,[lepton_deltaR_stack],             subdir+prefix+"lepton_deltaR_lin.png", False)
drawNMStacks(1,1,[lepton_deltaR_zoomed_stack],             subdir+prefix+"lepton_deltaR_zoomed_lin.png", False)
if not doOnlyMET:
  drawNMStacks(1,1,[met_stack],             subdir+prefix+"met_lin.png", False)
  drawNMStacks(1,1,[genmet_stack],             subdir+prefix+"genmet_lin.png", False)
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
