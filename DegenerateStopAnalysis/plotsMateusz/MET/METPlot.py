import ROOT
#import numpy as np
#import gtk, pygtk

from Workspace.HEPHYPythonTools.helpers import getChain#, getPlotFromChain, getYieldFromChain, getChunks
#from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_v3_Phys14V1 import*

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

dir1 = "/data/nrad/cmgTuples/postProcessed_v1_Phys14V5/none/"

signal=({\
"name" : "T2DegStop_300_270",
"bins" : ["T2DegStop_300_270"],
'dir' : dir1
})

ttJets=({\
"name" : "ttJets",
"bins" : ["TTJets"],
'dir' : dir1
})

WJetsHTToLNu=({\
"name" : "WJetsHTToLNu",
"bins" : ["WJetsToLNu_HT100to200", "WJetsToLNu_HT200to400", "WJetsToLNu_HT400to600", "WJetsToLNu_HT600toInf"],
'dir' : dir1,
})

T2DegSample = getChain(signal, histname='') #is Events also a chain?
TTSample    = getChain(ttJets, histname='')
WSample     = getChain(WJetsHTToLNu,histname='')

print 'Samples: ', signal['name'],"|",  ttJets['name'],"|",  WJetsHTToLNu['name']

#T2DegSample.Print() #Shows the tree structure of entire chain (entries, branches, leaves)
#TTSample.Print()
#WSample.Print()

#T2DegSample.Scan() #Shows all the values of the list of leaves separated by a colon
#TTSample.Scan()
#WSample.Scan()

#Selection
#entry = T2DegSample.GetLeaf("weight")
#entry.GetBranch().GetEntry(1)
#weight = entry.GetValue()
#print "Weight = " + str(weight)

METcut = 0
selection = "weight*(abs(met_pt)>" + str(METcut) +")"

#signalMET = ROOT.TH1F("signalMET","Histogram",1000,0,1000)
T2DegSample.Draw("met_pt>>signalMET(100,0,1000)",selection,"goff")
signalMET = ROOT.gDirectory.Get("signalMET")
#signalMET = ROOT.gPad.GetPrimitive("htemp")

signalMET.SetTitle("Degenerate Stop Signal MET")
signalMET.GetXaxis().SetTitle("Missing Transverse Energy #slash{E}_{T} / GeV")
signalMET.GetXaxis().CenterTitle()
signalMET.SetFillColor(0) #SetFillColourAlpha? (transparency)
signalMET.SetLineWidth(2)
signalMET.SetLineColor(ROOT.kAzure+2)

#signalMET.SetAxisRange(0,1000,"X")
#signalMET.SetAxisRange(0,2E6,"Y") #automatically calls SetMin-/Max-imum()
#signalMET.GetXaxis().SetRangeUser(0,1000)
#signalMET.SetMinimum(0)
#signalMET.SetMaximum(2E7)
#ROOT.gPad.SetLogy()

#c1.cd(3)
#entry = TTSample.GetLeaf("weight")
#entry.GetBranch().GetEntry(1)
#weight = entry.GetValue()
#print "Weight = " + str(weight)
#TTTMET = ROOT.TH1F("TTMET","Histogram",1000,0,1000)

TTSample.Draw("met_pt>>TTMET(100,0,1000)",selection,"goff")
TTMET = ROOT.gDirectory.Get("TTMET")
#TTMET = ROOT.gPad.GetPrimitive("htemp")

TTMET.SetTitle("t#bar{t} Background MET")
TTMET.GetXaxis().SetTitle("Missing Transverse Energy #slash{E}_{T} / GeV")
TTMET.GetXaxis().CenterTitle()
TTMET.SetFillColor(ROOT.kRed+2)

#TTMET.SetAxisRange(0,1000,"X")
#TTMET.SetAxisRange(0,2E6,"Y") #automatically calls SetMin-/Max-imum()
#TTMET.GetXaxis().SetRangeUser(0,1000)
#TTMET.SetMinimum(0)
#TTMET.SetMaximum(2E7)
#ROOT.gPad.SetLogy()

#c1.cd(4)
#WMET = ROOT.TH1F("WMET","Histogram",1000,0,1000)
#entry = WSample.GetLeaf("weight")
#entry.GetBranch().GetEntry(1)
#weight = entry.GetValue()
#print "Weight = " + str(weight)

WSample.Draw("met_pt>>WMET(100,0,1000)",selection,"goff")
WMET = ROOT.gDirectory.Get("WMET")
#WMET = ROOT.gPad.GetPrimitive("htemp")

WMET.SetTitle("W Background MET")
WMET.GetXaxis().SetTitle("Missing Transverse Energy #slash{E}_{T} / GeV")
WMET.GetXaxis().CenterTitle()
WMET.SetFillColor(ROOT.kGreen+3)

#WMET.SetAxisRange(0,1000,"X")
#WMET.SetAxisRange(0,2E6,"Y") #automatically calls SetMin-/Max-imum()
#WMET.GetXaxis().SetRangeUser(0,1000)
#WMET.SetMinimum(0)
#WMET.SetMaximum(2E7)
#ROOT.gPad.SetLogy()

stack = ROOT.THStack("stack", "MET Plot of Degenerate Stop Signal with t#bar{t} and W Backgrounds")
stack.Add(TTMET)
stack.Add(WMET)
stack.Print()

#Separate Histograms
c1 = ROOT.TCanvas("c1","MET Plots",1500,1000)
c1.Divide(2,2)
stack.Paint("pads")
c1.cd(1)
ROOT.gPad.SetLogy()
c1.cd(2)
ROOT.gPad.SetLogy()
c1.cd(3)
signalMET.Draw()

c1.SetGridx()
ROOT.gPad.SetLogy()

#Stacked Histograms
c2 = ROOT.TCanvas("c2","MET Plots",1500,1000)
stack.Draw() #Histograms paint stacked on top of each other #implies BuildStack()?
signalMET.Draw("same")
ROOT.gPad.SetLogy()
c2.SetGridx()

stack.GetXaxis().SetTitle("Missing Transverse Energy #slash{E}_{T} / GeV")
stack.GetYaxis().SetTitle("Counts")
stack.GetXaxis().CenterTitle()
stack.GetYaxis().CenterTitle()

leg = ROOT.TLegend(0.60,0.60,0.85,0.75)
leg.SetHeader("Legend")
leg.AddEntry("signalMET","Degenerate Stop Signal MET","F")
leg.AddEntry("TTMET","t#bar{t} Background MET","F")
leg.AddEntry("WMET","W Background MET","F")
leg.Draw()

header = leg.GetListOfPrimitives().First()
header.SetTextAlign(22)

#Full Screen
#height = ROOT.gClient.getDisplayHeight()
#c1.SetWindowSize(width, height)

c1.Modified()
c1.Update()
c2.Modified()
c2.Update()

#ROOT.TBrowser()
#T2DegSample.StartViewer()

c2.SaveAs("/afs/hephy.at/user/m/mzarucki/www/plots/degstopMETplot.png")
