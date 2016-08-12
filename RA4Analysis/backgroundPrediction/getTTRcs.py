import ROOT
import pickle
import os,sys
from math import pi, sqrt

from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.HEPHYPythonTools.asym_float import *
from Workspace.RA4Analysis.helpers import *

from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.binnedNBTagsFit import *
from Workspace.RA4Analysis.rCShelpers import *

def getTTRcs(samples, htb, stb, srNJet, presel, presel_MC, configs, deltaPhiCut=1.0, weight='weight', QCD_dict={}):
  isData            = configs['isData']
  useBTagWeights    = configs['useBTagWeights']
  btagWeightSuffix  = configs['btagWeightSuffix']
  weight_str        = configs['weight_str']
  weight_err_str    = configs['weight_err_str']
  ttjetsSB          = configs['ttjetsSB']
  wjetsSB           = configs['wjetsSB']
  nBTagVar          = configs['nBTagVar']
  dPhiStr           = configs['dPhiStr']


  cWJets = samples['W']
  cTTJets = samples['TT']
  cRest = samples['Rest']
  cBkg = samples['Bkg'] 
  cData = samples['Data']
  rd={}
  
  nJetCR = ttjetsSB
  
  if useBTagWeights:
    if isData:
      TTSB_name,    TTSB_cut    = nameAndCut(stb, htb, nJetCR, btb=(1,1), presel=presel, btagVar = nBTagVar)
    else:
      TTSB_name,    TTSB_cut    = nameAndCut(stb, htb, nJetCR, btb=None, presel=presel, btagVar = nBTagVar)
    TTSB_name_MC, TTSB_cut_MC = nameAndCut(stb, htb, nJetCR, btb=None, presel=presel_MC, btagVar = nBTagVar)
    weight_str_1b   = weight_str + '*weightBTag1'+btagWeightSuffix
    weight_str_1bMC = weight_str + '*weightBTag1_SF'
    weight_str_0bMC = weight_str + '*weightBTag0_SF'
  else:
    TTSB_name,    TTSB_cut    = nameAndCut(stb, htb, nJetCR, btb=(1,1), presel=presel, btagVar = nBTagVar)
    TTSB_name_MC, TTSB_cut_MC = nameAndCut(stb, htb, nJetCR, btb=(1,1), presel=presel_MC, btagVar = nBTagVar)
    weight_str_1b   = weight_str
    weight_str_1bMC = weight_str
    weight_str_0bMC = weight_str
  
  TTSB_CR_name    = TTSB_name + '_dPhi'+str(deltaPhiCut)
  TTSB_CR_cut     = TTSB_cut + "&&"+dPhiStr+"<"+str(deltaPhiCut)
  TTSB_CR_cut_MC  = TTSB_cut_MC + "&&"+dPhiStr+"<"+str(deltaPhiCut)
  
  QCD_lowDPhi  = QCD_dict[(1,1)]
  QCD_highDPhi = asym_float(0.,0.)
  
  print
  print 'Rcs(tt) pred'
  TT_Rcs_pred     = getRCSasym(cData, TTSB_cut, deltaPhiCut, weight=weight_str_1b, QCD_lowDPhi=QCD_lowDPhi, QCD_highDPhi=QCD_highDPhi, cutVar='deltaPhi_Wl', isData=isData)
  print TT_Rcs_pred.round(4)
  print 'Rcs(tt) MC 0b'
  TT_Rcs_MC_0b    = getRCSasym(cTTJets, TTSB_cut_MC, deltaPhiCut, weight=weight_str_0bMC, cutVar='deltaPhi_Wl', isData=False)
  print TT_Rcs_MC_0b.round(4)
  print 'Rcs(tt) MC 1b'
  TT_Rcs_MC_1b    = getRCSasym(cBkg, TTSB_cut_MC, deltaPhiCut, weight=weight_str_1bMC, cutVar='deltaPhi_Wl', isData=False)
  print TT_Rcs_MC_1b.round(4)

  rd['TT_Rcs_pred']   = TT_Rcs_pred
  rd['TT_Rcs_MC_0b']  = TT_Rcs_MC_0b
  rd['TT_Rcs_MC_1b']  = TT_Rcs_MC_1b
  
  return rd

