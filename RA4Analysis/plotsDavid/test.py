import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.cmgTuplesPostProcessed import *
#from localInfo import username

import os, copy, sys
sys.path.append('/afs/hephy.at/scratch/d/dhandl/CMSSW_7_0_6_patch1/src/Workspace/RA4Analysis/plotsDavid')

from Workspace.RA4Analysis.helpers import nameAndCut,nBTagBinName
from binnedNBTagsFit import binnedNBTagsFit
from math import pi, sqrt

cWJets  = getChain(WJetsHTToLNu)
cTTJets = getChain(ttJetsCSA1450ns)

#streg = [(200, 250), (250, 350), (350, 450), (450, -1)] 
#htreg = [(500,750),(750,1000),(1000,-1)]
streg = [(250,350), (350,-1)]
htreg = [(500,750), (750,-1)]
njreg = [(5,5),(6,-1)]
presel   ="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0"

dPhiStr = "acos((leptonPt+met_pt*cos(leptonPhi-met_phi))/sqrt(leptonPt**2+met_pt**2+2*met_pt*leptonPt*cos(leptonPhi-met_phi)))"
dPhiCut = 1.

#yWpos_crNJet_0b_lowDPhi_truth   = getYieldFromChain(cTTJets, crCut+"&&"+dPhiStr+"<"+str(dPhiCut), weight = "weight")
#yWneg_crNJet_0b_highDPhi_truth  = getYieldFromChain(cTTJets, crCut+"&&"+dPhiStr+">"+str(dPhiCut), weight = "weight")
#yW_crNjet_0b_

def nJetBinName(njb):
  if njb[0]==njb[1]:
    return "nJet=="+str(njb[0])
  n=str(list(njb)[0])+"<=nJet"
  if len(njb)>1 and njb[1]>0:
    n+='<='+str(njb[1])
  return n

def varBinName(vb, var):
  n=str(list(vb)[0])+"<"+var
  if len(vb)>1 and vb[1]>0:
    n+='<'+str(vb[1])
  return n

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

for i_htb, htb in enumerate(htreg):
  for stb in streg:
    for srNJet in njreg:
      print 'i_htb: ',i_htb,'htb: ',htb,'stb: ',stb,'srNJet: ',srNJet
      #print varBinName(htb,'htJet40ja')
      #print varBinName(htb,'(met_pt+leptonPt)')
      #print nJetBinName(srNJet)
      #Name, Cut = nameAndCut(stb,htb,srNJet,btb=(0,0), presel=presel, btagVar = 'nBJetMedium25')
      
      srName, srCut = nameAndCut(stb,htb,srNJet,btb=(0,0), presel=presel,btagVar = 'nBJetMedium25')      
      yWposPdg_srNJet_0b_highDPhi_truth   = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+">1"+'&&leptonPdg>0', weight = "weight")
      yWnegPdg_srNJet_0b_highDPhi_truth   = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+">1"+'&&leptonPdg<0', weight = "weight")
      yW_srNJet_0b_highDPhi_truth      = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+">1", weight = "weight")
      yWposPdg_srNJet_0b_highDPhi_truth_var   = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+">1"+'&&leptonPdg>0', weight = "weight*weight")
      yWnegPdg_srNJet_0b_highDPhi_truth_var   = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+">1"+'&&leptonPdg<0', weight = "weight*weight")
      yW_srNJet_0b_highDPhi_truth_var      = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+">1", weight = "weight*weight")

      yWposPdg_srNJet_0b_lowDPhi_truth   = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+"<1"+'&&leptonPdg>0', weight = "weight")
      yWnegPdg_srNJet_0b_lowDPhi_truth   = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+"<1"+'&&leptonPdg<0', weight = "weight")
      yW_srNJet_0b_lowDPhi_truth      = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+"<1", weight = "weight")
      yWposPdg_srNJet_0b_lowDPhi_truth_var   = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+"<1"+'&&leptonPdg>0', weight = "weight*weight")
      yWnegPdg_srNJet_0b_lowDPhi_truth_var   = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+"<1"+'&&leptonPdg<0', weight = "weight*weight")
      yW_srNJet_0b_lowDPhi_truth_var      = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+"<1", weight = "weight*weight")

      #yTT_srNJet_0b_highDPhi_truth      = getYieldFromChain(cTTJets, srCut+"&&"+dPhiStr+">1", weight = "weight")

      #fit_srName, fit_srCut = nameAndCut(stb,htb,srNJet,btb=None, presel=presel,btagVar = 'nBJetMedium25')
      #fit_srNJet_lowDPhi = binnedNBTagsFit(fit_srCut+"&&"+dPhiStr+"<"+str(dPhiCut), samples = {'W':cWJets, 'TT':cTTJets}, nBTagVar = 'nBJetMedium25', prefix=fit_srName)

      #yTT_srNJet_0b_lowDPhi =  fit_srNJet_lowDPhi['TT_AllPdg']['yield']*fit_srNJet_lowDPhi['TT_AllPdg']['template'].GetBinContent(1)
      #yTT_Var_srNJet_0b_lowDPhi =  fit_srNJet_lowDPhi['TT_AllPdg']['yieldVar']*fit_srNJet_lowDPhi['TT_AllPdg']['template'].GetBinContent(1)**2
#      yW_srNJet_0b_lowDPhi     =  fit_srNJet_lowDPhi['W_PosPdg']['yield']*fit_srNJet_lowDPhi['W_PosPdg']['template'].GetBinContent(1)\
#                               +  fit_srNJet_lowDPhi['W_NegPdg']['yield']*fit_srNJet_lowDPhi['W_NegPdg']['template'].GetBinContent(1)
#      yWposPdg_srNJet_0b_lowDPhi  =  fit_srNJet_lowDPhi['W_PosPdg']['yield']*fit_srNJet_lowDPhi['W_PosPdg']['template'].GetBinContent(1)
#      yWnegPdg_srNJet_0b_lowDPhi  =  fit_srNJet_lowDPhi['W_NegPdg']['yield']*fit_srNJet_lowDPhi['W_NegPdg']['template'].GetBinContent(1)
#      yW_srNJet_0b_lowDPhi_var     =  fit_srNJet_lowDPhi['W_PosPdg']['yieldVar']*fit_srNJet_lowDPhi['W_PosPdg']['template'].GetBinContent(1)**2\
#                                   +  fit_srNJet_lowDPhi['W_NegPdg']['yieldVar']*fit_srNJet_lowDPhi['W_NegPdg']['template'].GetBinContent(1)**2#FIXME I add that uncorrelated
#      yWposPdg_srNJet_0b_lowDPhi_var  =  fit_srNJet_lowDPhi['W_PosPdg']['yieldVar']*fit_srNJet_lowDPhi['W_PosPdg']['template'].GetBinContent(1)**2
#      yWnegPdg_srNJet_0b_lowDPhi_var  =  fit_srNJet_lowDPhi['W_NegPdg']['yieldVar']*fit_srNJet_lowDPhi['W_NegPdg']['template'].GetBinContent(1)**2

      #rCS_sr_Name_1b, rCS_sr_Cut_1b = nameAndCut(stb,htb,srNJet,btb=(1,1), presel=presel, btagVar = 'nBJetMedium25')
      #rCS_crLowNJet_Name_1b, rCS_crLowNJet_Cut_1b = nameAndCut(stb,htb,(4,5),btb=(1,1), presel=presel, btagVar = 'nBJetMedium25')
      rCS_srName_0b, rCS_srCut_0b = nameAndCut(stb,htb,srNJet,btb=(0,0), presel=presel, btagVar = 'nBJetMedium25')#for Check  
      rCS_crName_0b, rCS_crCut_0b = nameAndCut(stb,htb,(2,3),btb=(0,0), presel=presel, btagVar = 'nBJetMedium25')
      #rCS_srNJet_1b = getRCS(cBkg, rCS_sr_Cut_1b,  dPhiCut)
      #rCS_crLowNJet_1b = getRCS(cBkg, rCS_crLowNJet_Cut_1b,  dPhiCut) #Low njet tt-jets CR to be orthoganl to DPhi 
      #rCS_srNJet_1b_onlyTT = getRCS(cTTJets, rCS_sr_Cut_1b,  dPhiCut)
      #rCS_crLowNJet_1b_onlyTT = getRCS(cTTJets, rCS_crLowNJet_Cut_1b,  dPhiCut)
      #rCS_srNJet_0b_onlyTT = getRCS(cTTJets, rCS_sr_Cut_0b,  dPhiCut) #for check
      rCS_srNJet_0b_onlyW = getRCS(cWJets, rCS_srCut_0b,  dPhiCut) #for check
      rCS_srNJet_0b_onlyWposPdg = getRCS(cWJets, rCS_srCut_0b+'&&leptonPdg>0',  dPhiCut)
      rCS_srNJet_0b_onlyWnegPdg = getRCS(cWJets, rCS_srCut_0b+'&&leptonPdg<0',  dPhiCut)
      rCS_crNJet_0b_onlyW = getRCS(cWJets, rCS_crCut_0b,  dPhiCut) #for check
      rCS_crNJet_0b_onlyWposPdg = getRCS(cWJets, rCS_crCut_0b+'&&leptonPdg>0',  dPhiCut)
      rCS_crNJet_0b_onlyWnegPdg = getRCS(cWJets, rCS_crCut_0b+'&&leptonPdg<0',  dPhiCut)    
 
#      fit_srName_h, fit_srCut_h = nameAndCut(stb,htb,srNJet,btb=None, presel=presel,btagVar = 'nBJetMedium25') 
#      fit_srNJet_highDPhi = binnedNBTagsFit(fit_srCut_h+"&&"+dPhiStr+">"+str(dPhiCut), samples = {'W':cWJets, 'TT':cTTJets}, nBTagVar = 'nBJetMedium25', prefix=fit_srName_h) 
#      yW_srNJet_0b_highDPhi     =  fit_srNJet_highDPhi['W_PosPdg']['yield']*fit_srNJet_highDPhi['W_PosPdg']['template'].GetBinContent(2)\
#                                +  fit_srNJet_highDPhi['W_NegPdg']['yield']*fit_srNJet_highDPhi['W_NegPdg']['template'].GetBinContent(2)
#      yWposPdg_srNJet_0b_highDPhi  =  fit_srNJet_highDPhi['W_PosPdg']['yield']*fit_srNJet_highDPhi['W_PosPdg']['template'].GetBinContent(2)
#      yWnegPdg_srNJet_0b_highDPhi  =  fit_srNJet_highDPhi['W_NegPdg']['yield']*fit_srNJet_highDPhi['W_NegPdg']['template'].GetBinContent(2)
#      yW_srNJet_0b_highDPhi_var     =  fit_srNJet_highDPhi['W_PosPdg']['yieldVar']*fit_srNJet_highDPhi['W_PosPdg']['template'].GetBinContent(2)**2\
#                                    +  fit_srNJet_highDPhi['W_NegPdg']['yieldVar']*fit_srNJet_highDPhi['W_NegPdg']['template'].GetBinContent(2)**2
#      yWposPdg_srNJet_0b_highDPhi_var  =  fit_srNJet_highDPhi['W_PosPdg']['yieldVar']*fit_srNJet_highDPhi['W_PosPdg']['template'].GetBinContent(2)**2
#      yWnegPdg_srNJet_0b_highDPhi_var  =  fit_srNJet_highDPhi['W_NegPdg']['yieldVar']*fit_srNJet_highDPhi['W_NegPdg']['template'].GetBinContent(2)**2  
      #print rCS_sr_Name_0b
      print "rCS(W): ",rCS_crNJet_0b_onlyW['rCS'],'+-',rCS_crNJet_0b_onlyW['rCSE_sim'],"rCS(WposPdg): ",rCS_crNJet_0b_onlyWposPdg['rCS'],'+-',rCS_crNJet_0b_onlyWposPdg['rCSE_sim'],\
            "rCS(WnegPdg): ",rCS_crNJet_0b_onlyWnegPdg['rCS'],'+-',rCS_crNJet_0b_onlyWnegPdg['rCSE_sim']
      #Signal = rCS_srNJet_0b_onlyW['rCS']*yW_srNJet_0b_lowDPhi + rCS_srNJet_0b_onlyTT['rCS']*yTT_srNJet_0b_highDPhi_truth
      #Signal_charge = rCS_srNJet_0b_onlyW_pos['rCS']*yWpos_srNJet_0b_lowDPhi + rCS_srNJet_0b_onlyW_neg['rCS']*yWneg_srNJet_0b_lowDPhi + rCS_srNJet_0b_onlyTT['rCS']*yTT_srNJet_0b_highDPhi_truth
      #Signal_truth = rCS_srNJet_0b_onlyW['rCS']*yW_srNJet_0b_highDPhi_truth + rCS_srNJet_0b_onlyTT['rCS']*yTT_srNJet_0b_highDPhi_truth
      #Signal_truth_charge = rCS_srNJet_0b_onlyW_pos['rCS']*yWpos_srNJet_0b_highDPhi_truth + rCS_srNJet_0b_onlyW_neg['rCS']*yWneg_srNJet_0b_highDPhi_truth + rCS_srNJet_0b_onlyTT['rCS']*yTT_srNJet_0b_highDPhi_truth
      #print 'Signal: ',Signal,'Signal charge: ',Signal_charge
      #print 'Signal truth: ',Signal_truth,'Signal truth charge: ',Signal_truth_charge
#      print 'yW_srNJet_0b_lowDPhi_truth: ',yW_srNJet_0b_lowDPhi_truth,'+-',sqrt(yW_srNJet_0b_lowDPhi_truth_var),'yWposPdg_srNJet_0b_lowDPhi_truth: ',yWposPdg_srNJet_0b_lowDPhi_truth,'+-',sqrt(yWposPdg_srNJet_0b_lowDPhi_truth_var),\
#            'yWnegPdg_srNJet_0b_lowDPhi_truth: ',yWnegPdg_srNJet_0b_lowDPhi_truth,'+-',sqrt(yWnegPdg_srNJet_0b_lowDPhi_truth_var)
#      print 'yW_srNJet_0b_highDPhi_truth: ',yW_srNJet_0b_highDPhi_truth,'+-',sqrt(yW_srNJet_0b_highDPhi_truth_var),'yWposPdg_srNJet_0b_highDPhi_truth: ',yWposPdg_srNJet_0b_highDPhi_truth,'+-',sqrt(yWposPdg_srNJet_0b_highDPhi_truth_var),\
#            'yWnegPdg_srNJet_0b_highDPhi_truth: ',yWnegPdg_srNJet_0b_highDPhi_truth,'+-',sqrt(yWnegPdg_srNJet_0b_highDPhi_truth_var)
#      print 'yW_srNJet_0b_lowDPhi: ',yW_srNJet_0b_lowDPhi,'+-',yW_srNJet_0b_lowDPhi_var,'yWposPdg_srNJet_0b_lowDPhi: ',yWposPdg_srNJet_0b_lowDPhi,'+-',yWposPdg_srNJet_0b_lowDPhi_var,\
#            'yWnegPdg_srNJet_0b_lowDPhi: ',yWnegPdg_srNJet_0b_lowDPhi,'+-',yWnegPdg_srNJet_0b_lowDPhi_var
#      print 'yW_srNJet_0b_highDPhi: ',yW_srNJet_0b_highDPhi,'+-',yW_srNJet_0b_highDPhi_var,'yWposPdg_srNJet_0b_highDPhi: ',yWposPdg_srNJet_0b_highDPhi,'+-',yWposPdg_srNJet_0b_highDPhi_var,\
#            'yWnegPdg_srNJet_0b_highDPhi: ',yWnegPdg_srNJet_0b_highDPhi,'+-',yWnegPdg_srNJet_0b_highDPhi_var

