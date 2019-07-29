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
parser.add_argument("--dataset",   help = "Primary dataset",   type = str, default = "SingleMuon")
parser.add_argument("--dataEra",   help = "Data era",          type = str, default = "")
parser.add_argument("--options",   help = "Options",           type = str, default = ['noweight'], nargs = '+')
parser.add_argument("--year",      help = "Year",              type = str, default = "2018")
parser.add_argument("--lepTag",    help = "Lepton tag",        type = str, default = "def", choices = ["bare", "loose", "def"])
parser.add_argument("--region",    help = "Region",            type = str, default = "none")
parser.add_argument("--minLepPt",  help = "Lower lepton pT cut",   type = str, default = None, choices = ['30', '40'])
parser.add_argument("--maxLepPt",  help = "Upper lepton pT cut",   type = str, default = None, choices = ['30', '40', '50'])
parser.add_argument("--maxElePt",  help = "Upper electron pT cut", type = str, default = None, choices = ['30', '40', '50'])
parser.add_argument("--var1",      help = "Variable 1",        type = str, default = "leadBasJetPt")
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
dataset  = args.dataset
dataEra  = args.dataEra
options  = args.options
year     = args.year
lepTag   = args.lepTag
region   = args.region
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
    plateauCuts = {'lepPt':15, 'metPt':250, 'leadBasJetPt':150}
elif dataset == 'SingleMuon':
    skim = 'oneLepTight'
    denTrig = ['HLT_IsoMu24', 'HLT_IsoMu27']
    plateauCuts = {'lepPt':30, 'metPt':250, 'leadBasJetPt':150}
elif dataset == 'EGamma':
    denTrig = 'HLT_Ele32_WPTight_Gsf'
    plateauCuts = {'lepPt':15, 'metPt':250, 'leadBasJetPt':150}
elif dataset == 'Charmonium':
    skim = 'twoLep'
    denTrig = ['HLT_DoubleMu4_3_Jpsi', 'HLT_Dimuon25_Jpsi', 'HLT_Dimuon25_Jpsi_noCorrL1', 'HLT_Dimuon0_Jpsi3p5_Muon2', 'HLT_DoubleMu2_Jpsi_DoubleTkMu0_Phi', 'HLT_DoubleMu2_Jpsi_DoubleTrk1_Phi1p05']
elif dataset == 'DoubleMuon':
    skim = 'twoLepLoose'
    denTrig = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL", "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ", "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL", "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ", "HLT_TkMu17_TrkIsoVVL_TkMu8_TrkIsoVVL", "HLT_TkMu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ", "HLT_Mu30_TkMu11"]
else:
    print "Wrong dataset. Exiting."
    sys.exit()

plateauTag = 'plateau_lepPt%s_metPt%s_leadBasJetPt%s'%(plateauCuts['lepPt'], plateauCuts['metPt'], plateauCuts['leadBasJetPt'])

if type(denTrig) == type([]):
    denTrig = '(%s)'%'||'.join(denTrig)

# cut and weight options
cutWeightOptions = getCutWeightOptions(
    lepCol = 'Lepton',
    lep = 'mu',
    lepTag = lepTag,
    year = year,
    dataset = dataset,
    campaign = campaign,
    options = options
    )

lumiTag = makeLumiTag(cutWeightOptions['settings']['lumis'][year][dataset_name], latex = True)

CMS_lumi.lumi_13TeV = lumiTag
CMS_lumi.extraText = "Preliminary"
CMS_lumi.relPosX = 0.12
#CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)


sampleDefPath = 'Workspace.DegenerateStopAnalysis.samples.nanoAOD_postProcessed.nanoAOD_postProcessed_' + era
sampleDef = importlib.import_module(sampleDefPath)

if dataset in ['EGamma', 'Charmonium']:
    ppDir = "/afs/hephy.at/data/mzarucki02/nanoAOD/DegenerateStopAnalysis/postProcessing/processing_RunII_v6_2/nanoAOD_v6_2-0"
elif dataset in ['SingleMuon', 'DoubleMuon']:
    if "metNoMuPt" in [var1, var2]: 
        ppDir = "/afs/hephy.at/data/mzarucki02/nanoAOD/DegenerateStopAnalysis/postProcessing/processing_RunII_v6_5/nanoAOD_v6_5-1"
    else:
        ppDir = "/afs/hephy.at/data/mzarucki02/nanoAOD/DegenerateStopAnalysis/postProcessing/processing_RunII_v6_3/nanoAOD_v6_3-0"
elif dataset in ['MET']:
    ppDir = "/afs/hephy.at/data/mzarucki02/nanoAOD/DegenerateStopAnalysis/postProcessing/processing_RunII_v6_1/nanoAOD_v6_1-0"
else:
    print "Wrong dataset. Exiting."
    sys.exit()

mc_path     = ppDir + "/Autumn18_14Dec2018"
data_path   = ppDir + "/Run2018_14Dec2018"
signal_path = mc_path

PP = sampleDef.nanoPostProcessed(mc_path, signal_path, data_path)
samples = getSamples(PP = PP, skim = skim, sampleList = samplesList, scan = False, useHT = True, getData = True, settings = cutWeightOptions['settings'])

# cuts
#alt_vars = {'lepIndex':{'var':'Index{lepCol}_{lep}{lt}', 'latex':''}} # considering leading loose lepton
#alt_vars = {'lepPt':{'var':'{lepPt_loose}', 'latex':''}} # considering leading loose lepton

cuts_weights = CutsWeights(samples, cutWeightOptions)#, alternative_vars = alt_vars)
regDef = region
    
regDef = cuts_weights.cuts.addCut(regDef, 'lepEta_lt_1p5')
regDef = cuts_weights.cuts.addCut(regDef, 'leadBasJetEta_lt_2p4')

if minLepPt:
    regDef = cuts_weights.cuts.addCut(regDef, 'lepPt_gt_' + minLepPt)

if maxLepPt:
    regDef = cuts_weights.cuts.addCut(regDef, 'lepPt_lt_' + maxLepPt)

if maxElePt:
    regDef = cuts_weights.cuts.addCut(regDef, 'bareElePt_lt_' + maxLepPt)

#if region == "Zpeak":
#    regDef = cuts_weights.cuts.addCut(regDef, 'ptZ_lt_50')
    
cuts_weights.cuts._update(reset = False)
cuts_weights._update()

# save
if save:
    tag = samples[samples.keys()[0]].dir.split('/')[9]
    suff = '_' + '_'.join([tag, dataset, region])
    savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/softTrigEff/%s/%s/softTrigEff_2D/%s/%s/%s/%s"%(tag, year, lepTag, dataset_name, regDef, plateauTag)

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

varStrings = cuts_weights.cuts.vars_dict_format
varNames = {'metPt':"E^{miss}_{T}", 'caloMetPt':"Calo. E^{miss}_{T}", 'metNoMuPt':"E^{miss}_{T} (#mu Sub.)", 'leadBasJetPt':"Leading Jet p_{T}", 'lepPt':"Muon p_{T}"} 
plateauCutStrings = {key:varStrings[key] + " > " + str(val) for key,val in plateauCuts.iteritems()} 

regCutStr = getattr(cuts_weights.cuts, regDef).combined

# histograms
dens = {}
nums = {}

xmax  = {'metPt':500, 'ht':500, 'leadBasJetPt':300, 'lepPt':80}
nbins = {'metPt':100, 'ht':100, 'leadBasJetPt':60,  'lepPt':80}

xmax['caloMetPt'] = xmax['metPt']
xmax['metNoMuPt'] = xmax['metPt']

nbins['caloMetPt'] = nbins['metPt']
nbins['metNoMuPt'] = nbins['metPt']

hists = {}

for trig in triggers:
    makeDir("%s/%s/histos"%(savedir, trig))
    makeDir("%s/%s/root"%(savedir, trig))
    makeDir("%s/%s/pdf"%(savedir, trig))

    if trig == 'OR_ALL':
        trigCut = '(%s)'%'||'.join(allTrig)
    else:
        trigCut = trig

    hists[trig] = {}

    denSelList = ["Flag_Filters", "run >= 315974", regCutStr, denTrig]
    # plateau cuts
    for cut in plateauCuts:
        if cut not in [var1, var2]: # NOTE: careful with CaloMET
            denSelList.append(plateauCutStrings[cut])

    denSel = combineCutsList(denSelList)
    numSel = combineCuts(denSel, trigCut) 
    
    hists[trig]['dens'] = make2DHist(samples[dataset_name].tree, varStrings[var1], varStrings[var2], denSel, nbins[var1], 0, xmax[var1], nbins[var2], 0, xmax[var2]) 
    hists[trig]['nums'] = make2DHist(samples[dataset_name].tree, varStrings[var1], varStrings[var2], numSel, nbins[var1], 0, xmax[var1], nbins[var2], 0, xmax[var2]) 

    suff2 = '_%s_%s_%s%s'%(trig, var1, var2, suff)
    hists[trig]['dens'].SetName('den' + suff2)   
    hists[trig]['nums'].SetName('num' + suff2)   
 
    canv = ROOT.TCanvas("Canvas " + suff2, "Canvas " + suff2, 1500, 1500)
    #canv.SetGrid()
    canv.SetLogy(logy)

    f = ROOT.TFile('%s/%s/histos/histos%s.root'%(savedir, trig, suff2), "recreate")

    # Histograms
    hists[trig]['dens'].Write()
    hists[trig]['nums'].Write()
    f.Close()

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
