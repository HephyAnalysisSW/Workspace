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
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--nSR", dest="nSR", default=0, action="store", help="enter the number of SR you want to enter 0-27")
(options, args) = parser.parse_args()
          
nSR = int(options.nSR)
prefix = prefix+"_"+str(nSR)
signalRegions = signalRegions_Moriond2017_onebyone[nSR]
#signalRegions = signalRegions2016_onebyone[nSR]
#signalRegions = signalRegions2016_HT500_onebyone[nSR]

ROOT.TH1F().SetDefaultSumw2()

weight_str, weight_err_str = makeWeight(lumi, sampleLumi=sampleLumi, reWeight=MCweight)

samples={'W':cWJets, 'TT':cTTJets ,'Rest':cRest, 'Bkg':cBkg, 'Data': cData} #FIXME 'DiBoson1l':cDiboson_1l

signal = False
lepSel = 'hard'
if signal:
  allSignals=[
            {'name':'T5q^{4} 1.5/1.0', 'sample':SMS_T5qqqqVV_TuneCUETP8M1[1500][1000],  'weight':weight_str, 'color':ROOT.kAzure+9},
            {'name':'T5q^{4} 1.9/0.1', 'sample':SMS_T5qqqqVV_TuneCUETP8M1[1900][100],  'weight':weight_str, 'color':ROOT.kMagenta+2},
  ]

  for s in allSignals:
    s['chain'] = getChain(s['sample'],histname='')

bins = {}

if isData: dataSetString = 'data'
else: dataSetString = 'MC'
if QCDestimate: qcdstring = QCDpickle
else: qcdstring = 'not used'
if useBTagWeights: btagweightstring = 'b-tag weights used with suffix:'+btagWeightSuffix
else: btagweightstring = 'b-tag weights not used'
if unblinded: blindingstring = 'Results will be shown UNBLINDED'
elif validation: blindingstring = 'Results will be shown for validation, please check that SR are chosen accordingly'
else: blindingstring = 'We are still blinded, data yields in SR will not be shown!'
if templateBootstrap: bootstrapMessage='Using template-uncertainties obtained from bootstrapping'
else: bootstrapMessage='Not using additional template uncertainties'

print 
print 'Starting prediction with', dataSetString
print blindingstring
print
print 'Signal regions:', signalRegions
print
print 'Datalumi, templatelumi, samplelumi:',lumi,templateLumi,sampleLumi
print 'W sideband:',wjetsSB
print 'b-tag multiplicity:',bjreg
print 'QCD estimation:', qcdstring
print btagweightstring
print 'Result will be saved in:', pickleDir
print 'Plots will be saved in:', printDir
print 'Templates will be saved in:', templateDir
print bootstrapMessage
print 'Preselection to be used:'
print presel
print
print 'That is all for now, see you in a few hours!'
print


for srNJet in signalRegions:
  bins[srNJet] = {}
  for stb in signalRegions[srNJet]:
    bins[srNJet][stb] ={}
    for htb in signalRegions[srNJet][stb]:
      deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
      rd={}
      rd['deltaPhiCut'] = deltaPhiCut
      #join TT estimation results to dict
      print
      print '#################################################'
      print '## Prediction for SR',str(srNJet),str(stb),str(htb)
      print '## Using a dPhi cut value of',str(deltaPhiCut)
      print '#################################################'
      print
      makeTTPrediction(rd, samples, htb, stb, srNJet, presel, presel_MC, dPhiCut=deltaPhiCut, QCD=QCDestimate)

      #join W estimation results to dict
      makeWPrediction(rd, samples, htb, stb, srNJet, presel, presel_MC, dPhiCut=deltaPhiCut, QCD=QCDestimate)

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
      
      #write out data yields in MB, edit for blinding policies
      if isData or not useBTagWeights:
        srName, srCut = nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel, btagVar = nBTagVar)
        weight_str_sr = '(1)'
      else:
        srName, srCut = nameAndCut(stb, htb, srNJet, btb=None, presel=presel, btagVar = nBTagVar)
        weight_str_sr = weight_str+'*weightBTag0_SF'
      
      if unblinded or validation:
        y_srNJet_0b_highDPhi, y_Var_srNJet_0b_highDPhi = getYieldFromChain(cData, srCut+'&&deltaPhi_Wl>='+str(deltaPhiCut), weight_str_sr, returnVar=True)
        rd['y_srNJet_0b_highDPhi'] = y_srNJet_0b_highDPhi
        rd['y_Var_srNJet_0b_highDPhi'] = y_Var_srNJet_0b_highDPhi

      y_srNJet_0b_lowDPhi, y_Var_srNJet_0b_lowDPhi = getYieldFromChain(cData, srCut+'&&deltaPhi_Wl<'+str(deltaPhiCut), weight_str_sr, returnVar=True)
      rd['y_srNJet_0b_lowDPhi'] = y_srNJet_0b_lowDPhi
      rd['y_Var_srNJet_0b_lowDPhi'] = y_Var_srNJet_0b_lowDPhi

      rd.update({\
                'tot_pred':pred_total,'tot_pred_err':pred_total_err,\
                'tot_PosPdg_pred':pred_total_PosPdg,'tot_PosPdg_pred_err':pred_total_PosPdg_err,\
                'tot_NegPdg_pred':pred_total_NegPdg,'tot_NegPdg_pred_err':pred_total_NegPdg_err,\
                'tot_truth':truth_total,'tot_truth_err':truth_total_err,\
                'tot_PosPdg_truth':truth_total_PosPdg,'tot_PosPdg_truth_err':truth_total_PosPdg_err,\
                'tot_NegPdg_truth':truth_total_NegPdg,'tot_NegPdg_truth_err':truth_total_NegPdg_err,\
                })

      name, cut =  nameAndCut(stb, htb, srNJet, btb=bjreg, presel=presel, btagVar = nBTagVar)
      if signal:
        for s in allSignals:
          s['yield_NegPdg']     = getYieldFromChain(s['chain'], 'leptonPdg<0&&'+cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_str)
          s['yield_NegPdg_Var'] = getYieldFromChain(s['chain'], 'leptonPdg<0&&'+cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_err_str)
          s['FOM_NegPdg']       = getFOM(s['yield_NegPdg'],sqrt(s['yield_NegPdg_Var']),truth_total_NegPdg,truth_total_NegPdg_err) 
  
          s['yield_PosPdg']     = getYieldFromChain(s['chain'], 'leptonPdg>0&&'+cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_str)
          s['yield_PosPdg_Var'] = getYieldFromChain(s['chain'], 'leptonPdg>0&&'+cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_err_str)
          s['FOM_PosPdg']       = getFOM(s['yield_PosPdg'],sqrt(s['yield_PosPdg_Var']),truth_total_PosPdg,truth_total_PosPdg_err)

          s['yield']     = getYieldFromChain(s['chain'], cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_str)
          s['yield_Var'] = getYieldFromChain(s['chain'], cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_err_str)
          s['FOM']       = getFOM(s['yield'],sqrt(s['yield_Var']),truth_total_PosPdg,truth_total_PosPdg_err)

          rd.update({\
                      s['name']+'_yield_NegPdg':s['yield_NegPdg'],\
                      s['name']+'_yield_NegPdg_Var':s['yield_NegPdg_Var'],\
                      s['name']+'_FOM_NegPdg':s['FOM_NegPdg'],\
                      s['name']+'_yield_PosPdg':s['yield_PosPdg'],\
                      s['name']+'_yield_PosPdg_Var':s['yield_PosPdg_Var'],\
                      s['name']+'_FOM_PosPdg':s['FOM_PosPdg'],\
                      s['name']+'_yield':s['yield'],\
                      s['name']+'_yield_Var':s['yield_Var'],\
                      s['name']+'_FOM':s['FOM'],\
                    })

      bins[srNJet][stb][htb] = rd

pickle.dump(bins, file(pickleDir+prefix+'_estimationResults_pkl','w'))
print "written:" , pickleDir+prefix+'_estimationResults_pkl'
