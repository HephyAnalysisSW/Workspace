# WpolSystematics.py
# Script for determination of W polarisation systematics
# Mateusz Zarucki 2016

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
parser = argparse.ArgumentParser(description = "Input options")
#parser.add_argument("--plot", dest = "plot",  help = "Toggle plot", type = int, default = 0)
parser.add_argument("--saveFactors", dest = "saveFactors",  help = "Save factors", type = int, default = 0)
parser.add_argument("--makeTables", dest = "makeTables",  help = "Results table", type = int, default = 0)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
#plot = args.plot
saveFactors = args.saveFactors
makeTables = args.makeTables

tag = "8012_mAODv2_v3/80X_postProcessing_v10"

path = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/Wpol/13TeV_fractions/"%tag

makeDir(path)

WpolRatios = {} 
sysUnc = {}
totalSysUnc = {}

SRs = ['SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRL1b', 'SRL1c', 'SRH1a', 'SRH1b', 'SRH1c', 'SRV1a', 'SRV1b', 'SRV1c', 'SR2', 'SRL2', 'SRH2', 'SRV2']

for variation in ['FLminusFR', 'FLFR+', 'FLFR-', 'F0']:

   sysUnc[variation] = {}
 
   WpolRatios[variation] = pickle.load(open("%s/%s/WpolRatios.pkl"%(path, variation), "r"))
  
   for reg in SRs: 
      sysUnc[variation][reg] = WpolRatios[variation][reg]['ratio'].val - 1

sysUnc['total'] = {}

for reg in SRs: 
   sysUnc['total'][reg] = math.sqrt(sysUnc['FLminusFR'][reg]**2 + sysUnc['FLFR+'][reg]**2 + sysUnc['FLFR-'][reg]**2 + sysUnc['F0'][reg]**2)
   print "Total sys. unc.: ", reg, ":", sysUnc['total'][reg]*100
   totalSysUnc[reg] = sysUnc['total'][reg]*100

pickleFile = open("%s/WpolUncertainties.pkl"%path, "w")
pickle.dump(sysUnc, pickleFile)
pickleFile.close()

if saveFactors:

   publicdir = "/afs/hephy.at/user/m/mzarucki/public/results/Wpol"
   makeDir(publicdir)

   finalSysUnc = {}  
   finalRatios = {}
 
   for reg in SRs:
      finalSysUnc[reg] = sysUnc['FLminusFR'][reg]*100
      finalRatios[reg] = WpolRatios['FLminusFR'][reg]['ratio']

   pickleFile2 = open("%s/WpolSysUnc.pkl"%publicdir, "w")
   pickle.dump(finalSysUnc, pickleFile2)
   pickleFile2.close()
 
   pickleFile3 = open("%s/WpolRatios.pkl"%publicdir, "w")
   pickle.dump(finalRatios, pickleFile3)
   pickleFile3.close()

if makeTables:
   
   WpolRows = []
   listTitle = ['Region', 'FL-FR: SF(SR/CR) Ratio', 'FL-FR: Sys. Unc. (\%)', 'FLFR+: SF(SR/CR) Ratio', 'FLFR+: Sys. Unc. (\%)', 'FLFR-: SF(SR/CR) Ratio', 'FLFR-: Sys. Unc. (\%)', 'F0: SF(SR/CR) Ratio', 'F0: Sys. Unc. (\%)', 'Total Unc. (\%)'] 
   WpolRows.append(listTitle)
   for reg in SRs: 
      WpolRow = [reg, WpolRatios['FLminusFR'][reg]['ratio'].round(2), "%.2f"%(sysUnc['FLminusFR'][reg]*100),  WpolRatios['FLFR+'][reg]['ratio'].round(2), "%.2f"%(sysUnc['FLFR+'][reg]*100), WpolRatios['FLFR-'][reg]['ratio'].round(2), "%.2f"%(sysUnc['FLFR-'][reg]*100), WpolRatios['F0'][reg]['ratio'].round(2), "%.2f"%(sysUnc['F0'][reg]*100), "%.2f"%(sysUnc['total'][reg]*100)] 
      WpolRows.append(WpolRow)
   
   makeSimpleLatexTable(WpolRows, "WpolSysUnc", path)

#if plot:
#   for Zchannel in corr.keys():
#      #Sets TDR style
#      setup_style()
#      
#      #arrays for plot
#      CT_arr = [int(x) for x in CTs]
#      corr_el_arr = []
#      corr_el_err_arr = []
#      corr_mu_arr = []
#      corr_mu_err_arr = []
#      
#      for i, CT in enumerate(CTs):
#         corr_el_arr.append(corr[Zchannel]['CT' + CT]['electrons'].val)
#         corr_el_err_arr.append(corr[Zchannel]['CT' + CT]['electrons'].sigma)
#         corr_mu_arr.append(corr[Zchannel]['CT' + CT]['muons'].val)
#         corr_mu_err_arr.append(corr[Zchannel]['CT' + CT]['muons'].sigma)
#      
#      c1 = ROOT.TCanvas("c1", "ratioCT")
#      c1.SetGrid() #adds a grid to the canvas
#      #c1.SetFillColor(42)
#      c1.GetFrame().SetFillColor(21)
#      c1.GetFrame().SetBorderSize(12)
#      
#      gr1 = ROOT.TGraphErrors(len(CT_arr), np.array(CT_arr, 'float64'), np.array(corr_el_arr, 'float64'), np.array([0]), np.array(corr_el_err_arr, 'float64')) #graph object with error bars using arrays of data
#      gr1.SetTitle("Z_{inv} Correction Factors for N_{\nu\nu l}^{ MC}  as a Function C_{T2} Cut")
#      gr1.SetMarkerColor(ROOT.kBlue)
#      gr1.SetMarkerStyle(ROOT.kFullCircle)
#      gr1.SetMarkerSize(1)
#      gr1.GetXaxis().SetTitle("Lower Cut on C_{T1} = min(emulated #slash{E}_{T}, H_{T} - 100 GeV)")
#      if Zchannel == "Zmumu": gr1.GetYaxis().SetTitle("\\mathrm{R}_{\mu\mu \\mathscr{l}} = R_{\mu\mu}*R_{\mu\mu \\mathscr{l}/\mu\mu}")
#      elif Zchannel == "Zee": gr1.GetYaxis().SetTitle("\\mathrm{R_{ee \\mathscr{l}} = R_{ee}*R_{ee \\mathscr{l}/ee}}")
#      else: gr1.GetYaxis().SetTitle("\\mathscr{\\mathrm{R}_{ll l} = \\mathrm{R}_{ll}*\\mathrm{R}_{ll l/ll}}")
#      gr1.GetXaxis().CenterTitle()
#      gr1.GetYaxis().CenterTitle()
#      gr1.GetXaxis().SetTitleSize(0.04)
#      gr1.GetYaxis().SetTitleSize(0.04)
#      gr1.GetYaxis().SetNdivisions(512);
#      gr1.GetXaxis().SetTitleOffset(1.4)
#      gr1.GetYaxis().SetTitleOffset(1.6)
#      gr1.SetMinimum(0.2)
#      gr1.SetMaximum(2.7)
#      gr1.Draw("AP") #plots the graph with axes and points
#      
#      gr2 = ROOT.TGraphErrors(len(CT_arr), np.array(CT_arr, 'float64'), np.array(corr_mu_arr, 'float64'), np.array([0]), np.array(corr_mu_err_arr, 'float64')) #graph object with error bars using arrays of data
#      gr2.SetMarkerColor(ROOT.kRed)
#      gr2.SetMarkerStyle(ROOT.kFullCircle)
#      gr2.SetMarkerSize(1)
#      gr2.Draw("Psame")
#      
#      leg = ROOT.TLegend(0.20, 0.8, 0.55, 0.925) #x1,y1,x2,y2
#      #leg = ROOT.TLegend(0.600, 0.8, 0.95, 0.925) #x1,y1,x2,y2
#      leg.AddEntry(gr1, "Electron Channel", "P")
#      leg.AddEntry(gr2, "Muon Channel", "P")
#      leg.SetTextSize(0.03)
#      leg.Draw()
#
#      #Save to Web
#      c1.SaveAs("%s/ratioCTplot_%s.png"%(plotdir, Zchannel))
#      c1.SaveAs("%s/ratioCTplot_%s.pdf"%(plotdir, Zchannel))
#      c1.SaveAs("%s/ratioCTplot_%s.root"%(plotdir, Zchannel))
