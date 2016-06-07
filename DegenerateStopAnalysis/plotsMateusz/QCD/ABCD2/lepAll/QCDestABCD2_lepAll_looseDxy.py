#QCDestABCD2_lepAll_looseDxy.py
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
#METcut = args.MET
#METloose = args.METloose
#HTcut = args.HT
#enriched = args.enriched
eleWP = args.eleWP
plot = args.plot
save = args.save

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD2/estimation/lepAll/looseDxy"
   if not os.path.exists(savedir): os.makedirs(savedir)
   
suffix = "_" + eleWP

QCDcuts = {}
 
print makeLine()
print "Using LepAll collection."
#print "Ignoring " + otherCollection + " collection."
print makeLine()

#Gets all cuts (electron, SR, CR) for given electron ID
eleIDsel = electronIDs(ID = "nMinus1", removedCut = "d0", iso = False, collection = "LepAll")
#eleIDsel_other = electronIDs(ID = "nMinus1", removedCut = "d0", iso = False, collection = otherCollection)

##for s in samples.massScanList(): samples[s].weight = "weight" #removes ISR reweighting from official mass scan signal samples
#for s in samples: samples[s].tree.SetAlias("eleSel", allCuts[WP]['eleSel'])

etaAcc = 2.1
eleSel = "abs(LepAll_pdgId) == 11 && abs(LepAll_eta) < " + str(etaAcc) + " && " + eleIDsel[eleWP]
#eleSel_other = "abs(" + otherCollection + "_pdgId) == 11 && abs(" + otherCollection + "_eta) < " + str(etaAcc) + " && " + eleIDsel_other['Veto']

#Cuts
dxyCut = "abs(LepAll_dxy) < 0.02"
looseDxyCut = "abs(LepAll_dxy) < 0.05"

hybIsoCut = "(LepAll_relIso03*min(LepAll_pt, 25)) < 5"
antiHybIsoCut = "(LepAll_relIso03*min(LepAll_pt, 25)) > 5"
#hybIsoCut = "((LepAll_absIso03 < 5) || LepAll_relIso03 < 0.2))"
#antiHybIsoCut = "((LepAll_absIso03 > 5) && (LepAll_relIso03 > 0.2))"
   
elePt = {}
elePt['SR'] = "Max$(LepAll_pt*(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + "))"
elePt['ID'] = "Max$(LepAll_pt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + looseDxyCut + "))"
elePt['I_D'] = "Max$(LepAll_pt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + "))"
elePt['D_I'] = "Max$(LepAll_pt*(" + eleSel + "&&" + hybIsoCut + "&&" + looseDxyCut + "))"

eleMt = {}
eleMt['SR'] = "Max$(LepAll_mt*(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + "))"
eleMt['ID'] = "Max$(LepAll_mt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + looseDxyCut + "))"
eleMt['I_D'] = "Max$(LepAll_mt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + "))"
eleMt['D_I'] = "Max$(LepAll_mt*(" + eleSel + "&&" + hybIsoCut + "&&" + looseDxyCut + "))"

presel = CutClass("presel_SR", [
   ["MET300","met > 300"],
   ["HT300","ht_basJet > 300"],
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

for reg in ['SR', 'ID', 'I_D', 'D_I']:
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
      'SRV1c':["SRV1c", joinCutStrings([eleMt[reg] + " > 88", btw(elePt[reg], 20, 30)])]}

QCD = {}
regions = ['SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']

for reg in regions:
   QCD[reg] = {}
 
   #SR 
   QCD[reg]['SR'] = CutClass("QCD_SR_" + reg, [
      #["elePt<30", elePt['ID'] + " < 30"],
      SRs['SR'][reg],
      ["A", "vetoJet_dPhi_j1j2 < 2.5"],
      ["ID", "Sum$(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + ") == 1"],
      ], baseCut = presel)

   #nA
   QCD[reg]['I_DA'] = CutClass("QCD_I_DA_" + reg, [
      #["elePt<30", elePt['ID'] + " < 30"],
      SRs['I_D'][reg], 
      ["A", "vetoJet_dPhi_j1j2 < 2.5"], #applied
      ["anti-I+D", "Sum$(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + ") == 1"], #inverted, applied
      ], baseCut = presel)
   
   #nI
   QCD[reg]['DA_I'] = CutClass("QCD_DA_I_" + reg, [
      #["elePt<30", elePt['D_I'] + " < 30"],
      SRs['D_I'][reg], 
      ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
      ["I+loose-D", "Sum$(" + eleSel + "&&" + hybIsoCut + "&&" + looseDxyCut + ") == 1"], #applied, loose
      ], baseCut = presel)
   
   #nIDA
   QCD[reg]['IDA'] = CutClass("QCD_IDA_" + reg, [
      #["elePt<30", elePt['ID'] + " < 30"],
      SRs['ID'][reg], 
      ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
      ["anti-I+loose-D", "Sum$(" + eleSel + "&&" + antiHybIsoCut + "&&" + looseDxyCut + ") == 1"], #inverted, loose
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

