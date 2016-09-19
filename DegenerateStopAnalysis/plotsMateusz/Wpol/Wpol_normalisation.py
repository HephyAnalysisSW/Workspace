# Wpol_normalisation.py
# Script for calculating the normalisation change of W-polarization variation on Wjets cmg-tuple. Uses event loop. 
# Mateusz Zarucki 2016

import ROOT
import os, sys
import math
import argparse
import pickle
import glob
from array import array
from math import pi, sqrt #cos, sin, sinh, log
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.HEPHYPythonTools.helpers import getYieldFromChain # getChain, getPlotFromChain, getChunks
from Workspace.DegenerateStopAnalysis.cmgPostProcessing import cmgObjectSelection
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, makeDir, setup_style
#from Workspace.DegenerateStopAnalysis.tools.bTagWeights import bTagWeights
from Workspace.DegenerateStopAnalysis.samples.cmgTuples.RunIISpring16MiniAODv2_v3 import sample_path as mc_sample_path
#from Workspace.DegenerateStopAnalysis.samples.cmgTuples.Data2016_v3 import sample_path as data_sample_path
from Workspace.DegenerateStopAnalysis.tools.getSamples_8012 import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed

ROOT.gROOT.ProcessLine(".L %s/src/Workspace/HEPHYPythonTools/scripts/root/WPolarizationVariation.C+"%(os.path.expandvars("$CMSSW_BASE") ))

#Sets TDR style
setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--cmgTag", dest = "cmgTag",  help = "CMG Tag", type = str, default = "8012_mAODv2_v3")
parser.add_argument("--plot", dest = "plot",  help = "Toggle plotting", type = int, default = 0)
parser.add_argument("--plotHT", dest = "plotHT",  help = "Plot HT", type = int, default = 0)
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
cmgTag = args.cmgTag
plot = args.plot
plotHT = args.plotHT
logy = args.logy
save = args.save
verbose = args.verbose

print makeDoubleLine()
print "Running W polarisation (normalisation) script"
print makeDoubleLine()

#Samples
cmgPP = cmgTuplesPostProcessed()

samples = getSamples(cmgPP = cmgPP, skim = 'preIncLep', sampleList = ['w'], scan = False, useHT = True, getData = False)

if verbose:
   print makeLine()
   print "Using samples:"
   newLine()
   for s in samplesList:
      if s: print samples[s].name,":",s
      else:
         print "!!! Sample " + sample + " unavailable."
         sys.exit(0)

cmgDict = {'tag':cmgTag,
           'version':cmgTag.split('_')[2],
           'dir':"/data/nrad/cmgTuples/" + cmgTag}

cmgDict['mc_path'] =     cmgDict['dir'] + "/RunIISpring16MiniAODv2"
cmgDict['signal_path'] = cmgDict['dir'] + "/RunIISpring16MiniAODv2"
cmgDict['data_path'] =   cmgDict['dir'] + "/Data25ns"

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/Wpol"%tag
   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

chain = ROOT.TChain("tree")

for bin in samples['w'].sample['bins']:
   cmgPath = "%s/%s/%s_Chunk*/tree.root"%(cmgDict['mc_path'], bin, bin)

   files = glob.glob(cmgPath)

   for f in files:
      chain.Add(f)

hist_thetaStar1 = emptyHist("thetaStar1", 100, -3.14, 3.14)
hist_thetaStar2 = emptyHist("thetaStar2", 100, -3.14, 3.14)
hist_cosThetaStar1 = emptyHist("cosThetaStar1", 100, -1, 1)
hist_cosThetaStar2 = emptyHist("cosThetaStar2", 100, -1, 1)

if plotHT:
   hist_HT1 = emptyHist("HT1", 500, 0, 1000)
   hist_HT2 = emptyHist("HT2", 500, 0, 1000)

nEntries = chain.GetEntries()

#Selecting only used branches
chain.SetBranchStatus("*", 0)

usedBranches = ["GenPart_" + x for x in ['pt','eta','phi','mass','pdgId','motherId','motherIndex']]
usedBranches.append('xsec') 
if plotHT: usedBranches.extend(['Jet_' + x for x in ['pt', 'eta', 'id']])

for branch in chain.GetListOfBranches():
   if branch.GetName() in usedBranches: 
      chain.SetBranchStatus(branch.GetName(), 1)

for iEvt in range(nEntries):
   #print "EVENT ", iEvt 
   #if iEvt == 5000: break

   chain.GetEntry(iEvt)
   
   #chain.GetEntry(eList.GetEntry(iEvt))
   #TTree:GetEntry(entry) = Read all branches of entry and return total number of bytes read. The function returns the number of bytes read from the input buffer. If entry does not exist the function returns 0. If an I/O error occurs,
   #TEventList:GetEntry(index) = Return value of entry at index in the list. Return -1 if index is not in the list range. 
   #TEventList:GetIndex(entry) Return index in the list of element with value entry array is supposed to be sorted prior to this call. If match is found, function returns position of element.
    
   genPart = cmgObjectSelection.cmgObject(chain, chain, "GenPart", ['pt','eta','phi','mass','pdgId','motherId','motherIndex'])
   Jet = cmgObjectSelection.cmgObject(chain, chain, "Jet", ['pt','eta','id'])
   xsec = chain.GetLeaf("xsec").GetValue(0)
   #HT = chain.tree.GetLeaf("ht_basJet").GetValue(0)
   #print 'weight: ', weight

   lumiWeight = xsec*10000/nEntries

   nGenPart = genPart.nObj
  
   if plotHT: 
      HT = 0.0
      nJets = Jet.nObj

      for iJet in range(nJets):
         #print Jet.pt[iJet], " ", Jet.eta[iJet] 
         if Jet.pt[iJet] > 30 and abs(Jet.eta[iJet]) < 2.4 and Jet.id[iJet]:
            HT += Jet.pt[iJet]

      #print "HT: ",  HT
      #print "Lumi weight: ", lumiWeight
      hist_HT1.Fill(HT)
      hist_HT2.Fill(HT, lumiWeight)

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
       if abs( genPart.motherId[ilep] ) == 24:
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
   
   WpolWeight = (1 + 0.1*(1-cosThetaStar)**2)
   
   #print "COS THETA", cosThetaStar
   hist_cosThetaStar1.Fill(cosThetaStar, lumiWeight)
   hist_cosThetaStar2.Fill(cosThetaStar, lumiWeight*WpolWeight)
   #hist_thetaStar1.Fill(thetaStar)

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
   
   canv2 = ROOT.TCanvas("canv2", "Canvas", 1800, 1500)
   hist_HT1.Draw('hist')
   canv3 = ROOT.TCanvas("canv3", "Canvas", 1800, 1500)
   hist_HT2.Draw('hist')

#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   canv.SaveAs("%s/Wpol_normalisation.png"%(savedir))
   canv2.SaveAs("%s/HT1.png"%(savedir))
   canv3.SaveAs("%s/HT2.png"%(savedir))
   canv.SaveAs("%s/root/Wpol_normalisation.root"%(savedir))
   canv.SaveAs("%s/pdf/Wpol_normalisation.pdf"%(savedir))
