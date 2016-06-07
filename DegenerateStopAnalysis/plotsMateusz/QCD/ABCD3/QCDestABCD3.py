#QCDestABCD3.py
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
parser.add_argument("--MET", dest = "MET",  help = "MET Cut", type = str, default = "300")
parser.add_argument("--HT", dest = "HT",  help = "HT Cut", type = str, default = "300")
parser.add_argument("--METloose", dest = "METloose",  help = "Loose MET Cut", type = str, default = "250")
parser.add_argument("--eleWP", dest = "eleWP",  help = "Electron WP", type = str, default = "Veto")
parser.add_argument("--removedCut", dest = "removedCut",  help = "Variable removed from electron ID", type = str, default = "None") #"sigmaEtaEta" "hOverE" "ooEmooP" "dEta" "dPhi" "d0" "dz" "MissingHits" "convVeto"
parser.add_argument("--enriched", dest = "enriched",  help = "EM enriched QCD?", type = bool, default = False)
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
METcut = args.MET
METloose = args.METloose
HTcut = args.HT
eleWP = args.eleWP
removedCut = args.removedCut
enriched = args.enriched
save = args.save

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   if removedCut == "None": savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD3/estimation/" + eleWP + "/HT" + HTcut
   else: savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD3/estimation/" + eleWP + "_no_" + removedCut + "/HT" + HTcut
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
   
suffix = "_HT" + HTcut + "_MET" + METcut + "_METloose" + METloose
if enriched == True: suffix += "_EMenriched"

QCDcuts = {}
 
#if collection == "LepGood": otherCollection = "LepOther"
#elif collection == "LepOther": otherCollection = "LepGood"

print makeLine()
print "Using LepAll collection."
#print "Ignoring " + otherCollection + " collection."
print makeLine()

#Gets all cuts (electron, SR, CR) for given electron ID
#eleIDsel = electronIDs(ID = "nMinus1", removedCut = removedCut, iso = False, collection = "LepAll")
eleIDsel = electronIDs(ID = "manual", removedCut = "None", iso = False, collection = "LepAll")
#eleIDsel = electronIDs(ID = "nMinus1", removedCut = "d0", iso = False, collection = "LepAll")

##for s in samples.massScanList(): samples[s].weight = "weight" #removes ISR reweighting from official mass scan signal samples
#for s in samples: samples[s].tree.SetAlias("eleSel", allCuts[WP]['eleSel'])

etaAcc = 2.1
eleSel = "abs(LepAll_pdgId) == 11 && abs(LepAll_eta) < " + str(etaAcc) + " && " + eleIDsel[eleWP]
#eleSel_other = "abs(" + otherCollection + "_pdgId) == 11 && abs(" + otherCollection + "_eta) < " + str(etaAcc) + " && " + eleIDsel_other['Veto']

#Cuts
#dxyCut = "abs(LepAll_dxy) < 0.02"
#looseDxyCut = "abs(LepAll_dxy) < 0.05"

hybIsoCut = "(LepAll_relIso03*min(LepAll_pt, 25)) < 5"
antiHybIsoCut = "(LepAll_relIso03*min(LepAll_pt, 25)) > 5"
#hybIsoCut = "((LepAll_absIso03 < 5) || LepAll_relIso03 < 0.2))"
#antiHybIsoCut = "((LepAll_absIso03 > 5) && (LepAll_relIso03 > 0.2))"
   
elePt = {}
elePt['I'] = "Max$(LepAll_pt*(" + eleSel + "&&" + hybIsoCut + "))"
elePt['anti-I'] = "Max$(LepAll_pt*(" + eleSel + "&&" + antiHybIsoCut + "))"

eleMt = {}
eleMt['I'] = "Max$(LepAll_mt*(" + eleSel + "&&" + hybIsoCut + "))"
eleMt['anti-I'] = "Max$(LepAll_mt*(" + eleSel + "&&" + antiHybIsoCut + "))"

presel = CutClass("presel_SR", [
   ["METloose","met >" + METloose], #looser MET for B & D regions
   ["HT","ht_basJet >" + HTcut],
   ["ISR110", "nIsrJet >= 1"],
   ["No3rdJet60","nVetoJet <= 2"],
   ["BVeto","(nBSoftJet == 0 && nBHardJet == 0)"],
   ["eleSel", "Sum$(" + eleSel + ") == 1"],
   #["otherCollection", "Sum$(" + eleSel_other + ") == 0"],
   #["elePt<30", elePt + " < 30"],
   #["anti-AntiQCD", "vetoJet_dPhi_j1j2 > 2.5"],
   #["anti-HybIso", "Sum$(" + eleSel + "&&" + antiHybIsoCut + ") == 1"],
   #["anti-dxy", "Max$(abs(" + lep + "_dxy*(" + eleSel + "&&" + antiHybIsoCut + "))) > 0.02"],
   ], baseCut = None) #allCuts['None']['presel'])

SRs ={}

for reg in ['I', 'anti-I']:
   SRs[reg] = {\
      'SR1':["SR1","1"],
      'SR1a':["SR1a", eleMt[reg] + " < 60"],
      'SR1b':["SR1b", btw(eleMt[reg], 60, 88)],
      'SR1c':["SR1c", eleMt[reg] + " > 88"],
      
      'SRL1a':["SRL1a", joinCutStrings([eleMt[reg] + " < 60", btw(elePt[reg], 5, 12)])],
      'SRH1a':["SRH1a", joinCutStrings([eleMt[reg] + " < 60", btw(elePt[reg], 12, 20)])],
      'SRV1a':["SRV1a", joinCutStrings([eleMt[reg] + " < 60", btw(elePt[reg], 20, 30)])],
      
      'SRL1b':["SRL1b", joinCutStrings([btw(eleMt[reg], 60, 88), btw(elePt[reg], 5, 12)])],
      'SRH1b':["SRH1b", joinCutStrings([btw(eleMt[reg], 60, 88), btw(elePt[reg], 12, 20)])],
      'SRV1b':["SRV1b", joinCutStrings([btw(eleMt[reg], 60, 88), btw(elePt[reg], 20, 30)])],
      
      'SRL1c':["SRL1c", joinCutStrings([eleMt[reg] + " > 88", btw(elePt[reg], 5, 12)])],
      'SRH1c':["SRH1c", joinCutStrings([eleMt[reg] + " > 88", btw(elePt[reg], 12, 20)])],
      'SRV1c':["SRV1c", joinCutStrings([eleMt[reg] + " > 88", btw(elePt[reg], 20, 30)])]
   }

QCD = {}

regions = ['SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']

for reg in regions:
   QCD[reg] = {}
 
   #SR 
   QCD[reg]['SR'] = CutClass("QCD_SR_" + reg, [
      #["elePt<30", elePt['ID'] + " < 30"],
      SRs['I'][reg],
      ["MET", "met >" + METcut], #applied
      ["I", "Sum$(" + eleSel + "&&" + hybIsoCut + ") == 1"],
      ["A", "vetoJet_dPhi_j1j2 < 2.5"],
      ], baseCut = presel)

   #nA
   QCD[reg]['MI_A'] = CutClass("QCD_MI_A_" + reg, [
      #["elePt<30", elePt['ID'] + " < 30"],
      SRs['anti-I'][reg], 
      ["anti-I", "Sum$(" + eleSel + "&&" + antiHybIsoCut + ") == 1"], #inverted
      ["A", "vetoJet_dPhi_j1j2 < 2.5"], #applied
      ], baseCut = presel)
   
   #nI
   QCD[reg]['A_MI'] = CutClass("QCD_A_MI_" + reg, [
      #["elePt<30", elePt['D_I'] + " < 30"],
      SRs['I'][reg], 
      ["MET", "met >" + METcut], #applied
      ["I", "Sum$(" + eleSel + "&&" + hybIsoCut + ") == 1"], #applied
      ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
      ], baseCut = presel)
   
   #nIDA
   QCD[reg]['MIA'] = CutClass("QCD_MIA_" + reg, [
      #["elePt<30", elePt['ID'] + " < 30"],
      SRs['anti-I'][reg], 
      ["anti-I", "Sum$(" + eleSel + "&&" + antiHybIsoCut + ") == 1"], #inverted
      ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
      ], baseCut = presel) 

abcd = ['SR', 'MI_A', 'A_MI', 'MIA']

yields = {}
QCDexp = {}
   
if not os.path.isfile(savedir + "/QCDyields" + suffix + ".txt"):
   outfile = open(savedir + "/QCDyields" + suffix + ".txt", "w")
   outfile.write(eleWP + " Electron ID and (MET,HT) Preselection of (" + HTcut + "," + METcut + ")\nSR           A_MI                        MI_A                     MIA                       QCD                     MC                     Ratio\n")

for reg in regions:
   yields[reg] = {}
  
   for sel in abcd:
      yields[reg][sel] = Yields(samples, [qcd], QCD[reg][sel], cutOpt = "combinedList", weight = "weight", pklOpt = False, tableName = reg + "_" + sel, nDigits = 2, err = True, verbose = True, nSpaces = 10)
   
   if yields[reg]['MIA'].yieldDictFull[qcd]['QCD_MIA_' + reg].val: 
      QCDexp[reg] = (yields[reg]['MI_A'].yieldDictFull[qcd]['QCD_MI_A_' + reg] * yields[reg]['A_MI'].yieldDictFull[qcd]['QCD_A_MI_' + reg]/\
      yields[reg]['MIA'].yieldDictFull[qcd]['QCD_MIA_' + reg])
      
      #QCDerr[reg] = QCDexp * sqrt(\
      #         (totalErr['nAerr']/totalYlds['nA'])*(totalErr['nAerr']/totalYlds['nA']) +\
      #         (totalErr['nIerr']/totalYlds['nI'])*(totalErr['nIerr']/totalYlds['nI']) +\
      #         (totalErr['nDerr']/totalYlds['nD'])*(totalErr['nDerr']/totalYlds['nD']) +\
      #         2*(totalErr['nIDAerr']/totalYlds['nIDA'])*(totalErr['nIDAerr']/totalYlds['nIDA']))
  
      print makeLine()
      print "nA_MI = ", yields[reg]['A_MI'].yieldDictFull[qcd]['QCD_A_MI_' + reg], " | nMI_A = ", yields[reg]['MI_A'].yieldDictFull[qcd]['QCD_MI_A_' + reg],\
            " | nMIA = ", yields[reg]['MIA'].yieldDictFull[qcd]['QCD_MIA_' + reg]
      print "QCD Estimation in ", reg, ": ", QCDexp[reg]
      print "QCD MC yield in ", reg, ": ", yields[reg]['SR'].yieldDictFull[qcd]['QCD_SR_' + reg]
      print makeLine()
      
      with open(savedir + "/QCDyields" + suffix + ".txt", "a") as outfile:
            outfile.write(reg + "       " +\
            str(yields[reg]['A_MI'].yieldDictFull[qcd]['QCD_A_MI_' + reg]) + "             " +\
            str(yields[reg]['MI_A'].yieldDictFull[qcd]['QCD_MI_A_' + reg]) + "             " +\
            str(yields[reg]['MIA'].yieldDictFull[qcd]['QCD_MIA_' + reg]) + "             " +\
            str(QCDexp[reg].round(2)) + "             " +\
            str(yields[reg]['SR'].yieldDictFull[qcd]['QCD_SR_' + reg]) + "             ")
            if yields[reg]['SR'].yieldDictFull[qcd]['QCD_SR_' + reg].val:
               outfile.write(str((QCDexp[reg]/yields[reg]['SR'].yieldDictFull[qcd]['QCD_SR_' + reg]).round(2))  + "\n")
            else:
               outfile.write("\n")
