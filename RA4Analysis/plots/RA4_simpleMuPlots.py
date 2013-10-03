import ROOT
from array import array
from math import *
import os, copy

from simplePlotsCommon import *

import xsec
small = False

from defaultMu2012Samples import *
allVars=[]
allStacks=[]

signalColors = [ROOT.kBlack, ROOT.kBlue + 1, ROOT.kGreen + 2, ROOT.kOrange + 2]

## plots for studying preselection 
topIsLargest = True
minimum=10**(-0.5)

#WJETS_scale = 1.34068264918  #met>25
WJETS_scale = 1.0
subdir = "/8TeV/"
#additionalCut = "ht>900"
#preprefix = "ht900"
#additionalCut = "ht>300&&ht<900"
#preprefix = "ht300-900"
#additionalCut = "kinMetSig>9"
#preprefix = "kMs9"
#additionalCut = "kinMetSig>2.5&&kinMetSig<9"
#preprefix = "kMs2.5-9"
additionalCut = ""
preprefix = ""
presel = 
signalNumbers = [6, 9]

floatWJets = False
doOnlyMET = True
#floatWJets = True

chainstring = "empty"
commoncf = "(0)"
prefix="empty_"


if presel == "3j40":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "jet2pt>30&&lepton_pt>15&&singleMuonic&&nvetoMuons==1&&nvetoElectrons==0"

if additionalCut!="":
  commoncf+="&&"+additionalCut

prefix= "RA4_"+presel+"_"
if preprefix!="":
  prefix = preprefix+"_"+presel+"_"

for sample in allSamples:
  sample["Chain"] = chainstring

def getStack(varstring, binning, cutstring, signalNumbers, topIsLargest = False):
#  DATA          = variable(varstring, binning, cutstring)
#  DATA.sample   = data
##  DATA.color    = ROOT.kGray
#  DATA.color    = dataColor
#  DATA.legendText="Data"

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
#  res.append(DATA)
  return res


#met_stack = getStack(":met;#slash{E}_{T} (GeV);Number of Events / 40 GeV",[17,0,680], commoncf, signalNumbers, topIsLargest)
#allStacks.append(met_stack)
genmet_stack = getStack(":genmet;gen-#slash{E}_{T} (GeV);Number of Events / 15 GeV",[20,0,300], commoncf, signalNumbers, topIsLargest)
allStacks.append(genmet_stack)
if not doOnlyMET:
#  mT_stack  = getStack(":mT;m_{T} (GeV);Number of Events / 20 GeV",[13,0,260], commoncf, signalNumbers, topIsLargest)
#  allStacks.append(mT_stack)

  jet0_pt_stack                     = getStack(":jet0pt;p_{T} of leading jet (GeV);Number of Events / 20 GeV",[25,20,520], commoncf, signalNumbers, topIsLargest)
  allStacks.append(jet0_pt_stack)
  jet1_pt_stack                     = getStack(":jet1pt;p_{T} of 2^{nd} leading jet (GeV);Number of Events / 20 GeV",[15,20,320], commoncf, signalNumbers, topIsLargest)
  allStacks.append(jet1_pt_stack)
  jet2_pt_stack                     = getStack(":jet2pt;p_{T} of 3^{rd} leading jet (GeV);Number of Events / 20 GeV",[15,10,310], commoncf, signalNumbers, topIsLargest)
  allStacks.append(jet2_pt_stack)
  jet3_pt_stack                     = getStack(":jet3pt;p_{T} of 4^{th} leading jet (GeV);Number of Events / 20 GeV",[15,10,310], commoncf, signalNumbers, topIsLargest)
  allStacks.append(jet3_pt_stack)
  kinMetSig_stack                   = getStack(":kinMetSig;S_{MET};Number of Events",[16,0,16], commoncf, signalNumbers, topIsLargest)
  allStacks.append(kinMetSig_stack)
  ht_stack                          = getStack(":ht;H_{T} (GeV);Number of Events / 70 GeV",[25,0,1750], commoncf, signalNumbers, topIsLargest)
  allStacks.append(ht_stack)
#  ht2had_stack                      = getStack(":ht2;H_{T2}^{had.} (GeV);Number of Events / 30 GeV",[27,0,810], commoncf, signalNumbers, topIsLargest)
#  allStacks.append(ht2had_stack)
#  ht2_stack                         = getStack(":ht2+lepton_pt;H_{T2} (GeV);Number of Events / 30 GeV",[27,0,810], commoncf, signalNumbers, topIsLargest)
#  allStacks.append(ht2_stack)

  m3_stack = getStack(":m3;M_{3} (GeV);Number of Events / 30 GeV",[27,0,810], commoncf, signalNumbers, topIsLargest)
  allStacks.append(m3_stack)

  lepton_pt_stack = getStack("p_{T} (GeV):lepton_pt;p_{T,lep.} (GeV);Number of Events / 20 GeV",[15,15,315], commoncf, signalNumbers, topIsLargest)
  allStacks.append(lepton_pt_stack)
#  lepton_eta_stack                  = getStack(":lepton_eta;|#eta^{#mu}|;Number of Events",[31,0,3.1], commoncf, signalNumbers, topIsLargest)
#  allStacks.append(lepton_eta_stack)
#
#  lepton_dxy_stack                  = getStack(":lepton_dxy;d_{xy};Number of Events / 10 #mu m",[40,0,0.04], commoncf, signalNumbers, topIsLargest)
#  allStacks.append(lepton_dxy_stack)
#  lepton_vertex_dxy_stack                  = getStack(":lepton_vertex_dxy;d_{xy};Number of Events / 10 #mu m",[40,0,0.04], commoncf, signalNumbers, topIsLargest)
#  allStacks.append(lepton_vertex_dxy_stack)
#  lepton_vertex_dz_stack                  = getStack(":lepton_vertex_dz;d_{z, V};Number of Events / 10 #mu m",[40,-.201,.201], commoncf, signalNumbers, topIsLargest)
#  allStacks.append(lepton_vertex_dz_stack)
#
#  lepton_relIso_stack               = getStack(":lepton_relIso;relIso;Number of Events",[15,0,0.1], commoncf, signalNumbers, topIsLargest)
#  lepton_relIso_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(lepton_relIso_stack)
#
#  lepton_deltaR_stack          = getStack(":lepton_deltaR;#Delta R(l,jets);Number of Events",[30,0,6.28], commoncf, signalNumbers, topIsLargest)
#  allStacks.append(lepton_deltaR_stack)

for stack in allStacks:
  stack[0].minimum = minimum

#btag0_stack                   = getStack(":btag0;leading SSV_{HE};Number of Events",[30,-1,6.], commoncf, signalNumbers, topIsLargest)
#btag0_stack[0].minimum = 10**(-2)
#btag0_stack[0].legendCoordinates[0] = 0.25
#btag0_stack[0].legendCoordinates[2] = 0.25+0.23
#allStacks.append(btag0_stack)
#btag1_stack                   = getStack(":btag1;n-leading SSV_{HE};Number of Events",[30,-1,6.], commoncf, signalNumbers, topIsLargest)
#btag1_stack[0].minimum = 10**(-2)
#btag1_stack[0].legendCoordinates[0] = 0.25
#btag1_stack[0].legendCoordinates[2] = 0.25+0.23
#allStacks.append(btag1_stack)
#btag2_stack                   = getStack(":btag2;n^{2}-leading SSV_{HE};Number of Events",[30,-1,6.], commoncf, signalNumbers, topIsLargest)
#btag2_stack[0].minimum = 10**(-2)
#btag2_stack[0].legendCoordinates[0] = 0.25
#btag2_stack[0].legendCoordinates[2] = 0.25+0.23
#allStacks.append(btag2_stack)
#jet0btag_stack                   = getStack(":jet0btag;SSV_{HE} of j_{0};Number of Events",[30,-1,6.], commoncf, signalNumbers, topIsLargest)
#jet0btag_stack[0].minimum = 10**(-2)
#jet0btag_stack[0].legendCoordinates[0] = 0.25
#jet0btag_stack[0].legendCoordinates[2] = 0.25+0.23
#allStacks.append(jet0btag_stack)
#jet1btag_stack                   = getStack(":jet1btag;SSV_{HE} of j_{1};Number of Events",[30,-1,6.], commoncf, signalNumbers, topIsLargest)
#jet1btag_stack[0].minimum = 10**(-2)
#jet1btag_stack[0].legendCoordinates[0] = 0.25
#jet1btag_stack[0].legendCoordinates[2] = 0.25+0.23
#allStacks.append(jet1btag_stack)
#jet2btag_stack                   = getStack(":jet2btag;SSV_{HE} of j_{2};Number of Events",[30,-1,6.], commoncf, signalNumbers, topIsLargest)
#jet2btag_stack[0].minimum = 10**(-2)
#jet2btag_stack[0].legendCoordinates[0] = 0.25
#jet2btag_stack[0].legendCoordinates[2] = 0.25+0.23
#allStacks.append(jet2btag_stack)
#jet3btag_stack                   = getStack(":jet3btag;SSV_{HE} of j_{2};Number of Events",[30,-1,6.], commoncf, signalNumbers, topIsLargest)
#jet3btag_stack[0].minimum = 10**(-2)
#jet3btag_stack[0].legendCoordinates[0] = 0.25
#jet3btag_stack[0].legendCoordinates[2] = 0.25+0.23
#allStacks.append(jet3btag_stack)

#for stack in allStacks:
#  for var in stack:
#    var.addOverFlowBin = "both"

execfile("simplePlotsKernel.py")

for stack in allStacks:
  stack[0].maximum = 3.*stack[0].data_histo.GetMaximum()
  stack[0].logy = True
  stack[0].minimum = minimum
  stack[0].legendCoordinates=[0.61,0.95 - 0.08*5,.98,.95]
#  stack[0].lines = [[0.61, 0.48, "#font[22]{CMS preliminary}"], [0.61,0.43,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 7 TeV"]]
  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS preliminary}"], [0.2,0.85,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 7 TeV"]]

#drawNMStacks(1,1,[met_stack],             subdir+prefix+"met", False)
drawNMStacks(1,1,[genmet_stack],             subdir+prefix+"genmet", False)
if not doOnlyMET:
#  drawNMStacks(1,1,[mT_stack],              subdir+prefix+"mT", False)
  drawNMStacks(1,1,[kinMetSig_stack],       subdir+prefix+"kinMetSig", False)
  drawNMStacks(1,1,[ht_stack],              subdir+prefix+"ht", False)
#  drawNMStacks(1,1,[ht2had_stack],          subdir+prefix+"ht2had", False)
#  drawNMStacks(1,1,[ht2_stack],             subdir+prefix+"ht2", False)
  drawNMStacks(1,1,[jet0_pt_stack],         subdir+prefix+"jet0_pt", False)
  drawNMStacks(1,1,[jet1_pt_stack],         subdir+prefix+"jet1_pt", False)
  drawNMStacks(1,1,[jet2_pt_stack],         subdir+prefix+"jet2_pt", False)
  drawNMStacks(1,1,[jet3_pt_stack],         subdir+prefix+"jet3_pt", False)
  drawNMStacks(1,1,[m3_stack],              subdir+prefix+"m3", False)
  drawNMStacks(1,1,[lepton_pt_stack],       subdir+prefix+"lepton_pt", False)
#  drawNMStacks(1,1,[lepton_eta_stack],                  subdir+prefix+"lepton_eta", False)
#  drawNMStacks(1,1,[lepton_relIso_stack],               subdir+prefix+"lepton_relIso", False)
#  drawNMStacks(1,1,[lepton_deltaR_stack],               subdir+prefix+"lepton_deltaR", False)
#  drawNMStacks(1,1,[lepton_dxy_stack],                  subdir+prefix+"lepton_dxy", False)
#  drawNMStacks(1,1,[lepton_vertex_dxy_stack],                  subdir+prefix+"lepton_vertex_dxy", False)
#  drawNMStacks(1,1,[lepton_vertex_dz_stack],            subdir+prefix+"lepton_vertex_dz", False)

#drawNMStacks(1,1,[btag0_stack],            subdir+prefix+"btag0", False)
#drawNMStacks(1,1,[btag1_stack],            subdir+prefix+"btag1", False)
#drawNMStacks(1,1,[btag2_stack],            subdir+prefix+"btag2", False)
#drawNMStacks(1,1,[jet0btag_stack],         subdir+prefix+"jet0btag", False)
#drawNMStacks(1,1,[jet1btag_stack],         subdir+prefix+"jet1btag", False)
#drawNMStacks(1,1,[jet2btag_stack],         subdir+prefix+"jet2btag", False)
#drawNMStacks(1,1,[jet3btag_stack],         subdir+prefix+"jet3btag", False)

#for stack in allStacks:
#  stack[0].maximum = 1.2*stack[0].data_histo.GetMaximum()
#  stack[0].logy = False
#  stack[0].minumum=0
#
#drawNMStacks(1,1,[met_stack],             subdir+prefix+"met_lin", False)
#if not doOnlyMET:
##  drawNMStacks(1,1,[mT_stack],              subdir+prefix+"mT_lin", False)
#  drawNMStacks(1,1,[kinMetSig_stack],       subdir+prefix+"kinMetSig_lin", False)
#  drawNMStacks(1,1,[ht_stack],              subdir+prefix+"ht_lin", False)
##  drawNMStacks(1,1,[ht2had_stack],          subdir+prefix+"ht2had_lin", False)
##  drawNMStacks(1,1,[ht2_stack],             subdir+prefix+"ht2_lin", False)
#  drawNMStacks(1,1,[jet0_pt_stack],         subdir+prefix+"jet0_pt_lin", False)
#  drawNMStacks(1,1,[jet1_pt_stack],         subdir+prefix+"jet1_pt_lin", False)
#  drawNMStacks(1,1,[jet2_pt_stack],         subdir+prefix+"jet2_pt_lin", False)
#  drawNMStacks(1,1,[jet3_pt_stack],         subdir+prefix+"jet3_pt_lin", False)
#  drawNMStacks(1,1,[m3_stack],              subdir+prefix+"m3_lin", False)
##  drawNMStacks(1,1,[lepton_pt_stack],       subdir+prefix+"lepton_pt_lin", False)
##  drawNMStacks(1,1,[lepton_eta_stack],                  subdir+prefix+"lepton_eta_lin", False)
##  drawNMStacks(1,1,[lepton_relIso_stack],               subdir+prefix+"lepton_relIso_lin", False)
##  drawNMStacks(1,1,[lepton_deltaR_stack],               subdir+prefix+"lepton_deltaR_lin", False)
##  drawNMStacks(1,1,[lepton_dxy_stack],                  subdir+prefix+"lepton_dxy_lin", False)
##  drawNMStacks(1,1,[lepton_vertex_dxy_stack],                  subdir+prefix+"lepton_vertex_dxy_lin", False)
##  drawNMStacks(1,1,[lepton_vertex_dz_stack],            subdir+prefix+"lepton_vertex_dz_lin", False)
#
##drawNMStacks(1,1,[btag0_stack],            subdir+prefix+"btag0_lin", False)
##drawNMStacks(1,1,[btag1_stack],            subdir+prefix+"btag1_lin", False)
##drawNMStacks(1,1,[btag2_stack],            subdir+prefix+"btag2_lin", False)
##drawNMStacks(1,1,[jet0btag_stack],         subdir+prefix+"jet0btag_lin", False)
##drawNMStacks(1,1,[jet1btag_stack],         subdir+prefix+"jet1btag_lin", False)
##drawNMStacks(1,1,[jet2btag_stack],         subdir+prefix+"jet2btag_lin", False)
##drawNMStacks(1,1,[jet3btag_stack],         subdir+prefix+"jet3btag_lin", False)


#ROOT.Fit.doFit(met_stack[-1].data_histo)

#l  = ROOT.TLegend(0.62,0.45,.98,.85)
#met_stack[-1].data_histo.Draw()
#l.AddEntry(met_stack[-1].data_histo, "Data")
#colors = [ROOT.kBlue , ROOT.kRed , ROOT.kGreen , ROOT.kOrange , ROOT.kCyan, ROOT.kOrange -7  , ROOT.kOrange + 4, ROOT.kOrange + 3 , ROOT.kMagenta, ROOT.kRed + 3]
#for i in range(10):
#  template = ROOT.Fit.getFitTemplate(i)
#  template.SetLineColor(colors[i])
#  template.SetMarkerColor(colors[i])
#  opt="same"
#  if i==0:
#    opt = "same"
#  ROOT.Fit.getFitTemplate(i).Draw(opt)
#  l.AddEntry(ROOT.Fit.getFitTemplate(i), "Template "+str(i) )
#l.Draw()


