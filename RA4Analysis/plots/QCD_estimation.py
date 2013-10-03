import ROOT
from array import array
from math import *
import os, copy

from simplePlotsCommon import *
from funcs import *
from simpleStatTools import niceNum

import xsec
#xsec.xsec["WJets-HT300"] = 51.4
small = False
#mode = "Mu"
mode = "Ele"

if mode=="Mu":
  from defaultMuSamples import *

if mode=="Ele":
  from defaultEleSamples import *

for sample in allSamples:
  sample["dirname"] = "/data/schoef/pat_111201/"+mode.replace("Ele","EG")+"/"
  if mode=="Ele" and sample["name"].lower()=="mc":
    sample["dirname"] = "/data/schoef/pat_120119/EG/"
  sample["Chain"] = "Events"

bjetbins = {"inc":"(1)", \
            "b0":"(!(btag0>1.74))",
            "b1":"(btag0>1.74&&(!(btag1>1.74)))",
            "b2":"(btag1>1.74)"
            }

commoncf = "(0)"
if mode== "Mu":
  commoncf = "isopfRA4Tupelizer_jet2pt>40&&isopfRA4Tupelizer_leptonPt>20&&isopfRA4Tupelizer_singleMuonic"

if mode== "Ele":
  commoncf = "isopfRA4Tupelizer_jet2pt>40&&isopfRA4Tupelizer_leptonPt>20&&isopfRA4Tupelizer_singleElectronic"

#commoncf+="&&run<=166967" #no MHT trigger in that run-range 

control_commoncf = commoncf+"&&isopfRA4Tupelizer_run<166967&&isopfRA4Tupelizer_barepfmet<50&&isopfRA4Tupelizer_ht>300&&isopfRA4Tupelizer_leptonDxy>0.01"
if mode=="Ele":
  control_commoncf = commoncf+"&&isopfRA4Tupelizer_barepfmet>50&&isopfRA4Tupelizer_barepfmet<100&&isopfRA4Tupelizer_ht>300&&isopfRA4Tupelizer_leptonDxy>0.01"

signal_commoncf = commoncf+"&&isopfRA4Tupelizer_barepfmet>250&&isopfRA4Tupelizer_ht>750"
if mode=="Ele":
  signal_commoncf = commoncf+"&&isopfRA4Tupelizer_barepfmet>250&&isopfRA4Tupelizer_ht>300"

additionalCut = ""

allVars=[]
allStacks=[]

signalColors = [ROOT.kBlack, ROOT.kBlue + 1, ROOT.kGreen + 2, ROOT.kOrange + 2]

minimum=10**(-0.5)

preprefix=""
if small:
  preprefix="small"

subdir = "/pngQCD/"

normalizeToData = True

if additionalCut!="":
  commoncf+="&&"+additionalCut

prefix=mode+"_"
if preprefix != "":
  prefix+= preprefix+"_"

binningHT =  [300, 350, 500, 750, 1000]
binningMET = [100, 150, 200, 250, 350, 450, 550]
data = ROOT.TChain("Events")
data.Add("/data/schoef/pat_111201/"+mode.replace("Ele","EG")+"/Run2011A-Aug5ReReco-v1/*.root")
data.Add("/data/schoef/pat_111201/"+mode.replace("Ele","EG")+"/Run2011A-May10ReReco/*.root")
data.Add("/data/schoef/pat_111201/"+mode.replace("Ele","EG")+"/Run2011A-Prompt-v4/*.root")
data.Add("/data/schoef/pat_111201/"+mode.replace("Ele","EG")+"/Run2011A-Prompt-v6/*.root")
data.Add("/data/schoef/pat_111201/"+mode.replace("Ele","EG")+"/Run2011B-Prompt-v1/*.root")
 
sideBandYield = {}
for bjb in bjetbins.keys():
  print "At mode",mode,bjb,bjetbins[bjb]
  data.Draw(">>eListsideBand", signal_commoncf.replace("&&isopfRA4Tupelizer_barepfmet>250","")+"&&"+bjetbins[bjb])
  eListsideBand = ROOT.gROOT.Get("eListsideBand")
  sideBandYield[bjb] = {}
  for htcut in binningHT:
    sideBandYield[bjb][htcut] = {}
    for metcut in binningMET:
      sideBandYield[bjb][htcut][metcut] = {}
      sideBandYield[bjb][htcut][metcut]["0.5to1.5"]=0
      sideBandYield[bjb][htcut][metcut]["0.35to0.7"]=0
  for n in range(eListsideBand.GetN()):
    data.GetEntry(eListsideBand.GetEntry(n))
    ht = getValue (data, "isopfRA4Tupelizer_ht")
    met = getValue(data, "isopfRA4Tupelizer_barepfmet")
    relIso = getValue(data, "isopfRA4Tupelizer_leptonRelIso")
    for htcut in binningHT:
      if ht>htcut:
        for metcut in binningMET:
          if met > metcut:
            if relIso > 0.5 and relIso < 1.5:
              sideBandYield[bjb][htcut][metcut]["0.5to1.5"] += 1
            if relIso > 0.35 and relIso < 0.7:
              sideBandYield[bjb][htcut][metcut]["0.35to0.7"] += 1
  del eListsideBand

#def getStack(varstring, binning, cutstring, varfunc = ""):
#  DATA          = variable(varstring, binning, cutstring)
#  DATA.sample   = data
##  DATA.color    = ROOT.kGray
#  DATA.color    = dataColor
#  DATA.legendText="Data"
#  mc_cut = cutstring
#  if mode=="Ele":
#    mc_cut = cutstring+"&&isopfRA4Tupelizer_HLTEle10CaloIdLCaloIsoVLTrkIdVLTrkIsoVLHT200"
#
#  MC_QCD                       = variable(varstring, binning, mc_cut)
#  MC_QCD.minimum               = 10**(-1)
#
#  MC_TTJETS                    = copy.deepcopy(MC_QCD)
#  MC_WJETS                     = copy.deepcopy(MC_QCD)
#  MC_ZJETS                     = copy.deepcopy(MC_QCD)
#  MC_STOP                      = copy.deepcopy(MC_QCD)
#
#  MC_QCD                       = variable(varstring, binning, mc_cut)
#  MC_QCD.minimum               = 5*10**(-1)
#  MC_QCD.sample                = copy.deepcopy(mc)
#  MC_QCD.sample["bins"]        = QCD_Bins
#  MC_TTJETS                    = copy.deepcopy(MC_QCD)
#  MC_TTJETS.sample             = copy.deepcopy(mc)
#  MC_TTJETS.sample["bins"]     = ["TTJets"]
#  MC_WJETS                     = copy.deepcopy(MC_QCD)
#  MC_WJETS.sample              = copy.deepcopy(mc)
#  MC_WJETS.sample["bins"]      = WJets_Bins
#
#  MC_ZJETS                     = copy.deepcopy(MC_QCD)
#  MC_ZJETS.sample              = copy.deepcopy(mc)
#  MC_ZJETS.sample["bins"]      = ZJets_Bins
#  MC_STOP                     = copy.deepcopy(MC_QCD)
#  MC_STOP.sample              = copy.deepcopy(mc)
#  MC_STOP.sample["bins"]      = singleTop_Bins
#
#  MC_TTJETS.legendText         = "t#bar{t} + Jets"
#  MC_TTJETS.style              = "f0"
#  MC_TTJETS.color              = ROOT.kRed - 3
#
#  MC_ZJETS.legendText          = "DY + Jets"
#  MC_ZJETS.style               = "f0"
#  MC_ZJETS.add                 = [MC_TTJETS]
#  MC_ZJETS.color               = ROOT.kGreen + 3
#  MC_STOP.legendText          = "single Top"
#  MC_STOP.style               = "f0"
#  MC_STOP.add                 = [MC_ZJETS]
#  MC_STOP.color               = ROOT.kOrange + 4
#  MC_QCD.color                 = myBlue
#  MC_QCD.legendText            = "QCD"
#  MC_QCD.style                 = "f0"
#  MC_QCD.add                   = [MC_STOP]
#  MC_WJETS.legendText          = "W + Jets"
#  MC_WJETS.style               = "f0"
#  MC_WJETS.add                 = [MC_QCD]
#  MC_WJETS.color               = ROOT.kYellow
#  res = [MC_TTJETS, MC_WJETS, MC_QCD, MC_STOP, MC_ZJETS]
#  MC_TTJETS.add=[MC_WJETS]
#  MC_ZJETS.add=[]
#  res[0].dataMCRatio = [DATA, res[0]]
#
#  getLinesForStack(res, targetLumi)
#  nhistos = len(res)
#  for var in res:
#    var.legendCoordinates=[0.61,0.95 - 0.08*5,.98,.95]
##    var.legendCoordinates=[0.64,0.95 - 0.05*nhistos,.98,.95] #for signalnumbers = [0,1]
#  res.append(DATA)
#  if varfunc!="":
#    for var in res:
#      var.varfunc = varfunc
#  return res
#
#relIsoBinning = [15, 0, 1.5]
#if mode=="Ele":
#  relIsoBinning = [21, 0, 1.47]
#
#leptonRelIsoControl_stack = {}
#leptonRelIsoSignal_stack = {}
#for bjb in bjetbins.keys():
#  leptonRelIsoControl_stack[bjb]               = getStack(":isopfRA4Tupelizer_leptonRelIso;relIso;Number of Events",relIsoBinning, control_commoncf+"&&"+bjetbins[bjb])
#  leptonRelIsoControl_stack[bjb][0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonRelIsoControl_stack[bjb])
#
#  leptonRelIsoSignal_stack[bjb]               = getStack(":isopfRA4Tupelizer_leptonRelIso;relIso;Number of Events", relIsoBinning, signal_commoncf+"&&"+bjetbins[bjb])
#  leptonRelIsoSignal_stack[bjb][0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonRelIsoSignal_stack[bjb])
#
#
#for stack in allStacks:
#  stack[0].minimum = minimum
#
#for stack in allStacks:
#  for var in stack:
#    var.addOverFlowBin = "both"
#
#reweightingHistoFile = "reweightingHisto_Summer2011.root"
#execfile("simplePlotsLoopKernel.py")
#
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
#
#for stack in allStacks:
#  stack[0].maximum = 10.*stack[-1].data_histo.GetMaximum()
#  stack[0].logy = True
#  stack[0].minimum = minimum
##  stack[0].legendCoordinates=[0.76,0.95 - 0.3,.98,.95]
##  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS preliminary}"], [0.2,0.85,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 7 TeV"]]
#  stack[0].legendCoordinates=[0.61,0.95 - 0.08*5,.98,.95]
#  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS preliminary}"], [0.2,0.85, "#sqrt{s} = 7 TeV"]]
#
#for bjb in bjetbins.keys():
#  leptonRelIsoControl_stack[bjb][0].maximum = 1000.*leptonRelIsoControl_stack[bjb][-1].data_histo.GetMaximum()
#  #drawNMStacks(1,1,[ngoodVertices_stack],             subdir+prefix+"ngoodVertices", False)
#  drawNMStacks(1,1,[leptonRelIsoControl_stack[bjb]],             subdir+prefix+"leptonRelIsoControl_"+bjb, False)
#  drawNMStacks(1,1,[leptonRelIsoSignal_stack[bjb]],             subdir+prefix+"leptonRelIsoSignal_"+bjb, False)
#
#for stack in allStacks:
#  stack[0].maximum = 1.3*stack[-1].data_histo.GetMaximum()
#  stack[0].logy = False
#  stack[0].minumum=0
#
#for bjb in bjetbins.keys():
#  leptonRelIsoControl_stack[bjb][0].maximum = 2.*leptonRelIsoControl_stack[bjb][-1].data_histo.GetMaximum()
#
#  drawNMStacks(1,1,[leptonRelIsoControl_stack[bjb]],            subdir+prefix+"leptonRelIsoControl_"+bjb+"_lin", False)
#  drawNMStacks(1,1,[leptonRelIsoSignal_stack[bjb]],             subdir+prefix+"leptonRelIsoSignal_"+bjb+"_lin", False)
#
#
#def relIsoIntegral(histo, x0, x1):
#  if not type(histo)==type(ROOT.TH1F()):
#    histo = histo.data_histo
#  a = histo.GetXaxis()
#  return histo.Integral(a.FindBin(x0), a.FindBin(x1))
#
#def MCQCDcontribution(stack,x0,x1):
#  return relIsoIntegral(stack[2], x0, x1) - relIsoIntegral(stack[3], x0, x1)
#
#def MCEWKcontribution(stack,x0,x1):
#  return relIsoIntegral(stack[0], x0, x1)  - MCQCDcontribution(stack,x0,x1)
#
#def Datacontribution(stack,x0,x1):
#  return relIsoIntegral(stack[-1], x0, x1)
#
#prediction = {}
#predictionRatio = {}
#dataControlLow  = {} 
#dataControlHigh = {} 
#dataSignalHigh  = {} 
#dataSignalHighCorr ={}
#dataControlLowCorr ={}
#dataControlHighCorr= {}
#prediction_shape={}
#MCEWKControlLow  = {}
#MCEWKControlHigh = {}
#MCEWKSignalHigh  = {}
#
#relIsoControlRegion = 0.5
#if mode=="Ele":
#  relIsoControlRegion = 0.07 #FIXME
#
#for bjb in bjetbins.keys():
#  dataControlLow [bjb] = Datacontribution(leptonRelIsoControl_stack[bjb], 0, 0)
#  dataControlHigh[bjb] = Datacontribution(leptonRelIsoControl_stack[bjb],     relIsoControlRegion, 1.5)
#  dataSignalHigh [bjb] = Datacontribution(leptonRelIsoSignal_stack[bjb],      relIsoControlRegion, 1.5)
#  MCEWKControlLow [bjb] = MCEWKcontribution(leptonRelIsoControl_stack[bjb],   0, 0)
#  MCEWKControlHigh[bjb] = MCEWKcontribution(leptonRelIsoControl_stack[bjb],   relIsoControlRegion, 1.5)
#  MCEWKSignalHigh [bjb] = MCEWKcontribution(leptonRelIsoSignal_stack[bjb],    relIsoControlRegion, 1.5)
#  print "dataControlLow"  , niceNum(dataControlLow[bjb])
#  print "dataControlHigh" , niceNum(dataControlHigh[bjb])
#  print "dataSignalHigh"  , niceNum(dataSignalHigh[bjb])
#  print "MCEWKControlLow" , niceNum(MCEWKControlLow[bjb])
#  print "MCEWKControlHigh", niceNum(MCEWKControlHigh[bjb])
#  print "MCEWKSignalHigh" , niceNum(MCEWKSignalHigh[bjb])
#  dataControlLowCorr[bjb] = dataControlLow[bjb]
#  if dataControlLow[bjb]>MCEWKControlLow[bjb]:
#    dataControlLowCorr[bjb] = dataControlLow[bjb] - MCEWKControlLow[bjb]
#  else:
#    print "dataControlLow[bjb] not corrected!",dataControlLow[bjb],">",MCEWKControlLow[bjb]
#  dataControlHighCorr[bjb] = dataControlHigh[bjb]
#  if dataControlHigh[bjb]>MCEWKControlHigh[bjb]:
#    dataControlHighCorr[bjb] = dataControlHigh[bjb] - MCEWKControlHigh[bjb]
#  else:
#    print "dataControlHigh[bjb] not corrected!",dataControlHigh[bjb],">",MCEWKControlHigh[bjb]
#  dataSignalHighCorr[bjb] = dataSignalHigh[bjb]
#  if dataSignalHigh[bjb]>MCEWKSignalHigh[bjb]:
#    dataSignalHighCorr[bjb] = dataSignalHigh[bjb] - MCEWKSignalHigh[bjb]
#  else:
#    print "dataSignalHigh[bjb] not corrected!",dataSignalHigh[bjb],">",MCEWKSignalHigh[bjb]
#  prediction[bjb] = -1
#  predictionRatio[bjb] = -1
#  if dataControlHighCorr[bjb]>0:
#    predictionRatio[bjb] = (dataControlLowCorr[bjb]/dataControlHighCorr[bjb])
#    prediction[bjb] = dataSignalHighCorr[bjb]*predictionRatio[bjb]
#  prediction_shape[bjb]            = variable(":isopfRA4Tupelizer_leptonRelIso;relIso;Number of Events", relIsoBinning, control_commoncf)
#  prediction_shape[bjb].data_histo = leptonRelIsoControl_stack[bjb][2].data_histo.Clone()
#  if dataControlHighCorr[bjb]>0.:
#    prediction_shape[bjb].data_histo.Scale(dataSignalHighCorr[bjb]/relIsoIntegral(prediction_shape[bjb], 0.5, 1.5))
#  prediction_shape[bjb].legendText          = "prediction"
#  for stack in allStacks:
#    stack[0].maximum = 10.*stack[-1].data_histo.GetMaximum()
#    stack[0].logy = True
#    stack[0].minimum = minimum/10.
#  #  stack[0].legendCoordinates=[0.76,0.95 - 0.3,.98,.95]
#  #  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS preliminary}"], [0.2,0.85,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 7 TeV"]]
#    stack[0].legendCoordinates=[0.61,0.95 - 0.08*5,.98,.95]
#    stack[0].lines = [[0.2, 0.9, "#font[22]{CMS preliminary}"], [0.2,0.85, "#sqrt{s} = 7 TeV"]]
#  drawNMStacks(1,1,[leptonRelIsoSignal_stack[bjb]+[prediction_shape[bjb]]], subdir+prefix+"leptonRelIsoControl_"+bjb+"_withPrediction", False)
#
#if not small:
#  filename = "/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/"+prefix+"QCDResult.py"
#  outfile = file(filename,"w")
#  outfile.write("prediction="+repr(prediction)+"\n")
#  outfile.write("predictionRatio="+repr(predictionRatio)+"\n")
#  outfile.write("dataControlHighCorr="+repr(dataControlHighCorr)+"\n")
#  outfile.write("dataSignalHighCorr="+repr(dataSignalHighCorr)+"\n")
#  outfile.write("dataControlLowCorr="+repr(dataControlLowCorr)+"\n")
#  outfile.write("dataControlLowCorr="+repr(dataControlLowCorr)+"\n")
#  outfile.write("dataSignalHigh="+repr(dataSignalHigh)+"\n")
#  outfile.write("dataControlLow="+repr(dataControlLow)+"\n")
#  outfile.write("dataControlLow="+repr(dataControlLow)+"\n")
#  outfile.write("MCEWKControlLow" +repr(MCEWKControlLow)+"\n")
#  outfile.write("MCEWKControlHigh"+repr(MCEWKControlHigh)+"\n")
#  outfile.write("MCEWKSignalHigh" +repr(MCEWKSignalHigh)+"\n")
#  outfile.close()
#  print "Written ",outfile
#
#
#
#sideBandYield = {}
#for bjb in bjetbins.keys():
#  print "At mode",mode,bjb,bjetbins[bjb]
#  data.Draw(">>eListsideBand", signal_commoncf+"&&"+bjetbins[bjb]+"&&isopfRA4Tupelizer_leptonRelIso>"+str(relIsoControlRegion)+"&&isopfRA4Tupelizer_leptonRelIso<1.5")
#  eListsideBand = ROOT.gROOT.Get("eListsideBand")
#  sideBandYield[bjb] = {}
#  for htcut in binningHT:
#    sideBandYield[bjb][htcut] = {}
#    for metcut in binningMET:
#      sideBandYield[bjb][htcut][metcut] = 0.
#  for n in range(eListsideBand.GetN()):
#    data.GetEntry(eListsideBand.GetEntry(n))
#    ht = getValue (data, "ht")
#    met = getValue(data, "barepfmet")
#    for htcut in binningHT:
#      if ht>htcut:
#        for metcut in binningMET:
#          if met > metcut:
#            sideBandYield[bjb][htcut][metcut] += 1
#  del eListsideBand
#
#
#for htcut in binningHT:
#  print "\\hline & \\multicolumn{4}{c}{$\\HT >"+str(htcut)+"$ \\GeV, }\\\\ \\hline"
#  for metcut in binningMET:
#    sB = ""
#    for bjb in ["inc", "b0", "b1", "b2"]:
#      qcdPred =  "$"+str(niceNum(sideBandYield[bjb][htcut][metcut]*predictionRatio[bjb]))+"\\pm "+str(niceNum(sqrt(1.00**2 + max(1, sideBandYield[bjb][htcut][metcut]))*predictionRatio[bjb],3))+"$"
#      sB += qcdPred+" & "
#    sB = "$\\ETmiss > "+str(metcut)+"$ \\GeV & "+sB[:-2]+"\\\\"
#    print sB
#
