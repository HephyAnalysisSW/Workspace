# testSamples.py
# Script for testing samples interactively 
# Mateusz Zarucki 2016

import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style
from Workspace.DegenerateStopAnalysis.tools.bTagWeights import bTagWeights
#from Workspace.DegenerateStopAnalysis.tools.degCuts import *
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Sets TDR style
setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--cmgTag", dest = "cmgTag",  help = "CMG Tag", type = str, default = "8020_mAODv2_v0")
parser.add_argument("--ppsTag", dest = "ppsTag",  help = "PPS Tag", type = str, default = "v0")
parser.add_argument("--getData", dest = "getData",  help = "Get data samples", type = int, default = 1)
parser.add_argument("--dataset", dest = "dataset",  help = "Data", type = str, default = "dblind")
parser.add_argument("--skim", dest = "skim",  help = "Skim", type = str, default = "preIncLep")
parser.add_argument("--useHT", dest = "useHT",  help = "Use HT binned samples", type = int, default = 1)
parser.add_argument("--verbose", dest = "verbose",  help = "Verbosity switch", type = int, default = 0)
parser.add_argument("-b", dest = "batch",  help = "Batch mode", action = "store_true", default = False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
cmgTag = args.cmgTag
ppsTag = args.ppsTag
getData = args.getData
dataset = args.dataset
skim = args.skim
useHT = args.useHT
verbose = args.verbose

#Samples
cmgDict = {'tag':cmgTag,
           'version':cmgTag.split('_')[2],
           'dir':"/data/nrad/cmgTuples/" + cmgTag}

ppsDict = {'version':ppsTag}
ppsDict['dir'] = "/afs/hephy.at/data/mzarucki01/cmgTuples/postProcessed_mAODv2/%s/80X_postProcessing_%s/analysisHephy_13TeV_2016_v2_1/step1"%(cmgDict['tag'], ppsDict['version'])
ppsDict['mc_path'] =     ppsDict['dir'] + "/RunIISpring16MiniAODv2_%s"%cmgDict['version']
ppsDict['data_path'] =   ppsDict['dir'] + "/Data2016_%s"%cmgDict['version']
ppsDict['signal_path'] = ppsDict['mc_path'] 

cmgPP = cmgTuplesPostProcessed(ppsDict['mc_path'], ppsDict['signal_path'], ppsDict['data_path'])

if skim == "preIncLep": 
   samplesList = ["qcd", "tt", "w"] #"vv", "st", "qcd", "z", "dy", "tt", "w"]
   if getData:  
      samplesList.append(dataset)
elif skim == "oneLep": 
   samplesList = ["vv", "tt", "dy"]
   if getData:
      samplesList.append(dataset)

samples = getSamples(cmgPP = cmgPP, skim = skim, sampleList = samplesList, scan = False, useHT = useHT, getData = getData) 

if verbose:
   print makeLine()
   print "Using samples:"
   newLine()
   for s in samplesList:
      if s: print samples[s].name,":",s
      else: 
         print "!!! Sample " + sample + " unavailable."
         sys.exit(0)
