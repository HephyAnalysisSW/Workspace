import ROOT
import pickle

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()

from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getPropagatedError
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from rCShelpers import *
import math
from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.signalRegions import *
from array import array

from predictionConfig import *

#cData = getChain([single_mu_Run2015D, single_ele_Run2015D], histname='')
#predictionName = 'SFtemplates_fullSR_lep_data'
unblinded = False

ROOT.gStyle.SetOptTitle(0);
ROOT.gStyle.SetOptStat('')

useWcorrection  = False
useTTcorrection = False
withSystematics = True
useKappa        = True

showMCtruth     = False
signal = True
stackSignal = True
plotPull = False

#latextitle = ''
latextitle = 'Preliminary'

weight_str, weight_err_str = makeWeight(lumi, sampleLumi, reWeight=MCweight)

prefix = 'singleLeptonic_Spring15_'
#prefix = 'singleLeptonic_Spring16_'
#path = '/data/'+username+'/Results2015/Prediction_SFTemplate_MC_fullSR_lep_3.0/'
#pickleDir = '/data/easilar/Results2016/Prediction_SFtemplates_fullSR_lep_data_2p25/'
#pickleDir = '/data/dspitzbart/Results2015/Prediction_SFtemplates_validation_lep_data_2.1/'
#pickleDir = '/data/dspitzbart/Results2016/Prediction_SFtemplates_fullSR_lep_data_Moriond_2p3/'
#pickleDir = '/data/dspitzbart/Results2016/Prediction_SFtemplates_validation_4j_lep_data_2p3/'
#pickleDir = '/data/dspitzbart/Results2016/Prediction_Spring16_templates_VreducedSR_lep_data_0p8/'

#pickleDir = '/data/dspitzbart/Results2016/Prediction_Spring16_templates_validation_4j_lep_data_2p57/'
#pickleDir = '/data/dspitzbart/Results2016/Prediction_Spring16_templates_SR2015_lep_data_2p57/'

#pickleDir = '/data/dspitzbart/Results2016/Prediction_Spring16_templates_SR2016_v1_QCD_lep_MC_3p99/'
#pickleDir = '/data/dspitzbart/Results2016/Prediction_Spring16_templates_validation_4j_lep_data_3p99/'
#pickleDir = '/data/dspitzbart/Results2016/Prediction_Spring16_templates_SR2016_v1_100p_lep_data_3p99/'#resultsFinal_withSystematics_pkl
#pickleDir = '/data/dspitzbart/Results2016/Prediction_Spring16_templates_SR2016_v2_lep_data_7p62/'
#pickleDir = '/data/dspitzbart/Results2016/Prediction_Spring16_templates_validation_4j_altWSB_lep_data_12p9/'
#pickleDir = '/data/dspitzbart/Results2016/Prediction_Spring16_templates_SR2016_postApp_v2_lep_data_12p9/'
#pickleDir = '/afs/hephy.at/data/easilar01/Results2017/Prediction_Spring16_templates_SR_Moriond2017_v5_lep_data_36p5//singleLeptonic_Spring16_iso_Veto_ISRforttJets_OLDttJetsSB_addDiBoson_withSystematics_pkl'
#pickleDir = '/afs/hephy.at/data/easilar01/Results2017/Prediction_Spring16_templates_SR_Moriond2017_v5_lep_MC_SF_36p5//singleLeptonic_Spring16_iso_Veto_ISRforttJets_OLDttJetsSB_addDiBoson_MC_withSystematics_pkl'
#pickleDir = '/afs/hephy.at/data/easilar01/Results2017/Prediction_Spring16_templates_SR_Moriond2017_v8_lep_MC_SF_36p5//singleLeptonic_Spring16_iso_Veto_ISRforttJets_OLDttJetsSB_addDiBoson_MC_withSystematics_pkl'
#pickleDir = '/afs/hephy.at/data/easilar01/Results2017/Prediction_Spring16_templates_SR_Moriond2017_newTT_lep_data_36p5/singleLeptonic_Spring16_iso_Veto_ISRforttJets_NEWttJetsSB_addDiBoson_withSystematics_pkl'
#pickleDir = '/afs/hephy.at/data/easilar01/Results2017/Prediction_Spring16_templates_validation_4j_altWSB_newTT_v2_lep_data_36p5//singleLeptonic_Spring16_iso_Veto_ISRforttJets_NEWttJetsSB_addDiBoson_withSystematics_pkl'
#pickleDir = '/afs/hephy.at/data/easilar01/Results2017/Prediction_Spring16_templates_aggr_Moriond2017_v1_lep_data_36p5//singleLeptonic_Spring16_iso_Veto_ISRforttJets_NEWttJetsSB_addDiBoson_withSystematics_pkl'
#pickleDir = '/afs/hephy.at/data/easilar01/Results2017/Prediction_Spring16_templates_aggr_Moriond2017_v3_lep_MC_SF_36p5//singleLeptonic_Spring16_iso_Veto_ISRforttJets_NEWttJetsSB_addDiBoson_withSystematics_pkl'
pickleDir = '/afs/hephy.at/data/easilar01/Results2017/Prediction_Spring16_templates_SR_Moriond2017_dibosonfixed_lep_data_36p5//singleLeptonic_Spring16_iso_Veto_ISRforttJets_NEWttJetsSB_addDiBoson_withSystematics_pkl'
if not useKappa: res = pickle.load(file(pickleDir+'singleLeptonic_Spring16__estimationResults_pkl'))
else: res = pickle.load(file(pickleDir))
#else: res = pickle.load(file(pickleDir+'resultsFinal_withSystematics_pkl'))
if withSystematics:
  sys = pickle.load(file(pickleDir))

#sig = pickle.load(file('/data/easilar/Spring15/25ns/allSignals_2p3_v2_pkl'))
#sig = pickle.load(file('/data/easilar/Spring15/25ns/allSignals_2p25_allSyst_approval_pkl'))
sig2 = pickle.load(file('/afs/hephy.at/user/e/easilar/www/Moriond2017/pickles/signals/mglu1500Signal_isoVetoCorrected_pkl'))
sig1 = pickle.load(file('/afs/hephy.at/user/e/easilar/www/Moriond2017/pickles/signals/mglu1900Signal_isoVetoCorrected_pkl'))
#sig1 = pickle.load(file('/afs/hephy.at/user/e/easilar/www/Moriond2017/pickles/signals/mglu1900Signal_aggr_inc_pkl'))
#sig2 = pickle.load(file('/afs/hephy.at/user/e/easilar/www/Moriond2017/pickles/signals/mglu1500Signal_aggr_inc_pkl'))
#sig = pickle.load(file('/afs/hephy.at/data/dspitzbart01/Results2016/signals_with_unc_pkl'))

signalRegions = signalRegions_Moriond2017
#signalRegions = validationRegion
#signalRegions = validationRegion_Moriond_All
#signalRegions = aggregateRegions_Moriond2017
#signalRegions = aggregateRegions_Moriond2017_Test2


def getValErrString(val,err, precision=3):
  return str(round(val,precision))+' +/- '+str(round(err,precision))

rowsNJet = {}
rowsSt = {}
bins = 0
for srNJet in sorted(signalRegions):
  rowsNJet[srNJet] = {}
  rowsSt[srNJet] = {}
  rows = 0
  for stb in sorted(signalRegions[srNJet]):
    rows += len(signalRegions[srNJet][stb])
    rowsSt[srNJet][stb] = {'n':len(signalRegions[srNJet][stb])}
  rowsNJet[srNJet] = {'nST':len(signalRegions[srNJet]), 'n':rows}
  bins += rows

data_truth_H = ROOT.TH1F('data_truth_H','data',bins,0,bins)
data_truth_H.SetLineColor(ROOT.kBlack)
data_truth_H.SetLineWidth(2)
data_truth_H.SetMarkerColor(ROOT.kBlack)
data_truth_H.SetMarkerSize(1.3)
if isData:
  data_truth_H.SetBinErrorOption(ROOT.TH1F.kPoisson)


#benchmark1_H = ROOT.TH1F('benchmark1_H','T5qqqqWW (1.2,0.8)',bins,0,bins)
#benchmark2_H = ROOT.TH1F('benchmark2_H','T5qqqqWW (1.4,1.0)',bins,0,bins)
#benchmark3_H = ROOT.TH1F('benchmark3_H','T5qqqqWW (1.6,0.1)',bins,0,bins)

#benchmark1_H = ROOT.TH1F('benchmark1_H','T5qqqqWW (1.0,0.7)',bins,0,bins)
#benchmark2_H = ROOT.TH1F('benchmark2_H','T5qqqqWW (1.2,0.8)',bins,0,bins)
#benchmark3_H = ROOT.TH1F('benchmark3_H','T5qqqqWW (1.5,0.1)',bins,0,bins)

benchmark2_H = ROOT.TH1F('benchmark2_H','T5qqqqWW (1.9,0.1)',bins,0,bins)
benchmark3_H = ROOT.TH1F('benchmark3_H','T5qqqqWW (1.5,1.0)',bins,0,bins)

#benchmark1_H.SetLineColor(ROOT.kSpring+10)
benchmark2_H.SetLineColor(ROOT.kMagenta+2)
benchmark3_H.SetLineColor(ROOT.kRed+1)

#benchmark1_H.SetLineWidth(3)
benchmark2_H.SetLineWidth(3)
benchmark3_H.SetLineWidth(3)

#benchmark1_H.SetMarkerSize(0)
benchmark2_H.SetMarkerSize(0)
benchmark3_H.SetMarkerSize(0)

tt_pred_H  = ROOT.TH1F('tt_pred_H','t#bar{t} + jets',bins,0,bins)
tt_truth_H = ROOT.TH1F('tt_truth_H','tt+Jets truth',bins,0,bins)
tt_pred_H.SetLineColor(color('ttJets')-2)
tt_pred_H.SetFillColorAlpha(color('ttJets')-2,0.8)
tt_pred_H.SetLineWidth(2)
tt_truth_H.SetLineColor(color('ttJets')-1)
tt_truth_H.SetLineWidth(2)

w_pred_H  = ROOT.TH1F('w_pred_H','W + jets', bins,0,bins)
w_truth_H = ROOT.TH1F('w_truth_H','W + jets truth', bins,0,bins)
w_pred_H.SetLineColor(color('wJets'))
w_pred_H.SetFillColorAlpha(color('wJets'),0.8)
w_pred_H.SetLineWidth(2)
w_truth_H.SetLineColor(color('wJets')-1)
w_truth_H.SetLineWidth(2)

rest_H = ROOT.TH1F('rest_H','Other', bins,0,bins)
rest_H.SetLineColor(color('TTVH'))
rest_H.SetFillColorAlpha(color('TTVH'), 0.8)
rest_H.SetLineWidth(2)
w_truth_H.SetLineColor(color('DY'))

pred_H  = ROOT.TH1F('pred_H','Total', bins,0,bins)
#pred_H.SetBarWidth(0.4)
#pred_H.SetBarOffset(0.1)
truth_H = ROOT.TH1F('truth_H','Total MC truth',bins,0,bins)
if isData:
  truth_H.SetBinErrorOption(ROOT.TH1F.kPoisson)


pred_H.SetLineColor(ROOT.kGray+1)
pred_H.SetMarkerStyle(0)
pred_H.SetMarkerSize(0)
pred_H.SetLineWidth(3)

truth_H.SetLineColor(ROOT.kBlack)
truth_H.SetLineWidth(2)
truth_H.SetMarkerStyle(8)
truth_H.SetMarkerColor(ROOT.kBlack)

kappa_tt = ROOT.TH1F('kappa_tt','kappa', bins,0,bins)
kappa_tt.SetLineWidth(1)
kappa_tt.SetMarkerStyle(21)
kappa_tt.SetMarkerSize(1.5)
kappa_tt.SetMarkerColor(color('ttjets'))
kappa_tt.SetLineColor(color('ttjets'))

kappa_W = ROOT.TH1F('kappa_W','kappa', bins,0,bins)
kappa_W.SetLineWidth(1)
kappa_W.SetMarkerStyle(22)
kappa_W.SetMarkerSize(1.5)
kappa_W.SetMarkerColor(color('wjets'))
kappa_W.SetLineColor(color('wjets'))

kappa_global = ROOT.TH1F('kappa_global','kappa', bins,0,bins)
kappa_global.SetLineWidth(2)
kappa_global.SetMarkerStyle(20)
kappa_global.SetMarkerSize(0)
kappa_global.SetMarkerColor(ROOT.kBlack)
kappa_global.SetLineColor(ROOT.kBlack)

pull = ROOT.TH1F('pull','pull', bins,0,bins)
pull.SetLineWidth(2)
pull.SetMarkerStyle(24)
pull.SetMarkerSize(1)
pull.SetMarkerColor(ROOT.kBlue)
pull.SetLineColor(ROOT.kBlack)


one = ROOT.TH1F('one','one', bins,0,bins)
one.SetLineWidth(1)

zero = ROOT.TH1F('zero','zero', bins,0,bins)
zero.SetLineWidth(1)


drawOption = 'hist ][ e0'
drawOptionSame = drawOption + 'same'

predXErr = []
predYErr = []
predX = []
predY = []

predRelYErr = []
predRelY = []

ratioXErr = []
ratioYUp = []
ratioYDown = []
ratioX = []
ratioY = []

dataPXErr = []
dataPX = []
dataPY = []
dataPYUp = []
dataPYDown = []

kappaPYErr = []
kappaPXErr = []
kappaPX = []
kappaPY = []

total_meas      = 0
total_yield     = 0
total_err       = 0
total_stat_var  = 0

fmt = '{0:30} {1:>6}'
fmt2 = '{0:10}{1:>20}'

ratioWithE = []


i=1
for srNJet in sorted(signalRegions):
  for stb in sorted(signalRegions[srNJet]):
    for htb in sorted(signalRegions[srNJet][stb]):
      print
      print 'SR'+str(i)
      if useKappa:
        #calculate final tt yields and errors
        if not (math.isnan(res[srNJet][stb][htb]['TT_kappa']) and math.isnan(res[srNJet][stb][htb]['TT_kappa_err'])) :
          kappa_tt.SetBinContent(i, res[srNJet][stb][htb]['TT_kappa'])
          kappa_tt.SetBinError(i, res[srNJet][stb][htb]['TT_kappa_err'])
        else : 
          kappa_tt.SetBinContent(i, 1.)
          kappa_tt.SetBinError(i, 0.5)
          
        print fmt.format('tt w/o kappa, syst:', getValErrString(res[srNJet][stb][htb]['TT_pred'], res[srNJet][stb][htb]['TT_pred_err']))
        print fmt.format('tt with kappa, syst:',getValErrString(res[srNJet][stb][htb]['TT_pred_final'], res[srNJet][stb][htb]['TT_pred_final_tot_err']))

        #calculate final W yields and errors
        kappa_W.SetBinContent(i,res[srNJet][stb][htb]['W_kappa'])
        kappa_W.SetBinError(i, res[srNJet][stb][htb]['W_kappa_err'])

        #calculate final W yields and errors
        kappa_global.SetBinContent(i,res[srNJet][stb][htb]['tot_kappa'])
        kappa_global.SetBinError(i, res[srNJet][stb][htb]['tot_kappa_err'])

        print fmt.format('W w/o kappa, syst:', getValErrString(res[srNJet][stb][htb]['W_pred'], res[srNJet][stb][htb]['W_pred_err']))
        print fmt.format('W with kappa, syst:',getValErrString(res[srNJet][stb][htb]['W_pred_final'], res[srNJet][stb][htb]['W_pred_final_tot_err']))
        
        #calculate final rest yields and errors
        print fmt.format('rest w/o syst:', getValErrString(res[srNJet][stb][htb]['Rest_truth'], res[srNJet][stb][htb]['Rest_truth_err']))
        print fmt.format('rest with syst:', getValErrString(res[srNJet][stb][htb]['Rest_truth'], res[srNJet][stb][htb]['Rest_truth_final_tot_err']))

        print fmt.format('total MC', getValErrString(res[srNJet][stb][htb]['tot_truth'],res[srNJet][stb][htb]['tot_truth_err']))
        print fmt.format('- total pred w/o kappa, syst:', getValErrString(res[srNJet][stb][htb]['tot_pred'], res[srNJet][stb][htb]['tot_pred_err']))
        print fmt.format('- total pred with kappa, syst:', getValErrString(res[srNJet][stb][htb]['tot_pred_final'], res[srNJet][stb][htb]['tot_pred_final_tot_err']))
        
        
        if not (math.isnan(res[srNJet][stb][htb]['TT_pred_final'])) :
          tt_pred_H.SetBinContent(i, res[srNJet][stb][htb]['TT_pred_final'])
          tt_pred_H.SetBinError(i,   res[srNJet][stb][htb]['TT_pred_final_tot_err'])
        else:
          tt_pred_H.SetBinContent(i, res[srNJet][stb][htb]['TT_pred'])
          tt_pred_H.SetBinError(i, res[srNJet][stb][htb]['TT_pred_err'])

        w_pred_H.SetBinContent(i, res[srNJet][stb][htb]['W_pred_final'])
        w_pred_H.SetBinError(i,   res[srNJet][stb][htb]['W_pred_final_tot_err'])
        if not (math.isnan(res[srNJet][stb][htb]['TT_pred_final'])) :
          pred_H.SetBinContent(i, res[srNJet][stb][htb]['tot_pred_final'])
          pred_H.SetBinError(i,   res[srNJet][stb][htb]['tot_pred_final_tot_err'])
        else:
          pred_H.SetBinContent(i, res[srNJet][stb][htb]['tot_pred'])
          pred_H.SetBinError(i,   res[srNJet][stb][htb]['tot_pred_err'])
           
        predYErr.append(res[srNJet][stb][htb]['tot_pred_final_tot_err'])
        predRelYErr.append(res[srNJet][stb][htb]['tot_pred_final_tot_err']/res[srNJet][stb][htb]['tot_pred_final'])
        predY.append(res[srNJet][stb][htb]['tot_pred_final'])
        
      else:
        tt_pred_H.SetBinContent(i, res[srNJet][stb][htb]['TT_pred'])
        tt_pred_H.SetBinError(i,   res[srNJet][stb][htb]['TT_pred_err'])

        w_pred_H.SetBinContent(i, res[srNJet][stb][htb]['W_pred'])
        w_pred_H.SetBinError(i,   res[srNJet][stb][htb]['W_pred_err'])
        
        pred_H.SetBinContent(i, res[srNJet][stb][htb]['tot_pred'])
        pred_H.SetBinError(i,   res[srNJet][stb][htb]['tot_pred_err'])
        
        predYErr.append(res[srNJet][stb][htb]['tot_pred_err'])
        predRelYErr.append(res[srNJet][stb][htb]['tot_pred_err']/res[srNJet][stb][htb]['tot_pred'])
        predY.append(res[srNJet][stb][htb]['tot_pred'])
      
      tt_truth_H.SetBinContent(i,res[srNJet][stb][htb]['TT_truth'])
      tt_truth_H.SetBinError(i,  res[srNJet][stb][htb]['TT_truth_err'])

      w_truth_H.SetBinContent(i,res[srNJet][stb][htb]['W_truth'])
      w_truth_H.SetBinError(i,  res[srNJet][stb][htb]['W_truth_err'])

      rest_H.SetBinContent(i, res[srNJet][stb][htb]['Rest_truth'])
      rest_H.SetBinError(i,   res[srNJet][stb][htb]['Rest_truth_err'])

      one.SetBinContent(i,1)
      zero.SetBinContent(i,0)
      
      # set values to the uncertainty bands
      predXErr.append(0.5)
      predX.append(i-0.5)
      predRelY.append(1)
      
      if unblinded or validation:
        if isData:
          weight = 'weight'
          dcn, dc = nameAndCut(stb, htb, srNJet, (0,0), presel+'&&deltaPhi_Wl>'+str(signalRegions[srNJet][stb][htb]['deltaPhi']))
        else:
          weight =weight_str+'*weightBTag0_SF'
          dcn, dc = nameAndCut(stb, htb, srNJet, (0,-1), presel+'&&deltaPhi_Wl>'+str(signalRegions[srNJet][stb][htb]['deltaPhi']))
        #data_yield = getYieldFromChain(cData, dc,weight)
        data_yield = res[srNJet][stb][htb]['y_srNJet_0b_highDPhi']
        data_truth_H.SetBinContent(i,data_yield)
        data_truth_H.GetBinErrorLow(i)
        data_truth_H.GetBinErrorUp(i)
        print fmt.format('- Measured: ', getValErrString(data_yield, sqrt(data_yield)))
        truth_H.SetBinContent(i,data_yield)

        #get asymmetric errors for observation, ratio etc
        #truth_H.GetXaxis().SetBinLabel(i, str(i))
        truthLowE = truth_H.GetBinErrorLow(i)
        truthUpE = truth_H.GetBinErrorUp(i)
        if plotPull:
          if data_yield>0: pull.SetBinContent(i, (data_yield-res[srNJet][stb][htb]['tot_pred_final'])/sqrt(res[srNJet][stb][htb]['tot_pred_final_tot_err']**2+(0.5*(truthLowE+truthUpE))**2))
          else: pull.SetBinContent(i, (data_yield-res[srNJet][stb][htb]['tot_pred_final'])/sqrt(res[srNJet][stb][htb]['tot_pred_final_tot_err']**2+truthUpE**2))
          pull.SetBinError(i, 1)
        #ratioUp = getPropagatedError(truth_H.GetBinContent(i), truthUpE, res[srNJet][stb][htb]['tot_pred_final'], res[srNJet][stb][htb]['tot_pred_final_err'], returnCalcResult=True)
        #ratioLow = getPropagatedError(truth_H.GetBinContent(i), truthLowE, res[srNJet][stb][htb]['tot_pred_final'], res[srNJet][stb][htb]['tot_pred_final_err'], returnCalcResult=True)
        if useKappa: total_pred = res[srNJet][stb][htb]['tot_pred_final']
        else: total_pred = res[srNJet][stb][htb]['tot_pred']
        ratioUp = getPropagatedError(truth_H.GetBinContent(i), truthUpE, total_pred, 0, returnCalcResult=True)
        ratioLow = getPropagatedError(truth_H.GetBinContent(i), truthLowE, total_pred, 0, returnCalcResult=True)
        if not truth_H.GetBinContent(i)>0:
          ratioErrUp = truthUpE/total_pred
          ratioErrLow = 0
          ratioVal = 0
        else:
          ratioErrUp = ratioUp[1]
          ratioErrLow = ratioLow[1]
          ratioVal = ratioUp[0]
        ratioWithE.append({'v': ratioVal,'up': ratioErrUp, 'down': ratioErrLow})

        ratio_str = str(round(ratioVal,3))+' + ' +str(round(ratioErrUp,3)) + ' - ' + str(round(ratioErrLow,3))
        print fmt2.format('ratio:',ratio_str)
        
        ratioX.append(i-0.5)
        ratioY.append(ratioVal)
        ratioXErr.append(0)
        ratioYUp.append(ratioErrUp)
        ratioYDown.append(ratioErrLow)
        
        dataPX.append(i-0.5)
        dataPY.append(truth_H.GetBinContent(i))
        dataPXErr.append(0)
        dataPYUp.append(truthUpE)
        dataPYDown.append(truthLowE)

        if useKappa:
          kappaPX.append(i-0.5)
          kappaPY.append(res[srNJet][stb][htb]['tot_kappa'])
          kappaPXErr.append(0.5)
          kappaPYErr.append(res[srNJet][stb][htb]['tot_kappa_err'])


      else:
        truth_H.SetBinContent(i,res[srNJet][stb][htb]['tot_truth'])
        truth_H.SetBinError(i,  res[srNJet][stb][htb]['tot_truth_err'])
        truth_H.GetXaxis().SetBinLabel(i, str(i))
        
        ratioX.append(i-0.5)
        ratioY.append(1)
        ratioXErr.append(0)
        ratioYUp.append(0.)
        ratioYDown.append(0.)

        dataPX.append(i-0.5)
        dataPY.append(1)
        dataPXErr.append(0)
        dataPYUp.append(0)
        dataPYDown.append(0)
        
        if useKappa:
          kappaPX.append(i-0.5)
          kappaPY.append(res[srNJet][stb][htb]['tot_kappa'])
          kappaPXErr.append(0.5)
          kappaPYErr.append(res[srNJet][stb][htb]['tot_kappa_err'])

      if signal:
        if stackSignal:
          #benchmark1_H.SetBinContent(i,res[srNJet][stb][htb]['tot_pred_final']+sig[srNJet][stb][htb]['signals'][1200][800]['mod_yield_MB_SR'])
          #benchmark2_H.SetBinContent(i,res[srNJet][stb][htb]['tot_pred_final']+sig[srNJet][stb][htb]['signals'][1400][1000]['mod_yield_MB_SR'])
          #benchmark3_H.SetBinContent(i,res[srNJet][stb][htb]['tot_pred_final']+sig[srNJet][stb][htb]['signals'][1600][100]['mod_yield_MB_SR'])
          #benchmark1_H.SetBinContent(i,res[srNJet][stb][htb]['tot_pred_final']+sig[srNJet][stb][htb]['signals'][1000][700]['yield_MB_SR'])
          #benchmark2_H.SetBinContent(i,res[srNJet][stb][htb]['tot_pred_final']+sig1[srNJet][stb][htb]['signals'][1900][100]['yield_MB_SR'])
          #benchmark3_H.SetBinContent(i,res[srNJet][stb][htb]['tot_pred_final']+sig2[srNJet][stb][htb]['signals'][1500][1000]['yield_MB_SR'])
          benchmark2_H.SetBinContent(i,res[srNJet][stb][htb]['tot_pred_final']+sig1[srNJet][stb][htb]['signals'][1900][100]['yield_MB_SR'])
          benchmark3_H.SetBinContent(i,res[srNJet][stb][htb]['tot_pred_final']+sig2[srNJet][stb][htb]['signals'][1500][1000]['yield_MB_SR'])
        else:
          #benchmark1_H.SetBinContent(i,sig[srNJet][stb][htb]['signals'][1200][800]['mod_yield_MB_SR'])
          #benchmark2_H.SetBinContent(i,sig[srNJet][stb][htb]['signals'][1400][1000]['mod_yield_MB_SR'])
          #benchmark3_H.SetBinContent(i,sig[srNJet][stb][htb]['signals'][1600][100]['mod_yield_MB_SR'])
          #benchmark1_H.SetBinContent(i,sig[srNJet][stb][htb]['signals'][1000][700]['yield_MB_SR'])
          benchmark2_H.SetBinContent(i,sig1[srNJet][stb][htb]['signals'][1900][100]['yield_MB_SR'])
          benchmark3_H.SetBinContent(i,sig2[srNJet][stb][htb]['signals'][1500][1000]['yield_MB_SR'])
      if unblinded:
        total_meas     += data_yield
        if useKappa:
          total_yield     += res[srNJet][stb][htb]['tot_pred_final']
          total_err       += res[srNJet][stb][htb]['tot_pred_final_tot_err']
          #total_err       += res[srNJet][stb][htb]['systematics']['total']*res[srNJet][stb][htb]['tot_pred_final']
          total_stat_var  += res[srNJet][stb][htb]['tot_pred_final_err']**2
        else:
          total_yield     += res[srNJet][stb][htb]['tot_pred']
          total_err       += res[srNJet][stb][htb]['tot_pred_err']
          total_stat_var  += res[srNJet][stb][htb]['tot_pred_err']**2

      pred_H.GetXaxis().SetBinLabel(i,'#splitline{'+signalRegions[srNJet][stb][htb]['njet']+'}{#splitline{'+signalRegions[srNJet][stb][htb]['LT']+'}{'+signalRegions[srNJet][stb][htb]['HT']+'}}')
      i+=1


if unblinded:
  print
  print
  print 'Sum over all SRs:'
  print fmt.format('- Predicted: ', getValErrString(total_yield, sqrt(total_err**2+total_stat_var)))
  print fmt.format('- Measured: ', getValErrString(total_meas, sqrt(total_meas)))

print
print
#pred error
ax = array('d',predX)
ay = array('d',predY)
aexh = array('d',predXErr)
aexl = array('d',predXErr)
aeyh = array('d',predYErr)
aeyl = array('d',predYErr)

if useKappa:
  #pred error
  kx = array('d',kappaPX)
  ky = array('d',kappaPY)
  kex = array('d',kappaPXErr)
  key = array('d',kappaPYErr)

#pred rel error for ratio plot
a_r_eyh = array('d',predRelYErr)
a_r_eyl = array('d',predRelYErr)
a_r_y = array('d',predRelY)

#ratio errors
rx    = array('d',ratioX)
ry    = array('d',ratioY)
rexh  = array('d',ratioXErr)
rexl  = array('d',ratioXErr)
reyh  = array('d',ratioYUp)
reyl  = array('d',ratioYDown)

#data points
dx    = array('d',dataPX)
dy    = array('d',dataPY)
dexh  = array('d',dataPXErr)
dexl  = array('d',dataPXErr)
deyh  = array('d',dataPYUp)
deyl  = array('d',dataPYDown)

can = ROOT.TCanvas('can','can',1000,500)

pad1=ROOT.TPad("pad1","MyTitle",0.,0.3,1.,1.)
pad1.SetLeftMargin(0.1)
pad1.SetBottomMargin(0.02)
pad1.Draw()
pad1.cd()

h_Stack = ROOT.THStack('h_Stack','Stack')
h_Stack.Add(rest_H)
h_Stack.Add(w_pred_H)
h_Stack.Add(tt_pred_H)
if validation:
  h_Stack.SetMaximum(800)
  h_Stack.SetMinimum(0.70)
else:
  h_Stack.SetMaximum(1000)
  #h_Stack.SetMaximum(1000)
  h_Stack.SetMinimum(0.080)
  #h_Stack.SetMinimum(0.20)

#h_Stack.GetYaxis().SetTitle('Signal Region #')

truth_H.SetMaximum(20)
truth_H.GetYaxis().SetTitle('Events')
truth_H.GetXaxis().SetTitle('Signal Region #')
truth_H.GetYaxis().SetTitleSize(0.06)
truth_H.GetYaxis().SetLabelSize(0.06)

data_err = ROOT.TGraphAsymmErrors(bins, dx, dy, dexl, dexh, deyl, deyh)
data_err.SetMarkerStyle(10)
data_err.SetMarkerSize(1)
data_err.SetLineWidth(2)

pred_err = ROOT.TGraphAsymmErrors(bins, ax, ay, aexl, aexh, aeyl, aeyh)
pred_err.SetFillColor(ROOT.kGray+1)
pred_err.SetFillStyle(3444)
pred_err.SetLineWidth(3)
pred_err.SetLineColor(ROOT.kGray+1)
pred_err.SetMarkerColor(ROOT.kGray+1)
pred_err.SetMarkerStyle(0)
pred_err.SetMarkerSize(0)

if useKappa:
  kappa_err = ROOT.TGraphAsymmErrors(bins, kx, ky, kex, kex, key, key)
  kappa_err.SetFillColor(ROOT.kGray+1)
  kappa_err.SetFillStyle(3444)

leg = ROOT.TLegend(0.62,0.65,0.98,0.95)
leg.SetFillColor(ROOT.kWhite)
leg.SetShadowColor(ROOT.kWhite)
leg.SetBorderSize(1)
leg.SetTextSize(0.045)
#leg.AddEntry(None,'bla','')
if isData:
  if unblinded or validation:
    leg.AddEntry(data_err, 'Data', 'ep')
  else:
    leg.AddEntry(truth_H, 'MC truth')
else:
  if showMCtruth:
    leg.AddEntry(truth_H, 'MC truth')
#leg.AddEntry(pred_H,'','l')
leg.AddEntry(pred_err,'Pred. + uncertainty')
leg.AddEntry(tt_pred_H,'','f')
leg.AddEntry(w_pred_H,'','f')
leg.AddEntry(rest_H,'','f')
#leg.AddEntry(pred_err,'Pred. uncertainty')

h_Stack.Draw('hist')
h_Stack.GetYaxis().SetTitle('Events')
h_Stack.GetXaxis().SetBinLabel(1,'')

if signal:
  #benchmark1_H.Draw('hist same')
  benchmark2_H.Draw('hist same')
  benchmark3_H.Draw('hist same')

  leg3 = ROOT.TLegend(0.25,0.75,0.55,0.925)
  leg3.SetFillColor(ROOT.kWhite)
  leg3.SetShadowColor(ROOT.kWhite)
  leg3.SetBorderSize(0)
  leg3.SetTextSize(0.04)
  #leg3.AddEntry(benchmark1_H)
  leg3.AddEntry(benchmark2_H)
  leg3.AddEntry(benchmark3_H)
  leg3.Draw()


h_Stack.GetYaxis().SetTitleOffset(0.8)
h_Stack.GetYaxis().SetNdivisions(508)
pred_err.Draw('2 same')
truth_H.SetMarkerStyle(22)

pred_rel_err = ROOT.TGraphAsymmErrors(bins, ax, a_r_y, aexl, aexh, a_r_eyl, a_r_eyh)
pred_rel_err.SetFillColor(ROOT.kGray+1)
pred_rel_err.SetFillStyle(3444)
#pred_err.Draw('2 same')

ratio_err = ROOT.TGraphAsymmErrors(bins, rx, ry, rexl, rexh, reyl, reyh)
ratio_err.SetMarkerStyle(10)
ratio_err.SetMarkerSize(1.1)
ratio_err.SetLineWidth(2)

pred_H.Draw('hist same')


if unblinded or validation:
  truth_H.SetMarkerStyle(20)
  #truth_H.Draw('e0p same')
  data_err.Draw("P0 same")
else:
  truth_H.Draw('hist e same')

leg.Draw()

latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.04)
latex1.SetTextAlign(11)

latex1.DrawLatex(0.1,0.96,'CMS #bf{#it{'+latextitle+'}}')
latex1.DrawLatex(0.9,0.96,'#bf{'+printlumi+" fb^{-1} (13 TeV)}")

pad1.SetLogy()

can.cd()


pad2=ROOT.TPad("pad2","datavsMC",0.,0.,1.,.3)
pad2.SetLeftMargin(0.1)
pad2.SetBottomMargin(0.3)
pad2.SetTopMargin(0.02)
#pad2.SetGrid()
pad2.Draw()
pad2.cd()

if plotPull:
  pull.GetXaxis().SetTitleSize(0.13)
  pull.GetXaxis().SetLabelSize(0.09)
  pull.GetXaxis().SetNdivisions(508)
  pull.GetYaxis().SetTitleSize(0.13)
  pull.GetYaxis().SetLabelSize(0.13)
  pull.GetYaxis().SetTitleOffset(0.4)
  pull.GetYaxis().SetNdivisions(506)
  pull.GetYaxis().SetTitle('Pull')
  pull.SetMinimum(-4.)
  pull.SetMaximum(4.)
  setNiceBinLabel(pull, signalRegions)
  pull.Draw('p')
  zero.Draw('hist same')
  
  
else:
  print "at ratio"
  ratio2 = ROOT.TH1F('ratio_d','ratio pred/data',bins,0,bins)
  #ratio2.Sumw2()
  ratio2 = truth_H.Clone()
  ratio2.Divide(pred_H)
  ratio2.SetLineColor(ROOT.kBlack)
  ratio2.SetMarkerStyle(8)
  ratio2.SetMarkerSize(0)
  ratio2.SetLineWidth(0)
  ratio2.SetLineColor(ROOT.kWhite)
  ratio2.GetXaxis().SetTitle('')
  
  setNiceBinLabel(ratio2, signalRegions)
  
  ratio2.GetXaxis().SetTitleSize(0.13)
  ratio2.GetXaxis().SetLabelSize(0.11)
  ratio2.GetXaxis().SetNdivisions(508)
  ratio2.GetXaxis().SetLabelOffset(0.02)
  ratio2.GetYaxis().SetTitleSize(0.13)
  ratio2.GetYaxis().SetLabelSize(0.13)
  ratio2.GetYaxis().SetTitleOffset(0.4)
  ratio2.GetYaxis().SetNdivisions(506)

  #maxRatio = 1.95
  maxRatio = 2.2
  forceMaxRatioValue = False
  if ratio2.GetBinContent(ratio2.GetMaximumBin())>maxRatio and not forceMaxRatioValue: maxRatio = ratio2.GetBinContent(ratio2.GetMaximumBin())+0.2
  ratio2.SetMinimum(0.)
  ratio2.SetMaximum(maxRatio)
    
  if validation or unblinded:
    #ratio2.GetYaxis().SetTitle('#frac{Data}{Prediction}')
    ratio2.GetYaxis().SetTitle('Data/Pred.')
  else:
    ratio2.GetYaxis().SetTitle('MC/pred.')
  ratio2.Draw('p')
  #one.Draw('hist same')
  pred_rel_err.Draw('e2 same')
  ratio_err.Draw("P0 same")
  one.Draw('hist same')


can.cd()

if not unblinded:
  suffix = '_blind'
else:
  suffix = ''

if plotPull: suffix += '_pull'
if not stackSignal: suffix += '_overlaySignal'

can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2017/sumPlot/Prediction_'+predictionName+'_'+lumistr+suffix+'.png')
can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2017/sumPlot/Prediction_'+predictionName+'_'+lumistr+suffix+'.root')
can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2017/sumPlot/Prediction_'+predictionName+'_'+lumistr+suffix+'.pdf')

if useKappa:
  
  can2 = ROOT.TCanvas('can2','can2',1000,500)
  one.SetLineStyle(2)
  one.SetLineWidth(2)
  one.SetMaximum(3.65)
  one.SetMinimum(0.)
  kappa_global.SetMaximum(3.65)
  kappa_global.SetMinimum(0.)
  
  leg2 = ROOT.TLegend(0.75,0.8,0.98,0.95)
  leg2.SetFillColor(ROOT.kWhite)
  leg2.SetShadowColor(ROOT.kWhite)
  leg2.SetBorderSize(1)
  leg2.SetTextSize(0.04)
  leg2.AddEntry(kappa_tt,'t#bar{t}+jets')
  leg2.AddEntry(kappa_W,'W+jets')
  leg2.AddEntry(kappa_global,'total')
  
  setNiceBinLabel(kappa_global, signalRegions)
  kappa_global.GetYaxis().SetTitle('#kappa')
  kappa_global.GetXaxis().SetLabelSize(0.027)
  
  latex2 = ROOT.TLatex()
  latex2.SetNDC()
  latex2.SetTextSize(0.04)
  latex2.SetTextAlign(11)
  
  kappa_global.Draw('hist')
  kappa_err.Draw("2 same")
  kappa_global.Draw('hist same')
  one.Draw('hist same')
  kappa_tt.Draw('e1p same')
  kappa_W.Draw('e1p same')
  
  leg2.Draw()
  
  latex2.DrawLatex(0.16,0.96,'CMS #bf{#it{'+latextitle+'}}')
  latex2.DrawLatex(0.88,0.96,"#bf{MC (13TeV)}")
  
  can2.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2017/sumPlot/'+predictionName+'_Kappa.png')
  can2.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2017/sumPlot/'+predictionName+'_Kappa.root')
  can2.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2017/sumPlot/'+predictionName+'_Kappa.pdf')
  
