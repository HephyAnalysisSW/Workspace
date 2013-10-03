import ROOT
from array import array
from math import *
import os, copy

from simplePlotsCommon import *
import xsec
small = False
doWstacks = True
allSamples=[]

from defaultMu2012Samples import *

#prefix = "ht-300-500_"
additionalCut = ""
prefix = "bkgTauDec_3jet40_met-100_ht-450"
commoncf = "jet2pt>40&&singleMuonic&&met>100&&ht>450"
subdir = "8TeV/"
chainstring = "Events"

for sample in allSamples:
  sample["Chain"] = chainstring
  sample["hasWeight"] = False
#  sample["dirname"] = "/data/schoef/convertedTuples_v5/copy/"
#signalColors = [ROOT.kBlack, ROOT.kRed + 1, ROOT.kBlue + 2, ROOT.kGreen + 2, ROOT.kOrange + 2]
if additionalCut!="":
  commoncf+="&&"+additionalCut

#Check that they are exclusive!
singleMu_W = "&&nuMu+antinuMu==1"
#singleE_W  = "&&nuE+antinuE==1"
#noTau_W    = "&&nuTau+antinuTau==1&&nu_FromTausFromWs==0"
#eleTau_W   = "&&nuTau+antinuTau==1&&nuTau_FromTausFromWs==1&&nuE_FromTausFromWs==1"
muTau_W    = "&&nuTau+antinuTau==1&&nuTauFromTausFromWs==1&&nuMuFromTausFromWs==1"
hadTau_W   = "&&nuTau+antinuTau==1&&nuTauFromTausFromWs==1&&nuEFromTausFromWs+nuMuFromTausFromWs==0"

def adjustLegend(stack):
  nhistos = len(stack)
  stack[0].legendCoordinates = [0.62,0.98-0.05*nhistos,.98,.95]
#  stack[0].lines=[ \
#      [0.6,0.98-0.05*(nhistos+1),"#font[22]{CMS preliminary 2010}"],
#      [0.79,0.98-0.05*(nhistos+2),"#sqrt{s} = 7TeV"]
#      ]

def getShapeStack(stack):
  res=[]
  for var in stack:
    var_c = copy.deepcopy(var)
    var_c.add=[]
    var_c.style="l0"
    res.append(var_c)
  res[0].style = "f0"
  adjustLegend(res)
  return res

def getWStack(varstring, binning, cutstring):
  MC_WJETS_all                       = variable(varstring, binning, cutstring)
  MC_WJETS_all.sample                = wjets
  MC_WJETS_all.color                 = ROOT.kYellow
  MC_WJETS_all.legendText            = "all"
  MC_WJETS_all.style                 = "f0"

  MC_WJETS_muTau                         = variable(varstring, binning, cutstring + muTau_W)
  MC_WJETS_muTau.sample                  = wjets
#  MC_WJETS_muTau.add                     = [MC_WJETS_hadTau]
  MC_WJETS_muTau.color                   = ROOT.kRed + 2
  MC_WJETS_muTau.legendText              = "#tau#rightarrow#mu (2 #nu_{tau} 1 #nu_{#mu})"
  MC_WJETS_muTau.style                   = "f0"


  MC_WJETS_singleMu                       = variable(varstring, binning, cutstring + singleMu_W)
#  MC_WJETS_singleMu.minimum               = 10**(-3)
  MC_WJETS_singleMu.add                   = [MC_WJETS_muTau]
  MC_WJETS_singleMu.sample                = wjets
  MC_WJETS_singleMu.color                 = ROOT.kBlue + 2 
  MC_WJETS_singleMu.legendText            = "1 #mu (1 #nu_{#mu})"
  MC_WJETS_singleMu.style                 = "f0"
  res = [MC_WJETS_all, MC_WJETS_singleMu, MC_WJETS_muTau]
  for var in res:
    var.minimum=0.07
  getLinesForStack(res, targetLumi)
  adjustLegend(res)
  return res 

if doWstacks:
  genmet_Wstack         = getWStack(":genmet;#slash{E}_{T} (GeV);Number of Events / 20 GeV",[52,0,1040], commoncf )
  allStacks.append(genmet_Wstack)
  met_Wstack         = getWStack(":met;#slash{E}_{T} (GeV);Number of Events / 20 GeV",[52,0,1040], commoncf )
  allStacks.append(met_Wstack)
  lepton_pt_Wstack   = getWStack("p_{T}(GeV):leptonPt;p_{T,lep.} (GeV);Number of Events / 20 GeV",[31,0,620], commoncf)
  allStacks.append(lepton_pt_Wstack)
  mT_Wstack          = getWStack(":mT;m_{T} (GeV);Number of Events / 20 GeV",[31,0,620], commoncf)
  allStacks.append(mT_Wstack)
  ht_Wstack      = getWStack(":ht;H_{T} (GeV);Number of Events / 50 GeV",[31,0,1550], commoncf)
  allStacks.append(ht_Wstack)
  kinMetSig_Wstack   = getWStack(":kinMetSig;kin. #slash{E}_{T} Significance;Number of Events",[33,0,33], commoncf)
  allStacks.append(kinMetSig_Wstack)
  m3_Wstack   = getWStack(":m3;M_{3};Number of Events / 30 GeV",[86,0,2600], commoncf)
  allStacks.append(m3_Wstack)

  met_WshapeStack         = getShapeStack(met_Wstack) 
  allStacks.append(met_WshapeStack)
  lepton_pt_WshapeStack   = getShapeStack(lepton_pt_Wstack) 
  allStacks.append(lepton_pt_WshapeStack)
  mT_WshapeStack          = getShapeStack(mT_Wstack) 
  allStacks.append(mT_WshapeStack)
  ht_WshapeStack      = getShapeStack(ht_Wstack) 
  allStacks.append(ht_WshapeStack)
  kinMetSig_WshapeStack   = getShapeStack(kinMetSig_Wstack) 
  allStacks.append(kinMetSig_WshapeStack)
  m3_WshapeStack   = getShapeStack(m3_Wstack) 
  allStacks.append(m3_WshapeStack)

#One MC Muon
Mu_T            = "nuMu+antinuMu==1&&nuE+antinuE+nuTau+antinuTau==0" #1 Muon (nu_mu)
#Two MC Leptons
MuMu_T          = "nuMu==1&&antinuMu==1&&nuE+antinuE+nuTau+antinuTau==0"     #2 Muons (nu_mu, nu_mubar)
MuE_T           = "nuMu+antinuMu==1&&nuE+antinuE==1&&nuTau+antinuTau==0"     #1 Muon, 1 Electron (nu_mu, nu_E)
Taumu_T         = "nuTau+antinuTau==1&&nuE+antinuE+nuMu+antinuMu==0&&nuMuFromTausFromWs==1"  #1 myonic tau (nu_taubar + nu_tau + nu_mu)
MuTaue_T        = "nuTau+antinuTau==1&&nuE+antinuE==0&&nuMu+antinuMu==1&&nuEFromTausFromWs==1"  #1 Myon + 1 electronic tau (nu_mu + nu_e + nu_tau + nu_taubar)
ETaumu_T        = "nuTau+antinuTau==1&&nuE+antinuE==1&&nuMu+antinuMu==0&&nuMuFromTausFromWs==1"  #1 E + 1 myonic tau (nu_e + nu_mu + nu_tau + nu_taubar)
MuTaumu_T       = "nuTau+antinuTau==1&&nuE+antinuE==0&&nuMu+antinuMu==1&&nuMuFromTausFromWs==1"  #1 Mu + 1 myonic tau (nu_mu + nu_mu + nu_tau + nu_taubar)
TauTaumu_T      = "nuTau+antinuTau==2&&nuE+antinuE==0&&nuMu+antinuMu==0&&nuMuFromTausFromWs==1&&nuTauFromTausFromWs==2&&nuEFromTausFromWs==0"  #1 had. Tau + 1 myonic tau (nu_tau + nu_tau + nu_mu + nu_tau)
MuhadTau_T      = "nuTau+antinuTau==1&&nuE+antinuE==0&&nuMu+antinuMu==1&&nuTauFromTausFromWs==1&&nuFromTausFromWs==1"  #1 had. Tau + 1 Muon (nu_mu + nu_tau + nu_taubar )
TaueTaumu_T     = "nuTau+antinuTau==2&&nuE+antinuE==0&&nuMu+antinuMu==0&&nuEFromTausFromWs==1&&nuMuFromTausFromWs==1"  #1 electronic Tau + 1 myonic tau (nu_tau  + nu_taubar + nu_mu + nu_tau + nu_taubar + nu_E)
TaumuTaumu_T    = "nuTau+antinuTau==2&&nuE+antinuE==0&&nuMu+antinuMu==0&&nuEFromTausFromWs==0&&nuMuFromTausFromWs==2"  # 2 myonic tau (nu_tau  + nu_taubar + nu_mu + nu_tau + nu_taubar + nu_mu)

def nor(list):
  res = "!("
  for icond in range(len(list)):
    if icond>0:
      res+="||" 
    res+="("+list[icond]+")"
  res+=")"
  return res 

remaining = nor([Mu_T, MuMu_T, MuE_T, Taumu_T, MuTaue_T, ETaumu_T, MuTaumu_T, TauTaumu_T, MuhadTau_T, TaueTaumu_T, TaumuTaumu_T])
 
def getTStack(varstring, binning, cutstring):
  MC_ttbar_all                       = variable(varstring, binning, cutstring)
  MC_ttbar_all.sample                = ttbar
  MC_ttbar_all.color                 = ROOT.kYellow
  MC_ttbar_all.legendText            = "all"
  MC_ttbar_all.style                 = "f0"

  MC_ttbar_TaumuTaumu                       = variable(varstring, binning, cutstring + "&&" +  TaumuTaumu_T)
  MC_ttbar_TaumuTaumu.sample                = ttbar
  MC_ttbar_TaumuTaumu.color                 = ROOT.kRed + 2
  MC_ttbar_TaumuTaumu.legendText            = "2 #tau#rightarrow#mu (6 #nu)"
  MC_ttbar_TaumuTaumu.style                 = "f0"

  MC_ttbar_TaueTaumu                       = variable(varstring, binning, cutstring + "&&" +  TaueTaumu_T)
  MC_ttbar_TaueTaumu.add                   = [MC_ttbar_TaumuTaumu]
  MC_ttbar_TaueTaumu.sample                = ttbar
  MC_ttbar_TaueTaumu.color                 = ROOT.kViolet - 7
  MC_ttbar_TaueTaumu.legendText            = "#tau#rightarrow#mu, #tau#rightarrow e (6 #nu)"
  MC_ttbar_TaueTaumu.style                 = "f0"

  MC_ttbar_TauTaumu                       = variable(varstring, binning, cutstring + "&&" +  TauTaumu_T)
  MC_ttbar_TauTaumu.add                   = [MC_ttbar_TaueTaumu]
  MC_ttbar_TauTaumu.sample                = ttbar
  MC_ttbar_TauTaumu.color                 = ROOT.kCyan + 2
  MC_ttbar_TauTaumu.legendText            = "1 had. #tau, #tau#rightarrow#mu (5 #nu)"
  MC_ttbar_TauTaumu.style                 = "f0"

  MC_ttbar_MuTaumu                       = variable(varstring, binning, cutstring + "&&" +  MuTaumu_T)
  MC_ttbar_MuTaumu.add                   = [MC_ttbar_TauTaumu]
  MC_ttbar_MuTaumu.sample                = ttbar
  MC_ttbar_MuTaumu.color                 = ROOT.kGreen + 2
  MC_ttbar_MuTaumu.legendText            = "1 #mu, #tau#rightarrow#mu (4 #nu)"
  MC_ttbar_MuTaumu.style                 = "f0"

  MC_ttbar_ETaumu                       = variable(varstring, binning, cutstring + "&&" +  ETaumu_T)
  MC_ttbar_ETaumu.add                   = [MC_ttbar_MuTaumu]
  MC_ttbar_ETaumu.sample                = ttbar
  MC_ttbar_ETaumu.color                 = ROOT.kOrange + 2
  MC_ttbar_ETaumu.legendText            = "1 e, #tau#rightarrow#mu (4 #nu)"
  MC_ttbar_ETaumu.style                 = "f0"
 
  MC_ttbar_MuTaue                       = variable(varstring, binning, cutstring + "&&" +  MuTaue_T)
  MC_ttbar_MuTaue.add                   = [MC_ttbar_ETaumu]
  MC_ttbar_MuTaue.sample                = ttbar
  MC_ttbar_MuTaue.color                 = ROOT.kYellow + 2
  MC_ttbar_MuTaue.legendText            = "1 #mu, #tau#rightarrow e (4 #nu)"
  MC_ttbar_MuTaue.style                 = "f0"

  MC_ttbar_MuMu                         = variable(varstring, binning, cutstring + "&&" +  MuMu_T)
  MC_ttbar_MuMu.add                     = [MC_ttbar_MuTaue]
  MC_ttbar_MuMu.sample                  = ttbar
  MC_ttbar_MuMu.color                   = ROOT.kCyan - 2
  MC_ttbar_MuMu.legendText              = "2 #mu (2 #nu)"
  MC_ttbar_MuMu.style                   = "f0"

  MC_ttbar_MuE                          = variable(varstring, binning, cutstring + "&&" +  MuE_T)
  MC_ttbar_MuE.add                      = [MC_ttbar_MuMu]
  MC_ttbar_MuE.sample                   = ttbar
  MC_ttbar_MuE.color                    = ROOT.kBlue - 2
  MC_ttbar_MuE.legendText               = "1 #mu, 1 e (2 #nu)"
  MC_ttbar_MuE.style                    = "f0"

  MC_ttbar_MuhadTau                     = variable(varstring, binning, cutstring + "&&" +  MuhadTau_T)
  MC_ttbar_MuhadTau.add                 = [MC_ttbar_MuE]
  MC_ttbar_MuhadTau.sample              = ttbar
  MC_ttbar_MuhadTau.color               = ROOT.kRed - 2
  MC_ttbar_MuhadTau.legendText          = "1 #mu, had. #tau (3 #nu)"
  MC_ttbar_MuhadTau.style               = "f0"

  MC_ttbar_Taumu                     = variable(varstring, binning, cutstring + "&&" + Taumu_T)
  MC_ttbar_Taumu.add                 = [MC_ttbar_MuhadTau]
  MC_ttbar_Taumu.sample              = ttbar
  MC_ttbar_Taumu.color               = ROOT.kMagenta-6
  MC_ttbar_Taumu.legendText          = "#tau#rightarrow#mu (3 #nu)"
  MC_ttbar_Taumu.style               = "f0"
 
  MC_ttbar_Mu                           = variable(varstring, binning, cutstring + "&&" +  Mu_T)
  MC_ttbar_Mu.add                       = [MC_ttbar_Taumu]
  MC_ttbar_Mu.sample                    = ttbar
  MC_ttbar_Mu.color                     = ROOT.kGreen + 4
  MC_ttbar_Mu.legendText                = "1 #mu (1 #nu)"
  MC_ttbar_Mu.style                     = "f0"

  res = [MC_ttbar_all, MC_ttbar_Mu, MC_ttbar_Taumu,  MC_ttbar_MuhadTau, MC_ttbar_MuE, MC_ttbar_MuMu, MC_ttbar_MuTaue, MC_ttbar_ETaumu, MC_ttbar_MuTaumu, MC_ttbar_TauTaumu, MC_ttbar_TaueTaumu, MC_ttbar_TaumuTaumu]
  for var in res:
    var.minimum=0.07

  adjustLegend(res)
  getLinesForStack(res, targetLumi)

  return res 

genmet_stack         = getTStack(":genmet;#slash{E}_{T} (GeV);Number of Events / 40 GeV",[26,0,1040], commoncf )
allStacks.append(genmet_stack)
genmet_stack[0].addOverFlowBin = "upper"

#genmetstacks = {}
#htvals = [[350,400],[400,500],[500,600],[600,700],[700,800],[800,900],[900,1000],[1000,1200],[1200,1400]]
#for htval in  htvals:
#  stack = getTStack(":genmet;#slash{E}_{T} (GeV);Number of Events / 25 GeV",[41,0,1025], commoncf+"&&ht>"+str(htval[0])+"&&ht<"+str(htval[1]))
#  stack[0].addOverFlowBin = "upper"
#  allStacks.append(stack)
#  genmetstacks[str(htval[0])] = stack

met_Tstack         = getTStack(":met;#slash{E}_{T} (GeV);Number of Events / 40 GeV",[26,0,1040], commoncf )
allStacks.append(met_Tstack)
lepton_pt_Tstack   = getTStack("p_{T}(GeV):leptonPt;p_{T,lep.} (GeV);Number of Events / 20 GeV",[31,0,620], commoncf)
allStacks.append(lepton_pt_Tstack)
mT_Tstack          = getTStack(":mT;m_{T} (GeV);Number of Events / 20 GeV",[31,0,620], commoncf)
allStacks.append(mT_Tstack)
ht_Tstack      = getTStack(":ht2;HT_{2}^{had.} (GeV);Number of Events / 50 GeV",[31,0,1550], commoncf)
allStacks.append(ht_Tstack)
kinMetSig_Tstack   = getTStack(":kinMetSig;kin. #slash{E}_{T} Significance;Number of Events",[33,0,33], commoncf)
allStacks.append(kinMetSig_Tstack)
m3_Tstack   = getTStack(":m3;M_{3};Number of Events / 50 GeV",[26,0,2600], commoncf)
allStacks.append(m3_Tstack)
ht_Tstack   = getTStack(":ht;M_{3};Number of Events / 50 GeV",[52,0,2600], commoncf)
allStacks.append(ht_Tstack)

met_TshapeStack         = getShapeStack(met_Tstack[:5])
allStacks.append(met_TshapeStack)
lepton_pt_TshapeStack   = getShapeStack(lepton_pt_Tstack[:5]) 
allStacks.append(lepton_pt_TshapeStack)
mT_TshapeStack          = getShapeStack(mT_Tstack[:5]) 
allStacks.append(mT_TshapeStack)
ht_TshapeStack      = getShapeStack(ht_Tstack[:5]) 
allStacks.append(ht_TshapeStack)
kinMetSig_TshapeStack   = getShapeStack(kinMetSig_Tstack[:5]) 
allStacks.append(kinMetSig_TshapeStack)
m3_TshapeStack   = getShapeStack(m3_Tstack[:5]) 
allStacks.append(m3_TshapeStack)
ht_TshapeStack   = getShapeStack(ht_Tstack[:5]) 
allStacks.append(ht_TshapeStack)

execfile("simplePlotsLoopKernel.py")

ROOT.setTDRStyle()
ROOT.gStyle.SetOptStat(0)

if doWstacks:
  drawNMStacks(1,1,[met_Wstack],              subdir+prefix+"_W_met.png", False)
  drawNMStacks(1,1,[lepton_pt_Wstack],        subdir+prefix+"_W_lepton_pt.png", False)
  drawNMStacks(1,1,[mT_Wstack],               subdir+prefix+"_W_mT.png", False)
  drawNMStacks(1,1,[ht_Wstack],           subdir+prefix+"_W_ht.png", False)
  drawNMStacks(1,1,[kinMetSig_Wstack],        subdir+prefix+"_W_kinMetSig.png", False)
  drawNMStacks(1,1,[m3_Wstack],               subdir+prefix+"_W_m3.png", False)

  drawNMStacks(1,1,[met_WshapeStack],              subdir+prefix+"_W_shapes_met.png", True)
  drawNMStacks(1,1,[lepton_pt_WshapeStack],        subdir+prefix+"_W_shapes_lepton_pt.png", True)
  drawNMStacks(1,1,[mT_WshapeStack],               subdir+prefix+"_W_shapes_mT.png", True)
  drawNMStacks(1,1,[ht_WshapeStack],           subdir+prefix+"_W_shapes_ht.png", True)
  drawNMStacks(1,1,[kinMetSig_WshapeStack],        subdir+prefix+"_W_shapes_kinMetSig.png", True)
  drawNMStacks(1,1,[m3_WshapeStack],               subdir+prefix+"_W_shapes_m3.png", True)

drawNMStacks(1,1,[met_Tstack],              subdir+prefix+"_T_met.png", False)
drawNMStacks(1,1,[lepton_pt_Tstack],        subdir+prefix+"_T_lepton_pt.png", False)
drawNMStacks(1,1,[mT_Tstack],               subdir+prefix+"_T_mT.png", False)
drawNMStacks(1,1,[ht_Tstack],           subdir+prefix+"_T_ht.png", False)
drawNMStacks(1,1,[kinMetSig_Tstack],        subdir+prefix+"_T_kinMetSig.png", False)
drawNMStacks(1,1,[m3_Tstack],               subdir+prefix+"_T_m3.png", False)
drawNMStacks(1,1,[ht_Tstack],               subdir+prefix+"_T_ht.png", False)

drawNMStacks(1,1,[met_TshapeStack],              subdir+prefix+"_T_shapes_met.png", True)
drawNMStacks(1,1,[lepton_pt_TshapeStack],        subdir+prefix+"_T_shapes_lepton_pt.png", True)
drawNMStacks(1,1,[mT_TshapeStack],               subdir+prefix+"_T_shapes_mT.png", True)
drawNMStacks(1,1,[ht_TshapeStack],           subdir+prefix+"_T_shapes_ht.png", True)
drawNMStacks(1,1,[kinMetSig_TshapeStack],        subdir+prefix+"_T_shapes_kinMetSig.png", True)
drawNMStacks(1,1,[m3_TshapeStack],               subdir+prefix+"_T_shapes_m3.png", True)
drawNMStacks(1,1,[ht_TshapeStack],               subdir+prefix+"_T_shapes_ht.png", False)

drawNMStacks(1,1,[genmet_stack],             subdir+prefix+"genmet", False)
#for htval in htvals:
#  drawNMStacks(1,1,[genmetstacks[str(htval[0])]], subdir+prefix+"genmet_ht_"+str(htval[0])+"_"+str(htval[1])+".png", False)

