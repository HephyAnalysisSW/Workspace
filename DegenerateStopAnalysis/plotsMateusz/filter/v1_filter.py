#filter.py

import ROOT

from Workspace.HEPHYPythonTools.helpers import getChain#, getPlotFromChain, getYieldFromChain, getChunks

#ROOT Options
ROOT.gROOT.Reset() #re-initialises ROOT
#ROOT.gROOT.SetStyle("Plain")

ROOT.gStyle.SetOptStat(0)
#ROOT.gStyle.SetOptFit(1111) #1111 prints fits results on plot
#ROOT.gStyle.SetTitleX(0.15)
#ROOT.gStyle.SetFuncWidth(1)
#ROOT.gStyle.SetFuncColor(9)
#ROOT.gStyle.SetLineWidth(2)
#ROOT.gStyle.SetOptTitle(0) #suppresses title box

dir = "/afs/cern.ch/work/m/mzarucki/data"

signal=({\
"name" : "T2DegStop_300_270_RunII",
"bins" : ["T2DegStop_300_270_RunII"],
'dir' : dir
})

T2DegSample = getChain(signal, histname='',treeName="tree")

print 'Sample: ', signal['name']

#T2DegSample.Print() #Shows the tree structure of entire chain (entries, branches, leaves)

#T2DegSample.Scan() #Shows all the values of the list of leaves separated by a colon

def drawhist(sample, varname):
   #hist = ROOT.TH1F("signalMET","Histogram",1000,0,1000)
   sample.Draw(varname + ">>hname(100, 0, 1000)",selection(varname, weight, cuts['MET']), "goff")
   hist = ROOT.gDirectory.Get("hname")
   hist.SetTitle(varname + " Plot")
   hist.GetXaxis().SetTitle(varname + "/ GeV")
   hist.GetYaxis().SetTitle("Counts")
   hist.GetXaxis().CenterTitle()
   hist.GetYaxis().CenterTitle()
   #hist.SetAxisRange(0, 1000, "X")
   #hist.SetAxisRange(0, 2E6, "Y") #automatically calls SetMin-/Max-imum()
   #hist.GetXaxis().SetRangeUser(0, 1000)
   #hist.SetMinimum(0)
   #hist.SetMaximum(2E7)
   hist.SetName("hist")
   return hist 

#Selection function
def selection(varname, weight, cut):
   sel = str(weight) + "*(abs(" + varname + ">" + str(cut) + "))"
   return sel

#Creates Legend
def makeLegend():
   leg = ROOT.TLegend(0.60,0.60,0.85,0.75)
   leg.SetHeader("Legend")
   leg.AddEntry("hist","Degenerate Stop Signal","F")
   header = leg.GetListOfPrimitives().First()
   header.SetTextAlign(22)

   return leg 

#Selection
weight = 1
cuts=({\
'MET' : 0, #MET cut
'ISR' : 0 #ISR cut
})

#Canvas 1
c1 = ROOT.TCanvas("c1", "Canvas 1", 1500, 1000)
h1 = drawhist(T2DegSample, "met_pt")
h1.Draw()
h1.SetFillColor(ROOT.kAzure+7) #SetFillColourAlpha? (transparency)
h1.SetLineWidth(2)
h1.SetLineColor(ROOT.kAzure+2)
ROOT.gPad.SetLogy()
c1.SetGridx()
l1 = makeLegend()
l1.Draw()

c1.Modified()
c1.Update()

#Canvas 2
c2 = ROOT.TCanvas("c2", "Canvas 2", 1500, 1000)
h2 = drawhist(T2DegSample,"Jet_pt")
h2.Draw()
h2.SetFillColor(ROOT.kRed+1) #SetFillColourAlpha? (transparency)
h2.SetLineWidth(2)
h2.SetLineColor(ROOT.kAzure+2)
ROOT.gPad.SetLogy()
c2.SetGridx()

l2 = makeLegend()
l2.Draw()

c2.Modified()
c2.Update()

#Canvas 3
c3 = ROOT.TCanvas("c3", "Canvas 3", 1500, 1000)
h3 = drawhist(T2DegSample, "met_genPt")
h3.Draw()
h3.SetFillColor(ROOT.kGreen+2) #SetFillColourAlpha? (transparency)
h3.SetLineWidth(2)
h3.SetLineColor(ROOT.kAzure+2)
ROOT.gPad.SetLogy()
c3.SetGridx()
l3 = makeLegend()
l3.Draw()

c3.Modified()
c3.Update()

#Canvas 4
c4 = ROOT.TCanvas("c4", "Canvas 4", 1500, 1000)
h4 = drawhist(T2DegSample, "GenJet_pt")
h4.Draw()
h4.SetFillColor(ROOT.kOrange-2) #SetFillColourAlpha? (transparency)
h4.SetLineWidth(2)
h4.SetLineColor(ROOT.kAzure+2)
ROOT.gPad.SetLogy()
c4.SetGridx()
l4 = makeLegend()
l4.Draw()

c4.Modified()
c4.Update() 

#c1.SaveAs("/afs/cern.ch/work/m/mzarucki/plots/%s.png"%varname)
#Full Screen
#height = ROOT.gClient.getDisplayHeight()
#c1.SetWindowSize(width, height)


