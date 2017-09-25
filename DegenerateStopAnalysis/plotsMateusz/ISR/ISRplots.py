# ISRplots.py
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
parser.add_argument("--getData", dest = "getData",  help = "Get data samples", type = int, default = 0)
parser.add_argument("--getSignal", dest = "getSignal",  help = "Get signal samples", type = int, default = 1)
parser.add_argument("--genISR", dest = "genISR",  help = "Generated ISR", type = str, default = "")
parser.add_argument("--doControlPlots", dest = "doControlPlots",  help = "Do control plots", type = int, default = 1)
parser.add_argument("--region", dest = "region",  help = "Region", type = str, default = "none")
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

samplesList = ["st", "qcd", "dy", "z", "tt_2l", "tt_1l", "w"] #"vv",  "dy5to50",

if getSignal:
   samplesList.extend(["t2tt300_220", "t2tt500_470", "t2tt375_365"])

if getData: 
   data = "dblind"
   samplesList.append(data)

samples = getSamples(cmgPP = cmgPP, skim = 'met200', sampleList = samplesList, scan = getSignal, useHT = True, getData = getData, def_weights = [])
#samples = getSamples(cmgPP = cmgPP, skim = 'preIncLep', sampleList = samplesList, scan = getSignal, useHT = True, getData = getData, def_weights = [])

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
         sys.exit()

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/ISR/distributions"%tag
  
   suff = ''
 
   if genISR:
      savedir += "/GenJets"
      suff += "_GenJets"
   else:   
      savedir += "/RecoJets"
      suff += "_RecoJets"
   
   suff += "_" + region
   
   savedir += "/" + region
   
   makeDir("%s/root"%savedir)
   makeDir("%s/pdf"%savedir)

cuts_weights = CutsWeights(samples, cutWeightOptions)

# N-1 
reg = cuts_weights.cuts.removeCut(region, 'ISR100')
if reg != region: isrPtInc = '_no_ISR100'
else: isrPtInc = ''

var = {}

if genISR:
   trueISR = 'trueGenISR'
   var['pt'] = 'GenIsrPt'
   if doControlPlots:
      var['recoil'] = 'GenISR_recoil'
      var['dRmin'] =  'GenISR_dRmin'
      var['pdgId'] =  'GenISR_pdgId'
else:
   trueISR = 'trueISR'   
   var['pt'] = 'isrPt'
   if doControlPlots:
      var['recoil'] =         'ISR_recoil'
      var['dRmin'] =          'ISR_dRmin'
      var['pdgId'] =          'ISR_pdgId'
      var['mcFlavour'] =      'ISR_mcFlavour' 
      var['partonFlavour'] =  'ISR_partonFlavour' 
      var['mcMatchFlav'] =    'ISR_mcMatchFlav'
      var['partonId'] =       'ISR_partonId'
      var['partonMotherId'] = 'ISR_partonMotherId'
      var['qgl'] =            'ISR_qgl'
 
if doControlPlots:   
   var['ht'] = 'ht'

cuts_weights.cuts.addCut(region + isrPtInc, "ISRinEvt")
isrInEvt = "_plus_ISRinEvt"

# True ISR
cuts_weights.cuts.addCut(region + isrPtInc + isrInEvt, trueISR)
trueISRcutName = '_plus_' + trueISR

if not genISR:
   cuts_weights.cuts.addCut(region + isrPtInc + isrInEvt, "ISRfromGluon")

cuts_weights.cuts._update(reset = False)
cuts_weights._update()

variables = {}
for v in var:
   variables[v] = cuts_weights.cuts.vars_dict_format[var[v]]

plotList = [var['pt']]
if doControlPlots:
   plotList.append(var['recoil']) 
   plotList.append(var['dRmin']) 
   plotList.append(var['pdgId']) 
   #plotList.append(var['ht']) 
   if not genISR:
      plotList.extend([var['mcFlavour'], var['partonFlavour'], var['mcMatchFlav'], var['partonId'], var['partonMotherId'], var['qgl']])

plotDict = {
   var['pt']:       {'var':variables['pt'],       "bins":[50,0,1000],   "nMinus1":"", "decor":{"title":"isrPt",    "x":"%s ISR Jet p_{T}"%genISR,       "y":"Events", 'log':[0,logy,0]}},
   }
if doControlPlots:
   plotDict.update({
   var['recoil']:   {'var':variables['recoil'], "bins":[40,0,8],      "nMinus1":"", "decor":{"title":"Recoil",    "x":"%s ISR Jet p_{T}/MET"%genISR,   "y":"Events", 'log':[0,logy,0]}},
   var['dRmin']:    {'var':variables['dRmin'],  "bins":[50,0,1],      "nMinus1":"", "decor":{"title":"dRminIsr",  "x":"dRmin(GenPart, %s ISR)"%genISR, "y":"Events", 'log':[0,logy,0]}},
   var['pdgId']:    {'var':variables['pdgId'],  "bins":[35,-10,25],   "nMinus1":"", "decor":{"title":"ISR pdgId", "x":"ISR pdgId",                     "y":"Events", 'log':[0,logy,0]}},
   var['ht']:       {'var':variables['ht'],     "bins":[40,200,1000], "nMinus1":"", "decor":{"title":"HT",        "x":"H_{T} [GeV]",                   "y":"Events", 'log':[0,logy,0]}},
   })
   
   if not genISR: 
      plotDict.update({
      var['mcFlavour']:      {'var':variables['mcFlavour'],      "bins":[35,-10,25], "nMinus1":"", "decor":{"title":"ISR mcFlavour",      "x":"ISR mcFlavour",      "y":"Events", 'log':[0,logy,0]}},
      var['partonFlavour']:  {'var':variables['partonFlavour'],  "bins":[35,-10,25], "nMinus1":"", "decor":{"title":"ISR partonFlavour",  "x":"ISR partonFlavour",  "y":"Events", 'log':[0,logy,0]}},
      var['mcMatchFlav']:    {'var':variables['mcMatchFlav'],    "bins":[35,-10,25], "nMinus1":"", "decor":{"title":"ISR mcMatchFlav",    "x":"ISR mcMatchFlav",    "y":"Events", 'log':[0,logy,0]}},
      var['partonId']:       {'var':variables['partonId'],       "bins":[35,-10,25], "nMinus1":"", "decor":{"title":"ISR partonId",       "x":"ISR partonId",       "y":"Events", 'log':[0,logy,0]}},
      var['partonMotherId']: {'var':variables['partonMotherId'], "bins":[35,-10,25], "nMinus1":"", "decor":{"title":"ISR partonMotherId", "x":"ISR partonMotherId", "y":"Events", 'log':[0,logy,0]}},
      var['qgl']:            {'var':variables['qgl'],            "bins":[25,0,1],    "nMinus1":"", "decor":{"title":"ISR QG Likelihood",  "x":"ISR QG Likelihood",  "y":"Events", 'log':[0,logy,0]}},
      })
plotsDict = Plots(**plotDict)

if getSignal:
   den = 'sig'
else:
   den = 'w'

plots0_ =  getPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc], samplesList, plotList = plotList, addOverFlowBin='both')
plots0 =  drawPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc], samplesList, plotList = plotList, plotLimits = [1, 100], denoms = [den], noms = ['bkg'], fom = "AMSSYS", fomLimits = [0,1.8], plotMin = 1, normalize = False, save = False, leg = False)

plots1_ =  getPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc + isrInEvt], samplesList, plotList = plotList, addOverFlowBin='both')
plots1 =  drawPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc + isrInEvt], samplesList, plotList = plotList, plotLimits = [1, 100], denoms = [den], noms = ['bkg'], fom = "AMSSYS", fomLimits = [0,1.8], plotMin = 1, normalize = False, save = False, leg = False)

plots2_ =  getPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc + isrInEvt + trueISRcutName], samplesList, plotList = plotList, addOverFlowBin='both')
plots2 =  drawPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc + isrInEvt + trueISRcutName], samplesList, plotList = plotList, plotLimits = [1, 100], denoms = [den], noms = ['bkg'], fom = "AMSSYS", fomLimits = [0,1.8], plotMin = 1, normalize = False, save = False, leg = False)

if not genISR:
   plots3_ =  getPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc + isrInEvt + '_plus_ISRfromGluon'], samplesList, plotList = plotList, addOverFlowBin='both')
   plots3 =  drawPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc + isrInEvt + '_plus_ISRfromGluon'], samplesList, plotList = plotList, plotLimits = [1, 100], denoms = [den], noms = ['bkg'], fom = "AMSSYS", fomLimits = [0,1.8], plotMin = 1, normalize = False, save = False, leg = False)

#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   for canv in plots0['canvs']:
      plots0['canvs'][canv][0].SaveAs("%s/%s%s.png"%(savedir, canv, suff))
      plots0['canvs'][canv][0].SaveAs("%s/root/%s%s.root"%(savedir, canv, suff))
      plots0['canvs'][canv][0].SaveAs("%s/pdf/%s%s.pdf"%(savedir, canv, suff))
   for canv in plots1['canvs']:
      plots1['canvs'][canv][0].SaveAs("%s/%s%s.png"%(savedir, canv, suff))
      plots1['canvs'][canv][0].SaveAs("%s/root/%s%s.root"%(savedir, canv, suff))
      plots1['canvs'][canv][0].SaveAs("%s/pdf/%s%s.pdf"%(savedir, canv, suff))
   for canv in plots2['canvs']:
      plots2['canvs'][canv][0].SaveAs("%s/%s%s.png"%(savedir, canv, suff))
      plots2['canvs'][canv][0].SaveAs("%s/root/%s%s.root"%(savedir, canv, suff))
      plots2['canvs'][canv][0].SaveAs("%s/pdf/%s%s.pdf"%(savedir, canv, suff))

   if not genISR:
      for canv in plots3['canvs']:
         plots3['canvs'][canv][0].SaveAs("%s/%s%s.png"%(savedir, canv, suff))
         plots3['canvs'][canv][0].SaveAs("%s/root/%s%s.root"%(savedir, canv, suff))
         plots3['canvs'][canv][0].SaveAs("%s/pdf/%s%s.pdf"%(savedir, canv, suff))
