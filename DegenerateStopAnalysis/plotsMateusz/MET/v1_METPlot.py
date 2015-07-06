import ROOT
#import numpy as np
#import gtk, pygtk

from Workspace.HEPHYPythonTools.helpers import getChain#, getPlotFromChain, getYieldFromChain, getChunks
#from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_v3_Phys14V1 import*

#ROOT Options
ROOT.gROOT.Reset() #re-initialises ROOT
#ROOT.gROOT.SetStyle("Plain")

ROOT.gStyle.SetOptStat(1)
#ROOT.gStyle.SetOptFit(0) #1111 prints fits results on plot
#ROOT.gStyle.SetTitleX(0.15)
#ROOT.gStyle.SetFuncWidth(1)
#ROOT.gStyle.SetFuncColor(9)
#ROOT.gStyle.SetLineWidth(2)
#gStyle.SetOptTitle(0) #suppresses title box

dir1 = "/data/mzarucki"

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

#selection =  #cuts for selection

c1 = ROOT.TCanvas("c1","MET Plots")
c1.Divide(2,2)

c1.cd(2)

#signalMET = ROOT.TH1F("signalMET","Histogram",1000,0,1000)
T2DegSample.Draw("met_pt>>signalMET(100,0,1000)","","")
signalMET = ROOT.gDirectory.Get("signalMET")
#signalMET = ROOT.gPad.GetPrimitive("htemp")

signalMET.SetTitle("Signal MET")
signalMET.GetXaxis().SetTitle("Missing Transverse Energy E_{T} / GeV")
signalMET.GetXaxis().CenterTitle()
signalMET.SetFillColor(ROOT.kAzure+2)

#signalMET.SetAxisRange(0,1000,"X")
#signalMET.SetAxisRange(0,2E6,"Y") #automatically calls SetMin-/Max-imum()
#signalMET.GetXaxis().SetRangeUser(0,1000)
#signalMET.SetMinimum(0)
#signalMET.SetMaximum(2E7)
ROOT.gPad.SetLogy()

c1.cd(3)
#TTTMET = ROOT.TH1F("TTMET","Histogram",1000,0,1000)
TTSample.Draw("met_pt>>TTMET(100,0,1000)","","")
TTMET = ROOT.gDirectory.Get("TTMET")
#TTMET = ROOT.gPad.GetPrimitive("htemp")

TTMET.SetTitle("TT Background MET")
TTMET.GetXaxis().SetTitle("Missing Transverse Energy E_{T} / GeV")
TTMET.GetXaxis().CenterTitle()
TTMET.SetFillColor(ROOT.kRed+2)

#TTMET.SetAxisRange(0,1000,"X")
#TTMET.SetAxisRange(0,2E6,"Y") #automatically calls SetMin-/Max-imum()
#TTMET.GetXaxis().SetRangeUser(0,1000)
#TTMET.SetMinimum(0)
#TTMET.SetMaximum(2E7)
ROOT.gPad.SetLogy()

c1.cd(4)
#WMET = ROOT.TH1F("WMET","Histogram",1000,0,1000)
WSample.Draw("met_pt>>WMET(100,0,1000)","","")
WMET = ROOT.gDirectory.Get("WMET")
#WMET = ROOT.gPad.GetPrimitive("htemp")

WMET.SetTitle("W Background MET")
WMET.GetXaxis().SetTitle("Missing Transverse Energy E_{T} / GeV")
WMET.GetXaxis().CenterTitle()
WMET.SetFillColor(ROOT.kGreen+3)

#WMET.SetAxisRange(0,1000,"X")
#WMET.SetAxisRange(0,2E6,"Y") #automatically calls SetMin-/Max-imum()
#WMET.GetXaxis().SetRangeUser(0,1000)
#WMET.SetMinimum(0)
#WMET.SetMaximum(2E7)
ROOT.gPad.SetLogy()

#Stacked Histograms

stack = ROOT.THStack("stack", "Stacked MET Histograms")
stack.Add(signalMET)
stack.Add(TTMET)
stack.Add(WMET)

c1.cd(1)
stack.Draw()


#Full Screen
#width = ROOT.gClient.getDisplayWidth()
#height = ROOT.gClient.getDisplayHeight()
#c1.SetWindowSize(width, height)

c1.Modified()
c1.Update()
