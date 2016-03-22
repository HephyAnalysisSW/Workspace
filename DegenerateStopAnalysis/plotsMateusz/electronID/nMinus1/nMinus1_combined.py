# nMinus1_combined.py
# Script which combines solely the N-1 efficiency plots for all types (efficiency, misID, misID2)
# Author: Mateusz Zarucki

import ROOT
import os, sys
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from array import array
from math import pi, sqrt #cos, sin, sinh, log
import argparse

filedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronID/nMinus1"

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--zoom", dest="zoom",  help="Toggle zoom", type=int, default=1)
parser.add_argument("--save", dest="save",  help="Toggle Save", type=int, default=1)
parser.add_argument("-b", dest="batch",  help="Batch Mode", action="store_true", default=False)
#parser.add_argument("--mvaWPs", dest="mvaWPs",  help="Add MVA WPs", type=int, default=0) # includes MVA WPs
#parser.add_argument("--iso", dest="iso",  help="Isolation", type=str, default="relIso03") #"relIso03" "relIso04" "miniRelIso" "relIsoAn04"
args = parser.parse_args()
#if not len(sys.argv) > 1:
#   print makeLine()
#   print "No arguments given. Using default settings."
#   print makeLine()
#   #exit()

#Arguments
#mvaWPs = args.mvaWPs # includes MVA WPs
zooms = [0, 1] #args.zoom
save = 1 #args.save

#num = "manual"
variables = ["sigmaEtaEta", "dEta", "dPhi", "hOverE", "ooEmooP", "d0", "dz", "MissingHits", "convVeto"]

#Samples
privateSignals = ["S300_240Fast", "S300_270", "S300_270Fast", "S300_290Fast", "T2tt300_270Fast"]
officialSignals = ["T2_4bd300_240", "T2_4bd300_270", "T2_4bd300_290"]
backgrounds=["WJets", "TTJets", "ZJetsInv", "QCD"]
signals = privateSignals + officialSignals
samples = signals + backgrounds

print makeLine()
print "Samples:"
newLine()
for s in samples:
   print s
print makeLine()
         
#Bin size 
#nbins = 100
xmin = 0
#xmax = 1000

for var in variables:
   for sample in samples:
      #Zoom
      for zoom in zooms:
         if not zoom:
            xmax = 150
            z = ""
            #bins = array('d', range(xmin,50,2) + range(50,100,5) + range(100,xmax+10,10)) #Variable bin size
         else:
            #nbins = 10
            xmax = 20
            z = "_zoom"
            #bins = array('d',range(xmin,xmax+2,2))
         
         WPs = ['Veto','Loose','Medium','Tight']
         
         #if mvaWPs: 
         #   WPs.append('WP90') 
         #   WPs.append('WP80')
   
         #Gets root files
         if sample == "ZJetsInv" or sample == "QCD": plots = ["misID", "misID2"]
         else: plots = ["efficiency", "misID", "misID2"]
         
         total = {"efficiency":{}, "misID":{}, "misID2":{}}
         passed = {"efficiency":{}, "misID":{}, "misID2":{}}
         
         for plot in plots: 
            numFile = ROOT.TFile(filedir + "/variables/None/" + plot + "/root/" + plot + "_" + sample + z + ".root", "read")
            denFile = ROOT.TFile(filedir + "/variables/" + var + "/no_" + var + "/" + plot + "/root/" + plot + "_no_" + var + "_" + sample + z + ".root", "read")
            
            for iWP in WPs:
                  total[plot][iWP] = denFile.Get("c1").GetPrimitive("c1_1").GetPrimitive(plot + "_passed_" + iWP) 
                  passed[plot][iWP] = numFile.Get("c1").GetPrimitive("c1_1").GetPrimitive(plot + "_passed_" + iWP) 
         
         ##################################################################################Canvas 1#############################################################################################
         c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
         c1.Divide(1,3)
         
         n1effs = {"efficiency":{}, "misID": {}, "misID2": {}}
         
         for plot in plots:
            for iWP in WPs: 
               n1effs[plot][iWP] = makeEffPlot(passed[plot][iWP], total[plot][iWP])
               n1effs[plot][iWP].SetName("n1eff_" + plot + "_" + iWP) 
         
         for i,plot in enumerate(plots):
            c1.cd(i+1)
           
            if plot == "efficiency": n1effs[plot]['Veto'].SetTitle("Efficiency: ID without %s Cut (%s Sample) ; Generated Electron p_{T} / GeV ; Efficiency"%(var, sample))
            elif plot == "misID": n1effs[plot]['Veto'].SetTitle("MisID Efficiency: ID without %s Cut (%s Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency"%(var, sample))
            elif plot == "misID2": n1effs[plot]['Veto'].SetTitle("MisID2 Efficiency: ID without %s Cut (%s Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency"%(var, sample))
            
            n1effs[plot]['Veto'].SetMarkerColor(ROOT.kGreen+3) 
            n1effs[plot]['Veto'].SetLineColor(ROOT.kGreen+3) 
            n1effs[plot]['Veto'].Draw("AP") 
            #n1effs[plot]['Veto'].GetXaxis().SetLimits(xmin,xmax) 
            #n1effs[plot]['Veto'].GetXaxis().SetTitle("Generated Electron p_{T} / GeV")
            
            setupEffPlot(n1effs[plot]['Veto'])
            
            for iWP in WPs:
               if iWP != 'Veto': n1effs[plot][iWP].Draw("sameP")  
             
            #Colours 
            n1effs[plot]['Loose'].SetMarkerColor(ROOT.kBlue+1) 
            n1effs[plot]['Loose'].SetLineColor(ROOT.kBlue+1) 
            n1effs[plot]['Medium'].SetMarkerColor(ROOT.kOrange-2) 
            n1effs[plot]['Medium'].SetLineColor(ROOT.kOrange-2) 
            n1effs[plot]['Tight'].SetMarkerColor(ROOT.kRed+1) 
            n1effs[plot]['Tight'].SetLineColor(ROOT.kRed+1) 
            
            ROOT.gPad.Modified() 
            ROOT.gPad.Update() 
            
            if plot == "efficiency" or ((sample == "ZJetsInv" or sample == "QCD") and plot == "misID"): 
               l1 = makeLegend() 
               l1.AddEntry("n1eff_efficiency_Veto", "Veto ID", "P") 
               l1.AddEntry("n1eff_efficiency_Loose", "Loose ID", "P") 
               l1.AddEntry("n1eff_efficiency_Medium", "Medium ID", "P") 
               l1.AddEntry("n1eff_efficiency_Tight", "Tight ID", "P") 
         
            ROOT.gPad.Modified()
            ROOT.gPad.Update()
            l1.Draw()
         
         ROOT.gPad.Modified()
         ROOT.gPad.Update()           
         c1.Modified()
         c1.Update()
         
         #Write to file
         if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
            savedir = filedir + "/variables/" + var + "/combined"
            
            if not os.path.exists(savedir + "/root"): os.makedirs(savedir + "/root")
            if not os.path.exists(savedir + "/pdf"): os.makedirs(savedir + "/pdf")
            
            #Save to Web
            c1.SaveAs(savedir + "/nMinus1_%s_%s%s.png"%(var, sample, z))
            c1.SaveAs(savedir + "/root/nMinus1_%s_%s%s.root"%(var, sample, z))
            c1.SaveAs(savedir + "/pdf/nMinus1_%s_%s%s.pdf"%(var, sample, z))
