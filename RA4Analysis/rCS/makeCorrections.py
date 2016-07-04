import ROOT
import pickle
import os,sys,math
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getPropagatedError
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName

from Workspace.HEPHYPythonTools.user import username
from rCShelpers import *
from math import pi, sqrt
from Workspace.RA4Analysis.signalRegions import *

from predictionConfig import *

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()

ROOT.TH1F().SetDefaultSumw2()
if not createFits: loadedFit = pickle.load(file(fitDir+prefix+'_fit_pkl'))

weight_str, weight_err_str = makeWeight(3, sampleLumi=sampleLumi, reWeight = MCweight)

if validation:
  wJetBins = [(3,3),(4,4),(5,5),(6,7),(8,-1)]
else:
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

def getValErrString(val,err, precision=3):
  return str(round(val,precision))+' +/- '+str(round(err,precision))

def getValErrStringSyst(val,err,syst, precision=3):
  return str(round(val,precision))+' +/- '+str(round(err,precision)) +' +/- '+str(round(syst,precision))

res = pickle.load(file(pickleDir+prefix+'_estimationResults_pkl'))

scoreExp=0.
scoreStat=0.
total=0.
fitResults = {}

#correction is purly MC based, so cData should not enter anywhere here!

print
print 'Starting with fits for corrections and systematic errors, will use the following weight for all MC:'
print weight_str
print

ttcan = ROOT.TCanvas('ttcan','ttcan',700,700)
wcan = ROOT.TCanvas('wcan','wcan',700,700)


for i_njb, njb in enumerate(sorted(signalRegions)):
  bins[njb] = {}
  fitResults[njb] = {}
  for stb in sorted(signalRegions[njb]):
    bins[njb][stb] ={}
    fitResults[njb][stb] ={}
    for htb in sorted(signalRegions[njb][stb]):
      print
      print '#############################################'
      print '## * njet:',njb
      print '## * LT:  ',stb
      print '## * HT:  ',htb
      print '#############################################'
      print
      dPhiCut = signalRegions[njb][stb][htb]['deltaPhi']
      if createFits:
        #ttJets corrections
        ttJetRcsFitH = ROOT.TH1F("ttJetRcsFitH","",len(ttJetBins),0,len(ttJetBins))
        ttJetRcsFitH1b = ROOT.TH1F("ttJetRcsFitH1b","",len(ttJetBins),0,len(ttJetBins))

        #Rcs values w/o b-tag weights
        cname1bCRtt, cut1bCRtt = nameAndCut(stb,htb,(4,5), btb=(1,1) ,presel=presel_MC)
        cname0bCRtt, cut0bCRtt = nameAndCut(stb,htb,(4,5), btb=(0,0) ,presel=presel_MC)
        rcs1bCRtt = getRCS(cBkg, cut1bCRtt, dPhiCut, weight = weight_str)
        rcs0bCRtt = getRCS(cTTJets, cut0bCRtt, dPhiCut, weight = weight_str)
        
        #Rcs values w/ b-tag weights
        cnameCRtt, cutCRtt = nameAndCut(stb,htb,(4,5), btb=(0,-1) ,presel=presel_MC)
        samples = [{'chain':cWJets, 'cut':cutCRtt, 'weight':weight_str+'*weightBTag1'+btagWeightSuffix}, {'chain':cTTJets, 'cut':cutCRtt, 'weight':weight_str+'*weightBTag1'+btagWeightSuffix},{'chain':cDY, 'cut':cut1bCRtt, 'weight':weight_str},{'chain':cTTV, 'cut':cut1bCRtt, 'weight':weight_str},{'chain':csingleTop, 'cut':cut1bCRtt, 'weight':weight_str}]

        rcs1bCRtt_btag = combineRCS(samples, dPhiCut)
        rcs0bCRtt_btag = getRCS(cTTJets, cutCRtt, dPhiCut, weight = weight_str+'*weightBTag0'+btagWeightSuffix)

        #Kappa now calculated only in the SB bin (4,5) jets 1b allEWK MC vs 0b tt MC - no fit applied for the moment!
        kappaTT = divideRCSdict(rcs0bCRtt,rcs1bCRtt)
        kappaTT_btag = divideRCSdict(rcs0bCRtt_btag,rcs1bCRtt_btag)

        fitResults[njb][stb][htb] = {'kappaTT':kappaTT, 'rcs1bCRtt_btag':rcs1bCRtt_btag, 'rcs1bCRtt':rcs1bCRtt, 'rcs0bCRtt':rcs0bCRtt, 'rcs0bCRtt_btag':rcs0bCRtt_btag, 'kappaTT_btag':kappaTT_btag}

        #fill histograms
        # for the time being, bins with 0 entries (= Rcs=0) are not incorporated in the fit (same applies for wjets)
        for i_njbTT, njbTT in enumerate(ttJetBins):
          # get the Rcs plots, use b-tag weights and scale factors
          cname, cut     = nameAndCut(stb,htb,njbTT, btb=(0,-1) ,presel=presel_MC)
          cname1b, cut1b = nameAndCut(stb,htb,njbTT, btb=(0,-1) ,presel=presel_MC)
          rcsD = getRCS(cTTJets, cut, dPhiCut, weight = weight_str+'*weightBTag0'+btagWeightSuffix, avoidNan=True)
          rcsD1b = getRCS(cTTJets, cut1b, dPhiCut, weight = weight_str+'*weightBTag1'+btagWeightSuffix, avoidNan=True)
          ttJetRcsFitH.GetXaxis().SetBinLabel(i_njbTT+1,nJetBinName(njbTT))
          if not math.isnan(rcsD['rCS']):
            ttJetRcsFitH.SetBinContent(i_njbTT+1, rcsD['rCS'])
            ttJetRcsFitH.SetBinError(i_njbTT+1, rcsD['rCSE_sim'])
          #if math.isnan(rcsD['rCSE_sim']) or rcsD['rCS']==0:
          #  if i_njbTT>1: ttJetRcsFitH.SetBinError(i_njbTT+1, 2*ttJetRcsFitH.GetBinError(i_njbTT))
          #  else: ttJetRcsFitH.SetBinError(i_njbTT+1, 0.2)
          if not math.isnan(rcsD1b['rCS']):
            ttJetRcsFitH1b.SetBinContent(i_njbTT+1, rcsD1b['rCS'])
            ttJetRcsFitH1b.SetBinError(i_njbTT+1, rcsD1b['rCSE_sim'])

        message = '** Fits for tt+Jets Rcs values in 0b MC all charges **'
        stars = ''
        for star in range(len(message)):
          stars += '*'
        print
        print stars
        print message
        print stars
        print
        print 'Linear Fit for tt Jets Rcs values in 0b MC'

        #linear fit in 0b
        #filledBin = 0
        #for b in range(len(ttJetBins)):
        #  if ttJetRcsFitH.GetBinContent(b+1)>0:
        #    filledBin += 1
        #  else: break
        filledBin = len(ttJetBins)
        
        # fit pol1 to rcs hist
        FitFunc = ROOT.TF1("FitFunc", "[0]+[1]*x", 0, filledBin)
        FitFunc.SetParameters(2,-1)
        FitFunc.SetLineWidth(2)
        fitres = ttJetRcsFitH.Fit("FitFunc", "S")
        fitres.Print("V")
        ttD   = FitFunc.GetParameter(0)
        ttDE = FitFunc.GetParError(0)
        ttK   = FitFunc.GetParameter(1)
        ttKE = FitFunc.GetParError(1)

        covMatrix = fitres.GetCovarianceMatrix()
        a = covMatrix(0,0)
        b = c = covMatrix(0,1)
        d = covMatrix(1,1)
        f2 = ROOT.TF1("f2", "sqrt([0] + [1]*x + [2]*x**2) + [3] + [4]*x", 0, filledBin)
        f2.SetParameters(a,b+c,d, ttD, ttK)
        f2.SetLineColor(ROOT.kAzure)
        f2.SetLineStyle(2)
        f2.SetLineWidth(2)

        f3 = ROOT.TF1("f3", "-sqrt([0] + [1]*x + [2]*x**2) + [3] + [4]*x", 0, filledBin)
        f3.SetParameters(a,b+c,d, ttD, ttK)
        f3.SetLineColor(ROOT.kAzure)
        f3.SetLineStyle(2)
        f3.SetLineWidth(2)

        ttLinear = {'ttD':ttD, 'ttDE':ttDE, 'ttK':ttK, 'ttKE':ttKE}
        fitResults[njb][stb][htb].update({'ttLinear':ttLinear})
        f1 = ROOT.TF1("f1", "[0] + [1]*x", 0, filledBin)
        f1.SetParameters(rcs0bCRtt_btag['rCS'],0)
        f1.SetLineWidth(2)
        f1.SetLineColor(ROOT.kRed+1)
        f1.SetLineStyle(2)
        FitFunc.SetLineWidth(2)
        FitFunc.SetLineColor(ROOT.kOrange+1)
        ttcan.cd()
        ttJetRcsFitH.SetMarkerColor(ROOT.kBlue)
        ttJetRcsFitH.SetLineColor(ROOT.kBlue)
        ttJetRcsFitH.GetYaxis().SetTitle('R_{CS}')
        ttJetRcsFitH.GetYaxis().SetLabelSize(0.04)
        ttJetRcsFitH.GetXaxis().SetLabelSize(0.06)
        ttJetRcsFitH.SetLineWidth(2)
        ttJetRcsFitH.SetMarkerStyle(21)
        ttJetRcsFitH.SetBarWidth(1)
        ttJetRcsFitH.SetBarOffset(0)
        ttJetRcsFitH.SetStats(0)
        ttJetRcsFitH.SetMinimum(0)
        ttJetRcsFitH.SetMaximum(0.19)
        ttJetRcsFitH.Draw('EH1')
        
        latex1 = ROOT.TLatex()
        latex1.SetNDC()
        latex1.SetTextSize(0.035)
        latex1.SetTextAlign(11)
        latex1.DrawLatex(0.2,0.9,'linear fit k x + d')
        latex1.DrawLatex(0.2,0.865,'k = ('+str(round(ttK*1000,2))+' #pm '+str(round(ttKE*1000,2))+') #times 10^{-3}')
        latex1.DrawLatex(0.2,0.83,'d = ('+str(round(ttD*1000,2))+' #pm '+str(round(ttDE*1000,2))+') #times 10^{-3}')
        latex1.DrawLatex(0.65,0.9, varBinName(stb, 'L_{T}'))
        latex1.DrawLatex(0.65,0.865, varBinName(htb, 'H_{T}'))
       
        
        latex2 = ROOT.TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.04)
        latex2.SetTextAlign(11)
        latex2.DrawLatex(0.16,0.96,'CMS #bf{#it{Simulation}}')
        latex2.DrawLatex(0.85,0.96,"(13TeV)")
        
        f1.Draw('same')
        #f2.Draw('same')
        #f3.Draw('same')
        FitFunc.Draw('same')
        
        ttcan.Print(fitPrintDir+cname+'_ttjets_all_fit.png')
        ttcan.Print(fitPrintDir+cname+'_ttjets_all_fit.pdf')
        ttcan.Print(fitPrintDir+cname+'_ttjets_all_fit.root')
        
        #print ttD, ttK

        #constant fit in 0b and 1b
        print
        print 'Konstant Fit for tt Jets Rcs values in 0b MC'
        ttJetRcsFitH.Fit('pol0','','same',0,4)
        FitFunc     = ttJetRcsFitH.GetFunction('pol0')
        ttConst0  = FitFunc.GetParameter(0)
        ttConst0E = FitFunc.GetParError(0)
        ttC0 = {'ttConst0':ttConst0, 'ttConst0E':ttConst0E}
        
        print
        print 'Konstant Fit for tt Jets Rcs values in 1b MC'
        ttJetRcsFitH1b.Fit('pol0','','same',0,4)
        FitFunc     = ttJetRcsFitH1b.GetFunction('pol0')
        ttConst1  = FitFunc.GetParameter(0)
        ttConst1E = FitFunc.GetParError(0)
        ttC1 = {'ttConst1':ttConst1, 'ttConst1E':ttConst1E}
        fitResults[njb][stb][htb].update({'ttC0':ttC0, 'ttC1':ttC1})

      else:
        #Load fit results if fitting isn't done        
        rcs1bCRtt = loadedFit[njb][stb][htb]['rcs1bCRtt']
        rcs0bCRtt = loadedFit[njb][stb][htb]['rcs0bCRtt']
        rcs1bCRtt_btag = loadedFit[njb][stb][htb]['rcs1bCRtt_btag']
        rcs0bCRtt_btag = loadedFit[njb][stb][htb]['rcs0bCRtt_btag']
        kappaTT =   loadedFit[njb][stb][htb]['kappaTT']
        kappaTT_btag =   loadedFit[njb][stb][htb]['kappaTT_btag']
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
      
      # calculate the difference between the assumption that Rcs is flat over njet and the linear fit
      TT_rcs_diff = abs(rcs0bCRtt_btag['rCS'] - (ttD+ttK*(i_njb+1.5))) # use 0b (assume flatness in 0b) in fit and constant assumption
      
      print 'check'
      print rcs1bCRtt_btag['rCS']
      print kappaTT_btag['kappa']*rcs1bCRtt_btag['rCS']
      print rcs0bCRtt_btag
      print 'parameters for correction'
      print i_njb
      print ttD+ttK*(i_njb+1.5)
      print rcs1bCRtt_btag['rCS']
      print rcs1bCRtt_btag['rCS'] - (ttD+ttK*(i_njb+1.5)) # +1.5 needed to get to the correct bin - if sth is changed in SR this needs to get adapted
      print kappaTT_btag['kappa']*rcs1bCRtt_btag['rCS'] - (ttD+ttK*(i_njb+1.5))
      
      TT_y_diff = TT_rcs_diff*res[njb][stb][htb]['yTT_srNJet_0b_lowDPhi']
      
      TT_pred_rcs_corr, TT_pred_rcs_corr_err = getPropagatedError([res[njb][stb][htb]['rCS_crLowNJet_1b']['rCS'], kappaTT_btag['kappa']],[res[njb][stb][htb]['rCS_crLowNJet_1b']['rCSE_sim'], kappaTT_btag['kappaE_sim']],1,0, returnCalcResult=True)

      TT_pred_corr = res[njb][stb][htb]['TT_pred']*kappaTT_btag['kappa']
      res[njb][stb][htb]['rCS_crLowNJet_1b_kappa'] = {'rCS':TT_pred_rcs_corr, 'rCSE_sim':TT_pred_rcs_corr_err, 'rCSE_pred':TT_pred_rcs_corr_err}
      
      TT_stat_err = sqrt(res[njb][stb][htb]['TT_pred']**2*kappaTT_btag['kappaE_sim']**2+res[njb][stb][htb]['TT_pred_err']**2*kappaTT_btag['kappa']**2)
      TT_syst_err = TT_y_diff
      TT_pred_err = sqrt(TT_stat_err**2 + TT_syst_err**2)
      print
      print '## ** tt+jets prediction stat+syst/total **'
      print '##',getValErrStringSyst(res[njb][stb][htb]['TT_pred'],TT_stat_err,TT_syst_err)
      print '##',getValErrString(TT_pred_corr,TT_pred_err)
      print '## Kappa_b:',getValErrString(kappaTT_btag['kappa'],kappaTT_btag['kappaE_sim'])
      print '## **  **'
      print

      TT_corrections = {'k_0b/1b':kappaTT['kappa'], 'k_0b/1b_err':kappaTT['kappaE_sim'], 'k_0b/1b_btag':kappaTT_btag['kappa'], 'k_0b/1b_btag_err':kappaTT_btag['kappaE_sim'], 'k_0b/1b_fit':kappaTTfit, 'k_0b/1b_fit_err':kappaTTfitErr, '0b_fit_const':ttD,'0b_fit_const_err':ttDE, '0b_fit_grad':ttK, '0b_fit_grad_err':ttKE, 'syst':TT_syst_err, 'stat':TT_stat_err}
      res[njb][stb][htb].update({'TT_rCS_fits_MC':TT_corrections})
      
      # correct prediction, use only stat error -> all systematic errors will be applied in another script
      #res[njb][stb][htb]['TT_pred'] = TT_pred_corr
      #res[njb][stb][htb]['TT_pred_err'] = TT_stat_err

      # Wjets corrections
      Wcharges = [{'name':'PosPdg','cut':'leptonPdg>0', 'string':'_PosPdg'},{'name':'NegPdg','cut':'leptonPdg<0', 'string':'_NegPdg'},{'name':'all', 'cut':'(1)', 'string':''}]
      for Wc in Wcharges:
        cnameCRW, cutCRW = nameAndCut(stb,htb,(3,4), btb=(0,-1) ,presel=presel_MC)
        rcsCRW = getRCS(cWJets, cutCRW+'&&'+Wc['cut'], dPhiCut, weight = weight_str+'*weightBTag0'+btagWeightSuffix)
        if createFits:
          wJetRcsFitH = ROOT.TH1F("wJetRcsFitH","",len(wJetBins),0,len(wJetBins))
          
          #fill histograms for linear fit to account for possible non-flat rcs values
          for i_njbW, njbW in enumerate(wJetBins):
            cname, cut = nameAndCut(stb,htb,njbW, btb=(0,-1) ,presel=presel_MC)
            rcsD = getRCS(cWJets, cut+'&&'+Wc['cut'], dPhiCut, weight = weight_str+'*weightBTag0'+btagWeightSuffix, avoidNan=True)
            if not math.isnan(rcsD['rCS']):
              wJetRcsFitH.SetBinContent(i_njbW+1, rcsD['rCS'])
              wJetRcsFitH.SetBinError(i_njbW+1, rcsD['rCSE_sim'])
              wJetRcsFitH.GetXaxis().SetBinLabel(i_njbW+1,nJetBinName(njbW))
            #if math.isnan(rcsD['rCSE_sim']) or rcsD['rCS']==0:
            #  if i_njbW>1: wJetRcsFitH.SetBinError(i_njbW+1, 2*wJetRcsFitH.GetBinError(i_njbW))
            #  else: wJetRcsFitH.SetBinError(i_njbW+1, 0.2)
          message = '** Linear Fit for WJets Rcs values in 0b MC '+Wc['name']+' charges **'
          stars = ''
          for star in range(len(message)):
            stars += '*'
          print
          print stars
          print message
          print stars
          print
          #filledBin = 0
          #for b in range(len(wJetBins)):
          #  if wJetRcsFitH.GetBinContent(b+1)>0:
          #    filledBin += 1
          #  else: break
          filledBin = len(wJetBins)

          wJetRcsFitH.Fit('pol1','','same',0,filledBin)
          FitFunc     = wJetRcsFitH.GetFunction('pol1')
          wD  = FitFunc.GetParameter(0)
          wDE = FitFunc.GetParError(0)
          wK  = FitFunc.GetParameter(1)
          wKE = FitFunc.GetParError(1)
          fitResults[njb][stb][htb][Wc['name']] = {'wD':wD, 'wDE':wDE, 'wK':wK, 'wKE':wKE}
          f1 = ROOT.TF1("f1", "[0] + [1]*x", 0, wJetRcsFitH.GetNbinsX())
          f1.SetParameters(rcsCRW['rCS'],0)
          f1.SetLineWidth(2)
          f1.SetLineColor(ROOT.kRed+1)
          f1.SetLineStyle(2)
          FitFunc.SetLineWidth(2)
          FitFunc.SetLineColor(ROOT.kOrange+1)
          wcan.cd()
          wJetRcsFitH.SetMarkerColor(color('wjets'))
          wJetRcsFitH.SetMarkerStyle(21)
          wJetRcsFitH.SetLineWidth(2)
          wJetRcsFitH.SetLineColor(color('wjets'))
          wJetRcsFitH.SetBarWidth(1)
          wJetRcsFitH.SetBarOffset(0)
          wJetRcsFitH.SetStats(0)
          wJetRcsFitH.SetMinimum(0) 
          wJetRcsFitH.SetMaximum(0.11)
          wJetRcsFitH.GetYaxis().SetTitle('R_{CS}')
          wJetRcsFitH.GetYaxis().SetLabelSize(0.04)
          wJetRcsFitH.GetXaxis().SetLabelSize(0.06)
          wJetRcsFitH.Draw('EH1')
          f1.Draw('same')
          latex1 = ROOT.TLatex()
          latex1.SetNDC()
          latex1.SetTextSize(0.035)
          latex1.SetTextAlign(11)
          latex1.DrawLatex(0.2,0.9,'linear fit k x + d')
          latex1.DrawLatex(0.2,0.865,'k = ('+str(round(wK*1000,2))+' #pm '+str(round(wKE*1000,2))+') #times 10^{-3}')
          latex1.DrawLatex(0.2,0.83,'d = ('+str(round(wD*1000,2))+' #pm '+str(round(wDE*1000,2))+') #times 10^{-3}')
          latex1.DrawLatex(0.65,0.9, varBinName(stb, 'L_{T}'))
          latex1.DrawLatex(0.65,0.865, varBinName(htb, 'H_{T}'))
          
          latex2 = ROOT.TLatex()
          latex2.SetNDC()
          latex2.SetTextSize(0.04)
          latex2.SetTextAlign(11)
          latex2.DrawLatex(0.16,0.96,'CMS #bf{#it{Simulation}}')
          latex2.DrawLatex(0.85,0.96,"(13TeV)")
          
          wcan.Print(fitPrintDir+cname+'_Wjets_'+Wc['name']+'_fit.png')
          wcan.Print(fitPrintDir+cname+'_Wjets_'+Wc['name']+'_fit.pdf')
          wcan.Print(fitPrintDir+cname+'_Wjets_'+Wc['name']+'_fit.root')
          
        else:
          wD  = loadedFit[njb][stb][htb][Wc['name']]['wD']
          wDE = loadedFit[njb][stb][htb][Wc['name']]['wDE']
          wK  = loadedFit[njb][stb][htb][Wc['name']]['wK']
          wKE = loadedFit[njb][stb][htb][Wc['name']]['wKE']
        #difference of measured rcs and fit in 0b MC rcs

        cnameCRW, cutCRW = nameAndCut(stb,htb,(3,4), btb=(0,-1) ,presel=presel_MC)
        rcsCRW = getRCS(cWJets, cutCRW+'&&'+Wc['cut'], dPhiCut, weight = weight_str+'*weightBTag0'+btagWeightSuffix)

        print 'parameters for correction'
        print i_njb
        print wD+wK*i_njb
        print rcsCRW['rCS']
        print rcsCRW['rCS'] - (wD+wK*(i_njb+1.5)) # +1.5 needed to get to the correct bin - if sth is changed in SR this needs to get adapted

        rcsWdiff = abs(rcsCRW['rCS'] - (wD+wK*(i_njb+1.5))) #difference of rcs
        YieldLowDPhiKey = 'yW'+Wc['string']+'_srNJet_0b_lowDPhi'
        Wdiff = rcsWdiff*res[njb][stb][htb][YieldLowDPhiKey] #difference of yield
        
        # systematics of rcs measured in mu only compared to ele+mu
        # calculate disagreement between mu/ele+mu rcs values
        keyMu = 'rCS_crLowNJet_0b_onlyW_mu'+Wc['string']
        keyBoth = 'rCS_crLowNJet_0b_onlyW'+Wc['string']
        ratio = res[njb][stb][htb][keyMu]['rCS']/res[njb][stb][htb][keyBoth]['rCS']
        if math.isnan(ratio): ratio = 0.
  
        # take max of disagreement and stat. limit of ele+mu
        RcsKey = 'rCS_W'+Wc['string']+'_crNJet_0b_corr'
        WratioErr = max([abs(1-ratio),res[njb][stb][htb][keyBoth]['rCSE_sim']/res[njb][stb][htb][keyBoth]['rCS']]) * res[njb][stb][htb][RcsKey]*res[njb][stb][htb][YieldLowDPhiKey]
        #total error W
        PredErrKey = 'W'+Wc['string']+'_pred_err' #stat error
        W_stat_err = res[njb][stb][htb][PredErrKey]
        W_syst_err = sqrt(WratioErr**2+Wdiff**2)
        WexpandedErr = sqrt(W_stat_err**2 + W_syst_err**2)
        
        #save fit results in dict for pickle file
        WFitPar = {'const':wD,'const_err':wDE, 'grad':wK, 'grad_err':wKE}
        WFitKey = 'W_rCS_linearFit_MC_0b'+Wc['string']
        res[njb][stb][htb].update({WFitKey:WFitPar})

        W_errs = {'stat':W_stat_err, 'syst':W_syst_err, 'tot':WexpandedErr, 'ratio_mu_elemu':WratioErr, 'const_vs_slope':Wdiff}
        W_errs_key = 'W_pred_errs'+Wc['string'] #Key for new dict with all errors
        W_key = 'W'+Wc['string']+'_pred' #Key for W prediction
        W_err_key = 'W'+Wc['string']+'_pred_err' #Key for W prediction error

        print
        print '## ** W+jets prediction stat+syst/total **'
        print '##',getValErrStringSyst(res[njb][stb][htb][W_key],W_stat_err,W_syst_err)
        print '##',getValErrString(res[njb][stb][htb][W_key],WexpandedErr)
        print '## **  **'

        res[njb][stb][htb].update({W_errs_key:W_errs})        
        
        tot_key = 'tot'+Wc['string']+'_pred'
        tot_err_key = 'tot'+Wc['string']+'_pred_err'
        rest_key = 'Rest'+Wc['string']+'_truth'
        rest_err_key = 'Rest'+Wc['string']+'_truth_err'

        if not Wc['name']=='all':
          TT_pred_forTotal = 0.5*TT_pred_corr
          TT_pred_err_forTotal = 0.5*TT_stat_err
        else:
          TT_pred_forTotal = TT_pred_corr
          TT_pred_err_forTotal = TT_stat_err
        
        print
        print '## ** Total prediction origin/updated for',Wc['name'],'charges **'
        print '##',getValErrString(res[njb][stb][htb][tot_key],res[njb][stb][htb][tot_err_key])
        res[njb][stb][htb][tot_err_key] = sqrt(TT_pred_err_forTotal**2 + W_stat_err**2 + res[njb][stb][htb][rest_err_key]**2)
        res[njb][stb][htb][tot_key] = TT_pred_forTotal + res[njb][stb][htb][W_key] + res[njb][stb][htb][rest_key]
        print '##',getValErrString(res[njb][stb][htb][tot_key],res[njb][stb][htb][tot_err_key])
        print '## **  **'
        if createFits:
          del wJetRcsFitH

      print
      print 'Calculating kappa values'
      if isCentralPrediction:
        #kappa similar to multi-b analysis, does not invoke b-tag fit results (ratio of Rcs values)
        #TT_kappa, TT_kappa_err = getPropagatedError(res[njb][stb][htb]['rCS_srNJet_0b_onlyTT']['rCS'], res[njb][stb][htb]['rCS_srNJet_0b_onlyTT']['rCSE_sim'], res[njb][stb][htb]['rCS_crNJet_0b_onlyTT']['rCS'], res[njb][stb][htb]['rCS_crNJet_0b_onlyTT']['rCSE_sim'], returnCalcResult=True)
        
        TT_kappa, TT_kappa_err = getPropagatedError(res[njb][stb][htb]['rCS_srNJet_0b_onlyTT']['rCS'], res[njb][stb][htb]['rCS_srNJet_0b_onlyTT']['rCSE_sim'], TT_pred_rcs_corr, TT_pred_rcs_corr_err, returnCalcResult=True)
        W_kappa, W_kappa_err = getPropagatedError(res[njb][stb][htb]['rCS_srNJet_0b_onlyW']['rCS'], res[njb][stb][htb]['rCS_srNJet_0b_onlyW']['rCSE_sim'], res[njb][stb][htb]['rCS_W_crNJet_0b_corr'], sqrt(res[njb][stb][htb]['rCS_Var_W_crNJet_0b_corr']), returnCalcResult=True)
        W_corrRest_kappa, W_corrRest_kappa_err = getPropagatedError(res[njb][stb][htb]['rCS_srNJet_0b_onlyW']['rCS'], res[njb][stb][htb]['rCS_srNJet_0b_onlyW']['rCSE_sim'], res[njb][stb][htb]['rCS_W_crNJet_0b_corr_rest'], sqrt(res[njb][stb][htb]['rCS_Var_W_crNJet_0b_corr_rest']), returnCalcResult=True)
        
        global_kappa, global_kappa_err = getPropagatedError(res[njb][stb][htb]['tot_truth'], res[njb][stb][htb]['tot_truth_err'], res[njb][stb][htb]['tot_pred'], res[njb][stb][htb]['tot_pred_err'], returnCalcResult=True)
        
        #different kappa to get closure in MC
        TT_kappa_yield, TT_kappa_yield_err = getPropagatedError(res[njb][stb][htb]['TT_truth'], res[njb][stb][htb]['TT_truth_err'], TT_pred_forTotal, TT_pred_err_forTotal, returnCalcResult=True)
        W_yield_kappa, W_kappa_yield_err = getPropagatedError(res[njb][stb][htb]['W_truth'], res[njb][stb][htb]['W_truth_err'], res[njb][stb][htb]['W_pred'], res[njb][stb][htb]['W_pred_err'], returnCalcResult=True)
        W_yield_corrRest_kappa, W_yield_corrRest_kappa_err = getPropagatedError(res[njb][stb][htb]['W_truth'], res[njb][stb][htb]['W_truth_err'], res[njb][stb][htb]['W_pred_corrRest'], res[njb][stb][htb]['W_pred_corrRest_err'], returnCalcResult=True)
        res[njb][stb][htb]['TT_kappa'] = TT_kappa
        res[njb][stb][htb]['TT_kappa_err'] = TT_kappa_err
        res[njb][stb][htb]['W_kappa'] = W_kappa
        res[njb][stb][htb]['W_kappa_err'] = W_kappa_err
        res[njb][stb][htb]['W_corrRest_kappa'] = W_corrRest_kappa
        res[njb][stb][htb]['W_corrRest_kappa_err'] = W_corrRest_kappa_err
        res[njb][stb][htb]['tot_kappa'] =  global_kappa
        res[njb][stb][htb]['tot_kappa_err'] = global_kappa_err
        print 'kappa(TT):', getValErrString(TT_kappa,TT_kappa_err)
        print 'kappa(W):', getValErrString(W_kappa,W_kappa_err)
        print 'kappa(W_corrRest):', getValErrString(W_kappa,W_kappa_err)
        print 'kappa(total):', getValErrString(global_kappa,global_kappa_err)
      else:
        kappa_dict = pickle.load(file(kappa_dict_dir))
        TT_kappa              = kappa_dict[njb][stb][htb]['TT_kappa']
        TT_kappa_err          = kappa_dict[njb][stb][htb]['TT_kappa_err']
        W_kappa               = kappa_dict[njb][stb][htb]['W_kappa']
        W_kappa_err           = kappa_dict[njb][stb][htb]['W_kappa_err']
        W_corrRest_kappa      = kappa_dict[njb][stb][htb]['W_corrRest_kappa']
        W_corrRest_kappa_err  = kappa_dict[njb][stb][htb]['W_corrRest_kappa_err']
        global_kappa          = kappa_dict[njb][stb][htb]['tot_kappa']
        global_kappa_err      = kappa_dict[njb][stb][htb]['tot_kappa_err']

        res[njb][stb][htb]['TT_kappa'] = TT_kappa
        res[njb][stb][htb]['TT_kappa_err'] = TT_kappa_err
        res[njb][stb][htb]['W_kappa'] = W_kappa
        res[njb][stb][htb]['W_kappa_err'] = W_kappa_err
        res[njb][stb][htb]['W_corrRest_kappa'] = W_corrRest_kappa
        res[njb][stb][htb]['W_corrRest_kappa_err'] = W_corrRest_kappa_err
        res[njb][stb][htb]['tot_kappa'] =  global_kappa
        res[njb][stb][htb]['tot_kappa_err'] = global_kappa_err
      
      # correct the predictions, but don't apply uncertainties of kappas on them - they are systematic uncertainties
      TT_pred_kappa, TT_pred_kappa_err = getPropagatedError([res[njb][stb][htb]['TT_pred'], kappaTT_btag['kappa'], TT_kappa], [res[njb][stb][htb]['TT_pred_err'], 0, 0], 1, 0, returnCalcResult=True)
      W_pred_kappa, W_pred_kappa_err = getPropagatedError([res[njb][stb][htb]['W_pred'], W_kappa], [res[njb][stb][htb]['W_pred_err'], 0], 1, 0, returnCalcResult=True)
      #W_pred_corrRest_kappa, W_pred_corrRest_kappa_err = getPropagatedError([res[njb][stb][htb]['W_pred_corrRest'], W_corrRest_kappa], [res[njb][stb][htb]['W_pred_corrRest_err'], W_corrRest_kappa_err], 1, 0, returnCalcResult=True)
      
      if W_pred_kappa<0: W_pred_kappa = 0.
      if TT_pred_kappa<0: TT_pred_kappa = 0.
      if W_pred_kappa_err<0: W_pred_kappa_err = abs(W_pred_kappa_err)
      if TT_pred_kappa_err<0: TT_pred_kappa_err = abs(TT_pred_kappa_err)
      
      res[njb][stb][htb]['W_pred_final']      = W_pred_kappa
      res[njb][stb][htb]['W_pred_final_err']  = W_pred_kappa_err
      res[njb][stb][htb]['TT_pred_final']     = TT_pred_kappa
      res[njb][stb][htb]['TT_pred_final_err'] = TT_pred_kappa_err
      res[njb][stb][htb]['tot_pred_final']         = TT_pred_kappa + W_pred_kappa + res[njb][stb][htb]['Rest_truth']
      res[njb][stb][htb]['tot_pred_final_err']     = sqrt(TT_pred_kappa_err**2 + W_pred_kappa_err**2 + res[njb][stb][htb]['Rest_truth_err']**2)
      
      if not 'yQCD_crNJet_1b_lowDPhi' in res[njb][stb][htb].keys():
        res[njb][stb][htb]['yQCD_crNJet_1b_lowDPhi'] = 0.
        res[njb][stb][htb]['yQCD_Var_crNJet_1b_lowDPhi'] = 0.
      if not 'yQCD_crNJet_1b_highDPhi' in res[njb][stb][htb].keys():
        res[njb][stb][htb]['yQCD_crNJet_1b_highDPhi'] = 0.
        res[njb][stb][htb]['yQCD_Var_crNJet_1b_highDPhi'] = 0.
      if not 'yQCD_srNJet_0b_lowDPhi' in res[njb][stb][htb].keys():
        res[njb][stb][htb]['yQCD_srNJet_0b_lowDPhi'] = 0.
        res[njb][stb][htb]['yQCD_Var_srNJet_0b_lowDPhi'] = 0.

      if createFits:
        del ttJetRcsFitH, ttJetRcsFitH1b

if createFits: pickle.dump(fitResults ,file(fitDir+prefix+'_fit_pkl','w'))
pickle.dump(res,file(pickleDir+prefix+'_estimationResults_pkl_kappa_corrected','w'))

