#METmap.py script - Map of MET Gen. Filter Reduction Factor vs Efficiency on Reco Cut

import ROOT
import os
import numpy as np
#from array import array
#import scipy

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

path = "/afs/hephy.at/user/m/mzarucki/www/plots/filter/"

#if not os.path.exists(path):
#   os.makedirs(path)

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

files = []
buffer = []
redFactor1 = []; redFactor2 = []; redFactor3 = []; redFactor4 = []
effReco1 = []; effReco2 = []; effReco3 = []; effReco4 = []
cuts = []

#Gets all file paths with filter results
for dirname in sorted(os.listdir(path)): 
   if dirname.startswith("filter"):
      print dirname
      buffer = dirname.split("_")
      filename = 'reductionEfficiency_' + buffer[1] + '_' + buffer[2]  + '.txt'
      files.append(os.path.join(path,dirname,filename))

#Extraction of data from file
for filename in files:
   infile = open(filename, 'r') #.read() #opens data file
   print "Opening: ", infile.name

   #infile.seek(offset, [from]) # offset = number of bytes to be moved | [from] ref position from where bytes to be moved

   #infile.tell() #position in file

   for line in infile:
         #print line
         line = infile.next() 
         print line
         buffer = line.split()
         cuts.append(buffer[0]) #gMET cut
         cuts.append(buffer[1]) #gISR cut
         redFactor1.append(buffer[2]) #MET 1
         effReco1.append(buffer[3]) #MET 1
         redFactor2.append(buffer[4]) #MET 2
         effReco2.append(buffer[5]) #MET 2
         redFactor3.append(buffer[6]) # ISR 1
         effReco3.append(buffer[7]) #ISR 1
         redFactor4.append(buffer[8]) #ISR 2
         effReco4.append(buffer[9]) #ISR 2
   infile.close()

#Canvas 1: MET 1
c1 = ROOT.TCanvas("c1", "MET 1")
c1.SetGrid() #adds a grid to the canvas
#c1.SetFillColor(42)
c1.GetFrame().SetFillColor(21)
c1.GetFrame().SetBorderSize(12)
 
#pad1 = TPad("pad1","",0,0,1,1) 
 
#pad1->SetTicks(0,2); //adds labels on right side
#pad1->SetFillStyle(1001);
#pad1->SetFillColor(kYellow-10); //fill colour of borders
#pad1->SetFrameFillColor(kCyan-10); //fill colour of inside box
#pad1->SetFrameFillStyle(1001);
 
#pad1->Draw();
#pad1->cd();
 
gr1 = ROOT.TGraph(len(redFactor1), np.array(redFactor1, 'float64'), np.array(effReco1, 'float64')) #graph object with error bars using arrays of data
gr1.SetTitle("MET 1: Filter Efficiency at Reco Cut (200 GeV) vs Reduction Factor")
 
gr1.SetMarkerColor(ROOT.kBlue)
gr1.SetMarkerStyle(ROOT.kFullCircle)
gr1.SetMarkerSize(1)
gr1.GetXaxis().SetTitle("Reduction Factor")
gr1.GetYaxis().SetTitle("Filter Efficiency at Reco Cut Value")
gr1.GetXaxis().CenterTitle()
gr1.GetYaxis().CenterTitle()
#gr1.GetYaxis()->SetTicks("-"); //sets x-axis ticks

for x in my_range(0, 156-13, 13):
   print x
   print cuts[2*x], cuts[2*x+1]
   latex = ROOT.TLatex(gr1.GetX()[x], gr1.GetY()[x], "(" + cuts[2*x] + "," + cuts[2*x+1] + ")")
   latex.SetTextSize(0.02)
   #latex.SetTextColor(ROOT.kRed)
   gr1.GetListOfFunctions().Add(latex)

gr1.Draw("AP") #plots the graph with axes and points
#gr1.Print() #prints data plot values to the screen
 
#c1->Update();
#pad1->Update();
 
#gr->Paint(>)

#Canvas 2: MET 2
c2 = ROOT.TCanvas("c2", "MET 2")
c2.SetGrid() #adds a grid to the canvas
#c2->SetFillColor(42);
#c2->GetFrame()->SetFillColor(21);
#c2->GetFrame()->SetBorderSize(12);

#pad2 = TPad("pad1","",0,0,1,1) 

#pad2->SetTicks(0,2); //adds labels on right side
#pad2->SetFillStyle(1001);
#pad2->SetFillColor(kYellow-10); //fill colour of borders
#pad2->SetFrameFillColor(kCyan-10); //fill colour of inside box
#pad2->SetFrameFillStyle(1001);

#pad2->Draw();
#pad2->cd();

gr2 = ROOT.TGraph(len(redFactor2), np.array(redFactor2, 'float64'), np.array(effReco2, 'float64')) #graph object with error bars using arrays of data
gr2.SetTitle("MET 2: Filter Efficiency at Reco Cut (200 GeV) vs Reduction Factor")

gr2.SetMarkerColor(ROOT.kBlue)
gr2.SetMarkerStyle(ROOT.kFullCircle)
gr2.SetMarkerSize(0.5)
gr2.GetXaxis().SetTitle("Reduction Factor")
gr2.GetYaxis().SetTitle("Filter Efficiency at Reco Cut Value")
gr2.GetXaxis().CenterTitle()
gr2.GetYaxis().CenterTitle()
#gr2.GetYaxis()->SetTicks("-"); //sets x-axis ticks

for x in my_range(0, 156-13, 13):
   print x
   print cuts[2*x], cuts[2*x+1]
   latex = ROOT.TLatex(gr2.GetX()[x], gr2.GetY()[x], "(" + cuts[2*x] + "," + cuts[2*x+1] + ")")
   latex.SetTextSize(0.02)
   #latex.SetTextColor()
   gr2.GetListOfFunctions().Add(latex)

#for x in my_range(117, 129, 1):
#   print x
#   print cuts[2*x], cuts[2*x+1]
#   latex = ROOT.TLatex(gr2.GetX()[x], gr2.GetY()[x], "(" + cuts[2*x] + "," + cuts[2*x+1] + ")")
#   latex.SetTextSize(0.01)
#   latex.SetTextColor(ROOT.kRed)
#   gr2.GetListOfFunctions().Add(latex)

gr2.Draw("AP") #plots the graph with axes and points

#Canvas 3
c3 = ROOT.TCanvas("c3", "ISR 1")
c3.SetGrid() #adds a grid to the canvas
#c3->SetFillColor(42);
#c3->GetFrame()->SetFillColor(21);
#c3->GetFrame()->SetBorderSize(12);
 
#pad3 = TPad("pad1","",0,0,1,1) 
 
#pad3->SetTicks(0,2); //adds labels on right side
#pad3->SetFillStyle(1001);
#pad3->SetFillColor(kYellow-10); //fill colour of borders
#pad3->SetFrameFillColor(kCyan-10); //fill colour of inside box
#pad3->SetFrameFillStyle(1001);
 
#pad3->Draw();
#pad3->cd();
 
gr3 = ROOT.TGraph(len(redFactor3), np.array(redFactor3, 'float64'), np.array(effReco3, 'float64')) #graph object with error bars using arrays of data
gr3.SetTitle("ISR 1: Filter Efficiency at Reco Cut (110 GeV) vs Reduction Factor")
 
gr3.SetMarkerColor(ROOT.kBlue)
gr3.SetMarkerStyle(ROOT.kFullCircle)
gr3.SetMarkerSize(0.5)
gr3.GetXaxis().SetTitle("Reduction Factor")
gr3.GetYaxis().SetTitle("Filter Efficiency at Reco Cut Value")
gr3.GetXaxis().CenterTitle()
gr3.GetYaxis().CenterTitle()
#gr3.GetYaxis()->SetTicks("-"); //sets x-axis ticks
 
for x in my_range(117, 129, 1):
   print x
   print cuts[2*x], cuts[2*x+1]
   latex = ROOT.TLatex(gr3.GetX()[x], gr3.GetY()[x], "(" + cuts[2*x] + "," + cuts[2*x+1] + ")")
   latex.SetTextSize(0.02)
   #latex.SetTextColor()
   gr3.GetListOfFunctions().Add(latex)

gr3.Draw("AP") #plots the graph with axes and points

#Canvas 4
c4 = ROOT.TCanvas("c4", "ISR 2")
c4.SetGrid() #adds a grid to the canvas
#c4->SetFillColor(42);
#c4->GetFrame()->SetFillColor(21);
#c4->GetFrame()->SetBorderSize(12);

#pad4 = TPad("pad1","",0,0,1,1) 

#pad4->SetTicks(0,2); //adds labels on right side
#pad4->SetFillStyle(1001);
#pad4->SetFillColor(kYellow-10); //fill colour of borders
#pad4->SetFrameFillColor(kCyan-10); //fill colour of inside box
#pad4->SetFrameFillStyle(1001);

#pad4->Draw();
#pad4->cd();

gr4 = ROOT.TGraph(len(redFactor4), np.array(redFactor4, 'float64'), np.array(effReco4, 'float64')) #graph object with error bars using arrays of data
gr4.SetTitle("ISR 2: Filter Efficiency at Reco Cut (110 GeV) vs Reduction Factor")

gr4.SetMarkerColor(ROOT.kBlue)
gr4.SetMarkerStyle(ROOT.kFullCircle)
gr4.SetMarkerSize(0.5)
gr4.GetXaxis().SetTitle("Reduction Factor")
gr4.GetYaxis().SetTitle("Filter Efficiency at Reco Cut Value")
gr4.GetXaxis().CenterTitle()
gr4.GetYaxis().CenterTitle()
#gr4.GetYaxis()->SetTicks("-"); //sets x-axis ticks

for x in my_range(0, 156-13, 13):
   print x
   print cuts[2*x], cuts[2*x+1]
   latex = ROOT.TLatex(gr4.GetX()[x], gr4.GetY()[x], "(" + cuts[2*x] + "," + cuts[2*x+1] + ")")
   latex.SetTextSize(0.02)
   #latex.SetTextColor()
   gr4.GetListOfFunctions().Add(latex)

for x in my_range(117, 129, 1):
   print x
   print cuts[2*x], cuts[2*x+1]
   latex = ROOT.TLatex(gr4.GetX()[x], gr4.GetY()[x], "(" + cuts[2*x] + "," + cuts[2*x+1] + ")")
   latex.SetTextSize(0.02)
   latex.SetTextColor(ROOT.kRed)
   gr4.GetListOfFunctions().Add(latex)

gr4.Draw("AP") #plots the graph with axes and points

c1.SaveAs(path + "efficiencyMaps/MET/MET1map.root")
c1.SaveAs(path + "efficiencyMaps/MET/MET1map.png")
c1.SaveAs(path + "efficiencyMaps/MET/MET1map.pdf")

c2.SaveAs(path + "efficiencyMaps/MET/MET2map.root")
c2.SaveAs(path + "efficiencyMaps/MET/MET2map.png")
c2.SaveAs(path + "efficiencyMaps/MET/MET2map.pdf")

c3.SaveAs(path + "efficiencyMaps/ISR/ISR1map.root")
c3.SaveAs(path + "efficiencyMaps/ISR/ISR1map.png")
c3.SaveAs(path + "efficiencyMaps/ISR/ISR1map.pdf")

c4.SaveAs(path + "efficiencyMaps/ISR/ISR2map.root")
c4.SaveAs(path + "efficiencyMaps/ISR/ISR2map.png")
c4.SaveAs(path + "efficiencyMaps/ISR/ISR2map.pdf")
