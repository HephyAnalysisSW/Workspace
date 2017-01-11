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
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from pprint import pprint
from array import array
from math import pi, sqrt #cos, sin, sinh, log
from fakeRegions import regions

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--lep", dest = "lep",  help = "Lepton", type = str, default = "lep")
parser.add_argument("--region", dest = "reg",  help = "Measurement or application region", type = str, default = "application_sr1")
parser.add_argument("--getData", dest = "getData",  help = "Get data", type = int, default = 1)
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
getData = args.getData
logy = args.logy
save = args.save
verbose = args.verbose

#Samples
cmgPP = cmgTuplesPostProcessed()

if "measurement" in reg:
   skim = "oneLepGood_HT800"
   samplesList = ["w", "tt", "qcd"]
elif "application" in reg:
   skim = "preIncLep"
   samplesList = ["qcd", "z", "dy", "tt", "w"] #"st" "vv" 
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
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/fakesEstimation/noRunH"%tag

   savedir += "/%s/estimation/%s"%(reg, lepton)
   
   suffix = "%s_%s"%(reg, lep)
   
   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

#####
# Root file with fake rate

fakeRateDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate/"
fakeRateFile = "FakeRate_TightToLoose_lepPt_%s_data-EWK.root"%lep

f1 = ROOT.TFile(fakeRateDir + fakeRateFile)

fakeRate = {}

fakeRate['pt'] = f1.Get("c1").GetPrimitive("c1_2").GetPrimitive("ratio_data-EWK_pt")

#####

selection = regions(reg, lep)

if verbose:
   print makeLine()
   print "Using the following selection: ",
   pprint(selection)
   print makeLine()

index = selection['index']

pt = {}
eta = {}
mt = {}

for WP in ['loose', 'tight']:
   pt[WP] = "LepGood_pt[%s]"%index[WP]
   mt[WP] = "LepGood_mt[%s]"%index[WP]
   eta[WP] = "abs(LepGood_eta[%s])"%index[WP]

region = CutClass(reg, [
   ["region", selection[reg]],
   ["tight", selection['tight']],
   ], baseCut = None)

region_fakes = CutClass(reg + "_fakes", [
   ["region", selection[reg]],
   ["loose", selection['tight']],
   ["fake", selection['fakeTight']],
   ], baseCut = None)

region_prompt = CutClass(reg + "_prompt", [
   ["region", selection[reg]],
   ["loose", selection['tight']],
   ["fake", selection['promptTight']],
   ], baseCut = None)

looseFakeCR = CutClass(reg + "_looseFakeCR", [
   ["region", selection[reg]],
   ["loose", selection['loose']],
   ["fake", selection['fakeLoose']],
   ], baseCut = None)

#Sets TDR style
setup_style()

plotDict = {\
   "lepPt_loose":{'var':pt['loose'], "bins":[20,0,100], "decor":{"title": "Lepton p_{{T}} Plot", "y":"Events", "x":"%s p_{T} / GeV"%lepton, "log":[0,logy,0]}},
   "lepPt_tight":{'var':pt['tight'], "bins":[20,0,100], "decor":{"title": "Lepton p_{{T}} Plot", "y":"Events", "x":"%s p_{T} / GeV"%lepton, "log":[0,logy,0]}},
   #"lepEta":{'var': eta, "bins":[20,0,3],   "decor":{"title": "Lepton |#eta| Plot",  "y":"Events", "x":"|#eta|",                "log":[0,1,0]}},
   #"lepMt":{ 'var': mt,  "bins":[30,0,150], "decor":{"title": "Lepton m_{{T}} Plot", "y":"Events", "x":"%s m_{T} / GeV"%lepton, "log":[0,1,0]}},
}
plotsDict = Plots(**plotDict)

if logy: plotMin = 1
else: plotMin = 0

plots1 =           getPlots(samples, plotsDict, region,        samplesList, plotList = ['lepPt_tight'])# addOverFlowBin='both')
regPlots =        drawPlots(samples, plotsDict, region,        samplesList, plotList = ['lepPt_tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = "RATIO", fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)

plots2 =           getPlots(samples, plotsDict, region_fakes,  samplesList, plotList = ['lepPt_tight'])
regPlots_fakes =  drawPlots(samples, plotsDict, region_fakes,  samplesList, plotList = ['lepPt_tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = "RATIO", fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)

plots3 =           getPlots(samples, plotsDict, region_prompt, samplesList, plotList = ['lepPt_tight'])
regPlots_prompt = drawPlots(samples, plotsDict, region_prompt, samplesList, plotList = ['lepPt_tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = "RATIO", fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)

plots4 =            getPlots(samples, plotsDict, looseFakeCR,  samplesList, plotList = ['lepPt_loose'])
looseFakeCRPlots = drawPlots(samples, plotsDict, looseFakeCR,  samplesList, plotList = ['lepPt_loose'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = "RATIO", fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)

###
# Multiplying fake rate histogram with total bkg
looseCRPlots = copy.deepcopy(looseFakeCRPlots)

canvas = looseCRPlots['canvs']['lepPt_loose'][0].DrawClone()
#canvas.cd(1)
pad1 = looseCRPlots['canvs']['lepPt_loose'][1].DrawClone()
pad1.cd()

fakeBkgs = looseCRPlots['stacks']['bkg']['lepPt_loose'].GetStack().Last() #NOTE: last stack in GetStack() array is the sum of all stacks
fakeBkgs.SetFillColor(ROOT.kBlue-9)
fakeBkgs.Draw("hist")

looseCRPlots['latex'].DrawLatex(0.16,0.92, looseCRPlots['latexText']['L'])
looseCRPlots['latex'].DrawLatex(0.65,0.92, looseCRPlots['latexText']['R'])

#canvas.RedrawAxis()
canvas.Modified()
canvas.Update()
#canvas[p][cMain].cd()
#canvas[p][cMain].Update()

#fakeRate['pt'] = ROOT.TH1D()
#fakeRate['2D'].ProjectionX().Copy(fakeRate['pt'])#ProfileX()
#fakeRate['pt'].Sumw2()
#fakeRate['pt'].Scale(1./Nbins)

#fakeRate['pt'].Sumw2()
#fakeBkgs.Sumw2()

#fakes = multiplyHists(fakeBkgs, fakeRate['pt'])
fakes = fakeBkgs.Clone()*fakeRate['pt'].Clone()
fakes.SetLineWidth(2)
fakes.SetName("fakes")
fakes.Draw("same")

canvas.Modified()
canvas.Update()

#canvas2 = looseCRPlots['canvs']['lepPt_loose'][0].DrawClone()
#pad2 = looseCRPlots['canvs']['lepPt_loose'][1].DrawClone()
#pad2.cd()
#
#fakeRate['pt'].Draw() 
#
#canvas2.Modified()
#canvas2.Update()

##FakeRate values #NOTE: x-check
#momentum = 7 
#binX = fakeRate['pt'].GetXaxis().FindBin(momentum)
##binY = fakeRate['pt'].GetYaxis().FindBin(abs(eta))
#bin = fakeRate['pt'].GetBin(binX)#, binY)
#ratio = fakeRate['pt'].GetBinContent(bin)
#ratio_err = fakeRate['pt'].GetBinError(bin)

#print "Fake rate for pt ", momentum, " GeV = ", ratio, "+-", ratio_err 

#yld = fakeBkgs.GetBinContent(bin) 
#yld_err = fakeBkgs.GetBinError(bin)
#
#print "Yield in that bin", yld, "+-", yld_err 

if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   for canv in regPlots['canvs']:
      regPlots['canvs'][canv][0].SaveAs("%s/%s_%s.png"%(savedir, suffix, canv))
      regPlots['canvs'][canv][0].SaveAs("%s/root/%s_%s.root"%(savedir, suffix, canv))
      regPlots['canvs'][canv][0].SaveAs("%s/pdf/%s_%s.pdf"%(savedir, suffix, canv))
   for canv in regPlots_fakes['canvs']:
      regPlots_fakes['canvs'][canv][0].SaveAs("%s/%s_%s_fakes.png"%(savedir, suffix, canv))
      regPlots_fakes['canvs'][canv][0].SaveAs("%s/root/%s_%s_fakes.root"%(savedir, suffix, canv))
      regPlots_fakes['canvs'][canv][0].SaveAs("%s/pdf/%s_%s_fakes.pdf"%(savedir, suffix, canv))
   for canv in regPlots_prompt['canvs']:
      regPlots_prompt['canvs'][canv][0].SaveAs("%s/%s_%s_prompt.png"%(savedir, suffix, canv))
      regPlots_prompt['canvs'][canv][0].SaveAs("%s/root/%s_%s_prompt.root"%(savedir, suffix, canv))
      regPlots_prompt['canvs'][canv][0].SaveAs("%s/pdf/%s_%s_prompt.pdf"%(savedir, suffix, canv))
   for canv in looseFakeCRPlots['canvs']:
      looseFakeCRPlots['canvs'][canv][0].SaveAs("%s/looseFakeCR_%s_%s.png"%(savedir, suffix, canv))
      looseFakeCRPlots['canvs'][canv][0].SaveAs("%s/root/looseFakeCR_%s_%s.root"%(savedir, suffix, canv))
      looseFakeCRPlots['canvs'][canv][0].SaveAs("%s/pdf/looseFakeCR_%s_%s.pdf"%(savedir, suffix, canv))
   
   canvas.SaveAs("%s/fakesEstimation_%s.png"%(savedir, suffix))
   canvas.SaveAs("%s/root/fakesEstimation_%s.root"%(savedir, suffix))
   canvas.SaveAs("%s/pdf/fakesEstimation_%s.pdf"%(savedir, suffix))

   #canvas2.SaveAs("%s/fakeRate_%s.png"%(savedir, suffix))
   #canvas2.SaveAs("%s/root/fakeRate_%s.root"%(savedir, suffix))
   #canvas2.SaveAs("%s/pdf/fakeRate_%s.pdf"%(savedir, suffix))
