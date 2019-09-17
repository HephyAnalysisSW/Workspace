# plotTrigEff.py

import ROOT
import os, sys
import argparse
import importlib
from array import array
from math import sqrt

import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import makeHist, makeEffPlot, setupEffPlot, alignLegend
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import setup_style, makeLumiTag, makeDir
from Workspace.DegenerateStopAnalysis.tools.degCuts import CutsWeights
from Workspace.DegenerateStopAnalysis.tools.degPlots import Plots
from Workspace.DegenerateStopAnalysis.samples.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.samplesInfo import getCutWeightOptions

import Workspace.DegenerateStopAnalysis.samples.samplesInfo as samplesInfo
import Workspace.HEPHYPythonTools.CMS_lumi as CMS_lumi

# set style
setup_style()

#ROOT.gStyle.SetOptStat(0) # 0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis
ROOT.gStyle.SetOptFit(0) # 1111 prints fits results on plot
ROOT.gStyle.SetPadRightMargin(0.15)
ROOT.gStyle.SetPadLeftMargin(0.12)
ROOT.gStyle.SetPadBottomMargin(0.12)
#ROOT.gStyle.SetPadTopMargin(0.14)
ROOT.gStyle.SetTitleSize(0.04, "XYZ")
ROOT.gStyle.SetLabelSize(0.04, "XYZ")

# input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--triggers",       help = "Triggers",              type = str, default = "",           nargs = "+")
parser.add_argument("--samplesTag",     help = "Samples tag",           type = str, default = "nanoAOD_v6_6-1")
parser.add_argument("--dataset",        help = "Primary dataset",       type = str, default = "MET")
parser.add_argument("--dataEra",        help = "Data era",              type = str, default = "")
parser.add_argument("--year",           help = "Year",                  type = str, default = "2018")
parser.add_argument("--lepTag",         help = "Lepton tag",            type = str, default = "def", choices = ["bare", "loose", "def"])
parser.add_argument("--jetCol",         help = "Jet collection",        type = str, default = "Jet", choices = ["Jet", "JetClean"])
parser.add_argument("--basJets",        help = "Use basJets",           type = int, default = 0)
parser.add_argument("--baseDir",        help = "Base save dir",         type = str, default = "softTrigEff")
parser.add_argument("--plateauTag",     help = "Plateau tag",           type = str, default = "plus_lepEta_lt_1p5_plus_leadJetEta_lt_2p4_plus_leadJetId_plus_exact1Lep")
parser.add_argument("--region",         help = "Region",                type = str, default = "none")
parser.add_argument("--extraCuts",      help = "Extra cuts",            type = str, default = "plus_lepEta_lt_1p5_plus_leadBasJetEta_lt_2p4_plus_exact1Lep")
parser.add_argument("--minLepPt",       help = "Lower lepton pT cut",   type = str, default = None, choices = ['30', '40'])
parser.add_argument("--maxLepPt",       help = "Upper lepton pT cut",   type = str, default = None, choices = ['30', '40', '50'])
parser.add_argument("--maxElePt",       help = "Upper electron pT cut", type = str, default = None, choices = ['30', '40', '50'])
parser.add_argument("--variables",      help = "Variables to plot",     type = str, default = [],           nargs = '+')
parser.add_argument("--doVarBins",      help = "Variable bin size",     type = int, default = 1)
parser.add_argument("--doFit",          help = "Do fit",                type = int, default = 0)
parser.add_argument("--doName",         help = "Write name",            type = int, default = 0)
parser.add_argument("--doLegend",       help = "Draw legend",           type = int, default = 1)
parser.add_argument("--doBox",          help = "Draw box",              type = int, default = 0)
parser.add_argument("--doGrid",         help = "Draw grid",             type = int, default = 0)
parser.add_argument("--addOverFlowBin", help = "Add overflow bin",      type = int, default = 0)
parser.add_argument("--logy",           help = "Toggle logy",           type = int, default = 0)
parser.add_argument("--save",           help = "Toggle save",           type = int, default = 1)
parser.add_argument("--verbose",        help = "Verbosity switch",      type = int, default = 0)
parser.add_argument("--matchHLTjet",    help = "Match to HLT jet", type = int, default = 0)
args = parser.parse_args()
if not len(sys.argv) > 1:
    print makeLine()
    print "No arguments given. Using default settings."
    print makeLine()

# arguments
triggers       = args.triggers
dataset        = args.dataset
samplesTag     = args.samplesTag
dataEra        = args.dataEra
year           = args.year
lepTag         = args.lepTag
jetCol         = args.jetCol
basJets        = args.basJets
baseDir        = args.baseDir
plateauTag     = args.plateauTag
region         = args.region
extraCuts      = args.extraCuts
minLepPt       = args.minLepPt
maxLepPt       = args.maxLepPt
maxElePt       = args.maxElePt
variables      = args.variables
doVarBins      = args.doVarBins
doFit          = args.doFit
doName         = args.doName
doLegend       = args.doLegend
doBox          = args.doBox
doGrid         = args.doGrid
addOverFlowBin = args.addOverFlowBin
logy           = args.logy
save           = args.save
verbose        = args.verbose
matchHLTjet    = args.matchHLTjet

if basJets:
    leadJet = "leadBasJet"
else:
    leadJet = "leadJet"

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

plateauTag = 'plateau_' + plateauTag

lumiTag = makeLumiTag(samplesInfo.lumis[year][dataset_name], latex = True)

CMS_lumi.lumi_13TeV = lumiTag
CMS_lumi.extraText = "Preliminary"
CMS_lumi.relPosX = 0.12
#CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

regDef = region + "_" + extraCuts

# save
if save:
    suff = '_' + '_'.join([samplesTag, dataset, region])
    baseSavedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/%s/%s/softTrigEff/lepTag-%s/jetCol-%s/%s/%s/%s"%(baseDir, samplesTag, year, lepTag, jetCol, dataset_name, regDef, plateauTag)
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

# fit function
if doFit:
    fitFunc = ROOT.TF1("f1", "[0]*TMath::Erf((x-[1])/[2]) + [3]", 0, 1000) #Error function scaled to [0,1]
    fitFunc.SetParNames("Norm.", "Edge", "Resolution", "Y-Offset")
    #fitFunc.SetLineColor(ROOT.kAzure-1)
    #fitFunc.SetParameter(0, 0.5)
    #fitFunc.SetParameter(1, 150)
    #fitFunc.SetParameter(2, 50)  

    #fitFunc.SetParLimits(0, 0.4, 0.5) 
    #fitFunc.SetParLimits(1, 0, 200)
    #fitFunc.SetParLimits(2, 0, 50)
    #fitFunc.SetParLimits(3, 0.4, 0.8)

    #fitFunc.SetParameters(0.5, 30, 20, 0.5)
    #fitFunc.SetParameters(0.5, 140, 40, 0.50)

varNames = {'metPt':"E^{miss}_{T}", 'caloMetPt':"Calo. E^{miss}_{T}", 'metNoMuPt':"E^{miss}_{T} (#mu Sub.)", 'leadJetPt':"Leading Jet p_{T}", 'lepPt':"Muon p_{T}"} 

# histograms
dens = {}
nums = {}

xmax  = {'metPt':500, 'leadJetPt':300, 'lepPt':30}
nbins = {'metPt':100, 'leadJetPt':60,  'lepPt':30}

if doVarBins:
    varBins = {'metPt':range(0, 300, 5) + range(300, 400, 20) + range(400, xmax['metPt'] + 50, 50),
               'leadJetPt':range(0, 60, 60) + range(60, xmax['leadJetPt'] + xmax['leadJetPt']/nbins['leadJetPt'], xmax['leadJetPt']/nbins['leadJetPt']),
               'lepPt':range(0, xmax['lepPt'] + xmax['lepPt']/nbins['lepPt'], xmax['lepPt']/nbins['lepPt']),
    }

    if dataset == 'EGamma':
        varBins['metPt'] = range(0, 200, 5) + range(200, 300, 20) + range(400, xmax['metPt'] + 100, 100)
    elif dataset in ['DoubleMuon', 'Charmonium']:
        varBins['metPt'] = range(0, 100, 5) + range(100, 200, 10) + range(200, xmax['metPt'] + 50, 50)

    varBins['ht']        = varBins['metPt']
    varBins['caloMetPt'] = varBins['metPt']
    varBins['metNoMuPt'] = varBins['metPt']

xmax['ht']        = xmax['metPt']
xmax['caloMetPt'] = xmax['metPt']
xmax['metNoMuPt'] = xmax['metPt']

nbins['caloMetPt'] = nbins['metPt']
nbins['metNoMuPt'] = nbins['metPt']

hists = {}

for trig in triggers:

    makeDir("%s/%s"%(savedir, trig))
    makeDir("%s/%s/root"%(savedir, trig))
    makeDir("%s/%s/pdf"%(savedir, trig))

    hists[trig] = {'dens':{}, 'nums':{}}

    for var in variables:
        if var == "leadJetPt" and basJets:
            var_ = "leadBasJetPt"
        else:
            var_ = var

        suff2 = '_%s_%s%s'%(trig, var, suff)
                
        histosDir = '%s/%s/histos/histos%s.root'%(baseSavedir, trig, suff2)
       
        if not dataEra:
            hists[trig]['dens'][var] = ROOT.TH1D("den" + suff2, "den" + suff2, nbins[var], 0, xmax[var])
            hists[trig]['nums'][var] = ROOT.TH1D("num" + suff2, "num" + suff2, nbins[var], 0, xmax[var])

            for era in ['A', 'B', 'C', 'D']:
                try:
                    f = ROOT.TFile(histosDir.replace('Run2018', 'Run2018'+era), "read")
                    d = f.Get("den" + suff2)
                    n = f.Get("num" + suff2)

                    hists[trig]['dens'][var].Add(d)
                    hists[trig]['nums'][var].Add(n)
                except TypeError as exp:
                    print "!!! Missing histograms file for era", era, "!!!"
                    continue
        else:
            f = ROOT.TFile(histosDir, "read")

            hists[trig]['dens'][var] = f.Get("den" + suff2)
            hists[trig]['nums'][var] = f.Get("num" + suff2)

        if addOverFlowBin:
            for h in [hists[trig]['dens'][var], hists[trig]['nums'][var]]:
                nb = nbins[var] #nb = h.GetNbinsX()
                h.SetBinContent(nb, h.GetBinContent(nb) + h.GetBinContent(nb + 1))
                h.SetBinError(nb, sqrt(h.GetBinError(nb)**2 + h.GetBinError(nb + 1)**2))

        if doVarBins:
            varBins_ = array('d', varBins[var])
            hists[trig]['dens'][var] = hists[trig]['dens'][var].Rebin(len(varBins[var])-1, hists[trig]['dens'][var].GetName(), varBins_)
            hists[trig]['nums'][var] = hists[trig]['nums'][var].Rebin(len(varBins[var])-1, hists[trig]['nums'][var].GetName(), varBins_)
            hists[trig]['dens'][var].Sumw2()
            hists[trig]['nums'][var].Sumw2()
            hists[trig]['dens'][var].Scale(xmax[var]/nbins[var], "width")
            hists[trig]['nums'][var].Scale(xmax[var]/nbins[var], "width")
            suff += "_varBins"

        # Histograms
        hists[trig]['dens'][var].Draw('hist')
        hists[trig]['nums'][var].Draw('hist same')

        #hists[trig]['dens'][var].SetTitle('den' + suff2)
        hists[trig]['dens'][var].SetName('den' + suff2)
        hists[trig]['dens'][var].SetFillColor(0)
        hists[trig]['dens'][var].SetLineColor(ROOT.kBlue+2)
        hists[trig]['dens'][var].SetLineWidth(1)
        hists[trig]['dens'][var].SetLineStyle(7)
        
        #hists[trig]['nums'][var].SetTitle('num' + suff2)
        hists[trig]['nums'][var].SetName('num' + suff2)
        hists[trig]['nums'][var].GetXaxis().SetTitleOffset(1.2)
        hists[trig]['nums'][var].GetYaxis().SetTitleOffset(2)
        hists[trig]['nums'][var].GetYaxis().SetTitle("Events / %s GeV"%(xmax[var]/nbins[var]))
        hists[trig]['nums'][var].GetXaxis().SetTitle("%s [GeV]"%varNames[var])
        hists[trig]['nums'][var].GetYaxis().RotateTitle(1)
        hists[trig]['nums'][var].SetFillColor(ROOT.kAzure+7)
        hists[trig]['nums'][var].SetLineColor(ROOT.kBlack)
        hists[trig]['nums'][var].SetLineWidth(1)
        
        canv = ROOT.TCanvas("Canvas " + suff2, "Canvas " + suff2, 800, 800)
        canv.SetLogy(logy)
        canv.SetTicky(0)
        if doGrid:
            canv.SetGridx()
 
        ROOT.gPad.Modified()
        ROOT.gPad.Update()
        
        hists[trig]['nums'][var].SetMaximum(1.1 * hists[trig]['dens'][var].GetMaximum())
        
        hists[trig]['nums'][var].Draw('hist Y+')
        hists[trig]['dens'][var].Draw('hist same Y+')
        #ROOT.gPad.RedrawAxis('Y+')
        
        CMS_lumi.CMS_lumi(canv, 4, 0) # draw the lumi text on the canvas

        if doName:
            latex2 = ROOT.TLatex()
            latex2.SetNDC()
            latex2.SetTextSize(0.025)
            latex2.SetTextColor(ROOT.kRed+1)
            latex2.DrawLatex(0.15, 0.87, trig)

        # Efficiency
        eff = makeEffPlot(hists[trig]['nums'][var], hists[trig]['dens'][var])
        eff.SetName('eff')
        eff.SetMarkerSize(1.5)
        #eff.SetMarkerColor(ROOT.kAzure-1)
        #eff.SetTitle("; ; L1+HLT Leg Efficiency")
        
        if doLegend:
            leg = ROOT.TLegend()
            leg.AddEntry(eff, "Efficiency", "P")
            leg.AddEntry("den" + suff2, "Denominator", "F")
            leg.AddEntry("num" + suff2, "Numerator", "F")
            leg.SetBorderSize(0)
            leg.Draw()

            alignLegend(leg, x1 = 0.55, x2 = 0.75, y1 = 0.40, y2 = 0.55)

        overlay = ROOT.TPad("overlay", "", 0, 0, 1, 1)
        overlay.SetFillStyle(4000)
        overlay.SetFillColor(0)
        overlay.SetFrameFillStyle(4000)
        overlay.Draw()
        overlay.cd()

        frame = overlay.DrawFrame(0, 0, xmax[var], 1.1) # overlay.DrawFrame(pad.GetUxmin(), 0, pad.GetUxmax(), 1.1)
        eff.Draw("P")

        if doGrid: 
            axis = ROOT.TGaxis(ROOT.gPad.GetUxmin(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUxmin(), ROOT.gPad.GetUymax(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUymax(), 510, "W")
        else:
            axis = ROOT.TGaxis(ROOT.gPad.GetUxmin(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUxmin(), ROOT.gPad.GetUymax(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUymax())

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

        if doGrid:
            axis.SetGridLength(0.725)
        axis.Draw()

        hists[trig]['dens'][var].GetXaxis().Draw()

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
        canv.SaveAs(     "%s/%s/trigEff_%s_%s%s.png"%( savedir, trig, var, trig, suff))
        canv.SaveAs( "%s/%s/pdf/trigEff_%s_%s%s.pdf"%( savedir, trig, var, trig, suff))
        canv.SaveAs("%s/%s/root/trigEff_%s_%s%s.root"%(savedir, trig, var, trig, suff))
