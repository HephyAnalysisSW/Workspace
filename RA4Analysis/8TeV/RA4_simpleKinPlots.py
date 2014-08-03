import ROOT
from array import array
from math import *
import os, copy

from Workspace.RA4Analysis.simplePlotsCommon import *
from funcs import *

import xsec
small = False

allVars=[]
allStacks=[]

signalColors = [ROOT.kBlack, ROOT.kBlue + 1, ROOT.kGreen + 2, ROOT.kOrange + 2]

## plots for studying preselection 
minimum=10**(-0.5)
prefix=""
subdir = "/pngKin/"

noTrigSample = {'bins': ['TTJets-noTrig'],
 'dirname': '/scratch/schoef/pat_110917/Mu/',
 'name': 'MC',
  'Chain':"pfRA4Analyzer/Events",
 'specialCuts': []}
allSamples = [noTrigSample]
targetLumi = 1100

def getStack(varstring, binning, cutstring, varfunc = ""):
  MC_TTJETS          = variable(varstring, binning, cutstring)
  MC_TTJETS_g        = variable(varstring, binning, addCutString(cutstring, "abs(top_m0_pdgId)==21")) 
  MC_TTJETS_u        = variable(varstring, binning, addCutString(cutstring, "abs(top_m0_pdgId)==1")) 
  MC_TTJETS_d        = variable(varstring, binning, addCutString(cutstring, "abs(top_m0_pdgId)==2")) 
  MC_TTJETS_cs        = variable(varstring, binning, addCutString(cutstring, "(abs(top_m0_pdgId)==3||abs(top_m0_pdgId)==4)")) 
  MC_TTJETS_b        = variable(varstring, binning, addCutString(cutstring, "abs(top_m0_pdgId)==5")) 

  MC_TTJETS.color    = ROOT.kBlack
  MC_TTJETS.style    = "l02"
  MC_TTJETS.legendText="t#bar{t} + Jets"

  MC_TTJETS_g.legendText         = "gluon"
  MC_TTJETS_g.style              = "l02"
  MC_TTJETS_g.color              = ROOT.kRed
  MC_TTJETS_g.add                = [MC_TTJETS_u]

  MC_TTJETS_u.legendText         = "u-quark"
  MC_TTJETS_u.style              = "l02"
  MC_TTJETS_u.color              = ROOT.kBlue
  MC_TTJETS_u.add                = [MC_TTJETS_d]

  MC_TTJETS_d.legendText         = "d-quark"
  MC_TTJETS_d.style              = "l02"
  MC_TTJETS_d.color              = ROOT.kGreen
  
  MC_TTJETS_cs.legendText         = "c/s-quark"
  MC_TTJETS_cs.style              = "l02"
  MC_TTJETS_cs.color              = ROOT.kOrange
  
  MC_TTJETS_b.legendText         = "b-quark"
  MC_TTJETS_b.style              = "l02"
  MC_TTJETS_b.color              = ROOT.kYellow

  res = [MC_TTJETS, MC_TTJETS_g, MC_TTJETS_u, MC_TTJETS_d, MC_TTJETS_cs, MC_TTJETS_b]
  getLinesForStack(res, targetLumi)
  nhistos = len(res)
  for var in res:
    var.sample = noTrigSample
    var.legendCoordinates=[0.61,0.95 - 0.08*5,.98,.95]
#    var.legendCoordinates=[0.64,0.95 - 0.05*nhistos,.98,.95] #for signalnumbers = [0,1]
  if varfunc!="":
    for var in res:
      var.varfunc = varfunc
  return res

top_m0_pt_stack = getStack(":top_m0_pt;t_m0_pt;Number of Events",[45,0,450], "")
top_m0_pt_stack[0].addOverFlowBin = "upper"
allStacks.append(top_m0_pt_stack)

top_m0_pz_stack = getStack(":top_m0_pz;t_m0_pz;Number of Events",[70,-3500,3500], "")
top_m0_pz_stack[0].addOverFlowBin = "both"
allStacks.append(top_m0_pz_stack)

top_m1_pz_stack = getStack(":top_m1_pz;t_m1_pz;Number of Events",[70,-3500,3500], "")
top_m1_pz_stack[0].addOverFlowBin = "both"
allStacks.append(top_m1_pz_stack)

top_m0_p_stack = getStack(":top_m0_p;t_m0_p;Number of Events",[35,0,3500], "", top_m0_p)
top_m0_p_stack[0].addOverFlowBin = "upper"
allStacks.append(top_m0_p_stack)

s_inv_m_stack = getStack(":s_inv_m;t_m0_p;Number of Events",[100,0,30*10**6], "", s_inv_m)
s_inv_m_stack[0].addOverFlowBin = "upper"
allStacks.append(s_inv_m_stack)

top_0_pt_stack = getStack(":top_0_pt;t_0_pt;Number of Events",[35,0,3500], "")
top_0_pt_stack[0].addOverFlowBin = "upper"
allStacks.append(top_0_pt_stack)

top_1_pt_stack = getStack(":top_1_pt;t_1_pt;Number of Events",[35,0,3500], "")
top_1_pt_stack[0].addOverFlowBin = "upper"
allStacks.append(top_1_pt_stack)

top_0_pz_stack = getStack(":top_0_pz;t_0_pz;Number of Events",[70,-3500,3500], "")
top_0_pz_stack[0].addOverFlowBin = "upper"
allStacks.append(top_0_pz_stack)

top_1_pz_stack = getStack(":top_1_pz;t_1_pz;Number of Events",[70,-3500,3500], "")
top_1_pz_stack[0].addOverFlowBin = "upper"
allStacks.append(top_1_pz_stack)

execfile("simplePlotsLoopKernel.py")

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
  stack[0].maximum = 2.*stack[0].data_histo.GetMaximum()
  stack[0].logy = True
  stack[0].minimum = minimum
#  stack[0].legendCoordinates=[0.76,0.95 - 0.3,.98,.95]
#  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS preliminary}"], [0.2,0.85,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 7 TeV"]]
  stack[0].legendCoordinates=[0.61,0.95 - 0.08*5,.98,.95]
  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS preliminary}"], [0.2,0.85,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 7 TeV"]]

#drawNMStacks(1,1,[top_m0_pt_stack],             subdir+prefix+"top_m0_pt_stack.png", False)
drawNMStacks(1,1,[top_m1_pz_stack],             subdir+prefix+"top_m1_pz_stack.png", False)
drawNMStacks(1,1,[top_m0_pz_stack],             subdir+prefix+"top_m0_pz_stack.png", False)
drawNMStacks(1,1,[top_m0_p_stack],             subdir+prefix+"top_m0_p_stack.png", False)
drawNMStacks(1,1,[s_inv_m_stack],             subdir+prefix+"s_inv_m_stack.png", False)

drawNMStacks(1,1,[top_0_pz_stack],             subdir+prefix+"top_0_pz_stack.png", False)
drawNMStacks(1,1,[top_0_pt_stack],             subdir+prefix+"top_0_pt_stack.png", False)
drawNMStacks(1,1,[top_1_pz_stack],             subdir+prefix+"top_1_pz_stack.png", False)
drawNMStacks(1,1,[top_1_pt_stack],             subdir+prefix+"top_1_pt_stack.png", False)

for stack in allStacks:
  stack[0].maximum = stack[0].data_histo.GetMaximum()
  stack[0].logy = False
  stack[0].minimum=0
  
#drawNMStacks(1,1,[top_m0_pt_stack],             subdir+prefix+"top_m0_pt_stack_lin.png", False)
drawNMStacks(1,1,[top_m0_pz_stack],             subdir+prefix+"top_m0_pz_stack_lin.png", False)
drawNMStacks(1,1,[top_m1_pz_stack],             subdir+prefix+"top_m1_pz_stack_lin.png", False)
drawNMStacks(1,1,[top_m0_p_stack],             subdir+prefix+"top_m0_p_stack_lin.png", False)
drawNMStacks(1,1,[s_inv_m_stack],             subdir+prefix+"s_inv_m_stack_lin.png", False)

drawNMStacks(1,1,[top_0_pz_stack],             subdir+prefix+"top_0_pz_stack_lin.png", False)
drawNMStacks(1,1,[top_0_pt_stack],             subdir+prefix+"top_0_pt_stack_lin.png", False)
drawNMStacks(1,1,[top_1_pz_stack],             subdir+prefix+"top_1_pz_stack_lin.png", False)
drawNMStacks(1,1,[top_1_pt_stack],             subdir+prefix+"top_1_pt_stack_lin.png", False)
