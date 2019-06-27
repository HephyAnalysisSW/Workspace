# Zpeak.py

import ROOT
import os, sys
import argparse
import importlib

import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import getPlots, drawPlots, setup_style, makeDir
from Workspace.DegenerateStopAnalysis.tools.degCuts import CutsWeights
from Workspace.DegenerateStopAnalysis.tools.degPlots import Plots
from Workspace.DegenerateStopAnalysis.samples.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.samplesInfo import getCutWeightOptions

# Sets TDR style
setup_style()

# Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--getData",        help = "Get data samples",            type = int, default = 1)
parser.add_argument("--dataset",        help = "Primary dataset",             type = str, default = "SingleMuon")
parser.add_argument("--dataEra",        help = "Data era",                    type = str, default = "C")
parser.add_argument("--options",        help = "Options",                     type = str, nargs = '+', default = ['noweight'])
parser.add_argument("--year",           help = "Year",                        type = str, default = "2018")
parser.add_argument("--region",         help = "Region",                      type = str, default = "Zpeak")
parser.add_argument("--Zinc",           help = "Z mass inclusive",            type = int, default = 0)
parser.add_argument("--promptOnly",     help = "Prompt leptons",              type = int, default = 0)
parser.add_argument("--highWeightVeto", help = "Veto highly weighted events", type = int, default = 0)
parser.add_argument("--plotList",       help = "Plot list",                   type = str, default = [], nargs = '+')
parser.add_argument("--logy",           help = "Toggle logy",                 type = int, default = 1)
parser.add_argument("--save",           help = "Toggle save",                 type = int, default = 1)
parser.add_argument("--verbose",        help = "Verbosity switch",            type = int, default = 0)
args = parser.parse_args()
if not len(sys.argv) > 1:
    print makeLine()
    print "No arguments given. Using default settings."
    print makeLine()

# arguments
getData = args.getData
dataset   = args.dataset
dataEra   = args.dataEra
options = args.options
year = args.year
region = args.region
Zinc = args.Zinc
promptOnly = args.promptOnly
highWeightVeto = args.highWeightVeto
plotList = args.plotList
logy = args.logy
save = args.save
verbose = args.verbose

if verbose:
    print makeDoubleLine()
    print "Plotting Z-peak distributions"
    print makeDoubleLine()

# samples
samplesList = [] #"ttx", "st", "vv", "dy5to50", "dy", "qcd", "z", "tt_2l", "tt_1l", "w"]

if year == "2016":
    era = "Summer16"
    campaign = "05Feb2018"
elif year == "2017":
    era = "Fall17"
    campaign = "14Dec2018"
elif year == "2018":
    era = "Autumn18"
    campaign = "14Dec2018"
else:
    print "Wrong year %s. Exiting."%year
    sys.exit()

if getData:
    dataset_name = "%s_Run%s%s_%s"%(dataset, year, dataEra, campaign)
    samplesList.append(dataset_name)

# cut and weight options

cutWeightOptions = getCutWeightOptions(
    lepCol = 'Lepton',
    lep = 'mu',
    lepTag = 'def',
    year = year,
    dataset = dataset,
    campaign = campaign,
    options = options 
    )

sampleDefPath = 'Workspace.DegenerateStopAnalysis.samples.nanoAOD_postProcessed.nanoAOD_postProcessed_' + era
sampleDef = importlib.import_module(sampleDefPath)
PP = sampleDef.nanoPostProcessed()
samples = getSamples(PP = PP, skim = 'oneLep', sampleList = samplesList, scan = False, useHT = True, getData = getData, settings = cutWeightOptions['settings'])

plotDict = {
   "mZ":   {  'bins':[50,5,255],         'decor':{'title':"Di-lepton System Invariant Mass",      'x':"M_{ll} / GeV",              'y':"Events", 'log':[0,logy,0]}},
   "ptZ":  {  'bins':[50,0,250],         'decor':{'title':"Di-lepton System Transverse Momentum", 'x':"p_{T_{ll}} / GeV",          'y':"Events", 'log':[0,logy,0]}},
   #"phiZ": {  'bins':[20,-3.15,3.15],    'decor':{'title':"Di-lepton System Phi",                 'x':"Dilepton System Phi / GeV", 'y':"Events", 'log':[0,logy,0]}},

   "metPt":     {'bins':[20,200,1000],   'decor':{'title':"MET",                  'x':"MET / GeV",               'y':"Events", 'log':[0,logy,0]}},
   "ht":        {'bins':[35,0,1400],     'decor':{'title':"H_{{T}}",              'x':"H_{T} / GeV",             'y':"Events", 'log':[0,logy,0]}},
   
   "lepPt" :    {'bins':[20,0,200],      'decor':{'title':"Lepton p_{{T}}",       'x':"Lepton p_{T} / GeV",      'y':"Events", 'log':[0,logy,0]}},
   "lepEta":    {'bins':[50, -2.5, 2.5], 'decor':{'title':"Lepton #eta",          'x':"Lepton #eta",             'y':"Events", 'log':[0,logy,0]}}, 

   "lepMt":     {'bins':[20,0,200],      'decor':{'title':"Lepton m_{{T}}",       'x':"Lepton m_{T} / GeV",      'y':"Events", 'log':[0,logy,0]}},
   "lepWpt":    {'bins':[20,0,200],      'decor':{'title':"Lepton Wp_{{T}}",      'x':"Lepton Wp_{T} / GeV",     'y':"Events", 'log':[0,logy,0]}},
   
   "weight":    {'bins':[50, 0, 50],     'decor':{'title':"Weight",               'x':"Weight",                  'y':"Events", 'log':[0,logy,0]}},
   "norm":      {'bins':[1, 0, 1],       'decor':{'title':"Normalisation",        'x':"Normalisation",           'y':"Events", 'log':[0,logy,0]}},
   }

cuts_weights = CutsWeights(samples, cutWeightOptions)

vars_dict = cuts_weights.cuts.vars_dict_format

for var in plotDict:
    plotDict[var]['var'] = vars_dict[var]
    #plotDict[var]['var'] = plotDict[var]['var'].format(lepCol = cutWeightOptions['settings']['lepCol'], jetCol = cutWeightOptions['settings']['jetCol'], tauCol = cutWeightOptions['settings']['tauCol'])

plotsDict = Plots(**plotDict)

if not plotList:
    plotList = ["mZ", "ptZ", "metPt"]

# cuts

regDef = region
if 'sr' in region:
    regDef = cuts_weights.cuts.removeCut(regDef, 'lepPt_lt_30') # pt inclusive

if Zinc:
    regDef = cuts_weights.cuts.removeCut(regDef, 'Zmass15')

if promptOnly:
    regDef = cuts_weights.cuts.addCut(regDef, 'prompt')

if highWeightVeto: 
    regDef = cuts_weights.cuts.addCut(regDef, 'highWeightVeto')

cuts_weights.cuts._update(reset = False)
cuts_weights._update()

plots_args = {'samples': samples, 'plotsDict':plotsDict, 'cut':[cuts_weights, regDef], 'sampleList':samplesList, 'plotList':plotList, 'lumi_weight':"target_lumi"}
getPlots_args  = dict({'addOverFlowBin':'both'}, **plots_args)
drawPlots_args = dict({'plotLimits':[1, 100], 'noms':[dataset_name], 'denoms':["bkg"], 'fom':False, 'fomLimits':[0,2], 'plotMin':10, 'normalize':False, 'save':False}, **plots_args)

plots_ = getPlots(**getPlots_args)
plots = drawPlots(**drawPlots_args)

# save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots
    tag = samples[samples.keys()[0]].dir.split('/')[9]
    optionsTag = '_'.join(options)
    savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/%s/Zpeak/%s"%(tag, year, optionsTag)
    suffix = "_%s_%s"%(region, optionsTag)
    if Zinc:
        suffix += "_Zinc"   
 
    if promptOnly:
         suffix += "_prompt"
         savedir += "/promptOnly"
    if highWeightVeto:
         suffix += "_highWeightVeto5"
         savedir += "/highWeightVeto5"
    
    makeDir("%s/root"%savedir)
    makeDir("%s/pdf"%savedir)
    
    for canv in plots['canvs']:
       plots['canvs'][canv][0].SaveAs("%s/Zpeak_%s%s.png"%(savedir, canv, suffix))
       plots['canvs'][canv][0].SaveAs("%s/root/Zpeak_%s%s.root"%(savedir, canv, suffix))
       plots['canvs'][canv][0].SaveAs("%s/pdf/Zpeak_%s%s.pdf"%(savedir, canv, suffix))
