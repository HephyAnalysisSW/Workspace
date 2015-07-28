#turnon.py

#def main(gMETcut, gISRcut):

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
#str(weight) + "*(" + ")" 

gMETcut = input("Enter Generated MET cut value: ")
gISRcut = input("Enter Generated ISR Jet pT cut value: ")

cuts=({\
'MET' : 200, #MET cut (fixed)
'ISR' : 110, #ISR/Leading Jet cut (fixed)
'Eta' : 2.4, #eta cut (fixed)

'gMET' : gMETcut, #generated quantity cuts
'gISR' : gISRcut,
'gEta' : 2.5
})

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

###########################################################################Canvas 1: MET (single gen cut)
print makeDoubleLine()
print "                                                     MET (single generator cut):"
print makeDoubleLine()

c1 = ROOT.TCanvas("c1", "MET (1 gen cut)", 1800, 1500)
c1.Divide(1,2)

var = "met_pt"

nbins = 100
min = 0
max = 1000

c1.cd(1)
h1 = drawhist(T2DegSample, var, preSel1, nbins, min, max) #ISR preselection cut
h1.SetName("MET 1")
h1.SetTitle("Generated MET Filter Effect on Reconstructed MET")
h1.GetXaxis().SetTitle("Missing Transverse Energy #slash{E}_{T} / GeV")
h1.Draw()
h1.SetFillColor(ROOT.kRed+1)
h1.SetLineColor(ROOT.kBlack)
h1.SetLineWidth(4)

l1 = makeLegend()
l1.AddEntry("MET 1", "MET (no generator cuts)", "F")

ROOT.gPad.SetLogy()
ROOT.gPad.Update()

alignStats(h1)

h2 = drawhist(T2DegSample, var, preSel1 + "&&" + genSel1) # + genMET cut
h2.SetName("h2")
h2.Draw("same")
h2.SetFillColor(0)
#h3etFillStyle(3001)
h2.SetLineColor(ROOT.kAzure+7)
h2.SetLineWidth(4)

l1.AddEntry("h2", "MET (generator cut)", "F")
l1.Draw()

#Efficiency and Reduction Factor Calculation 
h3 = drawhist(T2DegSample, var, "") #no cuts  
h4 = drawhist(T2DegSample, var, genSel1) #genMET cut
   
eff1 = h4.GetEntries()/h3.GetEntries()
ineff1 = (h3.GetEntries()-h4.GetEntries())/h3.GetEntries() # = 1 - eff1
red1 = h3.GetEntries()/h4.GetEntries() # = 1/eff

#Number of Inefficiencies
#recoCutBin = int(cuts['MET']/(h1.GetXaxis().GetBinWidth(0)))
#numIneff1 = h1.Integral(recoCutBin, max) - h2.Integral(recoCutBin, max) #Integral() in min,max range; Integral(x, 1000000) of total

box1 = makeBox()
box1.AddText("Cuts:")
#box1.AddText("#bf{MET p_{T} cut: }" + str(cuts['MET']) + " GeV")
box1.AddText("#bf{ISR Jet p_{T} cut: }" + str(cuts['ISR']) + " GeV")
box1.AddText("#bf{ISR Jet #eta cut: }" + str(cuts['Eta']))
box1.AddText("#bf{Gen. MET p_{T} cut: }" + str(cuts['gMET']) + " GeV")
#box1.AddText("#bf{Gen. ISR Jet p_{T} cut: }" + str(cuts['gISR']) + " GeV")
#box1.AddText("#bf{Gen. ISR Jet Eta #eta cut: }" + str(cuts['gEta']))
#box1.AddLine(0, 0.5, 1, 0.5)
#box1.AddText("")
box1.AddText("Filter:")
box1.AddText("#bf{Filter Efficiency: }" + str("%0.3f"%eff1))
box1.AddText("#bf{Inefficiencies Fraction: }" + str("%0.3f"%ineff1))
box1.AddText("#bf{Reduction Factor: }" + str("%0.3f"%red1))
box1.Draw()

ROOT.gPad.Update()

#MET Turnon Plot
c1.cd(2)
metTurnon1 = ROOT.TEfficiency(h2, h1) #(passed, total)
metTurnon1.SetTitle("MET Turnon Plot (single generator cut) ; Missing Transverse Energy #slash{E}_{T} / GeV ; Counts")
metTurnon1.SetMarkerColor(ROOT.kBlue)
metTurnon1.SetMarkerStyle(33)
metTurnon1.SetMarkerSize(3)
metTurnon1.Draw("AP") 
metTurnon1.SetLineColor(ROOT.kBlack)
metTurnon1.SetLineWidth(2)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
ROOT.gPad.Update()
metTurnon1.GetPaintedGraph().GetXaxis().SetRangeUser(0,1000) #TEfficiency::GetPaintedGraph()
metTurnon1.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
metTurnon1.GetPaintedGraph().GetXaxis().CenterTitle()
metTurnon1.GetPaintedGraph().GetYaxis().CenterTitle()

#Fitting
fitFunc.SetParameters(0.5, 140, 40, 0.5) #init: (0.5, 140, 40, 0.5)
metTurnon1.Fit(fitFunc)

print makeLine()
print "Filter Efficiency: " + str("%0.3f"%eff1)
print "Inefficiencies Fraction: " + str("%0.3f"%ineff1)
print "Reduction Factor: " + str("%0.3f"%red1)

#Efficiency at Reco Cut
recoEff1_fit = fitFunc(cuts['MET'])
recoEff1_bin = metTurnon1.GetEfficiency(int(cuts['MET']/(h1.GetXaxis().GetBinWidth(0))))
print "Efficiency at Reco MET cut (bin): ", str("%0.3f"%recoEff1_bin)
print "Efficiency at Reco MET cut (fit): ", str("%0.3f"%recoEff1_fit)
#print "Number Inefficiencies after Reco MET cut: ", numIneff1

#Fit Parameter Extraction
fit1 = []
#fitFunc.GetParameters(fit1)
fit1.append(fitFunc.GetChisquare())
for x in xrange(0, 4):
   fit1.append(fitFunc.GetParameter(x))
   fit1.append(fitFunc.GetParError(x))

fit1.append(fitFunc.GetX(0.5))
fit1.append(fitFunc.GetX(0.75))
fit1.append(fitFunc.GetX(0.80))
fit1.append(fitFunc.GetX(0.85))
fit1.append(fitFunc.GetX(0.90))
fit1.append(fitFunc.GetX(0.95))
fit1.append(fitFunc.GetX(0.99))
fit1.append(fitFunc.GetX(1))

#box2.Copy(box1)
box2 = ROOT.TPaveText(box1)
box2.AddText("#bf{Efficiency at Reco Cut (bin): }" + str("%0.3f"%recoEff1_bin))
box2.AddText("#bf{Efficiency at Reco Cut (fit): }" + str("%0.3f"%recoEff1_fit))
#box2.AddText("Inefficiencies after Reco Cut: " + str(numIneff1))
#box2.AddText("              #bf{Plot:}")
#box2.AddEntry(metTurnon1, "MET Turnon Fit (single cut)", "LP")
box2.Draw()

#c1.SetGridx()
c1.Modified()
c1.Update()

########################################################################################Canvas 2: MET (both gen cuts)
print makeDoubleLine()
print "                                                       MET (both generator cuts):"
print makeDoubleLine()

c2 = ROOT.TCanvas("c2", "MET (2 gen cuts)", 1800, 1500)
c2.Divide(1,2)

#var = "met_pt"

#nbins = 100
#min = 0
#max = 1000

c2.cd(1)
h5 = drawhist(T2DegSample, var, preSel1 + "&&" + genSel1) #ISR preselection cut & MET generator cut
h5.SetName("MET 2")
h5.SetTitle("Generated MET & ISR Jet p_{T} Filter Effect on Reconstructed MET")
h5.GetXaxis().SetTitle("Missing Transverse Energy #slash{E}_{T} / GeV")
h5.Draw() 
h5.SetFillColor(ROOT.kRed+1)
h5.SetLineColor(ROOT.kBlack)
h5.SetLineWidth(4)

l2 = makeLegend()
l2.AddEntry("MET 2", "MET (no generator cuts)", "F")

ROOT.gPad.SetLogy()
ROOT.gPad.Update()

alignStats(h5)

h6 = drawhist(T2DegSample, var, preSel1 + "&&" + genSel1 + "&&" + genSel2) # + ISR generator cuts
h6.SetName("h6")
h6.Draw("same")
h6.SetFillColor(0)
#h6.SetFillStyle(3001)
h6.SetLineColor(ROOT.kAzure+7)
h6.SetLineWidth(4)

l2.AddEntry("h6", "MET (both generator cuts)", "F")
l2.Draw()

#Efficiency and Reduction Factor Calculation 
h7 = drawhist(T2DegSample, var, "") #no cuts 
h8 = drawhist(T2DegSample, var, genSel1 + "&&" + genSel2) #both gen cuts

eff2 = h8.GetEntries()/h7.GetEntries()
ineff2 = (h7.GetEntries()-h8.GetEntries())/h7.GetEntries()
red2 = h7.GetEntries()/h8.GetEntries() # = 1/eff

#Number of Inefficiencies
#recoCutBin = int(cuts['MET']/(h7.GetXaxis().GetBinWidth(0)))
#numIneff2 = h7.Integral(recoCutBin, max) - h8.Integral(recoCutBin, max) #Integral() in min,max range; Integral(x, 1000000) of total

box3 = makeBox()
box3.AddText("Cuts:")
#box3.AddText("#bf{MET p_{T} cut: }" + str(cuts['MET']) + " GeV")
box3.AddText("#bf{ISR Jet p_{T} cut: }" + str(cuts['ISR']) + " GeV")
box3.AddText("#bf{ISR Jet #eta cut: }" + str(cuts['Eta']))
box3.AddText("#bf{Gen. MET p_{T} cut: }" + str(cuts['gMET']) + " GeV")
box3.AddText("#bf{Gen. ISR Jet p_{T} cut: }" + str(cuts['gISR']) + " GeV")
box3.AddText("#bf{Gen. ISR Jet #eta cut: }" + str(cuts['gEta']))
box3.AddText("Filter:")
box3.AddText("#bf{Filter Efficiency: }" + str("%0.3f"%eff2))
box3.AddText("#bf{Inefficiencies Fraction: }" + str("%0.3f"%ineff2))
box3.AddText("#bf{Reduction Factor: }" + str("%0.3f"%red2))
box3.Draw()

#MET Turnon Plot
c2.cd(2)
metTurnon2 = ROOT.TEfficiency(h6, h5) #(passed, total)
metTurnon2.SetTitle("MET Turnon Plot (both generator cuts) ; Missing Transverse Energy #slash{E}_{T} / GeV ; Counts")
metTurnon2.SetMarkerColor(ROOT.kBlue)
metTurnon2.SetMarkerStyle(33)
metTurnon2.SetMarkerSize(3)
metTurnon2.Draw("AP") 
metTurnon2.SetLineColor(ROOT.kBlack)
metTurnon2.SetLineWidth(2)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
ROOT.gPad.Update()
metTurnon2.GetPaintedGraph().GetXaxis().SetRangeUser(0,1000) #TEfficiency::GetPaintedGraph()
metTurnon2.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
metTurnon2.GetPaintedGraph().GetXaxis().CenterTitle()
metTurnon2.GetPaintedGraph().GetYaxis().CenterTitle()

#Fitting
metTurnon2.Fit(fitFunc)

print makeLine()
print "Filter Efficiency: " + str("%0.3f"%eff2)
print "Inefficiencies Fraction: " + str("%0.3f"%ineff2)
print "Reduction Factor: " + str("%0.3f"%red2)

#Efficiency at Reco Cut
recoEff2_fit = fitFunc(cuts['MET'])
recoEff2_bin = metTurnon2.GetEfficiency(int(cuts['MET']/(h5.GetXaxis().GetBinWidth(0))))
print "Efficiency at Reco MET cut (bin): ", str("%0.3f"%recoEff2_bin) 
print "Efficiency at Reco MET cut (fit): ", str("%0.3f"%recoEff2_fit)
#print "Number of Inefficiencies after Reco MET cut: ", numIneff2

#Fit Parameter Extraction
fit2 = []
#fitFunc.GetParameters(fit3)
fit2.append(fitFunc.GetChisquare())
for x in xrange(0, 4):
   fit2.append(fitFunc.GetParameter(x))
   fit2.append(fitFunc.GetParError(x))

fit2.append(fitFunc.GetX(0.5))
fit2.append(fitFunc.GetX(0.75))
fit2.append(fitFunc.GetX(0.80))
fit2.append(fitFunc.GetX(0.85))
fit2.append(fitFunc.GetX(0.90))
fit2.append(fitFunc.GetX(0.95))
fit2.append(fitFunc.GetX(0.99))
fit2.append(fitFunc.GetX(1))

#box4.Copy(box3)
box4 = ROOT.TPaveText(box3)
box4.AddText("#bf{Efficiency at Reco Cut (bin): }" + str("%0.3f"%recoEff2_bin))
box4.AddText("#bf{Efficiency at Reco Cut (fit): }" + str("%0.3f"%recoEff2_fit))
#box4.AddText("Inefficiencies after Reco Cut: " + str(numIneff2))
#box4.AddText("              #bf{Plot:}")
#box4.AddEntry(metTurnon1, "MET Turnon Fit (both cuts)", "LP")
box4.Draw()

#c2.SetGridx()
c2.Modified()
c2.Update()

#################################################################Canvas 3: Jet Pt (single gen cut)
print makeDoubleLine()
print "                                              ISR Jet pT (single generator cut):"
print makeDoubleLine()

c3 = ROOT.TCanvas("c3", "ISR Jet (1 gen cut)", 1800, 1500)
c3.Divide(1,2)

var = "Max$(Jet_pt*(abs(Jet_eta)<" + str(cuts['Eta']) + "))" #Leading JET pt with eta < 2.4

#nbins = 100
#min = 0
#max = 1000

c3.cd(1)
h9 = drawhist(T2DegSample, var, preSel2) #MET preselection cut
h9.SetName("ISR 1")
h9.SetTitle("Generated ISR Jet p_{T} Filter Effect on Reconstructed ISR Jet p_{T}")
h9.GetXaxis().SetTitle("ISR Jet p_{T} / GeV")
h9.Draw()
h9.SetFillColor(ROOT.kRed+1)
h9.SetLineColor(ROOT.kBlack)
h9.SetLineWidth(4)

l3 = makeLegend()
l3.AddEntry("ISR 1", "ISR Jet p_{T} (no generator cuts)", "F")

ROOT.gPad.SetLogy()
ROOT.gPad.Update()

alignStats(h9)

h10 = drawhist(T2DegSample, var, preSel2 + "&&" + genSel2) # + ISR generator cut
h10.SetName("h10")
h10.Draw("same")
h10.SetFillColor(0)
#h10.SetFillStyle(3001)
h10.SetLineColor(ROOT.kAzure+7)
h10.SetLineWidth(4)

l3.AddEntry("h10", "ISR Jet p_{T} (generator cut)", "F")
l3.Draw()

#Efficiency and Reduction Factor Calculation 
h11 = drawhist(T2DegSample, var, "") #no cuts 
h12 = drawhist(T2DegSample, var, genSel2) #gISR cut

eff3 = h12.GetEntries()/h11.GetEntries()
ineff3 = (h11.GetEntries()-h12.GetEntries())/h11.GetEntries()
red3 = h11.GetEntries()/h12.GetEntries() # = 1/eff

#Number of Inefficiencies
#recoCutBin = int(cuts['MET']/(h3.GetXaxis().GetBinWidth(0)))
#numIneff3 = h9.Integral(recoCutBin, max) - h10.Integral(recoCutBin, max) #Integral() in min,max range; Integral(x, 1000000) of total

box5 = makeBox()
box5.AddText("Cuts:")
box5.AddText("#bf{MET p_{T} cut: }" + str(cuts['MET']) + " GeV")
#box5.AddText("#bf{ISR Jet p_{T} cut: }" + str(cuts['ISR']) + " GeV")
#box5.AddText("#bf{ISR Jet #eta cut: }" + str(cuts['Eta']))
#box5.AddText("#bf{Gen. MET p_{T} cut: }" + str(cuts['gMET']) + " GeV")
box5.AddText("#bf{Gen. ISR Jet p_{T} cut: }" + str(cuts['gISR']) + " GeV")
box5.AddText("#bf{Gen. ISR Jet #eta cut: }" + str(cuts['gEta']))
box5.AddText("Filter:")
box5.AddText("#bf{Filter Efficiency: }" + str("%0.3f"%eff3))
box5.AddText("#bf{Inefficiencies Fraction: }" + str("%0.3f"%ineff3))
box5.AddText("#bf{Reduction Factor: }" + str("%0.3f"%red3))
box5.Draw()

#Jet Turnon Plot
c3.cd(2)
jetTurnon1 = ROOT.TEfficiency(h10, h9)
jetTurnon1.SetTitle("ISR Jet p_{T} Turnon Plot (single generator cut) ; ISR Jet p_{T} / GeV ; Counts")
jetTurnon1.SetMarkerColor(ROOT.kBlue)
jetTurnon1.SetMarkerStyle(33)
jetTurnon1.SetMarkerSize(3)
jetTurnon1.Draw("AP") 
jetTurnon1.SetLineColor(ROOT.kBlack)
jetTurnon1.SetLineWidth(2)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
ROOT.gPad.Update()
jetTurnon1.GetPaintedGraph().GetXaxis().SetRangeUser(0,1000) #TEfficiency::GetPaintedGraph()
jetTurnon1.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
jetTurnon1.GetPaintedGraph().GetXaxis().CenterTitle()
jetTurnon1.GetPaintedGraph().GetYaxis().CenterTitle()

#Fitting
fitFunc.SetParameters(0.45, 70, 20, 0.6) #init: (0.45,60,20,0.6)
#fitFunc.SetParLimits(1, 0, 120) #init: [0,120]
jetTurnon1.Fit(fitFunc)

print makeLine()
print "Filter Efficiency: " + str("%0.3f"%eff3)
print "Reduction Factor: " + str("%0.3f"%red3)
print "Inefficiencies Fraction: " + str("%0.3f"%ineff3)

#Efficiency at Reco Cut
recoEff3_bin = jetTurnon1.GetEfficiency(int(cuts['MET']/(h9.GetXaxis().GetBinWidth(0))))
recoEff3_fit = fitFunc(cuts['ISR'])
print "Efficiency at Reco ISR Jet pT cut (bin): ", str("%0.3f"%recoEff3_bin) 
print "Efficiency at Reco ISR Jet pT cut (fit): ", str("%0.3f"%recoEff3_fit)
#print "Number of Inefficiencies after Reco ISR Jet pT cut: ", numIneff3

#Fit Parameter Extraction
fit3 = []
#fitFunc.GetParameters(fit2)
fit3.append(fitFunc.GetChisquare())
for x in xrange(0, 4):
   fit3.append(fitFunc.GetParameter(x))
   fit3.append(fitFunc.GetParError(x))

fit3.append(fitFunc.GetX(0.5))
fit3.append(fitFunc.GetX(0.75))
fit3.append(fitFunc.GetX(0.80))
fit3.append(fitFunc.GetX(0.85))
fit3.append(fitFunc.GetX(0.90))
fit3.append(fitFunc.GetX(0.95))
fit3.append(fitFunc.GetX(0.99))
fit3.append(fitFunc.GetX(1))

#box6.Copy(box1)
box6 = ROOT.TPaveText(box5)
box6.AddText("#bf{Efficiency at Reco Cut (bin): }" + str("%0.3f"%recoEff2_bin))
box6.AddText("#bf{Efficiency at Reco Cut (fit): }" + str("%0.3f"%recoEff2_fit))
#box6.AddText("Inefficiencies after Reco Cut: " + str(numIneff3))
#box6.AddText("              #bf{Plot:}")
#box6.AddEntry(jetTurnon1, "ISR Turnon Fit (single cut)", "LP")
box6.Draw()

#c3.SetGridx()
c3.Modified()
c3.Update() 

###############################################################################Canvas 4: Jet Pt (both gen cuts)
print makeDoubleLine()
print "                                                         ISR Jet pT (both generator cuts):"
print makeDoubleLine()

c4 = ROOT.TCanvas("c4", "ISR Jet (2 gen cuts)", 1800, 1500)
c4.Divide(1,2)

#var = "Max$(Jet_pt*(abs(Jet_eta)<" + str(cuts['Eta']) + "))" #Leading JET (highest pT) with eta < 2.4 

#nbins = 100
#min = 0
#max = 1000

c4.cd(1)
h13 = drawhist(T2DegSample, var, preSel2 + "&&" + genSel2) #MET preselection cut + ISR generator cut
h13.SetName("ISR 2")
h13.SetTitle("Generated ISR Jet p_{T} & MET Filter Effect on Reconstructed ISR Jet p_{T}")
h13.GetXaxis().SetTitle("ISR Jet p_{T} / GeV")
h13.Draw() #MET preselection cut
h13.SetFillColor(ROOT.kRed+1)
h13.SetLineColor(ROOT.kBlack)
h13.SetLineWidth(4)

l4 = makeLegend()
l4.AddEntry("ISR 2", "ISR Jet p_{T} (no generator cuts)", "F")

ROOT.gPad.SetLogy()
ROOT.gPad.Update()

alignStats(h13)

h14 = drawhist(T2DegSample, var, preSel2 + "&&" + genSel2 + "&&" + genSel1) # + MET generator cut
h14.SetName("h14")
h14.Draw("same")
h14.SetFillColor(0)
#h14.SetFillStyle(3001)
h14.SetLineColor(ROOT.kAzure+7)
h14.SetLineWidth(4)

l4.AddEntry("h14", "ISR Jet p_{T} (both generator cuts)", "F")
l4.Draw()

#Efficiency and Reduction Factor Calculation 
h15 = drawhist(T2DegSample, var, "") #no cuts
h16 = drawhist(T2DegSample, var, genSel2 + "&&" + genSel1) #both gen cuts

eff4 = h16.GetEntries()/h15.GetEntries()
ineff4 = (h15.GetEntries()-h16.GetEntries())/h15.GetEntries()
red4 = h15.GetEntries()/h16.GetEntries() # = 1/eff

#Number of Inefficiencies
#recoCutBin = int(cuts['MET']/(h15.GetXaxis().GetBinWidth(0)))
#numIneff4 = h15.Integral(recoCutBin, max) - h16.Integral(recoCutBin, max) #Integral() in min,max range; Integral(x, 1000000) of total

box7 = makeBox()
box7.AddText("Cuts:")
box7.AddText("#bf{MET p_{T} cut: }" + str(cuts['MET']) + " GeV")
#box7.AddText("#bf{ISR Jet p_{T} cut: }" + str(cuts['ISR']) + " GeV")
#box7.AddText("#bf{ISR Jet Eta #eta cut: }" + str(cuts['Eta']))
box7.AddText("#bf{Gen. MET p_{T} cut: }" + str(cuts['gMET']) + " GeV")
box7.AddText("#bf{Gen. ISR Jet p_{T} cut: }" + str(cuts['gISR']) + " GeV")
box7.AddText("#bf{Gen. ISR Jet #eta cut: }" + str(cuts['gEta']))
box7.AddText("Filter:")
box7.AddText("#bf{Filter Efficiency: }" + str("%0.3f"%eff4))
box7.AddText("#bf{Inefficiencies Fraction }" + str("%0.3f"%ineff4))
box7.AddText("#bf{Reduction Factor: }" + str("%0.3f"%red4))
box7.Draw()

#Jet Turnon Plot
c4.cd(2)
jetTurnon2 = ROOT.TEfficiency(h14, h13) #(passed, total)
jetTurnon2.SetTitle("ISR Jet p_{T} Turnon Plot (both generator cuts) ; ISR Jet p_{T} / GeV ; Counts")
jetTurnon2.SetMarkerColor(ROOT.kBlue)
jetTurnon2.SetMarkerStyle(33)
jetTurnon2.SetMarkerSize(3)
jetTurnon2.Draw("AP") #L/C option for curve | * - Star markers #X - no error bars
jetTurnon2.SetLineColor(ROOT.kBlack)
jetTurnon2.SetLineWidth(2)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
ROOT.gPad.Update()
jetTurnon2.GetPaintedGraph().GetXaxis().SetRangeUser(0,1000) #TEfficiency::GetPaintedGraph()
jetTurnon2.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
jetTurnon2.GetPaintedGraph().GetXaxis().CenterTitle()
jetTurnon2.GetPaintedGraph().GetYaxis().CenterTitle()

#Fitting
#fitFunc.SetParameters(0.45, 60, 20, 0.6) #init: (0.45,60,20,0.6)
#fitFunc.SetParLimits(2, 10, 16)
jetTurnon2.Fit(fitFunc)

print makeLine()
print "Filter Efficiency: " + str("%0.3f"%eff4)
print "Reduction Factor: " + str("%0.3f"%red4)
print "Inefficiencies Fraction: " + str("%0.3f"%ineff4)

#Efficiency at Reco Cut
recoEff4_bin = jetTurnon2.GetEfficiency(int(cuts['MET']/(h13.GetXaxis().GetBinWidth(0))))
recoEff4_fit = fitFunc(cuts['ISR'])
print "Efficiency at Reco ISR Jet pT cut (bin): ", str("%0.3f"%recoEff4_bin)
print "Efficiency at Reco ISR Jet pT cut (fit): ", str("%0.3f"%recoEff4_fit)
#print "Number of Inefficiencies after Reco ISR Jet pT cut: ", numIneff4
print makeLine()

#Fit Parameter Extraction
fit4 = []
#fitFunc.GetParameters(fit4)
fit4.append(fitFunc.GetChisquare())
for x in xrange(0, 4):
   fit4.append(fitFunc.GetParameter(x))
   fit4.append(fitFunc.GetParError(x))

fit4.append(fitFunc.GetX(0.5))
fit4.append(fitFunc.GetX(0.75))
fit4.append(fitFunc.GetX(0.80))
fit4.append(fitFunc.GetX(0.85))
fit4.append(fitFunc.GetX(0.90))
fit4.append(fitFunc.GetX(0.95))
fit4.append(fitFunc.GetX(0.99))
fit4.append(fitFunc.GetX(1))

#box8.Copy(box1)
box8 = ROOT.TPaveText(box7)
box8.AddText("#bf{Efficiency at Reco Cut (bin): }" + str("%0.3f"%recoEff4_bin))
box8.AddText("#bf{Efficiency at Reco Cut (fit): }" + str("%0.3f"%recoEff4_fit))
#box8.AddText("Inefficiencies after Reco Cut: " + str(numIneff4))
#box8.AddText("              #bf{Plot:}")
#box8.AddEntry(jetTurnon2, "ISR Turnon Fit (both cuts)", "LP")
box8.Draw()

#c4.SetGridx()
c4.Modified()
c4.Update() 

#Write to file
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/filter/filter_%s_%s"%(str(cuts["gMET"]),str(cuts["gISR"])) #web directory http://www.hephy.at/user/mzarucki/plots/filter/

if not os.path.exists(savedir):
   os.makedirs(savedir)

outfile1 = open(savedir + "/filterResults_%s_%s.txt"%(str(cuts["gMET"]),str(cuts["gISR"])), "w")
print >> outfile1, "Generator Filter Results", "\n", makeLine(), "\n", cutString, "\n", makeLine(), "\n", \
"Variable", "         ", "Filter Efficiency", "   ", "Inefficiencies Fraction", "   ", "Reduction Factor", "  ", "Efficiency at Reco Cut (bin)","   ", "Efficiency at Reco Cut (fit)", "\n\n", \
"MET (1 cut)", "        ", eff1,"     ", ineff1, "          ", red1, "      ", recoEff1_bin, "                ", recoEff1_fit, "\n\n", \
"MET (2 cuts)", "       ", eff2, "     ", ineff2, "         ", red2, "      ", recoEff2_bin, "                ", recoEff2_fit, "\n\n", \
"ISR Jet pT (1 cut)", " ", eff3, "     ", ineff3, "          ", red3, "       ", recoEff3_bin, "               ", recoEff3_fit, "\n\n", \
"ISR Jet pT (2 cuts)", "", eff4, "     ", ineff4, "         ", red4, "      ", recoEff4_bin, "                ", recoEff4_fit, "\n", \
makeLine(), "\n", \
"Turnon fit results:", "\n\n", \
" ", "ChiSquared", "   ", fitFunc.GetParName(0), "  ", fitFunc.GetParName(0) + "_Err", "    ", fitFunc.GetParName(1), "        ", \
fitFunc.GetParName(1) + "_Err", "     ", fitFunc.GetParName(2), "    ", fitFunc.GetParName(2) + "_Err", "   ", \
fitFunc.GetParName(3), "   ", fitFunc.GetParName(3) + "_Err", "\n\n", \
fit1[0], " ", fit1[1], " ", fit1[2], " ", fit1[3], " ", fit1[4], " ", fit1[5], " ", fit1[6], " ", fit1[7], " ", fit1[8], "\n\n", \
fit2[0], " ", fit2[1], " ", fit2[2], " ", fit2[3], " ", fit2[4], " ", fit2[5], " ", fit2[6], " ", fit2[7], " ", fit2[8], "\n\n", \
fit3[0], " ", fit3[1], " ", fit3[2], " ", fit3[3], " ", fit3[4], " ", fit3[5], " ", fit3[6], " ", fit3[7], " ", fit3[8], "\n\n", \
fit4[0], " ", fit4[1], " ", fit4[2], " ", fit4[3], " ", fit4[4], " ", fit4[5], " ", fit4[6], " ", fit4[7], " ", fit4[8], "\n", \
makeLine(), "\n", \
"Variable values for various efficiecies:", "\n\n", \
"     Efficiency             50%           75%            80%           85%           90%           95%           99%          100%", "\n\n", \
"MET (1 cut)          ", fit1[9], fit1[10], fit1[11], fit1[12], fit1[13], fit1[14], fit1[15], fit1[16], "\n\n", \
"MET (2 cuts)         ", fit2[9], fit2[10], fit2[11], fit2[12], fit2[13], fit2[14], fit2[15], fit2[16], "\n\n", \
"ISR Jet pT (1 cut)   ", fit3[9], fit3[10], fit3[11], fit3[12], fit3[13], fit3[14], fit3[15], fit3[16], "\n\n", \
"ISR Jet pT (2 cuts)  ", fit4[9], fit4[10], fit4[11], fit4[12], fit4[13], fit4[14], fit4[15], fit4[16]
outfile1.close()

outfile2 = open(savedir + "/reductionEfficiency_%s_%s.txt"%(str(cuts["gMET"]),str(cuts["gISR"])), "w")
outfile2.write(\
"gMET Cut" + "   " + "gISR Cut" + "   " + "MET 1 Red. Factor" + "   " + "MET 1 Reco Eff." + "   " + "MET 2 Red. Factor" + "   " + "MET 2 Reco Eff." + "   " + "ISR 1 Red. Factor" + "   " + "ISR 1 Reco Eff." + "   " + "ISR 2 Red. Factor" + "   " + "ISR 2 Reco Eff." + "\n" +\
str(cuts["gMET"]) + "        " + str(cuts["gISR"]) + "         " + str(red1) + "      " + str(recoEff1_bin) + "      " + str(red2) + "      " + str(recoEff2_bin) + "      " + str(red3) + "      " + str(recoEff3_bin) + "      " + str(red4) + "      " + str(recoEff4_bin)\
)
outfile2.close()


#outfile.write("")

#Save to Web
#c1.SaveAs(savedir + "/MET1_%s_%s.root"%( str(cuts['gMET']), str(cuts['gISR'])))
#c2.SaveAs(savedir + "/MET2_%s_%s.root"%(str(cuts['gMET']), str(cuts['gISR'])))
#c3.SaveAs(savedir + "/ISR1_%s_%s.root"%(str(cuts['gMET']), str(cuts['gISR'])))
#c4.SaveAs(savedir + "/ISR2_%s_%s.root"%(str(cuts['gMET']), str(cuts['gISR'])))
#
#c1.SaveAs(savedir + "/MET1_%s_%s.png"%(str(cuts['gMET']), str(cuts['gISR'])))
#c2.SaveAs(savedir + "/MET2_%s_%s.png"%(str(cuts['gMET']), str(cuts['gISR'])))
#c3.SaveAs(savedir + "/ISR1_%s_%s.png"%(str(cuts['gMET']), str(cuts['gISR'])))
#c4.SaveAs(savedir + "/ISR2_%s_%s.png"%(str(cuts['gMET']), str(cuts['gISR'])))
#
#c1.SaveAs(savedir + "/MET1_%s_%s.pdf"%(str(cuts['gMET']), str(cuts['gISR'])))
#c2.SaveAs(savedir + "/MET2_%s_%s.pdf"%(str(cuts['gMET']), str(cuts['gISR'])))
#c3.SaveAs(savedir + "/ISR1_%s_%s.pdf"%(str(cuts['gMET']), str(cuts['gISR'])))
#c4.SaveAs(savedir + "/ISR2_%s_%s.pdf"%(str(cuts['gMET']), str(cuts['gISR'])))

#if __name__ == '__main__':
#   sys.exit(main(sys.argv[1], sys.argv[2]))
