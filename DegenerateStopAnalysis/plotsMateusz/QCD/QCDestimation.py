# QCDestimation.py
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
from Workspace.DegenerateStopAnalysis.toolsMateusz.degTools import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.cutsEle import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.cmgTuplesPostProcessed_mAODv2_analysisHephy13TeV import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_mAODv2_analysisHephy13TeV import getSamples
#from Workspace.DegenerateStopAnalysis.toolsMateusz.cmgTuplesPostProcessed_mAODv2 import cmgTuplesPostProcessed
#from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_analysisHephy_13TeV import getSamples
#from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_PP_mAODv2_7412pass2_scan import getSamples

from array import array
from math import pi, sqrt #cos, sin, sinh, log

ROOT.setTDRStyle(1)
ROOT.gStyle.SetOptStat(0) #1111 #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--ABCD", dest = "ABCD",  help = "ABCD method", type = str, default = "4")
parser.add_argument("--MET", dest = "MET",  help = "MET Cut", type = str, default = "200")
parser.add_argument("--HT", dest = "HT",  help = "HT Cut", type = str, default = "200")
parser.add_argument("--METloose", dest = "METloose",  help = "Loose MET Cut", type = str, default = "200")
parser.add_argument("--eleWP", dest = "eleWP",  help = "Electron WP", type = str, default = "Veto")
parser.add_argument("--removedCut", dest = "removedCut",  help = "Variable removed from electron ID", type = str, default = "None") #"sigmaEtaEta" "hOverE" "ooEmooP" "dEta" "dPhi" "d0" "dz" "MissingHits" "convVeto"
parser.add_argument("--enriched", dest = "enriched",  help = "EM enriched QCD?", type = bool, default = False)
parser.add_argument("--plot", dest = "plot",  help = "Toggle plot", type = int, default = 0)
parser.add_argument("--save", dest = "save",  help = "Toggle save", type = int, default = 1)
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
enriched = args.enriched
plot = args.plot
save = args.save

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD/ABCD" + ABCD + "/estimation/"
   if ABCD == 3:
      if removedCut == "None": savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD3/estimation/" + eleWP 
      else: savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD3/estimation/" + eleWP + "_no_" + removedCut
   if not os.path.exists(savedir): os.makedirs(savedir)

#Samples
if enriched == True: qcd = "qcdem"
else: qcd = "qcd"

privateSignals = ["s10FS", "s30", "s30FS", "s60FS", "t2tt30FS"]
backgrounds = ["w","tt", "z", "qcd"]

cmgPP = cmgTuplesPostProcessed()#mc_path, signal_path, data_path)

samplesList = backgrounds # + privateSignals
samples = getSamples(cmgPP = cmgPP, skim = 'presel', sampleList = samplesList, scan = False, useHT = True, getData = False) 

officialSignals = ["s300_290", "s300_270", "s300_250"] #FIXME: crosscheck if these are in allOfficialSignals

allOfficialSignals = samples.massScanList()
allSignals = privateSignals + allOfficialSignals
allSamples = allSignals + backgrounds

#selectedSamples = privateSignals + officialSignals + backgrounds
selectedSamples = ["qcd", "z", "tt", "w"]

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
   
suffix = "_" + eleWP + "_HT" + HTcut + "_MET" + METcut
if ABCD == "3": suffix += "_METloose" + METloose
if enriched == True: suffix += "_EMenriched"

print makeDoubleLine()
print "Performing ABCD" + ABCD + " QCD estimation."
print makeDoubleLine()

collection = "LepAll" 
print makeLine()
print "Using " + collection + " collection."
print makeLine()

#Gets all cuts (electron, SR, CR) for given electron ID
if ABCD == "1" or ABCD == "2": eleIDsel = electronIDs(ID = "nMinus1", removedCut = "d0", iso = False, collection = collection)
elif ABCD == "3":              
   if removedCut == "None":    eleIDsel = electronIDs(ID = "manual", removedCut = "None", iso = False, collection = collection)
   else:                       eleIDsel = electronIDs(ID = "nMinus1", removedCut = removedCut, iso = False, collection = collection)
elif ABCD == "4":              eleIDsel = electronIDs(ID = "nMinus1", removedCut = "sigmaEtaEta", iso = False, collection = collection)

#Geometric cuts
etaAcc = 2.1
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap

eleSel = "abs(LepAll_pdgId) == 11 && abs(LepAll_eta) < " + str(etaAcc) + " && " + eleIDsel[eleWP]

#Common QCD cuts
hybIsoCut = "(LepAll_relIso03*min(LepAll_pt, 25)) < 5" #hybIsoCut = "((LepAll_absIso03 < 5) || LepAll_relIso03 < 0.2))"
antiHybIsoCut = "(LepAll_relIso03*min(LepAll_pt, 25)) > 5" #antiHybIsoCut = "((LepAll_absIso03 > 5) && (LepAll_relIso03 > 0.2))"
dPhiCut = "vetoJet_dPhi_j1j2 < 2.5"
antidPhiCut = "vetoJet_dPhi_j1j2 > 2.5"

#Differing QCD cuts
geoSel= {\
      'EB':"(abs(LepAll_eta) <= " + str(ebeeSplit) + ")", 
      'EE':"(abs(LepAll_eta) > " + str(ebeeSplit) + " && abs(LepAll_eta) < " + str(etaAcc) + ")"}

if ABCD == "1" or ABCD == "2": #dxy oriented
   #dxyCuts = {\
   #      'Veto':{'EB':0.0564, 'EE':0.222},
   #      'Loose':{'EB':0.0261, 'EE':0.118},
   #      'Medium':{'EB':0.0118, 'EE':0.0739},
   #      'Tight':{'EB':0.0111, 'EE':0.0351}}
   #
   #dxyCut = "(" + combineCuts(geoSel['EB'], "LepAll_dxy <" + str(dxyCuts[eleWP]['EB'])) + ") || (" + combineCuts(geoSel['EE'], "LepAll_dxy <" + str(dxyCuts[eleWP]['EE'])) + ")"
   dxyCut = "abs(LepAll_dxy) < 0.02"
   appliedCut = dxyCut

   if ABCD == "1": #ABCD1
      
      #antiDxyCut = "(" + combineCuts(geoSel['EB'], "LepAll_dxy >" + str(dxyCuts[eleWP]['EB'])) + ") || (" + combineCuts(geoSel['EE'], "LepAll_dxy >" + str(dxyCuts[eleWP]['EE'])) + ")"
      antiDxyCut = "abs(LepAll_dxy) > 0.02"
      invertedCut = antiDxyCut
   
   elif ABCD == "2": #ABCD2
      looseDxyCut = "abs(LepAll_dxy) < 0.05"
      invertedCut = looseDxyCut # NOTE: loosened rather than inverted

elif ABCD == "4": #ABCD4
   
   sigmaEtaEtaCuts = {\
      'Veto':{'EB':0.0114, 'EE':0.0352},
      'Loose':{'EB':0.0103, 'EE':0.0301},
      'Medium':{'EB':0.0101, 'EE':0.0283},
      'Tight':{'EB':0.0101, 'EE':0.0279}}
   
   sigmaEtaEtaCut = "(" + combineCuts(geoSel['EB'], "LepAll_sigmaIEtaIEta <" + str(sigmaEtaEtaCuts[eleWP]['EB'])) + ") || (" + combineCuts(geoSel['EE'], "LepAll_sigmaIEtaIEta <" + str(sigmaEtaEtaCuts[eleWP]['EE'])) + ")"
   antiSigmaEtaEtaCut = "(" + combineCuts(geoSel['EB'], "LepAll_sigmaIEtaIEta >" + str(sigmaEtaEtaCuts[eleWP]['EB'])) + ") || (" + combineCuts(geoSel['EE'], "LepAll_sigmaIEtaIEta >" + str(sigmaEtaEtaCuts[eleWP]['EE'])) + ")"

   appliedCut = sigmaEtaEtaCut
   invertedCut = antiSigmaEtaEtaCut

variables = {'elePt':["LepAll_pt",{}], 'eleMt':["LepAll_mt", {}]}

if plot: variables.update({'relIso':{}})

#Redefining variables in terms of electron selection
# ABCD1: X = D (inverted) | ABCD2: X = D (loose) | ABCD3: X = M (loose) | ABCD4: X = S (inverted)
Xs = {'1':'D', '2':'D', '3':'M', '4':'S'}

for var in variables:
   if ABCD == "1" or ABCD == "2" or ABCD == "4":
      variables[var][1]['SR'] = varSel(variables[var][0], combineCutsList([eleSel, hybIsoCut, appliedCut])) 
      variables[var][1]['X_I'] = varSel(variables[var][0], combineCutsList([eleSel, hybIsoCut, invertedCut])) 
      variables[var][1]['I_X'] = varSel(variables[var][0], combineCutsList([eleSel, antiHybIsoCut, appliedCut])) 
      variables[var][1]['IX'] = varSel(variables[var][0], combineCutsList([eleSel, antiHybIsoCut, invertedCut])) 
   if ABCD == "3":
      variables[var][1]['I'] = varSel(variables[var][0], combineCutsList([eleSel, hybIsoCut])) 
      variables[var][1]['anti-I'] = varSel(variables[var][0], combineCutsList([eleSel, antiHybIsoCut])) 

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

for sel in abcd.values(): 
   SRs[sel] = {\
      'SR1':["SR1", variables['elePt'][1][sel] + " < 30"],
      'SR1a':["SR1a", combineCuts(variables['eleMt'][1][sel] + " < 60", variables['elePt'][1][sel] + " < 30")],
      'SR1b':["SR1b", combineCuts(btw(variables['eleMt'][1][sel], 60, 88), variables['elePt'][1][sel] + " < 30")],
      'SR1c':["SR1c", combineCuts(variables['eleMt'][1][sel] + " > 88", variables['elePt'][1][sel] + " < 30")],
      
      'SRL1a':["SRL1a", combineCuts(variables['eleMt'][1][sel] + " < 60", btw(variables['elePt'][1][sel], 5, 12))],
      'SRH1a':["SRH1a", combineCuts(variables['eleMt'][1][sel] + " < 60", btw(variables['elePt'][1][sel], 12, 20))],
      'SRV1a':["SRV1a", combineCuts(variables['eleMt'][1][sel] + " < 60", btw(variables['elePt'][1][sel], 20, 30))],
      
      'SRL1b':["SRL1b", combineCuts(btw(variables['eleMt'][1][sel], 60, 88), btw(variables['elePt'][1][sel], 5, 12))],
      'SRH1b':["SRH1b", combineCuts(btw(variables['eleMt'][1][sel], 60, 88), btw(variables['elePt'][1][sel], 12, 20))],
      'SRV1b':["SRV1b", combineCuts(btw(variables['eleMt'][1][sel], 60, 88), btw(variables['elePt'][1][sel], 20, 30))],
      
      'SRL1c':["SRL1c", combineCuts(variables['eleMt'][1][sel] + " > 88", btw(variables['elePt'][1][sel], 5, 12))],
      'SRH1c':["SRH1c", combineCuts(variables['eleMt'][1][sel] + " > 88", btw(variables['elePt'][1][sel], 12, 20))],
      'SRV1c':["SRV1c", combineCuts(variables['eleMt'][1][sel] + " > 88", btw(variables['elePt'][1][sel], 20, 30))]
   }

QCD = {}

regions = ['SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']

for reg in regions:
   QCD[reg] = {}

   if ABCD == "1" or ABCD == "2" or ABCD == "4":
      QCD[reg]['SR'] = CutClass("QCD_SR_" + reg, [
         SRs['SR'][reg],
         ["A", dPhiCut], #applied
         ["IX", sumSel1(combineCuts(eleSel, hybIsoCut, appliedCut))],
         ], baseCut = presel)
      
      QCD[reg]['IX_A'] = CutClass("QCD_IX_A_" + reg, [
         SRs['IX'][reg],
         ["A", dPhiCut], #applied
         ["anti-IX", sumSel1(combineCuts(eleSel, antiHybIsoCut, invertedCut))], #inverted, inverted (loose)
         ], baseCut = presel)
      
      
      QCD[reg]['IXA'] = CutClass("QCD_IXA_" + reg, [
         SRs['IX'][reg],
         ["anti-A", antidPhiCut], #inverted
         ["anti-IX", sumSel1(combineCuts(eleSel, antiHybIsoCut, invertedCut))], #inverted, inverted
         ], baseCut = presel)

      if ABCD == "1" or ABCD == "4":
      
         QCD[reg]['XA_I'] = CutClass("QCD_XA_I_" + reg, [
            SRs['X_I'][reg],
            ["anti-A", antidPhiCut], #inverted
            ["I+anti-X", sumSel1(combineCuts(eleSel, hybIsoCut, invertedCut))], #applied, inverted
            ], baseCut = presel)
      
         QCD[reg]['IA_X'] = CutClass("QCD_IA_X_" + reg, [
            SRs['I_X'][reg],
            ["anti-A", antidPhiCut], #inverted
            ["anti-I+X", sumSel1(combineCuts(eleSel, antiHybIsoCut, appliedCut))], #inverted, applied
            ], baseCut = presel)

      elif ABCD == "2": 
         QCD[reg]['A_IX'] = CutClass("QCD_A_IX_" + reg, [
            SRs['SR'][reg],
            ["anti-A", antidPhiCut], #inverted
            ["IX", sumSel1(combineCuts(eleSel, hybIsoCut, appliedCut))], #applied, applied
            ], baseCut = presel)
    
   elif ABCD == "3": #loosened MET
      QCD[reg]['SR'] = CutClass("QCD_SR_" + reg, [
         SRs['I'][reg],
         ["MET", "met >" + METcut], #tight MET
         ["A", dPhiCut], #applied
         ["I", sumSel1(combineCuts(eleSel, hybIsoCut))],
         ], baseCut = presel)
   
      QCD[reg]['IX_A'] = CutClass("QCD_IX_A_" + reg, [ #loose MET
         SRs['anti-I'][reg],
         ["A", dPhiCut], #applied
         ["anti-I", sumSel1(combineCuts(eleSel, antiHybIsoCut))], #inverted
         ], baseCut = presel)
   
      QCD[reg]['A_IX'] = CutClass("QCD_A_IX_" + reg, [
         SRs['I'][reg],
         ["MET", "met >" + METcut], #tight MET
         ["anti-A", antidPhiCut], #inverted
         ["I", sumSel1(combineCuts(eleSel, hybIsoCut))], #applied, inverted
         ], baseCut = presel)
   
      QCD[reg]['IXA'] = CutClass("QCD_IXA_" + reg, [ #loose MET
         SRs['anti-I'][reg],
         ["anti-A", antidPhiCut], #inverted
         ["anti-I", sumSel1(combineCuts(eleSel, antiHybIsoCut))], #inverted, inverted
         ], baseCut = presel)
 
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
