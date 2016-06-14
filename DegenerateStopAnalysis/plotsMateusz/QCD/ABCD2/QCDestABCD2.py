#QCDestABCD2.py
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
parser.add_argument("--eleWP", dest = "eleWP",  help = "Electron WP", type = str, default = "Veto")
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
METcut = args.MET
HTcut = args.HT
eleWP = args.eleWP
#enriched = args.enriched
plot = args.plot
save = args.save

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD2/estimation"
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

suffix = ""

def QCDest(collection = "LepGood", samples = samples, plot = plot, save = save, savedir = savedir):
  
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
   eleSel = "abs(" + collection + "_pdgId) == 11 && abs(" + collection + "_eta) < " + str(etaAcc) + " && " + eleIDsel[eleWP]
   eleSel_other = "abs(" + otherCollection + "_pdgId) == 11 && abs(" + otherCollection + "_eta) < " + str(etaAcc) + " && " + eleIDsel_other[eleWP]
 
   #Cuts
   dxyCut = "abs(" + collection + "_dxy) < 0.02"
   looseDxyCut = "abs(" + collection + "_dxy) < 0.05"
   
   hybIsoCut = "(" + collection + "_relIso03*min(" + collection + "_pt, 25)) < 5"
   antiHybIsoCut = "(" + collection + "_relIso03*min(" + collection + "_pt, 25)) > 5"
   #hybIsoCut = "((" + collection + "_absIso03 < 5) || " + collection + "_relIso03 < 0.2))"
   #antiHybIsoCut = "((" + collection + "_absIso03 > 5) && (" + collection + "_relIso03 > 0.2))"
      
   elePt = {}
   elePt['SR'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + "))"
   elePt['ID'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + looseDxyCut + "))"
   #elePt['I_D'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + "))"
   #elePt['D_I'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + hybIsoCut + "&&" + looseDxyCut + "))"
   
   eleMt = {}
   eleMt['SR'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + "))"
   eleMt['ID'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + looseDxyCut + "))"
   #eleMt['I_D'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + "))"
   #eleMt['D_I'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + hybIsoCut + "&&" + looseDxyCut + "))"
   
   presel = CutClass("presel_SR", [
      ["MET","met > " + METcut],
      ["HT","ht_basJet > " + HTcut],
      ["ISR110", "nIsrJet >= 1"],
      ["No3rdJet60","nVetoJet <= 2"],
      ["BVeto","(nBSoftJet == 0 && nBHardJet == 0)"],
      #["elePt<30", elePt + " < 30"],
      #["anti-AntiQCD", "vetoJet_dPhi_j1j2 > 2.5"],
      #["anti-HybIso", "Sum$(" + eleSel + "&&" + antiHybIsoCut + ") == 1"],
      #["anti-dxy", "Max$(abs(" + lep + "_dxy*(" + eleSel + "&&" + antiHybIsoCut + "))) > 0.02"],
      ], baseCut = None) #allCuts['None']['presel'])
   
   SRs ={}
   
   for sel in ['SR', 'ID']:#, 'I_D', 'D_I']:
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
         'SRV1c':["SRV1c", combineCuts(eleMt[sel] + " > 88", btw(elePt[sel], 20, 30))]}
   
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
         ["anti-I+D", "Sum$(" + eleSel + "&&" + antiHybIsoCut + "&&" + looseDxyCut + ") == 1"], #inverted, loose
         ], baseCut = presel)
      
      #nI
      QCD[reg]['A_ID'] = CutClass("QCD_A_ID_" + reg, [
         #["elePt<30", elePt['D_I'] + " < 30"],
         SRs['SR'][reg], 
         ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
         ["I+loose-D", "Sum$(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + ") == 1"], #applied, applied
         ], baseCut = presel)
      
      #nIDA
      QCD[reg]['IDA'] = CutClass("QCD_IDA_" + reg, [
         #["elePt<30", elePt['ID'] + " < 30"],
         SRs['ID'][reg], 
         ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
         ["anti-I+loose-D", "Sum$(" + eleSel + "&&" + antiHybIsoCut + "&&" + looseDxyCut + ") == 1"], #inverted, loose
         ], baseCut = presel) 
  
      #QCDcuts[reg] = QCD
    
   return QCD

#LepGood & LepOther
QCDgood = QCDest("LepGood")
QCDother = QCDest("LepOther")

regions = ['SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']
abcd = ['SR', 'ID_A', 'A_ID', 'IDA']

yields = {}
QCD = {}
QCDexp = {}

if not os.path.isfile(savedir + "/QCDyields" + suffix + ".txt"):
   outfile = open(savedir + "/QCDyields" + suffix + ".txt", "w")
   outfile.write(eleWP + " Electron ID and Preselection of (MET, HT) > (" + METcut + "," + HTcut + ")\n")
   outfile.write("SR           ID_A                 A_ID                     IDA                       QCD                     MC                     Ratio\n")

for reg in regions:
   QCD[reg] = {}
   yields[reg] = {}
   for sel in abcd:
      QCD[reg][sel] = CutClass(reg + "_" + sel, [["combined", QCDgood[reg][sel].combined + "||" + QCDother[reg][sel].combined]], baseCut = None)
      yields[reg][sel] = Yields(samples, ['qcd'], QCD[reg][sel], cutOpt = "combinedList", weight = "weight", pklOpt = False, tableName = reg + "_" + sel, nDigits = 2, err = True, verbose = True, nSpaces = 10)
  
   if yields[reg]['IDA'].yieldDictFull['qcd'][reg + '_IDA'].val: 
      QCDexp[reg] = (yields[reg]['ID_A'].yieldDictFull['qcd'][reg + '_ID_A'] * yields[reg]['A_ID'].yieldDictFull['qcd'][reg + '_A_ID']/\
      yields[reg]['IDA'].yieldDictFull['qcd'][reg + '_IDA'])
      
      print makeLine()
      print "nID_A = ", yields[reg]['ID_A'].yieldDictFull['qcd'][reg + '_ID_A'], " | nA_ID = ", yields[reg]['A_ID'].yieldDictFull['qcd'][reg + '_A_ID'],\
            " | nIDA = ", yields[reg]['IDA'].yieldDictFull['qcd'][reg + '_IDA']
      print "QCD Estimation in ", reg, ": ", QCDexp[reg]
      print "QCD MC yield in ", reg, ": ", yields[reg]['SR'].yieldDictFull['qcd'][reg + '_SR']
      print makeLine()
      
      with open(savedir + "/QCDyields" + suffix + ".txt", "a") as outfile:
         outfile.write(reg + "     " +\
         str(yields[reg]['ID_A'].yieldDictFull['qcd'][reg + '_ID_A'].round(2)) + "             " +\
         str(yields[reg]['A_ID'].yieldDictFull['qcd'][reg + '_A_ID'].round(2)) + "             " +\
         str(yields[reg]['IDA'].yieldDictFull['qcd'][reg + '_IDA'].round(2)) + "             " +\
         str(QCDexp[reg].round(2)) + "             " +\
         str(yields[reg]['SR'].yieldDictFull['qcd'][reg + '_SR'].round(2)) + "             ")
         if yields[reg]['SR'].yieldDictFull['qcd'][reg + '_SR'].val: 
            outfile.write(str((QCDexp[reg]/yields[reg]['SR'].yieldDictFull['qcd'][reg + '_SR']).round(2))  + "\n")
         else:
            outfile.write("\n")
