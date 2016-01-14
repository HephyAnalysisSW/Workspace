#eleIdEff_iso.py
import ROOT
import os, sys
from Workspace.HEPHYPythonTools.helpers import getChunks, getChain#, getPlotFromChain, getYieldFromChain
from Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_7412pass2_v4 import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Input options
inputSample = "Signal" # "Signal" "TTJets" "WJets"
zoom = 1
save = 1
presel = 1
nEles = "01" # 01,01tau,1,2

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
#data_path = "/data/nrad/cmgTuples/RunII/7412pass2/RunIISpring15xminiAODv2"
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

for sample in getChunks(sampleName)[0]: Events.Add(sample['file'])

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
elif zoom == 0: normFactor = "((genLep_pt < 50)*0.5 + (genLep_pt >= 50 && genLep_pt < 100)*0.2 + (genLep_pt >= 100)*0.1)"

#Geometric divisions
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap
etaAcc = 2.5 #eta acceptance

ptSplit = 10 #we have above and below 10 GeV categories

#Preselection
preSel1 = "(met_pt > 200)" #MET
preSel2 = "(Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 4.5 && Jet_id)) > 200)" #HT = Sum of Jets > 30GeV
preSel3 = "(Max$(Jet_pt*(abs(Jet_eta) < " + str(etaAcc) + ") > 100))" #ISR

if presel == 1: preSel = preSel1 + "&&" + preSel2 + "&&" + preSel3
elif presel == 0: preSel = "1"

var = "genLep_pt"
deltaRcut = 0.3

#single-lepton (semileptonic) events
if nEles == "01":
   var = "genLep_pt[0]"
   if zoom == 0: normFactor = "((genLep_pt[0] < 50)*0.5 + (genLep_pt[0] >= 50 && genLep_pt[0] < 100)*0.2 + (genLep_pt[0] >= 100)*0.1)"
   
   #Generated electron selection
   nSel = "ngenLep == 1" #removes dileptonic events
   genSel1 = "(abs(genLep_pdgId[0]) == 11 && abs(genLep_eta[0]) < " + str(etaAcc) + ")" #electron selection #index [0] ok since (only element)
   genSel = nSel + "&&" + genSel1

   #Reconstructed electron selection
   deltaR = "sqrt((genLep_eta[0] - LepGood_eta)^2 + (genLep_phi[0] - LepGood_phi)^2)"
   matchSel = "(" + deltaR +"*(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mcMatchId != 0) <" + str(deltaRcut) +\
   "&& (" + deltaR +"*(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mcMatchId != 0)) != 0)"

#if nEles == "01tau":
#   #Generated electron selection
#   nSel = "((ngenLep == 1) != (ngenLepFromTau == 1))" #removes dileptonic events
#   genSel1 = "((abs(genLep_pdgId[0]) == 11 && abs(genLep_eta[0]) < " + str(etaAcc) + ") || (abs(genLepFromTau_pdgId[0]) == 11 && abs(genLepFromTau_eta[0]) < " + str(etaAcc) + "))" #electron selection #index [0] ok since (only element)
#   #genSel = nSel# + "&&" + genSel1
#
#   #Reconstructed electron selection
#   deltaR = "sqrt((genLep_eta[0] - LepGood_eta)^2 + (genLep_phi[0] - LepGood_phi)^2)"
#   deltaRtau = "sqrt((genLepFromTau_eta[0] - LepGood_eta)^2 + (genLepFromTau_phi[0] - LepGood_phi)^2)"
#   
#   matchSel = "(" + deltaR +"*(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mcMatchId != 0) <" + str(deltaRcut) +\
#   "&& (" + deltaR +"*(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mcMatchId != 0)) != 0)" +\
#   "||(" + deltaRtau +"*(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mcMatchId != 0) <" + str(deltaRcut) +\
#   "&& (" + deltaRtau +"*(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mcMatchId != 0)) != 0)"

#single-electron events (semileptonic & dileptonic)
elif nEles == "1":
   #Generated electron selection
   nSel = "ngenLep > 0" #redundant with genSel2 #nLepGood > 0 introduces bias
   genSel1 = "(abs(genLep_pdgId) == 11 && abs(genLep_eta) < " + str(etaAcc) + ")" #electron selection (includes dielectron evts) #ngenLep == 1 would remove dileptonic events # index [0] does not include single-electron events with muon as leading lepton
   genSel2 = "(Sum$(abs(genLep_pdgId) == 11 && abs(genLep_eta) < " + str(etaAcc) + ") == 1)" # = number of electrons (includes dileptonic and semileptonic events) 
   genSel = nSel + "&&" + genSel1 + "&&" + genSel2

elif nEles == "2":
   nSel = "ngenLep == 2" #does not include single-lepton events 
   genSel1 = "(abs(genLep_pdgId) == 11 && abs(genLep_eta) < " + str(etaAcc) + ")" #electron selection (includes dielectron evts) #ngenLep == 1 would remove dileptonic events
   genSel2 = "(Sum$(abs(genLep_pdgId) == 11 && abs(genLep_eta) < " + str(etaAcc) + ") == 2)" # = number of electrons (includes dilepton events only) 
   genSel = nSel + "&&" + genSel1 + "&&" + genSel2

#IDs: 0 - none, 1 - veto (~95% eff), 2 - loose (~90% eff), 3 - medium (~80% eff), 4 - tight (~70% eff)

cuts = {\
'Veto':{'sigmaEtaEta':{'Barrel':0.0114, 'Endcap':0.0352}, 'dEta':{'Barrel':0.0152, 'Endcap':0.0113}, 'dPhi':{'Barrel':0.216, 'Endcap':0.237}, 'hOverE':{'Barrel':0.181, 'Endcap':0.116}, 'ooEmooP':{'Barrel':0.207, 'Endcap':0.174},\
'd0':{'Barrel':0.0564, 'Endcap':0.222}, 'dz':{'Barrel':0.472, 'Endcap':0.921}, 'MissingHits':{'Barrel':2, 'Endcap':3}, 'convVeto':{'Barrel':1, 'Endcap':1}, 'relIso' : {'Barrel':0.126, 'Endcap':0.144}},
'Loose':{'sigmaEtaEta':{'Barrel':0.0103, 'Endcap':0.0301}, 'dEta':{'Barrel':0.0105, 'Endcap':0.00814}, 'dPhi':{'Barrel':0.115, 'Endcap':0.182}, 'hOverE':{'Barrel':0.104, 'Endcap':0.0897}, 'ooEmooP':{'Barrel':0.102, 'Endcap':0.126},\
'd0':{'Barrel':0.0261, 'Endcap':0.118}, 'dz':{'Barrel':0.41, 'Endcap':0.822}, 'MissingHits':{'Barrel':2, 'Endcap':1}, 'convVeto':{'Barrel':1, 'Endcap':1}, 'relIso' : {'Barrel':0.0893, 'Endcap':0.121}},
'Medium':{'sigmaEtaEta':{'Barrel':0.0101, 'Endcap':0.0283}, 'dEta':{'Barrel':0.0103, 'Endcap':0.00733}, 'dPhi':{'Barrel':0.0336, 'Endcap':0.114}, 'hOverE':{'Barrel':0.0876, 'Endcap':0.0678}, 'ooEmooP':{'Barrel':0.0174, 'Endcap':0.0898},\
'd0':{'Barrel':0.0118, 'Endcap':0.0739}, 'dz':{'Barrel':0.373, 'Endcap':0.602}, 'MissingHits':{'Barrel':2, 'Endcap':1}, 'convVeto':{'Barrel':1, 'Endcap':1}, 'relIso' : {'Barrel':0.0766, 'Endcap':0.0678}},
'Tight':{'sigmaEtaEta':{'Barrel':0.0101, 'Endcap':0.0279}, 'dEta':{'Barrel':0.00926, 'Endcap':0.00724}, 'dPhi':{'Barrel':0.0336, 'Endcap':0.0918}, 'hOverE':{'Barrel':0.0597, 'Endcap':0.0615}, 'ooEmooP':{'Barrel':0.012, 'Endcap':0.00999},\
'd0':{'Barrel':0.0111, 'Endcap':0.0351}, 'dz':{'Barrel':0.0466, 'Endcap':0.417}, 'MissingHits':{'Barrel':2, 'Endcap':1}, 'convVeto':{'Barrel':1, 'Endcap':1}, 'relIso' : {'Barrel':0.0354, 'Endcap':0.0646}}}

#cutSel = "LepGood_SPRING15_25ns_v1 >="

##################################################################################Canvas 1#############################################################################################
c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,2)

c1.cd(1)

#Generated electrons
hist_total = makeHistVarBins(Events, var, normFactor + "*" + weight + "*(" + preSel + "&&" + genSel + ")", bins)
hist_total.SetName("efficiency")
hist_total.SetTitle("Electron p_{T} Distributions for Various IDs (" + inputSample + " Sample)")
hist_total.GetXaxis().SetTitle("Generated Electron p_{T} / GeV")
hist_total.GetYaxis().SetTitle("Counts / GeV")
hist_total.GetXaxis().SetTitleOffset(1.2)
hist_total.GetYaxis().SetTitleOffset(1.2)
hist_total.SetFillColor(ROOT.kBlue-9)
hist_total.SetLineColor(ROOT.kBlack)
hist_total.SetLineWidth(3)
hist_total.Draw("hist")

ROOT.gPad.SetLogy()
ROOT.gPad.Update()

alignStats(hist_total)

hists_passed = {}

#Electron Cut IDs

isolation = "relIso04" #miniRelIso, relIso03, relIso04, relIsoAn04

for WP in cuts:
   cutSel = "(\
   (abs(LepGood_eta) <=" + str(ebeeSplit) + "&& LepGood_sigmaIEtaIEta <" + str(cuts[WP]['sigmaEtaEta']['Barrel']) + "&& abs(LepGood_dEtaScTrkIn) <" + str(cuts[WP]['dEta']['Barrel']) + \
   "&& abs(LepGood_dPhiScTrkIn) <" + str(cuts[WP]['dPhi']['Barrel']) + "&& LepGood_hadronicOverEm <" + str(cuts[WP]['hOverE']['Barrel']) + "&& abs(LepGood_eInvMinusPInv) <" + str(cuts[WP]['ooEmooP']['Barrel']) + \
   "&& abs(LepGood_dxy) <" + str(cuts[WP]['d0']['Barrel']) + "&& abs(LepGood_dz) <" + str(cuts[WP]['dz']['Barrel']) + "&& LepGood_lostHits <=" + str(cuts[WP]['MissingHits']['Barrel']) + \
   "&& LepGood_" + isolation + "<" + str(cuts[WP]['relIso']['Barrel']) + ") ||" + \
   "(abs(LepGood_eta) >" + str(ebeeSplit) + "&& abs(LepGood_eta) <" + str(etaAcc) + "&& LepGood_sigmaIEtaIEta <" + str(cuts[WP]['sigmaEtaEta']['Endcap']) + "&& abs(LepGood_dEtaScTrkIn) <" + str(cuts[WP]['dEta']['Endcap']) + \
   "&& abs(LepGood_dPhiScTrkIn) <" + str(cuts[WP]['dPhi']['Endcap']) + "&& LepGood_hadronicOverEm <" + str(cuts[WP]['hOverE']['Endcap']) + "&& abs(LepGood_eInvMinusPInv) <" + str(cuts[WP]['ooEmooP']['Endcap']) + \
   "&& abs(LepGood_dxy) <" + str(cuts[WP]['d0']['Endcap']) + "&& abs(LepGood_dz) <" + str(cuts[WP]['dz']['Endcap']) + "&& LepGood_lostHits <=" + str(cuts[WP]['MissingHits']['Endcap']) + \
   "&& LepGood_" + isolation + "<" + str(cuts[WP]['relIso']['Endcap']) + "))"
   
   hists_passed[WP] = makeHistVarBins(Events, var, normFactor + "*" + weight + "*(" + preSel + "&&" + genSel + "&&" + matchSel + "&& " + cutSel + ")", bins)
   hists_passed[WP].SetName("electrons_" + WP)
   hists_passed[WP].SetFillColor(0)
   hists_passed[WP].SetLineWidth(3)
   hists_passed[WP].Draw("histsame")

#Colours
hists_passed['Veto'].SetLineColor(ROOT.kGreen+3)
hists_passed['Loose'].SetLineColor(ROOT.kBlue+1)
hists_passed['Medium'].SetLineColor(ROOT.kOrange-2)
hists_passed['Tight'].SetLineColor(ROOT.kRed+1)

##Electron MVA IDs
#WPs = {'WP90':\
#         {'EB1_lowPt':-0.083313, 'EB2_lowPt':-0.235222, 'EE_lowPt':-0.67099, 'EB1':0.913286, 'EB2':0.805013, 'EE':0.358969},\
#       'WP80':\
#         {'EB1_lowPt':0.287435, 'EB2_lowPt':0.221846, 'EE_lowPt':-0.303263, 'EB1':0.967083, 'EB2':0.929117, 'EE':0.726311},\
#}
#
#for WP in WPs:
#   mvaSel = "(\
#   (LepGood_pt <=" + str(ptSplit) + "&& abs(LepGood_eta) < " + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB1_lowPt']) + ") || \
#   (LepGood_pt <=" + str(ptSplit) + "&& abs(LepGood_eta) >=" + str(ebSplit) + "&& abs(LepGood_eta) <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB2_lowPt']) + ") || \
#   (LepGood_pt <=" + str(ptSplit) + "&& abs(LepGood_eta) >=" + str(ebeeSplit) + "&& abs(LepGood_eta) <" + str(etaAcc) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EE_lowPt']) + ") || \
#   (LepGood_pt >" + str(ptSplit) + "&& abs(LepGood_eta) <" + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB1']) + ") || \
#   (LepGood_pt >" + str(ptSplit) + "&& abs(LepGood_eta) >=" + str(ebSplit) + "&& abs(LepGood_eta) <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EB2']) + ") || \
#   (LepGood_pt >" + str(ptSplit) + "&& abs(LepGood_eta) >=" + str(ebeeSplit) + "&& abs(LepGood_eta) <" + str(etaAcc) + "&& LepGood_mvaIdSpring15 >=" + str(WPs[WP]['EE']) + "))"
#   
#   hists_passed[WP] = makeHistVarBins(Events, var, normFactor + "*" + weight + "*(" + preSel + "&&" + genSel + "&&" + matchSel + "&&" + mvaSel + ")", bins)
#   hists_passed[WP].SetName("electrons_" + WP)
#   hists_passed[WP].SetFillColor(0)
#   hists_passed[WP].SetLineWidth(3)
#   hists_passed[WP].Draw("histsame")
#
#hists_passed['WP80'].SetLineColor(ROOT.kAzure+5)
#hists_passed['WP90'].SetLineColor(ROOT.kMagenta+2)

ROOT.gPad.Update()

l1 = makeLegend()
l1.AddEntry("efficiency", "Generated Electron p_{T}", "F")
l1.AddEntry("electrons_Veto", "Veto ID", "F")
l1.AddEntry("electrons_Loose", "Loose ID", "F")
l1.AddEntry("electrons_Medium", "Medium ID", "F")
l1.AddEntry("electrons_Tight", "Tight ID", "F")
#l1.AddEntry("electrons_WP80", "MVA ID (WP80)", "F")
#l1.AddEntry("electrons_WP90", "MVA ID (WP90)", "F")
l1.Draw()

################################################################################################################################################################################
#Efficiency curves
c1.cd(2)
l2 = makeLegend()

effs = {}

#Efficiency Veto
for WP in hists_passed:
   effs[WP] = ROOT.TEfficiency(hists_passed[WP], hist_total) #(passed, total)
   effs[WP].SetMarkerStyle(33)
   effs[WP].SetMarkerSize(1.5)
   effs[WP].SetLineWidth(2)

effs['Veto'].SetTitle("Electron ID Efficiencies (" + inputSample + " Sample) ; Generated Electron p_{T} / GeV ; Efficiency")
effs['Veto'].SetName("eff_Veto")
effs['Veto'].SetMarkerColor(ROOT.kGreen+3)
effs['Veto'].SetLineColor(ROOT.kGreen+3)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
effs['Veto'].Draw("AP") 
ROOT.gPad.Update()
effs['Veto'].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)
effs['Veto'].GetPaintedGraph().SetMinimum(0)
effs['Veto'].GetPaintedGraph().SetMaximum(1)
#effs['Veto'].GetPaintedGraph().GetXaxis().SetNdivisions(510, 1)
effs['Veto'].GetPaintedGraph().GetXaxis().CenterTitle()
effs['Veto'].GetPaintedGraph().GetYaxis().CenterTitle()

#Efficiency Loose
effs['Loose'].SetName("eff_Loose")
effs['Loose'].SetMarkerColor(ROOT.kBlue+1)
effs['Loose'].SetLineColor(ROOT.kBlue+1)
effs['Loose'].Draw("sameP") 

#Efficiency Medium
effs['Medium'].SetName("eff_Medium")
effs['Medium'].SetMarkerColor(ROOT.kOrange-2)
effs['Medium'].SetLineColor(ROOT.kOrange-2)
effs['Medium'].Draw("sameP") 

#Efficiency Tight
effs['Tight'].SetName("eff_Tight")
effs['Tight'].SetMarkerColor(ROOT.kRed+1)
effs['Tight'].SetLineColor(ROOT.kRed+1)
effs['Tight'].Draw("sameP") 

##Efficiency WP80
#effs['WP80'].SetName("eff_WP80")
#effs['WP80'].SetMarkerColor(ROOT.kAzure+5)
#effs['WP80'].SetMarkerStyle(22)
#effs['WP80'].SetMarkerSize(1)
#effs['WP80'].SetLineColor(ROOT.kAzure+5)
#effs['WP80'].Draw("sameP")
#
##Efficiency WP90
#effs['WP90'].SetName("eff_WP90")
#effs['WP90'].SetMarkerColor(ROOT.kMagenta+2)
#effs['WP90'].SetMarkerStyle(22)
#effs['WP90'].SetMarkerSize(1)
#effs['WP90'].SetLineColor(ROOT.kMagenta+2)
#effs['WP90'].Draw("sameP")

ROOT.gPad.Update()

l2.AddEntry("eff_Veto", "Veto ID", "P")
l2.AddEntry("eff_Loose", "Loose ID", "P")
l2.AddEntry("eff_Medium", "Medium ID", "P")
l2.AddEntry("eff_Tight", "Tight ID", "P")
#l2.AddEntry("eff_WP80", "MVA ID (WP80)", "P")
#l2.AddEntry("eff_WP90", "MVA ID (WP90)", "P")
l2.Draw()
#box1.Draw()

ROOT.gPad.Update()
c1.Modified()
c1.Update()

#Write to file
if save == 1:
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronReconstruction/electronID/iso/" + isolation + "/efficiency" #web address: http://www.hephy.at/user/mzarucki/plots/electronReconstruction/electronIdEfficiency
   
   if not os.path.exists(savedir):
      os.makedirs(savedir)
   if not os.path.exists(savedir + "/root"):
      os.makedirs(savedir + "/root")
   if not os.path.exists(savedir + "/pdf"):
      os.makedirs(savedir + "/pdf")
   
   #Save to Web
   c1.SaveAs(savedir + "/eleIDeff_iso_" + inputSample + z + ".png")
   c1.SaveAs(savedir + "/root/eleIDeff_iso_" + inputSample + z + ".root")
   c1.SaveAs(savedir + "/pdf/eleIDeff_iso_" + inputSample + z + ".pdf")
