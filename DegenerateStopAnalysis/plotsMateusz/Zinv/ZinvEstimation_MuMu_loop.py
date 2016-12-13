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
from Workspace.HEPHYPythonTools import u_float
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
parser.add_argument("--lepEta", dest = "lepEta",  help = "Extra soft lepton eta", type = float, default = 2.5)
parser.add_argument("--beforeEmul", dest = "beforeEmul",  help = "beforeEmul plot", type = int, default = 0)
parser.add_argument("--afterEmul", dest = "afterEmul",  help = "afterEmul plot", type = int, default = 1)
parser.add_argument("--leptons", dest = "leptons",  help = "Extra lepton distributions", type = int, default = 1)
parser.add_argument("--peak", dest = "peak",  help = "Z-peak selection", type = int, default = 0)
parser.add_argument("--doYields", dest = "doYields",  help = "Calulate yields", type = int, default = 1)
parser.add_argument("--btag", dest = "btag",  help = "B-tagging option", type = str, default = "sf")
parser.add_argument("--getData", dest = "getData",  help = "Get data samples", type = int, default = 1)
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
lepEta = args.lepEta
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
samplesList = ["vv", "tt", "dy5to50", "dy"]#"qcd", "w", "z", "st" 
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
   savedir1 = savedir + "/afterEmul/CT" + CT2cut
   savedir2 = savedir + "/leptons/CT" + CT2cut
   #
   #suffix1 = "_" + SR
   #suffix2 = suffix1 + "_" + CT2cut
   suffix = ""
   
   if peak: 
      suffix += "_peak"
      savedir1 += "/peak"
      savedir2 += "/peak"

   makeDir("%s/root"%(savedir1))
   makeDir("%s/pdf"%(savedir1))
   makeDir("%s/root"%(savedir2))
   makeDir("%s/pdf"%(savedir2))

#Indicies of leading muons
ind1 = "IndexLepAll_mu[0]"
ind2 = "IndexLepAll_mu[1]"

#btag weights
bWeightDict = bTagWeights(btag)
bTagString = bWeightDict['sr1_bjet']
#bTagString = "nBJet == 0" 

#Preselection & selection of Z->mumu events
dimuon = CutClass("dilepton", [
   ["ISR100", "nIsrJet >= 1"],
   ["TauVeto","Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
   ["BVeto", bTagString],
   ["No3rdJet60","nVetoJet <= 2"],
   ["2mu", "nLepAll_mu >= 2"], 
    
   #["muon1", "abs(LepAll_pdgId[" + ind1 + "]) == 13"], #redundant
   ["relIso", "LepAll_relIso03[" + ind1 + "] < 0.12"],
   ["pt26", "LepAll_pt[" + ind1 + "] > 26"],
    
   #["muon2", "abs(LepAll_pdgId[" + ind2 + "]) == 13"], #redundant
   ["relIso", "LepAll_relIso03[" + ind2 + "] < 0.12"],
   ["pt20", "LepAll_pt[" + ind2 + "] > 20"],
   
   ["OS", "LepAll_pdgId[" + ind1 + "] == -LepAll_pdgId[" + ind2 + "]"],
   ], baseCut = None)


#Empty histograms
hists = {}

for samp in samples:
   hists[samp] = { 
      'dimuon_mass':emptyHist("Di-muon System Invariant Mass Plot", 50, 5, 255),
      'dimuon_pt':emptyHist("Di-muon System pT Plot", 50, 0, 250),
      'dimuon_phi':emptyHist("Di-muon System phi Plot", 20, -3.15, 3.15),
      'MET':emptyHist("MET Plot", 50, 0, 500),
      'MET_phi':emptyHist("MET Phi Plot", 20, -3.15, 3.15),
      'MET_emul':emptyHist("MET_emul Plot", 50, 0, 500),
      'MET_emul_phi':emptyHist("MET_emul Phi Plot", 20, -3.15, 3.15),

      'elePt':emptyHist("Ele pT Plot", 10, 5, 30),
      'muPt':emptyHist("Muon pT Plot", 10, 5, 30),
      'eleMt':emptyHist("Ele mT Plot", 50, 0, 150),
      'muMt':emptyHist("Muon mT Plot", 50, 0, 150),
      'elePt_counts':emptyHist("Electron counts", 5, 2.5, 7.5),
      'muPt_counts':emptyHist("Muon counts", 5, 2.5, 7.5),
      'Zpeak_counts':emptyHist("Zpeak counts", 5, 2.5, 7.5),
   }

#Sets event list 
setEventListToChains(samples, samplesList, dimuon)
   
#colours = {'dy': 'ROOT.kMagenta+2', 'tt':'ROOT.kBlue-4', 'vv':'ROOT.kGreen+3'}

lepEta = 2.5

#Event Loop
for samp in samples:
   
   setEventListToChains(samples, [samp], dimuon)
   #samples[samp].tree.Draw(">>eList", dimuon.combined)
   #eList = ROOT.gDirectory.Get("eList")
   eList = samples[samp].tree.GetEventList()
   nListEntries = eList.GetN()
   #nChainEntries = samples[samp].tree.GetEntries()
   
   #print "Total entries: ", nChainEntries, " | eList entries: ", nListEntries 
   
   #Selecting only used branches
   samples[samp].tree.SetBranchStatus("*", 0)
   
   usedBranches = ["met_" + x for x in ['pt','eta','phi']]
   usedBranches.extend(["LepAll_" + x for x in ['pdgId','pt','eta','phi']])
   usedBranches.extend(['nLepAll_el', 'nLepAll_mu', 'IndexLepAll_el', 'IndexLepAll_mu'])
   usedBranches.extend(['weight', 'puReweight', 'weightBTag0_SF'])#, 'weightSBTag0_SF', 'weightSBTag1p_SF', 'weightHBTag0_SF', 'weightHBTag1p_SF', 'weightHBTag1_SF'])
   usedBranches.append('ht_basJet')
   
   for branch in samples[samp].tree.GetListOfBranches():
      if branch.GetName() in usedBranches:
         samples[samp].tree.SetBranchStatus(branch.GetName(), 1)

   for i in range(nListEntries):
      #print "eList index", i
      #if i == 500: break
   
      samples[samp].tree.GetEntry(eList.GetEntry(i))
      #TTree:GetEntry(entry) = Read all branches of entry and return total number of bytes read. The function returns the number of bytes read from the input buffer. If entry does not exist the function returns 0. If an I/O error occurs, the function returns -1.
      #TEventList:GetEntry(index) = Return value of entry at index in the list. Return -1 if index is not in the list range. 
      #TEventList:GetIndex(entry) Return index in the list of element with value entry array is supposed to be sorted prior to this call. If match is found, function returns position of element.
   
      MET = ROOT.TLorentzVector()
      MET_emul = ROOT.TLorentzVector()
      dimuonSys = ROOT.TLorentzVector()
      muon1 = ROOT.TLorentzVector()
      muon2 = ROOT.TLorentzVector()
      muon_mass = 0.1057 #rest mass
      
      #Weights 
      if not samples[samp].isData:
         lumiWeight = (12864.4/10000.0)
         weight = samples[samp].tree.GetLeaf("weight").GetValue(0)
         puWeight = samples[samp].tree.GetLeaf("puReweight").GetValue(0)
         #btag weights
         if btag == 'sf' and not samples[samp].isData:
            weightBTag0_SF = samples[samp].tree.GetLeaf("weightBTag0_SF").GetValue(0)
            bTagWeight = weightBTag0_SF
         else:
            bTagWeight = 1
         
         #totalWeight = (weight*lumiWeight*puWeight*bTagWeight)
         totalWeight = (weight*lumiWeight*puWeight*bTagWeight)
         #print "sample:weight:lumi:pu:btag", samp, weight, lumiWeight, puWeight, bTagWeight
      else: #data
         totalWeight = 1 
     
      #if samples[samp].isData: 
      #   nBJets = samples[samp].tree.GetLeaf("nBJet").GetValue(0)
      #   if nBJets != 0: continue
      #nBJets = samples[samp].tree.GetLeaf("nBJet").GetValue(0)
      #if nBJets != 0: continue
      
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
      
      #determination of dimuon system
      dimuonSys += muon1
      dimuonSys += muon2
   
      #adding dimuon system pt to MET   
      MET_emul += MET
      MET_emul += dimuonSys
   
      #print "MET", MET.P() 
      #print "Dimuon pT", dimuonSys.P() 
      #print "MET_emul", MET_emul.P()
      #print "HT", HT
      
      if dimuonSys.M() < 55: continue
   
      if MET_emul.Pt() < 75: continue #instead of cut on dilepton pt
      #if dimuonSys.Pt() < 75: continue
      if min(MET_emul.Pt(), HT - 100) < float(CT2cut): continue
      
      if peak:
         if abs(dimuonSys.M() - 91.1876) > 15: continue
     
      #Histogram filling 
      hists[samp]['dimuon_mass'].Fill(dimuonSys.M(), totalWeight)
      hists[samp]['dimuon_pt'].Fill(dimuonSys.Pt(), totalWeight)
      hists[samp]['dimuon_phi'].Fill(dimuonSys.Phi(), totalWeight)
      hists[samp]['MET'].Fill(MET.Pt(), totalWeight)
      hists[samp]['MET_phi'].Fill(MET.Phi(), totalWeight)
      hists[samp]['MET_emul'].Fill(MET_emul.Pt(), totalWeight)
      hists[samp]['MET_emul_phi'].Fill(MET_emul.Phi(), totalWeight)
      hists[samp]['Zpeak_counts'].Fill(5, totalWeight)
  
      #extra soft leptons
      if nEl == 1 or nEl == 2:
         ele1_pt = samples[samp].tree.GetLeaf("LepAll_pt").GetValue(ind_el1)
         ele1_eta = samples[samp].tree.GetLeaf("LepAll_eta").GetValue(ind_el1)
         ele1_phi = samples[samp].tree.GetLeaf("LepAll_phi").GetValue(ind_el1)
         ele1_pdgId = samples[samp].tree.GetLeaf("LepAll_pdgId").GetValue(ind_el1)
      
         ele1_mt_emul = math.sqrt(2*MET_emul.Pt()*ele1_pt*(1-math.cos(MET_emul.Phi() - ele1_phi)))
         
         if nEl == 2:
            ele2_pt = samples[samp].tree.GetLeaf("LepAll_pt").GetValue(ind_el2)
      
      if nMu == 3 or nMu == 4:
         muon3_pt = samples[samp].tree.GetLeaf("LepAll_pt").GetValue(ind_mu3)
         muon3_eta = samples[samp].tree.GetLeaf("LepAll_eta").GetValue(ind_mu3)
         muon3_phi = samples[samp].tree.GetLeaf("LepAll_phi").GetValue(ind_mu3)
         muon3_pdgId = samples[samp].tree.GetLeaf("LepAll_pdgId").GetValue(ind_mu3)
         
         muon3_mt_emul = math.sqrt(2*MET_emul.Pt()*muon3_pt*(1-math.cos(MET_emul.Phi() - muon3_phi)))
        
         if nMu == 4: 
            muon4_pt = samples[samp].tree.GetLeaf("LepAll_pt").GetValue(ind_mu4)
 
      if ((nEl == 1 and ele1_pt < 30) or (nEl == 2 and ele1_pt < 30 and ele2_pt < 20)) and (nMu == 2 or (nMu == 3 and muon3_pt < 20)) and abs(ele1_eta) < lepEta:
         if (ele1_mt_emul < 60 and ele1_pdgId == 11) or (60 < ele1_mt_emul < 95 and ele1_pdgId == 11) or (ele1_mt_emul > 95):
            hists[samp]['elePt'].Fill(ele1_pt, totalWeight) 
            hists[samp]['eleMt'].Fill(ele1_mt_emul, totalWeight) 
            
            hists[samp]['elePt_counts'].Fill(5, totalWeight)
     
            #print "elePdgId = ", ele1_pdgId
            #print "eleMt = ", ele1_mt_emul
 
      if ((nMu == 3 and muon3_pt < 30) or (nMu == 4 and muon3_pt < 30 and muon4_pt < 20)) and (nEl == 0 or (nEl == 1 and ele1_pt < 20)) and abs(muon3_eta) < lepEta: 
         if (muon3_mt_emul < 60 and muon3_pdgId == 13) or (60 < muon3_mt_emul < 95 and muon3_pdgId == 13) or (muon3_mt_emul > 95):
            hists[samp]['muPt'].Fill(muon3_pt, totalWeight)
            hists[samp]['muMt'].Fill(muon3_mt_emul, totalWeight) 

            #print "muPdgId = ", muon3_pdgId
            #print "muMt = ", muon3_mt_emul

            hists[samp]['muPt_counts'].Fill(5, totalWeight)

canvs = {}
stacks = {}

for hist in hists['dy']:
   canvs[hist] = ROOT.TCanvas("canv_" + hist , "Canvas " + hist, 1800, 1500)
   stacks[hist] = ROOT.THStack("stack_" + hist , "")

   #leg = makeLegend2()
   
   for samp in samplesList: 
      hists[samp][hist].SetName(samp)
      hists[samp][hist].SetTitle("Zinv Estimation (Z->#mu#mu) " + hist + " Plot")
      hists[samp][hist].GetXaxis().SetTitle(hist)
      hists[samp][hist].SetFillColor(samples[samp].color)
      #hist.SetLineColor(ROOT.kBlack)
      #hist.SetLineWidth(3)
       
      if not samples[samp].isData: 
         #print "Adding ", samp, " to stack"
         stacks[hist].Add(hists[samp][hist])
         #hists[samp][hist].Draw('hist same')
   
      #leg.AddEntry(samp, samp, "F")
    
   if hist not in ["elePt", "muPt", "eleMt", "muMt", "elePt_counts", "muPt_counts"]:
      stacks[hist].SetMinimum(0.1)
      stacks[hist].SetMaximum(10000)
      if logy: ROOT.gPad.SetLogy()
      ROOT.gPad.Modified()
      ROOT.gPad.Update()
   
   stacks[hist].Draw('hist')
   hists['d1muBlind'][hist].SetMarkerSize(0.9)
   hists['d1muBlind'][hist].SetMarkerStyle(20)
   hists['d1muBlind'][hist].Draw("E0Psame")
   #hists['d1muBlind'][hist].Draw("Psame")

   #Save canvas
   if save: #web address: http://www.hephy.at/user/mzarucki/plots
      if hist in ["elePt", "muPt", "eleMt", "muMt", "elePt_counts", "muPt_counts"]:
         dir = savedir2
      else:
         dir = savedir1

      canvs[hist].SaveAs("%s/%s%s.png"%(dir, hist, suffix))
      canvs[hist].SaveAs("%s/root/%s%s.root"%(dir, hist, suffix))
      canvs[hist].SaveAs("%s/pdf/%s%s.pdf"%(dir, hist, suffix))

if doYields and peak:
   ZinvYields = {'Zpeak':{}, 'Nel':{}, 'Nmu':{}}
   #Yields
   for samp in samples:
      ZinvYields['Zpeak'][samp] = u_float.u_float(hists[samp]['Zpeak_counts'].GetBinContent(hists[samp]['Zpeak_counts'].FindBin(5)), hists[samp]['Zpeak_counts'].GetBinError(hists[samp]['Zpeak_counts'].FindBin(5)))
      ZinvYields['Nel'][samp] = u_float.u_float(hists[samp]['elePt_counts'].GetBinContent(hists[samp]['elePt_counts'].FindBin(5)), hists[samp]['elePt_counts'].GetBinError(hists[samp]['elePt_counts'].FindBin(5)))
      ZinvYields['Nmu'][samp] = u_float.u_float(hists[samp]['muPt_counts'].GetBinContent(hists[samp]['muPt_counts'].FindBin(5)), hists[samp]['muPt_counts'].GetBinError(hists[samp]['muPt_counts'].FindBin(5)))
    
   if not os.path.isfile("%s/ZinvYields%s.txt"%(savedir1, suffix)):
      outfile = open("%s/ZinvYields%s.txt"%(savedir1, suffix), "w")
      outfile.write("Zinv Estimation Yields\n")
      outfile.write("CT       Zpeak_data          Zpeak_DY           Zpeak_TT           Zpeak_VV           Nel_data           Nel_DY           Nel_TT           Nel_VV           Nmu_data           Nmu_DY            Nmu_TT          Nmu_VV\n")
   
   with open("%s/ZinvYields%s.txt"%(savedir1, suffix), "a") as outfile:
      outfile.write(CT2cut.ljust(7) +\
      str(ZinvYields['Zpeak']['d1muBlind'].round(2)).ljust(18) +\
      str((ZinvYields['Zpeak']['dy'] + ZinvYields['Zpeak']['dy5to50']).round(2)).ljust(18) +\
      str(ZinvYields['Zpeak']['tt'].round(2)).ljust(18) +\
      str(ZinvYields['Zpeak']['vv'].round(2)).ljust(18) +\
      str(ZinvYields['Nel']['d1muBlind'].round(2)).ljust(18) +\
      str((ZinvYields['Nel']['dy'] + ZinvYields['Nel']['dy5to50']).round(2)).ljust(18) +\
      str(ZinvYields['Nel']['tt'].round(2)).ljust(18) +\
      str(ZinvYields['Nel']['vv'].round(2)).ljust(18) +\
      str(ZinvYields['Nmu']['d1muBlind'].round(2)).ljust(18) +\
      str((ZinvYields['Nmu']['dy'] + ZinvYields['Nmu']['dy5to50']).round(2)).ljust(18) +\
      str(ZinvYields['Nmu']['tt'].round(2)).ljust(18) +\
      str(ZinvYields['Nmu']['vv'].round(2)) + "\n")
   
   #Pickle results 
   pickleFile1 = open("%s/ZinvYields%s.pkl"%(savedir1,suffix), "w")
   pickle.dump(ZinvYields, pickleFile1)
   pickleFile1.close()
