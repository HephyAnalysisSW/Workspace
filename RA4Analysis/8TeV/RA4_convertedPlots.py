import ROOT
from array import array
from math import *
import os, copy
from simpleStatTools import niceNum
from Workspace.RA4Analysis.simplePlotsCommon import *
from funcs import *

import xsec
small = False
mode = "Mu"
#mode = "Ele"
#dataMode = "12fb"
dataMode = "20fb"

if dataMode == "12fb":
  targetLumi = 12000.
if dataMode == "20fb":
  targetLumi = 20000.

if mode=="Mu":
  from defaultMu2012Samples import *
if mode=="Ele":
  from defaultEle2012Samples import *

ttbar["bins"] = ["TTJets-PowHeg"]
wjets["bins"] = ["WJetsHT250"]
data["bins"] = ["data"]
stop["bins"] = ["singleTop"]
dy["bins"]  = ["DY"]
qcd["bins"] = ["QCD"]

allSamples = [ttbar, wjets, dy, stop, qcd, data]

defWeight = "weight"

for sample in allSamples:
  if dataMode=="12fb":
    sample["dirname"] = "/data/schoef/convertedTuples_v15/copyMET/"+mode+"/"
  if dataMode=="20fb":
    sample["dirname"] = "/data/schoef/convertedTuples_v16/copyMET/"+mode+"/"
  sample["hasWeight"] = True
  if sample['name'].lower().count('data'):
    sample["weight"] = "weight"
  else:
    sample["weight"] = defWeight
  

allVars=[]
allStacks=[]

signalColors = [ROOT.kBlack, ROOT.kBlue + 1, ROOT.kGreen + 2, ROOT.kOrange + 2]

## plots for studying preselection 
topIsLargest = True
minimum=10**(-0.5)


signalNumbers = []
presel = "pf-4j40"
preprefix     = mode+"_"+dataMode+"_converted-ht400-750-met150-bt2"
additionalCut = "met>150&&ht>400&&ht<750&&nbtags==2"
#preprefix     = mode+"_"+dataMode+"_converted-ht400-met150"
#additionalCut = "met>150&&ht>400"

subdir = "/8TeV/"

doOnlyMET = False
normalizeToData = False

chainstring = "empty"
commoncf = "(0)"
prefix="empty_"

if mode=="Mu":
  leptonCut="(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0)"
if mode=="Ele":
  leptonCut="(singleElectronic&&nvetoElectrons==1&&nvetoMuons==0)"

if presel == "pf-3j40":
  chainstring = "Events"
  commoncf = "jet2pt>40&&leptonPt>20&&"+leptonCut
if presel == "pf-4j40":
  chainstring = "Events"
  commoncf = "jet3pt>40&&leptonPt>20&&"+leptonCut

#if useConvertedTuples and mode=="singleMu":
#  commoncf+="&&leptonPt>45&&abs(leptonEta)<2.1"

if additionalCut!="":
  commoncf+="&&"+additionalCut

prefix= "RA4_"+presel+"_"
if preprefix!="":
  prefix = preprefix+"_"+presel+"_"
  
for sample in allSamples:
  sample["Chain"] = chainstring

#smsSample = {'Chain': 'Events',\
#  'Counter': 'bool_EventCounter_passed_PAT.obj',
#  'bins': [thisSMS],
#  'dirname': '/data/schoef/convertedTuples_v6//copy/Mu/T1tttt/',
##  'filenames': {'SMS': ['/data/schoef/convertedTuples_v6//copy/Mu/T1tttt/histo_T1tttt_700_200_-1.root']},
#  'hasWeight': True,
#  'name': 'SMS'+thisSMS}
#allSamples.append(smsSample)

def getStack(varstring, binning, cutstring, signalNumbers, topIsLargest = False, varfunc = ""):
  DATA          = variable(varstring, binning, cutstring)
  DATA.sample   = data
#  DATA.color    = ROOT.kGray
  DATA.color    = dataColor
  DATA.legendText="Data"

  MC_QCD                       = variable(varstring, binning, cutstring)
  MC_QCD.minimum               = 10**(-3)

  MC_TTJETS                    = copy.deepcopy(MC_QCD)
  MC_WJETS                     = copy.deepcopy(MC_QCD)
  MC_ZJETS                     = copy.deepcopy(MC_QCD)
  MC_STOP                      = copy.deepcopy(MC_QCD)

  MC_QCD                       = variable(varstring, binning, cutstring)
  MC_QCD.minimum               = 5*10**(-3)
  MC_QCD.sample                = qcd
#  MC_QCD.sample                = copy.deepcopy(mc)
#  MC_QCD.sample["bins"]        = QCD_Bins
  MC_TTJETS                    = copy.deepcopy(MC_QCD)
  MC_TTJETS.sample             = ttbar
#  MC_TTJETS.sample                = copy.deepcopy(mc)
#  MC_TTJETS.sample["bins"]        = ttbar["bins"]
  MC_WJETS                     = copy.deepcopy(MC_QCD)
  MC_WJETS.sample              = wjets
#  MC_WJETS.sample              = copy.deepcopy(mc)
#  MC_WJETS.sample["bins"]      = WJets_Bins

  MC_ZJETS                     = copy.deepcopy(MC_QCD)
  MC_ZJETS.sample              = dy
#  MC_ZJETS.sample              = copy.deepcopy(mc)
#  MC_ZJETS.sample["bins"]      = ZJets_Bins
  MC_STOP                     = copy.deepcopy(MC_QCD)
  MC_STOP.sample              = stop 
#  MC_STOP.sample              = copy.deepcopy(mc)
#  MC_STOP.sample["bins"]      = singleTop_Bins

  MC_TTJETS.legendText         = "t#bar{t} + Jets"
  MC_TTJETS.style              = "f0"
  MC_TTJETS.color              = ROOT.kRed - 3
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
  res[0].dataMCRatio = [DATA, res[0]]
  for i in range(len(signalNumbers)):
    MC_SIGNAL                    = copy.deepcopy(MC_QCD)
    MC_SIGNAL.sample             = copy.deepcopy(signals[str(signalNumbers[i])])
    MC_SIGNAL.legendText         = signals[str(signalNumbers[i])]["name"]
    MC_SIGNAL.style              = "l02"
    MC_SIGNAL.color              = signalColors[i]
    MC_SIGNAL.add = []
    res.append(MC_SIGNAL)

#  MC_sms                    = copy.deepcopy(MC_QCD)
#  MC_sms.sample             = smsSample 
#  MC_sms.legendText         = "sms" 
#  MC_sms.style              = "l"
#  MC_sms.color              = signalColors[1]
#  MC_sms.add = []
#  res.append(MC_sms)

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
#


met_stack = getStack(":met;#slash{E}_{T} (GeV);Number of Events / 50 GeV",[19,100,1050], commoncf, signalNumbers, topIsLargest)
met_stack[0].addOverFlowBin = "upper"
allStacks.append(met_stack)

  
#cleanMT095_stack  = getStack(":cleanMT095;m_{T} for cos(#Delta #phi(l, #slash{E}_{T})) > -0.95;Number of Events / 20 GeV",[27,0,540], commoncf, signalNumbers, topIsLargest, cleanMTFunc(0.95))
#allStacks.append(cleanMT095_stack)
#
#cleanMT09_stack  = getStack(":cleanMT09;m_{T} for cos(#Delta #phi(l, #slash{E}_{T})) > -0.9;Number of Events / 20 GeV",[27,0,540], commoncf, signalNumbers, topIsLargest, cleanMTFunc(0.9))
#allStacks.append(cleanMT09_stack)
#
#cleanMT08_stack  = getStack(":cleanMT08;m_{T} for cos(#Delta #phi(l, #slash{E}_{T})) > -0.8;Number of Events / 20 GeV",[27,0,540], commoncf, signalNumbers, topIsLargest, cleanMTFunc(0.8))
#allStacks.append(cleanMT08_stack)
#
#mTbare_stack  = getStack(":mTbare;m_{T} with raw #slash{E}_{T};Number of Events / 20 GeV",[27,0,540], commoncf, signalNumbers, topIsLargest, mTbare)
#allStacks.append(mTbare_stack)
#
#cosDeltaPhiLepMET_stack  = getStack(":xxx;cos(#Delta #phi(l, #slash{E}_{T}));Number of Events",[50,-1,1], commoncf, signalNumbers, topIsLargest, cosDeltaPhiLepMET)
#allStacks.append(cosDeltaPhiLepMET_stack)


#ht_stack                          = getStack(":ht;H_{T} (GeV);Number of Events / 25 GeV",[41,500,1525 ], commoncf, signalNumbers, topIsLargest)
#ht_stack[0].addOverFlowBin = "upper"
#allStacks.append(ht_stack)
#

#btag0mass_stack               = getStack(":btag0Mass;btag0Mass;Number of Events",[20,0,8.0], commoncf+"&&btag0>1.74", signalNumbers, topIsLargest)
#btag0mass_stack[0].addOverFlowBin = "upper"
#allStacks.append(btag0mass_stack)
#btag1mass_stack               = getStack(":btag1Mass;btag1Mass;Number of Events",[20,0,8.0], commoncf+"&&btag1>1.74", signalNumbers, topIsLargest)
#btag1mass_stack[0].addOverFlowBin = "upper"
#allStacks.append(btag1mass_stack)
#btag2mass_stack               = getStack(":btag2Mass;btag2Mass;Number of Events",[20,0,8.0], commoncf+"&&btag2>1.74", signalNumbers, topIsLargest)
#btag2mass_stack[0].addOverFlowBin = "upper"
#allStacks.append(btag2mass_stack)
#btag3mass_stack               = getStack(":btag3Mass;btag3Mass;Number of Events",[20,0,8.0], commoncf+"&&btag3>1.74", signalNumbers, topIsLargest)
#btag3mass_stack[0].addOverFlowBin = "upper"
#allStacks.append(btag3mass_stack)


#jlb_stack = getStack(":mht - leptonPt;JLB (GeV);Number of Events / 20 GeV",[52,-520,520], commoncf, signalNumbers, topIsLargest)
#jlb_stack[0].addOverFlowBin = "both"
#allStacks.append(jlb_stack)
#ptw_stack = getStack(":sqrt((metpx + leptonPt*cos(lepton_phi))**2 + (metpy + leptonPt*sin(lepton_phi))**2);(l+#slash{E})_{T}; Number of Events / 25 GeV",[21,0,525], commoncf, signalNumbers, topIsLargest)
#ptw_stack[0].addOverFlowBin = "upper"
#allStacks.append(ptw_stack)
#metiso_stack = getStack(":metiso;MET Iso from jets; Number of Events",[40,0,3.1415], commoncf, signalNumbers, topIsLargest)
#metiso_stack[0].addOverFlowBin = "upper"
#allStacks.append(metiso_stack)


if not doOnlyMET:
  met_zoomed_stack = getStack(":met;#slash{E}_{T} (GeV);Number of Events / 10 GeV",[21,100,310], commoncf, signalNumbers, topIsLargest)
  met_zoomed_stack[0].addOverFlowBin = "upper"
  allStacks.append(met_zoomed_stack)

  #type1phiMet_stack = getStack(":type1phiMet;#slash{E}_{T} (GeV);Number of Events / 50 GeV",[19,100,1050], commoncf.replace("met", "type1phiMet"), signalNumbers, topIsLargest)
  #type1phiMet_stack[0].addOverFlowBin = "upper"
  #allStacks.append(type1phiMet_stack)
  #
  #type1phiMet_zoomed_stack = getStack(":type1phiMet;#slash{E}_{T} (GeV);Number of Events / 10 GeV",[21,100,310], commoncf.replace("met", "type1phiMet"), signalNumbers, topIsLargest)
  #type1phiMet_zoomed_stack[0].addOverFlowBin = "upper"
  #allStacks.append(type1phiMet_zoomed_stack)

  ht_stack                          = getStack(":ht;H_{T} (GeV);Number of Events / 100 GeV", [26,0, 2600], commoncf, signalNumbers, topIsLargest)
  ht_stack[0].addOverFlowBin = "upper"
  allStacks.append(ht_stack)

  ht_zoomed_stack                          = getStack(":ht;H_{T} (GeV);Number of Events / 30 GeV", [21,400, 1030], commoncf, signalNumbers, topIsLargest)
  ht_zoomed_stack[0].addOverFlowBin = "upper"
  allStacks.append(ht_zoomed_stack)

  ngoodVertices_stack = getStack(":ngoodVertices;Number of Vertices;Number of Events",[51,0,51], commoncf, [], topIsLargest)
  ngoodVertices_stack[0].addOverFlowBin = "upper"
  allStacks.append(ngoodVertices_stack)

  mT_stack  = getStack(":mT;m_{T} (GeV);Number of Events / 20 GeV",[27,0,540], commoncf, signalNumbers, topIsLargest)
  mT_stack[0].addOverFlowBin = "upper"
  allStacks.append(mT_stack)

  rawmet_stack  = getStack(":rawmet; (GeV);Number of Events / 20 GeV",[27,0,540], commoncf, signalNumbers, topIsLargest, rawMET)
  rawmet_stack[0].addOverFlowBin = "upper"
  allStacks.append(rawmet_stack)


  jet0_pt_stack                     = getStack(":jet0pt;p_{T} of leading jet (GeV);Number of Events / 40 GeV",[26,0,1040], commoncf, signalNumbers, topIsLargest)
  jet0_pt_stack[0].addOverFlowBin = "upper"
  allStacks.append(jet0_pt_stack)
  jet1_pt_stack                     = getStack(":jet1pt;p_{T} of 2^{nd} leading jet (GeV);Number of Events / 40 GeV",[26,0,1040], commoncf, signalNumbers, topIsLargest)
  jet1_pt_stack[0].addOverFlowBin = "upper"
  allStacks.append(jet1_pt_stack)
  jet2_pt_stack                     = getStack(":jet2pt;p_{T} of 3^{rd} leading jet (GeV);Number of Events / 40 GeV",[21,0,840], commoncf, signalNumbers, topIsLargest)
  jet2_pt_stack[0].addOverFlowBin = "upper"
  allStacks.append(jet2_pt_stack)
  jet3_pt_stack                     = getStack(":jet3pt;p_{T} of 4^{th} leading jet (GeV);Number of Events / 40 GeV",[21,00,840], commoncf+"&&jet3pt>0", signalNumbers, topIsLargest)
  jet3_pt_stack[0].addOverFlowBin = "upper"
  allStacks.append(jet3_pt_stack)

  btag0pt_stack                     = getStack(":btag0pt;p_{T} of most b-tagged jet (GeV);Number of Events / 40 GeV",[26,0,1040], commoncf, signalNumbers, topIsLargest)
  btag0pt_stack[0].addOverFlowBin = "upper"
  allStacks.append(btag0pt_stack)
  btag1pt_stack                     = getStack(":btag1pt;p_{T} of 2^{nd} most btagged jet (GeV);Number of Events / 40 GeV",[26,0,1040], commoncf, signalNumbers, topIsLargest)
  btag1pt_stack[0].addOverFlowBin = "upper"
  allStacks.append(btag1pt_stack)

  kinMetSig_stack                   = getStack(":kinMetSig;S_{MET};Number of Events",[25,0,25], commoncf, signalNumbers, topIsLargest, kinMetSig)
  kinMetSig_stack[0].addOverFlowBin = "upper"
  allStacks.append(kinMetSig_stack)


  m3_stack = getStack(":m3;M_{3} (GeV);Number of Events / 100 GeV",[26, 0, 2600], commoncf, signalNumbers, topIsLargest)
  m3_stack[0].addOverFlowBin = "upper"
  allStacks.append(m3_stack)

  leptonPt_stack = getStack("p_{T} (GeV):leptonPt;p_{T,lep.} (GeV);Number of Events / 30 GeV",[26,0,780], commoncf, signalNumbers, topIsLargest)
  leptonPt_stack[0].addOverFlowBin = "upper"
  allStacks.append(leptonPt_stack)

  leptonEta_stack                  = getStack(":leptonEta;|#eta^{#mu}|;Number of Events",[62,-3.1,3.1], commoncf, signalNumbers, topIsLargest)
  leptonEta_stack[0].addOverFlowBin = "both"
  allStacks.append(leptonEta_stack)
 
  if mode=="Mu":
    ngoodElectrons_stack = getStack("ngoodElectrons :ngoodElectrons;Number of electrons;Number of Events",[5,0-.5,5-.5], commoncf.replace("singleMuonic&&nvetoMuons==1&&nvetoElectrons==0", "ngoodMuons==1&&nvetoMuons==1"), signalNumbers, topIsLargest)
    ngoodElectrons_stack[0].addOverFlowBin = "upper"
    allStacks.append(ngoodElectrons_stack)

    ngoodMuons_stack = getStack("ngoodMuons :ngoodMuons;Number of muons;Number of Events",[5,0-.5,5-.5], commoncf.replace("singleMuonic&&nvetoMuons==1", "ngoodMuons>0"), signalNumbers, topIsLargest)
    ngoodMuons_stack[0].addOverFlowBin = "upper"
    allStacks.append(ngoodMuons_stack)

    nvetoElectrons_stack = getStack("nvetoElectrons :nvetoElectrons;Number of veto electrons;Number of Events",[5,0-.5,5-.5], commoncf.replace("singleMuonic&&nvetoMuons==1&&nvetoElectrons==0","ngoodMuons==1&&nvetoMuons==1"), signalNumbers, topIsLargest)
    nvetoElectrons_stack[0].addOverFlowBin = "upper"
    allStacks.append(nvetoElectrons_stack)

    nvetoMuons_stack = getStack("nvetoMuons :nvetoMuons;Number of veto muons;Number of Events",[5,0-.5,5-.5], commoncf.replace("&&nvetoMuons==1",""), signalNumbers, topIsLargest)
    nvetoMuons_stack[0].addOverFlowBin = "upper"
    allStacks.append(nvetoMuons_stack)

  if mode=="Ele":
    ngoodElectrons_stack = getStack("ngoodElectrons :ngoodElectrons;Number of electrons;Number of Events",[5,0-.5,5-.5], commoncf.replace("singleElectronic&&nvetoElectrons==1", "ngoodElectrons>0"), signalNumbers, topIsLargest)
    ngoodElectrons_stack[0].addOverFlowBin = "upper"
    allStacks.append(ngoodElectrons_stack)

    ngoodMuons_stack = getStack("ngoodMuons :ngoodMuons;Number of muons;Number of Events",[5,0-.5,5-.5], commoncf.replace("singleElectronic&&nvetoElectrons==1&&nvetoMuons==0", "singleElectronic&&nvetoElectrons==1"), signalNumbers, topIsLargest)
    ngoodMuons_stack[0].addOverFlowBin = "upper"
    allStacks.append(ngoodMuons_stack)

    nvetoElectrons_stack = getStack("nvetoElectrons :nvetoElectrons;Number of veto electrons;Number of Events",[5,0-.5,5-.5], commoncf.replace("&&nvetoElectrons==1",""), signalNumbers, topIsLargest)
    nvetoElectrons_stack[0].addOverFlowBin = "upper"
    allStacks.append(nvetoElectrons_stack)

    nvetoMuons_stack = getStack("nvetoMuons :nvetoMuons;Number of veto muons;Number of Events",[5,0-.5,5-.5], commoncf.replace("singleElectronic&&nvetoElectrons==1&&nvetoMuons==0","singleElectronic&&nvetoElectrons==1"), signalNumbers, topIsLargest)
    nvetoMuons_stack[0].addOverFlowBin = "upper"
    allStacks.append(nvetoMuons_stack)



  nbtags_stack = getStack(":nbtags;Number of b-tagged Jets;Number of Events",[10,0,10], commoncf, [], topIsLargest)
  nbtags_stack[0].addOverFlowBin = "upper"
  allStacks.append(nbtags_stack)

  njets_stack = getStack(":njets;Number of Jets;Number of Events",[20,0,20], commoncf.replace("jet2pt>40&&",""), [], topIsLargest)
  njets_stack[0].addOverFlowBin = "upper"
  allStacks.append(njets_stack)

  phibb_stack            =   getStack( ":phibb;phi(bb);Number of Events", [10,0,pi], commoncf, [], topIsLargest)
  phibb_stack[0].addOverFlowBin = "both"
  allStacks.append(phibb_stack)

  mbl_stack              =   getStack( ":mbl;m(b,l);Number of Events / 30 GeV", [31,0,930], commoncf, [], topIsLargest)
  mbl_stack[0].addOverFlowBin = "upper"
  allStacks.append(mbl_stack)

  mbb_stack              =   getStack( ":mbb;m(b,b);Number of Events / 50 GeV", [31,0,1550], commoncf, [], topIsLargest)
  mbb_stack[0].addOverFlowBin = "upper"
  allStacks.append(mbb_stack)

  mbbzoomed_stack              =   getStack( ":mbb;m(b,b);Number of Events / 20 GeV", [21,0,420], commoncf, [], topIsLargest)
  mbbzoomed_stack[0].addOverFlowBin = "upper"
  allStacks.append(mbbzoomed_stack)


for stack in allStacks:
  stack[0].minimum = minimum


reweightingHistoFile = ""

execfile("simplePlotsLoopKernel.py")
#execfile("simplePlotsKernel.py")


if normalizeToData:
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

defaultLines = [[0.2, 0.9, "#font[22]{CMS Collaboration}"], [0.2,0.85,str(int(round(targetLumi/10.))/100.)+" fb^{-1},  #sqrt{s} = 8 TeV"]]
for stack in allStacks:
  stack[0].maximum = 4*10**4 # 10.*stack[-1].data_histo.GetMaximum()
  stack[0].logy = True
  stack[0].minimum = minimum
  stack[0].legendCoordinates=[0.61,0.95 - 0.08*5,.98,.95]
  stack[0].lines = defaultLines 

#cosDeltaPhiLepMET_stack[0].maximum = 4*10**6

#drawNMStacks(1,1,[mTbare_stack],              subdir+prefix+"mTbare", False)
#drawNMStacks(1,1,[cleanMT09_stack],              subdir+prefix+"cleanMT09", False)
#drawNMStacks(1,1,[cleanMT095_stack],              subdir+prefix+"cleanMT095", False)
#drawNMStacks(1,1,[cleanMT08_stack],              subdir+prefix+"cleanMT08", False)
#drawNMStacks(1,1,[cosDeltaPhiLepMET_stack],              subdir+prefix+"cosDeltaPhiLepMET", False)

if not doOnlyMET:
  drawNMStacks(1,1,[met_stack],             subdir+prefix+"met", False)
  drawNMStacks(1,1,[met_zoomed_stack],             subdir+prefix+"met_zoomed", False)
  #drawNMStacks(1,1,[type1phiMet_stack],             subdir+prefix+"type1phiMet", False)
  #drawNMStacks(1,1,[type1phiMet_zoomed_stack],             subdir+prefix+"type1phiMet_zoomed", False)
  drawNMStacks(1,1,[ht_stack],              subdir+prefix+"ht", False)
  drawNMStacks(1,1,[ht_zoomed_stack],              subdir+prefix+"ht_zoomed", False)
  drawNMStacks(1,1,[ngoodVertices_stack],             subdir+prefix+"ngoodVertices", False)
  drawNMStacks(1,1,[mT_stack],              subdir+prefix+"mT", False)
  drawNMStacks(1,1,[rawmet_stack],              subdir+prefix+"rawMET", False)
  drawNMStacks(1,1,[kinMetSig_stack],       subdir+prefix+"kinMetSig", False)
#  drawNMStacks(1,1,[ht2had_stack],          subdir+prefix+"ht2had", False)
#  drawNMStacks(1,1,[ht2_stack],             subdir+prefix+"ht2", False)
  drawNMStacks(1,1,[btag0pt_stack],         subdir+prefix+"btag0pt", False)
  drawNMStacks(1,1,[btag1pt_stack],         subdir+prefix+"btag1pt", False)
  drawNMStacks(1,1,[jet0_pt_stack],         subdir+prefix+"jet0_pt", False)
  drawNMStacks(1,1,[jet1_pt_stack],         subdir+prefix+"jet1_pt", False)
  drawNMStacks(1,1,[jet2_pt_stack],         subdir+prefix+"jet2_pt", False)
  drawNMStacks(1,1,[jet3_pt_stack],         subdir+prefix+"jet3_pt", False)
  drawNMStacks(1,1,[m3_stack],              subdir+prefix+"m3", False)
  drawNMStacks(1,1,[leptonPt_stack],       subdir+prefix+"leptonPt", False)
  drawNMStacks(1,1,[leptonEta_stack],                  subdir+prefix+"leptonEta", False)
  drawNMStacks(1,1,[ngoodElectrons_stack],  subdir+prefix+"ngoodElectrons", False)
  drawNMStacks(1,1,[ngoodMuons_stack],  subdir+prefix+"ngoodMuons", False)
  drawNMStacks(1,1,[nvetoElectrons_stack],  subdir+prefix+"nvetoElectrons", False)
  drawNMStacks(1,1,[nvetoMuons_stack],  subdir+prefix+"nvetoMuons", False)
  drawNMStacks(1,1,[nbtags_stack],             subdir+prefix+"nbtags", False)
  drawNMStacks(1,1,[njets_stack],             subdir+prefix+"njets", False)
  drawNMStacks(1,1,[phibb_stack],            subdir+prefix+"phibb", False)
  drawNMStacks(1,1,[mbl_stack],            subdir+prefix+"mbl", False)
  drawNMStacks(1,1,[mbb_stack],            subdir+prefix+"mbb", False)
  drawNMStacks(1,1,[mbbzoomed_stack],            subdir+prefix+"mbbzoomed", False)

