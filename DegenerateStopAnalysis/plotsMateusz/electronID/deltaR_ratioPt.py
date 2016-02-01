#deltaR_ratioPt.py
import ROOT
import os, sys
from Workspace.HEPHYPythonTools.helpers import getChunks, getChain#, getPlotFromChain, getYieldFromChain
#from Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_7412pass2 import * #data_path = "/data/nrad/cmgTuples/RunII/7412pass2_v4/RunIISpring15xminiAODv2"
from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_PP_mAODv2_7412pass2 import * #MC_path = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_v4_012016_v2/RunIISpring15DR74_25ns" SIGNAL_path = "/afs/hephy.at/dat
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from array import array
from math import pi, sqrt #cos, sin, sinh, log
from optparse import OptionParser

#Input options
parser = OptionParser()
parser.add_option("--sample", dest="sample",  help="Sample", type="str", default="S300_270FS") # "S300_240FS" "S300_270FS" "S300_290FS" "S300_270" "T2tt300_270FS" "TTJets" "WJets" "ZJets" 
parser.add_option("--presel", dest="presel",  help="Add preselection", type="int", default=1) # applies preselection
parser.add_option("--mvaWPs", dest="mvaWPs",  help="Add MVA WPs", type="int", default=0) # includes MVA WPs
parser.add_option("--save", dest="save",  help="Toggle save", type="int", default=1)
#parser.add_option("--id", dest="ID",  help="Electron ID type", type="str", default="standard") # "standard" "noIso" "iso"
#parser.add_option("--plot", dest="plot",  help="Plot type", type="str", default="efficiency") # "efficiency" "misID" "misID2"
#parser.add_option("--iso", dest="iso",  help="Isolation", type="str", default="relIso03") #"relIso03" "relIso04" "miniRelIso" "relIsoAn04"
#parser.add_option("--zoom", dest="zoom",  help="Toggle zoom", type="int", default=1)
#parser.add_option("-b", dest="batch",  help="batch", action="store_true", default=False)
(options, args) = parser.parse_args()
if len(args)==0:
   print "No arguments given. Using default settings."
   #exit()
#assert len(args)==1

#Arguments 
sample = options.sample 
presel = options.presel 
mvaWPs = options.mvaWPs
save = options.save
#ID = options.ID 
#plot = options.plot 
#zoom = options.zoom
#if ID == "iso": isolation = options.iso
#nEles = "01" # 01,01tau,1,2 #Number of electrons in event

#ROOT Options
ROOT.gROOT.Reset() #re-initialises ROOT
#ROOT.gROOT.SetStyle("Plain")

ROOT.gStyle.SetOptStat(1111) #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis
ROOT.gStyle.SetOptFit(1111) #1111 prints fits results on plot
#ROOT.gStyle.SetOptTitle(0) #suppresses title box
#ROOT.gStyle.SetFuncWidth(1)
#ROOT.gStyle.SetFuncColor(9)
#ROOT.gStyle.SetLineWidth(2)

ROOT.gStyle.SetPaintTextFormat("4.2f")
#ROOT.gStyle.SetTitleX(0.5) 
#ROOT.gStyle.SetTitleAlign(23)
#ROOT.gStyle.SetTitleW(0.8)

ROOT.gStyle.SetStatX(0.75)
ROOT.gStyle.SetStatY(0.65)
ROOT.gStyle.SetStatW(0.1)
ROOT.gStyle.SetStatH(0.15)

#Samples
samples = getSamples()
signals = ["S300_240FS", "S300_270FS", "S300_290FS", "S300_270", "T2tt300_270FS"]
backgrounds = ["TTJets", "WJets"]# "QCD", "ZJets"

print makeLine()
print "Samples:"
newLine()
for s in sorted(samples.keys()):
   print samples[s].name,":",s
   if samples[s].name not in signals and samples[s].name not in backgrounds:
      print makeLine()
      print "!!! Warning: Sample " + samples[s].name + " missing in samples lists. Please update."
      print makeLine()
   if sample == samples[s].name:
      sampleKey = s
      #break #would not scan all samples 
newLine()
print "Using", sample, "samples."
print makeLine()

#Geometric divisions
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap
etaAcc = 2.5 #eta acceptance

#Pt division for MVA ID
ptSplit = 10 #we have above and below 10 GeV categories 

#DeltaR cut for matching
deltaRcut = 0.3

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
deltaR = "sqrt((genLep_eta[0] - LepGood_eta)^2 + (genLep_phi[0] - LepGood_phi)^2)"

deltaRjet = "Min$(sqrt((LepGood_eta[0] - Jet_eta)^2 + (LepGood_phi[0] - Jet_phi)^2))"

#Bin size 
nbins = 100
xmin = 0
#xmax = 1000

if sample not in signals and sample not in backgrounds:
   print makeLine()
   print "!!! Sample " + sample + " unavailable."
   print makeLine()
   sys.exit(0)

#Selection criteria
#intLum = 10.0 #fb-1
#weight = "(xsec*" + str(intLum) + "*(10^3)/" + str(getChunks(sample)[1]) + ")" #xsec in pb
weight = samples[sampleKey].weight

#Preselection
preSel1 = "(met_pt > 200)" #MET
preSel2 = "(Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 4.5 && Jet_id)) > 200)" #HT = Sum of Jets > 30GeV
preSel3 = "(Max$(Jet_pt*(abs(Jet_eta) < " + str(etaAcc) + ") > 100))" #ISR

if presel == 1: preSel = preSel1 + "&&" + preSel2 + "&&" + preSel3
elif presel == 0: preSel = "1"

#if nEles == "01tau":
#   #Generated electron selection
#   nSel = "((ngenLep == 1) != (ngenLepFromTau == 1))" #removes dileptonic events
#   genSel1 = "((abs(genLep_pdgId[0]) == 11 && abs(genLep_eta[0]) < " + str(etaAcc) + ") || (abs(genLepFromTau_pdgId[0]) == 11 && abs(genLepFromTau_eta[0]) < " + str(etaAcc) + "))" #electron selection #index [0] ok since (only element)
#   #genSel = nSel# + "&&" + genSel1
#
#   #Reconstructed electron selection
#   deltaR = "sqrt((genLep_eta[0] - LepGood_eta)^2 + (genLep_phi[0] - LepGood_phi)^2)"
#   deltaRtau = "sqrt((genLepFromTau_eta[0] - LepGood_eta)^2 + (genLepFromTau_phi[0] - LepGood_phi)^2)"
#   
#   matchSel = "(" + deltaR +"*(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mcMatchId != 0) <" + str(deltaRcut) +\
#   "&& (" + deltaR +"*(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mcMatchId != 0)) != 0)" +\
#   "||(" + deltaRtau +"*(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mcMatchId != 0) <" + str(deltaRcut) +\
#   "&& (" + deltaRtau +"*(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mcMatchId != 0)) != 0)"

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

#WPcuts = {\
#'Veto':{'sigmaEtaEta':{'Barrel':0.0114, 'Endcap':0.0352}, 'dEta':{'Barrel':0.0152, 'Endcap':0.0113}, 'dPhi':{'Barrel':0.216, 'Endcap':0.237}, 'hOverE':{'Barrel':0.181, 'Endcap':0.116}, 'ooEmooP':{'Barrel':0.207, 'Endcap':0.174},\
#'d0':{'Barrel':0.0564, 'Endcap':0.222}, 'dz':{'Barrel':0.472, 'Endcap':0.921}, 'MissingHits':{'Barrel':2, 'Endcap':3}, 'convVeto':{'Barrel':1, 'Endcap':1}, 'relIso' : {'Barrel':0.126, 'Endcap':0.144}},
#'Loose':{'sigmaEtaEta':{'Barrel':0.0103, 'Endcap':0.0301}, 'dEta':{'Barrel':0.0105, 'Endcap':0.00814}, 'dPhi':{'Barrel':0.115, 'Endcap':0.182}, 'hOverE':{'Barrel':0.104, 'Endcap':0.0897}, 'ooEmooP':{'Barrel':0.102, 'Endcap':0.126},\
#'d0':{'Barrel':0.0261, 'Endcap':0.118}, 'dz':{'Barrel':0.41, 'Endcap':0.822}, 'MissingHits':{'Barrel':2, 'Endcap':1}, 'convVeto':{'Barrel':1, 'Endcap':1}, 'relIso' : {'Barrel':0.0893, 'Endcap':0.121}},
#'Medium':{'sigmaEtaEta':{'Barrel':0.0101, 'Endcap':0.0283}, 'dEta':{'Barrel':0.0103, 'Endcap':0.00733}, 'dPhi':{'Barrel':0.0336, 'Endcap':0.114}, 'hOverE':{'Barrel':0.0876, 'Endcap':0.0678}, 'ooEmooP':{'Barrel':0.0174, 'Endcap':0.0898},\
#'d0':{'Barrel':0.0118, 'Endcap':0.0739}, 'dz':{'Barrel':0.373, 'Endcap':0.602}, 'MissingHits':{'Barrel':2, 'Endcap':1}, 'convVeto':{'Barrel':1, 'Endcap':1}, 'relIso' : {'Barrel':0.0766, 'Endcap':0.0678}},
#'Tight':{'sigmaEtaEta':{'Barrel':0.0101, 'Endcap':0.0279}, 'dEta':{'Barrel':0.00926, 'Endcap':0.00724}, 'dPhi':{'Barrel':0.0336, 'Endcap':0.0918}, 'hOverE':{'Barrel':0.0597, 'Endcap':0.0615}, 'ooEmooP':{'Barrel':0.012, 'Endcap':0.00999},\
#'d0':{'Barrel':0.0111, 'Endcap':0.0351}, 'dz':{'Barrel':0.0466, 'Endcap':0.417}, 'MissingHits':{'Barrel':2, 'Endcap':1}, 'convVeto':{'Barrel':1, 'Endcap':1}, 'relIso' : {'Barrel':0.0354, 'Endcap':0.0646}}}

cutSel = {}

#if ID == "standard":
for i,WP in enumerate(WPs):
   cutSel[WP] = "LepGood_SPRING15_25ns_v1 >= " + str(i+1)

#elif ID == "noIso": 
#   for WP in WPcuts.keys():
#      cutSel[WP] = "(\
#      (abs(LepGood_eta) <=" + str(ebeeSplit) + "&& LepGood_sigmaIEtaIEta <" + str(WPcuts[WP]['sigmaEtaEta']['Barrel']) + "&& abs(LepGood_dEtaScTrkIn) <" + str(WPcuts[WP]['dEta']['Barrel']) + \
#      "&& abs(LepGood_dPhiScTrkIn) <" + str(WPcuts[WP]['dPhi']['Barrel']) + "&& LepGood_hadronicOverEm <" + str(WPcuts[WP]['hOverE']['Barrel']) + "&& abs(LepGood_eInvMinusPInv) <" + str(WPcuts[WP]['ooEmooP']['Barrel']) + \
#      "&& abs(LepGood_dxy) <" + str(WPcuts[WP]['d0']['Barrel']) + "&& abs(LepGood_dz) <" + str(WPcuts[WP]['dz']['Barrel']) + "&& LepGood_lostHits <=" + str(WPcuts[WP]['MissingHits']['Barrel']) + \
#      "&& LepGood_convVeto == " + str(WPcuts[WP]['convVeto']['Barrel']) + ") ||" + \
#      "(abs(LepGood_eta) >" + str(ebeeSplit) + "&& abs(LepGood_eta) <" + str(etaAcc) + "&& LepGood_sigmaIEtaIEta <" + str(WPcuts[WP]['sigmaEtaEta']['Endcap']) + "&& abs(LepGood_dEtaScTrkIn) <" + str(WPcuts[WP]['dEta']['Endcap']) + \
#      "&& abs(LepGood_dPhiScTrkIn) <" + str(WPcuts[WP]['dPhi']['Endcap']) + "&& LepGood_hadronicOverEm <" + str(WPcuts[WP]['hOverE']['Endcap']) + "&& abs(LepGood_eInvMinusPInv) <" + str(WPcuts[WP]['ooEmooP']['Endcap']) + \
#      "&& abs(LepGood_dxy) <" + str(WPcuts[WP]['d0']['Endcap']) + "&& abs(LepGood_dz) <" + str(WPcuts[WP]['dz']['Endcap']) + "&& LepGood_lostHits <=" + str(WPcuts[WP]['MissingHits']['Endcap']) + \
#      "&& LepGood_convVeto == " + str(WPcuts[WP]['convVeto']['Barrel']) + "))"

vars = {'deltaR':deltaR, 'ratioPt':"LepGood_pt/genLep_pt", 'deltaRjet':deltaRjet} # 
for i,var in enumerate(vars.items()):
   c1.cd(i+1)
   
   if var[0] == 'deltaR':
      xmax = 0.3
   elif var[0] == 'ratioPt':
      xmax = 3
   elif var[0] == 'deltaRjet':
      xmax = 7
   
   hists[var[0]]['None'] = makeHist(samples[sampleKey].tree, var[1], weight + "*(" + preSel + "&&" + genSel + "&&" + matchSel + ")", nbins, xmin, xmax)
   
   if var[0] == 'deltaR': 
      hists[var[0]]['None'].SetName("DeltaR")
      hists[var[0]]['None'].SetTitle("DeltaR between Generated and Reconstructed Electron Distributions for Various IDs (" + sample + " Sample)")
      hists[var[0]]['None'].GetXaxis().SetTitle("dR of GenEle and RecoEle")
   
   if var[0] == 'ratioPt' or var[0] == 'deltaRjet':
      deltaRcut = 0.3
   
      matchSel = "(" + deltaR +"*(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mcMatchId != 0) <" + str(deltaRcut) + "&& (" + deltaR +"*(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mcMatchId != 0)) != 0)"
      
      if var[0] == 'ratioPt':
         hists[var[0]]['None'].SetName("RatioPt")
         hists[var[0]]['None'].SetTitle("Distributions of p_{T} Ratio of Generated and Reconstructed Electrons for Various IDs (" + sample + " Sample)")
         hists[var[0]]['None'].GetXaxis().SetTitle("RecoEle p_{T} / GenEle p_{T}")
   
      elif var[0] == 'deltaRjet':
         hists[var[0]]['None'].SetName("DeltaRjet")
         hists[var[0]]['None'].SetTitle("Minimum DeltaR between Electron and Jet Distributions for Various IDs (" + sample + " Sample)")
         hists[var[0]]['None'].GetXaxis().SetTitle("Min(dR) of Electron and Jet")
   
   hists[var[0]]['None'].GetXaxis().SetTitleOffset(1.2)
   hists[var[0]]['None'].GetYaxis().SetTitleOffset(1.2)
   hists[var[0]]['None'].SetFillColor(ROOT.kBlue-9)
   hists[var[0]]['None'].SetLineColor(ROOT.kBlack)
   hists[var[0]]['None'].SetLineWidth(3)
   hists[var[0]]['None'].Draw("hist")
   
   for WP in WPs:
      hists[var[0]][WP] = makeHist(samples[sampleKey].tree, var[1], weight + "*(" + preSel + "&&" + genSel + "&&" + matchSel + "&&" + cutSel[WP] + ")", nbins, xmin, xmax)
      hists[var[0]][WP].SetName(var[0] + "_" + WP)
      hists[var[0]][WP].SetFillColor(0)
      hists[var[0]][WP].SetLineWidth(3)
      hists[var[0]][WP].Draw("histsame")
   
   ROOT.gPad.SetLogy()
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   alignStats(hists[var[0]]['None'])
   
   #Colours
   hists[var[0]]['Veto'].SetLineColor(ROOT.kGreen+3)
   hists[var[0]]['Loose'].SetLineColor(ROOT.kBlue+1)
   hists[var[0]]['Medium'].SetLineColor(ROOT.kOrange-2)
   hists[var[0]]['Tight'].SetLineColor(ROOT.kRed+1)
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   if i == 0: 
      l1 = makeLegend()
      #if var[0] == "deltaR": l1.AddEntry("DeltaR", "DeltaR", "F")
      #elif var[0] == "ratioPt": l1.AddEntry("RatioPt", "RecoEle p_{T} / GenEle p_{T}", "F")
      #elif var[0] == "deltaRjet": l1.AddEntry("DeltaRjet", "Min(dR_ele_jet)", "F")
      l1.AddEntry(var[0] + "_Veto", "Veto ID", "F")
      l1.AddEntry(var[0] + "_Loose", "Loose ID", "F")
      l1.AddEntry(var[0] + "_Medium", "Medium ID", "F")
      l1.AddEntry(var[0] + "_Tight", "Tight ID", "F")
   
   #Electron MVA IDs
   if mvaWPs == 1:
      mvaCuts = {'WP90':\
                {'EB1_lowPt':-0.083313, 'EB2_lowPt':-0.235222, 'EE_lowPt':-0.67099, 'EB1':0.913286, 'EB2':0.805013, 'EE':0.358969},\
                 'WP80':\
                {'EB1_lowPt':0.287435, 'EB2_lowPt':0.221846, 'EE_lowPt':-0.303263, 'EB1':0.967083, 'EB2':0.929117, 'EE':0.726311}}
      
      for WP in mvaCuts.keys():
         mvaSel = "(\
         (LepGood_pt <=" + str(ptSplit) + "&& abs(LepGood_eta) < " + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(mvaCuts[WP]['EB1_lowPt']) + ") || \
         (LepGood_pt <=" + str(ptSplit) + "&& abs(LepGood_eta) >=" + str(ebSplit) + "&& abs(LepGood_eta) <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(mvaCuts[WP]['EB2_lowPt']) + ") || \
         (LepGood_pt <=" + str(ptSplit) + "&& abs(LepGood_eta) >=" + str(ebeeSplit) + "&& abs(LepGood_eta) <" + str(etaAcc) + "&& LepGood_mvaIdSpring15 >=" + str(mvaCuts[WP]['EE_lowPt']) + ") || \
         (LepGood_pt >" + str(ptSplit) + "&& abs(LepGood_eta) <" + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(mvaCuts[WP]['EB1']) + ") || \
         (LepGood_pt >" + str(ptSplit) + "&& abs(LepGood_eta) >=" + str(ebSplit) + "&& abs(LepGood_eta) <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(mvaCuts[WP]['EB2']) + ") || \
         (LepGood_pt >" + str(ptSplit) + "&& abs(LepGood_eta) >=" + str(ebeeSplit) + "&& abs(LepGood_eta) <" + str(etaAcc) + "&& LepGood_mvaIdSpring15 >=" + str(mvaCuts[WP]['EE']) + "))"
         hists[var[0]][WP] = makeHist(samples[sampleKey].tree, var[1], weight + "*(" + preSel + "&&" + genSel + "&&" + matchSel + "&&" + mvaSel + ")", nbins, xmax, xmin)
         hists[var[0]][WP].SetName(var[0] + "_" + WP)
         hists[var[0]][WP].SetFillColor(0)
         hists[var[0]][WP].SetLineWidth(3)
         hists[var[0]][WP].Draw("histsame")
      
      hists[var[0]]['WP90'].SetLineColor(ROOT.kMagenta+2)
      hists[var[0]]['WP80'].SetLineColor(ROOT.kAzure+5)
   
      ROOT.gPad.Modified()
      ROOT.gPad.Update()
      
      l1.AddEntry(var[0] + "_WP90", "MVA ID (WP90)", "F")
      l1.AddEntry(var[0] + "_WP80", "MVA ID (WP80)", "F")
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   l1.Draw()

ROOT.gPad.Modified()
ROOT.gPad.Update()
c1.Modified()
c1.Update()

#Write to file
if save == 1: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   if mvaWPs == 0: 
      savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronID/standard/deltaR_ratioPt"
   elif mvaWPs == 1: 
      savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronID/standard/deltaR_ratioPt/withMva"
   
   if not os.path.exists(savedir):
      os.makedirs(savedir)
   if not os.path.exists(savedir + "/root"):
      os.makedirs(savedir + "/root")
   if not os.path.exists(savedir + "/pdf"):
      os.makedirs(savedir + "/pdf")

   #Save to Web
   c1.SaveAs(savedir + "/deltaR_ratioPt_" + sample + ".png")
   c1.SaveAs(savedir + "/root/deltaR_ratioPt_" + sample + ".root")
   c1.SaveAs(savedir + "/pdf/deltaR_ratioPt_" + sample + ".pdf")
