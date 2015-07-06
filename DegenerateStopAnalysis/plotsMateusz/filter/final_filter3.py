#filter.py

import ROOT

from Workspace.HEPHYPythonTools.helpers import getChain#, getPlotFromChain, getYieldFromChain, getChunks

#ROOT Options
ROOT.gROOT.Reset() #re-initialises ROOT
#ROOT.gROOT.SetStyle("Plain")

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(1111) #1111 prints fits results on plot
#ROOT.gStyle.SetTitleX(0.15)
#ROOT.gStyle.SetFuncWidth(1)
#ROOT.gStyle.SetFuncColor(9)
#ROOT.gStyle.SetLineWidth(2)
#ROOT.gStyle.SetOptTitle(0) #suppresses title box

ROOT.gStyle.SetStatX(0.75)
ROOT.gStyle.SetStatY(0.65)

dir = "/afs/cern.ch/work/n/nrad/cmgTuples/RunII/RunII_T2DegStop_300_270_prunedGenParticles/T2DegStop_300_270_RunII_genParticles"

#dir = "/afs/cern.ch/work/m/mzarucki/data"

signal=({\
"name" : "treeProducerSusySingleLepton",
"bins" : ["treeProducerSusySingleLepton"],
'dir' : dir
})

T2DegSample = getChain(signal, histname='',treeName="tree")

print 'Sample: ', signal['name']

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
   leg = ROOT.TLegend(0.60,0.60,0.85,0.75)
   leg.SetHeader("Legend")
   header = leg.GetListOfPrimitives().First()
   header.SetTextAlign(22)
   return leg 

#Creates Box 
def makeBox():
   box = ROOT.TLegend(0.70,0.15,0.85,0.40)
   #box.SetHeader("Cuts")
   #header = box.GetListOfPrimitives().First()
   #header.SetTextAlign(22)
   return box 

#def getJetPt(jets) #getJets(), #getLeadingJetPt() == Jet_pt[0]
#   for jet in jets:
#         return jet.pt()
#   return 0

#Fit Function
fitFunc = ROOT.TF1("f1", "[0]*TMath::Erf((x-[1])/[2]) + 0.5", 0, 1000) #Error function scaled to [0,1]
fitFunc.SetParNames("Normalisation a", "Turnon Edge b", "Resolution c")
fitFunc.SetParameters(0.5, 150, 30)
#fitFunc.SetParameter(0, 0.5)
#fitFunc.SetParameter(1, 150)
#fitFunc.SetParameter(2, 50)  
#fitFunc.SetParLimits(0, 0.5, 0.5) #keep fixed?
#fitFunc.SetParLimits(1, 0, 1000)
#fitFunc.SetParLimits(2, 0, 200)

#Selection
#weight = 1
#str(weight) + "*(" + ")" 

cuts=({\
'MET' : 200, #MET cut (fixed)
'ISR' : 110, #ISR/Leading Jet cut (fixed)
'Eta' : 2.4, #eta cut (fixed)

'gMET' : 150, #generated quantities
'gISR' : 80,
'gEta' : 2.4
})

#Preselection
#Variables: met_pt, met_genPt, Jet_pt, GenJet_pt, Jet_eta, GenJet_eta

preSel1 = "Max$(Jet_pt*(abs(Jet_eta)<" + str(cuts['Eta']) + "))" + ">" + str(cuts['ISR'])
#MaxIf$("Jet_pt", select("Jet_eta", cuts['Eta'], "<")) + ">" + cuts['ISR'], #Jet_pt[0] is one with max Pt

preSel2 = select("met_pt", cuts['MET'], ">")

#Generated Particles Selection
genSel1 = select("met_genPt", cuts['gMET'], ">")

genSel2 = "Max$(GenJet_pt*(abs(GenJet_eta)<" + str(cuts['gEta']) + "))" + ">" + str(cuts['gISR'])
#maxIf$("GenJet_pt", select("GenJet_eta", cuts['gEta'], "<")) + ">" + cuts['gISR'] + ")" #GenJet_pt[0] is one with max Pt

#Canvas 1: MET
c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,2)

var = "met_pt"
c1.cd(1)
h1 = drawhist(T2DegSample, var, preSel1) #ISR preselection cut
h1.SetName("h1")
h1.SetTitle("Generated MET Filter Effect on Reconstructed MET p_{T}")
h1.GetXaxis().SetTitle("Missing Transverse Energy #slash{E}_{T} / GeV")
h1.Draw()
h1.SetFillColor(ROOT.kRed+1)
h1.SetLineColor(ROOT.kBlack)
h1.SetLineWidth(4)
l1 = makeLegend()
l1.AddEntry("h1", "MET (no generator cuts)", "F")

h2 = drawhist(T2DegSample, var, preSel1 + "&&" + genSel1) # + MET generator cut
h2.SetName("h2")
h2.Draw("same")
h2.SetFillColor(0)
#h2.SetFillStyle(3001)
h2.SetLineColor(ROOT.kAzure+7)
h2.SetLineWidth(4)
l1.AddEntry("h2", "MET (generator cut)", "F")
l1.Draw()

ROOT.gPad.SetLogy()

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

metTurnon1.Fit(fitFunc) #Fit

box1 = makeBox()
box1.AddEntry(metTurnon1, "MET Turnon Fit (single cuts)", "LP")
box1.AddEntry("","           #bf{Cuts:}","")
#box1.AddEntry(0, "MET p_{T} cut: " + str(cuts['MET']) + " GeV", "")
box1.AddEntry(0, "ISR Jet p_{T} cut: " + str(cuts['ISR']) + " GeV", "")
box1.AddEntry(0, "ISR Jet Eta #eta cut: " + str(cuts['Eta']) + " GeV", "")
box1.AddEntry(0, "Gen. MET p_{T} cut: " + str(cuts['gMET']) + " GeV", "")
#box1.AddEntry(0, "Gen. ISR Jet p_{T} cut: " + str(cuts['gISR']) + " GeV", "")
#box1.AddEntry(0, "Gen. ISR Jet Eta #eta cut: " + str(cuts['gEta']) + " GeV", "")
box1.Draw()

c1.SetGridx()
c1.Modified()
c1.Update()

#Canvas 2: Jet Pt
c2 = ROOT.TCanvas("c2", "Canvas 2", 1800, 1500)
c2.Divide(1,2)

var = "Max$(Jet_pt*(abs(Jet_eta)<" + str(cuts['Eta']) + "))" #Leading JET pt with eta < 2.4
c2.cd(1)
h3 = drawhist(T2DegSample, var, preSel2) #MET preselection cut
h3.SetName("h3")
h3.SetTitle("Generated ISR Jet p_{T} Filter Effect on Reconstructed ISR Jet p_{T}")
h3.GetXaxis().SetTitle("Jet p_{T} / GeV")
h3.Draw()
h3.SetFillColor(ROOT.kRed+1)
h3.SetLineColor(ROOT.kBlack)
h3.SetLineWidth(4)
l2 = makeLegend()
l2.AddEntry("h3", "ISR Jet p_{T} (no generator cuts)", "F")

h4 = drawhist(T2DegSample, var, preSel2 + "&&" + genSel2) # + ISR generator cut
h4.SetName("h4")
h4.Draw("same")
h4.SetFillColor(0)
#h4.SetFillStyle(3001)
h4.SetLineColor(ROOT.kAzure+7)
h4.SetLineWidth(4)
l2.AddEntry("h4", "ISR Jet p_{T} (generator cut)", "F")
l2.Draw()

ROOT.gPad.SetLogy()

#Jet Turnon Plot
c2.cd(2)
jetTurnon1 = ROOT.TEfficiency(h4, h3)
jetTurnon1.SetTitle("ISR Jet p_{T} Turnon Plot (single generator cut) ; ISR Jet p_{T} / GeV ; Counts")
jetTurnon1.SetMarkerColor(ROOT.kBlue)
jetTurnon1.SetMarkerStyle(33)
jetTurnon1.SetMarkerSize(3)
jetTurnon1.Draw("AP") 
jetTurnon1.SetLineColor(ROOT.kBlack)
jetTurnon1.SetLineWidth(2)

jetTurnon1.Fit(fitFunc)

box2 = makeBox()
box2.AddEntry(jetTurnon1, "ISR Turnon Fit (single cuts)", "LP")
box2.AddEntry("","           #bf{Cuts:}","")
box2.AddEntry(0, "MET p_{T} cut: " + str(cuts['MET']) + " GeV", "")
#box2.AddEntry(0, "ISR Jet p_{T} cut: " + str(cuts['ISR']) + " GeV", "")
#box2.AddEntry(0, "ISR Jet Eta #eta cut: " + str(cuts['Eta']) + " GeV", "")
#box2.AddEntry(0, "Gen. MET p_{T} cut: " + str(cuts['gMET']) + " GeV", "")
box2.AddEntry(0, "Gen. ISR Jet p_{T} cut: " + str(cuts['gISR']) + " GeV", "")
box2.AddEntry(0, "Gen. ISR Jet Eta #eta cut: " + str(cuts['gEta']) + " GeV", "")
box2.Draw()

c2.SetGridx()
c2.Modified()
c2.Update() 

#Canvas 3: MET (both gen cuts)
c3 = ROOT.TCanvas("c3", "Canvas 3", 1800, 1500)
c3.Divide(1,2)

var = "met_pt"
c3.cd(1)
h1.SetTitle("Generated MET & ISR Jet p_{T} Filter Effect on Reconstructed MET p_{T}")
h1.Draw() #ISR preselection cut
#h3.SetFillColor(ROOT.kRed+1)
#h3.SetLineColor(ROOT.kBlack)
#h3.SetLineWidth(4)
l3 = makeLegend()
l3.AddEntry("h1", "MET (no generator cuts)", "F")

h5 = drawhist(T2DegSample, var, preSel1 + "&&" + genSel1 + "&&" + genSel2) # + both MET and ISR generator cuts
h5.SetName("h5")
h5.Draw("same")
h5.SetFillColor(0)
#h5.SetFillStyle(3001)
h5.SetLineColor(ROOT.kAzure+7)
h5.SetLineWidth(4)
l3.AddEntry("h5", "MET (both generator cuts)", "F")
l3.Draw()

ROOT.gPad.SetLogy()

#MET Turnon Plot
c3.cd(2)
metTurnon2 = ROOT.TEfficiency(h5, h1) #(passed, total)
metTurnon2.SetTitle("MET Turnon Plot (both generator cuts) ; Missing Transverse Energy #slash{E}_{T} / GeV ; Counts")
metTurnon2.SetMarkerColor(ROOT.kBlue)
metTurnon2.SetMarkerStyle(33)
metTurnon2.SetMarkerSize(3)
metTurnon2.Draw("AP") 
metTurnon2.SetLineColor(ROOT.kBlack)
metTurnon2.SetLineWidth(2)

metTurnon2.Fit(fitFunc)

box3 = makeBox()
box3.AddEntry(metTurnon2, "MET Turnon Fit (both cuts)", "LP")
box3.AddEntry("","           #bf{Cuts:}","")
#box3.AddEntry(0, "MET p_{T} cut: " + str(cuts['MET']) + " GeV", "")
box3.AddEntry(0, "ISR Jet p_{T} cut: " + str(cuts['ISR']) + " GeV", "")
box3.AddEntry(0, "ISR Jet Eta #eta cut: " + str(cuts['Eta']) + " GeV", "")
box3.AddEntry(0, "Gen. MET p_{T} cut: " + str(cuts['gMET']) + " GeV", "")
box3.AddEntry(0, "Gen. ISR Jet p_{T} cut: " + str(cuts['gISR']) + " GeV", "")
box3.AddEntry(0, "Gen. ISR Jet Eta #eta cut: " + str(cuts['gEta']) + " GeV", "")
box3.Draw()

c3.SetGridx()
c3.Modified()
c3.Update()

#Canvas 4: Jet Pt (both gen cuts)
c4 = ROOT.TCanvas("c4", "Canvas 4", 1800, 1500)
c4.Divide(1,2)

var = "Max$(Jet_pt*(abs(Jet_eta)<" + str(cuts['Eta']) + "))" #Leading JET pt with eta < 2.4 
c4.cd(1)
h3.SetTitle("Generated ISR Jet p_{T} & MET Filter Effect on Reconstructed ISR Jet p_{T}")
h3.Draw() #MET preselection cut
#h3.SetFillColor(ROOT.kRed+1)
#h3.SetLineColor(ROOT.kBlack)
#h3.SetLineWidth(4)
l4 = makeLegend()
l4.AddEntry("h3", "ISR Jet p_{T} (no generator cuts)", "F")

h6 = drawhist(T2DegSample, var, preSel2 + "&&" + genSel2 + "&&" + genSel1) # + both ISR and MET generator cuts
h6.SetName("h6")
h6.Draw("same")
h6.SetFillColor(0)
#h6.SetFillStyle(3001)
h6.SetLineColor(ROOT.kAzure+7)
h6.SetLineWidth(4)
l4.AddEntry("h6", "ISR Jet p_{T} (both generator cuts)", "F")
l4.Draw()

ROOT.gPad.SetLogy()

#Jet Turnon Plot
c4.cd(2)
jetTurnon2 = ROOT.TEfficiency(h4, h3)
jetTurnon2.SetTitle("ISR Jet p_{T} Turnon Plot (both generator cuts) ; ISR Jet p_{T} / GeV ; Counts")
jetTurnon2.SetMarkerColor(ROOT.kBlue)
jetTurnon2.SetMarkerStyle(33)
jetTurnon2.SetMarkerSize(3)
jetTurnon2.Draw("AP") #L/C option for curve | * - Star markers #X - no error bars
jetTurnon2.SetLineColor(ROOT.kBlack)
jetTurnon2.SetLineWidth(2)

jetTurnon2.Fit(fitFunc)

box4 = makeBox()
box4.AddEntry(jetTurnon2, "ISR Turnon Fit (both cuts)", "LP")
box3.AddEntry("","           #bf{Cuts:}","")
box4.AddEntry(0, "MET p_{T} cut: " + str(cuts['MET']) + " GeV", "")
#box4.AddEntry(0, "ISR Jet p_{T} cut: " + str(cuts['ISR']) + " GeV", "")
#box4.AddEntry(0, "ISR Jet Eta #eta cut: " + str(cuts['Eta']) + " GeV", "")
box4.AddEntry(0, "Gen. MET p_{T} cut: " + str(cuts['gMET']) + " GeV", "")
box4.AddEntry(0, "Gen. ISR Jet p_{T} cut: " + str(cuts['gISR']) + " GeV", "")
box4.AddEntry(0, "Gen. ISR Jet Eta #eta cut: " + str(cuts['gEta']) + " GeV", "")
box4.Draw()

c4.SetGridx()
c4.Modified()
c4.Update() 

c1.SaveAs("/afs/cern.ch/work/m/mzarucki/plots/filter/MET_%s_%s.png"%(str(cuts['gMET']),str(cuts['gISR'])))
c2.SaveAs("/afs/cern.ch/work/m/mzarucki/plots/filter/JET_%s_%s.png"%(str(cuts['gMET']),str(cuts['gISR'])))
c3.SaveAs("/afs/cern.ch/work/m/mzarucki/plots/filter/MET2_%s_%s.png"%(str(cuts['gMET']),str(cuts['gISR'])))
c4.SaveAs("/afs/cern.ch/work/m/mzarucki/plots/filter/JET2_%s_%s.png"%(str(cuts['gMET']),str(cuts['gISR'])))
