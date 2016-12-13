import ROOT
import pickle
import copy, os, sys

ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/WPolarizationVariation.C+")
#ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
#ROOT.TH1F().SetDefaultSumw2()
#ROOT.setTDRStyle()
ROOT.gStyle.SetMarkerStyle(1)
ROOT.gStyle.SetOptTitle(0)

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *

from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2_antiSel_postProcessed import *
from Workspace.RA4Analysis.signalRegions import *
from math import *
from Workspace.HEPHYPythonTools.user import username


picklePath = '/data/'+username+'/Results2016/WPolarizationEstimation/'
picklePresel = 'uncertainties_pkl'

uncertainties = pickle.load(file(picklePath+picklePresel))

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
signalRegions = signalRegions2016

rowsNJet = {}
rowsSt = {}
bins = 0
for srNJet in sorted(signalRegions):
  rowsNJet[srNJet] = {}
  rowsSt[srNJet] = {}
  rows = 0
  for stb in sorted(signalRegions[srNJet]):
    rows += len(signalRegions[srNJet][stb])
    rowsSt[srNJet][stb] = {'n':len(signalRegions[srNJet][stb])}
  rowsNJet[srNJet] = {'nST':len(signalRegions[srNJet]), 'n':rows}
  bins += rows


ttH_up = ROOT.TH1F('ttH_up','tt+jets up',bins,0,bins)
ttH_down = ROOT.TH1F('ttH_down','tt+jets down',bins,0,bins)

ttH_up.SetLineColor(ROOT.kBlue)
ttH_down.SetLineColor(ROOT.kBlue)

WH_up = ROOT.TH1F('WH_up','W+jets up',bins,0,bins)
WH_down = ROOT.TH1F('WH_down','W+jets down',bins,0,bins)

WH_up.SetLineColor(ROOT.kGreen+1)
WH_down.SetLineColor(ROOT.kGreen+1)

WpH_up = ROOT.TH1F('WpH_up','W+jets pos. up',bins,0,bins)
WpH_down = ROOT.TH1F('WpH_down','W+jets pos. down',bins,0,bins)

WpH_up.SetLineColor(ROOT.kRed+1)
WpH_down.SetLineColor(ROOT.kRed+1)

WmH_up = ROOT.TH1F('WmH_up','W+jets neg. up',bins,0,bins)
WmH_down = ROOT.TH1F('WmH_down','W+jets neg. down',bins,0,bins)

WmH_up.SetLineColor(ROOT.kOrange)
WmH_down.SetLineColor(ROOT.kOrange)

hists = [ttH_up,ttH_down,WH_up,WH_down,WpH_up,WpH_down,WmH_up,WmH_down]
for h in hists:
  h.SetLineWidth(2)
  h.SetMarkerSize(0)
  h.SetMarkerColor(h.GetLineColor())

i = 1

for i_njb, srNJet in enumerate(sorted(signalRegions)): #just changed this Nov 4th, not sorted before!
  for stb in sorted(signalRegions[srNJet]):
    for htb in sorted(signalRegions[srNJet][stb]):
      ttH_up.SetBinContent(i, abs(1-uncertainties['tt']['uncertainties'][srNJet][stb][htb]['up']))
      ttH_down.SetBinContent(i, -abs(1-uncertainties['tt']['uncertainties'][srNJet][stb][htb]['down']))

      WH_up.SetBinContent(i, abs(1-uncertainties['W']['uncertainties'][srNJet][stb][htb]['up']))
      WH_down.SetBinContent(i, -abs(1-uncertainties['W']['uncertainties'][srNJet][stb][htb]['down']))

      WpH_up.SetBinContent(i, abs(1-uncertainties['W_p']['uncertainties'][srNJet][stb][htb]['up']))
      WpH_down.SetBinContent(i, -abs(1-uncertainties['W_p']['uncertainties'][srNJet][stb][htb]['down']))

      WmH_up.SetBinContent(i, abs(1-uncertainties['W_m']['uncertainties'][srNJet][stb][htb]['up']))
      WmH_down.SetBinContent(i, -abs(1-uncertainties['W_m']['uncertainties'][srNJet][stb][htb]['down']))
      
      i += 1


can = ROOT.TCanvas('can','can',700,700)

ttH_up.SetMaximum(0.05)
ttH_up.SetMinimum(-0.05)

ttH_up.GetXaxis().SetLabelSize(0.027)
ttH_up.GetYaxis().SetLabelSize(0.04)

setNiceBinLabel(ttH_up, signalRegions)



printkey = 'hist'
first = True
for h in hists:
  h.Draw(printkey)
  printkey = 'hist same'


latex2 = ROOT.TLatex()
latex2.SetNDC()
latex2.SetTextSize(0.04)
latex2.SetTextAlign(11)

latex2.DrawLatex(0.16,0.96,'CMS #bf{#it{simulation}}')
latex2.DrawLatex(0.79,0.96,"#bf{MC (13TeV)}")

leg = ROOT.TLegend(0.65,0.79,0.98,0.95)
leg.SetFillColor(ROOT.kWhite)
leg.SetShadowColor(ROOT.kWhite)
leg.SetBorderSize(1)
leg.SetTextSize(0.035)
leg.AddEntry(ttH_up,'t#bar{t}+jets')
leg.AddEntry(WH_up,'W+jets')
leg.AddEntry(WpH_up,'W+jets, pos.')
leg.AddEntry(WmH_up,'W+jets, neg.')

leg.Draw()



