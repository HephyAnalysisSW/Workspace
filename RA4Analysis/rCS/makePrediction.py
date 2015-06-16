import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v9_Phys14V3_HT400ST200_ForTTJetsUnc import *
from makeTTPrediction import makeTTPrediction
from makeWPrediction import makeWPrediction
from localInfo import username
from binnedNBTagsFit import binnedNBTagsFit
from rCShelpers import * 
from math import pi, sqrt
#from pred_helper import lumi,weight_str , weight_err_str
from Workspace.RA4Analysis.signalRegions import *

lepSel = 'hard'
 
cWJets  = getChain(WJetsHTToLNu[lepSel],histname='')
cTTJets = getChain(ttJets[lepSel],histname='')
cRest = getChain([DY[lepSel], singleTop[lepSel], TTVH[lepSel]],histname='')#no QCD 
#cRest = getChain(TTVH[lepSel],histname='')#no QCD 
cBkg = getChain([WJetsHTToLNu[lepSel], ttJets[lepSel], DY[lepSel], singleTop[lepSel], TTVH[lepSel]],histname='')#no QCD


#weight_str = 'weight_Up'
#weight_err_str = 'weight_Up*weight_Up'

signalRegions = signalRegion3fb     ##because 10 one is full
lumi = 3.

weight_str, weight_err_str = makeWeight(lumi)

samples={'W':cWJets, 'TT':cTTJets, 'Rest':cRest, 'Bkg':cBkg}

signal = True
if signal:
  allSignals=[
            #"SMS_T1tttt_2J_mGl1200_mLSP800",
            #"SMS_T1tttt_2J_mGl1500_mLSP100",
            #"SMS_T2tt_2J_mStop425_mLSP325",
            #"SMS_T2tt_2J_mStop500_mLSP325",
            #"SMS_T2tt_2J_mStop650_mLSP325",
            #"SMS_T2tt_2J_mStop850_mLSP100",
            {'name':'T5q^{4} 1.2/1.0/0.8', 'sample':T5qqqqWW_mGo1200_mCh1000_mChi800[lepSel], 'weight':weight_str, 'color':ROOT.kBlack},
            {'name':'T5q^{4} 1.5/0.8/0.1', 'sample':T5qqqqWW_mGo1500_mCh800_mChi100[lepSel],  'weight':weight_str, 'color':ROOT.kMagenta},
            #{'name':'T5q^{4} 1.0/0.8/0.7', 'sample':T5qqqqWW_mGo1000_mCh800_mChi700[lepSel],  'weight':weight_str, 'color':ROOT.kYellow},
            #"T1ttbbWW_mGo1000_mCh725_mChi715",
            #"T1ttbbWW_mGo1000_mCh725_mChi720",
            #"T1ttbbWW_mGo1300_mCh300_mChi290",
            #"T1ttbbWW_mGo1300_mCh300_mChi295",
            #"T5ttttDeg_mGo1000_mStop300_mCh285_mChi280",
            #"T5ttttDeg_mGo1000_mStop300_mChi280",
            #"T5ttttDeg_mGo1300_mStop300_mCh285_mChi280",
            #"T5ttttDeg_mGo1300_mStop300_mChi280",
  ]

  for s in allSignals:
    s['chain'] = getChain(s['sample'],histname='')

ROOT.TH1F().SetDefaultSumw2()

prefix = 'singleLeptonic_Phys14V3_'
presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80"

btagString = 'nBJetMediumCSV30'


defDeltaPhiCut = 1.0
#streg = [[(250, 350), deltaPhiCut], [(350, 450), deltaPhiCut], [(450, -1), deltaPhiCut]] 
streg = [(250, 350), (350, 450), (450, -1)]
htreg = [(500,750), (750,1000), (1000,1250), (1250,-1)]
njreg = [(5,5),(6,7),(8,-1)]
bjreg = (0,0)


small = False 
#small = 0
if small:
  streg = [(250,350)]
  htreg = [(500,750)]
  njreg = [(5,5),(6,-1)]

bins = {}

for srNJet in signalRegions:
  bins[srNJet] = {}
  for stb in signalRegions[srNJet]:
    bins[srNJet][stb] ={}
    for htb in signalRegions[srNJet][stb]:
#for i_htb, htb in enumerate(htreg):
#  bins[htb] = {}
#  for stb in streg:
#    bins[htb][stb] = {}
#    for srNJet in njreg:
      deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
      #deltaPhiCut = dynDeltaPhi(defDeltaPhiCut, stb)
      rd={}
      #join TT estimation results to dict
      makeTTPrediction(rd, samples, htb, stb, srNJet, presel, dPhiCut=deltaPhiCut, btagVarString = btagString, lumi=lumi)

      #join W estimation results to dict
      makeWPrediction(rd, samples, htb, stb, srNJet, presel, dPhiCut=deltaPhiCut, btagVarString = btagString, lumi=lumi)

      ##If you want to make prediction of one of the bkgs, comment out all the estimation of total Bkgs
      #estimate total background
      pred_total = rd['TT_pred'] + rd['W_pred'] + rd['Rest_truth']
      pred_total_PosPdg = 0.5*(rd['TT_pred']) + rd['W_PosPdg_pred'] + rd['Rest_PosPdg_truth']
      pred_total_NegPdg = 0.5*(rd['TT_pred']) + rd['W_NegPdg_pred'] + rd['Rest_NegPdg_truth']
      pred_total_err = sqrt(rd['TT_pred_err']**2 + rd['W_pred_err']**2 + rd['Rest_truth_err']**2)
      pred_total_PosPdg_err = sqrt((0.5*(rd['TT_pred_err']))**2 + rd['W_PosPdg_pred_err']**2 + rd['Rest_PosPdg_truth_err']**2)
      pred_total_NegPdg_err = sqrt((0.5*(rd['TT_pred_err']))**2 + rd['W_NegPdg_pred_err']**2 + rd['Rest_NegPdg_truth_err']**2)
      
      truth_total = rd['TT_truth'] + rd['W_truth'] + rd['Rest_truth']
      truth_total_PosPdg = 0.5*(rd['TT_truth']) + rd['W_PosPdg_truth'] + rd['Rest_PosPdg_truth']
      truth_total_NegPdg = 0.5*(rd['TT_truth']) + rd['W_NegPdg_truth'] + rd['Rest_NegPdg_truth']
      truth_total_err = sqrt(rd['TT_truth_err']**2 + rd['W_truth_err']**2 + rd['Rest_truth_err']**2)
      truth_total_PosPdg_err = sqrt((0.5*(rd['TT_truth_err']))**2 + rd['W_PosPdg_truth_err']**2 + rd['Rest_PosPdg_truth_err']**2)
      truth_total_NegPdg_err = sqrt((0.5*(rd['TT_truth_err']))**2 + rd['W_NegPdg_truth_err']**2 + rd['Rest_NegPdg_truth_err']**2)

      rd.update({\
                'tot_pred':pred_total,'tot_pred_err':pred_total_err,\
                'tot_PosPdg_pred':pred_total_PosPdg,'tot_PosPdg_pred_err':pred_total_PosPdg_err,\
                'tot_NegPdg_pred':pred_total_NegPdg,'tot_NegPdg_pred_err':pred_total_NegPdg_err,\
                'tot_truth':truth_total,'tot_truth_err':truth_total_err,\
                'tot_PosPdg_truth':truth_total_PosPdg,'tot_PosPdg_truth_err':truth_total_PosPdg_err,\
                'tot_NegPdg_truth':truth_total_NegPdg,'tot_NegPdg_truth_err':truth_total_NegPdg_err,\
                })

      name, cut =  nameAndCut(stb, htb, srNJet, btb=bjreg, presel=presel, btagVar = btagString)
      if signal:
        for s in allSignals:
          s['yield_NegPdg']     = getYieldFromChain(s['chain'], 'leptonPdg<0&&'+cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_str)
          s['yield_NegPdg_Var'] = getYieldFromChain(s['chain'], 'leptonPdg<0&&'+cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_err_str)
          s['FOM_NegPdg']       = getFOM(s['yield_NegPdg'],sqrt(s['yield_NegPdg_Var']),truth_total_NegPdg,truth_total_NegPdg_err) 
  
          s['yield_PosPdg']     = getYieldFromChain(s['chain'], 'leptonPdg>0&&'+cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_str)
          s['yield_PosPdg_Var'] = getYieldFromChain(s['chain'], 'leptonPdg>0&&'+cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_err_str)
          s['FOM_PosPdg']       = getFOM(s['yield_PosPdg'],sqrt(s['yield_PosPdg_Var']),truth_total_PosPdg,truth_total_PosPdg_err)

          rd.update({\
                      s['name']+'_yield_NegPdg':s['yield_NegPdg'],\
                      s['name']+'_yield_NegPdg_Var':s['yield_NegPdg_Var'],\
                      s['name']+'_FOM_NegPdg':s['FOM_NegPdg'],\
                      s['name']+'_yield_PosPdg':s['yield_PosPdg'],\
                      s['name']+'_yield_PosPdg_Var':s['yield_PosPdg_Var'],\
                      s['name']+'_FOM_PosPdg':s['FOM_PosPdg'],\
                    })

      #bins[htb][stb][srNJet]=rd
      bins[srNJet][stb][htb] = rd
path = '/data/'+username+'/PHYS14v3/withCSV/rCS_0b_'+str(lumi)+'fbSlidingWcorrectionMuonChannel/'
if not os.path.exists(path):
  os.makedirs(path)
pickle.dump(bins, file(path+prefix+'_estimationResults_pkl','w'))
print "written:" , path+prefix+'_estimationResults_pkl'

