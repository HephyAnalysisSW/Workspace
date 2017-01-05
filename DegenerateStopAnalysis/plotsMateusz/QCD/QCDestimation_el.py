# QCDestimation_el.py
# QCD estimation for the electron channel 
# Mateusz Zarucki 2016

import ROOT
import os, sys
import argparse
import pickle
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.HEPHYPythonTools import u_float
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.eleWPs import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.regions import signalRegions
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, makeDir, setup_style
from Workspace.DegenerateStopAnalysis.tools.bTagWeights import bTagWeights
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Sets TDR style
setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--ABCD", dest = "ABCD",  help = "ABCD method", type = str, default = "2D")
parser.add_argument("--invertSigmaEtaEta", dest = "invertSigmaEtaEta",  help = "Invert sigmaEtaEta?", type = int, default = 0)
parser.add_argument("--loosenMET", dest = "loosenMET",  help = "Loosen MET?", type = int, default = 0)
parser.add_argument("--MET", dest = "MET",  help = "MET Cut", type = str, default = "300")
parser.add_argument("--METloose", dest = "METloose",  help = "Loose MET Cut", type = str, default = "200")
parser.add_argument("--HT", dest = "HT",  help = "HT Cut", type = str, default = "400")
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
ABCD = args.ABCD
invertSigmaEtaEta = args.invertSigmaEtaEta
loosenMET = args.loosenMET
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

print makeDoubleLine()
print "Performing ", ABCD, " ABCD QCD estimation" 
if loosenMET: print " with MET loosened to ", METloose
if invertSigmaEtaEta: print " with inverted sigmaEtaEta"
print "for the electron channel."
print makeDoubleLine()

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

#Save
#user/mzarucki/plots/QCD/muon/2D/plots/SR1c/METloose/appliedIP/HT400MET300METloose200
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/QCD/electron/%s"%(tag, ABCD)

   #savedir += "/bTagWeight_" + btag
     
   estdir = savedir + "/estimation"
   
   plotdir = savedir + "/plots"

   if loosenMET: 
      estdir += "/METloose"
      plotdir += "/METloose"
   else:
      estdir += "/noMETloose"
      plotdir += "/noMETloose"
   
   if ABCD == "2D":
      if invertSigmaEtaEta: 
         estdir += "/invertedSigmaEtaEta"
         plotdir += "/invertedSigmaEtaEta"
      else:
         estdir += "/appliedSigmaEtaEta"
         plotdir += "/appliedSigmaEtaEta"

   estdir += "/HT" + HTcut + "MET" + METcut
   plotdir += "/HT" + HTcut + "MET" + METcut
   suffix = "_HT" + HTcut + "_MET" + METcut

   if loosenMET: 
      estdir += "METloose" + METloose
      plotdir += "METloose" + METloose
      suffix += "_METloose" + METloose
   
   #if enriched == True: suffix += "_EMenriched"
   if plot: suffix2 = suffix + "_" + plotReg
   
   plotdir += "/" + plotReg
   
   if highWeightVeto: 
      estdir += "/highWeightVeto" 
      plotdir += "/highWeightVeto"
      suffix += "_highWeightVeto"
      if plot: suffix2 += "_highWeightVeto"
 
   #if enriched: 
   #   estdir += "_EMenriched"
   #   plotdir += "_EMenriched"
  
   makeDir(estdir)
  
   if plot: makeDir(plotdir)

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

geoSel= {\
      'EB':"(abs(LepAll_eta[" + ind2 + "]) <= " + str(ebeeSplit) + ")", 
      'EE':"(abs(LepAll_eta[" + ind2 + "]) > " + str(ebeeSplit) + " && abs(LepAll_eta[" + ind2 + "]) < " + str(etaAcc) + ")"}

sigmaEtaEtaCuts = {\
   'Veto':{'EB':0.0114, 'EE':0.0352},
   'Loose':{'EB':0.0103, 'EE':0.0301},
   'Medium':{'EB':0.0101, 'EE':0.0283},
   'Tight':{'EB':0.0101, 'EE':0.0279}}

sigmaEtaEtaCut = "((" + combineCuts(geoSel['EB'], "LepAll_sigmaIEtaIEta[" + ind2 + "] < " + str(sigmaEtaEtaCuts[eleWP]['EB'])) + ") || (" + combineCuts(geoSel['EE'], "LepAll_sigmaIEtaIEta[" + ind2 + "] < " + str(sigmaEtaEtaCuts[eleWP]['EE'])) + "))"
antiSigmaEtaEtaCut = "((" + combineCuts(geoSel['EB'], "LepAll_sigmaIEtaIEta[" + ind2 + "] > " + str(sigmaEtaEtaCuts[eleWP]['EB'])) + ") || (" + combineCuts(geoSel['EE'], "LepAll_sigmaIEtaIEta[" + ind2 + "] > " + str(sigmaEtaEtaCuts[eleWP]['EE'])) + "))"

variables = {'elePt':"LepAll_pt[" + ind2 + "]", 'eleMt':"LepAll_mt[" + ind2 + "]"}

if plot: variables.update({'absIso':"LepAll_absIso03[" + ind2 + "]", 'relIso':"LepAll_relIso03[" + ind2 + "]", 'hybIso':"(LepAll_relIso03[" + ind2 + "]*min(LepAll_pt[" + ind2 + "], 25))",  
                           'absDxy':"LepAll_dxy[" + ind2 + "]", 'sigmaEtaEta':"LepAll_sigmaIEtaIEta[" + ind2 + "]", 'hOverE':"LepAll_hadronicOverEm[" + ind2 + "]"})

#Redefining variables in terms of electron selection
Xs = {'2D':'', '3D':'S'}

#loosened MET cut
if loosenMET: METcutString = "met >" + METloose 
else: METcutString = "met >" + METcut

#bTagWeights
bWeightDict = bTagWeights(btag)
bTagString = bWeightDict['sr1_bjet'] #corresponds to bVeto
#bTagString = "nBJet == 0"

#Preselection & basic SR cuts
baseline = CutClass("baseline", [
   ["HT","ht_basJet >" + HTcut],
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

if ABCD == "3D":
   abcd = {'SR':'SR', 'SA_I':'S_I', 'IA_S':'I_S', 'IS_A':'IS', 'ISA':'IS'}
elif ABCD == "2D":
   abcd = {'SR':'I', 'A_I': 'I', 'I_A':'anti-I', 'IA':'anti-I'}

SRs = signalRegions("electron") #standard index
SRs_2 = signalRegions("electron", index = "2") #lep2 index

QCD = {}
regions = ['SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1', 'SRH1', 'SRV1', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']

for reg in regions:
   QCD[reg] = {}

   QCD[reg]['SR'] = CutClass("QCD_SR_" + reg, [
      ["MET", "met >" + METcut], #tight MET
      ["A", dPhiCut], #applied
      #["I", hybIsoCut], #applied #part of standard index
      #["S", sigmaEtaEtaCut], #applied #part of standard index
      SRs[reg],
      ], baseCut = lepsel)
  
   if ABCD == "2D":
      if not invertSigmaEtaEta:
         QCD[reg]['I_A'] = CutClass("QCD_I_A_" + reg, [
            ["MET", "met >" + METcut], #tight MET
            ["A", dPhiCut], #applied
            ["anti-I", antiHybIsoCut], #inverted
            ["S", sigmaEtaEtaCut], #applied
            SRs_2[reg],
            ], baseCut = lepsel2)
   
         QCD[reg]['A_I'] = CutClass("QCD_A_I_" + reg, [ 
            ["MET", METcutString], #loosened MET
            ["anti-A", antidPhiCut], #inverted
            ["I", hybIsoCut], #applied
            ["S", sigmaEtaEtaCut], #applied
            SRs_2[reg],
            ], baseCut = lepsel2)
   
         QCD[reg]['IA'] = CutClass("QCD_IA_" + reg, [
            ["MET", METcutString], #loosened MET
            ["anti-A", antidPhiCut], #inverted
            ["anti-I", antiHybIsoCut], #inverted
            ["S", sigmaEtaEtaCut], #applied
            SRs_2[reg],
            ], baseCut = lepsel2)
   
      elif invertSigmaEtaEta: #inverted sigmaEtaEta in two regions
         QCD[reg]['I_A'] = CutClass("QCD_I_A_" + reg, [
            ["MET", "met >" + METcut], #tight MET
            ["A", dPhiCut], #applied
            ["anti-I", antiHybIsoCut], #inverted
            ["anti-S", antiSigmaEtaEtaCut], #inverted
            SRs_2[reg],
            ], baseCut = lepsel2)
      
         QCD[reg]['A_I'] = CutClass("QCD_A_I_" + reg, [
            ["MET", METcutString], #loosened MET
            ["anti-A", antidPhiCut], #inverted
            ["I", hybIsoCut], #applied
            ["S", sigmaEtaEtaCut], #applied
            SRs_2[reg],
            ], baseCut = lepsel2)
      
         QCD[reg]['IA'] = CutClass("QCD_IA_" + reg, [ 
            ["MET", METcutString], #loosened MET
            ["anti-A", antidPhiCut], #inverted
            ["anti-I", antiHybIsoCut], #inverted
            ["anti-S", antiSigmaEtaEtaCut], #inverted
            SRs_2[reg],
            ], baseCut = lepsel2)

   elif ABCD == "3D":
      
      QCD[reg]['IS_A'] = CutClass("QCD_IS_A_" + reg, [
         ["MET", "met >" + METcut], #tight MET
         ["anti-I", antiHybIsoCut], #inverted,
         ["anti-S", antiSigmaEtaEtaCut], #inverted 
         ["A", dPhiCut], #applied
         SRs_2[reg],
         ], baseCut = lepsel2)
      
      QCD[reg]['SA_I'] = CutClass("QCD_SA_I_" + reg, [
         ["MET", METcutString], #loosened MET
         ["I", hybIsoCut], #applied
         ["anti-S", antiSigmaEtaEtaCut], #inverted
         ["anti-A", antidPhiCut], #inverted
         SRs_2[reg],
         ], baseCut = lepsel2)
      
      QCD[reg]['IA_S'] = CutClass("QCD_IA_S_" + reg, [
         ["MET", "met >" + METcut], #tight MET
         ["anti-I", antiHybIsoCut], #inverted
         ["S", sigmaEtaEtaCut], #applied
         ["anti-A", antidPhiCut], #inverted
         SRs_2[reg],
         ], baseCut = lepsel2)
      
      QCD[reg]['ISA'] = CutClass("QCD_ISA_" + reg, [
         ["MET", METcutString], #loosened MET
         ["anti-I", antiHybIsoCut], #inverted, 
         ["anti-S", antiSigmaEtaEtaCut], #inverted
         ["anti-A", antidPhiCut], #inverted
         SRs_2[reg],
         ], baseCut = lepsel2)
      
if estimation: 
   yields = {}
   QCDyields = {}
 
   SF_dataMC = {}
   QCDest_MC = {}
   QCDest = {}
   EWKsys = {}
   
   if save: 
      if not os.path.isfile("%s/QCDyields%s.txt"%(estdir,suffix)):
         outfile = open("%s/QCDyields%s.txt"%(estdir,suffix), "w")
         outfile.write(ABCD + " QCD Estimation for Electron Channel [" + eleWP + " Electron ID and Preselection of (MET, HT) > (" + METcut + "," + HTcut + ")]\n")
         if ABCD == "2D": 
            outfile.write("SR       I_A (MC)            A_I (MC)       |        IA (MC)             IA (data)           IA (EWK MC)           IA (data-EWK)         SF_dataMC (IA)      |      QCD est. (MC)         SR (MC)           Ratio       |       QCD est. (data)         EWKsys\n".replace("X", Xs[ABCD]))
         elif ABCD == "3D": 
            outfile.write("SR       IS_A (MC)         SA_I (MC)         IA_S (MC)       |        ISA (MC)           ISA (data)            ISA (EWK MC)        ISA (data-EWK)         SF_dataMC (ISA)     |     QCD est. (MC)         SR (MC)          Ratio      |       QCD est. (data)       EWKsys\n".replace("X", Xs[ABCD]))
   
   for reg in regions:
      yields[reg] = {}
      QCDyields[reg] = {}
      SF_dataMC[reg] = {}
    
      for sel in abcd:
         #setEventListToChains(samples, samplesList, QCD[reg][sel])
         yields[reg][sel] = Yields(samples, samplesList, QCD[reg][sel], cutOpt = "combinedList", pklOpt = False, tableName = reg + "_" + sel, nDigits = 2, err = True, verbose = True, nSpaces = 1)
     
      if ABCD == "2D":
         
         #MC
         QCDyields[reg]['SR'] =      yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg]
         
         QCDyields[reg]['I_A'] =     yields[reg]['I_A'].yieldDictFull['qcd']['QCD_I_A_' + reg]
         QCDyields[reg]['A_I'] =     yields[reg]['A_I'].yieldDictFull['qcd']['QCD_A_I_' + reg]
         QCDyields[reg]['IA_MC'] =   yields[reg]['IA'].yieldDictFull['qcd']['QCD_IA_' + reg]
         
         #Estimation from pure QCD MC 
         if QCDyields[reg]['IA_MC'].val:
            QCDest_MC[reg] = ((QCDyields[reg]['I_A']*QCDyields[reg]['A_I'])/(QCDyields[reg]['IA_MC']))
         else:
            QCDest_MC[reg] = u_float.u_float(0,0)

         #Data
         QCDyields[reg]['IA_data'] = yields[reg]['IA'].yieldDictFull['dblind']['QCD_IA_' + reg]
         
         #EWK subtraction
         QCDyields[reg]['IA_EWK'] =  yields[reg]['IA'].yieldDictFull['w']['QCD_IA_' + reg] + \
                                     yields[reg]['IA'].yieldDictFull['tt']['QCD_IA_' + reg] + \
                                     yields[reg]['IA'].yieldDictFull['z']['QCD_IA_' + reg] + \
                                     yields[reg]['IA'].yieldDictFull['dy']['QCD_IA_' + reg] + \
                                     yields[reg]['IA'].yieldDictFull['st']['QCD_IA_' + reg] + \
                                     yields[reg]['IA'].yieldDictFull['vv']['QCD_IA_' + reg]
         
         QCDyields[reg]['IA_data-EWK'] =  QCDyields[reg]['IA_data'] - QCDyields[reg]['IA_EWK']
         
         #Data-MC SF in ISA region 
         if QCDyields[reg]['IA_MC'].val:
            SF_dataMC[reg]['IA'] = (QCDyields[reg]['IA_data-EWK']/QCDyields[reg]['IA_MC']) 
         else:
            SF_dataMC[reg]['IA'] = u_float.u_float(0,0) 
    
         #Full estimation 
         QCDest[reg] = SF_dataMC[reg]['IA']*QCDest_MC[reg]
         
         if QCDyields[reg]['IA_MC'].val:
            EWKsys[reg] = 0.3*QCDyields[reg]['IA_EWK']*QCDest_MC[reg]/QCDyields[reg]['IA_MC']
         else:
            EWKsys[reg] = u_float.u_float(0,0) 
   
         #Pickle results 
         pickleFile1 = open("%s/QCDyields_electron%s.pkl"%(estdir,suffix), "w")
         pickle.dump(QCDyields, pickleFile1)
         pickleFile1.close()

         pickleFile2 = open("%s/SF_dataMC_electron%s.pkl"%(estdir,suffix), "w")
         pickle.dump(SF_dataMC, pickleFile2)
         pickleFile2.close()

         pickleFile3 = open("%s/QCDest_MC_electron%s.pkl"%(estdir,suffix), "w")
         pickle.dump(QCDest_MC, pickleFile3)
         pickleFile3.close()

         pickleFile4 = open("%s/QCDest_electron%s.pkl"%(estdir,suffix), "w")
         pickle.dump(QCDest, pickleFile4)
         pickleFile4.close()

         pickleFile5 = open("%s/EWKsys_electron%s.pkl"%(estdir,suffix), "w")
         pickle.dump(EWKsys, pickleFile5)
         pickleFile5.close()
 
         if verbose: 
            print makeLine()
            print "Region: ", reg
            print "QCD MC in I_A = ".replace("X", Xs[ABCD]), QCDyields[reg]['I_A'] 
            print "QCD MC in A_I = ".replace("X", Xs[ABCD]), QCDyields[reg]['A_I'] 
            print "QCD MC in IA = ".replace("X", Xs[ABCD]), QCDyields[reg]['IA_MC']
            print "Data in IA = ".replace("X", Xs[ABCD]),  QCDyields[reg]['IA_data'].round(2)
            print "EWK MC in IA = ".replace("X", Xs[ABCD]),  QCDyields[reg]['IA_EWK'].round(2)
            print "Data (EWK subtracted) in IA = ".replace("X", Xs[ABCD]),  QCDyields[reg]['IA_data-EWK'].round(2)
            print "SF_dataMC in IA = ".replace("X", Xs[ABCD]), SF_dataMC[reg]['IA'].round(2)
            print "QCD Estimation (pure MC) in ", reg, ": ", QCDest_MC[reg].round(2)
            print "QCD MC yield in ", reg, ": ", QCDyields[reg]['SR'] 
            if QCDyields[reg]['SR'].val: 
               print "Closure ratio (pure MC): ", (QCDest_MC[reg]/QCDyields[reg]['SR']).round(2)
            print makeLine()
            print "QCD Estimation in ", reg, ": ", QCDest[reg].round(2)
            print "Systematic unc. due to EWK subtraction in ", reg, ": ", EWKsys[reg].round(2)
 
         with open("%s/QCDyields%s.txt"%(estdir,suffix), "a") as outfile:
            outfile.write(reg.ljust(7) +\
            str(QCDyields[reg]['I_A'].round(2)).ljust(20) +\
            str(QCDyields[reg]['A_I'].round(2)).ljust(22) +\
            str(QCDyields[reg]['IA_MC'].round(2)).ljust(22) +\
            str(QCDyields[reg]['IA_data'].round(2)).ljust(22) +\
            str(QCDyields[reg]['IA_EWK'].round(2)).ljust(22) +\
            str(QCDyields[reg]['IA_data-EWK'].round(2)).ljust(25) +\
            str(SF_dataMC[reg]['IA'].round(2)).ljust(25) +\
            str(QCDest_MC[reg].round(2)).ljust(20) +\
            str(QCDyields[reg]['SR'].round(2)).ljust(20))
            if QCDyields[reg]['SR'].val: outfile.write(str((QCDest[reg]/QCDyields[reg]['SR']).round(2)).ljust(22))
            else: outfile.write("N/A".ljust(22))
            outfile.write(str(QCDest[reg].round(2)).ljust(20) +\
            str(EWKsys[reg].round(3)) + "\n")
      
      elif ABCD == "3D":
         
         #MC
         QCDyields[reg]['SR'] =       yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg]
         
         QCDyields[reg]['IS_A'] =     yields[reg]['IS_A'].yieldDictFull['qcd']['QCD_IS_A_' + reg]
         QCDyields[reg]['SA_I'] =     yields[reg]['SA_I'].yieldDictFull['qcd']['QCD_SA_I_' + reg]
         QCDyields[reg]['IA_S'] =     yields[reg]['IA_S'].yieldDictFull['qcd']['QCD_IA_S_' + reg]
         QCDyields[reg]['ISA_MC'] =   yields[reg]['ISA'].yieldDictFull['qcd']['QCD_ISA_' + reg]
         
         #Estimation from pure QCD MC 
         QCDest_MC[reg] = (QCDyields[reg]['IS_A'] * QCDyields[reg]['SA_I'] * QCDyields[reg]['IA_S'])/(QCDyields[reg]['ISA_MC'] * QCDyields[reg]['ISA_MC'])
         
         #Data
         QCDyields[reg]['ISA_data'] = yields[reg]['ISA'].yieldDictFull['dblind']['QCD_ISA_' + reg]

         #EWK subtraction
         QCDyields[reg]['ISA_EWK'] =  yields[reg]['ISA'].yieldDictFull['w']['QCD_ISA_' + reg] + \
                                      yields[reg]['ISA'].yieldDictFull['tt']['QCD_ISA_' + reg] + \
                                      yields[reg]['ISA'].yieldDictFull['z']['QCD_ISA_' + reg] + \
                                      yields[reg]['ISA'].yieldDictFull['dy']['QCD_ISA_' + reg] + \
                                      yields[reg]['ISA'].yieldDictFull['st']['QCD_ISA_' + reg] + \
                                      yields[reg]['ISA'].yieldDictFull['vv']['QCD_ISA_' + reg]
         
         QCDyields[reg]['ISA_data-EWK'] =  QCDyields[reg]['ISA_data'] - QCDyields[reg]['ISA_EWK']
        
         #Data-MC SF in ISA region 
         SF_dataMC[reg]['ISA'] = (QCDyields[reg]['ISA_data-EWK']/QCDyields[reg]['ISA_MC']) 
         
         #Full estimation 
         QCDest[reg] = SF_dataMC[reg]['ISA']*QCDest_MC[reg]
         EWKsys[reg] = 0.3*QCDyields[reg]['ISA_EWK']*QCDest_MC[reg]/QCDyields[reg]['ISA_MC']
         
         #Pickle results 
         pickleFile1 = open("%s/QCDyields_electron%s.pkl"%(estdir,suffix), "w")
         pickle.dump(QCDyields, pickleFile1)
         pickleFile1.close()

         pickleFile2 = open("%s/SF_dataMC_electron%s.pkl"%(estdir,suffix), "w")
         pickle.dump(SF_dataMC, pickleFile2)
         pickleFile2.close()

         pickleFile3 = open("%s/QCDest_MC_electron%s.pkl"%(estdir,suffix), "w")
         pickle.dump(QCDest_MC, pickleFile3)
         pickleFile3.close()

         pickleFile4 = open("%s/QCDest_electron%s.pkl"%(estdir,suffix), "w")
         pickle.dump(QCDest, pickleFile4)
         pickleFile4.close()

         pickleFile5 = open("%s/EWKsys_electron%s.pkl"%(estdir,suffix), "w")
         pickle.dump(EWKsys, pickleFile5)
         pickleFile5.close()
        
         if verbose: 
            print makeLine()
            print "Region: ", reg
            print "QCD MC in IS_A = ".replace("X", Xs[ABCD]), QCDyields[reg]['IS_A'] 
            print "QCD MC in SA_I = ".replace("X", Xs[ABCD]), QCDyields[reg]['SA_I'] 
            print "QCD MC in IA_S = ".replace("X", Xs[ABCD]), QCDyields[reg]['IA_S'] 
            print "QCD MC in ISA = ".replace("X", Xs[ABCD]), QCDyields[reg]['ISA_MC']
            print "Data in ISA = ".replace("X", Xs[ABCD]),  QCDyields[reg]['ISA_data'].round(2)
            print "EWK MC in ISA = ".replace("X", Xs[ABCD]),  QCDyields[reg]['ISA_EWK'].round(2)
            print "Data (EWK subtracted) in ISA = ".replace("X", Xs[ABCD]),  QCDyields[reg]['ISA_data-EWK'].round(2)
            print "SF_dataMC in ISA = ".replace("X", Xs[ABCD]), SF_dataMC[reg]['ISA'].round(2)
            print "QCD Estimation (pure MC) in ", reg, ": ", QCDest_MC[reg].round(2)
            print "QCD MC yield in ", reg, ": ", QCDyields[reg]['SR'] 
            if QCDyields[reg]['SR'].val:
               print "Closure ratio (pure MC): ", (QCDest_MC[reg]/QCDyields[reg]['SR']).round(2)
            print makeLine()
            print "QCD Estimation in ", reg, ": ", QCDest[reg].round(2)
            print "Systematic unc. due to EWK subtraction in ", reg, ": ", EWKsys[reg].round(2)
 
         with open("%s/QCDyields%s.txt"%(estdir,suffix), "a") as outfile:
            outfile.write(reg.ljust(7) +\
            str(QCDyields[reg]['IS_A'].round(2)).ljust(18)  +\
            str(QCDyields[reg]['SA_I'].round(2)).ljust(18) +\
            str(QCDyields[reg]['IA_S'].round(2)).ljust(25) +\
            str(QCDyields[reg]['ISA_MC'].round(2)).ljust(21) +\
            str(QCDyields[reg]['ISA_data'].round(2)).ljust(21) +\
            str(QCDyields[reg]['ISA_EWK'].round(2)).ljust(21) +\
            str(QCDyields[reg]['ISA_data-EWK'].round(2)).ljust(25) +\
            str(SF_dataMC[reg]['ISA'].round(2)).ljust(24) +\
            str(QCDest_MC[reg].round(2)).ljust(20) +\
            str(QCDyields[reg]['SR'].round(2)).ljust(18))
            if QCDyields[reg]['SR'].val: outfile.write(str((QCDest[reg]/QCDyields[reg]['SR']).round(2)).ljust(20))
            else: outfile.write("N/A".ljust(20))
            outfile.write(str(QCDest[reg].round(2)).ljust(20) +\
            str(EWKsys[reg].round(3)) + "\n")
      
if plot:

   if ABCD == "2D":

      QCD[plotReg]['AM_noSigmaEtaEta'] = CutClass("QCD_AM_noSigmaEtaEta_" + plotReg, [ #loose MET
         ["MET", METcutString], #loosened MET
         ["anti-A", antidPhiCut], #inverted
         SRs_2[plotReg],
         ], baseCut = lepsel2)
      
      QCD[plotReg]['I_noSigmaEtaEta'] = CutClass("QCD_I_noSigmaEtaEta_" + plotReg, [
         ["MET", "met >" + METcut], #tight MET
         ["anti-I", antiHybIsoCut], #inverted
         SRs_2[plotReg],
         ], baseCut = lepsel2)
      
      QCD[plotReg]['IAM_noSigmaEtaEta'] = CutClass("QCD_IAM_noSigmaEtaEta_" + plotReg, [
         ["MET", METcutString], #loosened MET
         ["anti-I", antiHybIsoCut], #inverted
         ["anti-A", antidPhiCut], #inverted
         SRs_2[plotReg],
         ], baseCut = lepsel2)

      if not invertSigmaEtaEta:
         QCD[plotReg]['AM'] = CutClass("QCD_AM_" + plotReg, [
           ["MET", METcutString], #loosened MET
           ["anti-A", antidPhiCut], #inverted
           ["S", sigmaEtaEtaCut], #applied
           SRs_2[plotReg],
           ], baseCut = lepsel2)
      
      elif invertSigmaEtaEta: 
         QCD[plotReg]['AMS'] = CutClass("QCD_AMS_" + plotReg, [ 
            ["MET", METcutString], #loosened MET
            ["anti-A", antidPhiCut], #inverted
            ["anti-S", antiSigmaEtaEtaCut], #inverted
            SRs_2[plotReg],
            ], baseCut = lepsel2)
   
   elif ABCD == "3D": 
      
      QCD[plotReg]['A'] = CutClass("QCD_A_" + plotReg, [
         ["MET", "met >" + METcut], #tight MET
         ["anti-A", antidPhiCut], #inverted
         SRs_2[plotReg],
         ], baseCut = lepsel2)
      
      QCD[plotReg]['IA'] = CutClass("QCD_IA_" + plotReg, [
         ["MET", "met >" + METcut], #tight MET
         ["anti-A", antidPhiCut], #inverted
         ["anti-I", antiHybIsoCut], #inverted
         SRs_2[plotReg],
         ], baseCut = lepsel2)
      
      #QCD[plotReg]['I_A'] = CutClass("QCD_I_A_" + plotReg, [
      #   ["MET", "met >" + METcut], #tight MET
      #   ["anti-I", antiHybIsoCut], #inverted
      #   ["A", dPhiCut], #applied
      #   SRs_2[plotReg],
      #   ], baseCut = lepsel2)
      
      QCD[plotReg]['S_A'] = CutClass("QCD_S_A_" + plotReg, [
         ["MET", "met >" + METcut], #tight MET
         ["anti-S", antiSigmaEtaEtaCut], #inverted
         ["A", dPhiCut], #applied
         SRs_2[plotReg],
         ], baseCut = lepsel2)
      
      QCD[plotReg]['A_S'] = CutClass("QCD_A_S_" + plotReg, [
         ["MET", "met >" + METcut], #tight MET
         ["anti-A", antidPhiCut], #inverted
         ["S", sigmaEtaEtaCut], #applied
         SRs_2[plotReg],
         ], baseCut = lepsel2)
         
      #QCD[plotReg]['A_I'] = CutClass("QCD_A_I_" + plotReg, [
      #   ["MET", METcutString], #loosened MET
      #   ["anti-A", antidPhiCut], #inverted
      #   ["I", hybIsoCut], #applied
      #   SRs_2[plotReg],
      #   ], baseCut = lepsel2)
      
      QCD[plotReg]['SA'] = CutClass("QCD_SA_" + plotReg, [
         ["MET", METcutString], #loosened MET
         ["anti-S", antiSigmaEtaEtaCut], #inverted
         ["anti-A", antidPhiCut], #inverted
         SRs_2[plotReg],
         ], baseCut = lepsel2)
      
   if ABCD == "3D": 
      plotRegions = abcd.keys()
      plotRegions.extend(['A', 'IA', 'SA', 'S_A', 'A_S']) #'I_A', 'A_I'
   elif ABCD == "2D": 
      plotRegions = abcd.keys()
      plotRegions.extend(["AM_noSigmaEtaEta", "I_noSigmaEtaEta", "IAM_noSigmaEtaEta"]) 
      
      if not invertSigmaEtaEta:
         plotRegions.append("AM")
      elif invertSigmaEtaEta:
         plotRegions.append("AMS")
   
   if getData: plotRegions.remove('SR')

   plotDict = {\
      "elePt":{      'var':variables['elePt'],                                'bins':[10, 0, 50],  'decor':{"title":"Electron pT Plot",     'x':"Electron p_{T} / GeV",            'y':"Events", 'log':[0,logy,0]}},
      "eleMt":{      'var':variables['eleMt'],                                'bins':[10,0,100],   'decor':{"title":"Electron mT Plot",     'x':"m_{T} / GeV",                     'y':"Events", 'log':[0,logy,0]}},
      "absIso":{     'var':variables['absIso'],                               'bins':[4, 0, 20],   'decor':{'title':"Electron absIso Plot", 'x':"I_{abs} / GeV",                   'y':"Events", 'log':[0,logy,0]}},
      "relIso":{     'var':variables['relIso'],                               'bins':[20, 0, 5],   'decor':{'title':"Electron relIso Plot", 'x':"I_{rel}",                         'y':"Events", 'log':[0,logy,0]}},
      "hybIso":{     'var':variables['hybIso'],                               'bins':[10, 0, 25],  'decor':{'title':"Electron hybIso Plot", 'x':"HI = I_{rel}*min(p_{T}, 25 GeV)", 'y':"Events", 'log':[0,logy,0]}},
      "hybIso2":{    'var':"(log(1 + " + variables['hybIso'] + ")/log(1+5))", 'bins':[8, 0, 4],    'decor':{'title':"Electron hybIso Plot", 'x':"log(1+HI)/log(1+5)",              'y':"Events", 'log':[0,logy,0]}},
      "absDxy":{     'var':variables['absDxy'],                               'bins':[4, 0, 0.04], 'decor':{'title':"Electron |dxy| Plot" , 'x':"|dxy|",                           'y':"Events", 'log':[0,logy,0]}},
      "delPhi":{     'var':"vetoJet_dPhi_j1j2",                               'bins':[8, 0, 3.14], 'decor':{'title':"deltaPhi(j1,j2) Plot", 'x':"#Delta#phi(j1,j2)",               'y':"Events", 'log':[0,logy,0]}},
      "sigmaEtaEta":{'var':variables['sigmaEtaEta'],                          'bins':[6,0,0.03],   'decor':{"title":"#sigma#eta#eta Plot",  'x':"#sigma#eta#eta",                  'y':"Events", 'log':[0,logy,0]}},
      "hOverE":{     'var':variables['hOverE'],                               'bins':[10,0,0.2],   'decor':{"title":"H/E Plot",             'x':"H/E" ,                            'y':"Events", 'log':[0,logy,0]}},
      "MET":{        'var':"met",                                             'bins':[50,0,500],   'decor':{'title':"MET Plot",             'x':"Missing E_{T} / GeV",             'y':"Events", 'log':[0,logy,0]}},
      "HT":{         'var':"ht_basJet",                                       'bins':[50,0,500],   'decor':{'title':"HT Plot",              'x':"H_{T} / GeV",                     'y':"Events", 'log':[0,logy,0]}},
      "weight":{     'var':"weight",                                          'bins':[20,0,400],   'decor':{'title':"Weight Plot",          'x':"Event Weight",                    'y':"Events", 'log':[0,1,0]}}}
   
   #setEventListToChains(samples, samplesList, QCD[plotReg][sel])

   #plotsList = ["hybIso2", "absDxy", "delPhi"]
   #plotsList = ["hybIso2", "sigmaEtaEta", "weight"]
   #plotsList = ["hybIso2", "absDxy", "delPhi", "sigmaEtaEta", "MET", "weight"]
   plotsList = ["elePt", "absIso", "relIso","hybIso", "hybIso2", "absDxy", "delPhi", "eleMt", "MET", "HT", "sigmaEtaEta", "hOverE", "weight"]
   plotsDict = Plots(**plotDict)
   
   plots = {}
   plots2 = {}
   
   for sel in plotRegions:
      plots[sel] = getPlots(samples, plotsDict, QCD[plotReg][sel], samplesList, plotList = plotsList, addOverFlowBin='upper')
      if getData: plots2[sel] = drawPlots(samples, plotsDict, QCD[plotReg][sel], samplesList, plotList = plotsList, denoms=["bkg"], noms = ["dblind"], fom="RATIO", fomLimits=[0,1.8], plotMin = 1, normalize = False, save=False)
      else: plots2[sel] = drawPlots(samples, plotsDict, QCD[plotReg][sel], samplesList, plotList = plotsList, plotMin = 1, normalize = False, save=False)
   
      #Save canvas
      if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
      
         makeDir("%s/%s/root"%(plotdir, sel.replace("X", Xs[ABCD])))
         makeDir("%s/%s/pdf"%(plotdir, sel.replace("X", Xs[ABCD])))

         for canv in plots2[sel]['canvs']:
            #if plot['canvs'][canv][0]:
            plots2[sel]['canvs'][canv][0].SaveAs("%s/%s/%s%s_%s.png"%(plotdir, sel.replace("X", Xs[ABCD]), canv, suffix2, sel.replace("X", Xs[ABCD])))
            plots2[sel]['canvs'][canv][0].SaveAs("%s/%s/root/%s%s_%s.root"%(plotdir, sel.replace("X", Xs[ABCD]), canv, suffix2, sel.replace("X", Xs[ABCD])))
            plots2[sel]['canvs'][canv][0].SaveAs("%s/%s/pdf/%s%s_%s.pdf"%(plotdir, sel.replace("X", Xs[ABCD]), canv, suffix2, sel.replace("X", Xs[ABCD])))
