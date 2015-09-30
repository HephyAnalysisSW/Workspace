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
pickleDir = '/data/'+username+'/Spring15/25ns/rCS_0b_'+str(lumi)+'/'

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
      print 'bin: \t njet \t\t LT \t\t HT'
      if len(str(njb))<7:
        print '\t',njb,'\t\t',stb,'\t',htb
      else:
        print '\t',njb,'\t',stb,'\t',htb
      dPhiCut = signalRegions[njb][stb][htb]['deltaPhi']
      wJetRcsFitH = ROOT.TH1F("wJetRcsFitH","",len(wJetBins),0,len(wJetBins))
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
      print 'Konstant Fit for tt Jets Rcs values in 0b MC'
      ttJetRcsFitH.Fit('pol0','','same',0,3)
      FitFunc     = ttJetRcsFitH.GetFunction('pol0')
      ttConst0  = FitFunc.GetParameter(0)
      ttConst0E = FitFunc.GetParError(0)
      print 'Konstant Fit for tt Jets Rcs values in 1b MC'
      ttJetRcsFitH1b.Fit('pol0','','same',0,3)
      FitFunc     = ttJetRcsFitH1b.GetFunction('pol0')
      ttConst1  = FitFunc.GetParameter(0)
      ttConst1E = FitFunc.GetParError(0)
      kappaTTfit = ttConst0/ttConst1

      rcsTTdiff = abs(res[njb][stb][htb]['rCS_crLowNJet_1b']['rCS'] - (ttD+ttK*i_njb))
      rcsTTdiffKappaCorr = abs(kappaTT['kappa']*res[njb][stb][htb]['rCS_crLowNJet_1b']['rCS'] - (ttD+ttK*i_njb))
      TTdiff = rcsTTdiff*res[njb][stb][htb]['yTT_srNJet_0b_lowDPhi']
      TTdiffKappaCorr = rcsTTdiffKappaCorr*res[njb][stb][htb]['yTT_srNJet_0b_lowDPhi']
      TTexpandedErr = res[njb][stb][htb]['TT_pred_err']+abs(1-kappaTT['kappa'])*res[njb][stb][htb]['TT_pred']+TTdiff
      
      ttCorrected = res[njb][stb][htb]['TT_pred']*kappaTT['kappa']
      ttCorrectedErr = sqrt(res[njb][stb][htb]['TT_pred']**2*kappaTT['kappaE_sim']**2+res[njb][stb][htb]['TT_pred_err']**2*kappaTT['kappa']**2) + TTdiffKappaCorr
      
      
      print
      print 'ttJets\tK\tKerr\tKfit\tRcsPred\tRcsFit\tRcsTrue\tRcs+K\tRcsDiff\t+K\tYDiff\t+K\tYpred\tYEpred\tYtrue\tYEtrue\tpropE'
      print '\t',round(kappaTT['kappa'],2), '\t',round(kappaTT['kappaE_sim'],2), '\t',round(kappaTTfit,2), '\t', round(res[njb][stb][htb]['rCS_crLowNJet_1b']['rCS'],3),'\t', round(ttD+ttK*i_njb,3),'\t',\
                 round(res[njb][stb][htb]['rCS_srNJet_0b_onlyTT']['rCS'],3),'\t',round(kappaTT['kappa']*res[njb][stb][htb]['rCS_crLowNJet_1b']['rCS'],3),'\t',\
                 round(rcsTTdiff,3), '\t', round(rcsTTdiffKappaCorr,3), '\t', round(TTdiff,3), '\t', round(TTdiffKappaCorr,3), '\t', round(res[njb][stb][htb]['TT_pred'],3), '\t',\
                 round(res[njb][stb][htb]['TT_pred_err'],3), '\t', round(res[njb][stb][htb]['TT_truth'],3), '\t', round(res[njb][stb][htb]['TT_truth_err'],3), '\t',\
                 round(TTexpandedErr,3)
      #total+=1
      #if (res[njb][stb][htb]['TT_pred']-TTexpandedErr)<=res[njb][stb][htb]['TT_truth']<=(res[njb][stb][htb]['TT_pred']+TTexpandedErr):
      #  print 'Truth value inside expanded error band!'
      #  scoreExp+=1
      #  if (res[njb][stb][htb]['TT_pred']-res[njb][stb][htb]['TT_pred_err'])<=res[njb][stb][htb]['TT_truth']<=(res[njb][stb][htb]['TT_pred']+res[njb][stb][htb]['TT_pred_err']):
      #    print 'Also already inside statistical error band!'
      #    scoreStat+=1
      res[njb][stb][htb]['TT_pred'] = ttCorrected
      res[njb][stb][htb]['TT_pred_err'] = ttCorrectedErr

      #Wjets corrections
      for i_njbW, njbW in enumerate(wJetBins):
        cname, cut = nameAndCut(stb,htb,njbW, btb=(0,0) ,presel=presel)
        rcsD = getRCS(cWJets, cut, dPhiCut)
        rcs = rcsD['rCS']
        rcsErrPred = rcsD['rCSE_pred']
        rcsErr = rcsD['rCSE_sim']
        if not math.isnan(rcs):
          wJetRcsFitH.SetBinContent(i_njbW+1, rcs)
          wJetRcsFitH.SetBinError(i_njbW+1, rcsErr)
      print 'Linear Fit for WJets Rcs values in 0b MC'
      wJetRcsFitH.Fit('pol1','','same',0,3)
      FitFunc     = wJetRcsFitH.GetFunction('pol1')
      wD  = FitFunc.GetParameter(0)
      wDE = FitFunc.GetParError(0)
      wK  = FitFunc.GetParameter(1)
      wKE = FitFunc.GetParError(1)
      rcsWdiff = abs(res[njb][stb][htb]['rCS_W_crNJet_0b_corr'] - (wD+wK*i_njb))
      Wdiff = rcsWdiff*res[njb][stb][htb]['yW_srNJet_0b_lowDPhi']
      
      WexpandedErr = res[njb][stb][htb]['W_pred_err']+Wdiff
      
      print
      print 'WJets\tRcsPred\tRcsFit\tRcsTrue\tRcsDiff\tYDiff\tYpred\tYEpred\tYtrue\tYEtrue\tpropE'
      print '\t',round(res[njb][stb][htb]['rCS_W_crNJet_0b_corr'],3),'\t', round(wD+wK*i_njb,3),'\t',\
                 round(res[njb][stb][htb]['rCS_srNJet_0b_onlyW']['rCS'],3),'\t',\
                 round(rcsWdiff,3), '\t', round(Wdiff,3), '\t', round(res[njb][stb][htb]['W_pred'],3), '\t',\
                 round(res[njb][stb][htb]['W_pred_err'],3), '\t', round(res[njb][stb][htb]['W_truth'],3), '\t', round(res[njb][stb][htb]['W_truth_err'],3), '\t',\
                 round(WexpandedErr,3)
      res[njb][stb][htb]['W_pred_err'] = WexpandedErr
      
      #res[njb][stb][htb]['tot_pred_err'] = sqrt(TTexpandedErr**2 + WexpandedErr**2 + res[njb][stb][htb]['Rest_truth_err']**2)
      res[njb][stb][htb]['tot_pred_err'] = sqrt(ttCorrectedErr**2 + WexpandedErr**2 + res[njb][stb][htb]['Rest_truth_err']**2)
      res[njb][stb][htb]['tot_pred'] = ttCorrected + res[njb][stb][htb]['W_pred'] + res[njb][stb][htb]['Rest_truth']
      #update res dict with new error
      del wJetRcsFitH, ttJetRcsFitH, ttJetRcsFitH1b
      

#print 'Events inside expanded error band:',scoreExp/total
#print 'Events inside stat error band:',scoreStat/total

pickle.dump(res,file(pickleDir+prefix+'_estimationResults_pkl_kappa_corrected','w'))

