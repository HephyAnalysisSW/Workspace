# fakesUncertainties.py 
# Mateusz Zarucki 2017

import os, sys
import ROOT
import argparse
import pickle
import math
import numpy as np
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import makeSimpleLatexTable, setup_style, makeDir
from Workspace.HEPHYPythonTools import u_float
   
#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--lep", dest = "lep", help = "Lepton", type = str, default = "el")
parser.add_argument("--region", dest = "reg", help = "Measurement or application region", type = str, default = "application_sr1")
parser.add_argument("--CT200", help = "Loosen CT cut to 200", action = "store_true")
parser.add_argument("--invAntiQCD", help = "Invert anti-QCD cut", action = "store_true")
parser.add_argument("--mva", help = "MVA", action = "store_true")
parser.add_argument("--measurementRegion", dest = "measurementRegion", help = "Measurement region", type = str, default = "measurement1")
parser.add_argument("--fakeRateMeasurement", dest = "fakeRateMeasurement", help = "Source of fake rate measurement", type = str, default = "MC")
parser.add_argument("--looseNotTight", help = "Loose-not-tight CR", action = "store_true")
parser.add_argument("--highPtBin", help = "High pt bin", action = "store_true")
parser.add_argument("--doPlots", dest = "doPlots",  help = "Toggle plot", type = int, default = 1)
parser.add_argument("--makeTables", dest = "makeTables",  help = "Results table", type = int, default = 0)
parser.add_argument("--varBins", help = "Variable bin size", action = "store_true")
parser.add_argument("--save", dest="save", help="Toggle save", type=int, default=1)
parser.add_argument("--verbose", help = "Verbosity switch", action = "store_true")
parser.add_argument("-b", dest="batch", help="Batch mode", action="store_true", default=False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
lep = args.lep
reg = args.reg
CT200 = args.CT200
invAntiQCD = args.invAntiQCD
mva = args.mva
measurementRegion = args.measurementRegion
fakeRateMeasurement = args.fakeRateMeasurement
looseNotTight = args.looseNotTight
highPtBin = args.highPtBin
doPlots = args.doPlots
makeTables = args.makeTables
varBins = args.varBins
save = args.save
verbose = args.verbose

if lep == "el":    lepton = "Electron" #pdgId = "11"
elif lep == "mu":  lepton = "Muon" #pdgId = "13" 
elif lep == "lep": lepton = "Lepton"

varBins = True
looseNotTight = True

#Bin dir 
if save:
   binDir = "/TL_" + fakeRateMeasurement

   if not varBins: binDir += "/fixedBins"
   else:           binDir += "/varBins"
#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   tag = "8020_mAODv2_v5/80X_postProcessing_v0"
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/fakesEstimation"%tag

   if mva: savedir += "/%s_id%s_bdt%s"%(reg, selection['mvaId'], selection['bdtcut'])
   else:   savedir += "/%s"%reg

   if CT200 and invAntiQCD: savedir += "/CT200_invAntiQCD"
   elif CT200:              savedir += "/CT200"
   elif invAntiQCD:         savedir += "/invAntiQCD"

   savedir += "/" + measurementRegion

   if highPtBin: savedir += "/highPtBin"
   else:         savedir += "/allBins"

   savedir += "/estimation/%s"%lepton

   if looseNotTight: savedir += "/L!T"
   else:             savedir += "/Loose"

   savedir += binDir

   suffix = "%s_%s"%(reg, lep)

   #tabledir = savedir + "/tables" 
   #plotdir = savedir + "/plots"
 
# Open results pickle

pklPath = "%s/fakesEstimation_%s.pkl"%(savedir,suffix)

fakesResults = pickle.load(open(pklPath, "r"))

estimate = {}
estimate['fakes'] = fakesResults['estimate']['fakes']
estimate['tot-prompt'] = fakesResults['estimate']['tot-prompt']

relErrEstimate = {'fakes':{}, 'tot-prompt':{}} 

for x in relErrEstimate:
   for bin in estimate[x]:
      if estimate[x][bin].val:
         relErrEstimate[x][bin] = estimate[x][bin].sigma/estimate[x][bin].val 

if lep == "mu":
   binNames = ["0-3.5", "3.5-5", "5-12", "12-20", "20-30", "30-50", "50-100", "100-200"]
else:
   binNames = ["0-5", "5-12", "12-20", "20-30", "30-50", "50-100", "100-200"]
 
if doPlots:
   #Sets TDR style
   setup_style()
   
   #arrays for plot
   bins = [int(x) for x in relErrEstimate[relErrEstimate.keys()[0]].keys()]

   relErr_arr = {}
   relErr_arr['fakes'] = []
   relErr_arr['tot-prompt'] = []
  
   relErr_err_arr = []
 
   for x in relErrEstimate:
      for bin in bins:
         relErr_arr[x].append(relErrEstimate[x][bin])
         relErr_err_arr.append(0)#relErrEstimate[bin].sigma)
   
   c1 = ROOT.TCanvas("c1", "relErr")
   c1.SetGrid() #adds a grid to the canvas
   #c1.SetFillColor(42)
   c1.GetFrame().SetFillColor(21)
   c1.GetFrame().SetBorderSize(12)
   
   gr1 = ROOT.TGraphErrors(len(bins), np.array(bins, 'float64'), np.array(relErr_arr['tot-prompt'], 'float64'), np.array([0]), np.array(relErr_err_arr, 'float64')) #graph object with error bars using arrays of data
   gr1.SetTitle("Relative error on Fake-Rate Estimate in %s (%s) with Prompt Subtraction Considered)"%(reg, measurementRegion))
   gr1.SetMarkerColor(ROOT.kBlue)
   gr1.SetMarkerStyle(ROOT.kFullCircle)
   gr1.SetMarkerSize(1)
   gr1.GetXaxis().SetTitle("Bin")
   gr1.GetYaxis().SetTitle("Relative Error on Prediction")
   gr1.GetXaxis().CenterTitle()
   gr1.GetYaxis().CenterTitle()
   gr1.GetXaxis().SetTitleSize(0.04)
   gr1.GetYaxis().SetTitleSize(0.04)
   gr1.GetYaxis().SetNdivisions(512);
   gr1.GetXaxis().SetTitleOffset(1.4)
   gr1.GetYaxis().SetTitleOffset(1.6)
   gr1.SetMinimum(0)
   gr1.SetMaximum(1.5)
   
   for i, binName in enumerate(binNames):
      binIndex = gr1.GetXaxis().FindBin(i)
      gr1.GetXaxis().SetBinLabel(binIndex, binName)

   gr1.Draw("AP") #plots the graph with axes and points
   
   gr2 = ROOT.TGraphErrors(len(bins), np.array(bins, 'float64'), np.array(relErr_arr['fakes'], 'float64'), np.array([0]), np.array(relErr_err_arr, 'float64')) #graph object with error bars using arrays of data
   gr2.SetMarkerColor(ROOT.kRed)
   gr2.SetMarkerStyle(ROOT.kFullCircle)
   gr2.SetMarkerSize(1)
   gr2.Draw("Psame")
   
   leg = ROOT.TLegend(0.20, 0.8, 0.75, 0.925) #x1,y1,x2,y2
   #leg = ROOT.TLegend(0.600, 0.8, 0.95, 0.925) #x1,y1,x2,y2
   leg.AddEntry(gr2, "No Prompt Subtraction", "P")
   leg.AddEntry(gr1, "Prompt Subtraction", "P")
   leg.SetTextSize(0.03)
   leg.Draw()
   
   #Save to Web
   c1.SaveAs("%s/relErrEstimate_promptSub%s.png"%(savedir, suffix))
   c1.SaveAs("%s/relErrEstimate_promptSub%s.pdf"%(savedir, suffix))
   c1.SaveAs("%s/relErrEstimate_promptSub%s.root"%(savedir, suffix))

#if makeTables:
#
#   #Ratios
#   for channel in corr:
#      ZinvRows = []
#      listTitle = ['CT', 'Zpeak_data', 'Zpeak_dy', 'Zpeak_tt', 'Zpeak_vv', 'Nel_data', 'Nel_dy', 'Nel_tt', 'Nel_vv', 'Nmu_data', 'Nmu_dy', 'Nmu_tt', 'Nmu_vv']
#      ZinvRows.append(listTitle)
#      for CT2 in CTs:
#         ZinvRow = [CT2, 
#         ZinvYields[channel]['CT' + CT2]['Zpeak']['data'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Zpeak']['dy'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Zpeak']['tt'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Zpeak']['vv'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Nel']['data'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Nel']['dy'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Nel']['tt'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Nel']['vv'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Nmu']['data'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Nmu']['dy'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Nmu']['tt'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Nmu']['vv'].round(4)] 
#         ZinvRows.append(ZinvRow)
#      
#      makeSimpleLatexTable(ZinvRows, "ZinvYields_" + channel, tabledir)
#
#      ZinvRows = []
#      listTitle = ['CT', 'Zpeak_dataMC', 'prob_el_data', 'prob_el_MC', 'prob_el_dataMC', 'prob_mu_data', 'prob_mu_MC', 'prob_mu_dataMC']
#      #listTitle.extend(ZinvRatios[channel]['CT' + CT2].keys())
#      ZinvRows.append(listTitle)
#      for CT2 in CTs:
#         ZinvRow = [CT2, ZinvRatios[channel]['CT' + CT2]['Zpeak_dataMC'].round(4), 
#                         ZinvRatios[channel]['CT' + CT2]['prob_el_data'].round(4), ZinvRatios[channel]['CT' + CT2]['prob_el_MC'].round(4), ZinvRatios[channel]['CT' + CT2]['prob_el_dataMC'].round(4),   
#                         ZinvRatios[channel]['CT' + CT2]['prob_mu_data'].round(4), ZinvRatios[channel]['CT' + CT2]['prob_mu_MC'].round(4), ZinvRatios[channel]['CT' + CT2]['prob_mu_dataMC'].round(4)]
#         #ZinvRow.extend([x.round(4) for x in ZinvRatios[channel]['CT' + CT2].values()])
#         ZinvRows.append(ZinvRow)
#      
#      makeSimpleLatexTable(ZinvRows, "ZinvRatios_" + channel, tabledir)
#      
#      ZinvRows = []
#      listTitle = ['CT', 'Correction electrons', 'Correction muons']
#      ZinvRows.append(listTitle)
#      for CT2 in CTs:
#         ZinvRow = [CT2, corr[channel]['CT' + CT2]['electrons'].round(3), corr[channel]['CT' + CT2]['muons'].round(3)]
#         #ZinvRow.extend([x.round(4) for x in ZinvRatios[channel]['CT' + CT2].values()])
#         ZinvRows.append(ZinvRow)
#      
#      makeSimpleLatexTable(ZinvRows, "ZinvCorrections_" + channel, tabledir)
