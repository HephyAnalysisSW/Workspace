# ZinvEstimation_MuMu_loop.py
# Zinv estimation using the Z->mumu channel, using an event loop 
# Mateusz Zarucki 2016

import ROOT
import os, sys
import argparse
import pickle
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, makeDir, setup_style
from Workspace.DegenerateStopAnalysis.tools.bTagWeights import bTagWeights
from Workspace.DegenerateStopAnalysis.tools.getSamples_8012 import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Sets TDR style
setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--SR", dest = "SR",  help = "SR", type = str, default = "SR1") # 'SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1', 'SRH1', 'SRV1', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c'
parser.add_argument("--CT2", dest = "CT2",  help = "CT2 Cut", type = str, default = "75")
#parser.add_argument("--MET", dest = "MET",  help = "MET Cut", type = str, default = "200")
#parser.add_argument("--HT", dest = "HT",  help = "HT Cut", type = str, default = "200")
parser.add_argument("--beforeEmul", dest = "beforeEmul",  help = "beforeEmul plot", type = int, default = 0)
parser.add_argument("--afterEmul", dest = "afterEmul",  help = "afterEmul plot", type = int, default = 1)
parser.add_argument("--leptons", dest = "leptons",  help = "Extra lepton distributions", type = int, default = 1)
parser.add_argument("--peak", dest = "peak",  help = "Z-peak selection", type = int, default = 0)
parser.add_argument("--doYields", dest = "doYields",  help = "Calulate yields", type = int, default = 1)
parser.add_argument("--btag", dest = "btag",  help = "B-tagging option", type = str, default = "sf")
parser.add_argument("--getData", dest = "getData",  help = "Get data samples", type = int, default = 0)
parser.add_argument("--plot", dest = "plot",  help = "Toggle plot", type = int, default = 0)
parser.add_argument("--logy", dest = "logy",  help = "Toggle logy", type = int, default = 1)
parser.add_argument("--save", dest = "save",  help = "Toggle save", type = int, default = 1)
parser.add_argument("--verbose", dest = "verbose",  help = "Verbosity switch", type = int, default = 0)
parser.add_argument("-b", dest = "batch",  help = "Batch mode", action = "store_true", default = False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
SR = args.SR
CT2cut = args.CT2
beforeEmul = args.beforeEmul
afterEmul = args.afterEmul
leptons = args.leptons
peak = args.peak
#METcut = args.MET
#HTcut = args.HT
doYields = args.doYields
btag = args.btag
getData = args.getData
plot = args.plot
logy = args.logy
save = args.save
verbose = args.verbose

print makeDoubleLine()
print "Performing Zinv estimation."
print makeDoubleLine()

#Samples
cmgPP = cmgTuplesPostProcessed()
samplesList = ["dy", "vv", "tt", "dy5to50", "dy"] #"qcd", "w", "z", "st" 
if getData: samplesList.append("d1muBlind")

samples = getSamples(cmgPP = cmgPP, skim = 'oneLep', sampleList = samplesList, scan = False, useHT = True, getData = getData) 

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
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/Zinv/loop"%tag
   
   ##savedir += "/bTagWeight_" + btag
   #
   #savedir += "/" + SR
   #
   #savedir1 = savedir + "/beforeEmul"
   #savedir2 = savedir + "/afterEmul/CT" + CT2cut
   #
   #suffix1 = "_" + SR
   #suffix2 = suffix1 + "_" + CT2cut
   suffix = ""
   
   if peak: 
      suffix += "_peak"
   #   savedir1 += "/peak"
   #   savedir2 += "/peak"

   #makeDir("%s/root"%(savedir1))
   #makeDir("%s/pdf"%(savedir1))
   #makeDir("%s/root"%(savedir2))
   #makeDir("%s/pdf"%(savedir2))
   makeDir("%s/root"%(savedir))
   makeDir("%s/pdf"%(savedir))

#Indicies of leading muons
ind1 = "IndexLepAll_mu[0]"
ind2 = "IndexLepAll_mu[1]"

#electron_mt_2 = "sqrt(2*met2*LepAll_pt[IndexLepAll_el[0]]*(1 - cos(met2_phi - LepAll_phi[IndexLepAll_el[0]])))"
#muon_mt_2 = "sqrt(2*met2*LepAll_pt[IndexLepAll_mu[2]]*(1 - cos(met2_phi - LepAll_phi[IndexLepAll_mu[2]])))"
#
#for s in samplesList: 
#   samples[s].tree.SetAlias("dimuon_mass", dimuon_mass)
#   samples[s].tree.SetAlias("dimuon_pt", dimuon_pt)
#   samples[s].tree.SetAlias("dimuon_phi", dimuon_phi)
#   samples[s].tree.SetAlias("met2", met2)
#   samples[s].tree.SetAlias("met2_phi", met2_phi)
#   samples[s].tree.SetAlias("electron_mt_2", electron_mt_2)
#   samples[s].tree.SetAlias("muon_mt_2", muon_mt_2)
#
##SRs
#def regions(lepton):
#   if lepton == "electron":
#      pdgId = "11"
#      ind = "IndexLepAll_el[0]"
#      mt_2 = "electron_mt_2"
#   elif lepton == "muon":
#      pdgId = "13"
#      ind = "IndexLepAll_mu[2]"
#      mt_2 = "muon_mt_2"
#   else:
#      assert False
#    
#   SRs = {\
#      #'SR1':["SR1","LepAll_pt[" + ind + "] < 30"],
#      'SR1a':["SR1a",   combineCuts(mt_2 + " < 60", "LepAll_pt[" + ind + "] < 30", "LepAll_pdgId[" + ind + "] == " + pdgId)],
#      'SR1b':["SR1b",   combineCuts(btw(mt_2, 60, 95), "LepAll_pt[" + ind + "] < 30", "LepAll_pdgId[" + ind + "] == " + pdgId)],
#      'SR1c':["SR1c",   combineCuts(mt_2 + " > 95", "LepAll_pt[" + ind + "] < 30")],
#      
#      'SRL1a':["SRL1a", combineCuts(mt_2 + " < 60", btw("LepAll_pt[" + ind + "]", 5, 12), "LepAll_pdgId[" + ind + "] == " + pdgId)],
#      'SRH1a':["SRH1a", combineCuts(mt_2 + " < 60", btw("LepAll_pt[" + ind + "]", 12, 20), "LepAll_pdgId[" + ind + "] == " + pdgId)],
#      'SRV1a':["SRV1a", combineCuts(mt_2 + " < 60", btw("LepAll_pt[" + ind + "]", 20, 30), "LepAll_pdgId[" + ind + "] == " + pdgId)],
#   
#      'SRL1b':["SRL1b", combineCuts(btw(mt_2, 60, 95), btw("LepAll_pt[" + ind + "]", 5, 12), "LepAll_pdgId[" + ind + "] == " + pdgId)],
#      'SRH1b':["SRH1b", combineCuts(btw(mt_2, 60, 95), btw("LepAll_pt[" + ind + "]", 12, 20), "LepAll_pdgId[" + ind + "] == " + pdgId)],
#      'SRV1b':["SRV1b", combineCuts(btw(mt_2, 60, 95), btw("LepAll_pt[" + ind + "]", 20, 30), "LepAll_pdgId[" + ind + "] == " + pdgId)],
#   
#      'SRL1c':["SRL1c", combineCuts(mt_2 + " > 95", btw("LepAll_pt[" + ind + "]", 5, 12))],
#      'SRH1c':["SRH1c", combineCuts(mt_2 + " > 95", btw("LepAll_pt[" + ind + "]", 12, 20))],
#      'SRV1c':["SRV1c", combineCuts(mt_2 + " > 95", btw("LepAll_pt[" + ind + "]", 20, 30))]}
#   
#   SRs['SR1'] =  ["SR1", "((" + SRs['SR1a'][1] + ") || (" + SRs['SR1b'][1] + ") || (" + SRs['SR1c'][1] + "))"]
#   SRs['SRL1'] = ["SRL1", combineCuts(SRs['SR1'][1], btw("LepAll_pt[" + ind + "]", 5, 12))]
#   SRs['SRH1'] = ["SRH1", combineCuts(SRs['SR1'][1], btw("LepAll_pt[" + ind + "]", 12, 20))]
#   SRs['SRV1'] = ["SRV1", combineCuts(SRs['SR1'][1], btw("LepAll_pt[" + ind + "]", 20, 30))]
#   
#   return SRs
#
#SRs_el = regions('electron')
#SRs_mu = regions('muon')

#btag weights
bWeightDict = bTagWeights(btag)
bTagString = bWeightDict['sr1_bjet']
#bTagString = "nBJet == 0" 

#Preselection & selection of Z->mumu events
dimuon = CutClass("dimuon", [
   ["ISR100", "nIsrJet >= 1"],
   ["TauVeto","Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
   ["BVeto", bTagString],
   ["No3rdJet60","nVetoJet <= 2"],
   ["2mu", "nLepAll_mu >= 2"], 
    
   ["muon1", "abs(LepAll_pdgId[" + ind1 + "]) == 13"], #redundant
   ["relIso", "LepAll_relIso03[" + ind1 + "] < 0.12"],
   ["pt28", "LepAll_pt[" + ind1 + "] > 28"],
    
   ["muon2", "abs(LepAll_pdgId[" + ind2 + "]) == 13"], #redundant
   ["relIso", "LepAll_relIso03[" + ind2 + "] < 0.12"],
   ["pt20", "LepAll_pt[" + ind2 + "] > 20"],
   
   ["OS", "LepAll_pdgId[" + ind1 + "] == -LepAll_pdgId[" + ind2 + "]"],
   ], baseCut = None)

#Selecting only used branches
#for s in selectedSamples: 
#   samples[s].tree.SetBranchStatus("*", 0)
#   for branch in samples[s].tree.GetListOfBranches():
#      if branch.GetName() in ["met_pt", "nLepAll_mu", "nLepAll_el", "LepAll_pdgId", "LepAll_pt", "LepAll_eta", "LepAll_phi", "LepAll_relIso03", "IndexLepAll_mu", "IndexLepAll_el", "nIsrJet", "nBSoftJet", "nBHardJet", "nVetoJet", "ht_bas
#         samples[s].tree.SetBranchStatus(branch.GetName(), 1)

#Empty histograms
hists = {}
for samp in samples:
   hists[samp] = { 
      'dimuon_mass':emptyHist("Di-muon System Invariant Mass Plot", 50, 5, 255),
      'dimuon_pt':emptyHist("Di-muon System pT Plot", 50, 0, 250),
      'MET':emptyHist("MET Plot", 50, 0, 500),
      'MET2':emptyHist("MET2 Plot", 50, 0, 500),
      'MET2_phi':emptyHist("MET2 Phi Plot", 20, -3.15, 3.15),
      'elePt':emptyHist("Ele pT Plot", 10, 5, 30),
      'muPt':emptyHist("Muon pT Plot", 10, 5, 30),
   }

#Sets event list 
setEventListToChains(samples, samplesList, dimuon)
#samples[samp].tree.Draw(">>eList", dimuon.combined)
#eList = ROOT.gDirectory.Get("eList")
eList = samples[samp].tree.GetEventList()
nListEntries = eList.GetN()
#nChainEntries = samples[samp].tree.GetEntries()

#print "Total entries: ", nChainEntries, " | eList entries: ", nListEntries 
   
canvs = {}
#colours = {'dy': 'ROOT.kMagenta+2', 'tt':'ROOT.kBlue-4', 'vv':'ROOT.kGreen+3'}

lumiWeight = (12864.4/10000.0)

#Event Loop
for samp in samples:

   #Selecting only used branches
   samples[samp].tree.SetBranchStatus("*", 0)
   
   usedBranches = ["met_" + x for x in ['pt','eta','phi']]
   usedBranches.extend(["LepAll_" + x for x in ['pt','eta','phi']])
   usedBranches.extend(['nLepAll_el', 'nLepAll_mu', 'IndexLepAll_el', 'IndexLepAll_mu'])
   usedBranches.extend(['weight', 'puReweight', 'weightBTag0_SF'])#, 'weightSBTag0_SF', 'weightSBTag1p_SF', 'weightHBTag0_SF', 'weightHBTag1p_SF', 'weightHBTag1_SF'])
   usedBranches.append('ht_basJet')
   
   for branch in samples[samp].tree.GetListOfBranches():
      if branch.GetName() in usedBranches:
         samples[samp].tree.SetBranchStatus(branch.GetName(), 1)

   for i in range(nListEntries):
      #print "eList index", i
      #if i == 50000: break
   
      samples[samp].tree.GetEntry(eList.GetEntry(i))
      #TTree:GetEntry(entry) = Read all branches of entry and return total number of bytes read. The function returns the number of bytes read from the input buffer. If entry does not exist the function returns 0. If an I/O error occurs, the function returns -1.
      #TEventList:GetEntry(index) = Return value of entry at index in the list. Return -1 if index is not in the list range. 
      #TEventList:GetIndex(entry) Return index in the list of element with value entry array is supposed to be sorted prior to this call. If match is found, function returns position of element.
   
      MET = ROOT.TLorentzVector()
      MET2 = ROOT.TLorentzVector()
      dimuonSys = ROOT.TLorentzVector()
      muon1 = ROOT.TLorentzVector()
      muon2 = ROOT.TLorentzVector()
      muon_mass = 0.1057 #rest mass
      
      #Weights 
      weight = samples[samp].tree.GetLeaf("weight").GetValue(0)
      puWeight = samples[samp].tree.GetLeaf("puReweight").GetValue(0)

      #btag weights
      weightBTag0_SF = samples[samp].tree.GetLeaf("weightBTag0_SF").GetValue(0)
      
      if btag == 'sf':
         bTagWeight = weightBTag0_SF
      else:
         bTagWeight = 1
      
      totalWeight = (weight*lumiWeight*puWeight*bTagWeight)
      
      HT = samples[samp].tree.GetLeaf("ht_basJet").GetValue(0)
      
      MET_pt = samples[samp].tree.GetLeaf("met_pt").GetValue(0)
      MET_eta = samples[samp].tree.GetLeaf("met_eta").GetValue(0)
      MET_phi = samples[samp].tree.GetLeaf("met_phi").GetValue(0)
      MET.SetPtEtaPhiM(MET_pt, MET_eta, MET_phi, 0)
     
      nEl = samples[samp].tree.GetLeaf("nLepAll_el").GetValue(0)
      nMu = samples[samp].tree.GetLeaf("nLepAll_mu").GetValue(0)
      
      #indicies
      #muons
      ind_mu1 = int(samples[samp].tree.GetLeaf("IndexLepAll_mu").GetValue(0)) #Z muon
      ind_mu2 = int(samples[samp].tree.GetLeaf("IndexLepAll_mu").GetValue(1)) #Z muon
      ind_mu3 = int(samples[samp].tree.GetLeaf("IndexLepAll_mu").GetValue(2))
      ind_mu4 = int(samples[samp].tree.GetLeaf("IndexLepAll_mu").GetValue(3))
      #electrons 
      ind_el1 = int(samples[samp].tree.GetLeaf("IndexLepAll_el").GetValue(0))
      ind_el2= int(samples[samp].tree.GetLeaf("IndexLepAll_el").GetValue(1))
   
      #dimuon system muons
      muon1_pt = samples[samp].tree.GetLeaf("LepAll_pt").GetValue(ind_mu1)
      muon1_eta = samples[samp].tree.GetLeaf("LepAll_eta").GetValue(ind_mu1)
      muon1_phi = samples[samp].tree.GetLeaf("LepAll_phi").GetValue(ind_mu1)
      #muon1_mass = samples[samp].tree.GetLeaf("LepAll_mass").GetValue(ind_mu1)
      muon1.SetPtEtaPhiM(muon1_pt, muon1_eta, muon1_phi, muon_mass)
   
      muon2_pt = samples[samp].tree.GetLeaf("LepAll_pt").GetValue(ind_mu2)
      muon2_eta = samples[samp].tree.GetLeaf("LepAll_eta").GetValue(ind_mu2)
      muon2_phi = samples[samp].tree.GetLeaf("LepAll_phi").GetValue(ind_mu2)
      #muon2_mass = samples[samp].tree.GetLeaf("LepAll_mass").GetValue(ind_mu2)
      muon2.SetPtEtaPhiM(muon2_pt, muon2_eta, muon2_phi, muon_mass)
     
      #extra soft leptons
      ele1_pt = samples[samp].tree.GetLeaf("LepAll_pt").GetValue(ind_el1)
      ele2_pt = samples[samp].tree.GetLeaf("LepAll_pt").GetValue(ind_el2)
      muon3_pt = samples[samp].tree.GetLeaf("LepAll_pt").GetValue(ind_mu3)
      muon4_pt = samples[samp].tree.GetLeaf("LepAll_pt").GetValue(ind_mu4)
   
      #determination of dimuon system
      dimuonSys += muon1
      dimuonSys += muon2
   
      if dimuonSys.M() < 55: continue
      #if dimuonSys.P() < 75: continue
   
      if peak:
         if abs(dimuonSys.M() - 91.1876) > 15: continue
   
      #adding dimuon system pt to MET   
      MET2 += MET
      MET2 += dimuonSys
   
      #print "MET", MET.P() 
      #print "Dimuon pT", dimuonSys.P() 
      #print "MET2", MET2.P()
      #print "HT", HT
        
      if MET2.P() < 75: continue
      if min(MET2.P(), HT - 100) < float(CT2cut): continue
    
      #Histogram filling 
      hists[samp]['dimuon_mass'].Fill(dimuonSys.M(), totalWeight)
      hists[samp]['dimuon_pt'].Fill(dimuonSys.P(), totalWeight)
      hists[samp]['MET'].Fill(MET.P(), totalWeight)
      hists[samp]['MET2'].Fill(MET2.P(), totalWeight)
      hists[samp]['MET2_phi'].Fill(MET2.Phi(), totalWeight)
   
      if ((nEl == 1 and ele1_pt < 30) or (nEl == 2 and ele1_pt < 30 and ele2_pt < 20)) and (nMu == 2 or (nMu == 3 and muon3_pt < 20)): hists[samp]['elePt'].Fill(ele1_pt, totalWeight) 
      if ((nMu == 3 and muon3_pt < 30) or (nMu == 4 and muon3_pt < 30 and muon4_pt < 20)) and (nEl == 0 or (nEl == 1 and ele1_pt < 20)): hists[samp]['muPt'].Fill(muon3_pt, totalWeight)

for hist in hists['dy']:
   canvs[hist] = ROOT.TCanvas("canv_" + hist , "Canvas " + hist, 1800, 1500)
   for samp in samples: 
      hists[samp][hist].SetName(hist)
      hists[samp][hist].SetTitle("Zinv Estimation (Z->#mu#mu) " +hist + " Plot")
      hists[samp][hist].GetXaxis().SetTitle(hist)
      hists[samp][hist].SetFillColor(samples[samp].color)
      hists[samp][hist].SetMaximum(100000)
      #hist.SetLineColor(ROOT.kBlack)
      #hist.SetLineWidth(3)
      
      if not samples[samp].isData: 
         hists[samp][hist].Draw('hist same')
      else: 
         hists[samp][hist].SetMarkerStyle(ROOT.kCircle)
         hists[samp][hist].Draw("P same")
      
      if logy: ROOT.gPad.SetLogy()
      ROOT.gPad.Modified()
      ROOT.gPad.Update()

#Save canvas
   if save: #web address: http://www.hephy.at/user/mzarucki/plots
      canvs[hist].SaveAs("%s/%s%s.png"%(savedir, hist, suffix))
      canvs[hist].SaveAs("%s/root/%s%s.root"%(savedir, hist, suffix))
      canvs[hist].SaveAs("%s/pdf/%s%s.pdf"%(savedir, hist, suffix))
