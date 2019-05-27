# plotAllBranches.py
# Simple script used to plot all branches of a sample (useful for checking inherent cuts) 
# Mateusz Zarucki 2016

import ROOT
import glob
import argparse
import sys, os
import pprint as pp

from Workspace.DegenerateStopAnalysis.tools.degTools import makeDir
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import makeLine, makeDoubleLine
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.tools.getSamples_8012 import getSamples

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
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()

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

cmgDict['mc_path'] =     cmgDict['dir'] + "/RunIISpring16MiniAODv2"
cmgDict['signal_path'] = cmgDict['dir'] + "/RunIISpring16MiniAODv2"
cmgDict['data_path'] =   cmgDict['dir'] + "/Data25ns"

ppsDict = {'version':ppsTag}
ppsDict['dir'] = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/%s/80X_postProcessing_%s/analysisHephy_13TeV_2016_v0/step1"%(cmgDict['tag'], ppsDict['version'])
ppsDict['mc_path'] =     ppsDict['dir'] + "/RunIISpring16MiniAODv2_%s"%cmgDict['version']
ppsDict['data_path'] =   ppsDict['dir'] + "/Data2016_%s"%cmgDict['version']
ppsDict['signal_path'] = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/8012_mAODv2_v3_1/80X_postProcessing_v10_1/analysisHephy_13TeV_2016_v0/step1/RunIISpring16MiniAODv2_v3" 

if verbose:
   print makeDoubleLine()
   print "Plotting all branches for the following tuples:"
   print pp.pprint(ppsDict)
   print makeDoubleLine()

if samplesList[0] == "all": samplesList = ['vv', 'st', 'dy', 'qcd', 'tt', 'w']

if getData:  
   samplesList.append(dataset)

cmgPP = cmgTuplesPostProcessed(ppsDict['mc_path'], ppsDict['signal_path'], ppsDict['data_path'])

samples = getSamples(cmgPP = cmgPP, skim = skim, sampleList = samplesList, scan = signalScan, useHT = useHT, getData = getData)

if 'tt' in samplesList and not useHT: 
   samplesList.remove('tt')
   samplesList.append('ttInc')

canv = ROOT.TCanvas("canv", "canvas", 1800, 1500)

for samp in samplesList:
   if verbose:
      print "Plotting branches of sample", samples[samp]['name'], "with", skim, "skim" 
      print makeDoubleLine()
   
   branches = samples[samp].tree.GetListOfBranches().Clone()
      
   for i,branch in enumerate(branches):
      branchName = branch.GetName()
      samples[samp].tree.Draw(branchName)
      canv.Update()   

      if save:
         savedir = "%s/plots/%s/%s"%(ppsDict['dir'], skim, samp)
         makeDir(savedir + "/root")
         
         canv.SaveAs("%s/%s.png"%(savedir, branchName))
         canv.SaveAs("%s/root/%s.root"%(savedir, branchName))
