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

def makeTTPrediction(bins, samples, htb, stb, srNJet, presel, dPhiCut=1.0, btagVarString = "nBJetMediumCSV30", lumi=4., printDir='/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Spring15/defaultDir/templateFit/',useBTagWeights=False):
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
  fit_srNJet_lowDPhi = binnedNBTagsFit(fit_srCut+"&&"+dPhiStr+"<"+str(dPhiCut), fit_srName, samples = samples, nBTagVar = btagVarString, lumi=lumi, prefix=fit_srName, printDir=printDir,useBTagWeights=useBTagWeights)
#  fit_srNJet_lowDPhi = binnedNBTagsFit(fit_srCut+"&&"+dPhiStr+"<"+str(dPhiCut), samples = {'W':cWJets, 'TT':cTTJets}, nBTagVar = 'nBJetMedium25', prefix=fit_srName)
  rd['fit_srNJet_lowDPhi'] = fit_srNJet_lowDPhi

  yTT_srNJet_0b_lowDPhi =  fit_srNJet_lowDPhi['TT_AllPdg']['yield']*fit_srNJet_lowDPhi['TT_AllPdg']['template'].GetBinContent(1)
  yTT_Var_srNJet_0b_lowDPhi =  fit_srNJet_lowDPhi['TT_AllPdg']['yieldVar']*fit_srNJet_lowDPhi['TT_AllPdg']['template'].GetBinContent(1)**2

  #rCS_crLowNJet_Name_1b, rCS_crLowNJet_Cut_1b = nameAndCut(stb, htb, (4,5), presel=presel, btagVar = btagVarString) 
  rCS_sr_Name_0b, rCS_sr_Cut_0b = nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel, btagVar = btagVarString)#for Check 
  #rCS_crLowNJet_1b = getRCS(cBkg, rCS_crLowNJet_Cut_1b,  dPhiCut) #Low njet tt-jets CR to be orthoganl to DPhi 
  if useBTagWeights:
    rCS_crLowNJet_Name, rCS_crLowNJet_Cut = nameAndCut(stb, htb, (4,5), presel=presel, btagVar = btagVarString)
    rCS_crLowNJet_Name_1b, rCS_crLowNJet_Cut_1b = nameAndCut(stb, htb, (4,5), btb=(0,0), presel=presel, btagVar = btagVarString)
    #getRCS does not work when using btagweights, therefore a more complicated method needs to be used
    #rCS_crLowNJet_1b = getRCS(cData, rCS_crLowNJet_Cut_1b,  dPhiCut, weight = weight_str+'*weightBTag1') #Low njet tt-jets CR to be orthoganl to DPhi
    y_LowDPhi_1b = getYieldFromChain(cRest, cutString = rCS_crLowNJet_Cut_1b+'&&'+dPhiStr+'<'+str(dPhiCut),weight=weight_str)
    y_LowDPhi_1b+= getYieldFromChain(cWJets, cutString = rCS_crLowNJet_Cut+'&&'+dPhiStr+'<'+str(dPhiCut),weight=weight_str+'*weightBTag1')
    y_LowDPhi_1b+= getYieldFromChain(cTTJets, cutString = rCS_crLowNJet_Cut+'&&'+dPhiStr+'<'+str(dPhiCut),weight=weight_str+'*weightBTag1')
    
    y_Var_LowDPhi_1b = getYieldFromChain(cRest, cutString = rCS_crLowNJet_Cut_1b+'&&'+dPhiStr+'<'+str(dPhiCut),weight=weight_err_str)
    y_Var_LowDPhi_1b+= getYieldFromChain(cWJets, cutString = rCS_crLowNJet_Cut+'&&'+dPhiStr+'<'+str(dPhiCut),weight=weight_err_str+'*weightBTag1*weightBTag1')
    y_Var_LowDPhi_1b+= getYieldFromChain(cTTJets, cutString = rCS_crLowNJet_Cut+'&&'+dPhiStr+'<'+str(dPhiCut),weight=weight_err_str+'*weightBTag1*weightBTag1')    
    
    y_HighDPhi_1b = getYieldFromChain(cRest, cutString = rCS_crLowNJet_Cut_1b+'&&'+dPhiStr+'>='+str(dPhiCut),weight=weight_str)
    y_HighDPhi_1b+= getYieldFromChain(cWJets, cutString = rCS_crLowNJet_Cut+'&&'+dPhiStr+'>='+str(dPhiCut),weight=weight_str+'*weightBTag1')
    y_HighDPhi_1b+= getYieldFromChain(cTTJets, cutString = rCS_crLowNJet_Cut+'&&'+dPhiStr+'>='+str(dPhiCut),weight=weight_str+'*weightBTag1')
    
    y_Var_HighDPhi_1b = getYieldFromChain(cRest, cutString = rCS_crLowNJet_Cut_1b+'&&'+dPhiStr+'>='+str(dPhiCut),weight=weight_err_str)
    y_Var_HighDPhi_1b+= getYieldFromChain(cWJets, cutString = rCS_crLowNJet_Cut+'&&'+dPhiStr+'>='+str(dPhiCut),weight=weight_err_str+'*weightBTag1*weightBTag1')
    y_Var_HighDPhi_1b+= getYieldFromChain(cTTJets, cutString = rCS_crLowNJet_Cut+'&&'+dPhiStr+'>='+str(dPhiCut),weight=weight_err_str+'*weightBTag1*weightBTag1')
    
    rCS_crLowNJet_1b = {'rCS':y_HighDPhi_1b/y_LowDPhi_1b, 'rCSE_sim':(y_HighDPhi_1b/y_LowDPhi_1b)*sqrt(y_Var_HighDPhi_1b/y_HighDPhi_1b**2+y_Var_LowDPhi_1b/y_LowDPhi_1b**2), 'rCSE_pred':(y_HighDPhi_1b/y_LowDPhi_1b)*sqrt(1./y_HighDPhi_1b+1./y_LowDPhi_1b)}
    rCS_crLowNJet_1b_onlyTT = getRCS(cTTJets, rCS_crLowNJet_Cut,  dPhiCut, weight = weight_str+'*weightBTag1') 
  else:
    rCS_crLowNJet_Name_1b, rCS_crLowNJet_Cut_1b = nameAndCut(stb, htb, (4,5), btb=(0,0), presel=presel, btagVar = btagVarString)
    rCS_crLowNJet_1b = getRCS(cData, rCS_crLowNJet_Cut_1b,  dPhiCut, weight = weight_str) #Low njet tt-jets CR to be orthoganl to DPhi 
    rCS_crLowNJet_1b_onlyTT = getRCS(cTTJets, rCS_crLowNJet_Cut_1b,  dPhiCut, weight = weight_str)
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

