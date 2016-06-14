# QCD_closure.py
 
import ROOT
import os, sys
import numpy as np
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from array import array
from math import pi, sqrt #cos, sin, sinh, log
import argparse

#Input options
parser = argparse.ArgumentParser(description="Input options")
#parser.add_argument("--ABCD", dest = "ABCD",  help = "ABCD method", type = str, default = "4")
parser.add_argument("--save", dest="save",  help="Toggle Save", type=int, default=1)
parser.add_argument("-b", dest="batch",  help="Batch Mode", action="store_true", default=False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

ROOT.gStyle.SetOptStat(0) #removes histogram statistics box

#Arguments 
#ABCD = args.ABCD
save = args.save

ABCDs = ["1", "2", "3", "4"]

for ABCD in ABCDs:
   filedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD/ABCD" + ABCD + "/estimation/Veto/highWeightVeto"
   suffix = "_HT300_MET300"
   if ABCD == "3": suffix += "_METloose250"
   filename = "QCDyields_Veto" + suffix + ".txt"
   
   yields = {}
   regions = ['SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']
   for reg in regions:
      yields[reg] = {}
   
   dummy = []
   
   ##Gets all file paths
   #for dirname in sorted(os.listdir(path)): 
   #   if dirname.startswith("histogramCounts"):
   #      print dirname
   #      dummy = dirname.split("_")
   #      filename = 'histogramCounts_' + dummy[1] + '_' + dummy[2]  + '.txt'
   #      files.append(os.path.join(path,dirname,filename))
   
   
   #sample = "S300_270Fast"
   c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
   
   #Extraction of data from file
   infile = open(filedir + "/" + filename, 'r') #.read() #opens data file
   print makeLine()
   print "Opening: ", infile.name
   print makeLine()
   
   for j,line in enumerate(infile):
      if j == 0:
         line = infile.next() 
         line = infile.next() 
      print line
      dummy = line.split()
      if ABCD == "1" or ABCD == "4": 
         yields[dummy[0]]['I_XA'] = float(dummy[1].split("+-")[0])
         yields[dummy[0]]['I_XA_err'] = float(dummy[1].split("+-")[1])
         yields[dummy[0]]['XA_I'] = float(dummy[2].split("+-")[0])
         yields[dummy[0]]['XA_I_err'] = float(dummy[2].split("+-")[1])
         yields[dummy[0]]['IA_X'] = float(dummy[3].split("+-")[0])
         yields[dummy[0]]['IA_X_err'] = float(dummy[3].split("+-")[1])
         yields[dummy[0]]['IXA'] = float(dummy[4].split("+-")[0])
         yields[dummy[0]]['IXA_err'] = float(dummy[4].split("+-")[1])
         yields[dummy[0]]['QCD'] = float(dummy[5].split("+-")[0])
         yields[dummy[0]]['QCD_err'] = float(dummy[5].split("+-")[1])
         yields[dummy[0]]['MC'] = float(dummy[6].split("+-")[0])
         yields[dummy[0]]['MC_err'] = float(dummy[6].split("+-")[1])
         #yields[dummy[0]]['Ratio'] = float(dummy[7].split("+-")[0])
         #yields[dummy[0]]['Ratio_err'] = float(dummy[7].split("+-")[1])
      elif ABCD == "2" or ABCD == "3":
         yields[dummy[0]]['I_XA'] = float(dummy[1].split("+-")[0])
         yields[dummy[0]]['I_XA_err'] = float(dummy[1].split("+-")[1])
         yields[dummy[0]]['A_IX'] = float(dummy[2].split("+-")[0])
         yields[dummy[0]]['A_IX_err'] = float(dummy[2].split("+-")[1])
         yields[dummy[0]]['IXA'] = float(dummy[3].split("+-")[0])
         yields[dummy[0]]['IXA_err'] = float(dummy[3].split("+-")[1])
         yields[dummy[0]]['QCD'] = float(dummy[4].split("+-")[0])
         yields[dummy[0]]['QCD_err'] = float(dummy[4].split("+-")[1])
         yields[dummy[0]]['MC'] = float(dummy[5].split("+-")[0])
         yields[dummy[0]]['MC_err'] = float(dummy[5].split("+-")[1])
         #yields[dummy[0]]['Ratio'] = float(dummy[6].split("+-")[0])
         #yields[dummy[0]]['Ratio_err'] = float(dummy[6].split("+-")[1])
 
   infile.close()
   
   #yvals = [yields[reg]['QCD'] for reg in regions]
   #yval_errs = [yields[reg]['QCD_err'] for reg in regions]
   
   gr1 = emptyHist("", len(regions) - 1, 0, len(regions) - 1) 
   #gr1 = ROOT.TGraphErrors(len(regions), np.array(array), np.array(yvals), np.zeros(len(regions)), np.array(yval_errs))
   gr1.SetName("QCD")
   gr1.SetTitle("Closure Test for ABCD" + ABCD + " Method | (MET, HT) > 300 GeV")
   
   for k,reg in enumerate(regions):
      if yields[reg]: 
         gr1.SetBinContent(k+1, float(yields[reg]['QCD']))
         gr1.SetBinError(k+1, float(yields[reg]['QCD_err']))
         gr1.GetXaxis().SetBinLabel(k+1, reg)
   
   
   gr1.Draw("PE1")
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   gr1.GetYaxis().SetTitle("Yield")
   gr1.GetYaxis().SetRangeUser(0,0.3)
   gr1.GetXaxis().SetRangeUser(0,15)
   
   gr1.SetMarkerStyle(33)
   gr1.SetMarkerColor(ROOT.kRed+1)
   gr1.SetMarkerSize(1.5)
   gr1.SetLineColor(ROOT.kRed+1)
   gr1.SetLineWidth(2)
   
   gr2 = emptyHist("", len(regions), 0, len(regions)) 
   #gr2 = ROOT.TGraphErrors(len(regions), np.array(array), np.array(yvals), np.zeros(len(regions)), np.array(yval_errs))
   gr2.SetName("MC")
   
   for k,reg in enumerate(regions):
      if yields[reg]:
         gr2.SetBinContent(k+1, float(yields[reg]['MC']))
         gr2.SetBinError(k+1, float(yields[reg]['MC_err']))
         gr2.GetXaxis().SetBinLabel(k+1, reg)
   
   gr2.Draw("samePE1")
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   gr2.SetMarkerStyle(20)
   gr2.SetMarkerColor(ROOT.kBlue+1)
   gr2.SetMarkerSize(1)
   gr2.SetLineColor(ROOT.kBlue+1)
   gr2.SetLineWidth(2)
   
   l1 = makeLegend()
   l1.AddEntry("QCD", "QCD est.", "P")
   l1.AddEntry("MC", "MC", "P")
   l1.Draw()
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   #alignLegend(l1) 
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   c1.Modified()
   c1.Update()
   
   #Write to file
   if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
      savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD/ABCD" + ABCD + "/closure"
   
      if not os.path.exists(savedir + "/root"): os.makedirs(savedir + "/root")
      if not os.path.exists(savedir + "/pdf"): os.makedirs(savedir + "/pdf")
   
      #Save to Web
      c1.SaveAs(savedir + "/closure_ABCD%s%s.png"%(ABCD, suffix))
      c1.SaveAs(savedir + "/root/closure_ABCD%s%s.root"%(ABCD, suffix))
      c1.SaveAs(savedir + "/pdf/closure_ABCD%s%s.pdf"%(ABCD, suffix))
