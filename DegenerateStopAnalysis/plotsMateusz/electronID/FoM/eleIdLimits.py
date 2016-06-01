#eleIdLimits.py
import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.degTools import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.cutsEle import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.cmgTuplesPostProcessed_mAODv2 import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_PP_mAODv2_7412pass2_scan import getSamples

from array import array
from math import pi, sqrt #cos, sin, sinh, log

ROOT.gStyle.SetOptStat(0) #1111 #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis

#Samples
privateSignals = ["s10FS", "s30", "s30FS", "s60FS", "t2tt30FS"]
backgrounds = ["w","tt", "z","qcd"]

samplesList = backgrounds # + privateSignals
samples = getSamples(sampleList = samplesList, scan = True, useHT = True, getData = False)#, cmgPP = cmgPP) 

officialSignals = ["s300_290", "s300_270", "s300_240"] #FIXME: crosscheck if these are in allOfficialSignals

allOfficialSignals = samples.massScanList()
#allOfficialSignals = [s for s in samples if samples[s]['isSignal'] and not samples[s]['isData'] and s not in privateSignals and s not in backgrounds] 
allSignals = privateSignals + allOfficialSignals
allSamples = allSignals + backgrounds

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--doLimits", dest = "doLimits",  help = "Draw exclusion limit plot", type = int, default = 0)
parser.add_argument("--doYields", dest = "doYields",  help = "Make yields table", type = int, default = 1)
parser.add_argument("--ID", dest = "ID",  help = "Electron ID type", type = str, default = "standard") # "standard" "manual" "nMinus1"
parser.add_argument("--removedCut", dest = "removedCut",  help = "Variable removed from electron ID", type = str, default = "None") #"sigmaEtaEta" "hOverE" "ooEmooP" "dEta" "dPhi" "d0" "dz" "MissingHits" "convVeto"
parser.add_argument("--iso", dest = "iso",  help = "Apply isolation", type = str, default = "")
parser.add_argument("--WP", dest = "WP",  help = "Electron ID Working Point", type = str, default = "None")
parser.add_argument("--save", dest = "save",  help = "Toggle save", type = int, default = 1)
parser.add_argument("-b", dest = "batch",  help = "Batch mode", action = "store_true", default = False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
doLimits = args.doLimits 
doYields = args.doYields 
ID = args.ID 
removedCut = args.removedCut 
iso = args.iso
WP = args.WP
save = args.save

if ID == "nMinus1":
   string1 = "no_" + removedCut
   string2 = "_no_" + removedCut
else: 
   string1 = ""
   string2 = ""

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronID/FoM"
   savedir1 = savedir + "/" + ID
   savedir2 = savedir + "/" + ID

   if iso:
      savedir1 += "/iso/" + iso
      savedir2 += "/iso/" + iso
      isoString = "_" + iso
   else:
      isoString = ""
   
   savedir1 += "/limits"
   savedir2 += "/yields"    

   if not os.path.exists("%s/cards/%s/%s%s"%(savedir1, string1, WP, string2)): os.makedirs("%s/cards/%s/%s%s"%(savedir1, string1, WP, string2))
   if not os.path.exists("%s/tex/%s/%s%s"%(savedir1, string1, WP, string2)): os.makedirs("%s/tex/%s/%s%s"%(savedir1, string1, WP, string2))
   if not os.path.exists("%s/tex/%s/%s%s"%(savedir2, string1, WP, string2)): os.makedirs("%s/tex/%s/%s%s"%(savedir2, string1, WP, string2))
   
   #if os.path.isfile(limitPkl):
   #      limits = pickle.load(file(limitPkl))

#Gets all cuts (electron, SR, CR) for given electron ID
eleIDsel = electronIDs(ID, removedCut, iso)
allCuts = cutClasses(eleIDsel, ID)

#for s in samples.massScanList(): samples[s].weight = "weight" #removes ISR reweighting from official mass scan signal samples
#for s in samples: samples[s].tree.SetAlias("eleSel", allCuts[WP]['eleSel'])

print makeLine()
print "ID type: ", ID, " | Electron ID WP: ", WP, " | Electron ID Cut Removed: ", removedCut, " | Isolation applied: ", iso
print makeLine()

if doLimits:
   selectedSamples = allOfficialSignals + backgrounds 
   
   limits={}
   
   setEventListToChains(samples, selectedSamples, allCuts['None']['presel'])

   allYields = Yields(samples, selectedSamples, allCuts[WP]['runI'], cutOpt = "list2", weight = "weight", pklOpt = False, tableName = "RunI_" + WP + string2 + isoString, nDigits = 2, err = True, verbose = True, nSpaces = 10)
   JinjaTexTable(allYields, pdfDir = savedir1, texDir = "%s/tex/%s/%s%s%s/"%(savedir1, string1, WP, string2, isoString), caption = "Yields: RunI Reload Electrons (" + WP + string2 + " WP)", transpose = True)
   
   for sig in allOfficialSignals:
      mstop, mlsp = [int(x) for x in sig[1:].rsplit("_")]
      print makeLine()
      print "signal, mstop, mlsp: ", sig, " ", mstop, " ", mlsp
      print makeLine()
      
      try: limits[mstop]
      except KeyError: limits[mstop]={}
      
      limits[mstop][mlsp] = getLimit(allYields, sig = sig, outDir = "%s/cards/%s"%(savedir1, string1), calc_limit = True) #, postfix = WP + string2 + isoString

   #pickle.dump(limits, open(savedir + "/cards/limits.pkl",'w'))
   exclCanv, exclPlot = drawExpectedLimit(limits, plotDir = "%s/%s/ExpectedLimit_eleID_%s%s%s.png"%(savedir1, string1, WP, string2, isoString), bins = None, key = None, title = "Expected Limits (%s %s %s Electron ID)"%(WP, string1, iso))
   #exclCanv.SetName("ExpectedLimit_eleID_%s.pkl"%(WP))

if doYields:
   selectedSamples = officialSignals + backgrounds 
   setEventListToChains(samples, selectedSamples, allCuts['None']['presel'])
   fewSignalYields = Yields(samples, selectedSamples, allCuts[WP]['runI'], cutOpt = "list2", weight = "weight", pklOpt = False, tableName = "RunI_" + WP + string2 + isoString, nDigits = 2, err = True, verbose = True, nSpaces = 10)
   JinjaTexTable(fewSignalYields, pdfDir = savedir2, texDir = "%s/%s/tex/%s%s%s/"%(savedir2, string1, WP, string2, isoString), caption = "Cut Flow Table: RunI Reload Electrons (" + WP + string2 + " WP)", transpose = False)
