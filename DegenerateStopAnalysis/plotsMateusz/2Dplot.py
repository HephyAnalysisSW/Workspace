# 2Dplots.py
# Mateusz Zarucki 2016

import ROOT
import os, sys
import argparse
import copy
#import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style, makeSimpleLatexTable, makeDir, makeLegend
#from Workspace.DegenerateStopAnalysis.tools.degCuts2 import Cuts, CutsWeights
from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import cutWeightOptions, triggers, filters, lumis
from Workspace.DegenerateStopAnalysis.tools.colors import colors
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_Summer16 import cmgTuplesPostProcessed

#Sets TDR style
#setup_style()

ROOT.gStyle.SetOptStat(0)

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--var1", dest="var1",  help="Variable 1", type=str, default="leadJetPt") #"muPt"
parser.add_argument("--var2", dest="var2",  help="Variable 2", type=str, default="MET")
#parser.add_argument("--slice", dest="slice",  help="Pt Slice Bounds (low,up)", type=int, nargs=2, metavar = ('slice_low', 'slice_up'))
parser.add_argument("--sample", dest="sample",  help="Sample", type=str, default="t2tt500_490")
#parser.add_argument("--eleWP", dest = "eleWP",  help = "Electron WP", type = str, default = "Veto")
parser.add_argument("--log", dest="log",  help="Log scale", type=int, default=1)
parser.add_argument("--save", dest="save",  help="Toggle Save", type=int, default=1)
parser.add_argument("--verbose", dest = "verbose",  help = "Verbosity switch", type = int, default = 0)
parser.add_argument("-b", dest="batch",  help="Batch Mode", action="store_true", default=False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
var1 = args.var1
var2 = args.var2
#slice = args.slice
sample = args.sample 
log = args.log
save = args.save
verbose = args.verbose

print makeDoubleLine()
print "Plotting 2D distributions"
print makeDoubleLine()

#Samples
cmgPP = cmgTuplesPostProcessed()
samples = getSamples(cmgPP = cmgPP, skim = 'met100', sampleList = [sample], scan = True, useHT = True, getData = False, def_weights = [])

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
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/SoftTriggers/2Dplots/" + sample

   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

variables = {'muPt':"Muon p_{T}", 'MET':'MET', 'leadJetPt':'Leading Jet p_{T}'}

plotDict = {
   "muPt":{     'var':"LepGood_pt[IndexLepGood_mu_lowpt[0]]",         'bins':[50,0,30],      'decor':{'title':"Lepton p_{{T}} Plot",   'y':"Events", 'x':"Muon p_{T} / GeV", "log":[0,log,0]}},
   "MET":{      'var':"met",                   'bins':[100,0,1000],     'decor':{'title':"MET Plot",     "y":"Events", "x":"MET / GeV",   "log":[0,log,0]}},
   "leadJetPt":{'var':"Max$(Jet_pt * (abs(Jet_eta)<2.4  && (Jet_id)))", 'bins':[100,0,1000], 'decor':{'title':"Leading Jet Pt Plot",     "y":"Events", "x":"Leading Jet Pt / GeV",   "log":[0,log,0]}},
   #"ht":{     'var':"ht_basJet_def",         'bins':[75,0,1500],  'decor':{'title':"H_{{T}} Plot", "y":"Events", "x":"H_{T} / GeV", "log":[0,log,0]}},
   }
plotsDict = Plots(**plotDict)



#plots0_ =  getPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc], samplesList, plotList = plotList, addOverFlowBin='both')
#plots0 =  drawPlots(samples, plotsDict, [cuts_weights.cuts, region + isrPtInc], samplesList, plotList = plotList, plotLimits = [1, 100], fom = "AMSSYS", fomIntegral = False, fomLimits = [0,0.1], plotMin = 1, normalize = False, save = False, leg = True)
         
c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,2)

cut = "nLepGood_mu_lowpt > 0"

#2D Histograms (wrt. pT)
hist = make2DHist(samples[sample].tree, plotDict[var1]['var'], plotDict[var2]['var'], cut, plotDict[var1]['bins'][0], plotDict[var1]['bins'][1], plotDict[var1]['bins'][2], plotDict[var2]['bins'][0], plotDict[var2]['bins'][1], plotDict[var2]['bins'][2])
hist.SetName("2D_" + var1 + "_" + var2)
hist.SetTitle(variables[var1] + " vs " + variables[var2] + " Distribution")
hist.GetXaxis().SetTitle("%s / GeV"%variables[var1])
hist.GetYaxis().SetTitle("%s / GeV"%variables[var2])
hist.Draw("COLZ") #CONT1-5 #plots the graph with axes and points
#hist.GetZaxis().SetRangeUser(0, 4)
if log: ROOT.gPad.SetLogz() 
#alignStats(hist)
   
c1.Modified()
c1.Update()

suff = ""#_min1Mu"
 
#Save to Web
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   c1.SaveAs("%s/2D_%s_%s_%s%s.png"%(savedir, var1, var2, samples[sample].name,suff))
   c1.SaveAs("%s/root/2D_%s_%s_%s%s.root"%(savedir, var1, var2, samples[sample].name,suff))
   c1.SaveAs("%s/pdf/2D_%s_%s_%s%s.pdf"%(savedir, var1, var2, samples[sample].name,suff))
