import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName
from Workspace.HEPHYPythonTools.user import username
from binnedNBTagsFit import binnedNBTagsFit
from rCShelpers import * 
from math import pi, sqrt, isnan
from rCShelpers import *

from predictionConfig import *

ROOT.TH1F().SetDefaultSumw2()

def makeTTPrediction(bins, samples, htb, stb, srNJet, presel, dPhiCut=1.0, QCD=False):
  #print "in make tt prediction lumi is :" , lumi
  weight_str, weight_err_str = makeWeight(lumi, sampleLumi, reWeight=MCweight)
  cWJets = samples['W']
  cTTJets = samples['TT']
  cRest = samples['Rest']
  cBkg = samples['Bkg']
  cData = samples['Data']
  rd = {}
  
  if isData:
    w = 'weight'
    w_err = 'weight**2'
  else:
    w = weight_str
    w_err = weight_err_str
  
  #TT Jets yield in srNJet, no b-tag cut, low DPhi
  fit_srName, fit_srCut = nameAndCut(stb, htb, srNJet, btb=None, presel=presel, btagVar = nBTagVar)

  if QCD:
    #Get QCD yields in CR for b-tag fit
    QCD_dict={0:{'y':QCD[srNJet][stb][htb][(0,0)][dPhiCut]['NQCDpred_lowdPhi'], 'e':QCD[srNJet][stb][htb][(0,0)][dPhiCut]['NQCDpred_lowdPhi_err'], 'totalY':QCD[srNJet][stb][htb][(0,0)][dPhiCut]['NQCDpred']},\
              1:{'y':QCD[srNJet][stb][htb][(1,1)][dPhiCut]['NQCDpred_lowdPhi'], 'e':QCD[srNJet][stb][htb][(1,1)][dPhiCut]['NQCDpred_lowdPhi_err'], 'totalY':QCD[srNJet][stb][htb][(1,1)][dPhiCut]['NQCDpred']},\
              2:{'y':QCD[srNJet][stb][htb][(2,-1)][dPhiCut]['NQCDpred_lowdPhi'], 'e':QCD[srNJet][stb][htb][(2,-1)][dPhiCut]['NQCDpred_lowdPhi_err'], 'totalY':QCD[srNJet][stb][htb][(2,-1)][dPhiCut]['NQCDpred']}}
    fit_srNJet_lowDPhi = binnedNBTagsFit(fit_srCut+"&&"+dPhiStr+"<"+str(dPhiCut), fit_srName+'_dPhi'+str(dPhiCut), samples = samples, prefix=fit_srName, QCD_dict=QCD_dict)
  else:
    fit_srNJet_lowDPhi = binnedNBTagsFit(fit_srCut+"&&"+dPhiStr+"<"+str(dPhiCut), fit_srName+'_dPhi'+str(dPhiCut), samples = samples, prefix=fit_srName)
  
#  fit_srNJet_lowDPhi = binnedNBTagsFit(fit_srCut+"&&"+dPhiStr+"<"+str(dPhiCut), samples = {'W':cWJets, 'TT':cTTJets}, nBTagVar = 'nBJetMedium25', prefix=fit_srName)
  rd['fit_srNJet_lowDPhi'] = fit_srNJet_lowDPhi

  yTT_srNJet_0b_lowDPhi =  fit_srNJet_lowDPhi['TT_AllPdg']['yield']*fit_srNJet_lowDPhi['TT_AllPdg']['template'].GetBinContent(1)
  if templateBootstrap:
    print
    print 'Using bootstrap template error'
  yTT_Var_srNJet_0b_lowDPhi =  fit_srNJet_lowDPhi['TT_AllPdg']['yieldVar']*fit_srNJet_lowDPhi['TT_AllPdg']['template'].GetBinContent(1)**2
  print yTT_Var_srNJet_0b_lowDPhi
  if templateBootstrap: yTT_Var_srNJet_0b_lowDPhi += fit_srNJet_lowDPhi['TT_AllPdg']['yield']**2*templateBootstrap['TTJets'][srNJet][stb][htb]**2
  print yTT_Var_srNJet_0b_lowDPhi
  print

  rCS_crLowNJet_Name, rCS_crLowNJet_Cut = nameAndCut(stb, htb, (4,5), presel=presel, btagVar = nBTagVar)
  rCS_sr_Name_0b, rCS_sr_Cut_0b = nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel, btagVar = nBTagVar)#for Check 
  rCS_sr_Name, rCS_sr_Cut = nameAndCut(stb, htb, srNJet, btb=None, presel=presel, btagVar = nBTagVar)
  rCS_crLowNJet_Name_1b, rCS_crLowNJet_Cut_1b = nameAndCut(stb, htb, (4,5), btb=(1,1), presel=presel, btagVar = nBTagVar)

  if useBTagWeights:
    weight_str_1b = weight_str+'*weightBTag1'+btagWeightSuffix
    weight_str_0b = weight_str+'*weightBTag0'+btagWeightSuffix
    weight_str_1bMC = weight_str+'*weightBTag1_SF'
    weight_str_0bMC = weight_str+'*weightBTag0_SF'
  else:
    weight_str_1b = weight_str
    weight_str_0b = weight_str
    weight_str_1bMC = weight_str
    weight_str_0bMC = weight_str
    rCS_crLowNJet_Cut = rCS_crLowNJet_Cut_1b
    rCS_sr_Cut = rCS_sr_Cut_0b
    

  # get MC truth values for W and ttbar
  yTT_crNJet_1b_lowDPhi_truth     = getYieldFromChain(cTTJets, cutString = rCS_crLowNJet_Cut+'&&'+dPhiStr+'<'+str(dPhiCut),weight=weight_str_1bMC, returnError = True)
  yTT_crNJet_1b_highDPhi_truth    = getYieldFromChain(cTTJets, cutString = rCS_crLowNJet_Cut+'&&'+dPhiStr+'>'+str(dPhiCut),weight=weight_str_1bMC, returnError = True)
  yW_crNJet_1b_lowDPhi_truth      = getYieldFromChain(cWJets, cutString = rCS_crLowNJet_Cut+'&&'+dPhiStr+'<'+str(dPhiCut),weight=weight_str_1bMC, returnError = True)
  yW_crNJet_1b_highDPhi_truth     = getYieldFromChain(cWJets, cutString = rCS_crLowNJet_Cut+'&&'+dPhiStr+'>'+str(dPhiCut),weight=weight_str_1bMC, returnError = True)
  yRest_crNJet_1b_lowDPhi_truth   = getYieldFromChain(cRest, cutString = rCS_crLowNJet_Cut+'&&'+dPhiStr+'<'+str(dPhiCut),weight=weight_str_1bMC, returnError = True)
  yRest_crNJet_1b_highDPhi_truth  = getYieldFromChain(cRest, cutString = rCS_crLowNJet_Cut+'&&'+dPhiStr+'>'+str(dPhiCut),weight=weight_str_1bMC, returnError = True)
  yQCD_crNJet_1b_lowDPhi_truth    = getYieldFromChain(cQCD, cutString = rCS_crLowNJet_Cut_1b+'&&'+dPhiStr+'<'+str(dPhiCut),weight=weight_str, returnError = True)
  yQCD_crNJet_1b_highDPhi_truth   = getYieldFromChain(cQCD, cutString = rCS_crLowNJet_Cut_1b+'&&'+dPhiStr+'>'+str(dPhiCut),weight=weight_str, returnError = True)

  rd['yTT_crNJet_1b_lowDPhi_truth']       = yTT_crNJet_1b_lowDPhi_truth[0]
  rd['yTT_Var_crNJet_1b_lowDPhi_truth']   = yTT_crNJet_1b_lowDPhi_truth[1]**2
  rd['yTT_crNJet_1b_highDPhi_truth']      = yTT_crNJet_1b_highDPhi_truth[0]
  rd['yTT_Var_crNJet_1b_highDPhi_truth']  = yTT_crNJet_1b_highDPhi_truth[1]**2

  rd['yW_crNJet_1b_lowDPhi_truth']      = yW_crNJet_1b_lowDPhi_truth[0]
  rd['yW_Var_crNJet_1b_lowDPhi_truth']  = yW_crNJet_1b_lowDPhi_truth[1]**2
  rd['yW_crNJet_1b_highDPhi_truth']     = yW_crNJet_1b_highDPhi_truth[0]
  rd['yW_Var_crNJet_1b_highDPhi_truth'] = yW_crNJet_1b_highDPhi_truth[1]**2

  rd['yRest_crNJet_1b_lowDPhi_truth']      = yRest_crNJet_1b_lowDPhi_truth[0]
  rd['yRest_Var_crNJet_1b_lowDPhi_truth']  = yRest_crNJet_1b_lowDPhi_truth[1]**2
  rd['yRest_crNJet_1b_highDPhi_truth']     = yRest_crNJet_1b_highDPhi_truth[0]
  rd['yRest_Var_crNJet_1b_highDPhi_truth'] = yRest_crNJet_1b_highDPhi_truth[1]**2

  rd['yQCD_crNJet_1b_lowDPhi_truth']      = yQCD_crNJet_1b_lowDPhi_truth[0]
  rd['yQCD_Var_crNJet_1b_lowDPhi_truth']  = yQCD_crNJet_1b_lowDPhi_truth[1]**2
  rd['yQCD_crNJet_1b_highDPhi_truth']     = yQCD_crNJet_1b_highDPhi_truth[0]
  rd['yQCD_Var_crNJet_1b_highDPhi_truth'] = yQCD_crNJet_1b_highDPhi_truth[1]**2

  if QCD: #get estimated QCD yields for Rcs calculation in 1b (high and low deltaPhi)
    QCD_lowDPhi  = {'y':QCD[(4,5)][stb][htb][(1,1)][dPhiCut]['NQCDpred_lowdPhi'], 'e':QCD[(4,5)][stb][htb][(1,1)][dPhiCut]['NQCDpred_lowdPhi_err']}
    QCD_highDPhi = {'y':QCD[(4,5)][stb][htb][(1,1)][dPhiCut]['NQCDpred_highdPhi'],'e':QCD[(4,5)][stb][htb][(1,1)][dPhiCut]['NQCDpred_highdPhi_err']}
    QCDlist = [QCD_lowDPhi, QCD_highDPhi]
    for q in QCDlist:
      for e in q:
        if isnan(q[e]):
          print 'found nan value error value in QCD estimation, setting error to 100% instead'
          q['e'] = q['y']

  if isData:
    if QCD:
      rCS_crLowNJet_1b = getRCS(cData, rCS_crLowNJet_Cut_1b,  dPhiCut, weight = w, QCD_lowDPhi=QCD_lowDPhi, QCD_highDPhi=QCD_highDPhi, returnValues=True) #Low njet tt-jets CR to be orthoganl to DPhi 
    else:
      rCS_crLowNJet_1b = getRCS(cData, rCS_crLowNJet_Cut_1b,  dPhiCut, weight = w, returnValues=True)

  else:
    if useQCDestimation:
      yTT_crNJet_1b_lowDPhi     = getYieldFromChain(cTTJets, cutString = rCS_crLowNJet_Cut+'&&'+dPhiStr+'<'+str(dPhiCut),weight=weight_str_1b, returnError = True)
      yTT_crNJet_1b_highDPhi    = getYieldFromChain(cTTJets, cutString = rCS_crLowNJet_Cut+'&&'+dPhiStr+'>'+str(dPhiCut),weight=weight_str_1b, returnError = True)
      yW_crNJet_1b_lowDPhi      = getYieldFromChain(cWJets, cutString = rCS_crLowNJet_Cut+'&&'+dPhiStr+'<'+str(dPhiCut),weight=weight_str_1b, returnError = True)
      yW_crNJet_1b_highDPhi     = getYieldFromChain(cWJets, cutString = rCS_crLowNJet_Cut+'&&'+dPhiStr+'>'+str(dPhiCut),weight=weight_str_1b, returnError = True)
      yRest_crNJet_1b_lowDPhi   = getYieldFromChain(cRest, cutString = rCS_crLowNJet_Cut+'&&'+dPhiStr+'<'+str(dPhiCut),weight=weight_str_1b, returnError = True)
      yRest_crNJet_1b_highDPhi  = getYieldFromChain(cRest, cutString = rCS_crLowNJet_Cut+'&&'+dPhiStr+'>'+str(dPhiCut),weight=weight_str_1b, returnError = True)
      yQCD_crNJet_1b_lowDPhi    = getYieldFromChain(cQCD, cutString = rCS_crLowNJet_Cut_1b+'&&'+dPhiStr+'<'+str(dPhiCut),weight=weight_str, returnError = True)
      yQCD_crNJet_1b_highDPhi   = getYieldFromChain(cQCD, cutString = rCS_crLowNJet_Cut_1b+'&&'+dPhiStr+'>'+str(dPhiCut),weight=weight_str, returnError = True)

      y_LowDPhi_1b = yTT_crNJet_1b_lowDPhi[0] + yW_crNJet_1b_lowDPhi[0] + yRest_crNJet_1b_lowDPhi[0] + yQCD_crNJet_1b_lowDPhi[0] - QCD_lowDPhi['y']
      y_Var_LowDPhi_1b = yTT_crNJet_1b_lowDPhi[1]**2 + yW_crNJet_1b_lowDPhi[1]**2 + yRest_crNJet_1b_lowDPhi[1]**2 + yQCD_crNJet_1b_lowDPhi[1]**2 + QCD_lowDPhi['e']**2

      y_HighDPhi_1b = yTT_crNJet_1b_highDPhi[0] + yW_crNJet_1b_highDPhi[0] + yRest_crNJet_1b_highDPhi[0] + yQCD_crNJet_1b_highDPhi[0] - QCD_highDPhi['y']
      y_Var_HighDPhi_1b = yTT_crNJet_1b_highDPhi[1]**2 + yW_crNJet_1b_highDPhi[1]**2 + yRest_crNJet_1b_highDPhi[1]**2 + yQCD_crNJet_1b_highDPhi[1]**2 + QCD_highDPhi['e']**2
      
      rCS_crLowNJet_1b = {'rCS':y_HighDPhi_1b/y_LowDPhi_1b, 'rCSE_sim':(y_HighDPhi_1b/y_LowDPhi_1b)*sqrt(y_Var_HighDPhi_1b/y_HighDPhi_1b**2+y_Var_LowDPhi_1b/y_LowDPhi_1b**2), 'rCSE_pred':(y_HighDPhi_1b/y_LowDPhi_1b)*sqrt(1./y_HighDPhi_1b+1./y_LowDPhi_1b), 'num':y_HighDPhi_1b, 'numE':sqrt(y_Var_HighDPhi_1b), 'denom':y_LowDPhi_1b, 'denomE':sqrt(y_Var_LowDPhi_1b)}
      
    else:    
      rCS_crLowNJet_1b = getRCS(cBkg, rCS_crLowNJet_Cut, dPhiCut, weight = weight_str_1b, returnValues=True)

  rCS_crLowNJet_1b_onlyTT = getRCS(cTTJets, rCS_crLowNJet_Cut,  dPhiCut, weight = weight_str_1bMC)
  rCS_srNJet_0b_onlyTT    = getRCS(cTTJets, rCS_sr_Cut,  dPhiCut, weight = weight_str_0bMC)

  rd['yTT_srNJet_0b_lowDPhi']     = yTT_srNJet_0b_lowDPhi
  rd['yTT_Var_srNJet_0b_lowDPhi'] = yTT_Var_srNJet_0b_lowDPhi
  
  rd['y_crNJet_1b_lowDPhi']       = rCS_crLowNJet_1b['denom']
  rd['y_Var_crNJet_1b_lowDPhi']   = rCS_crLowNJet_1b['denomE']**2
  rd['y_crNJet_1b_highDPhi']      = rCS_crLowNJet_1b['num']
  rd['y_Var_crNJet_1b_highDPhi']  = rCS_crLowNJet_1b['numE']**2
  
  if QCD:
    rd['yQCD_crNJet_1b_lowDPhi']      = QCD_lowDPhi['y']
    rd['yQCD_Var_crNJet_1b_lowDPhi']  = QCD_lowDPhi['e']**2
    rd['yQCD_crNJet_1b_highDPhi']     = QCD_highDPhi['y']
    rd['yQCD_Var_crNJet_1b_highDPhi'] = QCD_highDPhi['e']**2
    rd['yQCD_srNJet_0b_lowDPhi']      = QCD_dict[0]['y']
    rd['yQCD_Var_srNJet_0b_lowDPhi']  = QCD_dict[0]['e']**2
    rd['yQCD_srNJet_0b']              = QCD_dict[0]['totalY']
  
  rd['rCS_crLowNJet_1b']        = rCS_crLowNJet_1b
  rd['rCS_crLowNJet_1b_onlyTT'] = rCS_crLowNJet_1b_onlyTT
  rd['rCS_srNJet_0b_onlyTT']    = rCS_srNJet_0b_onlyTT

  #true yields measured from MC samples
  truth_TT, truth_TT_var = getYieldFromChain(cTTJets, rCS_sr_Cut+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_str_0bMC, returnVar=True)
  truth_TT_CR, truth_TT_CR_var = getYieldFromChain(cTTJets, rCS_sr_Cut+"&&"+dPhiStr+"<"+str(dPhiCut), weight = weight_str_0bMC, returnVar=True)
  rd['yTT_srNJet_0b_lowDPhi_truth'] = truth_TT_CR
  rd['yTT_Var_srNJet_0b_lowDPhi_truth'] = truth_TT_CR_var
#  truth_TT_var    = getYieldFromChain(cTTJets, rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_err_str)

  truth_QCD, truth_QCD_var = getYieldFromChain(cQCD, rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = weight_str, returnVar=True)
  truth_QCD_CR, truth_QCD_CR_var = getYieldFromChain(cQCD, rCS_sr_Cut_0b+"&&"+dPhiStr+"<"+str(dPhiCut), weight = weight_str, returnVar=True)
  rd['yQCD_srNJet_0b_lowDPhi_truth']      = truth_QCD_CR
  rd['yQCD_Var_srNJet_0b_lowDPhi_truth']  = truth_QCD_CR_var

  rd['QCD_truth']     = truth_QCD
  rd['QCD_truth_err'] = sqrt(truth_QCD_var)


  #predicted yields with RCS method
  ttJetsCRForRCS = rCS_crLowNJet_1b #New version, orthogonal to DPhi (lower njet region in 1b-tag bin)
#  kFactor = getTTcorr(stb,htb)
#  pred_TT    = yTT_srNJet_0b_lowDPhi*ttJetsCRForRCS['rCS']*kFactor['k']
#  pred_Var_TT= yTT_Var_srNJet_0b_lowDPhi*ttJetsCRForRCS['rCS']**2*kFactor['k']**2 + yTT_srNJet_0b_lowDPhi**2*ttJetsCRForRCS['rCSE_pred']**2*kFactor['k']**2 + yTT_srNJet_0b_lowDPhi**2*ttJetsCRForRCS['rCS']**2*kFactor['k_Error']**2
  pred_TT    = yTT_srNJet_0b_lowDPhi*ttJetsCRForRCS['rCS']
  pred_Var_TT= yTT_Var_srNJet_0b_lowDPhi*ttJetsCRForRCS['rCS']**2 + yTT_srNJet_0b_lowDPhi**2*ttJetsCRForRCS['rCSE_pred']**2
  pred_Var_TT_MC = yTT_Var_srNJet_0b_lowDPhi*ttJetsCRForRCS['rCS']**2 + yTT_srNJet_0b_lowDPhi**2*ttJetsCRForRCS['rCSE_sim']**2
  
  print "TT pred:",pred_TT,'+/-',sqrt(pred_Var_TT),' TT truth:',truth_TT,'+/-',sqrt(truth_TT_var)

  rd.update( {'TT_pred':pred_TT,"TT_pred_err":sqrt(pred_Var_TT),\
              "TT_truth":truth_TT,"TT_truth_err":sqrt(truth_TT_var), "TT_pred_err_MC":sqrt(pred_Var_TT_MC)})
  bins.update(rd)
  del rd
  return bins

