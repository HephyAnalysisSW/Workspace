#QCDestABCD4.py
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
#parser.add_argument("--isolation", dest = "isolation",  help = "Isolation (hybIso03/hybIso04)", type = str, default = "hybIso03")
parser.add_argument("--MET", dest = "MET",  help = "MET Cut", type = str, default = "300")
parser.add_argument("--HT", dest = "HT",  help = "HT Cut", type = str, default = "300")
#parser.add_argument("--METloose", dest = "METloose",  help = "Loose MET Cut", type = str, default = "250")
parser.add_argument("--eleWP", dest = "eleWP",  help = "Electron WP", type = str, default = "Veto")
#parser.add_argument("--removedCut", dest = "removedCut",  help = "Variable removed from electron ID", type = str, default = "None") #"sigmaEtaEta" "hOverE" "ooEmooP" "dEta" "dPhi" "d0" "dz" "MissingHits" "convVeto"
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
#METloose = args.METloose
HTcut = args.HT
eleWP = args.eleWP
#removedCut = args.removedCut
enriched = args.enriched
save = args.save

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD4/estimation/"
   #else: savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD4/estimation/" + eleWP + "_no_" + removedCut + "/MET" + METcut + "HT" + HTcut
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
   
suffix = "_" + eleWP + "_HT" + HTcut + "_MET" + METcut #+ "_METloose" + METloose
if enriched == True: suffix += "_EMenriched"

QCDcuts = {}
 
print makeLine()
print "Using LepAll collection."
#print "Ignoring " + otherCollection + " collection."
print makeLine()

#Gets all cuts (electron, SR, CR) for given electron ID
eleIDsel = electronIDs(ID = "nMinus1", removedCut = "sigmaEtaEta", iso = False, collection = "LepAll")

##for s in samples.massScanList(): samples[s].weight = "weight" #removes ISR reweighting from official mass scan signal samples
#for s in samples: samples[s].tree.SetAlias("eleSel", allCuts[WP]['eleSel'])

#Geometrical cuts
etaAcc = 2.1
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap

eleSel = "abs(LepAll_pdgId) == 11 && abs(LepAll_eta) < " + str(etaAcc) + " && " + eleIDsel[eleWP]

geoSel= {\
   'EB':"(abs(LepAll_eta) <= " + str(ebeeSplit) + ")", 
   'EE':"(abs(LepAll_eta) > " + str(ebeeSplit) + " && abs(LepAll_eta) < " + str(etaAcc) + ")"}

sigmaEtaEtaCuts = {\
   'Veto':{'EB':0.0114, 'EE':0.0352},
   'Loose':{'EB':0.0103, 'EE':0.0301},
   'Medium':{'EB':0.0101, 'EE':0.0283},
   'Tight':{'EB':0.0101, 'EE':0.0279}}

sigmaEtaEtaCut = "((" + geoSel['EB'] + " && LepAll_sigmaIEtaIEta <" + str(sigmaEtaEtaCuts[eleWP]['EB']) + ") || (" + geoSel['EE'] + "&& LepAll_sigmaIEtaIEta <" + str(sigmaEtaEtaCuts[eleWP]['EE']) + "))"
antiSigmaEtaEtaCut = "((" + geoSel['EB'] + " && LepAll_sigmaIEtaIEta >" + str(sigmaEtaEtaCuts[eleWP]['EB']) + ") || (" + geoSel['EE'] + "&& LepAll_sigmaIEtaIEta >" + str(sigmaEtaEtaCuts[eleWP]['EE']) + "))"

hybIsoCut = "(LepAll_relIso03*min(LepAll_pt, 25)) < 5"
antiHybIsoCut = "(LepAll_relIso03*min(LepAll_pt, 25)) > 5"
#hybIsoCut = "((LepAll_absIso03 < 5) || LepAll_relIso03 < 0.2))"
#antiHybIsoCut = "((LepAll_absIso03 > 5) && (LepAll_relIso03 > 0.2))"

#Redefining electron pT in terms of selection
elePt = {}
elePt['SR'] = "Max$(LepAll_pt*(" + combineCutsList([eleSel, hybIsoCut, sigmaEtaEtaCut]) + "))"
elePt['IS'] = "Max$(LepAll_pt*(" + combineCutsList([eleSel, antiHybIsoCut, antiSigmaEtaEtaCut]) + "))"
elePt['I_S'] = "Max$(LepAll_pt*(" + combineCutsList([eleSel, antiHybIsoCut, sigmaEtaEtaCut]) + "))"
elePt['S_I'] = "Max$(LepAll_pt*(" + combineCutsList([eleSel, hybIsoCut, antiSigmaEtaEtaCut]) + "))"

#Redefining mT in terms of selection
eleMt = {}
eleMt['SR'] = "Max$(LepAll_mt*(" + combineCutsList([eleSel, hybIsoCut, sigmaEtaEtaCut]) + "))"
eleMt['IS'] = "Max$(LepAll_mt*(" + combineCutsList([eleSel, antiHybIsoCut, antiSigmaEtaEtaCut]) + "))"
eleMt['I_S'] = "Max$(LepAll_mt*(" + combineCutsList([eleSel, antiHybIsoCut, sigmaEtaEtaCut]) + "))"
eleMt['S_I'] = "Max$(LepAll_mt*(" + combineCutsList([eleSel, hybIsoCut, antiSigmaEtaEtaCut]) + "))"

presel = CutClass("presel_SR", [
   ["MET","met >" + METcut],
   ["HT","ht_basJet >" + HTcut],
   ["ISR110", "nIsrJet >= 1"],
   ["No3rdJet60","nVetoJet <= 2"],
   ["BVeto","(nBSoftJet == 0 && nBHardJet == 0)"],
   #["METloose","met >" + METloose], #looser MET for B & D regions
   ], baseCut = None) #allCuts['None']['presel'])


abcd = {'SR':'SR', 'IS_A':'IS', 'SA_I':'S_I', 'IA_S':'I_S', 'ISA':'IS'}

SRs ={}

for sel in abcd.values(): 
   SRs[sel] = {\
      'SR1':["SR1", elePt[sel] + " < 30"],
      'SR1a':["SR1a", combineCuts(eleMt[sel] + " < 60", elePt[sel] + " < 30")],
      'SR1b':["SR1b", combineCuts(btw(eleMt[sel], 60, 88), elePt[sel] + " < 30")],
      'SR1c':["SR1c", combineCuts(eleMt[sel] + " > 88", elePt[sel] + " < 30")],
      
      'SRL1a':["SRL1a", combineCuts(eleMt[sel] + " < 60", btw(elePt[sel], 5, 12))],
      'SRH1a':["SRH1a", combineCuts(eleMt[sel] + " < 60", btw(elePt[sel], 12, 20))],
      'SRV1a':["SRV1a", combineCuts(eleMt[sel] + " < 60", btw(elePt[sel], 20, 30))],
      
      'SRL1b':["SRL1b", combineCuts(btw(eleMt[sel], 60, 88), btw(elePt[sel], 5, 12))],
      'SRH1b':["SRH1b", combineCuts(btw(eleMt[sel], 60, 88), btw(elePt[sel], 12, 20))],
      'SRV1b':["SRV1b", combineCuts(btw(eleMt[sel], 60, 88), btw(elePt[sel], 20, 30))],
      
      'SRL1c':["SRL1c", combineCuts(eleMt[sel] + " > 88", btw(elePt[sel], 5, 12))],
      'SRH1c':["SRH1c", combineCuts(eleMt[sel] + " > 88", btw(elePt[sel], 12, 20))],
      'SRV1c':["SRV1c", combineCuts(eleMt[sel] + " > 88", btw(elePt[sel], 20, 30))]
   }

QCD = {}

regions = ['SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']

for reg in regions:
   QCD[reg] = {}
 
   QCD[reg]['SR'] = CutClass("QCD_SR_" + reg, [
      #["elePt<30", elePt['SR'] + " < 30"],
      SRs['SR'][reg],
      ["A", "vetoJet_dPhi_j1j2 < 2.5"],
      ["IS", "Sum$(" + eleSel + "&&" + hybIsoCut + "&&" + sigmaEtaEtaCut + ") == 1"],
      ], baseCut = presel)
   
   QCD[reg]['IS_A'] = CutClass("QCD_IS_A_" + reg, [
      #["elePt<30", elePt['IS'] + " < 30"],
      SRs['IS'][reg],
      ["A", "vetoJet_dPhi_j1j2 < 2.5"], #applied
      ["anti-IS", "Sum$(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiSigmaEtaEtaCut + ") == 1"], #inverted, inverted
      ], baseCut = presel)
   
   QCD[reg]['SA_I'] = CutClass("QCD_SA_I_" + reg, [
      #["elePt<30", elePt['S_I'] + " < 30"],
      SRs['S_I'][reg],
      ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
      ["I+anti-S", "Sum$(" + eleSel + "&&" + hybIsoCut + "&&" + antiSigmaEtaEtaCut + ") == 1"], #applied, inverted
      ], baseCut = presel)
   
   QCD[reg]['IA_S'] = CutClass("QCD_IA_S_" + reg, [
      #["elePt<30", elePt['I_S'] + " < 30"],
      SRs['I_S'][reg],
      ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
      ["anti-I+S", "Sum$(" + eleSel + "&&" + antiHybIsoCut + "&&" + sigmaEtaEtaCut + ") == 1"], #inverted, applied
      ], baseCut = presel)
   
   QCD[reg]['ISA'] = CutClass("QCD_ISA_" + reg, [
      #["elePt<30", elePt['IS'] + " < 30"],
      SRs['IS'][reg],
      ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
      ["anti-IS", "Sum$(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiSigmaEtaEtaCut + ") == 1"], #inverted, inverted
      ], baseCut = presel)

yields = {}
QCDexp = {}
   
if not os.path.isfile(savedir + "/QCDyields" + suffix + ".txt"):
   outfile = open(savedir + "/QCDyields" + suffix + ".txt", "w")
   outfile.write(eleWP + " Electron ID and (MET,HT) Preselection of (" + HTcut + "," + METcut + ")\nSR           SA_I                 IA_S                    IS_A                     ISA                       QCD                     MC                     Ratio\n")

for reg in regions:
   yields[reg] = {}
   for sel in abcd:
      yields[reg][sel] = Yields(samples, ['qcd'], QCD[reg][sel], cutOpt = "combinedList", weight = "weight", pklOpt = False, tableName = reg + "_" + sel, nDigits = 2, err = True, verbose = True, nSpaces = 10)

   if yields[reg]['ISA'].yieldDictFull['qcd']['QCD_ISA_' + reg].val:
      QCDexp[reg] = (yields[reg]['IS_A'].yieldDictFull['qcd']['QCD_IS_A_' + reg] * yields[reg]['SA_I'].yieldDictFull['qcd']['QCD_SA_I_' + reg] * \
      yields[reg]['IA_S'].yieldDictFull['qcd']['QCD_IA_S_' + reg])/\
      (yields[reg]['ISA'].yieldDictFull['qcd']['QCD_ISA_' + reg] * yields[reg]['ISA'].yieldDictFull['qcd']['QCD_ISA_' + reg])

      print makeLine()
      print "nSA_I = ", yields[reg]['SA_I'].yieldDictFull['qcd']['QCD_SA_I_' + reg], " | nIA_S = ", yields[reg]['IA_S'].yieldDictFull['qcd']['QCD_IA_S_' + reg], " | ",\
            "nIS_A = ", yields[reg]['IS_A'].yieldDictFull['qcd']['QCD_IS_A_' + reg], " | nISA = ", yields[reg]['ISA'].yieldDictFull['qcd']['QCD_ISA_' + reg]
      print "QCD Estimation in ", reg, ": ", QCDexp[reg]
      print "QCD MC yield in ", reg, ": ", yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg]
      print makeLine()

      with open(savedir + "/QCDyields" + suffix + ".txt", "a") as outfile:
         outfile.write(reg + "     " +\
         str(yields[reg]['SA_I'].yieldDictFull['qcd']['QCD_SA_I_' + reg].round(2)) + "             " +\
         str(yields[reg]['IA_S'].yieldDictFull['qcd']['QCD_IA_S_' + reg].round(2)) + "             " +\
         str(yields[reg]['IS_A'].yieldDictFull['qcd']['QCD_IS_A_' + reg].round(2)) + "             " +\
         str(yields[reg]['ISA'].yieldDictFull['qcd']['QCD_ISA_' + reg].round(2)) + "             " +\
         str(QCDexp[reg].round(2)) + "             " +\
         str(yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg].round(2)) + "             ")
         if yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg].val:
            outfile.write(str((QCDexp[reg]/yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg]).round(2)) + "\n")
         else:
            outfile.write("\n")
