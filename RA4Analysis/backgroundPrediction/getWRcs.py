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

def getWRcs(samples, htb, stb, srNJet, presel, presel_MC, configs, deltaPhiCut=1.0, SBfits={}):
  isData            = configs['isData']
  useBTagWeights    = configs['useBTagWeights']
  btagWeightSuffix  = configs['btagWeightSuffix']
  weight_str        = configs['weight_str']
  weight_err_str    = configs['weight_err_str']
  ttjetsSB          = configs['ttjetsSB']
  wjetsSB           = configs['wjetsSB']
  nBTagVar          = configs['nBTagVar']
  dPhiStr           = configs['dPhiStr']
  templateBootstrap = configs['templateBootstrap']

  cWJets = samples['W']
  cTTJets = samples['TT']
  cRest = samples['Rest']
  cBkg = samples['Bkg'] 
  cData = samples['Data']
  rd={}
  
  nJetCR = wjetsSB
  
  WSB_name,    WSB_cut_fit    = nameAndCut(stb, htb, nJetCR, btb=None, presel=presel+'&&abs(leptonPdg)==13', btagVar = nBTagVar)
  WSB_name_MC, WSB_cut_fit_MC = nameAndCut(stb, htb, nJetCR, btb=None, presel=presel_MC+'&&abs(leptonPdg)==13', btagVar = nBTagVar)
  if useBTagWeights:
    if isData:
      WSB_name,    WSB_cut    = nameAndCut(stb, htb, nJetCR, btb=(0,0), presel=presel+'&&abs(leptonPdg)==13', btagVar = nBTagVar)
    else:
      WSB_name,    WSB_cut    = nameAndCut(stb, htb, nJetCR, btb=None, presel=presel+'&&abs(leptonPdg)==13', btagVar = nBTagVar)
    WSB_name_MC, WSB_cut_MC = nameAndCut(stb, htb, nJetCR, btb=None, presel=presel_MC+'&&abs(leptonPdg)==13', btagVar = nBTagVar)
    weight_str_0b   = weight_str + '*weightBTag0'+btagWeightSuffix
    weight_str_0bMC = weight_str + '*weightBTag0_SF'
  else:
    WSB_name,    WSB_cut    = nameAndCut(stb, htb, nJetCR, btb=(0,0), presel=presel+'&&abs(leptonPdg)==13', btagVar = nBTagVar)
    WSB_name_MC, WSB_cut_MC = nameAndCut(stb, htb, nJetCR, btb=(0,0), presel=presel_MC+'&&abs(leptonPdg)==13', btagVar = nBTagVar)
    weight_str_0b   = weight_str
    weight_str_0bMC = weight_str
  
  WSB_CR_name    = WSB_name + '_dPhi'+str(deltaPhiCut)+'_muonChannel'
  WSB_CR_cut_fit     = WSB_cut_fit + "&&"+dPhiStr+"<"+str(deltaPhiCut)
  WSB_CR_cut_fit_MC  = WSB_cut_fit_MC + "&&"+dPhiStr+"<"+str(deltaPhiCut)
  
  performSBfit = False
  try:
    fit_WSB_CR = SBfits[stb][htb][deltaPhiCut]
  except KeyError:
    performSBfit = True
  if performSBfit:
    print 'performing new SB fit'
    QCD_placeHolder = {}
    zero = asym_float(0.,0.)
    for nb in [(0,0),(1,1),(2,-1)]:
      QCD_placeHolder[nb] = zero
    fit_WSB_CR = {}
    binnedNBTagsFit(WSB_CR_cut_fit, WSB_CR_cut_fit_MC, WSB_CR_name, samples, configs, QCD_dict=QCD_placeHolder, res=fit_WSB_CR)
    SBfits[stb][htb][deltaPhiCut] = fit_WSB_CR
  else:
    print 'found SB fit, saving time!'
  
  
  print
  print 'Rcs(tt) MC'
  TT_Rcs_MC = getRCSasym(cTTJets, WSB_cut_MC, deltaPhiCut, weight=weight_str_0bMC, cutVar='deltaPhi_Wl', isData=False)
  print TT_Rcs_MC.round(4)
  
  TT_lowDPhi = fit_WSB_CR['TT_AllPdg']
  if templateBootstrap:
    TTBootstrap = asym_float(1.,templateBootstrap['TTJets_mu'][srNJet][stb][htb])
  else:
    TTBootstrap = asym_float(1.,0.)
  TT_lowDPhi  = TT_lowDPhi * TTBootstrap
  TT_highDPhi = TT_lowDPhi * TT_Rcs_MC

  print
  print 'Rcs(W) pred'
  W_Rcs_pred = getRCSasym(cData, WSB_cut, deltaPhiCut, weight=weight_str_0b, QCD_lowDPhi=TT_lowDPhi, QCD_highDPhi=TT_highDPhi, cutVar='deltaPhi_Wl', isData=isData)
  print W_Rcs_pred.round(4)
  print
  print 'Rcs(W) MC'
  W_Rcs_MC   = getRCSasym(cWJets, WSB_cut_MC, deltaPhiCut, weight=weight_str_0bMC, cutVar='deltaPhi_Wl', isData=False)
  print W_Rcs_MC.round(4)
  rd['W_Rcs_pred']  = W_Rcs_pred
  rd['W_Rcs_MC']    = W_Rcs_MC
  rd['fit_WSB_CR']  = fit_WSB_CR
  
  return rd

