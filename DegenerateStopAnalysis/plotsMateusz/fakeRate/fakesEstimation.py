# fakesEstimation.py
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
from Workspace.DegenerateStopAnalysis.tools.mvaTools import getMVATrees
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
parser.add_argument("--mva", help = "MVA", action = "store_true")
parser.add_argument("--fakeRateMeasurement", dest = "fakeRateMeasurement",  help = "Source of fake rate measurement", type = str, default = "data-EWK")
parser.add_argument("--looseNotTight", help = "Loose-not-tight CR", action = "store_true")
parser.add_argument("--oneBin", help = "One bin", action = "store_true")
parser.add_argument("--doYields", help = "Calculate yields", action = "store_true")
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
mva = args.mva
fakeRateMeasurement = args.fakeRateMeasurement
looseNotTight = args.looseNotTight
oneBin = args.oneBin
doYields = args.doYields
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

   if mva:
      reg = "application_srBDT"

else:
   print "Region unknown. Exiting."
   sys.exit()

if getData and "measurement" in reg:
   samplesList.append("djetBlind")

samples = getSamples(cmgPP = cmgPP, skim = skim, sampleList = samplesList, scan = False, useHT = True, getData = getData, def_weights = [])

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

#Bin dir   
if fakeRateMeasurement == "data-EWK" or fakeRateMeasurement == "MC":
   binDir = "/FR_" + fakeRateMeasurement

if not varBins: binDir += "/fixedBins"
else:           binDir += "/varBins"
 
# Root file with fake rate

fakeRateDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate"

if oneBin: fakeRateDir += "/oneBin"
   
fakeRateDir += binDir

fakeRateFile = "FakeRate_TightToLoose_lepPt_%s_%s.root"%(lep, fakeRateMeasurement)

if verbose:
   print makeLine()
   print "Using fake rate from ", fakeRateDir + "/" + fakeRateFile
   print makeLine()

f1 = ROOT.TFile(fakeRateDir + "/" + fakeRateFile)

fakeRate = {}

fakeRate['pt'] = f1.Get("c1").GetPrimitive("c1_2").GetPrimitive("ratio_%s_pt"%fakeRateMeasurement)

#####

WPs = ['loose', 'tight']
selection = {}
for WP in WPs:
   selection.update(regions(samples, reg, lep, WP, oneBin = oneBin, mva = mva))

if not mva: setEventListToChains(samples, samplesList, selection['kinematic'][reg])

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/fakesEstimation"%tag

   if oneBin: savedir += "/oneBin"

   if mva: savedir += "/%s_id%s_bdt%s/estimation/%s"%(reg, selection['mvaId'], selection['bdtcut'], lepton)
   else:   savedir += "/%s/estimation/%s"%(reg, lepton)

   if looseNotTight: savedir += "/L!T"
   else: savedir += "/Loose"

   savedir += binDir
   
   if logy: savedir += "/log"

   suffix = "%s_%s"%(reg, lep)
  
   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")


# Gets MVA friend trees
if mva:
   getMVATrees(samples, mvaIdIndex = selection['mvaIdIndex'])

if verbose:
   print makeLine()
   print "Using the following selection: \n",
   pprint(selection)
   print "\n",
   print makeLine()

index = {}
pt = {}
eta = {}
mt = {}
hybIso = {}
regionSel = {}

for WP in ['loose', 'tight']:
   index[WP] = selection[WP]['cuts'].vars.lepIndex
   pt[WP] = "LepGood_pt[%s]"%index[WP]
   mt[WP] = "LepGood_mt[%s]"%index[WP]
   eta[WP] = "abs(LepGood_eta[%s])"%index[WP]
   hybIso[WP] = "(LepGood_relIso03[{ind}]*min(LepGood_pt[{ind}], 25))".format(ind = index[WP])
   regionSel[WP] = selection[WP][reg][samplesList[0]][0] #NOTE: application region only

# Signal region
region = {'SR':{}, 'looseCR':{}}

region['SR']['total'] =  [selection['tight']['cuts'], selection['cutDef']] 
region['SR']['prompt'] = [selection['tight']['cuts'], selection['cutDef'] + '_prompt'] 
region['SR']['fakes'] =  [selection['tight']['cuts'], selection['cutDef'] + '_fakes'] 

# Loose (not-Tight) CR
if looseNotTight:
   notTight = "_notTight"
else:
   notTight = ""

region['looseCR']['total'] =  [selection['loose']['cuts'], selection['cutDef'] + notTight] 
region['looseCR']['prompt'] = [selection['loose']['cuts'], selection['cutDef'] + '_prompt' + notTight] 
region['looseCR']['fakes'] =  [selection['loose']['cuts'], selection['cutDef'] + '_fakes' + notTight] 

# Yields 
if doYields:
   yields = {'SR':{}, 'looseCR':{}}

   for x in yields: 
      yields[x]['total'] =  Yields(samples, samplesList, cutInst = None, cuts = region[x]['total'],  cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
      yields[x]['prompt'] = Yields(samples, samplesList, cutInst = None, cuts = region[x]['prompt'], cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
      yields[x]['fakes'] =  Yields(samples, samplesList, cutInst = None, cuts = region[x]['fakes'],  cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)

   if not os.path.isfile("%s/fakeYields_%s.txt"%(savedir, suffix)):
      outfile = open("%s/fakeYields_%s.txt"%(savedir, suffix), "w")
      outfile.write("Fake Estimation Yields in %s\n"%reg.title())
      outfile.write("Sample      Loose CR: Total         Loose CR: Prompt          Loose CR: Fakes          SR: Total              SR: Prompt               SR: Fakes\n") 

   yieldsList = samplesList[:]
   yieldsList.append('Total')

   with open("%s/fakeYields_%s.txt"%(savedir, suffix), "a") as outfile:
     for samp in yieldsList:
         outfile.write(samp.ljust(10) +\
         str(yields['looseCR']['total'].yieldDictFull[samp][selection['cutDef'] + notTight].round(2)).ljust(25) +\
         str(yields['looseCR']['prompt'].yieldDictFull[samp][selection['cutDef'] + '_prompt' + notTight].round(2)).ljust(25) +\
         str(yields['looseCR']['fakes'].yieldDictFull[samp][selection['cutDef'] + '_fakes' + notTight].round(2)).ljust(25) +\
         str(yields['SR']['total'].yieldDictFull[samp][selection['cutDef']].round(2)).ljust(25) +\
         str(yields['SR']['prompt'].yieldDictFull[samp][selection['cutDef'] + '_prompt'].round(2)).ljust(25) +\
         str(yields['SR']['fakes'].yieldDictFull[samp][selection['cutDef'] + '_fakes'].round(2)) + "\n")# .ljust(18) +\

# Plots
bins = binning(lep, varBins = varBins)

plotDict = {\
   "lepPt_loose":{'var':pt['loose'], "bins":bins['pt'], "decor":{"title": "Lepton p_{{T}} Plot", "y":"Events", "x":"%s p_{T} / GeV"%lepton, "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['pt'][1]-bins['pt'][0])},
   "lepPt_tight":{'var':pt['tight'], "bins":bins['pt'], "decor":{"title": "Lepton p_{{T}} Plot", "y":"Events", "x":"%s p_{T} / GeV"%lepton, "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['pt'][1]-bins['pt'][0])},
   "hybIso_loose":{ 'var':hybIso['loose'],  'bins':[10, 0, 25], 'decor':{'title':"Lepton hybIso Plot", 'x':"%s HI = I_{rel}*min(p_{T}, 25 GeV)"%lepton, 'y':"Events", 'log':[0,logy,0]}},
   "hybIso_tight":{ 'var':hybIso['tight'],  'bins':[10, 0, 25], 'decor':{'title':"Lepton hybIso Plot", 'x':"%s HI = I_{rel}*min(p_{T}, 25 GeV)"%lepton, 'y':"Events", 'log':[0,logy,0]}},
}
 
plotsDict = Plots(**plotDict)

if logy: plotMin = 1
else: plotMin = 0

plotList = {}
plotList['loose'] = ['lepPt_loose']
plotList['tight'] = ['lepPt_tight']
if not varBins: 
   plotList['loose'].append('hybIso_loose')
   plotList['tight'].append('hybIso_tight')

if doControlPlots:
   plots =                getPlots(samples, plotsDict, region['SR']['total'],       samplesList, plotList = plotList['tight'])# addOverFlowBin='both')
   regPlots     =        drawPlots(samples, plotsDict, region['SR']['total'],       samplesList, plotList = plotList['tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
   
   plots =                getPlots(samples, plotsDict, region['SR']['prompt'],      samplesList, plotList = plotList['tight'])
   regPlots_prompt =     drawPlots(samples, plotsDict, region['SR']['prompt'],      samplesList, plotList = plotList['tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
   
   plots =                getPlots(samples, plotsDict, region['looseCR']['total'],  samplesList, plotList = plotList['loose'])
   looseCRplots =        drawPlots(samples, plotsDict, region['looseCR']['total'],  samplesList, plotList = plotList['loose'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
   
   plots =                getPlots(samples, plotsDict, region['looseCR']['prompt'], samplesList, plotList = plotList['loose'])
   looseCRplots_prompt = drawPlots(samples, plotsDict, region['looseCR']['prompt'], samplesList, plotList = plotList['loose'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
   
plots =                   getPlots(samples, plotsDict, region['SR']['fakes'],       samplesList, plotList = plotList['tight'])
regPlots_fakes =         drawPlots(samples, plotsDict, region['SR']['fakes'],       samplesList, plotList = plotList['tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)

plots =                   getPlots(samples, plotsDict, region['looseCR']['fakes'],  samplesList, plotList = plotList['loose'])
looseCRplots_fakes =     drawPlots(samples, plotsDict, region['looseCR']['fakes'],  samplesList, plotList = plotList['loose'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)

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
   ratioTitle = "#epsilon_{TL}"

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

# MC Closure
SRplots_fakes = copy.deepcopy(regPlots_fakes)
fakesMC= SRplots_fakes['stacks']['bkg']['lepPt_tight'].Clone()

canvas2 = drawPlot(fakesMC, legend = leg, decor = plotsDict['lepPt_tight']['decor'], latexText = latex, ratio = (fakesEstimate, fakesMC), ratioLimits = [0,4], ratioTitle = "Pred./MC")
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
