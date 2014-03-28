import ROOT
from array import array
from math import *
import os, copy

from Workspace.RA4Analysis.simplePlotsCommon import *

import xsec
small = False

from newMuSamples import *
  
allVars=[]
allStacks=[]

signalColors = [ROOT.kBlack, ROOT.kBlue + 1, ROOT.kGreen + 2, ROOT.kOrange + 2]

## plots for studying preselection 
topIsLargest = True
minimum=10**(-0.5)
signalNumbers = []
subdir = "/pngTMP/"
presel = "pf-4j30"

additionalCut = ""
preprefix = "iso-Mu"

floatWJets = False
WJETS_scale = 1.7981563483

chainstring = "empty"
commoncf = "(0)"
prefix="empty_"

if presel == "4j30":
  chainstring = "isoRA4Analyzer/Events"
  commoncf = "jet1pt>30&&jet3pt>30&&lepton_pt>15&&singleMuonic"
if presel == "pf-4j30":
  chainstring = "isopfRA4Analyzer/Events"
  commoncf = "jet1pt>30&&jet3pt>30&&lepton_pt>15&&singleMuonic"

if additionalCut!="":
  commoncf+="&&"+additionalCut

prefix= "RA4_"+presel+"_"
if preprefix!="":
  prefix = preprefix+"_"+presel+"_"

for sample in allSamples:
  sample["Chain"] = chainstring

def getStack(varstring, binning, cutstring):
  DATA          = variable(varstring, binning, cutstring)
  DATA.sample   = data
  DATA.color    = dataColor
  DATA.legendText="Data"

  MC_QCD                       = variable(varstring, binning, cutstring)
  MC_QCD.minimum               = 10**(-1)

  MC_QCD                       = variable(varstring, binning, cutstring)
  MC_QCD.minimum               = 5*10**(-1)
  MC_QCD.sample                = copy.deepcopy(mc)
  MC_QCD.sample["bins"]        = copy.deepcopy(QCD_Bins)
  MC_EWK                       = copy.deepcopy(MC_QCD)
  MC_EWK.sample                = copy.deepcopy(mc)
  MC_EWK.sample["bins"]        = copy.deepcopy(WJets_Bins)
  MC_EWK.sample["bins"].append("TTJets")
  MC_EWK.sample["bins"].append("DYtoLL")
  MC_EWK.sample["bins"].extend(singleTop_Bins)

  MC_EWK.legendText         = "EWK"
  MC_EWK.style              = "f"
  MC_EWK.color              = ROOT.kRed - 3
  MC_EWK.normalizeTo        = DATA
  MC_EWK.add                = [MC_QCD]
  MC_QCD.color              = myBlue
  MC_QCD.legendText         = "QCD"
  MC_QCD.style              = "f"
  MC_QCD.normalizeTo        = DATA
  MC_QCD.normalizeWhat      = MC_EWK

  res = [MC_EWK, MC_QCD]

  getLinesForStack(res, targetLumi)
  nhistos = len(res)
  for var in res:
    var.legendCoordinates=[0.75,0.95 - 0.07*nhistos,.98,.95]
  res.append(DATA)
  return res

#lepton_relIso_stack               = getStack(":lepton_relIso;relIso;Number of Events",[25,0,0.5], commoncf)
#allStacks.append(lepton_relIso_stack)
#lepton_relIso2_stack               = getStack(":lepton_relIso;relIso;Number of Events",[25,0,1.5], commoncf)
#allStacks.append(lepton_relIso2_stack)
#
#tp_zmass_0j_stack          = getStack(":tp_zmass;m_{Z};Number of Events",[26,77,103], "kinMetSig<2.5&&ngoodElectrons==0&&ngoodMuons>0", signalNumbers, False)
#allStacks.append(tp_zmass_0j_stack)
#tp_zmass_1j_stack          = getStack(":tp_zmass;m_{Z};Number of Events",[26,77,103], "kinMetSig<2.5&&ngoodElectrons==0&&ngoodMuons>0&&jet0pt>30", signalNumbers, False)
#allStacks.append(tp_zmass_1j_stack)
#tp_zmass_2j_stack          = getStack(":tp_zmass;m_{Z};Number of Events",[26,77,103], "kinMetSig<2.5&&ngoodElectrons==0&&ngoodMuons>0&&jet1pt>30", signalNumbers, False)
#allStacks.append(tp_zmass_2j_stack)
#tp_zmass_3j_stack          = getStack(":tp_zmass;m_{Z};Number of Events",[26,77,103], "kinMetSig<2.5&&ngoodElectrons==0&&ngoodMuons>0&&jet2pt>30", signalNumbers, False)
#allStacks.append(tp_zmass_3j_stack)
#tp_zmass_4j_stack          = getStack(":tp_zmass;m_{Z};Number of Events",[26,77,103], "kinMetSig<2.5&&ngoodElectrons==0&&ngoodMuons>0&&jet3pt>30", signalNumbers, False)
#allStacks.append(tp_zmass_4j_stack)
#
#tp_p_relIso_0j_stack               = getStack(":tp_p_relIso;relIso;Number of Events",[25,0,1.5], "kinMetSig<2.5&&ngoodElectrons==0&&ngoodMuons>0&&abs(tp_zmass-91.2)<15.")
#allStacks.append(tp_p_relIso_0j_stack)
#tp_p_relIso_1j_stack               = getStack(":tp_p_relIso;relIso;Number of Events",[25,0,1.5], "kinMetSig<2.5&&ngoodElectrons==0&&ngoodMuons>0&&abs(tp_zmass-91.2)<15.&&jet0pt>30")
#allStacks.append(tp_p_relIso_1j_stack)
#tp_p_relIso_2j_stack               = getStack(":tp_p_relIso;relIso;Number of Events",[25,0,1.5], "kinMetSig<2.5&&ngoodElectrons==0&&ngoodMuons>0&&abs(tp_zmass-91.2)<15.&&jet1pt>30")
#allStacks.append(tp_p_relIso_2j_stack)
#tp_p_relIso_3j_stack               = getStack(":tp_p_relIso;relIso;Number of Events",[25,0,1.5], "kinMetSig<2.5&&ngoodElectrons==0&&ngoodMuons>0&&abs(tp_zmass-91.2)<15.&&jet2pt>30")
#allStacks.append(tp_p_relIso_3j_stack)
#tp_p_relIso_4j_stack               = getStack(":tp_p_relIso;relIso;Number of Events",[25,0,1.5], "kinMetSig<2.5&&ngoodElectrons==0&&ngoodMuons>0&&abs(tp_zmass-91.2)<15.&&jet3pt>30")
#allStacks.append(tp_p_relIso_4j_stack)

relIso_control_kMs_1_ht_200_300_stack               = getStack(":lepton_relIso;relIso;Number of Events",[30,0,1.5], "ngoodElectrons==0&&ngoodMuons==1&&kinMetSig<1.&&jet3pt>30&&200<ht&&ht<300")
allStacks.append(relIso_control_kMs_1_ht_200_300_stack)
relIso_control_kMs_1_ht_200_250_stack               = getStack(":lepton_relIso;relIso;Number of Events",[30,0,1.5], "ngoodElectrons==0&&ngoodMuons==1&&kinMetSig<1.&&jet3pt>30&&200<ht&&ht<250")
allStacks.append(relIso_control_kMs_1_ht_200_250_stack)
relIso_control_kMs_1_ht_150_200_stack               = getStack(":lepton_relIso;relIso;Number of Events",[30,0,1.5], "ngoodElectrons==0&&ngoodMuons==1&&kinMetSig<1.&&jet3pt>30&&150<ht&&ht<200")
allStacks.append(relIso_control_kMs_1_ht_150_200_stack)
relIso_control_kMs_1_ht_150_250_stack               = getStack(":lepton_relIso;relIso;Number of Events",[30,0,1.5], "ngoodElectrons==0&&ngoodMuons==1&&kinMetSig<1.&&jet3pt>30&&150<ht&&ht<250")
allStacks.append(relIso_control_kMs_1_ht_150_250_stack)
relIso_control_kMs_1_ht_300_350_stack               = getStack(":lepton_relIso;relIso;Number of Events",[30,0,1.5], "ngoodElectrons==0&&ngoodMuons==1&&kinMetSig<1.&&jet3pt>30&&300<ht&&ht<350")
allStacks.append(relIso_control_kMs_1_ht_300_350_stack)


relIso_control_kMs_05_ht_200_300_stack               = getStack(":lepton_relIso;relIso;Number of Events",[30,0,1.5], "ngoodElectrons==0&&ngoodMuons==1&&kinMetSig<0.5&&jet3pt>30&&200<ht&&ht<300")
allStacks.append(relIso_control_kMs_05_ht_200_300_stack)
relIso_control_kMs_05_ht_200_250_stack               = getStack(":lepton_relIso;relIso;Number of Events",[30,0,1.5], "ngoodElectrons==0&&ngoodMuons==1&&kinMetSig<0.5&&jet3pt>30&&200<ht&&ht<250")
allStacks.append(relIso_control_kMs_05_ht_200_250_stack)
relIso_control_kMs_05_ht_150_200_stack               = getStack(":lepton_relIso;relIso;Number of Events",[30,0,1.5], "ngoodElectrons==0&&ngoodMuons==1&&kinMetSig<0.5&&jet3pt>30&&150<ht&&ht<200")
allStacks.append(relIso_control_kMs_05_ht_150_200_stack)
relIso_control_kMs_05_ht_150_250_stack               = getStack(":lepton_relIso;relIso;Number of Events",[30,0,1.5], "ngoodElectrons==0&&ngoodMuons==1&&kinMetSig<0.5&&jet3pt>30&&150<ht&&ht<250")
allStacks.append(relIso_control_kMs_05_ht_150_250_stack)
relIso_control_kMs_05_ht_300_350_stack               = getStack(":lepton_relIso;relIso;Number of Events",[30,0,1.5], "ngoodElectrons==0&&ngoodMuons==1&&kinMetSig<0.5&&jet3pt>30&&300<ht&&ht<350")
allStacks.append(relIso_control_kMs_05_ht_300_350_stack)

relIso_signal_stack               = getStack(":lepton_relIso;relIso;Number of Events",[30,0,1.5], "ngoodElectrons==0&&ngoodMuons==1&&kinMetSig>2.5&&jet3pt>30&&ht>330")
allStacks.append(relIso_signal_stack)

relIso_A_stack               = getStack(":lepton_relIso;relIso;Number of Events",[30,0,1.5], "ngoodElectrons==0&&ngoodMuons==1&&kinMetSig>2.5&&kinMetSig<5.0&&jet3pt>30&&ht>330&&ht<410")
allStacks.append(relIso_A_stack)
relIso_B_stack               = getStack(":lepton_relIso;relIso;Number of Events",[30,0,1.5], "ngoodElectrons==0&&ngoodMuons==1&&kinMetSig>5&&jet3pt>30&&ht>330&&ht<410")
allStacks.append(relIso_B_stack)
relIso_C_stack               = getStack(":lepton_relIso;relIso;Number of Events",[30,0,1.5], "ngoodElectrons==0&&ngoodMuons==1&&kinMetSig>2.5&&kinMetSig<5.0&&jet3pt>30&&ht>410")
allStacks.append(relIso_C_stack)
relIso_D_stack               = getStack(":lepton_relIso;relIso;Number of Events",[30,0,1.5], "ngoodElectrons==0&&ngoodMuons==1&&kinMetSig>5.0&&jet3pt>30&&ht>410")
allStacks.append(relIso_D_stack)

for stack in allStacks:
  stack[0].minimum = minimum

execfile("simplePlotsKernel.py")

for stack in allStacks:
  stack[0].maximum = 3.*stack[-1].data_histo.GetMaximum()
  stack[0].logy = True
  stack[0].minimum = minimum

#drawNMStacks(1,1,[lepton_relIso_stack],               subdir+prefix+"lepton_relIso", False)
#drawNMStacks(1,1,[lepton_relIso2_stack],               subdir+prefix+"lepton_relIso2", False)
#drawNMStacks(1,1,[tp_zmass_0j_stack],               subdir+prefix+"tp_0j_zmass", False)
#drawNMStacks(1,1,[tp_zmass_1j_stack],               subdir+prefix+"tp_1j_zmass", False)
#drawNMStacks(1,1,[tp_zmass_2j_stack],               subdir+prefix+"tp_2j_zmass", False)
#drawNMStacks(1,1,[tp_zmass_3j_stack],               subdir+prefix+"tp_3j_zmass", False)
#drawNMStacks(1,1,[tp_zmass_4j_stack],               subdir+prefix+"tp_4j_zmass", False)
#
#drawNMStacks(1,1,[tp_p_relIso_0j_stack],            subdir+prefix+"tp_p_relIso_0j", False)
#drawNMStacks(1,1,[tp_p_relIso_1j_stack],            subdir+prefix+"tp_p_relIso_1j", False)
#drawNMStacks(1,1,[tp_p_relIso_2j_stack],            subdir+prefix+"tp_p_relIso_2j", False)
#drawNMStacks(1,1,[tp_p_relIso_3j_stack],            subdir+prefix+"tp_p_relIso_3j", False)
#drawNMStacks(1,1,[tp_p_relIso_4j_stack],            subdir+prefix+"tp_p_relIso_4j", False)

drawNMStacks(1,1,[relIso_control_kMs_1_ht_200_300_stack] ,             subdir+prefix+"relIso_control_kMs_1_ht_200_300_stack",False)
drawNMStacks(1,1,[relIso_control_kMs_1_ht_200_250_stack] ,             subdir+prefix+"relIso_control_kMs_1_ht_200_250_stack",False) 
drawNMStacks(1,1,[relIso_control_kMs_1_ht_150_200_stack] ,             subdir+prefix+"relIso_control_kMs_1_ht_150_200_stack",False)
drawNMStacks(1,1,[relIso_control_kMs_1_ht_150_250_stack] ,             subdir+prefix+"relIso_control_kMs_1_ht_150_250_stack",False)
drawNMStacks(1,1,[relIso_control_kMs_1_ht_300_350_stack] ,             subdir+prefix+"relIso_control_kMs_1_ht_300_350_stack",False)
drawNMStacks(1,1,[relIso_control_kMs_05_ht_200_300_stack] ,             subdir+prefix+"relIso_control_kMs_05_ht_200_300_stack",False)
drawNMStacks(1,1,[relIso_control_kMs_05_ht_200_250_stack] ,             subdir+prefix+"relIso_control_kMs_05_ht_200_250_stack",False) 
drawNMStacks(1,1,[relIso_control_kMs_05_ht_150_200_stack] ,             subdir+prefix+"relIso_control_kMs_05_ht_150_200_stack",False)
drawNMStacks(1,1,[relIso_control_kMs_05_ht_150_250_stack] ,             subdir+prefix+"relIso_control_kMs_05_ht_150_250_stack",False)
drawNMStacks(1,1,[relIso_control_kMs_05_ht_300_350_stack] ,             subdir+prefix+"relIso_control_kMs_05_ht_300_350_stack",False)

drawNMStacks(1,1,[relIso_signal_stack],             subdir+prefix+"relIso_signal", False)

for stack in allStacks:
  stack[0].maximum = 1.2*stack[-1].data_histo.GetMaximum()
  stack[0].minimum = 0
  stack[0].logy = False

#drawNMStacks(1,1,[lepton_relIso_stack],               subdir+prefix+"lepton_relIso_lin", False)
#drawNMStacks(1,1,[lepton_relIso2_stack],               subdir+prefix+"lepton_relIso2_lin", False)
#drawNMStacks(1,1,[tp_zmass_0j_stack],               subdir+prefix+"tp_0j_zmass_lin", False)
#drawNMStacks(1,1,[tp_zmass_1j_stack],               subdir+prefix+"tp_1j_zmass_lin", False)
#drawNMStacks(1,1,[tp_zmass_2j_stack],               subdir+prefix+"tp_2j_zmass_lin", False)
#drawNMStacks(1,1,[tp_zmass_3j_stack],               subdir+prefix+"tp_3j_zmass_lin", False)
#drawNMStacks(1,1,[tp_zmass_4j_stack],               subdir+prefix+"tp_4j_zmass_lin", False)
#
#drawNMStacks(1,1,[tp_p_relIso_0j_stack],            subdir+prefix+"tp_p_relIso_0j_lin", False)
#drawNMStacks(1,1,[tp_p_relIso_1j_stack],            subdir+prefix+"tp_p_relIso_1j_lin", False)
#drawNMStacks(1,1,[tp_p_relIso_2j_stack],            subdir+prefix+"tp_p_relIso_2j_lin", False)
#drawNMStacks(1,1,[tp_p_relIso_3j_stack],            subdir+prefix+"tp_p_relIso_3j_lin", False)
#drawNMStacks(1,1,[tp_p_relIso_4j_stack],            subdir+prefix+"tp_p_relIso_4j_lin", False)

drawNMStacks(1,1,[relIso_control_kMs_1_ht_200_300_stack] ,             subdir+prefix+"relIso_control_kMs_1_ht_200_300_stack_lin",False)
drawNMStacks(1,1,[relIso_control_kMs_1_ht_200_250_stack] ,             subdir+prefix+"relIso_control_kMs_1_ht_200_250_stack_lin",False) 
drawNMStacks(1,1,[relIso_control_kMs_1_ht_150_200_stack] ,             subdir+prefix+"relIso_control_kMs_1_ht_150_200_stack_lin",False)
drawNMStacks(1,1,[relIso_control_kMs_1_ht_150_250_stack] ,             subdir+prefix+"relIso_control_kMs_1_ht_150_250_stack_lin",False)
drawNMStacks(1,1,[relIso_control_kMs_1_ht_300_350_stack] ,             subdir+prefix+"relIso_control_kMs_1_ht_300_350_stack_lin",False)
drawNMStacks(1,1,[relIso_control_kMs_05_ht_200_300_stack] ,             subdir+prefix+"relIso_control_kMs_05_ht_200_300_stack_lin",False)
drawNMStacks(1,1,[relIso_control_kMs_05_ht_200_250_stack] ,             subdir+prefix+"relIso_control_kMs_05_ht_200_250_stack_lin",False) 
drawNMStacks(1,1,[relIso_control_kMs_05_ht_150_200_stack] ,             subdir+prefix+"relIso_control_kMs_05_ht_150_200_stack_lin",False)
drawNMStacks(1,1,[relIso_control_kMs_05_ht_150_250_stack] ,             subdir+prefix+"relIso_control_kMs_05_ht_150_250_stack_lin",False)
drawNMStacks(1,1,[relIso_control_kMs_05_ht_300_350_stack] ,             subdir+prefix+"relIso_control_kMs_05_ht_300_350_stack_lin",False)

drawNMStacks(1,1,[relIso_signal_stack],             subdir+prefix+"relIso_signal_lin", False)

def getYieldHighRelIso(thisvar):
  h = thisvar.data_histo
  return h.Integral(h.FindBin(0.5),h.FindBin(1.5)) 
def getYieldLowRelIso(thisvar):
  h = thisvar.data_histo
  return h.Integral(0, h.FindBin(0.1)-1) 
def getPred(this_lrc, this_hrc, this_hrs):
  cratio = this_lrc/this_hrc
  pred = cratio*this_hrs
  sigma2_ratio = this_lrc*(this_hrc+this_lrc)/this_hrc**3.
  relerr = sqrt(sigma2_ratio/cratio**2 + 1./this_hrs)
  print "Prediction:", pred,"+/-",pred*relerr

control_lowrelIso  = getYieldLowRelIso(relIso_control_kMs_05_ht_150_200_stack[0])  
control_highrelIso = getYieldHighRelIso(relIso_control_kMs_05_ht_150_200_stack[0])  
control_ratio = control_lowrelIso/control_highrelIso
signal_highreliso = getYieldHighRelIso(relIso_signal_stack[0]) 
A_highreliso = getYieldHighRelIso(relIso_A_stack[0]) 
B_highreliso = getYieldHighRelIso(relIso_B_stack[0]) 
C_highreliso = getYieldHighRelIso(relIso_C_stack[0]) 
D_highreliso = getYieldHighRelIso(relIso_D_stack[0]) 
print "MC: low, high control: ",control_lowrelIso, control_highrelIso, "ratio low/high relIso:",control_ratio, "signal high:",signal_highreliso, "pred. low:",signal_highreliso*control_ratio, "A",A_highreliso*control_ratio, "B",B_highreliso*control_ratio, "C",C_highreliso*control_ratio, "D",D_highreliso*control_ratio

print "A"
getPred(control_lowrelIso, control_highrelIso, A_highreliso)
print "B"
getPred(control_lowrelIso, control_highrelIso, B_highreliso)
print "C"
getPred(control_lowrelIso, control_highrelIso, C_highreliso)
print "D"
getPred(control_lowrelIso, control_highrelIso, D_highreliso)

control_lowrelIso  = getYieldLowRelIso(relIso_control_kMs_1_ht_150_200_stack[-1])
control_highrelIso = getYieldHighRelIso(relIso_control_kMs_1_ht_150_200_stack[-1])
control_ratio = control_lowrelIso/control_highrelIso
signal_highreliso = getYieldHighRelIso(relIso_signal_stack[-1])                    
A_highreliso = getYieldHighRelIso(relIso_A_stack[-1]) 
B_highreliso = getYieldHighRelIso(relIso_B_stack[-1]) 
C_highreliso = getYieldHighRelIso(relIso_C_stack[-1]) 
D_highreliso = getYieldHighRelIso(relIso_D_stack[-1]) 
print "Data: low, high control: ",control_lowrelIso, control_highrelIso, "ratio low/high relIso:",control_ratio, "signal high:",signal_highreliso, "pred. low:",signal_highreliso*control_ratio, "A",A_highreliso*control_ratio, "B",B_highreliso*control_ratio, "C",C_highreliso*control_ratio, "D",D_highreliso*control_ratio

print "A"
getPred(control_lowrelIso, control_highrelIso, A_highreliso)
print "B"
getPred(control_lowrelIso, control_highrelIso, B_highreliso)
print "C"
getPred(control_lowrelIso, control_highrelIso, C_highreliso)
print "D"
getPred(control_lowrelIso, control_highrelIso, D_highreliso)
