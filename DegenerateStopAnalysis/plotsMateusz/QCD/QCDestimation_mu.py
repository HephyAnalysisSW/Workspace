# QCDestimation_mu.py
# Combined script for the QCD estimation for muon channel 
# ABCD3: 2D ABCD with loosened MET

import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
#from Workspace.DegenerateStopAnalysis.toolsMateusz.eleWPs import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setup_style
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
print "Performing QCD estimation for the muon channel."
print makeDoubleLine()
   
if METcut != METloose: ABCD = "3"
else: ABCD = "2D"

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/muon"
 
   savedir += "/bTagWeight_" + btag
     
   estdir = savedir + "/estimation"
   
   plotdir = savedir + "/plots"
   plotdir += "/" + plotReg
   
   if ABCD == "3": 
      estdir += "/METloose"
      plotdir += "/METloose"
   elif ABCD == "2D": 
      estdir += "/noMETloose"
      plotdir += "/noMETloose"
   
   suffix = "_HT" + HTcut + "_MET" + METcut
   plotdir += "/HT" + HTcut + "MET" + METcut
   
   if ABCD == "3": 
      plotdir += "METloose" + METloose
      suffix += "_METloose" + METloose

   if plot: suffix += "_" + plotReg
   #if enriched == True: suffix += "_EMenriched"
   
   if highWeightVeto: 
      estdir += "/highWeightVeto" 
      plotdir += "/highWeightVeto"
      suffix += "_highWeightVeto"
 
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

#Index of leading muon
#NOTE: selection is implicit to index -> dependent on tuples!
ind = "IndexLepAll_mu2[0]" #index sel: no hybIso cut

#Geometric cuts
etaAcc = 2.1
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap

#selection on leading muon
muSel = "abs(LepAll_pdgId[" + ind + "]) == 13 && abs(LepAll_eta[" + ind + "]) < " + str(etaAcc) #NOTE: pdg cut redundant as included in index

#Common QCD cuts
hybIsoCut = "(LepAll_relIso03[" + ind + "]*min(LepAll_pt[" + ind + "], 25)) < 5" #hybIsoCut = "((LepAll_absIso03 < 5) || LepAll_relIso03 < 0.2))"
antiHybIsoCut = "(LepAll_relIso03[" + ind + "]*min(LepAll_pt[" + ind + "], 25)) > 5" #antiHybIsoCut = "((LepAll_absIso03 > 5) && (LepAll_relIso03 > 0.2))"
dPhiCut = "vetoJet_dPhi_j1j2 < 2.5"# || nVetoJet <= 1" #unnecessary as value set to -999 for monojet evts
antidPhiCut = "(vetoJet_dPhi_j1j2 > 2.5 || nVetoJet <= 1)" #or required for inclusion of monojet evts

#Differing QCD cuts

variables = {'muPt':"LepAll_pt[" + ind + "]", 'muMt':"LepAll_mt[" + ind + "]"}

if plot: variables.update({"absIso":"LepAll_absIso03[" + ind + "]", 'relIso':"LepAll_relIso03[" + ind + "]", "hybIso":"(LepAll_relIso03[" + ind + "]*min(LepAll_pt[" + ind + "], 25))", "absDxy":"LepAll_dxy[" + ind + "]"})

#Redefining variables in terms of muon selection
# ABCD1: X = D (inverted) | ABCD2: X = D (loose) | ABCD3: X = M (loose)
Xs = {'1':'D', '2':'D', '3':'M', '2D':''}

if METloose == METcut: METcutString = "met >" + METcut
elif ABCD == "3": METcutString = "met >" + METloose #loosened MET cut for ABCD3

print "MET cut string: ", METcutString

#bTagWeights
bWeightDict = bTagWeights(btag)
bTagString = bWeightDict['sr1_bjet'] #corresponds to bVeto

#Preselection & basic SR cuts
presel = CutClass("presel_SR", [
   ["HT","ht_basJet >" + HTcut],
   ["MET", METcutString],
   ["ISR100", "nIsrJet >= 1"],
   ["nMu", "(nLepAll_mu2 == 1 || (nLepAll_mu2 == 2 && LepAll_pt[IndexLepAll_mu2[1]] < 20))"],
   ["ElVeto","(nLepAll_el == 0 || (nLepAll_el == 1 && LepAll_pt[IndexLepAll_el[0]] < 20))"], 
   ["muSel", muSel],
   ["No3rdJet60","nVetoJet <= 2"],
   ["BVeto", bTagString],
   ["TauVeto","Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
   ["HighWeightVeto","weight < " + weightCut],
   ], baseCut = None)

abcd = {'SR':'I', 'A_IX': 'I', 'IX_A':'anti-I', 'IXA':'anti-I'}

SRs ={}

SRs = {\
   'SR1':["SR1","LepAll_pt[" + ind + "] < 30"],
   'SR1a':["SR1a", combineCuts("LepAll_mt[" + ind + "] < 60", "LepAll_pt[" + ind + "] < 30")],
   'SR1b':["SR1b", combineCuts(btw("LepAll_mt[" + ind + "]", 60, 95), "LepAll_pt[" + ind + "] < 30")],
   'SR1c':["SR1c", combineCuts("LepAll_mt[" + ind + "] > 95", "LepAll_pt[" + ind + "] < 30")],

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
   QCD_IX_A = {}
   QCD_A_IX = {}
   
   QCD_IXA_MC = {}
   QCD_IXA_data = {}
   SF_IXA_dataMC = {}
   QCDest_MC = {}
   QCDest = {}
   if save: 
      if not os.path.isfile("%s/QCDyields%s.txt"%(estdir,suffix)):
         outfile = open("%s/QCDyields%s.txt"%(estdir,suffix), "w")
         outfile.write("QCD Estimation for Muon Channel [Preselection of (MET, HT) > (" + METcut + "," + HTcut + ")]\n")
         outfile.write("SR           IX_A                 A_IX           |          IXA (Data-EWK)              IXA (MC)             SF_IXA_dataMC          |      QCD Est.               SR (QCD MC)                  Ratio\n".replace("X", Xs[ABCD]))
   
   for reg in regions:
      yields[reg] = {}
      for sel in abcd:
         yields[reg][sel] = Yields(samples, samplesList, QCD[reg][sel], cutOpt = "combinedList", pklOpt = False, tableName = reg + "_" + sel, nDigits = 2, err = True, verbose = True, nSpaces = 1)
  
      if yields[reg]['IXA'].yieldDictFull['qcd']['QCD_IXA_' + reg].val:
      
         QCD_IX_A[reg] =      yields[reg]['IX_A'].yieldDictFull['qcd']['QCD_IX_A_' + reg]
         QCD_A_IX[reg] =      yields[reg]['IA_X'].yieldDictFull['qcd']['QCD_IA_X_' + reg]
         QCD_IXA_MC[reg] =    yields[reg]['IXA'].yieldDictFull['qcd']['QCD_IXA_' + reg]
         QCD_IXA_data[reg] =  yields[reg]['IXA'].yieldDictFull['dblind']['QCD_IXA_' + reg] - \
                              yields[reg]['IXA'].yieldDictFull['w']['QCD_IXA_' + reg] - \
                              yields[reg]['IXA'].yieldDictFull['tt']['QCD_IXA_' + reg] - \
                              yields[reg]['IXA'].yieldDictFull['z']['QCD_IXA_' + reg] - \
                              yields[reg]['IXA'].yieldDictFull['st']['QCD_IXA_' + reg] - \
                              yields[reg]['IXA'].yieldDictFull['vv']['QCD_IXA_' + reg]
         
         
         #Estimation from pure QCD MC 
         QCDest_MC[reg] = ((QCD_IX_A[reg] * QCD_A_IX[reg])/(QCD_IXA_MC[reg]))

         SF_IXA_dataMC[reg] = (QCD_IXA_data[reg]/QCD_IXA_MC[reg]) 
         
         #Full estimation 
         QCDest[reg] = SF_IXA_dataMC[reg]*QCDest_MC[reg]
         
         #Estimation from pure QCD MC
         if verbose: 
            print makeLine()
            print "Region: ", reg
            print "QCD MC in IX_A = ".replace("X", Xs[ABCD]), QCD_IX_A[reg] 
            print "QCD MC in A_IX = ".replace("X", Xs[ABCD]), QCD_A_IX[reg] 
            print "data | MC in IXA = ".replace("X", Xs[ABCD]),  QCD_IXA_data[reg], "   |   ", QCD_IXA_MC[reg] 
            print "SF_dataMC in IXA = ", SF_IXA_dataMC[reg] 
            print "QCD Estimation in ", reg, ": ", QCDest[reg], " (", QCDest_MC[reg], ")"
            print "QCD MC yield in ", reg, ": ", yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg]
            if yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg].val:
               print "Closure ratio: ", QCDest[reg]/yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg]
            print makeLine()
   
         with open("%s/QCDyields%s.txt"%(estdir,suffix), "a") as outfile:
            outfile.write(reg + "     " +\
            str(QCD_IX_A[reg].round(2)) + "             " +\
            str(QCD_A_IX[reg].round(2)) + "             " +\
            str(QCD_IXA_data[reg].round(2)) + "             " +\
            str(QCD_IXA_MC[reg].round(2)) + "             " +\
            str(SF_IXA_dataMC[reg].round(2)) + "             " +\
            str(QCDest[reg].round(2)) + "             " +\
            str(yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg].round(2)) + "             ")
            if yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg].val:
               outfile.write(str((QCDexp[reg]/yields[reg]['SR'].yieldDictFull['qcd']['QCD_SR_' + reg]).round(2)) + "\n")
            else:
               outfile.write("\n")

abcd = {'SR':'I', 'A_IX': 'I', 'IX_A':'anti-I', 'IXA':'anti-I'}

if plot:
   
   QCD[plotReg]['X_A'] = CutClass("QCD_X_A_" + plotReg, [ #loose MET
      SRs[plotReg],
      ["A", dPhiCut], #applied
      ], baseCut = presel)
   
   QCD[plotReg]['A_X'] = CutClass("QCD_A_X_" + plotReg, [
      SRs[plotReg],
      ["anti-A", antidPhiCut], #inverted
      ["MET", "met >" + METcut], #tight MET
      ], baseCut = presel)
   
   plotsList = {}
   plotDict = {}
   plotsDict = {}
   plots = {}
   plots2 = {}
   
   plotRegions = ['SR', 'X_A', 'A_X', 'A_IX', 'IX_A', 'IXA']
  
   if getData: plotRegions.remove('SR')
   
   for sel in plotRegions:
      plotDict[sel] = {\
         "muPt_" + sel:{'var':variables['muPt'], "bins":[10, 0, 50], "decor":{"title": "Muon pT Plot" ,"x":"Muon p_{T} / GeV" , "y":"Events", 'log':[0, logy,0]}},
         "absIso_" + sel:{'var':variables['absIso'], "bins":[4, 0, 20], "decor":{"title": "Muon absIso Plot" ,"x":"I_{abs} / GeV" , "y":"Events", 'log':[0,logy,0]}},
         "relIso_" + sel:{'var':variables['relIso'], "bins":[20, 0, 5], "decor":{"title": "Muon relIso Plot" ,"x":"I_{rel}" , "y":"Events", 'log':[0,logy,0]}},
         "hybIso_" + sel:{'var':variables['hybIso'], "bins":[10, 0, 25], "decor":{"title": "Muon hybIso Plot" ,"x":"HI = I_{rel}*min(p_{T}, 25 GeV)" , "y":"Events", 'log':[0,logy,0]}},
         "hybIso2_" + sel:{'var':"(log(1 + " + variables['hybIso'] + ")/log(1+5))", "bins":[8, 0, 4], "decor":{"title": "Muon hybIso Plot" ,"x":"log(1+HI)/log(1+5)" , "y":"Events", 'log':[0,logy,0]}},
         "absDxy_" + sel:{'var':variables['absDxy'], "bins":[4, 0, 0.04], "decor":{"title": "Muon |dxy| Plot" ,"x":"|dxy|" , "y":"Events", "log":[0,logy,0]}},
         "delPhi_" + sel:{'var':"vetoJet_dPhi_j1j2", "bins":[8, 0, 3.14], "decor":{"title": "deltaPhi(j1,j2) Plot" ,"x":"#Delta#phi(j1,j2)" , "y":"Events", 'log':[0,logy,0]}},
         "muMt_" + sel:{'var':variables['muMt'], "bins":[10,0,100], "decor":{"title": "Muon mT Plot" ,"x":"m_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
         "MET_" + sel:{'var':"met", "bins":[50,0,500], "decor":{"title": "MET Plot" ,"x":"Missing E_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
         "HT_" + sel:{'var':"ht_basJet", "bins":[50,0,500], "decor":{"title": "HT Plot","x":"H_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
         "weight_" + sel:{'var':"weight", "bins":[20,0,400], "decor":{"title": "Weight Plot","x":"Event Weight" , "y":"Events", 'log':[0,1,0]}}
      }
      
      #plotsList[sel] = ["hybIso2_" + sel, "absDxy_" + sel, "delPhi_" + sel, "weight_" + sel]
      plotsList[sel] = ["muPt_" + sel, "absIso_" + sel, "relIso_" + sel,"hybIso_" + sel, "hybIso2_" + sel, "absDxy_" + sel, "delPhi_" + sel, "muMt_" + sel, "MET_" + sel, "HT_" + sel, "weight_" + sel]
      plotsDict[sel] = Plots(**plotDict[sel])
      plots[sel] = getPlots(samples, plotsDict[sel], QCD[plotReg][sel], samplesList, plotList = plotsList[sel], addOverFlowBin='upper')
      if getData: plots2[sel] = drawPlots(samples, plotsDict[sel], QCD[plotReg][sel], samplesList, plotList = plotsList[sel], denoms=["bkg"], noms = ["dblind"], fom="RATIO", fomLimits=[0,2.8], plotMin = 1, normalize = False, save=False)
      else: plots2[sel] = drawPlots(samples, plotsDict[sel], QCD[plotReg][sel], samplesList, plotList = plotsList[sel], plotMin = 1, normalize = False, save=False)
      
      #Save canvas
      if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
      
         if not os.path.exists("%s/%s/root"%(plotdir, sel.replace("X", Xs[ABCD]))): os.makedirs("%s/%s/root"%(plotdir, sel.replace("X", Xs[ABCD])))
         if not os.path.exists("%s/%s/pdf"%(plotdir, sel.replace("X", Xs[ABCD]))): os.makedirs("%s/%s/pdf"%(plotdir, sel.replace("X", Xs[ABCD])))

         for canv in plots2[sel]['canvs']:
            #if plot['canvs'][canv][0]:
            plots2[sel]['canvs'][canv][0].SaveAs("%s/%s/%s%s.png"%(plotdir, sel.replace("X", Xs[ABCD]), canv, suffix))
            plots2[sel]['canvs'][canv][0].SaveAs("%s/%s/root/%s%s.root"%(plotdir, sel.replace("X", Xs[ABCD]), canv, suffix))
            plots2[sel]['canvs'][canv][0].SaveAs("%s/%s/pdf/%s%s.pdf"%(plotdir, sel.replace("X", Xs[ABCD]), canv, suffix))
