#2Dfilter.py

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


dir = "/afs/hephy.at/work/n/nrad/cmgTuples/RunII/T2DegStop_300_270_RunII_withMotherRef"
#dir = "/afs/cern.ch/work/n/nrad/cmgTuples/RunII/RunII_T2DegStop_300_270_prunedGenParticles/T2DegStop_300_270_RunII_genParticles"
#dir = "/afs/cern.ch/work/m/mzarucki/data"

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

signal=({\
"name" : "treeProducerSusySingleLepton", #"T2DegStop_300_270_RunII"
"bins" : ["treeProducerSusySingleLepton"], #["T2DegStop_300_270_RunII"]
'dir' : dir
})

print makeLine()

T2DegSample = getChain(signal, histname='',treeName="tree")

print 'Sample: ', signal['name']

print makeLine()

#T2DegSample.Print() #Shows the tree structure of entire chain (entries, branches, leaves)

#T2DegSample.Scan() #Shows all the values of the list of leaves separated by a colon

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

#def getJetPt(jets) #getJets(), #getLeadingJetPt() == Jet_pt[0]
#   for jet in jets:
#         return jet.pt()
#   return 0

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

#gMETcut = input("Enter Generated MET cut value: ")
#gISRcut = input("Enter Generated ISR Jet pT cut value: ")

cuts=({\
'MET' : 200, #MET cut (fixed)
'ISR' : 110, #ISR/Leading Jet cut (fixed)
'Eta' : 2.4, #eta cut (fixed)

'gMET' : 130, #generated quantity cuts
'gISR' : 90,
'gEta' : 2.5
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
"Generated MET cut: " + str(cuts['gMET']) + "\n" \
"Generated ISR Jet pT cut: " + str(cuts['gISR']) + "\n" \
"Generated ISR Jet Eta cut: " + str(cuts['gEta']) 

print makeLine()
print cutString
 
#Preselection and Generated Particles Filter Selection

#Variables: met_pt, met_genPt, Jet_pt, GenJet_pt, Jet_eta, GenJet_eta

#MET Selection
preSel1 = "Max$(Jet_pt*(abs(Jet_eta)<" + str(cuts['Eta']) + "))" + ">" + str(cuts['ISR']) #normally would be with preSel2
#MaxIf$("Jet_pt", select("Jet_eta", cuts['Eta'], "<")) + ">" + cuts['ISR'], #Jet_pt[0] is one with max Pt

genSel1 = select("met_genPt", cuts['gMET'], ">")

#ISR Jet Pt Selection
preSel2 = select("met_pt", cuts['MET'], ">") #normally would be with preSel1

genSel2 = "Max$(GenJet_pt*(abs(GenJet_eta)<" + str(cuts['gEta']) + "))" + ">" + str(cuts['gISR'])
#maxIf$("GenJet_pt", select("GenJet_eta", cuts['gEta'], "<")) + ">" + cuts['gISR'] + ")" #GenJet_pt[0] is one with max Pt

###########################################################################Canvas 1: 2D Histograms

c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,4)

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
h1.SetTitle("MET and ISR Jet p_{T} Histogram (no generator cuts)")
h1.GetXaxis().SetTitle("ISR Jet p_{T} / GeV")
h1.GetYaxis().SetTitle("Missing Transverse Energy #slash{E}_{T} / GeV")
h1.GetZaxis().SetTitle("Counts")
h1.GetXaxis().SetTitleOffset(1.6)
h1.GetYaxis().SetTitleOffset(1.6)
h1.GetZaxis().SetTitleOffset(1.6)
h1.GetXaxis().CenterTitle()
h1.GetYaxis().CenterTitle()
h1.GetZaxis().CenterTitle()
h1.GetZaxis().SetRangeUser(0, 10000)
#h1.SetAxisRange(0, 1000, "X")
#h1.SetAxisRange(0, 2E6, "Y") #automatically calls SetMin-/Max-imum()
#h1.SetMinimum(0)
#h1.SetMaximum(2E7)
h1.Draw("SURF2")

ROOT.gPad.SetLogz()
ROOT.gPad.Update()

#alignStats(h1)

#Generator Filter Applied
c1.cd(2)
sel = genSel1 + "&&" + genSel2

h2 = ROOT.TH2F("h2", "Histogram", nbins, min, max, nbins, min, max)
T2DegSample.Draw(var1 + ":" + var2 + ">>h2", sel, "goff") #">>hname(100, 0, 1000)", sel, "goff")
#hist = ROOT.gDirectory.Get("hname")
#h2.SetName("h2")
h2.SetTitle("Generator Filter Effect on MET and ISR Jet p_{T}")
h2.GetXaxis().SetTitle("ISR Jet p_{T} / GeV")
h2.GetYaxis().SetTitle("Missing Transverse Energy #slash{E}_{T} / GeV")
h2.GetZaxis().SetTitle("Counts")
h2.GetXaxis().SetTitleOffset(1.6)
h2.GetYaxis().SetTitleOffset(1.6)
h2.GetZaxis().SetTitleOffset(1.6)
h2.GetXaxis().CenterTitle()
h2.GetYaxis().CenterTitle()
h2.GetZaxis().CenterTitle()
h2.GetZaxis().SetRangeUser(0, 10000)
#h2.SetAxisRange(0, 1000, "X")
#h2.SetAxisRange(0, 2E6, "Y") #automatically calls SetMin-/Max-imum()
#h2.SetMinimum(0)
#h2.SetMaximum(2E7)
h2.Draw("SURF2")

ROOT.gPad.SetLogz()

#Efficiency and Reduction Factor Calculation 
eff1 = h2.GetEntries()/h1.GetEntries()
ineff1 = (h1.GetEntries()-h2.GetEntries())/h1.GetEntries() # = 1 - eff1
red1 = h1.GetEntries()/h2.GetEntries() # = 1/eff

box1 = makeBox()
box1.AddText("Cuts:")
#box1.AddText("#bf{MET p_{T} cut: }" + str(cuts['MET']) + " GeV")
#box1.AddText("#bf{ISR Jet p_{T} cut: }" + str(cuts['ISR']) + " GeV")
#box1.AddText("#bf{ISR Jet #eta cut: }" + str(cuts['Eta']))
box1.AddText("#bf{Gen. MET p_{T} cut: }" + str(cuts['gMET']) + " GeV")
box1.AddText("#bf{Gen. ISR Jet p_{T} cut: }" + str(cuts['gISR']) + " GeV")
box1.AddText("#bf{Gen. ISR Jet Eta #eta cut: }" + str(cuts['gEta']))
#box1.AddLine(0, 0.5, 1, 0.5)
#box1.AddText("")
box1.AddText("Filter:")
box1.AddText("#bf{Filter Efficiency: }" + str("%0.3f"%eff1))
box1.AddText("#bf{Inefficiencies Fraction: }" + str("%0.3f"%ineff1))
box1.AddText("#bf{Reduction Factor: }" + str("%0.3f"%red1))
box1.Draw()

ROOT.gPad.Update()

c1.Modified()
c1.Update()

###########################################################################Canvas 2: 2D Difference and Efficiency Histograms

#c2 = ROOT.TCanvas("c2", "Canvas 2", 1800, 1500)
#c2.Divide(1,2)

#Difference between total and passed
#c2.cd(1)
c1.cd(3)
h3 = h1 - h2 #difference
h3.SetName("h3")
h3.SetTitle("Difference between MET and ISR Jet p_{T} Total and Passed Histograms for Generator Filter")
h3.GetXaxis().SetTitle("ISR Jet p_{T} / GeV")
h3.GetYaxis().SetTitle("Missing Transverse Energy #slash{E}_{T} / GeV")
h3.GetZaxis().SetTitle("Counts")
h3.GetXaxis().SetTitleOffset(1.6)
h3.GetYaxis().SetTitleOffset(1.6)
h3.GetZaxis().SetTitleOffset(1.6)
h3.GetXaxis().CenterTitle()
h3.GetYaxis().CenterTitle()
h3.GetZaxis().CenterTitle()
h3.GetZaxis().SetRangeUser(0, 10000)
#h1.SetAxisRange(0, 1000, "X")
#h1.SetAxisRange(0, 2E6, "Y") #automatically calls SetMin-/Max-imum()
#h1.SetMinimum(0)
#h1.SetMaximum(2E7)
h3.Draw("SURF2")

box1.Draw()

ROOT.gPad.SetLogz()
ROOT.gPad.Update()

#alignStats(h1)

#Generator Filter Efficiency
#c2.cd(2)
c1.cd(4)
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
h4.GetZaxis().SetRangeUser(0, 1)
#h4.SetAxisRange(0, 1000, "X")
#h4.SetAxisRange(0, 2E6, "Y") #automatically calls SetMin-/Max-imum()
#h4.SetMinimum(0)
#h4.SetMaximum(2E7)
h4.Draw("SURF2")

#ROOT.gPad.SetLogz()

box1.Draw()

ROOT.gPad.Update()

c1.Modified()
c1.Update()

#Save to Web
path = "/afs/hephy.at/user/m/mzarucki/www/plots/filter/ROI/finalCuts/"

c1.SaveAs(path + "%s_%s/2Dfilter_%s_%s.root"%(str(cuts['gMET']), str(cuts['gISR']), str(cuts['gMET']), str(cuts['gISR'])))
c1.SaveAs(path + "%s_%s/2Dfilter_%s_%s.png"%(str(cuts['gMET']), str(cuts['gISR']), str(cuts['gMET']), str(cuts['gISR'])))
c1.SaveAs(path + "%s_%s/2Dfilter_%s_%s.pdf"%(str(cuts['gMET']), str(cuts['gISR']), str(cuts['gMET']), str(cuts['gISR'])))
