# lepEff.py
# Mateusz Zarucki 2017

import ROOT
import os, sys
import copy
import math
import argparse
import pickle
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, makeSimpleLatexTable, makeDir
from Workspace.DegenerateStopAnalysis.tools.degCuts2 import Cuts, CutsWeights
from Workspace.DegenerateStopAnalysis.tools.Sample import Sample
from Workspace.DegenerateStopAnalysis.cmgPostProcessing import cmgObjectSelection
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_Summer16 import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import cutWeightOptions, triggers, filters
from Workspace.HEPHYPythonTools import u_float
from array import array
from math import pi, sqrt #cos, sin, sinh, log

ROOT.gStyle.SetOptStat(0) #1111 adds histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--lep", dest = "lep",  help = "Lepton", type = str, default = "mu")
parser.add_argument("--applySF", dest = "applySF",  help = "Apply data/MC SF", type = int, default = 0)
parser.add_argument("--standardBins", dest = "standardBins",  help = "Standard binning", type = int, default = 0)
parser.add_argument("--varBins", dest = "varBins",  help = "Variable bin size", type = int, default = 1)
parser.add_argument("--normalise", dest = "normalise",  help = "Normalise variable bins", type = int, default = 0)
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
applySF = args.applySF
standardBins = args.standardBins
varBins = args.varBins
normalise = args.normalise
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
ppsDir = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/8025_mAODv2_v7/80X_postProcessing_v1/analysisHephy_13TeV_2016_v2_3/step1"
mc_path     = ppsDir + "/RunIISummer16MiniAODv2_v7"
signal_path = ppsDir + "/RunIISummer16MiniAODv2_v7"
data_path   = ppsDir + "/Data2016_v7"

cmgPP = cmgTuplesPostProcessed(mc_path, signal_path, data_path)

samples = getSamples(cmgPP = cmgPP, skim = 'preSF', sampleList = ['tt_1l'], scan = False, useHT = False, getData = 0)

analysis = "SUS-17-001" #"SUS-16-037"

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/efficiencies/%s"%(tag, analysis)

   suffix = '_' + lep

   if applySF:
      savedir += "/leptonSFapplied"
   else:
      savedir += "/noLeptonSFapplied"

   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

ROOT.gStyle.SetOptStat(0)

# Cuts and Weights
cuts_weights = CutsWeights(samples, cutWeightOptions)

lepTag = cuts_weights.cuts.settings['lepTag'] # cutWeightOptions['settings']['lepTag']
index  = cuts_weights.cuts.vars_dict_format['lepIndex1']
presel = cuts_weights.cuts_weights['presel']['tt_1l'][0]
weight = cuts_weights.cuts_weights['presel']['tt_1l'][1]

#Variable to plot
variables = {\
   'pt':"GenPart_pt",
   'eta':"abs(GenPart_eta)",
}

if lep == 'el':   etaAcc = 2.5 #eta acceptance
elif lep == 'mu': etaAcc = 2.4

#Generated electron selection
genSelRaw = "(abs(GenPart_pdgId) == {pdgId} && abs(GenPart_motherId) == 24 && GenPart_isPromptHard && abs(GenPart_eta) < {etaAcc})".format(pdgId = pdgId, etaAcc = str(etaAcc))
genSel = "Sum$(%s) == 1"%genSelRaw

#Recostructed electron selection
recoSel = {}
recoSel['SUS-17-001'] = "(Sum$(abs(LepGood_pdgId) == {pdgId} && LepGood_mcMatchId != 0 && LepGood_mcMatchId != -99 && LepGood_mcMatchId != 100 && LepGood_mediumMuonId && LepGood_relIso03 < 0.12 && abs(LepGood_dxy) < 0.05 && abs(LepGood_dz) < 0.1) > 0)".format(pdgId = pdgId)
recoSel['SUS-16-037'] = "(Sum$(abs(LepGood_pdgId) == {pdgId} && LepGood_mcMatchId != 0 && LepGood_mcMatchId != -99 && LepGood_mcMatchId != 100 && LepGood_mediumMuonId && LepGood_miniRelIso < 0.2 && abs(LepGood_dxy) < 0.2 && abs(LepGood_dz) < 0.5) > 0)".format(pdgId = pdgId)
#recoSel = "(nLepGood_{}_{lt} >= 1 && (LepGood_mcMatchId[{ind}] != 0 && LepGood_mcMatchId[{ind}] != -99 && LepGood_mcMatchId[{ind}] != 100))".format(lep, lt = lepTag, ind = index)

#deltaR = "sqrt((GenPart_eta[0] - LepGood_eta)^2 + (GenPart_phi[0] - LepGood_phi)^2)"
#matchSel = "(" + deltaR +"*(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mcMatchId != 0) <" + str(deltaRcut) +\
#"&& (" + deltaR +"*(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mcMatchId != 0)) != 0)"

selList = {}
selection = {}

selList['den'] = ["1", genSel] 
selList['num'] = [genSel, recoSel[analysis]] 

plotVars = {'pt':{}, 'eta':{}}
plotVars['pt']['den'] =   varSel(variables['pt'],  genSelRaw)
plotVars['eta']['den'] =  varSel(variables['eta'], genSelRaw)
plotVars['pt']['num'] =   varSel(variables['pt'],  genSelRaw)
plotVars['eta']['num'] =  varSel(variables['eta'], genSelRaw)

selection['den'] = "%s*(%s)"%(weight, combineCutsList(selList['den']))
if applySF:
   weight += "*(LepGood_sftot[%s])"%index
selection['num'] = "%s*(%s)"%(weight, combineCutsList(selList['num']))

hists = {'Gen':{}, 'Reco':{}}
eff = {}

# Binning
def getBinning(lep, varBins = False, standardBins = False, xmax = 200):
   if lep == 'el':   etaAcc = 2.5 #eta acceptance
   elif lep == 'mu': etaAcc = 2.4

   bins = {}
   if not varBins:
      if standardBins:
         bins = {'pt':[20, 0, xmax], 'eta':[int(etaAcc*10), 0, etaAcc]}
      else:
         bins = {'pt':[int(xmax/10), 0, xmax], 'eta':[int(etaAcc*10), 0, etaAcc], 'mt':[int(xmax/10), 0, xmax]}
   else: # variable bin size
      if standardBins:
         bins = {'pt': range(0,50,10) + range(50,200+150,150)}
      else:
         bins['pt'] = [0, 20, 25, 30, 40, 50, xmax]
         #bins['pt'] = [0, 3.5, 5, 10, 15, 20, xmax]
         #bins['pt'] = [0, 3.5, 5, 12, 20, 30, xmax+5]

      if lep == 'mu':
         bins['eta'] = [0, 0.9, 1.2, 2.1, 2.4]
      elif lep == 'el':
         bins['eta'] = [0, 0.8, 1.4442, 1.556, 2, 2.5]
         #bins['eta'] = [0, 1.4442, 1.556, 2.5]
      else:
         bins['eta'] = [0, 1.5, etaAcc]

   return bins

bins = getBinning(lep, varBins = varBins, standardBins = standardBins, xmax = 200)

tree = samples['tt_1l'].tree

##################################################################################Canvas 1#############################################################################################
c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,2)

c1.cd(1)

#Efficiency
if not varBins: 
   hists['Gen']['pt'] = makeHist(tree, plotVars['pt']['den'], selection['den'], bins['pt'][0], bins['pt'][1], bins['pt'][2], addOverFlowBin = 'upper')
   hists['Gen']['pt'].GetYaxis().SetTitle("Events")
else: 
   hists['Gen']['pt'] = makeHistVarBins(tree, plotVars['pt']['den'], selection['den'], bins['pt'],  variableBinning = (varBins, bins['pt'][1]-bins['pt'][0]), addOverFlowBin = 'upper')
   if standardBins: hists['Gen']['pt'].GetYaxis().SetTitle("Events / 10 GeV")
   else: hists['Gen']['pt'].GetYaxis().SetTitle("Events / 5 GeV")
hists['Gen']['pt'].SetName("Gen_%s_pt"%lep)
hists['Gen']['pt'].SetTitle("%ss: Gen vs Reco comparison for tt Sample"%lepton)
hists['Gen']['pt'].GetXaxis().SetTitle("%s p_{T} / GeV"%(lepton))
hists['Gen']['pt'].SetFillColor(ROOT.kViolet+10)
hists['Gen']['pt'].SetMinimum(1)
hists['Gen']['pt'].SetMaximum(1000)
hists['Gen']['pt'].Draw("hist")

#alignStats(hists['Gen']['pt'])

if not varBins: 
   hists['Reco']['pt'] = makeHist(tree, plotVars['pt']['num'], selection['num'], bins['pt'][0], bins['pt'][1], bins['pt'][2], addOverFlowBin = 'upper')
else: 
   hists['Reco']['pt'] = makeHistVarBins(tree, plotVars['pt']['num'], selection['num'], bins['pt'],  variableBinning = (varBins, bins['pt'][1]-bins['pt'][0]), addOverFlowBin = 'upper')
hists['Reco']['pt'].SetName("Reco_%s_pt"%lep)
hists['Reco']['pt'].SetFillColor(ROOT.kRed+1)
hists['Reco']['pt'].SetFillColorAlpha(hists['Reco']['pt'].GetFillColor(), 0.8)
hists['Reco']['pt'].Draw("histsame")
 
if logy: ROOT.gPad.SetLogy()

ROOT.gPad.Modified()
ROOT.gPad.Update()

l1 = makeLegend2()
l1 = ROOT.TLegend()
l1.AddEntry("Gen_pt", "Gen", "F")
l1.AddEntry("Reco_pt", "Reco", "F")
l1.Draw()

alignLegend(l1, y1=0.5, y2=0.65)

##################################################################################################################################################################################
#Efficiency curves
c1.cd(2)

#Efficiency
eff['pt'] = divideHists(hists['Reco']['pt'], hists['Gen']['pt'])
eff['pt'].SetName("eff_%s_pt"%lep)
eff['pt'].Draw("P")
eff['pt'].SetTitle("%ss: Gen vs Reco Efficiency for tt Sample ; %s p_{T} / GeV ; Efficiency"%(lepton, lepton))
#setupEffPlot2(eff['pt'])

eff['pt'].SetMinimum(0.5)
eff['pt'].SetMaximum(1.1)

#eff['pt'].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)

#Colours
eff['pt'].SetMarkerColor(ROOT.kGreen+3)

ROOT.gPad.Modified()
ROOT.gPad.Update()

#l2 = makeLegend2()
#l2.AddEntry("eff_pt", "Veto", "P")
#l2.Draw()

c1.Modified()
c1.Update()

##################################################################################Canvas 2#############################################################################################
c2 = ROOT.TCanvas("c2", "Canvas 2", 1800, 1500)
c2.Divide(1,2)

c2.cd(1)

if not varBins: 
   hists['Gen']['eta'] = makeHist(tree, plotVars['eta']['den'], selection['den'], bins['eta'][0], bins['eta'][1], bins['eta'][2])
   hists['Gen']['eta'].GetYaxis().SetTitle("Events")
else: 
   hists['Gen']['eta'] = makeHistVarBins(tree, plotVars['eta']['den'], selection['den'], bins['eta'],  variableBinning = (varBins, bins['eta'][1]-bins['eta'][0]), addOverFlowBin = 'upper')
   hists['Gen']['eta'].GetYaxis().SetTitle("Events / 0.1 rad")
hists['Gen']['eta'].SetName("Gen_%s_eta"%lep)
hists['Gen']['eta'].SetTitle("%ss: Gen vs Reco comparison for tt Sample"%lepton)
hists['Gen']['eta'].GetXaxis().SetTitle("%s |#eta| "%(lepton))
hists['Gen']['eta'].SetFillColor(ROOT.kViolet+10)
hists['Gen']['eta'].SetMinimum(1)
hists['Gen']['eta'].SetMaximum(1000)
hists['Gen']['eta'].Draw("hist")

#alignStats(hists['Gen']['eta'])#, y1=0.4, y2=0.6)

if not varBins: 
   hists['Reco']['eta'] = makeHist(tree, plotVars['eta']['num'], selection['num'], bins['eta'][0], bins['eta'][1], bins['eta'][2])
else: 
   hists['Reco']['eta'] = makeHistVarBins(tree, plotVars['eta']['num'], selection['num'], bins['eta'],  variableBinning = (varBins, bins['eta'][1]-bins['eta'][0]), addOverFlowBin = 'upper')
hists['Reco']['eta'].SetName("Reco_%s_eta"%lep)
hists['Reco']['eta'].SetFillColor(ROOT.kRed+1)
hists['Reco']['eta'].SetFillColorAlpha(hists['Reco']['eta'].GetFillColor(), 0.8)
hists['Reco']['eta'].Draw("histsame")
   
if logy: ROOT.gPad.SetLogy()

ROOT.gPad.Modified()
ROOT.gPad.Update()

l2 = ROOT.TLegend()
l2.AddEntry("Gen_eta", "Gen", "F")
l2.AddEntry("Reco_eta", "Reco", "F")
l2.Draw()

alignLegend(l2, y1=0.5, y2=0.65)

##################################################################################################################################################################################
#Efficiency curves
c2.cd(2)

#Efficiency
eff['eta'] = divideHists(hists['Reco']['eta'], hists['Gen']['eta'])
eff['eta'].SetName("eff_%s_eta"%lep)
eff['eta'].Draw("P")
eff['eta'].SetTitle("%ss: Gen vs Reco Efficiency for tt Sample ; %s |#eta| ; Efficiency"%(lepton, lepton))
#setupEffPlot2(eff['eta'])

eff['eta'].SetMinimum(0.5)
eff['eta'].SetMaximum(1.1)

#Colours
eff['eta'].SetMarkerColor(ROOT.kGreen+3)

ROOT.gPad.Modified()
ROOT.gPad.Update()

#l2 = makeLegend2()
#l2.AddEntry("eff_eta", "Veto", "P")
#l2.Draw()
c2.Modified()
c2.Update()

#2D Histograms (wrt. pT)
if not varBins:
   hists['Gen']['2D'] = make2DHist(tree, plotVars['pt']['den'], plotVars['eta']['den'], selection['den'], bins['pt'][0], bins['pt'][1], bins['pt'][2], bins['eta'][0], bins['eta'][1], bins['eta'][2])
else:
   hists['Gen']['2D'] = make2DHistVarBins(tree, plotVars['pt']['den'], plotVars['eta']['den'], selection['den'], bins['pt'], bins['eta'])
    #hists[plotType][WP]['2D'][samp].GetYaxis().SetTitle("Events / 5 GeV")
hists['Gen']['2D'].SetName("Gen_%s_2D"%lep)
hists['Gen']['2D'].SetTitle("%s p_{T} vs |#eta| Distribution in Gen tt Sample"%(lepton))
hists['Gen']['2D'].GetXaxis().SetTitle("%s p_{T}"%lepton)
hists['Gen']['2D'].GetYaxis().SetTitle("%s |#eta|"%lepton)
#hist.GetZaxis().SetRangeUser(0, 4)
#alignStats(hist)

#2D Histograms (wrt. pT)
if not varBins:
   hists['Reco']['2D'] = make2DHist(tree, plotVars['pt']['num'], plotVars['eta']['num'], selection['num'], bins['pt'][0], bins['pt'][1], bins['pt'][2], bins['eta'][0], bins['eta'][1], bins['eta'][2])
else:
   hists['Reco']['2D'] = make2DHistVarBins(tree, plotVars['pt']['num'], plotVars['eta']['num'], selection['num'], bins['pt'], bins['eta'])
hists['Reco']['2D'].SetName("Reco_%s_2D"%lep)
hists['Reco']['2D'].SetTitle("%s p_{T} vs |#eta| Distribution in Reco tt Sample"%(lepton))
hists['Reco']['2D'].GetXaxis().SetTitle("%s p_{T}"%lepton)
hists['Reco']['2D'].GetYaxis().SetTitle("%s |#eta|"%lepton)

eff['2D'] = divideHists(hists['Reco']['2D'], hists['Gen']['2D'])
eff['2D'].SetName("eff_%s_2D"%lep)
eff['2D'].SetTitle("%ss: Gen vs Reco Efficiency for tt Sample"%lepton)
eff['2D'].GetXaxis().SetTitle("%s p_{T}"%lepton)
eff['2D'].GetYaxis().SetTitle("%s |#eta|"%lepton)
eff['2D'].SetMarkerSize(1.5)
#eff['2D'].SetMinimum(0.8)
#eff['2D'].SetMaximum(5)
eff['2D'].GetZaxis().SetRangeUser(0.5,1)

c4 = ROOT.TCanvas("c4", "Canvas 4", 1800, 1500)
eff['2D'].Draw("COLZ TEXT89") #CONT1-5 #plots the graph with axes and points
#alignStats(eff['2D'])

#if logy: ROOT.gPad.SetLogz()
c4.Modified()
c4.Update()

c3 = ROOT.TCanvas("c3", "Canvas 3", 1800, 1500)
c3.Divide(1,2)

c3.cd(1)
hists['Reco']['2D'].Draw("COLZ") #CONT1-5 #plots the graph with axes and points
if logy: ROOT.gPad.SetLogz()

c3.cd(2)
hists['Gen']['2D'].Draw("COLZ") #CONT1-5 #plots the graph with axes and points
if logy: ROOT.gPad.SetLogz()
c3.Modified()
c3.Update()

# Nice plot
nicePlot = ROOT.TH2D("eff_%s"%lep, "eff_%s"%lep, 5, 0, 50, 4, 0, 40)
nicePlot.SetTitle("Efficiency")
nicePlot.GetXaxis().SetTitle("%s p_{T} (GeV)"%lepton)
nicePlot.GetYaxis().SetTitle("|#eta|")
nicePlot.GetZaxis().SetTitle("Efficiency")
nicePlot.GetXaxis().SetTitleOffset(1.2)
nicePlot.GetYaxis().SetTitleOffset(1.2)
nicePlot.GetZaxis().SetTitleOffset(1.2)
nicePlot.GetZaxis().SetRangeUser(0,1)
nicePlot.SetMarkerSize(1.5)

n = eff['2D'].GetNbinsX()

if lep == 'el':   z = 1 # to omit ECAL gap bin
elif lep == 'mu': z = 0

binLabels = {\
   'mu':
   {'pt':{1:'20-25',2:'25-30', 3:'30-40', 4:'40-50', 5:'50-200'},
   'eta':{1:'0-0.9',2:'0.9-1.2', 3:'1.2-2.1', 4:'2.1-2.4'}},
   'el':
   {'pt':{1:'20-25',2:'25-30', 3:'30-40', 4:'40-50', 5:'50-200'},
   'eta':{1:'0-0.8',2:'0.8-1.4442', 3:'1.556-2', 4:'2-2.5'}}}

for i in range(n-1):
   i += 1

   nicePlot.SetBinContent(i, 1, eff['2D'].GetBinContent(i+1,1))
   nicePlot.SetBinError(i,   1, eff['2D'].GetBinError(i+1,1))

   nicePlot.SetBinContent(i, 2, eff['2D'].GetBinContent(i+1,2))
   nicePlot.SetBinError(i,   2, eff['2D'].GetBinError(i+1,2))

   nicePlot.SetBinContent(i, 3, eff['2D'].GetBinContent(i+1,3+z))
   nicePlot.SetBinError(i,   3, eff['2D'].GetBinError(i+1,3+z))

   nicePlot.SetBinContent(i, 4, eff['2D'].GetBinContent(i+1,4+z))
   nicePlot.SetBinError(i,   4, eff['2D'].GetBinError(i+1,4+z))

   nicePlot.GetXaxis().SetBinLabel(i, binLabels[lep]['pt'][i])

for j in range(1,5):
   nicePlot.GetYaxis().SetBinLabel(j, binLabels[lep]['eta'][j])

c5 = ROOT.TCanvas("c5", "Canvas 5", 1800, 1500)
ROOT.gStyle.SetPalette(1)
nicePlot.Draw("COLZ TEXTE") #CONT1-5 #plots the graph with axes and points
#alignStats(eff['2D'])

#if logy: ROOT.gPad.SetLogz()
c5.Modified()
c5.Update()

#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   c1.SaveAs("%s/lepEff%s_lepPt.png"%(savedir, suffix))
   c1.SaveAs("%s/pdf/lepEff%s_lepPt.pdf"%(savedir, suffix))
   c1.SaveAs("%s/root/lepEff%s_lepPt.root"%(savedir, suffix))
   
   c2.SaveAs("%s/lepEff%s_lepEta.png"%(savedir, suffix))
   c2.SaveAs("%s/pdf/lepEff%s_lepEta.pdf"%(savedir, suffix))
   c2.SaveAs("%s/root/lepEff%s_lepEta.root"%(savedir, suffix))
   
   c3.SaveAs("%s/lepEff%s_2D_distributions.png"%(savedir, suffix))
   c3.SaveAs("%s/pdf/lepEff%s_2D_distributions.pdf"%(savedir, suffix))
   c3.SaveAs("%s/root/lepEff%s_2D_distributions.root"%(savedir, suffix))
   
   c4.SaveAs("%s/lepEff%s_2D.png"%(savedir, suffix))
   c4.SaveAs("%s/pdf/lepEff%s_2D.pdf"%(savedir, suffix))
   c4.SaveAs("%s/root/lepEff%s_2D.root"%(savedir, suffix))
   
   c5.SaveAs("%s/lepEff%s.png"%(savedir, suffix))
   c5.SaveAs("%s/pdf/lepEff%s.pdf"%(savedir, suffix))
   c5.SaveAs("%s/root/lepEff%s.root"%(savedir, suffix))
