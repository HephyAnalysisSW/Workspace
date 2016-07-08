# nMinus1_full.py
# Script to create N-1 plots for a given type of efficiency plot (efficiency, misID, misID2)
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
signals = privateSignals# + officialSignals
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
      for zoom in zooms:
         if not zoom:
            xmax = 150
            z = ""
            #bins = array('d', range(xmin,50,2) + range(50,100,5) + range(100,xmax+10,10)) #Variable bin size
         else:
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
         
         passed_den = {"efficiency":{}, "misID":{}, "misID2":{}}
         passed_num = {"efficiency":{}, "misID":{}, "misID2":{}}
         noID = {"efficiency":{}, "misID":{}, "misID2":{}}
         
         effs_num = {"efficiency":{}, "misID": {}, "misID2": {}}
         effs_den = {"efficiency":{}, "misID": {}, "misID2": {}}
         n1effs = {"efficiency":{}, "misID": {}, "misID2": {}}
         diffs = {"efficiency":{}, "misID": {}, "misID2": {}}
         
         total_den = {"efficiency":{}, "misID":{}, "misID2":{}}
         total_num = {"efficiency":{}, "misID":{}, "misID2":{}}
         diffs_num = {"efficiency":{}, "misID": {}, "misID2": {}}
         diffs_den = {"efficiency":{}, "misID": {}, "misID2": {}}
         
         for plot in plots:
            numFilePath = filedir + "/variables/None/" + plot + "/root/histograms/histos_" + plot + "_no_None" + "_"  + sample + z + ".root"
            denFilePath = filedir + "/variables/" + var + "/no_" + var + "/" + plot + "/root/histograms/histos_" + plot + "_no_" + var + "_"  + sample + z + ".root"
            numFile = ROOT.TFile(numFilePath, "read")
            denFile = ROOT.TFile(denFilePath, "read")
            
            print makeLine()
            print "Sample: ", sample, " | Plot: ", plot
            print makeLine()
            print "Histograms in numFile " + numFilePath + ":\n"
            numFile.GetListOfKeys().Print()
            print makeLine()
            print "Histograms in denFile " + denFilePath + ":\n"
            denFile.GetListOfKeys().Print()
            print makeLine()

            noID[plot]['None'] = numFile.Get("%s_total_noID"%(plot))
            
            for iWP in WPs:
               passed_den[plot][iWP] = denFile.Get("%s_passed_%s"%(plot, iWP)) 
               passed_num[plot][iWP] = numFile.Get("%s_passed_%s"%(plot, iWP)) 
               total_den[plot][iWP] = denFile.Get("%s_total_%s"%(plot, iWP)) 
               total_num[plot][iWP] = numFile.Get("%s_total_%s"%(plot, iWP)) 
               
               effs_num[plot][iWP] = makeEffPlot(passed_num[plot][iWP], noID[plot]['None'])
               effs_num[plot][iWP].SetName("eff_num_%s_%s"%(plot, iWP)) 
               effs_den[plot][iWP] = makeEffPlot(passed_den[plot][iWP], noID[plot]['None'])
               effs_den[plot][iWP].SetName("eff_den_%s_%s"%(plot, iWP)) 
               n1effs[plot][iWP] = makeEffPlot(passed_num[plot][iWP], passed_den[plot][iWP])
               n1effs[plot][iWP].SetName("n1eff_%s_%s"%(plot, iWP)) 
               
               if plot == "efficiency" or plot == "misID2": 
                  diffs[plot][iWP] = makeEffPlot(passed_den[plot][iWP] - passed_num[plot][iWP], noID[plot]['None'])
                  #passed_den[plot][iWP].Divide(noID[plot]['None'])
                  #passed_num[plot][iWP].Divide(noID[plot]['None']) 
                  #diffs[plot][iWP] = passed_den[plot][iWP] - passed_num[plot][iWP]
               elif plot == "misID": 
                  diffs_num[plot][iWP] = (passed_den[plot][iWP]*total_num[plot][iWP]) - (passed_num[plot][iWP]*total_den[plot][iWP])
                  diffs_den[plot][iWP] = total_den[plot][iWP]*total_num[plot][iWP]
                  diffs[plot][iWP] = makeEffPlot(diffs_num[plot][iWP], diffs_den[plot][iWP])
                  #passed_den[plot][iWP].Divide(total_den[plot][iWP])
                  #passed_num[plot][iWP].Divide(total_num[plot][iWP]) 
                  #diffs[plot][iWP] = passed_den[plot][iWP] - passed_num[plot][iWP]
               diffs[plot][iWP].SetName("diff_" + plot + "_" + iWP) 
            
            ##################################################################################Canvas 1#############################################################################################
            c1 = ROOT.TCanvas("c1", "Canvas 1", 1400, 1500)
            c1.Divide(1,4)
 
            c1.cd(1)
            if plot == "efficiency": effs_num[plot]['Veto'].SetTitle("Efficiency: Standard Electron ID (%s Sample) ; Generated Electron p_{T} / GeV ; Efficiency"%(sample))
            elif plot == "misID": effs_num[plot]['Veto'].SetTitle("MisID: Standard Electron ID (%s Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency"%(sample))
            elif plot == "misID2": effs_num[plot]['Veto'].SetTitle("MisID2: Standard Electron ID (%s Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency"%(sample))
 
            effs_num[plot]['Veto'].SetMarkerColor(ROOT.kGreen+3) 
            effs_num[plot]['Veto'].SetLineColor(ROOT.kGreen+3) 
            effs_num[plot]['Veto'].Draw("AP")
            
            setupEffPlot(effs_num[plot]['Veto'])
            
            effs_num[plot]['Veto'].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax) #SetRangeUser(xmin,xmax)#
            
            for iWP in WPs:
               if iWP != 'Veto': effs_num[plot][iWP].Draw("sameP")  
             
            #Colours 
            effs_num[plot]['Loose'].SetMarkerColor(ROOT.kBlue+1) 
            effs_num[plot]['Loose'].SetLineColor(ROOT.kBlue+1) 
            effs_num[plot]['Medium'].SetMarkerColor(ROOT.kOrange-2) 
            effs_num[plot]['Medium'].SetLineColor(ROOT.kOrange-2) 
            effs_num[plot]['Tight'].SetMarkerColor(ROOT.kRed+1) 
            effs_num[plot]['Tight'].SetLineColor(ROOT.kRed+1) 
            
            ROOT.gPad.Modified() 
            ROOT.gPad.Update() 
            
            if plot == "efficiency" or ((plot == "misID" or plot == "misID2") and (sample == "ZJetsInv" or sample == "QCD")): #create once
               l1 = makeLegend()
               l1.AddEntry("eff_num_efficiency_Veto", "Veto ID", "P")
               l1.AddEntry("eff_num_efficiency_Loose", "Loose ID", "P")
               l1.AddEntry("eff_num_efficiency_Medium", "Medium ID", "P")
               l1.AddEntry("eff_num_efficiency_Tight", "Tight ID", "P")

            ROOT.gPad.Modified()
            ROOT.gPad.Update()
            l1.Draw()
            
            c1.cd(2)
            
            if plot == "efficiency": effs_den[plot]['Veto'].SetTitle("Efficiency: Electron ID without %s Cut (%s Sample) ; Generated Electron p_{T} / GeV ; Efficiency"%(var, sample))
            elif plot == "misID": effs_den[plot]['Veto'].SetTitle("MisID: Electron ID without %s Cut (%s Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency"%(var, sample))
            elif plot == "misID2": effs_den[plot]['Veto'].SetTitle("MisID2: Electron ID without %s Cut (%s Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency"%(var, sample))
 
            effs_den[plot]['Veto'].SetMarkerColor(ROOT.kGreen+3) 
            effs_den[plot]['Veto'].SetLineColor(ROOT.kGreen+3) 
            effs_den[plot]['Veto'].Draw("AP") 
            
            setupEffPlot(effs_den[plot]['Veto'])
            
            effs_den[plot]['Veto'].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax) 
            
            for iWP in WPs:
               if iWP != 'Veto': effs_den[plot][iWP].Draw("sameP")  
             
            #Colours 
            effs_den[plot]['Loose'].SetMarkerColor(ROOT.kBlue+1) 
            effs_den[plot]['Loose'].SetLineColor(ROOT.kBlue+1) 
            effs_den[plot]['Medium'].SetMarkerColor(ROOT.kOrange-2) 
            effs_den[plot]['Medium'].SetLineColor(ROOT.kOrange-2) 
            effs_den[plot]['Tight'].SetMarkerColor(ROOT.kRed+1) 
            effs_den[plot]['Tight'].SetLineColor(ROOT.kRed+1) 
            
            ROOT.gPad.Modified() 
            ROOT.gPad.Update() 
            
            l1.Draw()

            c1.cd(3)
             
            if plot == "efficiency": n1effs[plot]['Veto'].SetTitle("Efficiency: N-1 Plot (Ratio): %s (%s Sample) ; Generated Electron p_{T} / GeV ; Efficiency"%(var, sample))
            elif plot == "misID": n1effs[plot]['Veto'].SetTitle("MisID: N-1 Plot (Ratio): %s (%s Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency"%(var, sample))
            elif plot == "misID2": n1effs[plot]['Veto'].SetTitle("MisID2: N-1 Plot (Ratio): %s (%s Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency"%(var, sample))
            
            n1effs[plot]['Veto'].SetMarkerColor(ROOT.kGreen+3) 
            n1effs[plot]['Veto'].SetLineColor(ROOT.kGreen+3) 
            n1effs[plot]['Veto'].Draw("AP") 
            
            setupEffPlot(n1effs[plot]['Veto'])
            
            n1effs[plot]['Veto'].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax) 
            
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
            
            l1.Draw()
            
            c1.cd(4)
            if plot == "efficiency": diffs[plot]['Veto'].SetTitle("Efficiency: N-1 Plot (Difference): %s (%s Sample) ; Generated Electron p_{T} / GeV ; Efficiency"%(var, sample))
            elif plot == "misID": diffs[plot]['Veto'].SetTitle("MisID: N-1 Plot (Difference): %s (%s Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency"%(var, sample))
            elif plot == "misID2": diffs[plot]['Veto'].SetTitle("MisID2: N-1 Plot (Difference): %s (%s Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency"%(var, sample))
            
            diffs[plot]['Veto'].SetMarkerColor(ROOT.kGreen+3) 
            diffs[plot]['Veto'].SetLineColor(ROOT.kGreen+3) 
            diffs[plot]['Veto'].Draw("AP") 
            
            setupEffPlot(diffs[plot]['Veto'])
            
            diffs[plot]['Veto'].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)
            
            for iWP in WPs:
               if iWP != 'Veto': diffs[plot][iWP].Draw("sameP")  
             
            #Colours 
            diffs[plot]['Loose'].SetMarkerColor(ROOT.kBlue+1) 
            diffs[plot]['Loose'].SetLineColor(ROOT.kBlue+1) 
            diffs[plot]['Medium'].SetMarkerColor(ROOT.kOrange-2) 
            diffs[plot]['Medium'].SetLineColor(ROOT.kOrange-2) 
            diffs[plot]['Tight'].SetMarkerColor(ROOT.kRed+1) 
            diffs[plot]['Tight'].SetLineColor(ROOT.kRed+1) 
            
            ROOT.gPad.Modified() 
            ROOT.gPad.Update() 
            
            l1.Draw()
         
            ROOT.gPad.Modified()
            ROOT.gPad.Update()           
            c1.Modified()
            c1.Update()
            
            #Write to file
            if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
               savedir = filedir + "/variables/" + var + "/full/" + plot
               
               if not os.path.exists(savedir + "/root"): os.makedirs(savedir + "/root")
               if not os.path.exists(savedir + "/pdf"): os.makedirs(savedir + "/pdf")
               
               #Save to Web
               c1.SaveAs(savedir + "/nMinus1_%s_%s_%s%s.png"%(plot, var, sample,z))
               c1.SaveAs(savedir + "/root/nMinus1_%s_%s_%s%s.root"%(plot, var, sample,z))
               c1.SaveAs(savedir + "/pdf/nMinus1_%s_%s_%s%s.pdf"%(plot, var, sample,z))
