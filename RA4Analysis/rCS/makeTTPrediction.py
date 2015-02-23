import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName
from localInfo import username
from binnedNBTagsFit import binnedNBTagsFit
from rCShelpers import * 
from math import pi, sqrt

#lepSel = 'hard'
 
#cWJets  = getChain(WJetsHTToLNu[lepSel],histname='')
#cTTJets = getChain(ttJets[lepSel],histname='')
#cRest = getChain([DY[lepSel], singleTop[lepSel], TTVH[lepSel]],histname='')#no QCD 
#cBkg = getChain([WJetsHTToLNu[lepSel], ttJets[lepSel], DY[lepSel], singleTop[lepSel], TTVH[lepSel]],histname='')#no QCD

#ROOT_colors = [ROOT.kBlack, ROOT.kRed-7, ROOT.kBlue-2, ROOT.kGreen+3, ROOT.kOrange+1,ROOT.kRed-3, ROOT.kAzure+6, ROOT.kCyan+3, ROOT.kOrange , ROOT.kRed-10]
#dPhiStr = "acos((leptonPt+met*cos(leptonPhi-metPhi))/sqrt(leptonPt**2+met**2+2*met*leptonPt*cos(leptonPhi-metPhi)))"

#ROOT.TH1F().SetDefaultSumw2()

#prefix = 'singleLeptonic_20150220'
#presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0"

#streg = [[(250, 350), 1.], [(350, -1), 1.]] 
#htreg = [(500,750),(750,-1)]
#njreg = [(5,5),(6,-1)]

#small = True
#if small:
#  streg = [(250,350),1.]
#  htreg = (500,750)
#  njreg = (6,-1)


#res = {}
#for i_htb, htb in enumerate(htreg):
#  res[htb] = {}
#  for stb, dPhiCut in streg:
#    res[htb][stb] = {}
#    for srNJet in njreg:
#      rd = {}

def makeTTPrediction(dict, samples, htb, stb, srNJet, presel, dPhiCut=1.0):
  cWJets = samples['W']
  cTTJets = samples['TT']
  cRest = samples['Rest']
  cBkg = samples['Bkg']
  rd = {}

  #TT Jets yield in srNJet, no b-tag cut, low DPhi
  fit_srName, fit_srCut = nameAndCut(stb, htb, srNJet, btb=None, presel=presel, btagVar = 'nBJetMediumCMVA30') 
  fit_srNJet_lowDPhi = binnedNBTagsFit(fit_srCut+"&&"+dPhiStr+"<"+str(dPhiCut), samples = {'W':cWJets, 'TT':cTTJets, 'Rest':cRest}, nBTagVar = 'nBJetMediumCMVA30', prefix=fit_srName)
#  fit_srNJet_lowDPhi = binnedNBTagsFit(fit_srCut+"&&"+dPhiStr+"<"+str(dPhiCut), samples = {'W':cWJets, 'TT':cTTJets}, nBTagVar = 'nBJetMedium25', prefix=fit_srName)
  rd['fit_srNJet_lowDPhi'] = fit_srNJet_lowDPhi

  yTT_srNJet_0b_lowDPhi =  fit_srNJet_lowDPhi['TT_AllPdg']['yield']*fit_srNJet_lowDPhi['TT_AllPdg']['template'].GetBinContent(1)
  yTT_Var_srNJet_0b_lowDPhi =  fit_srNJet_lowDPhi['TT_AllPdg']['yieldVar']*fit_srNJet_lowDPhi['TT_AllPdg']['template'].GetBinContent(1)**2

  rCS_crLowNJet_Name_1b, rCS_crLowNJet_Cut_1b = nameAndCut(stb, htb, (4,5), btb=(1,1), presel=presel, btagVar = 'nBJetMediumCMVA30') 
  rCS_sr_Name_0b, rCS_sr_Cut_0b = nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel, btagVar = 'nBJetMediumCMVA30')#for Check 
  rCS_crLowNJet_1b = getRCS(cBkg, rCS_crLowNJet_Cut_1b,  dPhiCut) #Low njet tt-jets CR to be orthoganl to DPhi 
  rCS_crLowNJet_1b_onlyTT = getRCS(cTTJets, rCS_crLowNJet_Cut_1b,  dPhiCut) 
  rCS_srNJet_0b_onlyTT = getRCS(cTTJets, rCS_sr_Cut_0b,  dPhiCut) #for check
  rd['yTT_srNJet_0b_lowDPhi'] = yTT_srNJet_0b_lowDPhi
  rd['yTT_Var_srNJet_0b_lowDPhi'] = yTT_Var_srNJet_0b_lowDPhi
  rd['rCS_crLowNJet_1b'] = rCS_crLowNJet_1b
  rd['rCS_crLowNJet_1b_onlyTT'] = rCS_crLowNJet_1b_onlyTT
  rd['rCS_srNJet_0b_onlyTT'] = rCS_srNJet_0b_onlyTT

  #true yields measured from MC samples
  truth_TT        = getYieldFromChain(cTTJets, rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight")
  truth_TT_var    = getYieldFromChain(cTTJets, rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight*weight")

  #predicted yields with RCS method
  ttJetsCRForRCS = rCS_crLowNJet_1b #New version, orthogonal to DPhi (lower njet region in 1b-tag bin)
#  kFactor = getTTcorr(stb,htb)
#  pred_TT    = yTT_srNJet_0b_lowDPhi*ttJetsCRForRCS['rCS']*kFactor['k']
#  pred_Var_TT= yTT_Var_srNJet_0b_lowDPhi*ttJetsCRForRCS['rCS']**2*kFactor['k']**2 + yTT_srNJet_0b_lowDPhi**2*ttJetsCRForRCS['rCSE_pred']**2*kFactor['k']**2 + yTT_srNJet_0b_lowDPhi**2*ttJetsCRForRCS['rCS']**2*kFactor['k_Error']**2
  pred_TT    = yTT_srNJet_0b_lowDPhi*ttJetsCRForRCS['rCS']
  pred_Var_TT= yTT_Var_srNJet_0b_lowDPhi*ttJetsCRForRCS['rCS']**2 + yTT_srNJet_0b_lowDPhi**2*ttJetsCRForRCS['rCSE_pred']**2
  
  print "TT pred:",pred_TT,'+/-',sqrt(pred_Var_TT),' TT truth:',truth_TT,'+/-',truth_TT_var

  rd.update( {'TT_pred':pred_TT,"TT_pred_err":sqrt(pred_Var_TT),\
              "TT_truth":truth_TT,"TT_truth_err":sqrt(truth_TT_var)})
  dict.update(rd)
  del rd
  return dict

