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
from pprint import pprint
from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--lep", dest = "lep",  help = "Lepton", type = str, default = "lep")
parser.add_argument("--region", dest = "region",  help = "Measurement or application region", type = str, default = "measurement")
parser.add_argument("--getData", dest = "getData",  help = "Get data", type = int, default = 1)
parser.add_argument("--varBins", dest = "varBins",  help = "Variable bin size", action = "store_true")
parser.add_argument("--logy", dest = "logy",  help = "Toggle logy", type = int, default = 1)
parser.add_argument("--save", dest="save",  help="Toggle save", type=int, default=1)
parser.add_argument("--verbose", dest="verbose",  help="Verbosity switch", type=int, default=1)
parser.add_argument("-b", dest="batch",  help="Batch mode", action="store_true", default=False)
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
varBins = args.varBins
logy = args.logy
save = args.save
verbose = args.verbose

#Samples
cmgPP = cmgTuplesPostProcessed()

samplesList = ["w", "tt", "qcd"]

if getData and "measurement" in region: 
   samplesList.append("djetBlind")

if "measurement" in region:
   skim = "oneLepGood"
elif "application" in region:
   skim = "preIncLep"
else:
   print "Region unknown. Exiting."
   sys.exit()

samples = getSamples(cmgPP = cmgPP, skim = skim, sampleList = samplesList, scan = False, useHT = True, getData = 0)

if "measurement" in region: samplesList.append("data-EWK")

if lep == "el":    lepton = "Electron" #pdgId = "11"
elif lep == "mu":  lepton = "Muon" #pdgId = "13" 
elif lep == "lep": lepton = "Lepton"

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/fakesEstimation"%tag

   savedir += "/%s/fakeRate/simulPlots"%region
  
   if not varBins: binDir = "/fixedBins"
   else:           binDir = "/varBins"   
   
   savedir += binDir 
 
   suffix = "_%s"%lep
   
   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

#####
# Root file with fake rate

variables = {'pt':'lepPt'}#, 'eta':'lepEta'}
#variables = {'eta':'lepEta'}#,'pt':'lepPt'}
canvs = {'pt':'c1', 'eta':'c2'}
fakeRate = {}
rootFile = {}
canv = {}

for var in variables:
   fakeRate[var] = {}
   rootFile[var] = {}
   
   canv[var] = ROOT.TCanvas("c1_"+var, "Canvas " + var, 1200, 1200)
   leg = makeLegend2(0.15,0.3,0.65,0.85) 
  
   for i, samp in enumerate(samplesList):
      fakeRateDir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/fakesEstimation/%s/fakeRate/%s%s/root/"%(tag, region, lepton, binDir)
      fakeRateFile = "FakeRate_TightToLoose_%s_%s_%s.root"%(variables[var], lep, samp)
      plot = "ratio_%s_%s"%(samp, var)
      
      rootFile[var][samp] = ROOT.TFile(fakeRateDir + fakeRateFile)
      fakeRate[var][samp] = rootFile[var][samp].Get(canvs[var]).GetPrimitive("%s_2"%canvs[var]).GetPrimitive(plot).Clone()
 
      canv[var].cd()
      
      if i == 0: 
         dOpt = "P"
         fakeRate[var][samp].SetTitle("%ss: Tight to Loose Ratio in %s Region"%(lepton, region.title()))
      else: dOpt = "Psame"

      fakeRate[var][samp].SetMarkerColor(2+i)
      fakeRate[var][samp].SetLineColor(2+i)
      if samp == "data-EWK":
         fakeRate[var][samp].SetMarkerStyle(34)
         fakeRate[var][samp].SetMarkerColor(1)
         fakeRate[var][samp].SetLineColor(1)
         
      fakeRate[var][samp].Draw(dOpt) 
    
      ROOT.gPad.Modified()
      ROOT.gPad.Update()
  
      leg.AddEntry(plot, samp, "LP")
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   leg.Draw()
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   canv[var].Modified()
   canv[var].Update()

   if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
      canv[var].SaveAs("%s/simulFakeRatePlot%s_%s.png"%(savedir, suffix, var))
      canv[var].SaveAs("%s/root/simulFakeRatePlot%s_%s.root"%(savedir, suffix, var))
      canv[var].SaveAs("%s/pdf/simulFakeRatePlot%s_%s.pdf"%(savedir, suffix, var))
