# Wpol.py
# Script for calculating the effect of W-polarization variation in each SR and CR. Uses event loop. 
# Mateusz Zarucki 2016

import ROOT
import os, sys
import math
import argparse
import pickle
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, makeSimpleLatexTable, makeDir, setup_style
from Workspace.DegenerateStopAnalysis.tools.degCuts import Cuts
from Workspace.DegenerateStopAnalysis.cmgPostProcessing import cmgObjectSelection
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_Summer16 import cmgTuplesPostProcessed
from Workspace.HEPHYPythonTools import u_float
#from Workspace.DegenerateStopAnalysis.tools.degPlots import DegPlots
#from Workspace.DegenerateStopAnalysis.tools.bTagWeights import bTagWeights
from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Sets TDR style
setup_style()

base_path = "/afs/hephy.at/data/mzarucki01/cmgTuples/postProcessed_mAODv2/8025_mAODv2_v7/80X_postProcessing_v0/analysisHephy_13TeV_2016_v2_4/step1"
mc_path = base_path + "/RunIISummer16MiniAODv2_v7"
data_path = base_path + "/Data2016_v7"

cmgPP = cmgTuplesPostProcessed(mc_path = mc_path, data_path = data_path, signal_path = mc_path)

samples = getSamples(cmgPP = cmgPP, skim = 'HT300_ISR100', sampleList = ['w'], scan = False, useHT = True, getData = False)
#samples = getSamples(cmgPP = cmgPP, skim = 'HT300_ISR100_filter', sampleList = ['w'], scan = False, useHT = True, getData = False)

sys.exit()

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/Wpol/13TeV_fractions"%tag
   savedir += "/" + variation
    
   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

#f = ROOT.TFile("Wpol_fractions_8TeV.root")
#
#WpolFractions = {}
#
#WpolFractions['h_W_plus_fl'] = f.Get("h_W_plus_fl")
#WpolFractions['h_W_plus_fr'] = f.Get("h_W_plus_fr")
#WpolFractions['h_W_plus_f0'] = f.Get("h_W_plus_f0")
#
#WpolFractions['h_W_minus_fl'] = f.Get("h_W_minus_fl")
#WpolFractions['h_W_minus_fr'] = f.Get("h_W_minus_fr")
#WpolFractions['h_W_minus_f0'] = f.Get("h_W_minus_f0")

#binX = h.GetXaxis().FindBin(pt)
#binY = h.GetYaxis().FindBin(abs(eta))
#
#if binX < h.GetXaxis().GetFirst():
#   print "pt out of SF range. Using first bin value"
#   binX = h.GetXaxis().GetFirst()
#if binX > h.GetXaxis().GetLast():
#   print "pt out of SF range. Using last bin value"
#   binX = h.GetXaxis().GetLast()
#
#
#if binY > h.GetYaxis().GetLast():
#   print "eta out of SF range. Using last bin value"
#   binY = h.GetYaxis().GetLast()
#
##bin = h.FindBin(pt,abs(eta)) #NOTE: not modified to take last bin value
#bin = h.GetBin(binX, binY)
#
#print "x-bin #:", binX, "y-bin #:", binY,"Global bin #", bin
#
#if binY < h.GetYaxis().GetFirst():
#   print "ybin < first. Something is wrong. Exiting"
#   sys.exit(0)
#
#SF = h.GetBinContent(bin)

#Preselection

#bTagWeights
#bWeightDict = bTagWeights(btag)
#bTagString = bWeightDict['sr1_bjet'] #corresponds to bVeto
#bTagString = "nBJet == 0"

degcuts = Cuts("LepAll", "lep", sr1c_opt = "MT95_IncCharge", isrpt = 100, btag = 'sf')
#Wcuts = pickle.load(open("/afs/hephy.at/user/n/nrad/public/wcuts.pkl", "r"))

regions = {name:CutClass(name,[[name,cutlist]]) for name,cutlist in degcuts.bins_sum.list}
#regions = {'SR1a':degcuts.sr1a}#, degcuts.sr1b, degcuts.sr1c, degcuts.sr2]

hist1 = emptyHist("hist1", 10, 0, 10)
hist2 = emptyHist("hist2", 10, 0, 10)
hist_cosThetaStar1 = emptyHist("cosThetaStar1", 100, -1, 1)
hist_cosThetaStar2 = emptyHist("cosThetaStar2", 100, -1, 1)
#hist_HT1 = emptyHist("HT1", 500, 0, 1000)
#hist_HT2 = emptyHist("HT2", 500, 0, 1000)
   
chain = samples.w.tree
  
#normalisationChange = 0.873841238389

SR1s = ['SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRL1b', 'SRL1c', 'SRH1a', 'SRH1b', 'SRH1c', 'SRV1a', 'SRV1b', 'SRV1c']
SR2s = ['SR2', 'SRL2', 'SRH2', 'SRV2']
CR1s = ['CR1a', 'CR1b', 'CR1c']

WpolYields = {}

for reg in regions:
   #Sets event list 
   #chain.SetBranchStatus("*", 1)
   setEventListToChains(samples, ['w'], regions[reg])
   #samples[samp].tree.Draw(">>eList", degcuts.presel.combined)
   #eList = ROOT.gDirectory.Get("eList")
   eList = samples.w.tree.GetEventList()
   nListEntries = eList.GetN()
   #nChainEntries = samples[samp].tree.GetEntries()
  
   #Selecting only used branches
   chain.SetBranchStatus("*", 0)
   
   usedBranches = ["GenPart_" + x for x in ['pt','eta','phi','mass','pdgId','motherId','motherIndex']]
   usedBranches.extend(['weight', 'puReweight', 'weightBTag0_SF', 'weightSBTag0_SF', 'weightSBTag1p_SF', 'weightHBTag0_SF', 'weightHBTag1p_SF', 'weightHBTag1_SF'])
   usedBranches.extend(['met', 'met_pt'])
   
   for branch in chain.GetListOfBranches():
      if branch.GetName() in usedBranches:
         chain.SetBranchStatus(branch.GetName(), 1) 
   
   hist1.Reset()
   hist2.Reset()
   hist_cosThetaStar1.Reset()
   hist_cosThetaStar2.Reset()
   #hist_HT1.Reset()
   #hist_HT2.Reset()
   
   for i in range(nListEntries):
      #print "eList index", i
      #if i == 1000: break
   
      chain.GetEntry(eList.GetEntry(i))
      #TTree:GetEntry(entry) = Read all branches of entry and return total number of bytes read. The function returns the number of bytes read from the input buffer. If entry does not exist the function returns 0. If an I/O error occurs,
      #TEventList:GetEntry(index) = Return value of entry at index in the list. Return -1 if index is not in the list range. 
      #TEventList:GetIndex(entry) Return index in the list of element with value entry array is supposed to be sorted prior to this call. If match is found, function returns position of element.
      
      #Weights 
      lumiWeight = (12864.4/10000.0)
      
      weight = chain.GetLeaf("weight").GetValue(0)
      puWeight = chain.GetLeaf("puReweight").GetValue(0)
       
      #btag weights
      weightBTag0_SF = chain.GetLeaf("weightBTag0_SF").GetValue(0)
      weightSBTag0_SF = chain.GetLeaf("weightSBTag0_SF").GetValue(0)
      weightSBTag1p_SF = chain.GetLeaf("weightSBTag1p_SF").GetValue(0)
      weightHBTag0_SF = chain.GetLeaf("weightHBTag0_SF").GetValue(0)
      weightHBTag1p_SF = chain.GetLeaf("weightHBTag1p_SF").GetValue(0)
      weightHBTag1_SF = chain.GetLeaf("weightHBTag1_SF").GetValue(0)

      if reg in SR1s or reg in CR1s:
         bTagWeight = weightBTag0_SF
      elif reg in SR2s or reg == 'CR2':
         bTagWeight = (weightSBTag1p_SF * weightHBTag0_SF) 
      elif reg == "CRTT2":
         bTagWeight = (weightHBTag1p_SF - (weightSBTag0_SF*weightHBTag1_SF))
      else:
         bTagWeight = 1
      
      genPart = cmgObjectSelection.cmgObject(chain, chain, "GenPart", ['pt','eta','phi','mass','pdgId','motherId','motherIndex'])
      nGenPart = genPart.nObj
   
      lepIndices = []
      wIndices = []
      #print iEvt,
      #print [ [x, genPart.pdgId[x], genPart.motherId[x]] for x in range(nGenPart) ]
      for igp in range(nGenPart):
          #print 'igp: ', igp
          #print 'pdgId: ', abs(genPart.pdgId[igp])
          #print 'if 11, 13, 15: ', abs(genPart.pdgId[igp]) in [11,13,15]
          #print '-------------'
          if abs(genPart.pdgId[igp]) in [11,13,15]:
              lepIndices.append(igp)
          if abs(genPart.pdgId[igp]) == 24:
              wIndices.append(igp)
   
      #print lepIndices
      assert len(wIndices) <= 2 
      if not lepIndices:
          #print "no leptons found"
          continue
      
      wleps = []
      #print lepIndices
      for ilep in lepIndices:
          #print '----------------'
          #print 'ilep: ', ilep
          #print 'motherId: ', abs( genPart.motherId[ilep] )
          #print 'if mother = W: ', abs( genPart.motherId[ilep] ) == 24
          if abs(genPart.motherId[ilep]) == 24:
              #print 'found wlep! ', ilep
              wleps.append(ilep)
   
      #print "wleps: ", wleps
      
      wIndex = wIndices[0]
      W = ROOT.TLorentzVector()
      W.SetPtEtaPhiM(genPart.pt[wIndex], genPart.eta[wIndex], genPart.phi[wIndex], genPart.mass[wIndex])
   
      lep = ROOT.TLorentzVector()
      lepIndex = lepIndices[0]
      lep.SetPtEtaPhiM(genPart.pt[lepIndex], genPart.eta[lepIndex], genPart.phi[lepIndex], genPart.mass[lepIndex])
   
      p4W   = ROOT.LorentzVector(W.Px(), W.Py(), W.Pz(), W.E())
      p4lep = ROOT.LorentzVector(lep.Px(), lep.Py(), lep.Pz(), lep.E())
   
      cosThetaStar = ROOT.WjetPolarizationAngle(p4W, p4lep)

      #float GetWeightWjetsPolarizationFLminusFR(TLorentzVector _p4W, TLorentzVector _p4lepton,float PercentVariation, bool isWplus){
      #uses: float GetWeightFLminusFR(float x,float var,LorentzVector p4W, bool Wplus ){ // variable x is cos(theta) here
      
      #float GetWeightWjetsPolarizationF0(TLorentzVector _p4W, TLorentzVector _p4lepton,float PercentVariation, bool isWplus){
      #uses: float GetWeightF0(float x,float var,LorentzVector p4W, bool Wplus ){
      
      if variation == "simplified": 
         WpolWeight = (1 + 0.1*(1-cosThetaStar)**2)

      elif variation == "FLminusFR":
         #print makeLine()
         #print 'cosThetaStar: ', cosThetaStar
         #print 'pdgId ', genPart.pdgId[wIndex]
         #print 'isWplus ', genPart.pdgId[wIndex] > 0
         #print makeLine()
 
         WpolWeight = ROOT.GetWeightFLminusFR(cosThetaStar, 10, p4W, genPart.pdgId[wIndex] > 0)
         #print makeLine()
         #print "Wpol weight: ", WpolWeight
         #print "Wpol weight (xcheck): ", ROOT.GetWeightWjetsPolarizationF0(p4W, p4lep, 10, genPart.pdgId[wIndex] > 0) 
         #print makeLine()
      
      elif variation == "F0":
         WpolWeight = ROOT.GetWeightF0(cosThetaStar, 10, p4W, genPart.pdgId[wIndex] > 0)
      
      elif variation == "FLFR+":
         if genPart.pdgId[wIndex] > 0:
            WpolWeight = ROOT.GetWeightFLminusFR(cosThetaStar, 5, p4W, True)
            #WpolWeight = ROOT.GetWeightFLFR(cosThetaStar, 5, p4W, True)
         else:
            WpolWeight = 1
      
      elif variation == "FLFR-":
         if genPart.pdgId[wIndex] < 0:
            WpolWeight = ROOT.GetWeightFLminusFR(cosThetaStar, 5, p4W, False)
            #WpolWeight = ROOT.GetWeightFLFR(cosThetaStar, 5, p4W, False)
         else:
            WpolWeight = 1

      #print "COS THETA", cosThetaStar
      hist1.Fill(5, weight*puWeight*bTagWeight*lumiWeight)
      hist2.Fill(5, weight*puWeight*bTagWeight*lumiWeight*WpolWeight)
      hist_cosThetaStar1.Fill(cosThetaStar, weight*puWeight*bTagWeight*lumiWeight)
      hist_cosThetaStar2.Fill(cosThetaStar, weight*puWeight*bTagWeight*lumiWeight*WpolWeight) 
 
   nOrigVal = hist1.GetBinContent(hist1.FindBin(5))
   nOrigErr = hist1.GetBinError(hist1.FindBin(5))

   nCorrVal = hist2.GetBinContent(hist2.FindBin(5))
   nCorrErr = hist2.GetBinError(hist2.FindBin(5))
   
   WpolYields[reg] = {}
   WpolYields[reg]['original'] = u_float.u_float(nOrigVal, nOrigErr)
   WpolYields[reg]['corrected'] = u_float.u_float(nCorrVal, nCorrErr)

   print reg, " Yields - original: ", WpolYields[reg]['original'], " | corrected: ", WpolYields[reg]['corrected'] 
   
   #nOrig = hist_cosThetaStar1.Integral()
   #nCorr = hist_cosThetaStar2.Integral()
   #nOrig = hist_cosThetaStar1.IntegralAndError()
   #nCorr = hist_cosThetaStar2.IntegralAndError()

   if plot:  
      canv = ROOT.TCanvas("canv", "Canvas", 1800, 1500)

      hist_cosThetaStar1.SetName("cosThetaStar1")
      hist_cosThetaStar1.SetTitle("Cos(#theta*) Plot")
      hist_cosThetaStar1.GetXaxis().SetTitle("Cos(#theta*)")
      hist_cosThetaStar1.SetFillColor(samples['w'].color)
      hist_cosThetaStar1.SetFillColorAlpha(hist_cosThetaStar1.GetFillColor(), 0.7)
      #hist.SetLineColor(ROOT.kBlack)
      #hist.SetLineWidth(3)

      hist_cosThetaStar2.SetName("cosThetaStar2")
      hist_cosThetaStar2.SetTitle("Cos(#theta*) Plot")
      hist_cosThetaStar2.GetXaxis().SetTitle("Cos(#theta*)")
      #hist_cosThetaStar2.SetFillColor(ROOT.kBlue)

      #hist.SetLineColor(ROOT.kBlack)
      #hist.SetLineWidth(3)
      hist_cosThetaStar2.Draw('hist')
      hist_cosThetaStar1.Draw('hist same')

      if logy: ROOT.gPad.SetLogy()
      ROOT.gPad.Modified()
      ROOT.gPad.Update()

      #leg = makeLegend2()
      leg = ROOT.TLegend()
      leg.AddEntry("cosThetaStar1", "Original", "F")
      leg.AddEntry("cosThetaStar2", "Reweighted", "F")
      leg.Draw()

      alignLegend(leg, y1=0.7, y2=0.8, x1=0.8, x2=0.9)

      latex = ROOT.TLatex()
      latex.SetNDC()
      latex.SetTextSize(0.04)
      latex.DrawLatex(0.16,0.96,"#font[22]{CMS Simulation}")

      ROOT.gPad.Modified()
      ROOT.gPad.Update()

      #Save canvas
      if save: #web address: http://www.hephy.at/user/mzarucki/plots
         canv.SaveAs("%s/Wpol_%s.png"%(savedir, reg))
         canv.SaveAs("%s/root/Wpol_%s.root"%(savedir, reg))
         canv.SaveAs("%s/pdf/Wpol_%s.pdf"%(savedir, reg))
         #if reg.name == 'presel': 
         #   canv2.SaveAs("%s/HT_%s.png"%(savedir, reg.name))
         #   canv3.SaveAs("%s/HT_weight_%s.png"%(savedir, reg.name))

pickleFile1 = open("%s/WpolYields.pkl"%(savedir), "w")
pickle.dump(WpolYields, pickleFile1)
pickleFile1.close()

SRs = {'SR1a':'CR1a', 'SR1b':'CR1b', 'SR1c':'CR1c', 'SRL1a':'CR1a', 'SRL1b':'CR1b', 'SRL1c':'CR1c', 'SRH1a':'CR1a', 'SRH1b':'CR1b', 'SRH1c':'CR1c', 'SRV1a':'CR1a', 'SRV1b':'CR1b', 'SRV1c':'CR1c', 'SR2':'CR2', 'SRL2':'CR2', 'SRH2':'CR2', 'SRV2':'CR2'}
CRs = ['CR1a', 'CR1b', 'CR1c', 'CR2', 'CRTT2']
SRs_2 = ['SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRL1b', 'SRL1c', 'SRH1a', 'SRH1b', 'SRH1c', 'SRV1a', 'SRV1b', 'SRV1c', 'SR2', 'SRL2', 'SRH2', 'SRV2']

ratios = {} #SR/CR

for reg in SRs:
   ratios[reg] = {}
   if WpolYields[SRs[reg]]['original'].val: 
      ratios[reg]['original'] = WpolYields[reg]['original']/WpolYields[SRs[reg]]['original']
   else: 
      ratios[reg]['original'] = u_float.u_float(0., 0.)  
   
   if WpolYields[SRs[reg]]['corrected'].val: 
      ratios[reg]['corrected'] = WpolYields[reg]['corrected']/WpolYields[SRs[reg]]['corrected']
   else:
      ratios[reg]['corrected'] = u_float.u_float(0., 0.)

   if ratios[reg]['original'].val: 
      ratios[reg]['ratio'] = ratios[reg]['corrected']/ratios[reg]['original']
   else:
      ratios[reg]['ratio'] = u_float.u_float(0., 0.)

pickleFile2 = open("%s/WpolRatios.pkl"%(savedir), "w")
pickle.dump(ratios, pickleFile2)
pickleFile2.close()
   
if makeTable:
   print "Making table"
   WpolRows = []
   listTitle = ['$\mathbf{Region}$', '$\mathbf{Original~Yield}$', '$\mathbf{Corrected~Yield}$', '$\mathbf{SF(SR-CR)~[Original]}$', '$\mathbf{SF(SR-CR)~[Corrected]}$', '$\mathbf{SF(SR-CR)~Ratio}$']
   WpolRows.append(listTitle)
   for reg in SRs_2:
      WpolRows.append([reg, str(WpolYields[reg]['original'].round(2)), str(WpolYields[reg]['corrected'].round(2)), str(ratios[reg]['original'].round(2)), str(ratios[reg]['corrected'].round(2)), str(ratios[reg]['ratio'].round(2))])
      #WpolRows.append([reg, "$%.2f$"%(WpolYields[reg]['original']), "$%.2f$"%(WpolYields[reg]['corrected']), "$%.2f$"%(ratios[reg]['original']), "$%.2f$"%(ratios[reg]['corrected']), "$%.2f$"%(ratios[reg]['ratio'])]) 
   for reg in CRs:
      WpolRows.append([reg, str(WpolYields[reg]['original'].round(2)), str(WpolYields[reg]['corrected'].round(2)), "", "", ""])

   makeSimpleLatexTable(WpolRows, "WpolTable", savedir)
