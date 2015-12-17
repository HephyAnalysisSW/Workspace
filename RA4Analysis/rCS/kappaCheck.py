import ROOT
import pickle
import os,sys,math

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()

from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName
from Workspace.HEPHYPythonTools.user import username
from rCShelpers import *
from math import pi, sqrt, isnan
from Workspace.RA4Analysis.signalRegions import *

from binnedNBTagsFit import *

from predictionConfig import *


colorList = [ROOT.kBlue+1, ROOT.kCyan-9, ROOT.kOrange-4, ROOT.kGreen+1, ROOT.kRed+1]

ROOT.TH1F().SetDefaultSumw2()

lumi = 2.1
predictionName = 'data_newSR_lep_SFtemplates'
predictionName2 = 'MCwSF_newSR_lep_SFtemplates'
pickleDir   = '/data/'+username+'/Results2015/Prediction_'+predictionName+'_'+str(lumi)+'/'
pickleDir2   = '/data/'+username+'/Results2015/Prediction_'+predictionName2+'_'+str(lumi)+'/'

#res = pickle.load(file(pickleDir+'singleLeptonic_Spring15__estimationResults_pkl'))
#resMC = pickle.load(file(pickleDir2+'singleLeptonic_Spring15__estimationResults_pkl'))
def divideRCSdict(a,b):
  if b['rCS']>0:
    kappa = a['rCS']/b['rCS']
  else:
    kappa = float('nan')
    kappaErrorPred = float('nan')
    kappaErrorSim = float('nan')
  if a['rCS']>0 and b['rCS']>0:
    kappaErrorPred = (a['rCS']/b['rCS'])*sqrt(a['rCSE_pred']**2/a['rCS']**2+b['rCSE_pred']**2/b['rCS']**2)
    kappaErrorSim = (a['rCS']/b['rCS'])*sqrt(a['rCSE_sim']**2/a['rCS']**2+b['rCSE_sim']**2/b['rCS']**2)
  elif b['rCS']>0:
    kappaErrorPred = float('nan')
    kappaErrorSim  = float('nan')
  return {'kappa':kappa, 'kappaE_pred':kappaErrorPred, 'kappaE_sim':kappaErrorSim}

def getValErrString(val,err, precision=3):
  return str(round(val,precision))+' +/- '+str(round(err,precision))

def setNiceBinLabel(hist):
  i = 1
  for njb in sorted(signalRegions):
    for stb in sorted(signalRegions[njb]):
      for htb in sorted(signalRegions[njb][stb]):
        hist.GetXaxis().SetBinLabel(i,'#splitline{'+signalRegions[njb][stb][htb]['njet']+'}{#splitline{'+signalRegions[njb][stb][htb]['LT']+'}{'+signalRegions[njb][stb][htb]['HT']+'}}')
        i += 1


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

rcs1bMC   = ROOT.TH1F('rcs1bMC','Rcs 1b MC',bins,0,bins)
rcs1bMCrescale   = ROOT.TH1F('rcs1bMCrescale','Rcs 1b MC',bins,0,bins)
rcs1bMCrescaleD   = ROOT.TH1F('rcs1bMCrescaleD','Rcs 1b MC',bins,0,bins)


rcs1bdata = ROOT.TH1F('rcs1bdata','Rcs 1b data',bins,0,bins)
rcs1bdata_noQCDcorr = ROOT.TH1F('rcs1bdata_noQCDcorr','Rcs 1b data no QCD corr',bins,0,bins)

rcs2bMC   = ROOT.TH1F('rcs2bMC','Rcs 2b MC',bins,0,bins)
rcs2bdata = ROOT.TH1F('rcs2bdata','Rcs 2b data',bins,0,bins)
rcs2bdata_noQCDcorr = ROOT.TH1F('rcs2bdata_noQCDcorr','Rcs 2b data no QCD corr',bins,0,bins)


fit1bMC   = ROOT.TH1F('fit1bMC',  'Fit 1b MC',bins,0,bins)
fit1bdata = ROOT.TH1F('fit1bdata','Fit 1b data',bins,0,bins)
fit2bMC   = ROOT.TH1F('fit2bMC',  'Fit 2b MC',bins,0,bins)
fit2bdata = ROOT.TH1F('fit2bdata','Fit 2b data',bins,0,bins)

fit1bMC.SetLineColor(colorList[0])
fit1bMC.SetMarkerStyle(0)
fit1bMC.SetLineWidth(2)
fit1bMC.SetMaximum(1.2)
fit1bMC.SetMinimum(0)
fit1bMC.GetXaxis().SetLabelSize(0.04)
fit1bMC.GetYaxis().SetLabelSize(0.04)
fit1bMC.GetYaxis().SetTitle('t#bar{t} fraction')


fit1bdata.SetLineColor(colorList[3])
fit1bdata.SetMarkerStyle(0)
fit1bdata.SetLineWidth(2)

fit2bMC.SetLineColor(colorList[2])
fit2bMC.SetMarkerStyle(0)
fit2bMC.SetLineWidth(2)

fit2bdata.SetLineColor(colorList[4])
fit2bdata.SetMarkerStyle(0)
fit2bdata.SetLineWidth(2)


rcs1bMC.SetLineColor(colorList[0])
rcs1bMCrescale.SetLineColor(colorList[4])
rcs1bMCrescaleD.SetLineColor(colorList[2])

rcs1bdata.SetLineColor(colorList[3])
rcs2bMC.SetLineColor(colorList[2])
rcs2bdata.SetLineColor(colorList[4])

rcs1bMCrescaleD.SetMarkerColor(colorList[2])
rcs1bMCrescale.SetMarkerColor(colorList[4])
rcs1bdata.SetMarkerColor(colorList[3])
rcs1bMC.SetMarkerColor(colorList[0])

rcs1bMC.SetMarkerStyle(20)
rcs1bMCrescale.SetMarkerStyle(21)
rcs1bMCrescaleD.SetMarkerStyle(22)
rcs1bdata.SetMarkerStyle(23)
rcs2bMC.SetMarkerStyle(0)
rcs2bdata.SetMarkerStyle(0)

rcs1bMC.SetLineWidth(2)
rcs1bMCrescale.SetLineWidth(2)
rcs1bMCrescaleD.SetLineWidth(2)
rcs1bdata.SetLineWidth(2)
rcs2bMC.SetLineWidth(2)
rcs2bdata.SetLineWidth(2)

rcs1bMC.SetMinimum(0.)
rcs1bMC.SetMaximum(0.1)
rcs1bMC.GetYaxis().SetTitle('R_{CS}')
rcs1bMC.GetYaxis().SetLabelSize(0.04)
rcs1bMC.GetXaxis().SetLabelSize(0.04)



kappa01TT  = ROOT.TH1F('kappa01','tt(0b)/tt(1b)',bins,0,bins)
kappa12TT  = ROOT.TH1F('kappa12','tt(1b)/tt(2b)',bins,0,bins)
kappa0tt1EWK = ROOT.TH1F('kappa','tt(0b)/EWK(1b)',bins,0,bins)
kappa01EWK = ROOT.TH1F('kappa01ewk','EWK(0b)/EWK(1b)',bins,0,bins)
kappa12EWK = ROOT.TH1F('kappa12ewk','EWK(1b)/EWK(2b)',bins,0,bins)

kappa12data = ROOT.TH1F('kappa12data','data 1b/2b',bins,0,bins)

kappa01TT.SetLineColor(colorList[0])
kappa01TT.SetMinimum(0.)
kappa01TT.SetMaximum(2.)

kappa12TT.SetLineColor(colorList[1])
kappa0tt1EWK.SetLineColor(colorList[2])
kappa01EWK.SetLineColor(colorList[3])
kappa12EWK.SetLineColor(colorList[0])
kappa12data.SetLineColor(colorList[3])

kappa01TT.SetMarkerStyle(0)
kappa12TT.SetMarkerStyle(0)
kappa0tt1EWK.SetMarkerStyle(0)
kappa01EWK.SetMarkerStyle(0)
kappa12EWK.SetMarkerStyle(0)
kappa12data.SetMarkerStyle(0)

kappa01TT.SetLineWidth(2)
kappa12TT.SetLineWidth(2)
kappa0tt1EWK.SetLineWidth(2)
kappa01EWK.SetLineWidth(2)

kappa01EWK.SetMaximum(1.5)
kappa01EWK.SetMinimum(0)

kappa12EWK.SetLineWidth(2)
kappa12EWK.GetYaxis().SetLabelSize(0.04)
kappa12EWK.GetXaxis().SetLabelSize(0.04)
kappa12EWK.GetYaxis().SetTitle('#kappa_{b}')
setNiceBinLabel(kappa12EWK)

kappa12data.SetLineWidth(2)

i = 1
can = ROOT.TCanvas('c','c',700,700)

leg = ROOT.TLegend(0.65,0.75,0.98,0.95)
leg.SetFillColor(ROOT.kWhite)
leg.SetShadowColor(ROOT.kWhite)
leg.SetBorderSize(1)
leg.SetTextSize(0.035)

leg2 = ROOT.TLegend(0.65,0.75,0.98,0.95)
leg2.SetFillColor(ROOT.kWhite)
leg2.SetShadowColor(ROOT.kWhite)
leg2.SetBorderSize(1)
leg2.SetTextSize(0.035)

leg3 = ROOT.TLegend(0.65,0.82,0.98,0.95)
leg3.SetFillColor(ROOT.kWhite)
leg3.SetShadowColor(ROOT.kWhite)
leg3.SetBorderSize(1)
leg3.SetTextSize(0.035)

#presel = singleMu_presel

#presel += '&&abs(leptonPdg)==13'

frac = {}
b = 1

fitRescale = False

for i_njb, njb in enumerate(sorted(signalRegions)):
  frac[njb] = {}
  for stb in sorted(signalRegions[njb]):
    frac[njb][stb] = {}
    for htb in sorted(signalRegions[njb][stb]):
      frac[njb][stb][htb] = {}
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
      #ttJets corrections
      srNJet = (3,5)
      cname2bCRtt, cut2bCRtt =    nameAndCut(stb,htb,srNJet, btb=(2,-1) ,presel=presel)
      cname1bCRtt, cut1bCRtt =    nameAndCut(stb,htb,srNJet, btb=(1,1) ,presel=presel)
      cname1pbCRtt, cut1pbCRtt =  nameAndCut(stb,htb,srNJet, btb=(1,-1) ,presel=presel)
      cname0bCRtt, cut0bCRtt =    nameAndCut(stb,htb,srNJet, btb=(0,0) ,presel=presel)
      cnameCRtt, cutCRtt =        nameAndCut(stb,htb,srNJet, btb=(0,-1) ,presel=presel)
      #rcs1bCRtt = getRCS(cEWK, cut1bCRtt, dPhiCut)
      #rcs0bCRtt = getRCS(cTTJets, cut0bCRtt, dPhiCut)
      samples0b = [{'chain':cWJets, 'cut':cutCRtt, 'weight':'weight*weightBTag0'}, {'chain':cTTJets, 'cut':cutCRtt, 'weight':'weight*weightBTag0'},{'chain':cDY, 'cut':cut0bCRtt, 'weight':'weight'},{'chain':cTTV, 'cut':cut0bCRtt, 'weight':'weight'},{'chain':csingleTop, 'cut':cut0bCRtt, 'weight':'weight'}]
      samples1b = [{'chain':cWJets, 'cut':cutCRtt, 'weight':'weight*weightBTag1_SF'}, {'chain':cTTJets, 'cut':cutCRtt, 'weight':'weight*weightBTag1_SF'},{'chain':cDY, 'cut':cut1bCRtt, 'weight':'weight'},{'chain':cTTV, 'cut':cut1bCRtt, 'weight':'weight'},{'chain':csingleTop, 'cut':cut1bCRtt, 'weight':'weight'}]
      samples1pb = [{'chain':cWJets, 'cut':cutCRtt, 'weight':'weight*weightBTag1p_SF'}, {'chain':cTTJets, 'cut':cutCRtt, 'weight':'weight*weightBTag1p_SF'},{'chain':cDY, 'cut':cut1pbCRtt, 'weight':'weight'},{'chain':cTTV, 'cut':cut1pbCRtt, 'weight':'weight'},{'chain':csingleTop, 'cut':cut1pbCRtt, 'weight':'weight'}]
      samples2b = [{'chain':cWJets, 'cut':cutCRtt, 'weight':'weight*weightBTag2p_SF'}, {'chain':cTTJets, 'cut':cutCRtt, 'weight':'weight*weightBTag2p_SF'},{'chain':cDY, 'cut':cut2bCRtt, 'weight':'weight'},{'chain':cTTV, 'cut':cut2bCRtt, 'weight':'weight'},{'chain':csingleTop, 'cut':cut2bCRtt, 'weight':'weight'}]
      #rcs0bCRtt_btag_EWK = combineRCS(samples0b, dPhiCut)
      rcs1bCRtt_btag_EWK = combineRCS(samples1b, dPhiCut)
      #rcs1bCRtt_btag_EWK = combineRCS(samples1pb, dPhiCut)
      rcs2bCRtt_btag_EWK = combineRCS(samples2b, dPhiCut)
      
      QCD0b_lowDPhi  = {'y':QCDestimate[(4,5)][stb][htb][(0,0)][dPhiCut]['NQCDpred_lowdPhi'],  'e':QCDestimate[(4,5)][stb][htb][(0,0)][dPhiCut]['NQCDpred_lowdPhi_err']}
      
      QCD1b_lowDPhi  = {'y':QCDestimate[(4,5)][stb][htb][(1,1)][dPhiCut]['NQCDpred_lowdPhi'],  'e':QCDestimate[(4,5)][stb][htb][(1,1)][dPhiCut]['NQCDpred_lowdPhi_err']}
      QCD1b_highDPhi = {'y':QCDestimate[(4,5)][stb][htb][(1,1)][dPhiCut]['NQCDpred_highdPhi'], 'e':QCDestimate[(4,5)][stb][htb][(1,1)][dPhiCut]['NQCDpred_highdPhi_err']}

      QCD2b_lowDPhi  = {'y':QCDestimate[(4,5)][stb][htb][(2,-1)][dPhiCut]['NQCDpred_lowdPhi'],  'e':QCDestimate[(4,5)][stb][htb][(2,-1)][dPhiCut]['NQCDpred_lowdPhi_err']}
      QCD2b_highDPhi = {'y':QCDestimate[(4,5)][stb][htb][(2,-1)][dPhiCut]['NQCDpred_highdPhi'], 'e':QCDestimate[(4,5)][stb][htb][(2,-1)][dPhiCut]['NQCDpred_highdPhi_err']}
      
      QCD1pb_lowDPhi = {'y':QCD1b_lowDPhi['y']+QCD2b_lowDPhi['y'], 'e':sqrt(QCD1b_lowDPhi['e']**2+QCD2b_lowDPhi['e']**2)}
      QCD1pb_highDPhi = {'y':QCD1b_highDPhi['y']+QCD2b_highDPhi['y'], 'e':sqrt(QCD1b_highDPhi['e']**2+QCD2b_highDPhi['e']**2)}
      
      QCD = [QCD1b_lowDPhi,QCD1b_highDPhi,QCD2b_lowDPhi,QCD2b_highDPhi, QCD1pb_lowDPhi, QCD1pb_highDPhi]
      
      for q in QCD:
        if isnan(q['e']):
          print 'found nan error value', q['e'], 'going to set error to 100%'
          q['e'] = q['y']
      
      #QCD1b_highDPhi = {'y':0.,'e':0.} #test of high deltaPhi QCD estimation
      rcs1bCR_data = getRCS(cData, cut1bCRtt, dPhiCut, QCD_lowDPhi=QCD1b_lowDPhi, QCD_highDPhi=QCD1b_highDPhi)
      #rcs1bCR_data = getRCS(cData, cut1pbCRtt, dPhiCut, QCD_lowDPhi=QCD1pb_lowDPhi, QCD_highDPhi=QCD1pb_highDPhi)
      rcs1bCR_data_noQCDcorr = getRCS(cData, cut1bCRtt, dPhiCut)
      rcs2bCR_data = getRCS(cData, cut2bCRtt, dPhiCut, QCD_lowDPhi=QCD2b_lowDPhi, QCD_highDPhi=QCD2b_highDPhi)
      rcs2bCR_data_noQCDcorr = getRCS(cData, cut2bCRtt, dPhiCut)
      print rcs1bCR_data
      print rcs2bCR_data

      #rcs0bCRtt_btag = getRCS(cTTJets, cutCRtt, dPhiCut, weight = 'weight*weightBTag0')
      rcs1bCRtt_btag = getRCS(cTTJets, cutCRtt, dPhiCut, weight = 'weight*weightBTag1')
      rcs1bCRtt_btag_dilep = getRCS(cTTJets, cutCRtt+'&&(ngenLep+ngenTau)==2', dPhiCut, weight = 'weight*weightBTag1')
      rcs1bCRtt_btag_semilep = getRCS(cTTJets, cutCRtt+'&&(ngenLep+ngenTau)==1', dPhiCut, weight = 'weight*weightBTag1')
      rcs1bCRtt_btag_had = getRCS(cTTJets, cutCRtt+'&&(ngenLep+ngenTau)==0', dPhiCut, weight = 'weight*weightBTag1')

      
      rcs1bCRtt_btag_Pos = rcs1bCRtt_btag_Neg = rcs1bCRtt_btag
      rcs1bCRW_btag = getRCS(cWJets, cutCRtt, dPhiCut, weight = 'weight*weightBTag1')
      rcs1bCRW_btag_Pos = getRCS(cWJets, cutCRtt+'&&leptonPdg>0', dPhiCut, weight = 'weight*weightBTag1')
      rcs1bCRW_btag_Neg = getRCS(cWJets, cutCRtt+'&&leptonPdg<0', dPhiCut, weight = 'weight*weightBTag1')
      rcs1bCRRest = getRCS(cRest, cut1bCRtt, dPhiCut)
      rcs1bCRRest_Pos = getRCS(cRest, cut1bCRtt+'&&leptonPdg>0', dPhiCut)
      rcs1bCRRest_Neg = getRCS(cRest, cut1bCRtt+'&&leptonPdg<0', dPhiCut)
      
      yield_1b_Pos = getYieldFromChain(cBkg, cut1bCRtt+'&&leptonPdg>0&&deltaPhi_Wl<'+str(dPhiCut))
      yield_1b_Neg = getYieldFromChain(cBkg, cut1bCRtt+'&&leptonPdg<0&&deltaPhi_Wl<'+str(dPhiCut))
      
      print 'Fraction pos pdg 1b MC truth:',yield_1b_Pos/(yield_1b_Pos+yield_1b_Neg)
      
      rcs2bCRtt_btag = getRCS(cTTJets, cutCRtt, dPhiCut, weight = 'weight*weightBTag2')
      ##Kappa now calculated only in the SB bin (4,5) jets 1b allEWK MC vs 0b tt MC - no fit applied for the moment!
      #kappaTT01 = divideRCSdict(rcs0bCRtt_btag,rcs1bCRtt_btag)
      kappaTT12 = divideRCSdict(rcs1bCRtt_btag,rcs2bCRtt_btag)
      
      if fitRescale:
        #create a b-tag fit in the ttbar SB (4-5jets) - not done in prediction
        fit = binnedNBTagsFit(cutCRtt+"&&"+dPhiStr+"<"+str(dPhiCut), cnameCRtt+'_dPhi'+str(dPhiCut), samples={'W':cWJets, 'TT':cTTJets, 'Rest':cRest, 'Bkg':cBkg, 'Data': cData}, prefix = cnameCRtt, QCD_dict={0:QCD0b_lowDPhi, 1:QCD1b_lowDPhi,2:QCD2b_lowDPhi})
        
        #get true yields in 1b from data
        y1b_data = getYieldFromChain(cData,cut1bCRtt+'&&deltaPhi_Wl<'+str(dPhiCut),weight='(1)')
        y1b_data_Pos = getYieldFromChain(cData,cut1bCRtt+'&&deltaPhi_Wl<'+str(dPhiCut)+'&&leptonPdg>0',weight='(1)')
        y1b_data_Neg = getYieldFromChain(cData,cut1bCRtt+'&&deltaPhi_Wl<'+str(dPhiCut)+'&&leptonPdg<0',weight='(1)')
        
        #get yields in 1b from fit in low dphi (otherwise looking into 0b search bin), QCD is already taken care of in fit
        y1b_Pos =fit['TT_AllPdg']['template'].GetBinContent(2)*fit['TT_AllPdg']['yield']*0.5+fit['W_PosPdg']['template'].GetBinContent(2)*fit['W_PosPdg']['yield']+fit['Rest_PosPdg']['template'].GetBinContent(2)*fit['Rest_PosPdg']['yield']
        y1b_Neg =fit['TT_AllPdg']['template'].GetBinContent(2)*fit['TT_AllPdg']['yield']*0.5+fit['W_NegPdg']['template'].GetBinContent(2)*fit['W_NegPdg']['yield']+fit['Rest_NegPdg']['template'].GetBinContent(2)*fit['Rest_NegPdg']['yield']
        y1b = y1b_Neg+y1b_Pos
        
        #obtain the fit fractions in data
        fitFracTT1b = getPropagatedError([fit['TT_AllPdg']['template'].GetBinContent(2),fit['TT_AllPdg']['yield']], [fit['TT_AllPdg']['template'].GetBinError(2),sqrt(fit['TT_AllPdg']['yieldVar'])],y1b, sqrt(y1b), returnCalcResult=True)
        fitFracTT1b_Pos = getPropagatedError([fit['TT_AllPdg']['template'].GetBinContent(2),fit['TT_AllPdg']['yield']*0.5], [fit['TT_AllPdg']['template'].GetBinError(2),sqrt(fit['TT_AllPdg']['yieldVar'])],y1b_Pos, sqrt(y1b_Pos), returnCalcResult=True)
        fitFracTT1b_Neg = getPropagatedError([fit['TT_AllPdg']['template'].GetBinContent(2),fit['TT_AllPdg']['yield']*0.5], [fit['TT_AllPdg']['template'].GetBinError(2),sqrt(fit['TT_AllPdg']['yieldVar'])],y1b_Neg, sqrt(y1b_Neg), returnCalcResult=True)
        fitFracW1b_Pos = getPropagatedError([fit['W_PosPdg']['template'].GetBinContent(2),fit['W_PosPdg']['yield']], [fit['W_PosPdg']['template'].GetBinError(2),sqrt(fit['W_PosPdg']['yieldVar'])],y1b_Pos, sqrt(y1b_Pos), returnCalcResult=True)
        fitFracW1b_Neg = getPropagatedError([fit['W_NegPdg']['template'].GetBinContent(2),fit['W_NegPdg']['yield']], [fit['W_NegPdg']['template'].GetBinError(2),sqrt(fit['W_NegPdg']['yieldVar'])],y1b_Neg, sqrt(y1b_Neg), returnCalcResult=True)
        fitFracRest1b_Pos = getPropagatedError([fit['Rest_PosPdg']['template'].GetBinContent(2),fit['Rest_PosPdg']['yield']], [fit['Rest_PosPdg']['template'].GetBinError(2),sqrt(fit['Rest_PosPdg']['yieldVar'])],y1b_Pos, sqrt(y1b_Pos), returnCalcResult=True)
        fitFracRest1b_Neg = getPropagatedError([fit['Rest_NegPdg']['template'].GetBinContent(2),fit['Rest_NegPdg']['yield']], [fit['Rest_NegPdg']['template'].GetBinError(2),sqrt(fit['Rest_NegPdg']['yieldVar'])],y1b_Neg, sqrt(y1b_Neg), returnCalcResult=True)
        print 'Pos fractions tt, W, Rest, QCD',fitFracTT1b_Pos,fitFracW1b_Pos,fitFracRest1b_Pos, QCD1b_lowDPhi['y']*0.5/y1b_Pos

        ##rescaling redundant now
        #fitFracTT1b_Pos_rescale = fitFracTT1b_Pos[0]/(fitFracTT1b_Pos[0]+fitFracW1b_Pos[0]+fitFracRest1b_Pos[0])
        #fitFracW1b_Pos_rescale = fitFracW1b_Pos[0]/(fitFracTT1b_Pos[0]+fitFracW1b_Pos[0]+fitFracRest1b_Pos[0])
        #fitFracRest1b_Pos_rescale = fitFracRest1b_Pos[0]/(fitFracTT1b_Pos[0]+fitFracW1b_Pos[0]+fitFracRest1b_Pos[0])
        #fitFracTT1b_Neg_rescale = fitFracTT1b_Neg[0]/(fitFracTT1b_Neg[0]+fitFracW1b_Neg[0]+fitFracRest1b_Neg[0])
        #fitFracW1b_Neg_rescale = fitFracW1b_Neg[0]/(fitFracTT1b_Neg[0]+fitFracW1b_Neg[0]+fitFracRest1b_Neg[0])
        #fitFracRest1b_Neg_rescale = fitFracRest1b_Neg[0]/(fitFracTT1b_Neg[0]+fitFracW1b_Neg[0]+fitFracRest1b_Neg[0])

        print 'Neg fractions tt, W, Rest, QCD',fitFracTT1b_Neg,fitFracW1b_Neg,fitFracRest1b_Neg, QCD1b_lowDPhi['y']*0.5/y1b_Neg
        print 'Frac pos, neg', y1b_Pos/y1b,y1b_Neg/y1b
        y2b_Pos =fit['TT_AllPdg']['template'].GetBinContent(3)*fit['TT_AllPdg']['yield']*0.5+fit['W_PosPdg']['template'].GetBinContent(3)*fit['W_PosPdg']['yield']+fit['Rest_PosPdg']['template'].GetBinContent(3)*fit['Rest_PosPdg']['yield']
        y2b_Neg =fit['TT_AllPdg']['template'].GetBinContent(3)*fit['TT_AllPdg']['yield']*0.5+fit['W_NegPdg']['template'].GetBinContent(3)*fit['W_NegPdg']['yield']+fit['Rest_NegPdg']['template'].GetBinContent(3)*fit['Rest_NegPdg']['yield']
        y2b = y2b_Neg+y2b_Pos
        fitFracTT2b = getPropagatedError([fit['TT_AllPdg']['template'].GetBinContent(3),fit['TT_AllPdg']['yield']], [fit['TT_AllPdg']['template'].GetBinError(3),sqrt(fit['TT_AllPdg']['yieldVar'])],y2b, sqrt(y2b), returnCalcResult=True)
        
        #get MC truth fractions
        TT1bMC = getYieldFromChain(cTTJets,cut1bCRtt+'&&deltaPhi_Wl<'+str(dPhiCut),returnError=True)
        TT1bMC_dilep = getYieldFromChain(cTTJets,cut1bCRtt+'&&deltaPhi_Wl<'+str(dPhiCut)+'&&(ngenLep+ngenTau)==2',returnError=True)
        TT1bMC_semilep = getYieldFromChain(cTTJets,cut1bCRtt+'&&deltaPhi_Wl<'+str(dPhiCut)+'&&(ngenLep+ngenTau)==1',returnError=True)
        TT1bMC_had = getYieldFromChain(cTTJets,cut1bCRtt+'&&deltaPhi_Wl<'+str(dPhiCut)+'&&(ngenLep+ngenTau)==0',returnError=True)

        W1bMC = getYieldFromChain(cWJets,cut1bCRtt+'&&deltaPhi_Wl<'+str(dPhiCut),returnError=True)
        Rest1bMC = getYieldFromChain(cRest,cut1bCRtt+'&&deltaPhi_Wl<'+str(dPhiCut),returnError=True)


        Total1bMC = getYieldFromChain(cBkg,cut1bCRtt+'&&deltaPhi_Wl<'+str(dPhiCut),returnError=True)
        TT2bMC = getYieldFromChain(cTTJets,cut2bCRtt+'&&deltaPhi_Wl<'+str(dPhiCut),returnError=True)
        Total2bMC = getYieldFromChain(cBkg,cut2bCRtt+'&&deltaPhi_Wl<'+str(dPhiCut),returnError=True)
        truthFracTT1bMC =  getPropagatedError(TT1bMC[0],TT1bMC[1],Total1bMC[0],Total1bMC[1],returnCalcResult=True)
        truthFracTT2bMC =  getPropagatedError(TT2bMC[0],TT2bMC[1],Total2bMC[0],Total2bMC[1],returnCalcResult=True)
        print
        print '***********************************************************'
        print 'ttbar fractions in data and MC'
        print 'ttbar fractions 1b/2b:', getValErrString(fitFracTT1b[0],fitFracTT1b[1]), ',', getValErrString(fitFracTT2b[0],fitFracTT2b[1])
        #print 'fit MC fractions 1b/2b:', fitFracTT1bMC,fitFracTT2bMC
        print 'truth MC fractions 1b/2b:', getValErrString(truthFracTT1bMC[0], truthFracTT1bMC[1]),',',getValErrString(truthFracTT2bMC[0],truthFracTT2bMC[1])
        print '***********************************************************'
        print
        frac[njb][stb][htb]['data'] = fitFracTT1b, fitFracTT2b
        frac[njb][stb][htb]['MCtruth'] = truthFracTT1bMC,truthFracTT2bMC 

        # get a rescaled version of the total Rcs value by weighting the constituents according to fit results in data
        rcs1bCR_MC_rescale = (y1b_Pos/y1b)*(fitFracTT1b_Pos[0]*rcs1bCRtt_btag_Pos['rCS']+fitFracW1b_Pos[0]*rcs1bCRW_btag_Pos['rCS']+fitFracRest1b_Pos[0]*rcs1bCRRest_Pos['rCS']) + (y1b_Neg/y1b)*(fitFracTT1b_Neg[0]*rcs1bCRtt_btag_Neg['rCS']+fitFracW1b_Neg[0]*rcs1bCRW_btag_Neg['rCS']+fitFracRest1b_Neg[0]*rcs1bCRRest_Neg['rCS'])
        
        # define the magnitude of dilep ttbar scaleing - use the histogram of the dilep control sample
        dilep_downscale = (1 - 0.25)
        #dilep_downscale = dilep_frac_hist.GetBinContent(b)
        #dilep_downscale = dilep_frac_hist.GetBinContent(b)*dilep_tt_frac_hist.GetBinContent(b)
        b += 1

        # get Rcs value for ttbar with semi- and dileptonic fractions rescaled according to measurements in dileptonic control sample
        rcs1bCR_MC_dilepRescale_tt = (rcs1bCRtt_btag_dilep['rCS']*TT1bMC_dilep[0]*dilep_downscale + rcs1bCRtt_btag_semilep['rCS']*(TT1bMC_semilep[0]+TT1bMC_dilep[0]*(1-dilep_downscale))+rcs1bCRtt_btag_had['rCS']*TT1bMC_had[0])/TT1bMC[0]

        # get the total Rcs value in MC using Rcs(ttbar) from above, and weighting the constituents according to fit results in data
        rcs1bCR_MC_dilepRescale = (y1b_Pos/y1b)*(fitFracTT1b_Pos[0]*rcs1bCR_MC_dilepRescale_tt+fitFracW1b_Pos[0]*rcs1bCRW_btag_Pos['rCS']+fitFracRest1b_Pos[0]*rcs1bCRRest_Pos['rCS']) + (y1b_Neg/y1b)*(fitFracTT1b_Neg[0]*rcs1bCR_MC_dilepRescale_tt+fitFracW1b_Neg[0]*rcs1bCRW_btag_Neg['rCS']+fitFracRest1b_Neg[0]*rcs1bCRRest_Neg['rCS'])

        #rcs1bCR_MC_dilepRescale = (rcs1bCR_MC_dilepRescale_tt*TT1bMC[0]+rcs1bCRW_btag['rCS']*W1bMC[0]+rcs1bCRRest['rCS']*Rest1bMC[0])/Total1bMC[0]

        print 'Rcs MC 1b before/after rescaling',round(rcs1bCRtt_btag_EWK['rCS'],3),',',round(rcs1bCR_MC_rescale ,3),',',round(rcs1bCR_MC_dilepRescale ,3)
        print
        frac[njb][stb][htb]['rcs1bEWK_MC'] = rcs1bCRtt_btag_EWK['rCS']
        frac[njb][stb][htb]['rcs1bEWK_MC_rescale'] = rcs1bCR_MC_rescale
      #rcs1bCRtt_btag['rCS']=rcs1bCRtt_btag['rCS']*fitFracTT1b
      #rcs2bCRtt_btag['rCS']=rcs2bCRtt_btag['rCS']*fitFracTT2b
      #kappaTT12_data = divideRCSdict(rcs1bCRtt_btag,rcs2bCRtt_btag)

      #kappaEWK01 = divideRCSdict(rcs0bCRtt_btag_EWK,rcs1bCRtt_btag_EWK)
      kappaEWK12 = divideRCSdict(rcs1bCRtt_btag_EWK,rcs2bCRtt_btag_EWK)
      
      #kappa01EWK.SetBinContent(i,kappaEWK01['kappa'])
      #kappa01EWK.SetBinError(i,kappaEWK01['kappaE_sim'])
      kappa12EWK.SetBinContent(i,kappaEWK12['kappa'])
      kappa12EWK.SetBinError(i,kappaEWK12['kappaE_sim'])
      #kappa0tt1ewk = divideRCSdict(rcs0bCRtt_btag,rcs1bCRtt_btag_EWK)

      kappa_data = divideRCSdict(rcs1bCR_data,rcs2bCR_data)
      kappa12data.SetBinContent(i,kappa_data['kappa'])
      kappa12data.SetBinError(i,kappa_data['kappaE_pred'])

      #kappa01TT.SetBinContent(i,kappaTT01['kappa'])
      #kappa01TT.SetBinError(i,kappaTT01['kappaE_sim'])
      kappa12TT.SetBinContent(i,kappaTT12['kappa'])
      kappa12TT.SetBinError(i,kappaTT12['kappaE_sim'])

      #kappa0tt1EWK.SetBinContent(i,kappa0tt1ewk['kappa'])
      #kappa0tt1EWK.SetBinError(i,kappa0tt1ewk['kappaE_sim'])
      
      #kappa01EWK.SetBinContent(i,kappaEWK01['kappa'])
      #kappa01EWK.SetBinError(i,kappaEWK01['kappaE_sim'])
      #kappa12EWK.SetBinContent(i,kappaEWK12['kappa'])
      #kappa12EWK.SetBinError(i,kappaEWK12['kappaE_sim'])

      #fit1bMC.SetBinContent  (i,truthFracTT1bMC[0])
      #fit1bMC.SetBinError    (i,truthFracTT1bMC[1])
      #
      #fit1bdata.SetBinContent(i,fitFracTT1b[0])
      #fit1bdata.SetBinError  (i,fitFracTT1b[1])
      #fit2bMC.SetBinContent  (i,truthFracTT2bMC[0])
      #fit2bMC.SetBinError    (i,truthFracTT2bMC[1])
      #fit2bdata.SetBinContent(i,fitFracTT2b[0])
      #fit2bdata.SetBinError  (i,fitFracTT2b[1])

      rcs1bMC.SetBinContent(i,rcs1bCRtt_btag_EWK['rCS'])
      rcs1bMC.SetBinError(i,rcs1bCRtt_btag_EWK['rCSE_sim'])
      
      # errors for rescaled Rcs values are not propagated yet
      #rcs1bMCrescale.SetBinContent(i,rcs1bCR_MC_rescale)
      #rcs1bMCrescale.SetBinError(i,rcs1bCRtt_btag_EWK['rCSE_sim'])
      #rcs1bMCrescaleD.SetBinContent(i,rcs1bCR_MC_dilepRescale)
      #rcs1bMCrescaleD.SetBinError(i,rcs1bCRtt_btag_EWK['rCSE_sim'])

      rcs1bdata.SetBinContent(i,rcs1bCR_data['rCS'])
      rcs1bdata.SetBinError(i,rcs1bCR_data['rCSE_pred'])
      rcs2bMC.SetBinContent(i,rcs2bCRtt_btag_EWK['rCS'])
      rcs2bMC.SetBinError(i,rcs2bCRtt_btag_EWK['rCSE_sim'])
      rcs2bdata.SetBinContent(i,rcs2bCR_data['rCS'])
      rcs2bdata.SetBinError(i,rcs2bCR_data['rCSE_pred'])
      
      rcs1bdata_noQCDcorr.SetBinContent(i,rcs1bCR_data_noQCDcorr['rCS'])
      rcs1bdata_noQCDcorr.SetBinError(i,rcs1bCR_data_noQCDcorr['rCSE_pred'])
      rcs2bdata_noQCDcorr.SetBinContent(i,rcs2bCR_data_noQCDcorr['rCS'])
      rcs2bdata_noQCDcorr.SetBinError(i,rcs2bCR_data_noQCDcorr['rCSE_pred'])
      
      #print 'Total Electroweak'
      #print '0b/1b:', round(kappaEWK01['kappa'],2),'+/-',round(kappaEWK01['kappaE_sim'],2)
      #print '1b/2b:', round(kappaEWK12['kappa'],2),'+/-',round(kappaEWK12['kappaE_sim'],2)
      #print 'Data'
      #print '1b/2b:', round(kappa_data['kappa'],2),'+/-',round(kappa_data['kappaE_sim'],2)
      #print 'Kappa factor used'
      #print '0b/1b:', round(kappa0tt1ewk['kappa'],2),'+/-',round(kappa0tt1ewk['kappaE_sim'],2)
      i += 1

rcs1bdata_noQCDcorr.SetLineWidth(2)
rcs2bdata_noQCDcorr.SetLineWidth(2)
rcs1bdata_noQCDcorr.SetLineColor(ROOT.kGreen+2)
rcs2bdata_noQCDcorr.SetLineColor(ROOT.kRed+2)
rcs1bdata_noQCDcorr.SetMarkerColor(ROOT.kGreen+2)
rcs2bdata_noQCDcorr.SetMarkerColor(ROOT.kRed+2)
rcs1bdata_noQCDcorr.SetMarkerStyle(rcs1bdata.GetMarkerStyle())
rcs2bdata_noQCDcorr.SetMarkerStyle(rcs2bdata.GetMarkerStyle())




#plot Rcs
setNiceBinLabel(rcs1bMC)
rcs1bMC.Draw('hist e1')
#rcs1bMCrescale.Draw('hist e1 same')
#rcs1bMCrescaleD.Draw('hist e1 same')
rcs1bdata.Draw('hist e1 same')
#rcs1bdata_noQCDcorr.Draw('hist e1 same')
#rcs2bdata_noQCDcorr.Draw('hist e1 same')


rcs2bMC.Draw('hist e1 same')
rcs2bdata.Draw('hist e1 same')


leg.AddEntry(rcs1bMC, '1b MC')
leg.AddEntry(rcs1bdata, '1b data')
#leg.AddEntry(rcs1bMCrescale, '1b MC fit scale')
#leg.AddEntry(rcs1bMCrescaleD, '1b MC dilep sc.')
leg.AddEntry(rcs2bMC, '2b MC')
leg.AddEntry(rcs2bdata, '2b data')
#leg.AddEntry(rcs1bdata_noQCDcorr, '1b data w/QCD')
#leg.AddEntry(rcs2bdata_noQCDcorr, '2b data w/QCD')

leg.Draw()

latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.04)
latex1.SetTextAlign(11)

latex1.DrawLatex(0.16,0.96,'CMS #bf{#it{preliminary}}')
latex1.DrawLatex(0.7,0.96,"L=2.1fb^{-1} (13TeV)")

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()


##plot fractions
#can_frac = ROOT.TCanvas('can_frac','can_frac',700,700)
#setNiceBinLabel(fit1bMC)
#fit1bMC.Draw('hist e1')
#fit1bdata.Draw('hist e1 same')
#fit2bMC.Draw('hist e1 same')
#fit2bdata.Draw('hist e1 same')
#
#
#leg2.AddEntry(fit1bMC, '1b MC')
#leg2.AddEntry(fit1bdata, '1b data')
#leg2.AddEntry(fit2bMC, '2b MC')
#leg2.AddEntry(fit2bdata, '2b data')
#leg2.Draw()
#
#latex1.DrawLatex(0.16,0.96,'CMS #bf{#it{preliminary}}')
#latex1.DrawLatex(0.7,0.96,"L=2.1fb^{-1} (13TeV)")

#plot kappas
can_kap = ROOT.TCanvas('can_kap','can_kap',700,700)
kappa12EWK.Draw('hist e1')
kappa12data.Draw('hist e1 same')

leg3.AddEntry(kappa12EWK, '#kappa (1b/2b) MC')
leg3.AddEntry(kappa12data, '#kappa (1b/2b) data')
leg3.Draw()

latex1.DrawLatex(0.16,0.96,'CMS #bf{#it{preliminary}}')
latex1.DrawLatex(0.7,0.96,"L=2.1fb^{-1} (13TeV)")
