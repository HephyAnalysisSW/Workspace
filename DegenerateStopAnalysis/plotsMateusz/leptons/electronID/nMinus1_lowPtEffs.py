# nMinus1_lowPtEffs.py
# Script which calculates the total N-1 efficiencies for a low pT bin (6-10 GeV), showing N-1 efficiencies for all electron ID variables (note: misID and misID2 should be the same)
# Author: Mateusz Zarucki
  
import ROOT
import os, sys
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.tools.degTools import makeDir
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from array import array
from math import pi, sqrt #cos, sin, sinh, log
import argparse

#Input options
parser = argparse.ArgumentParser(description="Input options")
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
save = args.save

tag = "8012_mAODv2_v3/80X_postProcessing_v10"
filedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/electronID/nMinus1/histogramCounts"%tag
   
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/electronID/nMinus1/lowPtEffs"%tag

   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

dummy = []

#signals = ["S300_240Fast", "S300_270Fast", "S300_290Fast", "S300_270", "T2tt300_270Fast"]
backgrounds = ["TTJets", "WJets"]#, "QCD", "ZJets"]
allSamples = backgrounds #signals + 

passedCounts = {"None":{}, "sigmaEtaEta":{}, "dEta":{}, "dPhi":{}, "hOverE":{}, "ooEmooP":{}, "d0":{}, "dz":{}, "MissingHits":{}, "convVeto":{}}
totalCounts = {"None":{}, "sigmaEtaEta":{}, "dEta":{}, "dPhi":{}, "hOverE":{}, "ooEmooP":{}, "d0":{}, "dz":{}, "MissingHits":{}, "convVeto":{}}
variables = ["sigmaEtaEta", "dEta", "dPhi", "hOverE", "ooEmooP", "d0", "dz", "MissingHits", "convVeto"]

##Gets all file paths
#for dirname in sorted(os.listdir(path)): 
#   if dirname.startswith("histogramCounts"):
#      print dirname
#      dummy = dirname.split("_")
#      filename = 'histogramCounts_' + dummy[1] + '_' + dummy[2]  + '.txt'
#      files.append(os.path.join(path,dirname,filename))

#sample = "S300_270Fast"
for sample in allSamples:
   c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
   c1.Divide(1,3)

   plots = ["efficiency", "misID", "misID2"]
   graphs = {'efficiency':{}, 'misID':{}, 'misID2':{}}
   WPs = ['Veto', 'Loose', 'Medium', 'Tight']
      
   for i,plot in enumerate(plots):
      c1.cd(i+1) 
   
      #Extraction of data from file
      infile = open(filedir + "/" + plot + "/lowPt/histogramCounts_lowPt_%s_%s.txt"%(plot, sample), 'r') #.read() #opens data file
      print makeLine()
      print "Opening: ", infile.name
      print makeLine()
      
      for j,line in enumerate(infile):
         if j == 0:
            line = infile.next() 
            line = infile.next() 
         #print line
         dummy = line.split()
         if plot == "efficiency" or plot == "misID2":
            totalCounts[dummy[0]]['Total'] = int(float(dummy[1]))
            passedCounts[dummy[0]]['Veto'] = int(float(dummy[2]))
            passedCounts[dummy[0]]['Loose'] = int(float(dummy[3]))
            passedCounts[dummy[0]]['Medium'] = int(float(dummy[4]))
            passedCounts[dummy[0]]['Tight'] = int(float(dummy[5]))
         elif plot == "misID":
            totalCounts[dummy[0]]['Veto'] = int(float(dummy[1]))
            totalCounts[dummy[0]]['Loose'] = int(float(dummy[2]))
            totalCounts[dummy[0]]['Medium'] = int(float(dummy[3]))
            totalCounts[dummy[0]]['Tight'] = int(float(dummy[4]))
            passedCounts[dummy[0]]['Veto'] = int(float(dummy[5]))
            passedCounts[dummy[0]]['Loose'] = int(float(dummy[6]))
            passedCounts[dummy[0]]['Medium'] = int(float(dummy[7]))
            passedCounts[dummy[0]]['Tight'] = int(float(dummy[8]))
   
      infile.close()
 
      for j,iWP in enumerate(WPs):
         graphs[plot][iWP] = emptyHist("", len(variables), 0, len(variables))
         graphs[plot][iWP].SetName("n1eff_%s_%s"%(plot, iWP))
        
         if plot == "efficiency": graphs[plot]['Veto'].SetTitle("N-1 Efficiencies of Electron ID Variables in 6-10 GeV Electron p_{T} Region (%s Sample)"%(sample))
         elif plot == "misID": graphs[plot]['Veto'].SetTitle("MisID: N-1 Efficiencies of Electron ID Variables in 6-10 GeV Electron p_{T} Region (%s Sample)"%(sample))
         elif plot == "misID2": graphs[plot]['Veto'].SetTitle("MisID2: N-1 Efficiencies of Electron ID Variables in 6-10 GeV Electron p_{T} Region (%s Sample)"%(sample))
         
         for k,var in enumerate(variables):
            graphs[plot][iWP].SetBinContent(k+1, float(passedCounts['None'][iWP])/float(passedCounts[var][iWP]))
            graphs[plot][iWP].GetXaxis().SetBinLabel(k+1, var)
            graphs[plot][iWP].SetMarkerSize(2)
         
         if j == 0: graphs[plot][iWP].Draw("P")
         else: graphs[plot][iWP].Draw("sameP")
      
      ROOT.gPad.Modified()
      ROOT.gPad.Update()
      
      graphs[plot]['Veto'].GetYaxis().SetTitle("Cut Efficiency")
      graphs[plot]['Veto'].GetYaxis().SetRangeUser(0.35,1.1)
      
      graphs[plot]['Veto'].SetMarkerStyle(33)
      graphs[plot]['Veto'].SetMarkerColor(ROOT.kGreen+3)
      graphs[plot]['Veto'].SetLineColor(ROOT.kGreen+3)
      graphs[plot]['Loose'].SetMarkerStyle(20)
      graphs[plot]['Loose'].SetMarkerColor(ROOT.kBlue+1)
      graphs[plot]['Loose'].SetLineColor(ROOT.kBlue+1)
      graphs[plot]['Medium'].SetMarkerStyle(21)
      graphs[plot]['Medium'].SetMarkerColor(ROOT.kOrange-2)
      graphs[plot]['Medium'].SetLineColor(ROOT.kOrange-2)
      graphs[plot]['Tight'].SetMarkerStyle(22)
      graphs[plot]['Tight'].SetMarkerColor(ROOT.kRed+1)
      graphs[plot]['Tight'].SetLineColor(ROOT.kRed+1)
      
      if i == 0: 
         l1 = makeLegend2()
         l1.AddEntry("n1eff_" + plot + "_Veto", "Veto ID", "P")
         l1.AddEntry("n1eff_" + plot + "_Loose", "Loose ID", "P")
         l1.AddEntry("n1eff_" + plot + "_Medium", "Medium ID", "P")
         l1.AddEntry("n1eff_" + plot + "_Tight", "Tight ID", "P")
      l1.Draw()

      ROOT.gPad.Modified()
      ROOT.gPad.Update()

      alignLegend(l1) 
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   c1.Modified()
   c1.Update()
   
   #Save
   if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
      c1.SaveAs(savedir + "/nMinus1_lowPtEffs_%s.png"%(sample))
      c1.SaveAs(savedir + "/root/nMinus1_lowPtEffs_%s.root"%(sample))
      c1.SaveAs(savedir + "/pdf/nMinus1_lowPtEffs_%s.pdf"%(sample))
