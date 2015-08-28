import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName
from Workspace.HEPHYPythonTools.user import username
from binnedNBTagsFit import binnedNBTagsFit
from rCShelpers import * 
from math import pi, sqrt
from rCShelpers import *

dPhiStr='deltaPhi_Wl'

ROOT.TH1F().SetDefaultSumw2()

def makeTTPrediction(bins, samples, htb, stb, srNJet, presel, dPhiCut=1.0, btagVarString = "nBJetMediumCSV30", lumi=4., printDir='/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Spring15/defaultDir/templateFit/'):
  print "in make tt prediction lumi is :" , lumi
  weight_str, weight_err_str = makeWeight(lumi)
  cWJets = samples['W']
  cTTJets = samples['TT']
  cRest = samples['Rest']
  cBkg = samples['Bkg']
  cData = samples['Data']
  rd = {}

  #TT Jets yield in srNJet, no b-tag cut, low DPhi
  fit_srName, fit_srCut = nameAndCut(stb, htb, srNJet, btb=None, presel=presel, btagVar = btagVarString) 
  fit_srNJet_lowDPhi = binnedNBTagsFit(fit_srCut+"&&"+dPhiStr+"<"+str(dPhiCut), samples = samples, nBTagVar = btagVarString, lumi=lumi, prefix=fit_srName, printDir=printDir)
#  fit_srNJet_lowDPhi = binnedNBTagsFit(fit_srCut+"&&"+dPhiStr+"<"+str(dPhiCut), samples = {'W':cWJets, 'TT':cTTJets}, nBTagVar = 'nBJetMedium25', prefix=fit_srName)
  rd['fit_srNJet_lowDPhi'] = fit_srNJet_lowDPhi

  yTT_srNJet_0b_lowDPhi =  fit_srNJet_lowDPhi['TT_AllPdg']['yield']*fit_srNJet_lowDPhi['TT_AllPdg']['template'].GetBinContent(1)
  yTT_Var_srNJet_0b_lowDPhi =  fit_srNJet_lowDPhi['TT_AllPdg']['yieldVar']*fit_srNJet_lowDPhi['TT_AllPdg']['template'].GetBinContent(1)**2

  rCS_crLowNJet_Name_1b, rCS_crLowNJet_Cut_1b = nameAndCut(stb, htb, (4,5), btb=(1,1), presel=presel, btagVar = btagVarString) 
  rCS_sr_Name_0b, rCS_sr_Cut_0b = nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel, btagVar = btagVarString)#for Check 
  #rCS_crLowNJet_1b = getRCS(cBkg, rCS_crLowNJet_Cut_1b,  dPhiCut) #Low njet tt-jets CR to be orthoganl to DPhi 
  rCS_crLowNJet_1b = getRCS(cData, rCS_crLowNJet_Cut_1b,  dPhiCut) #Low njet tt-jets CR to be orthoganl to DPhi 
  rCS_crLowNJet_1b_onlyTT = getRCS(cTTJets, rCS_crLowNJet_Cut_1b,  dPhiCut) 
  rCS_srNJet_0b_onlyTT = getRCS(cTTJets, rCS_sr_Cut_0b,  dPhiCut) #for check

  #rCS_srPredErrorCandidates = [abs(1 - rCS_crLowNJet_1b['rCS']/rCS_srNJet_0b_onlyTT['rCS']), rCS_srNJet_0b_onlyTT['rCSE_sim']/rCS_srNJet_0b_onlyTT['rCS']]
  #rCS_srPredError = max(rCS_srPredErrorCandidates)

  rd['yTT_srNJet_0b_lowDPhi'] = yTT_srNJet_0b_lowDPhi
  rd['yTT_Var_srNJet_0b_lowDPhi'] = yTT_Var_srNJet_0b_lowDPhi
  rd['rCS_crLowNJet_1b'] = rCS_crLowNJet_1b
  rd['rCS_crLowNJet_1b_onlyTT'] = rCS_crLowNJet_1b_onlyTT
  rd['rCS_srNJet_0b_onlyTT'] = rCS_srNJet_0b_onlyTT

  #true yields measured from MC samples
  truth_TT        = getYieldFromChain(cTTJets, rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_str)
  truth_TT_var    = getYieldFromChain(cTTJets, rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_err_str)

  #predicted yields with RCS method
  ttJetsCRForRCS = rCS_crLowNJet_1b #New version, orthogonal to DPhi (lower njet region in 1b-tag bin)
#  kFactor = getTTcorr(stb,htb)
#  pred_TT    = yTT_srNJet_0b_lowDPhi*ttJetsCRForRCS['rCS']*kFactor['k']
#  pred_Var_TT= yTT_Var_srNJet_0b_lowDPhi*ttJetsCRForRCS['rCS']**2*kFactor['k']**2 + yTT_srNJet_0b_lowDPhi**2*ttJetsCRForRCS['rCSE_pred']**2*kFactor['k']**2 + yTT_srNJet_0b_lowDPhi**2*ttJetsCRForRCS['rCS']**2*kFactor['k_Error']**2
  pred_TT    = yTT_srNJet_0b_lowDPhi*ttJetsCRForRCS['rCS']
  pred_Var_TT= yTT_Var_srNJet_0b_lowDPhi*ttJetsCRForRCS['rCS']**2 + yTT_srNJet_0b_lowDPhi**2*ttJetsCRForRCS['rCSE_pred']**2
  
  print "TT pred:",pred_TT,'+/-',sqrt(pred_Var_TT),' TT truth:',truth_TT,'+/-',truth_TT_var

  rd.update( {'TT_pred':pred_TT,"TT_pred_err":sqrt(pred_Var_TT),\
              "TT_truth":truth_TT,"TT_truth_err":sqrt(truth_TT_var), "TT_pred_statisticalError":sqrt(pred_Var_TT)})
  bins.update(rd)
  del rd
  return bins

