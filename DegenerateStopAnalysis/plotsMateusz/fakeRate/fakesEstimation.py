# fakesEstimation.py
# Application of fake rate to estimate fake background contribution 
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
from fakeRegions import regions

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--lep", dest = "lep",  help = "Lepton", type = str, default = "lep")
parser.add_argument("--region", dest = "region",  help = "Measurement or application region", type = str, default = "application_sr1")
parser.add_argument("--getData", dest = "getData",  help = "Get data", type = int, default = 1)
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
logy = args.logy
save = args.save
verbose = args.verbose

#Samples
cmgPP = cmgTuplesPostProcessed()

samplesList = ["w", "tt", "qcd"]

if "application" in region:
   samplesList.reverse()

if getData and "measurement" in region: 
   samplesList.append("djetBlind")

if "measurement" in region:
   skim = "oneLepGood_HT800"
elif "application" in region:
   skim = "preIncLep"
else:
   print "Region unknown. Exiting."
   sys.exit()

if "application" in region: getData = False #NOTE: For now, do not plot data near SR

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
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/fakesEstimation/noRunH"%tag

   savedir += "/%s/estimation/%s"%(region, lepton)
   
   suffix = "_%s"%lep
   
   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

#####
# Root file with fake rate

fakeRateDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate/"
fakeRateFile = "FakeRate_TightToLoose_lepPt_lep_data-EWK.root"

f1 = ROOT.TFile(fakeRateDir + fakeRateFile)

fakeRate = {}

fakeRate['pt'] = f1.Get("c1").GetPrimitive("c1_2").GetPrimitive("ratio_data-EWK_pt")

#####

selection = regions(region, lep)

if verbose:
   print makeLine()
   print "Using the following selection: ",
   pprint(selection)
   print makeLine()

index = selection['index']

pt = "LepGood_pt[%s]"%index['loose']
eta = "abs(LepGood_eta[%s])"%index['loose']
mt = "LepGood_mt[%s]"%index['loose']

regionCuts = CutClass("regionCuts", [
   ["region", selection[region]],
   ["loose", selection['loose']],
   #["lepPt", pt + "< 30"],
   ], baseCut = None)

#Sets TDR style
setup_style()

plotDict = {\
   "lepPt":{ 'var': pt,  "bins":[15,0,100], "decor":{"title": "Lepton p_{{T}} Plot", "y":"Events", "x":"%s p_{T} / GeV"%lepton, "log":[0,1,0]}},
   #"lepEta":{'var': eta, "bins":[20,0,3],   "decor":{"title": "Lepton |#eta| Plot",  "y":"Events", "x":"|#eta|",                "log":[0,1,0]}},
   #"lepMt":{ 'var': mt,  "bins":[30,0,150], "decor":{"title": "Lepton m_{{T}} Plot", "y":"Events", "x":"%s m_{T} / GeV"%lepton, "log":[0,1,0]}},
}

plotsDict = Plots(**plotDict)
plotsList = ["lepPt"]#, "lepEta"]

plots = getPlots(samples, plotsDict, regionCuts, samplesList, plotList = plotsList)# addOverFlowBin='both')
fakePlots = drawPlots(samples, plotsDict, regionCuts, samplesList, plotList = plotsList, plotLimits = [1, 100], denoms = ["bkg"], noms = ["qcd"], fom = "RATIO", fomLimits = [0,2.8], plotMin = 1000, normalize = False, save = False)

canv = fakePlots['canvs']['lepPt'][0].DrawClone()
#canv.cd(1)
pad1 = fakePlots['canvs']['lepPt'][1].DrawClone()
pad1.cd()

bkgs = fakePlots['stacks']['bkg']['lepPt'].GetStack().Last() #NOTE: last stack in GetStack() array is the sum of all stacks
bkgs.SetFillColor(ROOT.kBlue-9)
bkgs.Draw("hist")

fakePlots['latex'].DrawLatex(0.16,0.92, fakePlots['latexText']['L'])
fakePlots['latex'].DrawLatex(0.65,0.92, fakePlots['latexText']['R'])

#canv.RedrawAxis()
canv.Modified()
canv.Update()
#canvs[p][cMain].cd()
#canvs[p][cMain].Update()

#####

# Multiplying fake rate histogram with total bkg

#fakeRate['pt'] = ROOT.TH1D()
#fakeRate['2D'].ProjectionX().Copy(fakeRate['pt'])#ProfileX()
#fakeRate['pt'].Sumw2()
#fakeRate['pt'].Scale(1./Nbins)

#fakeRate['pt'].Sumw2()
#bkgs.Sumw2()

fakes = multiplyHists(bkgs, fakeRate['pt'])
#fakes = bkgs.Clone()*fakeRate['pt'].Clone()
fakes.SetName("fakes")
fakes.Draw("same")

canv.Modified()
canv.Update()

if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   canv.SaveAs("%s/fakesEstimation%s.png"%(savedir, suffix))
   canv.SaveAs("%s/root/fakesEstimation%s.root"%(savedir, suffix))
   canv.SaveAs("%s/pdf/fakesEstimation%s.pdf"%(savedir, suffix))
