# Full-FastSimSFs_factored2.py
# Determination of global FullSim-FastSim SFs using indicies
# Mateusz Zarucki 2016

import ROOT
import os, sys
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style, makeDir
from Workspace.DegenerateStopAnalysis.tools.degCuts import Cuts
from Workspace.DegenerateStopAnalysis.tools.getSamples_8012 import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
#from Workspace.DegenerateStopAnalysis.toolsMateusz.cmgTuplesPostProcessed_mAODv2_analysisHephy13TeV import cmgTuplesPostProcessed
#from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_mAODv2_analysisHephy13TeV import getSamples

from array import array
from math import pi, sqrt #cos, sin, sinh, log
import argparse

ROOT.gStyle.SetOptStat(1111) #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--lep", dest = "lep",  help = "Lepton", type = str, default = "mu")
parser.add_argument("--standardBins", dest = "standardBins",  help = "Standard binning", type = int, default = 0)
parser.add_argument("--varBins", dest = "varBins",  help = "Variable bin size", type = int, default = 0)
parser.add_argument("--logy", dest = "logy",  help = "Toggle logy", type = int, default = 1)
parser.add_argument("--save", dest="save",  help="Toggle save", type=int, default=1)
parser.add_argument("--verbose", dest="verbose",  help="Verbosity switch", type=int, default=1)
parser.add_argument("-b", dest="batch",  help="Batch mode", action="store_true", default=False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
lep = args.lep
standardBins = args.standardBins
varBins = args.varBins
logy = args.logy
save = args.save
verbose = args.verbose

if lep == "el":
   lepton = "Electron"
   pdgId = "11"
elif lep == "mu":
   pdgId = "13"
   lepton = "Muon"

#Samples
cmgPP = cmgTuplesPostProcessed()

samplesList = ["tt"] #"qcd", "vv", "st", "dy", "z", "tt", "w"]

#if getData: samplesList.append("dblind")

samples = getSamples(cmgPP = cmgPP, skim = 'preIncLep', sampleList = samplesList, scan = False, useHT = True, getData = 0)

#officialSignals = ["s300_290", "s300_270", "s300_250"] #FIXME: crosscheck if these are in allOfficialSignals

if verbose:
   print makeLine()
   print "Using samples:"
   newLine()
   for s in samplesList:
      if s: print samples[s].name,":",s
      else:
         print "!!! Sample " + sample + " unavailable."
         sys.exit(0)

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/leptonSFs/global"
   
   if standardBins: savedir += "/standardBins"
   else: savedir += "/myBins"
   
   if varBins: savedir += "/varBins"
   else: savedir += "/fixedBins"
 
   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")
   
   suffix = "_" + lepton
   
#Geometric divisions
if lep == 'el': etaAcc = 2.5 #eta acceptance
elif lep == 'mu': etaAcc = 2.4

#DeltaR cut for matching
#deltaRcut = 0.3

#Selection criteria
#intLum = 10.0 #fb-1
#weight = "(xsec*" + str(intLum) + "*(10^3)/" + str(getChunks(sample)[1]) + ")" #xsec in pb
#weight = samples[sample].weight

##Preselection
#presel1 = "(met_pt > 200)" #MET
#presel2 = "(Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 4.5 && Jet_id)) > 200)" #HT = Sum of Jets > 30GeV
#presel3 = "(Max$(Jet_pt*(abs(Jet_eta) < " + str(etaAcc) + ") > 100))" #ISR
#preselList = [presel1, presel2, presel3]
#
#if presel: presel = combineCutsList(preselList) 
#else: presel = "1"

#filters
filters = samples['ttInc'].filters

#single-lepton (semileptonic) events
#if nEles == "01":

#Preselection & basic SR cuts
presel = CutClass("presel", [
   ["MET","met > 200"],
   ["HT","ht_basJet > 300"],
   ["ISR100", "nIsrJet >= 1"],
   ["No3rdJet60","nVetoJet <= 2"],
   ["AntiQCD", " (vetoJet_dPhi_j1j2 < 2.5)" ],
   ["TauVeto","Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
   ], baseCut = None)

preSel = presel.combined

#degcuts = Cuts("LepAll", lep, sr1c_opt = "MT95_IncCharge", isrpt = 100, btag = 'sf')
#
#presel = degcuts.presel.combined

#Variable to plot

#index
ind = "IndexLepAll_%s[0]"%(lep)

#Generated electron selection
#nSel = "ngenLep >= 1" #removes dileptonic events
#genSel1 = "(abs(genLep_pdgId[0]) == %s && abs(genLep_eta[0]) < %s)"%(pdgId, str(etaAcc)) #electron selection #index [0] ok since (only element)
#selection = combineCuts(nSel, genSel1)

pt = "LepAll_pt[%s]"%(ind)
eta = "abs(LepAll_eta[%s])"%(ind)
#pt = "genLep_pt[0]"
#eta = "genLep_eta[0]"

#Reconstructed electron selection
#deltaR = "sqrt((genLep_eta[0] - LepAll_eta)^2 + (genLep_phi[0] - LepAll_phi)^2)"

#matchSel = "(%s*(abs(LepAll_pdgId) == %s && abs(LepAll_eta) < %s && LepAll_mcMatchId != 0 && LepAll_mcMatchId != -1) < %s && (%s*(abs(LepAll_pdgId) == %s && abs(LepAll_eta) < %s && LepAll_mcMatchId != 0 && LepAll_mcMatchId != -1)) != 0)"%(deltaR, pdgId, etaAcc, deltaRcut, deltaR, pdgId, etaAcc)
#matchSel = "Sum$(LepAll_mcMatchId != 0 && LepAll_mcMatchId != -1) > 0"

#recoSel = "(abs(LepAll_pdgId) == 11 && abs(LepAll_eta) <" + str(etaAcc) + ")"
#lowPtSel = "(genLep_pt > 6 && genLep_pt < 10)" #Pt selection
#misMatchSel = "LepAll_mcMatchId == 0"

selection = "(nLepAll_{} > 0 && abs(LepAll_pdgId[{ind}]) == {} & abs(LepAll_eta[{ind}]) < {} && LepAll_mcMatchId[{ind}] != 0)".format(lep, pdgId, etaAcc, ind = ind)
#selection = "Sum$(abs(LepAll_pdgId) == %s && abs(LepAll_eta) < %s && LepAll_mcMatchId != 0) > 0"
#print selection
#xmin = 0
#xmax = 500

hists = {'FullSim':{}, 'FastSim':{}}
ratios = {}
xmax = 200
if not varBins:
   if standardBins: bins = {'pt':[20, 0, xmax], 'eta':[int(etaAcc*10), 0, etaAcc]}
   else: bins = {'pt':[int(xmax/5), 0, xmax], 'eta':[int(etaAcc*10), 0, etaAcc]} #old binning
else: #Variable bin size
   if standardBins:
      bins = {'pt': array('d', range(0,50,10) + range(50,200+150,150))}
      normFactor = {'pt': "((nLepAll_{lep} > 0)*(({var} < 50) + ({var} >= 50 && {var} < 200)*0.0666))".format(lep = lep, var = "LepAll_pt[max(IndexLepAll_%s[0], 0)]"%lep)}
   else:
      bins = {'pt': array('d', [0, 5, 12, 20, 30, 200])}
      normFactor = {'pt': "((nLepAll_{lep} > 0)*(({var} < 5) + ({var} >= 5 && {var} < 12)*0.714 + ({var} >= 12 && {var} < 20)*0.625 + ({var} >= 20 && {var} < 30)*0.5 + ({var} >= 30 && {var} < 200)*0.0294))".format(lep = lep, var = "LepAll_pt[max(IndexLepAll_%s[0], 0)]"%lep)}
      #bins = {'pt': array('d', range(0,30,5) + range(30,60,10) + range(60,100,20) + range(100,200+50,50))} #old binning
      #normFactor = {'pt': "(({var} < 30) + ({var} >= 30 && {var} < 60)*0.5 + ({var} >= 60 && {var} < 100)*0.25 + ({var} >= 100 && {var} < 200)*0.1)".format(var = pt)} #old binning

   if lep == 'mu':
      bins['eta'] = array('d', [0, 0.9, 1.2, 2.1, 2.4])
      normFactor['eta'] = "((nLepAll_{lep} > 0)*(({var} < 0.9)*0.111 + ({var} >= 0.9 && {var} < 1.2)*0.333 + ({var} >= 1.2 && {var} < 2.1)*0.111 + ({var} >= 2.1 && {var} < 2.4)*0.333))".format(lep = lep, var = "abs(LepAll_eta[max(IndexLepAll_%s[0], 0)])"%(lep))
   elif lep == 'el':
      bins['eta'] = array('d', [0, 1.4442, 1.556, 2.5])
      normFactor['eta'] = "((nLepAll_{lep} > 0)*(({var} < 1.4442)*0.0692 + ({var} >= 1.4442 && {var} < 1.556)*0.894 + ({var} >= 1.556 && {var} < 2.5)*0.106))".format(lep = lep, var = "abs(LepAll_eta[max(IndexLepAll_%s[0], 0)])"%(lep))

##################################################################################Canvas 1#############################################################################################
c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,2)

c1.cd(1)

#Efficiency
selList = [filters, preSel, selection] 
if not varBins: 
   hists['FullSim']['pt'] = makeHist(samples['ttInc'].tree, pt, "weight*(" + combineCutsList(selList) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2])
   hists['FullSim']['pt'].GetYaxis().SetTitle("Events")
else: 
   hists['FullSim']['pt'] = makeHistVarBins(samples['ttInc'].tree, pt, normFactor['pt']+ "*weight*(" + combineCutsList(selList) + ")", bins['pt'])
   if standardBins: hists['FullSim']['pt'].GetYaxis().SetTitle("Events / 10 GeV")
   else: hists['FullSim']['pt'].GetYaxis().SetTitle("Events / 5 GeV")
hists['FullSim']['pt'].SetName("FullSim_pt")
hists['FullSim']['pt'].SetTitle("%ss: FullSim vs FastSim comparison for TTJets Sample"%lepton)
hists['FullSim']['pt'].GetXaxis().SetTitle("%s p_{T} / GeV"%(lepton))
hists['FullSim']['pt'].SetFillColor(ROOT.kViolet+10)
hists['FullSim']['pt'].SetMinimum(1)
hists['FullSim']['pt'].SetMaximum(1000)
hists['FullSim']['pt'].Draw("hist")

alignStats(hists['FullSim']['pt'])

if not varBins: hists['FastSim']['pt'] = makeHist(samples['ttInc_FS'].tree, pt, "weight*(" + combineCutsList(selList) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2])
else: hists['FastSim']['pt'] = makeHistVarBins(samples['ttInc_FS'].tree, pt, normFactor['pt'] + "*weight*(" + combineCutsList(selList) + ")", bins['pt'])
hists['FastSim']['pt'].SetName("FastSim_pt")
hists['FastSim']['pt'].SetFillColor(ROOT.kRed+1)
hists['FastSim']['pt'].SetFillColorAlpha(hists['FastSim']['pt'].GetFillColor(), 0.8)
hists['FastSim']['pt'].Draw("histsame")
 
if logy: ROOT.gPad.SetLogy()

ROOT.gPad.Modified()
ROOT.gPad.Update()

l1 = makeLegend2()
l1 = ROOT.TLegend()
l1.AddEntry("FullSim_pt", "FullSim", "F")
l1.AddEntry("FastSim_pt", "FastSim", "F")
l1.Draw()

alignLegend(l1, y1=0.5, y2=0.65)

##################################################################################################################################################################################
#Efficiency curves
c1.cd(2)

#Efficiency
ratios['pt'] = makeEffPlot2(hists['FullSim']['pt'], hists['FastSim']['pt'])
ratios['pt'].SetName("ratio_pt")
ratios['pt'].Draw("P")
ratios['pt'].SetTitle("%ss: FullSim vs FastSim SFs for TTJets Sample ; %s p_{T} / GeV ; Ratio"%(lepton, lepton))
#setupEffPlot2(ratios['pt'])

ratios['pt'].SetMinimum(0.5)
ratios['pt'].SetMaximum(1.1)

#ratios['pt'].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)

#Colours
ratios['pt'].SetMarkerColor(ROOT.kGreen+3)

ROOT.gPad.Modified()
ROOT.gPad.Update()

#l2 = makeLegend2()
#l2.AddEntry("ratio_pt", "Veto", "P")
#l2.Draw()

c1.Modified()
c1.Update()

##################################################################################Canvas 1#############################################################################################
c2 = ROOT.TCanvas("c2", "Canvas 2", 1800, 1500)
c2.Divide(1,2)

c2.cd(1)

#Efficiency
if not varBins: 
   hists['FullSim']['eta'] = makeHist(samples['ttInc'].tree, eta, "weight*(" + combineCutsList(selList) + ")", bins['eta'][0], bins['eta'][1], bins['eta'][2])
   hists['FullSim']['eta'].GetYaxis().SetTitle("Events")
else: 
   hists['FullSim']['eta'] = makeHistVarBins(samples['ttInc'].tree, eta, normFactor['eta'] + "*weight*(" + combineCutsList(selList) + ")", bins['eta'])
   hists['FullSim']['eta'].GetYaxis().SetTitle("Events / 0.1 rad")
hists['FullSim']['eta'].SetName("FullSim_eta")
hists['FullSim']['eta'].SetTitle("%ss: FullSim vs FastSim comparison for TTJets Sample"%lepton)
hists['FullSim']['eta'].GetXaxis().SetTitle("%s |#eta| "%(lepton))
hists['FullSim']['eta'].SetFillColor(ROOT.kViolet+10)
hists['FullSim']['eta'].SetMinimum(1)
hists['FullSim']['eta'].SetMaximum(1000)
hists['FullSim']['eta'].Draw("hist")

alignStats(hists['FullSim']['eta'])#, y1=0.4, y2=0.6)

if not varBins: hists['FastSim']['eta'] = makeHist(samples['ttInc_FS'].tree, eta, "weight*(" + combineCutsList(selList) + ")", bins['eta'][0], bins['eta'][1], bins['eta'][2])
else: hists['FastSim']['eta'] = makeHistVarBins(samples['ttInc_FS'].tree, eta, normFactor['eta'] + "*weight*(" + combineCutsList(selList) + ")", bins['eta'])
hists['FastSim']['eta'].SetName("FastSim_eta")
hists['FastSim']['eta'].SetFillColor(ROOT.kRed+1)
hists['FastSim']['eta'].SetFillColorAlpha(hists['FastSim']['eta'].GetFillColor(), 0.8)
hists['FastSim']['eta'].Draw("histsame")
   
if logy: ROOT.gPad.SetLogy()

ROOT.gPad.Modified()
ROOT.gPad.Update()

l2 = ROOT.TLegend()
l2.AddEntry("FullSim_eta", "FullSim", "F")
l2.AddEntry("FastSim_eta", "FastSim", "F")
l2.Draw()

alignLegend(l2, y1=0.5, y2=0.65)

##################################################################################################################################################################################
#Efficiency curves
c2.cd(2)

#Efficiency
ratios['eta'] = makeEffPlot2(hists['FullSim']['eta'], hists['FastSim']['eta'])
ratios['eta'].SetName("ratio_eta")
ratios['eta'].Draw("P")
ratios['eta'].SetTitle("%ss: FullSim vs FastSim SFs for TTJets Sample ; %s |#eta| ; Ratio"%(lepton, lepton))
#setupEffPlot2(ratios['eta'])

ratios['eta'].SetMinimum(0.5)
ratios['eta'].SetMaximum(1.1)

#Colours
ratios['eta'].SetMarkerColor(ROOT.kGreen+3)

ROOT.gPad.Modified()
ROOT.gPad.Update()

#l2 = makeLegend2()
#l2.AddEntry("ratio_eta", "Veto", "P")
#l2.Draw()
c2.Modified()
c2.Update()

#2D Histograms (wrt. pT)
if not varBins: hists['FullSim']['2D'] = make2DHist(samples['ttInc'].tree, pt, eta, "weight*(" + combineCutsList(selList) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2], bins['eta'][0], bins['eta'][1], bins['eta'][2])
else: hists['FullSim']['2D'] = make2DHistVarBins(samples['ttInc'].tree, pt, eta, normFactor['pt'] + "*" + normFactor['eta'] + "*weight*(" + combineCutsList(selList) + ")", bins['pt'], bins['eta'])
hists['FullSim']['2D'].SetName("FullSim_2D")
hists['FullSim']['2D'].SetTitle("%s p_{T} vs |#eta| Distribution in FullSim TTJets Sample"%(lepton))
hists['FullSim']['2D'].GetXaxis().SetTitle("%s p_{T}"%lepton)
hists['FullSim']['2D'].GetYaxis().SetTitle("%s |#eta|"%lepton)
#hist.GetZaxis().SetRangeUser(0, 4)
#alignStats(hist)

#2D Histograms (wrt. pT)
if not varBins: hists['FastSim']['2D'] = make2DHist(samples['ttInc_FS'].tree, pt, eta, "weight*(" + combineCutsList(selList) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2], bins['eta'][0], bins['eta'][1], bins['eta'][2])
else: hists['FastSim']['2D'] = make2DHistVarBins(samples['ttInc_FS'].tree, pt, eta, normFactor['pt'] + "*" + normFactor['eta'] + "*weight*(" + combineCutsList(selList) + ")", bins['pt'], bins['eta'])
hists['FastSim']['2D'].SetName("FastSim_2D")
hists['FastSim']['2D'].SetTitle("%s p_{T} vs |#eta| Distribution in FastSim TTJets Sample"%(lepton))
hists['FastSim']['2D'].GetXaxis().SetTitle("%s p_{T}"%lepton)
hists['FastSim']['2D'].GetYaxis().SetTitle("%s |#eta|"%lepton)

ratios['2D'] = makeEffPlot2(hists['FullSim']['2D'], hists['FastSim']['2D'])
ratios['2D'].SetName("ratios_2D")
ratios['2D'].SetTitle("%ss: FullSim vs FastSim SFs for TTJets Sample"%lepton)
ratios['2D'].GetXaxis().SetTitle("%s p_{T}"%lepton)
ratios['2D'].GetYaxis().SetTitle("%s |#eta|"%lepton)
ratios['2D'].SetMarkerSize(0.8)
#ratios['2D'].SetMinimum(0.8)
#ratios['2D'].SetMaximum(5)
ratios['2D'].GetZaxis().SetRangeUser(0.8,1.2)

c4 = ROOT.TCanvas("c4", "Canvas 4", 1800, 1500)
ratios['2D'].Draw("COLZ TEXT89") #CONT1-5 #plots the graph with axes and points

alignStats(ratios['2D'])

#if logy: ROOT.gPad.SetLogz()
c4.Modified()
c4.Update()

c3 = ROOT.TCanvas("c3", "Canvas 3", 1800, 1500)
c3.Divide(1,2)

c3.cd(1)
hists['FastSim']['2D'].Draw("COLZ") #CONT1-5 #plots the graph with axes and points
if logy: ROOT.gPad.SetLogz()

c3.cd(2)
hists['FullSim']['2D'].Draw("COLZ") #CONT1-5 #plots the graph with axes and points
if logy: ROOT.gPad.SetLogz()
c3.Modified()
c3.Update()

#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   c1.SaveAs("%s/TTJets_FastVsFullSim_lepPt%s.png"%(savedir, suffix))
   c1.SaveAs("%s/pdf/TTJets_FastVsFullSim_lepPt%s.pdf"%(savedir, suffix))
   c1.SaveAs("%s/root/TTJets_FastVsFullSim_lepPt%s.root"%(savedir, suffix))
   
   c2.SaveAs("%s/TTJets_FastVsFullSim_lepEta%s.png"%(savedir, suffix))
   c2.SaveAs("%s/pdf/TTJets_FastVsFullSim_lepEta%s.pdf"%(savedir, suffix))
   c2.SaveAs("%s/root/TTJets_FastVsFullSim_lepEta%s.root"%(savedir, suffix))
   
   c3.SaveAs("%s/TTJets_FastVsFullSim_2D_distributions%s.png"%(savedir, suffix))
   c3.SaveAs("%s/pdf/TTJets_FastVsFullSim_2D_distributions%s.pdf"%(savedir, suffix))
   c3.SaveAs("%s/root/TTJets_FastVsFullSim_2D_distributions%s.root"%(savedir, suffix))
   
   c4.SaveAs("%s/TTJets_FastVsFullSim_2D_SFs%s.png"%(savedir, suffix))
   c4.SaveAs("%s/pdf/TTJets_FastVsFullSim_2D_SFs%s.pdf"%(savedir, suffix))
   c4.SaveAs("%s/root/TTJets_FastVsFullSim_2D_SFs%s.root"%(savedir, suffix))
