# PUsys.py
# Mateusz Zarucki 2016

import ROOT
import os, sys
import math
import argparse
import pickle
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, makeSimpleLatexTable, makeDir, setup_style
from Workspace.DegenerateStopAnalysis.tools.degCuts2 import Cuts, CutsWeights
from Workspace.DegenerateStopAnalysis.cmgPostProcessing import cmgObjectSelection
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_Summer16 import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import cutWeightOptions, triggers, filters
from Workspace.HEPHYPythonTools import u_float
from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Sets TDR style
#setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--sample", dest = "sample", help = "Sample", type = str, default = "t2tt300_270")
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
sample = args.sample
save = args.save
verbose = args.verbose

##Samples
cmgPP = cmgTuplesPostProcessed()

#samplesList = [sample]
samplesList = ["dblind", "t2tt300_270"]#, "t2tt300_220", "t2tt300_290", "t2bw300_220", "t2bw300_270", "t2bw300_290"]

samples = getSamples(cmgPP = cmgPP, skim = 'preIncLep', sampleList = samplesList, scan = True, useHT = True, getData = True, def_weights = [])

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/PU/application"%tag
    
   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

resultsDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/PU"

Rs = pickle.load(open("%s/PUsys_r.pkl"%resultsDir, "r"))
Rminus1s = pickle.load(open("%s/PUsys_e1.pkl"%resultsDir, "r"))

canvs = {}

plotDict = {
   "nVert" : {'var':"nVert", "bins":[60,0,60], "nMinus1":"", "decor":{"title":"nVert", "x":"nVert", "y":"Events", 'log':[0,0,0]}},
   }
plotsDict = Plots(**plotDict)

cuts_weights = CutsWeights(samples, cutWeightOptions)

presel = 0

if presel:
   cut = 'presel'
else:
   cut = 'none'

cuts_weights.cuts.addCut(cut, 'pu_gt_20')
cuts_weights.cuts.addCut(cut, 'pu_lt_20')

doExtraPlots = 1
if doExtraPlots:
   plots_ =  getPlots(samples, plotsDict, [cuts_weights.cuts, cut], samplesList, plotList = ['nVert'], addOverFlowBin='both')
   plots =  drawPlots(samples, plotsDict, [cuts_weights.cuts, cut], samplesList, plotList = ['nVert'], plotLimits = [1, 100], fom = None, fomLimits = [0,8], plotMin = 1, normalize = True, save = False)

plots1_ =  getPlots(samples, plotsDict, [cuts_weights.cuts, cut + '_plus_pu_lt_20'], samplesList, plotList = ['nVert'], addOverFlowBin='both')
plots1 =  drawPlots(samples, plotsDict, [cuts_weights.cuts, cut + '_plus_pu_lt_20'], samplesList, plotList = ['nVert'], plotLimits = [1, 100], fom = None, fomLimits = [0,8], plotMin = 1, normalize = True, save = False)

plots2_ =  getPlots(samples, plotsDict, [cuts_weights.cuts, cut + '_plus_pu_gt_20'], samplesList, plotList = ['nVert'], addOverFlowBin='both')
plots2 =  drawPlots(samples, plotsDict, [cuts_weights.cuts, cut + '_plus_pu_gt_20'], samplesList, plotList = ['nVert'], plotLimits = [1, 100], fom = None, fomLimits = [0,8], plotMin = 1, normalize = True, save = False)

hists = {'puIncl':{}, 'pu_lt_20':{}, 'pu_gt_20':{}}

for samp in samplesList:
   if doExtraPlots:
      hists['puIncl'][samp] =   plots['hists'][samp]['nVert']
   hists['pu_lt_20'][samp] = plots1['hists'][samp]['nVert']
   hists['pu_gt_20'][samp] = plots2['hists'][samp]['nVert']

for pu in ['puIncl', 'pu_lt_20', 'pu_gt_20']:
   canvs[pu] = ROOT.TCanvas("c_"+pu, "Canvas "+pu, 1500, 1500)

   for i, samp in enumerate(samplesList):
      if 'dblind' in samp:
         hists[pu][samp].SetLineColor(1)
         hists[pu][samp].SetLineWidth(2)
      hists[pu][samp].Draw('histsame') 

N1 = hists['pu_lt_20']['t2tt300_270'].GetMean()
N2 = hists['pu_gt_20']['t2tt300_270'].GetMean()

N1_data = hists['pu_lt_20']['dblind'].GetMean()
N2_data = hists['pu_gt_20']['dblind'].GetMean()

print "N1:", N1
print "N2:", N2
print "N1 (data):", N1_data
print "N2 (data):", N2_data

#N1 = 14.7442697019 #nTrueInt
#N2 = 24.7434792224 #nTrueInt
#
##N1 = 13.9216724129 #nVert
##N2 = 23.934471923  #nVert
#
#N1_data = 14.4630405243 #nVert
#N2_data = 24.6009156872 #nVert

suffix = ''

# Normalised efficiency
# e = (Rminus1s[SR]/(N2-N1)*(x-N1) + 1

#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   for canv in canvs:
      #if plot['canvs'][canv][0]:
      canvs[canv].SaveAs("%s/PUsys_application_%s%s.png"%(savedir, canv, suffix))
      canvs[canv].SaveAs("%s/root/PUsys_application_%s%s.root"%(savedir, canv, suffix))
      canvs[canv].SaveAs("%s/pdf/PUsys_application_%s%s.pdf"%(savedir, canv, suffix))

#SR1s = ['sr1a', 'sr1b', 'sr1c', 'sr1vla', 'sr1vlb', 'sr1vlc', 'sr1la', 'sr1lb', 'sr1lc', 'sr1ma', 'sr1mb', 'sr1mc', 'sr1ha', 'sr1hb', 'sr1hc']
#SR2s = ['sr2a', 'sr2b', 'sr2c', 'sr2vla', 'sr2vlb', 'sr2vlc', 'sr2la', 'sr2lb', 'sr2lc', 'sr2ma', 'sr2mb', 'sr2mc', 'sr2ha', 'sr2hb', 'sr2hc']
#CRs =  ['cr1a', 'cr1b', 'cr1c', 'cr2a', 'cr2b', 'cr2c']
#
#regions = SR1s + SR2s + CRs
#allRegions = []
#
#for x in regions:
#   allRegions.append(x+'X')
#   allRegions.append(x+'Y')
#
