# QCDestimation_el.py
# QCD estimation for the electron channel 

import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.eleWPs import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.regions import signalRegions
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style
from Workspace.DegenerateStopAnalysis.tools.bTagWeights import bTagWeights
from Workspace.DegenerateStopAnalysis.tools.getSamples_8011 import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed

from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Sets TDR style
setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
#parser.add_argument("--ABCD", dest = "ABCD",  help = "ABCD method", type = str, default = "4")
parser.add_argument("--MET", dest = "MET",  help = "MET Cut", type = str, default = "300")
parser.add_argument("--HT", dest = "HT",  help = "HT Cut", type = str, default = "400")
parser.add_argument("--METloose", dest = "METloose",  help = "Loose MET Cut", type = str, default = "300")
parser.add_argument("--eleWP", dest = "eleWP",  help = "Electron WP", type = str, default = "Veto")
parser.add_argument("--highWeightVeto", dest = "highWeightVeto",  help = "Remove high weighted events", type = int, default = 0)
#parser.add_argument("--enriched", dest = "enriched",  help = "EM enriched QCD?", type = bool, default = False)
parser.add_argument("--estimation", dest = "estimation",  help = "Toggle estimation", type = int, default = 1)
parser.add_argument("--btag", dest = "btag",  help = "B-tagging option", type = str, default = "sf")
parser.add_argument("--getData", dest = "getData",  help = "Get data samples", type = int, default = 1)
parser.add_argument("--plot", dest = "plot",  help = "Toggle plot", type = int, default = 0)
parser.add_argument("--plotReg", dest = "plotReg",  help = "Toggle plot", type = str, default = "SR1")
parser.add_argument("--logy", dest = "logy",  help = "Toggle logy", type = int, default = 1)
parser.add_argument("--save", dest = "save",  help = "Toggle save", type = int, default = 1)
parser.add_argument("--verbose", dest = "verbose",  help = "Verbosity switch", type = int, default = 0)
parser.add_argument("-b", dest = "batch",  help = "Batch mode", action = "store_true", default = False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
#ABCD = args.ABCD
METcut = args.MET
METloose = args.METloose
HTcut = args.HT
eleWP = args.eleWP
highWeightVeto = args.highWeightVeto
#enriched = args.enriched
estimation = args.estimation
btag = args.btag
getData = args.getData
plot = args.plot
plotReg = args.plotReg
logy = args.logy
save = args.save
verbose = args.verbose

if METcut != METloose: ABCD = "5"
else: ABCD = "4"

print makeDoubleLine()
print "Performing ABCD", ABCD, " QCD estimation for electron channel."
print makeDoubleLine()

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/electron"

   #savedir += "/bTagWeight_" + btag
     
   estdir = savedir + "/estimation"
   
   plotdir = savedir + "/plots"
   plotdir += "/" + plotReg

   if ABCD == "3" or ABCD == "5":
      estdir += "/METloose"
      plotdir += "/METloose"
   elif ABCD == "4":
      estdir += "/noMETloose"
      plotdir += "/noMETloose"

   plotdir += "/HT" + HTcut + "MET" + METcut
   suffix = "_HT" + HTcut + "_MET" + METcut

   if ABCD == "3" or ABCD == "5":
      plotdir += "METloose" + METloose
      suffix += "_METloose" + METloose
   
   #if enriched == True: suffix += "_EMenriched"
   if plot: suffix2 = suffix + "_" + plotReg
   
   if highWeightVeto: 
      estdir += "/highWeightVeto" 
      plotdir += "/highWeightVeto"
      suffix += "_highWeightVeto"
      if plot: suffix2 += "_highWeightVeto"
 
   #if enriched: 
   #   estdir += "_EMenriched"
   #   plotdir += "_EMenriched"
  
   if not os.path.exists(estdir): os.makedirs(estdir)
  
   if plot: 
      if not os.path.exists(plotdir): os.makedirs(plotdir)

#Samples
#if enriched == True: qcd = "qcdem"
#else: qcd = "qcd"

cmgPP = cmgTuplesPostProcessed()

samplesList = ["qcd", "vv", "st", "dy", "z", "tt", "w"]

if getData: samplesList.append("dblind")
samples = getSamples(cmgPP = cmgPP, skim = 'preIncLep', sampleList = samplesList, scan = False, useHT = True, getData = getData) 

#officialSignals = ["s300_290", "s300_270", "s300_250"] #FIXME: crosscheck if these are in allOfficialSignals
   
if verbose:
   print makeLine()
   print "Using samples:"
   newLine()
   for s in samplesList:
      if s: print samples[s].name,":",s
      else: 
         print "!!! Sample " + sample + " unavailable."
         sys.exit(0)
   
#Removal of high weight events
if highWeightVeto:
   weightCut = "50"
else:
   weightCut = "100000"

#Index of leading electron
#NOTE: selection is implicit to index -> dependent on tuples!
ind = "IndexLepAll_el[0]" #standard index sel 
ind2 = "IndexLepAll_el2[0]" #index sel: Veto ID w/o sigmaEtaEta and w/o hybIso

##Gets all cuts (electron, SR, CR) for given electron ID
#if ABCD == "3":   eleIDsel = electronIDsIndex(ID = "standard", removedCut = "None", iso = False, collection = collection)
#elif ABCD == "4": eleIDsel = electronIDsIndex(ID = "nMinus1", removedCut = "sigmaEtaEta", iso = False, collection = collection)

#Geometric cuts
etaAcc = 1.5
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap

#Common QCD cuts
hybIsoCut = "(LepAll_relIso03[" + ind2 + "]*min(LepAll_pt[" + ind2 + "], 25)) < 5" #hybIsoCut = "((LepAll_absIso03 < 5) || LepAll_relIso03 < 0.2))"
antiHybIsoCut = "(LepAll_relIso03[" + ind2 + "]*min(LepAll_pt[" + ind2 + "], 25)) > 5" #antiHybIsoCut = "((LepAll_absIso03 > 5) && (LepAll_relIso03 > 0.2))"
dPhiCut = "(vetoJet_dPhi_j1j2 < 2.5 || nVetoJet <= 1)" #nVetoJet selection unnecessary as value set to -999 for monojet evts
antidPhiCut = "(vetoJet_dPhi_j1j2 > 2.5 || nVetoJet <= 1)" #or required for inclusion of monojet evts

#Differing QCD cuts
#NOTE: ABCD 1 and 2 do not work as dxy cut is implicit to index

geoSel= {\
      'EB':"(abs(LepAll_eta[" + ind2 + "]) <= " + str(ebeeSplit) + ")", 
      'EE':"(abs(LepAll_eta[" + ind2 + "]) > " + str(ebeeSplit) + " && abs(LepAll_eta[" + ind2 + "]) < " + str(etaAcc) + ")"}

if ABCD == "4" or ABCD == "5": #ABCD4
   
   sigmaEtaEtaCuts = {\
      'Veto':{'EB':0.0114, 'EE':0.0352},
      'Loose':{'EB':0.0103, 'EE':0.0301},
      'Medium':{'EB':0.0101, 'EE':0.0283},
      'Tight':{'EB':0.0101, 'EE':0.0279}}
   
   sigmaEtaEtaCut = "((" + combineCuts(geoSel['EB'], "LepAll_sigmaIEtaIEta[" + ind2 + "] < " + str(sigmaEtaEtaCuts[eleWP]['EB'])) + ") || (" + combineCuts(geoSel['EE'], "LepAll_sigmaIEtaIEta[" + ind2 + "] < " + str(sigmaEtaEtaCuts[eleWP]['EE'])) + "))"
   antiSigmaEtaEtaCut = "((" + combineCuts(geoSel['EB'], "LepAll_sigmaIEtaIEta[" + ind2 + "] > " + str(sigmaEtaEtaCuts[eleWP]['EB'])) + ") || (" + combineCuts(geoSel['EE'], "LepAll_sigmaIEtaIEta[" + ind2 + "] > " + str(sigmaEtaEtaCuts[eleWP]['EE'])) + "))"

   appliedCut = sigmaEtaEtaCut
   invertedCut = antiSigmaEtaEtaCut

variables = {'elePt':"LepAll_pt[" + ind2 + "]", 'eleMt':"LepAll_mt[" + ind2 + "]"}

if plot: variables.update({"absIso":"LepAll_absIso03[" + ind2 + "]", 'relIso':"LepAll_relIso03[" + ind2 + "]", "hybIso":"(LepAll_relIso03[" + ind2 + "]*min(LepAll_pt[" + ind2 + "], 25))",  
                           "absDxy":"LepAll_dxy[" + ind2 + "]", "sigmaEtaEta":"LepAll_sigmaIEtaIEta[" + ind2 + "]", "hOverE":"LepAll_hadronicOverEm[" + ind2 + "]"})

#Redefining variables in terms of electron selection
# ABCD1: X = D (inverted) | ABCD2: X = D (loose) | ABCD3: X = M (loose) | ABCD4: X = S (inverted)
Xs = {'3':'M', '4':'S', '5':'S'} #'1':'D', '2':'D'

if ABCD == "3" or ABCD == "5": METcutString = "met >" + METloose #loosened MET cut for ABCD3 and ABCD5
else: METcutString = "met >" + METcut

#bTagWeights
bWeightDict = bTagWeights(btag)
bTagString = bWeightDict['sr1_bjet'] #corresponds to bVeto
#bTagString = "nBJet == 0"

#Preselection & basic SR cuts
baseline = CutClass("baseline", [
   ["HT","ht_basJet >" + HTcut],
   ["MET", METcutString],
   ["ISR100", "nIsrJet >= 1"],
   ["No3rdJet60","nVetoJet <= 2"],
   ["BVeto", bTagString],
   ["TauVeto","Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
   ["HighWeightVeto","weight < " + weightCut],
   ], baseCut = None)
         
setEventListToChains(samples, samplesList, baseline)

#leading electron acceptance cuts
eleSel = "abs(LepAll_eta[" + ind + "]) < " + str(etaAcc)# + "&& LepAll_pdgId[" + ind + "] == 11" # + "&&" + eleIDsel[eleWP] #redundant due to index sel
eleSel2 = "abs(LepAll_eta[" + ind2 + "]) < " + str(etaAcc)# + "&& LepAll_pdgId[" + ind + "] == 11" # + "&&" + eleIDsel[eleWP] #redundant due to index sel

lepsel = CutClass("lepsel", [
   ["nEle", "(nLepAll_el == 1 || (nLepAll_el == 2 && LepAll_pt[IndexLepAll_el[1]] < 20))"],
   ["MuVeto","(nLepAll_mu == 0 || (nLepAll_mu == 1 && LepAll_pt[IndexLepAll_mu[0]] < 20))"], 
   ["eleSel", eleSel],
   ], baseCut = baseline)

lepsel2 = CutClass("lepsel2", [
   ["nEle", "(nLepAll_el2 == 1 || (nLepAll_el2 == 2 && LepAll_pt[IndexLepAll_el2[1]] < 20))"],
   ["MuVeto","(nLepAll_mu == 0 || (nLepAll_mu == 1 && LepAll_pt[IndexLepAll_mu[0]] < 20))"], 
   ["eleSel", eleSel2],
   ], baseCut = baseline)

# ABCD1: X = D (inverted) | ABCD2: X = D (loose) | ABCD3: X = M (loose) | ABCD4: X = S (inverted)
abcd = {'SR':'SR', 'IX_A':'IX', 'IXA':'IX'}

if ABCD == "4" or ABCD == "5": # 3D ABCD
   abcd['IA_X'] = 'I_X' 
   abcd['XA_I'] = 'X_I'
#elif ABCD == "3": # 2D ABCD
#   abcd['SR'] = abcd['A_IX'] = 'I'
#   abcd['IX_A'] = abcd['IXA'] = 'anti-I'

SRs = signalRegions("electron") #standard index
SRs_2 = signalRegions("electron", index = "2") #lep2 index

QCD = {}
regions = ['SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']

for reg in regions:
   QCD[reg] = {}

   if ABCD == "4" or ABCD == "5":
      QCD[reg]['SR'] = CutClass("QCD_SR_" + reg, [
         ["MET", "met >" + METcut], #tight MET
         #["I", hybIsoCut], #applied #part of standard index
         #["X", appliedCut], #applied #part of standard index
         ["A", dPhiCut], #applied
         SRs[reg],
         ], baseCut = lepsel)
      
      QCD[reg]['IX_A'] = CutClass("QCD_IX_A_" + reg, [
         ["MET", "met >" + METcut], #tight MET
         ["anti-I", antiHybIsoCut], #inverted,
         ["anti-X", invertedCut], #inverted (loose)
         ["A", dPhiCut], #applied
         SRs_2[reg],
         ], baseCut = lepsel2)
      
      QCD[reg]['XA_I'] = CutClass("QCD_XA_I_" + reg, [ #loose MET
         ["I", hybIsoCut], #applied
         ["anti-X", invertedCut], #inverted
         ["anti-A", antidPhiCut], #inverted
         SRs_2[reg],
         ], baseCut = lepsel2)
      
      QCD[reg]['IA_X'] = CutClass("QCD_IA_X_" + reg, [
         ["MET", "met >" + METcut], #tight MET
         ["anti-I", antiHybIsoCut], #inverted
         ["X", appliedCut], #applied
         ["anti-A", antidPhiCut], #inverted
         SRs_2[reg],
         ], baseCut = lepsel2)
      
      QCD[reg]['IXA'] = CutClass("QCD_IXA_" + reg, [ #loose MET
         ["anti-I", antiHybIsoCut], #inverted, 
         ["anti-X", invertedCut], #inverted (loose)
         ["anti-A", antidPhiCut], #inverted
         SRs_2[reg],
         ], baseCut = lepsel2)
      
   #elif ABCD == "3": #loosened MET
   #   QCD[reg]['SR'] = CutClass("QCD_SR_" + reg, [
   #      ["MET", "met >" + METcut], #tight MET
   #      ["A", dPhiCut], #applied
   #      ["I", hybIsoCut],
   #      SRs_2[reg],
   #      ], baseCut = lepsel2)
   #
   #   QCD[reg]['IX_A'] = CutClass("QCD_IX_A_" + reg, [ #loose MET
   #      ["A", dPhiCut], #applied
   #      ["anti-I", antiHybIsoCut], #inverted
   #      SRs_2[reg],
   #      ], baseCut = lepsel2)
   #
   #   QCD[reg]['A_IX'] = CutClass("QCD_A_IX_" + reg, [
   #      ["MET", "met >" + METcut], #tight MET
   #      ["anti-A", antidPhiCut], #inverted
   #      ["I", hybIsoCut], #applied
   #      SRs_2[reg],
   #      ], baseCut = lepsel2)
   #
   #   QCD[reg]['IXA'] = CutClass("QCD_IXA_" + reg, [ #loose MET
   #      ["anti-A", antidPhiCut], #inverted
   #      ["anti-I", antiHybIsoCut], #inverted
   #      SRs_2[reg],
   #      ], baseCut = lepsel2)
      
if estimation: 
   yields = {}
   QCDyields = {}
 
   SF_dataMC = {}
   QCDest_MC = {}
   QCDest = {}
   
   if save: 
      if not os.path.isfile("%s/QCDyields%s.txt"%(estdir,suffix)):
         outfile = open("%s/QCDyields%s.txt"%(estdir,suffix), "w")
         outfile.write("QCD Estimation for Electron Channel [" + eleWP + " Electron ID and Preselection of (MET, HT) > (" + METcut + "," + HTcut + ")]\n")
         if ABCD == "4" or ABCD == "5": outfile.write("SR        IX_A (MC)            XA_I (MC)            IA_X  (MC)        |\
         IXA (MC)           IXA (data-EWK)          SF_dataMC (IXA)         |\
         QCD est. (MC)          SR (MC)             Ratio       |        QCD est. (data)\n".replace("X", Xs[ABCD]))
         elif ABCD == "3": outfile.write("SR\
         IX_A (MC)             A_IX (MC)                |\
         IXA (MC)           IXA (data-EWK)          SF_dataMC (IXA)         |\
         QCD est. (MC)          SR (MC)             Ratio               |\
         QCD est. (data)\n".replace("X", Xs[ABCD]))
   
   for reg in regions:
      yields[reg] = {}
      QCDyields[reg] = {}
      SF_dataMC[reg] = {}
 
      for sel in abcd:
         #setEventListToChains(samples, samplesList, QCD[reg][sel])
         yields[reg][sel] = Yields(samples, samplesList, QCD[reg][sel], cutOpt = "combinedList", pklOpt = False, tableName = reg + "_" + sel, nDigits = 2, err = True, verbose = True, nSpaces = 1)
  
      if ABCD == "4" or ABCD == "5": #3D ABCD
         #MC yields
         QCDyields[reg]['SR'] =        yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg]
         QCDyields[reg]['IX_A'] =      yields[reg]['IX_A'].yieldDictFull['qcd']['QCD_IX_A_' + reg]
         QCDyields[reg]['XA_I'] =      yields[reg]['XA_I'].yieldDictFull['qcd']['QCD_XA_I_' + reg]
         QCDyields[reg]['IA_X'] =      yields[reg]['IA_X'].yieldDictFull['qcd']['QCD_IA_X_' + reg]
         QCDyields[reg]['IXA_MC'] =    yields[reg]['IXA'].yieldDictFull['qcd']['QCD_IXA_' + reg]
         
         #Estimation from pure QCD MC 
         QCDest_MC[reg] = (QCDyields[reg]['IX_A'] * QCDyields[reg]['XA_I'] * QCDyields[reg]['IA_X'])/(QCDyields[reg]['IXA_MC'] * QCDyields[reg]['IXA_MC'])
         
         #EWK subtraction
         QCDyields[reg]['IXA_data'] =  yields[reg]['IXA'].yieldDictFull['dblind']['QCD_IXA_' + reg] - \
                                       yields[reg]['IXA'].yieldDictFull['w']['QCD_IXA_' + reg] - \
                                       yields[reg]['IXA'].yieldDictFull['tt']['QCD_IXA_' + reg] - \
                                       yields[reg]['IXA'].yieldDictFull['z']['QCD_IXA_' + reg] - \
                                       yields[reg]['IXA'].yieldDictFull['dy']['QCD_IXA_' + reg] - \
                                       yields[reg]['IXA'].yieldDictFull['st']['QCD_IXA_' + reg] - \
                                       yields[reg]['IXA'].yieldDictFull['vv']['QCD_IXA_' + reg]
        
         #Data-MC SF in IXA region 
         SF_dataMC[reg]['IXA'] = (QCDyields[reg]['IXA_data']/QCDyields[reg]['IXA_MC']) 
         
         #Full estimation 
         QCDest[reg] = SF_dataMC[reg]['IXA']*QCDest_MC[reg]
        
         if verbose: 
            print makeLine()
            print "Region: ", reg
            print "QCD MC in IX_A = ".replace("X", Xs[ABCD]), QCDyields[reg]['IX_A'] 
            print "QCD MC in XA_I = ".replace("X", Xs[ABCD]), QCDyields[reg]['XA_I'] 
            print "QCD MC in IA_X = ".replace("X", Xs[ABCD]), QCDyields[reg]['IA_X'] 
            print "QCD MC in IXA = ".replace("X", Xs[ABCD]), QCDyields[reg]['IXA_MC']
            print "Data (EWK subtracted) in IXA = ".replace("X", Xs[ABCD]),  QCDyields[reg]['IXA_data'].round(2)
            print "SF_dataMC in IXA = ".replace("X", Xs[ABCD]), SF_dataMC[reg]['IXA'].round(2)
            print "QCD Estimation (pure MC) in ", reg, ": ", QCDest_MC[reg].round(2)
            print "QCD MC yield in ", reg, ": ", QCDyields[reg]['SR'] 
            if QCDyields[reg]['SR'].val:
               print "Closure ratio (pure MC): ", (QCDest_MC[reg]/QCDyields[reg]['SR']).round(2)
            print makeLine()
            print "QCD Estimation in ", reg, ": ", QCDest[reg].round(2)
        
         with open("%s/QCDyields%s.txt"%(estdir,suffix), "a") as outfile:
            outfile.write(reg + "     " +\
            str(QCDyields[reg]['IX_A'].round(2)) + "          " +\
            str(QCDyields[reg]['XA_I'].round(2)) + "          " +\
            str(QCDyields[reg]['IA_X'].round(2)) + "                 " +\
            str(QCDyields[reg]['IXA_MC'].round(2)) + "          " +\
            str(QCDyields[reg]['IXA_data'].round(2)) + "          " +\
            str(SF_dataMC[reg]['IXA'].round(2)) + "                " +\
            str(QCDest_MC[reg].round(2)) + "          " +\
            str(QCDyields[reg]['SR'].round(2)) + "          ")
            if QCDyields[reg]['SR'].val: outfile.write(str((QCDest[reg]/QCDyields[reg]['SR']).round(2)) + "          ")
            else: outfile.write("N/A           ")
            outfile.write(str(QCDest[reg].round(2)) + "\n")
      
      #elif ABCD == "3": #2D ABCD
      #   QCD_IX_A[reg] =      yields[reg]['IX_A'].yieldDictFull['qcd']['QCD_IX_A_' + reg]
      #   QCD_A_IX[reg] =      yields[reg]['IA_X'].yieldDictFull['qcd']['QCD_IA_X_' + reg]
      #   QCD_IXA_MC[reg] =    yields[reg]['IXA'].yieldDictFull['qcd']['QCD_IXA_' + reg]
      #   QCD_IXA_data[reg] =  yields[reg]['IXA'].yieldDictFull['dblind']['QCD_IXA_' + reg] - \ 
      #                        yields[reg]['IXA'].yieldDictFull['w']['QCD_IXA_' + reg] - \
      #                        yields[reg]['IXA'].yieldDictFull['tt']['QCD_IXA_' + reg] - \
      #                        yields[reg]['IXA'].yieldDictFull['z']['QCD_IXA_' + reg] - \
      #                        yields[reg]['IXA'].yieldDictFull['st']['QCD_IXA_' + reg] - \
      #                        yields[reg]['IXA'].yieldDictFull['vv']['QCD_IXA_' + reg]
      #   
      #   
      #   #Estimation from pure QCD MC 
      #   QCDest_MC[reg] = ((QCD_IX_A[reg] * QCD_A_IX[reg])/(QCD_IXA_MC[reg]))

      #   SF_dataMC['IXA'][reg] = (QCD_IXA_data[reg]/QCD_IXA_MC[reg]) 
      #   
      #   #Full estimation 
      #   QCDest[reg] = SF_dataMC['IXA'][reg]*QCDest_MC[reg]
      #   
      #   #Estimation from pure QCD MC
      #   if verbose: 
      #      print makeLine()
      #      print "Region: ", reg
      #      print "QCD MC in IX_A = ".replace("X", Xs[ABCD]), QCD_IX_A[reg] 
      #      print "QCD MC in A_IX = ".replace("X", Xs[ABCD]), QCD_A_IX[reg] 
      #      print "data | MC in IXA = ".replace("X", Xs[ABCD]),  QCD_IXA_data[reg], "   |   ", QCD_IXA_MC[reg] 
      #      print "SF_dataMC in IXA = ", SF_dataMC['IXA'][reg] 
      #      print "QCD Estimation in ", reg, ": ", QCDest[reg], " (", QCDest_MC[reg], ")"
      #      print "QCD MC yield in ", reg, ": ", yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg]
      #      if yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg].val:
      #         print "Closure ratio: ", QCDest[reg]/yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg]
      #      print makeLine()
   
      #   with open("%s/QCDyields%s.txt"%(estdir,suffix), "a") as outfile:
      #      outfile.write(reg + "     " +\
      #      str(QCD_IX_A[reg].round(2)) + "             " +\
      #      str(QCD_A_IX[reg].round(2)) + "             " +\
      #      str(QCD_IXA_data[reg].round(2)) + "             " +\
      #      str(QCD_IXA_MC[reg].round(2)) + "             " +\
      #      str(SF_dataMC['IXA'][reg].round(2)) + "             " +\
      #      str(QCDest[reg].round(2)) + "             " +\
      #      str(yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg].round(2)) + "             ")
      #      if yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg].val:
      #         outfile.write(str((QCDexp[reg]/yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg]).round(2)) + "\n")
      #      else:
      #         outfile.write("\n")

if plot:
   
   QCD[plotReg]['A'] = CutClass("QCD_A_" + plotReg, [
      ["MET", "met >" + METcut], #tight MET
      ["anti-A", antidPhiCut], #inverted
      SRs_2[plotReg],
      ], baseCut = lepsel2)
   
   QCD[plotReg]['XA'] = CutClass("QCD_XA_" + plotReg, [
      ["anti-X", invertedCut], #inverted
      ["anti-A", antidPhiCut], #inverted
      SRs_2[plotReg],
      ], baseCut = lepsel2)
   
   QCD[plotReg]['IA'] = CutClass("QCD_IA_" + plotReg, [
      ["MET", "met >" + METcut], #tight MET
      ["anti-A", antidPhiCut], #inverted
      ["anti-I", antiHybIsoCut], #inverted
      SRs_2[plotReg],
      ], baseCut = lepsel2)
   
   QCD[plotReg]['I_A'] = CutClass("QCD_I_A_" + plotReg, [
      ["MET", "met >" + METcut], #tight MET
      ["anti-I", antiHybIsoCut], #inverted
      ["A", dPhiCut], #applied
      SRs_2[plotReg],
      ], baseCut = lepsel2)
   
   QCD[plotReg]['X_A'] = CutClass("QCD_X_A_" + plotReg, [
      ["MET", "met >" + METcut], #tight MET
      ["anti-X", invertedCut], #inverted
      ["A", dPhiCut], #applied
      SRs_2[plotReg],
      ], baseCut = lepsel2)
   
   QCD[plotReg]['A_X'] = CutClass("QCD_A_X_" + plotReg, [
      ["MET", "met >" + METcut], #tight MET
      ["anti-A", antidPhiCut], #inverted
      ["X", appliedCut], #applied
      SRs_2[plotReg],
      ], baseCut = lepsel2)
      
   if ABCD != "3":
      QCD[plotReg]['A_I'] = CutClass("QCD_A_I_" + plotReg, [
         ["anti-A", antidPhiCut], #inverted
         ["I", hybIsoCut], #applied
         SRs_2[plotReg],
         ], baseCut = lepsel2)
   
   #elif ABCD == "3":
   #   QCD[plotReg]['A_I'] = CutClass("QCD_A_I_" + plotReg, [
   #      ["MET", "met >" + METcut], #tight MET
   #      ["anti-A", antidPhiCut], #inverted
   #      ["I", hybIsoCut], #applied
   #      SRs_2[plotReg],
   #      ], baseCut = lepsel2)
   
   plotsList = {}
   plotDict = {}
   plotsDict = {}
   plots = {}
   plots2 = {}
   
   if ABCD == "4" or ABCD == "5": plotRegions = ['SR', 'A', 'IA', 'XA', 'I_A', 'A_I', 'X_A', 'A_X', 'IA_X', 'XA_I', 'IX_A', 'IXA']
  
   if getData: plotRegions.remove('SR')
   
   for sel in plotRegions:
      plotDict[sel] = {\
         "elePt_" + sel:{'var':variables['elePt'], "bins":[10, 0, 50], "decor":{"title": "Electron pT Plot" ,"x":"Electron p_{T} / GeV" , "y":"Events", 'log':[0, logy,0]}},
         "absIso_" + sel:{'var':variables['absIso'], "bins":[4, 0, 20], "decor":{"title": "Electron absIso Plot" ,"x":"I_{abs} / GeV" , "y":"Events", 'log':[0,logy,0]}},
         "relIso_" + sel:{'var':variables['relIso'], "bins":[20, 0, 5], "decor":{"title": "Electron relIso Plot" ,"x":"I_{rel}" , "y":"Events", 'log':[0,logy,0]}},
         "hybIso_" + sel:{'var':variables['hybIso'], "bins":[10, 0, 25], "decor":{"title": "Electron hybIso Plot" ,"x":"HI = I_{rel}*min(p_{T}, 25 GeV)" , "y":"Events", 'log':[0,logy,0]}},
         "hybIso2_" + sel:{'var':"(log(1 + " + variables['hybIso'] + ")/log(1+5))", "bins":[8, 0, 4], "decor":{"title": "Electron hybIso Plot" ,"x":"log(1+HI)/log(1+5)" , "y":"Events", 'log':[0,logy,0]}},
         "absDxy_" + sel:{'var':variables['absDxy'], "bins":[4, 0, 0.04], "decor":{"title": "Electron |dxy| Plot" ,"x":"|dxy|" , "y":"Events", "log":[0,logy,0]}},
         "delPhi_" + sel:{'var':"vetoJet_dPhi_j1j2", "bins":[8, 0, 3.14], "decor":{"title": "deltaPhi(j1,j2) Plot" ,"x":"#Delta#phi(j1,j2)" , "y":"Events", 'log':[0,logy,0]}},
         "eleMt_" + sel:{'var':variables['eleMt'], "bins":[10,0,100], "decor":{"title": "Electron mT Plot" ,"x":"m_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
         "MET_" + sel:{'var':"met", "bins":[50,0,500], "decor":{"title": "MET Plot" ,"x":"Missing E_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
         "HT_" + sel:{'var':"ht_basJet", "bins":[50,0,500], "decor":{"title": "HT Plot","x":"H_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
         "sigmaEtaEta_" + sel:{'var':variables['sigmaEtaEta'], "bins":[5,0,0.05], "decor":{"title": "#sigma#eta#eta Plot","x":"#sigma#eta#eta" , "y":"Events", 'log':[0,logy,0]}},
         "hOverE_" + sel:{'var':variables['hOverE'], "bins":[10,0,0.2], "decor":{"title": "H/E Plot","x":"H/E" , "y":"Events", 'log':[0,logy,0]}},
         "weight_" + sel:{'var':"weight", "bins":[20,0,400], "decor":{"title": "Weight Plot","x":"Event Weight" , "y":"Events", 'log':[0,1,0]}}
      }
         
      #setEventListToChains(samples, samplesList, QCD[plotReg][sel])
      
      #plotsList[sel] = ["hybIso2_" + sel, "absDxy_" + sel, "delPhi_" + sel]
      #plotsList[sel] = ["hybIso2_" + sel, "sigmaEtaEta_" + sel, "weight_" + sel]
      plotsList[sel] = ["hybIso2_" + sel, "absDxy_" + sel, "delPhi_" + sel, "sigmaEtaEta_" + sel, "weight_" + sel]
      #plotsList[sel] = ["elePt_" + sel, "absIso_" + sel, "relIso_" + sel,"hybIso_" + sel, "hybIso2_" + sel, "absDxy_" + sel, "delPhi_" + sel, "eleMt_" + sel, "MET_" + sel, "HT_" + sel, "sigmaEtaEta_" + sel, "hOverE_" + sel, "weight_" + sel]
      plotsDict[sel] = Plots(**plotDict[sel])
      plots[sel] = getPlots(samples, plotsDict[sel], QCD[plotReg][sel], samplesList, plotList = plotsList[sel], addOverFlowBin='upper')
      if getData: plots2[sel] = drawPlots(samples, plotsDict[sel], QCD[plotReg][sel], samplesList, plotList = plotsList[sel], denoms=["bkg"], noms = ["dblind"], fom="RATIO", fomLimits=[0,1.8], plotMin = 1, normalize = False, save=False)
      else: plots2[sel] = drawPlots(samples, plotsDict[sel], QCD[plotReg][sel], samplesList, plotList = plotsList[sel], plotMin = 1, normalize = False, save=False)
      
      #Save canvas
      if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
      
         if not os.path.exists("%s/%s/root"%(plotdir, sel.replace("X", Xs[ABCD]))): os.makedirs("%s/%s/root"%(plotdir, sel.replace("X", Xs[ABCD])))
         if not os.path.exists("%s/%s/pdf"%(plotdir, sel.replace("X", Xs[ABCD]))): os.makedirs("%s/%s/pdf"%(plotdir, sel.replace("X", Xs[ABCD])))

         for canv in plots2[sel]['canvs']:
            #if plot['canvs'][canv][0]:
            plots2[sel]['canvs'][canv][0].SaveAs("%s/%s/%s%s.png"%(plotdir, sel.replace("X", Xs[ABCD]), canv, suffix2))
            plots2[sel]['canvs'][canv][0].SaveAs("%s/%s/root/%s%s.root"%(plotdir, sel.replace("X", Xs[ABCD]), canv, suffix2))
            plots2[sel]['canvs'][canv][0].SaveAs("%s/%s/pdf/%s%s.pdf"%(plotdir, sel.replace("X", Xs[ABCD]), canv, suffix2))
