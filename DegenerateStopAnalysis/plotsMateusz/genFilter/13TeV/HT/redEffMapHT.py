#redEffMapHT.py script - Produces 2D map of reduction factors and efficiencies at reco, for varying genMET and genHT cuts.

print "\nExecuting redEffMapHT.py script..."

import ROOT
import os
import numpy as np

#Root options
#ROOT.gROOT.Reset() #re-initialises ROOT
#ROOT.gROOT.SetStyle("Default") #Plain = sets empty TStyle

#ROOT.gStyle.SetOptStat(1) #prints statistics on plots
#ROOT.gStyle.SetOptFit(0) #gStyle->SetOptFit(1111); //prints fit results of plot
#ROOT.gStyle.SetTitleX(0.15) #sets x-coord of title
#gStyle->SetFuncWidth(1) #sets width of fit line
#gStyle->SetFuncColor(9) #sets colours of fit line
#gStyle->SetLineWidth(2)
#gStyle->SetOptTitle(0) #suppresses title box

#ROOT.gStyle.SetCanvasBorderMode(0);
#ROOT.gStyle.SetPadBorderMode(0);
#ROOT.gStyle.SetPadColor(0);
#ROOT.gStyle.SetCanvasColor(0);
#ROOT.gStyle.SetTitleColor(0);
#ROOT.gStyle.SetStatColor(0);

dir = "/afs/hephy.at/user/m/mzarucki/www/plots/filter/13TeV/HT/alphaTdef/genJetPt30/eta3/"

files = []
buffer = []
redFactor1 = []; redFactor2 = []; redFactor3 = []; redFactor4 = []
effReco1 = []; effReco2 = []; effReco3 = []; effReco4 = []
cutsMET = []; cutsISR = []

#Gets all file paths with filter results
for dirname in sorted(os.listdir(dir + "turnons")): 
   if dirname.startswith("filter"):
      #print dirname
      buffer = dirname.split("_")
      filename = 'reductionEfficiency_' + buffer[1] + '_' + buffer[2]  + '.txt'
      files.append(os.path.join(dir + "turnons", dirname, filename))

#Extraction of data from file
for filename in files:
   infile = open(filename, 'r') #.read() #opens data file
   print "Opening: ", infile.name

   for line in infile:
         #print line
         line = infile.next() 
         #print line
         buffer = line.split()
         cutsMET.append(buffer[0]) #gMET cut
         cutsISR.append(buffer[1]) #gISR cut
         redFactor1.append(buffer[2]) #MET 1
         effReco1.append(buffer[3]) #MET 1
         redFactor2.append(buffer[4]) #MET 2
         effReco2.append(buffer[5]) #MET 2
         redFactor3.append(buffer[6]) # ISR 1
         effReco3.append(buffer[7]) #ISR 1
         redFactor4.append(buffer[8]) #ISR 2
         effReco4.append(buffer[9]) #ISR 2
   infile.close()

#Canvas 1
c1 = ROOT.TCanvas("c1", "Generator Cut Optimisation")

gr1 = ROOT.TGraph2D(len(effReco2), np.array(cutsMET, 'float64'), np.array(cutsISR, 'float64'), np.array(redFactor2, 'float64')) #graph object with error bars using arrays of data
gr1.SetTitle("Total Reduction Factor")
gr1.GetHistogram()
gr1.GetXaxis().SetTitle("genMET Cut / GeV")
gr1.GetYaxis().SetTitle("genHT Cut / GeV")
gr1.GetZaxis().SetTitle("Reduction Factor")
gr1.GetXaxis().SetTitleOffset(1.2)
gr1.GetYaxis().SetTitleOffset(1.2)
gr1.GetZaxis().SetTitleOffset(1.2)
gr1.GetXaxis().CenterTitle()
gr1.GetYaxis().CenterTitle()
gr1.GetZaxis().CenterTitle()

ROOT.gStyle.SetPalette(1) #55
gr1.Draw("COLZ") #CONT1-5 #plots the graph with axes and points
#gr1.SetMaximum(1.0)
#gr1.SetMinimum(0.9)
gr1.GetZaxis().SetRangeUser(2, 5)
gr1.GetXaxis().SetRangeUser(0, 110)
gr1.GetYaxis().SetRangeUser(140, 200)
#gr1.GetZaxis().SetNdivisions(520)

c1.Update()

#Canvas 2
c2 = ROOT.TCanvas("c2", "Generator Cut Optimisation")

#totalReduction
gr2 = ROOT.TGraph2D(len(effReco2), np.array(cutsMET, 'float64'), np.array(cutsISR, 'float64'), np.array(effReco2, 'float64')) #graph object with error bars using arrays of data
gr2.SetTitle("Generated MET Filter Efficiency at Reco Cut Value")
 
gr2.GetHistogram()
gr2.GetXaxis().SetTitle("genMET Cut / GeV")
gr2.GetYaxis().SetTitle("genHT Cut / GeV")
gr2.GetZaxis().SetTitle("Efficiency at Reco Cut")
gr2.GetXaxis().SetTitleOffset(1.2)
gr2.GetYaxis().SetTitleOffset(1.2)
gr2.GetZaxis().SetTitleOffset(1.2)
gr2.GetXaxis().CenterTitle()
gr2.GetYaxis().CenterTitle()
gr2.GetZaxis().CenterTitle()

#ROOT.gStyle.SetPalette(55) #55
gr2.Draw("COLZ") #CONT1-5 #plots the graph with axes and points #try opt. 0 (for min/max bins)
#gr2.SetMaximum(4)
#gr2.SetMinimum(6)
#gr2.GetZaxis().SetRangeUser(0.9, 1)
gr2.GetXaxis().SetRangeUser(0, 110)
gr2.GetYaxis().SetRangeUser(140, 200)

c2.Update()
#pad1->Update();

#Canvas 3
c3 = ROOT.TCanvas("c3", "Generator Cut Optimisation")

gr3 = ROOT.TGraph2D(len(effReco2), np.array(cutsMET, 'float64'), np.array(cutsISR, 'float64'), np.array(effReco4, 'float64')) #graph object with error bars using arrays of data
gr3.SetTitle("Generated HT Filter Efficiency at Reco Cut Value")
 
gr3.GetHistogram()
gr3.GetXaxis().SetTitle("genMET Cut / GeV")
gr3.GetYaxis().SetTitle("genHT Cut / GeV")
gr3.GetZaxis().SetTitle("Efficiency at Reco Cut")
gr3.GetXaxis().SetTitleOffset(1.2)
gr3.GetYaxis().SetTitleOffset(1.2)
gr3.GetZaxis().SetTitleOffset(1.2)
gr3.GetXaxis().CenterTitle()
gr3.GetYaxis().CenterTitle()
gr3.GetZaxis().CenterTitle()

#ROOT.gStyle.SetPalette(55) #55
gr3.Draw("COLZ") #CONT1-5 #plots the graph with axes and points #try opt. 0 (for min/max bins)
#gr3.SetMaximum(4)
#gr3.SetMinimum(6)
#gr3.GetZaxis().SetRangeUser(0.9, 1)
gr3.GetXaxis().SetRangeUser(0, 110)
gr3.GetYaxis().SetRangeUser(140, 200)

c3.Update()

#Save to Web
savedir = dir + "reductionEfficiency/"

if not os.path.exists(savedir):
      os.makedirs(savedir)

c1.SaveAs(savedir + "redEffMap_1.root")
c1.SaveAs(savedir + "redEffMap_1.png")
c1.SaveAs(savedir + "redEffMap_1.pdf")

c2.SaveAs(savedir + "redEffMap_2.root")
c2.SaveAs(savedir + "redEffMap_2.png")
c2.SaveAs(savedir + "redEffMap_2.pdf")

c3.SaveAs(savedir + "redEffMap_3.root")
c3.SaveAs(savedir + "redEffMap_3.png")
c3.SaveAs(savedir + "redEffMap_3.pdf")
