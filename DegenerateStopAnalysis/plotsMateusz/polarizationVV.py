# polarizationVV.py
# Mateusz Zarucki 2017

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
from Workspace.DegenerateStopAnalysis.tools.getSamples2 import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_Summer16_2 import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import cutWeightOptions, triggers, filters
from Workspace.HEPHYPythonTools import u_float
from array import array
from math import pi, sqrt #cos, sin, sinh, log

ROOT.gROOT.ProcessLine(".L %s/src/Workspace/HEPHYPythonTools/scripts/root/WPolarizationVariation.C+"%(os.path.expandvars("$CMSSW_BASE") ))

#Sets TDR style
setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
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
logy = args.logy
save = args.save
verbose = args.verbose

samplesList = ['vvinc', 'vv']

#Samples
cmgPP = cmgTuplesPostProcessed()
samples = getSamples(cmgPP = cmgPP, skim = 'preIncLep', sampleList = samplesList, scan = False, useHT = True, getData = False, def_weights = [])

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
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/polarizationVV"%tag
    
   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

# Cuts and Weights
cuts_weights = CutsWeights(samples, cutWeightOptions)

hists = {}

charge = 'pos'

suffix = ''

if charge:
   suffix += '_' + charge

for s in samplesList:

   hists[s] = emptyHist("cosThetaStar_"+s, 100, -1, 1)
 
   chain = samples[s].tree
     
   # Cuts and weights   
   #cut = cuts_weights.cuts_weights[reg]['w'][0]
   weight = cuts_weights.cuts_weights['none']['vvinc'][1]
   
   #Weights 
   #lumiWeight = (35854.9/10000.0)
   
   ##Sets event list 
   #chain.SetBranchStatus("*", 1)
   #chain.SetEventList(0)
   #setEventListToChains(samples, ['w'], cuts_weights.cuts.cutInsts[reg])
   ##samples[samp].tree.Draw(">>eList", degcuts.presel.combined)
   ##eList = ROOT.gDirectory.Get("eList")
   #eList = chain.GetEventList()
   #nListEntries = eList.GetN()
   ##nChainEntries = samples[samp].tree.GetEntries()
   #
   ##Selecting only used branches
   #chain.SetBranchStatus("*", 0)
   #
   #usedBranches = ["GenPart_" + x for x in ['pt','eta','phi','mass','pdgId','motherId','motherIndex']]
   #usedBranches.extend(['weight', 'puReweight', 'weightBTag0_SF_def', 'weightSBTag0_SF_def', 'weightSBTag1p_SF_def', 'weightHBTag0_SF_def', 'weightHBTag1p_SF_def', 'weightHBTag1_SF_def'])
   #usedBranches.extend(['met', 'met_pt'])
   #
   #for branch in chain.GetListOfBranches():
   #   if branch.GetName() in usedBranches:
   #      chain.SetBranchStatus(branch.GetName(), 1) 
   
   hists[s].Reset()
   hists[s].SetName("cosThetaStar_"+s)
   
   nEntries = chain.GetEntries()
   
   for i in range(nEntries):
      #print "eList index", i
      #if i == 1000: break
   
      chain.GetEntry(i)
      #TTree:GetEntry(entry) = Read all branches of entry and return total number of bytes read. The function returns the number of bytes read from the input buffer. If entry does not exist the function returns 0. If an I/O error occurs,
      #TEventList:GetEntry(index) = Return value of entry at index in the list. Return -1 if index is not in the list range. 
      #TEventList:GetIndex(entry) Return index in the list of element with value entry array is supposed to be sorted prior to this call. If match is found, function returns position of element.
   
      genPart = cmgObjectSelection.cmgObject(chain, chain, "GenPart", ['pt','eta','phi','mass','pdgId','motherId','motherIndex', 'isPromptHard'])
      nGenPart = genPart.nObj
   
      weight =   chain.GetLeaf("weight").GetValue(0)
      #puWeight = chain.GetLeaf("puReweight").GetValue(0)
   
      lepIndices = []
      nuIndices = []
      #wIndices = []
      #print iEvt,
      #print [ [x, genPart.pdgId[x], genPart.motherId[x]] for x in range(nGenPart) ]
      for igp in range(nGenPart):
          #print 'igp: ', igp
          #print 'pdgId: ', abs(genPart.pdgId[igp])
          #print 'if 11, 13, 15: ', abs(genPart.pdgId[igp]) in [11,13,15]
          #print '-------------'
          if abs(genPart.pdgId[igp]) in [11,13,15] and abs(genPart.motherId[igp]) == 24 and genPart.isPromptHard[igp]:
              lepIndices.append(igp)
          if abs(genPart.pdgId[igp]) in [12,14,16] and abs(genPart.motherId[igp]) == 24 and genPart.isPromptHard[igp]:
              nuIndices.append(igp)
          #if abs(genPart.pdgId[igp]) == 24:
          #    wIndices.append(igp)
      
      print '---'
      print 'leps: ', lepIndices
      print 'nus: ',  nuIndices
      #assert len(wIndices) <= 2 
      if not lepIndices:
          print "no leptons found"
          continue
      if not nuIndices:
          print "no neutrinos found"
          continue
      
      # cut on nleps and nu from W
      if len(lepIndices) != 1: continue
      if len(nuIndices) != 1: continue
     
      #wIndex =   wIndices[0]
      lepIndex = lepIndices[0]
      nuIndex = nuIndices[0]
      
      if charge == 'neg':
         if genPart.pdgId[lepIndex] < 0: continue 
      elif charge == 'pos':
         if genPart.pdgId[lepIndex] > 0: continue 
 
      W = ROOT.TLorentzVector()
      #W.SetPtEtaPhiM(genPart.pt[wIndex], genPart.eta[wIndex], genPart.phi[wIndex], genPart.mass[wIndex])
      
      lep = ROOT.TLorentzVector()
      lep.SetPtEtaPhiM(genPart.pt[lepIndex], genPart.eta[lepIndex], genPart.phi[lepIndex], genPart.mass[lepIndex])
      
      nu = ROOT.TLorentzVector()
      nu.SetPtEtaPhiM(genPart.pt[nuIndex], genPart.eta[nuIndex], genPart.phi[nuIndex], genPart.mass[nuIndex])
  
      W+=lep
      W+=nu

      print 'lep:', lep.Px(), lep.Py(), lep.Pz(), lep.E()
      print 'n:', nu.Px(), nu.Py(), nu.Pz(), nu.E()
      print 'W:', W.Px(), W.Py(), W.Pz(), W.E()
 
      p4W   = ROOT.LorentzVector(W.Px(), W.Py(), W.Pz(), W.E())
      p4lep = ROOT.LorentzVector(lep.Px(), lep.Py(), lep.Pz(), lep.E())
   
      cosThetaStar = ROOT.WjetPolarizationAngle(p4W, p4lep)
   
      #print "COS THETA", cosThetaStar
      #hist2.Fill(5, weight*WpolWeight)
      hists[s].Fill(cosThetaStar, weight)
      #hist_cosThetaStar2.Fill(cosThetaStar, weight*WpolWeight) 

canv = ROOT.TCanvas("canv", "Canvas", 1800, 1500)

hists['vvinc'].SetTitle("Cos(#theta*) Plot")
hists['vvinc'].GetXaxis().SetTitle("Cos(#theta*)")
#hists['vvinc'].SetMaximum(100)
hists['vvinc'].SetFillColor(samples['vvinc'].color)
hists['vvinc'].SetFillColorAlpha(hists['vvinc'].GetFillColor(), 0.7)

hists['vv'].SetTitle("Cos(#theta*) Plot")
hists['vv'].GetXaxis().SetTitle("Cos(#theta*)")
hists['vv'].SetFillColor(ROOT.kBlue)

hists['vv'].Draw('hist')
hists['vvinc'].Draw('histsame')

if logy: ROOT.gPad.SetLogy()
ROOT.gPad.Modified()
ROOT.gPad.Update()

#leg = makeLegend2()
leg = ROOT.TLegend()
leg.AddEntry("cosThetaStar_vvinc", "Inclusive VV (P8)", "F")
leg.AddEntry("cosThetaStar_vv", "Exclusive VV (NLO)", "F")
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
   canv.SaveAs("%s/Wpol%s.png"%(savedir, suffix))
   canv.SaveAs("%s/root/Wpol%s.root"%(savedir, suffix))
   canv.SaveAs("%s/pdf/Wpol%s.pdf"%(savedir, suffix))
   #if reg.name == 'presel': 
   #   canv2.SaveAs("%s/HT_%s.png"%(savedir, reg.name))
   #   canv3.SaveAs("%s/HT_weight_%s.png"%(savedir, reg.name))
