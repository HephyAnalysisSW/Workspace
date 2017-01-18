# fakeRate.py
# Determination of the fake rate (tight-to-loose ratio)
# Mateusz Zarucki 2017

import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style, makeDir
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples, lumis
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from pprint import pprint
from array import array
from math import pi, sqrt #cos, sin, sinh, log
from fakeRegions import regions, binning

#ROOT.gStyle.SetOptStat(1111) #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis
ROOT.gStyle.SetOptStat(0)

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--lep", dest = "lep",  help = "Lepton", type = str, default = "lep")
parser.add_argument("--region", dest = "region",  help = "Measurement or application region", type = str, default = "measurement")
parser.add_argument("--getData", dest = "getData",  help = "Get data", action = "store_true")
parser.add_argument("--sample", dest = "sample",  help = "Sample", type = str, default = "qcd")
parser.add_argument("--subtractEWK", dest = "subtractEWK",  help = "Subtract EWK MC from Data", action = "store_true")
parser.add_argument("--varBins", dest = "varBins",  help = "Variable bin size", action = "store_true")
parser.add_argument("--do2D", dest = "do2D",  help = "2D fake rate", action = "store_true")
parser.add_argument("--logy", dest = "logy",  help = "Toggle logy", type = int, default = 1)
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
region = args.region
getData = args.getData
sample = args.sample
subtractEWK = args.subtractEWK
varBins = args.varBins
do2D = args.do2D
logy = args.logy
save = args.save
verbose = args.verbose

#Samples
cmgPP = cmgTuplesPostProcessed()

if not (subtractEWK or getData):
   samplesList = [sample]
elif subtractEWK:
   getData = True
   sample = 'djetBlind'
   samplesList = ["w", "tt", "qcd"]
else:
   samplesList = []

if "application" in region: getData = False #NOTE: Just in case, no data near SR

if getData and "measurement" in region:   
   samplesList.append('djetBlind')

if "measurement" in region:
   skim = "oneLepGood"
elif "application" in region:
   skim = "preIncLep"
else:
   print "Region unknown. Exiting."
   sys.exit() 

samples = getSamples(cmgPP = cmgPP, skim = skim, sampleList = samplesList, scan = False, useHT = True, getData = getData)

if verbose:
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
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/fakesEstimation"%tag

   savedir += "/%s/fakeRate/%s"%(region, lepton)

   if not varBins: savedir += "/fixedBins"
   else:           savedir += "/varBins"
   
   if subtractEWK: suffix = "_%s_data-EWK"%lep
   else: suffix = "_%s_%s"%(lep, sample)

   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")
  
   if "measurement" in region: 
      resultsDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate"
   
      resultsDir1 = resultsDir + "/FR_data-EWK"
      resultsDir2 = resultsDir + "/FR_MC"
      
      if not varBins: 
         resultsDir1 += "/fixedBins"
         resultsDir2 += "/fixedBins"
      else:
         resultsDir1 += "/varBins"
         resultsDir2 += "/varBins"

      makeDir(resultsDir1)
      makeDir(resultsDir2)

#Weights
mcLum = samples[samples.keys()[0]].weights.weight_dict['lumis']['mc_lumi'] #10.0 #fb-1
tarLum = lumis['DataBlind_lumi'] #samples['djetBlind'].lumi #target lumi = data lumi
lumiWeight = tarLum/mcLum

baseWeight = samples[samples.keys()[0]].weights.weight_dict['baseWeight']
puWeight = samples[samples.keys()[0]].weights.weight_dict['pu']

weights = [baseWeight, puWeight, lumiWeight]
weight = "*".join("(%s)"%w for w in weights)

#NOTE: Fake rate should be the same indepdendent of the weight! (At least the central value)

selection = regions(region, lep)
setEventListToChains(samples, samplesList, selection[region])

if verbose:
   print makeLine()
   print "Using the following selection: \n",
   pprint(selection)
   print "\n",
   print region, "= \n",
   pprint(selection[region].fullList)
   print makeLine()

index = selection['index']

pt = "LepGood_pt[%s]"%index['loose']
eta = "abs(LepGood_eta[%s])"%index['loose']
mt = "LepGood_mt[%s]"%index['loose']

bins = binning(lep, varBins = varBins)
 
#normFactor = {}
#normFactor['pt'] =  "((nLepGood_{lep}_loose > 0)*(({var} < 5) + ({var} >= 5 && {var} < 12)*0.714 + ({var} >= 12 && {var} < 20)*0.625 + ({var} >= 20 && {var} < 30)*0.5 + ({var} >= 30 && {var} < 200)*0.0294))".format(lep = lep, var = pt)
#normFactor['eta'] = "((nLepGood_{lep}_loose > 0)*(({var} < 0.9)*0.111 + ({var} >= 0.9 && {var} < 1.2)*0.333 + ({var} >= 1.2 && {var} < 2.1)*0.111 + ({var} >= 2.1 && {var} < 2.4)*0.333))".format(lep = lep, var = eta)

#bins = {'pt': array('d', range(0,30,5) + range(30,60,10) + range(60,100,20) + range(100,200+50,50))} #old binning
#normFactor = {'pt': "(({var} < 30) + ({var} >= 30 && {var} < 60)*0.5 + ({var} >= 60 && {var} < 100)*0.25 + ({var} >= 100 && {var} < 200)*0.1)".format(var = pt)} #old binning

#"binningIsExplicit":varBins, "variableBinning":(varBins, bins['pt'][1]-bins['pt'][0])

##################################################################################################################################################################################

# Creation of histograms

hists = {'loose':{'pt':{}, 'eta':{}, '2D':{}}, 'tight':{'pt':{}, 'eta':{}, '2D':{}}}
ratios = {'pt':{}, 'eta':{}, '2D':{}}
selList = {}

for samp in samplesList:
   # Selection and weights 
   if not samples[samp].isData:
      finalWeight = weight
   else:
      finalWeight = "1"
 
   #loose definition
   selList['loose'] = [selection['filters'], selection[region].combined, selection['loose']] 
   
   if samples[samp].isData:
      selList['loose'].append(selection['trigger'])
   elif not subtractEWK:
      selList['loose'].append(selection['fakeLoose'])
   
   #tight definition
   selList['tight'] = selList['loose'][:]
   selList['tight'].extend([selection['tight'], selection['match']]) 
  
   if not (samples[sample].isData or subtractEWK):
      selList['tight'].append(selection['fakeTight'])

   # Histograms
   if not varBins:
      hists['loose']['pt'][samp] = makeHist(samples[samp].tree, pt,          finalWeight + "*(" + combineCutsList(selList['loose']) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2])
      hists['tight']['pt'][samp] = makeHist(samples[samp].tree, pt,          finalWeight + "*(" + combineCutsList(selList['tight']) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2])
      hists['loose']['eta'][samp] = makeHist(samples[samp].tree, eta,        finalWeight + "*(" + combineCutsList(selList['loose']) + ")", bins['eta'][0], bins['eta'][1], bins['eta'][2])
      hists['tight']['eta'][samp] = makeHist(samples[samp].tree, eta,        finalWeight + "*(" + combineCutsList(selList['tight']) + ")", bins['eta'][0], bins['eta'][1], bins['eta'][2])
        
      if do2D:
         hists['loose']['2D'][samp] = make2DHist(samples[sample].tree, pt, eta, finalWeight + "*(" + combineCutsList(selList['loose']) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2], bins['eta'][0], bins['eta'][1], bins['eta'][2])
         hists['tight']['2D'][samp] = make2DHist(samples[sample].tree, pt, eta, finalWeight + "*(" + combineCutsList(selList['tight']) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2], bins['eta'][0], bins['eta'][1], bins['eta'][2])
   else: 
      hists['loose']['pt'][samp] = makeHistVarBins(samples[samp].tree, pt,   finalWeight + "*(" + combineCutsList(selList['loose']) + ")", bins['pt'],  variableBinning = (varBins, bins['pt'][1]-bins['pt'][0]))
      hists['tight']['pt'][samp] = makeHistVarBins(samples[samp].tree, pt,   finalWeight + "*(" + combineCutsList(selList['tight']) + ")", bins['pt'],  variableBinning = (varBins, bins['pt'][1]-bins['pt'][0]))
      hists['loose']['eta'][samp] = makeHistVarBins(samples[samp].tree, eta, finalWeight + "*(" + combineCutsList(selList['loose']) + ")", bins['eta'], variableBinning = (varBins, bins['eta'][1]-bins['eta'][0]))
      hists['tight']['eta'][samp] = makeHistVarBins(samples[samp].tree, eta, finalWeight + "*(" + combineCutsList(selList['tight']) + ")", bins['eta'], variableBinning = (varBins, bins['eta'][1]-bins['eta'][0]))
     
      if do2D: 
         hists['loose']['2D'][samp] = make2DHistVarBins(samples[samp].tree, pt, eta, finalWeight + "*" + normFactor['pt']  + "*" + normFactor['eta'] + "*(" + combineCutsList(selList['loose']) + ")", bins['pt'], bins['eta'])
         hists['tight']['2D'][samp] = make2DHistVarBins(samples[samp].tree, pt, eta, finalWeight + "*" + normFactor['pt']  + "*" + normFactor['eta'] + "*(" + combineCutsList(selList['tight']) + ")", bins['pt'], bins['eta'])
   
      #hists['loose']['pt'][samp].GetYaxis().SetTitle("Events / 5 GeV")
      #hists['loose']['eta'][samp].GetYaxis().SetTitle("Events / 0.1 rad")

   hists['loose']['pt'][samp].SetName("loose_%s_pt"%samp)
   hists['tight']['pt'][samp].SetName("tight_%s_pt"%samp)
   hists['loose']['eta'][samp].SetName("loose_%s_eta"%samp)
   hists['tight']['eta'][samp].SetName("tight_%s_eta"%samp)
  
   if do2D:
      hists['loose']['2D'][samp].SetName("loose_%s_2D"%samp)
      hists['tight']['2D'][samp].SetName("tight_%s_2D"%samp)

if subtractEWK:
   plots = ['pt', 'eta']
   if do2D: plots.append('2D')

   for x in plots: 
      hists['loose'][x]['data-EWK'] = hists['loose'][x]['djetBlind'].Clone()
      hists['tight'][x]['data-EWK'] = hists['tight'][x]['djetBlind'].Clone()
      hists['loose'][x]['data-EWK'].SetName("loose_data-EWK_%s"%x)
      hists['tight'][x]['data-EWK'].SetName("tight_data-EWK_%s"%x)
 
      for samp in samplesList:
         if samp != 'djetBlind' and samp != 'qcd':
            hists['loose'][x]['data-EWK'].Add(hists['loose'][x][samp], -1) 
            hists['tight'][x]['data-EWK'].Add(hists['tight'][x][samp], -1) 
  
   sample = 'data-EWK'

   hists['loose']['pt'][sample].SetTitle("%ss: Loose vs Tight comparison for Data Sample (EWK Subtracted)"%lepton)
   hists['loose']['eta'][sample].SetTitle("%ss: Loose vs Tight comparison for Data Sample (EWK Subtracted)"%lepton)
   
   if do2D: 
      hists['loose']['2D'][sample].SetTitle("%ss: Loose p_{T} vs |#eta| Distribution in Data Sample (EWK Subtracted)"%lepton)
      hists['tight']['2D'][sample].SetTitle("%ss: Tight p_{T} vs |#eta| Distribution in Data Sample (EWK Subtracted)"%lepton)
else:
   hists['loose']['pt'][sample].SetTitle("%ss: Loose vs Tight comparison for %s Sample"%(lepton, samples[samp].name))
   hists['loose']['eta'][sample].SetTitle("%ss: Loose vs Tight comparison for %s Sample"%(lepton, samples[samp].name))
   
   if do2D: 
      hists['loose']['2D'][sample].SetTitle("%ss: Loose p_{T} vs |#eta| Distribution in %s Sample"%(lepton, samples[samp].name))
      hists['tight']['2D'][sample].SetTitle("%ss: Tight p_{T} vs |#eta| Distribution in %s Sample"%(lepton, samples[samp].name))

# Efficiency plots
ratios['pt'][sample] = divideHists(hists['tight']['pt'][sample], hists['loose']['pt'][sample])
ratios['eta'][sample] = divideHists(hists['tight']['eta'][sample], hists['loose']['eta'][sample])
ratios['pt'][sample].SetName("ratio_%s_pt"%sample)
ratios['eta'][sample].SetName("ratio_%s_eta"%sample)

if do2D:
   ratios['2D'][sample] = divideHists(hists['tight']['2D'][sample], hists['loose']['2D'][sample])
   ratios['2D'][sample].SetName("ratios_%s_2D"%sample)

if subtractEWK:
   ratios['pt'][sample].SetTitle("%ss: Tight to Loose Ratio for Data Sample (EWK Subtracted) ; %s p_{T} / GeV ; Ratio"%(lepton, lepton))
   ratios['eta'][sample].SetTitle("%ss: Tight to Loose Ratio for Data Sample (EWK Subtracted) ; %s |#eta| ; Ratio"%(lepton, lepton))
   if do2D: ratios['2D'][sample].SetTitle("{lep}s: Tight to Loose Ratio for Data Sample (EWK Subtracted) ; {lep} p_{{T}}; {lep} |#eta|".format(lep = lepton))
else:
   ratios['pt'][sample].SetTitle("%ss: Tight to Loose Ratio for %s Sample ; %s p_{T} / GeV ; Ratio"%(lepton, samples[sample].name, lepton))
   ratios['eta'][sample].SetTitle("%ss: Tight to Loose Ratio for %s Sample ; %s |#eta| ; Ratio"%(lepton, samples[sample].name, lepton))
   if do2D: ratios['2D'][sample].SetTitle("{lep}s: Tight to Loose Ratio for {} Sample ; {lep} p_{{T}}; {lep} |#eta|".format(samples[sample].name, lep = lepton))

###############################################################################################################################################################################

#####Canvas 1#####

c1 = ROOT.TCanvas("c1", "Canvas 1", 1200, 1700)
c1.Divide(1,2)

c1.cd(1)
   
hists['loose']['pt'][sample].GetXaxis().SetTitle("%s p_{T} / GeV"%lepton)
hists['loose']['pt'][sample].SetFillColor(ROOT.kViolet+10)
#hists['loose']['pt'][sample].SetMinimum(1)
#hists['loose']['pt'][sample].SetMaximum(1000)
hists['loose']['pt'][sample].Draw("hist")

#alignStats(hists['loose']['pt'][sample])

hists['tight']['pt'][sample].SetFillColor(ROOT.kRed+1)
hists['tight']['pt'][sample].SetFillColorAlpha(hists['tight']['pt'][sample].GetFillColor(), 0.8)
hists['tight']['pt'][sample].Draw("histsame")
 
if logy: ROOT.gPad.SetLogy()

ROOT.gPad.Modified()
ROOT.gPad.Update()

l1 = makeLegend2()
l1 = ROOT.TLegend()
l1.AddEntry("loose_%s_pt"%sample, "Loose", "F")
l1.AddEntry("tight_%s_pt"%sample, "Tight", "F")
l1.Draw()

alignLegend(l1, y1=0.5, y2=0.65)

#####

# Efficiency

c1.cd(2)

ratios['pt'][sample].Draw("P")

#setupEffPlot(ratios['pt'][sample])
ratios['pt'][sample].SetMinimum(0)
ratios['pt'][sample].SetMaximum(1.0)

#ratios['pt'][sample].GetPaintedGraph().SetMinimum(0)
#ratios['pt'][sample].GetPaintedGraph().SetMaximum(0.6)
#ratios['pt'][sample].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)

#Colours
ratios['pt'][sample].SetMarkerColor(ROOT.kGreen+3)

ROOT.gPad.Modified()
ROOT.gPad.Update()

#l2 = makeLegend2()
#l2.AddEntry("ratio_%s_pt"%sample, "Veto", "P")
#l2.Draw()

c1.Modified()
c1.Update()

#####Canvas 2######

c2 = ROOT.TCanvas("c2", "Canvas 2", 1200, 1700)
c2.Divide(1,2)

c2.cd(1)

hists['loose']['eta'][sample].GetXaxis().SetTitle("%s |#eta| "%(lepton))
hists['loose']['eta'][sample].SetFillColor(ROOT.kViolet+10)
#hists['loose']['eta'][sample].SetMinimum(1)
#hists['loose']['eta'][sample].SetMaximum(1000)
hists['loose']['eta'][sample].Draw("hist")

#alignStats(hists['loose']['eta'][sample])#, y1=0.4, y2=0.6)

hists['tight']['eta'][sample].SetFillColor(ROOT.kRed+1)
hists['tight']['eta'][sample].SetFillColorAlpha(hists['tight']['eta'][sample].GetFillColor(), 0.8)
hists['tight']['eta'][sample].Draw("histsame")
   
if logy: ROOT.gPad.SetLogy()

ROOT.gPad.Modified()
ROOT.gPad.Update()

l2 = ROOT.TLegend()
l2.AddEntry("loose_%s_eta"%sample, "Loose", "F")
l2.AddEntry("tight_%s_eta"%sample, "Tight", "F")
l2.Draw()

alignLegend(l2, y1=0.5, y2=0.65)

#####

c2.cd(2)

ratios['eta'][sample].Draw("P")

ratios['eta'][sample].SetMinimum(0)
ratios['eta'][sample].SetMaximum(0.6)

#setupEffPlot(ratios['eta'][sample])
#ratios['eta'][sample].GetPaintedGraph().SetMinimum(0)
#ratios['eta'][sample].GetPaintedGraph().SetMaximum(0.6)
#ratios['eta'][sample].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)

#Colours
ratios['eta'][sample].SetMarkerColor(ROOT.kGreen+3)

ROOT.gPad.Modified()
ROOT.gPad.Update()

#l3 = makeLegend2()
#l3.AddEntry("ratio_%s_eta"%sample, "Veto", "P")
#l3.Draw()

c2.Modified()
c2.Update()

if do2D:
   hists['loose']['2D'][sample].GetXaxis().SetTitle("%s p_{T}"%lepton)
   hists['loose']['2D'][sample].GetYaxis().SetTitle("%s |#eta|"%lepton)
   #hists['loose']['2D'][sample].GetZaxis().SetRangeUser(0, 4)
   #alignStats(hists['loose']['2D'][sample])
   
   hists['tight']['2D'][sample].GetXaxis().SetTitle("%s p_{T}"%lepton)
   hists['tight']['2D'][sample].GetYaxis().SetTitle("%s |#eta|"%lepton)
   
   ratios['2D'][sample].SetMarkerSize(0.8)
   
   #####Canvas 3#####
   
   c3 = ROOT.TCanvas("c3", "Canvas 3", 1800, 1500)
   ratios['2D'][sample].Draw("COLZ TEXTE89") #CONT1-5 #plots the graph with axes and points
   #ratios['2D'][sample].GetPaintedGraph().GetXaxis().SetTitle("%s p_{T}"%lepton)
   #ratios['2D'][sample].GetPaintedGraph().GetYaxis().SetTitle("%s |#eta|"%lepton)
   #ratios['2D'][sample].SetMinimum(0.8)
   #ratios['2D'][sample].SetMaximum(5)
   #ratios['2D'][sample].GetZaxis().SetRangeUser(0.8,1.2)
   
   #alignStats(ratios['2D'][sample])
   
   #if logy: ROOT.gPad.SetLogz()
   c3.Modified()
   c3.Update()
   
   #####Canvas 4#####
   
   c4 = ROOT.TCanvas("c4", "Canvas 4", 1800, 1500)
   c4.Divide(1,2)
   
   c4.cd(1)
   hists['tight']['2D'][sample].Draw("COLZ") #CONT1-5 #plots the graph with axes and points
   if logy: ROOT.gPad.SetLogz()
   
   c4.cd(2)
   hists['loose']['2D'][sample].Draw("COLZ") #CONT1-5 #plots the graph with axes and points
   if logy: ROOT.gPad.SetLogz()
   c4.Modified()
   c4.Update()

#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   c1.SaveAs("%s/FakeRate_TightToLoose_lepPt%s.png"%(savedir, suffix))
   c1.SaveAs("%s/pdf/FakeRate_TightToLoose_lepPt%s.pdf"%(savedir, suffix))
   c1.SaveAs("%s/root/FakeRate_TightToLoose_lepPt%s.root"%(savedir, suffix))
   
   c2.SaveAs("%s/FakeRate_TightToLoose_lepEta%s.png"%(savedir, suffix))
   c2.SaveAs("%s/pdf/FakeRate_TightToLoose_lepEta%s.pdf"%(savedir, suffix))
   c2.SaveAs("%s/root/FakeRate_TightToLoose_lepEta%s.root"%(savedir, suffix))

   if do2D:   
      c3.SaveAs("%s/FakeRate_TightToLoose_2D_Ratio%s.png"%(savedir, suffix))
      c3.SaveAs("%s/pdf/FakeRate_TightToLoose_2D_Ratio%s.pdf"%(savedir, suffix))
      c3.SaveAs("%s/root/FakeRate_TightToLoose_2D_Ratio%s.root"%(savedir, suffix))
      
      c4.SaveAs("%s/FakeRate_TightToLoose_2D_distributions%s.png"%(savedir, suffix))
      c4.SaveAs("%s/pdf/FakeRate_TightToLoose_2D_distributions%s.pdf"%(savedir, suffix))
      c4.SaveAs("%s/root/FakeRate_TightToLoose_2D_distributions%s.root"%(savedir, suffix))

   if "measurement" in region:
      if subtractEWK:
         c1.SaveAs("%s/FakeRate_TightToLoose_lepPt%s.root"%(resultsDir1, suffix))
         c2.SaveAs("%s/FakeRate_TightToLoose_lepEta%s.root"%(resultsDir1, suffix))
         if do2D: c3.SaveAs("%s/FakeRate_TightToLoose_2D_Ratio%s.root"%(resultsDir1, suffix))
      elif sample == "qcd":
         c1.SaveAs("{}/FakeRate_TightToLoose_lepPt{}.root".format(resultsDir2, suffix).replace("qcd", "MC"))
         c2.SaveAs("{}/FakeRate_TightToLoose_lepEta{}.root".format(resultsDir2, suffix).replace("qcd", "MC"))
         if do2D: c3.SaveAs("{}/FakeRate_TightToLoose_2D_Ratio{}.root".format(resultsDir2, suffix).replace("qcd", "MC"))

##Yields
#if doYields:
#   selList['loose'] = [filters, selection[region].combined, selection['loose']] 
#   selList['tight'] = selList['loose'][:]
#   selList['tight'].extend([selection['tight'], selection['match']]) 
#   
#   selClass = {}
#   selClass['loose'] = CutClass("loose", [["loose", combineCutsList(selList['loose'])]], baseCut = None)
#   selClass['tight'] = CutClass("tight", [["tight", combineCutsList(selList['tight'])]], baseCut = None)
#   
#   yields = {}
#   
#   yields['loose'] = Yields(samples, samplesList, selClass['loose'], cutOpt = "combinedList", pklOpt = False, tableName = "loose", nDigits = 2, err = True, verbose = True, nSpaces = 1)
#   yields['tight'] = Yields(samples, samplesList, selClass['tight'], cutOpt = "combinedList", pklOpt = False, tableName = "tight", nDigits = 2, err = True, verbose = True, nSpaces = 1)

#   #nBin['cmg'][bin] = getYieldFromChain(t1, skimString, "1")
#   
#   for samp in samplesList:
#      print "***"
#      print "Sample: ", samp
#      print "Using Yields class:"
#      print "L Entries (Yields):"
#      pprint(yields['loose'].yieldDictFull[samp])
#      print "From Histogram::"
#      print "L Entries (Hist): ", hists['loose']['pt'][samp].Integral(0, 100000)
#      print "T Entries (Hist): ", hists['tight']['pt'][samp].Integral(0, 100000)

#if doYields: 
#   print "Sample: data-EWK"
#   print "L Entries (Hist)", hists['loose']['pt']['data-EWK'].Integral(0, 1000)
#   print "T Entries (Hist)", hists['tight']['pt']['data-EWK'].Integral(0, 1000)
#   print "***"
