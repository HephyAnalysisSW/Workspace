import ROOT
ROOT.gROOT.ProcessLine('.L /afs/hephy.at/scratch/d/dhandl/CMSSW_7_0_6_patch1/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
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
cBkg = getChain([WJetsHTToLNu, ttJetsCSA1450ns])

#streg = [(200, 250), (250, 350), (350, 450), (450, -1)] 
#htreg = [(500,750),(750,1000),(1000,-1)]
#streg = [(250,350), (350,-1)]
#htreg = [(500,750), (750,-1)]
njreg = [(5,5),(6,-1)]

small = 1
if small == 1:
  streg = [(250, 350),(350,-1)]
  htreg = (400,500)
  njreg = [(2,2), (3,3), (4,4), (5,5)] 
presel   ="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0"
wwwDir = 'rCSpng/'
preprefix = 'singleMuonic_0b_'

dPhiStr = "acos((leptonPt+met_pt*cos(leptonPhi-met_phi))/sqrt(leptonPt**2+met_pt**2+2*met_pt*leptonPt*cos(leptonPhi-met_phi)))"
dPhiCut = 1.

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

histos = {}
histos['rCS'] = {}
histos['rCSposPdg'] = {}
histos['rCSnegPdg'] = {}
histos['rCSBkg'] = {}
histos['rCS_onlyTT'] = {}

for stb in streg:
  bin = varBinName(stb,'st')
  histos['rCS'][bin] = ROOT.TH1F('rCS hist','rCS hist',7,-0.5,6.5)
  histos['rCSposPdg'][bin] = ROOT.TH1F('rCSposPdg hist','rCSposPdg hist',7,-0.5,6.5)
  histos['rCSnegPdg'][bin] = ROOT.TH1F('rCSnegPdg hist','rCSnegPdg hist',7,-0.5,6.5)
  histos['rCSBkg'][bin] = ROOT.TH1F('rCSBkg hist','rCSBkg hist',7,-0.5,6.5)
  histos['rCS_onlyTT'][bin] = ROOT.TH1F('rCS_onlyTT hist','rCS_onlyTT hist',7,-0.5,6.5)
  for i_Njet, NJet in enumerate(njreg):
    print 'i: ',i_Njet,'stb: ',stb,'NJet: ',NJet
      #print varBinName(htb,'htJet40ja')
      #print varBinName(htb,'(met_pt+leptonPt)')
      #print nJetBinName(srNJet)
      #Name, Cut = nameAndCut(stb,htb,srNJet,btb=(0,0), presel=presel, btagVar = 'nBJetMedium25')
      
      #srName, srCut = nameAndCut(stb,htb,srNJet,btb=(0,0), presel=presel,btagVar = 'nBJetMedium25')      
      #yWposPdg_srNJet_0b_highDPhi_truth   = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+">1"+'&&leptonPdg>0', weight = "weight")
      #yWnegPdg_srNJet_0b_highDPhi_truth   = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+">1"+'&&leptonPdg<0', weight = "weight")
      #yW_srNJet_0b_highDPhi_truth      = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+">1", weight = "weight")
      #yWposPdg_srNJet_0b_highDPhi_truth_var   = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+">1"+'&&leptonPdg>0', weight = "weight*weight")
      #yWnegPdg_srNJet_0b_highDPhi_truth_var   = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+">1"+'&&leptonPdg<0', weight = "weight*weight")
      #yW_srNJet_0b_highDPhi_truth_var      = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+">1", weight = "weight*weight")

      #yWposPdg_srNJet_0b_lowDPhi_truth   = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+"<1"+'&&leptonPdg>0', weight = "weight")
      #yWnegPdg_srNJet_0b_lowDPhi_truth   = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+"<1"+'&&leptonPdg<0', weight = "weight")
      #yW_srNJet_0b_lowDPhi_truth      = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+"<1", weight = "weight")
      #yWposPdg_srNJet_0b_lowDPhi_truth_var   = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+"<1"+'&&leptonPdg>0', weight = "weight*weight")
      #yWnegPdg_srNJet_0b_lowDPhi_truth_var   = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+"<1"+'&&leptonPdg<0', weight = "weight*weight")
      #yW_srNJet_0b_lowDPhi_truth_var      = getYieldFromChain(cWJets, srCut+"&&"+dPhiStr+"<1", weight = "weight*weight")

      #yTT_srNJet_0b_highDPhi_truth      = getYieldFromChain(cTTJets, srCut+"&&"+dPhiStr+">1", weight = "weight")

      #fit_srName, fit_srCut = nameAndCut(stb,htb,srNJet,btb=None, presel=presel,btagVar = 'nBJetMedium25')
      #fit_srNJet_lowDPhi = binnedNBTagsFit(fit_srCut+"&&"+dPhiStr+"<"+str(dPhiCut), samples = {'W':cWJets, 'TT':cTTJets}, nBTagVar = 'nBJetMedium25', prefix=fit_srName)

      #yTT_srNJet_0b_lowDPhi =  fit_srNJet_lowDPhi['TT_AllPdg']['yield']*fit_srNJet_lowDPhi['TT_AllPdg']['template'].GetBinContent(1)
      #yTT_Var_srNJet_0b_lowDPhi =  fit_srNJet_lowDPhi['TT_AllPdg']['yieldVar']*fit_srNJet_lowDPhi['TT_AllPdg']['template'].GetBinContent(1)**2
      #yW_srNJet_0b_lowDPhi     =  fit_srNJet_lowDPhi['W_PosPdg']['yield']*fit_srNJet_lowDPhi['W_PosPdg']['template'].GetBinContent(1)\
      #                         +  fit_srNJet_lowDPhi['W_NegPdg']['yield']*fit_srNJet_lowDPhi['W_NegPdg']['template'].GetBinContent(1)
      #yWposPdg_srNJet_0b_lowDPhi  =  fit_srNJet_lowDPhi['W_PosPdg']['yield']*fit_srNJet_lowDPhi['W_PosPdg']['template'].GetBinContent(1)
      #yWnegPdg_srNJet_0b_lowDPhi  =  fit_srNJet_lowDPhi['W_NegPdg']['yield']*fit_srNJet_lowDPhi['W_NegPdg']['template'].GetBinContent(1)
      #yW_srNJet_0b_lowDPhi_var     =  fit_srNJet_lowDPhi['W_PosPdg']['yieldVar']*fit_srNJet_lowDPhi['W_PosPdg']['template'].GetBinContent(1)**2\
      #                             +  fit_srNJet_lowDPhi['W_NegPdg']['yieldVar']*fit_srNJet_lowDPhi['W_NegPdg']['template'].GetBinContent(1)**2#FIXME I add that uncorrelated
      #yWposPdg_srNJet_0b_lowDPhi_var  =  fit_srNJet_lowDPhi['W_PosPdg']['yieldVar']*fit_srNJet_lowDPhi['W_PosPdg']['template'].GetBinContent(1)**2
      #yWnegPdg_srNJet_0b_lowDPhi_var  =  fit_srNJet_lowDPhi['W_NegPdg']['yieldVar']*fit_srNJet_lowDPhi['W_NegPdg']['template'].GetBinContent(1)**2

      #rCS_sr_Name_1b, rCS_sr_Cut_1b = nameAndCut(stb,htb,srNJet,btb=(1,1), presel=presel, btagVar = 'nBJetMedium25')
      #rCS_crLowNJet_Name_1b, rCS_crLowNJet_Cut_1b = nameAndCut(stb,htb,(4,5),btb=(1,1), presel=presel, btagVar = 'nBJetMedium25')
    rCS_Name_0b, rCS_Cut_0b = nameAndCut(stb,htreg,NJet,btb=(0,0), presel=presel, btagVar = 'nBJetMedium25')  
      #rCS_srNJet_1b = getRCS(cBkg, rCS_sr_Cut_1b,  dPhiCut)
      #rCS_crLowNJet_1b = getRCS(cBkg, rCS_crLowNJet_Cut_1b,  dPhiCut) #Low njet tt-jets CR to be orthoganl to DPhi 
      #rCS_srNJet_1b_onlyTT = getRCS(cTTJets, rCS_sr_Cut_1b,  dPhiCut)
      #rCS_crLowNJet_1b_onlyTT = getRCS(cTTJets, rCS_crLowNJet_Cut_1b,  dPhiCut)
      #rCS_srNJet_0b_onlyTT = getRCS(cTTJets, rCS_sr_Cut_0b,  dPhiCut) #for check
    rCS_NJet_0b_onlyW = getRCS(cWJets, rCS_Cut_0b,  dPhiCut) #for check
    rCS_NJet_0b_onlyWposPdg = getRCS(cWJets, rCS_Cut_0b+'&&leptonPdg>0',  dPhiCut)
    rCS_NJet_0b_onlyWnegPdg = getRCS(cWJets, rCS_Cut_0b+'&&leptonPdg<0',  dPhiCut)
    rCS_NJet_0b_Bkg = getRCS(cBkg, rCS_Cut_0b,  dPhiCut)
    rCS_NJet_0b_onlyTT = getRCS(cTTJets, rCS_Cut_0b,  dPhiCut)
#    print "rCS(W): ",rCS_NJet_0b_onlyW['rCS'],'+-',rCS_NJet_0b_onlyW['rCSE_sim'],"rCS(WposPdg): ",rCS_NJet_0b_onlyWposPdg['rCS'],'+-',rCS_NJet_0b_onlyWposPdg['rCSE_sim'],\
#          "rCS(WnegPdg): ",rCS_NJet_0b_onlyWnegPdg['rCS'],'+-',rCS_NJet_0b_onlyWnegPdg['rCSE_sim']
    histos['rCS'][bin].SetBinContent(i_Njet+3, rCS_NJet_0b_onlyW['rCS'])
    histos['rCSposPdg'][bin].SetBinContent(i_Njet+3, rCS_NJet_0b_onlyWposPdg['rCS'])
    histos['rCSnegPdg'][bin].SetBinContent(i_Njet+3, rCS_NJet_0b_onlyWnegPdg['rCS'])
    histos['rCS'][bin].SetBinError(i_Njet+3, rCS_NJet_0b_onlyW['rCSE_sim'])
    histos['rCSposPdg'][bin].SetBinError(i_Njet+3, rCS_NJet_0b_onlyWposPdg['rCSE_sim'])
    histos['rCSnegPdg'][bin].SetBinError(i_Njet+3, rCS_NJet_0b_onlyWnegPdg['rCSE_sim'])
    histos['rCSBkg'][bin].SetBinContent(i_Njet+3, rCS_NJet_0b_Bkg['rCS'])
    histos['rCS_onlyTT'][bin].SetBinContent(i_Njet+3, rCS_NJet_0b_onlyTT['rCS'])
    histos['rCSBkg'][bin].SetBinError(i_Njet+3, rCS_NJet_0b_Bkg['rCSE_sim'])
    histos['rCS_onlyTT'][bin].SetBinError(i_Njet+3, rCS_NJet_0b_onlyTT['rCSE_sim'])
      #fit_srName_h, fit_srCut_h = nameAndCut(stb,htb,srNJet,btb=None, presel=presel,btagVar = 'nBJetMedium25') 
      #fit_srNJet_highDPhi = binnedNBTagsFit(fit_srCut_h+"&&"+dPhiStr+">"+str(dPhiCut), samples = {'W':cWJets, 'TT':cTTJets}, nBTagVar = 'nBJetMedium25', prefix=fit_srName_h) 
      #yW_srNJet_0b_highDPhi     =  fit_srNJet_highDPhi['W_PosPdg']['yield']*fit_srNJet_highDPhi['W_PosPdg']['template'].GetBinContent(2)\
      #                          +  fit_srNJet_highDPhi['W_NegPdg']['yield']*fit_srNJet_highDPhi['W_NegPdg']['template'].GetBinContent(2)
      #yWposPdg_srNJet_0b_highDPhi  =  fit_srNJet_highDPhi['W_PosPdg']['yield']*fit_srNJet_highDPhi['W_PosPdg']['template'].GetBinContent(2)
      #yWnegPdg_srNJet_0b_highDPhi  =  fit_srNJet_highDPhi['W_NegPdg']['yield']*fit_srNJet_highDPhi['W_NegPdg']['template'].GetBinContent(2)
      #yW_srNJet_0b_highDPhi_var     =  fit_srNJet_highDPhi['W_PosPdg']['yieldVar']*fit_srNJet_highDPhi['W_PosPdg']['template'].GetBinContent(2)**2\
      #                              +  fit_srNJet_highDPhi['W_NegPdg']['yieldVar']*fit_srNJet_highDPhi['W_NegPdg']['template'].GetBinContent(2)**2
      #yWposPdg_srNJet_0b_highDPhi_var  =  fit_srNJet_highDPhi['W_PosPdg']['yieldVar']*fit_srNJet_highDPhi['W_PosPdg']['template'].GetBinContent(2)**2
      #yWnegPdg_srNJet_0b_highDPhi_var  =  fit_srNJet_highDPhi['W_NegPdg']['yieldVar']*fit_srNJet_highDPhi['W_NegPdg']['template'].GetBinContent(2)**2  
      #print rCS_sr_Name_0b
      
    print "rCS(W): ",rCS_NJet_0b_onlyW['rCS'],'+-',rCS_NJet_0b_onlyW['rCSE_sim'],"rCS(WposPdg): ",rCS_NJet_0b_onlyWposPdg['rCS'],'+-',rCS_NJet_0b_onlyWposPdg['rCSE_sim'],\
          "rCS(WnegPdg): ",rCS_NJet_0b_onlyWnegPdg['rCS'],'+-',rCS_NJet_0b_onlyWnegPdg['rCSE_sim']
      #print 'yW_srNJet_0b_lowDPhi_truth: ',yW_srNJet_0b_lowDPhi_truth,'+-',sqrt(yW_srNJet_0b_lowDPhi_truth_var),'yWposPdg_srNJet_0b_lowDPhi_truth: ',yWposPdg_srNJet_0b_lowDPhi_truth,'+-',sqrt(yWposPdg_srNJet_0b_lowDPhi_truth_var),\
      #      'yWnegPdg_srNJet_0b_lowDPhi_truth: ',yWnegPdg_srNJet_0b_lowDPhi_truth,'+-',sqrt(yWnegPdg_srNJet_0b_lowDPhi_truth_var)
      #print 'yW_srNJet_0b_highDPhi_truth: ',yW_srNJet_0b_highDPhi_truth,'+-',sqrt(yW_srNJet_0b_highDPhi_truth_var),'yWposPdg_srNJet_0b_highDPhi_truth: ',yWposPdg_srNJet_0b_highDPhi_truth,'+-',sqrt(yWposPdg_srNJet_0b_highDPhi_truth_var),\
      #      'yWnegPdg_srNJet_0b_highDPhi_truth: ',yWnegPdg_srNJet_0b_highDPhi_truth,'+-',sqrt(yWnegPdg_srNJet_0b_highDPhi_truth_var)
      #print 'yW_srNJet_0b_lowDPhi: ',yW_srNJet_0b_lowDPhi,'+-',yW_srNJet_0b_lowDPhi_var,'yWposPdg_srNJet_0b_lowDPhi: ',yWposPdg_srNJet_0b_lowDPhi,'+-',yWposPdg_srNJet_0b_lowDPhi_var,\
      #      'yWnegPdg_srNJet_0b_lowDPhi: ',yWnegPdg_srNJet_0b_lowDPhi,'+-',yWnegPdg_srNJet_0b_lowDPhi_var
      #print 'yW_srNJet_0b_highDPhi: ',yW_srNJet_0b_highDPhi,'+-',yW_srNJet_0b_highDPhi_var,'yWposPdg_srNJet_0b_highDPhi: ',yWposPdg_srNJet_0b_highDPhi,'+-',yWposPdg_srNJet_0b_highDPhi_var,\
      #      'yWnegPdg_srNJet_0b_highDPhi: ',yWnegPdg_srNJet_0b_highDPhi,'+-',yWnegPdg_srNJet_0b_highDPhi_var

for stb in streg:
  bin = varBinName(stb,'st')
  ht = varBinName(htreg,'ht')
  #stbinstr = str(stb)
  #stbin = stbinstr[1]+stbinstr[2]+stbinstr[3]+stbinstr[4]+stbinstr[5]+stbinstr[6]+stbinstr[7]+stbinstr[8]
  #htbinstr = str(htreg)
  #htbin = htbinstr[1]+htbinstr[2]+htbinstr[3]+htbinstr[4]+htbinstr[5]+htbinstr[6]+htbinstr[7]+htbinstr[8]
  canvas = ROOT.TCanvas('rCS canvas','rCS canvas')
  l = ROOT.TLegend(0.6,0.7,0.95,0.95)
  l.SetFillColor(0)
  l.SetBorderSize(1)
  l.SetShadowColor(ROOT.kWhite)
  histos['rCS'][bin].GetXaxis().SetTitle('nJet')
  histos['rCS'][bin].GetYaxis().SetTitle('R_{CS}')
  histos['rCS'][bin].SetMaximum(0.1)
  histos['rCS'][bin].SetLineColor(ROOT.kBlack)
  histos['rCSposPdg'][bin].SetLineColor(ROOT.kBlue)
  histos['rCSnegPdg'][bin].SetLineColor(ROOT.kRed)
  histos['rCSBkg'][bin].SetLineColor(ROOT.kGreen+3)
  histos['rCS_onlyTT'][bin].SetLineColor(ROOT.kMagenta)
  #histos['rCS'][bin].SetLineWidth(2)
  #histos['rCSposPdg'][bin].SetLineWidth(2)
  #histos['rCSnegPdg'][bin].SetLineWidth(2)
  histos['rCS'][bin].SetMarkerStyle(2)
  histos['rCSposPdg'][bin].SetMarkerStyle(2)
  histos['rCSnegPdg'][bin].SetMarkerStyle(2)
  histos['rCSBkg'][bin].SetMarkerStyle(2)
  histos['rCS_onlyTT'][bin].SetMarkerStyle(2)
  #histos['rCS'][bin].SetMarkerSize(2)
  #histos['rCSposPdg'][bin].SetMarkerSize(2)
  #histos['rCSnegPdg'][bin].SetMarkerSize(2)
  histos['rCS'][bin].SetMarkerColor(ROOT.kBlack)
  histos['rCSposPdg'][bin].SetMarkerColor(ROOT.kBlue)
  histos['rCSnegPdg'][bin].SetMarkerColor(ROOT.kRed)
  histos['rCSBkg'][bin].SetMarkerColor(ROOT.kGreen+3)
  histos['rCS_onlyTT'][bin].SetMarkerColor(ROOT.kMagenta)
  l.AddEntry(histos['rCS'][bin],'R_{CS,W jets}')
  l.AddEntry(histos['rCSposPdg'][bin],'R_{CS,W^{-} jets}')
  l.AddEntry(histos['rCSnegPdg'][bin],'R_{CS,W^{+} jets}')
  l.AddEntry(histos['rCSBkg'][bin],'R_{CS,Bkg}')
  l.AddEntry(histos['rCS_onlyTT'][bin],'R_{CS,TT jets}')
  histos['rCS'][bin].Draw()
  histos['rCSposPdg'][bin].Draw('same')
  histos['rCSnegPdg'][bin].Draw('same')
  histos['rCSBkg'][bin].Draw('same')
  histos['rCS_onlyTT'][bin].Draw('same')

  l.Draw()
  
  text = ROOT.TLatex()
  text.SetNDC()
  text.DrawLatex(0.22,.86,bin)
  text.DrawLatex(0.22,.80,ht)
  text.DrawLatex(0.22,0.74,"N_{btag}=0")

  canvas.Print('/afs/hephy.at/user/d/dhandl/www/'+wwwDir+preprefix+bin+'_'+ht+'_'+'rCS'+'.png')
  canvas.Print('/afs/hephy.at/user/d/dhandl/www/'+wwwDir+preprefix+bin+'_'+ht+'_'+'rCS'+'.root')
  canvas.Print('/afs/hephy.at/user/d/dhandl/www/'+wwwDir+preprefix+bin+'_'+ht+'_'+'rCS'+'.pdf')
