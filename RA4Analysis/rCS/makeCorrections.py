import ROOT
import pickle
import os,sys,math
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v9_Phys14V3_HT400ST200_ForTTJetsUnc import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_Spring15_hard import *
from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed import *
#from makeTTPrediction import makeTTPrediction
#from makeWPrediction import makeWPrediction
from Workspace.HEPHYPythonTools.user import username
from binnedNBTagsFit import binnedNBTagsFit
from rCShelpers import *
from math import pi, sqrt
from Workspace.RA4Analysis.signalRegions import *

ROOT.TH1F().SetDefaultSumw2()

lepSel = 'hard'

cWJets  = getChain(WJetsHTToLNu_25ns,histname='')
cTTJets = getChain(TTJets_LO_25ns,histname='')
cEWK = getChain([WJetsHTToLNu_25ns,TTJets_LO_25ns,DY_25ns,singleTop_25ns],histname='')

#cBkg = getChain([WJetsHTToLNu[lepSel], ttJets[lepSel], DY[lepSel], singleTop[lepSel], TTVH[lepSel]],histname='')#no QCD
#cData = getChain([WJetsHTToLNu[lepSel], ttJets[lepSel], DY[lepSel], singleTop[lepSel], TTVH[lepSel]] , histname='')
#cData = getChain([WJetsHTToLNu[lepSel], ttJets[lepSel], DY[lepSel], singleTop[lepSel], TTVH[lepSel]],  ttJets[lepSel] , histname='')#no QCD , ##to calculate signal contamination
#cData = cBkg

signalRegions = signalRegion3fb

small = False
if small: signalRegions = smallRegion

#DEFINE LUMI AND PLOTDIR
lumi = 3.
printDir = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Spring15/25ns/templateFit/'
pickleDir = '/data/'+username+'/Spring15/25ns/NORMALIZATIONTEST_rCS_0b_'+str(lumi)+'/'

if not os.path.exists(pickleDir):
  os.makedirs(pickleDir)
if not os.path.exists(printDir):
  os.makedirs(printDir)

weight_str, weight_err_str = makeWeight(lumi, sampleLumi=3.)


prefix = 'singleLeptonic_Spring15_'
presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&Jet_pt[1]>80"
btagString = 'nBJetMediumCSV30'

wJetBins = [(3,4),(5,5),(6,7),(8,-1)]
ttJetBins = [(4,4),(5,5),(6,7),(8,-1)]

bins = {}

def divideRCSdict(a,b):
  kappa = a['rCS']/b['rCS']
  kappaErrorPred = (a['rCS']/b['rCS'])*sqrt(a['rCSE_pred']**2/a['rCS']**2+b['rCSE_pred']**2/b['rCS']**2)
  kappaErrorSim = (a['rCS']/b['rCS'])*sqrt(a['rCSE_sim']**2/a['rCS']**2+b['rCSE_sim']**2/b['rCS']**2)
  return {'kappa':kappa, 'kappaE_pred':kappaErrorPred, 'kappaE_sim':kappaErrorSim}

def printFloatInTableCell(a, cellWidth=20):
  print '>>%-'+str(cellWidth)+'s<<' %(str(a))

res = pickle.load(file(pickleDir+prefix+'_estimationResults_pkl'))

scoreExp=0.
scoreStat=0.
total=0.

for i_njb, njb in enumerate(signalRegions):
  bins[njb] = {}
  for stb in signalRegions[njb]:
    bins[njb][stb] ={}
    for htb in signalRegions[njb][stb]:
      print
      print '#############################################'
      print 'bin: \t njet \t\t LT \t\t HT'
      if len(str(njb))<7:
        print '\t',njb,'\t\t',stb,'\t',htb
      else:
        print '\t',njb,'\t',stb,'\t',htb
      print '#############################################'
      print
      dPhiCut = signalRegions[njb][stb][htb]['deltaPhi']
      #wJetRcsFitH = ROOT.TH1F("wJetRcsFitH","",len(wJetBins),0,len(wJetBins))
      ttJetRcsFitH = ROOT.TH1F("ttJetRcsFitH","",len(ttJetBins),0,len(ttJetBins))
      ttJetRcsFitH1b = ROOT.TH1F("ttJetRcsFitH1b","",len(ttJetBins),0,len(ttJetBins))
      
      #ttJets corrections
      cname1bCRtt, cut1bCRtt = nameAndCut(stb,htb,(4,5), btb=(1,1) ,presel=presel)
      cname0bCRtt, cut0bCRtt = nameAndCut(stb,htb,(4,5), btb=(0,0) ,presel=presel)
      rcs1bCRtt = getRCS(cEWK, cut1bCRtt, dPhiCut)
      rcs0bCRtt = getRCS(cTTJets, cut0bCRtt, dPhiCut)
      #Kappa now calculated only in the SB bin (4,5) jets 1b allEWK MC vs 0b tt MC - no fit applied for the moment!
      kappaTT = divideRCSdict(rcs0bCRtt,rcs1bCRtt)
      
      #fill histograms
      for i_njbTT, njbTT in enumerate(ttJetBins):
        cname, cut = nameAndCut(stb,htb,njbTT, btb=(0,0) ,presel=presel)
        cname1b, cut1b = nameAndCut(stb,htb,njbTT, btb=(1,1) ,presel=presel)
        rcsD = getRCS(cTTJets, cut, dPhiCut)
        rcsD1b = getRCS(cTTJets, cut1b, dPhiCut)
        #rcs = rcsD['rCS']
        #rcsErrPred = rcsD['rCSE_pred']
        #rcsErr = rcsD['rCSE_sim']
        if not math.isnan(rcsD['rCS']):
          ttJetRcsFitH.SetBinContent(i_njbTT+1, rcsD['rCS'])
          ttJetRcsFitH.SetBinError(i_njbTT+1, rcsD['rCSE_sim'])
        if not math.isnan(rcsD1b['rCS']):
          ttJetRcsFitH1b.SetBinContent(i_njbTT+1, rcsD1b['rCS'])
          ttJetRcsFitH1b.SetBinError(i_njbTT+1, rcsD1b['rCSE_sim'])
      print
      print 'Linear Fit for tt Jets Rcs values in 0b MC'
      #linear fit in 0b
      ttJetRcsFitH.Fit('pol1','','same',0,3)
      FitFunc     = ttJetRcsFitH.GetFunction('pol1')
      ttD  = FitFunc.GetParameter(0)
      ttDE = FitFunc.GetParError(0)
      ttK  = FitFunc.GetParameter(1)
      ttKE = FitFunc.GetParError(1)
      #print ttD, ttK
      
      #konstant fit in 0b and 1b
      print
      print 'Konstant Fit for tt Jets Rcs values in 0b MC'
      ttJetRcsFitH.Fit('pol0','','same',0,3)
      FitFunc     = ttJetRcsFitH.GetFunction('pol0')
      ttConst0  = FitFunc.GetParameter(0)
      ttConst0E = FitFunc.GetParError(0)
      print
      print 'Konstant Fit for tt Jets Rcs values in 1b MC'
      ttJetRcsFitH1b.Fit('pol0','','same',0,3)
      FitFunc     = ttJetRcsFitH1b.GetFunction('pol0')
      ttConst1  = FitFunc.GetParameter(0)
      ttConst1E = FitFunc.GetParError(0)
      kappaTTfit = ttConst0/ttConst1
      kappaTTfitErr = kappaTTfit*sqrt(ttConst1E**2/ttConst1**2+ttConst0E**2/ttConst0**2)

      TT_rcs_diff = abs(rcs0bCRtt['rCS'] - (ttD+ttK*i_njb))
      TT_rcs_diffKappaCorr = abs(kappaTT['kappa']*rcs0bCRtt['rCS'] - (ttD+ttK*i_njb))
      TT_y_diff = TT_rcs_diff*res[njb][stb][htb]['yTT_srNJet_0b_lowDPhi']
      TT_y_diffKappaCorr = TT_rcs_diffKappaCorr*res[njb][stb][htb]['yTT_srNJet_0b_lowDPhi']
      
      #TTexpandedErr = res[njb][stb][htb]['TT_pred_err']+abs(1-kappaTT['kappa'])*res[njb][stb][htb]['TT_pred']+TTdiff
      
      TT_pred_corr = res[njb][stb][htb]['TT_pred']*kappaTT['kappa']
      #ttCorrectedErr = sqrt(res[njb][stb][htb]['TT_pred']**2*kappaTT['kappaE_sim']**2+res[njb][stb][htb]['TT_pred_err']**2*kappaTT['kappa']**2) + TTdiffKappaCorr
      
      TT_stat_err = sqrt(res[njb][stb][htb]['TT_pred']**2*kappaTT['kappaE_sim']**2+res[njb][stb][htb]['TT_pred_err']**2*kappaTT['kappa']**2)
      TT_syst_err = TT_y_diff
      TT_pred_err = sqrt(TT_stat_err**2 + TT_syst_err**2)
      
      TT_corrections = {'k_0b/1b':kappaTT['kappa'], 'k_0b/1b_err':kappaTT['kappaE_sim'], 'k_0b/1b_fit':kappaTTfit, 'k_0b/1b_fit_err':kappaTTfitErr, '0b_fit_const':ttD,'0b_fit_const_err':ttDE, '0b_fit_grad':ttK, '0b_fit_grad_err':ttKE}
      res[njb][stb][htb].update({'TT_rCS_fits_MC':TT_corrections})
      
      #print
      #print 'ttJets\tK\tKerr\tKfit\tRcsPred\tRcsFit\tRcsTrue\tRcs+K\tRcsDiff\t+K\tYDiff\t+K\tYpred\tYEpred\tYtrue\tYEtrue\tpropE'
      #print '\t',round(kappaTT['kappa'],2), '\t',round(kappaTT['kappaE_sim'],2), '\t',round(kappaTTfit,2), '\t', round(res[njb][stb][htb]['rCS_crLowNJet_1b']['rCS'],3),'\t', round(ttD+ttK*i_njb,3),'\t',\
      #           round(res[njb][stb][htb]['rCS_srNJet_0b_onlyTT']['rCS'],3),'\t',round(kappaTT['kappa']*res[njb][stb][htb]['rCS_crLowNJet_1b']['rCS'],3),'\t',\
      #           round(TT_rcs_diff,3), '\t', round(TT_rcs_diffKappaCorr,3), '\t', round(TT_y_diff,3), '\t', round(TT_y_diffKappaCorr,3), '\t', round(res[njb][stb][htb]['TT_pred'],3), '\t',\
      #           round(res[njb][stb][htb]['TT_pred_err'],3), '\t', round(res[njb][stb][htb]['TT_truth'],3), '\t', round(res[njb][stb][htb]['TT_truth_err'],3), '\t',\
      #           round(TTexpandedErr,3)

      print
      print 'ttJets\tK\tK_err\tRcs:\tTruth\tPred\tFit\tMC0bSB\tYield:\tTruth\tPred\tCorr\tstat\tsyst\ttot_err'
      print '\t',round(kappaTT['kappa'],2), '\t',round(kappaTT['kappaE_sim'],2), '\t\t', round(res[njb][stb][htb]['rCS_srNJet_0b_onlyTT']['rCS'],3),'\t',\
                 round(res[njb][stb][htb]['rCS_crLowNJet_1b']['rCS'],3), '\t', round(ttD+ttK*i_njb,3),'\t', round(rcs0bCRtt['rCS'],3),'\t\t', \
                 round(res[njb][stb][htb]['TT_truth'],3), '\t',round(res[njb][stb][htb]['TT_pred'],3), '\t',round(TT_pred_corr,3),'\t',\
                 round(TT_stat_err,3), '\t',round(TT_syst_err,3), '\t',round(TT_pred_err,3)
      #total+=1
      #if (res[njb][stb][htb]['TT_pred']-TTexpandedErr)<=res[njb][stb][htb]['TT_truth']<=(res[njb][stb][htb]['TT_pred']+TTexpandedErr):
      #  print 'Truth value inside expanded error band!'
      #  scoreExp+=1
      #  if (res[njb][stb][htb]['TT_pred']-res[njb][stb][htb]['TT_pred_err'])<=res[njb][stb][htb]['TT_truth']<=(res[njb][stb][htb]['TT_pred']+res[njb][stb][htb]['TT_pred_err']):
      #    print 'Also already inside statistical error band!'
      #    scoreStat+=1
      res[njb][stb][htb]['TT_pred'] = TT_pred_corr
      res[njb][stb][htb]['TT_pred_err'] = TT_pred_err

      #Wjets corrections
      Wcharges = [{'name':'PosPdg','cut':'leptonPdg>0', 'string':'_PosPdg'},{'name':'NegPdg','cut':'leptonPdg<0', 'string':'_NegPdg'},{'name':'all', 'cut':'(1)', 'string':''}]
      for Wc in Wcharges:
        wJetRcsFitH = ROOT.TH1F("wJetRcsFitH","",len(wJetBins),0,len(wJetBins))
        
        #fill histograms for linear fit to account for possible non-flat rcs values
        for i_njbW, njbW in enumerate(wJetBins):
          cname, cut = nameAndCut(stb,htb,njbW, btb=(0,0) ,presel=presel)
          rcsD = getRCS(cWJets, cut+'&&'+Wc['cut'], dPhiCut)
          #rcs = rcsD['rCS']
          #rcsErrPred = rcsD['rCSE_pred']
          #rcsErr = rcsD['rCSE_sim']
          if not math.isnan(rcs):
            wJetRcsFitH.SetBinContent(i_njbW+1, rcsD['rCS'])
            wJetRcsFitH.SetBinError(i_njbW+1, rcsD['rCSE_sim'])

        print 'Linear Fit for WJets Rcs values in 0b MC', Wc['name'], 'charges'
        wJetRcsFitH.Fit('pol1','','same',0,3)
        FitFunc     = wJetRcsFitH.GetFunction('pol1')
        wD  = FitFunc.GetParameter(0)
        wDE = FitFunc.GetParError(0)
        wK  = FitFunc.GetParameter(1)
        wKE = FitFunc.GetParError(1)
        
        #difference of measured rcs and fit in 0b MC rcs

        cnameCRW, cutCRW = nameAndCut(stb,htb,(3,4), btb=(0,0) ,presel=presel)
        rcsCRW = getRCS(cWJets, cutCRW, dPhiCut)
        #RcsKey = 'rCS_W'+Wc['string']+'_crNJet_0b_corr'
        #rcsWdiff = abs(res[njb][stb][htb][RcsKey] - (wD+wK*i_njb)) #difference of rcs
        rcsWdiff = abs(rcsCRW['rCS'] - (wD+wK*i_njb)) #difference of rcs
        YieldLowDPhiKey = 'yW'+Wc['string']+'_srNJet_0b_lowDPhi'
        Wdiff = rcsWdiff*res[njb][stb][htb][YieldLowDPhiKey] #difference of yield
        
        #systematics of rcs measured in mu only compared to ele+mu
        # calculate disagreement between mu/ele+mu rcs values
        keyMu = 'rCS_crLowNJet_0b_onlyW_mu'+Wc['string']
        keyBoth = 'rCS_crLowNJet_0b_onlyW'+Wc['string']
        ratio = res[njb][stb][htb][keyMu]['rCS']/res[njb][stb][htb][keyBoth]['rCS']
        if math.isnan(ratio): ratio = 0.
  
        # take max of disagreement and stat. limit of ele+mu
        #print 'Error mu/e+mu: ratio, stat', abs(1-ratio), res[njb][stb][htb][keyBoth]['rCSE_sim']/res[njb][stb][htb][keyBoth]['rCS']
        WratioErr = max([abs(1-ratio),res[njb][stb][htb][keyBoth]['rCSE_sim']/res[njb][stb][htb][keyBoth]['rCS']])*res[njb][stb][htb][RcsKey]*res[njb][stb][htb][YieldLowDPhiKey]
        #WratioErr *= res[njb][stb][htb][YieldLowDPhiKey]
        #total error W
        PredErrKey = 'W'+Wc['string']+'_pred_err' #stat error
        W_stat_err = res[njb][stb][htb][PredErrKey]
        W_syst_err = sqrt(WratioErr**2+Wdiff**2)
        WexpandedErr = sqrt(W_stat_err**2 + W_syst_err**2)
        
        #save fit results in dict for pickle file
        WFitPar = {'const':wD,'const_err':wDE, 'grad':wK, 'grad_err':wKE}
        WFitKey = 'W_rCS_linearFit_MC_0b'+Wc['string']
        res[njb][stb][htb].update({WFitKey:WFitPar})
        W_errs = {'stat':W_stat_err, 'syst':W_syst_err, 'tot':WexpandedErr}
        W_errs_key = 'W_pred_errs'+Wc['string']
        res[njb][stb][htb].update({W_errs_key:W_errs})
        
        W_err_key = 'W_pred_err'+Wc['string']
        res[njb][stb][htb][W_err_key] = WexpandedErr
        del wJetRcsFitH

#      print
#      print 'WJets\tRcsPred\tRcsFit\tRcsTrue\tRcsDiff\tYDiff\tYpred\tYEpred\tYtrue\tYEtrue\tpropE'
#      print '\t',round(res[njb][stb][htb]['rCS_W_crNJet_0b_corr'],3),'\t', round(wD+wK*i_njb,3),'\t',\
#                 round(res[njb][stb][htb]['rCS_srNJet_0b_onlyW']['rCS'],3),'\t',\
#                 round(rcsWdiff,3), '\t', round(Wdiff,3), '\t', round(res[njb][stb][htb]['W_pred'],3), '\t',\
#                 round(res[njb][stb][htb]['W_pred_err'],3), '\t', round(res[njb][stb][htb]['W_truth'],3), '\t', round(res[njb][stb][htb]['W_truth_err'],3), '\t',\
#                 round(WexpandedErr,3)

      print
      print 'WJets\tRcs:\tTruth\tPred\tFit\tMC0bSB\tYield:\tTruth\tPred\tstat\tsyst\ttot_err'
      print '\t\t',round(res[njb][stb][htb]['rCS_srNJet_0b_onlyW']['rCS'],3), '\t',round(res[njb][stb][htb]['rCS_W_crNJet_0b_corr'],3), '\t', round(wD+wK*i_njb,3),'\t',\
                   round(rcsCRW['rCS'],3),'\t\t',\
                   round(res[njb][stb][htb]['W_truth'],3), '\t', round(res[njb][stb][htb]['W_pred'],3),'\t', \
                   round(W_stat_err,3), '\t',round(W_syst_err,3), '\t',round(WexpandedErr,3)



      #res[njb][stb][htb]['W_pred_err'] = WexpandedErr
      
      #res[njb][stb][htb]['tot_pred_err'] = sqrt(TTexpandedErr**2 + WexpandedErr**2 + res[njb][stb][htb]['Rest_truth_err']**2)
      res[njb][stb][htb]['tot_pred_err'] = sqrt(TT_pred_err**2 + WexpandedErr**2 + res[njb][stb][htb]['Rest_truth_err']**2)
      res[njb][stb][htb]['tot_pred'] = TT_pred_corr + res[njb][stb][htb]['W_pred'] + res[njb][stb][htb]['Rest_truth']
      #update res dict with new error
      del ttJetRcsFitH, ttJetRcsFitH1b
      

#print 'Events inside expanded error band:',scoreExp/total
#print 'Events inside stat error band:',scoreStat/total

pickle.dump(res,file(pickleDir+prefix+'_estimationResults_pkl_kappa_corrected','w'))

