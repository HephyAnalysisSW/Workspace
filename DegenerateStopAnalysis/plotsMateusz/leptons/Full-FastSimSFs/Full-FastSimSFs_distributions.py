# distributions.py
# Distributions of HI & IP in FullSim and FastSim samples 
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
parser.add_argument("--variable", dest = "variable",  help = "Variable", type = str, default = "all")
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
samplesList = ["tt"] #"qcd", "vv", "st", "dy", "z", "tt", "w"]
#if getData: samplesList.append("dblind")

cmgPP = cmgTuplesPostProcessed()
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
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/leptonSFs/distributions"
   
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

#Variable to plot

#Generated electron selection
#nSel = "ngenLep >= 1" #removes dileptonic events
#genSel1 = "(abs(genLep_pdgId[0]) == %s && abs(genLep_eta[0]) < %s)"%(pdgId, str(etaAcc)) #electron selection #index [0] ok since (only element)
#selection = combineCuts(nSel, genSel1)

var1 = "LepAll_relIso03*min(LepAll_pt, 25)"
var2 = "abs(LepAll_dxy)"
#var1 = "LepAll_pt"#[%s]"%(ind)
#var2 = "abs(LepAll_eta)"#[%s])"%(ind)

#Reconstructed electron selection
#deltaR = "sqrt((genLep_eta[0] - LepAll_eta)^2 + (genLep_phi[0] - LepAll_phi)^2)"

#matchSel = "(%s*(abs(LepAll_pdgId) == %s && abs(LepAll_eta) < %s && LepAll_mcMatchId != 0 && LepAll_mcMatchId != -1) < %s && (%s*(abs(LepAll_pdgId) == %s && abs(LepAll_eta) < %s && LepAll_mcMatchId != 0 && LepAll_mcMatchId != -1)) != 0)"%(deltaR, pdgId, etaAcc, deltaRcut, deltaR, pdgId, etaAcc)
#matchSel = "Sum$(LepAll_mcMatchId != 0 && LepAll_mcMatchId != -1) > 0"

#recoSel = "(abs(LepAll_pdgId) == 11 && abs(LepAll_eta) <" + str(etaAcc) + ")"
#lowPtSel = "(genLep_pt > 6 && genLep_pt < 10)" #Pt selection
#misMatchSel = "LepAll_mcMatchId == 0"

if lep == "mu": ID = "looseMuonId"
elif lep == "el": ID = "SPRING15_25ns_v1" # >= 1 = Veto ID

baseString = "(abs(LepAll_pdgId) == {} && LepAll_pt > 5 && abs(LepAll_eta) < {} && LepAll_{} >= 1 && LepAll_mcMatchId != 0)".format(pdgId, etaAcc, ID)#  && LepAll_mcMatchId != 0

dzCut = "abs(LepAll_dz) < 0.5"
dxyCut = "abs(LepAll_dxy) < 0.02"
hybIsoCut = "(LepAll_relIso03*min(LepAll_pt, 25)) < 5" 
#hybIsoCut = "((LepAll_absIso03 < 5) || (LepAll_relIso03 < 0.2))"
#hybIsoCut = "1"

if variable == "HI": selection = "Sum$(%s) > 0"%(combineCuts(baseString, hybIsoCut))
elif variable == "dxy": selection = "Sum$(%s) > 0"%(combineCuts(baseString, dxyCut))
elif variable == "dz": selection = "Sum$(%s) > 0"%(combineCuts(baseString, dzCut))
elif variable == "all": selection = "Sum$(%s) > 0"%(combineCutsList([baseString, hybIsoCut, dxyCut, dzCut]))

baseSel = "Sum$(%s) > 0"%(baseString)

print baseSel
print selection

baseSelList = [filters, preSel, baseSel] 
selList = [filters, preSel, selection] 

hists = {'FullSim':{'pt':{}, 'eta':{}, '2D':{}}, 'FastSim':{'pt':{}, 'eta':{}, '2D':{}}}
ratios = {'ID':{}, 'FullSim':{}, 'FastSim':{}}

bins = {'pt':[20, 0, 10], 'eta':[15, 0, 1.5]}

for sim in ['FullSim', 'FastSim']:

   if sim == 'FullSim': sample = 'ttInc'
   elif sim == 'FastSim': sample = 'ttInc_FS'

   #2D Histograms (wrt. pT)
   hists[sim]['2D']['den'] = make2DHist(samples[sample].tree, var1, var2, "weight*(" + combineCutsList(baseSelList) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2], bins['eta'][0], bins['eta'][1], bins['eta'][2])
   hists[sim]['2D']['den'].SetName("%s_2D_den"%(sim))
   #hists[sim]['2D']['den'].SetTitle("%s p_{T} vs |#eta| Distribution in %s TTJets Sample"%(lepton, sim))
   hists[sim]['2D']['den'].GetXaxis().SetTitle("%s p_{T}"%lepton)
   hists[sim]['2D']['den'].GetYaxis().SetTitle("%s |#eta|"%lepton)
   #hist.GetZaxis().SetRangeUser(0, 4)
   #alignStats(hist)
   
   #2D Histograms (wrt. pT)
   hists[sim]['2D']['num'] = make2DHist(samples[sample].tree, var1, var2, "weight*(" + combineCutsList(selList) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2], bins['eta'][0], bins['eta'][1], bins['eta'][2])
   hists[sim]['2D']['num'].SetName("%s_2D_num"%(sim))
   #hists[sim]['2D']['num'].SetTitle("%s p_{T} vs |#eta| Distribution in %s TTJets Sample"%(lepton, sim))
   hists[sim]['2D']['num'].GetXaxis().SetTitle("%s p_{T}"%lepton)
   hists[sim]['2D']['num'].GetYaxis().SetTitle("%s |#eta|"%lepton)
   
   ratios[sim]['2D'] = divideHists(hists[sim]['2D']['num'], hists[sim]['2D']['den'])
   ratios[sim]['2D'].SetName("%s_ratios_2D"%(sim))
   ratios[sim]['2D'].SetTitle("%s Efficiency for %s TTJets Sample"%(variable, sim))
   #ratios[sim]['2D'].GetXaxis().SetTitle("%s p_{T}"%lepton)
   #ratios[sim]['2D'].GetYaxis().SetTitle("%s |#eta|"%lepton)
   ratios[sim]['2D'].SetMarkerSize(0.8)
   #ratios[sim]['2D'].SetMinimum(0)
   #ratios[sim]['2D'].SetMaximum(5)
   ratios[sim]['2D'].GetZaxis().SetRangeUser(0,5)
   
   c4 = ROOT.TCanvas("c4", "Canvas 4", 1800, 1500)
   ratios[sim]['2D'].Draw("COLZ TEXT89") #CONT1-5 #plots the graph with axes and points
   
   alignStats(ratios[sim]['2D'])
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
      c3.SaveAs("%s/2D_distributions_%s%s.png"%(savedir, sim, suffix))
      c3.SaveAs("%s/pdf/2D_distributions_%s%s.pdf"%(savedir, sim, suffix))
      c3.SaveAs("%s/root/2D_distributions_%s%s.root"%(savedir, sim, suffix))
      
      c4.SaveAs("%s/2D_eff_%s%s.png"%(savedir, sim, suffix))
      c4.SaveAs("%s/pdf/2D_eff_%s%s.pdf"%(savedir, sim, suffix))
      c4.SaveAs("%s/root/2D_eff_%s%s.root"%(savedir, sim, suffix))
