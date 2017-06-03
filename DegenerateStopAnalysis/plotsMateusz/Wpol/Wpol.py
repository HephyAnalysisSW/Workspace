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
from Workspace.DegenerateStopAnalysis.tools.degCuts2 import Cuts, CutsWeights
from Workspace.DegenerateStopAnalysis.cmgPostProcessing import cmgObjectSelection
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_Summer16 import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import cutWeightOptions, triggers, filters
from Workspace.HEPHYPythonTools import u_float
from array import array
from math import pi, sqrt #cos, sin, sinh, log

ROOT.gROOT.ProcessLine(".L %s/src/Workspace/HEPHYPythonTools/scripts/root/WPolarizationVariation.C+"%(os.path.expandvars("$CMSSW_BASE") ))

#Sets TDR style
setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--variation", dest = "variation",  help = "Variation", type = str, default = "FLminusFR")
parser.add_argument("--plot", dest = "plot",  help = "Toggle plotting", type = int, default = 1)
parser.add_argument("--makeTable", dest = "makeTable",  help = "Make table", type = int, default = 1)
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
variation = args.variation
plot = args.plot
makeTable = args.makeTable
logy = args.logy
save = args.save
verbose = args.verbose

print makeDoubleLine()
print "Running W polarisation script"
print makeDoubleLine()

#Samples
cmgPP = cmgTuplesPostProcessed()
samples = getSamples(cmgPP = cmgPP, skim = 'preIncLep', sampleList = ['w'], scan = False, useHT = True, getData = False, def_weights = [])

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
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/Wpol"%tag
   savedir += "/" + variation
    
   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

# Cuts and Weights
cuts_weights = CutsWeights(samples, cutWeightOptions)

hist1 = emptyHist("hist1", 10, 0, 10)
hist2 = emptyHist("hist2", 10, 0, 10)
hist_cosThetaStar1 = emptyHist("cosThetaStar1", 100, -1, 1)
hist_cosThetaStar2 = emptyHist("cosThetaStar2", 100, -1, 1)
#hist_HT1 = emptyHist("HT1", 500, 0, 1000)
#hist_HT2 = emptyHist("HT2", 500, 0, 1000)
   
chain = samples.w.tree
  
WpolYields = {}

SR1s = ['sr1a', 'sr1b', 'sr1c', 'sr1vla', 'sr1vlb', 'sr1vlc', 'sr1la', 'sr1lb', 'sr1lc', 'sr1ma', 'sr1mb', 'sr1mc', 'sr1ha', 'sr1hb', 'sr1hc']
SR2s = ['sr2a', 'sr2b', 'sr2c', 'sr2vla', 'sr2vlb', 'sr2vlc', 'sr2la', 'sr2lb', 'sr2lc', 'sr2ma', 'sr2mb', 'sr2mc', 'sr2ha', 'sr2hb', 'sr2hc']
CRs =  ['cr1a', 'cr1b', 'cr1c', 'cr2a', 'cr2b', 'cr2c']

regions = SR1s + SR2s + CRs
allRegions = []

for x in regions:
   allRegions.append(x+'X')
   allRegions.append(x+'Y')

for reg in allRegions:
   print "Region: ", reg
   # Cuts and weights   
   #cut = cuts_weights.cuts_weights[reg]['w'][0]
   weight = cuts_weights.cuts_weights[reg]['w'][1]
   
   #Weights 
   lumiWeight = (35854.9/10000.0)
   
   #Sets event list 
   chain.SetBranchStatus("*", 1)
   chain.SetEventList(0)
   setEventListToChains(samples, ['w'], cuts_weights.cuts.cutInsts[reg])
   #samples[samp].tree.Draw(">>eList", degcuts.presel.combined)
   #eList = ROOT.gDirectory.Get("eList")
   eList = chain.GetEventList()
   nListEntries = eList.GetN()
   #nChainEntries = samples[samp].tree.GetEntries()
  
   #Selecting only used branches
   chain.SetBranchStatus("*", 0)
   
   usedBranches = ["GenPart_" + x for x in ['pt','eta','phi','mass','pdgId','motherId','motherIndex']]
   usedBranches.extend(['weight', 'puReweight', 'weightBTag0_SF_def', 'weightSBTag0_SF_def', 'weightSBTag1p_SF_def', 'weightHBTag0_SF_def', 'weightHBTag1p_SF_def', 'weightHBTag1_SF_def'])
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

      genPart = cmgObjectSelection.cmgObject(chain, chain, "GenPart", ['pt','eta','phi','mass','pdgId','motherId','motherIndex'])
      nGenPart = genPart.nObj
   
      weight =   chain.GetLeaf("weight").GetValue(0)
      puWeight = chain.GetLeaf("puReweight").GetValue(0)

      #btag weights
      weightBTag0_SF =   chain.GetLeaf("weightBTag0_SF_def").GetValue(0)
      weightSBTag0_SF =  chain.GetLeaf("weightSBTag0_SF_def").GetValue(0)
      weightSBTag1p_SF = chain.GetLeaf("weightSBTag1p_SF_def").GetValue(0)
      weightHBTag0_SF =  chain.GetLeaf("weightHBTag0_SF_def").GetValue(0)
      weightHBTag1p_SF = chain.GetLeaf("weightHBTag1p_SF_def").GetValue(0)
      weightHBTag1_SF =  chain.GetLeaf("weightHBTag1_SF_def").GetValue(0)

      if reg in SR1s or reg in CRs:
         bTagWeight = weightBTag0_SF
      elif reg in SR2s or reg == 'CR2':
         bTagWeight = (weightSBTag1p_SF * weightHBTag0_SF) 
      elif reg == "CRTT2":
         bTagWeight = (weightHBTag1p_SF - (weightSBTag0_SF*weightHBTag1_SF))
      else:
         bTagWeight = 1
   
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
      hist1.Fill(5, weight)
      hist2.Fill(5, weight*WpolWeight)
      hist_cosThetaStar1.Fill(cosThetaStar, weight)
      hist_cosThetaStar2.Fill(cosThetaStar, weight*WpolWeight) 
 
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

SCRs =  {'sr1a':'cr1a', 'sr1b':'cr1b', 'sr1c':'cr1c', 'sr1vla':'cr1a', 'sr1vlb':'cr1b', 'sr1vlc':'cr1c', 'sr1la':'cr1a', 'sr1lb':'cr1b', 'sr1lc':'cr1c', 'sr1ma':'cr1a', 'sr1mb':'cr1b', 'sr1mc':'cr1c', 'sr1ha':'cr1a', 'sr1hb':'cr1b', 'sr1hc':'cr1c'}
SCR2s = {'sr2a':'cr2a', 'sr2b':'cr2b', 'sr2c':'cr2c', 'sr2vla':'cr2a', 'sr2vlb':'cr2b', 'sr2vlc':'cr2c', 'sr2la':'cr2a', 'sr2lb':'cr2b', 'sr2lc':'cr2c', 'sr2ma':'cr2a', 'sr2mb':'cr2b', 'sr2mc':'cr2c', 'sr2ha':'cr2a', 'sr2hb':'cr2b', 'sr2hc':'cr2c'}

SCRs.update(SCR2s)   

CRs =   ['cr1a', 'cr1b', 'cr1c','cr2a', 'cr2b', 'cr2c']
SRs_2 = ['sr1a', 'sr1b', 'sr1c', 'sr1vla', 'sr1vlb', 'sr1vlc', 'sr1la', 'sr1lb', 'sr1lc', 'sr1ma', 'sr1mb', 'sr1mc', 'sr1ha', 'sr1hb', 'sr1hc', \
         'sr2a', 'sr2b', 'sr2c', 'sr2vla', 'sr2vlb', 'sr2vlc', 'sr2la', 'sr2lb', 'sr2lc', 'sr2ma', 'sr2mb', 'sr2mc', 'sr2ha', 'sr2hb', 'sr2hc']

ratios = {} #SR/CR

allSCRs = {}
allSRs = []
allCRs = []
for x in SCRs:
   allSCRs.update({x+'Y':SCRs[x]+'Y'})
   allSCRs.update({x+'X':SCRs[x]+'X'})

for x in SRs_2:
   allSRs.append(x+'X')
   allSRs.append(x+'Y')
for x in CRs:
   allCRs.append(x+'X')
   allCRs.append(x+'Y')

for reg in allSRs:
   ratios[reg] = {}
   if WpolYields[allSCRs[reg]]['original'].val: 
      ratios[reg]['original'] = WpolYields[reg]['original']/WpolYields[allSCRs[reg]]['original']
   else: 
      ratios[reg]['original'] = u_float.u_float(0., 0.)  
   
   if WpolYields[allSCRs[reg]]['corrected'].val: 
      ratios[reg]['corrected'] = WpolYields[reg]['corrected']/WpolYields[allSCRs[reg]]['corrected']
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
   listTitle = ['$\mathbf{Region}$', '$\mathbf{Original~Yield}$', '$\mathbf{Corrected~Yield}$', '$\mathbf{TF(SR-CR)~[Original]}$', '$\mathbf{TF(SR-CR)~[Corrected]}$', '$\mathbf{TF(SR-CR)~Ratio}$']
   WpolRows.append(listTitle)
   for reg in allSRs:
      WpolRows.append([reg, str(WpolYields[reg]['original'].round(2)), str(WpolYields[reg]['corrected'].round(2)), str(ratios[reg]['original'].round(2)), str(ratios[reg]['corrected'].round(2)), str(ratios[reg]['ratio'].round(2))])
      #WpolRows.append([reg, "$%.2f$"%(WpolYields[reg]['original']), "$%.2f$"%(WpolYields[reg]['corrected']), "$%.2f$"%(ratios[reg]['original']), "$%.2f$"%(ratios[reg]['corrected']), "$%.2f$"%(ratios[reg]['ratio'])]) 
   for reg in allCRs:
      WpolRows.append([reg, str(WpolYields[reg]['original'].round(2)), str(WpolYields[reg]['corrected'].round(2)), "", "", ""])

   makeSimpleLatexTable(WpolRows, "WpolTable", savedir)

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
