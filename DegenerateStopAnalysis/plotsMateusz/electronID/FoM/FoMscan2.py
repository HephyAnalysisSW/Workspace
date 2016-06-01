#FoMscan2.py
import os, sys
import argparse
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import makeLine

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--ID", dest = "ID",  help = "Electron ID type", type = str, default = "standard") # standard, MVA, manual, nMinus1
parser.add_argument("--removedCut", dest = "removedCut",  help = "Variable removed from electron ID", type = str, default = "None") #"sigmaEtaEta" "dEta" "dPhi" "hOverE" "ooEmooP" "d0" "dz" "MissingHits" "convVeto"
parser.add_argument("--iso", dest = "iso",  help = "Apply isolation (hybIso03/04)", type = str, default = "") # hybIso03, hybIso04
parser.add_argument("--WP", dest = "WP",  help = "Electron ID Working Point", type = str, default = "None")
parser.add_argument("--doPlots", dest = "doPlots",  help = "Draw plots", type = int, default = 0)
parser.add_argument("--doCutFlow", dest = "doCutFlow",  help = "Make cut flow table", type = int, default = 0)
parser.add_argument("--doLimits", dest = "doLimits",  help = "Draw exclusion limit plot", type = int, default = 0)
parser.add_argument("--doYields", dest = "doYields",  help = "Make yields table", type = int, default = 0)
parser.add_argument("-b", dest = "batch",  help = "Batch mode", action = "store_true", default = False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Please choose draw options."
   print makeLine()
   exit()

#Arguments
ID = args.ID
removedCut = args.removedCut
iso = args.iso
WP = args.WP
doPlots = args.doPlots
doCutFlow = args.doCutFlow
doLimits = args.doLimits
doYields = args.doYields

##Electron ID WPs and SRs/CRs
#if ID == "MVA": WPs = ['None', 'WP80', 'WP90']
#else: WPs = ['None', 'Veto', 'Loose', 'Medium', 'Tight']

selections1 = ['nosel', 'presel']
selections2 = ['preselEle', 'sr1', 'sr2', 'cr1', 'cr2', 'crtt2'] #'sr1Loose', 'cr1Loose'

#variables = ["sigmaEtaEta", "hOverE", "ooEmooP", "dEta", "dPhi", "d0", "dz", "MissingHits", "convVeto"]

if ID != "nMinus1": removedCut = "None"

print makeLine()
print "Scanning over ID type: ", ID, " | WP: ", WP, " | Electron ID Cut Removed: ", removedCut, " | Isolation applied: ", iso
print makeLine()

if doPlots or doCutFlow:
   for sel in selections1:
         if iso: os.system("python -b eleIdFoM.py --ID " + ID + " --removedCut " + removedCut + " --WP None --selection " + sel + " --doPlots " + str(doPlots) + " --doCutFlow " + str(doCutFlow) + " --iso " + iso) 
         else: os.system("python -b eleIdFoM.py --ID " + ID + " --removedCut " + removedCut + " --WP None --selection " + sel + " --doPlots " + str(doPlots) + " --doCutFlow " + str(doCutFlow)) 
   
   for sel in selections2:
      if iso: os.system("python -b eleIdFoM.py --ID " + ID + " --removedCut " + removedCut + " --WP " + WP + " --selection " + sel + " --doPlots " + str(doPlots) + " --doCutFlow " + str(doCutFlow) + " --iso " + iso) 
      else: os.system("python -b eleIdFoM.py --ID " + ID + " --removedCut " + removedCut + " --WP " + WP + " --selection " + sel + " --doPlots " + str(doPlots) + " --doCutFlow " + str(doCutFlow)) 

if doLimits or doYields:
   if iso: os.system("python -b eleIdLimits.py --ID " + ID + " --removedCut " + removedCut + " --WP " + WP + " --doLimits " + str(doLimits) + " --doYields " + str(doYields) + " --iso " + iso)
   else: os.system("python -b eleIdLimits.py --ID " + ID + " --removedCut " + removedCut + " --WP " + WP + " --doLimits " + str(doLimits) + " --doYields " + str(doYields))
