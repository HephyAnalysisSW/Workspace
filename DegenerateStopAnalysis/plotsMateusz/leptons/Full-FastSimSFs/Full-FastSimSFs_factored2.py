# Full-FastSimSFs_factored2.py
# Determination of factored out HI & IP FullSim-FastSim SFs using indicies (mu2 only without these cuts)
# Mateusz Zarucki 2016

import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style, makeDir
#from Workspace.DegenerateStopAnalysis.tools.degCuts import Cuts
from Workspace.DegenerateStopAnalysis.tools.getSamples_8012 import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from array import array
from math import pi, sqrt #cos, sin, sinh, log

ROOT.gStyle.SetOptStat(1111) #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--lep", dest = "lep",  help = "Lepton", type = str, default = "mu")
parser.add_argument("--base", dest = "base",  help = "Base cut", type = str, default = "ID")
parser.add_argument("--variable", dest = "variable",  help = "Variable", type = str, default = "HI+IP")
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
base = args.base
variable = args.variable
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
ppsDir = '/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/8012_mAODv2_v3_1/80X_postProcessing_v10/analysisHephy_13TeV_2016_v0/step1'

mc_path     = ppsDir + "/RunIISpring16MiniAODv2_v3_1"
signal_path = ppsDir + "/RunIISpring16MiniAODv2_v3_1"
data_path   = ppsDir + "/Data2016_v3_1"

cmgPP = cmgTuplesPostProcessed(mc_path, signal_path, data_path)

#if getData: samplesList.append("dblind")

samples = getSamples(cmgPP = cmgPP, skim = 'preIncLep', sampleList = ['tt'], scan = False, useHT = False, getData = 0)

#officialSignals = ["s300_290", "s300_270", "s300_250"] #FIXME: crosscheck if these are in allOfficialSignals

samplesList = ['ttInc', 'ttInc_FS']

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
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/leptonSFs/factored2/"
   
   savedir += base + "_base/" + variable
 
   if standardBins: savedir += "/standardBins"
   else: savedir += "/myBins"
   
   if varBins: savedir += "/varBins"
   else: savedir += "/fixedBins"

   savedir += "/" + lepton
 
   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")
   
   suffix = "_" + variable + "_" + lepton
   
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

#index
ind1 = "IndexLepAll_%s[0]"%(lep)
ind2 = "IndexLepAll_%s2[0]"%(lep)

#Generated electron selection
#nSel = "ngenLep >= 1" #removes dileptonic events
#genSel1 = "(abs(genLep_pdgId[0]) == %s && abs(genLep_eta[0]) < %s)"%(pdgId, str(etaAcc)) #electron selection #index [0] ok since (only element)
#selection = combineCuts(nSel, genSel1)

pt = "LepAll_pt[%s]"%(ind2)
eta = "abs(LepAll_eta[%s])"%(ind2)
#pt = "genLep_pt[0]"
#eta = "genLep_eta[0]"


baseSel = "(nLepAll_{}2 > 0 && abs(LepAll_pdgId[{ind}]) == {} && abs(LepAll_eta[{ind}]) < {} && LepAll_mcMatchId[{ind}] != 0)".format(lep, pdgId, etaAcc, ind = ind2)
selection = "(nLepAll_{} > 0 && abs(LepAll_pdgId[{ind}]) == {} && abs(LepAll_eta[{ind}]) < {} && LepAll_mcMatchId[{ind}] != 0)".format(lep, pdgId, etaAcc, ind = ind1)

#baseString = "(abs(LepAll_pdgId) == {} && LepAll_pt > 5 && abs(LepAll_eta) < {} && {} && LepAll_mcMatchId != 0)".format(pdgId, etaAcc, IDCut)
#baseString = "(abs(LepAll_pdgId) == {} && LepAll_pt > 5 && abs(LepAll_eta) < {} && LepAll_mcMatchId != 0)".format(pdgId, etaAcc)

#if lep == "mu": ID = "looseMuonId"
#elif lep == "el": ID = "SPRING15_25ns_v1" # >= 1 = Veto ID
#IDCut = "LepAll_%s >= 1"%(ID)

#dzCut = "abs(LepAll_dz[%s]) < 0.5"
#dxyCut = "abs(LepAll_dxy) < 0.02"
#hybIsoCut = "(LepAll_relIso03*min(LepAll_pt, 25)) < 5" 
#hybIsoCut = "(LepAll_absIso03/LepAll_pt*min(LepAll_pt, 25)) < 5" 
#hybIsoCut = "((LepAll_absIso03 < 5) || (LepAll_relIso03 < 0.2))"
#hybIsoCut = "1"

#if variable == "HI": selString = combineCuts(baseString, hybIsoCut)
#elif variable == "IP": selString = combineCuts(baseString, dxyCut, dzCut)
#elif variable == "HI+IP": selString = combineCutsList([baseString, hybIsoCut, dxyCut, dzCut])
#else:
#   print "Wrong base + variable combination."
#   sys.exit(0)

#print selection
#xmin = 0
#xmax = 500

print baseSel
print selection

baseSelList = [filters, preSel, baseSel]
selList = [filters, preSel, baseSel, selection]

print "cutstr1: (" + combineCutsList(baseSelList) + ")"
print "cutstr2: (" + combineCutsList(selList) + ")"

hists = {'FullSim':{'pt':{}, 'eta':{}, '2D':{}}, 'FastSim':{'pt':{}, 'eta':{}, '2D':{}}}
ratios = {'ID':{}, 'FullSim':{}, 'FastSim':{}, 'Full-Fast':{}}

xmax = 200
if not varBins:
   if standardBins: bins = {'pt':[20, 0, xmax], 'eta':[int(etaAcc*10), 0, etaAcc]}
   else: bins = {'pt':[int(xmax/5), 0, xmax], 'eta':[int(etaAcc*10), 0, etaAcc]} #old binning
else: #Variable bin size
   if standardBins:
      bins = {'pt': array('d', range(0,50,10) + range(50,200+150,150))}
      #normFactor = {'pt': "((nLepAll_{lep} > 0)*(({var} < 50) + ({var} >= 50 && {var} < 200)*0.0666))".format(lep = lep, var = "LepAll_pt[max(IndexLepAll_%s[0], 0)]"%lep)}
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
      
normFactor = {'pt': "1", 'eta': "1"}

for sim in ['FullSim', 'FastSim']:

   if sim == 'FullSim': sample = 'ttInc'
   elif sim == 'FastSim': sample = 'ttInc_FS'

   #print sim, " : ", sample

   ##################################################################################Canvas 1#############################################################################################
   
   #Efficiency of variable 
   
   c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
   c1.Divide(1,2)
   
   c1.cd(1)
   
   #Efficiency
   if not varBins: 
      hists[sim]['pt']['den'] = makeHist(samples[sample].tree, pt, "weight*(" + combineCutsList(baseSelList) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2])
      hists[sim]['pt']['den'].GetYaxis().SetTitle("Events")
   else: 
      hists[sim]['pt']['den'] = makeHistVarBins(samples[sample].tree, pt, normFactor['pt']+ "*weight*(" + combineCutsList(baseSelList) + ")", bins['pt'])
      if standardBins: hists[sim]['pt']['den'].GetYaxis().SetTitle("Events / 10 GeV")
      else: hists[sim]['pt']['den'].GetYaxis().SetTitle("Events / 5 GeV")

   hists[sim]['pt']['den'].SetName("%s_pt_den"%(sim))
   hists[sim]['pt']['den'].SetTitle("%ss: %s Efficiency for %s TTJets Sample"%(lepton, variable, sim))
   hists[sim]['pt']['den'].GetXaxis().SetTitle("%s p_{T} / GeV"%lepton)
   hists[sim]['pt']['den'].SetFillColor(ROOT.kViolet+10)
   hists[sim]['pt']['den'].SetMinimum(1)
   hists[sim]['pt']['den'].SetMaximum(10000)
   hists[sim]['pt']['den'].Draw("hist")
   
   alignStats(hists[sim]['pt']['den'])
   
   if not varBins: hists[sim]['pt']['num'] = makeHist(samples[sample].tree, pt, "weight*(" + combineCutsList(selList) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2])
   else: hists[sim]['pt']['num'] = makeHistVarBins(samples[sample].tree, pt, normFactor['pt'] + "*weight*(" + combineCutsList(selList) + ")", bins['pt'])
   hists[sim]['pt']['num'].SetName("%s_pt_num"%sim)
   hists[sim]['pt']['num'].SetFillColor(ROOT.kRed+1)
   hists[sim]['pt']['num'].SetFillColorAlpha(hists[sim]['pt']['num'].GetFillColor(), 0.8)
   hists[sim]['pt']['num'].Draw("histsame")
    
   if logy: ROOT.gPad.SetLogy()
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   l1 = makeLegend2()
   l1 = ROOT.TLegend()
   l1.AddEntry("%s_pt_den"%(sim), "%s"%sim, "F")
   l1.AddEntry("%s_pt_num"%(sim), "%s (%s)"%(sim, variable), "F")
   l1.Draw()
   
   alignLegend(l1, y1=0.5, y2=0.65)
   
   ############################################################################################
   #Efficiency curves
   c1.cd(2)
   
   #Efficiency
   ratios[sim]['pt'] = makeEffPlot(hists[sim]['pt']['num'], hists[sim]['pt']['den'])
   ratios[sim]['pt'].SetName("%s_ratio_pt"%sim)
   #ratios[sim]['pt'].Draw("P")
   ratios[sim]['pt'].Draw("AP")
   ratios[sim]['pt'].SetTitle("%ss: %s Efficiency for %s TTJets Sample"%(lepton, variable, sim))
   #ratios[sim]['pt'].GetXaxis().SetTitle("%s p_{T} / GeV"%lepton)
   #setupEffPlot2(ratios['pt'])
   
   #ratios[sim]['pt'].SetMinimum(0.8)
   #ratios[sim]['pt'].SetMaximum(1.1)
   
   #Colours
   ratios[sim]['pt'].SetMarkerColor(ROOT.kGreen+3)
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   ratios[sim]['pt'].GetPaintedGraph().GetXaxis().SetTitle("%s p_{T} / GeV"%lepton)
   ratios[sim]['pt'].GetPaintedGraph().SetMinimum(0.5)
   ratios[sim]['pt'].GetPaintedGraph().SetMaximum(1.1)
   #ratios[sim]['pt'].GetPaintedGraph().GetYaxis().SetLimits(0, 1.1)
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   #l2 = makeLegend2()
   #l2.AddEntry("ratio_pt", "Veto", "P")
   #l2.Draw()
   
   c1.Modified()
   c1.Update()
   
   ##################################################################################Canvas 1#############################################################################################
   
   #%s Efficiency of variable 
   
   c2 = ROOT.TCanvas("c2", "Canvas 2", 1800, 1500)
   c2.Divide(1,2)
   
   c2.cd(1)
   
   #Efficiency
   if not varBins: 
      hists[sim]['eta']['den'] = makeHist(samples[sample].tree, eta, "weight*(" + combineCutsList(baseSelList) + ")", bins['eta'][0], bins['eta'][1], bins['eta'][2])
      hists[sim]['eta']['den'].GetYaxis().SetTitle("Events")
   else: 
      hists[sim]['eta']['den'] = makeHistVarBins(samples[sample].tree, eta, normFactor['eta']+ "*weight*(" + combineCutsList(baseSelList) + ")", bins['eta'])
      hists[sim]['eta']['den'].GetYaxis().SetTitle("Events / 0.1 rad")
   hists[sim]['eta']['den'].SetName("%s_eta_den"%sim)
   hists[sim]['eta']['den'].SetTitle("%ss: %s Efficiency for %s TTJets Sample"%(lepton, variable, sim))
   hists[sim]['eta']['den'].GetXaxis().SetTitle("%s |#eta|"%lepton)
   hists[sim]['eta']['den'].SetFillColor(ROOT.kViolet+10)
   hists[sim]['eta']['den'].SetMinimum(1)
   hists[sim]['eta']['den'].SetMaximum(10000)
   hists[sim]['eta']['den'].Draw("hist")
   
   alignStats(hists[sim]['eta']['den'])
   
   if not varBins: hists[sim]['eta']['num'] = makeHist(samples[sample].tree, eta, "weight*(" + combineCutsList(selList) + ")", bins['eta'][0], bins['eta'][1], bins['eta'][2])
   else: hists[sim]['eta']['num'] = makeHistVarBins(samples[sample].tree, eta, normFactor['eta'] + "*weight*(" + combineCutsList(selList) + ")", bins['eta'])
   hists[sim]['eta']['num'].SetName("%s_eta_num"%sim)
   hists[sim]['eta']['num'].SetFillColor(ROOT.kRed+1)
   hists[sim]['eta']['num'].SetFillColorAlpha(hists[sim]['eta']['num'].GetFillColor(), 0.8)
   hists[sim]['eta']['num'].Draw("histsame")
    
   if logy: ROOT.gPad.SetLogy()
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   l2 = makeLegend2()
   l2 = ROOT.TLegend()
   l2.AddEntry("%s_eta_den"%sim, "%s"%sim, "F")
   l2.AddEntry("%s_eta_num"%sim, "%s (%s)"%(sim, variable), "F")
   l2.Draw()
   
   alignLegend(l2, y1=0.8, y2=0.65)
   
   ############################################################################################
   #Efficiency curves
   c2.cd(2)
   
   #Efficiency
   ratios[sim]['eta'] = makeEffPlot(hists[sim]['eta']['num'], hists[sim]['eta']['den'])
   ratios[sim]['eta'].SetName("%s_ratio_eta"%sim)
   ratios[sim]['eta'].Draw("AP")
   #ratios[sim]['eta'].Draw("P")
   ratios[sim]['eta'].SetTitle("%ss: %s Efficiency for %s TTJets Sample"%(lepton, variable, sim))
   #ratios[sim]['eta'].GetXaxis().SetTitle("%s |#eta|"%lepton)
   #setupEffPlot2(ratios['eta'])
   
   #ratios[sim]['eta'].SetMinimum(0.5)
   #ratios[sim]['eta'].SetMaximum(1.1)
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   ratios[sim]['eta'].GetPaintedGraph().GetXaxis().SetTitle("%s |#eta|"%lepton)
   ratios[sim]['eta'].GetPaintedGraph().SetMinimum(0.5)
   ratios[sim]['eta'].GetPaintedGraph().SetMaximum(1.1)
   #ratios[sim]['eta'].GetPaintedGraph().GetYaxis().SetLimits(0, 1.1)
   
   #Colours
   ratios[sim]['eta'].SetMarkerColor(ROOT.kGreen+3)
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   #l2 = makeLegend2()
   #l2.AddEntry("ratio_eta", "Veto", "P")
   #l2.Draw()
   
   c2.Modified()
   c2.Update()
   
   #2D Histograms (wrt. pT)
   if not varBins: hists[sim]['2D']['den'] = make2DHist(samples[sample].tree, pt, eta, "weight*(" + combineCutsList(baseSelList) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2], bins['eta'][0], bins['eta'][1], bins['eta'][2])
   else: hists[sim]['2D']['den'] = make2DHistVarBins(samples[sample].tree, pt, eta, normFactor['pt'] + "*" + normFactor['eta'] + "*weight*(" + combineCutsList(baseSelList) + ")", bins['pt'], bins['eta'])
   hists[sim]['2D']['den'].SetName("%s_2D_den"%sim)
   hists[sim]['2D']['den'].SetTitle("%s p_{T} vs |#eta| Distribution in %s TTJets Sample"%(lepton, sim))
   hists[sim]['2D']['den'].GetXaxis().SetTitle("%s p_{T}"%lepton)
   hists[sim]['2D']['den'].GetYaxis().SetTitle("%s |#eta|"%lepton)
   #hist.GetZaxis().SetRangeUser(0, 4)
   #alignStats(hist)
   
   #2D Histograms (wrt. pT)
   if not varBins: hists[sim]['2D']['num'] = make2DHist(samples[sample].tree, pt, eta, "weight*(" + combineCutsList(selList) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2], bins['eta'][0], bins['eta'][1], bins['eta'][2])
   else: hists[sim]['2D']['num'] = make2DHistVarBins(samples[sample].tree, pt, eta, normFactor['pt'] + "*" + normFactor['eta'] + "*weight*(" + combineCutsList(selList) + ")", bins['pt'], bins['eta'])
   hists[sim]['2D']['num'].SetName("%s_2D_num"%sim)
   hists[sim]['2D']['num'].SetTitle("%s p_{T} vs |#eta| Distribution in %s TTJets Sample"%(lepton, sim))
   hists[sim]['2D']['num'].GetXaxis().SetTitle("%s p_{T}"%lepton)
   hists[sim]['2D']['num'].GetYaxis().SetTitle("%s |#eta|"%lepton)
   
   ratios[sim]['2D'] = makeEffPlot(hists[sim]['2D']['num'], hists[sim]['2D']['den'])
   ratios[sim]['2D'].SetName("%s_ratios_2D"%sim)
   ratios[sim]['2D'].SetTitle("%s Efficiency for %s TTJets Sample"%(variable, sim))
   #ratios[sim]['2D'].GetXaxis().SetTitle("%s p_{T}"%lepton)
   #ratios[sim]['2D'].GetYaxis().SetTitle("%s |#eta|"%lepton)
   ratios[sim]['2D'].SetMarkerSize(0.8)
   #ratios[sim]['2D'].SetMinimum(0.5)
   #ratios[sim]['2D'].SetMaximum(5)
   #ratios[sim]['2D'].GetZaxis().SetRangeUser(0.5, 5)
   
   if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
      c1.SaveAs("%s/TTJets_%s_lepPt%s.png"%(savedir, sim, suffix))
      c1.SaveAs("%s/pdf/TTJets_%s_lepPt%s.pdf"%(savedir, sim, suffix))
      c1.SaveAs("%s/root/TTJets_%s_lepPt%s.root"%(savedir, sim, suffix))
      
      c2.SaveAs("%s/TTJets_%s_lepEta%s.png"%(savedir, sim, suffix))
      c2.SaveAs("%s/pdf/TTJets_%s_lepEta%s.pdf"%(savedir, sim, suffix))
      c2.SaveAs("%s/root/TTJets_%s_lepEta%s.root"%(savedir, sim, suffix))
   
c5 = ROOT.TCanvas("c5", "Canvas 5", 1800, 1500)

a = ratios['FullSim']['2D'].GetPassedHistogram().Clone()
b = ratios['FullSim']['2D'].GetTotalHistogram().Clone()
c = ratios['FastSim']['2D'].GetPassedHistogram().Clone()
d = ratios['FastSim']['2D'].GetTotalHistogram().Clone()

a.Divide(b)
c.Divide(d)

ratios['Full-Fast']['2D'] = divideHists(a,c)
ratios['Full-Fast']['2D'].SetName("Full-Fast_ratios_2D")
ratios['Full-Fast']['2D'].SetTitle("%ss: FullSim-FastSim SFs for TTJets Sample"%lepton)
ratios['Full-Fast']['2D'].GetXaxis().SetTitle("%s p_{T}"%lepton)
ratios['Full-Fast']['2D'].GetYaxis().SetTitle("%s |#eta|"%lepton)
ratios['Full-Fast']['2D'].SetMarkerSize(0.8)
#ratios['Full-Fast']['2D'].SetMinimum(0.8)
#ratios['Full-Fast']['2D'].SetMaximum(1.1)
ratios['Full-Fast']['2D'].GetZaxis().SetRangeUser(0.8,1.2)

ratios['Full-Fast']['2D'].Draw("COLZ TEXT89") #CONT1-5 #plots the graph with axes and points
   
alignStats(ratios['Full-Fast']['2D'])

c5.Modified()
c5.Update()
      
c5.SaveAs("%s/TTJets_Full-FastSimSFs%s.png"%(savedir, suffix))
c5.SaveAs("%s/pdf/TTJets_Full-FastSimSFs%s.pdf"%(savedir, suffix))
c5.SaveAs("%s/root/TTJets_Full-FastSimSFs%s.root"%(savedir, suffix))

c6 = ROOT.TCanvas("c6", "Canvas 6", 1800, 1500)

if not varBins: ratios['Full-Fast']['pt'] = divideEff(ratios['FullSim']['pt'], ratios['FastSim']['pt'])
else: ratios['Full-Fast']['pt'] = divideEffVarBins(ratios['FullSim']['pt'], ratios['FastSim']['pt'])
ratios['Full-Fast']['pt'].SetName("Full-Fast_ratios_pt")
ratios['Full-Fast']['pt'].SetTitle("%ss: FullSim-FastSim SFs for TTJets Sample"%lepton)
ratios['Full-Fast']['pt'].GetXaxis().SetTitle("%s p_{T}"%lepton)
ratios['Full-Fast']['pt'].GetYaxis().SetTitle("FullSim-FastSim SF")
ratios['Full-Fast']['pt'].GetXaxis().CenterTitle()
ratios['Full-Fast']['pt'].GetYaxis().CenterTitle()
ratios['Full-Fast']['pt'].GetXaxis().SetTitleOffset(1.3)
ratios['Full-Fast']['pt'].GetYaxis().SetTitleOffset(1.3)
ratios['Full-Fast']['pt'].SetMarkerSize(0.8)
ratios['Full-Fast']['pt'].SetMinimum(0.8)
ratios['Full-Fast']['pt'].SetMaximum(1.1)
ratios['Full-Fast']['pt'].GetXaxis().SetLimits(0,205)
ratios['Full-Fast']['pt'].Draw("AP") #CONT1-5 #plots the graph with axes and points
   
#alignStats(ratios['Full-Fast']['pt'])

c6.Modified()
c6.Update()

c6.SaveAs("%s/TTJets_Full-FastSimSFs_pt%s.png"%(savedir, suffix))
c6.SaveAs("%s/pdf/TTJets_Full-FastSimSFs_pt%s.pdf"%(savedir, suffix))
c6.SaveAs("%s/root/TTJets_Full-FastSimSFs_pt%s.root"%(savedir, suffix))
  
for sim in ['FullSim', 'FastSim']:
 
   c4 = ROOT.TCanvas("c4", "Canvas 4", 1800, 1500)
   ratios[sim]['2D'].Draw("COLZ TEXT89") #CONT1-5 #plots the graph with axes and points
   #alignStats(ratios[sim]['2D'])
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   #ratios[sim]['2D'].GetPaintedGraph().SetMaximum(5)
   
   #if logy: ROOT.gPad.SetLogz()
   c4.Modified()
   c4.Update()
   
   c3 = ROOT.TCanvas("c3", "Canvas 3", 1800, 1500)
   c3.Divide(1,2)
   
   c3.cd(1)
   hists[sim]['2D']['den'].Draw("COLZ") #CONT1-5 #plots the graph with axes and points
   if logy: ROOT.gPad.SetLogz()
   
   c3.cd(2)
   hists[sim]['2D']['num'].Draw("COLZ") #CONT1-5 #plots the graph with axes and points
   if logy: ROOT.gPad.SetLogz()
   c3.Modified()
   c3.Update()
   
   #Save canvas
   if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
      c3.SaveAs("%s/TTJets_%s_2D_distributions%s.png"%(savedir, sim, suffix))
      c3.SaveAs("%s/pdf/TTJets_%s_2D_distributions%s.pdf"%(savedir, sim, suffix))
      c3.SaveAs("%s/root/TTJets_%s_2D_distributions%s.root"%(savedir, sim, suffix))
      
      c4.SaveAs("%s/TTJets_%s_2D_eff%s.png"%(savedir, sim, suffix))
      c4.SaveAs("%s/pdf/TTJets_%s_2D_eff%s.pdf"%(savedir, sim, suffix))
      c4.SaveAs("%s/root/TTJets_%s_2D_eff%s.root"%(savedir, sim, suffix))

##Sets TDR style
#setup_style()
#
#plotDict = {
#   "lep_mt":           {'var':"LepAll_mt[IndexLepAll_lep[0]]"       ,"bins":[40,0,200]          ,"nMinus1":None         ,"decor":{"title":"lepMT"    ,"x":"M_{{T}}({lepLatex}) "      ,"y":"Events"  ,'log':[0,logy,0] }},
#   "lepPt" :        {'var':"LepAll_pt[IndexLepAll_lep[0]]"       ,"bins":[10,0,200]          ,"nMinus1":""      ,"decor":{"title":"lepPt"           ,"x":"Lepton p_{T}"      ,"y":"Events"  ,'log':[0,logy,0] }},
#   "lep_Eta" :       {'var':"LepAll_eta[IndexLepAll_lep[0]]"                         ,"bins":[20,-3,3]           ,"nMinus1":""         ,"decor":{"title":"lepEta"     ,"x":"#eta({lepLatex})"       ,"y":"Events  "  ,'log':[0,logy,0] }},
#   "lep_Phi" :      {'var':"LepAll_phi[IndexLepAll_lep[0]]"                         ,"bins":[20,-3.15,3.15]           ,"nMinus1":None         ,"decor":{"title":"lepPhi"     ,"x":"lep Phi"      ,"y":"Events  "  ,'log':[0,logy,0] }},
#   "met":          {'var':"met"                            ,"bins":[40,200,1000]        ,"nMinus1":"met"        ,"decor":{"title":"MET"    ,"x":"E^{miss}_{T}"      ,"y":"Events"  ,'log':[0,logy,0] }},
#   "ht":           {'var':"ht_basJet"                     ,"bins":[40,200,1000]        ,"nMinus1":""           ,"decor":{"title":"HT"    ,"x":"H_{T}"      ,"y":"Events"  ,'log':[0,logy,0] }},
#   "ct":           {'var':"min(met_pt,ht_basJet)"         ,"bins":[40,100,1000]        ,"nMinus1":""           ,"decor":{"title":"CT"    ,"x":"C_{T}"      ,"y":"Events"  ,'log':[0,logy,0] }},
#   "MetPhi":       {'var':"met_phi"                        ,"bins":[20,-3.15,3.15]           ,"nMinus1":None         ,"decor":{"title":"MetPhi"    ,"x":"Met Phi"      ,"y":"Events"  ,'log':[0,logy,0] }},
#   "isrPt":        {'var':"Jet_pt[IndexJet_basJet[0]]"     ,"bins":[45,100,1000]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet P_{{T}}"    ,"x":"isrJetPt"      ,"y":"Events  "  ,'log':[0,logy,0] }},
#   "isrPt2":       {'var':"Jet_pt[IndexJet_basJet[0]]"     ,"bins":[20,100,900]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet P_{{T}}"    ,"x":"isrJetPt"      ,"y":"Events  "  ,'log':[0,logy,0] }},
#   "isrPt_fine":   {'var':"Jet_pt[IndexJet_basJet[0]]"    ,"bins":[100,0,1000]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet P_{{T}} "    ,"x":"isrJetPt"      ,"y":"Events  "  ,'log':[0,logy,0] }},
#   "nJets30":      {'var':"nBasJet"                       ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 30GeV"    ,"x":"Number of Jets with P_{T} > 30GeV"      ,"y":"Events  "  ,'log'
#   "nJets60":      {'var':"nVetoJet"                      ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 60GeV"    ,"x":"Number of Jets with P_{T} > 60GeV"      ,"y":"Events  "  ,'log'
#   "nSoftBJets":   {'var':"(nBSoftJet)"                   ,"bins":[6,0,6]            ,"nMinus1":None         ,"decor":{"title":"Number of Soft B-Tagged Jets with P_{{T}} < 60GeV"    ,"x":"Number of Soft B-Tagged Jets with P_{T} < 60GeV"
#   "nHardBJets":   {'var':"(nBHardJet)"                   ,"bins":[6,0,6]            ,"nMinus1":None         ,"decor":{"title":"Number of B-Tagged Jets with P_{{T}} > 60GeV"    ,"x":"Number of Hard B-Tagged Jets with P_{T} > 60GeV"
#   "nBJets":       {'var':"(nBHardJet + nBSoftJet)"       ,"bins":[6,0,6]            ,"nMinus1":None         ,"decor":{"title":"Number of B-Tagged Jets"                         ,"x":"Number of B-Tagged Jets"      ,"y":"Events  "  ,'log':
#   "bJetPt":       {'var':"Jet_pt[ max(IndexJet_bJet[0],0)] *(nBJet>0)"      ,"bins":[100,0,1000]          ,"nMinus1":None         ,"decor":{"title":"bJet P_{{T}} "    ,"x":"P_{T}(BJet)"      ,"y":"Events  "  ,'log':[0,logy,0] }},
#   "bSoftJetPt":       {'var':"Jet_pt[ max(IndexJet_bSoftJet[0],0)] *(nBSoftJet>0)"      ,"bins":[10,20,70]          ,"nMinus1":None         ,"decor":{"title":"bSoftJet P_{{T}} "    ,"x":"P_{T}(Soft BJet)"      ,"y":"Events  "  ,'log':[0
#   "bHardJetPt":       {'var':"Jet_pt[ max(IndexJet_bHardJet[0],0)] *(nBHardJet>0)"      ,"bins":[100,0,1000]          ,"nMinus1":None         ,"decor":{"title":"bHardJet P_{{T}} "    ,"x":"P_{T}(Hard BJet)"      ,"y":"Events  "  ,'log':
#   }
#
#
#WTT_plots = getPlots(samples, plotsDict, cut, samplesList, plotList = ["lepPt"], addOverFlowBin='upper')
##if getData: WTT_plots2 = drawPlots(samples, plotsDict, degcuts.presel, samplesList, plotList = ["lepPt"], plotLimits = [1, 100], denoms=["bkg"], noms = ["bkg"], fom="RATIO", fomLimits=[0,1.8], normalize = False, save=False) #, plotMin =
##else: WTT_plots2 = drawPlots(samples, plotsDict, degcuts.presel, samplesList, plotList = ["lepPt"], plotMin = 1, normalize = True, save = False)
#WTT_plots2 = drawPlots(samples, plotsDict, cut, samplesList, plotList = ["lepPt"], plotLimits = [1, 100], denoms=["w"], noms = ["tt"], fom="RATIO", fomLimits=[0,1.8], normalize = False, save=False) #, plotMin = 0.1
##Save canvas
#if save: #web address: http://www.hephy.at/user/mzarucki/plots
#      for canv in WTT_plots2['canvs']:
#         #if plot['canvs'][canv][0]:
#         WTT_plots2['canvs'][canv][0].SaveAs("%s/WTT_%s%s.png"%(savedir, canv, suffix))
#         WTT_plots2['canvs'][canv][0].SaveAs("%s/root/WTT_%s%s.root"%(savedir, canv, suffix))
#         WTT_plots2['canvs'][canv][0].SaveAs("%s/pdf/WTT_%s%s.pdf"%(savedir, canv, suffix))

##single-electron events (semileptonic & dileptonic)
#elif nEles == "1": #semileptonic
#   #Generated electron selection
#   nSel = "ngenLep > 0" #redundant with genSel2 #nLepAll > 0 introduces bias
#   genSel1 = "(abs(genLep_pdgId) == 11 && abs(genLep_eta) < " + str(etaAcc) + ")" #electron selection (includes dielectron evts) #ngenLep == 1 would remove dileptonic events # index [0] does not include single-electron events with muon 
#   genSel2 = "(Sum$(abs(genLep_pdgId) == 11 && abs(genLep_eta) < " + str(etaAcc) + ") == 1)" # = number of electrons (includes dileptonic and semileptonic events) 
#   genSel = nSel + "&&" + genSel1 + "&&" + genSel2
#
#elif nEles == "2": #dileptonic
#   nSel = "ngenLep == 2" #does not include single-lepton events 
#   genSel1 = "(abs(genLep_pdgId) == 11 && abs(genLep_eta) < " + str(etaAcc) + ")" #electron selection (includes dielectron evts) #ngenLep == 1 would remove dileptonic events
#   genSel2 = "(Sum$(abs(genLep_pdgId) == 11 && abs(genLep_eta) < " + str(etaAcc) + ") == 2)" # = number of electrons (includes dilepton events only) 
#   genSel = nSel + "&&" + genSel1 + "&&" + genSel2
