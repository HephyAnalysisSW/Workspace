# deltaR_ratioPt.py
# Script to plot the deltaR and pT ratio distributions between generated and reconstructed electrons
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
parser.add_argument("--presel", dest="presel",  help="Add Preselection", type=int, default=1) # applies preselection
parser.add_argument("--sample", dest="sample",  help="Sample", type=str, default="s300_270")
parser.add_argument("--mvaWPs", dest="mvaWPs",  help="Add MVA WPs", type=int, default=1) # includes MVA WPs
parser.add_argument("--save", dest="save",  help="Toggle Save", type=int, default=1)
parser.add_argument("-b", dest="batch",  help="Batch Mode", action="store_true", default=False)
#parser.add_argument("--zoom", dest="zoom",  help="Toggle zoom", type=int, default=1)
#parser.add_argument("--id", dest="ID",  help="Electron ID type", type=str, default="standard") # "standard" "noIso" "iso"
#parser.add_argument("--iso", dest="iso",  help="Isolation", type=str, default="relIso03") #"relIso03" "relIso04" "miniRelIso" "relIsoAn04"
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments 
sample = args.sample 
presel = args.presel 
mvaWPs = args.mvaWPs
save = args.save
#zoom = args.zoom
#ID = args.ID 
#if ID == "iso": isolation = args.iso
#nEles = "01" # 01,01tau,1,2 #Number of electrons in event

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

#Bin size 
nbins = 100
xmin = 0
#xmax = 1000

#Selection criteria
#intLum = 10.0 #fb-1
weight = samples[sample].weight

#Preselection
preSel1 = "(met_pt > 200)" #MET
preSel2 = "(Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 4.5 && Jet_id)) > 200)" #HT = Sum of Jets > 30GeV
preSel3 = "(Max$(Jet_pt*(abs(Jet_eta) < " + str(etaAcc) + ") > 100))" #ISR

if presel: preSel = preSel1 + "&&" + preSel2 + "&&" + preSel3
else: preSel = "1"

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

deltaRjet = "Min$(sqrt((LepGood_eta[0] - Jet_eta)^2 + (LepGood_phi[0] - Jet_phi)^2))"

##single-electron events (semileptonic & dileptonic)
#elif nEles == "1":
#   #Generated electron selection
#   nSel = "ngenLep > 0" #redundant with genSel2 #nLepGood > 0 introduces bias
#   genSel1 = "(abs(genLep_pdgId) == 11 && abs(genLep_eta) < " + str(etaAcc) + ")" #electron selection (includes dielectron evts) #ngenLep == 1 would remove dileptonic events # index [0] does not include single-electron events with muon a
#   genSel2 = "(Sum$(abs(genLep_pdgId) == 11 && abs(genLep_eta) < " + str(etaAcc) + ") == 1)" # = number of electrons (includes dileptonic and semileptonic events) 
#   genSel = nSel + "&&" + genSel1 + "&&" + genSel2
#
#elif nEles == "2":
#   nSel = "ngenLep == 2" #does not include single-lepton events 
#   genSel1 = "(abs(genLep_pdgId) == 11 && abs(genLep_eta) < " + str(etaAcc) + ")" #electron selection (includes dielectron evts) #ngenLep == 1 would remove dileptonic events
#   genSel2 = "(Sum$(abs(genLep_pdgId) == 11 && abs(genLep_eta) < " + str(etaAcc) + ") == 2)" # = number of electrons (includes dilepton events only) 
#   genSel = nSel + "&&" + genSel1 + "&&" + genSel2

##################################################################################Canvas 1#############################################################################################
c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,3)

#Electron Cut IDs
hists = {'deltaR':{}, 'ratioPt':{}, 'deltaRjet':{}}

#IDs: 0 - none, 1 - veto (~95% eff), 2 - loose (~90% eff), 3 - medium (~80% eff), 4 - tight (~70% eff)
WPs = ['Veto', 'Loose', 'Medium', 'Tight']

cutSel = {}

for i,iWP in enumerate(WPs):
   cutSel[iWP] = "LepGood_SPRING15_25ns_v1 >= " + str(i+1)

variables = {'deltaR':deltaR, 'ratioPt':"LepGood_pt/genLep_pt", 'deltaRjet':deltaRjet} # 
for i,var in enumerate(variables.items()):
   c1.cd(i+1)
   
   if var[0] == 'deltaR':
      xmax = 0.3
   elif var[0] == 'ratioPt':
      xmax = 3
   elif var[0] == 'deltaRjet':
      xmax = 7
   
   hists[var[0]]['None'] = makeHist(samples[sample].tree, var[1], weight + "*(" + preSel + "&&" + genSel + "&&" + matchSel + ")", nbins, xmin, xmax)
   
   if var[0] == 'deltaR': 
      hists[var[0]]['None'].SetName("DeltaR")
      hists[var[0]]['None'].SetTitle("DeltaR between Generated and Reconstructed Electron Distributions for Various IDs (" + samples[sample].name + " Sample)")
      hists[var[0]]['None'].GetXaxis().SetTitle("dR of GenEle and RecoEle")
   
   if var[0] == 'ratioPt' or var[0] == 'deltaRjet':
      deltaRcut = 0.3
   
      matchSel = "(" + deltaR +"*(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mcMatchId != 0) <" + str(deltaRcut) + "&& (" + deltaR +"*(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mcMatchId != 0)) != 0)"
      
      if var[0] == 'ratioPt':
         hists[var[0]]['None'].SetName("RatioPt")
         hists[var[0]]['None'].SetTitle("Distributions of p_{T} Ratio of Generated and Reconstructed Electrons for Various IDs (" + samples[sample].name + " Sample)")
         hists[var[0]]['None'].GetXaxis().SetTitle("RecoEle p_{T} / GenEle p_{T}")
   
      elif var[0] == 'deltaRjet':
         hists[var[0]]['None'].SetName("DeltaRjet")
         hists[var[0]]['None'].SetTitle("Minimum DeltaR between Electron and Jet Distributions for Various IDs (" + samples[sample].name + " Sample)")
         hists[var[0]]['None'].GetXaxis().SetTitle("Min(dR) of Electron and Jet")
   
   hists[var[0]]['None'].Draw("hist")
   
   for iWP in WPs:
      hists[var[0]][iWP] = makeHist(samples[sample].tree, var[1], weight + "*(" + preSel + "&&" + genSel + "&&" + matchSel + "&&" + cutSel[iWP] + ")", nbins, xmin, xmax)
      hists[var[0]][iWP].SetName(var[0] + "_" + iWP)
      hists[var[0]][iWP].SetFillColor(0)
      hists[var[0]][iWP].Draw("histsame")
   
   ROOT.gPad.SetLogy()
   
   alignStats(hists[var[0]]['None'])
   
   #Colours
   hists[var[0]]['Veto'].SetLineColor(ROOT.kGreen+3)
   hists[var[0]]['Loose'].SetLineColor(ROOT.kBlue+1)
   hists[var[0]]['Medium'].SetLineColor(ROOT.kOrange-2)
   hists[var[0]]['Tight'].SetLineColor(ROOT.kRed+1)
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   if i == 0: 
      l1 = makeLegend2()
      #if var[0] == "deltaR": l1.AddEntry("DeltaR", "DeltaR", "F")
      #elif var[0] == "ratioPt": l1.AddEntry("RatioPt", "RecoEle p_{T} / GenEle p_{T}", "F")
      #elif var[0] == "deltaRjet": l1.AddEntry("DeltaRjet", "Min(dR_ele_jet)", "F")
      l1.AddEntry(var[0] + "_Veto", "Veto ID", "F")
      l1.AddEntry(var[0] + "_Loose", "Loose ID", "F")
      l1.AddEntry(var[0] + "_Medium", "Medium ID", "F")
      l1.AddEntry(var[0] + "_Tight", "Tight ID", "F")
   
   #Electron MVA IDs
   if mvaWPs:
      mvaCuts = {'WP90':\
                {'EB1_lowPt':-0.083313, 'EB2_lowPt':-0.235222, 'EE_lowPt':-0.67099, 'EB1':0.913286, 'EB2':0.805013, 'EE':0.358969},\
                 'WP80':\
                {'EB1_lowPt':0.287435, 'EB2_lowPt':0.221846, 'EE_lowPt':-0.303263, 'EB1':0.967083, 'EB2':0.929117, 'EE':0.726311}}
      
      for iWP in mvaCuts.keys():
         mvaSel = "(\
         (LepGood_pt <= " + str(ptSplit) + " && abs(LepGood_eta) < " + str(ebSplit) + " && LepGood_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EB1_lowPt']) + ") || \
         (LepGood_pt <= " + str(ptSplit) + " && abs(LepGood_eta) >= " + str(ebSplit) + " && abs(LepGood_eta) < " + str(ebeeSplit) + " && LepGood_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EB2_lowPt']) + ") || \
         (LepGood_pt <= " + str(ptSplit) + " && abs(LepGood_eta) >= " + str(ebeeSplit) + " && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EE_lowPt']) + ") || \
         (LepGood_pt > " + str(ptSplit) + " && abs(LepGood_eta) < " + str(ebSplit) + " && LepGood_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EB1']) + ") || \
         (LepGood_pt > " + str(ptSplit) + " && abs(LepGood_eta) >= " + str(ebSplit) + " && abs(LepGood_eta) < " + str(ebeeSplit) + " && LepGood_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EB2']) + ") || \
         (LepGood_pt > " + str(ptSplit) + " && abs(LepGood_eta) >= " + str(ebeeSplit) + " && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EE']) + "))"
         hists[var[0]][iWP] = makeHist(samples[sample].tree, var[1], weight + "*(" + preSel + "&&" + genSel + "&&" + matchSel + "&&" + mvaSel + ")", nbins, xmax, xmin)
         hists[var[0]][iWP].SetName(var[0] + "_" + iWP)
         hists[var[0]][iWP].SetFillColor(0)
         hists[var[0]][iWP].Draw("histsame")
     
      hists[var[0]]['WP90'].SetLineColor(ROOT.kMagenta+2)
      hists[var[0]]['WP80'].SetLineColor(ROOT.kAzure+5)
   
      ROOT.gPad.Modified()
      ROOT.gPad.Update()
      
      if i == 0: 
         l1.AddEntry(var[0] + "_WP90", "MVA ID (WP90)", "F")
         l1.AddEntry(var[0] + "_WP80", "MVA ID (WP80)", "F")
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   l1.Draw()

c1.Modified()
c1.Update()

#Write to file
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronID/efficiencies/standard/deltaR_ratioPt"
   
   if not os.path.exists(savedir + "/root"): os.makedirs(savedir + "/root")
   if not os.path.exists(savedir + "/pdf"): os.makedirs(savedir + "/pdf")

   #Save to Web
   c1.SaveAs(savedir + "/deltaR_ratioPt_%s.png"%(samples[sample].name))
   c1.SaveAs(savedir + "/pdf/deltaR_ratioPt_%s.pdf"%(samples[sample].name))
   c1.SaveAs(savedir + "/root/deltaR_ratioPt_%s.root"%(samples[sample].name))
