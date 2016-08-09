#ttPtReweight.py
import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style
#from Workspace.DegenerateStopAnalysis.tools.bTagWeights import bTagWeights
#from Workspace.DegenerateStopAnalysis.tools.degCuts import *
from Workspace.DegenerateStopAnalysis.tools.weights import Weights
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.tools.getSamples_8011 import getSamples

from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Sets TDR style
setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--getData", dest = "getData",  help = "Get data samples", type = int, default = 1)
parser.add_argument("--ttPtReweight", dest = "ttPtReweight",  help = "ttPtReweight", type = str, default = "")
parser.add_argument("--doYields", dest = "doYields",  help = "Calulate yields", type = int, default = 0)
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
ttPtReweight = args.ttPtReweight
doYields = args.doYields
logy = args.logy
save = args.save
verbose = args.verbose

print makeDoubleLine()
print "Performing tt pt reweighting calculation"
print makeDoubleLine()

#Samples
cmgPP = cmgTuplesPostProcessed()
samplesList = ["vv", "st", "qcd", "z", "dy", "tt", "w"]
if getData: 
   data = "dblind"
   samplesList.append(data)

weights_ = Weights(lepCol = "LepAll", ttpt = ttPtReweight) 
weights     = weights_.weights
def_weights = weights_.def_weights

samples = getSamples(cmgPP = cmgPP, skim = "preIncLep", sampleList = samplesList, scan = False, useHT = True, getData = getData, weights = weights, def_weights = def_weights) 

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
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/ttPtReweight"
   if ttPtReweight: suffix = "_ttPtReweighted"
   else: suffix = ""   
   if not os.path.exists("%s/root"%(savedir)): os.makedirs("%s/root"%(savedir))
   if not os.path.exists("%s/pdf"%(savedir)): os.makedirs("%s/pdf"%(savedir))


#Geometric cuts
#etaAcc = 2.1
#ebSplit = 0.8 #barrel is split into two regions
#ebeeSplit = 1.479 #division between barrel and endcap

presel = CutClass("presel", [
   ["MET200", "met > 200"],
   ["HT300", "ht_basJet > 300"],
   ["ISR100", "nIsrJet >= 1"],
   ["No3rdJet60","nVetoJet<=2"],
   ["AntiQCD", "(vetoJet_dPhi_j1j2 < 2.5)"],
   ["TauVeto","Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
   ["lep30Veto-2lep20Veto", "((nLepAll_lep == 1) || (nLepAll_lep == 2 && LepAll_pt[IndexLepAll_lep[1]] < 20))"],
   ], baseCut = None)

plotDict = {
   "ht":           {'var':"ht_basJet"                     ,"bins":[40,200,1000]        ,"nMinus1":""           ,"decor":{"title":"HT"    ,"x":"H_{T}"      ,"y":"Events"  ,'log':[0,1,0] }},
   "met":          {'var':"met"                            ,"bins":[40,200,1000]        ,"nMinus1":"met"        ,"decor":{"title":"MET"    ,"x":"E^{miss}_{T}"      ,"y":"Events"  ,'log':[0,1,0] }},
   "ct":           {'var':"min(met_pt,ht_basJet)"         ,"bins":[40,100,1000]        ,"nMinus1":""           ,"decor":{"title":"CT"    ,"x":"C_{T}"      ,"y":"Events"  ,'log':[0,1,0] }},
   #"wpt":          {'var':wpt                            ,"bins":[40,200,1000]        ,"nMinus1":""        ,"decor":{"title":"WPT"    ,"x":"P_{T}(W)"      ,"y":"Events"  ,'log':[0,1,0] }},
   #"lep_mt":           {'var':"LepAll_mt[IndexLepAll_lep[0]]"       ,"bins":[40,0,200]          ,"nMinus1":None         ,"decor":{"title":"lepMT"    ,"x":"M_{{T}}({lepLatex}) "      ,"y":"Events"  ,'log':[0,1,0] }},
   #"lep_Pt" :        {'var':"LepAll_pt[IndexLepAll_lep[0]]"       ,"bins":[40,0,200]          ,"nMinus1":""      ,"decor":{"title":"lepPt"           ,"x":"P_{{T}}({lepLatex})"      ,"y":"Events"  ,'log':[0,1,0] }},
   #"lep_Eta" :       {'var':"LepAll_eta[IndexLepAll_lep[0]]"                         ,"bins":[20,-3,3]           ,"nMinus1":""         ,"decor":{"title":"lepEta"     ,"x":"#eta({lepLatex})"       ,"y":"Events  "  ,'log':[0,1,0] }},
   #"lep_Phi" :      {'var':"LepAll_phi[IndexLepAll_lep[0]]"                         ,"bins":[20,-3.15,3.15]           ,"nMinus1":None         ,"decor":{"title":"lepPhi"     ,"x":"lep Phi"      ,"y":"Events  "  ,'log':[0,1,0] }},
   #"MetPhi":       {'var':"met_phi"                        ,"bins":[20,-3.15,3.15]           ,"nMinus1":None         ,"decor":{"title":"MetPhi"    ,"x":"Met Phi"      ,"y":"Events"  ,'log':[0,1,0] }},
   #"isrPt":        {'var':"Jet_pt[IndexJet_basJet[0]]"     ,"bins":[45,100,1000]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet P_{{T}}"    ,"x":"isrJetPt"      ,"y":"Events  "  ,'log':[0,1,0] }},
   #"isrPt2":       {'var':"Jet_pt[IndexJet_basJet[0]]"     ,"bins":[20,100,900]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet P_{{T}}"    ,"x":"isrJetPt"      ,"y":"Events  "  ,'log':[0,1,0] }},
   #"isrPt_fine":   {'var':"Jet_pt[IndexJet_basJet[0]]"    ,"bins":[100,0,1000]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet P_{{T}} "    ,"x":"isrJetPt"      ,"y":"Events  "  ,'log':[0,1,0] }},
   #"nJets30":      {'var':"nBasJet"                       ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 30GeV"    ,"x":"Number of Jets with P_{T} > 30GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
   #"nJets60":      {'var':"nVetoJet"                      ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 60GeV"    ,"x":"Number of Jets with P_{T} > 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
   #"nSoftBJets":   {'var':"(nBSoftJet)"                   ,"bins":[6,0,6]            ,"nMinus1":None         ,"decor":{"title":"Number of Soft B-Tagged Jets with P_{{T}} < 60GeV"    ,"x":"Number of Soft B-Tagged Jets with P_{T} < 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
   #"nHardBJets":   {'var':"(nBHardJet)"                   ,"bins":[6,0,6]            ,"nMinus1":None         ,"decor":{"title":"Number of B-Tagged Jets with P_{{T}} > 60GeV"    ,"x":"Number of Hard B-Tagged Jets with P_{T} > 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
   #"nBJets":       {'var':"(nBHardJet + nBSoftJet)"       ,"bins":[6,0,6]            ,"nMinus1":None         ,"decor":{"title":"Number of B-Tagged Jets"                         ,"x":"Number of B-Tagged Jets"      ,"y":"Events  "  ,'log':[0,1,0] }},
   #"bJetPt":       {'var':"Jet_pt[ max(IndexJet_bJet[0],0)] *(nBJet>0)"      ,"bins":[100,0,1000]          ,"nMinus1":None         ,"decor":{"title":"bJet P_{{T}} "    ,"x":"P_{T}(BJet)"      ,"y":"Events  "  ,'log':[0,1,0] }},
   #"bSoftJetPt":       {'var':"Jet_pt[ max(IndexJet_bSoftJet[0],0)] *(nBSoftJet>0)"      ,"bins":[10,20,70]          ,"nMinus1":None         ,"decor":{"title":"bSoftJet P_{{T}} "    ,"x":"P_{T}(Soft BJet)"      ,"y":"Events  "  ,'log':[0,1,0] }},
   #"bHardJetPt":       {'var':"Jet_pt[ max(IndexJet_bHardJet[0],0)] *(nBHardJet>0)"      ,"bins":[100,0,1000]          ,"nMinus1":None         ,"decor":{"title":"bHardJet P_{{T}} "    ,"x":"P_{T}(Hard BJet)"      ,"y":"Events  "  ,'log':[0,1,0] }},
   }

setEventListToChains(samples, samplesList, presel)
   
plotsList = ["ht", "met", "ct"]

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
