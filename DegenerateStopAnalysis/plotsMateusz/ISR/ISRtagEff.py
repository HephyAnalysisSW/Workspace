# ISRtagEff.py
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
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_Summer16_ISR import cmgTuplesPostProcessed
#from Workspace.DegenerateStopAnalysis.tools.mvaTools import getMVATrees
from Workspace.HEPHYPythonTools import u_float
from pprint import pprint
from array import array
from math import pi, sqrt

#Sets TDR style
setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--sample", dest = "sample", help = "Sample", type = str, default = "tt_1l")
parser.add_argument("--getData", dest = "getData",  help = "Get data samples", type = int, default = 0)
parser.add_argument("--getSignal", dest = "getSignal",  help = "Get signal samples", type = int, default = 0)
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
sample =         args.sample
getData =        args.getData
getSignal =      args.getSignal
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

if sample == 'allSignal':
    getSignal = True

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
   savedir1 = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/ISR/tagEff"%tag
   
   suff = "_" + sample 

   suff += "_RecoJets"
   
   suff += "_" + region
   
   savedir1 += "/" + region
   
   savedir2 = savedir1 + "/controlPlots"

   makeDir("%s/root"%savedir1)
   makeDir("%s/pdf"%savedir1)
   makeDir("%s/root"%savedir2)
   makeDir("%s/pdf"%savedir2)

if sample == 'allSignal':

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
reg = cuts_weights.cuts.removeCut(region, 'ISR100')
if reg != region: isrPtInc = '_no_ISR100'
else: isrPtInc = ''

var = {}

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

# Matched ISR
cuts_weights.cuts.addCut(region + isrPtInc + isrInEvt, "matchedISR")
matchedISRcutName = '_plus_matchedISR'

cuts_weights.cuts.addCut(region + isrPtInc + isrInEvt, "ISRfromGluon")

cuts_weights.cuts._update(reset = False)
cuts_weights._update()

variables = {}
for v in var:
   variables[v] = cuts_weights.cuts.vars_dict_format[var[v]]

plotList = [var['pt']]
if doControlPlots:
   #plotList.append(var['recoil'])
   #plotList.append(var['dRmin'])
   plotList.append(var['pdgId'])
   #plotList.append(var['ht']) 
   plotList.extend([var['mcFlavour'], var['qgl']])
   #plotList.extend([var['mcFlavour'], var['partonFlavour'], var['mcMatchFlav'], var['partonId'], var['partonMotherId']])#, var['qgl']])

plotDict = {
   var['pt']:       {'var':variables['pt'],       "bins":[50,0,1000],   "nMinus1":"", "decor":{"title":"isrPt",    "x":"J_{1} p_{T}",       "y":"Events", 'log':[0,logy,0]}},
   }
if doControlPlots:
   plotDict.update({
   var['ht']:             {'var':variables['ht'],             "bins":[40,200,1000], "nMinus1":"", "decor":{"title":"HT",                         "x":"H_{T} [GeV]",           "y":"Events", 'log':[0,logy,0]}},
   var['recoil']:         {'var':variables['recoil'],         "bins":[40,0,8],      "nMinus1":"", "decor":{"title":"Recoil",                     "x":"J_{1} p_{T}/MET",       "y":"Events", 'log':[0,logy,0]}},
   var['dRmin']:          {'var':variables['dRmin'],          "bins":[50,0,1],      "nMinus1":"", "decor":{"title":"dRminIsr",                   "x":"dRmin(GenPart, J_{1})", "y":"Events", 'log':[0,logy,0]}},
   var['pdgId']:          {'var':variables['pdgId'],          "bins":[35,-10,25],   "nMinus1":"", "decor":{"title":"Leading Jet pdgId",          "x":"J_{1} pdgId",           "y":"Events", 'log':[0,logy,0]}},
   var['mcFlavour']:      {'var':variables['mcFlavour'],      "bins":[35,-10,25],   "nMinus1":"", "decor":{"title":"Leading Jet mcFlavour",      "x":"J_{1} mcFlavour",       "y":"Events", 'log':[0,logy,0]}},
   var['partonFlavour']:  {'var':variables['partonFlavour'],  "bins":[35,-10,25],   "nMinus1":"", "decor":{"title":"Leading Jet partonFlavour",  "x":"J_{1} partonFlavour",   "y":"Events", 'log':[0,logy,0]}},
   var['mcMatchFlav']:    {'var':variables['mcMatchFlav'],    "bins":[35,-10,25],   "nMinus1":"", "decor":{"title":"Leading Jet mcMatchFlav",    "x":"J_{1} mcMatchFlav",     "y":"Events", 'log':[0,logy,0]}},
   var['partonId']:       {'var':variables['partonId'],       "bins":[35,-10,25],   "nMinus1":"", "decor":{"title":"Leading Jet partonId",       "x":"J_{1} partonId",        "y":"Events", 'log':[0,logy,0]}},
   var['partonMotherId']: {'var':variables['partonMotherId'], "bins":[35,-10,25],   "nMinus1":"", "decor":{"title":"Leading Jet partonMotherId", "x":"J_{1} partonMotherId",  "y":"Events", 'log':[0,logy,0]}},
   var['qgl']:            {'var':variables['qgl'],            "bins":[25,0,1],      "nMinus1":"", "decor":{"title":"Leading Jet QG Likelihood",  "x":"J_{1} QG Likelihood",   "y":"Events", 'log':[0,logy,0]}},
   })
plotsDict = Plots(**plotDict)

plots0_ =  getPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc], samplesList, plotList = plotList, addOverFlowBin='both')
plots0 =  drawPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc], samplesList, plotList = plotList, plotLimits = [1, 100], denoms = [sample], noms = [sample], fom = None, fomLimits = [0,1.8], plotMin = 1, normalize = False, save = False, leg = False)

plots1_ =  getPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc + isrInEvt], samplesList, plotList = plotList, addOverFlowBin='both')
plots1 =  drawPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc + isrInEvt], samplesList, plotList = plotList, plotLimits = [1, 100], denoms = [sample], noms = [sample], fom = None, fomLimits = [0,1.8], plotMin = 1, normalize = False, save = False, leg = False)

plots2_ =  getPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc + isrInEvt + matchedISRcutName], samplesList, plotList = plotList, addOverFlowBin='both')
plots2 =  drawPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc + isrInEvt + matchedISRcutName], samplesList, plotList = plotList, plotLimits = [1, 100], denoms = [sample], noms = [sample], fom = None, fomLimits = [0,1.8], plotMin = 1, normalize = False, save = False, leg = False)

#plots3_ =  getPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc + isrInEvt + '_plus_ISRfromGluon'], samplesList, plotList = plotList, addOverFlowBin='both')
#plots3 =  drawPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc + isrInEvt + '_plus_ISRfromGluon'], samplesList, plotList = plotList, plotLimits = [1, 100], denoms = [sample], noms = [sample], fom = None, fomLimits = [0,1.8], plotMin = 1, normalize = False, save = False, leg = False)

latex = copy.deepcopy(plots1['latexText'])
#leg = copy.deepcopy(plots1['legs'])
#if len(leg) > 2:
#   leg = [leg[0], leg[1]]

canvs = {}
hists = {}
ratioPlot = {}
for plot in plotList:
   hists[plot] = {}

   hists[plot]['total'] = plots0['hists'][sample][plot].Clone()
   hists[plot]['ISR'] =   plots1['hists'][sample][plot].Clone()
   hists[plot]['matched'] =  plots2['hists'][sample][plot].Clone()
  
   #hists[plot]['ISRfromGluon'] = plots3['hists'][sample][plot].Clone()

   #NISR = hists[plot]['ISR'].GetEntries()
   #NISRfromGluon = hists[plot]['ISRfromGluon'].GetEntries()
   #print "# evts with ISR: ", NISR 
   #print "# evts with ISR from gluon: ", NISRfromGluon 
   #print "# evts with ISR from quarks: ", NISR - NISRfromGluon 
 
   hists[plot]['total'].SetFillColor(ROOT.kAzure)
   hists[plot]['ISR'].SetFillColor(ROOT.kMagenta+2)
   hists[plot]['matched'].SetFillColor(ROOT.kRed)
   hists[plot]['total'].SetLineColor(1)
   hists[plot]['ISR'].SetLineColor(1)
   hists[plot]['matched'].SetLineColor(1)
   hists[plot]['total'].SetLineWidth(1)
   hists[plot]['ISR'].SetLineWidth(1)
   hists[plot]['matched'].SetLineWidth(1)
   
   leg1 = [makeLegend2()]
   leg1[-1].AddEntry(hists[plot]['total'], sample, "F")
   leg1[-1].AddEntry(hists[plot]['ISR'], sample + ' (ISR Present)', "F")
   leg1[-1].AddEntry(hists[plot]['matched'], sample + ' (Matched ISR)', "F")
   
   #leg2 = [makeLegend2()]
   #leg2[-1].AddEntry(hists['ISR'], sample + ' (ISR Present)', "F")
   #leg2[-1].AddEntry(hists['matched'], sample + ' (Matched ISR)', "F")
   
   canvs[plot] = drawPlot(hists[plot]['total'], legend = leg1, decor = plotsDict[plot]['decor'], latexText = latex, ratio = (hists[plot]['ISR'], hists[plot]['total']), ratioLimits = [0, 1], ratioTitle = "#splitline{Black: % ISR}{Green: Matched ISR}", unity = True)
   hists[plot]['ISR'].Draw("histsame")
   
   #canvs2 = drawPlot(hists['ISR'], legend = leg2, decor = plotsDict[var_pt]['decor'], latexText = latex, ratio = (hists['matched'], hists['ISR']), ratioLimits = [0, 1], ratioTitle = "% Matched ISR", unity = True)
   hists[plot]['matched'].Draw("histsame")
   
   # Superimposed ratio = Matched ISR 
   canvs[plot]['canvs'][2].cd()
   num = hists[plot]['matched'].Clone() 
   den = hists[plot]['ISR'].Clone()
   num.Sumw2()
   den.Sumw2()
   ratioPlot[plot] = num
   ratioPlot[plot].Divide(den)
   ratioPlot[plot].SetFillColor(ROOT.kBlue-8)
   ratioPlot[plot].SetFillStyle(3003)
   ratioPlot[plot].SetMarkerColor(8)
   ratioPlot[plot].SetMarkerStyle(20)
   ratioPlot[plot].SetMarkerSize(1)
   ratioPlot[plot].SetLineWidth(2)
   ratioPlot[plot].Draw("E2same") #adds shaded area around error bars
   ratioPlot[plot].Draw("Esame")

   #Save canvas
   if save: #web address: http://www.hephy.at/user/mzarucki/plots
      suffix = suff
      suffix += '_' + plot
   
      if 'Pt' in plot:
         savedir = savedir1
      else:
         savedir = savedir2
   
      canvs[plot]['canvs'][0].SaveAs("%s/ISR%s.png"%(savedir, suffix))
      canvs[plot]['canvs'][0].SaveAs("%s/root/ISR%s.root"%(savedir, suffix))
      canvs[plot]['canvs'][0].SaveAs("%s/pdf/ISR%s.pdf"%(savedir, suffix))
