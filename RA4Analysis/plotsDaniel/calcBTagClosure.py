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

prefix = 'singleLeptonic_Spring15_'
signalRegions = signalRegion3fb

ROOT.gStyle.SetOptTitle(0);
ROOT.gStyle.SetOptStat('')

lumi = 1.55
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

baseDir = '/data/'+username+'/Results2015/'
b_upDir =   'Prediction_SFtemplates_fullSR_lep_MC_SF_b_Up_2.1/'
b_downDir = 'Prediction_SFtemplates_fullSR_lep_MC_SF_b_Down_2.1/'
light_upDir =   'Prediction_SFtemplates_fullSR_lep_MC_SF_light_Up_2.1/'
light_downDir = 'Prediction_SFtemplates_fullSR_lep_MC_SF_light_Down_2.1/'

nominalDir = 'Prediction_SFtemplates_fullSR_lep_MC_SF_2.1/'
 
light_up =    pickle.load(file(baseDir+light_upDir+prefix+'_estimationResults_pkl_kappa_btag_corrected'))
light_down =  pickle.load(file(baseDir+light_downDir+prefix+'_estimationResults_pkl_kappa_btag_corrected'))
b_up =        pickle.load(file(baseDir+b_upDir+prefix+'_estimationResults_pkl_kappa_btag_corrected'))
b_down =      pickle.load(file(baseDir+b_downDir+prefix+'_estimationResults_pkl_kappa_btag_corrected'))
nominal =     pickle.load(file(baseDir+nominalDir+prefix+'_estimationResults_pkl_kappa_btag_corrected'))

varUp = []
varDown = []
signDown = 1
signUp = 1


Up_H  = ROOT.TH1F('Up_H','total Up',bins,0,bins)
Down_H  = ROOT.TH1F('Down_H','total Down',bins,0,bins)
b_Up_H  = ROOT.TH1F('b_Up_H','b Up',bins,0,bins)
b_Down_H  = ROOT.TH1F('b_Down_H','b Down',bins,0,bins)
light_Up_H  = ROOT.TH1F('light_Up_H','light Up',bins,0,bins)
light_Down_H  = ROOT.TH1F('light_Down_H','light Down',bins,0,bins)

max_H = ROOT.TH1F('max_H','total max',bins,0,bins)
min_H = ROOT.TH1F('min_H','total min',bins,0,bins)
zero_H = ROOT.TH1F('zero_H','zero',bins,0,bins)

i = 1

b_err = {}
l_err = {}

for i_njb, srNJet in sorted(enumerate(signalRegions)): #just changed this Nov 4th, not sorted before!
  b_err[srNJet] = {}
  l_err[srNJet] = {}
  for stb in sorted(signalRegions[srNJet]):
    b_err[srNJet][stb] = {}
    l_err[srNJet][stb] = {}
    for htb in sorted(signalRegions[srNJet][stb]):
      print
      print '#############################################'
      print 'bin: \t njet \t\t LT \t\t HT'
      if len(str(srNJet))<7:
        print '\t',srNJet,'\t\t',stb,'\t',htb
      else:
        print '\t',srNJet,'\t',stb,'\t',htb
      print
      light_upDiff   = (light_up[srNJet][stb][htb]['tot_pred']-nominal[srNJet][stb][htb]['tot_pred'])/nominal[srNJet][stb][htb]['tot_pred']
      light_downDiff = (light_down[srNJet][stb][htb]['tot_pred']-nominal[srNJet][stb][htb]['tot_pred'])/nominal[srNJet][stb][htb]['tot_pred']
      print 'light up, down:', light_upDiff, light_downDiff
      b_upDiff   = (b_up[srNJet][stb][htb]['tot_pred']-nominal[srNJet][stb][htb]['tot_pred'])/nominal[srNJet][stb][htb]['tot_pred']
      b_downDiff = (b_down[srNJet][stb][htb]['tot_pred']-nominal[srNJet][stb][htb]['tot_pred'])/nominal[srNJet][stb][htb]['tot_pred']
      upDiff = sqrt(light_upDiff**2 + b_upDiff**2)
      downDiff = sqrt(light_downDiff**2 + b_downDiff**2)
      Up_H.SetBinContent(i,-upDiff)
      Up_H.GetXaxis().SetBinLabel(i,str(i))
      Down_H.SetBinContent(i,downDiff)
      b_Up_H.SetBinContent(i,b_upDiff)
      b_Down_H.SetBinContent(i,b_downDiff)
      light_Up_H.SetBinContent(i,light_upDiff)
      light_Down_H.SetBinContent(i,light_downDiff)
      varUp.append(upDiff)
      varDown.append(downDiff)
      b_err[srNJet][stb][htb] = (abs(b_upDiff)+abs(b_downDiff))/2
      l_err[srNJet][stb][htb] = (abs(light_upDiff)+abs(light_downDiff))/2
      i += 1

can = ROOT.TCanvas('can','can',700,700)
#can.SetGrid()
#pad1=ROOT.TPad("pad1","MyTitle",0.,0.0,1.,1.)
#pad1.SetLeftMargin(0.15)
#pad1.SetBottomMargin(0.15)
#pad1.Draw()
#pad1.cd()

maxDown = max(map(abs,varDown))
if varDown[0]<0: signDown = -1
maxUp = max(map(abs,varUp))
if varUp[0]<0: signUp = -1

print
print 'Max. change to nominal for variation up:',maxUp*signUp
print 'Max. change to nominal for variation down:',maxDown*signDown

Up_H.GetXaxis().SetTitle('Signal Region #')
Up_H.GetXaxis().SetTitleSize(0.05)
Up_H.GetXaxis().SetTitleOffset(1.0)
Up_H.GetXaxis().SetLabelSize(0.08)

Up_H.GetYaxis().SetTitle('#delta_{k}')

Up_H.SetMinimum(-0.13)
Up_H.SetMaximum(0.13)
Up_H.SetFillColor(ROOT.kGray)
Up_H.SetMarkerStyle(0)
Down_H.SetFillColor(ROOT.kGray)
Up_H.SetLineColor(ROOT.kBlack)
Up_H.SetLineWidth(2)
Down_H.SetLineColor(ROOT.kBlack)
Down_H.SetLineWidth(2)
b_Up_H.SetLineColor(ROOT.kOrange+8)
b_Up_H.SetMarkerStyle(0)
b_Up_H.SetLineWidth(2)
b_Down_H.SetLineColor(ROOT.kOrange+8)
b_Down_H.SetLineWidth(2)
light_Up_H.SetLineColor(ROOT.kBlue)
light_Up_H.SetMarkerStyle(0)
light_Up_H.SetLineWidth(2)
light_Down_H.SetLineColor(ROOT.kBlue)
light_Down_H.SetLineWidth(2)

for i in range(1,bins+1):
  max_H.SetBinContent(i,-maxUp*signUp)
  min_H.SetBinContent(i,maxDown*signDown)
  zero_H.SetBinContent(i,0)
max_H.SetLineStyle(3)
min_H.SetLineStyle(3)

Up_H.Draw()
Down_H.Draw('same')
b_Up_H.Draw('same')
b_Down_H.Draw('same')
light_Up_H.Draw('same')
light_Down_H.Draw('same')

max_H.Draw('same')
min_H.Draw('same')
zero_H.Draw('same')

can.RedrawAxis()


leg = ROOT.TLegend(0.65,0.8,0.98,0.95)
leg.SetFillColor(ROOT.kWhite)
leg.SetShadowColor(ROOT.kWhite)
leg.SetBorderSize(1)
leg.SetTextSize(0.04)
leg.AddEntry(Up_H,'total')
leg.AddEntry(b_Up_H,'b/c var')
leg.AddEntry(light_Up_H,'light var')

leg.Draw()

latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.035)
latex1.SetTextAlign(11)

#latex1.DrawLatex(0.18,0.96,'CMS Simulation')
latex1.DrawLatex(0.15,0.96,'CMS #bf{#it{simulation}}')
latex1.DrawLatex(0.68,0.96,"L=2.1fb^{-1} (13TeV)")

setNiceBinLabel(Up_H, signalRegion3fb)
Up_H.GetXaxis().SetLabelSize(0.04)
Up_H.GetXaxis().SetTitle('')
