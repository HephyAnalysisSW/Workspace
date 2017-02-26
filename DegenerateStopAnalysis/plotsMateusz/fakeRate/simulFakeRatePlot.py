# simulFakeRatePlot.py
# Simulteanous plot of fake rates 
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
from Workspace.DegenerateStopAnalysis.tools.colors import colors 
from pprint import pprint
from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--lep", dest = "lep", help = "Lepton", type = str, default = "el")
parser.add_argument("--region", dest = "region", help = "Measurement or application region", type = str, default = "measurement")
parser.add_argument("--variable", dest = "variable", help = "Plotting variable", type = str, default = "pt")
parser.add_argument("--getData", dest = "getData", help = "Get data", type = int, default = 1)
parser.add_argument("--varBins", help = "Variable bin size", action = "store_true")
parser.add_argument("--logy", dest = "logy", help = "Toggle logy", type = int, default = 1)
parser.add_argument("--save", dest="save", help="Toggle save", type=int, default=1)
parser.add_argument("--verbose", dest="verbose", help="Verbosity switch", type=int, default=1)
parser.add_argument("-b", help="Batch mode", action="store_true", default=False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
lep = args.lep
region = args.region
variable = args.variable
getData = args.getData
varBins = args.varBins
logy = args.logy
save = args.save
verbose = args.verbose

#Samples
cmgPP = cmgTuplesPostProcessed()

samplesList = ["w", "tt", "qcd"]
#samplesList.extend(["st", "vv", "z", "dy"])

if "measurement" in region:
   skim = "oneLepGood"
   if getData:
      if region == "measurement1": 
         samplesList.append("djetBlind")
      elif region == "measurement2": 
         if lep == "el":
            samplesList.append("d1elBlind")
         elif lep == "mu":
            samplesList.append("d1muBlind")
         else:
            print "Wrong lepton input for measurement region 2. Exiting."
            sys.exit()

elif "application" in region:
   skim = "preIncLep"
else:
   print "Region unknown. Exiting."
   sys.exit()

samples = getSamples(cmgPP = cmgPP, skim = skim, sampleList = samplesList, scan = False, useHT = True, getData = 0)

if "measurement1" in region: samplesList.extend(["data-EWK", "MC"])
elif "measurement2" in region: samplesList.append("MC")

if lep == "el":    lepton = "Electron" #pdgId = "11"
elif lep == "mu":  lepton = "Muon" #pdgId = "13" 
elif lep == "lep": lepton = "Lepton"

#Save
tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
baseDir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/fakesEstimation/%s/allBins/fakeRate"%(tag, region)

if not varBins: binDir = "fixedBins"
else:           binDir = "varBins"   

fakeRateDir = "%s/%s/%s/root/"%(baseDir, lepton, binDir)

if save:   
   savedir = "%s/simulPlots/%s"%(baseDir, binDir)

   suffix = "_%s"%lep
   
   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

#####
# Root file with fake rate

variables = {'pt':'lepPt', 'eta':'lepEta'}
canvs = {'pt':'c1', 'eta':'c2'}
fakeRate = {}
rootFile = {}
canv = {}

colors['djetBlind'] = colors['d1elBlind'] = colors['d1muBlind'] = ROOT.kRed+1
colors['MC'] = ROOT.kOrange+1

fakeRate[variable] = {}
rootFile[variable] = {}

canv[variable] = ROOT.TCanvas("c1_"+variable, "Canvas " + variable, 1200, 1200)

if varBins: leg = makeLegend2(0.70,0.85,0.65,0.85) 
else:       leg = makeLegend2(0.15,0.3,0.65,0.85) 

for i, samp in enumerate(samplesList):
   fakeRateFile = "FakeRate_TightToLoose_%s_%s_%s.root"%(variables[variable], lep, samp)
   plot = "ratio_%s_%s"%(samp, variable)
   
   rootFile[variable][samp] = ROOT.TFile(fakeRateDir + fakeRateFile)
   fakeRate[variable][samp] = rootFile[variable][samp].Get(canvs[variable]).GetPrimitive("%s_2"%canvs[variable]).GetPrimitive(plot).Clone()

   canv[variable].cd()
   
   if i == 0: 
      dOpt = "P"
      fakeRate[variable][samp].SetTitle("%ss: Tight to Loose Ratio in %s Region"%(lepton, region.title()))
   else: dOpt = "Psame"

   if samp == "data-EWK":
      fakeRate[variable][samp].SetMarkerStyle(33)
      fakeRate[variable][samp].SetMarkerColor(1)
      fakeRate[variable][samp].SetMarkerSize(2)
      fakeRate[variable][samp].SetLineColor(1)
   else:
      fakeRate[variable][samp].SetMarkerColor(colors[samp])
      fakeRate[variable][samp].SetLineColor(colors[samp])
      
   fakeRate[variable][samp].SetMaximum(0.6) 
   fakeRate[variable][samp].Draw(dOpt) 
 
   ROOT.gPad.Modified()
   ROOT.gPad.Update()

   leg.AddEntry(plot, samp, "LP")

ROOT.gPad.Modified()
ROOT.gPad.Update()
leg.Draw()

ROOT.gPad.Modified()
ROOT.gPad.Update()
canv[variable].Modified()
canv[variable].Update()

if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   canv[variable].SaveAs("%s/simulFakeRatePlot%s_%s.png"%(savedir, suffix, variable))
   canv[variable].SaveAs("%s/root/simulFakeRatePlot%s_%s.root"%(savedir, suffix, variable))
   canv[variable].SaveAs("%s/pdf/simulFakeRatePlot%s_%s.pdf"%(savedir, suffix, variable))
