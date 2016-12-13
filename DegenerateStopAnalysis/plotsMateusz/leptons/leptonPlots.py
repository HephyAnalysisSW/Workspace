# leptonPlots.py
# Script for making basic lepton plots using the Sum$ method
# Mateusz Zarucki 2016

import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style
from Workspace.DegenerateStopAnalysis.tools.bTagWeights import bTagWeights
#from Workspace.DegenerateStopAnalysis.tools.degCuts import *
from Workspace.DegenerateStopAnalysis.tools.getSamples_8012 import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Sets TDR style
setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--getData", dest = "getData",  help = "Get data samples", type = int, default = 1)
parser.add_argument("--getSignal", dest = "getSignal",  help = "Get signal samples", type = int, default = 1)
parser.add_argument("--doYields", dest = "doYields",  help = "Calulate yields", type = int, default = 0)
parser.add_argument("--lep", dest = "lep",  help = "Lepton", type = str, default = "el")
parser.add_argument("--btag", dest = "btag",  help = "B-tagging option", type = str, default = "")
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
getData = args.getData
getSignal = args.getSignal
doYields = args.doYields
btag = args.btag
lep = args.lep
logy = args.logy
save = args.save
verbose = args.verbose

print makeDoubleLine()
print "Plotting lepton distributions"
print makeDoubleLine()

#Samples
cmgPP = cmgTuplesPostProcessed()
samplesList = ["vv", "st", "qcd", "z", "dy", "tt", "w"]
if getData: 
   data = "dblind"
   samplesList.append(data)

if getSignal: 
   samplesList.extend(['s300_270', 's300_290', 's300_220'])

samples = getSamples(cmgPP = cmgPP, skim = "preIncLep", sampleList = samplesList, scan = getSignal, useHT = True, getData = getData) 

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
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/leptonPlots/%s"%(tag,lep)
   
   #if btag: savedir += "/" + btag
   #else: savedir += "/no_btag"
   suffix = ""   
   if not os.path.exists("%s/root"%(savedir)): os.makedirs("%s/root"%(savedir))
   if not os.path.exists("%s/pdf"%(savedir)): os.makedirs("%s/pdf"%(savedir))

if btag:
   bWeightDict = bTagWeights(btag)
   bTagString = bWeightDict['sr1_bjet']
else:
   bTagString = "1"

#degcuts = Cuts("LepAll", "lep", sr1c_opt = "MT95_IncCharge", isrpt = 100, btag = 'sf')


#Geometric cuts
if lep == "el":
   pdgId = "11"
   etaAcc = "2.5"
   ID = "SPRING15_25ns_v1"
elif lep == "mu":
   pdgId = "13"
   etaAcc = "2.4"
   ID = "looseMuonId"

lepSel = "(abs(LepAll_pdgId) == %s && abs(LepAll_eta) < %s  && LepAll_%s >= 1)"%(pdgId, etaAcc, ID)

print lepSel

presel = CutClass("presel", [
   ["MET200", "met > 200"],
   ["HT300", "ht_basJet > 300"],
   ["ISR100", "nIsrJet >= 1"],
   ["No3rdJet60","nVetoJet<=2"],
   ["AntiQCD", "(vetoJet_dPhi_j1j2 < 2.5)"],
   ["TauVeto","Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
   ["lep", "Sum$(" + lepSel + ") == 1"],
   #["pt5", varSel("LepAll_pt", lepSel) + "> 5"],
   #["lep30Veto-2lep20Veto", "((nLepAll_lep == 1) || (nLepAll_lep == 2 && LepAll_pt[IndexLepAll_lep[1]] < 20))"],
   #["BVeto", bTagString],
   ], baseCut = None)

print presel.combined

#hybIsoCut = "(LepAll_relIso03*min(LepAll_pt, 25)) < 5" #hybIsoCut = "((LepAll_absIso03 < 5) || LepAll_relIso03 < 0.2))"
#dPhiCut = "vetoJet_dPhi_j1j2 < 2.5"# || nVetoJet <= 1" #unnecessary as value set to -999 for monojet evts
#dxyCut = "abs(LepAll_dxy) < 0.02"

#Reconstructed electron selection
matchSel = "LepAll_mcMatchId != 0"

hybIso = "(LepAll_relIso03*min(LepAll_pt, 25))"

plotDict = {
"pt":     {'var':varSel("LepAll_pt"      , lepSel), "bins":[50,0,100],      "nMinus1":None, "decor":{"title":"pt"            ,"x": "p_{T}"           ,"y":"Events", 'log':[0,1,0]}},
"dxy":    {'var':varSel("LepAll_dxy"     , lepSel), "bins":[40,-0.1,0.1],   "nMinus1":None, "decor":{"title":"dxy"           ,"x": "dxy"             ,"y":"Events", 'log':[0,1,0]}},
#"dxy":    {'var':varSel("LepAll_dxy"     , lepSel), "bins":[40,-0.2,0.2],   "nMinus1":None, "decor":{"title":"dxy"           ,"x": "dxy"             ,"y":"Events", 'log':[0,1,0]}},
"dz":     {'var':varSel("LepAll_dz"      , lepSel), "bins":[30,-0.3,0.3]  , "nMinus1":None, "decor":{"title":"dz"            ,"x": "dz"              ,"y":"Events", 'log':[0,1,0]}},
#"dz":     {'var':varSel("LepAll_dz"      , lepSel), "bins":[30,-0.6,0.6]  , "nMinus1":None, "decor":{"title":"dz"            ,"x": "dz"              ,"y":"Events", 'log':[0,1,0]}},
"pdgId":  {'var':varSel("LepAll_pdgId"   , lepSel), "bins":[40,-20,20]    , "nMinus1":None, "decor":{"title":"pdgId"         ,"x": "pdgId"           ,"y":"Events", 'log':[0,1,0]}},
"relIso": {'var':varSel("LepAll_relIso03", lepSel), "bins":[40,0,1]       , "nMinus1":None, "decor":{"title":"relIso"        ,"x": "relIso"          ,"y":"Events", 'log':[0,1,0]}},
"absIso": {'var':varSel("LepAll_absIso03", lepSel), "bins":[40,0,10]      , "nMinus1":None, "decor":{"title":"absIso"        ,"x": "absIso"          ,"y":"Events", 'log':[0,1,0]}},
"hybIso":{ 'var':varSel(hybIso, lepSel),                               'bins':[10, 0, 25],  'decor':{'title':"Electron hybIso Plot", 'x':"HI = I_{rel}*min(p_{T}, 25 GeV)", 'y':"Events", 'log':[0,logy,0]}},
"hybIso2":{'var':"(log(1 + " + varSel(hybIso, lepSel) + ")/log(1+5))", 'bins':[8, 0, 4],    'decor':{'title':"Electron hybIso Plot", 'x':"log(1+HI)/log(1+5)",              'y':"Events", 'log':[0,logy,0]}},
   }

setEventListToChains(samples, samplesList, presel)
   
plotsList = ["pt", "dxy", "dz", "pdgId", "relIso", "absIso", "hybIso", "hybIso2"]

plotsDict = Plots(**plotDict)

plots = getPlots(samples, plotsDict, presel, samplesList, plotList = plotsList, addOverFlowBin='upper')
plots2 = drawPlots(samples, plotsDict, presel, samplesList, plotList = plotsList, plotLimits = [1, 100], denoms=["bkg"], noms = [data], fom="RATIO", fomLimits=[0,1.8], normalize = False, save=False) #, plotMin = 0.1

if doYields:
   yields = Yields(samples, samplesList, presel, cutOpt = "combinedList", pklOpt = False, tableName = "dataMC", nDigits = 2, err = True, verbose = True, nSpaces = 1)
   
   print makeLine()
   print "Yields"
   for samp in yields.yieldDictFull:
      print samp, ": ", yields.yieldDictFull[samp]

#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
      for canv in plots2['canvs']:
         #if plot['canvs'][canv][0]:
         plots2['canvs'][canv][0].SaveAs("%s/%s%s.png"%(savedir, canv, suffix))
         plots2['canvs'][canv][0].SaveAs("%s/root/%s%s.root"%(savedir, canv, suffix))
         plots2['canvs'][canv][0].SaveAs("%s/pdf/%s%s.pdf"%(savedir, canv, suffix))
