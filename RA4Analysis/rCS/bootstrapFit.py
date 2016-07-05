import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName

from makeTTPrediction import makeTTPrediction
from makeWPrediction import makeWPrediction
from Workspace.HEPHYPythonTools.user import username
from binnedNBTagsFit import binnedNBTagsFit
from rCShelpers import *
from math import pi, sqrt
from Workspace.RA4Analysis.signalRegions import *

from predictionConfig import *

ROOT.TH1F().SetDefaultSumw2()

weight_str, weight_err_str = makeWeight(lumi, sampleLumi=sampleLumi, reWeight=MCweight)

samples={'W':cWJets, 'TT':cTTJets, 'Rest':cRest, 'Bkg':cBkg, 'Data': cData}

#stb = (250,350)
#htb = (500,-1)
#srNJet = (5,5)
#dPhiCut = 1.
#name, cut = nameAndCut(stb, htb, srNJet, btb=None, presel=presel, btagVar = nBTagVar)

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

tt_err = ROOT.TH1F('tt_err','tt',bins,0,bins)
tt_WSB_err = ROOT.TH1F('tt_WSB_err','tt_WSB',bins,0,bins)
w_pos_err = ROOT.TH1F('w_pos_err','w pos',bins,0,bins)
w_neg_err = ROOT.TH1F('w_neg_err','w neg',bins,0,bins)
rest_pos_err = ROOT.TH1F('rest_pos_err','rest pos',bins,0,bins)
rest_neg_err = ROOT.TH1F('rest_neg_err','rest neg',bins,0,bins)

#QCD = QCDestimate
#
#QCD_dict={0:{'y':QCD[srNJet][stb][htb][(0,0)][dPhiCut]['NQCDpred_lowdPhi'], 'e':QCD[srNJet][stb][htb][(0,0)][dPhiCut]['NQCDpred_lowdPhi_err'], 'totalY':QCD[srNJet][stb][htb][(0,0)][dPhiCut]['NQCDpred']},\
#              1:{'y':QCD[srNJet][stb][htb][(1,1)][dPhiCut]['NQCDpred_lowdPhi'], 'e':QCD[srNJet][stb][htb][(1,1)][dPhiCut]['NQCDpred_lowdPhi_err'], 'totalY':QCD[srNJet][stb][htb][(1,1)][dPhiCut]['NQCDpred']},\
#              2:{'y':QCD[srNJet][stb][htb][(2,-1)][dPhiCut]['NQCDpred_lowdPhi'], 'e':QCD[srNJet][stb][htb][(2,-1)][dPhiCut]['NQCDpred_lowdPhi_err'], 'totalY':QCD[srNJet][stb][htb][(2,-1)][dPhiCut]['NQCDpred']}}

#fit = binnedNBTagsFit(cut+"&&"+dPhiStr+"<"+str(dPhiCut), name+'_dPhi'+str(dPhiCut), samples = samples, prefix=name)
#
#w_pos_max = fit['W_PosPdg']['yield_high']*fit['W_PosPdg']['template'].GetBinContent(1)*1.2
#w_pos_min = fit['W_PosPdg']['yield_low']*fit['W_PosPdg']['template'].GetBinContent(1)*0.8
#w_pos = ROOT.TH1F('w_pos','w_pos',100,w_pos_min,w_pos_max)
#
#w_neg_max = fit['W_NegPdg']['yield_high']*fit['W_NegPdg']['template'].GetBinContent(1)*1.2
#w_neg_min = fit['W_NegPdg']['yield_low']* fit['W_NegPdg']['template'].GetBinContent(1)*0.8
#w_neg = ROOT.TH1F('w_neg','w_neg',100,w_neg_min,w_neg_max)
#
#tt_max = fit['TT_AllPdg']['yield_high']*fit['TT_AllPdg']['template'].GetBinContent(1)*1.2
#tt_min = fit['TT_AllPdg']['yield_low']* fit['TT_AllPdg']['template'].GetBinContent(1)*0.8
#tt = ROOT.TH1F('tt','tt',100,tt_min,tt_max)
#
#rest_pos_max = fit['Rest_PosPdg']['yield_high']*fit['Rest_PosPdg']['template'].GetBinContent(1)*1.2
#rest_pos_min = fit['Rest_PosPdg']['yield_low']* fit['Rest_PosPdg']['template'].GetBinContent(1)*0.8
#rest_pos = ROOT.TH1F('rest_pos','rest_pos',100,rest_pos_min,rest_pos_max)
#
#rest_neg_max = fit['Rest_NegPdg']['yield_high']*fit['Rest_NegPdg']['template'].GetBinContent(1)*1.2
#rest_neg_min = fit['Rest_NegPdg']['yield_low']* fit['Rest_NegPdg']['template'].GetBinContent(1)*0.8
#rest_neg = ROOT.TH1F('rest_neg','rest_neg',100,rest_neg_min,rest_neg_max)


b = 1

signalRegions = signalRegions2016
n_bootstrap = 100
WSB = False

templateBootstrap = {'TTJets':{},'TTJets_mu':{}, 'WJets_PosPdg':{}, 'WJets_NegPdg':{}, 'Rest_PosPdg':{}, 'Rest_NegPdg':{}}

for i_njb, njb in enumerate(sorted(signalRegions)):
  templateBootstrap['TTJets'][njb] = {}
  templateBootstrap['TTJets_mu'][njb] = {}
  templateBootstrap['WJets_PosPdg'][njb] = {}
  templateBootstrap['WJets_NegPdg'][njb] = {}
  templateBootstrap['Rest_PosPdg'][njb] = {}
  templateBootstrap['Rest_NegPdg'][njb] = {}

  for stb in sorted(signalRegions[njb]):
    templateBootstrap['TTJets'][njb][stb] = {}
    templateBootstrap['TTJets_mu'][njb][stb] = {}
    templateBootstrap['WJets_PosPdg'][njb][stb] = {}
    templateBootstrap['WJets_NegPdg'][njb][stb] = {}
    templateBootstrap['Rest_PosPdg'][njb][stb] = {}
    templateBootstrap['Rest_NegPdg'][njb][stb] = {}

    for htb in sorted(signalRegions[njb][stb]):
      templateBootstrap['TTJets'][njb][stb][htb] = {}
      templateBootstrap['TTJets_mu'][njb][stb][htb] = {}
      templateBootstrap['WJets_PosPdg'][njb][stb][htb] = {}
      templateBootstrap['WJets_NegPdg'][njb][stb][htb] = {}
      templateBootstrap['Rest_PosPdg'][njb][stb][htb] = {}
      templateBootstrap['Rest_NegPdg'][njb][stb][htb] = {}

      print
      print '#############################################'
      print '## * njet:',njb
      print '## * LT:  ',stb
      print '## * HT:  ',htb
      print '#############################################'
      print
      dPhiCut = signalRegions[njb][stb][htb]['deltaPhi']
      srNJet = njb
      if WSB:
        srNJet = (3,4)
        presel += '&&abs(leptonPdg)==13'
      
      name, cut       = nameAndCut(stb, htb, srNJet, btb=None, presel=presel, btagVar = nBTagVar)
      WSBname, WSBcut = nameAndCut(stb, htb, (3,4), btb=None, presel=presel+'&&abs(leptonPdg)==13', btagVar = nBTagVar)

      fit     = binnedNBTagsFit(cut+"&&"+dPhiStr+"<"+str(dPhiCut), cut+"&&"+dPhiStr+"<"+str(dPhiCut), name+'_dPhi'+str(dPhiCut), samples = samples, prefix=name)
      fitWSB  = binnedNBTagsFit(WSBcut+"&&"+dPhiStr+"<"+str(dPhiCut), WSBcut+"&&"+dPhiStr+"<"+str(dPhiCut), WSBname+'_dPhi'+str(dPhiCut), samples = samples, prefix=WSBname)
      
      w_pos_max = fit['W_PosPdg']['yield_high']*fit['W_PosPdg']['template'].GetBinContent(1)*1.2
      w_pos_min = fit['W_PosPdg']['yield_low']*fit['W_PosPdg']['template'].GetBinContent(1)*0.8
      w_pos = ROOT.TH1F('w_pos','w_pos',100,w_pos_min,w_pos_max)
      
      w_neg_max = fit['W_NegPdg']['yield_high']*fit['W_NegPdg']['template'].GetBinContent(1)*1.2
      w_neg_min = fit['W_NegPdg']['yield_low']* fit['W_NegPdg']['template'].GetBinContent(1)*0.8
      w_neg = ROOT.TH1F('w_neg','w_neg',100,w_neg_min,w_neg_max)
      
      tt_max = fit['TT_AllPdg']['yield_high']*fit['TT_AllPdg']['template'].GetBinContent(1)*1.2
      tt_min = fit['TT_AllPdg']['yield_low']* fit['TT_AllPdg']['template'].GetBinContent(1)*0.8
      tt = ROOT.TH1F('tt','tt',100,tt_min,tt_max)
      
      tt_WSB_max = fitWSB['TT_AllPdg']['yield_high']*fitWSB['TT_AllPdg']['template'].GetBinContent(1)*1.2
      tt_WSB_min = fitWSB['TT_AllPdg']['yield_low']* fitWSB['TT_AllPdg']['template'].GetBinContent(1)*0.8
      tt_WSB = ROOT.TH1F('tt','tt',100,tt_WSB_min,tt_WSB_max)
      
      rest_pos_max = fit['Rest_PosPdg']['yield_high']*fit['Rest_PosPdg']['template'].GetBinContent(1)*1.2
      rest_pos_min = fit['Rest_PosPdg']['yield_low']* fit['Rest_PosPdg']['template'].GetBinContent(1)*0.8
      rest_pos = ROOT.TH1F('rest_pos','rest_pos',100,rest_pos_min,rest_pos_max)
      
      rest_neg_max = fit['Rest_NegPdg']['yield_high']*fit['Rest_NegPdg']['template'].GetBinContent(1)*1.2
      rest_neg_min = fit['Rest_NegPdg']['yield_low']* fit['Rest_NegPdg']['template'].GetBinContent(1)*0.8
      rest_neg = ROOT.TH1F('rest_neg','rest_neg',100,rest_neg_min,rest_neg_max)


      for i in range(n_bootstrap):
        'Bootstrapping now...', i
        fit     = binnedNBTagsFit(cut+"&&"+dPhiStr+"<"+str(dPhiCut), cut+"&&"+dPhiStr+"<"+str(dPhiCut), name+'_dPhi'+str(dPhiCut), samples = samples, prefix=name, bootstrap=True)
        fitWSB  = binnedNBTagsFit(WSBcut+"&&"+dPhiStr+"<"+str(dPhiCut), WSBcut+"&&"+dPhiStr+"<"+str(dPhiCut), WSBname+'_dPhi'+str(dPhiCut), samples = samples, prefix=WSBname, bootstrap=True)
        w_pos.Fill(fit['W_PosPdg']['template'].GetBinContent(1)*fit['W_PosPdg']['yield'])
        w_neg.Fill(fit['W_NegPdg']['template'].GetBinContent(1)*fit['W_NegPdg']['yield'])
        tt.Fill(fit['TT_AllPdg']['template'].GetBinContent(1)*fit['TT_AllPdg']['yield'])
        tt_WSB.Fill(fitWSB['TT_AllPdg']['template'].GetBinContent(1)*fitWSB['TT_AllPdg']['yield'])
        rest_pos.Fill(fit['Rest_PosPdg']['template'].GetBinContent(1)*fit['Rest_PosPdg']['yield'])
        rest_neg.Fill(fit['Rest_NegPdg']['template'].GetBinContent(1)*fit['Rest_NegPdg']['yield'])
      
      if tt.GetMean()>0:
        tt_err.SetBinContent(b, tt.GetRMS()/tt.GetMean())
        templateBootstrap['TTJets'][njb][stb][htb] = tt.GetRMS()/tt.GetMean()
      if tt_WSB.GetMean()>0:
        tt_WSB_err.SetBinContent(b, tt_WSB.GetRMS()/tt_WSB.GetMean())
        templateBootstrap['TTJets_mu'][njb][stb][htb] = tt_WSB.GetRMS()/tt_WSB.GetMean()
      if w_pos.GetMean()>0:
        w_pos_err.SetBinContent(b, w_pos.GetRMS()/w_pos.GetMean())
        templateBootstrap['WJets_PosPdg'][njb][stb][htb] = w_pos.GetRMS()/w_pos.GetMean()
      if w_neg.GetMean()>0:
        w_neg_err.SetBinContent(b, w_neg.GetRMS()/w_neg.GetMean())
        templateBootstrap['WJets_NegPdg'][njb][stb][htb] = w_neg.GetRMS()/w_neg.GetMean()
      if rest_pos.GetMean()>0:
        rest_pos_err.SetBinContent(b, rest_pos.GetRMS()/rest_pos.GetMean())
        templateBootstrap['Rest_PosPdg'][njb][stb][htb] = rest_pos.GetRMS()/rest_pos.GetMean()
      if rest_neg.GetMean()>0:
        rest_neg_err.SetBinContent(b, rest_neg.GetRMS()/rest_neg.GetMean())
        templateBootstrap['Rest_NegPdg'][njb][stb][htb] = rest_neg.GetRMS()/rest_neg.GetMean()
      
      b += 1

tmpFile_TTJets =       ROOT.TFile('/data/dspitzbart/bootstrap2016/TTJets.root','new')
tt_err.Write()
tmpFile_TTJets.Close()

tmpFile_TTJets_mu =    ROOT.TFile('/data/dspitzbart/bootstrap2016/TTJets_mu.root','new')
tt_WSB_err.Write()
tmpFile_TTJets_mu.Close()

tmpFile_WJets_PosPdg = ROOT.TFile('/data/dspitzbart/bootstrap2016/WJets_PosPdg.root','new')
w_pos_err.Write()
tmpFile_WJets_PosPdg.Close()

tmpFile_WJets_NegPdg = ROOT.TFile('/data/dspitzbart/bootstrap2016/WJets_NegPdg.root','new')
w_neg_err.Write()
tmpFile_WJets_NegPdg.Close()

tmpFile_Rest_PosPdg =  ROOT.TFile('/data/dspitzbart/bootstrap2016/Rest_PosPdg.root','new')
rest_pos_err.Write()
tmpFile_Rest_PosPdg.Close()

tmpFile_Rest_NegPdg =  ROOT.TFile('/data/dspitzbart/bootstrap2016/Rest_NegPdg.root','new')
rest_neg_err.Write()
tmpFile_Rest_NegPdg.Close()

pickle.dump(templateBootstrap, file('/data/dspitzbart/bootstrap2016/bootstrap_unc_pkl','w'))
