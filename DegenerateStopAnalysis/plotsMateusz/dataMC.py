# dataMC.py

import ROOT
import os, sys
import argparse
import importlib

import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style, makeSimpleLatexTable, makeDir, makeLegend
from Workspace.DegenerateStopAnalysis.tools.degCuts2 import Cuts, CutsWeights
from Workspace.DegenerateStopAnalysis.samples.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import getCutWeightOptions, triggers, filters

# Sets TDR style
setup_style()

# Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--getData", dest = "getData",  help = "Get data samples", type = int, default = 1)
parser.add_argument("--year", dest = "year",  help = "Year", type = str, default = "2016")
parser.add_argument("--region", dest = "region",  help = "Region", type = str, default = "presel")
parser.add_argument("--promptOnly", dest = "promptOnly",  help = "Prompt leptons", type = int, default = 0)
parser.add_argument("--highWeightVeto", dest = "highWeightVeto",  help = "Veto highly weighted events", type = int, default = 1)
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
getData = args.getData
year = args.year
region = args.region
promptOnly = args.promptOnly
highWeightVeto = args.highWeightVeto
logy = args.logy
save = args.save
verbose = args.verbose

if verbose:
   print makeDoubleLine()
   print "Plotting MC distributions"
   print makeDoubleLine()

# samples
samplesList = ["ttx", "st", "vv", "dy5to50", "dy", "qcd", "z", "tt_2l", "tt_1l", "w"]

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

if getData:
   dataset = 'MET' 
   dataset_name = "%s_Run%s_%s"%(dataset, year, campaign)
   samplesList.append(dataset_name)

# cut and weight options
    
options = ['trig_eff', 'pu', 'isr_Wpt', 'isr_nIsr']

if year == "2016":
    options.append('lepSF')

cutWeightOptions = getCutWeightOptions(
    year = year,
    dataset = dataset,
    campaign = campaign,
    options = options 
    )

sampleDefPath = 'Workspace.DegenerateStopAnalysis.samples.nanoAOD_postProcessed.nanoAOD_postProcessed_' + era
sampleDef = importlib.import_module(sampleDefPath)
PP = sampleDef.nanoPostProcessed()
samples = getSamples(PP = PP, skim = 'preIncLep', sampleList = samplesList, scan = False, useHT = True, getData = getData, def_weights = [], settings = cutWeightOptions['settings'])

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
   "met":       {'var':"MET_pt",                             'bins':[40,200,1000],   'decor':{'title':"MET",                  'x':"MET / GeV",               'y':"Events", 'log':[0,logy,0]}},
   "ht":        {'var':"ht_basJet_def",                      'bins':[75,0,1500],     'decor':{'title':"H_{{T}}",              'x':"H_{T} / GeV",             'y':"Events", 'log':[0,logy,0]}},
   
   "nJets":     {'var':"nJet_basJet_def",                    'bins':[10,0,10],       'decor':{'title':"Number of Jets",       'x':"Number of Jets",          'y':"Events", 'log':[0,logy,0]}},
   "nSoftJets": {'var':"nJet_softJet_def",                   'bins':[10,0,10],       'decor':{'title':"Number of Soft Jets",  'x':"Number of Soft Jets",     'y':"Events", 'log':[0,logy,0]}},
   "nHardJets": {'var':"nJet_hardJet_def",                   'bins':[10,0,10],       'decor':{'title':"Number of Hard Jets",  'x':"Number of Hard Jets",     'y':"Events", 'log':[0,logy,0]}},
   "nBJets":    {'var':"nJet_bJet_def",                      'bins':[10,0,10],       'decor':{'title':"Number of B Jets",     'x':"Number of B Jets",        'y':"Events", 'log':[0,logy,0]}},
   "isrPt" :    {'var':"Jet_pt[IndexJet_isrJet_def[0]]" ,    'bins':[45,100,1000],   'decor':{'title':"Leading Jet p_{{T}}",  'x':"Leading Jet p_{T} / GeV", 'y':"Events", 'log':[0,logy,0]}}, 
   "delPhi":    {'var':"dPhi_j1j2_vetoJet_def",              'bins':[8, 0, 3.14],    'decor':{'title':"deltaPhi(j1,j2)",      'x':"#Delta#phi(j1,j2)",       'y':"Events", 'log':[0,logy,0]}},

   "lepPt" :    {'var':"Lepton_pt[IndexLepton_lep_def[0]]",  'bins':[20,0,200],      'decor':{'title':"Lepton p_{{T}}",       'x':"Lepton p_{T} / GeV",      'y':"Events", 'log':[0,logy,0]}},
   "muPt" :     {'var':"Lepton_pt[IndexLepton_mu_def[0]]",   'bins':[20,0,200],      'decor':{'title':"Muon p_{{T}}",         'x':"Muon p_{T} / GeV",        'y':"Events", 'log':[0,logy,0]}},
   "elePt" :    {'var':"Lepton_pt[IndexLepton_el_def[0]]",   'bins':[20,0,200],      'decor':{'title':"Electron p_{{T}}",     'x':"Electron p_{T} / GeV",    'y':"Events", 'log':[0,logy,0]}},
   "lepEta":    {'var':"Lepton_eta[IndexLepton_lep_def[0]]", 'bins':[50, -2.5, 2.5], 'decor':{'title':"Lepton #eta",          'x':"Lepton #eta",             'y':"Events", 'log':[0,logy,0]}}, 
   "muEta":     {'var':"Lepton_eta[IndexLepton_mu_def[0]]",  'bins':[48, -2.4, 2.4], 'decor':{'title':"Muon #eta",            'x':"Muon #eta",               'y':"Events", 'log':[0,logy,0]}}, 
   "eleEta":    {'var':"Lepton_eta[IndexLepton_el_def[0]]",  'bins':[50, -2.5, 2.5], 'decor':{'title':"Electron #eta",        'x':"Electron #eta",           'y':"Events", 'log':[0,logy,0]}}, 

   "lepWpt" :   {'var':"Lepton_Wpt[IndexLepton_lep_def[0]]", 'bins':[20,0,200],      'decor':{'title':"Lepton Wp_{{T}}",      'x':"Lepton Wp_{T} / GeV",     'y':"Events", 'log':[0,logy,0]}},
   
   "weight":    {'var':"weight_lumi",                        'bins':[50, 0, 50],     'decor':{'title':"Weight",               'x':"weight",                  'y':"Events", 'log':[0,logy,0]}},
   "norm":      {'var':"1",                                  'bins':[1, 0, 1],       'decor':{'title':"Normalisation",        'x':"Normalisation",           'y':"Events", 'log':[0,logy,0]}},
   }
plotsDict = Plots(**plotDict)

plotList = ['met', 'ht', 'nJets', 'nSoftJets', 'nHardJets', 'nBJets', 'isrPt', 'delPhi', 'lepPt', 'lepEta', 'muPt', 'muEta', 'elePt', 'eleEta', 'lepWpt', 'weight', 'norm']

# cuts

cuts_weights = CutsWeights(samples, cutWeightOptions)

regDef = region
if 'sr' in region:
   regDef = cuts_weights.cuts.removeCut(regDef, 'lepPt_lt_30') # pt inclusive

if promptOnly:
   regDef = cuts_weights.cuts.addCut(regDef, 'prompt')

if highWeightVeto: 
   regDef = cuts_weights.cuts.addCut(regDef, 'highWeightVeto')

cuts_weights.cuts._update(reset = False)
cuts_weights._update()

plots_ =  getPlots(samples, plotsDict, [cuts_weights, regDef], samplesList, plotList = plotList, addOverFlowBin='both')
plots =  drawPlots(samples, plotsDict, [cuts_weights, regDef], samplesList, plotList = plotList, plotLimits = [1, 100], noms = [dataset_name], denoms = ["bkg"], fom = "RATIO", fomLimits = [0,2], plotMin = 10, normalize = False, save = False)

#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   tag = samples[samples.keys()[0]].dir.split('/')[9]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/%s/dataMC"%(tag, year)
   #savedir += "/" + skim
   #if btag: savedir += "/" + btag
   #else: savedir += "/no_btag"
   suffix = "_" + region

   if promptOnly:
        suffix += "_prompt"
        savedir += "/promptOnly"
   if highWeightVeto:
        suffix += "_highWeightVeto5"
        savedir += "/highWeightVeto5"
 
   makeDir("%s/root"%savedir)
   makeDir("%s/pdf"%savedir)

   for canv in plots['canvs']:
      plots['canvs'][canv][0].SaveAs("%s/dataMC_%s%s.png"%(savedir, canv, suffix))
      plots['canvs'][canv][0].SaveAs("%s/root/dataMC_%s%s.root"%(savedir, canv, suffix))
      plots['canvs'][canv][0].SaveAs("%s/pdf/dataMC_%s%s.pdf"%(savedir, canv, suffix))
