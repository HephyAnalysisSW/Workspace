import ROOT
import os, sys
import math
import argparse
import pickle
from array import array
from math import pi, sqrt #cos, sin, sinh, log

#from DataFormats.FWLite import Events, Handle

from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *

from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_Summer16 import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples

ROOT.gStyle.SetOptStat(0) #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptFit(1111) #1111 prints fits results on plot

ROOT.gStyle.SetPaintTextFormat("4.2f")
#ROOT.gStyle->SetTitleX(0.1)
#ROOT.gStyle->SetTitleW(0.8)

ROOT.gStyle.SetStatX(0.875)
ROOT.gStyle.SetStatY(0.75)
ROOT.gStyle.SetStatW(0.1)
ROOT.gStyle.SetStatH(0.1)


samplesList = ['w', 'tt_1l', 'tt_2l']

trigger = 'HLT_PFMET120_PFMHT120_IDTight'

skim = 'oneLepGood20_ISR100'

skims = {'oneLepGood20_ISR100':'/afs/hephy.at/data/mzarucki01/cmgTuples/postProcessed_mAODv2/8025_mAODv2_v7/80X_postProcessing_v0/analysisHephy_13TeV_2016_v2_4/step1'}

ppDir = skims[skim]
mc_path     = ppDir + "/RunIISummer16MiniAODv2_v7"
data_path   = ppDir + "/Data2016_v7"

savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/TriggerStudies/StandardTriggers/%s"%skim

#cmgPP = cmgTuplesPostProcessed()
cmgPP = cmgTuplesPostProcessed(mc_path = mc_path, signal_path = mc_path, data_path = data_path)
samples = getSamples(cmgPP = cmgPP, skim = skim, sampleList = samplesList, scan = False, useHT = True, getData = False)

#infile = '/afs/hephy.at/data/mzarucki02/TriggerStudies/CMSSW_9_2_12/AOD/T2tt_dM-10to80_mStop-500_mLSP-460_noPU_SoftTriggers_V9_HLT_AODSIM.root'
#triggerList = "SoftTriggers_V9.list"

doFit = True

# Functions

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        #if exc.errno == errno.EEXIST and os.path.isdir(path):
        if os.path.isdir(path):
            pass
        else:
            raise

def makeDir(path):
    if "." in path[-5:]:
        path = path.replace(os.path.basename(path),"")
        print path
    if os.path.isdir(path):
        return
    else:
        mkdir_p(path)

def getListFromFile(filename):
   f = open(filename,'r')
   outlist = []
   for l in f:
      l = l.strip('\n')
      outlist.append(l)
   f.close()
   return outlist

# Efficiency
def makeEffPlot(passed,total):
   a = passed.Clone()
   b = total.Clone()
   eff = ROOT.TEfficiency(a,b)
   eff.SetTitle("Efficiency Plot")
   eff.SetMarkerStyle(33)
   eff.SetMarkerSize(2)
   eff.SetLineWidth(2)
   return eff

def setupEffPlot(eff):
   ROOT.gPad.Modified()
   ROOT.gPad.Update()

   ROOT.gPad.SetGridx()
   ROOT.gPad.SetGridy()
   eff.GetPaintedGraph().GetYaxis().SetTitle("Efficiency")
   eff.GetPaintedGraph().SetMinimum(0)
   eff.GetPaintedGraph().SetMaximum(1)
   eff.GetPaintedGraph().GetXaxis().CenterTitle()
   eff.GetPaintedGraph().GetYaxis().CenterTitle()

   ROOT.gPad.Modified()
   ROOT.gPad.Update()

def drawText(text, x, y):        
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.015)
    latex.DrawLatex(x,y, "#font[42]{%s}"%text)

#triggers = getListFromFile(triggerList) 
#variables = ['MET']#, 'HT', 'JetPt', 'MuPt', 'ElePt']
variables = {'MET':'met'}#, 'HT', 'JetPt', 'MuPt', 'ElePt']

# Histograms

dens = {}
nums = {}

xmax = {'MET':500, 'HT':500, 'JetPt':300, 'MuPt':80, 'ElePt':150}

#f = ROOT.TFile(infile)
#tree = f.Get("Events")

hists = {}

denSel = "1"
numSel = "(%s && %s)"%(denSel, trigger)

for samp in samplesList:
    hists[samp] = {'dens':{}, 'nums':{}}
    for var in variables:
        hists[samp]['dens'][var] = makeHist(samples[samp].tree, variables[var], denSel, 100, 0, xmax[var]) 
        #hists[samp]['dens'][var].GetXaxis().SetTitleOffset(1.2)
        hists[samp]['dens'][var].GetYaxis().SetTitleOffset(1.3)
        hists[samp]['dens'][var].GetYaxis().SetTitle("Events")
        hists[samp]['dens'][var].GetXaxis().SetTitle("%s / GeV"%var)
        hists[samp]['dens'][var].GetXaxis().CenterTitle()
        hists[samp]['dens'][var].GetYaxis().CenterTitle()
        hists[samp]['dens'][var].SetFillColor(ROOT.kBlue-9)
        
        hists[samp]['nums'][var] = makeHist(samples[samp].tree, variables[var], numSel, 100, 0, xmax[var]) 
        hists[samp]['nums'][var].SetFillColor(ROOT.kGreen+2)
        hists[samp]['nums'][var].SetLineColor(ROOT.kBlack)
        hists[samp]['nums'][var].SetLineWidth(2)

# Fit Function
if doFit:
    fitFunc = ROOT.TF1("f1", "[0]*TMath::Erf((x-[1])/[2]) + [3]", 0, 1000) #Error function scaled to [0,1]
    fitFunc.SetParNames("Norm.", "Edge", "Resolution", "Y-Offset")
    #fitFunc.SetLineColor(ROOT.kAzure-1)
    #fitFunc.SetParameter(0, 0.5)
    #fitFunc.SetParameter(1, 150)
    #fitFunc.SetParameter(2, 50)  
    
    fitFunc.SetParLimits(0, 0.4, 0.65) 
    fitFunc.SetParLimits(1, 0, 200) #init: [0,200]
    fitFunc.SetParLimits(2, 0, 60) #init: [0,60]
    fitFunc.SetParLimits(3, 0.45, 0.8) #init: [0.45,0.8]
    
    fitFunc.SetParameters(0.55, 50, 35, 0.5) #init: (0.5, 140, 40, 0.5)
    #fitFunc.SetParameters(0.5, 140, 40, 0.50) #init: (0.45,60,20,0.6) #HT

for samp in samplesList:
    for var in variables:
        canv = ROOT.TCanvas("Canvas %s_%s"%(var,samp), "Canvas %s_%s"%(var,samp), 1500, 1500)
        canv.SetGrid()

        # Histograms
               
        hists[samp]['dens'][var].Draw('hist')
        hists[samp]['nums'][var].Draw('hist same')
        
        ROOT.gPad.Modified()
        ROOT.gPad.Update()
        
        latex1 = ROOT.TLatex()
        latex1.SetNDC()
        latex1.SetTextSize(0.03)
        latex1.DrawLatex(0.12, 0.95, "CMS Simulation")
        #latex1.DrawLatex(0.12, 0.92, "#font[62]{CMS Simulation}")
        
        latex2 = ROOT.TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.025)
        latex2.SetTextColor(ROOT.kRed+1)
        latex2.DrawLatex(0.45, 0.85, trigger)
            
        ## Efficiency

        overlay = ROOT.TPad("overlay", "", 0, 0, 1, 1)
        overlay.SetFillStyle(4000)
        overlay.SetFillColor(0)
        overlay.SetFrameFillStyle(4000)
        overlay.Draw()
        overlay.cd()

        frame = overlay.DrawFrame(0, 0, xmax[var], 1.1) # overlay.DrawFrame(pad.GetUxmin(), 0, pad.GetUxmax(), 1.2)
 
        eff = makeEffPlot(hists[samp]['nums'][var],hists[samp]['dens'][var])
        #eff.SetMarkerColor(ROOT.kAzure-1)
        #eff.SetTitle("%s Trigger Efficiency; %s; Trigger Efficiency"%(samp,var))
        eff.Draw("P")
       
        # axis on the right side
        axis = ROOT.TGaxis(ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymax(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUymax(), 510, "+L")
        axis.SetTitle("#font[42]{Trigger Efficiency}")
        axis.CenterTitle()
        axis.SetLabelSize(0.03)
        axis.SetTitleSize(0.03)
        axis.SetTitleOffset(1.4)
        axis.SetLabelColor(ROOT.kAzure-1)
        axis.SetLineColor(ROOT.kAzure-1)
        axis.SetTextColor(ROOT.kAzure-1)
        axis.Draw()

        if doFit:
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
       
            #print 'Fit parameters', var, samp, fitParams
 
            ROOT.gPad.Modified()
            ROOT.gPad.Update()
   
            setupEffPlot(eff)
        
            pad = ROOT.TPad("pad", "", 0, 0, 1, 1)
            pad.SetFillStyle(0)
            pad.Draw()
            pad.cd()
            
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
        makeDir(savedir) 
        canv.SaveAs("%s/trigEff_%s_%s.png"%(savedir,var,samp))
