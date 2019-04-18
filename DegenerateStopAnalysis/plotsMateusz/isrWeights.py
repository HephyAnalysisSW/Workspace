# isrWeights.py
# Script for plotting effect of ISR reweighting 

import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style, makeSimpleLatexTable, makeDir, makeLegend
from Workspace.DegenerateStopAnalysis.tools.degCuts2 import Cuts, CutsWeights
from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import getCutWeightOptions, triggers, filters
from Workspace.DegenerateStopAnalysis.samples.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.nanoAOD_postProcessed.nanoAOD_postProcessed_Summer16 import nanoPostProcessed
from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Sets TDR style
setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--isrWeight", dest = "isrWeight",  help = "ISR Weight", type = str, default = "isr_nIsr", choices = ['isr_nIsr', 'isr_Wpt', 'noweight'])
parser.add_argument("--sample", dest = "sample",  help = "Sample", type = str, default = "tt", choices = ['tt', 'w'])
parser.add_argument("--year", dest = "year",  help = "Year", type = str, default = "2016")
parser.add_argument("--region", dest = "region",  help = "Region", type = str, default = "presel")
parser.add_argument("--doYields", dest = "doYields",  help = "Calulate yields", type = int, default = 0)
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

# arguments
isrWeight = args.isrWeight
sample = args.sample
year = args.year
region = args.region
doYields = args.doYields
logy = args.logy
save = args.save
verbose = args.verbose

# samples
if sample == 'tt':
    samplesList = ['tt_1l', 'tt_2l']
else:
    samplesList = [sample]

cutWeightOptions = {}

cutWeightOptions[isrWeight] = getCutWeightOptions(
    year = year,
    options = [isrWeight]
    )

cutWeightOptions['noIsrWeight'] = getCutWeightOptions(
    year = year,
    options = ['noweight']
    )

PP = nanoPostProcessed()
samples = getSamples(PP = PP, skim = 'preIncLep', sampleList = samplesList, scan = False, useHT = True, getData = False, def_weights = [], settings = cutWeightOptions[isrWeight]['settings'])

if verbose:
    print makeLine()
    print "Using samples:"
    newLine()
    for s in samplesList:
        if s: print samples[s].name,":",s
        else: 
            print "!!! Sample " + sample + " unavailable."
            sys.exit(0)
 
plotDict = {
   "met"  : {'var':"MET_pt",                            'bins':[40,200,1000], 'decor':{"title":"MET",            'x':"E^{miss}_{T} / GeV", 'y':"Events", 'log':[0,logy,0]}},
   "ht"   : {'var':"ht_basJet_def",                     'bins':[40,200,1000], 'decor':{"title":"H_{{T}}",        'x':"H_{T} / GeV",        'y':"Events", 'log':[0,logy,0]}},
   "ct"   : {'var':"min(MET_pt,ht_basJet_def)",         'bins':[40,100,1000], 'decor':{"title":"C_{{T}}",        'x':"C_{T} / GeV",        'y':"Events", 'log':[0,logy,0]}},
   "lepPt": {'var':"Lepton_pt[IndexLepton_lep_def[0]]", 'bins':[20,0,200],    'decor':{'title':"Lepton p_{{T}}", 'x':"Lepton p_{T} / GeV", 'y':"Events", 'log':[0,logy,0]}},
   }
plotsDict = Plots(**plotDict)

plotsList = ["met", "ht", "ct", "lepPt"]

hists = {}
cuts_weights = {}
plots_ = {}
plots = {}

# reweighted

cuts_weights[isrWeight] = CutsWeights(samples, cutWeightOptions[isrWeight])
plots_[isrWeight] =  getPlots(samples, plotsDict, [cuts_weights[isrWeight], region], samplesList, plotList = plotsList, addOverFlowBin='both')
plots[isrWeight] =  drawPlots(samples, plotsDict, [cuts_weights[isrWeight], region], samplesList, plotList = plotsList, plotLimits = [1, 100], noms = None, denoms = None, fom = False, fomLimits = [0,2], plotMin = 10, normalize = False, save = False)
    
#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots
    tag = samples[samples.keys()[0]].dir.split('/')[9]
    savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/%s/isrWeights"%(tag, year)

    suffix = "_%s_%s"%(isrWeight, sample)

    makeDir("%s/root"%savedir) 
    makeDir("%s/pdf"%savedir) 

    for canv in plots[isrWeight]['canvs']:
        plots[isrWeight]['canvs'][canv][0].SaveAs("%s/%s%s_%s.png"%(savedir, canv, suffix, isrWeight))
        plots[isrWeight]['canvs'][canv][0].SaveAs("%s/root/%s%s_%s.root"%(savedir, canv, suffix, isrWeight))
        plots[isrWeight]['canvs'][canv][0].SaveAs("%s/pdf/%s%s_%s.pdf"%(savedir, canv, suffix, isrWeight))
    
# no weights
cuts_weights['noIsrWeight'] = CutsWeights(samples, cutWeightOptions['noIsrWeight'])
plots_['noIsrWeight'] =  getPlots(samples, plotsDict, [cuts_weights['noIsrWeight'], region], samplesList, plotList = plotsList, addOverFlowBin='both')
plots['noIsrWeight'] =  drawPlots(samples, plotsDict, [cuts_weights['noIsrWeight'], region], samplesList, plotList = plotsList, plotLimits = [1, 100], noms = None, denoms = None, fom = False, fomLimits = [0,2], plotMin = 10, normalize = False, save = False)
    
#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots
    for canv in plots['noIsrWeight']['canvs']:
        plots['noIsrWeight']['canvs'][canv][0].SaveAs("%s/%s%s_noIsrWeight.png"%(savedir, canv, suffix))
        plots['noIsrWeight']['canvs'][canv][0].SaveAs("%s/root/%s%s_noIsrWeight.root"%(savedir, canv, suffix))
        plots['noIsrWeight']['canvs'][canv][0].SaveAs("%s/pdf/%s%s_noIsrWeight.pdf"%(savedir, canv, suffix))

# ratio

hists[isrWeight] = {}
hists['noIsrWeight'] = {}

for plot in plotsList:

    for x in [isrWeight, 'noIsrWeight']:
        if sample == 'tt':
            hists[x][sample] = plots[x]['hists']['tt_1l'][plot].Clone() + plots[x]['hists']['tt_2l'][plot].Clone()
        else:
            hists[x][sample] = plots[x]['hists'][sample][plot].Clone()
    
    hists['noIsrWeight'][sample].SetFillColor(ROOT.kBlue-5)
    hists['noIsrWeight'][sample].SetFillColorAlpha(hists['noIsrWeight'][sample].GetFillColor(), 0.7)
    hists['noIsrWeight'][sample].SetFillStyle(3001)
    hists['noIsrWeight'][sample].SetMarkerSize(0)
    
    leg = makeLegend2()
    leg.SetBorderSize(1)
    leg.AddEntry(hists[isrWeight][sample], '%s (%s reweighted)'%(sample, isrWeight.replace('isr_','')), 'F')
    leg.AddEntry(hists['noIsrWeight'][sample], '%s (no weight)'%sample, 'F')
    
    ratio = drawPlot(hists[isrWeight][sample], ratio = (hists[isrWeight][sample], hists['noIsrWeight'][sample]), ratioTitle = "Ratio", ratioLimits = [0.5, 1.5], legend = leg, decor = {'log':[0,logy,0]})
    hists['noIsrWeight'][sample].Draw('histsame')
    
    #Save canvas
    if save: #web address: http://www.hephy.at/user/mzarucki/plots
        ratio['canvs'][0].SaveAs("%s/ratio_%s%s.png"%(savedir, plot, suffix))
        ratio['canvs'][0].SaveAs("%s/root/ratio_%s%s.root"%(savedir, plot, suffix))
        ratio['canvs'][0].SaveAs("%s/pdf/ratio_%s%s.pdf"%(savedir, plot, suffix))
