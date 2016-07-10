# distributions.py
# Script to calculate the 2D distributions of electron ID variables and electron pT, as well slices between a given pT range.
# Author: Mateusz Zarucki

import ROOT
import os, sys
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.cmgTuplesPostProcessed_mAODv2_analysisHephy13TeV import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_mAODv2_analysisHephy13TeV import getSamples
#from Workspace.DegenerateStopAnalysis.toolsMateusz.cmgTuplesPostProcessed_mAODv2 import cmgTuplesPostProcessed
#from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_PP_mAODv2_7412pass2_scan import getSamples
from array import array
from math import pi, sqrt #cos, sin, sinh, log
import argparse

#Samples
privateSignals = ["s10FS", "s30", "s30FS", "s60FS", "t2tt30FS"]
backgrounds=["w","tt", "z","qcd"]

cmgPP = cmgTuplesPostProcessed()

samplesList = backgrounds # + privateSignals
samples = getSamples(cmgPP=cmgPP, sampleList=samplesList, scan=True, useHT=True, getData=False)

officialSignals = ["s300_290", "s300_270", "s300_240"] #FIXME: crosscheck if these are in allOfficialSignals

allOfficialSignals = samples.massScanList()
#allOfficialSignals = [s for s in samples if samples[s]['isSignal'] and not samples[s]['isData'] and s not in privateSignals and s not in backgrounds] 
allSignals = privateSignals + allOfficialSignals
allSamples = allSignals + backgrounds

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--var", dest="var",  help="Electron ID Variable", type=str, default="sigmaEtaEta") #"sigmaEtaEta" "hOverE" "ooEmooP" "dPhi" "dEta" "d0" "dz" "MissingHits" "convVeto"
parser.add_argument("--slice", dest="slice",  help="Pt Slice Bounds (low,up)", type=int, nargs=2, metavar = ('slice_low', 'slice_up'))
parser.add_argument("--sample", dest="sample",  help="Sample", type=str, default="s300_270")
parser.add_argument("--presel", dest="presel",  help="Add Preselection", type=int, default=1) # applies preselection
parser.add_argument("--save", dest="save",  help="Toggle Save", type=int, default=1)
parser.add_argument("-b", dest="batch",  help="Batch Mode", action="store_true", default=False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
var = args.var
sample = args.sample 
presel = args.presel
slice = args.slice
save = args.save

variables = {'sigmaEtaEta':"sigmaIEtaIEta",'hOverE':"hadronicOverEm",'ooEmooP':"eInvMinusPInv",'dPhi':"dPhiScTrkIn",'dEta':"dEtaScTrkIn",'d0':"dxy",'dz':"dz",'MissingHits':"lostHits",'convVeto':"convVeto"} # Variable counterparts in tuples

if var not in variables.keys(): 
   print makeLine()
   print "!!! Wrong variable input."
   print makeLine()
   sys.exit(0)

print makeLine()
print "Samples:"
newLine()
for s in sorted(samples.keys()):
   print samples[s].name,":",s
print makeLine()
if sample in samples.keys(): print "Using", samples[sample].name, "sample."
else:
   print "!!! Sample " + sample + " unavailable."
   sys.exit(0)
print makeLine()

#Geometric divisions
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap
etaAcc = 2.5 #eta acceptance

#Pt division for MVA ID
ptSplit = 10 #we have above and below 10 GeV categories 

#DeltaR cut for matching
deltaRcut = 0.3

#Selection criteria
#intLum = 10.0 #fb-1
weight = samples[sample].weight

#Preselection
preSel1 = "(met_pt > 200)" #MET
preSel2 = "(Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 4.5 && Jet_id)) > 200)" #HT = Sum of Jets > 30GeV
preSel3 = "(Max$(Jet_pt*(abs(Jet_eta) < " + str(etaAcc) + ") > 100))" #ISR

if presel: preSel = preSel1 + "&&" + preSel2 + "&&" + preSel3
else: preSel = "1"

WPcuts = {\
'Veto':{'sigmaEtaEta':{'EB':0.0114, 'EE':0.0352}, 'dEta':{'EB':0.0152, 'EE':0.0113}, 'dPhi':{'EB':0.216, 'EE':0.237}, 'hOverE':{'EB':0.181, 'EE':0.116}, 'ooEmooP':{'EB':0.207, 'EE':0.174},\
'd0':{'EB':0.0564, 'EE':0.222}, 'dz':{'EB':0.472, 'EE':0.921}, 'MissingHits':{'EB':2, 'EE':3}, 'convVeto':{'EB':1, 'EE':1}, 'relIso' : {'EB':0.126, 'EE':0.144}},
'Loose':{'sigmaEtaEta':{'EB':0.0103, 'EE':0.0301}, 'dEta':{'EB':0.0105, 'EE':0.00814}, 'dPhi':{'EB':0.115, 'EE':0.182}, 'hOverE':{'EB':0.104, 'EE':0.0897}, 'ooEmooP':{'EB':0.102, 'EE':0.126},\
'd0':{'EB':0.0261, 'EE':0.118}, 'dz':{'EB':0.41, 'EE':0.822}, 'MissingHits':{'EB':2, 'EE':1}, 'convVeto':{'EB':1, 'EE':1}, 'relIso' : {'EB':0.0893, 'EE':0.121}},
'Medium':{'sigmaEtaEta':{'EB':0.0101, 'EE':0.0283}, 'dEta':{'EB':0.0103, 'EE':0.00733}, 'dPhi':{'EB':0.0336, 'EE':0.114}, 'hOverE':{'EB':0.0876, 'EE':0.0678}, 'ooEmooP':{'EB':0.0174, 'EE':0.0898},\
'd0':{'EB':0.0118, 'EE':0.0739}, 'dz':{'EB':0.373, 'EE':0.602}, 'MissingHits':{'EB':2, 'EE':1}, 'convVeto':{'EB':1, 'EE':1}, 'relIso' : {'EB':0.0766, 'EE':0.0678}},
'Tight':{'sigmaEtaEta':{'EB':0.0101, 'EE':0.0279}, 'dEta':{'EB':0.00926, 'EE':0.00724}, 'dPhi':{'EB':0.0336, 'EE':0.0918}, 'hOverE':{'EB':0.0597, 'EE':0.0615}, 'ooEmooP':{'EB':0.012, 'EE':0.00999},\
'd0':{'EB':0.0111, 'EE':0.0351}, 'dz':{'EB':0.0466, 'EE':0.417}, 'MissingHits':{'EB':2, 'EE':1}, 'convVeto':{'EB':1, 'EE':1}, 'relIso' : {'EB':0.0354, 'EE':0.0646}}}

#Bin size 
nbins = 60
xmin = {'0':0, 'Pt':5}
if var in ['dEta', 'dPhi', 'ooEmooP', 'd0', 'dz']:
   xmin['EB'] = -WPcuts['Veto'][var]['EB']*1.75
   xmin['EE'] = -WPcuts['Veto'][var]['EE']*1.75
else:
   xmin['EB'] = xmin['EE'] = 0

xmax = {'Pt':30, 'EB':WPcuts['Veto'][var]['EB']*1.75, 'EE':WPcuts['Veto'][var]['EE']*1.75}

#single-lepton (semileptonic) events
#if nEles == "01":
#Generated electron selection
nSel = "ngenLep == 1" #removes dileptonic events
genSel1 = "(abs(genLep_pdgId[0]) == 11 && abs(genLep_eta[0]) < " + str(etaAcc) + ")" #electron selection #index [0] ok since (only element)
genSel = nSel + "&&" + genSel1

#Reconstructed electron selection
deltaR = "sqrt((genLep_eta[0] - LepGood_eta)^2 + (genLep_phi[0] - LepGood_phi)^2)"
matchSel = "(" + deltaR +"*(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mcMatchId != 0) <" + str(deltaRcut) +\
"&& (" + deltaR +"*(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mcMatchId != 0)) != 0)"

##single-electron events (semileptonic & dileptonic)
#elif nEles == "1":
#   #Generated electron selection
#   nSel = "ngenLep > 0" #redundant with genSel2 #nLepGood > 0 introduces bias
#   genSel1 = "(abs(genLep_pdgId) == 11 && abs(genLep_eta) < " + str(etaAcc) + ")" #electron selection (includes dielectron evts) #ngenLep == 1 would remove dileptonic events # index [0] does not include single-electron events with muon 
#   genSel2 = "(Sum$(abs(genLep_pdgId) == 11 && abs(genLep_eta) < " + str(etaAcc) + ") == 1)" # = number of electrons (includes dileptonic and semileptonic events) 
#   genSel = nSel + "&&" + genSel1 + "&&" + genSel2
#
#elif nEles == "2":
#   nSel = "ngenLep == 2" #does not include single-lepton events 
#   genSel1 = "(abs(genLep_pdgId) == 11 && abs(genLep_eta) < " + str(etaAcc) + ")" #electron selection (includes dielectron evts) #ngenLep == 1 would remove dileptonic events
#   genSel2 = "(Sum$(abs(genLep_pdgId) == 11 && abs(genLep_eta) < " + str(etaAcc) + ") == 2)" # = number of electrons (includes dilepton events only) 
#   genSel = nSel + "&&" + genSel1 + "&&" + genSel2

##################################################################################Canvas 1############################################################################################
c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,2)

#IDs: 0 - none, 1 - veto (~95% eff), 2 - loose (~90% eff), 3 - medium (~80% eff), 4 - tight (~70% eff)
WPs = ['Veto', 'Loose', 'Medium', 'Tight']

#cutSel = {}
#recoSel = "(abs(LepGood_pdgId) == 11)"
#misMatchSel = "(LepGood_mcMatchId == 0)"

geoSel= {'EB':"(abs(LepGood_eta) <= " + str(ebeeSplit) + ")", 'EE':"(abs(LepGood_eta) > " + str(ebeeSplit) + "&& abs(LepGood_eta) < " + str(etaAcc) + ")"}

hists = {}
hlines = {'Veto':{var:{}}, 'Loose':{var:{}}, 'Medium':{var:{}}, 'Tight':{var:{}}}
hlines2 = {'Veto':{var:{}}, 'Loose':{var:{}}, 'Medium':{var:{}}, 'Tight':{var:{}}}

#2D Histograms (wrt. pT)
for i,reg in enumerate(geoSel.keys()):
   c1.cd(i+1)
   hists["2D_" + var + "_" + reg] = make2DHist(samples[sample].tree, "LepGood_pt", "LepGood_" + variables[var], weight + "*(" + preSel + "&&" + genSel + "&&" + matchSel + "&&" + geoSel[reg] + ")", nbins, xmin['Pt'], xmax['Pt'], nbins, xmin[reg], xmax[reg])
   hists["2D_" + var + "_" + reg].SetName("2D_" + var + "_" + reg)
   hists["2D_" + var + "_" + reg].SetTitle(var + " and Electron p_{T} Distribution (" + reg + ")")
   hists["2D_" + var + "_" + reg].GetXaxis().SetTitle("Reconstructed Electron p_{T}")
   hists["2D_" + var + "_" + reg].GetYaxis().SetTitle(var)
   hists["2D_" + var + "_" + reg].Draw("COLZ") #CONT1-5 #plots the graph with axes and points
   hists["2D_" + var + "_" + reg].GetZaxis().SetRangeUser(0, 4)
    
   alignStats(hists["2D_" + var + "_" + reg])
   
   for iWP in WPs:
      hlines[iWP][var][reg] = ROOT.TLine(xmin['Pt'], WPcuts[iWP][var][reg], xmax['Pt'], WPcuts[iWP][var][reg])
      hlines[iWP][var][reg].SetLineWidth(3)
      if var in ['dEta', 'dPhi', 'ooEmooP', 'd0', 'dz']:
         hlines2[iWP][var][reg] = ROOT.TLine(xmin['Pt'], -WPcuts[iWP][var][reg], xmax['Pt'], -WPcuts[iWP][var][reg])
         hlines2[iWP][var][reg].SetLineWidth(3)
 
   hlines['Veto'][var][reg].SetLineColor(ROOT.kGreen+3)
   hlines['Loose'][var][reg].SetLineColor(ROOT.kBlue+1)
   hlines['Medium'][var][reg].SetLineColor(ROOT.kOrange-2)
   hlines['Tight'][var][reg].SetLineColor(ROOT.kRed+1)
  
   if var in ['dEta', 'dPhi', 'ooEmooP', 'd0', 'dz']:
      hlines2['Veto'][var][reg].SetLineColor(ROOT.kGreen+3)
      hlines2['Loose'][var][reg].SetLineColor(ROOT.kBlue+1)
      hlines2['Medium'][var][reg].SetLineColor(ROOT.kOrange-2)
      hlines2['Tight'][var][reg].SetLineColor(ROOT.kRed+1)

   for iWP in WPs:
      hlines[iWP][var][reg].Draw()
      if var in ['dEta', 'dPhi', 'ooEmooP', 'd0', 'dz']:
         hlines2[iWP][var][reg].Draw()
   
   if i == 0: 
      l1 = makeLegend2()
      l1.AddEntry(hlines['Veto'][var][reg], "Veto ID", "l")
      l1.AddEntry(hlines['Loose'][var][reg], "Loose ID", "l")
      l1.AddEntry(hlines['Medium'][var][reg], "Medium ID", "l")
      l1.AddEntry(hlines['Tight'][var][reg], "Tight ID", "l")
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()

   l1.Draw()
   
c1.Modified()
c1.Update()
   
##################################################################################Canvas 2#############################################################################################
c2 = ROOT.TCanvas("c2", "Canvas 2", 1800, 1500)
c2.Divide(1,2)

#l2 = ROOT.TLegend(l1) #l1.Copy(l2)

vlines = {'Veto':{var:{}}, 'Loose':{var:{}}, 'Medium':{var:{}}, 'Tight':{var:{}}}
vlines2 = {'Veto':{var:{}}, 'Loose':{var:{}}, 'Medium':{var:{}}, 'Tight':{var:{}}}

if slice is not None:
   ptSel = "(LepGood_pt >" + str(slice[0]) + "&& LepGood_pt <" + str(slice[1]) + ")"
else:
   ptSel = "1"

#1D Histogram
for i,reg in enumerate(geoSel.keys()):
   c2.cd(i+1)
   hists[var + "_" + reg] = makeHist(samples[sample].tree, "LepGood_" + variables[var], weight + "*(" + preSel + "&&" + genSel + "&&" + matchSel + "&&" + geoSel[reg] + "&&" + ptSel + ")", nbins, xmin[reg], xmax[reg])
   hists[var + "_" + reg].SetName(var + "_" + reg)
   if slice is not None: hists[var + "_" + reg].SetTitle(var + " Distribution between " + str(slice[0]) + "-" + str(slice[1]) + " GeV Electron p_{T} (" + reg + " ; " + samples[sample].name + " Sample)")
   else: hists[var + "_" + reg].SetTitle("Total " + var + " Distribution (" + reg + " ; " + samples[sample].name + " Sample)")
   hists[var + "_" + reg].GetXaxis().SetTitle(var)
   hists[var + "_" + reg].Draw("hist")
      
   ROOT.gPad.SetLogy()
   alignStats(hists[var + "_" + reg])
   
   for iWP in WPs:
      vlines[iWP][var][reg] = ROOT.TLine(WPcuts[iWP][var][reg], 0, WPcuts[iWP][var][reg], hists[var + "_" + reg].GetBinContent(hists[var + "_" + reg].GetXaxis().FindBin(WPcuts[iWP][var][reg])))#int(WPcuts[iWP][var][reg]*nbins/xmax[reg])+1))
      vlines[iWP][var][reg].SetLineWidth(3)
      if var in ['dEta', 'dPhi', 'ooEmooP', 'd0', 'dz']:
         vlines2[iWP][var][reg] = ROOT.TLine(-WPcuts[iWP][var][reg], 0, -WPcuts[iWP][var][reg], hists[var + "_" + reg].GetBinContent(hists[var + "_" + reg].GetXaxis().FindBin(WPcuts[iWP][var][reg])))
         vlines2[iWP][var][reg].SetLineWidth(3)

   vlines['Veto'][var][reg].SetLineColor(ROOT.kGreen+3)
   vlines['Loose'][var][reg].SetLineColor(ROOT.kBlue+1)
   vlines['Medium'][var][reg].SetLineColor(ROOT.kOrange-2)
   vlines['Tight'][var][reg].SetLineColor(ROOT.kRed+1)
   
   if var in ['dEta', 'dPhi', 'ooEmooP', 'd0', 'dz']:
      vlines2['Veto'][var][reg].SetLineColor(ROOT.kGreen+3)
      vlines2['Loose'][var][reg].SetLineColor(ROOT.kBlue+1)
      vlines2['Medium'][var][reg].SetLineColor(ROOT.kOrange-2)
      vlines2['Tight'][var][reg].SetLineColor(ROOT.kRed+1)
 
   for iWP in WPs:
      vlines[iWP][var][reg].Draw() 
      if var in ['dEta', 'dPhi', 'ooEmooP', 'd0', 'dz']:
         vlines2[iWP][var][reg].Draw() 
 
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   l1.Draw()
   #alignLegend(l1,0.775,0.875,0.25,0.45)

c2.Modified()
c2.Update()

#Write to file
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronID/nMinus1/distributions/" + var + "/" + samples[sample].name
   
   if not os.path.exists(savedir + "/root"): os.makedirs(savedir + "/root")
   if not os.path.exists(savedir + "/pdf"): os.makedirs(savedir + "/pdf")

   #Save to Web
   if slice is None:
      c1.SaveAs(savedir + "/%s_2D_%s.png"%(var, samples[sample].name))
      c1.SaveAs(savedir + "/root/%s_2D_%s.root"%(var, samples[sample].name))
      c1.SaveAs(savedir + "/pdf/%s_2D_%s.pdf"%(var, samples[sample].name))
   
      c2.SaveAs(savedir + "/%s_total_%s.png"%(var, samples[sample].name))
      c2.SaveAs(savedir + "/root/%s_total_%s.root"%(var, samples[sample].name))
      c2.SaveAs(savedir + "/pdf/%s_total_%s.pdf"%(var, samples[sample].name))
   else:
      c2.SaveAs(savedir + "/%s_slice_%s_%s_%s.png"%(var, str(slice[0]), str(slice[1]), samples[sample].name))
      c2.SaveAs(savedir + "/pdf/%s_slice_%s_%s_%s.pdf"%(var, str(slice[0]), str(slice[1]), samples[sample].name))
      c2.SaveAs(savedir + "/root/%s_slice_%s_%s_%s.root"%(var, str(slice[0]), str(slice[1]), samples[sample].name))
