# simulFakesUnc.py 
# Mateusz Zarucki 2017

import os
import numpy as np
from fakeInfo import *

script = os.path.basename(__file__) #sys.argv[0]

#Arguments
args = fakeParser(script)

lep = args.lep
region = args.region
measurementRegion = args.measurementRegion
measurementType = args.measurementType
considerFakeTaus = args.considerFakeTaus
doPlots = args.doPlots
#makeTables = args.makeTables
varBins = args.varBins
save = args.save
verbose = args.verbose

fakeInfo = fakeInfo(script, vars(args))

lepton =      fakeInfo['lepton']
samplesList = fakeInfo['samplesList']
samples =     fakeInfo['samples']
selection =   fakeInfo['selection']
bins =        fakeInfo['bins']

if save:
   baseDir = fakeInfo['baseDir']
   baseDir += "/applicationRegions"
   savedir = baseDir + "/fakesUncertainties"
   suffix = "_%s"%lep 

   if considerFakeTaus:
      fakeTauDir = "fakeTausConsidered"
   else:
      fakeTauDir = "fakeTausNotConsidered"

   if varBins:
      binDir = "varBins"
   else:
      binDir = "fixedBins"

   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

ARs = [d for d in os.listdir(baseDir) if os.path.isdir(os.path.join(baseDir, d)) and 'application' in d]

# Open results pickle
estimate = {}
relErrEstimate = {}

for AR in ARs:
   pklPath = "%s/%s/estimation/SR/%s/allBins/%s/%s/L!T/TL_%s/%s/fakesEstimation_yields_%s_%s_%s.pkl"%(baseDir, AR, measurementRegion, fakeTauDir, lepton, measurementType, binDir, lep, AR, measurementType)

   fakesResults = pickle.load(open(pklPath, "r"))
   
   estimate[AR] = {}
   estimate[AR]['fakes'] =      fakesResults['estimate']['fakes']
   estimate[AR]['tot-prompt'] = fakesResults['estimate']['tot-prompt']
   
   relErrEstimate[AR] = {'fakes':{}, 'tot-prompt':{}} 
   
   for x in relErrEstimate[AR]:
      for bin in estimate[AR][x]:
         if estimate[AR][x][bin].val:
            relErrEstimate[AR][x][bin] = estimate[AR][x][bin].sigma/estimate[AR][x][bin].val 

if lep == "mu":
   binNames = ["0-3.5", "3.5-5", "5-12", "12-20", "20-30", "30-200", ">200"]
else:
   binNames = ["0-5", "5-12", "12-20", "20-30", "30-200", ">200"]
 
if doPlots:
   #Sets TDR style
   setup_style()
   
   #arrays for plot
   bins = [int(x) for x in relErrEstimate[ARs[0]][relErrEstimate[ARs[0]].keys()[0]].keys()]

   relErr_arr = {}
   relErr_err_arr = {}
   
   for AR in ARs:
      relErr_arr[AR] = {}
      relErr_arr[AR]['fakes'] = []
      relErr_arr[AR]['tot-prompt'] = []
  
      relErr_err_arr[AR] = []
 
      for x in relErrEstimate[AR]:
         for bin in bins:
            relErr_arr[AR][x].append(relErrEstimate[AR][x][bin])
            relErr_err_arr[AR].append(0)#relErrEstimate[bin].sigma)
   
   c1 = ROOT.TCanvas("c1", "relErr")
   c1.SetGrid() #adds a grid to the canvas
   #c1.SetFillColor(42)
   c1.GetFrame().SetFillColor(21)
   c1.GetFrame().SetBorderSize(12)
  
   gr = {}
   
   for i, AR in enumerate(ARs):
 
      gr[AR] = ROOT.TGraphErrors(len(bins), np.array(bins, 'float64'), np.array(relErr_arr[AR]['tot-prompt'], 'float64'), np.array([0]), np.array(relErr_err_arr[AR], 'float64')) #graph object with error bars using arrays of data
      
      if i == 0:
         gr[AR].SetTitle("Relative error on Fake-Rate Estimate in %s (%s) with Prompt Subtraction Considered)"%(region, measurementRegion))
         gr[AR].GetXaxis().SetTitle("%s p_{T}"%lepton)
         gr[AR].GetYaxis().SetTitle("Relative Error on Prediction")
         gr[AR].GetXaxis().CenterTitle()
         gr[AR].GetYaxis().CenterTitle()
         gr[AR].GetXaxis().SetTitleSize(0.04)
         gr[AR].GetYaxis().SetTitleSize(0.04)
         gr[AR].GetYaxis().SetNdivisions(512);
         gr[AR].GetXaxis().SetTitleOffset(1.4)
         gr[AR].GetYaxis().SetTitleOffset(1.6)
         gr[AR].SetMinimum(0)
         gr[AR].SetMaximum(1.5)
      
         leg = ROOT.TLegend(0.20, 0.75, 0.35, 0.925) #x1,y1,x2,y2
         leg.SetTextSize(0.03)
      
         for x, binName in enumerate(binNames):
            binIndex = gr[AR].GetXaxis().FindBin(x+1)
            gr[AR].GetXaxis().SetBinLabel(binIndex, binName)
         
      gr[AR].SetMarkerStyle(ROOT.kFullCircle)
      gr[AR].SetMarkerSize(1)
      gr[AR].SetMarkerColor(2+i)
      
      if i == 0: gr[AR].Draw("AP") #plots the graph with axes and points
      else:      gr[AR].Draw("Psame")
   
   #leg = ROOT.TLegend(0.600, 0.8, 0.95, 0.925) #x1,y1,x2,y2
      leg.AddEntry(gr[AR], AR.replace('application_', ''), "P")
         
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
