# QCD_closure.py
# Script to calculate the MC closure of the QCD estimation 
# Mateusz Zarucki 2016

import ROOT
import os, sys
import argparse
import pickle
import numpy as np
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import makeDir, setup_style
from Workspace.HEPHYPythonTools import u_float
from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--ABCD", dest = "ABCD",  help = "ABCD method", type = str, default = "2D")
parser.add_argument("--SR", dest = "SR",  help = "Signal region", type = str, default = "SR1")
parser.add_argument("--loosenMET", dest = "loosenMET",  help = "Loosen MET?", type = int, default = 0)
parser.add_argument("--save", dest="save",  help="Toggle Save", type=int, default=1)
parser.add_argument("-b", dest="batch",  help="Batch Mode", action="store_true", default=False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Sets TDR style
#setup_style()
ROOT.gStyle.SetOptStat(0)

#Arguments 
ABCD = args.ABCD
SR = args.SR
loosenMET = args.loosenMET
save = args.save

if loosenMET:
   HT_MET = {"1":["250", "250", "200"], "2":["300", "250", "200"], "3":["300", "300", "200"], "4":["300", "300", "250"], "5":["350", "300", "200"], "6":["350", "300", "250"], "7":["400", "300", "200"], "8":["400", "300", "250"]}
else:
   HT_MET = {"1":["200", "200"], "2":["250", "200"], "3":["250", "250"], "4":["300", "250"], "5":["300", "300"], "6":["350", "300"], "7":["400", "300"]}

path = {'muon':{}, 'electron':{}}
QCDyields = {'muon':{}, 'electron':{}}
QCDest_MC = {'muon':{}, 'electron':{}}

#regions = ['SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']

tag = "8012_mAODv2_v3/80X_postProcessing_v10"
path = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/QCD"%tag

if loosenMET: suffix = "METloose"
else: suffix = "noMETloose"

for channel in ['electron', 'muon']:
   for point in HT_MET:
   
      if loosenMET:
         if channel == "muon": path[channel][point] = "%s/%s/2D/estimation/METloose/loosenedIP/HT%sMET%sMETloose%s"%(path, channel, HT_MET[point][0], HT_MET[point][1], HT_MET[point][2])
         if channel == "electron": path[channel][point] = "%s/%s/2D/estimation/METloose/invertedSigmaEtaEta/HT%sMET%sMETloose%s"%(path, channel, HT_MET[point][0], HT_MET[point][1], HT_MET[point][2])
         
         if channel == "muon": QCDyields[channel][point] = pickle.load(open("%s/QCDyields_muon_HT%s_MET%s_METloose%s.pkl"%(path[channel][point], HT_MET[point][0], HT_MET[point][1], HT_MET[point][2]), "r"))
         if channel == "electron": QCDyields[channel][point] = pickle.load(open("%s/QCDyields_ele_HT%s_MET%s_METloose%s.pkl"%(path[channel][point], HT_MET[point][0], HT_MET[point][1], HT_MET[point][2]), "r"))
         
         if channel == "muon": QCDest_MC[channel][point] = pickle.load(open("%s/QCDest_MC_muon_HT%s_MET%s_METloose%s.pkl"%(path[channel][point], HT_MET[point][0], HT_MET[point][1], HT_MET[point][2]), "r"))
         if channel == "electron": QCDest_MC[channel][point] = pickle.load(open("%s/QCDest_MC_ele_HT%s_MET%s_METloose%s.pkl"%(path[channel][point], HT_MET[point][0], HT_MET[point][1], HT_MET[point][2]), "r"))

      else:
         if channel == "muon": path[channel][point] = "%s/%s/2D/estimation/noMETloose/appliedIP/HT%sMET%s"%(path, channel, HT_MET[point][0], HT_MET[point][1])
         if channel == "electron": path[channel][point] = "%s/%s/2D/estimation/noMETloose/invertedSigmaEtaEta/HT%sMET%s"%(path, channel, HT_MET[point][0], HT_MET[point][1])

         if channel == "muon": QCDyields[channel][point] = pickle.load(open("%s/QCDyields_muon_HT%s_MET%s.pkl"%(path[channel][point], HT_MET[point][0], HT_MET[point][1]), "r"))
         if channel == "electron": QCDyields[channel][point] = pickle.load(open("%s/QCDyields_ele_HT%s_MET%s.pkl"%(path[channel][point], HT_MET[point][0], HT_MET[point][1]), "r"))

         if channel == "muon": QCDest_MC[channel][point] = pickle.load(open("%s/QCDest_MC_muon_HT%s_MET%s.pkl"%(path[channel][point], HT_MET[point][0], HT_MET[point][1]), "r"))
         if channel == "electron": QCDest_MC[channel][point] = pickle.load(open("%s/QCDest_MC_ele_HT%s_MET%s.pkl"%(path[channel][point], HT_MET[point][0], HT_MET[point][1]), "r"))

   c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
   
   gr1 = emptyHist("", len(HT_MET), 0, len(HT_MET)) 
   #gr1 = ROOT.TGraphErrors(len(regions), np.array(array), np.array(yvals), np.zeros(len(regions)), np.array(yval_errs))
   gr1.SetName("MC")
   gr1.SetTitle("Closure Test: Pure MC QCD Estimate vs QCD MC Yield in %s for the %s ABCD Method in the %s Channel"%(SR, ABCD, channel.title()))
   
   gr2 = emptyHist("", len(HT_MET), 0, len(HT_MET)) 
   #gr2 = ROOT.TGraphErrors(len(regions), np.array(array), np.array(yvals), np.zeros(len(regions)), np.array(yval_errs))
   gr2.SetName("QCDest")
   
   for point in HT_MET:
      #print "HT%s_MET%s_METloose%s"%(HT_MET[point][0], HT_MET[point][1], HT_MET[point][2]), ":", float(QCDest_MC[channel][point][SR].val), "+-", float(QCDest_MC[channel][point][SR].sigma), "vs", float(QCDyields[channel][point][SR]['SR'].val), "+-", float(QCDyields[channel][point][SR]['SR'].sigma)
      gr1.SetBinContent(int(point), float(QCDyields[channel][point][SR]['SR'].val))
      gr1.SetBinError(int(point), float(QCDyields[channel][point][SR]['SR'].sigma))
      if loosenMET: gr1.GetXaxis().SetBinLabel(int(point), "HT%s_MET%s_METloose%s"%(HT_MET[point][0], HT_MET[point][1], HT_MET[point][2]))
      else:         gr1.GetXaxis().SetBinLabel(int(point), "HT%s_MET%s"%(HT_MET[point][0], HT_MET[point][1]))     
 
      gr2.SetBinContent(int(point), float(QCDest_MC[channel][point][SR].val))
      gr2.SetBinError(int(point), float(QCDest_MC[channel][point][SR].sigma))
      #gr2.GetXaxis().SetBinLabel(int(point), "HT%s_MET%s_METloose%s"%(HT_MET[point][0], HT_MET[point][1], HT_MET[point][2]))
   
   gr1.Draw("PE1")

   ROOT.gStyle.SetErrorX(0)
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   gr1.GetYaxis().SetTitle("Events")
   gr1.GetYaxis().SetRangeUser(0, float(QCDyields[channel]['1'][SR]['SR'].val) * 3)
   #gr1.GetYaxis().SetRangeUser(0,20)
   gr1.GetXaxis().SetLabelSize(0.02)
   #gr1.GetXaxis().SetRangeUser(0,50)
   
   gr1.SetMarkerStyle(33)
   gr1.SetMarkerColor(ROOT.kRed+1)
   gr1.SetMarkerSize(2)
   gr1.SetLineColor(ROOT.kRed+1)
   gr1.SetLineWidth(2)
   
   gr2.Draw("samePE1")
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   gr2.SetMarkerStyle(20)
   gr2.SetMarkerColor(ROOT.kBlue+1)
   gr2.SetMarkerSize(1.5)
   gr2.SetLineColor(ROOT.kBlue+1)
   gr2.SetLineWidth(2)

   leg = ROOT.TLegend(0.6, 0.7, 0.875, 0.875) #x1,y1,x2,y2
   leg.AddEntry("QCDest", "QCD Estimate (pure MC)", "P")
   leg.AddEntry("MC", "MC Yield", "P")
   leg.Draw()
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   #alignLegend(l1) 
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   c1.Modified()
   c1.Update()
   
   #Write to file
   if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID

      makeDir("%s/closure/%s/root"%(path, channel))
      makeDir("%s/closure/%s/pdf"%(path, channel))
   
      #Save to Web
      c1.SaveAs("%s/closure/%s/closure_%s_%s_%s_%s.png"%(path, channel, channel, suffix, ABCD, SR))
      c1.SaveAs("%s/closure/%s/root/closure_%s_%s_%s_%s.root"%(path, channel, channel, suffix, ABCD, SR))
      c1.SaveAs("%s/closure/%s/pdf/closure_%s_%s_%s_%s.pdf"%(path, channel, channel, suffix, ABCD, SR))
