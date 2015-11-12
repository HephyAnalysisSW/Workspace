import ROOT
import pickle
import os,sys,math
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName

from Workspace.HEPHYPythonTools.user import username
from rCShelpers import *
from math import pi, sqrt
from Workspace.RA4Analysis.signalRegions import *

from predictionConfig import *

ROOT.TH1F().SetDefaultSumw2()

if not createFits: loadedFit = pickle.load(file(fitDir+prefix+'_fit_pkl'))

weight_str, weight_err_str = makeWeight(lumi, sampleLumi=sampleLumi)

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
fitResults = {}

for i_njb, njb in enumerate(signalRegions):
  bins[njb] = {}
  fitResults[njb] = {}
  for stb in signalRegions[njb]:
    bins[njb][stb] ={}
    fitResults[njb][stb] ={}
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
      if createFits:
        #ttJets corrections
        ttJetRcsFitH = ROOT.TH1F("ttJetRcsFitH","",len(ttJetBins),0,len(ttJetBins))
        ttJetRcsFitH1b = ROOT.TH1F("ttJetRcsFitH1b","",len(ttJetBins),0,len(ttJetBins))
        cname1bCRtt, cut1bCRtt = nameAndCut(stb,htb,(4,5), btb=(1,1) ,presel=presel)
        cname0bCRtt, cut0bCRtt = nameAndCut(stb,htb,(4,5), btb=(0,0) ,presel=presel)
        cnameCRtt, cutCRtt = nameAndCut(stb,htb,(4,5), btb=(0,-1) ,presel=presel)
        rcs1bCRtt = getRCS(cEWK, cut1bCRtt, dPhiCut)
        rcs0bCRtt = getRCS(cTTJets, cut0bCRtt, dPhiCut)
        samples = [{'chain':cWJets, 'cut':cutCRtt, 'weight':'weight*weightBTag1'}, {'chain':cTTJets, 'cut':cutCRtt, 'weight':'weight*weightBTag1'},{'chain':cDY, 'cut':cut1bCRtt, 'weight':'weight'},{'chain':cTTV, 'cut':cut1bCRtt, 'weight':'weight'},{'chain':csingleTop, 'cut':cut1bCRtt, 'weight':'weight'}]
        rcs1bCRtt_btag = combineRCS(samples, dPhiCut)
        rcs0bCRtt_btag = getRCS(cTTJets, cutCRtt, dPhiCut, weight = 'weight*weightBTag0')
        #Kappa now calculated only in the SB bin (4,5) jets 1b allEWK MC vs 0b tt MC - no fit applied for the moment!
        kappaTT = divideRCSdict(rcs0bCRtt,rcs1bCRtt)
        kappaTT_btag = divideRCSdict(rcs0bCRtt_btag,rcs1bCRtt_btag)
        fitResults[njb][stb][htb] = {'kappaTT':kappaTT, 'rcs1bCRtt':rcs1bCRtt, 'rcs0bCRtt':rcs0bCRtt, 'kappaTT_btag':kappaTT_btag}
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
        ttLinear = {'ttD':ttD, 'ttDE':ttDE, 'ttK':ttK, 'ttKE':ttKE}
        fitResults[njb][stb][htb].update({'ttLinear':ttLinear})
        #print ttD, ttK
        #constant fit in 0b and 1b
        print
        print 'Konstant Fit for tt Jets Rcs values in 0b MC'
        ttJetRcsFitH.Fit('pol0','','same',0,3)
        FitFunc     = ttJetRcsFitH.GetFunction('pol0')
        ttConst0  = FitFunc.GetParameter(0)
        ttConst0E = FitFunc.GetParError(0)
        ttC0 = {'ttConst0':ttConst0, 'ttConst0E':ttConst0E}
        
        print
        print 'Konstant Fit for tt Jets Rcs values in 1b MC'
        ttJetRcsFitH1b.Fit('pol0','','same',0,3)
        FitFunc     = ttJetRcsFitH1b.GetFunction('pol0')
        ttConst1  = FitFunc.GetParameter(0)
        ttConst1E = FitFunc.GetParError(0)
        ttC1 = {'ttConst1':ttConst1, 'ttConst1E':ttConst1E}
        fitResults[njb][stb][htb].update({'ttC0':ttC0, 'ttC1':ttC1})
      else:
        
        rcs1bCRtt = loadedFit[njb][stb][htb]['rcs1bCRtt']
        rcs0bCRtt = loadedFit[njb][stb][htb]['rcs0bCRtt']
        kappaTT =   loadedFit[njb][stb][htb]['kappaTT']
        ttD =       loadedFit[njb][stb][htb]['ttLinear']['ttD']
        ttDE =      loadedFit[njb][stb][htb]['ttLinear']['ttDE']
        ttK =       loadedFit[njb][stb][htb]['ttLinear']['ttK']
        ttKE =      loadedFit[njb][stb][htb]['ttLinear']['ttKE']
        ttConst0 =  loadedFit[njb][stb][htb]['ttC0']['ttConst0']
        ttConst0E = loadedFit[njb][stb][htb]['ttC0']['ttConst0E']
        ttConst1 =  loadedFit[njb][stb][htb]['ttC1']['ttConst1']
        ttConst1E = loadedFit[njb][stb][htb]['ttC1']['ttConst1E']


      kappaTTfit = ttConst0/ttConst1
      kappaTTfitErr = kappaTTfit*sqrt(ttConst1E**2/ttConst1**2+ttConst0E**2/ttConst0**2)

      TT_rcs_diff = abs(rcs1bCRtt['rCS'] - (ttD+ttK*i_njb))
      TT_rcs_diffKappaCorr = abs(kappaTT['kappa']*rcs1bCRtt['rCS'] - (ttD+ttK*i_njb))
      TT_y_diff = TT_rcs_diff*res[njb][stb][htb]['yTT_srNJet_0b_lowDPhi']
      TT_y_diffKappaCorr = TT_rcs_diffKappaCorr*res[njb][stb][htb]['yTT_srNJet_0b_lowDPhi']
      
      #TTexpandedErr = res[njb][stb][htb]['TT_pred_err']+abs(1-kappaTT['kappa'])*res[njb][stb][htb]['TT_pred']+TTdiff
      
      TT_pred_corr = res[njb][stb][htb]['TT_pred']*kappaTT['kappa']
      #ttCorrectedErr = sqrt(res[njb][stb][htb]['TT_pred']**2*kappaTT['kappaE_sim']**2+res[njb][stb][htb]['TT_pred_err']**2*kappaTT['kappa']**2) + TTdiffKappaCorr
      
      TT_stat_err = sqrt(res[njb][stb][htb]['TT_pred']**2*kappaTT['kappaE_sim']**2+res[njb][stb][htb]['TT_pred_err']**2*kappaTT['kappa']**2)
      TT_syst_err = TT_y_diff
      TT_pred_err = sqrt(TT_stat_err**2 + TT_syst_err**2)
      
      TT_corrections = {'k_0b/1b':kappaTT['kappa'], 'k_0b/1b_err':kappaTT['kappaE_sim'], 'k_0b/1b_btag':kappaTT_btag['kappa'], 'k_0b/1b_btag_err':kappaTT_btag['kappaE_sim'], 'k_0b/1b_fit':kappaTTfit, 'k_0b/1b_fit_err':kappaTTfitErr, '0b_fit_const':ttD,'0b_fit_const_err':ttDE, '0b_fit_grad':ttK, '0b_fit_grad_err':ttKE}
      res[njb][stb][htb].update({'TT_rCS_fits_MC':TT_corrections})
      
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
        if createFits:
          wJetRcsFitH = ROOT.TH1F("wJetRcsFitH","",len(wJetBins),0,len(wJetBins))
          
          #fill histograms for linear fit to account for possible non-flat rcs values
          for i_njbW, njbW in enumerate(wJetBins):
            cname, cut = nameAndCut(stb,htb,njbW, btb=(0,0) ,presel=presel)
            rcsD = getRCS(cWJets, cut+'&&'+Wc['cut'], dPhiCut)
            #rcs = rcsD['rCS']
            #rcsErrPred = rcsD['rCSE_pred']
            #rcsErr = rcsD['rCSE_sim']
            if not math.isnan(rcsD['rCS']):
              wJetRcsFitH.SetBinContent(i_njbW+1, rcsD['rCS'])
              wJetRcsFitH.SetBinError(i_njbW+1, rcsD['rCSE_sim'])

          print 'Linear Fit for WJets Rcs values in 0b MC', Wc['name'], 'charges'
          wJetRcsFitH.Fit('pol1','','same',0,3)
          FitFunc     = wJetRcsFitH.GetFunction('pol1')
          wD  = FitFunc.GetParameter(0)
          wDE = FitFunc.GetParError(0)
          wK  = FitFunc.GetParameter(1)
          wKE = FitFunc.GetParError(1)
          fitResults[njb][stb][htb][Wc['name']] = {'wD':wD, 'wDE':wDE, 'wK':wK, 'wKE':wKE}
        else:
          wD  = loadedFit[njb][stb][htb][Wc['name']]['wD']
          wDE = loadedFit[njb][stb][htb][Wc['name']]['wDE']
          wK  = loadedFit[njb][stb][htb][Wc['name']]['wK']
          wKE = loadedFit[njb][stb][htb][Wc['name']]['wKE']
        #difference of measured rcs and fit in 0b MC rcs

        cnameCRW, cutCRW = nameAndCut(stb,htb,(3,4), btb=(0,0) ,presel=presel)
        rcsCRW = getRCS(cWJets, cutCRW, dPhiCut)
        RcsKey = 'rCS_W'+Wc['string']+'_crNJet_0b_corr'
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
        
        W_key = 'W'+Wc['string']+'_pred'
        W_err_key = 'W'+Wc['string']+'_pred_err'
        res[njb][stb][htb][W_err_key] = WexpandedErr
        
        tot_key = 'tot'+Wc['string']+'_pred'
        tot_err_key = 'tot'+Wc['string']+'_pred_err'
        rest_key = 'Rest'+Wc['string']+'_truth'
        rest_err_key = 'Rest'+Wc['string']+'_truth_err'

        if not Wc['name']=='all':
          TT_pred_forTotal = 0.5*TT_pred_corr
          TT_pred_err_forTotal = 0.5*TT_pred_err
        else:
          TT_pred_forTotal = TT_pred_corr
          TT_pred_err_forTotal = TT_pred_err

        res[njb][stb][htb][tot_err_key] = sqrt(TT_pred_err_forTotal**2 + WexpandedErr**2 + res[njb][stb][htb][rest_err_key]**2)
        res[njb][stb][htb][tot_key] = TT_pred_forTotal + res[njb][stb][htb][W_key] + res[njb][stb][htb][rest_key]
        
        if createFits:
          del wJetRcsFitH

      print
      print 'WJets\tRcs:\tTruth\tPred\tFit\tMC0bSB\tYield:\tTruth\tPred\tstat\tsyst\ttot_err'
      print '\t\t',round(res[njb][stb][htb]['rCS_srNJet_0b_onlyW']['rCS'],3), '\t',round(res[njb][stb][htb]['rCS_W_crNJet_0b_corr'],3), '\t', round(wD+wK*i_njb,3),'\t',\
                   round(rcsCRW['rCS'],3),'\t\t',\
                   round(res[njb][stb][htb]['W_truth'],3), '\t', round(res[njb][stb][htb]['W_pred'],3),'\t', \
                   round(W_stat_err,3), '\t',round(W_syst_err,3), '\t',round(WexpandedErr,3)


      if createFits:
        del ttJetRcsFitH, ttJetRcsFitH1b
      

#print 'Events inside expanded error band:',scoreExp/total
#print 'Events inside stat error band:',scoreStat/total

if createFits: pickle.dump(fitResults ,file(fitDir+prefix+'_fit_pkl','w'))
pickle.dump(res,file(pickleDir+prefix+'_estimationResults_pkl_kappa_btag_corrected','w'))

