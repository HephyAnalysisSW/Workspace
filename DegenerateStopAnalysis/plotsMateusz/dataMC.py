# dataMC.py
# Mateusz Zarucki 2017

import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style, makeSimpleLatexTable, makeDir, makeLegend
from Workspace.DegenerateStopAnalysis.tools.degCuts2 import Cuts, CutsWeights
from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import cutWeightOptions, triggers, filters
#from Workspace.DegenerateStopAnalysis.tools.colors import colors
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_Summer16 import cmgTuplesPostProcessed
#from Workspace.DegenerateStopAnalysis.tools.mvaTools import getMVATrees
from Workspace.HEPHYPythonTools import u_float
from pprint import pprint
from array import array
from math import pi, sqrt

#Sets TDR style
setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--getData", dest = "getData",  help = "Get data samples", type = int, default = 0)
parser.add_argument("--region", dest = "region",  help = "Region", type = str, default = "presel")
parser.add_argument("--promptOnly", dest = "promptOnly",  help = "Prompt leptons", type = int, default = 0)
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
region = args.region
promptOnly = args.promptOnly
logy = args.logy
save = args.save
verbose = args.verbose

if verbose:
   print makeDoubleLine()
   print "Plotting MC distributions"
   print makeDoubleLine()

#Samples
samplesList = ["ttx", "st", "vv", "qcd", "dy5to50", "dy", "z", "tt_2l", "tt_1l", "w"]

if getData: 
   data = "dblind"
   samplesList.append(data)

cmgPP = cmgTuplesPostProcessed()
samples = getSamples(cmgPP = cmgPP, skim = 'preIncLep', sampleList = samplesList, scan = False, useHT = True, getData = getData, def_weights = [])

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
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/dataMC"%tag
   #savedir += "/" + skim
   #if btag: savedir += "/" + btag
   #else: savedir += "/no_btag"
   suffix = "_" + region

   if promptOnly: suffix += "_prompt"  
 
   makeDir("%s/root"%savedir)
   makeDir("%s/pdf"%savedir)

plotDict = {
   "lepPt" : {'var':"LepGood_pt[IndexLepGood_lep_def[0]]", "bins":[20,0,200], "nMinus1":"", "decor":{"title":"lepPt", "x":"Lepton p_{T}", "y":"Events", 'log':[0,logy,0]}},
   }
plotsDict = Plots(**plotDict)

cuts_weights = CutsWeights(samples, cutWeightOptions)

# pt inclusive
if 'sr' in region:
   cuts_weights.cuts.removeCut(region, 'lepPt_lt_30')
   ptInc = '_no_lepPt_lt_30'
else:
   ptInc = ''

if promptOnly:
   cuts_weights.cuts.addCut(region + ptInc, 'prompt')
   prompt = '_plus_prompt'
else:
   prompt = ''

cuts_weights.cuts._update(reset = False)
cuts_weights._update()

plots_ =  getPlots(samples, plotsDict, [cuts_weights.cuts, region + ptInc + prompt], samplesList, plotList = ['lepPt'], addOverFlowBin='both')
plots =  drawPlots(samples, plotsDict, [cuts_weights.cuts, region + ptInc + prompt], samplesList, plotList = ['lepPt'], plotLimits = [1, 100], denoms = ["tt_1l"], noms = ["tt_2l"], fom = "RATIO", fomLimits = [0,8], plotMin = 1, normalize = False, save = False)

#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   for canv in plots['canvs']:
      #if plot['canvs'][canv][0]:
      plots['canvs'][canv][0].SaveAs("%s/dataMC_%s%s.png"%(savedir, canv, suffix))
      plots['canvs'][canv][0].SaveAs("%s/root/dataMC_%s%s.root"%(savedir, canv, suffix))
      plots['canvs'][canv][0].SaveAs("%s/pdf/dataMC_%s%s.pdf"%(savedir, canv, suffix))
