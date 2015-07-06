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
   return hist 

#Selection function
def selection(varname, weight, cut):
   sel = str(weight) + "*(abs(" + varname + ">" + str(cut) + "))"
   return sel

#Creates Legend
def makeLegend():
   leg = ROOT.TLegend(0.60,0.60,0.85,0.75)
   leg.SetHeader("Legend")
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
c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)

variable = "met_pt"
h1 = drawhist(T2DegSample, variable)
h1.SetName("h1")
h1.SetTitle("Generated and Reconstructed MET Comparison")
h1.GetXaxis().SetTitle("Missing Transverse Energy #slash{E}_{T} / GeV")
h1.Draw()
h1.SetFillColor(ROOT.kRed+1)
h1.SetLineWidth(4)
h1.SetLineColor(ROOT.kBlack)


l1 = makeLegend()
l1.AddEntry("h1", variable, "F")

variable = "met_genPt"
h2 = drawhist(T2DegSample, variable)
h2.SetName("h2")
h2.Draw("same")
h2.SetFillColor(0)
#h2.SetFillStyle(4050) 
h2.SetLineWidth(4)
h2.SetLineColor(ROOT.kAzure+7)
l1.AddEntry("h2", variable, "F")

l1.Draw()

ROOT.gPad.SetLogy()
c1.SetGridx()

c1.Modified()
c1.Update()

#Canvas 2
c2 = ROOT.TCanvas("c2", "Canvas 2", 1800, 1500)

variable = "Jet_pt"
h3 = drawhist(T2DegSample, variable)
h3.SetName("h3")
h3.SetTitle("Generated and Reconstructed Jet p_{T} Comparison")
h3.GetXaxis().SetTitle("Jet p_{T} / GeV")
h3.Draw()
h3.SetFillColor(ROOT.kRed+1)
h3.SetLineWidth(4)
h3.SetLineColor(ROOT.kBlack)
l2 = makeLegend()
l2.AddEntry("h3", variable, "F")

variable = "GenJet_pt"
h4 = drawhist(T2DegSample, variable)
h4.SetName("h4")
h4.Draw("same")
h4.SetFillColor(0)
#h4.SetFillStyle(3001)
h4.SetLineWidth(4)
h4.SetLineColor(ROOT.kAzure+7)
ROOT.gPad.SetLogy()
c2.SetGridx()

l2.AddEntry("h4", variable, "F")
l2.Draw()

c2.Modified()
c2.Update() 

#c1.SaveAs("/afs/cern.ch/work/m/mzarucki/plots/%s.png"%varname)
#Full Screen
#height = ROOT.gClient.getDisplayHeight()
#c1.SetWindowSize(width, height)


