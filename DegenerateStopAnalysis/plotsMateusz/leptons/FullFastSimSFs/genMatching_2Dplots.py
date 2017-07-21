# 2Dplots.py
# Script for making 2D plots for gen-matching variables 
# Mateusz Zarucki 2016

import ROOT
import os, sys
import argparse
import pickle
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.eleWPs import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.regions import signalRegions
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, makeDir, setup_style
from Workspace.DegenerateStopAnalysis.tools.bTagWeights import bTagWeights
from Workspace.DegenerateStopAnalysis.tools.getSamples_8012 import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Sets TDR style
#setup_style()

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--sample", dest="sample",  help="Sample", type=str, default="tt")
parser.add_argument("--MET", dest = "MET",  help = "MET Cut", type = str, default = "200")
parser.add_argument("--HT", dest = "HT",  help = "HT Cut", type = str, default = "400")
parser.add_argument("--btag", dest = "btag",  help = "B-tagging option", type = str, default = "sf")
parser.add_argument("--getData", dest = "getData",  help = "Get data samples", type = int, default = 0)
parser.add_argument("--plot", dest = "plot",  help = "Toggle plot", type = int, default = 0)
parser.add_argument("--logy", dest = "logy",  help = "Toggle logy", type = int, default = 1)
parser.add_argument("--save", dest="save",  help="Toggle Save", type=int, default=1)
parser.add_argument("--verbose", dest = "verbose",  help = "Verbosity switch", type = int, default = 0)
parser.add_argument("-b", dest="batch",  help="Batch Mode", action="store_true", default=False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
sample = args.sample 
METcut = args.MET
HTcut = args.HT
btag = args.btag
getData = args.getData
plot = args.plot
logy = args.logy
save = args.save
verbose = args.verbose

print makeDoubleLine()
print "Plotting 2D distributions"
print makeDoubleLine()

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/leptonSFs/2Dplots"%tag
   
   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

#Samples
backgrounds = ["tt"]#, "vv", "st", "dy", "z", "tt", "w"]
#privateSignals = ["s10FS", "s30", "s30FS", "s60FS", "t2tt30FS"]
officialSignals = ["s300_290", "s300_270", "s300_240"] #FIXME: crosscheck if these are in allOfficialSignals

samplesList = backgrounds #+ officialSignals

if getData: samplesList.append("dblind")

cmgPP = cmgTuplesPostProcessed()
samples = getSamples(cmgPP = cmgPP, skim = 'preIncLep', sampleList = samplesList, scan = False, useHT = True, getData = getData)

#allOfficialSignals = samples.massScanList()
##allOfficialSignals = [s for s in samples if samples[s]['isSignal'] and not samples[s]['isData'] and s not in privateSignals and s not in backgrounds] 
#allSignals = privateSignals + allOfficialSignals
#allSamples = allSignals + backgrounds

if verbose:
   print makeLine()
   print "Using samples:"
   newLine()
   for s in samplesList:
      if s: print samples[s].name,":",s
      else:
         print "!!! Sample " + sample + " unavailable."
         sys.exit(0)

#Geometric divisions
etaAcc = 2.5 #eta acceptance
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap

#bTagWeights
bWeightDict = bTagWeights(btag)
bTagString = bWeightDict['sr1_bjet'] #corresponds to bVeto
#bTagString = "nBJet == 0"

#Preselection & basic SR cuts
baseline = CutClass("baseline", [
   ["HT",         "ht_basJet >" + HTcut],
   ["MET",        "met >" + METcut],
   ["ISR100",     "nIsrJet >= 1"],
   #["No3rdJet60", "nVetoJet <= 2"],
   #["lepton",     lepCondition],
   #["BVeto",     bTagString],
   #["TauVeto",   "Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
   ], baseCut = None)

c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,2)

genColl = "GenPart" #GenPart, genLep, genTau, genLepFromTau (genPartAll)
var1 = "LepAll_mcMatchId"
#var1 = "n%s"%genColl
var2 = "%s_sourceId"%genColl

sel = "1"
#sel = baseline.combined 

#2D Histograms (wrt. pT)
#hist = make2DHist(samples[sample].tree, var1, var2, "weight*(%s)"%(sel), 20, -10, 10, 20, -10, 10)
hist = make2DHist(samples[sample].tree, var1, var2, "weight*(%s)"%(sel), 120, -10, 110, 120, -10, 110)
hist.SetName("2D_" + var1 + "_" + var2)
hist.SetTitle(var1 + " vs " + var2 + " Distribution")
hist.GetXaxis().SetTitle(var1)
hist.GetYaxis().SetTitle(var2)
hist.Draw("COLZ") #CONT1-5 #plots the graph with axes and points
#hist.GetZaxis().SetRangeUser(0, 4)
if logy: ROOT.gPad.SetLogz() 
#alignStats(hist)
   
c1.Modified()
c1.Update()
   
#Write to file
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID

   #Save to Web
   c1.SaveAs("%s/2D_%s_vs_%s_%s.png"%(savedir, var1, var2, samples[sample].name))
   c1.SaveAs("%s/root/2D_%s_vs_%s_%s.root"%(savedir, var1, var2, samples[sample].name))
   c1.SaveAs("%s/pdf/2D_%s_vs_%s_%s.pdf"%(savedir, var1, var2, samples[sample].name))
