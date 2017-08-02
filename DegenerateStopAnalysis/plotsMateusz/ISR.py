# ISR.py
# Mateusz Zarucki 2017

import ROOT
import os, sys
import argparse
import copy
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style, makeSimpleLatexTable, makeDir, makeLegend
from Workspace.DegenerateStopAnalysis.tools.degCuts2 import Cuts, CutsWeights
from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import cutWeightOptions, triggers, filters, lumis
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
parser.add_argument("--sample", dest = "sample", help = "Sample", type = str, default = "allSignal")
parser.add_argument("--getData", dest = "getData",  help = "Get data samples", type = int, default = 0)
parser.add_argument("--getSignal", dest = "getSignal",  help = "Get signal samples", type = int, default = 0)
parser.add_argument("--genISR", dest = "genISR",  help = "Generated ISR", type = int, default = 1)
parser.add_argument("--doControlPlots", dest = "doControlPlots",  help = "Do control plots", type = int, default = 0)
parser.add_argument("--region", dest = "region",  help = "Region", type = str, default = "presel")
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
sample =         args.sample
getData =        args.getData
getSignal =      args.getSignal
genISR =         args.genISR
doControlPlots = args.doControlPlots
region =         args.region
logy =           args.logy
save =           args.save
verbose =        args.verbose

if verbose:
   print makeDoubleLine()
   print "Running ISR script"
   print makeDoubleLine()

#Samples
cmgPP = cmgTuplesPostProcessed()

samplesList = [sample]
#samplesList = ["s30_FullSim", "s20_FullSim", "s50_FullSim"]
#samplesList = ["st", "vv", "qcd", "dy5to50", "dy", "z", "tt_2l", "tt_1l", "w"]

if getData: 
   data = "dblind"
   samplesList.append(data)

samples = getSamples(cmgPP = cmgPP, skim = 'preIncLep', sampleList = samplesList, scan = getSignal, useHT = True, getData = getData, def_weights = [])

#deltaMhists = {'T2tt':{'lt20':{10:[], 20:[], 30:[], 40:[], 50:[], 60:[], 70:[], 80:[]},
#                       'gt20':{10:[], 20:[], 30:[], 40:[], 50:[], 60:[], 70:[], 80:[]}}}
#
#for x in ratiosPkl['hists']:
#   for y in ratiosPkl['hists'][x]:
#      deltaMhists[y.split('-')[0]][x][int(y.split('-')[1])-int(y.split('-')[2])].append(ratiosPkl['hists'][x][y])

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
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/ISR/NEWEST"%tag
   #savedir += "/" + skim
   #if btag: savedir += "/" + btag
   #else: savedir += "/no_btag"
   
   savedir2 = savedir + "/controlPlots"

   suffix = "_" + sample 
   suffix += "_" + region

   makeDir("%s/root"%savedir)
   makeDir("%s/pdf"%savedir)
   makeDir("%s/root"%savedir2)
   makeDir("%s/pdf"%savedir2)

if 'all' in sample:

   from Workspace.DegenerateStopAnalysis.tools.Sample import Sample, Samples

   sampleDict = {}   

   allSignal = ROOT.TChain("Events", "Events")
   for s in samples.sigList():
      if 't2tt' in s and not 't2ttold' in s:
         allSignal.Add(samples[s].tree)

   sampleDict.update({
      'allSignal':{'name':'allSignal', 'sample':{'dir':samples[samples.keys()[0]].dir}, 'tree':allSignal, 'color':ROOT.kRed, 'isSignal':3 , 'isData':0, 'lumi':lumis["MC_lumi"]},
   })

   sampleDict2 = {}
   sampleDict2['allSignal'] = Sample(**sampleDict['allSignal'])
   samples = Samples(**sampleDict2)

cuts_weights = CutsWeights(samples, cutWeightOptions)

# N-1 
cuts_weights.cuts.removeCut(region, 'ISR100')
isrPtInc = '_no_ISR100'

if genISR:
   var = 'genIsrPt'
   var_dR = 'dRminGenIsr'
   trueISR = 'trueGenISR'
else:
   var = 'isrPt'
   var_dR = 'dRminIsr'
   trueISR = 'trueISR'   

plotList = [var]
if doControlPlots:
   plotList.append(var_dR) 

cuts_weights.cuts.addCut(region + isrPtInc, "ISRinEvt")
isrInEvt = "_plus_ISRinEvt"

# True ISR
cuts_weights.cuts.addCut(region + isrPtInc + isrInEvt, trueISR)
trueISRcutName = '_plus_' + trueISR

cuts_weights.cuts._update(reset = False)
cuts_weights._update()

variables = {}
variables['isrPt'] =    cuts_weights.cuts.vars_dict_format['isrPt']
variables['genIsrPt'] = cuts_weights.cuts.vars_dict_format['genIsrPt']

variables['dRminIsr'] =    cuts_weights.cuts.vars_dict_format['dRminIsr']
variables['dRminGenIsr'] = cuts_weights.cuts.vars_dict_format['dRminGenIsr']

plotDict = {
   "isrPt" :    {'var':variables['isrPt'],    "bins":[50,0,1000], "nMinus1":"", "decor":{"title":"isrPt", "x":"ISR Jet p_{T}", "y":"Events", 'log':[0,logy,0]}},
   "genIsrPt" : {'var':variables['genIsrPt'], "bins":[50,0,1000], "nMinus1":"", "decor":{"title":"genIsrPt", "x":"Gen. ISR p_{T}", "y":"Events", 'log':[0,logy,0]}},
   "dRminIsr" :    {'var':variables['dRminIsr'],    "bins":[50,0,1], "nMinus1":"", "decor":{"title":"dRminIsr", "x":"dR(GenPart, ISR)", "y":"Events", 'log':[0,logy,0]}},
   "dRminGenIsr" : {'var':variables['dRminGenIsr'], "bins":[50,0,1], "nMinus1":"", "decor":{"title":"dRminIsr", "x":"dR(GenPart, Gen. ISR)", "y":"Events", 'log':[0,logy,0]}},
   }
plotsDict = Plots(**plotDict)

plots0_ =  getPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc], samplesList, plotList = plotList, addOverFlowBin='both')
plots0 =  drawPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc], samplesList, plotList = plotList, plotLimits = [1, 100], denoms = [sample], noms = [sample], fom = None, fomLimits = [0,1.8], plotMin = 1, normalize = False, save = False, leg = False)

plots1_ =  getPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc + isrInEvt], samplesList, plotList = plotList, addOverFlowBin='both')
plots1 =  drawPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc + isrInEvt], samplesList, plotList = plotList, plotLimits = [1, 100], denoms = [sample], noms = [sample], fom = None, fomLimits = [0,1.8], plotMin = 1, normalize = False, save = False, leg = False)

plots2_ =  getPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc + isrInEvt + trueISRcutName], samplesList, plotList = plotList, addOverFlowBin='both')
plots2 =  drawPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc + isrInEvt + trueISRcutName], samplesList, plotList = plotList, plotLimits = [1, 100], denoms = [sample], noms = [sample], fom = None, fomLimits = [0,1.8], plotMin = 1, normalize = False, save = False, leg = False)

latex = copy.deepcopy(plots1['latexText'])
#leg = copy.deepcopy(plots1['legs'])
#if len(leg) > 2:
#   leg = [leg[0], leg[1]]

hists = {}
hists['total'] = plots0['hists'][sample][var].Clone()
hists['ISR'] =   plots1['hists'][sample][var].Clone()
hists['true'] =  plots2['hists'][sample][var].Clone()

hists['true'].SetFillColor(ROOT.kRed)
hists['ISR'].SetFillColor(ROOT.kMagenta+2)

leg1 = [makeLegend2()]
leg1[-1].AddEntry(hists['total'], sample, "F")
leg1[-1].AddEntry(hists['ISR'], sample + ' (ISR Present)', "F")
leg1[-1].AddEntry(hists['true'], sample + ' (True ISR)', "F")

#leg2 = [makeLegend2()]
#leg2[-1].AddEntry(hists['ISR'], sample + ' (ISR Present)', "F")
#leg2[-1].AddEntry(hists['true'], sample + ' (True ISR)', "F")

canvas = drawPlot(hists['total'], legend = leg1, decor = plotsDict[var]['decor'], latexText = latex, ratio = (hists['ISR'], hists['total']), ratioLimits = [0, 1], ratioTitle = "#splitline{Black: % ISR}{Green: True ISR}", unity = True)
hists['ISR'].Draw("histsame")

#canvas2 = drawPlot(hists['ISR'], legend = leg2, decor = plotsDict[var]['decor'], latexText = latex, ratio = (hists['true'], hists['ISR']), ratioLimits = [0, 1], ratioTitle = "% True ISR", unity = True)
hists['true'].Draw("histsame")

# Superimposed ratio = True ISR 
canvas['canvs'][2].cd()
num = hists['true'].Clone() 
den = hists['ISR'].Clone()
num.Sumw2()
den.Sumw2()
ratioPlot = num
ratioPlot.Divide(den)
ratioPlot.SetFillColor(ROOT.kBlue-8)
ratioPlot.SetFillStyle(3003)
ratioPlot.SetMarkerColor(8)
ratioPlot.SetMarkerStyle(20)
ratioPlot.SetMarkerSize(1)
ratioPlot.SetLineWidth(2)
ratioPlot.Draw("E2same") #adds shaded area around error bars
ratioPlot.Draw("Esame")

#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots
      suffix += '_' + var
     
      canvas['canvs'][0].SaveAs("%s/ratioISR%s.png"%(savedir, suffix))
      canvas['canvs'][0].SaveAs("%s/root/ratioISR%s.root"%(savedir, suffix))
      canvas['canvs'][0].SaveAs("%s/pdf/ratioISR%s.pdf"%(savedir, suffix))
      
      #canvas2['canvs'][0].SaveAs("%s/ratioTrueISR%s.png"%(savedir, suffix))
      #canvas2['canvs'][0].SaveAs("%s/root/ratioTrueISR%s.root"%(savedir, suffix))
      #canvas2['canvs'][0].SaveAs("%s/pdf/ratioTrueISR%s.pdf"%(savedir, suffix))

      if doControlPlots:
         for canv in plots1['canvs']:
            #if plot['canvs'][canv][0]:
            plots1['canvs'][canv][0].SaveAs("%s/dR_%s%s.png"%(savedir2, canv, suffix))
            plots1['canvs'][canv][0].SaveAs("%s/root/dR_%s%s.root"%(savedir2, canv, suffix))
            plots1['canvs'][canv][0].SaveAs("%s/pdf/dR_%s%s.pdf"%(savedir2, canv, suffix))

         #suffix += '_trueISR'     
 
         #for canv in plots2['canvs']:
         #   #if plot['canvs'][canv][0]:
         #   plots2['canvs'][canv][0].SaveAs("%s/ISR_%s%s.png"%(savedir2, canv, suffix))
         #   plots2['canvs'][canv][0].SaveAs("%s/root/ISR_%s%s.root"%(savedir2, canv, suffix))
         #   plots2['canvs'][canv][0].SaveAs("%s/pdf/ISR_%s%s.pdf"%(savedir2, canv, suffix))
