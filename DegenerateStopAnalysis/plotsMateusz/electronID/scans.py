# scans.py
# Script to scan over all samples for the following scripts: eleIDeffs.py, deltaR_ratioPt.py, distributions.py, comparisons.py
# Author: Mateusz Zarucki

import os, sys
import argparse
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *

from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_mAODv2 import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.navidTools.getSamples_PP_mAODv2_7412pass2_scan import getSamples

mc_path     = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v3/RunIISpring15DR74_25ns"
signal_path = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v3/RunIISpring15DR74_25ns"
data_path   = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v3/Data_25ns"

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--scan", dest="scan",  help="Scan type", type=str, default="standard") #standard, deltaR_ratioPt, nMinus1, slices, comparisons
parser.add_argument("--lowPt", dest="lowPt",  help="Low electron pt selection", type=str, default=0)
parser.add_argument("-b", dest="batch",  help="Batch mode", action="store_true", default=False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
scan = args.scan
lowPt = args.lowPt

#Save
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronID/nMinus1/histogramCounts"

#Samples
privateSignals = ["s10FS", "s30", "s30FS", "s60FS", "t2tt30FS"]
officialSignals = ["s300_290", "s300_270", "s300_240"]
backgrounds1 = ["w", "tt"]
backgrounds2 = ["z", "qcd"]

samples = privateSignals + officialSignals + backgrounds1
#sampleList = privateSignals + backgrounds1

if scan == "standard" or scan == "nMinus1":
   samples += backgrounds2
#   samplesList += backgrounds2

#cmgPP = cmgTuplesPostProcessed(mc_path, signal_path, data_path)
#allSamples = getSamples(sampleList=samplesList, scan=True, useHT=False, cmgPP=cmgPP, getData=False)

#Electron ID Variables
variables = ["sigmaEtaEta", "hOverE", "ooEmooP", "d0", "dz", "MissingHits", "convVeto", "dEta", "dPhi"]

if scan == "standard" or scan == "nMinus1":
   samples += backgrounds2

   zooms = [0, 1]
   
   if scan == "standard": 
      
      IDs = ["standard", "manual", "iso"]
      isolations = ["miniRelIso", "relIso03", "relIso04"] #relIsoAn04
   
      for sample in samples:
      
         if sample == "qcd" or sample == "z": plots = ["misID", "misID2"]
         else: plots = ["efficiency", "misID", "misID2"]
      
         for ID in IDs:
            for plot in plots:
               for zoom in zooms: 
                  if ID == "standard":
                     os.system("python -b eleIDeffs.py --mvaWPs 1 --sample " + sample + " --id " + ID + " --plot " + plot + " --lowPt " + str(lowPt) + " --zoom " + str(zoom))
                  elif ID == "iso":
                     for iso in isolations:
                        os.system("python -b eleIDeffs.py --sample " + sample + " --id " + ID + " --plot " + plot + " --iso " + iso + " --lowPt " + str(lowPt) + " --zoom " + str(zoom))
                  else:
                     os.system("python -b eleIDeffs.py --sample " + sample + " --id " + ID + " --plot " + plot + " --lowPt " + str(lowPt) + " --zoom " + str(zoom))

   elif scan == "nMinus1":
      variables.append("None")
      for sample in samples:
        
         if sample == "qcd" or sample == "z": plots = ["misID", "misID2"]
         else: plots = ["efficiency", "misID", "misID2"]
         
         for plot in plots:
            if not lowPt: 
               if not os.path.exists(savedir + "/" + plot): os.makedirs(savedir + "/" + plot)
               #outfile = open(savedir + "/" + plot + "/histogramCounts_" + plot + "_" + allSamples[sample].name + ".txt", "w") #makes new file after each scan
               for var in variables:
                  os.system("python -b eleIDeffs.py --zoom 0 --sample " + sample + " --removedCut " + var + " --plot " + plot)
                  os.system("python -b eleIDeffs.py --zoom 1 --sample " + sample + " --removedCut " + var + " --plot " + plot)
            else:   
               if not os.path.exists(savedir + "/" + plot + "/lowPt"): os.makedirs(savedir + "/" + plot + "/lowPt")
               #outfile = open(savedir + "/" + plot + "/lowPt/histogramCounts_lowPt_" +  plot + "_" + allSamples[sample].name + ".txt", "w") #makes new file after each scan
               for var in variables:
                  os.system("python -b eleIDeffs.py --zoom 0 --lowPt 1 --sample " + sample + " --removedCut " + var + " --plot " + plot)
               #outfile.close()

elif scan == "slices": 
   slice_width = 5
   slices_low = range(5,30,slice_width)
   slices_up = [x + slice_width for x in slices_low]

   for sample in samples:
      for var in variables:
         os.system("python -b distributions.py" + " --sample " + sample + " --var " + var)
   
         for i in range(0,len(slices_up)):
            os.system("python -b distributions.py" + " --sample " + sample + " --var " + var + " --slice " + str(slices_low[i]) + " " + str(slices_up[i]))

elif scan == "deltaR_ratioPt":
   for sample in samples:
      os.system("python -b deltaR_ratioPt.py" + " --sample " + sample)

elif scan == "comparisons":
   os.system("\
   python -b comparisons.py --num manual --den standard;\
   python -b comparisons.py --num iso --den standard;\
   ")
