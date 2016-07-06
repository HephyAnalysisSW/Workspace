import ROOT
import pickle
import os,sys,math
from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
from Workspace.HEPHYPythonTools.user import username
from math import pi, sqrt
from Workspace.RA4Analysis.signalRegions import *

from helpers import *


ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()

signalRegions = signalRegions2016

ROOT.gStyle.SetOptTitle(0);
ROOT.gStyle.SetOptStat('')

small = False
if small: signalRegions = smallRegion

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

baseDir = '/data/'+username+'/Results2016/'


nominalDir  = 'Prediction_Spring16_templates_SR2016_v1_lep_MC_3p99/' 
WupDir      = 'Prediction_Spring16_templates_SR2016_v1_100p_lep_MC_WPol_Wup_3p99/' 
WdownDir    = 'Prediction_Spring16_templates_SR2016_v1_100p_lep_MC_WPol_Wdown_3p99/' 
TTupDir     = 'Prediction_Spring16_templates_SR2016_v1_100p_lep_MC_WPol_TTup_3p99/' 
TTdownDir   = 'Prediction_Spring16_templates_SR2016_v1_100p_lep_MC_WPol_TTdown_3p99/' 


savePkl = True

prefix = 'singleLeptonic_Spring16_'
#postfix = '_kappa_corrected'
postfix = ''


TT_up     = pickle.load(file(baseDir+TTupDir+prefix+'_estimationResults_pkl'+postfix))
TT_down   = pickle.load(file(baseDir+TTdownDir+prefix+'_estimationResults_pkl'+postfix))
W_up      = pickle.load(file(baseDir+WupDir+prefix+'_estimationResults_pkl'+postfix))
W_down    = pickle.load(file(baseDir+WdownDir+prefix+'_estimationResults_pkl'+postfix))
nominal   = pickle.load(file(baseDir+nominalDir+prefix+'_estimationResults_pkl'+postfix))


W_Up_H  = ROOT.TH1F('W_Up_H','b Up',bins,0,bins)
W_Down_H  = ROOT.TH1F('W_Down_H','b Down',bins,0,bins)
TT_Up_H  = ROOT.TH1F('TT_Up_H','b Up',bins,0,bins)
TT_Down_H  = ROOT.TH1F('TT_Down_H','b Down',bins,0,bins)

zero_H = ROOT.TH1F('zero_H','zero',bins,0,bins)

i = 1

W_err = {}

key = 'tot_pred'
keyTruth = 'tot_truth'

for i_njb, srNJet in enumerate(sorted(signalRegions)): #just changed this Nov 4th, not sorted before!
  W_err[srNJet] = {}
  for stb in sorted(signalRegions[srNJet]):
    W_err[srNJet][stb] = {}
    for htb in sorted(signalRegions[srNJet][stb]):
      W_err[srNJet][stb][htb] = {}

      print
      print '#############################################'
      print 'bin: \t njet \t\t LT \t\t HT'
      if len(str(srNJet))<7:
        print '\t',srNJet,'\t\t',stb,'\t',htb
      else:
        print '\t',srNJet,'\t',stb,'\t',htb
      print
      W_upDiff    = (W_up[srNJet][stb][htb][key]    / W_up[srNJet][stb][htb][keyTruth])   / (nominal[srNJet][stb][htb][key]/nominal[srNJet][stb][htb][keyTruth]) - 1
      W_downDiff  = (W_down[srNJet][stb][htb][key]  / W_down[srNJet][stb][htb][keyTruth]) / (nominal[srNJet][stb][htb][key]/nominal[srNJet][stb][htb][keyTruth]) - 1
      TT_upDiff   = (TT_up[srNJet][stb][htb][key]   / TT_up[srNJet][stb][htb][keyTruth])  / (nominal[srNJet][stb][htb][key]/nominal[srNJet][stb][htb][keyTruth]) - 1
      TT_downDiff = (TT_down[srNJet][stb][htb][key] / TT_down[srNJet][stb][htb][keyTruth])/ (nominal[srNJet][stb][htb][key]/nominal[srNJet][stb][htb][keyTruth]) - 1
      #W_upDiff    = (W_up[srNJet][stb][htb][key]    - nominal[srNJet][stb][htb][key]) / nominal[srNJet][stb][htb][key]
      #W_downDiff  = (W_down[srNJet][stb][htb][key]  - nominal[srNJet][stb][htb][key]) / nominal[srNJet][stb][htb][key]
      #TT_upDiff   = (TT_up[srNJet][stb][htb][key]   - nominal[srNJet][stb][htb][key]) / nominal[srNJet][stb][htb][key]
      #TT_downDiff = (TT_down[srNJet][stb][htb][key] - nominal[srNJet][stb][htb][key]) / nominal[srNJet][stb][htb][key]
      print 'W up, down:', W_upDiff, W_downDiff
      print 'tt up, down:', TT_upDiff, TT_downDiff
      
      W_Up_H.SetBinContent(i,abs(W_upDiff))
      W_Down_H.SetBinContent(i,-abs(W_downDiff))
      TT_Up_H.SetBinContent(i,abs(TT_upDiff))
      TT_Down_H.SetBinContent(i,-abs(TT_downDiff))

      W_err[srNJet][stb][htb]['W'] = (abs(W_upDiff)+abs(W_downDiff))/2
      W_err[srNJet][stb][htb]['TT'] = (abs(TT_upDiff)+abs(TT_downDiff))/2
      i += 1


W_Up_H.SetLineColor(color('wjets'))
W_Up_H.SetMarkerStyle(0)
W_Up_H.SetLineWidth(2)

W_Down_H.SetLineColor(color('wjets'))
W_Down_H.SetMarkerStyle(0)
W_Down_H.SetLineWidth(2)

TT_Up_H.SetLineColor(color('ttjets'))
TT_Up_H.SetMarkerStyle(0)
TT_Up_H.SetLineWidth(2)
TT_Down_H.SetLineColor(color('ttjets'))
TT_Down_H.SetMarkerStyle(0)
TT_Down_H.SetLineWidth(2)



latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.035)
latex1.SetTextAlign(11)


can2 = ROOT.TCanvas('can2','can2',700,700)

W_Up_H.SetMinimum(-0.25)
W_Up_H.SetMaximum(0.25)


W_Up_H.Draw()
W_Down_H.Draw('same')
TT_Up_H.Draw('same')
TT_Down_H.Draw('same')

zero_H.Draw('same')

can2.RedrawAxis()

leg2 = ROOT.TLegend(0.65,0.85,0.98,0.95)
leg2.SetFillColor(ROOT.kWhite)
leg2.SetShadowColor(ROOT.kWhite)
leg2.SetBorderSize(1)
leg2.SetTextSize(0.04)
leg2.AddEntry(W_Up_H,'W+jets')
leg2.AddEntry(TT_Up_H,'tt+jets')

leg2.Draw()

latex1.DrawLatex(0.16,0.96,'CMS #bf{#it{simulation}}')
latex1.DrawLatex(0.81,0.96,"#bf{MC (13TeV)}")

setNiceBinLabel(W_Up_H, signalRegions)

W_Up_H.GetYaxis().SetTitle('#delta_{k}')
W_Up_H.GetXaxis().SetLabelSize(0.027)
W_Up_H.GetYaxis().SetLabelSize(0.04)
W_Up_H.GetXaxis().SetTitle('')

if savePkl:
  pickle.dump(W_err, file(baseDir+'/systematics2016/Wpol_pkl','w'))


