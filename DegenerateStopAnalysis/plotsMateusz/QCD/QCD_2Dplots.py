# 2Dplots.py
# Script to calculate the 2D distributions of QCD variables 
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
parser.add_argument("--channel", dest="channel",  help="Channel", type=str, default="electron")
parser.add_argument("--var1", dest="var1",  help="Variable 1", type=str, default="delPhi")
parser.add_argument("--var2", dest="var2",  help="Variable 2", type=str, default="hybIso")
#parser.add_argument("--slice", dest="slice",  help="Pt Slice Bounds (low,up)", type=int, nargs=2, metavar = ('slice_low', 'slice_up'))
parser.add_argument("--sample", dest="sample",  help="Sample", type=str, default="qcd")
parser.add_argument("--MET", dest = "MET",  help = "MET Cut", type = str, default = "200")
parser.add_argument("--HT", dest = "HT",  help = "HT Cut", type = str, default = "400")
#parser.add_argument("--eleWP", dest = "eleWP",  help = "Electron WP", type = str, default = "Veto")
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
channel = args.channel
var1 = args.var1
var2 = args.var2
#slice = args.slice
sample = args.sample 
METcut = args.MET
HTcut = args.HT
#eleWP = args.eleWP
btag = args.btag
getData = args.getData
plot = args.plot
logy = args.logy
save = args.save
verbose = args.verbose

print makeDoubleLine()
print "Plotting 2D distributions"
print makeDoubleLine()

#Samples
backgrounds = ["qcd"]#, "vv", "st", "dy", "z", "tt", "w"]
officialSignals = ["s300_290", "s300_270", "s300_240"] #FIXME: crosscheck if these are in allOfficialSignals

samplesList = backgrounds #+ officialSignals
if getData: samplesList.append("dblind")

cmgPP = cmgTuplesPostProcessed()
samples = getSamples(cmgPP = cmgPP, skim = 'preIncLep', sampleList = samplesList, scan = False, useHT = True, getData = getData)

if verbose:
   print makeLine()
   print "Using samples:"
   newLine()
   for s in samplesList:
      if s: print samples[s].name,":",s
      else:
         print "!!! Sample " + sample + " unavailable."
         sys.exit(0)

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/QCD/2Dplots/%s"%(tag, channel)

   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

#Geometric divisions
etaAcc = 2.5 #eta acceptance
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap

#bTagWeights
bWeightDict = bTagWeights(btag)
bTagString = bWeightDict['sr1_bjet'] #corresponds to bVeto
#bTagString = "nBJet == 0"
if channel == "electron":
   lepCondition = "nLepAll_el2 > 0"
elif channel == "muon":
   lepCondition = "nLepAll_mu2 > 0"

#Preselection & basic SR cuts
baseline = CutClass("baseline", [
   ["HT",         "ht_basJet >" + HTcut],
   ["MET",        "met >" + METcut],
   ["ISR100",     "nIsrJet >= 1"],
   ["No3rdJet60", "nVetoJet <= 2"],
   ["lepton",     lepCondition],
   #["BVeto",     bTagString],
   #["TauVeto",   "Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
   ], baseCut = None)

if channel == "electron":
   ind = "IndexLepAll_el[0]" #standard index sel 
   ind2 = "IndexLepAll_el2[0]" #index sel: Veto ID w/o sigmaEtaEta and w/o hybIso
elif channel == "muon":
   ind = "IndexLepAll_mu[0]" #standard index sel 
   ind2 = "IndexLepAll_mu2[0]" #index sel: no hybIso and IP cut

variables = {'delPhi':"vetoJet_dPhi_j1j2", 
             'hybIso':"(LepAll_relIso03[" + ind2 + "]*min(LepAll_pt[" + ind2 + "], 25))",
             'absDxy':"LepAll_dxy[" + ind2 + "]", 
             'absIso':"LepAll_absIso03[" + ind2 + "]", 
             'relIso':"LepAll_relIso03[" + ind2 + "]",
             'lepPt':"LepAll_pt[" + ind2 + "]", 
             'lepMt':"LepAll_mt[" + ind2 + "]"}

plotDict = {\
   "MET":{    'var':"met",                                             'bins':[100,0,500],   'decor':{'title':"MET Plot",             'x':"Missing E_{T} / GeV",             'y':"Events", 'log':[0,logy,0]}},
   "HT":{     'var':"ht_basJet",                                       'bins':[100,0,500],   'decor':{'title':"HT Plot",              'x':"H_{T} / GeV",                     'y':"Events", 'log':[0,logy,0]}},
   "delPhi":{ 'var':"vetoJet_dPhi_j1j2",                               'bins':[16, 0, 3.14], 'decor':{'title':"deltaPhi(j1,j2) Plot", 'x':"#Delta#phi(j1,j2)",               'y':"Events", 'log':[0,logy,0]}},
   "lepPt":{  'var':variables['lepPt'],                                'bins':[20, 0, 50],  'decor':{'title':"Lepton pT Plot" ,      'x':"Muon p_{T} / GeV",                'y':"Events", 'log':[0,logy,0]}},
   "lepMt":{  'var':variables['lepMt'],                                'bins':[20,0,100],   'decor':{'title':"Lepton mT Plot",       'x':"m_{T} / GeV",                     'y':"Events", 'log':[0,logy,0]}},
   "hybIso2":{'var':"(log(1 + " + variables['hybIso'] + ")/log(1+5))", 'bins':[16, 0, 4],    'decor':{'title':"Lepton hybIso Plot",   'x':"log(1+HI)/log(1+5)",              'y':"Events", 'log':[0,logy,0]}},
   "hybIso":{ 'var':variables['hybIso'],                               'bins':[20, 0, 25],  'decor':{'title':"Lepton hybIso Plot",   'x':"HI = I_{rel}*min(p_{T}, 25 GeV)", 'y':"Events", 'log':[0,logy,0]}},
   "absIso":{ 'var':variables['absIso'],                               'bins':[8, 0, 20],   'decor':{'title':"Lepton absIso Plot",   'x':"I_{abs} / GeV",                   'y':"Events", 'log':[0,logy,0]}},
   "relIso":{ 'var':variables['relIso'],                               'bins':[40, 0, 5],   'decor':{'title':"Lepton relIso Plot",   'x':"I_{rel}",                         'y':"Events", 'log':[0,logy,0]}},
   "absDxy":{ 'var':variables['absDxy'],                               'bins':[8, 0, 0.04], 'decor':{'title':"Lepton |dxy| Plot" ,   'x':"|dxy|",                           'y':"Events", 'log':[0,logy,0]}},
   "weight":{ 'var':"weight",                                          'bins':[40,0,400],   'decor':{'title':"Weight Plot",          'x':"Event Weight",                    'y':"Events", 'log':[0,1,0]}}
}

if channel == "electron":
   variables.update(
   {'hOverE':"LepAll_hadronicOverEm[" + ind2 + "]",
   'sigmaEtaEta':"LepAll_sigmaIEtaIEta[" + ind2 + "]"})

   plotDict.update(
      {"sigmaEtaEta":{'var':variables['sigmaEtaEta'], 'bins':[6,0,0.03], 'decor':{"title":"#sigma#eta#eta Plot", 'x':"#sigma#eta#eta", 'y':"Events", 'log':[0,logy,0]}},
      "hOverE":{      'var':variables['hOverE'],      'bins':[10,0,0.2], 'decor':{"title":"H/E Plot",            'x':"H/E" ,           'y':"Events", 'log':[0,logy,0]}}})

c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,2)

#2D Histograms (wrt. pT)
hist = make2DHist(samples[sample].tree, variables[var1], variables[var2], "weight*(%s)"%(baseline.combined), plotDict[var1]['bins'][0], plotDict[var1]['bins'][1], plotDict[var1]['bins'][2], plotDict[var2]['bins'][0], plotDict[var2]['bins'][1], plotDict[var2]['bins'][2])
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
   
#Save to Web
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   c1.SaveAs("%s/2D_%s_%s_%s.png"%(savedir, var1, var2, samples[sample].name))
   c1.SaveAs("%s/root/2D_%s_%s_%s.root"%(savedir, var1, var2, samples[sample].name))
   c1.SaveAs("%s/pdf/2D_%s_%s_%s.pdf"%(savedir, var1, var2, samples[sample].name))
