# softTrigEff.py

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

# set style
#setup_style()

ROOT.gStyle.SetOptStat(0) #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis
ROOT.gStyle.SetOptTitle(0)
#ROOT.gStyle.SetOptFit(1111) #1111 prints fits results on plot

ROOT.gStyle.SetPaintTextFormat("4.2f")
#ROOT.gStyle->SetTitleX(0.1)
#ROOT.gStyle->SetTitleW(0.8)

ROOT.gStyle.SetStatX(0.875)
ROOT.gStyle.SetStatY(0.75)
ROOT.gStyle.SetStatW(0.1)
ROOT.gStyle.SetStatH(0.1)

# input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--triggers",  help = "Triggers",          type = str, default = "",           nargs = "+")
parser.add_argument("--dataset",   help = "Primary dataset",   type = str, default = "MET")
parser.add_argument("--dataEra",   help = "Data era",          type = str, default = "")
parser.add_argument("--options",   help = "Options",           type = str, default = ['noweight'], nargs = '+')
parser.add_argument("--year",      help = "Year",              type = str, default = "2018")
parser.add_argument("--lepTag",    help = "Lepton tag",        type = str, default = "loose", choices = ["bare", "loose", "def"])
parser.add_argument("--region",    help = "Region",            type = str, default = "softTrigEta")
parser.add_argument("--variables", help = "Variables to plot", type = str, default = [],           nargs = '+')
parser.add_argument("--doFit",     help = "Do fit",            type = int, default = 1)
parser.add_argument("--doName",    help = "Write name",        type = int, default = 1)
parser.add_argument("--doBox",     help = "Draw box",          type = int, default = 0)
parser.add_argument("--logy",      help = "Toggle logy",       type = int, default = 0)
parser.add_argument("--save",      help = "Toggle save",       type = int, default = 1)
parser.add_argument("--verbose",   help = "Verbosity switch",  type = int, default = 0)
args = parser.parse_args()
if not len(sys.argv) > 1:
    print makeLine()
    print "No arguments given. Using default settings."
    print makeLine()

# arguments
triggers  = args.triggers
dataset   = args.dataset
dataEra   = args.dataEra
options   = args.options
year      = args.year
lepTag    = args.lepTag
region    = args.region
variables = args.variables
doFit     = args.doFit
doName    = args.doName
doBox     = args.doBox
logy      = args.logy
save      = args.save
verbose   = args.verbose

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

if dataset == 'MET':
    denTrig = 'HLT_PFMET120_PFMHT120_IDTight'
    if not variables:
        variables = ['lepPt']
    plateauCuts = {'lepPt':15, 'metPt':250, 'leadJetPt':150}
elif dataset == 'SingleMuon':
    denTrig = 'HLT_IsoMu24'
    if not variables:
        variables = ['metPt', 'leadJetPt']
    plateauCuts = {'lepPt':40, 'metPt':250, 'leadJetPt':150}
else:
    print "Wrong dataset. Exiting."
    sys.exit()

plateauTag = 'plateau_lepPt%s_metPt%s_leadJetPt%s'%(plateauCuts['lepPt'], plateauCuts['metPt'], plateauCuts['leadJetPt'])

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

sampleDefPath = 'Workspace.DegenerateStopAnalysis.samples.nanoAOD_postProcessed.nanoAOD_postProcessed_' + era
sampleDef = importlib.import_module(sampleDefPath)
PP = sampleDef.nanoPostProcessed()
samples = getSamples(PP = PP, skim = 'oneLep', sampleList = samplesList, scan = False, useHT = True, getData = True, settings = cutWeightOptions['settings'])

# save
if save:
    tag = samples[samples.keys()[0]].dir.split('/')[9]
    suff = '_'.join([tag, dataset, region])
    savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/%s/softTrigEff/%s/%s/%s/%s"%(tag, year, lepTag, dataset_name, region, plateauTag)

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

# cuts
#alt_vars = {'lepIndex':{'var':'Index{lepCol}_{lep}{lt}', 'latex':''}} # considering leading loose lepton
#alt_vars = {'lepPt':{'var':'{lepPt_loose}', 'latex':''}} # considering leading loose lepton

cuts_weights = CutsWeights(samples, cutWeightOptions)#, alternative_vars = alt_vars)
regDef = region
#regDef = cuts_weights.cuts.addCut(regDef, 'trig_MET')
#cuts_weights.cuts._update(reset = False)
#cuts_weights._update()

varStrings = cuts_weights.cuts.vars_dict_format
varNames = {'metPt':"E^{miss}_{T}", 'leadJetPt':"Leading Jet p_{T}", 'lepPt':"Muon p_{T}"} 
plateauCutStrings = {key:varStrings[key] + " > " + str(val) for key,val in plateauCuts.iteritems()} 

regCutStr = getattr(cuts_weights.cuts, regDef).combined

# histograms
dens = {}
nums = {}

xmax = {'metPt':500, 'ht':500, 'leadJetPt':300, 'lepPt':80}

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
        denSelList = ["Flag_Filters", "run >= 315974", regCutStr, denTrig] 
        # plateau cuts
        for cut in plateauCuts:
            if cut != var:
                denSelList.append(plateauCutStrings[cut])

        denSel = combineCutsList(denSelList)
        numSel = combineCuts(denSel, trigCut) 
        
        hists[trig]['dens'][var] = makeHist(samples[dataset_name].tree, varStrings[var], denSel, 100, 0, xmax[var]) 
        #hists[trig]['dens'][var].GetXaxis().SetTitleOffset(1.2)
        hists[trig]['dens'][var].GetYaxis().SetTitleOffset(1.3)
        hists[trig]['dens'][var].GetYaxis().SetTitle("Events")
        hists[trig]['dens'][var].GetXaxis().SetTitle("%s / GeV"%varNames[var])
        hists[trig]['dens'][var].GetXaxis().CenterTitle()
        hists[trig]['dens'][var].GetYaxis().CenterTitle()
        hists[trig]['dens'][var].SetFillColor(ROOT.kBlue-9)
        
        hists[trig]['nums'][var] = makeHist(samples[dataset_name].tree, varStrings[var], numSel, 100, 0, xmax[var]) 
        hists[trig]['nums'][var].SetFillColor(ROOT.kGreen+2)
        hists[trig]['nums'][var].SetLineColor(ROOT.kBlack)
        hists[trig]['nums'][var].SetLineWidth(2)
    
        canv = ROOT.TCanvas("Canvas %s_%s"%(var,trig), "Canvas %s_%s"%(var,trig), 1500, 1500)
        canv.SetGrid()
        canv.SetLogy(logy)

        f = ROOT.TFile('%s/%s/histos/histos_%s_%s%s.root'%(savedir, trig, var, trig, suff), "recreate")

        # Histograms
        hists[trig]['dens'][var].Write()
        hists[trig]['nums'][var].Write()
        f.Close()

        hists[trig]['dens'][var].Draw('hist')
        hists[trig]['nums'][var].Draw('hist same')

        ROOT.gPad.Modified()
        ROOT.gPad.Update()

        latex1 = ROOT.TLatex()
        latex1.SetNDC()
        latex1.SetTextSize(0.03)
        latex1.DrawLatex(0.1, 0.92, "CMS #it{Preliminary}") #font[62]{CMS Simulation}"
        latex1.DrawLatex(0.55, 0.92, "%s PD %s (13 TeV)"% (dataset, lumiTag))

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
    
        frame = overlay.DrawFrame(0, 0, xmax[var], 1.1) # overlay.DrawFrame(pad.GetUxmin(), 0, pad.GetUxmax(), 1.2)
    
        eff = makeEffPlot(hists[trig]['nums'][var],hists[trig]['dens'][var])
        #eff.SetMarkerColor(ROOT.kAzure-1)
        #eff.SetTitle("%s Trigger Efficiency; %s; Trigger Efficiency"%(trig,var))
        eff.Draw("P")
       
        # axis on the right side
        axis = ROOT.TGaxis(ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymax(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUymax(), 510, "+L")
        axis.SetTitle("#font[42]{Leg Efficiency}")
        axis.CenterTitle()
        axis.SetLabelSize(0.03)
        axis.SetTitleSize(0.03)
        axis.SetTitleOffset(1.4)
        axis.SetLabelColor(ROOT.kAzure-1)
        axis.SetLineColor(ROOT.kAzure-1)
        axis.SetTextColor(ROOT.kAzure-1)
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

            #print 'Fit parameters', var, trig, fitParams

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
                drawText("  99 %%: %.0f GeV"%fitParams['val99'],  0.725, 0.45)
                drawText("  95 %%: %.0f GeV"%fitParams['val95'],  0.725, 0.425)
                drawText("  90 %%: %.0f GeV"%fitParams['val90'],  0.725, 0.4)
                drawText("  85 %%: %.0f GeV"%fitParams['val85'],  0.725, 0.375)

            ROOT.gPad.Modified()
            ROOT.gPad.Update()
    
        #Save canvas
        canv.SaveAs(    "%s/%s/trigEff_%s_%s_%s.png"%(  savedir, trig, var, trig, suff))
        canv.SaveAs("%s/%s/pdf/trigEff_%s_%s_%s.pdf"%(  savedir, trig, var, trig, suff))
        canv.SaveAs("%s/%s/root/trigEff_%s_%s_%s.root"%(savedir, trig, var, trig, suff))
