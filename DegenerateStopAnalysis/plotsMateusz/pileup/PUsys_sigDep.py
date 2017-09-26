# PUsys.py
# Mateusz Zarucki 2016

import ROOT
import os, sys
import re
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
samplesList = ["t2tt300_270"]#, "t2tt300_220", "t2tt300_290", "t2bw300_220", "t2bw300_270", "t2bw300_290"]

samples = getSamples(cmgPP = cmgPP, skim = 'preIncLep', sampleList = samplesList, scan = True, useHT = True, getData = 0, def_weights = [])
#
#if 'all' in sample:
#   allFastSim = ROOT.TChain("Events", "Events")
#   for s in samples.sigList():
#      if 't2tt' in s and not 't2ttold' in s:
#         if 'global' in scriptTag and s not in ['t2tt275_205', 't2tt350_330', 't2tt400_350']: continue
#         allFastSim.Add(samples[s].tree)
#
#if verbose:
#   print makeLine()
#   print "Using samples:"
#   newLine()
#   for s in samplesList:
#      if s: print samples[s].name,":",s
#      else:
#         print "!!! Sample " + sample + " unavailable."
#         sys.exit(0)

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/PU/signalDependence"%tag
    
   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

ratiosPkl = "/afs/hephy.at/user/n/nrad/public/share/PUHistsRatios.pkl"
pkl = pickle.load(open(ratiosPkl, "r"))

effs = {'diff':{}}
effs['pu_lt_20'] = pkl['hists']['lt20']
effs['pu_gt_20'] = pkl['hists']['gt20']
ratios = pkl['ratios']

signals = []

binNumber = 42

mStops = ['250', '300', '400', '500']

#mStops = ['600', '700', '800']

def sorted_nicely( l ): 
   convert = lambda text: int(text) if text.isdigit() else text 
   alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
   return sorted(l, key = alphanum_key)

signals_sorted = sorted_nicely(ratios.keys())

for z in signals_sorted:
   for mStop in mStops:
      if 'T2tt-' + mStop in z:
         signals.append(z)

#signals = [z for z in ratios if 'T2tt' in z]

x = [] 
y = {'r':[], 'e1':[], 'e2':[]}

for i, sig in enumerate(signals):
   i+=1
   #hists['T2tt'].SetBinContent(i, ratios[sig].GetBinContent(1))
   x.append(i)
   #print i, sig, 'e1: ', effs['pu_lt_20'][sig].GetBinContent(1), 'e2: ', effs['pu_gt_20'][sig].GetBinContent(1), 'r: ', ratios[sig].GetBinContent(1)
   y['r'].append(ratios[sig].GetBinContent(binNumber))
   y['e1'].append(effs['pu_lt_20'][sig].GetBinContent(binNumber))
   y['e2'].append(effs['pu_gt_20'][sig].GetBinContent(binNumber))

hists = {'r':  ROOT.TGraph(len(x), array('d',x), array('d',y['r'])),
         'e1': ROOT.TGraph(len(x), array('d',x), array('d',y['e1'])),
         'e2': ROOT.TGraph(len(x), array('d',x), array('d',y['e2']))}

for i, sig in enumerate(signals):
   i+=1
   #print i, sig
   hists['r'].GetXaxis().SetBinLabel(hists['r'].GetXaxis().FindBin(i), sig)
   hists['e1'].GetXaxis().SetBinLabel(hists['e1'].GetXaxis().FindBin(i), sig)

   #latex = ROOT.TLatex(gr->GetX()[5], gr->GetY()[5],"my annotation");
   #gr->GetListOfFunctions()->Add(latex);
   #gr->Draw("alp");

#hists = {'all':  ROOT.TGraph("hist_all",  "hist_all",  200, 0, 200),
#         'T2tt': ROOT.TGraph("hist_T2tt", "hist_T2tt", 200, 0, 200),
#         'T2bW': ROOT.TGraph("hist_T2bW", "hist_T2bW", 200, 0, 200)}

SR = ratios['T2tt-300-270'].GetXaxis().GetBinLabel(binNumber)

hists['r'].SetTitle("R in " + SR)
hists['e1'].SetTitle("Efficiencies in " + SR)

canvs = {}

canvs['r'] = ROOT.TCanvas("c1", "Canvas 1", 1800, 1800)

hists['r'].SetMarkerStyle(20)
hists['r'].SetMarkerSize(2)
hists['r'].SetMarkerColor(2)
hists['r'].SetName('r')
hists['r'].SetMinimum(0)
hists['r'].SetMaximum(4)

hists['r'].Draw("AP")

canvs['effs'] = ROOT.TCanvas("c2", "Canvas 2", 1800, 1800)
hists['e1'].SetMarkerStyle(20)
hists['e2'].SetMarkerStyle(20)
hists['e1'].SetMarkerSize(2)
hists['e2'].SetMarkerSize(2)
hists['e1'].SetMarkerColor(3)
hists['e2'].SetMarkerColor(4)
hists['e1'].SetName('e1')
hists['e2'].SetName('e2')
hists['e1'].SetMinimum(0)
hists['e1'].SetMaximum(0.04)

hists['e1'].Draw("APsame")
hists['e2'].Draw("Psame")

#alignStats(hists['r'])

l1 = makeLegend2(y1=0.65,y2=0.85)
l1.AddEntry("e1", "e1", "P")
l1.AddEntry("e2", "e2", "P")
l1.Draw()

suffix = '_' + SR + '_' + mStop
 
#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   for canv in canvs:
      #if plot['canvs'][canv][0]:
      canvs[canv].SaveAs("%s/PUsys_%s%s.png"%(savedir, canv, suffix))
      canvs[canv].SaveAs("%s/root/PUsys_%s%s.root"%(savedir, canv, suffix))
      canvs[canv].SaveAs("%s/pdf/PUsys_%s%s.pdf"%(savedir, canv, suffix))
