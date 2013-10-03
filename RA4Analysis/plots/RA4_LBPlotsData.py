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
#data["bins"]    = ['Run2010A-Nov4ReReco','Run2010B-Nov4ReReco', 'Run2010B-Nov4ReReco-2e32']
data["bins"]    = ['Run2010A-Nov4ReReco', 'Run2010B-Nov4ReReco-2e32']

data["specialCuts"] = []
allSamples.append(data)
#targetLumi = 3.16+18.08 +14.52 
targetLumi = 3.16+14.52 

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
  signal["dirname"] = "/scratch/schoef/pat_101203/Mu/383/"
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


## plots for studying preselection 
topIsLargest = True
minimum=10**(-1.5)
signalNumbers = [0,1]
presel = "4j30"
subdir = "/pngPAT/"
#presel = "2j503j30"
#presel = "2j503j20"
#presel = "2j504j20"

chainstring = "empty"
commoncf = "(0)"
prefix="empty_"

if presel == "4j30":
  chainstring = "RA4Analyzer/Events"
  commoncf = "RA4Events.jet1pt>30&&RA4Events.jet3pt>30&&RA4Events.lepton_pt>15&&RA4Events.singleMuonic"
if presel == "pf-4j30":
  chainstring = "pfRA4Analyzer/Events"
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

prefix= "Full-38X_"+presel+"_"

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

#finn_met_stack = getStack(":RA4Events.met;#slash{E}_{T} [GeV];Number of Events / 20 GeV",[16,0,320], finn_cf, [] , topIsLargest)
#allStacks.append(finn_met_stack)
met_stack = getStack(":RA4Events.met;#slash{E}_{T} [GeV];Number of Events / 20 GeV",[21,0,420], commoncf, signalNumbers, topIsLargest)
allStacks.append(met_stack)
mT_stack  = getStack(":RA4Events.mT;m_{T} [GeV];Number of Events / 20 GeV",[21,0,420], commoncf, signalNumbers, topIsLargest)
allStacks.append(mT_stack)
jet0_pt_stack                     = getStack(":RA4Events.jet0pt;p_{T, jet_{0}} [GeV];Number of Events / 20 GeV",[31,10,630], commoncf, signalNumbers, topIsLargest)
allStacks.append(jet0_pt_stack)
jet1_pt_stack                     = getStack(":RA4Events.jet1pt;p_{T, jet_{1}} [GeV];Number of Events / 20 GeV",[19,10,390], commoncf, signalNumbers, topIsLargest)
allStacks.append(jet1_pt_stack)
jet2_pt_stack                     = getStack(":RA4Events.jet2pt;p_{T, jet_{2}} [GeV];Number of Events / 20 GeV",[19,10,390], commoncf, signalNumbers, topIsLargest)
allStacks.append(jet2_pt_stack)
jet3_pt_stack                     = getStack(":RA4Events.jet3pt;p_{T, jet_{3}} [GeV];Number of Events / 20 GeV",[19,10,390], commoncf, signalNumbers, topIsLargest)
allStacks.append(jet3_pt_stack)
kinMetSig_stack                   = getStack(":RA4Events.kinMetSig;S_{MET};Number of Events",[31,0,31], commoncf, signalNumbers, topIsLargest)
allStacks.append(kinMetSig_stack)
ht_stack                          = getStack(":RA4Events.ht;HT [GeV];Number of Events / 50 GeV",[31,0,1550], commoncf, signalNumbers, topIsLargest)
allStacks.append(ht_stack)
ht2had_stack                      = getStack(":RA4Events.ht2;HT_{2}^{had.} [GeV];Number of Events / 30 GeV",[36,0,1080], commoncf, signalNumbers, topIsLargest)
allStacks.append(ht2had_stack)
ht2_stack                         = getStack(":RA4Events.ht2+lepton_pt;HT_{2} [GeV];Number of Events / 30 GeV",[36,0,1080], commoncf, signalNumbers, topIsLargest)
allStacks.append(ht2_stack)

met_kMs35_stack = getStack(":RA4Events.met;#slash{E}_{T} [GeV];Number of Events / 20 GeV",[21,0,420], commoncf+"&&kinMetSig>3.5", signalNumbers, topIsLargest)
allStacks.append(met_kMs35_stack)
mT_kMs35_stack  = getStack(":RA4Events.mT;m_{T} [GeV];Number of Events / 20 GeV",[21,0,420], commoncf+"&&kinMetSig>3.5", signalNumbers, topIsLargest)
allStacks.append(mT_kMs35_stack)
jet0_pt_kMs35_stack                     = getStack(":RA4Events.jet0pt;p_{T, jet_{0}} [GeV];Number of Events / 20 GeV",[31,10,630], commoncf+"&&kinMetSig>3.5", signalNumbers, topIsLargest)
allStacks.append(jet0_pt_kMs35_stack)
jet1_pt_kMs35_stack                     = getStack(":RA4Events.jet1pt;p_{T, jet_{1}} [GeV];Number of Events / 20 GeV",[19,10,390], commoncf+"&&kinMetSig>3.5", signalNumbers, topIsLargest)
allStacks.append(jet1_pt_kMs35_stack)
jet2_pt_kMs35_stack                     = getStack(":RA4Events.jet2pt;p_{T, jet_{2}} [GeV];Number of Events / 20 GeV",[19,10,390], commoncf+"&&kinMetSig>3.5", signalNumbers, topIsLargest)
allStacks.append(jet2_pt_kMs35_stack)
jet3_pt_kMs35_stack                     = getStack(":RA4Events.jet3pt;p_{T, jet_{3}} [GeV];Number of Events / 20 GeV",[19,10,390], commoncf+"&&kinMetSig>3.5", signalNumbers, topIsLargest)
allStacks.append(jet3_pt_kMs35_stack)
ht_kMs35_stack                          = getStack(":RA4Events.ht;HT [GeV];Number of Events / 50 GeV",[31,0,1550], commoncf+"&&kinMetSig>3.5", signalNumbers, topIsLargest)
allStacks.append(ht_kMs35_stack)
ht2had_kMs35_stack                      = getStack(":RA4Events.ht2;HT_{2}^{had.} [GeV];Number of Events / 30 GeV",[36,0,1080], commoncf+"&&kinMetSig>3.5", signalNumbers, topIsLargest)
allStacks.append(ht2had_kMs35_stack)
ht2_kMs35_stack                         = getStack(":RA4Events.ht2+lepton_pt;HT_{2} [GeV];Number of Events / 30 GeV",[36,0,1080], commoncf+"&&kinMetSig>3.5", signalNumbers, topIsLargest)
allStacks.append(ht2_kMs35_stack)

#met_kMs5_stack = getStack(":RA4Events.met;#slash{E}_{T} [GeV];Number of Events / 20 GeV",[21,0,420], commoncf+"&&kinMetSig>5", signalNumbers, topIsLargest)
#allStacks.append(met_kMs5_stack)
#mT_kMs5_stack  = getStack(":RA4Events.mT;m_{T} [GeV];Number of Events / 20 GeV",[21,0,420], commoncf+"&&kinMetSig>5", signalNumbers, topIsLargest)
#allStacks.append(mT_kMs5_stack)
#jet0_pt_kMs5_stack                     = getStack(":RA4Events.jet0pt;p_{T, jet_{0}} [GeV];Number of Events / 20 GeV",[31,10,630], commoncf+"&&kinMetSig>5", signalNumbers, topIsLargest)
#allStacks.append(jet0_pt_kMs5_stack)
#jet1_pt_kMs5_stack                     = getStack(":RA4Events.jet1pt;p_{T, jet_{1}} [GeV];Number of Events / 20 GeV",[19,10,390], commoncf+"&&kinMetSig>5", signalNumbers, topIsLargest)
#allStacks.append(jet1_pt_kMs5_stack)
#jet2_pt_kMs5_stack                     = getStack(":RA4Events.jet2pt;p_{T, jet_{2}} [GeV];Number of Events / 20 GeV",[19,10,390], commoncf+"&&kinMetSig>5", signalNumbers, topIsLargest)
#allStacks.append(jet2_pt_kMs5_stack)
#jet3_pt_kMs5_stack                     = getStack(":RA4Events.jet3pt;p_{T, jet_{3}} [GeV];Number of Events / 20 GeV",[19,10,390], commoncf+"&&kinMetSig>5", signalNumbers, topIsLargest)
#allStacks.append(jet3_pt_kMs5_stack)
#ht_kMs5_stack                          = getStack(":RA4Events.ht;HT [GeV];Number of Events / 50 GeV",[31,0,1550], commoncf+"&&kinMetSig>5", signalNumbers, topIsLargest)
#allStacks.append(ht_kMs5_stack)
#ht2had_kMs5_stack                      = getStack(":RA4Events.ht2;HT_{2}^{had.} [GeV];Number of Events / 30 GeV",[36,0,1080], commoncf+"&&kinMetSig>5", signalNumbers, topIsLargest)
#allStacks.append(ht2had_kMs5_stack)
#ht2_kMs5_stack                         = getStack(":RA4Events.ht2+lepton_pt;HT_{2} [GeV];Number of Events / 30 GeV",[36,0,1080], commoncf+"&&kinMetSig>5", signalNumbers, topIsLargest)
#allStacks.append(ht2_kMs5_stack)

met_HT2_150_stack = getStack(":RA4Events.met;#slash{E}_{T} [GeV];Number of Events / 20 GeV",[21,0,420], commoncf+"&&ht2>150", signalNumbers, topIsLargest)
allStacks.append(met_HT2_150_stack)
mT_HT2_150_stack  = getStack(":RA4Events.mT;m_{T} [GeV];Number of Events / 20 GeV",[21,0,420], commoncf+"&&ht2>150", signalNumbers, topIsLargest)
allStacks.append(mT_HT2_150_stack)
jet0_pt_HT2_150_stack                     = getStack(":RA4Events.jet0pt;p_{T, jet_{0}} [GeV];Number of Events / 20 GeV",[31,10,630], commoncf+"&&ht2>150", signalNumbers, topIsLargest)
allStacks.append(jet0_pt_HT2_150_stack)
jet1_pt_HT2_150_stack                     = getStack(":RA4Events.jet1pt;p_{T, jet_{1}} [GeV];Number of Events / 20 GeV",[19,10,390], commoncf+"&&ht2>150", signalNumbers, topIsLargest)
allStacks.append(jet1_pt_HT2_150_stack)
jet2_pt_HT2_150_stack                     = getStack(":RA4Events.jet2pt;p_{T, jet_{2}} [GeV];Number of Events / 20 GeV",[19,10,390], commoncf+"&&ht2>150", signalNumbers, topIsLargest)
allStacks.append(jet2_pt_HT2_150_stack)
jet3_pt_HT2_150_stack                     = getStack(":RA4Events.jet3pt;p_{T, jet_{3}} [GeV];Number of Events / 20 GeV",[19,10,390], commoncf+"&&ht2>150", signalNumbers, topIsLargest)
allStacks.append(jet3_pt_HT2_150_stack)
kinMetSig_HT2_150_stack                   = getStack(":RA4Events.kinMetSig;S_{MET};Number of Events",[31,0,31], commoncf+"&&ht2>150", signalNumbers, topIsLargest)
allStacks.append(kinMetSig_HT2_150_stack)
ht_HT2_150_stack                          = getStack(":RA4Events.ht;HT [GeV];Number of Events / 50 GeV",[31,0,1550], commoncf+"&&ht2>150", signalNumbers, topIsLargest)
allStacks.append(ht_HT2_150_stack)
ht2_HT2_150_stack                         = getStack(":RA4Events.ht2+lepton_pt;HT_{2} [GeV];Number of Events / 30 GeV",[36,0,1080], commoncf+"&&ht2>150", signalNumbers, topIsLargest)
allStacks.append(ht2_HT2_150_stack)

#lepton_pt_stack = getStack("p_{T} [GeV]:RA4Events.lepton_pt;p_{T,lep.} [GeV];Number of Events / 20 GeV",[19,0,380], commoncf, signalNumbers, topIsLargest)
#allStacks.append(lepton_pt_stack)
#lepton_eta_stack                  = getStack(":RA4Events.lepton_eta;|#eta^{#mu}|;Number of Events",[31,0,3.1], commoncf, signalNumbers, topIsLargest)
#allStacks.append(lepton_eta_stack)
#
#lepton_dxy_stack                  = getStack(":RA4Events.lepton_dxy;d_{xy};Number of Events / 10 #mu m",[40,0,0.04], commoncf, signalNumbers, topIsLargest)
#allStacks.append(lepton_dxy_stack)
#lepton_vertex_dz_stack                  = getStack(":RA4Events.lepton_vertex_dz;d_{z, V};Number of Events / 10 #mu m",[40,-.201,.201], commoncf, signalNumbers, topIsLargest)
#allStacks.append(lepton_vertex_dz_stack)
#lepton_isGlobalPromptTight_stack  = getStack(":RA4Events.lepton_isGlobalMuonPromptTight;isGlobalPromptTight;Number of Events",[2,-.5,1.5], commoncf, signalNumbers, topIsLargest)
#lepton_isGlobalPromptTight_stack[0].legendCoordinates[0] = 0.16 
#lepton_isGlobalPromptTight_stack[0].legendCoordinates[2] = 0.16+0.23 
#allStacks.append(lepton_isGlobalPromptTight_stack)
#
#lepton_relIso_stack               = getStack(":RA4Events.lepton_relIso;relIso;Number of Events / 2 MeV",[30,0,0.06], commoncf, signalNumbers, topIsLargest)
#allStacks.append(lepton_relIso_stack)
#
#lepton_deltaR_stack          = getStack(":RA4Events.lepton_deltaR;#Delta R(l,jets);Number of Events",[101,0,6.28], commoncf, signalNumbers, topIsLargest)
#allStacks.append(lepton_deltaR_stack)

for stack in allStacks:
  stack[0].minimum = minimum

#for stack in allStacks:
#  for var in stack:
#    var.addOverFlowBin = "both"

execfile("simplePlotsKernel.py")

for stack in allStacks:
  stack[0].maximum = 3.*stack[-1].data_histo.GetMaximum()
  stack[0].logy = True

#drawNMStacks(1,1,[finn_met_stack],             "pngPAT/"+prefix+"finn_met.png", False)
#finn_met_stack[0].logy = False
#finn_met_stack[0].maximum = 1.2*finn_met_stack[-1].data_histo.GetMaximum()
#drawNMStacks(1,1,[finn_met_stack],             "pngPAT/"+prefix+"finn_met_lin.png", False)

drawNMStacks(1,1,[met_stack],             subdir+prefix+"met.png", False)
drawNMStacks(1,1,[mT_stack],              subdir+prefix+"mT.png", False)
drawNMStacks(1,1,[kinMetSig_stack],       subdir+prefix+"kinMetSig.png", False)
drawNMStacks(1,1,[ht_stack],              subdir+prefix+"ht.png", False)
drawNMStacks(1,1,[ht2had_stack],          subdir+prefix+"ht2had.png", False)
drawNMStacks(1,1,[ht2_stack],             subdir+prefix+"ht2.png", False)
drawNMStacks(1,1,[jet0_pt_stack],         subdir+prefix+"jet0_pt.png", False)
drawNMStacks(1,1,[jet1_pt_stack],         subdir+prefix+"jet1_pt.png", False)
drawNMStacks(1,1,[jet2_pt_stack],         subdir+prefix+"jet2_pt.png", False)
drawNMStacks(1,1,[jet3_pt_stack],         subdir+prefix+"jet3_pt.png", False)

#drawNMStacks(1,1,[met_kMs5_stack],             subdir+prefix+"kMs-5_met.png", False)
#drawNMStacks(1,1,[mT_kMs5_stack],              subdir+prefix+"kMs-5_mT.png", False)
#drawNMStacks(1,1,[ht_kMs5_stack],              subdir+prefix+"kMs-5_ht.png", False)
#drawNMStacks(1,1,[ht2had_kMs5_stack],          subdir+prefix+"kMs-5_ht2had.png", False)
#drawNMStacks(1,1,[ht2_kMs5_stack],             subdir+prefix+"kMs-5_ht2.png", False)
#drawNMStacks(1,1,[jet0_pt_kMs5_stack],         subdir+prefix+"kMs-5_jet0_pt.png", False)
#drawNMStacks(1,1,[jet1_pt_kMs5_stack],         subdir+prefix+"kMs-5_jet1_pt.png", False)
#drawNMStacks(1,1,[jet2_pt_kMs5_stack],         subdir+prefix+"kMs-5_jet2_pt.png", False)
#drawNMStacks(1,1,[jet3_pt_kMs5_stack],         subdir+prefix+"kMs-5_jet3_pt.png", False)
#
drawNMStacks(1,1,[met_kMs35_stack],             subdir+prefix+"kMs-3.5_met.png", False)
drawNMStacks(1,1,[mT_kMs35_stack],              subdir+prefix+"kMs-3.5_mT.png", False)
drawNMStacks(1,1,[ht_kMs35_stack],              subdir+prefix+"kMs-3.5_ht.png", False)
drawNMStacks(1,1,[ht2had_kMs35_stack],          subdir+prefix+"kMs-3.5_ht2had.png", False)
drawNMStacks(1,1,[ht2_kMs35_stack],             subdir+prefix+"kMs-3.5_ht2.png", False)
drawNMStacks(1,1,[jet0_pt_kMs35_stack],         subdir+prefix+"kMs-3.5_jet0_pt.png", False)
drawNMStacks(1,1,[jet1_pt_kMs35_stack],         subdir+prefix+"kMs-3.5_jet1_pt.png", False)
drawNMStacks(1,1,[jet2_pt_kMs35_stack],         subdir+prefix+"kMs-3.5_jet2_pt.png", False)
drawNMStacks(1,1,[jet3_pt_kMs35_stack],         subdir+prefix+"kMs-3.5_jet3_pt.png", False)

drawNMStacks(1,1,[met_HT2_150_stack],             subdir+prefix+"HT2-150_met.png", False)
drawNMStacks(1,1,[mT_HT2_150_stack],              subdir+prefix+"HT2-150_mT.png", False)
drawNMStacks(1,1,[kinMetSig_HT2_150_stack],       subdir+prefix+"HT2-150_kinMetSig.png", False)
drawNMStacks(1,1,[ht_HT2_150_stack],              subdir+prefix+"HT2-150_ht.png", False)
drawNMStacks(1,1,[ht2_HT2_150_stack],             subdir+prefix+"HT2-150_ht2.png", False)
drawNMStacks(1,1,[jet0_pt_HT2_150_stack],         subdir+prefix+"HT2-150_jet0_pt.png", False)
drawNMStacks(1,1,[jet1_pt_HT2_150_stack],         subdir+prefix+"HT2-150_jet1_pt.png", False)
drawNMStacks(1,1,[jet2_pt_HT2_150_stack],         subdir+prefix+"HT2-150_jet2_pt.png", False)
drawNMStacks(1,1,[jet3_pt_HT2_150_stack],         subdir+prefix+"HT2-150_jet3_pt.png", False)

#drawNMStacks(1,1,[lepton_pt_stack],                   subdir+prefix+"lepton_pt", False)
#drawNMStacks(1,1,[lepton_eta_stack],                  subdir+prefix+"lepton_eta", False)
#drawNMStacks(1,1,[lepton_relIso_stack],               subdir+prefix+"lepton_relIso", False)
#drawNMStacks(1,1,[lepton_deltaR_stack],               subdir+prefix+"lepton_deltaR", False)
#drawNMStacks(1,1,[lepton_dxy_stack],                  subdir+prefix+"lepton_dxy", False)
#drawNMStacks(1,1,[lepton_vertex_dz_stack],            subdir+prefix+"lepton_vertex_dz", False)
#drawNMStacks(1,1,[lepton_isGlobalPromptTight_stack],  subdir+prefix+"lepton_isGlobalPromptTight", False)

#drawNMStacks(1,1,[btag0_stack],            subdir+prefix+"btag0", False)
#drawNMStacks(1,1,[btag1_stack],            subdir+prefix+"btag1", False)
#drawNMStacks(1,1,[btag2_stack],            subdir+prefix+"btag2", False)
#drawNMStacks(1,1,[jet0btag_stack],         subdir+prefix+"jet0btag", False)
#drawNMStacks(1,1,[jet1btag_stack],         subdir+prefix+"jet1btag", False)
#drawNMStacks(1,1,[jet2btag_stack],         subdir+prefix+"jet2btag", False)
#drawNMStacks(1,1,[jet3btag_stack],         subdir+prefix+"jet3btag", False)

for stack in allStacks:
  stack[0].maximum = 1.2*stack[-1].data_histo.GetMaximum()
  stack[0].logy = False

drawNMStacks(1,1,[met_stack],             subdir+prefix+"met_lin.png", False)
drawNMStacks(1,1,[mT_stack],              subdir+prefix+"mT_lin.png", False)
drawNMStacks(1,1,[kinMetSig_stack],       subdir+prefix+"kinMetSig_lin.png", False)
drawNMStacks(1,1,[ht_stack],              subdir+prefix+"ht_lin.png", False)
drawNMStacks(1,1,[ht2had_stack],          subdir+prefix+"ht2had_lin.png", False)
drawNMStacks(1,1,[ht2_stack],             subdir+prefix+"ht2_lin.png", False)
drawNMStacks(1,1,[jet0_pt_stack],         subdir+prefix+"jet0_pt_lin.png", False)
drawNMStacks(1,1,[jet1_pt_stack],         subdir+prefix+"jet1_pt_lin.png", False)
drawNMStacks(1,1,[jet2_pt_stack],         subdir+prefix+"jet2_pt_lin.png", False)
drawNMStacks(1,1,[jet3_pt_stack],         subdir+prefix+"jet3_pt_lin.png", False)

#drawNMStacks(1,1,[met_kMs5_stack],             subdir+prefix+"kMs-5_met_lin.png", False)
#drawNMStacks(1,1,[mT_kMs5_stack],              subdir+prefix+"kMs-5_mT_lin.png", False)
#drawNMStacks(1,1,[kinMetSig_kMs5_stack],       subdir+prefix+"kMs-5_kinMetSig_lin.png", False)
#drawNMStacks(1,1,[ht_kMs5_stack],              subdir+prefix+"kMs-5_ht_lin.png", False)
#drawNMStacks(1,1,[ht2had_kMs5_stack],          subdir+prefix+"kMs-5_ht2had_lin.png", False)
#drawNMStacks(1,1,[ht2_kMs5_stack],             subdir+prefix+"kMs-5_ht2_lin.png", False)
#drawNMStacks(1,1,[jet0_pt_kMs5_stack],         subdir+prefix+"kMs-5_jet0_pt_lin.png", False)
#drawNMStacks(1,1,[jet1_pt_kMs5_stack],         subdir+prefix+"kMs-5_jet1_pt_lin.png", False)
#drawNMStacks(1,1,[jet2_pt_kMs5_stack],         subdir+prefix+"kMs-5_jet2_pt_lin.png", False)
#drawNMStacks(1,1,[jet3_pt_kMs5_stack],         subdir+prefix+"kMs-5_jet3_pt_lin.png", False)

drawNMStacks(1,1,[met_kMs35_stack],             subdir+prefix+"kMs-3.5_met_lin.png", False)
drawNMStacks(1,1,[mT_kMs35_stack],              subdir+prefix+"kMs-3.5_mT_lin.png", False)
drawNMStacks(1,1,[ht_kMs35_stack],              subdir+prefix+"kMs-3.5_ht_lin.png", False)
drawNMStacks(1,1,[ht2had_kMs35_stack],          subdir+prefix+"kMs-3.5_ht2had_lin.png", False)
drawNMStacks(1,1,[ht2_kMs35_stack],             subdir+prefix+"kMs-3.5_ht2_lin.png", False)
drawNMStacks(1,1,[jet0_pt_kMs35_stack],         subdir+prefix+"kMs-3.5_jet0_pt_lin.png", False)
drawNMStacks(1,1,[jet1_pt_kMs35_stack],         subdir+prefix+"kMs-3.5_jet1_pt_lin.png", False)
drawNMStacks(1,1,[jet2_pt_kMs35_stack],         subdir+prefix+"kMs-3.5_jet2_pt_lin.png", False)
drawNMStacks(1,1,[jet3_pt_kMs35_stack],         subdir+prefix+"kMs-3.5_jet3_pt_lin.png", False)

drawNMStacks(1,1,[met_HT2_150_stack],             subdir+prefix+"HT2-150_met_lin.png", False)
drawNMStacks(1,1,[mT_HT2_150_stack],              subdir+prefix+"HT2-150_mT_lin.png", False)
drawNMStacks(1,1,[kinMetSig_HT2_150_stack],       subdir+prefix+"HT2-150_kinMetSig_lin.png", False)
drawNMStacks(1,1,[ht_HT2_150_stack],              subdir+prefix+"HT2-150_ht_lin.png", False)
drawNMStacks(1,1,[ht2_HT2_150_stack],             subdir+prefix+"HT2-150_ht2_lin.png", False)
drawNMStacks(1,1,[jet0_pt_HT2_150_stack],         subdir+prefix+"HT2-150_jet0_pt_lin.png", False)
drawNMStacks(1,1,[jet1_pt_HT2_150_stack],         subdir+prefix+"HT2-150_jet1_pt_lin.png", False)
drawNMStacks(1,1,[jet2_pt_HT2_150_stack],         subdir+prefix+"HT2-150_jet2_pt_lin.png", False)
drawNMStacks(1,1,[jet3_pt_HT2_150_stack],         subdir+prefix+"HT2-150_jet3_pt_lin.png", False)

#drawNMStacks(1,1,[lepton_pt_stack],                   subdir+prefix+"lepton_pt_lin", False)
#drawNMStacks(1,1,[lepton_eta_stack],                  subdir+prefix+"lepton_eta_lin", False)
#drawNMStacks(1,1,[lepton_relIso_stack],               subdir+prefix+"lepton_relIso_lin", False)
#drawNMStacks(1,1,[lepton_deltaR_stack],               subdir+prefix+"lepton_deltaR_lin", False)
#drawNMStacks(1,1,[lepton_dxy_stack],                  subdir+prefix+"lepton_dxy_lin", False)
#drawNMStacks(1,1,[lepton_vertex_dz_stack],            subdir+prefix+"lepton_vertex_dz_lin", False)
#drawNMStacks(1,1,[lepton_isGlobalPromptTight_stack],  subdir+prefix+"lepton_isGlobalPromptTight_lin", False)

#drawNMStacks(1,1,[btag0_stack],            subdir+prefix+"btag0_lin", False)
#drawNMStacks(1,1,[btag1_stack],            subdir+prefix+"btag1_lin", False)
#drawNMStacks(1,1,[btag2_stack],            subdir+prefix+"btag2_lin", False)
#drawNMStacks(1,1,[jet0btag_stack],         subdir+prefix+"jet0btag_lin", False)
#drawNMStacks(1,1,[jet1btag_stack],         subdir+prefix+"jet1btag_lin", False)
#drawNMStacks(1,1,[jet2btag_stack],         subdir+prefix+"jet2btag_lin", False)
#drawNMStacks(1,1,[jet3btag_stack],         subdir+prefix+"jet3btag_lin", False)

