# shapeComparison.py
# Script for comparing W and TT shape (superimposed) 
# Mateusz Zarucki 2016

import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style, makeSimpleLatexTable, makeDir, makeLegend
from Workspace.DegenerateStopAnalysis.tools.degCuts2 import Cuts, CutsWeights
from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import cutWeightOptions, triggers, filters
#from Workspace.DegenerateStopAnalysis.tools.colors import colors
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_Summer16 import cmgTuplesPostProcessed
#from Workspace.DegenerateStopAnalysis.tools.mvaTools import getMVATrees
from Workspace.HEPHYPythonTools import u_float
from pprint import pprint
from array import array
from math import pi, sqrt

#Sets TDR style
setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--getData", dest = "getData",  help = "Get data samples", type = int, default = 0)
parser.add_argument("--region", dest = "region",  help = "Region", type = str, default = "presel")
parser.add_argument("--promptOnly", dest = "promptOnly",  help = "Prompt leptons", type = int, default = 1)
parser.add_argument("--scale", dest = "scale",  help = "Scale", type = int, default = 0)
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
getData = args.getData
region = args.region
promptOnly = args.promptOnly
scale = args.scale
logy = args.logy
save = args.save
verbose = args.verbose

if verbose:
   print makeDoubleLine()
   print "Plotting MC distributions"
   print makeDoubleLine()

if scale: logy = 0

#Samples
samplesList = ["tt_1l", "tt_2l", "w"]
#samplesList = ["vv", "st", "qcd", "z", "dy", "tt", "w"]
if getData: 
   data = "dblind"
   samplesList.append(data)

cmgPP = cmgTuplesPostProcessed()
samples = getSamples(cmgPP = cmgPP, skim = 'preIncLep', sampleList = samplesList, scan = False, useHT = True, getData = getData, def_weights = [])

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
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/WTTplots"%tag
   #savedir += "/" + skim
   #if btag: savedir += "/" + btag
   #else: savedir += "/no_btag"
   suffix = "_" + region

   if promptOnly: suffix += "_prompt"  
   if scale: suffix += "_areaNormalised"
 
   makeDir("%s/root"%savedir)
   makeDir("%s/pdf"%savedir)

plotDict = {
   "lepPt" : {'var':"LepGood_pt[IndexLepGood_lep_def[0]]", "bins":[10,0,200], "nMinus1":"", "decor":{"title":"lepPt", "x":"Lepton p_{T}", "y":"Events", 'log':[0,logy,0]}},
   }
plotsDict = Plots(**plotDict)

cuts_weights = CutsWeights(samples, cutWeightOptions)

# pt inclusive
if 'sr' in region:
   cuts_weights.cuts.removeCut(region, 'lepPt_lt_30')
   ptInc = '_no_lepPt_lt_30'
else:
   ptInc = ''

if promptOnly:
   cuts_weights.cuts.addCut(region + ptInc, 'prompt')
   prompt = '_plus_prompt'
else:
   prompt = ''

cuts_weights.cuts._update(reset = False)
cuts_weights._update()

plots_ =  getPlots(samples, plotsDict, [cuts_weights.cuts, region + ptInc + prompt], samplesList, plotList = ['lepPt'], addOverFlowBin='both')
plots =  drawPlots(samples, plotsDict, [cuts_weights.cuts, region + ptInc + prompt], samplesList, plotList = ['lepPt'], plotLimits = [1, 100], denoms = ["tt_1l"], noms = ["w"], fom = "RATIO", fomLimits = [0,1.8], plotMin = 1, normalize = False, save = False)

hists = {}

if scale:
   hists['tt_1l'] = plots['hists']['tt_1l']['lepPt']
   hists['tt_2l'] = plots['hists']['tt_2l']['lepPt']
   hists['tt'] = hists['tt_1l'] + hists['tt_2l']
   hists['w'] = plots['hists']['w']['lepPt']
   hists['tt'].SetFillColorAlpha(hists['tt'].GetFillColor(), 0.7)
   #hist['w'].SetFillColorAlpha(hist_w.GetFillColor(), 0.80)
   
   hists['w'].Scale(1/hists['w'].Integral())
   hists['tt'].Scale(1/hists['tt'].Integral())
   
   hists['w'].Draw('hist')
   #hists['w'].GetYaxis().SetTitle()
   hists['tt'].Draw('histsame')
  
   errBarHist1 = hists['w'].Clone()
   errBarHist2 = hists['tt'].Clone()

   errBarHist1.SetFillColor(ROOT.kBlue-5)
   errBarHist2.SetFillColor(ROOT.kBlue-5)
   errBarHist1.SetFillStyle(3001)
   errBarHist2.SetFillStyle(3001)
   errBarHist1.SetMarkerSize(0)
   errBarHist2.SetMarkerSize(0)
   errBarHist1.Draw("E2same")
   errBarHist2.Draw("E2same")
 
   if not logy: 
      hists['w'].SetMinimum(0)
      hists['w'].SetMaximum(0.3)#25)
   
   leg = plots['legs'][0].Clone()
   leg.Clear()
   leg.AddEntry(hists['w'], 'WJets', 'F')
   leg.AddEntry(hists['tt'], 'TT', 'F')
   leg.Draw('same')
   
   latex = ROOT.TLatex()
   latex.SetNDC()
   latex.SetTextSize(0.04)
   
   latex.DrawLatex(0.16,0.92,"#font[22]{CMS Simulation}")
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   plots['canvs']['lepPt'][2].cd()
   ratio = hists['w'].Clone()
   ratio.Divide(hists['tt'])
   ratio.SetMinimum(0)
   ratio.SetMaximum(3)
   ratio.SetFillColor(ROOT.kBlue-5)
   ratio.SetFillStyle(3001)
   ratio.GetXaxis().SetTitleSize(0.1)
   ratio.GetXaxis().SetTitleOffset(0.8)
   ratio.GetYaxis().SetTitle("W/TT Ratio")
   ratio.GetYaxis().SetTitleSize(0.1)
   ratio.GetYaxis().SetTitleOffset(0.4)
   ratio.GetYaxis().CenterTitle()
   ratio.Draw("E2") #adds shaded area around error bars
   ratio.Draw("same")
   ROOT.gPad.Modified()
   ROOT.gPad.Update()

#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots
      for canv in plots['canvs']:
         #if plot['canvs'][canv][0]:
         plots['canvs'][canv][0].SaveAs("%s/WTTshapeComparison_%s%s.png"%(savedir, canv, suffix))
         plots['canvs'][canv][0].SaveAs("%s/root/WTTshapeComparison_%s%s.root"%(savedir, canv, suffix))
         plots['canvs'][canv][0].SaveAs("%s/pdf/WTTshapeComparison_%s%s.pdf"%(savedir, canv, suffix))
