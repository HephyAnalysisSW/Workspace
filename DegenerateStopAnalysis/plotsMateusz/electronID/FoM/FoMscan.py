#FoMscan.py
import os, sys
import argparse
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--doPlots", dest="doPlots",  help="Draw plots", type=int, default=0)
parser.add_argument("--doYields", dest="doYields",  help="Make yields table", type=int, default=0)
parser.add_argument("--doLimits", dest="doLimits",  help="Draw exclusion limit plot", type=int, default=0)
parser.add_argument("--doCutFlow", dest="doCutFlow",  help="Make cut flow table", type=int, default=0)

#parser.add_argument("--scan", dest="scan",  help="Scan type", type=str, default="standard") #standard, deltaR_ratioPt, nMinus1, slices
parser.add_argument("-b", dest="batch",  help="Batch mode", action="store_true", default=False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Please choose draw options."
   print makeLine()
   exit()

#Arguments
doPlots = args.doPlots
doYields = args.doYields
doLimits = args.doLimits
doCutFlow = args.doCutFlow
#scan = args.scan

#Electron ID Variables
WPs = ['None', 'Veto', 'Loose', 'Medium', 'Tight']
selections1 = ['nosel', 'presel']
selections2 = ['preselEle', 'sr1', 'sr1Loose', 'sr2', 'cr1', 'cr1Loose', 'cr2', 'crtt2']
#selections3 = ['sr1abc', 'sr1abc_ptbin', 'mtabc', 'mtabc_ptbin', 'sr2_ptbin', 'cr1abc']

variables = ["sigmaEtaEta", "hOverE", "ooEmooP", "d0", "dz", "MissingHits", "convVeto", "dEta", "dPhi"]

if doPlots or doYields:
   for sel in selections1:
         os.system("python -b eleIdFoM.py --ID standard --WP None --selection " + sel + " --doPlots " + str(doPlots) + " --doYields " + str(doYields)) # " --removedCut " + var
   
   for sel in selections2:
      for iWP in WPs:
         os.system("python -b eleIdFoM.py --ID standard --WP " + iWP + " --selection " + sel + " --doPlots " + str(doPlots) + " --doYields " + str(doYields)) # " --removedCut " + var

if doLimits or doCutFlow:
   for iWP in WPs:
      os.system("python -b eleIdLimits.py --ID standard --WP " + iWP + " --doLimits " + str(doLimits) + " --doCutFlow " + str(doCutFlow)) # " --removedCut " + var
