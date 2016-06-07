#QCDest2.py
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
#eleWP = args.eleWP
#enriched = args.enriched
save = args.save

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD1/estimation/QCDest2"
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

suffix = ""
#suffix = "_HT" + HTcut + "_MET" + METcut + "_METloose" + METloose
#if enriched == True: suffix += "_EMenriched"

def QCDest(collection = "LepGood", samples = samples, save = save, savedir = savedir):
  
   QCDcuts = {}
    
   if collection == "LepGood": otherCollection = "LepOther"
   elif collection == "LepOther": otherCollection = "LepGood"
   
   print makeLine()
   print "Using " + collection + " collection."
   print "Ignoring " + otherCollection + " collection."
   print makeLine()

   #Gets all cuts (electron, SR, CR) for given electron ID
   eleIDsel = electronIDs(ID = "nMinus1", removedCut = "d0", iso = False, collection = collection)
   eleIDsel_other = electronIDs(ID = "nMinus1", removedCut = "d0", iso = False, collection = otherCollection)
 
   ##for s in samples.massScanList(): samples[s].weight = "weight" #removes ISR reweighting from official mass scan signal samples
   #for s in samples: samples[s].tree.SetAlias("eleSel", allCuts[WP]['eleSel'])

   etaAcc = 2.1
   eleSel = "abs(" + collection + "_pdgId) == 11 && abs(" + collection + "_eta) < " + str(etaAcc) + " && " + eleIDsel['Veto']
   eleSel_other = "abs(" + otherCollection + "_pdgId) == 11 && abs(" + otherCollection + "_eta) < " + str(etaAcc) + " && " + eleIDsel_other['Veto']
 
   #Cuts
   dxyCut = "abs(" + collection + "_dxy) < 0.02"
   antiDxyCut = "abs(" + collection + "_dxy) > 0.02"
   
   hybIsoCut = "(" + collection + "_relIso03*min(" + collection + "_pt, 25)) < 5"
   antiHybIsoCut = "(" + collection + "_relIso03*min(" + collection + "_pt, 25)) > 5"
   #hybIsoCut = "((" + collection + "_absIso03 < 5) || " + collection + "_relIso03 < 0.2))"
   #antiHybIsoCut = "((" + collection + "_absIso03 > 5) && (" + collection + "_relIso03 > 0.2))"
      
   elePt = {}
   elePt['SR'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + "))"
   elePt['ID'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiDxyCut + "))"
   elePt['I_D'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + "))"
   elePt['D_I'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + hybIsoCut + "&&" + antiDxyCut + "))"
   
   eleMt = {}
   eleMt['SR'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + "))"
   eleMt['ID'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiDxyCut + "))"
   eleMt['I_D'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + "))"
   eleMt['D_I'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + hybIsoCut + "&&" + antiDxyCut + "))"
   
   presel = CutClass("presel_loose", [
      ["MET300","met > 300"],
      ["HT300","ht_basJet > 300"],
      ["ISR110", "nIsrJet >= 1"],
      ["No3rdJet60","nVetoJet <= 2"],
      ["BVeto","(nBSoftJet == 0 && nBHardJet == 0)"],
      ["eleSel", "Sum$(" + eleSel + ") == 1"],
      ["otherCollection", "Sum$(" + eleSel_other + ") == 0"],
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
      QCD[reg]['ID_A'] = CutClass("QCD_ID_A_" + reg, [
         #["elePt<30", elePt['ID'] + " < 30"],
         SRs['ID'][reg], 
         ["A", "vetoJet_dPhi_j1j2 < 2.5"], #applied
         ["anti-ID", "Sum$(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiDxyCut + ") == 1"], #inverted, inverted
         ], baseCut = presel)
      
      #nI
      QCD[reg]['DA_I'] = CutClass("QCD_DA_I_" + reg, [
         #["elePt<30", elePt['D_I'] + " < 30"],
         SRs['D_I'][reg], 
         ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
         ["I+anti-D", "Sum$(" + eleSel + "&&" + hybIsoCut + "&&" + antiDxyCut + ") == 1"], #applied, inverted
         ], baseCut = presel)
      
      #nD
      QCD[reg]['IA_D'] = CutClass("QCD_IA_D_" + reg, [
         #["elePt<30", elePt['I_D'] + " < 30"],
         SRs['I_D'][reg], 
         ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
         ["anti-I+D", "Sum$(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + ") == 1"], #inverted, applied
         ], baseCut = presel)
      
      #nIDA
      QCD[reg]['IDA'] = CutClass("QCD_IDA_" + reg, [
         #["elePt<30", elePt['ID'] + " < 30"],
         SRs['ID'][reg], 
         ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
         ["anti-ID", "Sum$(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiDxyCut + ") == 1"], #inverted, inverted
         ], baseCut = presel) 
  
      #QCDcuts[reg] = QCD
    
   return QCD

#LepGood & LepOther
QCDgood = QCDest("LepGood")
QCDother = QCDest("LepOther")

regions = ['SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']
abcd = ['SR', 'ID_A', 'DA_I', 'IA_D', 'IDA']

yields = {}
QCD = {}
QCDexp = {}

for reg in regions:
   QCD[reg] = {}
   yields[reg] = {}
   for sel in abcd:
      QCD[reg][sel] = CutClass(reg + "_" + sel, [["combined", QCDgood[reg][sel].combined + "||" + QCDother[reg][sel].combined]], baseCut = None)
      
      yields[reg][sel] = Yields(samples, ['qcd'], QCD[reg][sel], cutOpt = "combinedList", weight = "weight", pklOpt = False, tableName = reg + "_" + sel, nDigits = 2, err = True, verbose = True, nSpaces = 10)
 
   if yields[reg]['IDA'].yieldDictFull['qcd'][reg + '_IDA'].val: 
      QCDexp[reg] = (yields[reg]['ID_A'].yieldDictFull['qcd'][reg + '_ID_A'] * yields[reg]['DA_I'].yieldDictFull['qcd'][reg + '_DA_I'] * \
      yields[reg]['IA_D'].yieldDictFull['qcd'][reg + '_IA_D'])/\
      (yields[reg]['IDA'].yieldDictFull['qcd'][reg + '_IDA'] * yields[reg]['IDA'].yieldDictFull['qcd'][reg + '_IDA'])
      
      #QCDerr[reg] = QCDexp * sqrt(\
      #         (totalErr['nAerr']/totalYlds['nA'])*(totalErr['nAerr']/totalYlds['nA']) +\
      #         (totalErr['nIerr']/totalYlds['nI'])*(totalErr['nIerr']/totalYlds['nI']) +\
      #         (totalErr['nDerr']/totalYlds['nD'])*(totalErr['nDerr']/totalYlds['nD']) +\
      #         2*(totalErr['nIDAerr']/totalYlds['nIDA'])*(totalErr['nIDAerr']/totalYlds['nIDA']))
      
      print makeLine()
      print "nI = ", yields[reg]['DA_I'].yieldDictFull['qcd'][reg + '_DA_I'], " | nD = ", yields[reg]['IA_D'].yieldDictFull['qcd'][reg + '_IA_D'], " | ",\
            "nA = ", yields[reg]['ID_A'].yieldDictFull['qcd'][reg + '_ID_A'], " | nIDA = ", yields[reg]['IDA'].yieldDictFull['qcd'][reg + '_IDA']
      print "QCD Estimation in ", reg, ": ", QCDexp[reg]
      print "QCD MC yield in ", reg, ": ", yields[reg]['SR'].yieldDictFull['qcd'][reg + '_SR']
      print makeLine()
      
      if not os.path.isfile(savedir + "/QCDyields_combined" + suffix + ".txt"):
         outfile = open(savedir + "/QCDyields_combined" + suffix + ".txt", "w")
         outfile.write(" SR           DA_I              IA_D               ID_A               IDA               QCD               MC               Ratio\n")
      with open(savedir + "/QCDyields_combined" + suffix + ".txt", "a") as outfile:
         outfile.write(reg + "     " +\
         str(yields[reg]['DA_I'].yieldDictFull['qcd'][reg + '_DA_I'].round(2)) + "        " +\
         str(yields[reg]['IA_D'].yieldDictFull['qcd'][reg + '_IA_D'].round(2)) + "        " +\
         str(yields[reg]['ID_A'].yieldDictFull['qcd'][reg + '_ID_A'].round(2)) + "        " +\
         str(yields[reg]['IDA'].yieldDictFull['qcd'][reg + '_IDA'].round(2)) + "        " +\
         str(QCDexp[reg].round(2)) + "        " +\
         str(yields[reg]['SR'].yieldDictFull['qcd'][reg + '_SR'].round(2)) + "        ")
         if yields[reg]['SR'].yieldDictFull['qcd'][reg + '_SR'].val:
            outfile.write(str((QCDexp[reg]/yields[reg]['SR'].yieldDictFull['qcd'][reg + '_SR']).round(2)) + "\n")
         else:
            outfile.write("\n")
