# compareSamples.py
# Script for comparing nanoAOD and CMG post-processed samples 

import ROOT
import os, sys
import argparse
import importlib

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
parser.add_argument("--sample", dest = "sample",  help = "Sample", type = str, default = "all")
parser.add_argument("--options", dest = "options",  help = "Options", type = str, nargs = '+', default = ["noweight"])
parser.add_argument("--year", dest = "year",  help = "Year", type = str, default = "2016")
parser.add_argument("--region", dest = "region",  help = "Region", type = str, default = "presel")
parser.add_argument("--removeCut", dest = "removeCut",  help = "Remove cut", type = str, default = None)
parser.add_argument("--promptOnly", dest = "promptOnly",  help = "Prompt leptons", type = int, default = 0)
parser.add_argument("--highWeightVeto", dest = "highWeightVeto",  help = "Veto highly weighted events", type = int, default = 0)
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
sample = args.sample
options = args.options
year = args.year
region = args.region
removeCut = args.removeCut
promptOnly = args.promptOnly
highWeightVeto = args.highWeightVeto
doYields = args.doYields
logy = args.logy
save = args.save
verbose = args.verbose

print options

# samples
if sample == 'all':
    samplesList = ["ttx", "vv", "dy5to50", "dy", "qcd", "z", "tt_2l", "tt_1l", "w"] # "st" # FIXME
else:
    samplesList = [sample]

if year == "2016":
    era = "Summer16"
    campaign = "05Feb2018"
elif year == "2017":
    era = "Fall17"
    campaign = "14Dec2018"
elif year == "2018":
    era = "Autumn18"
    campaign = "14Sep2018"
else:
    print "Wrong year %s. Exiting."%year
    sys.exit()

cutWeightOptions = {}
cutWeightOptions['nanoAOD'] = getCutWeightOptions(
    year = year,
    campaign = campaign, 
    options = options
    )

cutWeightOptions['CMG'] = getCutWeightOptions(
    year = year,
    campaign = campaign,
    lepCol = "LepGood",
    jetCol = "Jet",
    tauCol = "Tau",
    cmgVars = True, 
    options = options
    )

sampleDefPaths = {}
sampleDefs = {}
PP = {}
samples = {}

sampleDefPaths['nanoAOD'] = 'Workspace.DegenerateStopAnalysis.samples.nanoAOD_postProcessed.nanoAOD_postProcessed_' + era
sampleDefPaths['CMG']     = 'Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_' + era

for x in sampleDefPaths:
    sampleDefs[x] = importlib.import_module(sampleDefPaths[x])
    if x == 'nanoAOD':
        PP[x] = sampleDefs[x].nanoPostProcessed()
    elif x == 'CMG':
        PP[x] = sampleDefs[x].cmgTuplesPostProcessed()
    samples[x] = getSamples(PP = PP[x], skim = 'preIncLep', sampleList = samplesList, scan = False, useHT = True, getData = False, def_weights = [], settings = cutWeightOptions[x]['settings'])

if verbose:
    print makeLine()
    print "Using samples:"
    newLine()
    for s in samplesList:
        if s: print samples[s].name,":",s
        else: 
            print "!!! Sample " + sample + " unavailable."
            sys.exit(0)

plotDict = {}
plotsDict = {}

plotDict['nanoAOD'] = {
   "met"  : {'var':"MET_pt",                            'bins':[20,200,1000], 'decor':{"title":"MET",              'x':"E^{miss}_{T} / GeV",   'y':"Events", 'log':[0,logy,0]}},
   "ht"   : {'var':"ht_basJet_def",                     'bins':[20,200,1000], 'decor':{"title":"H_{{T}}",          'x':"H_{T} / GeV",          'y':"Events", 'log':[0,logy,0]}},
   "ct"   : {'var':"min(MET_pt,ht_basJet_def)",         'bins':[20,100,1000], 'decor':{"title":"C_{{T}}",          'x':"C_{T} / GeV",          'y':"Events", 'log':[0,logy,0]}},
   "lepPt": {'var':"Lepton_pt[IndexLepton_lep_def[0]]", 'bins':[20,0,200],    'decor':{'title':"Lepton p_{{T}}",   'x':"Lepton p_{T} / GeV",   'y':"Events", 'log':[0,logy,0]}},
   "muPt" : {'var':"Lepton_pt[IndexLepton_mu_def[0]]",  'bins':[20,0,200],    'decor':{'title':"Muon p_{{T}}",     'x':"Muon p_{T} / GeV",     'y':"Events", 'log':[0,logy,0]}},
   "elePt": {'var':"Lepton_pt[IndexLepton_el_def[0]]",  'bins':[20,0,200],    'decor':{'title':"Electron p_{{T}}", 'x':"Electron p_{T} / GeV", 'y':"Events", 'log':[0,logy,0]}},
   }
plotsDict['nanoAOD'] = Plots(**plotDict['nanoAOD'])

plotDict['CMG'] = {
   "met"  : {'var':"met",                                 'bins':[20,200,1000], 'decor':{"title":"MET",              'x':"E^{miss}_{T} / GeV",   'y':"Events", 'log':[0,logy,0]}},
   "ht"   : {'var':"ht_basJet_def",                       'bins':[20,200,1000], 'decor':{"title":"H_{{T}}",          'x':"H_{T} / GeV",          'y':"Events", 'log':[0,logy,0]}},
   "ct"   : {'var':"min(met,ht_basJet_def)",              'bins':[20,100,1000], 'decor':{"title":"C_{{T}}",          'x':"C_{T} / GeV",          'y':"Events", 'log':[0,logy,0]}},
   "lepPt": {'var':"LepGood_pt[IndexLepGood_lep_def[0]]", 'bins':[20,0,200],    'decor':{'title':"Lepton p_{{T}}",   'x':"Lepton p_{T} / GeV",   'y':"Events", 'log':[0,logy,0]}},
   "muPt" : {'var':"LepGood_pt[IndexLepGood_mu_def[0]]",  'bins':[20,0,200],    'decor':{'title':"Muon p_{{T}}",     'x':"Muon p_{T} / GeV",     'y':"Events", 'log':[0,logy,0]}},
   "elePt": {'var':"LepGood_pt[IndexLepGood_el_def[0]]",  'bins':[20,0,200],    'decor':{'title':"Electron p_{{T}}", 'x':"Electron p_{T} / GeV", 'y':"Events", 'log':[0,logy,0]}},
   }
plotsDict['CMG'] = Plots(**plotDict['CMG'])

plotsList = ["met", "ht", "ct", "lepPt", "muPt", "elePt"]

hists = {}
plots_ = {}
plots = {}
cuts_weights = {}
    
regDef = {'nanoAOD':region, 'CMG':region}

for x in ['nanoAOD', 'CMG']:
    cuts_weights[x] = CutsWeights(samples[x], cutWeightOptions[x])

    if 'sr' in region:
        regDef[x] = cuts_weights[x].cuts.removeCut(regDef[x], 'lepPt_lt_30') # pt inclusive

    if removeCut:
        regDef[x] = cuts_weights[x].cuts.removeCut(regDef[x], removeCut)
    
    if promptOnly:
        regDef[x] = cuts_weights[x].cuts.addCut(regDef[x], 'prompt')
    
    if highWeightVeto:
        regDef[x] = cuts_weights[x].cuts.addCut(regDef[x], 'highWeightVeto')

    cuts_weights[x].cuts._update(reset = False)
    cuts_weights[x]._update()

assert regDef['nanoAOD'] == regDef['CMG']

plots_['nanoAOD'] =  getPlots(samples['nanoAOD'], plotsDict['nanoAOD'], [cuts_weights['nanoAOD'], regDef[x]], samplesList, plotList = plotsList, addOverFlowBin='both')
plots['nanoAOD'] =  drawPlots(samples['nanoAOD'], plotsDict['nanoAOD'], [cuts_weights['nanoAOD'], regDef[x]], samplesList, plotList = plotsList, plotLimits = [1, 100], noms = None, denoms = None, fom = False, fomLimits = [0,2], plotMin = 10, normalize = False, save = False)
    
# save canvas
if save: # web address: http://www.hephy.at/user/mzarucki/plots
    tags = {'nanoAOD': samples['nanoAOD'][samples['nanoAOD'].keys()[0]].dir.split('/')[9], 'CMG': samples['CMG'][samples['CMG'].keys()[0]].dir.split('/')[7] + "/" + samples['CMG'][samples['CMG'].keys()[0]].dir.split('/')[8]}
    optionsTag = '_'.join(options)
    savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/%s/compareSamples/%s/%s/%s/%s"%(tags['nanoAOD'], year, tags['CMG'], region, sample, optionsTag)
    suffix = "_%s_%s_%s"%(sample, regDef['nanoAOD'], optionsTag)

    if promptOnly:
        suffix += "_prompt"
        savedir += "/promptOnly"
    if highWeightVeto:
        suffix += "_highWeightVeto5"
        savedir += "/highWeightVeto5"

    makeDir("%s/root"%savedir) 
    makeDir("%s/pdf"%savedir) 

    for canv in plots['nanoAOD']['canvs']:
        plots['nanoAOD']['canvs'][canv][0].SaveAs("%s/nanoAOD_%s%s.png"%(savedir, canv, suffix))
        plots['nanoAOD']['canvs'][canv][0].SaveAs("%s/root/nanoAOD_%s%s.root"%(savedir, canv, suffix))
        plots['nanoAOD']['canvs'][canv][0].SaveAs("%s/pdf/nanoAOD_%s%s.pdf"%(savedir, canv, suffix))
    
plots_['CMG'] =  getPlots(samples['CMG'], plotsDict['CMG'], [cuts_weights['CMG'], regDef[x]], samplesList, plotList = plotsList, addOverFlowBin='both')
plots['CMG'] =  drawPlots(samples['CMG'], plotsDict['CMG'], [cuts_weights['CMG'], regDef[x]], samplesList, plotList = plotsList, plotLimits = [1, 100], noms = None, denoms = None, fom = False, fomLimits = [0,2], plotMin = 10, normalize = False, save = False)
    
# save canvas
if save: # web address: http://www.hephy.at/user/mzarucki/plots
    for canv in plots['CMG']['canvs']:
        plots['CMG']['canvs'][canv][0].SaveAs("%s/CMG_%s%s.png"%(savedir, canv, suffix))
        plots['CMG']['canvs'][canv][0].SaveAs("%s/root/CMG_%s%s.root"%(savedir, canv, suffix))
        plots['CMG']['canvs'][canv][0].SaveAs("%s/pdf/CMG_%s%s.pdf"%(savedir, canv, suffix))

# ratio
hists['nanoAOD'] = {}
hists['CMG'] = {}

for plot in plotsList:

    for x in ['nanoAOD', 'CMG']:
        if sample == 'all':
            hists[x][sample] = plots[x]['hists'][samplesList[0]][plot].Clone()
            hists[x][sample].SetName(sample)
            hists[x][sample].Reset()
            for s in samplesList:
                hists[x][sample].Add(plots[x]['hists'][s][plot].Clone())
        else: 
            hists[x][sample] = plots[x]['hists'][sample][plot].Clone()
    
    hists['CMG'][sample].SetFillColor(ROOT.kBlue-5)
    hists['CMG'][sample].SetFillColorAlpha(hists['CMG'][sample].GetFillColor(), 0.7)
    hists['CMG'][sample].SetFillStyle(3001)
    hists['CMG'][sample].SetMarkerSize(0)
    
    leg = makeLegend2()
    leg.SetBorderSize(1)
    leg.AddEntry(hists['nanoAOD'][sample], '%s (nanoAOD)'%sample, 'F')
    leg.AddEntry(hists['CMG'][sample], '%s (CMG)'%sample, 'F')
    
    ratio = drawPlot(hists['nanoAOD'][sample], ratio = (hists['nanoAOD'][sample], hists['CMG'][sample]), ratioTitle = "Ratio", ratioLimits = [0, 2], legend = leg, decor = {'log':[0,logy,0]})
    hists['CMG'][sample].Draw('histsame')
    
    #Save canvas
    if save: #web address: http://www.hephy.at/user/mzarucki/plots
        ratio['canvs'][0].SaveAs("%s/ratio_%s%s.png"%(savedir, plot, suffix))
        ratio['canvs'][0].SaveAs("%s/root/ratio_%s%s.root"%(savedir, plot, suffix))
        ratio['canvs'][0].SaveAs("%s/pdf/ratio_%s%s.pdf"%(savedir, plot, suffix))
