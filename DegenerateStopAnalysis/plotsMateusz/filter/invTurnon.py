#invTurnon.py
print "\nExecuting invTurnon.py script..."

import ROOT
import os

from Workspace.HEPHYPythonTools.helpers import getChain#, getPlotFromChain, getYieldFromChain, getChunks

#ROOT Options
ROOT.gROOT.Reset() #re-initialises ROOT
#ROOT.gROOT.SetStyle("Plain")

ROOT.gStyle.SetOptStat(0) #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis
#ROOT.gStyle.SetOptFit(1111) #1111 prints fits results on plot
#ROOT.gStyle.SetTitleX(0.15)
#ROOT.gStyle.SetFuncWidth(1)
#ROOT.gStyle.SetFuncColor(9)
#ROOT.gStyle.SetLineWidth(2)
#ROOT.gStyle.SetOptTitle(0) #suppresses title box

ROOT.gStyle.SetPaintTextFormat("4.2f")
#ROOT.gStyle->SetTitleX(0.1)
#ROOT.gStyle->SetTitleW(0.8)

ROOT.gStyle.SetStatX(0.65)
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

def drawhist(sample, varname, sel):
   #hist = ROOT.TH1F("signalMET","Histogram",1000,0,1000)
   sample.Draw(varname + ">>hname(100, 0, 1000)", sel, "goff")
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
def select(varname, cut, option): #option = {>, =, <}
   sel = "abs(" + varname + option + str(cut) + ")"
   return sel

#Creates Legend
def makeLegend():
   leg = ROOT.TLegend(0.60,0.70,0.85,0.85)
   leg.SetHeader("#bf{Legend}")
   header = leg.GetListOfPrimitives().First()
   header.SetTextAlign(22)
   return leg 

#Creates Box 
def makeBox():
   box = ROOT.TLegend(0.70,0.40,0.875,0.65)
   #box.SetHeader("Cuts")
   #header = box.GetListOfPrimitives().First()
   #header.SetTextAlign(22)
   return box 

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
fitFunc.SetParLimits(1, 0, 200)
fitFunc.SetParLimits(2, 0, 60)
#fitFunc.SetParLimits(3, 0.45, 0.8)

#Selection
#weight = 1
#str(weight) + "*(" + ")" 

cuts=({\
'MET' : 200, #MET cut (fixed)
'ISR' : 110, #ISR/Leading Jet cut (fixed)
'Eta' : 2.4, #eta cut (fixed)

'gMET' : 10, #generated quantity cuts
'gISR' : 20,
'gEta' : 2.6
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

c1 = ROOT.TCanvas("c1", "MET (1 reco cut)", 1800, 1500)
c1.Divide(1,2)

var = "met_genPt"
c1.cd(1)
h1 = drawhist(T2DegSample, var, genSel2) #ISR preselection cut
h1.SetName("h1")
h1.SetTitle("Reconstructed MET Filter Effect on Generated MET (Inverted)")
h1.GetXaxis().SetTitle("Generated Missing Transverse Energy #slash{E}_{T} / GeV")
h1.Draw()
h1.SetFillColor(ROOT.kRed+1)
h1.SetLineColor(ROOT.kBlack)
h1.SetLineWidth(4)
l1 = makeLegend()
l1.AddEntry("h1", "Gen. MET (no reco cuts)", "F")

h2 = drawhist(T2DegSample, var, genSel2 + "&&" + preSel2) # + reco cut
h2.SetName("h2")
h2.Draw("same")
h2.SetFillColor(0)
#h2.SetFillStyle(3001)
h2.SetLineColor(ROOT.kAzure+7)
h2.SetLineWidth(4)
l1.AddEntry("h2", "Gen. MET (reco cut)", "F")
l1.Draw()

ROOT.gPad.SetLogy()

#Reduction Factor
eff1 = h2.GetEntries()/h1.GetEntries()
red1 = (h1.GetEntries()-h2.GetEntries())/h1.GetEntries()

box1 = makeBox()
box1.AddEntry("","             #bf{Cuts:}","")
box1.AddEntry(0, "MET p_{T} cut: " + str(cuts['MET']) + " GeV", "")
#box1.AddEntry(0, "ISR Jet p_{T} cut: " + str(cuts['ISR']) + " GeV", "")
#box1.AddEntry(0, "ISR Jet #eta cut: " + str(cuts['Eta']), "")
#box1.AddEntry(0, "Gen. MET p_{T} cut: " + str(cuts['gMET']) + " GeV", "")
box1.AddEntry(0, "Gen. ISR Jet p_{T} cut: " + str(cuts['gISR']) + " GeV", "")
box1.AddEntry(0, "Gen. ISR Jet Eta #eta cut: " + str(cuts['gEta']), "")
box1.AddEntry("","             #bf{Filter:}","")
box1.AddEntry("", "Filter Efficiency: " + str("%0.3f"%eff1), "")
box1.AddEntry("", "Reduction Factor: " + str("%0.3f"%red1), "")
box1.Draw()

#MET Inverse Turnon Plot
c1.cd(2)
metTurnon1 = ROOT.TEfficiency(h2, h1) #(passed, total)
metTurnon1.SetTitle("Inverse MET Turnon Plot (single generator cut) ; Generated Missing Transverse Energy #slash{E}_{T} / GeV ; Counts")
metTurnon1.SetMarkerColor(ROOT.kBlue)
metTurnon1.SetMarkerStyle(33)
metTurnon1.SetMarkerSize(3)
metTurnon1.Draw("AP") 
metTurnon1.SetLineColor(ROOT.kBlack)
metTurnon1.SetLineWidth(2)
ROOT.gPad.SetGridx(1)
ROOT.gPad.Update()
metTurnon1.GetPaintedGraph().GetXaxis().SetRangeUser(0,1000) #TEfficiency::GetPaintedGraph()
metTurnon1.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
metTurnon1.GetPaintedGraph().GetXaxis().CenterTitle()
metTurnon1.GetPaintedGraph().GetYaxis().CenterTitle()

#Fitting
fitFunc.SetParameters(0.5, 200, 40, 0.5)
metTurnon1.Fit(fitFunc)

print makeLine()
print "Filter Efficiency: " + str("%0.3f"%eff1)
print "Reduction Factor: " + str("%0.3f"%red1)

#Efficiency at Reco Cut
recoEff1 = fitFunc(cuts['MET'])
print "Efficiency at Reco MET cut: ", recoEff1 #metTurnon1.GetEfficiency(nbin)

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

#box5 = makeBox()
#box5.Copy(box1)
box5 = ROOT.TLegend(box1)
box5.AddEntry("","Efficiency at " + str(cuts['MET']) + " GeV (reco cut): " + str("%0.3f"%recoEff1),"")
box5.AddEntry("","              #bf{Plot:}","")
box5.AddEntry(metTurnon1, "Inverse MET Turnon Fit (single cut)", "LP")	
box5.Draw()

#c1.SetGridx()
c1.Modified()
c1.Update()

########################################################################################Canvas 2: MET (both gen cuts)
print makeDoubleLine()
print "                                                       MET (both generator cuts):"
print makeDoubleLine()

c3 = ROOT.TCanvas("c3", "MET (2 reco cuts)", 1800, 1500)
c3.Divide(1,2)

var = "met_genPt"
c3.cd(1)
h5 = h1.Clone()
h5.SetName("h5")
h5.SetTitle("Reconstructed MET & ISR Jet p_{T} Filter Effect on Generated MET (Inverted)")
h5.Draw() #ISR preselection cut
#h5.SetFillColor(ROOT.kRed+1)
#h5.SetLineColor(ROOT.kBlack)
#h5.SetLineWidth(4)
l3 = makeLegend()
l3.AddEntry("h5", "Gen. MET (no reco cuts)", "F")

h6 = drawhist(T2DegSample, var, genSel2 + "&&" + preSel2 + "&&" + preSel1) # + both MET and ISR generator cuts
h6.SetName("h6")
h6.Draw("same")
h6.SetFillColor(0)
#h6.SetFillStyle(3001)
h6.SetLineColor(ROOT.kAzure+7)
h6.SetLineWidth(4)
l3.AddEntry("h6", "Gen. MET (both reco cuts)", "F")
l3.Draw()

ROOT.gPad.SetLogy()

#Reduction Factor
eff3 = h6.GetEntries()/h5.GetEntries()
red3 = (h5.GetEntries()-h6.GetEntries())/h5.GetEntries()

box3 = makeBox()
box3.AddEntry("","             #bf{Cuts:}","")
box3.AddEntry(0, "MET p_{T} cut: " + str(cuts['MET']) + " GeV", "")
box3.AddEntry(0, "ISR Jet p_{T} cut: " + str(cuts['ISR']) + " GeV", "")
box3.AddEntry(0, "ISR Jet #eta cut: " + str(cuts['Eta']), "")
#box3.AddEntry(0, "Gen. MET p_{T} cut: " + str(cuts['gMET']) + " GeV", "")
box3.AddEntry(0, "Gen. ISR Jet p_{T} cut: " + str(cuts['gISR']) + " GeV", "")
box3.AddEntry(0, "Gen. ISR Jet #eta cut: " + str(cuts['gEta']), "")
box3.AddEntry("","             #bf{Filter:}","")
box3.AddEntry("", "Filter Efficiency: " + str("%0.3f"%eff3), "")
box3.AddEntry("", "Reduction Factor: " + str("%0.3f"%red3), "")
box3.Draw()

#MET Turnon Plot
c3.cd(2)
metTurnon2 = ROOT.TEfficiency(h6, h5) #(passed, total)
metTurnon2.SetTitle("MET Inverse Turnon Plot (both generator cuts) ; Generated Missing Transverse Energy #slash{E}_{T} / GeV ; Counts")
metTurnon2.SetMarkerColor(ROOT.kBlue)
metTurnon2.SetMarkerStyle(33)
metTurnon2.SetMarkerSize(3)
metTurnon2.Draw("AP") 
metTurnon2.SetLineColor(ROOT.kBlack)
metTurnon2.SetLineWidth(2)
ROOT.gPad.SetGridx()
ROOT.gPad.Update()
metTurnon2.GetPaintedGraph().GetXaxis().SetRangeUser(0,1000) #TEfficiency::GetPaintedGraph()
metTurnon2.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
metTurnon2.GetPaintedGraph().GetXaxis().CenterTitle()
metTurnon2.GetPaintedGraph().GetYaxis().CenterTitle()

#Fitting
fitFunc.SetParameters(0.5, 200, 40, 0.5)
metTurnon2.Fit(fitFunc)
print makeLine()
print "Filter Efficiency: " + str("%0.3f"%eff3)
print "Reduction Factor: " + str("%0.3f"%red3)
#print "Reduction Factor: " + str(1 - eff3)

#Efficiency at Reco Cut
recoEff2 = fitFunc(cuts['MET'])
print "Efficiency at Reco MET cut: ", recoEff2 #metTurnon2.GetEfficiency(nbin)

#Fit Parameter Extraction
fit3 = []
#fitFunc.GetParameters(fit3)
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

#box7 = makeBox()
box7 = ROOT.TLegend(box3)
box7.AddEntry("","Efficiency at " + str(cuts['MET']) + " GeV (reco cut): " + str("%0.3f"%recoEff2),"")
box7.AddEntry("","              #bf{Plot:}","")
box7.AddEntry(metTurnon2, "MET Inverse Turnon Fit (both cuts)", "LP")
#box7.Copy(box1)
box7.Draw()

#c3.SetGridx()
c3.Modified()
c3.Update()

#################################################################Canvas 3: Jet Pt (single gen cut)
print makeDoubleLine()
print "                                              ISR Jet pT (single generator cut):"
print makeDoubleLine()

c2 = ROOT.TCanvas("c2", "ISR Jet (1 reco cut)", 1800, 1500)
c2.Divide(1,2)

var = "Max$(GenJet_pt*(abs(GenJet_eta)<" + str(cuts['gEta']) + "))" #Leading JET pt with eta < 2.4
c2.cd(1)
h3 = drawhist(T2DegSample, var, genSel1) #MET preselection cut
h3.SetName("h3")
h3.SetTitle("Reconstructed ISR Jet p_{T} Filter Effect on Generated ISR Jet p_{T} (Inverted)")
h3.GetXaxis().SetTitle("Generated Jet p_{T} / GeV")
h3.Draw()
h3.SetFillColor(ROOT.kRed+1)
h3.SetLineColor(ROOT.kBlack)
h3.SetLineWidth(4)
l2 = makeLegend()
l2.AddEntry("h3", "Gen. ISR Jet p_{T} (no reco cuts)", "F")

h4 = drawhist(T2DegSample, var, genSel1 + "&&" + preSel1) # + ISR generator cut
h4.SetName("h4")
h4.Draw("same")
h4.SetFillColor(0)
#h4.SetFillStyle(3001)
h4.SetLineColor(ROOT.kAzure+7)
h4.SetLineWidth(4)
l2.AddEntry("h4", "Gen. ISR Jet p_{T} (reco cut)", "F")
l2.Draw()

ROOT.gPad.SetLogy()

#Reduction Factor
eff2 = h4.GetEntries()/h3.GetEntries()
red2 = (h3.GetEntries()-h4.GetEntries())/h3.GetEntries()

box2 = makeBox()
box2.AddEntry("","             #bf{Cuts:}","")
#box2.AddEntry(0, "MET p_{T} cut: " + str(cuts['MET']) + " GeV", "")
box2.AddEntry(0, "ISR Jet p_{T} cut: " + str(cuts['ISR']) + " GeV", "")
box2.AddEntry(0, "ISR Jet #eta cut: " + str(cuts['Eta']), "")
box2.AddEntry(0, "Gen. MET p_{T} cut: " + str(cuts['gMET']) + " GeV", "")
#box2.AddEntry(0, "Gen. ISR Jet p_{T} cut: " + str(cuts['gISR']) + " GeV", "")
#box2.AddEntry(0, "Gen. ISR Jet #eta cut: " + str(cuts['gEta']), "")
box2.AddEntry("", "             #bf{Filter:}","")
box2.AddEntry("", "Filter Efficiency: " + str("%0.3f"%eff2), "")
box2.AddEntry("", "Reduction Factor: " + str("%0.3f"%red2), "")
box2.Draw()

#Jet Turnon Plot
c2.cd(2)
jetTurnon1 = ROOT.TEfficiency(h4, h3)
jetTurnon1.SetTitle("ISR Jet p_{T} Inverse Turnon Plot (single generator cut) ; Generated ISR Jet p_{T} / GeV ; Counts")
jetTurnon1.SetMarkerColor(ROOT.kBlue)
jetTurnon1.SetMarkerStyle(33)
jetTurnon1.SetMarkerSize(3)
jetTurnon1.Draw("AP") 
jetTurnon1.SetLineColor(ROOT.kBlack)
jetTurnon1.SetLineWidth(2)
ROOT.gPad.SetGridx()
ROOT.gPad.Update()
jetTurnon1.GetPaintedGraph().GetXaxis().SetRangeUser(0,1000) #TEfficiency::GetPaintedGraph()
jetTurnon1.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
jetTurnon1.GetPaintedGraph().GetXaxis().CenterTitle()
jetTurnon1.GetPaintedGraph().GetYaxis().CenterTitle()

#Fitting
fitFunc.SetParameters(0.5, 100, 20, 0.5)
fitFunc.SetParLimits(1, 0, 120)
jetTurnon1.Fit(fitFunc)

print makeLine()
print "Filter Efficiency: " + str("%0.3f"%eff1)
print "Reduction Factor: " + str("%0.3f"%red1)
#print "Reduction Factor: " + str(1 - eff1)

#Efficiency at Reco Cut
recoEff3 = fitFunc(cuts['ISR'])
print "Efficiency at Reco ISR Jet pT cut: ", recoEff3 #jetTurnon1.GetEfficiency(nbin)

#Fit Parameter Extraction
fit2 = []
#fitFunc.GetParameters(fit2)
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

#box6 = makeBox()
box6 = ROOT.TLegend(box2)
box6.AddEntry("","Efficiency at " + str(cuts['ISR']) + " GeV (reco cut): " + str("%0.3f"%recoEff3),"")
box6.AddEntry("","              #bf{Plot:}","")
box6.AddEntry(jetTurnon1, "ISR Inverse Turnon Fit (single cut)", "LP")
#box6.Copy(box1)
box6.Draw()

#c2.SetGridx()
c2.Modified()
c2.Update() 

###############################################################################Canvas 4: Jet Pt (both gen cuts)
print makeDoubleLine()
print "                                                         ISR Jet pT (both generator cuts):"
print makeDoubleLine()

c4 = ROOT.TCanvas("c4", "ISR Jet (2 reco cuts)", 1800, 1500)
c4.Divide(1,2)

var = "Max$(GenJet_pt*(abs(GenJet_eta)<" + str(cuts['Eta']) + "))" #Leading JET pt with eta < 2.4 
c4.cd(1)
h7 = h3.Clone()
h7.SetName("h7")
h7.SetTitle("Reconstructed ISR Jet p_{T} & MET Filter Effect on Generated ISR Jet p_{T} (Inverted)")
h7.Draw() #MET preselection cut
#h3.SetFillColor(ROOT.kRed+1)
#h3.SetLineColor(ROOT.kBlack)
#h3.SetLineWidth(4)
l4 = makeLegend()
l4.AddEntry("h7", "Gen. ISR Jet p_{T} (no reco cuts)", "F")

h8 = drawhist(T2DegSample, var, genSel1 + "&&" + preSel1 + "&&" + preSel2) # + both ISR and MET generator cuts
h8.SetName("h8")
h8.Draw("same")
h8.SetFillColor(0)
#h6.SetFillStyle(3001)
h8.SetLineColor(ROOT.kAzure+7)
h8.SetLineWidth(4)
l4.AddEntry("h8", "Gen. ISR Jet p_{T} (both reco cuts)", "F")
l4.Draw()

ROOT.gPad.SetLogy()

#Reduction Factor
eff4 = h8.GetEntries()/h7.GetEntries()
red4 = (h7.GetEntries()-h8.GetEntries())/h7.GetEntries()

box4 = makeBox()
box4.AddEntry("","             #bf{Cuts:}","")
box4.AddEntry(0, "MET p_{T} cut: " + str(cuts['MET']) + " GeV", "")
box4.AddEntry(0, "ISR Jet p_{T} cut: " + str(cuts['ISR']) + " GeV", "")
box4.AddEntry(0, "ISR Jet Eta #eta cut: " + str(cuts['Eta']), "")
box4.AddEntry(0, "Gen. MET p_{T} cut: " + str(cuts['gMET']) + " GeV", "")
#box4.AddEntry(0, "Gen. ISR Jet p_{T} cut: " + str(cuts['gISR']) + " GeV", "")
#box4.AddEntry(0, "Gen. ISR Jet #eta cut: " + str(cuts['gEta']), "")
box4.AddEntry("","             #bf{Filter:}","")
box4.AddEntry("", "Filter Efficiency: " + str("%0.3f"%eff4), "")
box4.AddEntry("", "Reduction Factor: " + str("%0.3f"%red4), "")
box4.Draw()

#Jet Turnon Plot
c4.cd(2)
jetTurnon2 = ROOT.TEfficiency(h8, h7) #(passed, total)
jetTurnon2.SetTitle("ISR Jet p_{T} Inverse Turnon Plot (both reco cuts) ; Generated ISR Jet p_{T} / GeV ; Counts")
jetTurnon2.SetMarkerColor(ROOT.kBlue)
jetTurnon2.SetMarkerStyle(33)
jetTurnon2.SetMarkerSize(3)
jetTurnon2.Draw("AP") #L/C option for curve | * - Star markers #X - no error bars
jetTurnon2.SetLineColor(ROOT.kBlack)
jetTurnon2.SetLineWidth(2)
ROOT.gPad.SetGridx()
ROOT.gPad.Update()
jetTurnon2.GetPaintedGraph().GetXaxis().SetRangeUser(0,1000) #TEfficiency::GetPaintedGraph()
jetTurnon2.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
jetTurnon2.GetPaintedGraph().GetXaxis().CenterTitle()
jetTurnon2.GetPaintedGraph().GetYaxis().CenterTitle()

#Fitting
fitFunc.SetParameters(0.5, 100, 30, 0.5)
jetTurnon2.Fit(fitFunc)

print makeLine()
print "Filter Efficiency: " + str("%0.3f"%eff4)
print "Reduction Factor: " + str("%0.3f"%red4)
#print "Reduction Factor: " + str(1 - eff3)

#Efficiency at Reco Cut
recoEff4 = fitFunc(cuts['ISR'])
print "Efficiency at Reco ISR Jet pT cut: ", recoEff4 #jetTurnon2.GetEfficiency(nbin)
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

#box8 = makeBox()
box8 = ROOT.TLegend(box4)
box8.AddEntry("","Efficiency at " + str(cuts['ISR']) + " GeV (reco cut): " + str("%0.3f"%recoEff4),"")
box8.AddEntry("","              #bf{Plot:}","")
box8.AddEntry(jetTurnon2, "ISR Turnon Fit (both cuts)", "LP")
#box8.Copy(box1)
box8.Draw()

#c4.SetGridx()
c4.Modified()
c4.Update() 

#Write to file
savedir = "/afs/hephy.at/work/m/mzarucki/plots/filter/invTurnon_%s_%s"%(str(cuts["MET"]),str(cuts["ISR"]))
webdir = "/afs/hephy.at/user/m/mzarucki/www/plots/filter/invTurnon_%s_%s"%(str(cuts["MET"]),str(cuts["ISR"]))

if not os.path.exists(savedir):
   os.makedirs(savedir)

if not os.path.exists(webdir):
   os.makedirs(webdir)

outfile = open(savedir + "/invTurnonResults_%s_%s.txt"%(str(cuts["gMET"]),str(cuts["gISR"])), "w")
print >> outfile, "Generator Filter Results", "\n", makeLine(), "\n", cutString, "\n", makeLine(), "\n", \
"Variable", "         ", "Filter Efficiency", "   ", "Reduction Factor", "\n\n", \
"MET (1 cut)", "        ", eff1,"   ", red1, "\n\n", \
"ISR Jet pT (1 cut)", " ", eff2, "   ", red2, "\n\n", \
"MET (2 cuts)", "       ", eff3, "   ", red3, "\n\n", \
"ISR Jet pT (2 cuts)", "", eff4, "   ", red4,  "\n", \
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
"ISR Jet pT (1 cut)   ", fit2[9], fit2[10], fit2[11], fit2[12], fit2[13], fit2[14], fit2[15], fit2[16], "\n\n", \
"MET pT (2 cuts)      ", fit3[9], fit3[10], fit3[11], fit3[12], fit3[13], fit3[14], fit3[15], fit3[16], "\n\n", \
"ISR Jet pT (2 cuts)  ", fit4[9], fit4[10], fit4[11], fit4[12], fit4[13], fit4[14], fit4[15], fit4[16]
outfile.close()

#Save to file (.root)
c1.SaveAs(savedir + "/invMET_%s_%s.root"%( str(cuts['MET']), str(cuts['ISR'])))
c2.SaveAs(savedir + "/invISR_%s_%s.root"%(str(cuts['MET']), str(cuts['ISR'])))
c3.SaveAs(savedir + "/invMET2_%s_%s.root"%(str(cuts['MET']), str(cuts['ISR'])))
c4.SaveAs(savedir + "/invISR2_%s_%s.root"%(str(cuts['MET']), str(cuts['ISR'])))

#Save to Web
c1.SaveAs(webdir + "/invMET_%s_%s.png"%(str(cuts['MET']), str(cuts['ISR'])))
c2.SaveAs(webdir + "/invISR_%s_%s.png"%(str(cuts['MET']), str(cuts['ISR'])))
c3.SaveAs(webdir + "/invMET2_%s_%s.png"%(str(cuts['MET']), str(cuts['ISR'])))
c4.SaveAs(webdir + "/invISR2_%s_%s.png"%(str(cuts['MET']), str(cuts['ISR'])))
