import ROOT
import os, sys
import math
import argparse
import pickle
from array import array
from math import pi, sqrt #cos, sin, sinh, log

from DataFormats.FWLite import Events, Handle

trigger = 'MET'
triggerName = 'HLT_MET120_MHT120_IDTight'
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/TriggerStudies"

infile = '/afs/hephy.at/data/mzarucki02/TriggerStudies/CMSSW_9_2_12/AOD/T2tt_dM-10to80_mStop-500_mLSP-460_noPU_SoftTriggers_HLT_AODSIM.root'
outfile = 'trigEff_%s.root'%trigger

f = ROOT.TFile(infile)
tree = f.Get("Events")

#Efficiency
def makeEffPlot(passed,total):
   a = passed.Clone()
   b = total.Clone()
   eff = ROOT.TEfficiency(a,b)
   eff.SetTitle("Efficiency Plot")
   eff.SetMarkerStyle(33)
   eff.SetMarkerSize(2)
   eff.SetLineWidth(2)
   return eff

def setupEffPlot(eff):
   ROOT.gPad.Modified()
   ROOT.gPad.Update()

   ROOT.gPad.SetGridx()
   ROOT.gPad.SetGridy()
   eff.GetPaintedGraph().GetYaxis().SetTitle("Efficiency")
   eff.GetPaintedGraph().SetMinimum(0)
   eff.GetPaintedGraph().SetMaximum(1)
   eff.GetPaintedGraph().GetXaxis().CenterTitle()
   eff.GetPaintedGraph().GetYaxis().CenterTitle()

   ROOT.gPad.Modified()
   ROOT.gPad.Update()

den = ROOT.TH1D("den", "den", 100, 0, 500)
den.SetTitle("MET Distribution")
den.GetYaxis().SetTitle("Events")
den.GetXaxis().SetTitle("PF-MET")
den.GetXaxis().CenterTitle()
den.GetYaxis().CenterTitle()
den.GetXaxis().SetTitleOffset(1.2)
den.GetYaxis().SetTitleOffset(1.2)
den.SetFillColor(ROOT.kBlue-9)
den.SetLineColor(ROOT.kBlack)
den.SetLineWidth(2)

num = ROOT.TH1D("num", "num", 100, 0, 500)
num.GetYaxis().SetTitle("Events")
num.GetXaxis().SetTitle("PF-MET")
num.GetXaxis().CenterTitle()
num.GetYaxis().CenterTitle()
num.GetXaxis().SetTitleOffset(1.2)
num.GetYaxis().SetTitleOffset(1.2)
num.SetFillColor(ROOT.kRed+1)
num.SetLineColor(ROOT.kBlack)
num.SetLineWidth(2)

##Sets event list 
#tree.SetBranchStatus("*", 1)
#tree.SetEventList(0)
#setEventListToChains(samples, ['w'], cuts_weights.cuts.cutInsts[reg])
##samples[samp].tree.Draw(">>eList", degcuts.presel.combined)
##eList = ROOT.gDirectory.Get("eList")
#eList = tree.GetEventList()
#nListEntries = eList.GetN()
##nChainEvents = samples[samp].tree.GetEntries()
#
##Selecting only used branches
#tree.SetBranchStatus("*", 0)
#
#usedBranches = ["GenPart_" + x for x in ['pt','eta','phi','mass','pdgId','motherId','motherIndex']]
#usedBranches.extend(['weight', 'puReweight', 'weightBTag0_SF_def', 'weightSBTag0_SF_def', 'weightSBTag1p_SF_def', 'weightHBTag0_SF_def', 'weightHBTag1p_SF_def', 'weightHBTag1_SF_def'])
#usedBranches.extend(['met', 'met_pt'])
#
#for branch in tree.GetListOfBranches():
#   if branch.GetName() in usedBranches:
#      tree.SetBranchStatus(branch.GetName(), 1) 

#nEvents = nListEntries
nEvents = tree.GetEntries() 

handleMETs = Handle("std::vector<reco::PFMET>")

files = infile

events = Events(files)

#for i in range(nEvents):
for i,event in enumerate(events):
   #print i
   #print "eList index", i
   #if i == 100: break

   tree.GetEntry(i)
   #tree.GetEntry(eList.GetEntry(i))
   #TTree:GetEntry(entry) = Read all branches of entry and return total number of bytes read. The function returns the number of bytes read from the input buffer. If entry does not exist the function returns 0. If an I/O error occurs,
   #TEventList:GetEntry(index) = Return value of entry at index in the list. Return -1 if index is not in the list range. 
   #TEventList:GetIndex(entry) Return index in the list of element with value entry array is supposed to be sorted prior to this call. If match is found, function returns position of element.

   event.getByLabel(("pfMet", '', 'RECO'), handleMETs)
   met = handleMETs.product().front()
   MET = met.pt()
   
   #MET = tree.GetLeaf("recoPFMETs_pfMet__RECO.obj").pt().GetValue(0)

   decision = tree.GetLeaf("bool_trigDec_HLTPFMET120PFMHT120IDTight_SoftTriggers.obj").GetValue()
   
   den.Fill(MET)
   if decision:
      num.Fill(MET)

canv = ROOT.TCanvas("Canvas", "Canvas", 1500, 1500)
canv.Divide(1,2)

canv.cd(1)

den.Draw('hist')
num.Draw('hist same')

ROOT.gPad.Modified()
ROOT.gPad.Update()

#latex = ROOT.TLatex()
#latex.SetNDC()
#latex.SetTextSize(0.04)
#latex.DrawLatex(0.16,0.96,"#font[22]{CMS Simulation}")

canv.cd(2)

eff = makeEffPlot(num,den)
eff.SetTitle("%s Trigger Efficiency; PF-MET; Trigger Efficiency"%triggerName)
eff.Draw("AP")

ROOT.gPad.Modified()
ROOT.gPad.Update()

setupEffPlot(eff)

#Save canvas
canv.SaveAs("%s/trigEff_%s.png"%(savedir, triggerName))
