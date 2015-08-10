import ROOT
from array import array
from math import *
import os, copy, sys

ROOT.TH1F().SetDefaultSumw2()

paths = ['../../HEPHYPythonTools/python', '../../HEPHYPythonTools/plots', '../../RA4Analysis/plots', '../python']
#path = os.path.abspath('../../HEPHYPythonTools/python')
for path in [os.path.abspath(p) for p in paths]:
  if not path in sys.path:
    sys.path.insert(1, path)

from helpers import getObjFromFile, passPUJetID

from simplePlotsCommon import *

import xsec
small = False

targetLumi = 19700.

from defaultConvertedTuples import * 
Zcut = "abs(Zm-91.187)<15"

allVars=[]
allStacks=[]

## plots for studying preselection 

minimum=10**(-0.5)
weight = 'puWeight'
#weight = 'weight'
#mode = "Zmumu"
mode = "Zee"
presel = "inc"
ver = "v1"

additionalCut = "(1)"
addData = True
normalizeToData = False

subdir = "/pngZ/"

doAnalysisVars            = True

chainstring = "Events"
commoncf = "(0)"
prefix="empty_"
if presel == "inc":
#  commoncf="isrJetPt>110&&isrJetBTBVetoPassed&&softIsolatedMuPt>5&&nHardElectrons+nHardMuonsRelIso02==0&&njet60<=2&&softIsolatedMuDz<0.2"
  commoncf="(1)"

if additionalCut!="":
  commoncf+="&&"+additionalCut
prefix= mode+"_"+weight+"_"+presel+"_"

allSamples = [dy[mode], ttJets[mode], wJetsToLNu[mode], singleTop[mode], diboson[mode], data[mode]]

for sample in allSamples:
  sample["Chain"] = chainstring
  sample["dirname"] = "/data/schoef/dileptonTuples_"+ver+"/"+mode+"/"
  sample["weight"] = {}
  for bin in sample['bins']:
    sample['weight'][bin]=weight
#  sample["weight"] = "weight"
for bin in data[mode]['bins']:
  data[mode]['weight'][bin]="(1)"

if mode=="Zee":
  ebCuts = {\
  'All'   : '(1)',
  'EEcut' : "abs(l0eta)>1.479&&abs(l1eta)>1.479",
  'EBcut' : "((abs(l0eta)>1.479&&abs(l1eta)<1.479)||(abs(l1eta)>1.479&&abs(l0eta)<1.479))",
  'BBcut' : "abs(l0eta)<1.479&&abs(l1eta)<1.479"
  }
if mode=="Zmumu":
  ebCuts = {\
  'All'   : '(1)',
  'EEcut' : "abs(l0eta)>1.1&&abs(l1eta)>1.1",
  'EBcut' : "((abs(l0eta)>1.1&&abs(l1eta)<1.1)||(abs(l1eta)>1.1&&abs(l0eta)<1.1))",
  'BBcut' : "abs(l0eta)<1.1&&abs(l1eta)<1.1"
  }

def getStack(varstring, binning, cutstring, varfunc = "", addData=True, additionalCutFunc = ""):
  DATA            = variable(varstring, binning, cutstring,additionalCutFunc=additionalCutFunc)
  DATA.sample     = data[mode]
#  DATA.color    = ROOT.kGray
  DATA.color      = dataColor
  DATA.legendText = "Data"
  DATA.markerSize = 0.4

  MC_DY                        = variable(varstring, binning, cutstring, additionalCutFunc=additionalCutFunc) 
  MC_DY.sample                 = dy[mode]
  MC_DIBOSON                   = variable(varstring, binning, cutstring, additionalCutFunc=additionalCutFunc) 
  MC_DIBOSON.sample            = diboson[mode]
  MC_TTJETS                    = variable(varstring, binning, cutstring, additionalCutFunc=additionalCutFunc)
  MC_TTJETS.sample             = ttJets[mode]
  MC_STOP                      = variable(varstring, binning, cutstring, additionalCutFunc=additionalCutFunc) 
  MC_STOP.sample               = singleTop[mode]
  MC_WJETS                     = variable(varstring, binning, cutstring, additionalCutFunc=additionalCutFunc) 
  MC_WJETS.sample              = wJetsToLNu[mode]

  MC_DY.legendText             = "Z(ll) + Jets"
  MC_DY.style                  = "f0"
  MC_DY.add                    = [MC_DIBOSON]
  MC_DY.color                  = ROOT.kOrange - 2
  MC_DIBOSON.legendText        = "WW, WZ, ZZ"
  MC_DIBOSON.style             = "f0"
  MC_DIBOSON.color             = ROOT.kOrange + 7
  MC_DIBOSON.add               = [MC_TTJETS]
  MC_TTJETS.legendText         = "t#bar{t} + Jets"
  MC_TTJETS.style              = "f0"
  MC_TTJETS.color              = ROOT.kRed + 1
  MC_TTJETS.add                =  [MC_STOP]
  MC_STOP.legendText           = "single t"
  MC_STOP.style                = "f0"
  MC_STOP.add                  = [MC_WJETS]
  MC_STOP.color                = ROOT.kGreen + 3
  MC_WJETS.legendText          = "W + Jets"
  MC_WJETS.style               = "f0"
  MC_WJETS.add                 = []
  MC_WJETS.color               = ROOT.kYellow

  res = [MC_DY, MC_DIBOSON, MC_TTJETS, MC_STOP, MC_WJETS]
  for v in res:
    v.legendCoordinates=[0.61,0.95 - 0.08*3,.98,.95]
 
  getLinesForStack(res, targetLumi)
  nhistos = len(res)
  if addData:
    res.append(DATA)
    res[0].dataMCRatio = [DATA, res[0]]
  if varfunc!="":
    for var in res:
      var.varfunc = varfunc
  return res

mZBinning = [180,82,100]

if doAnalysisVars:
  Zm_stack    = {}
  Zpt_stack   = {}
  Zphi_stack  = {}
  ngoodVertices_stack = {}
  for k in ebCuts.keys():
    Zm_stack[k] = getStack(":Zm;m(ll) (GeV);Number of Events",mZBinning, commoncf+"&&"+ebCuts[k], addData = addData)
    Zm_stack[k][0].addOverFlowBin = "none"
    allStacks.append(Zm_stack[k])

    Zpt_stack[k] = getStack(":Zpt;p_{T,Z} (GeV);Number of Events",[100,0,1000], commoncf+"&&"+Zcut+"&&"+ebCuts[k], addData = addData)
    Zpt_stack[k][0].addOverFlowBin = "none"
    allStacks.append(Zpt_stack[k])

    Zphi_stack[k] = getStack(":Zphi;#phi_{Z};Number of Events",[200,-pi,pi], commoncf+"&&"+Zcut+"&&"+ebCuts[k], addData = addData)
    Zphi_stack[k][0].addOverFlowBin = "none"
    allStacks.append(Zphi_stack[k])

    ngoodVertices_stack[k] = getStack(":ngoodVertices;n_{vertex};Number of Events",[50,0,50], commoncf+"&&"+Zcut+"&&"+ebCuts[k], addData = addData)
    ngoodVertices_stack[k][0].addOverFlowBin = "none"
    allStacks.append(ngoodVertices_stack[k])

for stack in allStacks:
  stack[0].minimum = minimum
  
execfile("../../RA4Analysis/plots/simplePlotsKernel.py")

if normalizeToData:
  for stack in allStacks:
    for var in stack[:-1]:
      var.normalizeTo = stack[-1]
      var.normalizeWhat = stack[0]
    stack[-1].normalizeTo=""
    stack[-1].normalizeWhat=""
#else:
#  for stack in allStacks:
#    for var in stack:
#      var.normalizeTo = ""
#      var.normalizeWhat = "" 
#
for stack in allStacks:
  if addData:
    stack[0].maximum = 6*10**2 *stack[-1].data_histo.GetMaximum()
#    stack[-1].data_histo.SetMarkerStyle(24)
  else:
    stack[0].maximum = 6*10**2 *stack[0].data_histo.GetMaximum()
  stack[0].logy = True
  stack[0].minimum = minimum
#  stack[0].legendCoordinates=[0.76,0.95 - 0.3,.98,.95]
#  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS preliminary}"], [0.2,0.85,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 7 TeV"]]
  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS Collaboration}"], [0.2,0.85,str(int(round(targetLumi/10.))/100.)+" fb^{-1},  #sqrt{s} = 8 TeV"]]


if doAnalysisVars:
  for k in ebCuts.keys():
    ROOT.gStyle.SetOptFit(0)
    Zvoigtian_mc = ROOT.TF1("voigtian_mc", "[4]*exp(-x*[5])+[0]*TMath::Voigt(x-[1],[2], [3], 5)", mZBinning[1], mZBinning[2])
    Zvoigtian_mc.SetParameter(0, 1000)
    Zvoigtian_mc.SetParameter(1, 90.)
    Zvoigtian_mc.SetParameter(2, 2.)
    Zvoigtian_mc.SetParLimits(2, 1., 20.)
    Zvoigtian_mc.FixParameter(3, 2.4952)
    Zvoigtian_mc.SetParameter(4, 10.)
    Zvoigtian_mc.SetParameter(5, 0.0004)
    Zm_stack[k][0].data_histo.Fit(Zvoigtian_mc, "R", "goff")
    Zvoigtian_data = ROOT.TF1("voigtian_data", "[4]*exp(-x*[5])+[0]*TMath::Voigt(x-[1],[2], [3], 5)", mZBinning[1], mZBinning[2] )
    Zvoigtian_data.SetParameter(0, Zvoigtian_mc.GetParameter(0))
    Zvoigtian_data.SetParameter(1, Zvoigtian_mc.GetParameter(1))
    Zvoigtian_data.SetParameter(2, Zvoigtian_mc.GetParameter(2))
    Zvoigtian_data.SetParLimits(2, 1., 20.)
    Zvoigtian_data.FixParameter(3, 2.4952)
    Zvoigtian_data.SetParameter(4, Zvoigtian_mc.GetParameter(4))
    Zvoigtian_data.SetParameter(5, Zvoigtian_mc.GetParameter(5))
    Zm_stack[k][-1].data_histo.Fit(Zvoigtian_data, "R", "goff")
    tsize = 0.03
    Zm_stack[k][0].lines += [[ 0.2, 0.8, "Sim."  ,tsize ]]
    Zm_stack[k][0].lines += [[ 0.27, 0.8, "m_{Z}"  ,tsize ], [0.32, 0.8, str(round(Zvoigtian_mc.GetParameter(1),2))+" #pm "+str(round(Zvoigtian_mc.GetParError(1),3)) +" GeV", tsize ]]
    Zm_stack[k][0].lines += [[ 0.27, 0.77, "#sigma",tsize ], [0.32, 0.77, str(round(Zvoigtian_mc.GetParameter(2),2))+" #pm "+str(round(Zvoigtian_mc.GetParError(2),3))+" GeV", tsize ]]
    Zm_stack[k][0].lines += [[ 0.2, 0.74, "Data"  ,tsize ]]
    Zm_stack[k][0].lines += [[ 0.27, 0.74, "m_{Z}"  ,tsize ],[0.32, 0.74, str(round(Zvoigtian_data.GetParameter(1),2))+" #pm "+str(round(Zvoigtian_data.GetParError(1),3)) +" GeV", tsize ]]
    Zm_stack[k][0].lines += [[ 0.27, 0.71, "#sigma",tsize ], [0.32, 0.71, str(round(Zvoigtian_data.GetParameter(2),2))+" #pm "+str(round(Zvoigtian_data.GetParError(2),3))+" GeV", tsize ]]
    Zm_stack[k][0].lines += [[ 0.2, 0.65, "#Gamma" ,tsize ],[0.25, 0.65, str(round(Zvoigtian_mc.GetParameter(3),3))+" GeV (frozen)", tsize]]

    drawNMStacks(1,1,[Zm_stack[k]],             subdir+prefix+"Zm_"+k)
    drawNMStacks(1,1,[Zpt_stack[k]],             subdir+prefix+"Zpt_"+k)
    ngoodVertices_stack[k][0].logy = False
    ngoodVertices_stack[k][0].maximum = 600*10**3 
    ngoodVertices_stack[k][0].minimum = 0 
    drawNMStacks(1,1,[ngoodVertices_stack[k]],             subdir+prefix+"ngoodVertices_"+k)

    drawNMStacks(1,1,[Zphi_stack[k]],             subdir+prefix+"Zphi_"+k)
