#totalReduction.py script 

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
cutsMET = []; cutsISR = []

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

#Canvas 1: MET 1
c1 = ROOT.TCanvas("c1", "Total Reduction Factor")
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
 
gr1 = ROOT.TGraph2D(len(effReco2), np.array(cutsMET, 'float64'), np.array(cutsISR, 'float64'), np.array(redFactor2, 'float64')) #graph object with error bars using arrays of data
gr1.SetTitle("Total Reduction Factor for Both Generator Cuts")
 
#gr1.SetMarkerColor(ROOT.kBlue)
#gr1.SetMarkerStyle(ROOT.kFullCircle)
#gr1.SetMarkerSize(1)
gr1.GetHistogram()
gr1.GetXaxis().SetTitle("genMET Cut / GeV")
gr1.GetYaxis().SetTitle("genISR Cut / GeV")
gr1.GetZaxis().SetTitle("Reduction Factor at both Reco Cut Values")
gr1.GetXaxis().SetTitleOffset(1.2)
gr1.GetYaxis().SetTitleOffset(1.2)
gr1.GetZaxis().SetTitleOffset(1.2)
gr1.GetXaxis().CenterTitle()
gr1.GetYaxis().CenterTitle()
gr1.GetZaxis().CenterTitle()
#gr1.GetYaxis()->SetTicks("-"); //sets x-axis ticks

#for x in my_range(0, 156-13, 13):
#   print x
#   print cuts[2*x], cuts[2*x+1]
#   latex = ROOT.TLatex(gr1.GetX()[x], gr1.GetY()[x], "(" + cuts[2*x] + "," + cuts[2*x+1] + ")")
#   latex.SetTextSize(0.02)
   #latex.SetTextColor(ROOT.kRed)
#   gr1.GetListOfFunctions().Add(latex)
ROOT.gStyle.SetPalette(1) #55
gr1.Draw("COLZ") #CONT1-5 #plots the graph with axes and points
#gr1.Print() #prints data plot values to the screen

#print np.array(effReco2, 'float64')*np.array(effReco4, 'float64') 
c1.Update()
#pad1->Update();
c1.SaveAs(path + "efficiencyMaps/total3D/totalReduction.root")
c1.SaveAs(path + "efficiencyMaps/total3D/totalReduction.png")
c1.SaveAs(path + "efficiencyMaps/total3D/totalReduction.pdf")
