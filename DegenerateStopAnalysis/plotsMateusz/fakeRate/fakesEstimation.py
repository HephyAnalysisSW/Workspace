# fakesEstimate.py
# Application of fake rate to estimate fake background contribution 
# Mateusz Zarucki 2017

import ROOT
import os, sys
import argparse
import copy
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style, makeDir
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from pprint import pprint
from array import array
from math import pi, sqrt #cos, sin, sinh, log
from fakeRegions import regions, binning

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--lep", dest = "lep",  help = "Lepton", type = str, default = "lep")
parser.add_argument("--region", dest = "reg",  help = "Measurement or application region", type = str, default = "application_sr1")
parser.add_argument("--fakeRateMeasurement", dest = "fakeRateMeasurement",  help = "Source of fake rate measurement", type = str, default = "data-EWK")
parser.add_argument("--looseNotTight", help = "Loose-not-tight CR", action = "store_true")
parser.add_argument("--doControlPlots", help = "Additional plots of regions", action = "store_true")
parser.add_argument("--getData", dest = "getData",  help = "Get data", type = int, default = 1)
parser.add_argument("--varBins", help = "Variable bin size", action = "store_true")
parser.add_argument("--logy", action = "store_true",  help = "Log scale")
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
reg = args.reg
fakeRateMeasurement = args.fakeRateMeasurement
looseNotTight = args.looseNotTight
doControlPlots = args.doControlPlots
getData = args.getData
varBins = args.varBins
logy = args.logy
save = args.save
verbose = args.verbose

#Sets TDR style
setup_style()

#Samples
cmgPP = cmgTuplesPostProcessed()

if "measurement" in reg:
   skim = "oneLepGood"
   samplesList = ["w", "tt", "qcd"]
elif "application" in reg:
   skim = "preIncLep"
   samplesList = ["st", "vv", "qcd", "z", "dy", "tt", "w"]
   getData = False #NOTE: For now, do not plot data near SR
else:
   print "Region unknown. Exiting."
   sys.exit()

if getData and "measurement" in reg:
   samplesList.append("djetBlind")

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
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/fakesEstimation"%tag

   savedir += "/%s/estimation/%s"%(reg, lepton)

   if looseNotTight: savedir += "/L!T"
   else: savedir += "/Loose"

   if fakeRateMeasurement == "data-EWK" or fakeRateMeasurement == "MC":
      binDir = "/FR_" + fakeRateMeasurement
   
   if not varBins: binDir += "/fixedBins"
   else:           binDir += "/varBins"
 
   savedir += binDir
   
   if logy: savedir += "/log"

   suffix = "%s_%s"%(reg, lep)
  
   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

#####
# Root file with fake rate

fakeRateDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate%s/"%binDir
fakeRateFile = "FakeRate_TightToLoose_lepPt_%s_%s.root"%(lep, fakeRateMeasurement)

if verbose:
   print makeLine()
   print "Using fake rate from ", fakeRateDir + fakeRateFile
   print makeLine()

f1 = ROOT.TFile(fakeRateDir + fakeRateFile)

fakeRate = {}

fakeRate['pt'] = f1.Get("c1").GetPrimitive("c1_2").GetPrimitive("ratio_%s_pt"%fakeRateMeasurement.replace("MC", "qcd"))

#####

selection = regions(reg, lep)
setEventListToChains(samples, samplesList, selection[reg])

if verbose:
   print makeLine()
   print "Using the following selection: \n",
   pprint(selection)
   print "\n",
   print reg, "= \n",
   pprint(selection[reg].fullList)
   print makeLine()

index = selection['index']

pt = {}
eta = {}
mt = {}

for WP in ['loose', 'tight']:
   pt[WP] = "LepGood_pt[%s]"%index[WP]
   mt[WP] = "LepGood_mt[%s]"%index[WP]
   eta[WP] = "abs(LepGood_eta[%s])"%index[WP]

# Signal region

region = CutClass(reg, [
   ["tight", selection['tight']],
   ], baseCut = selection[reg])

region_fakes = CutClass(reg + "_fakes", [
   ["loose", selection['tight']],
   ["fake", selection['fakeTight']],
   ], baseCut = selection[reg])

region_prompt = CutClass(reg + "_prompt", [
   ["loose", selection['tight']],
   ["prompt", selection['promptTight']],
   ], baseCut = selection[reg])

# Loose (not-Tight) CR

if looseNotTight:
   looseNotTightString = selection['notTight'] 
else:
   looseNotTightString = "1"

looseCR = CutClass(reg + "_looseCR", [
   ["loose", selection['loose']],
   ["notTight", looseNotTightString],
   ], baseCut = selection[reg])

looseCR_fakes = CutClass(reg + "_looseCR_fakes", [
   ["loose", selection['loose']],
   ["notTight", looseNotTightString],
   ["fake", selection['fakeLoose']],
   ], baseCut = selection[reg])

looseCR_prompt = CutClass(reg + "_looseCR_prompt", [
   ["loose", selection['loose']],
   ["notTight", looseNotTightString],
   ["prompt", selection['promptTight']],
   ], baseCut = selection[reg])

bins = binning(lep, varBins = varBins)

plotDict = {\
   "lepPt_loose":{'var':pt['loose'], "bins":bins['pt'], "decor":{"title": "Lepton p_{{T}} Plot", "y":"Events", "x":"%s p_{T} / GeV"%lepton, "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['pt'][1]-bins['pt'][0])},
   "lepPt_tight":{'var':pt['tight'], "bins":bins['pt'], "decor":{"title": "Lepton p_{{T}} Plot", "y":"Events", "x":"%s p_{T} / GeV"%lepton, "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['pt'][1]-bins['pt'][0])},
   #"lepEta":{'var': eta, "bins":[20,0,3],   "decor":{"title": "Lepton |#eta| Plot",  "y":"Events", "x":"|#eta|",                "log":[0,1,0]}},
   #"lepMt":{ 'var': mt,  "bins":[30,0,150], "decor":{"title": "Lepton m_{{T}} Plot", "y":"Events", "x":"%s m_{T} / GeV"%lepton, "log":[0,1,0]}},
}
   
plotsDict = Plots(**plotDict)

if logy: plotMin = 1
else: plotMin = 0

if doControlPlots:
   plots =                getPlots(samples, plotsDict, region,        samplesList, plotList = ['lepPt_tight'])# addOverFlowBin='both')
   regPlots     =        drawPlots(samples, plotsDict, region,        samplesList, plotList = ['lepPt_tight'], plotLimits = [10, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
   
   plots =                getPlots(samples, plotsDict, region_prompt, samplesList, plotList = ['lepPt_tight'])
   regPlots_prompt =     drawPlots(samples, plotsDict, region_prompt, samplesList, plotList = ['lepPt_tight'], plotLimits = [10, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
   
   plots =                getPlots(samples, plotsDict, looseCR,        samplesList, plotList = ['lepPt_loose'])
   looseCRplots =        drawPlots(samples, plotsDict, looseCR,        samplesList, plotList = ['lepPt_loose'], plotLimits = [10, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
   
   plots =                getPlots(samples, plotsDict, looseCR_prompt, samplesList, plotList = ['lepPt_loose'])
   looseCRplots_prompt = drawPlots(samples, plotsDict, looseCR_prompt, samplesList, plotList = ['lepPt_loose'], plotLimits = [10, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
   
plots =                   getPlots(samples, plotsDict, region_fakes,  samplesList, plotList = ['lepPt_tight'])
regPlots_fakes =         drawPlots(samples, plotsDict, region_fakes,  samplesList, plotList = ['lepPt_tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)

plots =                   getPlots(samples, plotsDict, looseCR_fakes,  samplesList, plotList = ['lepPt_loose'])
looseCRplots_fakes =     drawPlots(samples, plotsDict, looseCR_fakes,  samplesList, plotList = ['lepPt_loose'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)

####
## Multiplying fake rate histogram with total bkg
looseCRfakes = copy.deepcopy(looseCRplots_fakes)

# Legend
leg = copy.deepcopy(looseCRfakes['legs'])
latex = copy.deepcopy(looseCRfakes['latexText'])

fakeBkgs_CR_ = looseCRfakes['stacks']['bkg']['lepPt_loose'].Clone()
fakeBkgs_CR = fakeBkgs_CR_.GetStack().Last() #NOTE: last stack in GetStack() array is the sum of all stacks
fakeBkgs_CR.SetFillColor(ROOT.kBlue-9)
#fakeBkgs_CR.Draw("hist")

# unity histogram
unity = fakeRate['pt'].Clone()
unity.Reset()

nBins = unity.GetNbinsX()
for i in range(nBins):
   unity.SetBinContent(i+1,1)

# fakes estimation
#fakesEstimate = multiplyHists(fakeBkgs_CR, fakeRate['pt'])
fakesEstimate = fakeBkgs_CR.Clone()*fakeRate['pt'].Clone()
fakesEstimate.SetName("fakesEstimate")
fakesEstimate.SetMarkerSize(0.9)
fakesEstimate.SetMarkerStyle(20)
fakesEstimate.SetLineWidth(2)

if looseNotTight: 
   fakesEstimate.Divide(unity-fakeRate['pt'].Clone())
   ratioTitle = "#frac{#epsilon_{TL}}{(1 - #epsilon_{TL})}"
else:
   ratioTitle = "Fake Rate #epsilon_{TL}"

leg[-1].AddEntry(fakesEstimate, "Fakes (Estimate)", "LP")
canvas = drawPlot(fakeBkgs_CR_, legend = leg, decor = plotsDict['lepPt_loose']['decor'], latexText = latex, ratio = (fakesEstimate, fakeBkgs_CR), ratioLimits = [0,0.7], ratioTitle = ratioTitle) #base canvas with plot
fakesEstimate.Draw("same")

##fakeRate['pt'] = ROOT.TH1D()
##fakeRate['2D'].ProjectionX().Copy(fakeRate['pt'])#ProfileX()
##fakeRate['pt'].Sumw2()
##fakeRate['pt'].Scale(1./Nbins)
#
#fakeRate['pt'].Sumw2()
#fakeBkgs_CR.Sumw2()

###
# MC Closure

SRplots_fakes = copy.deepcopy(regPlots_fakes)
fakesMC= SRplots_fakes['stacks']['bkg']['lepPt_tight'].Clone()

canvas2 = drawPlot(fakesMC, legend = leg, decor = plotsDict['lepPt_tight']['decor'], latexText = latex, ratio = (fakesEstimate, fakesMC), ratioLimits = [0,4], ratioTitle = "MC Closure")
fakesEstimate.Draw("same")

if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   if doControlPlots:
      for canv in regPlots['canvs']:
         regPlots['canvs'][canv][0].SaveAs("%s/SR_%s_%s.png"%(savedir, suffix, canv))
         regPlots['canvs'][canv][0].SaveAs("%s/root/SR_%s_%s.root"%(savedir, suffix, canv))
         regPlots['canvs'][canv][0].SaveAs("%s/pdf/SR_%s_%s.pdf"%(savedir, suffix, canv))
      for canv in regPlots_fakes['canvs']:
         regPlots_fakes['canvs'][canv][0].SaveAs("%s/SR_%s_%s_fakes.png"%(savedir, suffix, canv))
         regPlots_fakes['canvs'][canv][0].SaveAs("%s/root/SR_%s_%s_fakes.root"%(savedir, suffix, canv))
         regPlots_fakes['canvs'][canv][0].SaveAs("%s/pdf/SR_%s_%s_fakes.pdf"%(savedir, suffix, canv))
      for canv in regPlots_prompt['canvs']:
         regPlots_prompt['canvs'][canv][0].SaveAs("%s/SR_%s_%s_prompt.png"%(savedir, suffix, canv))
         regPlots_prompt['canvs'][canv][0].SaveAs("%s/root/SR_%s_%s_prompt.root"%(savedir, suffix, canv))
         regPlots_prompt['canvs'][canv][0].SaveAs("%s/pdf/SR_%s_%s_prompt.pdf"%(savedir, suffix, canv))
      
      for canv in looseCRplots['canvs']:
         looseCRplots['canvs'][canv][0].SaveAs("%s/looseCR_%s_%s.png"%(savedir, suffix, canv))
         looseCRplots['canvs'][canv][0].SaveAs("%s/root/looseCR_%s_%s.root"%(savedir, suffix, canv))
         looseCRplots['canvs'][canv][0].SaveAs("%s/pdf/looseCR_%s_%s.pdf"%(savedir, suffix, canv))
      for canv in looseCRplots_fakes['canvs']:
         looseCRplots_fakes['canvs'][canv][0].SaveAs("%s/looseCR_%s_%s_fakes.png"%(savedir, suffix, canv))
         looseCRplots_fakes['canvs'][canv][0].SaveAs("%s/root/looseCR_%s_%s_fakes.root"%(savedir, suffix, canv))
         looseCRplots_fakes['canvs'][canv][0].SaveAs("%s/pdf/looseCR_%s_%s_fakes.pdf"%(savedir, suffix, canv))
      for canv in looseCRplots_prompt['canvs']:
         looseCRplots_prompt['canvs'][canv][0].SaveAs("%s/looseCR_%s_%s_prompt.png"%(savedir, suffix, canv))
         looseCRplots_prompt['canvs'][canv][0].SaveAs("%s/root/looseCR_%s_%s_prompt.root"%(savedir, suffix, canv))
         looseCRplots_prompt['canvs'][canv][0].SaveAs("%s/pdf/looseCR_%s_%s_prompt.pdf"%(savedir, suffix, canv))
   
   canvas['canvs'][0].SaveAs("%s/fakesEstimate_%s.png"%(savedir, suffix))
   canvas['canvs'][0].SaveAs("%s/root/fakesEstimate_%s.root"%(savedir, suffix))
   canvas['canvs'][0].SaveAs("%s/pdf/fakesEstimate_%s.pdf"%(savedir, suffix))

   canvas2['canvs'][0].SaveAs("%s/closureMC_%s.png"%(savedir, suffix))
   canvas2['canvs'][0].SaveAs("%s/root/closureMC_%s.root"%(savedir, suffix))
   canvas2['canvs'][0].SaveAs("%s/pdf/closureMC_%s.pdf"%(savedir, suffix))

##FakeRate values #NOTE: x-check
#momentum = 7 
#binX = fakeRate['pt'].GetXaxis().FindBin(momentum)
##binY = fakeRate['pt'].GetYaxis().FindBin(abs(eta))
#bin = fakeRate['pt'].GetBin(binX)#, binY)
#ratio = fakeRate['pt'].GetBinContent(bin)
#ratio_err = fakeRate['pt'].GetBinError(bin)

#print "Fake rate for pt ", momentum, " GeV = ", ratio, "+-", ratio_err 

#yld = fakeBkgs_CR.GetBinContent(bin) 
#yld_err = fakeBkgs_CR.GetBinError(bin)
#
#print "Yield in that bin", yld, "+-", yld_err 

