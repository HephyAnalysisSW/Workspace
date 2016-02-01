#eleIdEffs_nMinus1.py
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
parser.add_option("--removedCut", dest="removedCut",  help="Variable removed from Electron ID", type="str", default="None") #"sigmaEtaEta" "dEta" "dPhi" "hOverE" "ooEmooP" "d0" "dz" "MissingHits" "convVeto"
parser.add_option("--plot", dest="plot",  help="Plot type", type="str", default="efficiency") # "efficiency" "misID" "misID2"
parser.add_option("--sample", dest="sample",  help="Sample", type="str", default="S300_270FS") # "S300_240FS" "S300_270FS" "S300_290FS" "S300_270" "T2tt300_270FS" "TTJets" "WJets" "ZJets" 
parser.add_option("--presel", dest="presel",  help="Add preselection", type="int", default=1) # applies preselection
parser.add_option("--zoom", dest="zoom",  help="Toggle zoom", type="int", default=1)
parser.add_option("--save", dest="save",  help="Toggle save", type="int", default=1)
#parser.add_option("--id", dest="ID",  help="Electron ID type", type="str", default="standard") # "standard" "noIso" "iso"
#parser.add_option("--mvaWPs", dest="mvaWPs",  help="Add MVA WPs", type="int", default=0) # includes MVA WPs
#parser.add_option("--iso", dest="iso",  help="Isolation", type="str", default="relIso03") #"relIso03" "relIso04" "miniRelIso" "relIsoAn04"
#parser.add_option("-b", dest="batch",  help="batch", action="store_true", default=False)
(options, args) = parser.parse_args()
if len(args)==0:
   print "No arguments given. Using default settings."
   #exit()
#assert len(args)==1

#Arguments
removedCut = options.removedCut 
plot = options.plot 
sample = options.sample 
presel = options.presel 
zoom = options.zoom
save = options.save
#ID = options.ID 
#mvaWPs = options.mvaWPs
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
backgrounds = ["TTJets", "WJets", "QCD", "ZJets"]

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

#Variable to plot
if plot == "efficiency": var = "genLep_pt[0]"
elif plot == "misID" or plot == "misID2": var = "LepGood_pt"

#Bin size 
#nbins = 100
xmin = 0
#xmax = 1000

#Zoom
if zoom == 0:
   if sample in signals:
      xmax = 150
   elif sample in backgrounds:
      xmax = 500
   else:
      print makeLine()
      print "!!! Sample " + sample + " unavailable."
      print makeLine()
      sys.exit(0)

   bins = array('d', range(xmin,50,2) + range(50,100,5) + range(100,xmax+10,10)) #Variable bin size
   normFactor = "((" + var + " < 50)*0.5 + (" + var + " >= 50 &&" + var + " < 100)*0.2 + (" + var + " >= 100)*0.1)"
   z = ""

elif zoom == 1:
   #nbins = 10
   xmax = 50
   bins = array('d',range(xmin,xmax+2,2))
   normFactor = "(0.5)"
   z = "_lowPt"

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
#   genSel1 = "(abs(genLep_pdgId) == 11 && abs(genLep_eta) < " + str(etaAcc) + ")" #electron selection (includes dielectron evts) #ngenLep == 1 would remove dileptonic events # index [0] does not include single-electron events with muon 
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
c1.Divide(1,2)

c1.cd(1)

#Electron Cut IDs
hists_total = {}
hists_passed = {}

#IDs: 0 - none, 1 - veto (~95% eff), 2 - loose (~90% eff), 3 - medium (~80% eff), 4 - tight (~70% eff)
WPs = ['Veto', 'Loose', 'Medium', 'Tight']

WPcuts = {\
'Veto':{'sigmaEtaEta':{'Barrel':0.0114, 'Endcap':0.0352}, 'dEta':{'Barrel':0.0152, 'Endcap':0.0113}, 'dPhi':{'Barrel':0.216, 'Endcap':0.237}, 'hOverE':{'Barrel':0.181, 'Endcap':0.116}, 'ooEmooP':{'Barrel':0.207, 'Endcap':0.174},\
'd0':{'Barrel':0.0564, 'Endcap':0.222}, 'dz':{'Barrel':0.472, 'Endcap':0.921}, 'MissingHits':{'Barrel':2, 'Endcap':3}, 'convVeto':{'Barrel':1, 'Endcap':1}, 'relIso' : {'Barrel':0.126, 'Endcap':0.144}},
'Loose':{'sigmaEtaEta':{'Barrel':0.0103, 'Endcap':0.0301}, 'dEta':{'Barrel':0.0105, 'Endcap':0.00814}, 'dPhi':{'Barrel':0.115, 'Endcap':0.182}, 'hOverE':{'Barrel':0.104, 'Endcap':0.0897}, 'ooEmooP':{'Barrel':0.102, 'Endcap':0.126},\
'd0':{'Barrel':0.0261, 'Endcap':0.118}, 'dz':{'Barrel':0.41, 'Endcap':0.822}, 'MissingHits':{'Barrel':2, 'Endcap':1}, 'convVeto':{'Barrel':1, 'Endcap':1}, 'relIso' : {'Barrel':0.0893, 'Endcap':0.121}},
'Medium':{'sigmaEtaEta':{'Barrel':0.0101, 'Endcap':0.0283}, 'dEta':{'Barrel':0.0103, 'Endcap':0.00733}, 'dPhi':{'Barrel':0.0336, 'Endcap':0.114}, 'hOverE':{'Barrel':0.0876, 'Endcap':0.0678}, 'ooEmooP':{'Barrel':0.0174, 'Endcap':0.0898},\
'd0':{'Barrel':0.0118, 'Endcap':0.0739}, 'dz':{'Barrel':0.373, 'Endcap':0.602}, 'MissingHits':{'Barrel':2, 'Endcap':1}, 'convVeto':{'Barrel':1, 'Endcap':1}, 'relIso' : {'Barrel':0.0766, 'Endcap':0.0678}},
'Tight':{'sigmaEtaEta':{'Barrel':0.0101, 'Endcap':0.0279}, 'dEta':{'Barrel':0.00926, 'Endcap':0.00724}, 'dPhi':{'Barrel':0.0336, 'Endcap':0.0918}, 'hOverE':{'Barrel':0.0597, 'Endcap':0.0615}, 'ooEmooP':{'Barrel':0.012, 'Endcap':0.00999},\
'd0':{'Barrel':0.0111, 'Endcap':0.0351}, 'dz':{'Barrel':0.0466, 'Endcap':0.417}, 'MissingHits':{'Barrel':2, 'Endcap':1}, 'convVeto':{'Barrel':1, 'Endcap':1}, 'relIso' : {'Barrel':0.0354, 'Endcap':0.0646}}}

cutSel = {}
recoSel = "(abs(LepGood_pdgId) == 11)"
misMatchSel = "(LepGood_mcMatchId == 0)"

if removedCut == "None":
   for WP in WPcuts.keys():
      cutSel[WP] = "(\
      (abs(LepGood_eta) <=" + str(ebeeSplit) + "&& LepGood_sigmaIEtaIEta <" + str(WPcuts[WP]['sigmaEtaEta']['Barrel']) + "&& abs(LepGood_dEtaScTrkIn) <" + str(WPcuts[WP]['dEta']['Barrel']) + \
      "&& abs(LepGood_dPhiScTrkIn) <" + str(WPcuts[WP]['dPhi']['Barrel']) + "&& LepGood_hadronicOverEm <" + str(WPcuts[WP]['hOverE']['Barrel']) + "&& abs(LepGood_eInvMinusPInv) <" + str(WPcuts[WP]['ooEmooP']['Barrel']) + \
      "&& abs(LepGood_dxy) <" + str(WPcuts[WP]['d0']['Barrel']) + "&& abs(LepGood_dz) <" + str(WPcuts[WP]['dz']['Barrel']) + "&& LepGood_lostHits <=" + str(WPcuts[WP]['MissingHits']['Barrel']) + \
      "&& LepGood_convVeto == " + str(WPcuts[WP]['convVeto']['Barrel']) +  ") ||" + \
      "(abs(LepGood_eta) >" + str(ebeeSplit) + "&& abs(LepGood_eta) <" + str(etaAcc) + "&& LepGood_sigmaIEtaIEta <" + str(WPcuts[WP]['sigmaEtaEta']['Endcap']) + "&& abs(LepGood_dEtaScTrkIn) <" + str(WPcuts[WP]['dEta']['Endcap']) + \
      "&& abs(LepGood_dPhiScTrkIn) <" + str(WPcuts[WP]['dPhi']['Endcap']) + "&& LepGood_hadronicOverEm <" + str(WPcuts[WP]['hOverE']['Endcap']) + "&& abs(LepGood_eInvMinusPInv) <" + str(WPcuts[WP]['ooEmooP']['Endcap']) + \
      "&& abs(LepGood_dxy) <" + str(WPcuts[WP]['d0']['Endcap']) + "&& abs(LepGood_dz) <" + str(WPcuts[WP]['dz']['Endcap']) + "&& LepGood_lostHits <=" + str(WPcuts[WP]['MissingHits']['Endcap']) + \
      "&& LepGood_convVeto == " + str(WPcuts[WP]['convVeto']['Barrel']) + "))"
elif removedCut == "sigmaEtaEta":
   for WP in WPcuts.keys():
      cutSel[WP] = "(\
      (abs(LepGood_eta) <=" + str(ebeeSplit) + "&& abs(LepGood_dEtaScTrkIn) <" + str(WPcuts[WP]['dEta']['Barrel']) + \
      "&& abs(LepGood_dPhiScTrkIn) <" + str(WPcuts[WP]['dPhi']['Barrel']) + "&& LepGood_hadronicOverEm <" + str(WPcuts[WP]['hOverE']['Barrel']) + "&& abs(LepGood_eInvMinusPInv) <" + str(WPcuts[WP]['ooEmooP']['Barrel']) + \
      "&& abs(LepGood_dxy) <" + str(WPcuts[WP]['d0']['Barrel']) + "&& abs(LepGood_dz) <" + str(WPcuts[WP]['dz']['Barrel']) + "&& LepGood_lostHits <=" + str(WPcuts[WP]['MissingHits']['Barrel']) + \
      "&& LepGood_convVeto == " + str(WPcuts[WP]['convVeto']['Barrel']) +  ") ||" + \
      "(abs(LepGood_eta) >" + str(ebeeSplit) + "&& abs(LepGood_eta) <" + str(etaAcc) + "&& abs(LepGood_dEtaScTrkIn) <" + str(WPcuts[WP]['dEta']['Endcap']) + \
      "&& abs(LepGood_dPhiScTrkIn) <" + str(WPcuts[WP]['dPhi']['Endcap']) + "&& LepGood_hadronicOverEm <" + str(WPcuts[WP]['hOverE']['Endcap']) + "&& abs(LepGood_eInvMinusPInv) <" + str(WPcuts[WP]['ooEmooP']['Endcap']) + \
      "&& abs(LepGood_dxy) <" + str(WPcuts[WP]['d0']['Endcap']) + "&& abs(LepGood_dz) <" + str(WPcuts[WP]['dz']['Endcap']) + "&& LepGood_lostHits <=" + str(WPcuts[WP]['MissingHits']['Endcap']) + \
      "&& LepGood_convVeto == " + str(WPcuts[WP]['convVeto']['Barrel']) + "))"
elif removedCut == "dEta":
   for WP in WPcuts.keys():
      cutSel[WP] = "(\
      (abs(LepGood_eta) <=" + str(ebeeSplit) + "&& LepGood_sigmaIEtaIEta <" + str(WPcuts[WP]['sigmaEtaEta']['Barrel']) + \
      "&& abs(LepGood_dPhiScTrkIn) <" + str(WPcuts[WP]['dPhi']['Barrel']) + "&& LepGood_hadronicOverEm <" + str(WPcuts[WP]['hOverE']['Barrel']) + "&& abs(LepGood_eInvMinusPInv) <" + str(WPcuts[WP]['ooEmooP']['Barrel']) + \
      "&& abs(LepGood_dxy) <" + str(WPcuts[WP]['d0']['Barrel']) + "&& abs(LepGood_dz) <" + str(WPcuts[WP]['dz']['Barrel']) + "&& LepGood_lostHits <=" + str(WPcuts[WP]['MissingHits']['Barrel']) + \
      "&& LepGood_convVeto == " + str(WPcuts[WP]['convVeto']['Barrel']) +  ") ||" + \
      "(abs(LepGood_eta) >" + str(ebeeSplit) + "&& abs(LepGood_eta) <" + str(etaAcc) + "&& LepGood_sigmaIEtaIEta <" + str(WPcuts[WP]['sigmaEtaEta']['Endcap']) + \
      "&& abs(LepGood_dPhiScTrkIn) <" + str(WPcuts[WP]['dPhi']['Endcap']) + "&& LepGood_hadronicOverEm <" + str(WPcuts[WP]['hOverE']['Endcap']) + "&& abs(LepGood_eInvMinusPInv) <" + str(WPcuts[WP]['ooEmooP']['Endcap']) + \
      "&& abs(LepGood_dxy) <" + str(WPcuts[WP]['d0']['Endcap']) + "&& abs(LepGood_dz) <" + str(WPcuts[WP]['dz']['Endcap']) + "&& LepGood_lostHits <=" + str(WPcuts[WP]['MissingHits']['Endcap']) + \
      "&& LepGood_convVeto == " + str(WPcuts[WP]['convVeto']['Barrel']) + "))"
elif removedCut == "dPhi":
   for WP in WPcuts.keys():
      cutSel[WP] = "(\
      (abs(LepGood_eta) <=" + str(ebeeSplit) + "&& LepGood_sigmaIEtaIEta <" + str(WPcuts[WP]['sigmaEtaEta']['Barrel']) + "&& abs(LepGood_dEtaScTrkIn) <" + str(WPcuts[WP]['dEta']['Barrel']) + \
      "&& LepGood_hadronicOverEm <" + str(WPcuts[WP]['hOverE']['Barrel']) + "&& abs(LepGood_eInvMinusPInv) <" + str(WPcuts[WP]['ooEmooP']['Barrel']) + \
      "&& abs(LepGood_dxy) <" + str(WPcuts[WP]['d0']['Barrel']) + "&& abs(LepGood_dz) <" + str(WPcuts[WP]['dz']['Barrel']) + "&& LepGood_lostHits <=" + str(WPcuts[WP]['MissingHits']['Barrel']) + \
      "&& LepGood_convVeto == " + str(WPcuts[WP]['convVeto']['Barrel']) +  ") ||" + \
      "(abs(LepGood_eta) >" + str(ebeeSplit) + "&& abs(LepGood_eta) <" + str(etaAcc) + "&& LepGood_sigmaIEtaIEta <" + str(WPcuts[WP]['sigmaEtaEta']['Endcap']) + "&& abs(LepGood_dEtaScTrkIn) <" + str(WPcuts[WP]['dEta']['Endcap']) + \
      "&& LepGood_hadronicOverEm <" + str(WPcuts[WP]['hOverE']['Endcap']) + "&& abs(LepGood_eInvMinusPInv) <" + str(WPcuts[WP]['ooEmooP']['Endcap']) + \
      "&& abs(LepGood_dxy) <" + str(WPcuts[WP]['d0']['Endcap']) + "&& abs(LepGood_dz) <" + str(WPcuts[WP]['dz']['Endcap']) + "&& LepGood_lostHits <=" + str(WPcuts[WP]['MissingHits']['Endcap']) + \
      "&& LepGood_convVeto == " + str(WPcuts[WP]['convVeto']['Barrel']) + "))"
elif removedCut == "hOverE":
   for WP in WPcuts.keys():
      cutSel[WP] = "(\
      (abs(LepGood_eta) <=" + str(ebeeSplit) + "&& LepGood_sigmaIEtaIEta <" + str(WPcuts[WP]['sigmaEtaEta']['Barrel']) + "&& abs(LepGood_dEtaScTrkIn) <" + str(WPcuts[WP]['dEta']['Barrel']) + \
      "&& abs(LepGood_dPhiScTrkIn) <" + str(WPcuts[WP]['dPhi']['Barrel']) + "&& abs(LepGood_eInvMinusPInv) <" + str(WPcuts[WP]['ooEmooP']['Barrel']) + \
      "&& abs(LepGood_dxy) <" + str(WPcuts[WP]['d0']['Barrel']) + "&& abs(LepGood_dz) <" + str(WPcuts[WP]['dz']['Barrel']) + "&& LepGood_lostHits <=" + str(WPcuts[WP]['MissingHits']['Barrel']) + \
      "&& LepGood_convVeto == " + str(WPcuts[WP]['convVeto']['Barrel']) +  ") ||" + \
      "(abs(LepGood_eta) >" + str(ebeeSplit) + "&& abs(LepGood_eta) <" + str(etaAcc) + "&& LepGood_sigmaIEtaIEta <" + str(WPcuts[WP]['sigmaEtaEta']['Endcap']) + "&& abs(LepGood_dEtaScTrkIn) <" + str(WPcuts[WP]['dEta']['Endcap']) + \
      "&& abs(LepGood_dPhiScTrkIn) <" + str(WPcuts[WP]['dPhi']['Endcap']) + "&& abs(LepGood_eInvMinusPInv) <" + str(WPcuts[WP]['ooEmooP']['Endcap']) + \
      "&& abs(LepGood_dxy) <" + str(WPcuts[WP]['d0']['Endcap']) + "&& abs(LepGood_dz) <" + str(WPcuts[WP]['dz']['Endcap']) + "&& LepGood_lostHits <=" + str(WPcuts[WP]['MissingHits']['Endcap']) + \
      "&& LepGood_convVeto == " + str(WPcuts[WP]['convVeto']['Barrel']) + "))"
elif removedCut == "ooEmooP":
   for WP in WPcuts.keys():
      cutSel[WP] = "(\
      (abs(LepGood_eta) <=" + str(ebeeSplit) + "&& LepGood_sigmaIEtaIEta <" + str(WPcuts[WP]['sigmaEtaEta']['Barrel']) + "&& abs(LepGood_dEtaScTrkIn) <" + str(WPcuts[WP]['dEta']['Barrel']) + \
      "&& abs(LepGood_dPhiScTrkIn) <" + str(WPcuts[WP]['dPhi']['Barrel']) + "&& LepGood_hadronicOverEm <" + str(WPcuts[WP]['hOverE']['Barrel']) + \
      "&& abs(LepGood_dxy) <" + str(WPcuts[WP]['d0']['Barrel']) + "&& abs(LepGood_dz) <" + str(WPcuts[WP]['dz']['Barrel']) + "&& LepGood_lostHits <=" + str(WPcuts[WP]['MissingHits']['Barrel']) + \
      "&& LepGood_convVeto == " + str(WPcuts[WP]['convVeto']['Barrel']) +  ") ||" + \
      "(abs(LepGood_eta) >" + str(ebeeSplit) + "&& abs(LepGood_eta) <" + str(etaAcc) + "&& LepGood_sigmaIEtaIEta <" + str(WPcuts[WP]['sigmaEtaEta']['Endcap']) + "&& abs(LepGood_dEtaScTrkIn) <" + str(WPcuts[WP]['dEta']['Endcap']) + \
      "&& abs(LepGood_dPhiScTrkIn) <" + str(WPcuts[WP]['dPhi']['Endcap']) + "&& LepGood_hadronicOverEm <" + str(WPcuts[WP]['hOverE']['Endcap']) + \
      "&& abs(LepGood_dxy) <" + str(WPcuts[WP]['d0']['Endcap']) + "&& abs(LepGood_dz) <" + str(WPcuts[WP]['dz']['Endcap']) + "&& LepGood_lostHits <=" + str(WPcuts[WP]['MissingHits']['Endcap']) + \
      "&& LepGood_convVeto == " + str(WPcuts[WP]['convVeto']['Barrel']) + "))"
elif removedCut == "d0":
   for WP in WPcuts.keys():
      cutSel[WP] = "(\
      (abs(LepGood_eta) <=" + str(ebeeSplit) + "&& LepGood_sigmaIEtaIEta <" + str(WPcuts[WP]['sigmaEtaEta']['Barrel']) + "&& abs(LepGood_dEtaScTrkIn) <" + str(WPcuts[WP]['dEta']['Barrel']) + \
      "&& abs(LepGood_dPhiScTrkIn) <" + str(WPcuts[WP]['dPhi']['Barrel']) + "&& LepGood_hadronicOverEm <" + str(WPcuts[WP]['hOverE']['Barrel']) + "&& abs(LepGood_eInvMinusPInv) <" + str(WPcuts[WP]['ooEmooP']['Barrel']) + \
      "&& abs(LepGood_dz) <" + str(WPcuts[WP]['dz']['Barrel']) + "&& LepGood_lostHits <=" + str(WPcuts[WP]['MissingHits']['Barrel']) + \
      "&& LepGood_convVeto == " + str(WPcuts[WP]['convVeto']['Barrel']) +  ") ||" + \
      "(abs(LepGood_eta) >" + str(ebeeSplit) + "&& abs(LepGood_eta) <" + str(etaAcc) + "&& LepGood_sigmaIEtaIEta <" + str(WPcuts[WP]['sigmaEtaEta']['Endcap']) + "&& abs(LepGood_dEtaScTrkIn) <" + str(WPcuts[WP]['dEta']['Endcap']) + \
      "&& abs(LepGood_dPhiScTrkIn) <" + str(WPcuts[WP]['dPhi']['Endcap']) + "&& LepGood_hadronicOverEm <" + str(WPcuts[WP]['hOverE']['Endcap']) + "&& abs(LepGood_eInvMinusPInv) <" + str(WPcuts[WP]['ooEmooP']['Endcap']) + \
      "&& abs(LepGood_dz) <" + str(WPcuts[WP]['dz']['Endcap']) + "&& LepGood_lostHits <=" + str(WPcuts[WP]['MissingHits']['Endcap']) + \
      "&& LepGood_convVeto == " + str(WPcuts[WP]['convVeto']['Barrel']) + "))"
elif removedCut == "dz":
   for WP in WPcuts.keys():
      cutSel[WP] = "(\
      (abs(LepGood_eta) <=" + str(ebeeSplit) + "&& LepGood_sigmaIEtaIEta <" + str(WPcuts[WP]['sigmaEtaEta']['Barrel']) + "&& abs(LepGood_dEtaScTrkIn) <" + str(WPcuts[WP]['dEta']['Barrel']) + \
      "&& abs(LepGood_dPhiScTrkIn) <" + str(WPcuts[WP]['dPhi']['Barrel']) + "&& LepGood_hadronicOverEm <" + str(WPcuts[WP]['hOverE']['Barrel']) + "&& abs(LepGood_eInvMinusPInv) <" + str(WPcuts[WP]['ooEmooP']['Barrel']) + \
      "&& abs(LepGood_dxy) <" + str(WPcuts[WP]['d0']['Barrel']) + "&& LepGood_lostHits <=" + str(WPcuts[WP]['MissingHits']['Barrel']) + \
      "&& LepGood_convVeto == " + str(WPcuts[WP]['convVeto']['Barrel']) +  ") ||" + \
      "(abs(LepGood_eta) >" + str(ebeeSplit) + "&& abs(LepGood_eta) <" + str(etaAcc) + "&& LepGood_sigmaIEtaIEta <" + str(WPcuts[WP]['sigmaEtaEta']['Endcap']) + "&& abs(LepGood_dEtaScTrkIn) <" + str(WPcuts[WP]['dEta']['Endcap']) + \
      "&& abs(LepGood_dPhiScTrkIn) <" + str(WPcuts[WP]['dPhi']['Endcap']) + "&& LepGood_hadronicOverEm <" + str(WPcuts[WP]['hOverE']['Endcap']) + "&& abs(LepGood_eInvMinusPInv) <" + str(WPcuts[WP]['ooEmooP']['Endcap']) + \
      "&& abs(LepGood_dxy) <" + str(WPcuts[WP]['d0']['Endcap']) + "&& LepGood_lostHits <=" + str(WPcuts[WP]['MissingHits']['Endcap']) + \
      "&& LepGood_convVeto == " + str(WPcuts[WP]['convVeto']['Barrel']) + "))"
elif removedCut == "MissingHits":
   for WP in WPcuts.keys():
      cutSel[WP] = "(\
      (abs(LepGood_eta) <=" + str(ebeeSplit) + "&& LepGood_sigmaIEtaIEta <" + str(WPcuts[WP]['sigmaEtaEta']['Barrel']) + "&& abs(LepGood_dEtaScTrkIn) <" + str(WPcuts[WP]['dEta']['Barrel']) + \
      "&& abs(LepGood_dPhiScTrkIn) <" + str(WPcuts[WP]['dPhi']['Barrel']) + "&& LepGood_hadronicOverEm <" + str(WPcuts[WP]['hOverE']['Barrel']) + "&& abs(LepGood_eInvMinusPInv) <" + str(WPcuts[WP]['ooEmooP']['Barrel']) + \
      "&& abs(LepGood_dxy) <" + str(WPcuts[WP]['d0']['Barrel']) + "&& abs(LepGood_dz) <" + str(WPcuts[WP]['dz']['Barrel']) + \
      "&& LepGood_convVeto == " + str(WPcuts[WP]['convVeto']['Barrel']) + ") ||" + \
      "(abs(LepGood_eta) >" + str(ebeeSplit) + "&& abs(LepGood_eta) <" + str(etaAcc) + "&& LepGood_sigmaIEtaIEta <" + str(WPcuts[WP]['sigmaEtaEta']['Endcap']) + "&& abs(LepGood_dEtaScTrkIn) <" + str(WPcuts[WP]['dEta']['Endcap']) + \
      "&& abs(LepGood_dPhiScTrkIn) <" + str(WPcuts[WP]['dPhi']['Endcap']) + "&& LepGood_hadronicOverEm <" + str(WPcuts[WP]['hOverE']['Endcap']) + "&& abs(LepGood_eInvMinusPInv) <" + str(WPcuts[WP]['ooEmooP']['Endcap']) + \
      "&& abs(LepGood_dxy) <" + str(WPcuts[WP]['d0']['Endcap']) + "&& abs(LepGood_dz) <" + str(WPcuts[WP]['dz']['Endcap']) + \
      "&& LepGood_convVeto == " + str(WPcuts[WP]['convVeto']['Barrel']) + "))"
elif removedCut == "convVeto":
   for WP in WPcuts.keys():
      cutSel[WP] = "(\
      (abs(LepGood_eta) <=" + str(ebeeSplit) + "&& LepGood_sigmaIEtaIEta <" + str(WPcuts[WP]['sigmaEtaEta']['Barrel']) + "&& abs(LepGood_dEtaScTrkIn) <" + str(WPcuts[WP]['dEta']['Barrel']) + \
      "&& abs(LepGood_dPhiScTrkIn) <" + str(WPcuts[WP]['dPhi']['Barrel']) + "&& LepGood_hadronicOverEm <" + str(WPcuts[WP]['hOverE']['Barrel']) + "&& abs(LepGood_eInvMinusPInv) <" + str(WPcuts[WP]['ooEmooP']['Barrel']) + \
      "&& abs(LepGood_dxy) <" + str(WPcuts[WP]['d0']['Barrel']) + "&& abs(LepGood_dz) <" + str(WPcuts[WP]['dz']['Barrel']) + "&& LepGood_lostHits <=" + str(WPcuts[WP]['MissingHits']['Barrel']) + ") ||" + \
      "(abs(LepGood_eta) >" + str(ebeeSplit) + "&& abs(LepGood_eta) <" + str(etaAcc) + "&& LepGood_sigmaIEtaIEta <" + str(WPcuts[WP]['sigmaEtaEta']['Endcap']) + "&& abs(LepGood_dEtaScTrkIn) <" + str(WPcuts[WP]['dEta']['Endcap']) + \
      "&& abs(LepGood_dPhiScTrkIn) <" + str(WPcuts[WP]['dPhi']['Endcap']) + "&& LepGood_hadronicOverEm <" + str(WPcuts[WP]['hOverE']['Endcap']) + "&& abs(LepGood_eInvMinusPInv) <" + str(WPcuts[WP]['ooEmooP']['Endcap']) + \
      "&& abs(LepGood_dxy) <" + str(WPcuts[WP]['d0']['Endcap']) + "&& abs(LepGood_dz) <" + str(WPcuts[WP]['dz']['Endcap']) + "&& LepGood_lostHits <=" + str(WPcuts[WP]['MissingHits']['Endcap']) + "))"
else: 
   print "!!! Wrong variable input."
   sys.exit(0)

#Efficiency
if plot == "efficiency":
   hists_total['None'] = makeHistVarBins(samples[sampleKey].tree, var, normFactor + "*" + weight + "*(" + preSel + "&&" + genSel + ")", bins)
   hists_total['None'].SetName("EleID")
   if removedCut == "None": hists_total['None'].SetTitle("Electron p_{T} Distributions for Various IDs (" + sample + " Sample)")
   else: hists_total['None'].SetTitle("Electron p_{T} Distributions for Various IDs without " + removedCut + " Cut (" + sample + " Sample)")
   hists_total['None'].GetXaxis().SetTitle("Generated Electron p_{T} / GeV")
   hists_total['None'].GetYaxis().SetTitle("Counts / GeV")
   hists_total['None'].GetXaxis().SetTitleOffset(1.2)
   hists_total['None'].GetYaxis().SetTitleOffset(1.2)
   hists_total['None'].SetFillColor(ROOT.kBlue-9)
   hists_total['None'].SetLineColor(ROOT.kBlack)
   hists_total['None'].SetLineWidth(3)
   hists_total['None'].Draw("hist")
   
   for WP in WPs:
      hists_passed[WP] = makeHistVarBins(samples[sampleKey].tree, var, normFactor + "*" + weight + "*(" + preSel + "&&" + genSel + "&&" + matchSel + "&& " + cutSel[WP] + ")", bins)
      hists_passed[WP].SetName("eleID_" + WP)
      hists_passed[WP].SetFillColor(0)
      hists_passed[WP].SetLineWidth(3)
      hists_passed[WP].Draw("histsame")
#MisID
elif plot == "misID" or plot == "misID2":
   for i,WP in enumerate(WPs):
      print WP
      hists_passed[WP] = makeHistVarBins(samples[sampleKey].tree, "LepGood_pt", normFactor + "*" + weight + "*(" + preSel + "&&" + recoSel + "&&" + misMatchSel + "&& (" + cutSel[WP] + "))", bins)
      if plot == "misID":
         hists_passed[WP].SetName("misID_" + WP)
         if i == 0:
            hists_total['None'] = makeHistVarBins(samples[sampleKey].tree, "LepGood_pt", normFactor + "*" + weight + "*(" + preSel + "&&" + recoSel + ")", bins)
            hists_total['None'].SetName("MisID")
         hists_total[WP] = makeHistVarBins(samples[sampleKey].tree, "LepGood_pt", normFactor + "*" + weight + "*(" + preSel + "&&" + recoSel + "&& (" + cutSel[WP] + "))", bins)
      if plot == "misID2": 
         hists_passed[WP].SetName("misID2_" + WP)
         if i == 0:
            hists_total['None'] = makeHistVarBins(samples[sampleKey].tree, "LepGood_pt", normFactor + "*" + weight + "*(" + preSel + "&&" + recoSel + "&&" + misMatchSel + ")", bins)
            hists_total['None'].SetName("MisID2")
      if i == 0: hists_total['None'].Draw("hist")
      hists_passed[WP].SetFillColor(0)
      hists_passed[WP].SetLineWidth(3)
      hists_passed[WP].Draw("histsame")

   if removedCut == "None": hists_total['None'].SetTitle(hists_total['None'].GetName() +": Fake (Non-Prompt) Electron p_{T} Distributions for Various IDs (" + sample + " Sample)")
   else: hists_total['None'].SetTitle(hists_total['None'].GetName() +": Fake (Non-Prompt) Electron p_{T} Distributions for Various IDs without " + removedCut + " Cut (" + sample + " Sample)")
   hists_total['None'].GetXaxis().SetTitle("Reconstructed Electron p_{T} / GeV")
   hists_total['None'].GetYaxis().SetTitle("Counts / GeV")
   hists_total['None'].GetXaxis().SetTitleOffset(1.2)
   hists_total['None'].GetYaxis().SetTitleOffset(1.2)
   hists_total['None'].SetFillColor(ROOT.kBlue-9)
   hists_total['None'].SetLineColor(ROOT.kBlack)
   hists_total['None'].SetLineWidth(3)

else:
   print "!!! Wrong plot input."
   sys.exit(0)

ROOT.gPad.SetLogy()
ROOT.gPad.Modified()
ROOT.gPad.Update()

alignStats(hists_total['None'])

#Colours
hists_passed['Veto'].SetLineColor(ROOT.kGreen+3)
hists_passed['Loose'].SetLineColor(ROOT.kBlue+1)
hists_passed['Medium'].SetLineColor(ROOT.kOrange-2)
hists_passed['Tight'].SetLineColor(ROOT.kRed+1)

ROOT.gPad.Modified()
ROOT.gPad.Update()

l1 = makeLegend()
if plot == "efficiency":
   l1.AddEntry("EleID", "Generated Electron p_{T}", "F")
   l1.AddEntry("eleID_Veto", "Veto ID", "F")
   l1.AddEntry("eleID_Loose", "Loose ID", "F")
   l1.AddEntry("eleID_Medium", "Medium ID", "F")
   l1.AddEntry("eleID_Tight", "Tight ID", "F")
elif plot == "misID":
   l1.AddEntry("MisID", "Reconstructed Electron p_{T}", "F")
   l1.AddEntry("misID_Veto", "Veto ID", "F")
   l1.AddEntry("misID_Loose", "Loose ID", "F")
   l1.AddEntry("misID_Medium", "Medium ID", "F")
   l1.AddEntry("misID_Tight", "Tight ID", "F")
elif plot == "misID2":
   l1.AddEntry("MisID2", "Reconstructed Electron p_{T}", "F")
   l1.AddEntry("misID2_Veto", "Veto ID", "F")
   l1.AddEntry("misID2_Loose", "Loose ID", "F")
   l1.AddEntry("misID2_Medium", "Medium ID", "F")
   l1.AddEntry("misID2_Tight", "Tight ID", "F")

#Electron MVA IDs
#if mvaWPs == 1:
#   mvaCuts = {'WP90':\
#             {'EB1_lowPt':-0.083313, 'EB2_lowPt':-0.235222, 'EE_lowPt':-0.67099, 'EB1':0.913286, 'EB2':0.805013, 'EE':0.358969},\
#              'WP80':\
#             {'EB1_lowPt':0.287435, 'EB2_lowPt':0.221846, 'EE_lowPt':-0.303263, 'EB1':0.967083, 'EB2':0.929117, 'EE':0.726311}}
#   
#   for WP in mvaCuts.keys():
#      mvaSel = "(\
#      (LepGood_pt <=" + str(ptSplit) + "&& abs(LepGood_eta) < " + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(mvaCuts[WP]['EB1_lowPt']) + ") || \
#      (LepGood_pt <=" + str(ptSplit) + "&& abs(LepGood_eta) >=" + str(ebSplit) + "&& abs(LepGood_eta) <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(mvaCuts[WP]['EB2_lowPt']) + ") || \
#      (LepGood_pt <=" + str(ptSplit) + "&& abs(LepGood_eta) >=" + str(ebeeSplit) + "&& abs(LepGood_eta) <" + str(etaAcc) + "&& LepGood_mvaIdSpring15 >=" + str(mvaCuts[WP]['EE_lowPt']) + ") || \
#      (LepGood_pt >" + str(ptSplit) + "&& abs(LepGood_eta) <" + str(ebSplit) + "&& LepGood_mvaIdSpring15 >=" + str(mvaCuts[WP]['EB1']) + ") || \
#      (LepGood_pt >" + str(ptSplit) + "&& abs(LepGood_eta) >=" + str(ebSplit) + "&& abs(LepGood_eta) <" + str(ebeeSplit) + "&& LepGood_mvaIdSpring15 >=" + str(mvaCuts[WP]['EB2']) + ") || \
#      (LepGood_pt >" + str(ptSplit) + "&& abs(LepGood_eta) >=" + str(ebeeSplit) + "&& abs(LepGood_eta) <" + str(etaAcc) + "&& LepGood_mvaIdSpring15 >=" + str(mvaCuts[WP]['EE']) + "))"
#      if plot == "efficiency": 
#         hists_passed[WP] = makeHistVarBins(samples[sampleKey].tree, var, normFactor + "*" + weight + "*(" + preSel + "&&" + genSel + "&&" + matchSel + "&&" + mvaSel + ")", bins)
#         hists_passed[WP].SetName("eleID_" + WP)
#      if plot == "misID" or plot == "misID2":
#         hists_passed[WP] = makeHistVarBins(samples[sampleKey].tree, "LepGood_pt", normFactor + "*" + weight + "*(" + preSel + "&&" + recoSel + "&&" + misMatchSel + "&& (" + mvaSel + "))", bins)
#         if plot == "misID":
#            hists_passed[WP].SetName("misID_" + WP)
#            hists_total[WP] = makeHistVarBins(samples[sampleKey].tree, "LepGood_pt", normFactor + "*" + weight + "*(" + preSel + "&&" + recoSel + "&& (" + mvaSel + "))", bins)
#         if plot == "misID2": 
#            hists_passed[WP].SetName("misID2_" + WP)
#       
#      hists_passed[WP].SetFillColor(0)
#      hists_passed[WP].SetLineWidth(3)
#      hists_passed[WP].Draw("histsame")
#   
#   hists_passed['WP90'].SetLineColor(ROOT.kMagenta+2)
#   hists_passed['WP80'].SetLineColor(ROOT.kAzure+5)
#
#   ROOT.gPad.Modified()
#   ROOT.gPad.Update()
#   
#   if plot == "efficiency":
#      l1.AddEntry("eleID_WP90", "MVA ID (WP90)", "F")
#      l1.AddEntry("eleID_WP80", "MVA ID (WP80)", "F")
#   if plot == "misID":
#      l1.AddEntry("misID_WP90", "MVA ID (WP90)", "F")
#      l1.AddEntry("misID_WP80", "MVA ID (WP80)", "F")
#   if plot == "misID2":
#      l1.AddEntry("misID2_WP90", "MVA ID (WP90)", "F")
#      l1.AddEntry("misID2_WP80", "MVA ID (WP80)", "F")

ROOT.gPad.Modified()
ROOT.gPad.Update()

l1.Draw()

################################################################################################################################################################################
#Efficiency curves
c1.cd(2)

effs = {}

#Efficiency
for WP in sorted(hists_passed.keys()):
   if plot == "efficiency" or plot == "misID2": effs[WP] = ROOT.TEfficiency(hists_passed[WP], hists_total['None'])
   elif plot == "misID": effs[WP] = ROOT.TEfficiency(hists_passed[WP], hists_total[WP])
   effs[WP].SetName("eff_" + WP)
   effs[WP].SetMarkerStyle(33)
   effs[WP].SetMarkerSize(1.5)
   effs[WP].SetLineWidth(2)
   if WP == 'Loose': effs['Loose'].Draw("AP")
   elif WP != 'Loose': effs[WP].Draw("sameP")

if plot == "efficiency": 
   if removedCut == "None": effs['Loose'].SetTitle("Electron ID Efficiencies (" + sample + " Sample) ; Generated Electron p_{T} / GeV ; Efficiency")
   else: effs['Loose'].SetTitle("Electron ID Efficiencies without " + removedCut + " Cut (" + sample + " Sample) ; Generated Electron p_{T} / GeV ; Efficiency")
elif plot == "misID" or plot == "misID2": 
   if removedCut == "None": effs['Loose'].SetTitle("Electron Mismatch Efficiencies for Various IDs (" + sample + " Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency")
   else: effs['Loose'].SetTitle("Electron Mismatch Efficiencies for Various IDs without " + removedCut + " Cut (" + sample + " Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency")
effs['Loose'].SetMarkerColor(ROOT.kBlue+1)
effs['Loose'].SetLineColor(ROOT.kBlue+1)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
ROOT.gPad.Modified()
ROOT.gPad.Update()
effs['Loose'].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)
effs['Loose'].GetPaintedGraph().SetMinimum(0)
effs['Loose'].GetPaintedGraph().SetMaximum(1)
effs['Loose'].GetPaintedGraph().GetXaxis().CenterTitle()
effs['Loose'].GetPaintedGraph().GetYaxis().CenterTitle()

ROOT.gPad.Modified()
ROOT.gPad.Update()

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

#if mvaWPs == 1:
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

ROOT.gPad.Modified()
ROOT.gPad.Update()
c1.Modified()
c1.Update()

#Write to file
if save == 1: #web address: http://www.hephy.at/user/mzarucki/plots/electronReconstruction/electronIdEfficiency
   if removedCut == "None": savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronID/nMinus1/relEff/allCuts/" + plot
   else: savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronID/nMinus1/relEff/no_" + removedCut + "/" + plot
   
   if not os.path.exists(savedir):
      os.makedirs(savedir)
   if not os.path.exists(savedir + "/root"):
      os.makedirs(savedir + "/root")
   if not os.path.exists(savedir + "/pdf"):
      os.makedirs(savedir + "/pdf")

   #Save to Web
   if removedCut == "None":
      c1.SaveAs(savedir + "/" + plot + "_" + sample + z + ".png")
      c1.SaveAs(savedir + "/root/" + plot + "_" + sample + z + ".root")
      c1.SaveAs(savedir + "/pdf/" + plot + "_" + sample + z + ".pdf")
   else:
      c1.SaveAs(savedir + "/" + plot + "_no_" + removedCut + "_" + sample + z + ".png")
      c1.SaveAs(savedir + "/root/" + plot + "_no_" + removedCut + "_" + sample + z + ".root")
      c1.SaveAs(savedir + "/pdf/" + plot + "_no_" + removedCut + "_" + sample + z + ".pdf")
