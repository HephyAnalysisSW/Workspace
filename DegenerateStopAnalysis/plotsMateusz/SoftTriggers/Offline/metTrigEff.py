# metTrigEff.py

import ROOT
import os, sys
import argparse
import importlib

import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import makeHist
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import setup_style, makeLumiTag, makeDir
from Workspace.DegenerateStopAnalysis.tools.degCuts import CutsWeights
from Workspace.DegenerateStopAnalysis.tools.degPlots import Plots
from Workspace.DegenerateStopAnalysis.samples.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.samplesInfo import getCutWeightOptions

import Workspace.HEPHYPythonTools.CMS_lumi as CMS_lumi

# set style
setup_style()

#ROOT.gStyle.SetOptStat(0) # 0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis
ROOT.gStyle.SetOptFit(0) # 1111 prints fits results on plot
ROOT.gStyle.SetPadRightMargin(0.14)
ROOT.gStyle.SetPadLeftMargin(0.12)
ROOT.gStyle.SetPadBottomMargin(0.12)
#ROOT.gStyle.SetPadTopMargin(0.14)
ROOT.gStyle.SetTitleSize(0.04, "XYZ")
ROOT.gStyle.SetLabelSize(0.04, "XYZ")

# input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--triggers",   help = "Triggers",              type = str, default = "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60",           nargs = "+")
parser.add_argument("--dataset",    help = "Primary dataset",       type = str, default = "SingleMuon")
parser.add_argument("--dataEra",    help = "Data era",              type = str, default = "B")
parser.add_argument("--options",    help = "Options",               type = str, default = ['noweight'], nargs = '+')
parser.add_argument("--year",       help = "Year",                  type = str, default = "2018")
parser.add_argument("--lepTag",     help = "Lepton tag",            type = str, default = "def", choices = ["bare", "loose", "def"])
parser.add_argument("--region",     help = "Region",                type = str, default = "none")
parser.add_argument("--minLepPt",   help = "Lower lepton pT cut",   type = str, default = None, choices = ['30', '40', '50'])
parser.add_argument("--maxLepPt",   help = "Upper lepton pT cut",   type = str, default = None, choices = ['30', '40', '50'])
parser.add_argument("--maxElePt",   help = "Upper electron pT cut", type = str, default = None, choices = ['30', '40', '50'])
parser.add_argument("--maxPtZ",     help = "Upper ptZ cut",         type = str, default = None, choices = ['20', '30', '50'])
parser.add_argument("--applyJetId", help = "Apply jet ID",          type = int, default = 0)
parser.add_argument("--oneLep",     help = "Exactly one lepton",    type = int, default = 1)
parser.add_argument("--htCut",      help = "HT cut",                type = str, default = "")
parser.add_argument("--variables",  help = "Variables to plot",     type = str, default = ["metNoMuPt"],           nargs = '+')
parser.add_argument("--doFit",      help = "Do fit",                type = int, default = 1)
parser.add_argument("--doName",     help = "Write name",            type = int, default = 0)
parser.add_argument("--doLegend",   help = "Draw legend",           type = int, default = 1)
parser.add_argument("--doBox",      help = "Draw box",              type = int, default = 0)
parser.add_argument("--logy",       help = "Toggle logy",           type = int, default = 0)
parser.add_argument("--save",       help = "Toggle save",           type = int, default = 1)
parser.add_argument("--verbose",    help = "Verbosity switch",      type = int, default = 0)
args = parser.parse_args()
if not len(sys.argv) > 1:
    print makeLine()
    print "No arguments given. Using default settings."
    print makeLine()

# arguments
triggers   = args.triggers
dataset    = args.dataset
dataEra    = args.dataEra
options    = args.options
year       = args.year
lepTag     = args.lepTag
region     = args.region
minLepPt   = args.minLepPt
maxLepPt   = args.maxLepPt
maxElePt   = args.maxElePt
maxPtZ     = args.maxPtZ
applyJetId = args.applyJetId
oneLep     = args.oneLep
htCut      = args.htCut
variables  = args.variables
doFit      = args.doFit
doName     = args.doName
doLegend   = args.doLegend
doBox      = args.doBox
logy       = args.logy
save       = args.save
verbose    = args.verbose

if 'metPt' in variables or 'metNoMuPt' in variables:
    doFit = False

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
    if not variables:
        variables = ['lepPt', 'leadBasJetPt']
    #plateauCuts = {'lepPt':15, 'metPt':250, 'leadBasJetPt':150}
elif dataset == 'SingleMuon':
    skim = 'oneLepTight'
    denTrig = ['HLT_IsoMu24', 'HLT_IsoMu27']
    if not variables:
        variables = ['metPt', 'metNoMuPt']
    #plateauCuts = {'lepPt':30, 'metPt':250, 'leadBasJetPt':150}
else:
    print "Wrong dataset. Exiting."
    sys.exit()

#plateauTag = 'plateau_lepPt%s_metPt%s_leadBasJetPt%s'%(plateauCuts['lepPt'], plateauCuts['metPt'], plateauCuts['leadBasJetPt'])

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

if dataset in ['SingleMuon', 'DoubleMuon']:
    ppDir = "/afs/hephy.at/data/mzarucki02/nanoAOD/DegenerateStopAnalysis/postProcessing/processing_RunII_v6_5/nanoAOD_v6_5-1"

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
    
#regDef = cuts_weights.cuts.addCut(regDef, 'lepEta_lt_1p5')
#regDef = cuts_weights.cuts.addCut(regDef, 'leadBasJetEta_lt_2p4')

if minLepPt:
    regDef = cuts_weights.cuts.addCut(regDef, 'lepPt_gt_' + minLepPt)

if maxLepPt:
    regDef = cuts_weights.cuts.addCut(regDef, 'lepPt_lt_' + maxLepPt)

if maxElePt:
    regDef = cuts_weights.cuts.addCut(regDef, 'bareElePt_lt_' + maxLepPt)

if applyJetId:
    regDef = cuts_weights.cuts.addCut(regDef, 'leadBasJetId')

if oneLep:
    regDef = cuts_weights.cuts.addCut(regDef, 'exact1Lep')

if htCut:
    regDef = cuts_weights.cuts.addCut(regDef, 'HT' + htCut)

if region == "Zpeak":
    regDef = cuts_weights.cuts.addCut(regDef, 'ptZ_lt_' + maxPtZ)

cuts_weights.cuts._update(reset = False)
cuts_weights._update()

# save
if save:
    tag = samples[samples.keys()[0]].dir.split('/')[9]
    suff = '_' + '_'.join([tag, dataset, region])
    savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/metTrigEff/%s/%s/metTrigEff/%s/%s/%s"%(tag, year, lepTag, dataset_name, regDef)#, plateauTag)

allTrig = [
    'HLT_PFMET110_PFMHT110_IDTight',
    'HLT_PFMET120_PFMHT120_IDTight',
    'HLT_PFMET130_PFMHT130_IDTight',
    'HLT_PFMET140_PFMHT140_IDTight',

    'HLT_PFMETNoMu110_PFMHTNoMu110_IDTight',
    'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight',
    'HLT_PFMETNoMu130_PFMHTNoMu130_IDTight',
    'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight',
    
    'HLT_PFMET120_PFMHT120_IDTight_PFHT60',
    'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60',
    ]

if not triggers:
    triggers = allTrig

# fit function
if doFit:
    fitFunc = ROOT.TF1("f1", "[0]*TMath::Erf((x-[1])/[2]) + [3]", 0, 1000) #Error function scaled to [0,1]
    fitFunc.SetParNames("Norm.", "Edge", "Resolution", "Y-Offset")
    #fitFunc.SetLineColor(ROOT.kAzure-1)
    #fitFunc.SetParameter(0, 0.5)
    #fitFunc.SetParameter(1, 150)
    #fitFunc.SetParameter(2, 50)  

    #fitFunc.SetParLimits(0, 0.4, 0.65) 
    #fitFunc.SetParLimits(1, 0, 100)
    #fitFunc.SetParLimits(2, 0, 50)
    #fitFunc.SetParLimits(3, 0.4, 0.8)

    #fitFunc.SetParameters(0.5, 30, 20, 0.5)
    #fitFunc.SetParameters(0.5, 140, 40, 0.50)

varStrings = cuts_weights.cuts.vars_dict_format
varNames = {'metPt':"E^{miss}_{T}", 'caloMetPt':"Calo. E^{miss}_{T}", 'metNoMuPt':"E^{miss}_{T} (#mu Sub.)", 'leadBasJetPt':"Leading Jet p_{T}", 'lepPt':"Muon p_{T}"} 
#plateauCutStrings = {key:varStrings[key] + " > " + str(val) for key,val in plateauCuts.iteritems()} 

regCutStr = getattr(cuts_weights.cuts, regDef).combined

# histograms
dens = {}
nums = {}

xmax  = {'metPt':500, 'ht':500, 'leadBasJetPt':1000, 'lepPt':80}
nbins = {'metPt':100, 'ht':100, 'leadBasJetPt':100,  'lepPt':80}

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

    hists[trig] = {'dens':{}, 'nums':{}}

    for var in variables:
        denSelList = ["Flag_Filters", regCutStr, denTrig]

        ## plateau cuts
        #for cut in plateauCuts:
        #    if var not in ['caloMetPt', 'metNoMuPt']:
        #        if cut != var:
        #            denSelList.append(plateauCutStrings[cut])
        #    else:
        #        if cut != 'metPt':
        #            denSelList.append(plateauCutStrings[cut]) # NOTE: do not cut on MET when variable is CaloMET

        denSel = combineCutsList(denSelList)
        numSel = combineCuts(denSel, trigCut) 
        
        suff2 = '_%s_%s%s'%(trig, var, suff)

        hists[trig]['dens'][var] = makeHist(samples[dataset_name].tree, varStrings[var], denSel, nbins[var], 0, xmax[var]) 
        #hists[trig]['dens'][var].SetTitle('den' + suff2)
        hists[trig]['dens'][var].SetName('den' + suff2)
        hists[trig]['dens'][var].GetXaxis().SetTitleOffset(1.2)
        hists[trig]['dens'][var].GetYaxis().SetTitleOffset(2)
        hists[trig]['dens'][var].GetYaxis().SetTitle("Events / %s GeV"%(xmax[var]/nbins[var]))
        hists[trig]['dens'][var].GetXaxis().SetTitle("%s [GeV]"%varNames[var])
        hists[trig]['dens'][var].GetYaxis().RotateTitle(1)
        hists[trig]['dens'][var].SetFillColor(0)
        hists[trig]['dens'][var].SetLineColor(ROOT.kBlue+2)
        hists[trig]['dens'][var].SetLineWidth(1)
        hists[trig]['dens'][var].SetLineStyle(7)
        
        hists[trig]['nums'][var] = makeHist(samples[dataset_name].tree, varStrings[var], numSel, nbins[var], 0, xmax[var]) 
        #hists[trig]['nums'][var].SetTitle('num' + suff2)
        hists[trig]['nums'][var].SetName('num' + suff2)
        hists[trig]['nums'][var].SetFillColor(ROOT.kAzure+7)
        hists[trig]['nums'][var].SetLineColor(ROOT.kBlack)
        hists[trig]['nums'][var].SetLineWidth(1)
        
        canv = ROOT.TCanvas("Canvas " + suff2, "Canvas " + suff2, 800, 800)
        canv.SetLogy(logy)
        canv.SetTicky(0)
        canv.SetGridx()
 
        f = ROOT.TFile('%s/%s/histos/histos%s.root'%(savedir, trig, suff2), "recreate")
        hists[trig]['dens'][var].Write()
        hists[trig]['nums'][var].Write()
        f.Close()

        hists[trig]['dens'][var].Draw('hist Y+')
        hists[trig]['nums'][var].Draw('hist same Y+')
        
        ROOT.gPad.Modified()
        ROOT.gPad.Update()

        if doLegend:
            leg = ROOT.TLegend()
            leg.AddEntry("den" + suff2, "Denominator", "F")
            leg.AddEntry("num" + suff2, "Numerator", "F")
            leg.SetBorderSize(0)
            leg.Draw()

        CMS_lumi.CMS_lumi(canv, 4, 0) # draw the lumi text on the canvas
        
        if doName:
            latex2 = ROOT.TLatex()
            latex2.SetNDC()
            latex2.SetTextSize(0.025)
            latex2.SetTextColor(ROOT.kRed+1)
            latex2.DrawLatex(0.15, 0.87, trig)

        # Efficiency
        overlay = ROOT.TPad("overlay", "", 0, 0, 1, 1)
        overlay.SetFillStyle(4000)
        overlay.SetFillColor(0)
        overlay.SetFrameFillStyle(4000)
        overlay.Draw()
        overlay.cd()
    
        frame = overlay.DrawFrame(0, 0, xmax[var], 1.1) # overlay.DrawFrame(pad.GetUxmin(), 0, pad.GetUxmax(), 1.1)
    
        eff = makeEffPlot(hists[trig]['nums'][var], hists[trig]['dens'][var])
        #eff.SetMarkerColor(ROOT.kAzure-1)
        eff.SetMarkerSize(1.5)
        #eff.SetTitle("; ; Leg Efficiency")
        eff.Draw("P")
 
        axis = ROOT.TGaxis(ROOT.gPad.GetUxmin(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUxmin(), ROOT.gPad.GetUymax(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUymax())#, 510, "R")
        axis.SetTitle("#font[42]{L1+HLT Leg Efficiency}")
        axis.SetTitleColor(1)
        axis.SetTitleSize(0.04)
        axis.SetTitleOffset(1.3)
        axis.SetLabelColor(1)
        axis.SetLabelFont(42)
        axis.SetLabelOffset(0.007)
        axis.SetLabelSize(0.04)
        axis.SetTickLength(0.03)
        axis.SetNdivisions(510)
        axis.Draw()

        if doFit:
            if var in ['lepPt']:
                fitFunc.SetParameters(0.5, 5, 20, 0.5)
            elif 'Jet' in var:
                fitFunc.SetParameters(0.5, 120, 30, 0.5)
            else:
                fitFunc.SetParameters(0.5, 150, 50, 0.5)

            eff.Fit(fitFunc)

            # Fit Parameter Extraction
            fitParams = {}
            #fitFunc.GetParameters(fit)
            fitParams['chiSq'] = fitFunc.GetChisquare()
            for x in xrange(0, 4):
               fitParams['var%s'%x] = fitFunc.GetParameter(x)
               fitParams['var%s'%x] = fitFunc.GetParError(x)

               fitParams['val50'] =  fitFunc.GetX(0.5)
               fitParams['val75'] =  fitFunc.GetX(0.75)
               fitParams['val80'] =  fitFunc.GetX(0.80)
               fitParams['val85'] =  fitFunc.GetX(0.85)
               fitParams['val90'] =  fitFunc.GetX(0.90)
               fitParams['val95'] =  fitFunc.GetX(0.95)
               fitParams['val99'] =  fitFunc.GetX(0.99)
               fitParams['val100'] = fitFunc.GetX(1)

            ROOT.gPad.Modified()
            ROOT.gPad.Update()

            setupEffPlot(eff)
        
            if doBox:
                pad = ROOT.TPad("pad", "", 0, 0, 1, 1)
                pad.SetFillStyle(0)
                pad.Draw()
                pad.cd()
                
                ROOT.gPad.Modified()
                ROOT.gPad.Update()

                box = ROOT.TBox(0.7, 0.35, 0.875, 0.525)
                box.SetFillColor(0)
                box.Draw('l')

                drawText("#bf{Turn-on:}", 0.75, 0.5)
                drawText("100 %%: %.0f GeV"%fitParams['val100'], 0.725, 0.475)
                drawText(" 99 %%: %.0f GeV"%fitParams['val99'],  0.725, 0.45)
                drawText(" 95 %%: %.0f GeV"%fitParams['val95'],  0.725, 0.425)
                drawText(" 90 %%: %.0f GeV"%fitParams['val90'],  0.725, 0.4)
                drawText(" 85 %%: %.0f GeV"%fitParams['val85'],  0.725, 0.375)

            ROOT.gPad.Modified()
            ROOT.gPad.Update()
    
        #Save canvas
        canv.SaveAs(    "%s/%s/trigEff_%s_%s%s.png"%(  savedir, trig, var, trig, suff))
        canv.SaveAs("%s/%s/pdf/trigEff_%s_%s%s.pdf"%(  savedir, trig, var, trig, suff))
        canv.SaveAs("%s/%s/root/trigEff_%s_%s%s.root"%(savedir, trig, var, trig, suff))