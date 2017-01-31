# getSamplesCutsWeights.py
# Gets all cuts and weights for all samples using the baseline values from baselineSamplesInfo 

import sys
import argparse
import importlib
import Workspace.DegenerateStopAnalysis.tools.degCuts2 as degCuts
from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import cutWeightOptions
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed, ppDir, mc_path, data_path, signal_path
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.tools.degTools import getSampleTriggersFilters 

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--cmgUserDir", dest = "cmgUserDir",  help = "CMG user directory", type = str, default = "")
parser.add_argument("--cmgInAFS", dest = "cmgInAFS",  help = "cmgInAFS", type = bool, default = True)
parser.add_argument("--ppUserDir", dest = "ppUserDir",  help = "PP user directory", type = str, default = "")
parser.add_argument("--cmgTag", dest = "cmgTag",  help = "CMG Tag", type = str, default = "8020_mAODv2_v5")
parser.add_argument("--ppTag", dest = "ppTag",  help = "PP Tag", type = str, default = "v0")
parser.add_argument("--parameterSet", dest = "parameterSet",  help = "Parameter set", type = str, default = "analysisHephy_13TeV_2016_v2_1")
parser.add_argument("--samples", dest = "samples",  help = "Samples", type = str, nargs = "+", default = "all")
parser.add_argument("--signalScan", dest = "signalScan",  help = "Get signal scan", type = bool, default = True)
parser.add_argument("--getData", dest = "getData",  help = "Get data", type = bool, default = True)
parser.add_argument("--dataset", dest = "dataset",  help = "Data", type = str, default = "dblind")
parser.add_argument("--useHT", dest = "useHT",  help = "Use HT-binned samples", type = bool, default = True)
parser.add_argument("--skim", dest = "skim",  help = "Skim", type = str, default = "preIncLep")
args = parser.parse_args()
if not len(sys.argv) > 1:
   print "No arguments given. Using default settings."

# Arguments
if isinstance(args.samples, list): samplesList  = args.samples
else: samplesList = [args.samples]
cmgUserDir = args.cmgUserDir
cmgInAFS = args.cmgInAFS
ppUserDir = args.ppUserDir
cmgTag = args.cmgTag
ppTag = args.ppTag
parameterSet = args.parameterSet
signalScan = args.signalScan
getData = args.getData
dataset = args.dataset
useHT = args.useHT
skim = args.skim

### Samples ###

# CMG Tuples
cmgDict = {'tag':cmgTag, 'version':cmgTag.split('_')[2]}

if not cmgUserDir: #directory taken from cmgTuples sample definition file 
   cmg_MC_path =   'Workspace.DegenerateStopAnalysis.samples.cmgTuples.RunIISpring16MiniAODv2_%s'%cmgDict['version']
   cmg_data_path = 'Workspace.DegenerateStopAnalysis.samples.cmgTuples.Data2016_%s'%cmgDict['version']

   cmg_MC = importlib.import_module(cmg_MC_path)
   cmg_data = importlib.import_module(cmg_data_path)

   cmgDict['dir'] =         cmg_MC.sample_path_base
   cmgDict['mc_path'] =     cmg_MC.sample_path
   cmgDict['data_path'] =   cmg_data.sample_path
   cmgDict['signal_path'] = cmgDict['mc_path']

else: #directory taken from manual input
   if cmgInAFS: cmgDict['dir'] = "/afs/hephy.at/data/%s/cmgTuples/%s"%(cmgUserDir, cmgTag) #afs/hephy.at/data
   else:        cmgDict['dir'] = "/data/%s/cmgTuples/%s"%(cmgUserDir, cmgTag) #/data

   cmgDict['mc_path'] =     cmgDict['dir'] + "/RunIISpring16MiniAODv2"
   cmgDict['data_path'] =   cmgDict['dir'] + "/Data25ns"
   cmgDict['signal_path'] = cmgDict['mc_path']

# PP Tuples
ppDict = {'version':ppTag}

if not ppUserDir: #directory taken from PP tuples sample definition file
   ppDict['dir'] =         ppDir
   ppDict['mc_path'] =     mc_path
   ppDict['data_path'] =   data_path
   ppDict['signal_path'] = signal_path
else: #directory taken from manual input
   ppDict['dir'] = "/afs/hephy.at/data/%s/cmgTuples/postProcessed_mAODv2/%s/80X_postProcessing_%s/%s/step1"%(ppUserDir, cmgDict['tag'], ppDict['version'], parameterSet)
   ppDict['mc_path'] =     ppDict['dir'] + "/RunIISpring16MiniAODv2_%s"%cmgDict['version']
   ppDict['data_path'] =   ppDict['dir'] + "/Data2016_%s"%cmgDict['version']
   ppDict['signal_path'] = ppDict['mc_path']

if samplesList[0] == "all": samplesList = ['w', 'tt', 'qcd', 'z', 'dy', 'st', 'vv']

cmgPP = cmgTuplesPostProcessed(ppDict['mc_path'], ppDict['signal_path'], ppDict['data_path'])

samples = getSamples(cmgPP = cmgPP, skim = skim, sampleList = samplesList, scan = signalScan, useHT = useHT, getData = getData)

### Cuts and Weights ###
settings = cutWeightOptions['settings']
def_weights = cutWeightOptions['def_weights']
options = cutWeightOptions['options']

cuts = degCuts.Cuts(settings, def_weights, options)

cut_weights = {}

for reg in cuts.regions['bins_sum']['regions']:
   cut_weights[reg] = {}

   for samp in samples:
      c,w = cuts.getSampleCutWeight(samples[samp].name, cutListNames = [reg]) #, weightListNames = [])
      
      c,w = getSampleTriggersFilters(samples[samp], c, w)
      
      cut_weights[reg][samp] = (c,w)

if cut_weights:
   print "All cuts and weights for all samples saved in the cut_weights dictionary."
