# matching.py 
# Plot of generator MC matching variables
# Mateusz Zarucki 2017

import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style, makeDir
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from collections import OrderedDict
from pprint import pprint
from array import array
from math import pi, sqrt #cos, sin, sinh, log
from fakeRegions import regions, binning

parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--lep", dest = "lep",  help = "Lepton", type = str, default = "el")
parser.add_argument("--WP",  dest = "WP",  help = "Working point", type = str, default = "loose")
parser.add_argument("--sample",  dest = "sample",  help = "Sample", type = str, default = "w")
parser.add_argument("--region", dest = "reg",  help = "Measurement or application region", type = str, default = "application_sr1")
parser.add_argument("--simulPlot", help = "Simultaneous plots (no stack)", action = "store_true")
parser.add_argument("--doStack", help = "doStack", action = "store_true")
parser.add_argument("--looseCR", help = "Calculate yields", action = "store_true")
parser.add_argument("--logy", action = "store_true",  help = "Log scale")
parser.add_argument("--save", dest="save",  help="Toggle save", type=int, default=1)
parser.add_argument("--verbose", dest="verbose",  help="Verbosity switch", type=int, default=1)
parser.add_argument("-b", dest="batch",  help="Batch mode", action="store_true", default=False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
lep = args.lep
WP = args.WP
sample = args.sample
reg = args.reg
simulPlot = args.simulPlot
doStack = args.doStack
looseCR = args.looseCR
logy = args.logy
save = args.save
verbose = args.verbose

if not simulPlot: doStack = False

ROOT.gStyle.SetOptStat(0)

#Samples
cmgPP = cmgTuplesPostProcessed()

if "measurement" in reg:
   skim = "oneLepGood"
   samplesList = ["w", "tt", "qcd"]
elif "application" in reg:
   skim = "preIncLep"
   samplesList = ["st", "vv", "qcd", "z", "dy", "tt", "w"]
   getData = False #NOTE: For now, do not plot data near SR
else:
   print "Region unknown. Exiting."
   sys.exit()

if getData and "measurement" in reg:
   samplesList.append("djetBlind")

samples = getSamples(cmgPP = cmgPP, skim = skim, sampleList = samplesList, scan = False, useHT = True, getData = getData)

print makeLine()
print "Using samples:"
newLine()
for s in samplesList:
   if s: print samples[s].name,":",s
   else:
      print "!!! Sample " + sample + " unavailable."
      sys.exit()

if lep == "el":    lepton = "Electron" #pdgId = "11"
elif lep == "mu":  lepton = "Muon" #pdgId = "13"
elif lep == "lep": lepton = "Lepton"
      
#Save
if save:
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/fakesEstimation/matching"%tag
   
   savedir += "/" + sample
   
   if looseCR: savedir += "/looseCR"
   
   if logy: savedir += "/log"
   
   makeDir(savedir)
   
   suffix = ""
   
selection = regions(reg, lep)
#setEventListToChains(samples, samplesList, selection[reg])

print makeLine()
print "Using the following selection: \n",
pprint(selection)
print "\n",
print reg, "= \n",
pprint(selection[reg].fullList)
print makeLine()

index = selection['index']

#variables = {\
#   'pt':"LepGood_pt[%s]"%index[WP],
#   'eta':"abs(LepGood_eta[%s])"%index[WP],
#   'mt':"LepGood_mt[%s]"%index[WP],
#   'absIso':"LepGood_absIso03[%s]"%index[WP],
#   'relIso':"LepGood_relIso03[%s]"%index[WP],
#   'hybIso':"(LepGood_relIso03[{ind}]*min(LepGood_pt[{ind}], 25))".format(ind = index[WP]),
#}
#   
#variables['hybIso2'] = "(log(1 + " + variables['hybIso'] + ")/log(1+5))"

region = {}

region['total'] = CutClass(reg, [
   ["WP", selection[WP]],
   ], baseCut = selection[reg])

region['prompt'] = CutClass(reg + "_prompt", [
   ["prompt", selection['promptLoose']],
   ["WP", selection[WP]],
   ], baseCut = selection[reg])

region['fakes'] = CutClass(reg + "_fakes", [
   ["fake", selection['fakeLoose']],
   ["WP", selection[WP]],
   ], baseCut = selection[reg])

##Sets TDR style
#setup_style()

sel = {'mcMatchId':{}, 'mcMatchAny':{}}
sel['mcMatchId']['0'] =   "(LepGood_mcMatchId[{ind}] == 0)".format(ind = index[WP])
sel['mcMatchId']['24'] =  "(abs(LepGood_mcMatchId[{ind}]) == 24)".format(ind = index[WP])
sel['mcMatchId']['99'] =  "(LepGood_mcMatchId[{ind}] == 99)".format(ind = index[WP])
sel['mcMatchId']['100'] = "(LepGood_mcMatchId[{ind}] == 100)".format(ind = index[WP])
#sel['mcMatchId']['fake'] =    "(LepGood_mcMatchId[{ind}] == 0 || LepGood_mcMatchId[{ind}] == 99 || LepGood_mcMatchId[{ind}] == 100)".format(ind = index[WP])
#sel['mcMatchId']['prompt'] =  "(LepGood_mcMatchId[{ind}] != 0 && LepGood_mcMatchId[{ind}] != 99 && LepGood_mcMatchId[{ind}] != 99)".format(ind = index[WP])

sel['mcMatchAny']['0'] =       "(LepGood_mcMatchAny[{ind}] == 0)".format(ind = index[WP])
sel['mcMatchAny']['1'] =       "(LepGood_mcMatchAny[{ind}] == 1)".format(ind = index[WP])
sel['mcMatchAny']['4'] =       "(LepGood_mcMatchAny[{ind}] == 4)".format(ind = index[WP])
sel['mcMatchAny']['5'] =       "(LepGood_mcMatchAny[{ind}] == 5)".format(ind = index[WP])
#sel['mcMatchAny']['fake'] =    "(LepGood_mcMatchAny[{ind}] == 0 || LepGood_mcMatchAny[{ind}] == 4 || LepGood_mcMatchAny[{ind}] == 5)".format(ind = index[WP])

if looseCR:
   for x in ['mcMatchId', 'mcMatchAny']:
      for y in sel[x]:
         sel[x][y] += "&& (" + region['total'].combined + ")"

canvs = {}
stacks = {}
legs = {}
hists = {'mcMatchId':OrderedDict(), 'mcMatchAny':OrderedDict()}
   
for x in ['mcMatchId', 'mcMatchAny']:
   canvs[x] = ROOT.TCanvas("c_" + x, "Canvas " + x, 1200, 1200)
   legs[x] = makeLegend2(y1 = 0.65, y2 = 0.85)
   stacks[x] = ROOT.THStack("stack_" + x,"stack_" + x)

   if x == 'mcMatchId': 
      y = 'mcMatchAny'
      bins = [140, -30, 110]
   elif x == 'mcMatchAny': 
      y = 'mcMatchId'
      bins = [14, -4, 10]

   hists[x]['noSel'] =        makeHist(samples[sample].tree, "LepGood_%s[%s]"%(x,index[WP]), "",               bins[0], bins[1], bins[2])
   #hists[x][y + '_fake'] =    makeHist(samples[sample].tree, "LepGood_%s[%s]"%(x,index[WP]), sel[y]['fake'],   bins[0], bins[1], bins[2])
   if x == 'mcMatchAny': 
      hists[x][y + '_100'] = makeHist(samples[sample].tree, "LepGood_%s[%s]"%(x,index[WP]), sel[y]['100'], bins[0], bins[1], bins[2])
      hists[x][y + '_99'] =  makeHist(samples[sample].tree, "LepGood_%s[%s]"%(x,index[WP]), sel[y]['99'],  bins[0], bins[1], bins[2])
      hists[x][y + '_24'] =  makeHist(samples[sample].tree, "LepGood_%s[%s]"%(x,index[WP]), sel[y]['24'],  bins[0], bins[1], bins[2])
   if x == 'mcMatchId': 
      hists[x][y + '_4'] =  makeHist(samples[sample].tree, "LepGood_%s[%s]"%(x,index[WP]), sel[y]['4'], bins[0], bins[1], bins[2])
      hists[x][y + '_5'] =  makeHist(samples[sample].tree, "LepGood_%s[%s]"%(x,index[WP]), sel[y]['5'], bins[0], bins[1], bins[2])
      hists[x][y + '_1'] =  makeHist(samples[sample].tree, "LepGood_%s[%s]"%(x,index[WP]), sel[y]['1'], bins[0], bins[1], bins[2])
      #hists[x][y + '_prompt'] =  makeHist(samples[sample].tree, "LepGood_%s[%s]"%(x,index[WP]), sel[y]['prompt'], bins[0], bins[1], bins[2])
   
   hists[x][y + '_0'] =       makeHist(samples[sample].tree, "LepGood_%s[%s]"%(x,index[WP]), sel[y]['0'],      bins[0], bins[1], bins[2])

for canv in canvs:
   canvs[canv].cd()
   if logy: canvs[canv].SetLogy()
   for i, name in enumerate(hists[canv]):
      if canv in name: continue

      hists[canv][name].SetName(canv + "_" + name)
      
      if not canvs[canv].GetLogy(): 
         hists[canv][name].SetMinimum(0)
         stacks[canv].SetMinimum(0)
      if sample == 'w':   
         if canv == 'mcMatchId':    
            if looseCR: stacks[canv].SetMaximum(50000)
            else: stacks[canv].SetMaximum(450000)
         elif canv == 'mcMatchAny': 
            if looseCR: stacks[canv].SetMaximum(70000)
            else: stacks[canv].SetMaximum(600000)
         else: 
            hists[canv][name].SetMinimum(1)
            hists[canv][name].SetMaximum(1000000)
            stacks[canv].SetMinimum(1)
            stacks[canv].SetMaximum(1000000)
      elif sample == 'qcd':   
         if canv == 'mcMatchId':    
            if looseCR: stacks[canv].SetMaximum(500)
            else: stacks[canv].SetMaximum(45000)
         elif canv == 'mcMatchAny': 
            if looseCR: stacks[canv].SetMaximum(700)
            else: stacks[canv].SetMaximum(60000)
         else: 
            hists[canv][name].SetMinimum(1)
            hists[canv][name].SetMaximum(10000)
            stacks[canv].SetMinimum(1)
            stacks[canv].SetMaximum(10000)
      
      hists[canv][name].SetLineWidth(2)
      hists[canv][name].SetFillColor(0)
      #hists[canv][name].SetLineColor(2+i)
         
      if not simulPlot: hists[canv][name].SetLineStyle(1)
      
      if "noSel" in name: 
         if simulPlot: hists[canv][name].SetFillColor(19)
         else:             hists[canv][name].SetFillColor(ROOT.kBlue-10)
         hists[canv][name].SetLineColor(1)
         hists[canv][name].SetLineWidth(0)
      if not simulPlot: 
         hists[canv]['noSel'].Draw("hist")
      
      if "prompt" in name:
         hists[canv][name].SetLineColor(ROOT.kBlue+1)
         if doStack: hists[canv][name].SetFillColor(ROOT.kBlue+1)
         #hists[canv][name].SetLineStyle(2)
      elif "fake" in name:
         hists[canv][name].SetLineColor(ROOT.kRed+1)
         if doStack: hists[canv][name].SetFillColor(ROOT.kRed+1)
         #hists[canv][name].SetLineStyle(2)
      elif not "100" in name and "0" in name:
         hists[canv][name].SetLineColor(ROOT.kGreen+1)
         if doStack: hists[canv][name].SetFillColor(ROOT.kGreen+1)
         #hists[canv][name].SetLineStyle(2)
      elif "1" in name:
         hists[canv][name].SetLineColor(ROOT.kViolet+1)
         if doStack: hists[canv][name].SetFillColor(ROOT.kViolet+1)
         #hists[canv][name].SetLineStyle(2)
      elif "4" in name:
         hists[canv][name].SetLineColor(ROOT.kOrange+1)
         if doStack: hists[canv][name].SetFillColor(ROOT.kOrange+1)
         #hists[canv][name].SetLineStyle(2)
      elif "99" or "5" in name:
         hists[canv][name].SetLineColor(ROOT.kCyan)
         if doStack: hists[canv][name].SetFillColor(ROOT.kCyan+1)
         #hists[canv][name].SetLineStyle(2)

      if not simulPlot: legs[canv].Clear()
      if "noSel" in name and not doStack: legs[canv].AddEntry(hists[canv][name], "No selection", "F")
      else:               
         legs[canv].AddEntry(hists[canv][name], hists[canv][name].GetName().replace(canv+'_', '').replace('_','='), "LP")
      
      if doStack and not "noSel" in name: stacks[canv].Add(hists[canv][name])
      else: hists[canv][name].Draw("histsame")

      if not simulPlot and not "noSel" in name: 
         legs[canv].Draw()
         canvs[canv].Modified()
         canvs[canv].Update()
         suffix = "_" + hists[canv][name].GetName()
         if save: canvs[canv].SaveAs("%s/matching%s.png"%(savedir, suffix))

   if simulPlot:
      if doStack: 
         stacks[canv].Draw('hist')
         suffix = "_stacked"
      legs[canv].Draw()

      canvs[canv].Modified()
      canvs[canv].Update()
  
      if save: canvs[canv].SaveAs("%s/matching_%s_simul%s.png"%(savedir, canv, suffix))
