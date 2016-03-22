# comparisons.py
# Script to compare electron ID efficiency plots with various ID definitions
# Author: Mateusz Zarucki

import ROOT
import os, sys
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from array import array
from math import pi, sqrt #cos, sin, sinh, log
import argparse

filedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronID/efficiencies"

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--num", dest="num",  help="Numerator ID type", type=str, default="manual") # "standard" "manual" "iso"
parser.add_argument("--den", dest="den",  help="Denominator ID type", type=str, default="standard") # "standard" "manual" "iso"
parser.add_argument("--iso", dest="iso",  help="Isolation", type=str, default="relIso03") #"relIso03" "relIso04" "miniRelIso" "relIsoAn04"
parser.add_argument("--mvaWPs", dest="mvaWPs",  help="Add MVA WPs", type=int, default=0) # includes MVA WPs
parser.add_argument("--zoom", dest="zoom",  help="Toggle zoom", type=int, default=1)
parser.add_argument("--save", dest="save",  help="Toggle Save", type=int, default=1)
parser.add_argument("-b", dest="batch",  help="Batch Mode", action="store_true", default=False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
num = args.num # "iso" | "manual"
den = args.den # "manual" | "standard"
if num == "iso" or den == "iso": isolations = ["miniRelIso", "relIso03", "relIso04"] #args.iso #relIsoAn04
else: isolations = [""]
mvaWPs = args.mvaWPs # includes MVA WPs
zooms = [0,1] #zoom
save = 1 #args.save

privateSignals = ["S300_240Fast", "S300_270", "S300_270Fast", "S300_290Fast", "T2tt300_270Fast"]
officialSignals = ["T2_4bd300_240", "T2_4bd300_270", "T2_4bd300_290"]
backgrounds=["WJets", "TTJets", "ZJetsInv", "QCD"] 
signals = privateSignals + officialSignals
samples = signals + backgrounds

#Bin size 
#nbins = 100
xmin = 0
#xmax = 1000

for sample in samples:
   for zoom in zooms:
      for isolation in isolations:
         #Zoom
         if not zoom:
            xmax = 150
            z = ""
            #bins = array('d', range(xmin,50,2) + range(50,100,5) + range(100,xmax+10,10)) #Variable bin size
         else:
            xmax = 20
            bins = array('d',range(xmin,xmax+2,2))
            z = "_zoom"

         WPs = ['Veto','Loose','Medium','Tight']
         if mvaWPs: 
            WPs.append('WP90') 
            WPs.append('WP80')

         #Gets root files
         if sample == "ZJetsInv" or sample == "QCD": plots = ["misID", "misID2"]
         else: plots = ["efficiency", "misID", "misID2"]
         
         total = {"efficiency":{}, "misID":{}, "misID2":{}}
         passed = {"efficiency":{}, "misID":{}, "misID2":{}}
         
         for plot in plots: 
            if den == "iso": denFile = ROOT.TFile(filedir + "/iso/" + isolation + "/" + plot + "/root/%s_%s_%s%s.root"%(plot, isolation, sample, z), "read")
            else: denFile = ROOT.TFile(filedir + "/" + den + "/" + plot + "/root/%s_%s_%s%s.root"%(plot, den, sample, z), "read")
            
            if num == "iso": numFile = ROOT.TFile(filedir + "/iso/" + isolation + "/" + plot + "/root/%s_%s_%s%s.root"%(plot, isolation, sample, z), "read")
            else: numFile = ROOT.TFile(filedir + "/" + num + "/" + plot + "/root/%s_%s_%s%s.root"%(plot, num, sample, z), "read")
            
            for iWP in WPs:
                  total[plot][iWP] = denFile.Get("c1").GetPrimitive("c1_1").GetPrimitive(plot + "_passed_" + iWP) 
                  passed[plot][iWP] = numFile.Get("c1").GetPrimitive("c1_1").GetPrimitive(plot + "_passed_" + iWP) 
         
         ##################################################################################Canvas 1#############################################################################################
         c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
         c1.Divide(1,3)
         
         effs = {"efficiency":{}, "misID": {}, "misID2": {}}
         
         for plot in plots:
            for iWP in WPs: 
               effs[plot][iWP] = makeEffPlot2(passed[plot][iWP],total[plot][iWP])
               effs[plot][iWP].SetName("eff_%s_%s"%(plot, iWP)) 
         
         for i,plot in enumerate(plots):
            c1.cd(i+1)
           
            if num == "iso":
               if plot == "efficiency": effs[plot]['Veto'].SetTitle("Efficiency: Comparison of " + isolation + " and " + den + " Plots (" + sample + " Sample) ; Generated Electron p_{T} / GeV ; Efficiency")
               elif plot == "misID": effs[plot]['Veto'].SetTitle("MisID Efficiency: Comparison of " + isolation + " and " + den + " Plots (" + sample + " Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency")
               elif plot == "misID2": effs[plot]['Veto'].SetTitle("MisID2 Efficiency: Comparison of " + isolation + " and " + den + " Plots (" + sample + " Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency")
            else: 
               if plot == "efficiency": effs[plot]['Veto'].SetTitle("Efficiency: Comparison of " + num + " and " + den + " Plots (" + sample + " Sample) ; Generated Electron p_{T} / GeV ; Efficiency")
               elif plot == "misID": effs[plot]['Veto'].SetTitle("MisID Efficiency: Comparison of " + num + " and " + den + " Plots (" + sample + " Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency")
               elif plot == "misID2": effs[plot]['Veto'].SetTitle("MisID2 Efficiency: Comparison of " + num + " and " + den + " Plots (" + sample + " Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency")
            
            effs[plot]['Veto'].SetMarkerColor(ROOT.kGreen+3) 
            effs[plot]['Veto'].SetLineColor(ROOT.kGreen+3) 
            effs[plot]['Veto'].Draw("P") 
            
            setupEffPlot2(effs[plot]['Veto'])
            
            #ROOT.gPad.RedrawAxis()
            #if plot == "efficiency": effs[plot]['Veto'].GetXaxis().SetTitle("Generated Electron p_{T} / GeV")
            #elif plot == "misID" or plot == "misID2": effs[plot]['Veto'].GetXaxis().SetTitle("Reconstructed Electron p_{T} / GeV")
             
            if num == "manual" and den == "standard": effs[plot]['Veto'].SetMaximum(3) 
            
            alignStats(effs[plot]['Veto'])
          
            for iWP in WPs:
               if iWP != 'Veto': effs[plot][iWP].Draw("sameP")  
             
            #Colours 
            effs[plot]['Loose'].SetMarkerColor(ROOT.kBlue+1) 
            effs[plot]['Loose'].SetLineColor(ROOT.kBlue+1) 
            effs[plot]['Medium'].SetMarkerColor(ROOT.kOrange-2) 
            effs[plot]['Medium'].SetLineColor(ROOT.kOrange-2) 
            effs[plot]['Tight'].SetMarkerColor(ROOT.kRed+1) 
            effs[plot]['Tight'].SetLineColor(ROOT.kRed+1) 
            
            ROOT.gPad.Modified() 
            ROOT.gPad.Update() 
            
            if plot == "efficiency": 
               l1 = makeLegend() 
               l1.AddEntry("eff_efficiency_Veto", "Veto ID", "P") 
               l1.AddEntry("eff_efficiency_Loose", "Loose ID", "P") 
               l1.AddEntry("eff_efficiency_Medium", "Medium ID", "P") 
               l1.AddEntry("eff_efficiency_Tight", "Tight ID", "P") 
            l1.Draw()
         
         c1.Modified()
         c1.Update()
         
         #Write to file
         if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
            if num == "iso": savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronID/efficiencies/comparisons/" + isolation + "_" + den
            elif den == "iso": savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronID/efficiencies/comparisons/" + num + "_" + isolation
            else: savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronID/efficiencies/comparisons/" + num + "_" + den
            
            if not os.path.exists(savedir + "/root"): os.makedirs(savedir + "/root")
            if not os.path.exists(savedir + "/pdf"): os.makedirs(savedir + "/pdf")
            
            #Save to Web
            if num == "iso": 
               c1.SaveAs(savedir + "/comparison_%s_%s_%s%s.png"%(isolation, den, sample, z))
               c1.SaveAs(savedir + "/pdf/comparison_%s_%s_%s%s.pdf"%(isolation, den, sample, z))
               c1.SaveAs(savedir + "/root/comparison_%s_%s_%s%s.root"%(isolation, den, sample, z))
            elif den == "iso": 
               c1.SaveAs(savedir + "/comparison_%s_%s_%s%s.png"%(num, isolation, sample, z))
               c1.SaveAs(savedir + "/pdf/comparison_%s_%s_%s%s.pdf"%(num, isolation, sample, z))
               c1.SaveAs(savedir + "/root/comparison_%s_%s_%s%s.root"%(num, isolation, sample, z))
            else: 
               c1.SaveAs(savedir + "/comparison_%s_%s_%s%s.png"%(num, den, sample, z))
               c1.SaveAs(savedir + "/pdf/comparison_%s_%s_%s%s.pdf"%(num, den, sample, z))
               c1.SaveAs(savedir + "/root/comparison_%s_%s_%s%s.root"%(num, den, sample, z))
