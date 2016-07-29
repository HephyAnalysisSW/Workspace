import ROOT
import pickle
import os,sys,math
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName
from Workspace.HEPHYPythonTools.user import username
from math import pi, sqrt
from Workspace.RA4Analysis.signalRegions import *

from helpers import *

from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *


triggers = "(HLT_EleHT350||HLT_MuHT350)"
#filters = "Flag_goodVertices && Flag_HBHENoiseFilter_fix && Flag_CSCTightHaloFilter && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter"
filters = "Flag_goodVertices && Flag_HBHENoiseFilter_fix && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter && veto_evt_list"
presel = "((!isData&&singleLeptonic)||(isData&&"+triggers+"&&((muonDataSet&&singleMuonic)||(eleDataSet&&singleElectronic))&&"+filters+"))"
presel += "&& nLooseHardLeptons==1 && nTightHardLeptons==1 && nLooseSoftLeptons==0 && Jet_pt[1]>80 && st>250 && nJet30>2 && htJet30j>500"

MCweight = 'lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*0.94'


ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()

prefix = 'singleLeptonic_Spring16_'
signalRegions = signalRegions2016

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


b_upDir       = 'Prediction_Spring16_templates_SR2016_v2_lep_MC_SF_b_Down_12p9/'
b_downDir     = 'Prediction_Spring16_templates_SR2016_v2_lep_MC_SF_b_Down_12p9/'
light_upDir   = 'Prediction_Spring16_templates_SR2016_v2_lep_MC_SF_light_Up_12p9/'
light_downDir = 'Prediction_Spring16_templates_SR2016_v2_lep_MC_SF_light_Down_12p9/'
nominalDir    = 'Prediction_Spring16_templates_SR2016_v2_lep_MC_SF_12p9/'

topDir        = 'Prediction_SFtemplates_fullSR_lep_MC_SF_noTopPTweights2_2p25/'

#b_upDir       = 'Prediction_SFtemplates_validation_lep_MC_SF_b_Up_2p3/'
#b_downDir     = 'Prediction_SFtemplates_validation_lep_MC_SF_b_Down_2p3/'
#light_upDir   = 'Prediction_SFtemplates_validation_lep_MC_SF_light_Up_2p3/'
#light_downDir = 'Prediction_SFtemplates_validation_lep_MC_SF_light_Down_2p3/'
#nominalDir    = 'Prediction_SFtemplates_validation_lep_MC_SF_2p3/'

savePkl = True

#postfix = '_kappa_corrected'
postfix = ''

light_up =    pickle.load(file(baseDir+light_upDir+prefix+'_estimationResults_pkl'+postfix))
light_down =  pickle.load(file(baseDir+light_downDir+prefix+'_estimationResults_pkl'+postfix))
b_up =        pickle.load(file(baseDir+b_upDir+prefix+'_estimationResults_pkl'+postfix))
b_down =      pickle.load(file(baseDir+b_downDir+prefix+'_estimationResults_pkl'+postfix))
nominal =     pickle.load(file(baseDir+nominalDir+prefix+'_estimationResults_pkl'+postfix))

#top = pickle.load(file(baseDir+topDir+prefix+'_estimationResults_pkl'+postfix))

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

#cWJets      = getChain(WJetsHTToLNu_25ns,histname='')
#cTTJets     = getChain(TTJets_combined,histname='')
#cBkg        = getChain([WJetsHTToLNu_25ns, TTJets_combined, singleTop_25ns, DY_25ns, TTV_25ns], histname='')#no QCD


key = 'W_kappa'
#keys = ['TT_kappa','W_kappa','tot_pred']
keys = ['tot_pred']

for key in keys:
  varUp = []
  varDown = []
  b_err = {}
  l_err = {}
  qcd_err = {}
  top_err = {}
  i = 1
  for i_njb, srNJet in enumerate(sorted(signalRegions)): #just changed this Nov 4th, not sorted before!
    b_err[srNJet] = {}
    l_err[srNJet] = {}
    qcd_err[srNJet] = {}
    top_err[srNJet] = {}
    for stb in sorted(signalRegions[srNJet]):
      b_err[srNJet][stb] = {}
      l_err[srNJet][stb] = {}
      qcd_err[srNJet][stb] = {}
      top_err[srNJet][stb] = {}
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
        b_upDiff   = -(b_up[srNJet][stb][htb][key]-nominal[srNJet][stb][htb][key])/nominal[srNJet][stb][htb][key]
        b_downDiff = (b_down[srNJet][stb][htb][key]-nominal[srNJet][stb][htb][key])/nominal[srNJet][stb][htb][key]
        print 'b/c up, down:', b_upDiff, b_downDiff
        
        #if key == 'tot_pred':
        #  n, cut = nameAndCut(stb,htb, srNJet, btb=None, presel=presel)
        #  truthPrime = getYieldFromChain(cBkg, cut+'&&deltaPhi_Wl>'+str(signalRegions[srNJet][stb][htb]['deltaPhi']), 'weightBTag0_SF*weight*(2.25/3.)*'+MCweight)
        #  truth = getYieldFromChain(cBkg, cut+'&&deltaPhi_Wl>'+str(signalRegions[srNJet][stb][htb]['deltaPhi']), 'weightBTag0_SF*weight*TopPtWeight*(2.25/3.)*'+MCweight)
        #  #print truthPrime, truth
        #
        #  #w_truthPrime = getYieldFromChain(cWJets, cut+'&&deltaPhi_Wl>'+str(signalRegions[srNJet][stb][htb]['deltaPhi']), 'weightBTag0_SF*weight*(2.25/3.)*'+MCweight)
        #  #w_truth = getYieldFromChain(cWJets, cut+'&&deltaPhi_Wl>'+str(signalRegions[srNJet][stb][htb]['deltaPhi']), 'weightBTag0_SF*weight*TopPtWeight*(2.25/3.)*'+MCweight)

        #  #tt_truthPrime = getYieldFromChain(cTTJets, cut+'&&deltaPhi_Wl>'+str(signalRegions[srNJet][stb][htb]['deltaPhi']), 'weightBTag0_SF*weight*(2.25/3.)*'+MCweight)
        #  #tt_truth = getYieldFromChain(cTTJets, cut+'&&deltaPhi_Wl>'+str(signalRegions[srNJet][stb][htb]['deltaPhi']), 'weightBTag0_SF*weight*TopPtWeight*(2.25/3.)*'+MCweight)
        #  alt_top_diff = (abs((top[srNJet][stb][htb]['TT_kappa']-nominal[srNJet][stb][htb]['TT_kappa'])/nominal[srNJet][stb][htb]['TT_kappa'])*nominal[srNJet][stb][htb]['TT_pred'] + abs((top[srNJet][stb][htb]['W_kappa']-nominal[srNJet][stb][htb]['W_kappa'])/nominal[srNJet][stb][htb]['W_kappa'])*nominal[srNJet][stb][htb]['W_pred'])/nominal[srNJet][stb][htb]['tot_pred']
        #          
        #  top_diff = (top[srNJet][stb][htb][key]/truthPrime)/(nominal[srNJet][stb][htb][key]/truth)-1
        #  #w_top_diff = (top[srNJet][stb][htb]['W_pred']/w_truthPrime)/(nominal[srNJet][stb][htb]['W_pred']/w_truth)-1
        #  #tt_top_diff = (top[srNJet][stb][htb]['TT_pred']/tt_truthPrime)/(nominal[srNJet][stb][htb]['TT_pred']/tt_truth)-1
        #  print 'top delta:', top_diff
        #  print 'alt top delta:', alt_top_diff
        #  #print 'W', w_top_diff,top[srNJet][stb][htb]['W_pred'], w_truthPrime, nominal[srNJet][stb][htb]['W_pred'], w_truth
        #  #print 'tt', tt_top_diff, top[srNJet][stb][htb]['TT_pred'], tt_truthPrime, nominal[srNJet][stb][htb]['TT_pred'], tt_truth
        
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
  
        varUp.append(upDiff)
        varDown.append(-downDiff)
        b_err[srNJet][stb][htb] = (abs(b_upDiff)+abs(b_downDiff))/2
        l_err[srNJet][stb][htb] = (abs(light_upDiff)+abs(light_downDiff))/2
        #top_err[srNJet][stb][htb] = top_diff
        i += 1
  
  can = ROOT.TCanvas('can','can',700,700)
  can.SetGrid()
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
  print tot_max
  print
  print 'Max. change to nominal for variation up:',maxUp*signUp
  print 'Max. change to nominal for variation down:',maxDown*signDown
  
  #Up_H.GetXaxis().SetTitle('Signal Region #')
  #Up_H.GetXaxis().SetTitleSize(0.05)
  #Up_H.GetXaxis().SetTitleOffset(1.0)
  #Up_H.GetXaxis().SetLabelSize(0.08)
  #
  #Up_H.GetYaxis().SetTitle('#delta_{k}')
  #
  #Up_H.SetMinimum(-0.2)
  #Up_H.SetMaximum(0.2)
  #Up_H.SetFillColor(ROOT.kGray)
  #Up_H.SetMarkerStyle(0)
  #Down_H.SetFillColor(ROOT.kGray)
  #Up_H.SetLineColor(ROOT.kBlack)
  #Up_H.SetLineWidth(2)
  #Down_H.SetLineColor(ROOT.kBlack)
  #Down_H.SetLineWidth(2)
  #b_Up_H.SetLineColor(ROOT.kOrange+8)
  #b_Up_H.SetMarkerStyle(0)
  #b_Up_H.SetLineWidth(2)
  #
  #b_Down_H.SetLineColor(ROOT.kOrange+8)
  #b_Down_H.SetLineWidth(2)
  #
  #light_Up_H.SetLineColor(ROOT.kBlue)
  #light_Up_H.SetMarkerStyle(0)
  #light_Up_H.SetLineWidth(2)
  #
  #light_Down_H.SetLineColor(ROOT.kBlue)
  #light_Down_H.SetLineWidth(2)
  #
  #for i in range(1,bins+1):
  #  max_H.SetBinContent(i,maxUp*signUp)
  #  min_H.SetBinContent(i,-maxDown*signDown)
  #  zero_H.SetBinContent(i,0)
  #max_H.SetLineStyle(3)
  #min_H.SetLineStyle(3)
  #
  #Up_H.Draw()
  #Down_H.Draw('same')
  #b_Up_H.Draw('same')
  #b_Down_H.Draw('same')
  #light_Up_H.Draw('same')
  #light_Down_H.Draw('same')
  #
  ##qcd_Up_H.Draw('same')
  ##qcd_Down_H.Draw('same')
  #
  #max_H.Draw('same')
  #min_H.Draw('same')
  #zero_H.Draw('same')
  #
  #can.RedrawAxis()
  #
  #
  #leg = ROOT.TLegend(0.65,0.8,0.98,0.95)
  #leg.SetFillColor(ROOT.kWhite)
  #leg.SetShadowColor(ROOT.kWhite)
  #leg.SetBorderSize(1)
  #leg.SetTextSize(0.04)
  #leg.AddEntry(Up_H,'total')
  #leg.AddEntry(b_Up_H,'b/c var')
  #leg.AddEntry(light_Up_H,'light var')
  #
  #leg.Draw()
  #
  #latex1 = ROOT.TLatex()
  #latex1.SetNDC()
  #latex1.SetTextSize(0.035)
  #latex1.SetTextAlign(11)
  #
  ##latex1.DrawLatex(0.18,0.96,'CMS Simulation')
  #latex1.DrawLatex(0.15,0.96,'CMS #bf{#it{simulation}}')
  #latex1.DrawLatex(0.68,0.96,"L=2.1fb^{-1} (13TeV)")
  #
  #setNiceBinLabel(Up_H, signalRegions)
  #Up_H.GetXaxis().SetLabelSize(0.027)
  #Up_H.GetXaxis().SetTitle('')
  #
  #can.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016/btag_uncertainty/'+key+'_approval.png')
  #can.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016/btag_uncertainty/'+key+'_approval.pdf')
  #can.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016/btag_uncertainty/'+key+'_approval.root')
  #
  b_dict[key] = b_err
  l_dict[key] = l_err


saveDir = '/data/dspitzbart/Results2016/systematics2016/'
if savePkl:
  pickle.dump(b_dict, file(saveDir+'btagErr_approval_pkl','w'))
  pickle.dump(l_dict, file(saveDir+'mistagErr_approval_pkl','w'))


