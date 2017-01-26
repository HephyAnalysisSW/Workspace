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
parser.add_argument("--region", dest = "reg",  help = "Measurement or application region", type = str, default = "measurement")
parser.add_argument("--getData", dest = "getData",  help = "Get data", type = int, default = 1)
parser.add_argument("--WP", dest = "WP",  help = "Loose or Tight WP", type = str, default = "tight")
parser.add_argument("--oneBin", help = "One bin", action = "store_true")
parser.add_argument("--doPlots", dest = "doPlots",  help = "Plot", type = int, default = 1)
parser.add_argument("--doYields", help = "Calculate yields", action = "store_true")
parser.add_argument("--doControlPlots", help = "Additional plots of regions", action = "store_true")
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
reg = args.reg
getData = args.getData
WP = args.WP
oneBin = args.oneBin
doPlots = args.doPlots
doYields = args.doYields
doControlPlots = args.doControlPlots
varBins = args.varBins
logy = args.logy
save = args.save
verbose = args.verbose

#Sets TDR style
setup_style()

#Samples
cmgPP = cmgTuplesPostProcessed()

if "measurement" in reg:
   skim = "oneLepGood"
   samplesList = ["w", "tt", "qcd"]
   fom = "RATIO"
elif "application" in reg:
   skim = "preIncLep"
   samplesList = ["st", "vv", "qcd", "z", "dy", "tt", "w"]
   getData = False #NOTE: For now, do not plot data near SR
   fom = False

if getData and "measurement" in reg: 
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

   if oneBin: savedir += "/oneBin"

   if doYields: 
      yieldDir = "%s/%s/yields"%(savedir, reg)
      makeDir(yieldDir)

   savedir += "/%s/distribution/%s"%(reg, lepton)

   if not varBins: savedir += "/fixedBins"
   else:           savedir += "/varBins"

   if logy: savedir += "/log"
   
   suffix = "_%s_%s"%(lep, WP)
   
   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")
  
selection = regions(reg, lep, oneBin = oneBin)
setEventListToChains(samples, samplesList, selection[reg])

if verbose:
   print makeLine()
   print "Using the following selection: \n",
   pprint(selection)
   print "\n",
   print reg, "= \n",
   pprint(selection[reg].fullList)
   print makeLine()

index = selection['index']

variables = {\
   'pt':"LepGood_pt[%s]"%index[WP],
   'eta':"abs(LepGood_eta[%s])"%index[WP],
   'mt':"LepGood_mt[%s]"%index[WP],
   'lepDxy':"abs(LepGood_dxy[%s])"%index[WP],
   'lepDz':"abs(LepGood_dz[%s])"%index[WP],
   'absIso':"LepGood_absIso03[%s]"%index[WP],
   'relIso':"LepGood_relIso03[%s]"%index[WP],
   'hybIso':"(LepGood_relIso03[{ind}]*min(LepGood_pt[{ind}], 25))".format(ind = index[WP]),
   'mcMatchId':"LepGood_mcMatchId[%s]"%index[WP],
   'mcMatchAny':"LepGood_mcMatchAny[%s]"%index[WP],
}
   
variables['hybIso2'] = "(log(1 + " + variables['hybIso'] + ")/log(1+5))"

## Loose (not-Tight) CR
#
#if looseNotTight:
#   looseNotTightString = selection['notTight']
#else:
#   looseNotTightString = "1"

region = {}

region['total'] = CutClass(reg, [
   ["WP", selection[WP]],
   #["notTight", looseNotTightString],
   ], baseCut = selection[reg])

region['prompt'] = CutClass(reg+"_prompt", [
   ["WP", selection[WP]],
   ["prompt", selection['promptLoose']],
   #["notTight", looseNotTightString],
   ], baseCut = selection[reg])

region['fakes'] = CutClass(reg+"_fakes", [
   ["WP", selection[WP]],
   ["fake", selection['fakeLoose']],
   #["notTight", looseNotTightString],
   ], baseCut = selection[reg])

# Yields

if doYields:
   yields = {}

   yields['total'] =  Yields(samples, samplesList, region['total'],  cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
   yields['prompt'] = Yields(samples, samplesList, region['prompt'], cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
   yields['fakes'] =  Yields(samples, samplesList, region['fakes'],  cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
   
   if not os.path.isfile("%s/fakeYields_%s%s.txt"%(yieldDir, reg, suffix)):
      outfile = open("%s/fakeYields_%s%s.txt"%(yieldDir, reg, suffix), "w")
      outfile.write("Fake Estimation Yields in %s %s\n"%(WP, reg.title()))
      outfile.write("Sample        Total                Prompt                Fakes\n")

   yieldsList = samplesList[:]
   yieldsList.append('Total')

   with open("%s/fakeYields_%s%s.txt"%(yieldDir, reg, suffix), "a") as outfile:
     for samp in yieldsList:
         outfile.write(samp.ljust(10) +\
         str(yields['total'].yieldDictFull[samp][reg].round(2)).ljust(25) +\
         str(yields['prompt'].yieldDictFull[samp][reg+"_prompt"].round(2)).ljust(25) +\
         str(yields['fakes'].yieldDictFull[samp][reg+"_fakes"].round(2)) + "\n")# .ljust(18) +\

# Plots

bins = binning(lep, varBins = varBins)

plotDict = {\
   "ht":{     'var':"ht_basJet_def",      'bins':[50,0,1000], 'decor':{'title':"H_{{T}} Plot" , "y":"Events", "x":"H_{T} / GeV", "log":[0,logy,0]}},
   "met":{    'var':"met",                'bins':[30,0,300],  'decor':{'title':"MET Plot" ,     "y":"Events", "x":"MET / GeV",   "log":[0,logy,0]}},
   "lepPt":{  'var':variables['pt'],      'bins':bins['pt'],  'decor':{'title':"Lepton p_{{T}} Plot", "y":"Events", "x":"%s %s p_{T} / GeV"%(WP.title(),lepton), "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['pt'][1]-bins['pt'][0])},
   "lepEta":{ 'var':variables['eta'],     'bins':bins['eta'], 'decor':{'title':"Lepton |#eta| Plot",  "y":"Events", "x":"%s %s |#eta|"%(WP.title(),lepton),      "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['pt'][1]-bins['pt'][0])}, 
   "lepMt":{  'var':variables['mt'],      'bins':bins['mt'],  'decor':{'title':"Lepton m_{{T}} Plot", "y":"Events", "x":"%s %s m_{T} / GeV"%(WP.title(),lepton), "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['pt'][1]-bins['pt'][0])}, 
   "lepDxy":{ 'var':variables['lepDxy'],  'bins':[10, 0, 0.1], 'decor':{'title':"Lepton |dxy| Plot", 'x':"%s %s|dxy|"%(WP.title(),lepton),                            'y':"Events", 'log':[0,logy,0]}},
   "lepDz":{  'var':variables['lepDz'],   'bins':[10, 0, 0.5], 'decor':{'title':"Lepton |dz| Plot",  'x':"%s %s|dz|"%(WP.title(),lepton),                             'y':"Events", 'log':[0,logy,0]}},
   "absIso":{ 'var':variables['absIso'],  'bins':[4, 0, 20],  'decor':{'title':"Lepton absIso Plot", 'x':"%s %s I_{abs} / GeV"%(WP.title(),lepton),                   'y':"Events", 'log':[0,logy,0]}},
   "relIso":{ 'var':variables['relIso'],  'bins':[20, 0, 5],  'decor':{'title':"Lepton relIso Plot", 'x':"%s %s I_{rel}"%(WP.title(),lepton),                         'y':"Events", 'log':[0,logy,0]}},
   "hybIso":{ 'var':variables['hybIso'],  'bins':[10, 0, 25], 'decor':{'title':"Lepton hybIso Plot", 'x':"%s %s HI = I_{rel}*min(p_{T}, 25 GeV)"%(WP.title(),lepton), 'y':"Events", 'log':[0,logy,0]}},
   "hybIso2":{'var':variables['hybIso2'], 'bins':[8, 0, 4],   'decor':{'title':"Lepton hybIso Plot", 'x':"%s %s log(1+HI)/log(1+5)"%(WP.title(),lepton),              'y':"Events", 'log':[0,logy,0]}},
   "delPhi":{ 'var':"dPhi_j1j2_vetoJet_def",  'bins':[8, 0, 3.14], 'decor':{'title':"deltaPhi(j1,j2) Plot", 'x':"#Delta#phi(j1,j2)",                                      'y':"Events", 'log':[0,logy,0]}},
   "mcMatchId":{'var':variables['mcMatchId'],   'bins':[140, -30, 110], 'decor':{'title':"Lepton mcMatchId Plot",  'x':"%s %s mcMatchId"%(WP.title(),lepton),         'y':"Events", 'log':[0,logy,0]}},
   "mcMatchAny":{'var':variables['mcMatchAny'], 'bins':[14, -4, 10],    'decor':{'title':"Lepton mcMatchAny Plot", 'x':"%s %s mcMatchAny"%(WP.title(),lepton),        'y':"Events", 'log':[0,logy,0]}},
}

if "application" in reg:
   if not varBins: plotDict['met']['bins'] = [100, 0, 1000]
   
if logy: plotMin = 10
else: plotMin = 0

plotsDict = Plots(**plotDict)
plotsList = ["lepPt", "lepMt", "lepEta"]
if not varBins: plotsList.extend(["met", "ht", "lepDxy", "lepDz", "absIso", "relIso", "hybIso", "hybIso2", "delPhi", "mcMatchId", "mcMatchAny"])

if doPlots:   
   plots =       getPlots(samples, plotsDict, region['total'], samplesList, plotList = plotsList, addOverFlowBin='both')
   fakePlots =  drawPlots(samples, plotsDict, region['total'], samplesList, plotList = plotsList, plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["djetBlind"], fom = fom, fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)

   if doControlPlots:
      if 'djetBlind' in samplesList: samplesList.remove('djetBlind')
      plots =       getPlots(samples, plotsDict, region['prompt'], samplesList, plotList = plotsList, addOverFlowBin='both')
      fakePlots2 = drawPlots(samples, plotsDict, region['prompt'], samplesList, plotList = plotsList, plotLimits = [plotMin, 100], fom = None, plotMin = plotMin, normalize = False, save = False)
      
      plots =       getPlots(samples, plotsDict, region['fakes'], samplesList, plotList = plotsList, addOverFlowBin='both')
      fakePlots3 = drawPlots(samples, plotsDict, region['fakes'], samplesList, plotList = plotsList, plotLimits = [plotMin, 100], fom = None, plotMin = plotMin, normalize = False, save = False)
   
   if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
      for canv in fakePlots['canvs']:
         fakePlots['canvs'][canv][0].SaveAs("%s/%s%s.png"%(savedir, canv, suffix))
         fakePlots['canvs'][canv][0].SaveAs("%s/root/%s%s.root"%(savedir, canv, suffix))
         fakePlots['canvs'][canv][0].SaveAs("%s/pdf/%s%s.pdf"%(savedir, canv, suffix))
      if doControlPlots:
         for canv in fakePlots2['canvs']:
            fakePlots2['canvs'][canv][0].SaveAs("%s/%s%s_prompt.png"%(savedir, canv, suffix))
            fakePlots2['canvs'][canv][0].SaveAs("%s/root/%s%s_prompt.root"%(savedir, canv, suffix))
            fakePlots2['canvs'][canv][0].SaveAs("%s/pdf/%s%s_prompt.pdf"%(savedir, canv, suffix))
         for canv in fakePlots3['canvs']:
            fakePlots3['canvs'][canv][0].SaveAs("%s/%s%s_fakes.png"%(savedir, canv, suffix))
            fakePlots3['canvs'][canv][0].SaveAs("%s/root/%s%s_fakes.root"%(savedir, canv, suffix))
            fakePlots3['canvs'][canv][0].SaveAs("%s/pdf/%s%s_fakes.pdf"%(savedir, canv, suffix))
