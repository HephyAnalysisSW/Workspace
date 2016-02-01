#2Dfilter.py - Plots 2D histogram along 2D turn-ons.

print "Executing 2Dfilter.py script..."

import ROOT
import os, sys

from Workspace.HEPHYPythonTools.helpers import getChain#, getPlotFromChain, getYieldFromChain, getChunks

#ROOT Options
ROOT.gROOT.Reset() #re-initialises ROOT
#ROOT.gROOT.SetStyle("Plain")

ROOT.gStyle.SetOptStat(1111) #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis
ROOT.gStyle.SetOptFit(1111) #1111 prints fits results on plot
#ROOT.gStyle.SetTitleX(0.15)
#ROOT.gStyle.SetFuncWidth(1)
#ROOT.gStyle.SetFuncColor(9)
#ROOT.gStyle.SetLineWidth(2)
#ROOT.gStyle.SetOptTitle(0) #suppresses title box

ROOT.gStyle.SetPaintTextFormat("4.2f")
#ROOT.gStyle->SetTitleX(0.1)
#ROOT.gStyle->SetTitleW(0.8)

ROOT.gStyle.SetStatX(0.75)
ROOT.gStyle.SetStatY(0.65)
ROOT.gStyle.SetStatW(0.1)
ROOT.gStyle.SetStatH(0.15)


def makeLine():
   line = "\n**********************************************************************************************************************************\n"
   return line

def makeDoubleLine():
   line = "\n**********************************************************************************************************************************\n\
**********************************************************************************************************************************\n"
   return line

def newLine():
   print ""
   return 

dir = "/afs/hephy.at/work/n/nrad/cmgTuples/RunII/T2DegStop_300_270_RunII_withMotherRef"

signal=({\
"name" : "treeProducerSusySingleLepton", 
"bins" : ["treeProducerSusySingleLepton"], 
'dir' : dir
})

T2DegSample = getChain(signal, histname='',treeName="tree")

print makeLine()
print 'Sample: ', signal['name']
print makeLine()

def drawhist(sample, varname, sel, nbins = 100, min = 0, max = 1000):
   hist = ROOT.TH1F("hist", "Histogram", nbins, min, max)
   sample.Draw(varname + ">>hist", sel, "goff") #">>hname(100, 0, 1000)", sel, "goff")
   #hist = ROOT.gDirectory.Get("hname")
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
def select(varname, cut, option): #option = {>, =, <}
   sel = "abs(" + varname + option + str(cut) + ")"
   return sel

#Creates Legend
def makeLegend():
   leg = ROOT.TLegend(0.60,0.70,0.75,0.85)
   leg.SetHeader("#bf{Legend}")
   header = leg.GetListOfPrimitives().First()
   header.SetTextAlign(22)
   return leg 

#Creates Box 
def makeBox():
   box = ROOT.TPaveText(0.775,0.40,0.875,0.65, "NDC") #NB & ARC
   #box.SetHeader("Cuts")
   #header = box.GetListOfPrimitives().First()
   #header.SetTextAlign(22)
   return box 

def alignStats(hist):
   st = hist.FindObject("stats")
   st.SetX1NDC(0.775)
   st.SetX2NDC(0.875)
   st.SetY1NDC(0.7)
   st.SetY2NDC(0.85)

#Fit Function
fitFunc = ROOT.TF1("f1", "[0]*TMath::Erf((x-[1])/[2]) + [3]", 0, 1000) #Error function scaled to [0,1]
fitFunc.SetParNames("Normalisation", "Edge", "Resolution", "Y-Offset")
#fitFunc.SetParameter(0, 0.5)
#fitFunc.SetParameter(1, 150)
#fitFunc.SetParameter(2, 50)  
#fitFunc.SetParLimits(0, 0.4, 0.65) #keep fixed?
fitFunc.SetParLimits(1, 0, 200) #init: [0,200]
fitFunc.SetParLimits(2, 0, 60) #init: [0,60]
fitFunc.SetParLimits(3, 0.45, 0.8) #init: [0.45,0.8]

#Selection
#weight = 1
#str(weight) + "*(" && ")" 

#genMETcut = input("Enter Generated MET cut value: ")
#genISRcut = input("Enter Generated ISR Jet pT cut value: ")

cuts=({\
'MET' : 200, #MET cut (fixed)
'ISR' : 110, #ISR/Leading Jet cut (fixed)
'Eta' : 2.4, #eta cut (fixed)

'genMET' : 145, #generated quantity cuts
'genISR' : 0,
'genEta' : 5
})

nbins = 100
min = 0 #GeV
max = 1000 #GeV

#recoBinMET = int(cuts['MET']*nbins/(max - min)) + 1 #cuts['MET']/(h1.GetXaxis().GetBinWidth(0)) # + 1 to get correct bin
#recoBinISR = int(cuts['ISR']*nbins/(max - min)) + 1 #cuts['ISR']/(h1.GetXaxis().GetBinWidth(0))

cutString = \
"Preselection cuts: \n\n" + \
"MET cut: " + str(cuts['MET']) + "\n" \
"ISR Jet pT cut: " + str(cuts['ISR']) + "\n" \
"ISR Jet Eta cut: " + str(cuts['Eta']) + "\n\n" + \
"Generator cuts:" + "\n" + \
"Generated MET cut: " + str(cuts['genMET']) + "\n" \
"Generated ISR Jet pT cut: " + str(cuts['genISR']) + "\n" \
"Generated ISR Jet Eta cut: " + str(cuts['genEta']) 

print makeLine()
print cutString
 
#Preselection and Generated Particles Filter Selection

#Variables: met_pt, met_genPt, Jet_pt, GenJet_pt, Jet_eta, GenJet_eta

#MET Selection
preSel1 = "Max$(Jet_pt*(abs(Jet_eta)<" + str(cuts['Eta']) + "))" + ">" + str(cuts['ISR']) #normally would be with preSel2
#MaxIf$("Jet_pt", select("Jet_eta", cuts['Eta'], "<")) + ">" + cuts['ISR'], #Jet_pt[0] is one with max Pt

genSel1 = select("met_genPt", cuts['genMET'], ">")

#ISR Jet Pt Selection
preSel2 = select("met_pt", cuts['MET'], ">") #normally would be with preSel1

genSel2 = "Max$(GenJet_pt*(abs(GenJet_eta)<" + str(cuts['genEta']) + "))" + ">" + str(cuts['genISR'])
#maxIf$("GenJet_pt", select("GenJet_eta", cuts['genEta'], "<")) + ">" + cuts['genISR'] + ")" #GenJet_pt[0] is one with max Pt

###########################################################################Canvas 1: 2D Histograms

c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,2)

#nbins = 100
#min = 0
#max = 1000

var1 = "met_pt"
var2 = "Max$(Jet_pt*(abs(Jet_eta)<" + str(cuts['Eta']) + "))" #Leading JET pt with eta < 2.4
sel = ""

#Reco Histogram
c1.cd(1)
h1 = ROOT.TH2F("h1", "Histogram", nbins, min, max, nbins, min, max)
T2DegSample.Draw(var1 + ":" + var2 + ">>h1", sel, "goff") #">>hname(100, 0, 1000)", sel, "goff")
#h1 = ROOT.gDirectory.Get("hist")
#h1.SetName("h1")
h1.SetTitle("MET and ISR Jet p_{T} Histogram")
h1.GetXaxis().SetTitle("ISR Jet p_{T} / GeV")
h1.GetYaxis().SetTitle("Missing Transverse Energy #slash{E}_{T} / GeV")
h1.GetZaxis().SetTitle("Counts")
h1.GetXaxis().SetTitleOffset(1.6)
h1.GetYaxis().SetTitleOffset(1.6)
h1.GetZaxis().SetTitleOffset(1.6)
h1.GetXaxis().CenterTitle()
h1.GetYaxis().CenterTitle()
h1.GetZaxis().CenterTitle()
h1.GetYaxis().SetRangeUser(0, 500)
h1.GetXaxis().SetRangeUser(0, 500)
h1.GetZaxis().SetRangeUser(0, 10000)
#h1.SetAxisRange(0, 1000, "X")
#h1.SetAxisRange(0, 2E6, "Y") #automatically calls SetMin-/Max-imum()
#h1.SetMinimum(0)
#h1.SetMaximum(2E7)
h1.Draw("COLZ") #CONT1-5 #plots the graph with axes and points

ROOT.gPad.SetLogz()
ROOT.gPad.Update()

alignStats(h1)

#Generator Filter Applied
sel = genSel1 + "&&" + genSel2

h2 = ROOT.TH2F("h2", "Histogram", nbins, min, max, nbins, min, max)
T2DegSample.Draw(var1 + ":" + var2 + ">>h2", sel, "goff") #">>hname(100, 0, 1000)", sel, "goff")

#ROOT.gPad.SetLogz()

#Efficiency and Reduction Factor Calculation 
#eff1 = h2.GetEntries()/h1.GetEntries()
#ineff1 = (h1.GetEntries()-h2.GetEntries())/h1.GetEntries() # = 1 - eff1
#red1 = h1.GetEntries()/h2.GetEntries() # = 1/eff

box1 = makeBox()
box1.AddText("Cuts:")
#box1.AddText("#bf{MET p_{T} cut: }" + str(cuts['MET']) + " GeV")
#box1.AddText("#bf{ISR Jet p_{T} cut: }" + str(cuts['ISR']) + " GeV")
#box1.AddText("#bf{ISR Jet #eta cut: }" + str(cuts['Eta']))
box1.AddText("#bf{Gen. MET p_{T} cut: }" + str(cuts['genMET']) + " GeV")
box1.AddText("#bf{Gen. ISR Jet p_{T} cut: }" + str(cuts['genISR']) + " GeV")
box1.AddText("#bf{Gen. ISR Jet Eta #eta cut: }" + str(cuts['genEta']))
#box1.AddText("Filter:")
#box1.AddText("#bf{Filter Efficiency: }" + str("%0.3f"%eff1))
#box1.AddText("#bf{Inefficiencies Fraction: }" + str("%0.3f"%ineff1))
#box1.AddText("#bf{Reduction Factor: }" + str("%0.3f"%red1))
box1.Draw()

ROOT.gPad.Update()

#alignStats(h2)

#Generator Filter Efficiency
c1.cd(2)
h4 = ROOT.TH2F("h4", "Histogram", nbins, min, max, nbins, min, max)
h4.Divide(h2, h1) #quotient
h4.SetTitle("Generator Filter Efficiency for MET and ISR Jet p_{T}")
h4.GetXaxis().SetTitle("ISR Jet p_{T} / GeV")
h4.GetYaxis().SetTitle("Missing Transverse Energy #slash{E}_{T} / GeV")
h4.GetZaxis().SetTitle("Counts")
h4.GetXaxis().SetTitleOffset(1.6)
h4.GetYaxis().SetTitleOffset(1.6)
h4.GetZaxis().SetTitleOffset(1.6)
h4.GetXaxis().CenterTitle()
h4.GetYaxis().CenterTitle()
h4.GetZaxis().CenterTitle()
h4.GetXaxis().SetRangeUser(0, 500)
h4.GetYaxis().SetRangeUser(0, 500)
h4.GetZaxis().SetRangeUser(0.9, 1)
#h4.SetAxisRange(0, 1000, "X")
#h4.SetAxisRange(0, 2E6, "Y") #automatically calls SetMin-/Max-imum()
#h4.SetMinimum(0)
#h4.SetMaximum(2E7)
h4.Draw("COLZ") #CONT1-5 #plots the graph with axes and points

#ROOT.gPad.SetLogz()

ROOT.gPad.Update()

alignStats(h4)

c1.Modified()
c1.Update()

#Save to Web
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/filter/final/13TeV/%s_%s/"%(str(cuts['genMET']), str(cuts['genISR']))

if not os.path.exists(savedir):
      os.makedirs(savedir)

c1.SaveAs(savedir + "2Dfilter_%s_%s.root"%(str(cuts['genMET']), str(cuts['genISR'])))
c1.SaveAs(savedir + "2Dfilter_%s_%s.png"%(str(cuts['genMET']), str(cuts['genISR'])))
c1.SaveAs(savedir + "2Dfilter_%s_%s.pdf"%(str(cuts['genMET']), str(cuts['genISR'])))
