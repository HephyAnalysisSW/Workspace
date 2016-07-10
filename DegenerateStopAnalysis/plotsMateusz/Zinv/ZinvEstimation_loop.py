# ZinvEstimation_loop.py
import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.navidTools.NavidTools import Plots, getPlots, drawPlots, setup_style
#from Workspace.DegenerateStopAnalysis.toolsMateusz.degTools import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.cutsEle import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.cmgTuplesPostProcessed_mAODv2_analysisHephy13TeV import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_mAODv2_analysisHephy13TeV import getSamples

from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Sets TDR style
setup_style()
ROOT.gStyle.SetOptStat(0) #1111 #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--CT", dest = "CT",  help = "CT Cut", type = str, default = "200")
#parser.add_argument("--MET", dest = "MET",  help = "MET Cut", type = str, default = "200")
#parser.add_argument("--HT", dest = "HT",  help = "HT Cut", type = str, default = "200")
parser.add_argument("--getData", dest = "getData",  help = "Get data samples", type = int, default = 1)
parser.add_argument("--plot", dest = "plot",  help = "Toggle plot", type = int, default = 1)
parser.add_argument("--logy", dest = "logy",  help = "Toggle logy", type = int, default = 1)
parser.add_argument("--save", dest = "save",  help = "Toggle save", type = int, default = 1)
parser.add_argument("-b", dest = "batch",  help = "Batch mode", action = "store_true", default = False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
CTcut = args.CT
#METcut = args.MET
#HTcut = args.HT
getData = args.getData
plot = args.plot
logy = args.logy
save = args.save

print makeDoubleLine()
print "Performing Zinv estimation."
print makeDoubleLine()

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/Zinv"
   if getData: savedir += "/data"
   if not os.path.exists(savedir): os.makedirs(savedir)

suffix = "_loop"

#Samples
cmgPP = cmgTuplesPostProcessed()#mc_path, signal_path, data_path)

samplesList = ["qcd", "w", "tt", "z", "dy"]

if getData: samplesList.append("dblind")
samples = getSamples(cmgPP = cmgPP, skim = 'presel', sampleList = samplesList, scan = False, useHT = True, getData = getData)
selectedSamples = samplesList #["qcd", "z", "tt", "w"]
selectedSamples.remove("dy") 
#selectedSamples.append("dy5")
selectedSamples.append("dy50")

##for s in samples.massScanList(): samples[s].weight = "weight" #removes ISR reweighting from official mass scan signal samples
#for s in samples: samples[s].tree.SetAlias("eleSel", allCuts[WP]['eleSel'])

print makeLine()
print "Using samples:"
newLine()
for s in selectedSamples:
   if s: print samples[s].name,":",s
   else:
      print "!!! Sample " + sample + " unavailable."
      sys.exit(0)

collection = "LepAll"
print makeLine()
print "Using " + collection + " collection."
print makeLine()

#Selecting only used branches
#for s in selectedSamples: 
#   samples[s].tree.SetBranchStatus("*", 0)
#   for branch in samples[s].tree.GetListOfBranches():
#      if branch.GetName() in ["met_pt", "nLepAll_mu", "nLepAll_el", "LepAll_pdgId", "LepAll_pt", "LepAll_eta", "LepAll_phi", "LepAll_relIso03", "IndexLepAll_mu", "IndexLepAll_el", "nIsrJet", "nBSoftJet", "nBHardJet", "nVetoJet", "ht_bas
#         samples[s].tree.SetBranchStatus(branch.GetName(), 1)

#Geometric cuts
etaAcc = 2.1
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap

hybIsoCut = lambda ind: "(LepAll_relIso03[" + ind + "]*min(LepAll_pt[" + ind + "], 25)) < 5" #hybIsoCut = "((LepAll_absIso03 < 5) || LepAll_relIso03 < 0.2))"

#variables = {'elePt':"LepAll_pt[" + ind + "]", 'eleMt':"LepAll_mt[" + ind + "]"}

#Index of leading electron
ind1 = "IndexLepAll_mu[0]"
ind2 = "IndexLepAll_mu[1]"

#Preselection & basic SR cuts
presel = CutClass("presel_SR", [
   ["CT","min(met, ht_basJet - 100) > 75"],
   #["MET","met >" + METcut],
   #["HT","ht_basJet >" + HTcut],
   #["ISR110", "nIsrJet >= 1"],
   #["anti-QCD", "vetoJet_dPhi_j1j2 < 2.5"],
   #["No3rdJet60","nVetoJet <= 2"],
   #["BVeto","(nBSoftJet == 0 && nBHardJet == 0)"],
   ], baseCut = None)

muSel = {}

muSel['mu'] = CutClass("muSel", [
   ["2mu", "nLepAll_mu >= 2"],
   ], baseCut = presel)

muSel['mu1'] = CutClass("muSel1", [
   ["muon", "abs(LepAll_pdgId[" + ind1 + "]) == 13"],
   ["relIso", "LepAll_relIso03[" + ind1 + "] < 0.12"],
   ["pt25", "LepAll_pt[" + ind1 + "] > 25"],
   #["hybIso", hybIsoCut(ind1)],
   ], baseCut = muSel['mu'])

muSel['mu2'] = CutClass("muSel2", [
   ["muon", "abs(LepAll_pdgId[" + ind2 + "]) == 13"],
   ["relIso", "LepAll_relIso03[" + ind2 + "] < 0.12"],
   ["pt25", "LepAll_pt[" + ind2 + "] > 20"],
   #["hybIso", hybIsoCut(ind1)],
   ], baseCut = muSel['mu'])

allCuts = CutClass("all", [] , baseCut = presel)
allCuts.add(muSel['mu'])#, baseCutString = sr1[iWP].inclCombined)
allCuts.add(muSel['mu1'])#, baseCutString = sr1[iWP].inclCombined)
allCuts.add(muSel['mu2'])#, baseCutString = sr1[iWP].inclCombined)

#for s in samples:
#   samples[s].tree.SetAlias("dimuon_mass", dimuon_mass)

#Empty histograms
hist = emptyHist("Di-muon System Invariant Mass Plot", 50, 0, 250)
print "Cut string: ", allCuts.combined
samples.dy50.tree.Draw(">>eList", allCuts.combined)
elist = ROOT.gDirectory.Get("eList")
nEvents = elist.GetN()

#Event Loop
for i in range(nEvents):
   #if i == 1000: break
   
   samples.dy50.tree.GetEntry(elist.GetEntry(i))
   
   dimuon = ROOT.TLorentzVector()
   muon1 = ROOT.TLorentzVector()
   muon2 = ROOT.TLorentzVector()
   muon_mass = 0.1057

   #Index of leading electron
   ind1 = int(samples.dy50.tree.GetLeaf("IndexLepAll_mu").GetValue(0))
   ind2 = int(samples.dy50.tree.GetLeaf("IndexLepAll_mu").GetValue(1))
   #print "index: ", ind1, " ", ind2
   muon1_pt = samples.dy50.tree.GetLeaf("LepAll_pt").GetValue(ind1)
   muon1_eta = samples.dy50.tree.GetLeaf("LepAll_eta").GetValue(ind1)
   muon1_phi = samples.dy50.tree.GetLeaf("LepAll_phi").GetValue(ind1)
   #muon1_mass = samples.dy50.tree.GetLeaf("LepAll_mass").GetValue(ind1)
   
   muon2_pt = samples.dy50.tree.GetLeaf("LepAll_pt").GetValue(ind2)
   muon2_eta = samples.dy50.tree.GetLeaf("LepAll_eta").GetValue(ind2)
   muon2_phi = samples.dy50.tree.GetLeaf("LepAll_phi").GetValue(ind2)
   #muon2_mass = samples.dy50.tree.GetLeaf("LepAll_mass").GetValue(ind2)
    
   muon1.SetPtEtaPhiM(muon1_pt, muon1_eta, muon1_phi, muon_mass)
   muon2.SetPtEtaPhiM(muon2_pt, muon2_eta, muon2_phi, muon_mass)
   
   dimuon += muon1 
   dimuon += muon2 
   dimuon_mass = dimuon.M()
   
   #Histogram filling   
   
   #HT
   hist.Fill(dimuon_mass)

c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)

hist.SetName("dimuon")
hist.SetTitle("Di-muon System Invariant Mass Plot")
hist.GetXaxis().SetTitle("m_{#mu#mu}")
hist.Draw()

if logy: ROOT.gPad.SetLogy()
ROOT.gPad.Modified()
ROOT.gPad.Update()

#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   if not os.path.exists("%s/root"%(savedir)): os.makedirs("%s/root"%(savedir))
   if not os.path.exists("%s/pdf"%(savedir)): os.makedirs("%s/pdf"%(savedir))

   c1.SaveAs("%s/dimuon_mass%s.png"%(savedir, suffix))
   c1.SaveAs("%s/root/dimuon_mass%s.root"%(savedir, suffix))
   c1.SaveAs("%s/pdf/dimuon_mass%s.pdf"%(savedir, suffix))
