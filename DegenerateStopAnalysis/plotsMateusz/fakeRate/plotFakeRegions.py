# plotFakeRegions.py
# Plots of regions for fake rate estimation 
# Mateusz Zarucki 2017

import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style, makeDir
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from pprint import pprint
from array import array
from math import pi, sqrt #cos, sin, sinh, log
from fakeRegions import regions, binning

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--lep", dest = "lep",  help = "Lepton", type = str, default = "lep")
parser.add_argument("--region", dest = "region",  help = "Measurement or application region", type = str, default = "measurement")
parser.add_argument("--getData", dest = "getData",  help = "Get data", type = int, default = 1)
parser.add_argument("--WP", dest = "WP",  help = "Loose or Tight WP", type = str, default = "tight")
parser.add_argument("--doPlots", dest = "doPlots",  help = "Plot", type = int, default = 1)
parser.add_argument("--varBins", dest = "varBins",  help = "Variable bin size", action = "store_true")
parser.add_argument("--logy", dest = "logy",  help = "Toggle logy", type = int, default = 1)
parser.add_argument("--save", dest="save",  help="Toggle save", type=int, default=1)
parser.add_argument("--verbose", help="Verbosity switch", action = "store_true")
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
lep = args.lep
region = args.region
getData = args.getData
WP = args.WP
doPlots = args.doPlots
varBins = args.varBins
logy = args.logy
save = args.save
verbose = args.verbose

#Samples
cmgPP = cmgTuplesPostProcessed()

if "measurement" in region:
   skim = "oneLepGood"
   samplesList = ["w", "tt", "qcd"]
   fom = "RATIO"
elif "application" in region:
   skim = "preIncLep"
   samplesList = ["st", "vv", "qcd", "z", "dy", "tt", "w"]
   getData = False #NOTE: For now, do not plot data near SR
   fom = False

if getData and "measurement" in region: 
   samplesList.append("djetBlind")

samples = getSamples(cmgPP = cmgPP, skim = skim, sampleList = samplesList, scan = False, useHT = True, getData = getData)

if verbose:
   print makeLine()
   print "Using samples:"
   newLine()
   for s in samplesList:
      if s: print samples[s].name,":",s
      else:
         print "!!! Sample " + sample + " unavailable."
         sys.exit()

if lep == "el":    lepton = "Electron" #pdgId = "11"
elif lep == "mu":  lepton = "Muon" #pdgId = "13"
elif lep == "lep": lepton = "Lepton"
      
#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/fakesEstimation"%tag

   savedir += "/%s/distribution/%s"%(region, lepton)

   if not varBins: savedir += "/fixedBins"
   else:           savedir += "/varBins"

   if logy: savedir += "/log"
   
   suffix = "_%s_%s"%(lep, WP)
   
   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")
  
selection = regions(region, lep)
setEventListToChains(samples, samplesList, selection[region])

if verbose:
   print makeLine()
   print "Using the following selection: \n",
   pprint(selection)
   print "\n",
   print region, "= \n",
   pprint(selection[region].fullList)
   print makeLine()

index = selection['index']

variables = {\
   'pt':"LepGood_pt[%s]"%index[WP],
   'eta':"abs(LepGood_eta[%s])"%index[WP],
   'mt':"LepGood_mt[%s]"%index[WP],
   'absIso':"LepGood_absIso03[%s]"%index[WP],
   'relIso':"LepGood_relIso03[%s]"%index[WP],
   'hybIso':"(LepGood_relIso03[{ind}]*min(LepGood_pt[{ind}], 25))".format(ind = index[WP]),
}
   
variables['hybIso2'] = "(log(1 + " + variables['hybIso'] + ")/log(1+5))"

regionCuts = CutClass("regionCuts", [
   ["WP", selection[WP]],
   ], baseCut = selection[region])

bins = binning(lep, varBins = varBins)

plotDict = {\
   "ht":{     'var':"ht_basJet_def",      'bins':[50,0,1000], 'decor':{'title':"H_{{T}} Plot" , "y":"Events", "x":"H_{T} / GeV", "log":[0,logy,0]}},
   "met":{    'var':"met",                'bins':[30,0,300],  'decor':{'title':"MET Plot" ,     "y":"Events", "x":"MET / GeV",   "log":[0,logy,0]}},
   "lepPt":{  'var':variables['pt'],      'bins':bins['pt'],  'decor':{'title':"Lepton p_{{T}} Plot", "y":"Events", "x":"%s %s p_{T} / GeV"%(WP.title(),lepton), "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['pt'][1]-bins['pt'][0])},
   "lepEta":{ 'var':variables['eta'],     'bins':bins['eta'], 'decor':{'title':"Lepton |#eta| Plot",  "y":"Events", "x":"%s %s |#eta|"%(WP.title(),lepton),      "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['pt'][1]-bins['pt'][0])}, 
   "lepMt":{  'var':variables['mt'],      'bins':bins['mt'],  'decor':{'title':"Lepton m_{{T}} Plot", "y":"Events", "x":"%s %s m_{T} / GeV"%(WP.title(),lepton), "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['pt'][1]-bins['pt'][0])}, 
   "absIso":{ 'var':variables['absIso'],  'bins':[4, 0, 20],  'decor':{'title':"Lepton absIso Plot", 'x':"%s %s I_{abs} / GeV"%(WP.title(),lepton),                   'y':"Events", 'log':[0,logy,0]}},
   "relIso":{ 'var':variables['relIso'],  'bins':[20, 0, 5],  'decor':{'title':"Lepton relIso Plot", 'x':"%s %s I_{rel}"%(WP.title(),lepton),                         'y':"Events", 'log':[0,logy,0]}},
   "hybIso":{ 'var':variables['hybIso'],  'bins':[10, 0, 25], 'decor':{'title':"Lepton hybIso Plot", 'x':"%s %s HI = I_{rel}*min(p_{T}, 25 GeV)"%(WP.title(),lepton), 'y':"Events", 'log':[0,logy,0]}},
   "hybIso2":{'var':variables['hybIso2'], 'bins':[8, 0, 4],   'decor':{'title':"Lepton hybIso Plot", 'x':"%s %s log(1+HI)/log(1+5)"%(WP.title(),lepton),              'y':"Events", 'log':[0,logy,0]}},
}

if "application" in region:
   if logy: plotMin = 10
   else: plotMin = 0
   if not varBins: plotDict['met']['bins'] = [100, 0, 1000]
elif "measurement" in region:
   plotMin = 100

plotsDict = Plots(**plotDict)
plotsList = ["lepPt", "lepMt", "lepEta"]
if not varBins: plotsList.extend(["met", "ht", "absIso", "relIso", "hybIso", "hybIso2"])

#Sets TDR style
setup_style()

c1 = ROOT.TCanvas("c1", "Canvas 1", 1200, 1700)

if doPlots:   
   plots = getPlots(samples, plotsDict, regionCuts, samplesList, plotList = plotsList, addOverFlowBin='both')
   
   fakePlots = drawPlots(samples, plotsDict, regionCuts, samplesList, plotList = plotsList, plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["djetBlind"], fom = fom, fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)
   
   if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
      for canv in fakePlots['canvs']:
         fakePlots['canvs'][canv][0].SaveAs("%s/%s%s.png"%(savedir, canv, suffix))
         fakePlots['canvs'][canv][0].SaveAs("%s/root/%s%s.root"%(savedir, canv, suffix))
         fakePlots['canvs'][canv][0].SaveAs("%s/pdf/%s%s.pdf"%(savedir, canv, suffix))
