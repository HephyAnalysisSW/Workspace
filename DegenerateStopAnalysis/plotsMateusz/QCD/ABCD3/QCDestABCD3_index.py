#QCDestABCD3_index.py
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
parser.add_argument("--MET", dest = "MET",  help = "MET Cut", type = str, default = "200") 
parser.add_argument("--HT", dest = "HT",  help = "HT Cut", type = str, default = "200") 
parser.add_argument("--METloose", dest = "METloose",  help = "Loose MET Cut", type = str, default = "150") 
parser.add_argument("--eleWP", dest = "eleWP",  help = "Electron WP", type = str, default = "Veto") 
parser.add_argument("--removedCut", dest = "removedCut",  help = "Variable removed from electron ID", type = str, default = "None") #"sigmaEtaEta" "hOverE" "ooEmooP" "dEta" "dPhi" "d0" "dz" "MissingHits" "convVeto"
#parser.add_argument("--highWeightVeto", dest = "highWeightVeto",  help = "Remove high weighted events", type = bool, default = False)
parser.add_argument("--enriched", dest = "enriched",  help = "EM enriched QCD?", type = bool, default = False) 
parser.add_argument("--index", dest = "index",  help = "Electron index", type = str, default = "leadingEle")
parser.add_argument("--plot", dest = "plot",  help = "Toggle plot", type = int, default = 1)
parser.add_argument("--save", dest = "save",  help = "Toggle save", type = int, default = 1)
parser.add_argument("-b", dest = "batch",  help = "Batch mode", action = "store_true", default = False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
#isolation = args.isolation
index = args.index
METcut = args.MET
METloose = args.METloose
HTcut = args.MET
eleWP = args.eleWP
removedCut = args.removedCut
#highWeightVeto = args.highWeightVeto
enriched = args.enriched
plot = args.plot
save = args.save

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   if removedCut == "None": savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD3/estimation/" + eleWP
   else: savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD3/estimation/" + eleWP + "_no_" + removedCut
   #if highWeightVeto: savedir += "/highWeightVeto"
   if not os.path.exists(savedir): os.makedirs(savedir)

suffix = "_" + eleWP + "_HT" + HTcut + "_MET" + METcut + "_METloose" + METloose

#Samples
if enriched == True:
   qcd = "qcdem"
   suffix += "_EMenriched"
else: qcd = "qcd"

#privateSignals = ["s10FS", "s30", "s30FS", "s60FS", "t2tt30FS"]
#backgrounds = ["w","tt", "z", "qcd"]

cmgPP = cmgTuplesPostProcessed()#mc_path, signal_path, data_path)

#samplesList = backgrounds # + privateSignals
samplesList = ["qcd"] 
samples = getSamples(cmgPP = cmgPP, skim = 'presel', sampleList = samplesList, scan = False, useHT = True, getData = False)

#officialSignals = ["s300_290", "s300_270", "s300_250"] #FIXME: crosscheck if these are in allOfficialSignals
#
#allOfficialSignals = samples.massScanList()
##allOfficialSignals = [s for s in samples if samples[s]['isSignal'] and not samples[s]['isData'] and s not in privateSignals and s not in backgrounds] 
#allSignals = privateSignals + allOfficialSignals
#allSamples = allSignals + backgrounds

#selectedSamples = privateSignals + officialSignals + backgrounds
selectedSamples = samplesList 

print makeLine()
print "Using samples:"
newLine()
for s in selectedSamples:
   if s: print samples[s].name,":",s
   else: 
      print "!!! Sample " + sample + " unavailable."
      sys.exit(0)

suffix = "_HT" + HTcut + "_MET" + METcut + "_METloose" + METloose

if removedCut == "None": suffix += "_" + eleWP 
else: suffix += "_" + eleWP +"_no_" + removedCut

if enriched == True: suffix += "_EMenriched"

suffix += "_" + index

QCDcuts = {}

if index == "leadingEle":
   ind = "IndexLepAll_el[0]"
elif index == "leadingLep":
   ind = "0"

QCDcuts = {}
 
#if collection == "LepAll": otherCollection = "LepOther"
#elif collection == "LepOther": otherCollection = "LepAll"

print makeLine()
print "Using LepAll collection."
#print "Ignoring " + otherCollection + " collection."
print makeLine()

#Gets all cuts (electron, SR, CR) for given electron ID
if removedCut == "None": eleIDsel = electronIDsIndex(ID = "standard", removedCut = "None", iso = False, collection = "LepAll", index = index)
else: eleIDsel = electronIDsIndex(ID = "nMinus1", removedCut = removedCut, iso = False, collection = "LepAll", index = index)

##for s in samples.massScanList(): samples[s].weight = "weight" #removes ISR reweighting from official mass scan signal samples
#for s in samples: samples[s].tree.SetAlias("eleSel", allCuts[WP]['eleSel'])

etaAcc = 2.1
eleSel = "abs(LepAll_pdgId[" + ind + "]) == 11 && abs(LepAll_eta[" + ind + "]) < " + str(etaAcc) + " && " + eleIDsel[eleWP]
#eleSel_other = "abs(" + otherCollection + "_pdgId) == 11 && abs(" + otherCollection + "_eta) < " + str(etaAcc) + " && " + eleIDsel_other['Veto']

#elePt = "LepAll_pt[IndexLepAll_el[0]]"
#dxy = "abs(LepAll_dxy[IndexLepAll_el[0]])"
#absIso = "LepAll_absIso03[IndexLepAll_el[0]]"
#relIso = "LepAll_relIso03[IndexLepAll_el[0]]"
#hybIso = "(LepAll_relIso03[IndexLepAll_el[0]]*min(LepAll_pt[IndexLepAll_el[0]], 25))"

#Cuts
#dxyCut = "abs(LepAll_dxy[" + ind + "]) < 0.02"
#looseDxyCut = "abs(LepAll_dxy[" + ind + "]) < 0.05"

hybIsoCut = "(LepAll_relIso03[" + ind + "]*min(LepAll_pt[" + ind + "], 25)) < 5"
antiHybIsoCut = "(LepAll_relIso03[" + ind + "]*min(LepAll_pt[" + ind + "], 25)) > 5"
#hybIsoCut = "((LepAll_absIso03 < 5) || LepAll_relIso03 < 0.2))"
#antiHybIsoCut = "((LepAll_absIso03 > 5) && (LepAll_relIso03 > 0.2))"
   
presel = CutClass("presel_SR", [
   ["METloose","met >" + METloose], #looser MET for B & D regions
   ["HT","ht_basJet >" + HTcut],
   ["ISR110", "nIsrJet >= 1"],
   ["No3rdJet60","nVetoJet <= 2"],
   ["BVeto","(nBSoftJet == 0 && nBHardJet == 0)"],
   ["eleSel", "nLepAll_el > 0 &&" + eleSel],
   ], baseCut = None) #allCuts['None']['presel'])

SRs = {\
   'SR1':["SR1","LepAll_pt[" + ind + "] < 30"],
   'SR1a':["SR1a", combineCuts("LepAll_mt[" + ind + "] < 60", "LepAll_pt[" + ind + "] < 30")],
   'SR1b':["SR1b", combineCuts(btw("LepAll_mt[" + ind + "]", 60, 88), "LepAll_pt[" + ind + "] < 30")],
   'SR1c':["SR1c", combineCuts("LepAll_mt[" + ind + "] > 88", "LepAll_pt[" + ind + "] < 30")],

   'SRL1a':["SRL1a", combineCuts("LepAll_mt[" + ind + "] < 60", btw("LepAll_pt[" + ind + "]", 5, 12))],
   'SRH1a':["SRH1a", combineCuts("LepAll_mt[" + ind + "] < 60", btw("LepAll_pt[" + ind + "]", 12, 20))],
   'SRV1a':["SRV1a", combineCuts("LepAll_mt[" + ind + "] < 60", btw("LepAll_pt[" + ind + "]", 20, 30))],
   
   'SRL1b':["SRL1b", combineCuts(btw("LepAll_mt[" + ind + "]", 60, 88), btw("LepAll_pt[" + ind + "]", 5, 12))],
   'SRH1b':["SRH1b", combineCuts(btw("LepAll_mt[" + ind + "]", 60, 88), btw("LepAll_pt[" + ind + "]", 12, 20))],
   'SRV1b':["SRV1b", combineCuts(btw("LepAll_mt[" + ind + "]", 60, 88), btw("LepAll_pt[" + ind + "]", 20, 30))],
   
   'SRL1c':["SRL1c", combineCuts("LepAll_mt[" + ind + "] > 88", btw("LepAll_pt[" + ind + "]", 5, 12))],
   'SRH1c':["SRH1c", combineCuts("LepAll_mt[" + ind + "] > 88", btw("LepAll_pt[" + ind + "]", 12, 20))],
   'SRV1c':["SRV1c", combineCuts("LepAll_mt[" + ind + "] > 88", btw("LepAll_pt[" + ind + "]", 20, 30))]}

QCD = {}
regions = ['SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']

for reg in regions:
   QCD[reg] = {}
 
   #SR 
   QCD[reg]['SR'] = CutClass("QCD_SR_" + reg, [
      SRs[reg],
      ["tight-MET", "met >" + METcut], #applied
      ["I", hybIsoCut], #applied
      ["A", "vetoJet_dPhi_j1j2 < 2.5"], #applied
      ], baseCut = presel)

   #nA
   QCD[reg]['IM_A'] = CutClass("QCD_IM_A_" + reg, [
      SRs[reg], 
      ["anti-I", antiHybIsoCut], #inverted
      ["A", "vetoJet_dPhi_j1j2 < 2.5"], #applied
      ], baseCut = presel)
   
   #nI
   QCD[reg]['A_IM'] = CutClass("QCD_A_IM_" + reg, [
      SRs[reg], 
      ["tight-MET", "met >" + METcut], #applied
      ["I", hybIsoCut], #applied
      ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
      ], baseCut = presel)
   
   #nIDA
   QCD[reg]['IMA'] = CutClass("QCD_IMA_" + reg, [
      SRs[reg], 
      ["anti-I", antiHybIsoCut], #inverted
      ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
      ], baseCut = presel) 

abcd = ['SR', 'IM_A', 'A_IM', 'IMA']

yields = {}
QCDexp = {}

if not os.path.isfile(savedir + "/QCDyields" + suffix + ".txt"):
   outfile = open(savedir + "/QCDyields" + suffix + ".txt", "w")
   outfile.write(eleWP + " Electron ID and Preselection of (MET, HT) > (" + METcut + "," + HTcut + ")\nSR           IM_A                 A_IM                     IMA                       QCD                     MC                     Ratio\n")

for reg in regions:
   yields[reg] = {}
   
   for sel in abcd:
      yields[reg][sel] = Yields(samples, ['qcd'], QCD[reg][sel], cutOpt = "combinedList", weight = "weight", pklOpt = False, tableName = reg + "_" + sel, nDigits = 2, err = True, verbose = True, nSpaces = 10)
  
   QCDexp[reg] = (yields[reg]['IM_A'].yieldDictFull['qcd']['QCD_IM_A_' + reg] * yields[reg]['A_IM'].yieldDictFull['qcd']['QCD_A_IM_' + reg]/\
   yields[reg]['IMA'].yieldDictFull['qcd']['QCD_IMA_' + reg])
   
   print makeLine()
   print "nIM_A = ", yields[reg]['IM_A'].yieldDictFull['qcd']['QCD_IM_A_' + reg], " | nA_IM = ", yields[reg]['A_IM'].yieldDictFull['qcd']['QCD_A_IM_' + reg],\
         " | nIMA = ", yields[reg]['IMA'].yieldDictFull['qcd']['QCD_IMA_' + reg]
   print "QCD Estimation in ", reg, ": ", QCDexp[reg]
   print "QCD MC yield in ", reg, ": ", yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg]
   print makeLine()
  
   with open(savedir + "/QCDyields" + suffix + ".txt", "a") as outfile:
         outfile.write(reg + "     " +\
         str(yields[reg]['IM_A'].yieldDictFull[qcd]['QCD_IM_A_' + reg]) + "             " +\
         str(yields[reg]['A_IM'].yieldDictFull[qcd]['QCD_A_IM_' + reg]) + "             " +\
         str(yields[reg]['IMA'].yieldDictFull[qcd]['QCD_IMA_' + reg]) + "             " +\
         str(QCDexp[reg].round(2)) + "             " +\
         str(yields[reg]['SR'].yieldDictFull[qcd]['QCD_SR_' + reg]) + "             ")
         if yields[reg]['SR'].yieldDictFull[qcd]['QCD_SR_' + reg].val:
            outfile.write(str((QCDexp[reg]/yields[reg]['SR'].yieldDictFull[qcd]['QCD_SR_' + reg]).round(2))  + "\n")
         else:
            outfile.write("\n")
