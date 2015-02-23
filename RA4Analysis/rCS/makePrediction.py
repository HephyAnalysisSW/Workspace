import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400ST150 import *
from makeTTPrediction import makeTTPrediction
from makeWPrediction import makeWPrediction
from localInfo import username
from binnedNBTagsFit import binnedNBTagsFit
from rCShelpers import * 
from math import pi, sqrt

lepSel = 'hard'
 
cWJets  = getChain(WJetsHTToLNu[lepSel],histname='')
cTTJets = getChain(ttJets[lepSel],histname='')
cRest = getChain([DY[lepSel], singleTop[lepSel], TTVH[lepSel]],histname='')#no QCD 
cBkg = getChain([WJetsHTToLNu[lepSel], ttJets[lepSel], DY[lepSel], singleTop[lepSel], TTVH[lepSel]],histname='')#no QCD

samples={'W':cWJets, 'TT':cTTJets, 'Rest':cRest, 'Bkg':cBkg}

ROOT.TH1F().SetDefaultSumw2()

prefix = 'singleLeptonic_20150223'
presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0"

streg = [[(250, 350), 1.], [(350, -1), 1.]] 
htreg = [(500,750),(750,-1)]
njreg = [(5,5),(6,-1)]

small = 1
#small = 0
if small == 1:
  streg = [(250,350),1.]
  htreg = (500,750)
  njreg = (6,-1)

dict = {}
for i_htb, htb in enumerate(htreg):
  dict[htb] = {}
  for stb, dPhiCut in streg:
    dict[htb][stb] = {}
    for srNJet in njreg:

      rd={}
      #join TT estimation results to dict
      makeTTPrediction(rd, samples, htb, stb, srNJet, presel, dPhiCut=1.0)
      #join W estimation results to dict
      makeWPrediction(rd, samples, htb, stb, srNJet, presel, dPhiCut=1.0)

      #estimate total background
      pred_total = rd['TT_pred'] + rd['W_pred'] + rd['Rest_truth']
      pred_total_PosPdg = 0.5*(rd['TT_pred']) + rd['W_PosPdg_pred'] + rd['Rest_PosPdg_truth']
      pred_total_NegPdg = 0.5*(rd['TT_pred']) + rd['W_NegPdg_pred'] + rd['Rest_NegPdg_truth']
      pred_total_err = rd['TT_pred_err'] + rd['W_pred_err'] + rd['Rest_truth_err']
      pred_total_PosPdg_err = 0.5*(rd['TT_pred_err']) + rd['W_PosPdg_pred_err'] + rd['Rest_PosPdg_truth_err']
      pred_total_NegPdg_err = 0.5*(rd['TT_pred_err']) + rd['W_NegPdg_pred_err'] + rd['Rest_NegPdg_truth_err']
      truth_total = rd['TT_truth'] + rd['W_truth'] + rd['Rest_truth']
      truth_total_PosPdg = 0.5*(rd['TT_truth']) + rd['W_PosPdg_truth'] + rd['Rest_PosPdg_truth']
      truth_total_NegPdg = 0.5*(rd['TT_truth']) + rd['W_NegPdg_truth'] + rd['Rest_NegPdg_truth']
      truth_total_err = rd['TT_truth_err'] + rd['W_truth_err'] + rd['Rest_truth_err']
      truth_total_PosPdg_err = 0.5*(rd['TT_truth_err']) + rd['W_PosPdg_truth_err'] + rd['Rest_PosPdg_truth_err']
      truth_total_NegPdg_err = 0.5*(rd['TT_truth_err']) + rd['W_NegPdg_truth_err'] + rd['Rest_NegPdg_truth_err']
      rd.update({\
                'tot_pred':pred_total,'tot_pred_err':pred_total_err,\
                'tot_PosPdg_pred':pred_total_PosPdg,'tot_PosPdg_pred_err':pred_total_PosPdg_err,\
                'tot_NegPdg_pred':pred_total_NegPdg,'tot_NegPdg_pred_err':pred_total_NegPdg_err,\
                'tot_truth':truth_total,'tot_truth_err':truth_total_err,\
                'tot_PosPdg_truth':truth_total_PosPdg,'tot_PosPdg_truth_err':truth_total_PosPdg_err,\
                'tot_NegPdg_truth':truth_total_NegPdg,'tot_NegPdg_truth_err':truth_total_NegPdg_err,\

                })

      dict[htb][stb][srNJet]=rd

pickle.dump(dict, file('/data/'+username+'/results2014/rCS_0b/'+prefix+'_estimationResults_pkl','w'))


