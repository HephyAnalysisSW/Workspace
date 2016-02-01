#nMinus1.py
import ROOT
import os, sys
from Workspace.HEPHYPythonTools.helpers import getChunks, getChain#, getPlotFromChain, getYieldFromChain
#from Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_7412pass2 import * #data_path = "/data/nrad/cmgTuples/RunII/7412pass2_v4/RunIISpring15xminiAODv2"
from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_PP_mAODv2_7412pass2 import * #MC_path = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_v4_012016_v2/RunIISpring15DR74_25ns" SIGNAL_path = "/afs/hephy.at/dat
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from array import array
from math import pi, sqrt #cos, sin, sinh, log
from optparse import OptionParser

filedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronID/nMinus1"

#Arguments
parser = OptionParser()
parser.add_option("--zoom", dest="zoom",  help="Toggle zoom", type="int", default=1)
parser.add_option("--save", dest="save",  help="Toggle save", type="int", default=1)
#parser.add_option("--mvaWPs", dest="mvaWPs",  help="Add MVA WPs", type="int", default=0) # includes MVA WPs
#parser.add_option("-b", dest="batch",  help="batch", action="store_true", default=False)
(options, args) = parser.parse_args()

#Input options
#mvaWPs = options.mvaWPs # includes MVA WPs
zooms = [0,1] #zoom
save = 1 #options.save

num = "allCuts"
dens = ["sigmaEtaEta", "dEta", "dPhi", "hOverE", "ooEmooP", "d0", "dz", "MissingHits", "convVeto"]

#ROOT Options
ROOT.gROOT.Reset() #re-initialises ROOT
#ROOT.gROOT.SetStyle("Plain")

ROOT.gStyle.SetOptStat(1111) #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis
ROOT.gStyle.SetOptFit(1111) #1111 prints fits results on plot
#ROOT.gStyle.SetOptTitle(0) #suppresses title box
#ROOT.gStyle.SetFuncWidth(1)
#ROOT.gStyle.SetFuncColor(9)
#ROOT.gStyle.SetLineWidth(2)

ROOT.gStyle.SetPaintTextFormat("4.2f")
#ROOT.gStyle.SetTitleX(0.5) 
#ROOT.gStyle.SetTitleAlign(23)
#ROOT.gStyle.SetTitleW(0.8)

ROOT.gStyle.SetStatX(0.75)
ROOT.gStyle.SetStatY(0.65)
ROOT.gStyle.SetStatW(0.1)
ROOT.gStyle.SetStatH(0.15)

#Samples
signals = ["S300_240FS", "S300_270FS", "S300_290FS", "S300_270", "T2tt300_270FS"]
backgrounds = ["TTJets", "WJets", "QCD", "ZJets"]
allSamples = signals + backgrounds

print makeLine()
print "Samples:"
newLine()
for s in allSamples:
   print s
print makeLine()
         
#Bin size 
#nbins = 100
xmin = 0
#xmax = 1000

for den in dens:
   for sample in allSamples:
      #Zoom
      for zoom in zooms:
         if zoom == 0:
            if sample in signals:
               xmax = 150
            elif sample in backgrounds:
               xmax = 500
            else:
               print makeLine()
               print "!!! Sample " + sample + " unavailable."
               print makeLine()
               sys.exit(0)

            #bins = array('d', range(xmin,50,2) + range(50,100,5) + range(100,xmax+10,10)) #Variable bin size
            #normFactor = "((" + var + " < 50)*0.5 + (" + var + " >= 50 &&" + var + " < 100)*0.2 + (" + var + " >= 100)*0.1)"
            z = ""
         
         elif zoom == 1:
            #nbins = 10
            xmax = 50
            bins = array('d',range(xmin,xmax+2,2))
            z = "_lowPt"
         
         #Selection criteria
         #intLum = 10.0 #fb-1
         ##weight = "(xsec*" + str(intLum) + "*(10^3)/" + str(getChunks(sample)[1]) + ")" #xsec in pb
         #weight = samples[sampleKey].weight
         
         WPs = ['Veto','Loose','Medium','Tight']
         #if mvaWPs == 1: 
         #   WPs.append('WP90') 
         #   WPs.append('WP80')
   
         #Gets root files
         if sample == "ZJets" or sample == "QCD": plots = ["misID", "misID2"]
         else: plots = ["efficiency", "misID", "misID2"]
         
         total = {"efficiency":{}, "misID":{}, "misID2":{}}
         passed = {"efficiency":{}, "misID":{}, "misID2":{}}
         
         for plot in plots: 
            numFile = ROOT.TFile(filedir + "/relEff/" + num + "/" + plot + "/root/" + plot + "_" + sample + z + ".root", "read")
            denFile = ROOT.TFile(filedir + "/relEff/no_" + den + "/" + plot + "/root/" + plot + "_no_" + den + "_" + sample + z + ".root", "read")
            
            for WP in WPs:
               if plot == "efficiency":
                  total[plot][WP] = denFile.Get("c1").GetPrimitive("c1_1").GetPrimitive("eleID_" + WP) 
                  passed[plot][WP] = numFile.Get("c1").GetPrimitive("c1_1").GetPrimitive("eleID_" + WP) 
               else:
                  total[plot][WP] = denFile.Get("c1").GetPrimitive("c1_1").GetPrimitive(plot + "_" + WP) 
                  passed[plot][WP] = numFile.Get("c1").GetPrimitive("c1_1").GetPrimitive(plot + "_" + WP) 
         
         ##################################################################################Canvas 1#############################################################################################
         c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
         c1.Divide(1,3)
         
         effs = {"efficiency":{}, "misID": {}, "misID2": {}}
         
         for plot in plots:
            for WP in WPs: 
               effs[plot][WP] = passed[plot][WP]
               effs[plot][WP].Divide(total[plot][WP])
               effs[plot][WP].SetName("eff_" + plot + "_" + WP) 
               effs[plot][WP].SetMarkerStyle(33) 
               effs[plot][WP].SetMarkerSize(1.5) 
               effs[plot][WP].SetLineWidth(2) 
         
         for i,plot in enumerate(plots):
            c1.cd(i+1)
           
            if plot == "efficiency": effs[plot]['Veto'].SetTitle("Efficiency: ID without " + den + " Cut (" + sample + " Sample) ; Generated Electron p_{T} / GeV ; Efficiency")
            elif plot == "misID": effs[plot]['Veto'].SetTitle("MisID Efficiency: ID without " + den + " Cut (" + sample + " Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency")
            elif plot == "misID2": effs[plot]['Veto'].SetTitle("MisID2 Efficiency: ID without " + den + " Cut (" + sample + " Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency")
            
            effs[plot]['Veto'].SetMarkerColor(ROOT.kGreen+3) 
            effs[plot]['Veto'].SetLineColor(ROOT.kGreen+3) 
            effs[plot]['Veto'].Draw("P") 
            ROOT.gPad.SetGridx() 
            ROOT.gPad.SetGridy() 
            #ROOT.gPad.RedrawAxis()
            ROOT.gPad.Modified() 
            ROOT.gPad.Update() 
            #effs[plot]['Veto'].GetXaxis().SetLimits(xmin,xmax) 
            #effs[plot]['Veto'].GetYaxis().SetTitle("Efficiency")
            #effs[plot]['Veto'].GetXaxis().SetTitle("Generated Electron p_{T} / GeV")
            effs[plot]['Veto'].SetMinimum(0) 
            effs[plot]['Veto'].SetMaximum(1) 
            
            effs[plot]['Veto'].GetXaxis().CenterTitle() 
            effs[plot]['Veto'].GetYaxis().CenterTitle() 
            
            alignStats(effs[plot]['Veto'])
          
            for WP in WPs:
               if WP != 'Veto': effs[plot][WP].Draw("sameP")  
             
            #Colours 
            effs[plot]['Loose'].SetMarkerColor(ROOT.kBlue+1) 
            effs[plot]['Loose'].SetLineColor(ROOT.kBlue+1) 
            effs[plot]['Medium'].SetMarkerColor(ROOT.kOrange-2) 
            effs[plot]['Medium'].SetLineColor(ROOT.kOrange-2) 
            effs[plot]['Tight'].SetMarkerColor(ROOT.kRed+1) 
            effs[plot]['Tight'].SetLineColor(ROOT.kRed+1) 
            
            ROOT.gPad.Modified() 
            ROOT.gPad.Update() 
            
            if plot == "efficiency" or ((sample == "ZJets" or sample == "QCD") and plot == "misID"): 
               l1 = makeLegend() 
               l1.AddEntry("eff_efficiency_Veto", "Veto ID", "P") 
               l1.AddEntry("eff_efficiency_Loose", "Loose ID", "P") 
               l1.AddEntry("eff_efficiency_Medium", "Medium ID", "P") 
               l1.AddEntry("eff_efficiency_Tight", "Tight ID", "P") 
            l1.Draw()
         
         ROOT.gPad.Modified()
         ROOT.gPad.Update()
         c1.Modified()
         c1.Update()
         
         #Write to file
         if save == 1: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
            savedir = filedir + "/absEff/" + den
            
            if not os.path.exists(savedir):
               os.makedirs(savedir)
            if not os.path.exists(savedir + "/root"):
               os.makedirs(savedir + "/root")
            if not os.path.exists(savedir + "/pdf"):
               os.makedirs(savedir + "/pdf")
            
            #Save to Web
            c1.SaveAs(savedir + "/nMinus1_" + den + "_" + sample + z + ".png")
            c1.SaveAs(savedir + "/root/nMinus1_" + den + "_" + sample + z + ".root")
            c1.SaveAs(savedir + "/pdf/nMinus1_" + den + "_" + sample + z + ".pdf")
