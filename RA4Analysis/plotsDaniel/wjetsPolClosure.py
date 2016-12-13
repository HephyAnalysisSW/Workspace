import ROOT
import pickle 
import copy, os, sys
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.TH1F().SetDefaultSumw2()
ROOT.setTDRStyle()
#ROOT.tdrStyle.SetPadBottomMargin(0.2)
#ROOT.tdrStyle.SetPadRightMargin(0.25)
ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetHistMinimumZero()

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.signalRegions import *
from draw_helpers import *
from math import *
from Workspace.HEPHYPythonTools.user import username

preprefix = 'WPolarizationEstimation/closurePlots'
wwwDir = '/afs/hephy.at/user/d/dhandl/www/RunII/Spring15_25ns/'+preprefix+'/'
presel = ''

if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

path = '/data/'+username+'/Spring15/25ns/PredictionAN_3.0/'
pickleFileWPolPlus10  = 'singleLeptonic_Spring15_WPolPlus10_estimationResults_pkl_kappa_corrected'
pickleFileWPolMinus10 = 'singleLeptonic_Spring15_WPolMinus10_estimationResults_pkl_kappa_corrected'
pickleFileTTPolPlus5  = 'singleLeptonic_Spring15_TTPolPlus5_estimationResults_pkl_kappa_corrected'
pickleFileTTPolMinus5 = 'singleLeptonic_Spring15_TTPolMinus5_estimationResults_pkl_kappa_corrected'
pickleFile            = 'singleLeptonic_Spring15_estimationResults_pkl_kappa_corrected'
resWPolPlus10 = pickle.load(file(path+pickleFileWPolPlus10))
resWPolMinus10 = pickle.load(file(path+pickleFileWPolMinus10))
resTTPolPlus5 = pickle.load(file(path+pickleFileTTPolPlus5))
resTTPolMinus5 = pickle.load(file(path+pickleFileTTPolMinus5))
resTruth = pickle.load(file(path+pickleFile))

wPolPickleFile = '/data/'+username+'/results2015/WPolarizationEstimation/20151218_wjetsPolSys_pkl'

targetLumi = 3.

def getFraction(Bkg, Bkg_err, QCD, QCD_err):
  try: res = QCD/Bkg
  except ZeroDivisionError: res = float('nan')
  try: res_err = res*sqrt(Bkg_err**2/Bkg**2 + QCD_err**2/QCD**2)
  except ZeroDivisionError: res_err = float('nan')
  return res, res_err

#define SR
signalRegions = signalRegion3fb
signalRegion = {#(3, 4): {(250, 350): {(500, -1):   {'deltaPhi': 1.0}, #3-4jets QCD and W+jets control region
                #                      (500, 750):  {'deltaPhi': 1.0},
                #                      (750, -1):   {'deltaPhi': 1.0}},
                #         (350, 450): {(500, -1):   {'deltaPhi': 1.0},
                #                      (500, -1):   {'deltaPhi': 0.75},
                #                      (500, 750):  {'deltaPhi': 1.0},
                #                      (750, -1):   {'deltaPhi': 1.0}},
                #         (450, -1):  {(500, -1):   {'deltaPhi': 1.0},
                #                      (500, -1):   {'deltaPhi': 0.75},
                #                      (500, 1000): {'deltaPhi': 0.75},
                #                      (1000, -1):  {'deltaPhi': 0.75}}},
                #(4, 5): {(250, 350): {(500, -1):   {'deltaPhi': 1.0}, #4-5jets TTbar control region
                #                      (500, 750):  {'deltaPhi': 1.0},
                #                      (750, -1):   {'deltaPhi': 1.0}},
                #         (350, 450): {(500, -1):   {'deltaPhi': 1.0},
                #                      (500, -1):   {'deltaPhi': 0.75},
                #                      (500, 750):  {'deltaPhi': 1.0},
                #                      (750, -1):   {'deltaPhi': 1.0}},
                #         (450, -1):  {(500, -1):   {'deltaPhi': 1.0},
                #                      (500, -1):   {'deltaPhi': 0.75},
                #                      (500, 1000): {'deltaPhi': 0.75},
                #                      (1000, -1):  {'deltaPhi': 0.75}}},
                (5, 5): {(250, 350): {(500, -1):   {'deltaPhi': 1.0}},  #signal regions
                         (350, 450): {(500, -1):   {'deltaPhi': 1.0}},
                         (450, -1):  {(500, -1):   {'deltaPhi': 1.0}}},
                (6, 7): {(250, 350): {(500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                         (350, 450): {(500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                          (450, -1): {(500, 1000): {'deltaPhi': 0.75},
                                      (1000, -1):  {'deltaPhi': 0.75}}},
                (8, -1): {(250, 350):{(500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                          (350, 450):{(500, -1):   {'deltaPhi': 0.75}},
                          (450, -1): {(500, -1):   {'deltaPhi': 0.75}}}
}

btreg = [(0,0)]#, (1,1), (2,2)] #1b and 2b estimates are needed for the btag fit

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

WPolPlus10  = []
WPolMinus10 = []
TTPolPlus5  = []
TTPolMinus5 = []
pickleBins = {}
for srNJet in sorted(signalRegions):
  pickleBins[srNJet] = {}
  for stb in sorted(signalRegions[srNJet]):
    pickleBins[srNJet][stb] = {}
    for htb in sorted(signalRegions[srNJet][stb]):
      pickleBins[srNJet][stb][htb] = {}
      uWPolPlus10  = ((resWPolPlus10[srNJet][stb][htb]['tot_pred']/resWPolPlus10[srNJet][stb][htb]['tot_truth'])/(resTruth[srNJet][stb][htb]['tot_pred']/resTruth[srNJet][stb][htb]['tot_truth'])) - 1.
      uWPolMinus10 = ((resWPolMinus10[srNJet][stb][htb]['tot_pred']/resWPolMinus10[srNJet][stb][htb]['tot_truth'])/(resTruth[srNJet][stb][htb]['tot_pred']/resTruth[srNJet][stb][htb]['tot_truth'])) - 1.
      uTTPolPlus5  = ((resTTPolPlus5[srNJet][stb][htb]['tot_pred']/resTTPolPlus5[srNJet][stb][htb]['tot_truth'])/(resTruth[srNJet][stb][htb]['tot_pred']/resTruth[srNJet][stb][htb]['tot_truth'])) - 1.
      uTTPolMinus5 = ((resTTPolMinus5[srNJet][stb][htb]['tot_pred']/resTTPolMinus5[srNJet][stb][htb]['tot_truth'])/(resTruth[srNJet][stb][htb]['tot_pred']/resTruth[srNJet][stb][htb]['tot_truth'])) - 1.
      
      WPolPlus10.append(uWPolPlus10)
      WPolMinus10.append(uWPolMinus10)
      TTPolPlus5.append(uTTPolPlus5)
      TTPolMinus5.append(uTTPolMinus5)
      pickleBins[srNJet][stb][htb].update({'uWPolPlus10':uWPolPlus10, 'uWPolMinus10':uWPolMinus10, 'uTTPolPlus5':uTTPolPlus5, 'uTTPolMinus5':uTTPolMinus5 })

WPolPlus10_H  = ROOT.TH1F('WPolPlus10_H','WPolPlus10_H',bins,0,bins)
WPolMinus10_H = ROOT.TH1F('WPolMinus10_H','WPolMinus10_H',bins,0,bins)
WPolPlus10_H.SetLineColor(0)
WPolMinus10_H.SetLineColor(0)
WPolPlus10_H.SetFillColor(color('wJets'))
WPolMinus10_H.SetFillColor(color('wJets'))
WPolPlus10_H.SetStats(0)
WPolMinus10_H.SetStats(0)
WPolPlus10_H.SetMinimum(-0.05)
WPolMinus10_H.SetMinimum(-0.05)
WPolPlus10_H.SetMaximum(0.05)
WPolMinus10_H.SetMaximum(0.05)

TTPolPlus5_H  = ROOT.TH1F('TTPolPlus5_H','TTPolPlus5_H',bins,0,bins)
TTPolMinus5_H = ROOT.TH1F('TTPolMinus5_H','TTPolMinus5_H',bins,0,bins)
TTPolPlus5_H.SetLineColor(0)
TTPolMinus5_H.SetLineColor(0)
TTPolPlus5_H.SetFillColor(color('ttJets'))
TTPolMinus5_H.SetFillColor(color('ttJets'))
TTPolPlus5_H.SetStats(0)
TTPolMinus5_H.SetStats(0)
TTPolPlus5_H.SetMinimum(-0.05)
TTPolMinus5_H.SetMinimum(-0.05)
TTPolPlus5_H.SetMaximum(0.05)
TTPolMinus5_H.SetMaximum(0.05)

text = ROOT.TLatex()
text.SetNDC()
text.SetTextSize(0.04)
text.SetTextAlign(11)
canv = ROOT.TCanvas('canv','canv',600,600)
canv.SetGrid()
l = ROOT.TLegend(0.65,0.8,0.98,0.95)
l.SetFillColor(0)
l.SetBorderSize(1)
l.SetShadowColor(ROOT.kWhite)


j=0
for i_njb, njb in enumerate(sorted(signalRegion)):
  for i_CR, ltb in enumerate(sorted(signalRegion[njb])):
    for i_htb,htb in enumerate(sorted(signalRegion[njb][ltb])):
      j+=1
      WPolPlus10_H.SetBinContent(j,WPolPlus10[j-1])
      WPolMinus10_H.SetBinContent(j,WPolMinus10[j-1])
      TTPolPlus5_H.SetBinContent(j,TTPolPlus5[j-1])
      TTPolMinus5_H.SetBinContent(j,TTPolMinus5[j-1])
      TTPolMinus5_H.GetXaxis().SetBinLabel(j,str(j))

WPolPlus10_H.SetBarOffset(0.)
WPolPlus10_H.SetBarWidth(0.5)
WPolPlus10_H.Draw("bar")
WPolMinus10_H.SetBarOffset(0.)
WPolMinus10_H.SetBarWidth(0.5)
WPolMinus10_H.Draw("bar same")
TTPolPlus5_H.SetBarOffset(0.5)
TTPolPlus5_H.SetBarWidth(0.5)
TTPolPlus5_H.Draw("'bar same")
TTPolMinus5_H.SetBarOffset(0.5)
TTPolMinus5_H.SetBarWidth(0.5)
TTPolMinus5_H.GetXaxis().SetTitle('signal region')
TTPolMinus5_H.Draw("bar same")
l.AddEntry(WPolPlus10_H,'W+jets #pm10% var.','f')
l.AddEntry(TTPolPlus5_H,'t#bar{t}+jets #pm5% var.','f')
text.DrawLatex(0.17,.96,"CMS #bf{#it{Simulation}}")
text.DrawLatex(0.7,0.96,"#bf{L="+str(targetLumi)+" fb^{-1} (13 TeV)}")
l.Draw()
canv.Print(wwwDir+'WpolSystematics_totalBkg_inSR.png')
canv.Print(wwwDir+'WpolSystematics_totalBkg_inSR.pdf')
canv.Print(wwwDir+'WpolSystematics_totalBkg_inSR.root')

pickle.dump(pickleBins, file(wPolPickleFile,'w'))
