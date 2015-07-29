import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName
from Workspace.HEPHYPythonTools.user import username
from binnedNBTagsFit import binnedNBTagsFit
from rCShelpers import * 
from math import pi, sqrt
from rCShelpers import *
#from pred_helper import weight_str , weight_err_str
#lepSel = 'hard'
 
#nBTagCMVA = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCMVA>0.732)' 

#cWJets  = getChain(WJetsHTToLNu[lepSel],histname='')
#cTTJets = getChain(ttJets[lepSel],histname='')
#cRest = getChain([DY[lepSel], singleTop[lepSel], TTVH[lepSel]],histname='')#no QCD 
#cBkg = getChain([WJetsHTToLNu[lepSel], ttJets[lepSel], DY[lepSel], singleTop[lepSel], TTVH[lepSel]],histname='')#no QCD
#for c in [cWJets, cTTJets, cRest, cBkg]:
#  c.SetAlias('nBTagCMVA', nBTagCMVA)

#ROOT_colors = [ROOT.kBlack, ROOT.kRed-7, ROOT.kBlue-2, ROOT.kGreen+3, ROOT.kOrange+1,ROOT.kRed-3, ROOT.kAzure+6, ROOT.kCyan+3, ROOT.kOrange , ROOT.kRed-10]
#dPhiStr = "acos((leptonPt+met*cos(leptonPhi-metPhi))/sqrt(leptonPt**2+met**2+2*met*leptonPt*cos(leptonPhi-metPhi)))"

ROOT.TH1F().SetDefaultSumw2()

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

#crNJet = (2,3)
#res = {}
#for i_htb, htb in enumerate(htreg):
#  res[htb] = {}
#  for stb, dPhiCut in streg:
#    res[htb][stb] = {}
#    for srNJet in njreg:
      
def makeWPrediction(bins, samples, htb, stb, srNJet, presel, dPhiCut=1.0, btagVarString = 'nBJetMediumCSV30', lumi=4.0):
  print "in W predition lumi is :"  , lumi
  weight_str, weight_err_str = makeWeight(lumi)
  cWJets = samples['W']
  cTTJets = samples['TT']
  cRest = samples['Rest']
  cBkg = samples['Bkg'] 
  cData = samples['Data']
  rd={}

  #TT Jets yield in crNJet, no b-tag cut, low DPhi
  fit_crName, fit_crCut = nameAndCut(stb, htb, (2,3), btb=None, presel=presel+'&&abs(leptonPdg)==13', btagVar = btagVarString) 
  fit_crNJet_lowDPhi = binnedNBTagsFit(fit_crCut+"&&"+dPhiStr+"<"+str(dPhiCut), samples=samples, nBTagVar = btagVarString , lumi=lumi, prefix=fit_crName)
#  fit_crNJet_lowDPhi = binnedNBTagsFit(fit_crCut+"&&"+dPhiStr+"<"+str(dPhiCut), samples = {'W':cWJets, 'TT':cTTJets}, nBTagVar = 'nBJetMedium25', prefix=fit_crName)
  rd['fit_crNJet_lowDPhi'] = fit_crNJet_lowDPhi
  
  rCS_cr_Name_1b, rCS_cr_Cut_1b = nameAndCut(stb, htb, (2,3), btb=(1,1), presel=presel, btagVar = btagVarString) 
  rCS_cr_Name_0b, rCS_cr_Cut_0b = nameAndCut(stb, htb, (2,3), btb=(0,0), presel=presel+'&&abs(leptonPdg)==13', btagVar = btagVarString) #THIS ONE GOT CHANGED FROM 2-3 TO 2-4!
  #rCS_cr_Name_0b, rCS_cr_Cut_0b = nameAndCut(stb, htb, (2,3), btb=(0,0), presel=presel, btagVar = btagVarString)
  #rCS_crNJet_1b = getRCS(cBkg, rCS_cr_Cut_1b,  dPhiCut) 
  rCS_crNJet_1b = getRCS(cData, rCS_cr_Cut_1b,  dPhiCut) 
  rCS_crNJet_1b_onlyTT = getRCS(cTTJets, rCS_cr_Cut_1b,  dPhiCut) 
  rCS_crNJet_0b_onlyTT = getRCS(cTTJets, rCS_cr_Cut_0b,  dPhiCut) 
  rd['rCS_crNJet_1b'] = rCS_crNJet_1b
  rd['rCS_crNJet_1b_onlyTT'] = rCS_crNJet_1b_onlyTT
  rd['rCS_crNJet_0b_onlyTT'] = rCS_crNJet_0b_onlyTT

  #low njet CR: crNJet, 0-btags, low DPhi
  crName, crCut = nameAndCut(stb, htb, (2,3),btb=(0,0), presel=presel, btagVar=btagVarString) 

  yTT_crNJet_0b_lowDPhi         = fit_crNJet_lowDPhi['TT_AllPdg']['yield']*fit_crNJet_lowDPhi['TT_AllPdg']['template'].GetBinContent(1)
  yTT_Var_crNJet_0b_lowDPhi     = fit_crNJet_lowDPhi['TT_AllPdg']['yieldVar']*fit_crNJet_lowDPhi['TT_AllPdg']['template'].GetBinContent(1)**2
  yTT_crNJet_0b_highDPhi        = rCS_crNJet_0b_onlyTT['rCS']*yTT_crNJet_0b_lowDPhi
  #yTT_crNJet_0b_highDPhi        = rCS_crNJet_1b['rCS']*yTT_crNJet_0b_lowDPhi
  yTT_Var_crNJet_0b_highDPhi    = rCS_crNJet_0b_onlyTT['rCSE_pred']**2*yTT_crNJet_0b_lowDPhi**2 + rCS_crNJet_0b_onlyTT['rCS']**2*yTT_Var_crNJet_0b_lowDPhi
  #yTT_Var_crNJet_0b_highDPhi    = rCS_crNJet_1b['rCSE_pred']**2*yTT_crNJet_0b_lowDPhi**2 + rCS_crNJet_1b['rCS']**2*yTT_Var_crNJet_0b_lowDPhi
  yTT_crNJet_0b_lowDPhi_truth   = getYieldFromChain(cTTJets, crCut+"&&"+dPhiStr+"<"+str(dPhiCut), weight = weight_str)
  yTT_crNJet_0b_highDPhi_truth  = getYieldFromChain(cTTJets, crCut+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_str)
  rd['yTT_crNJet_0b_lowDPhi']          =  yTT_crNJet_0b_lowDPhi         
  rd['yTT_Var_crNJet_0b_lowDPhi']      =  yTT_Var_crNJet_0b_lowDPhi     
  rd['yTT_crNJet_0b_highDPhi']         =  yTT_crNJet_0b_highDPhi        
  rd['yTT_Var_crNJet_0b_highDPhi']     =  yTT_Var_crNJet_0b_highDPhi    
  rd['yTT_crNJet_0b_lowDPhi_truth']    =  yTT_crNJet_0b_lowDPhi_truth   
  rd['yTT_crNJet_0b_highDPhi_truth']   =  yTT_crNJet_0b_highDPhi_truth  

#  print "Check: Impact of TT on RCS(W)"
#  print "Subtract numerator  ", yTT_crNJet_0b_highDPhi,'(rcs=',rCS_crNJet_1b['rCS'],'yield_0b',yTT_crNJet_0b_lowDPhi,') true',yTT_crNJet_0b_highDPhi_truth
#  print "Subtract denominator", yTT_crNJet_0b_lowDPhi,'true', yTT_crNJet_0b_lowDPhi_truth
  
  #calculate corrected rCS for W
  y_crNJet_0b_highDPhi     = getYieldFromChain(cBkg, crCut+"&&abs(leptonPdg)==13&&"+dPhiStr+">"+str(dPhiCut), weight = weight_str)
  y_Var_crNJet_0b_highDPhi = getYieldFromChain(cBkg, crCut+"&&abs(leptonPdg)==13&&"+dPhiStr+">"+str(dPhiCut), weight = weight_err_str)
  y_crNJet_0b_lowDPhi      = getYieldFromChain(cBkg, crCut+"&&abs(leptonPdg)==13&&"+dPhiStr+"<"+str(dPhiCut), weight = weight_str)
  y_Var_crNJet_0b_lowDPhi  = getYieldFromChain(cBkg, crCut+"&&abs(leptonPdg)==13&&"+dPhiStr+"<"+str(dPhiCut), weight = weight_err_str)
  rCS_W_crNJet_0b_corr     = (y_crNJet_0b_highDPhi - yTT_crNJet_0b_highDPhi)/(y_crNJet_0b_lowDPhi - yTT_crNJet_0b_lowDPhi)
  rCS_Var_W_crNJet_0b_corr = rCS_W_crNJet_0b_corr**2*(\
      (y_Var_crNJet_0b_highDPhi + yTT_Var_crNJet_0b_highDPhi)/(y_crNJet_0b_highDPhi - yTT_crNJet_0b_highDPhi)**2 
     +(y_Var_crNJet_0b_lowDPhi + yTT_Var_crNJet_0b_lowDPhi)/(y_crNJet_0b_lowDPhi - yTT_crNJet_0b_lowDPhi)**2
      )
  rCS_W_crNJet_0b_notcorr     = (y_crNJet_0b_highDPhi )/(y_crNJet_0b_lowDPhi )
  rCS_Var_W_crNJet_0b_notcorr = rCS_W_crNJet_0b_notcorr**2*( (y_Var_crNJet_0b_highDPhi )/(y_crNJet_0b_highDPhi)**2 + (y_Var_crNJet_0b_lowDPhi)/(y_crNJet_0b_lowDPhi)**2 )

  #calculate corrected rCS(+-) for W(+-) [because of yTT is symmetric in charge one have to subtract 0.5*yTT]
  #PosPdg
  y_crNJet_0b_highDPhi_PosPdg     = getYieldFromChain(cBkg, 'leptonPdg>0&&abs(leptonPdg)==13&&'+crCut+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_str)
  y_Var_crNJet_0b_highDPhi_PosPdg = getYieldFromChain(cBkg, 'leptonPdg>0&&abs(leptonPdg)==13&&'+crCut+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_err_str)
  y_crNJet_0b_lowDPhi_PosPdg      = getYieldFromChain(cBkg, 'leptonPdg>0&&abs(leptonPdg)==13&&'+crCut+"&&"+dPhiStr+"<"+str(dPhiCut), weight = weight_str)
  y_Var_crNJet_0b_lowDPhi_PosPdg  = getYieldFromChain(cBkg, 'leptonPdg>0&&abs(leptonPdg)==13&&'+crCut+"&&"+dPhiStr+"<"+str(dPhiCut), weight = weight_err_str)
  rCS_W_PosPdg_crNJet_0b_corr     = (y_crNJet_0b_highDPhi_PosPdg - (0.5*yTT_crNJet_0b_highDPhi))/(y_crNJet_0b_lowDPhi_PosPdg - (0.5*yTT_crNJet_0b_lowDPhi))
  rCS_Var_W_PosPdg_crNJet_0b_corr = rCS_W_PosPdg_crNJet_0b_corr**2*(\
      (y_Var_crNJet_0b_highDPhi_PosPdg + (0.5*yTT_Var_crNJet_0b_highDPhi))/(y_crNJet_0b_highDPhi_PosPdg - (0.5*yTT_crNJet_0b_highDPhi))**2 
     +(y_Var_crNJet_0b_lowDPhi_PosPdg + (0.5*yTT_Var_crNJet_0b_lowDPhi))/(y_crNJet_0b_lowDPhi_PosPdg - (0.5*yTT_crNJet_0b_lowDPhi))**2
      )
  rCS_W_PosPdg_crNJet_0b_notcorr     = (y_crNJet_0b_highDPhi_PosPdg )/(y_crNJet_0b_lowDPhi_PosPdg )
  rCS_Var_W_PosPdg_crNJet_0b_notcorr = rCS_W_PosPdg_crNJet_0b_notcorr**2*( (y_Var_crNJet_0b_highDPhi_PosPdg )/(y_crNJet_0b_highDPhi_PosPdg)**2 + (y_Var_crNJet_0b_lowDPhi_PosPdg)/(y_crNJet_0b_lowDPhi_PosPdg)**2 )
  #NegPdg
  y_crNJet_0b_highDPhi_NegPdg     = getYieldFromChain(cBkg, 'leptonPdg<0&&abs(leptonPdg)==13&&'+crCut+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_str)
  y_Var_crNJet_0b_highDPhi_NegPdg = getYieldFromChain(cBkg, 'leptonPdg<0&&abs(leptonPdg)==13&&'+crCut+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_err_str)
  y_crNJet_0b_lowDPhi_NegPdg      = getYieldFromChain(cBkg, 'leptonPdg<0&&abs(leptonPdg)==13&&'+crCut+"&&"+dPhiStr+"<"+str(dPhiCut), weight = weight_str)
  y_Var_crNJet_0b_lowDPhi_NegPdg  = getYieldFromChain(cBkg, 'leptonPdg<0&&abs(leptonPdg)==13&&'+crCut+"&&"+dPhiStr+"<"+str(dPhiCut), weight = weight_err_str)
  rCS_W_NegPdg_crNJet_0b_corr     = (y_crNJet_0b_highDPhi_NegPdg - (0.5*yTT_crNJet_0b_highDPhi))/(y_crNJet_0b_lowDPhi_NegPdg - (0.5*yTT_crNJet_0b_lowDPhi))
  rCS_Var_W_NegPdg_crNJet_0b_corr = rCS_W_NegPdg_crNJet_0b_corr**2*(\
      (y_Var_crNJet_0b_highDPhi_NegPdg + (0.5*yTT_Var_crNJet_0b_highDPhi))/(y_crNJet_0b_highDPhi_NegPdg - (0.5*yTT_crNJet_0b_highDPhi))**2
     +(y_Var_crNJet_0b_lowDPhi_NegPdg + (0.5*yTT_Var_crNJet_0b_lowDPhi))/(y_crNJet_0b_lowDPhi_NegPdg - (0.5*yTT_crNJet_0b_lowDPhi))**2
      )
  rCS_W_NegPdg_crNJet_0b_notcorr     = (y_crNJet_0b_highDPhi_NegPdg )/(y_crNJet_0b_lowDPhi_NegPdg )
  rCS_Var_W_NegPdg_crNJet_0b_notcorr = rCS_W_NegPdg_crNJet_0b_notcorr**2*( (y_Var_crNJet_0b_highDPhi_NegPdg )/(y_crNJet_0b_highDPhi_NegPdg)**2 + (y_Var_crNJet_0b_lowDPhi_NegPdg)/(y_crNJet_0b_lowDPhi_NegPdg)**2 )

  rd['y_crNJet_0b_highDPhi']       = y_crNJet_0b_highDPhi
  rd['y_Var_crNJet_0b_highDPhi']   = y_Var_crNJet_0b_highDPhi
  rd['y_crNJet_0b_lowDPhi']        = y_crNJet_0b_lowDPhi
  rd['y_Var_crNJet_0b_lowDPhi']    = y_Var_crNJet_0b_lowDPhi
  rd['rCS_W_crNJet_0b_corr']       = rCS_W_crNJet_0b_corr
  rd['rCS_Var_W_crNJet_0b_corr']   = rCS_Var_W_crNJet_0b_corr
  rd['rCS_W_crNJet_0b_notcorr']       = rCS_W_crNJet_0b_notcorr
  rd['rCS_Var_W_crNJet_0b_notcorr']   = rCS_Var_W_crNJet_0b_notcorr
  rd['rCS_W_crNJet_0b_truth']       = getRCS(cWJets, crCut,  dPhiCut)
  #PosPdg
  rd['y_crNJet_0b_highDPhi_PosPdg']       = y_crNJet_0b_highDPhi_PosPdg
  rd['y_Var_crNJet_0b_highDPhi_PosPdg']   = y_Var_crNJet_0b_highDPhi_PosPdg
  rd['y_crNJet_0b_lowDPhi_PosPdg']        = y_crNJet_0b_lowDPhi_PosPdg
  rd['y_Var_crNJet_0b_lowDPhi_PosPdg']    = y_Var_crNJet_0b_lowDPhi_PosPdg
  rd['rCS_W_PosPdg_crNJet_0b_corr']       = rCS_W_PosPdg_crNJet_0b_corr
  rd['rCS_Var_W_PosPdg_crNJet_0b_corr']   = rCS_Var_W_PosPdg_crNJet_0b_corr
  rd['rCS_W_PosPdg_crNJet_0b_notcorr']       = rCS_W_PosPdg_crNJet_0b_notcorr
  rd['rCS_Var_W_PosPdg_crNJet_0b_notcorr']   = rCS_Var_W_PosPdg_crNJet_0b_notcorr
  rd['rCS_W_PosPdg_crNJet_0b_truth']  = getRCS(cWJets, 'leptonPdg>0&&'+crCut, dPhiCut)
  #NegPdg
  rd['y_crNJet_0b_highDPhi_NegPdg']       = y_crNJet_0b_highDPhi_NegPdg
  rd['y_Var_crNJet_0b_highDPhi_NegPdg']   = y_Var_crNJet_0b_highDPhi_NegPdg
  rd['y_crNJet_0b_lowDPhi_NegPdg']        = y_crNJet_0b_lowDPhi_NegPdg
  rd['y_Var_crNJet_0b_lowDPhi_NegPdg']    = y_Var_crNJet_0b_lowDPhi_NegPdg
  rd['rCS_W_NegPdg_crNJet_0b_corr']       = rCS_W_NegPdg_crNJet_0b_corr
  rd['rCS_Var_W_NegPdg_crNJet_0b_corr']   = rCS_Var_W_NegPdg_crNJet_0b_corr
  rd['rCS_W_NegPdg_crNJet_0b_notcorr']       = rCS_W_NegPdg_crNJet_0b_notcorr
  rd['rCS_Var_W_NegPdg_crNJet_0b_notcorr']   = rCS_Var_W_NegPdg_crNJet_0b_notcorr
  rd['rCS_W_NegPdg_crNJet_0b_truth']  = getRCS(cWJets, 'leptonPdg<0&&'+crCut, dPhiCut)

  fit_srName, fit_srCut = nameAndCut(stb, htb, srNJet, btb=None, presel=presel,btagVar = btagVarString) 
  fit_srNJet_lowDPhi = binnedNBTagsFit(fit_srCut+"&&"+dPhiStr+"<"+str(dPhiCut), samples = samples, nBTagVar = btagVarString, lumi=lumi, prefix=fit_srName)
#  fit_srNJet_lowDPhi = binnedNBTagsFit(fit_srCut+"&&"+dPhiStr+"<"+str(dPhiCut), samples = {'W':cWJets, 'TT':cTTJets}, nBTagVar = 'nBJetMedium25', prefix=fit_srName)

  rd['fit_srNJet_lowDPhi'] = fit_srNJet_lowDPhi
#  print "Check: Impact of TT on RCS(W)"
#  print "Subtract numerator  ", yTT_crNJet_0b_highDPhi,'(rcs=',rCS_crNJet_1b['rCS'],'yield_0b',yTT_crNJet_0b_lowDPhi,') true',yTT_crNJet_0b_highDPhi_truth
#  print "Subtract denominator", yTT_crNJet_0b_lowDPhi,'true', yTT_crNJet_0b_lowDPhi_truth

  yW_srNJet_0b_lowDPhi  =  fit_srNJet_lowDPhi['W_PosPdg']['yield']*fit_srNJet_lowDPhi['W_PosPdg']['template'].GetBinContent(1)\
                        +  fit_srNJet_lowDPhi['W_NegPdg']['yield']*fit_srNJet_lowDPhi['W_NegPdg']['template'].GetBinContent(1)
  yW_Var_srNJet_0b_lowDPhi  =  fit_srNJet_lowDPhi['W_PosPdg']['yieldVar']*fit_srNJet_lowDPhi['W_PosPdg']['template'].GetBinContent(1)**2\
                            +  fit_srNJet_lowDPhi['W_NegPdg']['yieldVar']*fit_srNJet_lowDPhi['W_NegPdg']['template'].GetBinContent(1)**2#FIXME I add that uncorrelated
  yW_PosPdg_srNJet_0b_lowDPhi = fit_srNJet_lowDPhi['W_PosPdg']['yield']*fit_srNJet_lowDPhi['W_PosPdg']['template'].GetBinContent(1)
  yW_PosPdg_Var_srNJet_0b_lowDPhi = fit_srNJet_lowDPhi['W_PosPdg']['yieldVar']*fit_srNJet_lowDPhi['W_PosPdg']['template'].GetBinContent(1)**2
  yW_NegPdg_srNJet_0b_lowDPhi = fit_srNJet_lowDPhi['W_NegPdg']['yield']*fit_srNJet_lowDPhi['W_NegPdg']['template'].GetBinContent(1)
  yW_NegPdg_Var_srNJet_0b_lowDPhi = fit_srNJet_lowDPhi['W_NegPdg']['yieldVar']*fit_srNJet_lowDPhi['W_NegPdg']['template'].GetBinContent(1)**2

  # for systematics
  rCS_crLowNJet_0b_onlyW = getRCS(cWJets, crCut, dPhiCut)
  rCS_crLowNJet_0b_onlyW_PosPdg = getRCS(cWJets, 'leptonPdg>0&&'+crCut, dPhiCut)
  rCS_crLowNJet_0b_onlyW_NegPdg = getRCS(cWJets, 'leptonPdg<0&&'+crCut, dPhiCut)
  rCS_crLowNJet_0b_onlyW_mu = getRCS(cWJets, crCut+'&&abs(leptonPdg)==13', dPhiCut)
  rCS_crLowNJet_0b_onlyW_mu_PosPdg = getRCS(cWJets, crCut+'&&leptonPdg>0&&abs(leptonPdg)==13', dPhiCut)
  rCS_crLowNJet_0b_onlyW_mu_NegPdg = getRCS(cWJets, crCut+'&&leptonPdg<0&&abs(leptonPdg)==13', dPhiCut)  
  rd['rCS_crLowNJet_0b_onlyW'] = rCS_crLowNJet_0b_onlyW
  rd['rCS_crLowNJet_0b_onlyW_PosPdg'] = rCS_crLowNJet_0b_onlyW_PosPdg
  rd['rCS_crLowNJet_0b_onlyW_NegPdg'] = rCS_crLowNJet_0b_onlyW_NegPdg
  rd['rCS_crLowNJet_0b_onlyW_mu'] = rCS_crLowNJet_0b_onlyW_mu
  rd['rCS_crLowNJet_0b_onlyW_mu_PosPdg'] = rCS_crLowNJet_0b_onlyW_mu_PosPdg
  rd['rCS_crLowNJet_0b_onlyW_mu_NegPdg'] = rCS_crLowNJet_0b_onlyW_mu_NegPdg
  
  rCS_sr_Name_0b, rCS_sr_Cut_0b = nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel, btagVar = btagVarString)#for Check 
  rCS_srNJet_0b_onlyW = getRCS(cWJets, rCS_sr_Cut_0b,  dPhiCut) #for check
  rCS_srNJet_0b_onlyW_mu = getRCS(cWJets, rCS_sr_Cut_0b+'&&abs(leptonPdg)==13',  dPhiCut) #for check
  rCS_srNJet_0b_onlyW_ele = getRCS(cWJets, rCS_sr_Cut_0b+'&&abs(leptonPdg)==11',  dPhiCut) #for check
  rCS_srNJet_0b_onlyW_PosPdg = getRCS(cWJets, 'leptonPdg>0&&'+rCS_sr_Cut_0b,  dPhiCut) #for check
  rCS_srNJet_0b_onlyW_NegPdg = getRCS(cWJets, 'leptonPdg<0&&'+rCS_sr_Cut_0b,  dPhiCut) #for check
  rCS_srNJet_0b_onlyW_mu_PosPdg = getRCS(cWJets, 'leptonPdg>0&&abs(leptonPdg)==13&&'+rCS_sr_Cut_0b,  dPhiCut) #for check
  rCS_srNJet_0b_onlyW_mu_NegPdg = getRCS(cWJets, 'leptonPdg<0&&abs(leptonPdg)==13&&'+rCS_sr_Cut_0b,  dPhiCut) #for check
  rCS_srNJet_0b_onlyW_ele_PosPdg = getRCS(cWJets, 'leptonPdg>0&&abs(leptonPdg)==11&&'+rCS_sr_Cut_0b,  dPhiCut) #for check
  rCS_srNJet_0b_onlyW_ele_NegPdg = getRCS(cWJets, 'leptonPdg<0&&abs(leptonPdg)==11&&'+rCS_sr_Cut_0b,  dPhiCut) #for check
  rd['yW_srNJet_0b_lowDPhi'] = yW_srNJet_0b_lowDPhi  
  rd['yW_Var_srNJet_0b_lowDPhi'] = yW_Var_srNJet_0b_lowDPhi 
  rd['yW_PosPdg_srNJet_0b_lowDPhi'] = yW_PosPdg_srNJet_0b_lowDPhi
  rd['yW_PosPdg_Var_srNJet_0b_lowDPhi'] = yW_PosPdg_Var_srNJet_0b_lowDPhi
  rd['yW_NegPdg_srNJet_0b_lowDPhi'] = yW_NegPdg_srNJet_0b_lowDPhi
  rd['yW_NegPdg_Var_srNJet_0b_lowDPhi'] = yW_NegPdg_Var_srNJet_0b_lowDPhi
  rd['rCS_srNJet_0b_onlyW'] = rCS_srNJet_0b_onlyW
  rd['rCS_srNJet_0b_onlyW_mu'] = rCS_srNJet_0b_onlyW_mu
  rd['rCS_srNJet_0b_onlyW_ele'] = rCS_srNJet_0b_onlyW_ele
  rd['rCS_srNJet_0b_onlyW_PosPdg'] = rCS_srNJet_0b_onlyW_PosPdg #Rcs in SR for ele+mu, pos PDG
  rd['rCS_srNJet_0b_onlyW_NegPdg'] = rCS_srNJet_0b_onlyW_NegPdg #Rcs in SR for ele+mu, neg PDG
  rd['rCS_srNJet_0b_onlyW_mu_PosPdg'] = rCS_srNJet_0b_onlyW_mu_PosPdg #Rcs in SR for mu, pos PDG
  rd['rCS_srNJet_0b_onlyW_mu_NegPdg'] = rCS_srNJet_0b_onlyW_mu_NegPdg #Rcs in SR for mu, neg PDG
  rd['rCS_srNJet_0b_onlyW_ele_PosPdg'] = rCS_srNJet_0b_onlyW_ele_PosPdg #Rcs in SR for ele, pos PDG
  rd['rCS_srNJet_0b_onlyW_ele_NegPdg'] = rCS_srNJet_0b_onlyW_ele_NegPdg #Rcs in SR for ele, neg PDG

  #rd['rCS_srNJet_0b_onlyW_NegPdg_Ratio'] = rCS_srNJet_0b_onlyW_mu_NegPdg['rCS']/rCS_srNJet_0b_onlyW_NegPdg['rCS']
  #rd['rCS_Var_srNJet_0b_onlyW_NegPdg_Ratio'] = rCS_srNJet_0b_onlyW_mu_NegPdg['rCS']**2/rCS_srNJet_0b_onlyW_NegPdg['rCS']**2*((rCS_srNJet_0b_onlyW_mu_NegPdg['rCSE_sim']/rCS_srNJet_0b_onlyW_mu_NegPdg['rCS'])**2+\
  #                                              (rCS_srNJet_0b_onlyW_NegPdg['rCSE_sim']/rCS_srNJet_0b_onlyW_NegPdg['rCS'])**2)

  #rd['rCS_srNJet_0b_onlyW_PosPdg_Ratio'] = rCS_srNJet_0b_onlyW_mu_PosPdg['rCS']/rCS_srNJet_0b_onlyW_PosPdg['rCS']
  #rd['rCS_Var_srNJet_0b_onlyW_PosPdg_Ratio'] = rCS_srNJet_0b_onlyW_mu_PosPdg['rCS']**2/rCS_srNJet_0b_onlyW_PosPdg['rCS']**2*((rCS_srNJet_0b_onlyW_mu_PosPdg['rCSE_sim']/rCS_srNJet_0b_onlyW_mu_PosPdg['rCS'])**2+\
  #                                              (rCS_srNJet_0b_onlyW_PosPdg['rCSE_sim']/rCS_srNJet_0b_onlyW_PosPdg['rCS'])**2)

  #rd['rCS_srNJet_0b_onlyW_Ratio'] = rCS_srNJet_0b_onlyW_mu['rCS']/rCS_srNJet_0b_onlyW['rCS']
  #rd['rCS_Var_srNJet_0b_onlyW_Ratio'] = rCS_srNJet_0b_onlyW_mu['rCS']**2/rCS_srNJet_0b_onlyW['rCS']**2*((rCS_srNJet_0b_onlyW_mu['rCSE_sim']/rCS_srNJet_0b_onlyW_mu['rCS'])**2+\
  #                                              (rCS_srNJet_0b_onlyW['rCSE_sim']/rCS_srNJet_0b_onlyW['rCS'])**2)

  #true yields measured from MC samples, residual background is also calculated here and added to the dict
  truth_W         = getYieldFromChain(cWJets,  rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_str)
  truth_W_var     = getYieldFromChain(cWJets,  rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_err_str)
  truth_Rest      = getYieldFromChain(cRest,   rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_str)
  truth_Rest_var  = getYieldFromChain(cRest,   rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_err_str)

  truth_W_PosPdg         = getYieldFromChain(cWJets, 'leptonPdg>0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_str)
  truth_W_var_PosPdg     = getYieldFromChain(cWJets, 'leptonPdg>0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_err_str)
  truth_W_NegPdg         = getYieldFromChain(cWJets, 'leptonPdg<0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_str)
  truth_W_var_NegPdg     = getYieldFromChain(cWJets, 'leptonPdg<0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_err_str)
  truth_Rest_PosPdg      = getYieldFromChain(cRest,  'leptonPdg>0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_str)
  truth_Rest_var_PosPdg  = getYieldFromChain(cRest,  'leptonPdg>0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_err_str)
  truth_Rest_NegPdg      = getYieldFromChain(cRest,  'leptonPdg<0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_str)
  truth_Rest_var_NegPdg  = getYieldFromChain(cRest,  'leptonPdg<0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_err_str)

  #predicted yields with RCS method
  pred_W     = yW_srNJet_0b_lowDPhi*rCS_W_crNJet_0b_corr
  pred_Var_W = yW_Var_srNJet_0b_lowDPhi*rCS_W_crNJet_0b_corr**2 + yW_srNJet_0b_lowDPhi**2*rCS_Var_W_crNJet_0b_corr

  pred_W_PosPdg     = yW_PosPdg_srNJet_0b_lowDPhi*rCS_W_PosPdg_crNJet_0b_corr
  pred_Var_W_PosPdg = yW_PosPdg_Var_srNJet_0b_lowDPhi*rCS_W_PosPdg_crNJet_0b_corr**2 + yW_PosPdg_srNJet_0b_lowDPhi**2*rCS_Var_W_PosPdg_crNJet_0b_corr
  pred_W_NegPdg     = yW_NegPdg_srNJet_0b_lowDPhi*rCS_W_NegPdg_crNJet_0b_corr
  pred_Var_W_NegPdg = yW_NegPdg_Var_srNJet_0b_lowDPhi*rCS_W_NegPdg_crNJet_0b_corr**2 + yW_NegPdg_srNJet_0b_lowDPhi**2*rCS_Var_W_NegPdg_crNJet_0b_corr

#  pred_total = pred_TT + pred_W + truth_Rest
#  pred_total_PosPdg = (0.5*pred_TT) + pred_W_PosPdg + truth_Rest_PosPdg
#  pred_total_NegPdg = (0.5*pred_TT) + pred_W_NegPdg + truth_Rest_NegPdg
#  pred_Var_total = pred_Var_TT + pred_Var_W + truth_Rest_var
#  pred_Var_total_PosPdg = (0.5*pred_Var_TT) + pred_Var_W_PosPdg + truth_Rest_var_PosPdg
#  pred_Var_total_NegPdg = (0.5*pred_Var_TT) + pred_Var_W_NegPdg + truth_Rest_var_NegPdg 

  print "W pred:",pred_W,'+/-',sqrt(pred_Var_W),'W truth:',truth_W,'+/-',sqrt(truth_W_var)
  print "W(-) pred:",pred_W_PosPdg,'+/-',sqrt(pred_Var_W_PosPdg),'W truth:',truth_W_PosPdg,'+/-',sqrt(truth_W_var_PosPdg)
  print "W(+) pred:",pred_W_NegPdg,'+/-',sqrt(pred_Var_W_NegPdg),'W truth:',truth_W_NegPdg,'+/-',sqrt(truth_W_var_NegPdg)

  rd.update( {"W_pred":pred_W,"W_pred_err":sqrt(pred_Var_W),\
              "W_truth":truth_W,"W_truth_err":sqrt(truth_W_var),\
              "W_PosPdg_pred":pred_W_PosPdg,"W_PosPdg_pred_err":sqrt(pred_Var_W_PosPdg),\
              "W_PosPdg_truth":truth_W_PosPdg,"W_PosPdg_truth_err":sqrt(truth_W_var_PosPdg),\
              "W_NegPdg_pred":pred_W_NegPdg,"W_NegPdg_pred_err":sqrt(pred_Var_W_NegPdg),\
              "W_NegPdg_truth":truth_W_NegPdg,"W_NegPdg_truth_err":sqrt(truth_W_var_NegPdg),\
              'Rest_truth':truth_Rest,'Rest_truth_err':sqrt(truth_Rest_var),\
              'Rest_PosPdg_truth':truth_Rest_PosPdg,'Rest_PosPdg_truth_err':sqrt(truth_Rest_var_PosPdg),\
              'Rest_NegPdg_truth':truth_Rest_NegPdg,'Rest_NegPdg_truth_err':sqrt(truth_Rest_var_NegPdg),\
#              'tot_pred':pred_total,'tot_pred_err':sqrt(pred_Var_total),\
#              'tot_PosPdg_pred':pred_total_PosPdg,'tot_PosPdg_pred_err':sqrt(pred_Var_total_PosPdg),\
#              'tot_NegPdg_pred':pred_total_NegPdg,'tot_NegPdg_pred_err':sqrt(pred_Var_total_NegPdg),\
#              'tot_truth':truth_TT+truth_W+truth_Rest,'tot_truth_err':sqrt(truth_TT_var + truth_W_var + truth_Rest_var),\
#              'tot_PosPdg_truth':(0.5*truth_TT)+truth_W_PosPdg+truth_Rest_PosPdg,'tot_PosPdg_truth_err':sqrt((0.5*truth_TT_var) + truth_W_var_PosPdg + truth_Rest_var_PosPdg),\
#              'tot_NegPdg_truth':(0.5*truth_TT)+truth_W_NegPdg+truth_Rest_NegPdg,'tot_NegPdg_truth_err':sqrt((0.5*truth_TT_var) + truth_W_var_NegPdg + truth_Rest_var_NegPdg)})
              })
  bins.update(rd)
  del rd
  return bins

