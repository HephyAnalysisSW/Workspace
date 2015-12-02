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

fit = binnedNBTagsFit(cut+"&&"+dPhiStr+"<"+str(dPhiCut), name+'_dPhi'+str(dPhiCut), samples = samples, prefix=name)

w_pos = ROOT.TH1F('w_pos','w_pos',200,0,1.)
w_neg = ROOT.TH1F('w_neg','w_neg',200,0,1.)
tt = ROOT.TH1F('tt','tt',200,0,1.)
rest_pos = ROOT.TH1F('rest_pos','rest_pos',200,0,1.)
rest_neg = ROOT.TH1F('rest_neg','rest_neg',200,0,1.)


for i in range(100):
  fit = binnedNBTagsFit(cut+"&&"+dPhiStr+"<"+str(dPhiCut), name+'_dPhi'+str(dPhiCut), samples = samples, prefix=name, bootstrap=True)
  w_pos.Fill(fit['W_PosPdg']['template'].GetBinContent(1))
  w_neg.Fill(fit['W_NegPdg']['template'].GetBinContent(1))
  tt.Fill(fit['TT_AllPdg']['template'].GetBinContent(1))
  rest_pos.Fill(fit['Rest_PosPdg']['template'].GetBinContent(1))
  rest_neg.Fill(fit['Rest_NegPdg']['template'].GetBinContent(1))
