#QCDestABCD2_lepAll_index.py
import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.degTools import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.cutsEle import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_mAODv2_analysisHephy13TeV import getSamples
from Workspace.DegenerateStopAnalysis.toolsMateusz.cmgTuplesPostProcessed_mAODv2_analysisHephy13TeV import cmgTuplesPostProcessed
#from Workspace.DegenerateStopAnalysis.toolsMateusz.cmgTuplesPostProcessed_mAODv2 import cmgTuplesPostProcessed
#from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_analysisHephy_13TeV import getSamples
#from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_PP_mAODv2_7412pass2_scan import getSamples

from array import array
from math import pi, sqrt #cos, sin, sinh, log

ROOT.setTDRStyle(1)
ROOT.gStyle.SetOptStat(0) #1111 #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis

#Input options
parser = argparse.ArgumentParser(description = "Input options")
#parser.add_argument("--isolation", dest = "isolation",  help = "Isolation (hybIso03/hybIso04)", type = str, default = "hybIso03")
#parser.add_argument("--MET", dest = "MET",  help = "MET Cut", type = str, default = "300")
#parser.add_argument("--HT", dest = "HT",  help = "HT Cut", type = str, default = "300")
#parser.add_argument("--METloose", dest = "METloose",  help = "Loose MET Cut", type = str, default = "100")
#parser.add_argument("--eleWP", dest = "eleWP",  help = "Electron WP", type = str, default = "Veto")
#parser.add_argument("--enriched", dest = "enriched",  help = "EM enriched QCD?", type = bool, default = False)
parser.add_argument("--index", dest = "index",  help = "Electron index", type = str, default = "leadingEle")
parser.add_argument("--plot", dest = "plot",  help = "Toggle plot", type = int, default = 1)
#parser.add_argument("--save", dest = "save",  help = "Toggle save", type = int, default = 1)
parser.add_argument("-b", dest = "batch",  help = "Batch mode", action = "store_true", default = False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
#isolation = args.isolation
#METcut = args.MET
#METloose = args.METloose
#HTcut = args.HT
#eleWP = args.eleWP
#enriched = args.enriched
index = args.index
plot = args.plot
save = args.save

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD2/estimation/lepAll/index"
   if not os.path.exists(savedir): os.makedirs(savedir)

#Samples
#if enriched == True: qcd = "qcdem"
#else: qcd = "qcd"

privateSignals = ["s10FS", "s30", "s30FS", "s60FS", "t2tt30FS"]
backgrounds = ["w","tt", "z", "qcd"]

cmgPP = cmgTuplesPostProcessed()#mc_path, signal_path, data_path)

samplesList = backgrounds # + privateSignals
samples = getSamples(cmgPP = cmgPP, skim = 'presel', sampleList = samplesList, scan = False, useHT = True, getData = False)

officialSignals = ["s300_290", "s300_270", "s300_250"] #FIXME: crosscheck if these are in allOfficialSignals

allOfficialSignals = samples.massScanList()
#allOfficialSignals = [s for s in samples if samples[s]['isSignal'] and not samples[s]['isData'] and s not in privateSignals and s not in backgrounds] 
allSignals = privateSignals + allOfficialSignals
allSamples = allSignals + backgrounds

#selectedSamples = privateSignals + officialSignals + backgrounds
selectedSamples = ["qcd", "z", "tt", "w"]#, "s300_270"]

print makeLine()
print "Using samples:"
newLine()
for s in selectedSamples:
   if s: print samples[s].name,":",s
   else:
      print "!!! Sample " + sample + " unavailable."
      sys.exit(0)

#suffix = "_HT" + HTcut + "_MET" + METcut + "_METloose" + METloose
#if enriched == True: suffix += "_EMenriched"

suffix = "_" + index

if index == "leadingEle":
   ind = "IndexLepAll_el[0]"
elif index == "leadingLep":
   ind = "0"

QCDcuts = {}
 
print makeLine()
print "Using LepAll collection."
#print "Ignoring " + otherCollection + " collection."
print makeLine()

#Gets all cuts (electron, SR, CR) for given electron ID
eleIDsel = electronIDsIndex(ID = "nMinus1", removedCut = "d0", iso = False, collection = "LepAll", index = index)
#eleIDsel_other = electronIDs(ID = "nMinus1", removedCut = "d0", iso = False, collection = otherCollection)

##for s in samples.massScanList(): samples[s].weight = "weight" #removes ISR reweighting from official mass scan signal samples
#for s in samples: samples[s].tree.SetAlias("eleSel", allCuts[WP]['eleSel'])

etaAcc = 2.1
eleSel = "abs(LepAll_pdgId[" + ind + "]) == 11 && abs(LepAll_eta[" + ind + "]) < " + str(etaAcc) + " && " + eleIDsel['Veto']
#eleSel_other = "abs(" + otherCollection + "_pdgId) == 11 && abs(" + otherCollection + "_eta) < " + str(etaAcc) + " && " + eleIDsel_other['Veto']

#elePt = "LepAll_pt[IndexLepAll_el[0]]"
#dxy = "abs(LepAll_dxy[IndexLepAll_el[0]])"
#absIso = "LepAll_absIso03[IndexLepAll_el[0]]"
#relIso = "LepAll_relIso03[IndexLepAll_el[0]]"
#hybIso = "(LepAll_relIso03[IndexLepAll_el[0]]*min(LepAll_pt[IndexLepAll_el[0]], 25))"

#Cuts
dxyCut = "abs(LepAll_dxy[" + ind + "]) < 0.02"
looseDxyCut = "abs(LepAll_dxy[" + ind + "]) < 0.05"

hybIsoCut = "(LepAll_relIso03[" + ind + "]*min(LepAll_pt[" + ind + "], 25)) < 5"
antiHybIsoCut = "(LepAll_relIso03[" + ind + "]*min(LepAll_pt[" + ind + "], 25)) > 5"
#hybIsoCut = "((LepAll_absIso03 < 5) || LepAll_relIso03 < 0.2))"
#antiHybIsoCut = "((LepAll_absIso03 > 5) && (LepAll_relIso03 > 0.2))"
   
presel = CutClass("presel_SR", [
   ["MET300","met > 200"],
   ["HT300","ht_basJet > 200"],
   ["ISR110", "nIsrJet >= 1"],
   ["No3rdJet60","nVetoJet <= 2"],
   ["BVeto","(nBSoftJet == 0 && nBHardJet == 0)"],
   ["eleSel", "nLepAll_el > 0 && " + eleSel],
   #["otherCollection", "Sum$(" + eleSel_other + ") == 0"],
   #["elePt<30", elePt + " < 30"],
   #["anti-AntiQCD", "vetoJet_dPhi_j1j2 > 2.5"],
   #["anti-HybIso", "Sum$(" + eleSel + "&&" + antiHybIsoCut + ") == 1"],
   #["anti-dxy", "Max$(abs(" + lep + "_dxy*(" + eleSel + "&&" + antiHybIsoCut + "))) > 0.02"],
   ], baseCut = None) #allCuts['None']['presel'])

SRs = {\
   'SR1':["SR1","1"],
   'SR1a':["SR1a", joinCutStrings(["LepAll_mt[" + ind + "] < 60", "LepAll_pt < 30"])],
   'SR1b':["SR1b", joinCutStrings([btw("LepAll_mt[" + ind + "]", 60, 88), "LepAll_pt < 30"])],
   'SR1c':["SR1c", joinCutStrings(["LepAll_mt[" + ind + "] < 88", "LepAll_pt < 30"])],
   
   'SRL1a':["SRL1a", joinCutStrings(["LepAll_mt[" + ind + "] < 60", btw("LepAll_pt[" + ind + "]", 5, 12)])],
   'SRH1a':["SRH1a", joinCutStrings(["LepAll_mt[" + ind + "] < 60", btw("LepAll_pt[" + ind + "]", 12, 20)])],
   'SRV1a':["SRV1a", joinCutStrings(["LepAll_mt[" + ind + "] < 60", btw("LepAll_pt[" + ind + "]", 20, 30)])],
   
   'SRL1b':["SRL1b", joinCutStrings([btw("LepAll_mt[" + ind + "]", 60, 88), btw("LepAll_pt[" + ind + "]", 5, 12)])],
   'SRH1b':["SRH1b", joinCutStrings([btw("LepAll_mt[" + ind + "]", 60, 88), btw("LepAll_pt[" + ind + "]", 12, 20)])],
   'SRV1b':["SRV1b", joinCutStrings([btw("LepAll_mt[" + ind + "]", 60, 88), btw("LepAll_pt[" + ind + "]", 20, 30)])],
   
   'SRL1c':["SRL1c", joinCutStrings(["LepAll_mt[" + ind + "] > 88", btw("LepAll_pt[" + ind + "]", 5, 12)])],
   'SRH1c':["SRH1c", joinCutStrings(["LepAll_mt[" + ind + "] > 88", btw("LepAll_pt[" + ind + "]", 12, 20)])],
   'SRV1c':["SRV1c", joinCutStrings(["LepAll_mt[" + ind + "] > 88", btw("LepAll_pt[" + ind + "]", 20, 30)])]}


QCD = {}

regions = ['SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']

for reg in regions:
   QCD[reg] = {}
 
   #SR 
   QCD[reg]['SR'] = CutClass("QCD_SR_" + reg, [
      #["elePt<30", elePt['ID'] + " < 30"],
      SRs[reg],
      ["I", hybIsoCut], #applied
      ["D", dxyCut], #applied
      ["A", "vetoJet_dPhi_j1j2 < 2.5"], #applied
      ], baseCut = presel)

   #nA
   QCD[reg]['I_DA'] = CutClass("QCD_I_DA_" + reg, [
      #["elePt<30", elePt['ID'] + " < 30"],
      SRs[reg], 
      ["anti-I", antiHybIsoCut], #inverted
      ["D", dxyCut], #applied
      ["A", "vetoJet_dPhi_j1j2 < 2.5"], #applied
      ], baseCut = presel)
   
   #nI
   QCD[reg]['DA_I'] = CutClass("QCD_DA_I_" + reg, [
      #["elePt<30", elePt['D_I'] + " < 30"],
      SRs[reg], 
      ["I", hybIsoCut], #applied
      ["loose-D", looseDxyCut], #inverted 
      ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
      ], baseCut = presel)
   
   #nIDA
   QCD[reg]['IDA'] = CutClass("QCD_IDA_" + reg, [
      #["elePt<30", elePt['ID'] + " < 30"],
      SRs[reg], 
      ["anti-I", antiHybIsoCut], #inverted
      ["loose-D", looseDxyCut], #inverted 
      ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
      ], baseCut = presel) 

abcd = ['SR', 'I_DA', 'DA_I', 'IDA']

yields = {}
QCDexp = {}

for reg in regions:
   yields[reg] = {}
   
   for sel in abcd:
      yields[reg][sel] = Yields(samples, ['qcd'], QCD[reg][sel], cutOpt = "combinedList", weight = "weight", pklOpt = False, tableName = reg + "_" + sel, nDigits = 2, err = True, verbose = True, nSpaces = 10)
  
   QCDexp[reg] = (yields[reg]['I_DA'].yieldDictFull['qcd']['QCD_I_DA_' + reg] * yields[reg]['DA_I'].yieldDictFull['qcd']['QCD_DA_I_' + reg]/\
   yields[reg]['IDA'].yieldDictFull['qcd']['QCD_IDA_' + reg])
   
   #QCDerr[reg] = QCDexp * sqrt(\
   #         (totalErr['nAerr']/totalYlds['nA'])*(totalErr['nAerr']/totalYlds['nA']) +\
   #         (totalErr['nIerr']/totalYlds['nI'])*(totalErr['nIerr']/totalYlds['nI']) +\
   #         (totalErr['nDerr']/totalYlds['nD'])*(totalErr['nDerr']/totalYlds['nD']) +\
   #         2*(totalErr['nIDAerr']/totalYlds['nIDA'])*(totalErr['nIDAerr']/totalYlds['nIDA']))
  
   print makeLine()
   print "nI_DA = ", yields[reg]['I_DA'].yieldDictFull['qcd']['QCD_I_DA_' + reg], " | nDA_I = ", yields[reg]['DA_I'].yieldDictFull['qcd']['QCD_DA_I_' + reg],\
         " | nIDA = ", yields[reg]['IDA'].yieldDictFull['qcd']['QCD_IDA_' + reg]
   print "QCD Estimation in ", reg, ": ", QCDexp[reg]
   print "QCD MC yield in ", reg, ": ", yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg]
   print makeLine()
   
   if not os.path.isfile(savedir + "/QCDyields" + suffix + ".txt"):
      outfile = open(savedir + "/QCDyields" + suffix + ".txt", "w")
      outfile.write(" SR           I_DA               DA_I               IDA               QCD               MC               Ratio\n")
   with open(savedir + "/QCDyields" + suffix + ".txt", "a") as outfile:
      outfile.write(reg + "     " +\
      str(yields[reg]['I_DA'].yieldDictFull['qcd']['QCD_I_DA_' + reg]) + "        " +\
      str(yields[reg]['DA_I'].yieldDictFull['qcd']['QCD_DA_I_' + reg]) + "        " +\
      str(yields[reg]['IDA'].yieldDictFull['qcd']['QCD_IDA_' + reg]) + "        " +\
      str(QCDexp[reg].round(2)) + "        " +\
      str(yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg]) + "        ")
      if yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg].val:
         outfile.write(str((QCDexp[reg]/yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg]).round(2))  + "\n")
      else:
         outfile.write("\n")
