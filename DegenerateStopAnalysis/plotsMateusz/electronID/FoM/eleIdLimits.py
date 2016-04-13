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
backgrounds=["w","tt", "z","qcd"]

samplesList = backgrounds #privateSignals + 
samples = getSamples(sampleList=samplesList, scan=True, useHT=False, getData=False)#, cmgPP=cmgPP) 

officialSignals = ["s300_290", "s300_270", "s300_240"] #FIXME: crosscheck if these are in allOfficialSignals

allOfficialSignals = samples.massScanList()
#allOfficialSignals = [s for s in samples if samples[s]['isSignal'] and not samples[s]['isData'] and s not in privateSignals and s not in backgrounds] 
allSignals = privateSignals + allOfficialSignals
allSamples = allSignals + backgrounds

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--doLimits", dest="doLimits",  help="Draw exclusion limit plot", type=int, default=0)
parser.add_argument("--doCutFlow", dest="doCutFlow",  help="Draw cut flow table", type=int, default=1)
parser.add_argument("--ID", dest="ID",  help="Electron ID type", type=str, default="standard") # "standard" "manual" "nMinus1"
parser.add_argument("--WP", dest="WP",  help="Electron ID Working Point", type=str, default="None")
parser.add_argument("--removedCut", dest="removedCut",  help="Variable removed from electron ID", type=str, default="None") #"sigmaEtaEta" "dEta" "dPhi" "hOverE" "ooEmooP" "d0" "dz" "MissingHits" "convVeto"
parser.add_argument("--save", dest="save",  help="Toggle save", type=int, default=1)
parser.add_argument("--zoom", dest="zoom",  help="Toggle zoom", type=int, default=1)
parser.add_argument("-b", dest="batch",  help="Batch mode", action="store_true", default=False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
doLimits = args.doLimits 
doCutFlow = args.doCutFlow 
ID = args.ID 
WP = args.WP
removedCut = args.removedCut 
zoom = args.zoom
save = args.save
#if ID == "iso": isolation = args.iso

#Geometric divisions
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap
etaAcc = 2.5 #eta acceptance

#Pt division for MVA ID
ptSplit = 10 #we have above and below 10 GeV categories 

#Number of Leptons (hadronic, semileptonic, dileptonic)
nSel = ["(nLepGood == 0)", "(nLepGood == 1)", "(nLepGood == 2)"]

#Bin size 
#nbins = 100
xmin = 0
#xmax = 1000

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronID/FoM"
   savedir1 = savedir + "/limits/" + WP
   savedir2 = savedir + "/yields/" + WP
   if not os.path.exists(savedir1 + "/cards"): os.makedirs(savedir1 + "/cards")
   if not os.path.exists(savedir1 + "/tex"): os.makedirs(savedir1 + "/tex")
   if not os.path.exists(savedir2 + "/tex"): os.makedirs(savedir2 + "/tex")
   
   #if os.path.isfile(limitPkl):
   #      limits = pickle.load(file(limitPkl))

#Gets all cuts (electron, SR, CR) for given electronID
allCuts = cutClasses(ID) #standard manual nMinus1

#for s in samples.massScanList(): samples[s].weight = "weight" #removes ISR reweighting from official mass scan signal samples
for s in samples: samples[s].tree.SetAlias("eleSel", allCuts[WP]['eleSel'])

if doLimits:
   selectedSamples = allOfficialSignals + backgrounds 
   
   limits={}
   
   setEventListToChains(samples, selectedSamples, allCuts['None']['presel'])

   allYields = Yields(samples, selectedSamples, allCuts[WP]['runI'], cutOpt="list2", weight="weight", pklOpt=False, tableName = "RunI", nDigits=2, err=True, verbose=True, nSpaces=10)
   JinjaTexTable(allYields, pdfDir = savedir1, texDir = savedir1 + "/tex/", caption="Cut Flow Table: RunI Reload Electrons (" + WP + " WP)", transpose=True)
   
   for sig in allOfficialSignals:
      mstop, mlsp = [int(x) for x in sig[1:].rsplit("_")]
      print makeLine()
      print "signal, mstop, mlsp: ", sig, " ", mstop, " ", mlsp
      print makeLine()
      
      try: limits[mstop]
      except KeyError: limits[mstop]={}
      
      limits[mstop][mlsp] = getLimit(allYields, sig=sig, outDir = savedir1 + "/cards" , postfix= "", calc_limit = True) 

      #pickle.dump(limits, open(savedir + "/cards/limits.pkl",'w'))
      exclCanv , exclPlot = drawExpectedLimit(limits, plotDir = savedir1 + "/ExpectedLimit_eleID_%s.png"%(WP), bins=None, key=None)
      #exclCanv.SetName("ExpectedLimit_eleID_%s.pkl"%(WP))

if doCutFlow:
   selectedSamples = officialSignals + backgrounds 
   setEventListToChains(samples, selectedSamples, allCuts['None']['presel'])
   fewSignalYields = Yields(samples, selectedSamples, allCuts[WP]['runI'], cutOpt="list2", weight="weight", pklOpt=False, tableName = "RunI", nDigits=2, err=True, verbose=True, nSpaces=10)
   JinjaTexTable(fewSignalYields, pdfDir = savedir2, texDir = savedir2 + "/tex/", caption="Cut Flow Table: RunI Reload Electrons (" + WP + " WP)", transpose=False)
