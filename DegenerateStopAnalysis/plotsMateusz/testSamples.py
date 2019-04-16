import ROOT
import glob
import argparse
import sys, os
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import makeLine, makeDoubleLine
from Workspace.DegenerateStopAnalysis.samples.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.nanoAOD_postProcessed.nanoAOD_postProcessed_Summer16 import nanoPostProcessed
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_Summer16 import cmgTuplesPostProcessed, ppDir, mc_path, data_path, signal_path

#Input options
parser = argparse.ArgumentParser(description = "Input options")
#parser.add_argument("--ppUserDir", dest = "ppUserDir",  help = "PP user directory", type = str, default = "")
#parser.add_argument("--ppTag", dest = "ppTag",  help = "PP Tag", type = str, default = "v0")
#parser.add_argument("--parameterSet", dest = "parameterSet",  help = "Parameter set", type = str, default = "analysisHephy_13TeV_2016_v2_3")
parser.add_argument("--samples", dest = "samples",  help = "Samples", type = str, nargs = "+", default = "all")
parser.add_argument("--signalScan", action = "store_true",  help = "Compare bins")
parser.add_argument("--getData", action = "store_true",  help = "Get data")
parser.add_argument("--dataset", dest = "dataset",  help = "Data", type = str, default = "dblind")
parser.add_argument("--useHT", dest = "useHT",  help = "Use HT", type = int, default = 1)
parser.add_argument("--skim", dest = "skim",  help = "Skim", type = str, default = "preIncLep")
parser.add_argument("--verbose", action = "store_true",  help = "Verbose")
parser.add_argument("-b", dest = "batch",  help = "Batch mode", action = "store_true", default = False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()

# Arguments
if isinstance(args.samples, list): samplesList  = args.samples
else: samplesList = [args.samples]
#ppUserDir = args.ppUserDir
#ppTag = args.ppTag
#parameterSet = args.parameterSet
signalScan = args.signalScan
getData = args.getData
dataset = args.dataset
useHT = args.useHT
skim = args.skim
verbose = args.verbose

if samplesList[0] == "all": samplesList = ['w', 'tt', 'qcd', 'z', 'dy', 'dy5to50', 'st', 'vv', 'ttx']

if getData:  
   samplesList.append(dataset)

PP = nanoPostProcessed()
samples = getSamples(PP = PP, skim = skim, sampleList = samplesList, scan = signalScan, useHT = useHT, getData = getData)

if verbose:
   print makeLine()
   print "Using samples:"
   newLine()
   for s in samplesList:
      if s: print samples[s].name,":",s
      else:
         print "!!! Sample " + sample + " unavailable."
         sys.exit(0)
