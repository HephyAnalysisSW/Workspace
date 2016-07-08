# QCDestimation_index.py
# Combined script for the QCD estimation using 4 various ABCD methods:
# ABCD1: 3D ABCD with IDA (inverted dxy)
# ABCD2: 2D ABCD with loosened D
# ABCD3: 2D ABCD with loosened MET
# ABCD4: 3D ABCD with ISA (inverted simgaEtaEta)

import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.navidTools.NavidTools import Plots, getPlots, drawPlots, Yields, setup_style
from Workspace.DegenerateStopAnalysis.toolsMateusz.cutsEle import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.cmgTuplesPostProcessed_mAODv2_analysisHephy13TeV import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_mAODv2_analysisHephy13TeV import getSamples
#from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_analysisHephy_13TeV import getSamples
#from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_PP_mAODv2_7412pass2_scan import getSamples

from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Sets TDR style
setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--ABCD", dest = "ABCD",  help = "ABCD method", type = str, default = "4")
parser.add_argument("--MET", dest = "MET",  help = "MET Cut", type = str, default = "200")
parser.add_argument("--HT", dest = "HT",  help = "HT Cut", type = str, default = "200")
parser.add_argument("--METloose", dest = "METloose",  help = "Loose MET Cut", type = str, default = "200")
parser.add_argument("--eleWP", dest = "eleWP",  help = "Electron WP", type = str, default = "Veto")
parser.add_argument("--removedCut", dest = "removedCut",  help = "Variable removed from electron ID", type = str, default = "None") #"sigmaEtaEta" "hOverE" "ooEmooP" "dEta" "dPhi" "d0" "dz" "MissingHits" "convVeto"
parser.add_argument("--highWeightVeto", dest = "highWeightVeto",  help = "Remove high weighted events", type = bool, default = False)
parser.add_argument("--enriched", dest = "enriched",  help = "EM enriched QCD?", type = bool, default = False)
parser.add_argument("--estimation", dest = "estimation",  help = "Toggle estimation", type = int, default = 1)
parser.add_argument("--getData", dest = "getData",  help = "Get data samples", type = int, default = 1)
parser.add_argument("--plot", dest = "plot",  help = "Toggle plot", type = int, default = 0)
parser.add_argument("--logy", dest = "logy",  help = "Toggle logy", type = int, default = 0)
parser.add_argument("--save", dest = "save",  help = "Toggle save", type = int, default = 1)
parser.add_argument("--new", dest = "new",  help = "New", type = int, default = 0)
parser.add_argument("-b", dest = "batch",  help = "Batch mode", action = "store_true", default = False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
ABCD = args.ABCD
METcut = args.MET
METloose = args.METloose
HTcut = args.HT
eleWP = args.eleWP
removedCut = args.removedCut
highWeightVeto = args.highWeightVeto
enriched = args.enriched
estimation = args.estimation
getData = args.getData
plot = args.plot
logy = args.logy
save = args.save
new = args.new

print makeDoubleLine()
print "Performing ABCD" + ABCD + " QCD estimation."
print makeDoubleLine()

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   if removedCut == "None": savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD/ABCD" + ABCD + "/estimation/" + eleWP 
   else: savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD/ABCD" + ABCD + "/estimation/" + eleWP + "_no_" + removedCut
   if highWeightVeto: savedir += "/highWeightVeto" 
   if not os.path.exists(savedir): os.makedirs(savedir)

suffix = "_" + eleWP + "_HT" + HTcut + "_MET" + METcut
if ABCD == "3": suffix += "_METloose" + METloose
if enriched == True: suffix += "_EMenriched"

suffix += "_index"

#Samples
if enriched == True: qcd = "qcdem"
else: qcd = "qcd"

cmgPP = cmgTuplesPostProcessed()#mc_path, signal_path, data_path)

samplesList = ["qcd"]

if plot: samplesList.extend(["w", "tt", "z"])

if getData: samplesList.append("dblind")
samples = getSamples(cmgPP = cmgPP, skim = 'presel', sampleList = samplesList, scan = False, useHT = True, getData = getData) 

#officialSignals = ["s300_290", "s300_270", "s300_250"] #FIXME: crosscheck if these are in allOfficialSignals

#allOfficialSignals = samples.massScanList()
#allSignals = privateSignals + allOfficialSignals
#allSamples = allSignals + backgrounds

#selectedSamples = privateSignals + officialSignals + backgrounds
selectedSamples = samplesList #["qcd", "z", "tt", "w"]

##for s in samples.massScanList(): samples[s].weight = "weight" #removes ISR reweighting from official mass scan signal samples
#for s in samples: samples[s].tree.SetAlias("eleSel", allCuts[WP]['eleSel'])

print makeLine()
print "Using samples:"
newLine()
for s in selectedSamples:
   if s: print samples[s].name,":",s
   else: 
      print "!!! Sample " + sample + " unavailable."
      sys.exit(0)
   
collection = "LepAll" 
print makeLine()
print "Using " + collection + " collection."
print makeLine()

#Removal of high weight events
if highWeightVeto:
   weightCut = "50"
else:
   weightCut = "100000"

#Index of leading electron
ind = "IndexLepAll_el[0]"

#Gets all cuts (electron, SR, CR) for given electron ID
if ABCD == "1" or ABCD == "2": eleIDsel = electronIDsIndex(ID = "nMinus1", removedCut = "d0", iso = False, collection = collection)
elif ABCD == "3":              
   if removedCut == "None":    eleIDsel = electronIDsIndex(ID = "standard", removedCut = "None", iso = False, collection = collection)
   else:                       eleIDsel = electronIDsIndex(ID = "nMinus1", removedCut = removedCut, iso = False, collection = collection)
elif ABCD == "4":              eleIDsel = electronIDsIndex(ID = "nMinus1", removedCut = "sigmaEtaEta", iso = False, collection = collection)

#Geometric cuts
etaAcc = 2.1
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap

eleSel = "abs(LepAll_pdgId[" + ind + "]) == 11 && abs(LepAll_eta[" + ind + "]) < " + str(etaAcc) + " && " + eleIDsel[eleWP]

#Common QCD cuts
hybIsoCut = "(LepAll_relIso03[" + ind + "]*min(LepAll_pt[" + ind + "], 25)) < 5" #hybIsoCut = "((LepAll_absIso03 < 5) || LepAll_relIso03 < 0.2))"
antiHybIsoCut = "(LepAll_relIso03[" + ind + "]*min(LepAll_pt[" + ind + "], 25)) > 5" #antiHybIsoCut = "((LepAll_absIso03 > 5) && (LepAll_relIso03 > 0.2))"
dPhiCut = "vetoJet_dPhi_j1j2 < 2.5"
antidPhiCut = "vetoJet_dPhi_j1j2 > 2.5"

#Differing QCD cuts
geoSel= {\
      'EB':"(abs(LepAll_eta[" + ind + "]) <= " + str(ebeeSplit) + ")", 
      'EE':"(abs(LepAll_eta[" + ind + "]) > " + str(ebeeSplit) + " && abs(LepAll_eta[" + ind + "]) < " + str(etaAcc) + ")"}

if ABCD == "1" or ABCD == "2": #dxy oriented
   #dxyCuts = {\
   #      'Veto':{'EB':0.0564, 'EE':0.222},
   #      'Loose':{'EB':0.0261, 'EE':0.118},
   #      'Medium':{'EB':0.0118, 'EE':0.0739},
   #      'Tight':{'EB':0.0111, 'EE':0.0351}}
   
   #dxyCut = "(" + combineCuts(geoSel['EB'], "LepAll_dxy <" + str(dxyCuts[eleWP]['EB'])) + ") || (" + combineCuts(geoSel['EE'], "LepAll_dxy <" + str(dxyCuts[eleWP]['EE'])) + ")"
   dxyCut = "abs(LepAll_dxy[" + ind + "]) < 0.02"
   appliedCut = dxyCut

   if ABCD == "1": #ABCD1
      
      #antiDxyCut = "(" + combineCuts(geoSel['EB'], "LepAll_dxy >" + str(dxyCuts[eleWP]['EB'])) + ") || (" + combineCuts(geoSel['EE'], "LepAll_dxy >" + str(dxyCuts[eleWP]['EE'])) + ")"
      antiDxyCut = "abs(LepAll_dxy[" + ind + "]) > 0.02"
      invertedCut = antiDxyCut
   
   elif ABCD == "2": #ABCD2
      looseDxyCut = "abs(LepAll_dxy[" + ind + "]) < 0.05"
      invertedCut = looseDxyCut # NOTE: loosened rather than inverted

elif ABCD == "4": #ABCD4
   
   sigmaEtaEtaCuts = {\
      'Veto':{'EB':0.0114, 'EE':0.0352},
      'Loose':{'EB':0.0103, 'EE':0.0301},
      'Medium':{'EB':0.0101, 'EE':0.0283},
      'Tight':{'EB':0.0101, 'EE':0.0279}}
   
   sigmaEtaEtaCut = "(" + combineCuts(geoSel['EB'], "LepAll_sigmaIEtaIEta[" + ind + "] <" + str(sigmaEtaEtaCuts[eleWP]['EB'])) + ") || (" + combineCuts(geoSel['EE'], "LepAll_sigmaIEtaIEta[" + ind + "] <" + str(sigmaEtaEtaCuts[eleWP]['EE'])) + ")"
   antiSigmaEtaEtaCut = "(" + combineCuts(geoSel['EB'], "LepAll_sigmaIEtaIEta[" + ind + "] >" + str(sigmaEtaEtaCuts[eleWP]['EB'])) + ") || (" + combineCuts(geoSel['EE'], "LepAll_sigmaIEtaIEta[" + ind + "] >" + str(sigmaEtaEtaCuts[eleWP]['EE'])) + ")"

   appliedCut = sigmaEtaEtaCut
   invertedCut = antiSigmaEtaEtaCut

variables = {'elePt':"LepAll_pt[" + ind + "]", 'eleMt':"LepAll_mt[" + ind + "]"}

if plot: variables.update({"absIso":"LepAll_absIso03[" + ind + "]", 'relIso':"LepAll_relIso03[" + ind + "]", "hybIso":"(LepAll_relIso03[" + ind + "]*min(LepAll_pt[" + ind + "], 25))" ,  "absDxy":"LepAll_dxy[" + ind + "]" , "sigmaEtaEta":"LepAll_sigmaIEtaIEta[" + ind + "]"})

#Redefining variables in terms of electron selection
# ABCD1: X = D (inverted) | ABCD2: X = D (loose) | ABCD3: X = M (loose) | ABCD4: X = S (inverted)
Xs = {'1':'D', '2':'D', '3':'M', '4':'S'}

if ABCD == "3":
   MET = CutClass("MET", [["MET","met >" + METloose]], baseCut = None) #loosened MET cut for ABCD3
else:
   MET = CutClass("MET", [["MET","met >" + METcut]], baseCut = None)

#Preselection & basic SR cuts
presel = CutClass("presel_SR", [
   ["HT","ht_basJet >" + HTcut],
   ["ISR110", "nIsrJet >= 1"],
   ["No3rdJet60","nVetoJet <= 2"],
   ["BVeto","(nBSoftJet == 0 && nBHardJet == 0)"],
   ["HighWeightVeto","weight < " + weightCut],
   ["eleSel", "nLepAll_el > 0 &&" + eleSel],
   ], baseCut = MET)

# ABCD1: X = D (inverted) | ABCD2: X = D (loose) | ABCD3: X = M (loose) | ABCD4: X = S (inverted)
abcd = {'SR':'SR', 'IX_A':'IX', 'IXA':'IX'}

if ABCD == "1" or ABCD == "4": # 3D ABCD
   abcd['IA_X'] = 'I_X' 
   abcd['XA_I'] = 'X_I'
elif ABCD == "2": # 2D ABCD
   abcd['A_IX'] = 'SR'
elif ABCD == "3": # 2D ABCD
   abcd['SR'] = abcd['A_IX'] = 'I'
   abcd['IX_A'] = abcd['IXA'] = 'anti-I'

SRs ={}

SRs = {\
   'SR1':["SR1","LepAll_pt[" + ind + "] < 30"],
   'SR1a':["SR1a", combineCuts("LepAll_mt[" + ind + "] < 60", "LepAll_pt[" + ind + "] < 30")],
   'SR1b':["SR1b", combineCuts(btw("LepAll_mt[" + ind + "]", 60, 88), "LepAll_pt[" + ind + "] < 30")],
   'SR1c':["SR1c", combineCuts("LepAll_mt[" + ind + "] > 88", "LepAll_pt[" + ind + "] < 30")],

   'SRL1a':["SRL1a", combineCuts("LepAll_mt[" + ind + "] < 60", btw("LepAll_pt[" + ind + "]", 5, 12))],
   'SRH1a':["SRH1a", combineCuts("LepAll_mt[" + ind + "] < 60", btw("LepAll_pt[" + ind + "]", 12, 20))],
   'SRV1a':["SRV1a", combineCuts("LepAll_mt[" + ind + "] < 60", btw("LepAll_pt[" + ind + "]", 20, 30))],

   'SRL1b':["SRL1b", combineCuts(btw("LepAll_mt[" + ind + "]", 60, 95), btw("LepAll_pt[" + ind + "]", 5, 12))],
   'SRH1b':["SRH1b", combineCuts(btw("LepAll_mt[" + ind + "]", 60, 95), btw("LepAll_pt[" + ind + "]", 12, 20))],
   'SRV1b':["SRV1b", combineCuts(btw("LepAll_mt[" + ind + "]", 60, 95), btw("LepAll_pt[" + ind + "]", 20, 30))],

   'SRL1c':["SRL1c", combineCuts("LepAll_mt[" + ind + "] > 95", btw("LepAll_pt[" + ind + "]", 5, 12))],
   'SRH1c':["SRH1c", combineCuts("LepAll_mt[" + ind + "] > 95", btw("LepAll_pt[" + ind + "]", 12, 20))],
   'SRV1c':["SRV1c", combineCuts("LepAll_mt[" + ind + "] > 95", btw("LepAll_pt[" + ind + "]", 20, 30))]}

QCD = {}
regions = ['SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']

for reg in regions:
   QCD[reg] = {}

   if ABCD == "1" or ABCD == "2" or ABCD == "4":
      QCD[reg]['SR'] = CutClass("QCD_SR_" + reg, [
         SRs[reg],
         ["I", hybIsoCut], #applied
         ["X", appliedCut], #applied
         ["A", dPhiCut], #applied
         ], baseCut = presel)
      
      QCD[reg]['IX_A'] = CutClass("QCD_IX_A_" + reg, [
         SRs[reg],
         ["anti-I", antiHybIsoCut], #inverted,
         ["anti-X", invertedCut], #inverted (loose)
         ["A", dPhiCut], #applied
         ], baseCut = presel)
      
      QCD[reg]['IXA'] = CutClass("QCD_IXA_" + reg, [
         SRs[reg],
         ["anti-I", antiHybIsoCut], #inverted, 
         ["anti-X", invertedCut], #inverted (loose)
         ["anti-A", antidPhiCut], #inverted
         ], baseCut = presel)

      if ABCD == "1" or ABCD == "4":
      
         QCD[reg]['XA_I'] = CutClass("QCD_XA_I_" + reg, [
            SRs[reg],
            ["I", hybIsoCut], #applied
            ["anti-X", invertedCut], #inverted
            ["anti-A", antidPhiCut], #inverted
            ], baseCut = presel)
      
         QCD[reg]['IA_X'] = CutClass("QCD_IA_X_" + reg, [
            SRs[reg],
            ["anti-I", antiHybIsoCut], #inverted
            ["X", appliedCut], #applied
            ["anti-A", antidPhiCut], #inverted
            ], baseCut = presel)

      elif ABCD == "2": 
         QCD[reg]['A_IX'] = CutClass("QCD_A_IX_" + reg, [
            SRs[reg],
            ["I", hybIsoCut], #applied
            ["X", appliedCut], #applied
            ["anti-A", antidPhiCut], #inverted
            ], baseCut = presel)
    
   elif ABCD == "3": #loosened MET
      QCD[reg]['SR'] = CutClass("QCD_SR_" + reg, [
         SRs[reg],
         ["MET", "met >" + METcut], #tight MET
         ["A", dPhiCut], #applied
         ["I", hybIsoCut],
         ], baseCut = presel)
   
      QCD[reg]['IX_A'] = CutClass("QCD_IX_A_" + reg, [ #loose MET
         SRs[reg],
         ["A", dPhiCut], #applied
         ["anti-I", antiHybIsoCut], #inverted
         ], baseCut = presel)
   
      QCD[reg]['A_IX'] = CutClass("QCD_A_IX_" + reg, [
         SRs[reg],
         ["MET", "met >" + METcut], #tight MET
         ["anti-A", antidPhiCut], #inverted
         ["I", hybIsoCut], #applied
         ], baseCut = presel)
   
      QCD[reg]['IXA'] = CutClass("QCD_IXA_" + reg, [ #loose MET
         SRs[reg],
         ["anti-A", antidPhiCut], #inverted
         ["anti-I", antiHybIsoCut], #inverted
         ], baseCut = presel)

if estimation: 
   yields = {}
   QCDexp = {}
      
   if not os.path.isfile(savedir + "/QCDyields" + suffix + ".txt"):
      outfile = open(savedir + "/QCDyields" + suffix + ".txt", "w")
      outfile.write(eleWP + " Electron ID and Preselection of (MET, HT) > (" + METcut + "," + HTcut + ")\n")
      if ABCD == "1" or ABCD == "4": outfile.write("SR           IX_A                 XA_I                    IA_X                     IXA                       QCD                     MC                     Ratio\n".replace("X", Xs[ABCD]))
      elif ABCD == "2" or ABCD == "3": outfile.write("SR           IX_A                 A_IX                     IXA                       QCD                     MC                     Ratio\n".replace("X", Xs[ABCD]))
   
   for reg in regions:
      yields[reg] = {}
      for sel in abcd:
         yields[reg][sel] = Yields(samples, ['qcd'], QCD[reg][sel], cutOpt = "combinedList", weight = "weight", pklOpt = False, tableName = reg + "_" + sel, nDigits = 2, err = True, verbose = True, nSpaces = 10)
   
      if yields[reg]['IXA'].yieldDictFull['qcd']['QCD_IXA_' + reg].val:
         
         if ABCD == "1" or ABCD == "4": #3D ABCD
            
            QCDexp[reg] = (yields[reg]['IX_A'].yieldDictFull['qcd']['QCD_IX_A_' + reg] * yields[reg]['XA_I'].yieldDictFull['qcd']['QCD_XA_I_' + reg] * \
            yields[reg]['IA_X'].yieldDictFull['qcd']['QCD_IA_X_' + reg])/\
            (yields[reg]['IXA'].yieldDictFull['qcd']['QCD_IXA_' + reg] * yields[reg]['IXA'].yieldDictFull['qcd']['QCD_IXA_' + reg])
            
            print makeLine()
            print "nXA_I = ", yields[reg]['XA_I'].yieldDictFull['qcd']['QCD_XA_I_' + reg], " | nIA_X = ", yields[reg]['IA_X'].yieldDictFull['qcd']['QCD_IA_X_' + reg], " | ",\
                  "nIX_A = ", yields[reg]['IX_A'].yieldDictFull['qcd']['QCD_IX_A_' + reg], " | nIXA = ", yields[reg]['IXA'].yieldDictFull['qcd']['QCD_IXA_' + reg]
            print "QCD Estimation in ", reg, ": ", QCDexp[reg]
            print "QCD MC yield in ", reg, ": ", yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg]
            print makeLine()
            
            with open(savedir + "/QCDyields" + suffix + ".txt", "a") as outfile:
               outfile.write(reg + "     " +\
               str(yields[reg]['IX_A'].yieldDictFull['qcd']['QCD_IX_A_' + reg].round(2)) + "             " +\
               str(yields[reg]['XA_I'].yieldDictFull['qcd']['QCD_XA_I_' + reg].round(2)) + "             " +\
               str(yields[reg]['IA_X'].yieldDictFull['qcd']['QCD_IA_X_' + reg].round(2)) + "             " +\
               str(yields[reg]['IXA'].yieldDictFull['qcd']['QCD_IXA_' + reg].round(2)) + "             " +\
               str(QCDexp[reg].round(2)) + "             " +\
               str(yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg].round(2)) + "             ")
               if yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg].val:
                  outfile.write(str((QCDexp[reg]/yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg]).round(2)) + "\n")
               else:
                  outfile.write("\n")
         
         elif ABCD == "2" or ABCD == "3": #2D ABCD
        
            QCDexp[reg] = (yields[reg]['IX_A'].yieldDictFull[qcd]['QCD_IX_A_' + reg] * yields[reg]['A_IX'].yieldDictFull[qcd]['QCD_A_IX_' + reg]/\
            yields[reg]['IXA'].yieldDictFull[qcd]['QCD_IXA_' + reg])
   
            print makeLine()
            print "nIX_A = ", yields[reg]['IX_A'].yieldDictFull[qcd]['QCD_IX_A_' + reg], " | nA_IX = ", yields[reg]['A_IX'].yieldDictFull[qcd]['QCD_A_IX_' + reg],\
                  " | nIXA = ", yields[reg]['IXA'].yieldDictFull[qcd]['QCD_IXA_' + reg]
            print "QCD Estimation in ", reg, ": ", QCDexp[reg]
            print "QCD MC yield in ", reg, ": ", yields[reg]['SR'].yieldDictFull[qcd]['QCD_SR_' + reg]
            print makeLine()
   
            with open(savedir + "/QCDyields" + suffix + ".txt", "a") as outfile:
               outfile.write(reg + "     " +\
               str(yields[reg]['IX_A'].yieldDictFull['qcd']['QCD_IX_A_' + reg].round(2)) + "             " +\
               str(yields[reg]['A_IX'].yieldDictFull['qcd']['QCD_A_IX_' + reg].round(2)) + "             " +\
               str(yields[reg]['IXA'].yieldDictFull['qcd']['QCD_IXA_' + reg].round(2)) + "             " +\
               str(QCDexp[reg].round(2)) + "             " +\
               str(yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg].round(2)) + "             ")
               if yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg].val:
                  outfile.write(str((QCDexp[reg]/yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg]).round(2)) + "\n")
               else:
                  outfile.write("\n")

if plot:
   
   if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
      if removedCut == "None": plotdir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD/ABCD" + ABCD + "/plots/" + eleWP
      else: plotdir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD3/plots/" + eleWP + "_no_" + removedCut
     
      if getData: plotdir += "/data"
      
      plotdir += "/HT" + HTcut + "MET" + METcut
      
      if highWeightVeto: plotdir += "/highWeightVeto"
      if enriched == True: plotdir += "_EMenriched"
      if not os.path.exists(plotdir): os.makedirs(plotdir)

      QCD['SR1']['I_A'] = CutClass("QCD_I_A_SR1", [
         SRs['SR1'],
         ["A", dPhiCut], #applied
         ["anti-I", antiHybIsoCut], #inverted
         ], baseCut = presel)
      
      QCD['SR1']['IA'] = CutClass("QCD_IA_SR1", [
         SRs['SR1'],
         ["anti-A", antidPhiCut], #inverted
         ["anti-I", antiHybIsoCut], #inverted
         ], baseCut = presel)

      if ABCD != "3":
         QCD['SR1']['A_I'] = CutClass("QCD_A_I_SR1", [
            SRs['SR1'],
            ["anti-A", antidPhiCut], #inverted
            ["I", hybIsoCut], #applied
            ], baseCut = presel)
      elif ABCD == "3":
         QCD['SR1']['A_I'] = CutClass("QCD_A_I_SR1", [
            SRs['SR1'],
            ["MET", "met >" + METcut], #tight MET
            ["anti-A", antidPhiCut], #inverted
            ["I", hybIsoCut], #applied
            ], baseCut = presel)
   
   plotsList = {}
   plotDict = {}
   plotsDict = {}
   plots = {}
   plots2 = {}
   
   plotSamples = [qcd, "z", "tt", "w"]
   plotRegions = {'I_A':'anti-I', 'IA':'anti-I', 'A_I':'I'}
   plotRegions.update(abcd) 
  
   if getData:
      del plotRegions['SR']
      plotSamples.append("dblind")
   
   for sel in plotRegions:
      plotDict[sel] = {\
         "elePt_" + sel:{'var':variables['elePt'], "bins":[10, 0, 50], "decor":{"title": "Electron pT Plot" ,"x":"Electron p_{T} / GeV" , "y":"Events", 'log':[0, logy,0]}},
         "absIso_" + sel:{'var':variables['absIso'], "bins":[4, 0, 20], "decor":{"title": "Electron absIso Plot" ,"x":"I_{abs} / GeV" , "y":"Events", 'log':[0,logy,0]}},
         "relIso_" + sel:{'var':variables['relIso'], "bins":[20, 0, 5], "decor":{"title": "Electron relIso Plot" ,"x":"I_{rel}" , "y":"Events", 'log':[0,logy,0]}},
         "hybIso_" + sel:{'var':variables['hybIso'], "bins":[10, 0, 25], "decor":{"title": "Electron hybIso Plot" ,"x":"HI = I_{rel}*min(p_{T}, 25 GeV)" , "y":"Events", 'log':[0,logy,0]}},
         "hybIso2_" + sel:{'var':"(log(1 + " + variables['hybIso'] + ")/log(1+5))", "bins":[8, 0, 4], "decor":{"title": "Electron hybIso Plot" ,"x":"log(1+HI)/log(1+5)" , "y":"Events", 'log':[0,logy,0]}},
         "absDxy_" + sel:{'var':variables['absDxy'], "bins":[4, 0, 0.04], "decor":{"title": "Electron |dxy| Plot" ,"x":"|dxy|" , "y":"Events", "log":[0,logy,0]}},
         "delPhi_" + sel:{'var':"vetoJet_dPhi_j1j2", "bins":[8, 0, 3.14], "decor":{"title": "deltaPhi(j1,j2) Plot" ,"x":"#Delta#phi(j1,j2)" , "y":"Events", 'log':[0,logy,0]}},
         "eleMt_" + sel:{'var':variables['eleMt'], "bins":[10,0,100], "decor":{"title": "mT Plot" ,"x":"m_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
         "MET_" + sel:{'var':"met", "bins":[50,0,500], "decor":{"title": "MET Plot" ,"x":"Missing E_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
         "HT_" + sel:{'var':"ht_basJet", "bins":[50,0,500], "decor":{"title": "HT Plot","x":"H_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
         "sigmaEtaEta_" + sel:{'var':variables['sigmaEtaEta'], "bins":[5,0,0.05], "decor":{"title": "#sigma#eta#eta Plot","x":"#sigma#eta#eta" , "y":"Events", 'log':[0,logy,0]}},
         "weight_" + sel:{'var':"weight", "bins":[20,0,400], "decor":{"title": "Weight Plot","x":"Event Weight" , "y":"Events", 'log':[0,1,0]}}
      }
   
      plotsList[sel] = ["elePt_" + sel, "absIso_" + sel, "relIso_" + sel,"hybIso_" + sel, "hybIso2_" + sel, "absDxy_" + sel, "delPhi_" + sel, "eleMt_" + sel, "MET_" + sel, "HT_" + sel, "sigmaEtaEta_" + sel, "weight_" + sel]
      #plotsList[sel] = ["hybIso2_" + sel, "absDxy_" + sel, "delPhi_" + sel, "sigmaEtaEta_" + sel, "weight_" + sel]
      #plotsList[sel] = ["hybIso2_" + sel, "absDxy_" + sel, "delPhi_" + sel]
      plotsDict[sel] = Plots(**plotDict[sel])
      plots[sel] = getPlots(samples, plotsDict[sel], QCD['SR1'][sel], plotSamples, plotList = plotsList[sel], addOverFlowBin='upper')
      if getData: plots2[sel] = drawPlots(samples, plotsDict[sel], QCD['SR1'][sel], plotSamples, plotList = plotsList[sel], denoms=["bkg"], noms = ["dblind"], fom="RATIO", fomLimits=[0,2.8], plotMin = 0.1, normalize = False, save=False)
      else: plots2[sel] = drawPlots(samples, plotsDict[sel], QCD['SR1'][sel], plotSamples, plotList = plotsList[sel], plotMin = 0.1, normalize = False, save=False)
 
      #Save canvas
      if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
         if not os.path.exists("%s/%s/root"%(plotdir, sel)): os.makedirs("%s/%s/root"%(plotdir, sel))
         if not os.path.exists("%s/%s/pdf"%(plotdir, sel)): os.makedirs("%s/%s/pdf"%(plotdir, sel))
   
         for canv in plots2[sel]['canvs']:
            #if plot['canvs'][canv][0]:
            plots2[sel]['canvs'][canv][0].SaveAs("%s/%s/%s%s.png"%(plotdir, sel, canv, suffix))
            plots2[sel]['canvs'][canv][0].SaveAs("%s/%s/root/%s%s.root"%(plotdir, sel, canv, suffix))
            plots2[sel]['canvs'][canv][0].SaveAs("%s/%s/pdf/%s%s.pdf"%(plotdir, sel, canv, suffix))
