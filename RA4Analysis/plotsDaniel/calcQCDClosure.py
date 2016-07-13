import ROOT
import pickle
import os,sys,math
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName
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

#QCD_upDir      = 'Prediction_Spring16_templates_SR2016_v1_QCD_lep_MC_QCDup_3p99/'
#QCD_downDir    = 'Prediction_Spring16_templates_SR2016_v1_QCD_lep_MC_QCDdown_3p99/'
#QCD_nominalDir = 'Prediction_Spring16_templates_SR2016_v1_QCD_lep_MC_3p99/'

QCD_upDir      = 'Prediction_Spring16_templates_SR2016_v2_QCD_lep_MC_QCDup_3p99/'
QCD_downDir    = 'Prediction_Spring16_templates_SR2016_v2_QCD_lep_MC_QCDdown_3p99/'
QCD_nominalDir = 'Prediction_Spring16_templates_SR2016_v2_QCD_lep_MC_3p99/'


savePkl = True

prefix = 'singleLeptonic_Spring16_'
#postfix = '_kappa_corrected'
postfix = ''

qcd_up =      pickle.load(file(baseDir+QCD_upDir+prefix+'_estimationResults_pkl'+postfix))
qcd_down =    pickle.load(file(baseDir+QCD_downDir+prefix+'_estimationResults_pkl'+postfix))
qcd_nominal = pickle.load(file(baseDir+QCD_nominalDir+prefix+'_estimationResults_pkl'+postfix))


qcd_Up_H  = ROOT.TH1F('qcd_Up_H','b Up',bins,0,bins)
qcd_Down_H  = ROOT.TH1F('qcd_Down_H','b Down',bins,0,bins)

max_H = ROOT.TH1F('max_H','total max',bins,0,bins)
min_H = ROOT.TH1F('min_H','total min',bins,0,bins)
zero_H = ROOT.TH1F('zero_H','zero',bins,0,bins)

i = 1

qcd_err = {}

key = 'tot_pred'
keyTruth = 'tot_truth'

for i_njb, srNJet in enumerate(sorted(signalRegions)): #just changed this Nov 4th, not sorted before!
  qcd_err[srNJet] = {}
  for stb in sorted(signalRegions[srNJet]):
    qcd_err[srNJet][stb] = {}
    for htb in sorted(signalRegions[srNJet][stb]):
      print
      print '#############################################'
      print 'bin: \t njet \t\t LT \t\t HT'
      if len(str(srNJet))<7:
        print '\t',srNJet,'\t\t',stb,'\t',htb
      else:
        print '\t',srNJet,'\t',stb,'\t',htb
      print
      qcd_upDiff    = (qcd_up[srNJet][stb][htb][key]    / qcd_up[srNJet][stb][htb][keyTruth])   / (qcd_nominal[srNJet][stb][htb][key]/qcd_nominal[srNJet][stb][htb][keyTruth]) - 1
      qcd_downDiff  = (qcd_down[srNJet][stb][htb][key]  / qcd_down[srNJet][stb][htb][keyTruth]) / (qcd_nominal[srNJet][stb][htb][key]/qcd_nominal[srNJet][stb][htb][keyTruth]) - 1

      #qcd_upDiff = (qcd_up[srNJet][stb][htb][key]-qcd_nominal[srNJet][stb][htb][key])/qcd_nominal[srNJet][stb][htb][key]
      #qcd_downDiff = (qcd_down[srNJet][stb][htb][key]-qcd_nominal[srNJet][stb][htb][key])/qcd_nominal[srNJet][stb][htb][key]
      print 'qcd up, down:', qcd_upDiff, qcd_downDiff
      
      qcd_Up_H.SetBinContent(i,qcd_upDiff)
      qcd_Down_H.SetBinContent(i,qcd_downDiff)

      qcd_err[srNJet][stb][htb] = (abs(qcd_upDiff)+abs(qcd_downDiff))/2
      i += 1


qcd_Up_H.SetLineColor(426)
qcd_Up_H.SetMarkerStyle(0)
qcd_Up_H.SetLineWidth(2)

qcd_Down_H.SetLineColor(426+4)
qcd_Down_H.SetMarkerStyle(0)
qcd_Down_H.SetLineWidth(2)


latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.035)
latex1.SetTextAlign(11)


can2 = ROOT.TCanvas('can2','can2',700,700)

qcd_Up_H.SetMinimum(-0.13)
qcd_Up_H.SetMaximum(0.13)


qcd_Up_H.Draw()
qcd_Down_H.Draw('same')
zero_H.Draw('same')

can2.RedrawAxis()

leg2 = ROOT.TLegend(0.65,0.85,0.98,0.95)
leg2.SetFillColor(ROOT.kWhite)
leg2.SetShadowColor(ROOT.kWhite)
leg2.SetBorderSize(1)
leg2.SetTextSize(0.04)
leg2.AddEntry(qcd_Up_H,'QCD up')
leg2.AddEntry(qcd_Down_H,'QCD down')

leg2.Draw()

latex1.DrawLatex(0.16,0.96,'CMS #bf{#it{simulation}}')
latex1.DrawLatex(0.81,0.96,"#bf{MC (13TeV)}")

setNiceBinLabel(qcd_Up_H, signalRegions)

qcd_Up_H.GetYaxis().SetTitle('#delta_{k}')
qcd_Up_H.GetXaxis().SetLabelSize(0.027)
qcd_Up_H.GetYaxis().SetLabelSize(0.04)
qcd_Up_H.GetXaxis().SetTitle('')

if savePkl:
  pickle.dump(qcd_err, file(baseDir+'systematics2016/qcdErr_pkl','w'))


