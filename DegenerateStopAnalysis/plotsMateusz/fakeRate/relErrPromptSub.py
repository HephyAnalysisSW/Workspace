# relErrPromptSub.py 
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
   savedir = fakeInfo['savedir']
   suffix =  fakeInfo['suffix']

# Open results pickle

pklPath = "%s/fakesEstimation_yields%s.pkl"%(savedir,suffix)

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
   binNames = ["0-3.5", "3.5-5", "5-12", "12-20", "20-30", "30-200", ">200"]
else:
   binNames = ["0-5", "5-12", "12-20", "20-30", "30-200", ">200"]
 
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
   gr1.SetTitle("Relative error on Fake-Rate Estimate in %s (%s) with Prompt Subtraction Considered)"%(region, measurementRegion))
   gr1.SetMarkerColor(ROOT.kBlue)
   gr1.SetMarkerStyle(ROOT.kFullCircle)
   gr1.SetMarkerSize(1)
   gr1.GetXaxis().SetTitle("%s p_{T}"%lepton)
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
      binIndex = gr1.GetXaxis().FindBin(i+1)
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
