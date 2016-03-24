#FoMscan.py
import os, sys
#import argparse
#
##Input options
#parser = argparse.ArgumentParser(description="Input options")
##parser.add_argument("--scan", dest="scan",  help="Scan type", type=str, default="standard") #standard, deltaR_ratioPt, nMinus1, slices
#parser.add_argument("-b", dest="batch",  help="Batch mode", action="store_true", default=False)
#args = parser.parse_args()
#if not len(sys.argv) > 1:
#   print makeLine()
#   print "No arguments given. Using default settings."
#   print makeLine()
#   #exit()

#Arguments
#scan = args.scan

#Electron ID Variables
WPs = ['None', 'Veto', 'Loose', 'Medium', 'Tight']
selections1 = ['NoSel', 'Presel']
selections2 = ['preselEle', 'sr1',  'sr1Loose', 'cr1Loose', 'crtt2', 'cr2']
selections3 = ['sr1abc']#, 'sr1abc_ptbin', 'mtabc', 'mtabc_ptbin', 'sr2_ptbin', 'cr1abc']

variables = ["sigmaEtaEta", "hOverE", "ooEmooP", "d0", "dz", "MissingHits", "convVeto", "dEta", "dPhi"]

#for sel in selections1:
#      os.system("python -b eleIdFoM.py --ID standard --WP None --selection " + sel) # " --removedCut " + var
#
#for sel in selections2:
#   for iWP in WPs:
#      os.system("python -b eleIdFoM.py --ID standard --WP " + iWP + " --selection " + sel) # " --removedCut " + var

for sel in selections3:
   for iWP in WPs:
      os.system("python -b eleIdFoM.py --ID standard --WP " + iWP + " --selection " + sel) # " --removedCut " + var
