#redEffPlotHT.py script - Gen. Filter Reduction Factor vs Efficiency at Reco Cut Plot

print "\nExecuting redEffPlotHT.py script..."

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

path = "/afs/hephy.at/user/m/mzarucki/www/plots/filter/13TeV/HT/ROI/"

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

   for line in infile:
         #print line
         line = infile.next() 
         print line
         buffer = line.split()
         cuts.append(buffer[0]) #gMET cut
         cuts.append(buffer[1]) #gHT cut
         redFactor1.append(buffer[2]) #MET 1
         effReco1.append(buffer[3]) #MET 1
         redFactor2.append(buffer[4]) #MET 2
         effReco2.append(buffer[5]) #MET 2
         redFactor3.append(buffer[6]) # HT 1
         effReco3.append(buffer[7]) #HT 1
         redFactor4.append(buffer[8]) #HT 2
         effReco4.append(buffer[9]) #HT 2
   infile.close()

#Canvas 1: MET 1
c1 = ROOT.TCanvas("c1", "MET 1")
c1.SetGrid() #adds a grid to the canvas
#c1.SetFillColor(42)
c1.GetFrame().SetFillColor(21)
c1.GetFrame().SetBorderSize(12)
 
gr1 = ROOT.TGraph(len(redFactor1), np.array(redFactor1, 'float64'), np.array(effReco1, 'float64')) #graph object with error bars using arrays of data
gr1.SetTitle("MET 1: Filter Efficiency at Reco Cut vs. Reduction Factor")
 
gr1.SetMarkerColor(ROOT.kBlue)
gr1.SetMarkerStyle(ROOT.kFullCircle)
gr1.SetMarkerSize(0.7)
gr1.GetXaxis().SetTitle("Reduction Factor")
gr1.GetYaxis().SetTitle("Filter Efficiency at Reco Cut Value")
gr1.GetXaxis().SetTitleOffset(1.2)
gr1.GetYaxis().SetTitleOffset(1.3)
gr1.GetXaxis().CenterTitle()
gr1.GetYaxis().CenterTitle()

for x in range(len(cuts)/2):
   print x
   print cuts[2*x], cuts[2*x+1]
   latex = ROOT.TLatex(gr1.GetX()[x] + 0.0005, gr1.GetY()[x] + 0.0005, "(" + cuts[2*x] + "," + cuts[2*x+1] + ")")
   latex.SetTextSize(0.03)
   #latex.SetTextColor(ROOT.kRed)
   gr1.GetListOfFunctions().Add(latex)

gr1.Draw("AP") #plots the graph with axes and points
 
#Canvas 2: MET 2
c2 = ROOT.TCanvas("c2", "MET 2")
c2.SetGrid() #adds a grid to the canvas

gr2 = ROOT.TGraph(len(redFactor2), np.array(redFactor2, 'float64'), np.array(effReco2, 'float64')) #graph object with error bars using arrays of data
gr2.SetTitle("Generated MET Filter Efficiency at Reco Cut vs. Reduction Factor")

gr2.SetMarkerColor(ROOT.kBlue)
gr2.SetMarkerStyle(ROOT.kFullCircle)
gr2.SetMarkerSize(0.7)
gr2.GetXaxis().SetTitle("Reduction Factor")
gr2.GetYaxis().SetTitle("Filter Efficiency at Reco Cut Value")
gr2.GetXaxis().SetTitleOffset(1.2)
gr2.GetYaxis().SetTitleOffset(1.3)
gr2.GetXaxis().CenterTitle()
gr2.GetYaxis().CenterTitle()

for x in range(len(cuts)/2):
   print x
   print cuts[2*x], cuts[2*x+1]
   latex = ROOT.TLatex(gr2.GetX()[x] + 0.00005, gr2.GetY()[x] + 0.00005, "(" + cuts[2*x] + "," + cuts[2*x+1] + ")")
   latex.SetTextSize(0.03)
   #latex.SetTextColor()
   gr2.GetListOfFunctions().Add(latex)

gr2.Draw("AP") #plots the graph with axes and points

#Canvas 3
c3 = ROOT.TCanvas("c3", "HT 1")
c3.SetGrid() #adds a grid to the canvas
 
gr3 = ROOT.TGraph(len(redFactor3), np.array(redFactor3, 'float64'), np.array(effReco3, 'float64')) #graph object with error bars using arrays of data
gr3.SetTitle("HT 1: Filter Efficiency at Reco Cut vs. Reduction Factor")
 
gr3.SetMarkerColor(ROOT.kBlue)
gr3.SetMarkerStyle(ROOT.kFullCircle)
gr3.SetMarkerSize(0.7)
gr3.GetXaxis().SetTitle("Reduction Factor")
gr3.GetYaxis().SetTitle("Filter Efficiency at Reco Cut Value")
gr3.GetXaxis().SetTitleOffset(1.2)
gr3.GetYaxis().SetTitleOffset(1.3)
gr3.GetXaxis().CenterTitle()
gr3.GetYaxis().CenterTitle()
 
for x in range(len(cuts)/2):
   print x
   print cuts[2*x], cuts[2*x+1]
   latex = ROOT.TLatex(gr3.GetX()[x] + 0.0005, gr3.GetY()[x] + 0.0005, "(" + cuts[2*x] + "," + cuts[2*x+1] + ")")
   latex.SetTextSize(0.03)
   #latex.SetTextColor()
   gr3.GetListOfFunctions().Add(latex)

gr3.Draw("AP") #plots the graph with axes and points

#Canvas 4
c4 = ROOT.TCanvas("c4", "HT 2")
c4.SetGrid() #adds a grid to the canvas

gr4 = ROOT.TGraph(len(redFactor4), np.array(redFactor4, 'float64'), np.array(effReco4, 'float64')) #graph object with error bars using arrays of data
gr4.SetTitle("Generated HT Filter Efficiency at Reco Cut Value vs. Reduction Factor")

gr4.SetMarkerColor(ROOT.kBlue)
gr4.SetMarkerStyle(ROOT.kFullCircle)
gr4.SetMarkerSize(0.7)
gr4.GetXaxis().SetTitle("Reduction Factor")
gr4.GetYaxis().SetTitle("Filter Efficiency at Reco Cut Value")
gr4.GetXaxis().SetTitleOffset(1.2)
gr4.GetYaxis().SetTitleOffset(1.3)
gr4.GetXaxis().CenterTitle()
gr4.GetYaxis().CenterTitle()

for x in range(len(cuts)/2):
   print x
   print cuts[2*x], cuts[2*x+1]
   latex = ROOT.TLatex(gr4.GetX()[x] + 0.0005, gr4.GetY()[x] + 0.0005, "(" + cuts[2*x] + "," + cuts[2*x+1] + ")")
   latex.SetTextSize(0.03)
   #latex.SetTextColor()
   gr4.GetListOfFunctions().Add(latex)

gr4.Draw("AP") #plots the graph with axes and points

#Save to Web
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/filter/13TeV/HT/ROI/reductionEfficiency/"

if not os.path.exists(savedir):
      os.makedirs(savedir)

c1.SaveAs(path + "reductionEfficiency/redEffMET1plotROI.root")
c1.SaveAs(path + "reductionEfficiency/redEffMET1plotROI.png")
c1.SaveAs(path + "reductionEfficiency/redEffMET1plotROI.pdf")

c2.SaveAs(path + "reductionEfficiency/redEffMET2plotROI.root")
c2.SaveAs(path + "reductionEfficiency/redEffMET2plotROI.png")
c2.SaveAs(path + "reductionEfficiency/redEffMET2plotROI.pdf")

#c2.SaveAs(savedir + "MET_ROC.root")
#c2.SaveAs(savedir + "MET_ROC.png")
#c2.SaveAs(savedir + "MET_ROC.pdf")

c3.SaveAs(path + "reductionEfficiency/redEffHT1plotROI.root")
c3.SaveAs(path + "reductionEfficiency/redEffHT1plotROI.png")
c3.SaveAs(path + "reductionEfficiency/redEffHT1plotROI.pdf")

c4.SaveAs(path + "reductionEfficiency/redEffHT2plotROI.root")
c4.SaveAs(path + "reductionEfficiency/redEffHT2plotROI.png")
c4.SaveAs(path + "reductionEfficiency/redEffHT2plotROI.pdf")

#c4.SaveAs(savedir + "HT_ROC.root")
#c4.SaveAs(savedir + "HT_ROC.png")
#c4.SaveAs(savedir + "HT_ROC.pdf")
