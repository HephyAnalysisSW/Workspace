# softTrigEff_2D.py

import ROOT
import os, sys
import argparse
import importlib

import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import setup_style, makeLumiTag, makeDir
from Workspace.DegenerateStopAnalysis.tools.degCuts import CutsWeights
from Workspace.DegenerateStopAnalysis.tools.degPlots import Plots
from Workspace.DegenerateStopAnalysis.samples.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.samplesInfo import getCutWeightOptions

from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *

import Workspace.DegenerateStopAnalysis.samples.samplesInfo as samplesInfo
import Workspace.HEPHYPythonTools.CMS_lumi as CMS_lumi

# set style
setup_style()

#ROOT.gStyle.SetOptStat(0) # 0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis
ROOT.gStyle.SetOptFit(0) # 1111 prints fits results on plot
ROOT.gStyle.SetPadRightMargin(0.18)
ROOT.gStyle.SetPadLeftMargin(0.15)
ROOT.gStyle.SetPadBottomMargin(0.12)
#ROOT.gStyle.SetPadTopMargin(0.14)
ROOT.gStyle.SetTitleSize(0.04, "XYZ")
ROOT.gStyle.SetTitleXOffset(1)
#ROOT.gStyle.SetTitleYOffset(1.3)
ROOT.gStyle.SetLabelSize(0.04, "XYZ")

# input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--triggers",  help = "Triggers",          type = str, default = "",           nargs = "+")
parser.add_argument("--samplesTag", help = "Samples tag",           type = str, default = "nanoAOD_v6_3-0")
parser.add_argument("--dataset",   help = "Primary dataset",   type = str, default = "SingleMuon")
parser.add_argument("--dataEra",   help = "Data era",          type = str, default = "")
parser.add_argument("--year",      help = "Year",              type = str, default = "2018")
parser.add_argument("--lepTag",    help = "Lepton tag",        type = str, default = "def", choices = ["bare", "loose", "def"])
parser.add_argument("--region",    help = "Region",            type = str, default = "none")
parser.add_argument("--extraCuts",  help = "Extra cuts",            type = str, default = "plus_lepEta_lt_1p5_plus_leadJetEta_lt_2p5")
parser.add_argument("--minLepPt",  help = "Lower lepton pT cut",   type = str, default = None, choices = ['30', '40'])
parser.add_argument("--maxLepPt",  help = "Upper lepton pT cut",   type = str, default = None, choices = ['30', '40', '50'])
parser.add_argument("--maxElePt",  help = "Upper electron pT cut", type = str, default = None, choices = ['30', '40', '50'])
parser.add_argument("--var1",      help = "Variable 1",        type = str, default = "leadJetPt")
parser.add_argument("--var2",      help = "Variable 2",        type = str, default = "metPt")
parser.add_argument("--doName",    help = "Write name",        type = int, default = 0)
parser.add_argument("--logy",      help = "Toggle logy",       type = int, default = 0)
parser.add_argument("--save",      help = "Toggle save",       type = int, default = 1)
parser.add_argument("--verbose",   help = "Verbosity switch",  type = int, default = 0)
args = parser.parse_args()
if not len(sys.argv) > 1:
    print makeLine()
    print "No arguments given. Using default settings."
    print makeLine()

# arguments
triggers = args.triggers
samplesTag = args.samplesTag
dataset  = args.dataset
dataEra  = args.dataEra
year     = args.year
lepTag   = args.lepTag
region   = args.region
extraCuts  = args.extraCuts
minLepPt  = args.minLepPt
maxLepPt  = args.maxLepPt
maxElePt  = args.maxElePt
var1     = args.var1
var2     = args.var2
doName   = args.doName
logy     = args.logy
save     = args.save
verbose  = args.verbose

# samples
if year == "2016":
    era = "Summer16"
    campaign = "05Feb2018"
elif year == "2017":
    era = "Fall17"
    campaign = "14Dec2018"
elif year == "2018":
    era = "Autumn18"
    campaign = "14Dec2018"
else:
    print "Wrong year %s. Exiting."%year
    sys.exit()

dataset_name = "%s_Run%s%s_%s"%(dataset, year, dataEra, campaign)
samplesList = [dataset_name]

skim = 'oneLep'
if dataset == 'MET':
    denTrig = 'HLT_PFMET120_PFMHT120_IDTight'
    plateauCuts = {'lepPt':15, 'metPt':250, 'leadJetPt':150}
elif dataset == 'SingleMuon':
    skim = 'oneLepTight'
    denTrig = ['HLT_IsoMu24', 'HLT_IsoMu27']
    plateauCuts = {'lepPt':30, 'metPt':250, 'leadJetPt':150}
elif dataset == 'EGamma':
    denTrig = 'HLT_Ele32_WPTight_Gsf'
    plateauCuts = {'lepPt':15, 'metPt':250, 'leadJetPt':150}
elif dataset == 'Charmonium':
    skim = 'twoLep'
    denTrig = ['HLT_DoubleMu4_3_Jpsi', 'HLT_Dimuon25_Jpsi', 'HLT_Dimuon25_Jpsi_noCorrL1', 'HLT_Dimuon0_Jpsi3p5_Muon2', 'HLT_DoubleMu2_Jpsi_DoubleTkMu0_Phi', 'HLT_DoubleMu2_Jpsi_DoubleTrk1_Phi1p05']
elif dataset == 'DoubleMuon':
    skim = 'twoLepLoose'
    denTrig = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL", "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ", "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL", "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ", "HLT_TkMu17_TrkIsoVVL_TkMu8_TrkIsoVVL", "HLT_TkMu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ", "HLT_Mu30_TkMu11"]
else:
    print "Wrong dataset. Exiting."
    sys.exit()

plateauTag = 'plateau_lepPt%s_metPt%s_leadJetPt%s'%(plateauCuts['lepPt'], plateauCuts['metPt'], plateauCuts['leadJetPt'])

lumiTag = makeLumiTag(samplesInfo.lumis[year][dataset_name], latex = True)

CMS_lumi.lumi_13TeV = lumiTag
CMS_lumi.extraText = "Preliminary"
CMS_lumi.relPosX = 0.12
#CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

regDef = region + "_" + extraCuts

# save
if save:
    suff = '_' + '_'.join([samplesTag, dataset, region])
    baseSavedir = "/afs/hephy.at/user/m/mzarucki/www/plots/softTrigEff_NEW/%s/%s/softTrigEff_2D/%s/%s/%s/%s"%(samplesTag, year, lepTag, dataset_name, regDef, plateauTag)
    savedir = baseSavedir + '/finalPlots'

allTrig = [
    'HLT_Mu3er1p5_PFJet100er2p5_PFMET70_PFMHT70_IDTight',
    'HLT_Mu3er1p5_PFJet100er2p5_PFMET80_PFMHT80_IDTight',
    'HLT_Mu3er1p5_PFJet100er2p5_PFMET90_PFMHT90_IDTight',
    'HLT_Mu3er1p5_PFJet100er2p5_PFMET100_PFMHT100_IDTight',
    'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu70_PFMHTNoMu70_IDTight',
    'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu80_PFMHTNoMu80_IDTight',
    'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu90_PFMHTNoMu90_IDTight',
    'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu100_PFMHTNoMu100_IDTight'
    ]

if not triggers:
    triggers = allTrig

varNames = {'metPt':"E^{miss}_{T}", 'caloMetPt':"Calo. E^{miss}_{T}", 'leadJetPt':"Leading Jet p_{T}", 'lepPt':"Muon p_{T}"} 

# histograms
dens = {}
nums = {}

xmax  = {'metPt':500, 'caloMetPt':500, 'ht':500, 'leadJetPt':300, 'lepPt':80}
nbins = {'metPt':100, 'caloMetPt':100, 'ht':100, 'leadJetPt':60,  'lepPt':80}

hists = {}

for trig in triggers:
    makeDir("%s/%s/histos"%(savedir, trig))
    makeDir("%s/%s/root"%(savedir, trig))
    makeDir("%s/%s/pdf"%(savedir, trig))

    hists[trig] = {}
    
    suff2 = '_%s_%s_%s%s'%(trig, var1, var2, suff)
        
    histosDir = '%s/%s/histos/histos%s.root'%(baseSavedir, trig, suff2)

    if not dataEra:
        hists[trig]['dens'] = ROOT.TH2D("den" + suff2, "den" + suff2, nbins[var1], 0, xmax[var1], nbins[var2], 0, xmax[var2])
        hists[trig]['nums'] = ROOT.TH2D("num" + suff2, "num" + suff2, nbins[var1], 0, xmax[var1], nbins[var2], 0, xmax[var2])

        for era in ['A', 'B', 'C', 'D']:
            try:
                f = ROOT.TFile(histosDir.replace('Run2018', 'Run2018'+era), "read")
                d = f.Get("den" + suff2)
                n = f.Get("num" + suff2)

                hists[trig]['dens'].Add(d)
                hists[trig]['nums'].Add(n)
            except TypeError as exp:
                print "!!! Missing histograms file for era", era, "!!!"
                continue
    else:
        f = ROOT.TFile(histosDir, "read")

        hists[trig]['dens'] = f.Get("den" + suff2)
        hists[trig]['nums'] = f.Get("num" + suff2)
        
 
    canv = ROOT.TCanvas("Canvas " + suff2, "Canvas " + suff2, 1500, 1500)
    #canv.SetGrid()
    canv.SetLogy(logy)

    # Efficiency
    hists[trig]['eff'] = hists[trig]['nums'].Clone()
    hists[trig]['eff'].Divide(hists[trig]['dens'])
    hists[trig]['eff'].Draw('COLZ')
        
    CMS_lumi.CMS_lumi(canv, 4, 0) # draw the lumi text on the canvas
    
    hists[trig]['eff'].GetXaxis().SetTitle("%s [GeV]"%varNames[var1])
    hists[trig]['eff'].GetYaxis().SetTitle("%s [GeV]"%varNames[var2])
    hists[trig]['eff'].GetZaxis().SetTitle("Trigger Efficiency")
    hists[trig]['eff'].GetZaxis().RotateTitle(1)
    hists[trig]['eff'].GetYaxis().SetTitleOffset(1.4)
    hists[trig]['eff'].GetZaxis().SetTitleOffset(1.4)
    
    hists[trig]['eff'].GetZaxis().SetRangeUser(0, 1)

    ROOT.gPad.Modified()
    ROOT.gPad.Update()

    if doName:
        latex2 = ROOT.TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.025)
        latex2.SetTextColor(ROOT.kRed+1)
        latex2.DrawLatex(0.15, 0.87, trig)

    #Save canvas
    canv.SaveAs(     "%s/%s/trigEff_2D-%s-%s_%s_%s.png"%( savedir, trig, var1, var2, trig, suff))
    canv.SaveAs( "%s/%s/pdf/trigEff_2D-%s-%s_%s_%s.pdf"%( savedir, trig, var1, var2, trig, suff))
    canv.SaveAs("%s/%s/root/trigEff_2D-%s-%s_%s_%s.root"%(savedir, trig, var1, var2, trig, suff))
