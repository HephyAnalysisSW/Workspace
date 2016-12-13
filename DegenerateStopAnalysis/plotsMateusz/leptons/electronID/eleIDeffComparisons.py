# effComparison.py
# Script to produce electron ID efficiency plots with different ID definitions: standard EG Spring 15 (25ns) ID, manually applied cuts, including isolation and with one cut removed (N-1)
# Author: Mateusz Zarucki

import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import makeDir
from Workspace.DegenerateStopAnalysis.tools.getSamples_8012 import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from array import array
from math import pi, sqrt #cos, sin, sinh, log

ROOT.gStyle.SetOptStat(1111) #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--plot", dest="plot",  help="Plot type", type=str, default="efficiency") # "efficiency" "misID" "misID2"
parser.add_argument("--id", dest="ID",  help="Electron ID type", type=str, default="standard") # "standard" "manual" "iso"
parser.add_argument("--removedCut", dest="removedCut",  help="Variable removed from electron ID", type=str, default="") #"sigmaEtaEta" "dEta" "dPhi" "hOverE" "ooEmooP" "d0" "dz" "MissingHits" "convVeto"
parser.add_argument("--iso", dest="iso",  help="Isolation", type=str, default="relIso03") #"relIso03" "relIso04" "miniRelIso" "relIsoAn04"
#parser.add_argument("--mvaWPs", dest="mvaWPs",  help="Add MVA WPs", type=int, default=0) # includes MVA WPs
parser.add_argument("--presel", dest="presel",  help="Add preselection", type=int, default=1) # applies preselection
#parser.add_argument("--lowPt", dest="lowPt",  help="Low electron pt selection", type=int, default=0)
parser.add_argument("--sample", dest="sample",  help="Sample", type=str, default="qcd")
parser.add_argument("--save", dest="save",  help="Toggle save", type=int, default=1)
#parser.add_argument("--zoom", dest="zoom",  help="Toggle zoom", type=int, default=1)
parser.add_argument("-b", dest="batch",  help="Batch mode", action="store_true", default=False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
plot = args.plot 
ID = args.ID 
removedCut = args.removedCut 
#mvaWPs = args.mvaWPs
presel = args.presel
#lowPt = args.lowPt 
sample = args.sample 
#zoom = args.zoom
save = args.save
iso = args.iso
#nEles = "01" # 01,01tau,1,2 #Number of electrons in event

#Samples
privateSignals = ["s10FS", "s30", "s30FS", "s60FS", "t2tt30FS"]
backgrounds=["w","tt", "z","qcd"]

samplesList = backgrounds # + privateSignals

cmgPP = cmgTuplesPostProcessed()
samples = getSamples(cmgPP = cmgPP, skim = 'preIncLep', sampleList = samplesList, scan = False, useHT = True, getData = False)

officialSignals = ["s300_290", "s300_270", "s300_240"] #FIXME: crosscheck if these are in allOfficialSignals

allOfficialSignals = samples.massScanList()
#allOfficialSignals = [s for s in samples if samples[s]['isSignal'] and not samples[s]['isData'] and s not in privateSignals and s not in backgrounds] 
allSignals = privateSignals + allOfficialSignals
allSamples = allSignals + backgrounds

print makeLine()
print "Samples:"
newLine()
for s in sorted(samples.keys()): print samples[s].name,":",s
print makeLine()
if sample in samples.keys(): print "Using", samples[sample].name, "sample."
else: 
   print "!!! Sample " + sample + " unavailable."
   sys.exit(0)
print makeLine()

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/electronID/effComparison"%tag
 
   #Save path
   if not removedCut:
      savedir += "/" + plot
      
   makeDir(savedir + "/root/histograms")
   makeDir(savedir + "/pdf")

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
#weight = "(xsec*" + str(intLum) + "*(10^3)/" + str(getChunks(sample)[1]) + ")" #xsec in pb
weight = samples[sample].weight

#Preselection
preSel1 = "(met_pt > 200)" #MET
preSel2 = "(Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 4.5 && Jet_id)) > 200)" #HT = Sum of Jets > 30GeV
preSel3 = "(Max$(Jet_pt*(abs(Jet_eta) < " + str(etaAcc) + ") > 100))" #ISR
preSelList = [preSel1, preSel2, preSel3]

if presel: preSel = combineCutsList(preSelList) 
else: preSel = "1"

#single-lepton (semileptonic) events
#if nEles == "01":
#Generated electron selection
nSel = "ngenLep == 1" #removes dileptonic events
genSel1 = "(abs(genLep_pdgId[0]) == 11 && abs(genLep_eta[0]) < " + str(etaAcc) + ")" #electron selection #index [0] ok since (only element)
genSel = combineCuts(nSel, genSel1)

#Reconstructed electron selection
matchSel = "LepAll_mcMatchId != 0"
#deltaR = "sqrt((genLep_eta[0] - LepAll_eta)^2 + (genLep_phi[0] - LepAll_phi)^2)"
#matchSel = "(" + deltaR +"*(abs(LepAll_pdgId) == 11 && abs(LepAll_eta) < " + str(etaAcc) + " && LepAll_mcMatchId != 0) <" + str(deltaRcut) +\
#"&& (" + deltaR +"*(abs(LepAll_pdgId) == 11 && abs(LepAll_eta) < " + str(etaAcc) + " && LepAll_mcMatchId != 0)) != 0)"

#Variable to plot
if plot == "efficiency": variable = "genLep_pt[0]"
elif plot == "misID" or plot == "misID2": variable = "LepAll_pt"

##single-electron events (semileptonic & dileptonic)
#elif nEles == "1": #semileptonic
#   #Generated electron selection
#   nSel = "ngenLep > 0" #redundant with genSel2 #nLepAll > 0 introduces bias
#   genSel1 = "(abs(genLep_pdgId) == 11 && abs(genLep_eta) < " + str(etaAcc) + ")" #electron selection (includes dielectron evts) #ngenLep == 1 would remove dileptonic events # index [0] does not include single-electron events with muon 
#   genSel2 = "(Sum$(abs(genLep_pdgId) == 11 && abs(genLep_eta) < " + str(etaAcc) + ") == 1)" # = number of electrons (includes dileptonic and semileptonic events) 
#   genSel = nSel + "&&" + genSel1 + "&&" + genSel2
#
#elif nEles == "2": #dileptonic
#   nSel = "ngenLep == 2" #does not include single-lepton events 
#   genSel1 = "(abs(genLep_pdgId) == 11 && abs(genLep_eta) < " + str(etaAcc) + ")" #electron selection (includes dielectron evts) #ngenLep == 1 would remove dileptonic events
#   genSel2 = "(Sum$(abs(genLep_pdgId) == 11 && abs(genLep_eta) < " + str(etaAcc) + ") == 2)" # = number of electrons (includes dilepton events only) 
#   genSel = nSel + "&&" + genSel1 + "&&" + genSel2

#Bin size 
#nbins = 100
#nbins = 10
xmin = 5
xmax = 20
bins = array('d',range(xmin,xmax+1,1))
normFactor = "1" #(0.5)"
z = ""

###############################################################################################################################################################################
#Electron ID Definitions
#IDs: 0 - none, 1 - veto (~95% eff), 2 - loose (~90% eff), 3 - medium (~80% eff), 4 - tight (~70% eff)
WPs = ['Veto', 'Loose', 'Medium', 'Tight']
variables = ['sigmaEtaEta', 'dEta',  'dPhi', 'hOverE', 'ooEmooP', 'd0', 'dz', 'MissingHits', 'convVeto']

WPcuts = {\
'Veto':{'sigmaEtaEta':{'EB':0.0114, 'EE':0.0352}, 'dEta':{'EB':0.0152, 'EE':0.0113}, 'dPhi':{'EB':0.216, 'EE':0.237}, 'hOverE':{'EB':0.181, 'EE':0.116}, 'ooEmooP':{'EB':0.207, 'EE':0.174},\
'd0':{'EB':0.0564, 'EE':0.222}, 'dz':{'EB':0.472, 'EE':0.921}, 'MissingHits':{'EB':2, 'EE':3}, 'convVeto':{'EB':1, 'EE':1}, 'relIso' : {'EB':0.126, 'EE':0.144}},

'Loose':{'sigmaEtaEta':{'EB':0.0103, 'EE':0.0301}, 'dEta':{'EB':0.0105, 'EE':0.00814}, 'dPhi':{'EB':0.115, 'EE':0.182}, 'hOverE':{'EB':0.104, 'EE':0.0897}, 'ooEmooP':{'EB':0.102, 'EE':0.126},\
'd0':{'EB':0.0261, 'EE':0.118}, 'dz':{'EB':0.41, 'EE':0.822}, 'MissingHits':{'EB':2, 'EE':1}, 'convVeto':{'EB':1, 'EE':1}, 'relIso' : {'EB':0.0893, 'EE':0.121}},

'Medium':{'sigmaEtaEta':{'EB':0.0101, 'EE':0.0283}, 'dEta':{'EB':0.0103, 'EE':0.00733}, 'dPhi':{'EB':0.0336, 'EE':0.114}, 'hOverE':{'EB':0.0876, 'EE':0.0678}, 'ooEmooP':{'EB':0.0174, 'EE':0.0898},\
'd0':{'EB':0.0118, 'EE':0.0739}, 'dz':{'EB':0.373, 'EE':0.602}, 'MissingHits':{'EB':2, 'EE':1}, 'convVeto':{'EB':1, 'EE':1}, 'relIso' : {'EB':0.0766, 'EE':0.0678}},

'Tight':{'sigmaEtaEta':{'EB':0.0101, 'EE':0.0279}, 'dEta':{'EB':0.00926, 'EE':0.00724}, 'dPhi':{'EB':0.0336, 'EE':0.0918}, 'hOverE':{'EB':0.0597, 'EE':0.0615}, 'ooEmooP':{'EB':0.012, 'EE':0.00999},\
'd0':{'EB':0.0111, 'EE':0.0351}, 'dz':{'EB':0.0466, 'EE':0.417}, 'MissingHits':{'EB':2, 'EE':1}, 'convVeto':{'EB':1, 'EE':1}, 'relIso' : {'EB':0.0354, 'EE':0.0646}}}

#WPcuts['Veto']['sigmaEtaEta']['EB'] = 0.014

cutIDsels = {iWP:{} for iWP in WPs}

for iWP in WPs:
   for var in variables: cutIDsels[iWP][var] = {}
   
for iWP in WPs:
   for reg in ['EE','EB']:
      cutIDsels[iWP]['sigmaEtaEta'][reg] = "LepAll_sigmaIEtaIEta < " + str(WPcuts[iWP]['sigmaEtaEta'][reg]) 
      cutIDsels[iWP]['dEta'][reg] = "abs(LepAll_dEtaScTrkIn) < " + str(WPcuts[iWP]['dEta'][reg])
      cutIDsels[iWP]['dPhi'][reg] = "abs(LepAll_dPhiScTrkIn) < " + str(WPcuts[iWP]['dPhi'][reg]) 
      cutIDsels[iWP]['hOverE'][reg] = "LepAll_hadronicOverEm < " + str(WPcuts[iWP]['hOverE'][reg])
      cutIDsels[iWP]['ooEmooP'][reg] = "abs(LepAll_eInvMinusPInv) < " + str(WPcuts[iWP]['ooEmooP'][reg])
      cutIDsels[iWP]['d0'][reg] = "abs(LepAll_dxy) < " + str(WPcuts[iWP]['d0'][reg])
      cutIDsels[iWP]['dz'][reg] = "abs(LepAll_dz) < " + str(WPcuts[iWP]['dz'][reg])
      cutIDsels[iWP]['MissingHits'][reg] = "LepAll_lostHits <= " + str(WPcuts[iWP]['MissingHits'][reg])
      cutIDsels[iWP]['convVeto'][reg]= "LepAll_convVeto == " + str(WPcuts[iWP]['convVeto'][reg])

geoSel= {'EB':"(abs(LepAll_eta) <= " + str(ebeeSplit) + ")", 'EE':"(abs(LepAll_eta) > " + str(ebeeSplit) + " && abs(LepAll_eta) < " + str(etaAcc) + ")"}
lowPtSel = "(genLep_pt > 6 && genLep_pt < 10)" #Pt selection
recoSel = "(abs(LepAll_pdgId) == 11)"
misMatchSel = "(LepAll_mcMatchId == 0)"
cutSel = {}

if not removedCut:
   if ID == "standard":
      for i,iWP in enumerate(WPs): cutSel[iWP] = "LepAll_SPRING15_25ns_v1 >= " + str(i+1)
   
else: 
   print makeLine()
   print "!!! Wrong variable input."
   print makeLine()
   sys.exit(0)

#"relIso03" "relIso04" "miniRelIso"
miniIsoSel1 = "LepAll_miniRelIso < 0.5"
miniIsoSel2= "LepAll_miniRelIso < 0.1"

if iso == "relIso04":
   relIsoSel = "LepAll_relIso04 < 0.2"
elif iso == "relIso03":
   relIsoSel = "LepAll_relIso03 < 0.2"

##################################################################################Canvas 1#############################################################################################
c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,2)

c1.cd(1)

#Electron Cut IDs
hists_total = {}
hists_passed = {}

for i,iWP in enumerate(WPs):
   selList = [preSel, recoSel, cutSel['Veto'], miniIsoSel1]
   hists_total[iWP] = makeHistVarBins(samples[sample].tree, variable, normFactor + "*" + weight + "*(" + combineCutsList(selList) + ")", bins)
   hists_total[iWP].SetName("%s_total_%s"%(plot,iWP))

   if i == 0:
      hists_total['Veto'].Draw("hist")
   
   del selList[:] 
   selList = [preSel, recoSel, cutSel[iWP], miniIsoSel2, relIsoSel]
   
   hists_passed[iWP] = makeHistVarBins(samples[sample].tree, variable, normFactor + "*" + weight + "*(" + combineCutsList(selList) + ")", bins)
   hists_passed[iWP].SetName("%s_passed_%s"%(plot,iWP))
   hists_passed[iWP].SetFillColor(0)
   hists_passed[iWP].Draw("histsame")

   if not removedCut: hists_total['Veto'].SetTitle("Electron p_{T} Distributions for Various IDs (%s Sample)"%(samples[sample].name))
   else: hists_total['Veto'].SetTitle("Electron p_{T} Distributions for Various IDs without %s Cut (%s Sample)"%(removedCut, samples[sample].name))
   hists_total['Veto'].GetXaxis().SetTitle("Reconstructed Electron p_{T} / GeV")
   hists_total['Veto'].GetYaxis().SetTitle("Counts / GeV")

ROOT.gPad.SetLogy()

alignStats(hists_total['Veto'])

#Colours
hists_passed['Veto'].SetLineColor(ROOT.kGreen+3)
hists_passed['Loose'].SetLineColor(ROOT.kBlue+1)
hists_passed['Medium'].SetLineColor(ROOT.kOrange-2)
hists_passed['Tight'].SetLineColor(ROOT.kRed+1)

ROOT.gPad.Modified()
ROOT.gPad.Update()

l1 = makeLegend()
if plot == "efficiency":
   l1.AddEntry("%s_total_Veto"%(plot), "Generated Electron p_{T}", "F")
elif plot == "misID" or plot == "misID2":
   l1.AddEntry("%s_total_noID"%(plot), "Reconstructed Electron p_{T}", "F")

l1.AddEntry("%s_passed_Veto"%(plot), "Veto ID", "F")
l1.AddEntry("%s_passed_Loose"%(plot), "Loose ID", "F")
l1.AddEntry("%s_passed_Medium"%(plot), "Medium ID", "F")
l1.AddEntry("%s_passed_Tight"%(plot), "Tight ID", "F")

ROOT.gPad.Modified()
ROOT.gPad.Update()

##Electron MVA IDs
#if mvaWPs:
#   mvaCuts = {'WP90':\
#             {'EB1_lowPt':-0.083313, 'EB2_lowPt':-0.235222, 'EE_lowPt':-0.67099, 'EB1':0.913286, 'EB2':0.805013, 'EE':0.358969},\
#              'WP80':\
#             {'EB1_lowPt':0.287435, 'EB2_lowPt':0.221846, 'EE_lowPt':-0.303263, 'EB1':0.967083, 'EB2':0.929117, 'EE':0.726311}}
#   
#   for iWP in mvaCuts.keys():
#      mvaSel = "(\
#      (LepAll_pt <= " + str(ptSplit) + " && abs(LepAll_eta) < " + str(ebSplit) + " && LepAll_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EB1_lowPt']) + ") || \
#      (LepAll_pt <= " + str(ptSplit) + " && abs(LepAll_eta) >= " + str(ebSplit) + " && abs(LepAll_eta) < " + str(ebeeSplit) + " && LepAll_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EB2_lowPt']) + ") || \
#      (LepAll_pt <= " + str(ptSplit) + " && abs(LepAll_eta) >= " + str(ebeeSplit) + " && abs(LepAll_eta) < " + str(etaAcc) + " && LepAll_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EE_lowPt']) + ") || \
#      (LepAll_pt > " + str(ptSplit) + " && abs(LepAll_eta) < " + str(ebSplit) + " && LepAll_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EB1']) + ") || \
#      (LepAll_pt > " + str(ptSplit) + " && abs(LepAll_eta) >= " + str(ebSplit) + " && abs(LepAll_eta) < " + str(ebeeSplit) + " && LepAll_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EB2']) + ") || \
#      (LepAll_pt > " + str(ptSplit) + " && abs(LepAll_eta) >= " + str(ebeeSplit) + " && abs(LepAll_eta) < " + str(etaAcc) + " && LepAll_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EE']) + "))"
#      if plot == "efficiency": 
#         del selList[:]
#         selList = [preSel, genSel, matchSel, mvaSel]
#         if lowPt: selList.append(lowPtSel)
#         hists_passed[iWP] = makeHistVarBins(samples[sample].tree, variable, normFactor + "*" + weight + "*(" + combineCutsList(selList) + ")", bins)
#      
#      elif plot == "misID" or plot == "misID2":
#         del selList[:]
#         selList = [preSel, recoSel, misMatchSel, mvaSel]
#         if lowPt: selList.append(lowPtSel)
#         hists_passed[iWP] = makeHistVarBins(samples[sample].tree, variable, normFactor + "*" + weight + "*(" + combineCutsList(selList) + ")", bins)
#         
#         if plot == "misID":
#            del selList[:]
#            selList = [preSel, recoSel, mvaSel]
#            if lowPt: selList.append(lowPtSel)
#            hists_total[iWP] = makeHistVarBins(samples[sample].tree, variable, normFactor + "*" + weight + "*(" + combineCutsList(selList) + ")", bins)
#         
#      hists_passed[iWP].SetName("%s_passed_%s"%(plot,iWP))
#      hists_passed[iWP].SetFillColor(0)
#      hists_passed[iWP].Draw("histsame")
#   
#   hists_passed['WP90'].SetLineColor(ROOT.kMagenta+2)
#   hists_passed['WP80'].SetLineColor(ROOT.kAzure+5)
#
#   ROOT.gPad.Modified()
#   ROOT.gPad.Update()
#   
#   l1.AddEntry("%s_passed_WP90"%(plot), "MVA ID (WP90)", "F")
#   l1.AddEntry("%s_passed_WP80"%(plot), "MVA ID (WP80)", "F")

ROOT.gPad.Modified()
ROOT.gPad.Update()

l1.Draw()

################################################################################################################################################################################
#Efficiency curves
c1.cd(2)

effs = {}

#Efficiency
for iWP in sorted(hists_passed.keys()):
   effs[iWP] = makeEffPlot(hists_passed[iWP], hists_total[iWP])
   effs[iWP].SetName("eff_" + iWP)
   
   if iWP == 'Loose': effs['Loose'].Draw("AP")
   else: effs[iWP].Draw("sameP")

   if not removedCut: effs['Loose'].SetTitle("Electron ID Efficiencies (%s Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency"%(samples[sample].name))
   else: effs['Loose'].SetTitle("Electron ID Efficiencies without %s Cut (%s Sample) ; Generated Electron p_{T} / GeV ; Efficiency"%(removedCut, samples[sample].name))

effs['Loose'].SetMarkerColor(ROOT.kBlue+1)
effs['Loose'].SetLineColor(ROOT.kBlue+1)

setupEffPlot(effs['Loose'])

for iWP in WPs: effs[iWP].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)

#Colours
effs['Veto'].SetMarkerColor(ROOT.kGreen+3)
effs['Veto'].SetLineColor(ROOT.kGreen+3)
effs['Medium'].SetMarkerColor(ROOT.kOrange-2)
effs['Medium'].SetLineColor(ROOT.kOrange-2)
effs['Tight'].SetMarkerColor(ROOT.kRed+1)
effs['Tight'].SetLineColor(ROOT.kRed+1)

ROOT.gPad.Modified()
ROOT.gPad.Update()

l2 = makeLegend()
l2.AddEntry("eff_Veto", "Veto ID", "P")
l2.AddEntry("eff_Loose", "Loose ID", "P")
l2.AddEntry("eff_Medium", "Medium ID", "P")
l2.AddEntry("eff_Tight", "Tight ID", "P")

#if mvaWPs:
#   effs['WP90'].SetMarkerColor(ROOT.kMagenta+2)
#   effs['WP90'].SetLineColor(ROOT.kMagenta+2)
#   effs['WP90'].SetMarkerStyle(22)
#   effs['WP90'].SetMarkerSize(1)
#   effs['WP80'].SetMarkerColor(ROOT.kAzure+5)
#   effs['WP80'].SetLineColor(ROOT.kAzure+5)
#   effs['WP80'].SetMarkerStyle(22)
#   effs['WP80'].SetMarkerSize(1)
#
#   ROOT.gPad.Modified()
#   ROOT.gPad.Update()
#
#   l2.AddEntry("eff_WP90", "MVA ID (WP90)", "P")
#   l2.AddEntry("eff_WP80", "MVA ID (WP80)", "P")

ROOT.gPad.Modified()
ROOT.gPad.Update()

l2.Draw()

c1.Modified()
c1.Update()

#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   if not removedCut:
      c1.SaveAs(savedir + "/%s_%s_%s%s.png"%(plot, iso, samples[sample].name, z))
      c1.SaveAs(savedir + "/pdf/%s_%s_%s%s.pdf"%(plot, iso, samples[sample].name, z))
      c1.SaveAs(savedir + "/root/%s_%s_%s%s.root"%(plot, iso, samples[sample].name, z))
   elif removedCut == "None":
      c1.SaveAs(savedir + "/%s_%s%s.png"%(plot, samples[sample].name, z))
      c1.SaveAs(savedir + "/pdf/%s_%s%s.pdf"%(plot, samples[sample].name, z))
      c1.SaveAs(savedir + "/root/%s_%s%s.root"%(plot, samples[sample].name, z))
   else:
      c1.SaveAs(savedir + "/%s_no_%s_%s%s.png"%(plot, removedCut, samples[sample].name, z))
      c1.SaveAs(savedir + "/pdf/%s_no_%s_%s%s.pdf"%(plot, removedCut, samples[sample].name, z))
      c1.SaveAs(savedir + "/root/%s_no_%s_%s%s.root"%(plot, removedCut, samples[sample].name, z))
