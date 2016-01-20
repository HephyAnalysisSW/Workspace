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

baseDir = '/data/'+username+'/Results2016/'
#QCD_upDir      = 'Prediction_SFtemplates_fullSR_lep_MC_QCDup_SF_QCDup_2.1/'
#QCD_downDir    = 'Prediction_SFtemplates_fullSR_lep_MC_QCDdown_SF_QCDdown_2.1/'
#QCD_nominalDir = 'Prediction_SFtemplates_fullSR_lep_MC_QCDzentral_SF_QCDzentral_2.1/'

b_upDir       = 'Prediction_SFtemplates_validation_lep_MC_SF_b_Up_2p3/'
b_downDir     = 'Prediction_SFtemplates_validation_lep_MC_SF_b_Down_2p3/'
light_upDir   = 'Prediction_SFtemplates_validation_lep_MC_SF_light_Up_2p3/'
light_downDir = 'Prediction_SFtemplates_validation_lep_MC_SF_light_Down_2p3/'
nominalDir    = 'Prediction_SFtemplates_validation_lep_MC_SF_2p3/'

savePkl = True

postfix = '_kappa_corrected'
#postfix = ''

light_up =    pickle.load(file(baseDir+light_upDir+prefix+'_estimationResults_pkl'+postfix))
light_down =  pickle.load(file(baseDir+light_downDir+prefix+'_estimationResults_pkl'+postfix))
b_up =        pickle.load(file(baseDir+b_upDir+prefix+'_estimationResults_pkl'+postfix))
b_down =      pickle.load(file(baseDir+b_downDir+prefix+'_estimationResults_pkl'+postfix))
nominal =     pickle.load(file(baseDir+nominalDir+prefix+'_estimationResults_pkl'+postfix))

#qcd_up =      pickle.load(file(baseDir+QCD_upDir+prefix+'_estimationResults_pkl'+postfix))
#qcd_down =    pickle.load(file(baseDir+QCD_downDir+prefix+'_estimationResults_pkl'+postfix))
#qcd_nominal = pickle.load(file(baseDir+QCD_nominalDir+prefix+'_estimationResults_pkl'+postfix))

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

qcd_Up_H  = ROOT.TH1F('qcd_Up_H','b Up',bins,0,bins)
qcd_Down_H  = ROOT.TH1F('qcd_Down_H','b Down',bins,0,bins)

max_H = ROOT.TH1F('max_H','total max',bins,0,bins)
min_H = ROOT.TH1F('min_H','total min',bins,0,bins)
zero_H = ROOT.TH1F('zero_H','zero',bins,0,bins)

i = 1

l_dict = {}
b_dict = {}


key = 'W_kappa'
keys = ['TT_kappa','W_kappa','tot_pred']

for key in keys:
  varUp = []
  varDown = []
  b_err = {}
  l_err = {}
  qcd_err = {}
  i = 1
  for i_njb, srNJet in enumerate(sorted(signalRegions)): #just changed this Nov 4th, not sorted before!
    b_err[srNJet] = {}
    l_err[srNJet] = {}
    qcd_err[srNJet] = {}
    for stb in sorted(signalRegions[srNJet]):
      b_err[srNJet][stb] = {}
      l_err[srNJet][stb] = {}
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
        light_upDiff   = (light_up[srNJet][stb][htb][key]-nominal[srNJet][stb][htb][key])/nominal[srNJet][stb][htb][key]
        light_downDiff = (light_down[srNJet][stb][htb][key]-nominal[srNJet][stb][htb][key])/nominal[srNJet][stb][htb][key]
        print 'light up, down:', light_upDiff, light_downDiff
        b_upDiff   = (b_up[srNJet][stb][htb][key]-nominal[srNJet][stb][htb][key])/nominal[srNJet][stb][htb][key]
        b_downDiff = (b_down[srNJet][stb][htb][key]-nominal[srNJet][stb][htb][key])/nominal[srNJet][stb][htb][key]
        print 'b/c up, down:', b_upDiff, b_downDiff
        #qcd_upDiff = (qcd_up[srNJet][stb][htb][key]-qcd_nominal[srNJet][stb][htb][key])/qcd_nominal[srNJet][stb][htb][key]
        #qcd_downDiff = (qcd_down[srNJet][stb][htb][key]-qcd_nominal[srNJet][stb][htb][key])/qcd_nominal[srNJet][stb][htb][key]
        #print 'qcd up, down:', qcd_upDiff, qcd_downDiff
        if sign(light_upDiff) == sign(light_downDiff): print '!!strange!!'
        if sign(light_upDiff)==1:
          light_pos = light_upDiff
          light_neg = light_downDiff
        else:
          light_neg = light_upDiff
          light_pos = light_downDiff
        if sign(b_upDiff) == sign(b_downDiff): print '!!strange!!'
        if sign(b_upDiff)==1:
          b_pos = b_upDiff
          b_neg = b_downDiff
        else:
          b_neg = b_upDiff
          b_pos = b_downDiff
        upDiff = sqrt(light_pos**2 + b_pos**2)
        downDiff = sqrt(light_neg**2 + b_neg**2)
        Up_H.SetBinContent(i,upDiff)
        Up_H.GetXaxis().SetBinLabel(i,str(i))
        Down_H.SetBinContent(i,-downDiff)
      
        b_Up_H.SetBinContent(i,b_pos)
        b_Down_H.SetBinContent(i,b_neg)
        light_Up_H.SetBinContent(i,light_pos)
        light_Down_H.SetBinContent(i,light_neg)
        #qcd_Up_H.SetBinContent(i,qcd_upDiff)
        #qcd_Down_H.SetBinContent(i,qcd_downDiff)
  
        varUp.append(upDiff)
        varDown.append(-downDiff)
        b_err[srNJet][stb][htb] = (abs(b_upDiff)+abs(b_downDiff))/2
        l_err[srNJet][stb][htb] = (abs(light_upDiff)+abs(light_downDiff))/2
        #qcd_err[srNJet][stb][htb] = (abs(qcd_upDiff)+abs(qcd_downDiff))/2
        i += 1
  
  can = ROOT.TCanvas('can','can',700,700)
  #can.SetGrid()
  #pad1=ROOT.TPad("pad1","MyTitle",0.,0.0,1.,1.)
  #pad1.SetLeftMargin(0.15)
  #pad1.SetBottomMargin(0.15)
  #pad1.Draw()
  #pad1.cd()
  
  signUp = 1
  signDown = 1
  
  maxDown = max(map(abs,varDown))
  #if varDown[0]<0: signDown = -1
  maxUp = max(map(abs,varUp))
  #if varUp[0]<0: signUp = -1
  
  tot_max = max(map(abs,[maxUp,maxDown]))
  
  print
  print 'Max. change to nominal for variation up:',maxUp*signUp
  print 'Max. change to nominal for variation down:',maxDown*signDown
  
  Up_H.GetXaxis().SetTitle('Signal Region #')
  Up_H.GetXaxis().SetTitleSize(0.05)
  Up_H.GetXaxis().SetTitleOffset(1.0)
  Up_H.GetXaxis().SetLabelSize(0.08)
  
  Up_H.GetYaxis().SetTitle('#delta_{k}')
  
  Up_H.SetMinimum(-1.7*tot_max)
  Up_H.SetMaximum(1.7*tot_max)
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
  
  #qcd_Up_H.SetLineColor(426)
  #qcd_Up_H.SetMarkerStyle(0)
  #qcd_Up_H.SetLineWidth(2)
  #
  #qcd_Down_H.SetLineColor(426+4)
  #qcd_Down_H.SetMarkerStyle(0)
  #qcd_Down_H.SetLineWidth(2)
  
  
  for i in range(1,bins+1):
    max_H.SetBinContent(i,maxUp*signUp)
    min_H.SetBinContent(i,-maxDown*signDown)
    zero_H.SetBinContent(i,0)
  max_H.SetLineStyle(3)
  min_H.SetLineStyle(3)
  
  Up_H.Draw()
  Down_H.Draw('same')
  b_Up_H.Draw('same')
  b_Down_H.Draw('same')
  light_Up_H.Draw('same')
  light_Down_H.Draw('same')
  
  #qcd_Up_H.Draw('same')
  #qcd_Down_H.Draw('same')
  
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
  
  can.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016/btag_uncertainty/'+key+'.png')
  can.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016/btag_uncertainty/'+key+'.pdf')
  can.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016/btag_uncertainty/'+key+'.root')
  
  b_dict[key] = b_err
  l_dict[key] = l_err


#can2 = ROOT.TCanvas('can2','can2',700,700)
#
#qcd_Up_H.SetMinimum(-0.13)
#qcd_Up_H.SetMaximum(0.13)
#
#
#qcd_Up_H.Draw()
#qcd_Down_H.Draw('same')
##max_H.Draw('same')
##min_H.Draw('same')
#zero_H.Draw('same')
#
#can2.RedrawAxis()
#
#leg2 = ROOT.TLegend(0.65,0.85,0.98,0.95)
#leg2.SetFillColor(ROOT.kWhite)
#leg2.SetShadowColor(ROOT.kWhite)
#leg2.SetBorderSize(1)
#leg2.SetTextSize(0.04)
#leg2.AddEntry(qcd_Up_H,'QCD up')
#leg2.AddEntry(qcd_Down_H,'QCD down')
#
#leg2.Draw()
#
#latex1.DrawLatex(0.15,0.96,'CMS #bf{#it{simulation}}')
#latex1.DrawLatex(0.68,0.96,"L=2.1fb^{-1} (13TeV)")
#
#setNiceBinLabel(qcd_Up_H, signalRegion3fb)
#
#qcd_Up_H.GetYaxis().SetTitle('#delta_{k}')
#qcd_Up_H.GetXaxis().SetLabelSize(0.04)
#qcd_Up_H.GetXaxis().SetTitle('')

if savePkl:
  pickle.dump(b_dict, file(baseDir+'btagErr_pkl','w'))
  pickle.dump(l_dict, file(baseDir+'mistagErr_pkl','w'))
  #pickle.dump(qcd_err, file(baseDir+'qcdErr_pkl','w'))


