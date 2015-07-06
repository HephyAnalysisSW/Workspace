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

#def getJetPt(jets) #getJets(), #getLeadingJetPt() == Jet_pt[0]
#   for jet in jets:
#         return jet.pt()
#   return 0


#Selection

#weight = 1
#str(weight) + "*(" + ")" 

cuts=({\
'MET' : 100, #MET cut
'ISR' : 100, #ISR/Leading Jet cut
'Eta' : 2.4, #eta cut

'gMET' : 100, #generated quantities
'gISR' : 100,
'gEta' : 2.4
})

#Preselection
preSel = \
select("met_pt", cuts['MET'], ">") + "&&" + \
select("Jet_pt", cuts['ISR'], ">")
#maxIf$("Jet_pt", select("Jet_eta", cuts['Eta'], "<")) + ">" + cuts['ISR'] + ")", #Jet_pt[0] is one with max Pt

#Generated Particles Selection
genSel = \
select("met_genPt", cuts['gMET'], ">") + "&&" + \
select("GenJet_pt", cuts['gISR'], ">")
#maxIf$("GenJet_pt", select("GenJet_eta", cuts['gEta'], "<")) + ">" + cuts['gISR'] + ")" #GenJet_pt[0] is one with max Pt

#selection = preSel + "&&" + genSel

#Canvas 1: MET
c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,2)

var = "met_pt" #or met_genPt
c1.cd(1)
h1 = drawhist(T2DegSample, var, preSel)
h1.SetName("h1")
h1.SetTitle("Generated MET and Jet P_{T} Filter Effect on Reconstructed MET p_{T}")
h1.GetXaxis().SetTitle("Missing Transverse Energy #slash{E}_{T} / GeV")
h1.Draw()
h1.SetFillColor(ROOT.kRed+1)
h1.SetLineColor(ROOT.kBlack)
h1.SetLineWidth(4)
l1 = makeLegend()
l1.AddEntry("h1", var + " (no generator cuts)", "F")

h2 = drawhist(T2DegSample, var, preSel + "&&" + genSel)
h2.SetName("h2")
h2.Draw("same")
h2.SetFillColor(0)
#h2.SetFillStyle(3001)
h2.SetLineColor(ROOT.kAzure+7)
h2.SetLineWidth(4)
l1.AddEntry("h2", var + " (with generator cuts)", "F")
l1.Draw()

ROOT.gPad.SetLogy()

#MET Turnon Plot
c1.cd(2)
metTurnon = ROOT.TEfficiency(h2, h1) #(passed, total)
metTurnon.SetTitle("MET Turnon Plot ; Missing Transverse Energy #slash{E}_{T} / GeV ; Counts")
metTurnon.SetMarkerColor(ROOT.kBlue)
metTurnon.SetMarkerStyle(33)
metTurnon.SetMarkerSize(3)
metTurnon.Draw("AP") #L/C option for curve | * - Star markers
metTurnon.SetLineColor(ROOT.kBlack)
metTurnon.SetLineWidth(2)

box = ROOT.TLegend(0.70,0.20,0.85,0.45)
box.AddEntry(0, "met_pt cut: " + str(cuts['MET']) + " GeV", "")
box.AddEntry(0, "Jet_pt cut: " + str(cuts['ISR']) + " GeV", "")
box.AddEntry(0, "Jet_eta cut: " + str(cuts['Eta']) + " GeV", "")
box.AddEntry(0, "met_genPt cut: " + str(cuts['gMET']) + " GeV", "")
box.AddEntry(0, "GenJet_pt cut: " + str(cuts['gISR']) + " GeV", "")
box.AddEntry(0, "GenJet_eta cut: " + str(cuts['gEta']) + " GeV", "")
box.Draw()

#Fit
#f1 = ROOT.TF1("f1", "expo")
#f1 = ROOT.TF1("f1", "gaus(0)+(x<[1])")
#f1.SetParNames("Constant", "Mean", "Sigma")
#f1.SetParameters(1, 150, 50)
#f1->SetParLimits(0,
#f1->SetParLimits(1,
#f1->SetParLimits(2,
#f1.Draw("same")
#metTurnon.Fit(f1)

c1.SetGridx()
c1.Modified()
c1.Update()

#Canvas 2: Jet Pt
c2 = ROOT.TCanvas("c2", "Canvas 2", 1800, 1500)
c2.Divide(1,2)

var = "Jet_pt" #"GenJet_pt"
c2.cd(1)
h3 = drawhist(T2DegSample, var, preSel)
h3.SetName("h3")
h3.SetTitle("Generated MET and Jet P_{T} Filter Effect on Reconstructed Jet p_{T}")
h3.GetXaxis().SetTitle("Jet p_{T} / GeV")
h3.Draw()
h3.SetFillColor(ROOT.kRed+1)
h3.SetLineColor(ROOT.kBlack)
h3.SetLineWidth(4)
l2 = makeLegend()
l2.AddEntry("h3", var + " (no generator cuts)", "F")

h4 = drawhist(T2DegSample, var, preSel + "&&" + genSel)
h4.SetName("h4")
h4.Draw("same")
h4.SetFillColor(0)
#h4.SetFillStyle(3001)
h4.SetLineColor(ROOT.kAzure+7)
h4.SetLineWidth(4)
l2.AddEntry("h4", var + " (with generator cuts)", "F")
l2.Draw()

ROOT.gPad.SetLogy()

#Jet Turnon Plot
c2.cd(2)
jetTurnon = ROOT.TEfficiency(h4, h3)
jetTurnon.SetTitle("Jet p_{T} Turnon Plot ; Jet p_{T} / GeV ; Counts")
jetTurnon.SetMarkerColor(ROOT.kBlue)
jetTurnon.SetMarkerStyle(33)
jetTurnon.SetMarkerSize(3)
jetTurnon.Draw("AP") #L/C option for curve | * - Star markers #X - no error bars
jetTurnon.SetLineColor(ROOT.kBlack)
jetTurnon.SetLineWidth(2)

box.Draw()

c2.SetGridx()
c2.Modified()
c2.Update() 

c1.SaveAs("/afs/cern.ch/work/m/mzarucki/plots/filter/MET_%s_%s.png"%(str(cuts['gMET']),str(cuts['gISR'])))
c2.SaveAs("/afs/cern.ch/work/m/mzarucki/plots/filter/JET_%s_%s.png"%(str(cuts['gMET']),str(cuts['gISR'])))
