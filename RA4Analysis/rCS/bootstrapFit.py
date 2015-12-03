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

weight_str, weight_err_str = makeWeight(lumi, sampleLumi=sampleLumi)

samples={'W':cWJets, 'TT':cTTJets, 'Rest':cRest, 'Bkg':cBkg, 'Data': cData}


stb = (250,350)
htb = (500,-1)
srNJet = (5,5)
dPhiCut = 1.
name, cut = nameAndCut(stb, htb, srNJet, btb=None, presel=presel, btagVar = nBTagVar)

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


for i in range(100):
  fit = binnedNBTagsFit(cut+"&&"+dPhiStr+"<"+str(dPhiCut), name+'_dPhi'+str(dPhiCut), samples = samples, prefix=name, bootstrap=True)
  w_pos.Fill(fit['W_PosPdg']['template'].GetBinContent(1)*fit['W_PosPdg']['yield'])
  w_neg.Fill(fit['W_NegPdg']['template'].GetBinContent(1)*fit['W_NegPdg']['yield'])
  tt.Fill(fit['TT_AllPdg']['template'].GetBinContent(1)*fit['TT_AllPdg']['yield'])
  rest_pos.Fill(fit['Rest_PosPdg']['template'].GetBinContent(1)*fit['Rest_PosPdg']['yield'])
  rest_neg.Fill(fit['Rest_NegPdg']['template'].GetBinContent(1)*fit['Rest_NegPdg']['yield'])
