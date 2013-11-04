import ROOT
from array import array
from math import *
import os, copy, sys

ROOT.TH1F().SetDefaultSumw2()

paths = ['../../HEPHYCommonTools/python', '../../HEPHYCommonTools/plots', '../../RA4Analysis/plots']
#path = os.path.abspath('../../HEPHYCommonTools/python')
for path in [os.path.abspath(p) for p in paths]:
  if not path in sys.path:
    sys.path.insert(1, path)

from simplePlotsCommon import *
from funcs import *

import xsec
small = False

targetLumi = 19375.
lumiScale = 1.

#FastSim = {}
#FastSim["bins"] = ["S300N270"]
#FastSim["name"] = "S300N270"
#
#FullSim = {}
#FullSim["bins"] = ["S300N270FullSim"]
#FullSim["name"] = "S300N270FullSim"

chmode = "copy"
stop300lsp270g200 = {}
stop300lsp270g200["bins"]     = ["stop300lsp270g200FastSim"]
stop300lsp270g200["name"]     = "stop300lsp270g200FastSim"
stop300lsp270g200["color"]     = ROOT.kBlack
stop300lsp270g200["legendText"]  = "m_{#tilde t} = 300, m_{LSP} = 270, g=200"
stop300lsp270g200["dirname"]  = "/data/schoef/monoJetTuples_v1/"+chmode+"/"

stop300lsp270g175 = {}
stop300lsp270g175["bins"]     = ["stop300lsp270g175FastSim"]
stop300lsp270g175["name"]     = "stop300lsp270g175FastSim"
stop300lsp270g175["color"]     = ROOT.kRed - 3
stop300lsp270g175["legendText"]  = "m_{#tilde t} = 300, m_{LSP} = 270, g=175"
stop300lsp270g175["dirname"]  = "/data/schoef/monoJetTuples_v1/"+chmode+"/"

allSamples = [stop300lsp270g200, stop300lsp270g175]
signals = allSamples

for sample in allSamples:
  sample["hasWeight"] = False
#  if sample['name'].lower().count('data'):
#    sample["weight"] = "weight"
#  else:
#    sample["weight"] = defWeight

allVars=[]
allStacks=[]

signalColors = [ROOT.kBlack, ROOT.kBlue + 1, ROOT.kGreen + 2, ROOT.kOrange + 2]

## plots for studying preselection 
topIsLargest = True

minimum=10**(-0.5)

preprefix     = "fc"
#presel = "refSel"
presel = "refSel"
additionalCut = ""
#additionalCut = "met>250"


subdir = "/pngMJ/"

normalizeToData = False

chainstring = "empty"
commoncf = "(0)"
prefix="empty_"
if presel == "refSel":
  commoncf="isrJetPt>110&&isrJetBTBVetoPassed&&softIsolatedMuPt>5&&nHardElectrons+nHardMuons==0&&njet60<=2"
#  commoncf="njet<=3"
  chainstring = "Events"
if presel == "inclusive":
  commoncf="(1)"
#  commoncf="njet<=3"
  chainstring = "Events"

if additionalCut!="":
  commoncf+="&&"+additionalCut

prefix= "MonoJet_"+presel+"_"+chmode+"_"
if preprefix!="":
  prefix = preprefix+"_"+presel+"_"+chmode+"_"

for sample in allSamples:
  sample["Chain"] = chainstring


def getStack(varstring, binning, cutstring, signals, topIsLargest = False, varfunc = ""):
  res = []
  for s in signals:
    sMC          = variable(varstring, binning, cutstring)
    sMC.sample   = s
    sMC.color      = s['color']
    sMC.legendText = s["legendText"]
    sMC.style      = "l11"
    res.append(sMC)

#  res = [FastS, FullS]

#  res[0].dataMCRatio = [FastS,FullS]
#  res[0].ratioVarName = "Fast / Full"

  getLinesForStack(res, targetLumi)
  nhistos = len(res)
  for var in res:
    var.legendCoordinates=[0.51,0.95 - -0.08*3 ,.98,.95]
    var.scale = lumiScale
#    var.legendCoordinates=[0.64,0.95 - 0.05*nhistos,.98,.95] #for signalnumbers = [0,1]
  if varfunc!="":
    for var in res:
      var.varfunc = varfunc
  return res




isrJetPt_stack = getStack(":isrJetPt;p_{T} of ISR jet;Number of Events / 50 GeV",[50,0,1000], commoncf, signals, topIsLargest)
isrJetPt_stack[0].addOverFlowBin = "upper"
allStacks.append(isrJetPt_stack)

isrJetEta_stack = getStack(":isrJetEta;#eta of ISR jet;Number of Events",[20,-5,5], commoncf, signals, topIsLargest)
isrJetEta_stack[0].addOverFlowBin = "upper"
allStacks.append(isrJetEta_stack)

isrJetPhi_stack = getStack(":isrJetPhi;#phi of ISR jet;Number of Events",[20,-pi,pi], commoncf, signals, topIsLargest)
isrJetPhi_stack[0].addOverFlowBin = "upper"
allStacks.append(isrJetPhi_stack)

isrJetPdg_stack = getStack(":isrJetPdg;pdgId of ISR jet;Number of Events",[44,-22,22], commoncf, signals, topIsLargest)
isrJetPdg_stack[0].addOverFlowBin = "upper"
allStacks.append(isrJetPdg_stack)

isrJetBtag_stack = getStack(":isrJetBtag;CSV b-tag of ISR jet;Number of Events",[20,-1,1], commoncf, signals, topIsLargest)
isrJetBtag_stack[0].addOverFlowBin = "upper"
allStacks.append(isrJetBtag_stack)

isrJetChef_stack = getStack(":isrJetChef;Chef of ISR jet;Number of Events",[20,0,1], commoncf, signals, topIsLargest)
isrJetChef_stack[0].addOverFlowBin = "upper"
allStacks.append(isrJetChef_stack)

isrJetNhef_stack = getStack(":isrJetNhef;Nhef of ISR jet;Number of Events",[20,0,1], commoncf, signals, topIsLargest)
isrJetNhef_stack[0].addOverFlowBin = "upper"
allStacks.append(isrJetNhef_stack)

isrJetCeef_stack = getStack(":isrJetCeef;Ceef of ISR jet;Number of Events",[20,0,1], commoncf, signals, topIsLargest)
isrJetCeef_stack[0].addOverFlowBin = "upper"
allStacks.append(isrJetCeef_stack)

isrJetNeef_stack = getStack(":isrJetNeef;Neef of ISR jet;Number of Events",[20,0,1], commoncf, signals, topIsLargest)
isrJetNeef_stack[0].addOverFlowBin = "upper"
allStacks.append(isrJetNeef_stack)

isrJetHFhef_stack = getStack(":isrJetHFhef;HFhef of ISR jet;Number of Events",[20,0,1], commoncf, signals, topIsLargest)
isrJetHFhef_stack[0].addOverFlowBin = "upper"
allStacks.append(isrJetHFhef_stack)

isrJetHFeef_stack = getStack(":isrJetHFeef;HFeef of ISR jet;Number of Events",[20,0,1], commoncf, signals, topIsLargest)
isrJetHFeef_stack[0].addOverFlowBin = "upper"
allStacks.append(isrJetHFeef_stack)

isrJetMuef_stack = getStack(":isrJetMuef;Muef of ISR jet;Number of Events",[20,0,1], commoncf, signals, topIsLargest)
isrJetMuef_stack[0].addOverFlowBin = "upper"
allStacks.append(isrJetMuef_stack)

isrJetElef_stack = getStack(":isrJetElef;Elef of ISR jet;Number of Events",[20,0,1], commoncf, signals, topIsLargest)
isrJetElef_stack[0].addOverFlowBin = "upper"
allStacks.append(isrJetElef_stack)

isrJetPhef_stack = getStack(":isrJetPhef;Phef of ISR jet;Number of Events",[20,0,1], commoncf, signals, topIsLargest)
isrJetPhef_stack[0].addOverFlowBin = "upper"
allStacks.append(isrJetPhef_stack)

softIsolatedMuPt_stack = getStack(":softIsolatedMuPt;p_{T} of soft isolated muon;Number of Events / 1.25 GeV",[16,0,20], commoncf, signals, topIsLargest)
softIsolatedMuPt_stack[0].addOverFlowBin = "upper"
allStacks.append(softIsolatedMuPt_stack)

njet_stack = getStack(":njet;n_{jet};Number of Events / 50 GeV",[10,0,10], commoncf.replace('&&njet60<=2',''), signals, topIsLargest)
njet_stack[0].addOverFlowBin = "upper"
allStacks.append(njet_stack)

njet60_stack = getStack(":njet60;n_{jet};Number of Events / 50 GeV",[10,0,10], commoncf.replace('&&njet60<=2',''), signals, topIsLargest)
njet60_stack[0].addOverFlowBin = "upper"
allStacks.append(njet60_stack)

ht_stack = getStack(":ht;H_{T} (GeV);Number of Events / 25 GeV",[40,0,1000], commoncf, signals, topIsLargest)
ht_stack[0].addOverFlowBin = "upper"
allStacks.append(ht_stack)

type1phiMet_stack = getStack(":type1phiMet;#slash{E}_{T} (GeV);Number of Events / 25 GeV",[40,0,1000], commoncf.replace('&&type1phiMet>250',''), signals, topIsLargest)
type1phiMet_stack[0].addOverFlowBin = "upper"
allStacks.append(type1phiMet_stack)

type1phiMetphi_stack = getStack(":type1phiMetphi;#phi(#slash{E}_{T});Number of Events",[40,-pi,pi], commoncf.replace('&&type1phiMetphi>250',''), signals, topIsLargest)
type1phiMetphi_stack[0].addOverFlowBin = "upper"
allStacks.append(type1phiMetphi_stack)

genmetphi_stack = getStack(":genmetphi;#phi(gen-#slash{E}_{T});Number of Events",[40,-pi, pi], commoncf.replace('&&genmetphi>250',''), signals, topIsLargest)
genmetphi_stack[0].addOverFlowBin = "upper"
allStacks.append(genmetphi_stack)

genmet_stack = getStack(":genmet;#slash{E}_{T} (GeV);Number of Events / 25 GeV",[40,0,1000], commoncf.replace('&&genmet>250',''), signals, topIsLargest)
genmet_stack[0].addOverFlowBin = "upper"
genmet_stack[0].data_histo.GetXaxis().SetLabelSize(0.02)
allStacks.append(genmet_stack)

genmet_reversed_stack = copy.deepcopy(genmet_stack) 
genmet_reversed_stack.reverse()
genmet_reversed_stack[0].addOverFlowBin = "upper"
genmet_reversed_stack[0].data_histo.GetXaxis().SetLabelSize(0.02)
allStacks.append(genmet_reversed_stack)
  
ngoodVertices_stack = getStack(":ngoodVertices;Number of Vertices;Number of Events",[51,0,51], commoncf, signals, topIsLargest)
ngoodVertices_stack[0].addOverFlowBin = "upper"
allStacks.append(ngoodVertices_stack)


for stack in allStacks:
  stack[0].minimum = minimum
#for stack in allStacks:
#  for var in stack:
#    var.addOverFlowBin = "both"
#reweightingHistoFile = "PU/reweightingHisto_Summer2012-S10-Run2012AB-Jul13ReReco.root"
reweightingHistoFile = ""

execfile("../../RA4Analysis/plots/simplePlotsLoopKernel.py")

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
  stack[0].legendCoordinates=[0.51,0.95 - 0.08*3 ,.98,.95]
  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS Collaboration}"], [0.2,0.85,str(int(round(targetLumi/10.))/100.)+" fb^{-1}"],[0.2,0.8,  "sqrt{s} = 8 TeV"]]


drawNMStacks(1,1,[softIsolatedMuPt_stack],             subdir+prefix+"softIsolatedMuPt", False)
drawNMStacks(1,1,[isrJetPt_stack],             subdir+prefix+"isrJetPt", False)
drawNMStacks(1,1,[isrJetEta_stack],             subdir+prefix+"isrJetEta", False)
drawNMStacks(1,1,[isrJetPhi_stack],             subdir+prefix+"isrJetPhi", False)
drawNMStacks(1,1,[isrJetPdg_stack],             subdir+prefix+"isrJetPdg", False)
drawNMStacks(1,1,[isrJetBtag_stack],            subdir+prefix+"isrJetBtag", False)
drawNMStacks(1,1,[isrJetChef_stack],            subdir+prefix+"isrJetChef", False)
drawNMStacks(1,1,[isrJetNhef_stack],            subdir+prefix+"isrJetNhef", False)
drawNMStacks(1,1,[isrJetCeef_stack],            subdir+prefix+"isrJetCeef", False)
drawNMStacks(1,1,[isrJetNeef_stack],            subdir+prefix+"isrJetNeef", False)
drawNMStacks(1,1,[isrJetHFhef_stack],           subdir+prefix+"isrJetHFhef", False)
drawNMStacks(1,1,[isrJetHFeef_stack],           subdir+prefix+"isrJetHFeef", False)
drawNMStacks(1,1,[isrJetMuef_stack],            subdir+prefix+"isrJetMuef", False)
drawNMStacks(1,1,[isrJetElef_stack],            subdir+prefix+"isrJetElef", False)
drawNMStacks(1,1,[isrJetPhef_stack],            subdir+prefix+"isrJetPhef", False)

drawNMStacks(1,1,[njet_stack],             subdir+prefix+"njet", False)
drawNMStacks(1,1,[njet60_stack],             subdir+prefix+"njet60", False)
drawNMStacks(1,1,[type1phiMet_stack],             subdir+prefix+"type1phiMet", False)
drawNMStacks(1,1,[type1phiMetphi_stack],             subdir+prefix+"type1phiMetphi", False)
drawNMStacks(1,1,[genmetphi_stack],             subdir+prefix+"genmetphi", False)
drawNMStacks(1,1,[ht_stack],             subdir+prefix+"ht", False)
drawNMStacks(1,1,[genmet_stack],             subdir+prefix+"genmet", False)
drawNMStacks(1,1,[genmet_reversed_stack],             subdir+prefix+"genmet_reversed", False)
drawNMStacks(1,1,[ngoodVertices_stack],             subdir+prefix+"ngoodVertices", False)
