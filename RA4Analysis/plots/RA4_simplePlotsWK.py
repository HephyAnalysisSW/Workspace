import ROOT
from array import array
from math import *
import os, copy

from simplePlotsCommon import *
#execfile("simplePlotsCommon.py")
import xsec
small = False

allSamples=[]

data={}
data["name"]     = "Data";
data["dirname"] = "/scratch/schoef/pat_101128/Mu/383/"
data["bins"]    = ['Run2010A-Nov4ReReco','Run2010B-Nov4ReReco', 'Run2010B-Nov4ReReco-2e32']
#data["bins"]    = ['Run2010A-Nov4ReReco','Run2010B-Nov4ReReco']

data["specialCuts"] = []
allSamples.append(data)
targetLumi = 3.16+18.08 +14.52 

ewk={}
ewk["name"]     = "EWK";
ewk["dirname"] = "/scratch/schoef/pat_101203/Mu/383/"
ewk["specialCuts"] = []
#WJets_Bins = ["W0Jets_Pt0to100","W1Jets_Pt0to100", "W2Jets_Pt0to100", "W3Jets_Pt0to100", "W4Jets_Pt0to100", "W5Jets_Pt0to100", "W1Jets_Pt100to300", "W2Jets_Pt100to300", "W3Jets_Pt100to300", "W4Jets_Pt100to300", "W5Jets_Pt100to300", "W1Jets_Pt300to800", "W2Jets_Pt300to800", "W3Jets_Pt300to800", "W4Jets_Pt300to800", "W5Jets_Pt300to800", "W1Jets_Pt800to1600","W2Jets_Pt800to1600","W3Jets_Pt800to1600","W4Jets_Pt800to1600","W5Jets_Pt800to1600"]
WJets_Bins = ["W1Jets_ptW-0to100","W1Jets_ptW-100to300","W1Jets_ptW-300to800","W1Jets_ptW-800to1600","W2Jets_ptW-0to100","W2Jets_ptW-100to300","W2Jets_ptW-300to800","W2Jets_ptW-800to1600","W3Jets_ptW-0to100","W3Jets_ptW-100to300","W3Jets_ptW-300to800","W3Jets_ptW-800to1600","W4Jets_ptW-0to100","W4Jets_ptW-100to300","W4Jets_ptW-300to800","W4Jets_ptW-800to1600","W5Jets_ptW-0to100","W5Jets_ptW-100to300","W5Jets_ptW-300to800","W5Jets_ptW-800to1600"]
#WJets_Bins = ["WJets"]
ZJets_Bins = ["ZJets"]
ewk["bins"] =  ["TTJets"]         #WARNING: pat_101124/383 copied from pat_101109/363
ewk["bins"].extend(WJets_Bins)
ewk["bins"].extend(ZJets_Bins)
allSamples.append(ewk) 

qcd={}
qcd["name"]     = "QCD";
qcd["dirname"] = "/scratch/schoef/pat_101203/Mu/383/"
qcd["specialCuts"] = []
qcd["bins"] =  ["QCD_Pt20to30_MuPt5Enriched",  "QCD_Pt30to50_MuPt5Enriched", "QCD_Pt50to80_MuPt5Enriched",  "QCD_Pt80to120_MuPt5Enriched", "QCD_Pt120to150_MuPt5Enriched", "QCD_Pt150_MuPt5Enriched"]
allSamples.append(qcd) 

def getSignal(n):
  signal={}
  signal["name"]     = "LM"+str(n);
  signal["dirname"] = "/scratch/schoef/pat_101203/Mu/363/"
  signal["bins"] = [signal["name"]]
  return signal
signals = {}
for i in range(0,10):
  sig = getSignal(i)
  allSamples.append(sig)
  signals[str(i)] = sig


allVars=[]
allStacks=[]

signalColors = [ROOT.kBlack, ROOT.kBlue + 1, ROOT.kGreen + 2, ROOT.kOrange + 2]

### plots with 2j30
#topIsLargest = True
#signalNumbers = []
#commoncf = "RA4Events.jet1pt>30&&RA4Events.lepton_pt>20&&RA4Events.singleMuonic"
#prefix="RA4_2j30_Data38_38X363_"
#minimum=10**(-1.5)

### plots with SIGNAL
#topIsLargest = True
#signalNumbers = [0,1]
#commoncf = "RA4Events.njets==2&&RA4Events.jet1pt>30&&RA4Events.lepton_pt>15&&RA4Events.singleMuonic"
##commoncf = "RA4Events.jet2pt>30&&RA4Events.lepton_pt>15&&RA4Events.lepton_relIso<0.1&&RA4Events.ngoodMuons>=1"
#
#prefix="17pb_3j30_"
#minimum=10**(-2.5)

#topIsLargest = False
#signalNumbers = [1]
#commoncf = "RA4Events.jet3pt>30&&RA4Events.lepton_pt>20&&RA4Events.singleMuonic&&RA4Events.lepton_pt>15&&RA4Events.lepton_pt<30"
#prefix="10nb_38X36X_l-pt15to30_"
##minimum=10**(-2.5)

## plots for studying preselection 
topIsLargest = True
minimum=10**(-1.5)
signalNumbers = [0,1]
#presel = "4j30"
presel = "2j503j30"
#presel = "2j503j20"
#presel = "2j504j20"

chainstring = "empty"
commoncf = "(0)"
prefix="empty_"

if presel == "4j30":
  chainstring = "RA4Analyzer/Events"
  commoncf = "RA4Events.jet1pt>30&&RA4Events.jet3pt>30&&RA4Events.lepton_pt>15&&RA4Events.singleMuonic"
if presel == "2j503j30":
  chainstring = "RA4Analyzer/Events"
  commoncf = "RA4Events.jet1pt>50&&RA4Events.jet2pt>30&&RA4Events.lepton_pt>15&&RA4Events.singleMuonic"
if presel == "2j503j20":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "RA4Events.jet1pt>50&&RA4Events.jet2pt>20&&RA4Events.lepton_pt>15&&RA4Events.singleMuonic"
if presel == "2j504j20":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "RA4Events.jet1pt>50&&RA4Events.jet3pt>20&&RA4Events.lepton_pt>15&&RA4Events.singleMuonic"

prefix= "WK_"+presel+"_"

for sample in allSamples:
  sample["Chain"] = chainstring

def getStack(varstring, binning, cutstring, signalNumbers, topIsLargest = False):
  DATA          = variable(varstring, binning, cutstring)
  DATA.sample   = data
#  DATA.color    = ROOT.kGray
  DATA.color    = dataColor
  DATA.legendText="Data"
  MC_QCD                       = variable(varstring, binning, cutstring)
  MC_QCD.minimum               = 5*10**(-1)
  MC_QCD.sample                = qcd 
  MC_TTJETS                    = copy.deepcopy(MC_QCD)
  MC_TTJETS.sample             = copy.deepcopy(ewk)
  MC_TTJETS.sample["bins"]     = ["TTJets"]
  MC_WJETS                     = copy.deepcopy(MC_QCD)
  MC_WJETS.sample              = copy.deepcopy(ewk)
  MC_WJETS.sample["bins"]      = WJets_Bins
  MC_ZJETS                     = copy.deepcopy(MC_QCD)
  MC_ZJETS.sample              = copy.deepcopy(ewk)
  MC_ZJETS.sample["bins"]      = ZJets_Bins

  MC_TTJETS.legendText         = "TTJets"
  MC_TTJETS.style              = "f"
  MC_TTJETS.color              = ROOT.kRed - 3
  MC_ZJETS.legendText          = "ZJets"
  MC_ZJETS.style               = "f"
  MC_ZJETS.add                 = [MC_TTJETS]
  MC_ZJETS.color               = ROOT.kGreen + 3
  MC_QCD.color                 = myBlue
  MC_QCD.legendText            = "QCD"
  MC_QCD.style                 = "f"
  MC_QCD.add                   = [MC_ZJETS]
  MC_WJETS.legendText          = "WJets"
  MC_WJETS.style               = "f"
  MC_WJETS.add                 = [MC_QCD]
  MC_WJETS.color               = ROOT.kYellow
#  res = [MC_WJETS, MC_QCD, MC_ZJETS, MC_TTJETS, DATA, ISO_DATA]
  res=[]
  if topIsLargest:
    res = [MC_TTJETS, MC_WJETS, MC_QCD, MC_ZJETS]
    MC_TTJETS.add=[MC_WJETS]
    MC_ZJETS.add=[]
  else:
    res = [MC_WJETS, MC_QCD, MC_ZJETS, MC_TTJETS]
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
    var.legendCoordinates=[0.75,0.95 - 0.04*nhistos,.98,.95]
  res.append(DATA) 
  return res


met_signal_stack = getStack(":RA4Events.met;#slash{E}_{T} [GeV];Number of Events / 20 GeV",[19,0,380], commoncf + "&&RA4Events.m3>=280&&RA4Events.ht>=340&&kinMetSig>=8", signalNumbers, topIsLargest)
allStacks.append(met_signal_stack)

ht_signal_stack                          = getStack(":RA4Events.ht;HT [GeV];Number of Events / 20 GeV",[52,0,1040], commoncf + "&&RA4Events.m3>=280&&kinMetSig>=8", signalNumbers, topIsLargest)
allStacks.append(ht_signal_stack)

m3_signal_stack                          = getStack(":RA4Events.m3;m3 [GeV];Number of Events / 20 GeV",[77,0,1540], commoncf + "RA4Events.ht>=340&&kinMetSig>=8", signalNumbers, topIsLargest)
allStacks.append(m3_signal_stack)

kinMetSig_signal_stack                   = getStack(":RA4Events.kinMetSig;S_{MET};Number of Events",[44,0,44], commoncf + "&&RA4Events.m3>=280&&RA4Events.ht>=340", signalNumbers, topIsLargest)
allStacks.append(kinMetSig_signal_stack)

met_bkg_stack = getStack(":RA4Events.met;#slash{E}_{T} [GeV];Number of Events / 20 GeV",[19,0,380], commoncf + "&&RA4Events.m3<=280&&RA4Events.ht<=340&&kinMetSig<=8", signalNumbers, topIsLargest)
allStacks.append(met_bkg_stack)

ht_bkg_stack                          = getStack(":RA4Events.ht;HT [GeV];Number of Events / 20 GeV",[52,0,1040], commoncf + "&&RA4Events.m3<=280&&kinMetSig<=8", signalNumbers, topIsLargest)
allStacks.append(ht_bkg_stack)

m3_bkg_stack                          = getStack(":RA4Events.m3;m3 [GeV];Number of Events / 20 GeV",[77,0,1540], commoncf + "RA4Events.ht<=340&&kinMetSig<=8", signalNumbers, topIsLargest)
allStacks.append(m3_bkg_stack)

kinMetSig_bkg_stack                   = getStack(":RA4Events.kinMetSig;S_{MET};Number of Events",[44,0,44], commoncf + "&&RA4Events.m3<=280&&RA4Events.ht<=340", signalNumbers, topIsLargest)
allStacks.append(kinMetSig_bkg_stack)

#for stack in allStacks:
#  for var in stack:
#    var.addOverFlowBin = "both"

execfile("simplePlotsKernel.py")

for stack in allStacks:
  stack[0].maximum = 3.*stack[-1].data_histo.GetMaximum()
  stack[0].logy = True

drawNMStacks(1,1,[met_signal_stack], "pngFit/"+prefix+"met_signal.png")
drawNMStacks(1,1,[ht_signal_stack], "pngFit/"+prefix+"ht_signal.png")
drawNMStacks(1,1,[m3_signal_stack], "pngFit/"+prefix+"m3_signal.png")
drawNMStacks(1,1,[kinMetSig_signal_stack], "pngFit/"+prefix+"kinMetSig_signal.png")

drawNMStacks(1,1,[met_bkg_stack], "pngFit/"+prefix+"met_bkg.png")
drawNMStacks(1,1,[ht_bkg_stack], "pngFit/"+prefix+"ht_bkg.png")
drawNMStacks(1,1,[m3_bkg_stack], "pngFit/"+prefix+"m3_bkg.png")
drawNMStacks(1,1,[kinMetSig_bkg_stack], "pngFit/"+prefix+"kinMetSig_bkg.png")

