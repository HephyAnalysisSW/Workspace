#eleMisId2.py
import ROOT
import os, sys
from Workspace.HEPHYPythonTools.helpers import getChunks, getChain#, getPlotFromChain, getYieldFromChain
from Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_7412pass2 import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Input options
inputSample = "WJets" # "Signal" "TTJets" "WJets"
zoom = 1
save = 1
presel = 1

#ROOT Options
ROOT.gROOT.Reset() #re-initialises ROOT
#ROOT.gROOT.SetStyle("Plain")

ROOT.gStyle.SetOptStat(1111) #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis
ROOT.gStyle.SetOptFit(1111) #1111 prints fits results on plot
#ROOT.gStyle.SetOptTitle(0) #suppresses title box
#ROOT.gStyle.SetFuncWidth(1)
#ROOT.gStyle.SetFuncColor(9)
#ROOT.gStyle.SetLineWidth(2)

ROOT.gStyle.SetPaintTextFormat("4.2f")
#ROOT.gStyle->SetTitleX(0.1)
#ROOT.gStyle->SetTitleW(0.8)

ROOT.gStyle.SetStatX(0.75)
ROOT.gStyle.SetStatY(0.65)
ROOT.gStyle.SetStatW(0.1)
ROOT.gStyle.SetStatH(0.15)
 
#CMG Tuples
#data_path = "/data/nrad/cmgTuples/RunII/RunIISpring15MiniAODv2/"
#data_path = "/afs/hephy.at/data/mzarucki01/cmgTuples"

print makeLine()
print "Signal Samples:"
newLine()
for s in allSignals: print s['name']
print makeLine()
print "Background Samples:"
newLine()
for s in samples: print s['name']
#print makeLine()

print makeLine()
print "Using", inputSample, "samples."
print makeLine()

Events = ROOT.TChain("tree")

#for s in allSamples_Spring15_25ns:
#   if sample in s['name']:
#      print s['name']
#      for f in getChunks(s)[0]: Events.Add(f['file'])

#Bin size 
#nbins = 100
xmin = 0
xmax = 1000
sampleName = allSignals[0]

if inputSample == "Signal":
   sampleName = allSignals[0]
   xmax = 150
elif inputSample == "TTJets":
   sampleName = TTJets_LO
   xmax = 500
elif inputSample == "WJets":
   sampleName = WJetsToLNu
   xmax = 500
else:
   print "Sample unavailable (check name)."
   sys.exit(0)

for f in getChunks(sampleName)[0]: Events.Add(f['file'])

bins = array('d', range(xmin,50,2) + range(50,100,5) + range(100,xmax+10,10)) #Variable bin size

#Zoom
z = ""
if zoom == 1:
   #nbins = 10
   xmax = 50
   bins = array('d',range(xmin,xmax+2,2))
   z = "_lowPt"

#Selection criteria
intLum = 10.0 #fb-1
weight = "(xsec*" + str(intLum) + "*(10^3)/" + str(getChunks(sampleName)[1]) + ")" #xsec in pb
if zoom == 1: normFactor = "(0.5)"
elif zoom == 0: normFactor = "((LepGood_pt < 50)*0.5 + (LepGood_pt >= 50 && LepGood_pt < 100)*0.2 + (LepGood_pt >= 100)*0.1)"

#Geometric divisons
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap
etaAcc = 2.5 #eta acceptance

#Preselection
preSel1 = "(met_pt > 200)" #MET
preSel2 = "(Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 4.5 && Jet_id)) > 200)" #HT = Sum of Jets > 30GeV
preSel3 = "(Max$(Jet_pt*(abs(Jet_eta) < " + str(etaAcc) + ") > 100))" #ISR

if presel == 1: preSel = preSel1 + "&&" + preSel2 + "&&" + preSel3
elif presel == 0: preSel = "1"

#IDs: 0 - none, 1 - veto (~95% eff), 2 - loose (~90% eff), 3 - medium (~80% eff), 4 - tight (~70% eff)
recoSel = "(abs(LepGood_pdgId) == 11)"
misMatchSel = "(LepGood_mcMatchId == 0)"
cutSel = "LepGood_SPRING15_25ns_v1 >="

##################################################################################Canvas 1#############################################################################################
c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,2)

c1.cd(1)

#Reconstructed selection
hist_total = makeHistVarBins(Events, "LepGood_pt", normFactor + "*" + weight + "*(" + preSel + "&&" + recoSel + "&&" + misMatchSel + ")", bins) 
hist_total.SetName("misID2")
hist_total.SetTitle("Fake (Non-Prompt) Electron p_{T} Distributions for Various IDs (" + inputSample + " Sample)")
hist_total.GetXaxis().SetTitle("Reconstructed Electron p_{T} / GeV")
hist_total.GetXaxis().SetTitleOffset(1.2)
hist_total.GetYaxis().SetTitleOffset(1.2)
hist_total.SetFillColor(ROOT.kBlue-9)
hist_total.SetLineColor(ROOT.kBlack)
hist_total.SetLineWidth(3)
hist_total.Draw("hist")

ROOT.gPad.SetLogy()
ROOT.gPad.Update()

alignStats(hist_total)

hists_passed = []

#Electron Cut IDs
for i in range(1,5): #hists 1-4
   hists_passed.append(makeHistVarBins(Events, "LepGood_pt", normFactor + "*" + weight + "*(" + preSel + "&&" + recoSel + "&&" + misMatchSel + "&& (" + cutSel + str(i) + "))", bins)) 
   hists_passed[i-1].SetFillColor(0)
   hists_passed[i-1].SetLineWidth(3)
   hists_passed[i-1].Draw("histsame")



hists_passed[0].SetName("electrons_veto")
hists_passed[0].SetLineColor(ROOT.kGreen+3)

#Loose ID
hists_passed[1].SetName("electrons_loose")
hists_passed[1].SetLineColor(ROOT.kBlue+1)

#Medium ID
hists_passed[2].SetName("electrons_medium")
hists_passed[2].SetLineColor(ROOT.kOrange-2)

#Tight ID
hists_passed[3].SetName("electrons_tight")
hists_passed[3].SetLineColor(ROOT.kRed+1)

#Electron MVA IDs
WPs = {'WP90':\
         {'EB1_lowPt':-0.083313, 'EB2_lowPt':-0.235222, 'EE_lowPt':-0.67099, 'EB1':0.913286, 'EB2':0.805013, 'EE':0.358969},\
       'WP80':\
         {'EB1_lowPt':0.287435, 'EB2_lowPt':0.221846, 'EE_lowPt':-0.303263, 'EB1':0.967083, 'EB2':0.929117, 'EE':0.726311},\
}

ptSplit = 10 #we have above and below 10 GeV categories

for i,WP in enumerate(WPs):
   mvaSel = "(\
   (LepGood_pt <=" + str(ptSplit) + "&& abs(LepGood_eta) < " + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB1_lowPt']) + ") || \
   (LepGood_pt <=" + str(ptSplit) + "&& abs(LepGood_eta) >=" + str(ebSplit) + "&& abs(LepGood_eta) <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB2_lowPt']) + ") || \
   (LepGood_pt <=" + str(ptSplit) + "&& abs(LepGood_eta) >=" + str(ebeeSplit) + "&& abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EE_lowPt']) + ") || \
   (LepGood_pt >" + str(ptSplit) + "&& abs(LepGood_eta) <" + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB1']) + ") || \
   (LepGood_pt >" + str(ptSplit) + "&& abs(LepGood_eta) >=" + str(ebSplit) + "&& abs(LepGood_eta) <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB2']) + ") || \
   (LepGood_pt >" + str(ptSplit) + "&& abs(LepGood_eta) >=" + str(ebeeSplit) + "&& abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EE']) + "))"
   hists_passed.append(makeHistVarBins(Events, "LepGood_pt", normFactor + "*" + weight + "*(" + preSel + "&&" + recoSel + "&&" + misMatchSel + "&&" + mvaSel + ")", bins))
   hists_passed[4+i].SetName("electrons_mva_" + WP)

hists_passed[4].Draw("histsame")
hists_passed[4].SetFillColor(0)
hists_passed[4].SetLineColor(ROOT.kAzure+5)
hists_passed[4].SetLineWidth(3)

hists_passed[5].Draw("histsame")
hists_passed[5].SetFillColor(0)
hists_passed[5].SetLineColor(ROOT.kMagenta+2)
hists_passed[5].SetLineWidth(3)

ROOT.gPad.Update()

l1 = makeLegend()
l1.AddEntry("misID2", "Reconstructed Electron p_{T}", "F")
l1.AddEntry("electrons_veto", "Veto ID", "F")
l1.AddEntry("electrons_loose", "Loose ID", "F")
l1.AddEntry("electrons_medium", "Medium ID", "F")
l1.AddEntry("electrons_tight", "Tight ID", "F")
l1.AddEntry("electrons_mva_WP80", "MVA ID (WP80)", "F")
l1.AddEntry("electrons_mva_WP90", "MVA ID (WP90)", "F")
l1.Draw()

#######################################################################################################################################################
#Efficiency curves
c1.cd(2)
l2 = makeLegend()

effs = []

#Efficiency Veto
for i in range (0, 6):
   effs.append(ROOT.TEfficiency(hists_passed[i], hist_total)) #(passed, total)
   effs[i].SetMarkerStyle(33)
   effs[i].SetMarkerSize(1.5)
   effs[i].SetLineWidth(2)

effs[0].SetTitle("Electron Mismatch Efficiencies for Various IDs (" + inputSample + " Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency")
effs[0].SetName("eff1")
effs[0].SetMarkerColor(ROOT.kGreen+3)
effs[0].SetLineColor(ROOT.kGreen+3)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
effs[0].Draw("AP") 
ROOT.gPad.Update()
effs[0].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)
#effs[0].GetPaintedGraph().GetYaxis().SetLimits(0,1)
effs[0].GetPaintedGraph().SetMinimum(0)
effs[0].GetPaintedGraph().SetMaximum(1)
#effs[0].GetPaintedGraph().GetXaxis().SetNdivisions(510, 1)
effs[0].GetPaintedGraph().GetXaxis().CenterTitle()
effs[0].GetPaintedGraph().GetYaxis().CenterTitle()

#Efficiency Loose
effs[1].SetName("eff2")
effs[1].SetMarkerColor(ROOT.kBlue+1)
effs[1].SetLineColor(ROOT.kBlue+1)
effs[1].Draw("sameP") 

#Efficiency Medium
effs[2].SetName("eff3")
effs[2].SetMarkerColor(ROOT.kOrange-2)
effs[2].SetLineColor(ROOT.kOrange-2)
effs[2].Draw("sameP")

#Efficiency Tight
effs[3].SetName("eff4")
effs[3].SetMarkerColor(ROOT.kRed+1)
effs[3].SetLineColor(ROOT.kRed+1)
effs[3].Draw("sameP")


#Efficiency WP80
effs[4].SetName("eff6")
effs[4].SetMarkerColor(ROOT.kAzure+5)
effs[4].SetMarkerStyle(22)
effs[4].SetMarkerSize(1)
effs[4].Draw("sameP")
effs[4].SetLineColor(ROOT.kAzure+5)

#Efficiency WP90
effs[5].SetName("eff5")
effs[5].SetMarkerColor(ROOT.kMagenta+2)
effs[5].SetMarkerStyle(22)
effs[5].SetMarkerSize(1)
effs[5].Draw("sameP")
effs[5].SetLineColor(ROOT.kMagenta+2)

ROOT.gPad.Update()

l2.AddEntry("eff1", "Veto ID", "P")
l2.AddEntry("eff2", "Loose ID", "P")
l2.AddEntry("eff3", "Medium ID", "P")
l2.AddEntry("eff4", "Tight ID", "P")
l2.AddEntry("eff5", "MVA ID (WP80)", "P")
l2.AddEntry("eff6", "MVA ID (WP90)", "P")
l2.Draw()

ROOT.gPad.Update()
c1.Modified()
c1.Update()

#Write to file
if save == 1:
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronReconstruction/electronID/misID2" #web address: http://www.hephy.at/user/mzarucki/plots/electronReconstruction/electronIdEfficiency
   
   if not os.path.exists(savedir):
      os.makedirs(savedir)
   if not os.path.exists(savedir + "/root"):
      os.makedirs(savedir + "/root")
   if not os.path.exists(savedir + "/pdf"):
      os.makedirs(savedir + "/pdf")
   
   #Save to Web
   c1.SaveAs(savedir + "/eleMisID2_" + inputSample + z + ".png")
   c1.SaveAs(savedir + "/root/eleMisID2_" + inputSample + z + ".root")
   c1.SaveAs(savedir + "/pdf/eleMisID2_" + inputSample + z + ".pdf")
