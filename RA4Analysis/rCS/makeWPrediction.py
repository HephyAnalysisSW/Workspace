import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName
from Workspace.HEPHYPythonTools.user import username
from binnedNBTagsFit import binnedNBTagsFit
from rCShelpers import * 
from math import pi, sqrt
from rCShelpers import *
 
from predictionConfig import *

ROOT.TH1F().SetDefaultSumw2()

def makeWPrediction(bins, samples, htb, stb, srNJet, presel, dPhiCut=1.0, QCD=False):
  print "in W predition lumi is :"  , lumi
  if useBTagWeights: 'Will use b-tag weights for W-jets prediction!'
  weight_str, weight_err_str = makeWeight(lumi)
  cWJets = samples['W']
  cTTJets = samples['TT']
  cRest = samples['Rest']
  cBkg = samples['Bkg'] 
  cData = samples['Data']
  rd={}
  
  nJetCR = wjetsSB
  
  if isData:
    w = 'weight'
    w_err = 'weight**2'
  else:
    w = weight_str
    w_err = weight_err_str
  
  #TT Jets yield in crNJet, no b-tag cut, low DPhi
  fit_crName, fit_crCut = nameAndCut(stb, htb, nJetCR, btb=None, presel=presel+'&&abs(leptonPdg)==13', btagVar = nBTagVar) 
  fit_crNJet_lowDPhi = binnedNBTagsFit(fit_crCut+"&&"+dPhiStr+"<"+str(dPhiCut), fit_crName+'_dPhi'+str(dPhiCut)+'_muonChannel', samples=samples, prefix=fit_crName) #no QCD subtraction - there should only be a very small QCD contamination in muon channel
#  fit_crNJet_lowDPhi = binnedNBTagsFit(fit_crCut+"&&"+dPhiStr+"<"+str(dPhiCut), samples = {'W':cWJets, 'TT':cTTJets}, nBTagVar = 'nBJetMedium25', prefix=fit_crName)
  rd['fit_crNJet_lowDPhi'] = fit_crNJet_lowDPhi
  
  crNameTruth, crCutTruth = nameAndCut(stb, htb, nJetCR,btb=(0,0), presel=presel, btagVar=nBTagVar)
  if useBTagWeights:
    crName, crCut = nameAndCut(stb, htb, nJetCR, presel=presel, btagVar=nBTagVar)
    weight_str_0b = weight_str+'*weightBTag0'+btagWeightSuffix #this is used for everything that could also be data
    weight_str_0bMC = weight_str+'*weightBTag0_SF' #this is used for values that always come from MC and should not be varied when the SFs are
  else:
    crName, crCut = nameAndCut(stb, htb, nJetCR,btb=(0,0), presel=presel, btagVar=nBTagVar)
    weight_str_0b = weight_str
    weight_str_0bMC = weight_str
  
  rCS_crNJet_0b_onlyTT = getRCS(cTTJets, crCut+'&&abs(leptonPdg)==13',  dPhiCut, weight_str_0bMC)
  rd['rCS_crNJet_0b_onlyTT'] = rCS_crNJet_0b_onlyTT #no reweighting here, still from MC!

  #low njet CR: crNJet, 0-btags, low DPhi

  yTT_crNJet_0b_lowDPhi         = fit_crNJet_lowDPhi['TT_AllPdg']['yield']*fit_crNJet_lowDPhi['TT_AllPdg']['template'].GetBinContent(1)
  yTT_Var_crNJet_0b_lowDPhi     = fit_crNJet_lowDPhi['TT_AllPdg']['yieldVar']*fit_crNJet_lowDPhi['TT_AllPdg']['template'].GetBinContent(1)**2
  if templateBootstrap: yTT_Var_crNJet_0b_lowDPhi += fit_crNJet_lowDPhi['TT_AllPdg']['yield']**2*templateBootstrap['TTJets_mu'][srNJet][stb][htb]**2
  yTT_crNJet_0b_highDPhi        = rCS_crNJet_0b_onlyTT['rCS']*yTT_crNJet_0b_lowDPhi
  yTT_Var_crNJet_0b_highDPhi    = rCS_crNJet_0b_onlyTT['rCSE_pred']**2*yTT_crNJet_0b_lowDPhi**2 + rCS_crNJet_0b_onlyTT['rCS']**2*yTT_Var_crNJet_0b_lowDPhi
  yTT_Var_crNJet_0b_highDPhi_MC = rCS_crNJet_0b_onlyTT['rCSE_sim']**2*yTT_crNJet_0b_lowDPhi**2 + rCS_crNJet_0b_onlyTT['rCS']**2*yTT_Var_crNJet_0b_lowDPhi
  #yTT_Var_crNJet_0b_highDPhi    = rCS_crNJet_1b['rCSE_pred']**2*yTT_crNJet_0b_lowDPhi**2 + rCS_crNJet_1b['rCS']**2*yTT_Var_crNJet_0b_lowDPhi

  # Get all the MC truth yields and save them in the pickle file, use all available SFs.

  chargeList = [{'charge':'', 'muonCut':"&&abs(leptonPdg)==13&&"},{'charge':'_PosPdg', 'muonCut':'&&leptonPdg>0&&abs(leptonPdg)==13&&'}, {'charge':'_NegPdg', 'muonCut':'&&leptonPdg<0&&abs(leptonPdg)==13&&'}]
  MCsamples = [{'name':'TT', 'chain':cTTJets}, {'name':'W', 'chain':cWJets}, {'name':'Rest','chain':cRest}]
  
  for charge in chargeList:
    for s in MCsamples:
      
      truthYield_lowDPhi  = getYieldFromChain(s['chain'], crCut+charge['muonCut']+dPhiStr+"<"+str(dPhiCut), weight = weight_str+'*weightBTag0'+btagWeightSuffix, returnError = True)
      truthYield_highDPhi = getYieldFromChain(s['chain'], crCut+charge['muonCut']+dPhiStr+">"+str(dPhiCut), weight = weight_str+'*weightBTag0'+btagWeightSuffix, returnError = True)
      
      rd['y'+s['name']+'_crNJet_0b_lowDPhi_truth'+charge['charge']]      = truthYield_lowDPhi[0]
      rd['y'+s['name']+'_Var_crNJet_0b_lowDPhi_truth'+charge['charge']]  = truthYield_lowDPhi[1]**2
      rd['y'+s['name']+'_crNJet_0b_highDPhi_truth'+charge['charge']]     = truthYield_highDPhi[0]
      rd['y'+s['name']+'_Var_crNJet_0b_highDPhi_truth'+charge['charge']] = truthYield_highDPhi[1]**2
      
  
  rd['yTT_crNJet_0b_lowDPhi']          =  yTT_crNJet_0b_lowDPhi         
  rd['yTT_Var_crNJet_0b_lowDPhi']      =  yTT_Var_crNJet_0b_lowDPhi     
  rd['yTT_crNJet_0b_highDPhi']         =  yTT_crNJet_0b_highDPhi        
  rd['yTT_Var_crNJet_0b_highDPhi']     =  yTT_Var_crNJet_0b_highDPhi    

#  print "Check: Impact of TT on RCS(W)"
#  print "Subtract numerator  ", yTT_crNJet_0b_highDPhi,'(rcs=',rCS_crNJet_1b['rCS'],'yield_0b',yTT_crNJet_0b_lowDPhi,') true',yTT_crNJet_0b_highDPhi_truth
#  print "Subtract denominator", yTT_crNJet_0b_lowDPhi,'true', yTT_crNJet_0b_lowDPhi_truth

  muonCut = "&&abs(leptonPdg)==13"
  correction_lowDPhi        = {'y':yTT_crNJet_0b_lowDPhi,'e':yTT_Var_crNJet_0b_lowDPhi}
  correction_highDPhi       = {'y':yTT_crNJet_0b_highDPhi,'e':yTT_Var_crNJet_0b_highDPhi}
  correction_lowDPhi_rest   = {'y':yTT_crNJet_0b_lowDPhi+rd['yRest_crNJet_0b_lowDPhi_truth'],'e':yTT_Var_crNJet_0b_lowDPhi+sqrt(rd['yRest_Var_crNJet_0b_lowDPhi_truth'])}
  correction_highDPhi_rest  = {'y':yTT_crNJet_0b_highDPhi+rd['yRest_crNJet_0b_highDPhi_truth'],'e':yTT_Var_crNJet_0b_highDPhi+sqrt(rd['yRest_Var_crNJet_0b_highDPhi_truth'])}

  if isData:
    #treat contamination like QCD
    rCS_W_crNJet_0b_corr      = getRCS(cData, crCutTruth+muonCut,dPhiCut, QCD_lowDPhi=correction_lowDPhi, QCD_highDPhi=correction_highDPhi, returnValues=True)
    rCS_W_crNJet_0b_corr_rest = getRCS(cData, crCutTruth+muonCut,dPhiCut, QCD_lowDPhi=correction_lowDPhi_rest, QCD_highDPhi=correction_highDPhi_rest, returnValues=True)
    rCS_W_crNJet_0b_notcorr   = getRCS(cData, crCutTruth+muonCut, dPhiCut, returnValues = True)
    
  else:
    rCS_W_crNJet_0b_corr      = getRCS(cBkg, crCut+muonCut, dPhiCut, weight=weight_str_0b, QCD_lowDPhi=correction_lowDPhi, QCD_highDPhi=correction_highDPhi, returnValues=True)
    rCS_W_crNJet_0b_corr_rest = getRCS(cBkg, crCut+muonCut, dPhiCut, weight=weight_str_0b, QCD_lowDPhi=correction_lowDPhi_rest, QCD_highDPhi=correction_highDPhi_rest, returnValues=True)
    rCS_W_crNJet_0b_notcorr   = getRCS(cBkg, crCut+muonCut, dPhiCut, weight=weight_str_0b, returnValues=True)


  #calculate corrected rCS(+-) for W(+-) [because of yTT is symmetric in charge one have to subtract 0.5*yTT]
  #PosPdg
  muonCut = '&&leptonPdg>0&&abs(leptonPdg)==13'
  correction_lowDPhi        = {'y':0.5*yTT_crNJet_0b_lowDPhi,'e':0.5*yTT_Var_crNJet_0b_lowDPhi}
  correction_highDPhi       = {'y':0.5*yTT_crNJet_0b_highDPhi,'e':0.5*yTT_Var_crNJet_0b_highDPhi}
  correction_lowDPhi_rest   = {'y':yTT_crNJet_0b_lowDPhi+rd['yRest_crNJet_0b_lowDPhi_truth_PosPdg'],'e':yTT_Var_crNJet_0b_lowDPhi+sqrt(rd['yRest_Var_crNJet_0b_lowDPhi_truth_PosPdg'])}
  correction_highDPhi_rest  = {'y':yTT_crNJet_0b_highDPhi+rd['yRest_crNJet_0b_highDPhi_truth_PosPdg'],'e':yTT_Var_crNJet_0b_highDPhi+sqrt(rd['yRest_Var_crNJet_0b_highDPhi_truth_PosPdg'])}
  
  if isData:
    #treat contamination like QCD
    rCS_W_PosPdg_crNJet_0b_corr       = getRCS(cData, crCutTruth+muonCut,dPhiCut, QCD_lowDPhi=correction_lowDPhi, QCD_highDPhi=correction_highDPhi, returnValues=True)
    rCS_W_PosPdg_crNJet_0b_corr_rest  = getRCS(cData, crCutTruth+muonCut,dPhiCut, QCD_lowDPhi=correction_lowDPhi_rest, QCD_highDPhi=correction_highDPhi_rest, returnValues=True)
    rCS_W_PosPdg_crNJet_0b_notcorr    = getRCS(cData, crCutTruth+muonCut, dPhiCut, returnValues = True)

  else:
    rCS_W_PosPdg_crNJet_0b_corr       = getRCS(cBkg, crCut+muonCut,dPhiCut, weight=weight_str_0b, QCD_lowDPhi=correction_lowDPhi, QCD_highDPhi=correction_highDPhi, returnValues=True)
    rCS_W_PosPdg_crNJet_0b_corr_rest  = getRCS(cBkg, crCut+muonCut,dPhiCut, weight=weight_str_0b, QCD_lowDPhi=correction_lowDPhi_rest, QCD_highDPhi=correction_highDPhi_rest, returnValues=True)
    rCS_W_PosPdg_crNJet_0b_notcorr    = getRCS(cBkg, crCut+muonCut, dPhiCut, weight=weight_str_0b, returnValues=True)

  #NegPdg
  muonCut = '&&leptonPdg<0&&abs(leptonPdg)==13'
  correction_lowDPhi_rest   = {'y':yTT_crNJet_0b_lowDPhi+rd['yRest_crNJet_0b_lowDPhi_truth_NegPdg'],'e':yTT_Var_crNJet_0b_lowDPhi+sqrt(rd['yRest_Var_crNJet_0b_lowDPhi_truth_NegPdg'])}
  correction_highDPhi_rest  = {'y':yTT_crNJet_0b_highDPhi+rd['yRest_crNJet_0b_highDPhi_truth_NegPdg'],'e':yTT_Var_crNJet_0b_highDPhi+sqrt(rd['yRest_Var_crNJet_0b_highDPhi_truth_NegPdg'])}

  if isData:
    #treat contamination like QCD
    rCS_W_NegPdg_crNJet_0b_corr       = getRCS(cData, crCutTruth+muonCut,dPhiCut, QCD_lowDPhi=correction_lowDPhi, QCD_highDPhi=correction_highDPhi, returnValues=True)
    rCS_W_NegPdg_crNJet_0b_corr_rest  = getRCS(cData, crCutTruth+muonCut,dPhiCut, QCD_lowDPhi=correction_lowDPhi_rest, QCD_highDPhi=correction_highDPhi_rest, returnValues=True)
    rCS_W_NegPdg_crNJet_0b_notcorr    = getRCS(cData, crCutTruth+muonCut, dPhiCut, returnValues = True)

  else:
    rCS_W_NegPdg_crNJet_0b_corr       = getRCS(cBkg, crCut+muonCut,dPhiCut, weight=weight_str_0b, QCD_lowDPhi=correction_lowDPhi, QCD_highDPhi=correction_highDPhi, returnValues=True)
    rCS_W_NegPdg_crNJet_0b_corr_rest  = getRCS(cBkg, crCut+muonCut,dPhiCut, weight=weight_str_0b, QCD_lowDPhi=correction_lowDPhi_rest, QCD_highDPhi=correction_highDPhi_rest, returnValues=True)
    rCS_W_NegPdg_crNJet_0b_notcorr    = getRCS(cBkg, crCut+muonCut, dPhiCut, weight=weight_str_0b, returnValues=True)


  rd['y_crNJet_0b_highDPhi']          = rCS_W_crNJet_0b_notcorr['num']
  rd['y_Var_crNJet_0b_highDPhi']      = rCS_W_crNJet_0b_notcorr['numE']**2
  rd['y_crNJet_0b_lowDPhi']           = rCS_W_crNJet_0b_notcorr['denom']
  rd['y_Var_crNJet_0b_lowDPhi']       = rCS_W_crNJet_0b_notcorr['denomE']**2
  rd['rCS_W_crNJet_0b_corr']          = rCS_W_crNJet_0b_corr['rCS']
  rd['rCS_Var_W_crNJet_0b_corr']      = rCS_W_crNJet_0b_corr['rCSE_sim']**2
  rd['rCS_W_crNJet_0b_notcorr']       = rCS_W_crNJet_0b_notcorr['rCS']
  rd['rCS_Var_W_crNJet_0b_notcorr']   = rCS_W_crNJet_0b_notcorr['rCSE_sim']**2
  rd['rCS_W_crNJet_0b_corr_rest']     = rCS_W_crNJet_0b_corr_rest['rCS']
  rd['rCS_Var_W_crNJet_0b_corr_rest'] = rCS_W_crNJet_0b_corr_rest['rCSE_sim']**2
  rd['rCS_W_crNJet_0b_truth']         = getRCS(cWJets, crCut,  dPhiCut, weight_str_0bMC)
  #PosPdg
  rd['y_crNJet_0b_highDPhi_PosPdg']          = rCS_W_PosPdg_crNJet_0b_notcorr['num'] 
  rd['y_Var_crNJet_0b_highDPhi_PosPdg']      = rCS_W_PosPdg_crNJet_0b_notcorr['numE']**2 
  rd['y_crNJet_0b_lowDPhi_PosPdg']           = rCS_W_PosPdg_crNJet_0b_notcorr['denom'] 
  rd['y_Var_crNJet_0b_lowDPhi_PosPdg']       = rCS_W_PosPdg_crNJet_0b_notcorr['denomE']**2 
  rd['rCS_W_PosPdg_crNJet_0b_corr']          = rCS_W_PosPdg_crNJet_0b_corr['rCS'] 
  rd['rCS_Var_W_PosPdg_crNJet_0b_corr']      = rCS_W_PosPdg_crNJet_0b_corr['rCSE_sim']**2 
  rd['rCS_W_PosPdg_crNJet_0b_notcorr']       = rCS_W_PosPdg_crNJet_0b_notcorr['rCS'] 
  rd['rCS_Var_W_PosPdg_crNJet_0b_notcorr']   = rCS_W_PosPdg_crNJet_0b_notcorr['rCSE_sim']**2
  rd['rCS_W_PosPdg_crNJet_0b_corr_rest']     = rCS_W_PosPdg_crNJet_0b_corr_rest['rCS']
  rd['rCS_Var_W_PosPdg_crNJet_0b_corr_rest'] = rCS_W_PosPdg_crNJet_0b_corr_rest['rCSE_sim']**2 
  rd['rCS_W_PosPdg_crNJet_0b_truth']         = getRCS(cWJets, 'leptonPdg>0&&'+crCut, dPhiCut, weight_str_0bMC)
  #NegPdg
  rd['y_crNJet_0b_highDPhi_NegPdg']          = rCS_W_NegPdg_crNJet_0b_notcorr['num'] 
  rd['y_Var_crNJet_0b_highDPhi_NegPdg']      = rCS_W_NegPdg_crNJet_0b_notcorr['numE']**2 
  rd['y_crNJet_0b_lowDPhi_NegPdg']           = rCS_W_NegPdg_crNJet_0b_notcorr['denom'] 
  rd['y_Var_crNJet_0b_lowDPhi_NegPdg']       = rCS_W_NegPdg_crNJet_0b_notcorr['denomE']**2 
  rd['rCS_W_NegPdg_crNJet_0b_corr']          = rCS_W_NegPdg_crNJet_0b_notcorr['rCS'] 
  rd['rCS_Var_W_NegPdg_crNJet_0b_corr']      = rCS_W_NegPdg_crNJet_0b_notcorr['rCSE_sim']**2 
  rd['rCS_W_NegPdg_crNJet_0b_notcorr']       = rCS_W_NegPdg_crNJet_0b_notcorr['rCS'] 
  rd['rCS_Var_W_NegPdg_crNJet_0b_notcorr']   = rCS_W_NegPdg_crNJet_0b_notcorr['rCSE_sim']**2
  rd['rCS_W_NegPdg_crNJet_0b_corr_rest']     = rCS_W_NegPdg_crNJet_0b_corr_rest['rCS']
  rd['rCS_Var_W_NegPdg_crNJet_0b_corr_rest'] = rCS_W_NegPdg_crNJet_0b_corr_rest['rCSE_sim']**2
  rd['rCS_W_NegPdg_crNJet_0b_truth']         = getRCS(cWJets, 'leptonPdg<0&&'+crCut, dPhiCut, weight_str_0bMC)
  
  fit_srName, fit_srCut = nameAndCut(stb, htb, srNJet, btb=None, presel=presel,btagVar = nBTagVar)
  #QCD yields in CR for b-tag fit
  if QCD:
    QCD_dict={0:{'y':QCD[srNJet][stb][htb][(0,0)][dPhiCut]['NQCDpred_lowdPhi'], 'e':QCD[srNJet][stb][htb][(0,0)][dPhiCut]['NQCDpred_lowdPhi_err'], 'totalY':QCD[srNJet][stb][htb][(0,0)][dPhiCut]['NQCDpred']},\
              1:{'y':QCD[srNJet][stb][htb][(1,1)][dPhiCut]['NQCDpred_lowdPhi'], 'e':QCD[srNJet][stb][htb][(1,1)][dPhiCut]['NQCDpred_lowdPhi_err'], 'totalY':QCD[srNJet][stb][htb][(1,1)][dPhiCut]['NQCDpred']},\
              2:{'y':QCD[srNJet][stb][htb][(2,-1)][dPhiCut]['NQCDpred_lowdPhi'], 'e':QCD[srNJet][stb][htb][(2,-1)][dPhiCut]['NQCDpred_lowdPhi_err'], 'totalY':QCD[srNJet][stb][htb][(2,-1)][dPhiCut]['NQCDpred']}}
    fit_srNJet_lowDPhi = binnedNBTagsFit(fit_srCut+"&&"+dPhiStr+"<"+str(dPhiCut), fit_srName+'_dPhi'+str(dPhiCut), samples = samples, prefix=fit_srName, QCD_dict=QCD_dict)
  else:
    fit_srNJet_lowDPhi = binnedNBTagsFit(fit_srCut+"&&"+dPhiStr+"<"+str(dPhiCut), fit_srName+'_dPhi'+str(dPhiCut), samples = samples, prefix=fit_srName)
#  fit_srNJet_lowDPhi = binnedNBTagsFit(fit_srCut+"&&"+dPhiStr+"<"+str(dPhiCut), samples = {'W':cWJets, 'TT':cTTJets}, nBTagVar = 'nBJetMedium25', prefix=fit_srName)

  rd['fit_srNJet_lowDPhi_W'] = fit_srNJet_lowDPhi
#  print "Check: Impact of TT on RCS(W)"
#  print "Subtract numerator  ", yTT_crNJet_0b_highDPhi,'(rcs=',rCS_crNJet_1b['rCS'],'yield_0b',yTT_crNJet_0b_lowDPhi,') true',yTT_crNJet_0b_highDPhi_truth
#  print "Subtract denominator", yTT_crNJet_0b_lowDPhi,'true', yTT_crNJet_0b_lowDPhi_truth

  yW_srNJet_0b_lowDPhi  =  fit_srNJet_lowDPhi['W_PosPdg']['yield']*fit_srNJet_lowDPhi['W_PosPdg']['template'].GetBinContent(1)\
                        +  fit_srNJet_lowDPhi['W_NegPdg']['yield']*fit_srNJet_lowDPhi['W_NegPdg']['template'].GetBinContent(1)
  yW_Var_srNJet_0b_lowDPhi  =  fit_srNJet_lowDPhi['W_PosPdg']['yieldVar']*fit_srNJet_lowDPhi['W_PosPdg']['template'].GetBinContent(1)**2\
                            +  fit_srNJet_lowDPhi['W_NegPdg']['yieldVar']*fit_srNJet_lowDPhi['W_NegPdg']['template'].GetBinContent(1)**2#FIXME I add that uncorrelated
  if templateBootstrap: yW_Var_srNJet_0b_lowDPhi += fit_srNJet_lowDPhi['W_PosPdg']['yield']**2*templateBootstrap['WJets_PosPdg'][srNJet][stb][htb]**2\
                                                  + fit_srNJet_lowDPhi['W_NegPdg']['yield']**2*templateBootstrap['WJets_NegPdg'][srNJet][stb][htb]**2

  yW_PosPdg_srNJet_0b_lowDPhi = fit_srNJet_lowDPhi['W_PosPdg']['yield']*fit_srNJet_lowDPhi['W_PosPdg']['template'].GetBinContent(1)
  yW_PosPdg_Var_srNJet_0b_lowDPhi = fit_srNJet_lowDPhi['W_PosPdg']['yieldVar']*fit_srNJet_lowDPhi['W_PosPdg']['template'].GetBinContent(1)**2
  if templateBootstrap: yW_PosPdg_Var_srNJet_0b_lowDPhi += fit_srNJet_lowDPhi['W_PosPdg']['yield']**2*templateBootstrap['WJets_PosPdg'][srNJet][stb][htb]**2
  
  yW_NegPdg_srNJet_0b_lowDPhi = fit_srNJet_lowDPhi['W_NegPdg']['yield']*fit_srNJet_lowDPhi['W_NegPdg']['template'].GetBinContent(1)
  yW_NegPdg_Var_srNJet_0b_lowDPhi = fit_srNJet_lowDPhi['W_NegPdg']['yieldVar']*fit_srNJet_lowDPhi['W_NegPdg']['template'].GetBinContent(1)**2
  if templateBootstrap: yW_NegPdg_Var_srNJet_0b_lowDPhi += fit_srNJet_lowDPhi['W_NegPdg']['yield']**2*templateBootstrap['WJets_NegPdg'][srNJet][stb][htb]**2

  # for systematics
  rCS_crLowNJet_0b_onlyW            = getRCS(cWJets, crCut, dPhiCut, weight_str_0bMC)
  rCS_crLowNJet_0b_onlyW_PosPdg     = getRCS(cWJets, 'leptonPdg>0&&'+crCut, dPhiCut, weight_str_0bMC)
  rCS_crLowNJet_0b_onlyW_NegPdg     = getRCS(cWJets, 'leptonPdg<0&&'+crCut, dPhiCut, weight_str_0bMC)
  rCS_crLowNJet_0b_onlyW_mu         = getRCS(cWJets, crCut+'&&abs(leptonPdg)==13', dPhiCut, weight_str_0bMC)
  rCS_crLowNJet_0b_onlyW_mu_PosPdg  = getRCS(cWJets, crCut+'&&leptonPdg>0&&abs(leptonPdg)==13', dPhiCut, weight_str_0bMC)
  rCS_crLowNJet_0b_onlyW_mu_NegPdg  = getRCS(cWJets, crCut+'&&leptonPdg<0&&abs(leptonPdg)==13', dPhiCut, weight_str_0bMC)  
  rd['rCS_crLowNJet_0b_onlyW']           = rCS_crLowNJet_0b_onlyW
  rd['rCS_crLowNJet_0b_onlyW_PosPdg']    = rCS_crLowNJet_0b_onlyW_PosPdg
  rd['rCS_crLowNJet_0b_onlyW_NegPdg']    = rCS_crLowNJet_0b_onlyW_NegPdg
  rd['rCS_crLowNJet_0b_onlyW_mu']        = rCS_crLowNJet_0b_onlyW_mu
  rd['rCS_crLowNJet_0b_onlyW_mu_PosPdg'] = rCS_crLowNJet_0b_onlyW_mu_PosPdg
  rd['rCS_crLowNJet_0b_onlyW_mu_NegPdg'] = rCS_crLowNJet_0b_onlyW_mu_NegPdg
  
  rCS_sr_Name_0b, rCS_sr_Cut_0b = nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel, btagVar = nBTagVar)#for Check 
  if useBTagWeights:
    rCS_sr_Name, rCS_sr_Cut = nameAndCut(stb, htb, srNJet, btb=None, presel=presel, btagVar = nBTagVar)
  else:
    rCS_sr_Cut = rCS_sr_Cut_0b
  rCS_srNJet_0b_onlyW             = getRCS(cWJets, rCS_sr_Cut,  dPhiCut, weight_str_0bMC)
  rCS_srNJet_0b_onlyW_mu          = getRCS(cWJets, rCS_sr_Cut+'&&abs(leptonPdg)==13',  dPhiCut, weight_str_0bMC)
  rCS_srNJet_0b_onlyW_ele         = getRCS(cWJets, rCS_sr_Cut+'&&abs(leptonPdg)==11',  dPhiCut, weight_str_0bMC)
  rCS_srNJet_0b_onlyW_PosPdg      = getRCS(cWJets, 'leptonPdg>0&&'+rCS_sr_Cut,  dPhiCut, weight_str_0bMC)
  rCS_srNJet_0b_onlyW_NegPdg      = getRCS(cWJets, 'leptonPdg<0&&'+rCS_sr_Cut,  dPhiCut, weight_str_0bMC)
  rCS_srNJet_0b_onlyW_mu_PosPdg   = getRCS(cWJets, 'leptonPdg>0&&abs(leptonPdg)==13&&'+rCS_sr_Cut,  dPhiCut, weight_str_0bMC)
  rCS_srNJet_0b_onlyW_mu_NegPdg   = getRCS(cWJets, 'leptonPdg<0&&abs(leptonPdg)==13&&'+rCS_sr_Cut,  dPhiCut, weight_str_0bMC)
  rCS_srNJet_0b_onlyW_ele_PosPdg  = getRCS(cWJets, 'leptonPdg>0&&abs(leptonPdg)==11&&'+rCS_sr_Cut,  dPhiCut, weight_str_0bMC)
  rCS_srNJet_0b_onlyW_ele_NegPdg  = getRCS(cWJets, 'leptonPdg<0&&abs(leptonPdg)==11&&'+rCS_sr_Cut,  dPhiCut, weight_str_0bMC)

  rd['yW_srNJet_0b_lowDPhi']            = yW_srNJet_0b_lowDPhi  
  rd['yW_Var_srNJet_0b_lowDPhi']        = yW_Var_srNJet_0b_lowDPhi 
  rd['yW_PosPdg_srNJet_0b_lowDPhi']     = yW_PosPdg_srNJet_0b_lowDPhi
  rd['yW_PosPdg_Var_srNJet_0b_lowDPhi'] = yW_PosPdg_Var_srNJet_0b_lowDPhi
  rd['yW_NegPdg_srNJet_0b_lowDPhi']     = yW_NegPdg_srNJet_0b_lowDPhi
  rd['yW_NegPdg_Var_srNJet_0b_lowDPhi'] = yW_NegPdg_Var_srNJet_0b_lowDPhi

  rd['rCS_srNJet_0b_onlyW']             = rCS_srNJet_0b_onlyW
  rd['rCS_srNJet_0b_onlyW_mu']          = rCS_srNJet_0b_onlyW_mu
  rd['rCS_srNJet_0b_onlyW_ele']         = rCS_srNJet_0b_onlyW_ele
  rd['rCS_srNJet_0b_onlyW_PosPdg']      = rCS_srNJet_0b_onlyW_PosPdg #Rcs in SR for ele+mu, pos PDG
  rd['rCS_srNJet_0b_onlyW_NegPdg']      = rCS_srNJet_0b_onlyW_NegPdg #Rcs in SR for ele+mu, neg PDG
  rd['rCS_srNJet_0b_onlyW_mu_PosPdg']   = rCS_srNJet_0b_onlyW_mu_PosPdg #Rcs in SR for mu, pos PDG
  rd['rCS_srNJet_0b_onlyW_mu_NegPdg']   = rCS_srNJet_0b_onlyW_mu_NegPdg #Rcs in SR for mu, neg PDG
  rd['rCS_srNJet_0b_onlyW_ele_PosPdg']  = rCS_srNJet_0b_onlyW_ele_PosPdg #Rcs in SR for ele, pos PDG
  rd['rCS_srNJet_0b_onlyW_ele_NegPdg']  = rCS_srNJet_0b_onlyW_ele_NegPdg #Rcs in SR for ele, neg PDG

  #true yields measured from MC samples, residual background is also calculated here and added to the dict
  truth_W, truth_W_var       = getYieldFromChain(cWJets,  rCS_sr_Cut+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_str_0bMC, returnVar=True)
  truth_Rest, truth_Rest_var = getYieldFromChain(cRest,   rCS_sr_Cut+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_str_0bMC, returnVar=True)

  truth_W_PosPdg, truth_W_var_PosPdg       = getYieldFromChain(cWJets, 'leptonPdg>0&&'+rCS_sr_Cut+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_str_0bMC, returnVar=True)
  truth_W_NegPdg, truth_W_var_NegPdg       = getYieldFromChain(cWJets, 'leptonPdg<0&&'+rCS_sr_Cut+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_str_0bMC, returnVar=True)
  truth_Rest_PosPdg, truth_Rest_var_PosPdg = getYieldFromChain(cRest,  'leptonPdg>0&&'+rCS_sr_Cut+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_str_0bMC, returnVar=True)
  truth_Rest_NegPdg, truth_Rest_var_NegPdg = getYieldFromChain(cRest,  'leptonPdg<0&&'+rCS_sr_Cut+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_str_0bMC, returnVar=True)

  #predicted yields with RCS method
  pred_W                = yW_srNJet_0b_lowDPhi*rCS_W_crNJet_0b_corr['rCS']
  pred_Var_W            = yW_Var_srNJet_0b_lowDPhi*rCS_W_crNJet_0b_corr['rCS']**2 + yW_srNJet_0b_lowDPhi**2*rCS_W_crNJet_0b_corr['rCSE_sim']**2
  pred_corrRest_W       = yW_srNJet_0b_lowDPhi*rCS_W_crNJet_0b_corr_rest['rCS']
  pred_Var_corrRest_W   = yW_Var_srNJet_0b_lowDPhi*rCS_W_crNJet_0b_corr_rest['rCS']**2 + yW_srNJet_0b_lowDPhi**2*rCS_W_crNJet_0b_corr_rest['rCSE_sim']**2

  pred_W_PosPdg               = yW_PosPdg_srNJet_0b_lowDPhi*rCS_W_PosPdg_crNJet_0b_corr['rCS']
  pred_Var_W_PosPdg           = yW_PosPdg_Var_srNJet_0b_lowDPhi*rCS_W_PosPdg_crNJet_0b_corr['rCS']**2 + yW_PosPdg_srNJet_0b_lowDPhi**2*rCS_W_PosPdg_crNJet_0b_corr['rCSE_sim']**2
  pred_corrRest_W_PosPdg      = yW_PosPdg_srNJet_0b_lowDPhi*rCS_W_PosPdg_crNJet_0b_corr_rest['rCS']
  pred_Var_corrRest_W_PosPdg  = yW_PosPdg_Var_srNJet_0b_lowDPhi*rCS_W_PosPdg_crNJet_0b_corr_rest['rCS']**2 + yW_PosPdg_srNJet_0b_lowDPhi**2*rCS_W_PosPdg_crNJet_0b_corr_rest['rCSE_sim']**2

  pred_W_NegPdg               = yW_NegPdg_srNJet_0b_lowDPhi*rCS_W_NegPdg_crNJet_0b_corr['rCS']
  pred_Var_W_NegPdg           = yW_NegPdg_Var_srNJet_0b_lowDPhi*rCS_W_NegPdg_crNJet_0b_corr['rCS']**2 + yW_NegPdg_srNJet_0b_lowDPhi**2*rCS_W_NegPdg_crNJet_0b_corr['rCSE_sim']**2
  pred_corrRest_W_NegPdg      = yW_NegPdg_srNJet_0b_lowDPhi*rCS_W_NegPdg_crNJet_0b_corr_rest['rCS']
  pred_Var_corrRest_W_NegPdg  = yW_NegPdg_Var_srNJet_0b_lowDPhi*rCS_W_NegPdg_crNJet_0b_corr_rest['rCS']**2 + yW_NegPdg_srNJet_0b_lowDPhi**2*rCS_W_NegPdg_crNJet_0b_corr_rest['rCSE_sim']**2


  print "W pred:",pred_W,'+/-',sqrt(pred_Var_W),'W truth:',truth_W,'+/-',sqrt(truth_W_var)
  print "W(-) pred:",pred_W_PosPdg,'+/-',sqrt(pred_Var_W_PosPdg),'W truth:',truth_W_PosPdg,'+/-',sqrt(truth_W_var_PosPdg)
  print "W(+) pred:",pred_W_NegPdg,'+/-',sqrt(pred_Var_W_NegPdg),'W truth:',truth_W_NegPdg,'+/-',sqrt(truth_W_var_NegPdg)


  rd.update( {"W_pred":pred_W,"W_pred_err":sqrt(pred_Var_W),\
              "W_pred_corrRest":pred_corrRest_W,"W_pred_corrRest_err":sqrt(pred_Var_corrRest_W),\
              "W_truth":truth_W,"W_truth_err":sqrt(truth_W_var),\
              "W_PosPdg_pred":pred_W_PosPdg,"W_PosPdg_pred_err":sqrt(pred_Var_W_PosPdg),\
              "W_PosPdg_pred_corrRest":pred_corrRest_W_PosPdg,"W_PosPdg_pred_corrRest_err":sqrt(pred_Var_corrRest_W_PosPdg),\
              "W_PosPdg_truth":truth_W_PosPdg,"W_PosPdg_truth_err":sqrt(truth_W_var_PosPdg),\
              "W_NegPdg_pred":pred_W_NegPdg,"W_NegPdg_pred_err":sqrt(pred_Var_W_NegPdg),\
              "W_NegPdg_pred_corrRest":pred_corrRest_W_NegPdg,"W_NegPdg_pred_corrRest_err":sqrt(pred_Var_corrRest_W_NegPdg),\
              "W_NegPdg_truth":truth_W_NegPdg,"W_NegPdg_truth_err":sqrt(truth_W_var_NegPdg),\
              'Rest_truth':truth_Rest,'Rest_truth_err':sqrt(truth_Rest_var),\
              'Rest_PosPdg_truth':truth_Rest_PosPdg,'Rest_PosPdg_truth_err':sqrt(truth_Rest_var_PosPdg),\
              'Rest_NegPdg_truth':truth_Rest_NegPdg,'Rest_NegPdg_truth_err':sqrt(truth_Rest_var_NegPdg),\
              })
  bins.update(rd)
  del rd
  return bins

