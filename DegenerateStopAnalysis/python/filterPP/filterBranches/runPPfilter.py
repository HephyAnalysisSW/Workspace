# runPPfilter.py
# Simple script used to filter root tuples. Uses filterPP.py script.
# Mateusz Zarucki 2016
# (based on Ivan's scripts)

import ROOT
import argparse
import sys, os, time
import pprint as pp

from Workspace.DegenerateStopAnalysis.tools.degTools import makeDir
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import makeLine, makeDoubleLine
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.tools.getSamples_8012 import getSamples
from Workspace.HEPHYPythonTools.user import username
from filterPP import dofilter

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--cmgTag", dest = "cmgTag",  help = "CMG Tag", type = str, default = "8012_mAODv2_v3")
parser.add_argument("--ppsTag", dest = "ppsTag",  help = "PPS Tag", type = str, default = "v10")
parser.add_argument("--samples", dest = "samples",  help = "Samples", type = str, nargs = "+", default = "all")
parser.add_argument("--signalScan", dest = "signalScan",  help = "Signal scan", type = int, default = 0)
parser.add_argument("--getData", dest = "getData",  help = "Get data samples", type = int, default = 0)
parser.add_argument("--dataset", dest = "dataset",  help = "Data", type = str, default = "dblind")
parser.add_argument("--useHT", dest = "useHT",  help = "Use HT", type = int, default = 0)
parser.add_argument("--skim", dest = "skim",  help = "Skim", type = str, default = "preIncLep")
parser.add_argument("--save", dest = "save",  help = "Save", type = int, default = 1)
parser.add_argument("--verbose", dest = "verbose",  help = "Verbosity switch", type = int, default = 0)
parser.add_argument("-b", dest = "batch",  help = "Batch mode", action = "store_true", default = False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print "No arguments given. Using default settings."

# Arguments
if isinstance(args.samples, list): samplesList  = args.samples
else: samplesList = [args.samples]
cmgTag = args.cmgTag
ppsTag = args.ppsTag
signalScan = args.signalScan
getData = args.getData
dataset = args.dataset
useHT = args.useHT
skim = args.skim
save = args.save
verbose = args.verbose

# Directories
cmgDict = {'tag':cmgTag,
           'version':cmgTag.split('_')[2],
           'dir':"/data/nrad/cmgTuples/" + cmgTag}

ppsDict = {'version':ppsTag}
ppsDict['dir'] = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/%s/80X_postProcessing_%s/analysisHephy_13TeV_2016_v0/step1"%(cmgDict['tag'], ppsDict['version'])
ppsDict['mc_path'] =     ppsDict['dir'] + "/RunIISpring16MiniAODv2_%s"%cmgDict['version']
ppsDict['data_path'] =   ppsDict['dir'] + "/Data2016_%s"%cmgDict['version']
ppsDict['signal_path'] = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/8012_mAODv2_v3_1/80X_postProcessing_v10_1/analysisHephy_13TeV_2016_v0/step1/RunIISpring16MiniAODv2_v3"

if verbose:
   print makeDoubleLine()
   print "Filtering the following tuples:"
   print pp.pprint(ppsDict)
   print makeDoubleLine()

if samplesList[0] == "all": samplesList = ['vv', 'st', 'dy', 'qcd', 'tt']#, 'w']

if getData:
   samplesList.append(dataset)

cmgPP = cmgTuplesPostProcessed(ppsDict['mc_path'], ppsDict['signal_path'], ppsDict['data_path'])

samples = getSamples(cmgPP = cmgPP, skim = skim, sampleList = samplesList, scan = signalScan, useHT = useHT, getData = getData)

if 'tt' in samplesList and not useHT:
   samplesList.remove('tt')
   samplesList.append('ttInc')

for samp in samplesList:
   if verbose:
      print "Filtering sample", samples[samp]['name']
      print makeDoubleLine()
   
   savedir = "/afs/hephy.at/data/%s01/filteredTuples/cmgTuples/%s"%(username, samples[samp].sample['dir'].split("cmgTuples/")[1])
   makeDir(savedir)
   
   outfile = savedir + "/" + samples[samp].sample['name'] + ".root"
   
   #startM = time.clock()
   #startC = time.time()
   
   #print 'start time:',time.strftime('%X %x %Z')  
   #filterscript = "filterPP.py"
   dofilter(samples[samp].tree, outfile)
   #print 'end time:',time.strftime('%X %x %Z')
           
   #endM = time.clock()
   #endC = time.time()
   
   #print "-"*20,"total","-"*20
   #print "machine:", (endM-startM), "wall clock:", (endC-startC)
