import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v3 import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v4_PHYS14V1 import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v5_Phys14V2 import *
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName
from localInfo import username
from math import pi, sqrt

import os, copy, sys
sys.path.append('/afs/hephy.at/scratch/d/dhandl/CMSSW_7_2_3/src/Workspace/RA4Analysis/plotsDavid')
from binnedNBTagsFit import binnedNBTagsFit

lepSel = 'hard'
 
nBTagCMVA = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCMVA>0.732)' 
cWJets  = getChain(WJetsHTToLNu[lepSel],histname='')
cTTJets = getChain(ttJets[lepSel],histname='')
cRest = getChain([DY[lepSel], singleTop[lepSel], TTVH[lepSel]],histname='')#no QCD 
cBkg = getChain([WJetsHTToLNu[lepSel], ttJets[lepSel], DY[lepSel], singleTop[lepSel], TTVH[lepSel]],histname='')#no QCD
for c in [cWJets, cTTJets, cRest, cBkg]:
  c.SetAlias('nBTagCMVA', nBTagCMVA)

signals=[
          {'name':"T5qqqq_1200_1000_800", 'sample':SMS_T5qqqqWW_Gl1200_Chi1000_LSP800[lepSel]} , 
          {'name':"T5qqqq_1500_800_100",  'sample':SMS_T5qqqqWW_Gl1500_Chi800_LSP100[lepSel]},
          #{'name':"T1qqqq_1400_325_300",'sample':T1qqqq_1400_325_300}
        ]

for s in signals:
  s['chain']=getChain(s['sample'],histname='')

ROOT_colors = [ROOT.kBlack, ROOT.kRed-7, ROOT.kBlue-2, ROOT.kGreen+3, ROOT.kOrange+1,ROOT.kRed-3, ROOT.kAzure+6, ROOT.kCyan+3, ROOT.kOrange , ROOT.kRed-10]
dPhiStr = "acos((leptonPt+met*cos(leptonPhi-metPhi))/sqrt(leptonPt**2+met**2+2*met*leptonPt*cos(leptonPhi-metPhi)))"

#def nBTagStr(minPt=30, maxEta=2.4, minCMVATag=0.732):
#  return "Sum$(Jet_pt>"+str(minPt)+"&&abs(Jet_eta)<"+str(maxEta)+"&&Jet_id&&Jet_btagCMVA>"+str(minCMVATag)+")"

ROOT.TH1F().SetDefaultSumw2()
def getRCS(c, cut, dPhiCut):
  h = getPlotFromChain(c, dPhiStr, [0,dPhiCut,pi], cutString=cut, binningIsExplicit=True)
  if h.GetBinContent(1)>0 and h.GetBinContent(2)>0:
    rcs = h.GetBinContent(2)/h.GetBinContent(1)
    rCSE_sim = rcs*sqrt(h.GetBinError(2)**2/h.GetBinContent(2)**2 + h.GetBinError(1)**2/h.GetBinContent(1)**2)
    rCSE_pred = rcs*sqrt(1./h.GetBinContent(2)**2 + 1./h.GetBinContent(1)**2)
    del h
    return {'rCS':rcs, 'rCSE_pred':rCSE_pred, 'rCSE_sim':rCSE_sim}
  del h

#def getTTcorr(stb,htb,filename='hardSingleLeptonic_TTfitnjet_', dir='/afs/hephy.at/user/d/dhandl/www/pngCMG2/rCS/'):
#  binreg = nameAndCut(stb,htb,njetb=None)[0]
#  f0 = ROOT.TFile(dir+filename+binreg+'.root')
#  f1 = ROOT.TFile(dir+'hardSingleLeptonic_fullBkgFitnjet_'+binreg+'.root')
#  can0 = f0.Get('c1_n2')
#  can1 = f1.Get('c1_n2')
#  assert can0, 'Error: could not find TCanvas in '+str(f0)+str(f0.ls())
#  Profile_0b = can0.GetPrimitive('profile_rCS_njet_bTag0')
#  Profile_1b = can1.GetPrimitive('profile_rCS_njet_bTag1')
#  assert Profile_0b and Profile_1b,'Error: could not find TProfile'
#  FitPar0b = Profile_0b.GetFunction('pol0').GetParameter(0)
#  FitPar1b = Profile_1b.GetFunction('pol0').GetParameter(0)
#  FitParError0b = Profile_0b.GetFunction('pol0').GetParError(0)
#  FitParError1b = Profile_1b.GetFunction('pol0').GetParError(0)
#  assert Profile_0b.GetFunction('pol0') and Profile_1b.GetFunction('pol0'), 'Error: could not find Function'
#  k = FitPar0b/FitPar1b
#  k_E = k* sqrt(FitParError0b**2/FitPar0b**2 + FitParError1b**2/FitPar1b**2)
#  del f0
#  del f1
#  return {'k':k, 'k_Error':k_E}

#streg = [[(250, 350), 1.], [(350, 450), 1.], [(450, -1), 0.5]]
#htreg = [(400,500),(500,750),(750, 1000),(1000,-1)]
#njreg = [(1,1), (2,2),(3,3),(4,4),(5,5),(6,-1)]

prefix = 'chargeSep_singleLeptonic_20150213'
streg = [[(250, 350), 1.], [(350, -1), 1.]] 
htreg = [(500,750),(750,-1)]
njreg = [(5,5),(6,-1)]

#small = True
#if small:
#  streg = [(250,350),1.]
#  htreg = (500,750)
#  njreg = (6,-1)

#presel   ="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0"
#presel_0b="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0&&nBJetMedium25==0"
#presel    ="singleMuonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0"
presel    ="singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0"


#crNJet = (3,4)
crNJet = (2,3)
res = {}
for i_htb, htb in enumerate(htreg):
  res[htb] = {}
  for stb, dPhiCut in streg:
    res[htb][stb] = {}
    for srNJet in njreg:
      rd = {}
      #Signal region yield
#      srName, srCut = nameAndCut(stb,htb,srNJet, btb=None, presel=presel_0b) 
#      srYield = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight")
#      srYieldErr = sqrt(getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight*weight"))

      #TT Jets yield in crNJet, no b-tag cut, low DPhi
      fit_crName, fit_crCut = nameAndCut(stb,htb,crNJet,btb=None, presel=presel,btagVar = 'nBTagCMVA') 
      fit_crNJet_lowDPhi = binnedNBTagsFit(fit_crCut+"&&"+dPhiStr+"<"+str(dPhiCut), samples = {'W':cWJets, 'TT':cTTJets, 'Rest':cRest}, nBTagVar = 'nBTagCMVA' , prefix=fit_crName)
#      fit_crNJet_lowDPhi = binnedNBTagsFit(fit_crCut+"&&"+dPhiStr+"<"+str(dPhiCut), samples = {'W':cWJets, 'TT':cTTJets}, nBTagVar = 'nBJetMedium25', prefix=fit_crName)
      rd['fit_crNJet_lowDPhi'] = fit_crNJet_lowDPhi
      
#      print "Check: TT yield for W-correction: lowDPhi, ",fit_crNJet_lowDPhi['TT_AllPdg']['yield']*fit_crNJet_lowDPhi['TT_AllPdg']['template'].GetBinContent(1), getYieldFromChain(cTTJets, fit_crCut+"&&"+dPhiStr+"<"+str(dPhiCut)+"&&nBJetMedium25==0", weight = "weight")

      rCS_cr_Name_1b, rCS_cr_Cut_1b = nameAndCut(stb,htb,crNJet,btb=(1,1), presel=presel, btagVar = 'nBTagCMVA') 
      rCS_cr_Name_0b, rCS_cr_Cut_0b = nameAndCut(stb,htb,crNJet,btb=(0,0), presel=presel, btagVar = 'nBTagCMVA') 
      rCS_crNJet_1b = getRCS(cBkg, rCS_cr_Cut_1b,  dPhiCut) 
      rCS_crNJet_1b_onlyTT = getRCS(cTTJets, rCS_cr_Cut_1b,  dPhiCut) 
      rCS_crNJet_0b_onlyTT = getRCS(cTTJets, rCS_cr_Cut_0b,  dPhiCut) 
#      print "Check: rCS(TT) for W-correction: all samples, ",rCS_crNJet_1b,"only TT",rCS_crNJet_1b_onlyTT,'cut',rCS_cr_Cut_1b
      rd['rCS_crNJet_1b'] = rCS_crNJet_1b
      rd['rCS_crNJet_1b_onlyTT'] = rCS_crNJet_1b_onlyTT
      rd['rCS_crNJet_0b_onlyTT'] = rCS_crNJet_0b_onlyTT

      #low njet CR: crNJet, 0-btags, low DPhi
      crName, crCut = nameAndCut(stb,htb,crNJet,btb=(0,0), presel=presel, btagVar='nBTagCMVA') 

      yTT_crNJet_0b_lowDPhi         = fit_crNJet_lowDPhi['TT_AllPdg']['yield']*fit_crNJet_lowDPhi['TT_AllPdg']['template'].GetBinContent(1)
      yTT_Var_crNJet_0b_lowDPhi     = fit_crNJet_lowDPhi['TT_AllPdg']['yieldVar']*fit_crNJet_lowDPhi['TT_AllPdg']['template'].GetBinContent(1)**2
      yTT_crNJet_0b_highDPhi        = rCS_crNJet_1b['rCS']*yTT_crNJet_0b_lowDPhi
      yTT_Var_crNJet_0b_highDPhi    = rCS_crNJet_1b['rCSE_pred']**2*yTT_crNJet_0b_lowDPhi**2 + rCS_crNJet_1b['rCS']**2*yTT_Var_crNJet_0b_lowDPhi
      yTT_crNJet_0b_lowDPhi_truth   = getYieldFromChain(cTTJets, crCut+"&&"+dPhiStr+"<"+str(dPhiCut), weight = "weight")
      yTT_crNJet_0b_highDPhi_truth  = getYieldFromChain(cTTJets, crCut+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight")
      rd['yTT_crNJet_0b_lowDPhi']          =  yTT_crNJet_0b_lowDPhi         
      rd['yTT_Var_crNJet_0b_lowDPhi']      =  yTT_Var_crNJet_0b_lowDPhi     
      rd['yTT_crNJet_0b_highDPhi']         =  yTT_crNJet_0b_highDPhi        
      rd['yTT_Var_crNJet_0b_highDPhi']     =  yTT_Var_crNJet_0b_highDPhi    
      rd['yTT_crNJet_0b_lowDPhi_truth']    =  yTT_crNJet_0b_lowDPhi_truth   
      rd['yTT_crNJet_0b_highDPhi_truth']   =  yTT_crNJet_0b_highDPhi_truth  

#      print "Check: Impact of TT on RCS(W)"
#      print "Subtract numerator  ", yTT_crNJet_0b_highDPhi,'(rcs=',rCS_crNJet_1b['rCS'],'yield_0b',yTT_crNJet_0b_lowDPhi,') true',yTT_crNJet_0b_highDPhi_truth
#      print "Subtract denominator", yTT_crNJet_0b_lowDPhi,'true', yTT_crNJet_0b_lowDPhi_truth
    
      #calculate corrected rCS for W
      y_crNJet_0b_highDPhi     = getYieldFromChain(cBkg, crCut+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight")
      y_Var_crNJet_0b_highDPhi = getYieldFromChain(cBkg, crCut+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight*weight")
      y_crNJet_0b_lowDPhi      = getYieldFromChain(cBkg, crCut+"&&"+dPhiStr+"<"+str(dPhiCut), weight = "weight")
      y_Var_crNJet_0b_lowDPhi  = getYieldFromChain(cBkg, crCut+"&&"+dPhiStr+"<"+str(dPhiCut), weight = "weight*weight")
      rCS_W_crNJet_0b_corr     = (y_crNJet_0b_highDPhi - yTT_crNJet_0b_highDPhi)/(y_crNJet_0b_lowDPhi - yTT_crNJet_0b_lowDPhi)
      rCS_Var_W_crNJet_0b_corr = rCS_W_crNJet_0b_corr**2*(\
          (y_Var_crNJet_0b_highDPhi + yTT_Var_crNJet_0b_highDPhi)/(y_crNJet_0b_highDPhi - yTT_crNJet_0b_highDPhi)**2 
         +(y_Var_crNJet_0b_lowDPhi + yTT_Var_crNJet_0b_lowDPhi)/(y_crNJet_0b_lowDPhi - yTT_crNJet_0b_lowDPhi)**2
          )
      rCS_W_crNJet_0b_notcorr     = (y_crNJet_0b_highDPhi )/(y_crNJet_0b_lowDPhi )
      rCS_Var_W_crNJet_0b_notcorr = rCS_W_crNJet_0b_notcorr**2*( (y_Var_crNJet_0b_highDPhi )/(y_crNJet_0b_highDPhi)**2 + (y_Var_crNJet_0b_lowDPhi)/(y_crNJet_0b_lowDPhi)**2 )

      #calculate corrected rCS(+-) for W(+-) [because of yTT is symmetric in charge one have to subtract 0.5*yTT]
      #PosPdg
      y_crNJet_0b_highDPhi_PosPdg     = getYieldFromChain(cBkg, 'leptonPdg>0&&'+crCut+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight")
      y_Var_crNJet_0b_highDPhi_PosPdg = getYieldFromChain(cBkg, 'leptonPdg>0&&'+crCut+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight*weight")
      y_crNJet_0b_lowDPhi_PosPdg      = getYieldFromChain(cBkg, 'leptonPdg>0&&'+crCut+"&&"+dPhiStr+"<"+str(dPhiCut), weight = "weight")
      y_Var_crNJet_0b_lowDPhi_PosPdg  = getYieldFromChain(cBkg, 'leptonPdg>0&&'+crCut+"&&"+dPhiStr+"<"+str(dPhiCut), weight = "weight*weight")
      rCS_W_PosPdg_crNJet_0b_corr     = (y_crNJet_0b_highDPhi_PosPdg - (0.5*yTT_crNJet_0b_highDPhi))/(y_crNJet_0b_lowDPhi_PosPdg - (0.5*yTT_crNJet_0b_lowDPhi))
      rCS_Var_W_PosPdg_crNJet_0b_corr = rCS_W_PosPdg_crNJet_0b_corr**2*(\
          (y_Var_crNJet_0b_highDPhi_PosPdg + (0.5*yTT_Var_crNJet_0b_highDPhi))/(y_crNJet_0b_highDPhi_PosPdg - (0.5*yTT_crNJet_0b_highDPhi))**2 
         +(y_Var_crNJet_0b_lowDPhi_PosPdg + (0.5*yTT_Var_crNJet_0b_lowDPhi))/(y_crNJet_0b_lowDPhi_PosPdg - (0.5*yTT_crNJet_0b_lowDPhi))**2
          )
      rCS_W_PosPdg_crNJet_0b_notcorr     = (y_crNJet_0b_highDPhi_PosPdg )/(y_crNJet_0b_lowDPhi_PosPdg )
      rCS_Var_W_PosPdg_crNJet_0b_notcorr = rCS_W_PosPdg_crNJet_0b_notcorr**2*( (y_Var_crNJet_0b_highDPhi_PosPdg )/(y_crNJet_0b_highDPhi_PosPdg)**2 + (y_Var_crNJet_0b_lowDPhi_PosPdg)/(y_crNJet_0b_lowDPhi_PosPdg)**2 )
      #NegPdg
      y_crNJet_0b_highDPhi_NegPdg     = getYieldFromChain(cBkg, 'leptonPdg<0&&'+crCut+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight")
      y_Var_crNJet_0b_highDPhi_NegPdg = getYieldFromChain(cBkg, 'leptonPdg<0&&'+crCut+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight*weight")
      y_crNJet_0b_lowDPhi_NegPdg      = getYieldFromChain(cBkg, 'leptonPdg<0&&'+crCut+"&&"+dPhiStr+"<"+str(dPhiCut), weight = "weight")
      y_Var_crNJet_0b_lowDPhi_NegPdg  = getYieldFromChain(cBkg, 'leptonPdg<0&&'+crCut+"&&"+dPhiStr+"<"+str(dPhiCut), weight = "weight*weight")
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

#      print "Check RCS for W (corrected for TT):",rCS_W_crNJet_0b_corr,"true",getRCS(cWJets, crCut,  dPhiCut)['rCS'],'uncorrected',getRCS(cBkg, crCut,  dPhiCut)['rCS']

      #TT Jets yield in srNJet, no b-tag cut, low DPhi
      fit_srName, fit_srCut = nameAndCut(stb,htb,srNJet,btb=None, presel=presel,btagVar = 'nBTagCMVA') 
      fit_srNJet_lowDPhi = binnedNBTagsFit(fit_srCut+"&&"+dPhiStr+"<"+str(dPhiCut), samples = {'W':cWJets, 'TT':cTTJets, 'Rest':cRest}, nBTagVar = 'nBTagCMVA', prefix=fit_srName)
#      fit_srNJet_lowDPhi = binnedNBTagsFit(fit_srCut+"&&"+dPhiStr+"<"+str(dPhiCut), samples = {'W':cWJets, 'TT':cTTJets}, nBTagVar = 'nBJetMedium25', prefix=fit_srName)

      rd['fit_srNJet_lowDPhi'] = fit_srNJet_lowDPhi
#      print "Check: Impact of TT on RCS(W)"
#      print "Subtract numerator  ", yTT_crNJet_0b_highDPhi,'(rcs=',rCS_crNJet_1b['rCS'],'yield_0b',yTT_crNJet_0b_lowDPhi,') true',yTT_crNJet_0b_highDPhi_truth
#      print "Subtract denominator", yTT_crNJet_0b_lowDPhi,'true', yTT_crNJet_0b_lowDPhi_truth

      yTT_srNJet_0b_lowDPhi =  fit_srNJet_lowDPhi['TT_AllPdg']['yield']*fit_srNJet_lowDPhi['TT_AllPdg']['template'].GetBinContent(1)
      yTT_Var_srNJet_0b_lowDPhi =  fit_srNJet_lowDPhi['TT_AllPdg']['yieldVar']*fit_srNJet_lowDPhi['TT_AllPdg']['template'].GetBinContent(1)**2
      yW_srNJet_0b_lowDPhi  =  fit_srNJet_lowDPhi['W_PosPdg']['yield']*fit_srNJet_lowDPhi['W_PosPdg']['template'].GetBinContent(1)\
                            +  fit_srNJet_lowDPhi['W_NegPdg']['yield']*fit_srNJet_lowDPhi['W_NegPdg']['template'].GetBinContent(1)
      yW_Var_srNJet_0b_lowDPhi  =  fit_srNJet_lowDPhi['W_PosPdg']['yieldVar']*fit_srNJet_lowDPhi['W_PosPdg']['template'].GetBinContent(1)**2\
                                +  fit_srNJet_lowDPhi['W_NegPdg']['yieldVar']*fit_srNJet_lowDPhi['W_NegPdg']['template'].GetBinContent(1)**2#FIXME I add that uncorrelated
      yW_PosPdg_srNJet_0b_lowDPhi = fit_srNJet_lowDPhi['W_PosPdg']['yield']*fit_srNJet_lowDPhi['W_PosPdg']['template'].GetBinContent(1)
      yW_NegPdg_srNJet_0b_lowDPhi = fit_srNJet_lowDPhi['W_NegPdg']['yield']*fit_srNJet_lowDPhi['W_NegPdg']['template'].GetBinContent(1)
      yW_PosPdg_Var_srNJet_0b_lowDPhi = fit_srNJet_lowDPhi['W_PosPdg']['yieldVar']*fit_srNJet_lowDPhi['W_PosPdg']['template'].GetBinContent(1)**2
      yW_NegPdg_Var_srNJet_0b_lowDPhi = fit_srNJet_lowDPhi['W_NegPdg']['yieldVar']*fit_srNJet_lowDPhi['W_NegPdg']['template'].GetBinContent(1)**2

      rCS_sr_Name_1b, rCS_sr_Cut_1b = nameAndCut(stb,htb,srNJet,btb=(1,1), presel=presel, btagVar = 'nBTagCMVA') 
      rCS_crLowNJet_Name_1b, rCS_crLowNJet_Cut_1b = nameAndCut(stb,htb,(4,5),btb=(1,1), presel=presel, btagVar = 'nBTagCMVA') 
      rCS_sr_Name_0b, rCS_sr_Cut_0b = nameAndCut(stb,htb,srNJet,btb=(0,0), presel=presel, btagVar = 'nBTagCMVA')#for Check 
      rCS_srNJet_1b = getRCS(cBkg, rCS_sr_Cut_1b,  dPhiCut) 
      rCS_crLowNJet_1b = getRCS(cBkg, rCS_crLowNJet_Cut_1b,  dPhiCut) #Low njet tt-jets CR to be orthoganl to DPhi 
      rCS_srNJet_1b_onlyTT = getRCS(cTTJets, rCS_sr_Cut_1b,  dPhiCut) 
      rCS_crLowNJet_1b_onlyTT = getRCS(cTTJets, rCS_crLowNJet_Cut_1b,  dPhiCut) 
      rCS_srNJet_0b_onlyTT = getRCS(cTTJets, rCS_sr_Cut_0b,  dPhiCut) #for check
      rCS_srNJet_0b_onlyW = getRCS(cWJets, rCS_sr_Cut_0b,  dPhiCut) #for check
      rCS_srNJet_0b_onlyW_PosPdg = getRCS(cWJets, 'leptonPdg>0&&'+rCS_sr_Cut_0b,  dPhiCut) #for check
      rCS_srNJet_0b_onlyW_NegPdg = getRCS(cWJets, 'leptonPdg<0&&'+rCS_sr_Cut_0b,  dPhiCut) #for check
      rd['yTT_srNJet_0b_lowDPhi'] = yTT_srNJet_0b_lowDPhi
      rd['yTT_Var_srNJet_0b_lowDPhi'] = yTT_Var_srNJet_0b_lowDPhi
      rd['yW_srNJet_0b_lowDPhi'] = yW_srNJet_0b_lowDPhi  
      rd['yW_Var_srNJet_0b_lowDPhi'] = yW_Var_srNJet_0b_lowDPhi 
      rd['yW_PosPdg_srNJet_0b_lowDPhi'] = yW_PosPdg_srNJet_0b_lowDPhi
      rd['yW_PosPdg_Var_srNJet_0b_lowDPhi'] = yW_PosPdg_Var_srNJet_0b_lowDPhi
      rd['yW_NegPdg_srNJet_0b_lowDPhi'] = yW_NegPdg_srNJet_0b_lowDPhi
      rd['yW_NegPdg_Var_srNJet_0b_lowDPhi'] = yW_NegPdg_Var_srNJet_0b_lowDPhi
      rd['rCS_srNJet_1b'] = rCS_srNJet_1b
      rd['rCS_srNJet_1b_onlyTT'] = rCS_srNJet_1b_onlyTT
      rd['rCS_crLowNJet_1b'] = rCS_crLowNJet_1b
      rd['rCS_crLowNJet_1b_onlyTT'] = rCS_crLowNJet_1b_onlyTT
      rd['rCS_srNJet_0b_onlyTT'] = rCS_srNJet_0b_onlyTT
      rd['rCS_srNJet_0b_onlyW'] = rCS_srNJet_0b_onlyW
      rd['rCS_srNJet_0b_onlyW_PosPdg'] = rCS_srNJet_0b_onlyW_PosPdg
      rd['rCS_srNJet_0b_onlyW_NegPdg'] = rCS_srNJet_0b_onlyW_NegPdg

      print "Check: rCS(TT) for TT estimate: all samples, ",rCS_srNJet_1b['rCS'],"only TT",rCS_srNJet_1b_onlyTT['rCS'],'onlyTT and 0b',rCS_srNJet_0b_onlyTT['rCS']

      #true yields measured from MC samples
      truth_TT        = getYieldFromChain(cTTJets, rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight")
      truth_TT_var    = getYieldFromChain(cTTJets, rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight*weight")
      truth_W         = getYieldFromChain(cWJets,  rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight")
      truth_W_var     = getYieldFromChain(cWJets,  rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight*weight")
      truth_Rest      = getYieldFromChain(cRest,   rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight")
      truth_Rest_var  = getYieldFromChain(cRest,   rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight*weight")

      truth_W_PosPdg         = getYieldFromChain(cWJets, 'leptonPdg>0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight")
      truth_W_var_PosPdg     = getYieldFromChain(cWJets, 'leptonPdg>0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight*weight")
      truth_W_NegPdg         = getYieldFromChain(cWJets, 'leptonPdg<0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight")
      truth_W_var_NegPdg     = getYieldFromChain(cWJets, 'leptonPdg<0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight*weight")
      truth_Rest_PosPdg      = getYieldFromChain(cRest,  'leptonPdg>0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight")
      truth_Rest_var_PosPdg  = getYieldFromChain(cRest,  'leptonPdg>0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight*weight")
      truth_Rest_NegPdg      = getYieldFromChain(cRest,  'leptonPdg<0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight")
      truth_Rest_var_NegPdg  = getYieldFromChain(cRest,  'leptonPdg<0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight*weight")

      #predicted yields with RCS method
      #ttJetsCRForRCS = rCS_srNJet_1b   #Version as of Nov. 11th 
      ttJetsCRForRCS = rCS_crLowNJet_1b #New version, orthogonal to DPhi (lower njet region in 1b-tag bin)
#      kFactor = getTTcorr(stb,htb)
#      pred_TT    = yTT_srNJet_0b_lowDPhi*ttJetsCRForRCS['rCS']*kFactor['k']
#      pred_Var_TT= yTT_Var_srNJet_0b_lowDPhi*ttJetsCRForRCS['rCS']**2*kFactor['k']**2 + yTT_srNJet_0b_lowDPhi**2*ttJetsCRForRCS['rCSE_pred']**2*kFactor['k']**2 + yTT_srNJet_0b_lowDPhi**2*ttJetsCRForRCS['rCS']**2*kFactor['k_Error']**2
      pred_TT    = yTT_srNJet_0b_lowDPhi*ttJetsCRForRCS['rCS']
      pred_Var_TT= yTT_Var_srNJet_0b_lowDPhi*ttJetsCRForRCS['rCS']**2 + yTT_srNJet_0b_lowDPhi**2*ttJetsCRForRCS['rCSE_pred']**2
      pred_W     = yW_srNJet_0b_lowDPhi*rCS_W_crNJet_0b_corr
      pred_Var_W = yW_Var_srNJet_0b_lowDPhi*rCS_W_crNJet_0b_corr**2 + yW_srNJet_0b_lowDPhi**2*rCS_Var_W_crNJet_0b_corr

      pred_W_PosPdg     = yW_PosPdg_srNJet_0b_lowDPhi*rCS_W_PosPdg_crNJet_0b_corr
      pred_Var_W_PosPdg = yW_PosPdg_Var_srNJet_0b_lowDPhi*rCS_W_PosPdg_crNJet_0b_corr**2 + yW_PosPdg_srNJet_0b_lowDPhi**2*rCS_Var_W_PosPdg_crNJet_0b_corr
      pred_W_NegPdg     = yW_NegPdg_srNJet_0b_lowDPhi*rCS_W_NegPdg_crNJet_0b_corr
      pred_Var_W_NegPdg = yW_NegPdg_Var_srNJet_0b_lowDPhi*rCS_W_NegPdg_crNJet_0b_corr**2 + yW_NegPdg_srNJet_0b_lowDPhi**2*rCS_Var_W_NegPdg_crNJet_0b_corr

      pred_total = pred_TT + pred_W + truth_Rest
      pred_total_PosPdg = (0.5*pred_TT) + pred_W_PosPdg + truth_Rest_PosPdg
      pred_total_NegPdg = (0.5*pred_TT) + pred_W_NegPdg + truth_Rest_NegPdg
      pred_Var_total = pred_Var_TT + pred_Var_W + truth_Rest_var
      pred_Var_total_PosPdg = (0.5*pred_Var_TT) + pred_Var_W_PosPdg + truth_Rest_var_PosPdg
      pred_Var_total_NegPdg = (0.5*pred_Var_TT) + pred_Var_W_NegPdg + truth_Rest_var_NegPdg 

      print "TT",pred_TT,sqrt(pred_Var_TT),'truth',truth_TT
      print "W",pred_W,sqrt(pred_Var_W),'truth',truth_W
      print "W(-)",pred_W_PosPdg,sqrt(pred_Var_W_PosPdg),'truth',truth_W_PosPdg
      print "W(+)",pred_W_NegPdg,sqrt(pred_Var_W_NegPdg),'truth',truth_W_NegPdg
      print "Total",pred_total,sqrt(pred_Var_total),'truth',truth_TT+truth_W + truth_Rest
      print "Total PosPdg",pred_total_PosPdg,sqrt(pred_Var_total_PosPdg),'truth',(0.5*truth_TT)+truth_W_PosPdg+truth_Rest_PosPdg      
      print "Total NegPdg",pred_total_NegPdg,sqrt(pred_Var_total_NegPdg),'truth',(0.5*truth_TT)+truth_W_NegPdg+truth_Rest_NegPdg

#Attention: Variances of Total Pos/NegPdg are not yet included!!! I calculated it with total TT Bkg
      rd.update( {#'kFactorTT':kFactor,\
                  'TT_pred':pred_TT,"TT_pred_err":sqrt(pred_Var_TT),\
                  "TT_truth":truth_TT,"TT_truth_err":sqrt(truth_TT_var),\
                  "W_pred":pred_W,"W_pred_err":sqrt(pred_Var_W), \
                  "W_truth":truth_W,"W_truth_err":sqrt(truth_W_var),\
                  "W_PosPdg_pred":pred_W_PosPdg,"W_PosPdg_pred_err":sqrt(pred_Var_W_PosPdg),\
                  "W_PosPdg_truth":truth_W_PosPdg,"W_PosPdg_truth_err":sqrt(truth_W_var_PosPdg),\
                  "W_NegPdg_pred":pred_W_NegPdg,"W_NegPdg_pred_err":sqrt(pred_Var_W_NegPdg),\
                  "W_NegPdg_truth":truth_W_NegPdg,"W_NegPdg_truth_err":sqrt(truth_W_var_NegPdg),\
                  'Rest_truth':truth_Rest,'Rest_truth_err':sqrt(truth_Rest_var),\
                  'Rest_PosPdg_truth':truth_Rest_PosPdg,'Rest_PosPdg_truth_err':sqrt(truth_Rest_var_PosPdg),\
                  'Rest_NegPdg_truth':truth_Rest_NegPdg,'Rest_NegPdg_truth_err':sqrt(truth_Rest_var_NegPdg),\
                  'tot_pred':pred_total,'tot_pred_err':sqrt(pred_Var_total),\
                  'tot_PosPdg_pred':pred_total_PosPdg,'tot_PosPdg_pred_err':sqrt(pred_Var_total_PosPdg),\
                  'tot_NegPdg_pred':pred_total_NegPdg,'tot_NegPdg_pred_err':sqrt(pred_Var_total_NegPdg),\
                  'tot_truth':truth_TT+truth_W+truth_Rest,'tot_truth_err':sqrt(truth_TT_var + truth_W_var + truth_Rest_var),\
                  'tot_PosPdg_truth':(0.5*truth_TT)+truth_W_PosPdg+truth_Rest_PosPdg,'tot_PosPdg_truth_err':sqrt((0.5*truth_TT_var) + truth_W_var_PosPdg + truth_Rest_var_PosPdg),\
                  'tot_NegPdg_truth':(0.5*truth_TT)+truth_W_NegPdg+truth_Rest_NegPdg,'tot_NegPdg_truth_err':sqrt((0.5*truth_TT_var) + truth_W_var_NegPdg + truth_Rest_var_NegPdg)})
      res[htb][stb][srNJet] = rd


pickle.dump(res, file('/data/'+username+'/results2014/rCS_0b/'+prefix+'_estimationResults_pkl','w'))

res = pickle.load(file('/data/'+username+'/results2014/rCS_0b/'+prefix+'_estimationResults_pkl'))

def getNumString(n,ne, acc=2):
  return str(round(n,acc))+'&$\pm$&'+str(round(ne,acc))

print "Results"
print
for i_htb, htb in enumerate(htreg):
  if i_htb!=0:print '\\hline'
  print '& & \multicolumn{6}{c|}{$t\overline{t}$+Jets}&\multicolumn{6}{c|}{$W$+Jets}&\multicolumn{6}{c}{total}\\\\'
  print '\multicolumn{2}{c|}{$'+varBinName(htb, 'H_{T}')+\
        '$} & \multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c}{simulation}\\\\\\hline'
  for stb, dPhiCut in streg:
    for srNJet in njreg:
      print '$'+nJetBinName(srNJet)+'$ & $'+varBinName(stb, 'S_{T}')+'$'+' & '+getNumString(res[htb][stb][srNJet]['TT_pred'], res[htb][stb][srNJet]['TT_pred_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['TT_truth'], res[htb][stb][srNJet]['TT_truth_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['W_pred'], res[htb][stb][srNJet]['W_pred_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['W_truth'], res[htb][stb][srNJet]['W_truth_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['tot_pred'], res[htb][stb][srNJet]['tot_pred_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['tot_truth'], res[htb][stb][srNJet]['tot_truth_err']) +'\\\\'
print

for i_htb, htb in enumerate(htreg):
  if i_htb!=0:print '\\hline'
  print '& & \multicolumn{6}{c|}{$W+$ Jets}&\multicolumn{6}{c|}{$W-$ Jets}&\multicolumn{6}{c}{$W$ Jets}\\\\'
  print '\multicolumn{2}{c|}{$'+varBinName(htb, 'H_{T}')+\
        '$} & \multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c}{simulation}\\\\\\hline'
  for stb, dPhiCut in streg:
    for srNJet in njreg:
      print '$'+nJetBinName(srNJet)+'$ & $'+varBinName(stb, 'S_{T}')+'$'+' & '+getNumString(res[htb][stb][srNJet]['W_NegPdg_pred'], res[htb][stb][srNJet]['W_NegPdg_pred_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['W_NegPdg_truth'], res[htb][stb][srNJet]['W_NegPdg_truth_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['W_PosPdg_pred'], res[htb][stb][srNJet]['W_PosPdg_pred_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['W_PosPdg_truth'], res[htb][stb][srNJet]['W_PosPdg_truth_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['W_pred'], res[htb][stb][srNJet]['W_pred_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['W_truth'], res[htb][stb][srNJet]['W_truth_err']) +'\\\\'
print
for i_htb, htb in enumerate(htreg):
  if i_htb!=0:print '\\hline'
  print '& & \multicolumn{6}{c|}{total (+ charge)}&\multicolumn{6}{c|}{total (- charge)}&\multicolumn{6}{c}{total}\\\\'
  print '\multicolumn{2}{c|}{$'+varBinName(htb, 'H_{T}')+\
        '$} & \multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c}{simulation}\\\\\\hline'
  for stb, dPhiCut in streg:
    for srNJet in njreg:
      print '$'+nJetBinName(srNJet)+'$ & $'+varBinName(stb, 'S_{T}')+'$'+' & '+getNumString(res[htb][stb][srNJet]['tot_NegPdg_pred'], res[htb][stb][srNJet]['tot_NegPdg_pred_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['tot_NegPdg_truth'], res[htb][stb][srNJet]['tot_NegPdg_truth_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['tot_PosPdg_pred'], res[htb][stb][srNJet]['tot_PosPdg_pred_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['tot_PosPdg_truth'], res[htb][stb][srNJet]['tot_PosPdg_truth_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['tot_pred'], res[htb][stb][srNJet]['tot_pred_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['tot_truth'], res[htb][stb][srNJet]['tot_truth_err']) +'\\\\'
print
print 'residual Backgrounds'
print
for i_htb, htb in enumerate(htreg):
  if i_htb!=0:print '\\hline'
  print '& & \multicolumn{3}{c|}{other Background (+ charge)}&\multicolumn{3}{c|}{other Background (- charge)}&\multicolumn{3}{c}{other Background}\\\\'
  print '\multicolumn{2}{c|}{$'+varBinName(htb, 'H_{T}')+\
        '$} & &\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{simulation}\\\\\\hline'
  for stb, dPhiCut in streg:
    for srNJet in njreg:
      print '$'+nJetBinName(srNJet)+'$ & $'+varBinName(stb, 'S_{T}')+'$'+' & '+getNumString(res[htb][stb][srNJet]['Rest_NegPdg_truth'], res[htb][stb][srNJet]['Rest_NegPdg_truth_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['Rest_PosPdg_truth'], res[htb][stb][srNJet]['Rest_PosPdg_truth_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['Rest_truth'], res[htb][stb][srNJet]['Rest_truth_err']) +'\\\\'
print

print "rCS(TT) comparison used for rCS(W) correction"
print
for i_htb, htb in enumerate(htreg):
  for stb, dPhiCut in streg:
    for srNJet in njreg[:1]:
      print '$'+varBinName(htb, 'H_{T}')+'$&$'+varBinName(stb, 'S_{T}')+'$ & '+\
          ' & '.join([getNumString(res[htb][stb][srNJet]['rCS_crNJet_1b']['rCS'], res[htb][stb][srNJet]['rCS_crNJet_1b']['rCSE_sim'],3), \
                      getNumString(res[htb][stb][srNJet]['rCS_crNJet_1b_onlyTT']['rCS'], res[htb][stb][srNJet]['rCS_crNJet_1b_onlyTT']['rCSE_sim'],3),\
                      getNumString(res[htb][stb][srNJet]['rCS_crNJet_0b_onlyTT']['rCS'], res[htb][stb][srNJet]['rCS_crNJet_0b_onlyTT']['rCSE_sim'],3)])+'\\\\'
print

print "RCS corr comparison" 
print
for i_htb, htb in enumerate(htreg):
  for stb, dPhiCut in streg:
    print '$'+varBinName(htb, 'H_{T}')+'$&$'+varBinName(stb, 'S_{T}')+'$ & '+\
        ' & '.join([getNumString(res[htb][stb][njreg[0]]['rCS_W_crNJet_0b_corr'],sqrt(res[htb][stb][njreg[0]]['rCS_Var_W_crNJet_0b_corr']),4), \
                    getNumString(res[htb][stb][njreg[0]]['rCS_srNJet_0b_onlyW']['rCS'], res[htb][stb][njreg[0]]['rCS_srNJet_0b_onlyW']['rCSE_sim'],4),\
                    getNumString(res[htb][stb][njreg[1]]['rCS_srNJet_0b_onlyW']['rCS'], res[htb][stb][njreg[1]]['rCS_srNJet_0b_onlyW']['rCSE_sim'],4)])+'\\\\'
print
for i_htb, htb in enumerate(htreg):
  for stb, dPhiCut in streg:
    print '& & \multicolumn{3}{c|}{$R^{corr.}_{CS}(0b,2/3j)$ (- charge)}&\multicolumn{3}{c|}{$R_{CS,W^{-}_{jets}}(0b,==5j)$}&\multicolumn{3}{c}{$R_{CS,W^{-}_{jets}}(0b,>=6j)$}\\\\hline'
    print '$'+varBinName(htb, 'H_{T}')+'$&$'+varBinName(stb, 'S_{T}')+'$ & '+\
        ' & '.join([getNumString(res[htb][stb][njreg[0]]['rCS_W_PosPdg_crNJet_0b_corr'],sqrt(res[htb][stb][njreg[0]]['rCS_Var_W_PosPdg_crNJet_0b_corr']),4), \
                    getNumString(res[htb][stb][njreg[0]]['rCS_srNJet_0b_onlyW_PosPdg']['rCS'], res[htb][stb][njreg[0]]['rCS_srNJet_0b_onlyW_PosPdg']['rCSE_sim'],4),\
                    getNumString(res[htb][stb][njreg[1]]['rCS_srNJet_0b_onlyW_PosPdg']['rCS'], res[htb][stb][njreg[1]]['rCS_srNJet_0b_onlyW_PosPdg']['rCSE_sim'],4)])+'\\\\'
print
print
for i_htb, htb in enumerate(htreg):
  for stb, dPhiCut in streg:
    print '& & \multicolumn{3}{c|}{$R^{corr.}_{CS}(0b,2/3j)$ (+ charge)}&\multicolumn{3}{c|}{$R_{CS,W^{+}_{jets}}(0b,==5j)$}&\multicolumn{3}{c}{$R_{CS,W^{+}_{jets}}(0b,>=6j)$}\\\\hline'
    print '$'+varBinName(htb, 'H_{T}')+'$&$'+varBinName(stb, 'S_{T}')+'$ & '+\
        ' & '.join([getNumString(res[htb][stb][njreg[0]]['rCS_W_NegPdg_crNJet_0b_corr'],sqrt(res[htb][stb][njreg[0]]['rCS_Var_W_NegPdg_crNJet_0b_corr']),4), \
                    getNumString(res[htb][stb][njreg[0]]['rCS_srNJet_0b_onlyW_NegPdg']['rCS'], res[htb][stb][njreg[0]]['rCS_srNJet_0b_onlyW_NegPdg']['rCSE_sim'],4),\
                    getNumString(res[htb][stb][njreg[1]]['rCS_srNJet_0b_onlyW_NegPdg']['rCS'], res[htb][stb][njreg[1]]['rCS_srNJet_0b_onlyW_NegPdg']['rCSE_sim'],4)])+'\\\\'
print

print "rCS(TT) comparison used for tt estimation"
print
for i_htb, htb in enumerate(htreg):
  if i_htb!=0:print '\\hline'
#  print '& & \multicolumn{6}{c|}{$t\overline{t}$+Jets}&\multicolumn{6}{c|}{$W$+Jets}&\multicolumn{6}{c}{total}\\\\'
  print '\multicolumn{2}{c|}{$'+varBinName(htb, 'H_{T}')+"$}&"\
      + "\multicolumn{3}{c|}{$R_{CS}(1b,4/5j)$}&\multicolumn{3}{c|}{$R_{CS,t\overline{t}}(1b,4/5j)$}&\multicolumn{3}{c}{$R_{CS,t\overline{t}}(0b)$}\\\\\\hline"

  for stb, dPhiCut in streg:
    for srNJet in njreg:
      print '$'+nJetBinName(srNJet)+'$ & $'+varBinName(stb, 'S_{T}')+'$'+' & '+\
          ' & '.join([getNumString(res[htb][stb][srNJet]['rCS_crLowNJet_1b']['rCS'], res[htb][stb][srNJet]['rCS_crLowNJet_1b']['rCSE_sim'],acc=3), \
                      getNumString(res[htb][stb][srNJet]['rCS_crLowNJet_1b_onlyTT']['rCS'], res[htb][stb][srNJet]['rCS_crLowNJet_1b_onlyTT']['rCSE_sim'],acc=3),\
                      getNumString(res[htb][stb][srNJet]['rCS_srNJet_0b_onlyTT']['rCS'], res[htb][stb][srNJet]['rCS_srNJet_0b_onlyTT']['rCSE_sim'],acc=3)])+'\\\\'

print "signal yields (+charge)"
print
for i_htb, htb in enumerate(htreg):
  for stb, dPhiCut in streg:
    for srNJet in njreg:
      rCS_sr_Name_0b = nameAndCut(stb,htb,srNJet,btb=(0,0), presel=presel, btagVar = 'nBTagCMVA')#for Check 
      strings=[]
      for s in signals:
        sig =     getYieldFromChain(s['chain'], 'leptonPdg<0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+'>'+str(dPhiCut), weight = "weight")
        sigErr  = getYieldFromChain(s['chain'], 'leptonPdg<0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+'>'+str(dPhiCut), weight = "weight*weight")
        strings.append( getNumString(sig, sigErr, 3) )
      print " , ".join(strings), rCS_sr_Name_0b
print
print "signal yields (-charge)"
print
for i_htb, htb in enumerate(htreg):
  for stb in streg:
    for srNJet in njreg:
      rCS_sr_Name_0b = nameAndCut(stb,htb,srNJet,btb=(0,0), presel=presel, btagVar = 'nBTagCMVA')#for Check 
      strings=[]
      for s in signals:
        sig =     getYieldFromChain(s['chain'], 'leptonPdg>0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+'>'+str(dPhiCut), weight = "weight")
        sigErr  = getYieldFromChain(s['chain'], 'leptonPdg>0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+'>'+str(dPhiCut), weight = "weight*weight")
        strings.append( getNumString(sig, sigErr, 3) )
      print " , ".join(strings), rCS_sr_Name_0b
print

