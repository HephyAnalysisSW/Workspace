import ROOT
import os, sys, copy

import pickle

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
from array import array

from Workspace.HEPHYPythonTools.helpers import getVarValue, getChain, deltaPhi
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400ST150_withDF import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2 import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_softLepton import *

from Workspace.RA4Analysis.helpers import *

#ROOT.TH1F().SetDefaultSumw2()

deltaPhiCut=1.
varstring='deltaPhi_Wl'
binning=[16,0,3.2]
lepSel = 'hard'

nBtagReg=[0,1,2]
nJetReg=[(6,-1)]#,(3,3),(4,4),(5,5),(6,-1)]
stReg=[(250,-1)]#,(350,450),(450,-1)]
htReg=[(500,-1)]#,(750,1000),(1000,1250),(1250,-1)]

startpath = '/afs/hephy.at/user/d/dspitzbart/www/subBkgFinalCodeTest/'


#Load the Background Chain
c = getChain(ttJets[lepSel],histname='')
#c = getChain(WJetsHTToLNu[lepSel],histname='')

#Sub Background Definitions
ngNuEFromW = "Sum$(abs(genPart_pdgId)==12&&abs(genPart_motherId)==24)"
ngNuMuFromW = "Sum$(abs(genPart_pdgId)==14&&abs(genPart_motherId)==24)"
ngNuTauFromW = "Sum$(abs(genPart_pdgId)==16&&abs(genPart_motherId)==24)"
lTau_H  = ngNuEFromW+"+"+ngNuMuFromW+"==0&&"+ngNuTauFromW+"==1&&Sum$(genTau_nNuE+genTau_nNuMu==1&&genTau_nNuTau==1)==1"
lTau_l  = ngNuEFromW+"+"+ngNuMuFromW+"==1&&"+ngNuTauFromW+"==1&&Sum$(genTau_nNuE+genTau_nNuMu==1&&genTau_nNuTau==1)==1"
hTau_H  = ngNuEFromW+"+"+ngNuMuFromW+"==0&&"+ngNuTauFromW+"==1&&Sum$(genTau_nNuE+genTau_nNuMu==0&&genTau_nNuTau==1)==1"
hTau_l  = ngNuEFromW+'+'+ngNuMuFromW+"==1&&"+ngNuTauFromW+"==1&&Sum$(genTau_nNuE+genTau_nNuMu==0&&genTau_nNuTau==1)==1"
diLepEff   = ngNuEFromW+"+"+ngNuMuFromW+"==2&&"+ngNuTauFromW+"==0&&Sum$(genLep_pt>10&&(abs(genLep_eta)<2.1&&abs(genLep_pdgId)==13||abs(genLep_eta)<2.4&&abs(genLep_pdgId)==11))==2"
diLepAcc   = ngNuEFromW+"+"+ngNuMuFromW+"==2&&"+ngNuTauFromW+"==0&&Sum$(genLep_pt>10&&(abs(genLep_eta)<2.1&&abs(genLep_pdgId)==13||abs(genLep_eta)<2.4&&abs(genLep_pdgId)==11))!=2"
diTau   = ngNuEFromW+"+"+ngNuMuFromW+"==0&&"+ngNuTauFromW+"==2"
diHad   = ngNuEFromW+"+"+ngNuMuFromW+"==0&&"+ngNuTauFromW+"==0"
l_H     = ngNuEFromW+"+"+ngNuMuFromW+"==1&&"+ngNuTauFromW+"==0"
#combined SubBkgs
allHad = "(("+diHad+")||("+hTau_H+"))"
allDiLep = ngNuEFromW+"+"+ngNuMuFromW+"==2&&"+ngNuTauFromW+"==0&&Sum$(genLep_pt>10)"
#in Progress
jetFromW = ngNuEFromW+"+"+ngNuMuFromW+"==0&&Sum$(genTau_nNuE+genTau_nNuMu>=0&&genTau_nNuTau==1)==1&&Sum$(genTau_nNuE+genTau_nNuMu<=1&&genTau_nNuTau==1)==1"
lepFromW = ngNuEFromW+"+"+ngNuMuFromW+"==1&&Sum$(genTau_nNuE+genTau_nNuMu>=0&&genTau_nNuTau==1)==1&&Sum$(genTau_nNuE+genTau_nNuMu<=1&&genTau_nNuTau==1)==1"
hadTau = "("+ngNuEFromW+"+"+ngNuMuFromW+")<=1&&("+ngNuEFromW+"+"+ngNuMuFromW+")>=0&&Sum$(genTau_nNuE+genTau_nNuMu==0&&genTau_nNuTau==1)==1"#not working
lepTau = "("+ngNuEFromW+"+"+ngNuMuFromW+")<=1&&("+ngNuEFromW+"+"+ngNuMuFromW+")>=0&&Sum$(genTau_nNuE+genTau_nNuMu==1&&genTau_nNuTau==1)==1"#not working

##Sub Background Definitions
#ngNuEFromW = "Sum$(abs(genLep_pdgId)==11&&abs(genLep_motherId)==24)"
#ngNuMuFromW = "Sum$(abs(genLep_pdgId)==13&&abs(genLep_motherId)==24)"
#ngNuTauFromW = "Sum$(abs(genLep_pdgId)==15&&abs(genLep_motherId)==24)"
#lTau_H  = ngNuEFromW+"+"+ngNuMuFromW+"==0&&"+ngNuTauFromW+"==1&&Sum$(genTau_nNuE+genTau_nNuMu==1&&genTau_nNuTau==1)==1"
#lTau_l  = ngNuEFromW+"+"+ngNuMuFromW+"==1&&"+ngNuTauFromW+"==1&&Sum$(genTau_nNuE+genTau_nNuMu==1&&genTau_nNuTau==1)==1"
#hTau_H  = ngNuEFromW+"+"+ngNuMuFromW+"==0&&"+ngNuTauFromW+"==1&&Sum$(genTau_nNuE+genTau_nNuMu==0&&genTau_nNuTau==1)==1"
#hTau_l  = ngNuEFromW+'+'+ngNuMuFromW+"==1&&"+ngNuTauFromW+"==1&&Sum$(genTau_nNuE+genTau_nNuMu==0&&genTau_nNuTau==1)==1"
#diLepEff   = ngNuEFromW+"+"+ngNuMuFromW+"==2&&"+ngNuTauFromW+"==0&&Sum$(genLep_pt>10&&(abs(genLep_eta)<2.1&&abs(genLep_pdgId)==13||abs(genLep_eta)<2.4&&abs(genLep_pdgId)==11))==2"
#diLepAcc   = ngNuEFromW+"+"+ngNuMuFromW+"==2&&"+ngNuTauFromW+"==0&&Sum$(genLep_pt>10&&(abs(genLep_eta)<2.1&&abs(genLep_pdgId)==13||abs(genLep_eta)<2.4&&abs(genLep_pdgId)==11))!=2"
#diTau   = ngNuEFromW+"+"+ngNuMuFromW+"==0&&"+ngNuTauFromW+"==2"
#diHad   = ngNuEFromW+"+"+ngNuMuFromW+"==0&&"+ngNuTauFromW+"==0"
#l_H     = ngNuEFromW+"+"+ngNuMuFromW+"==1&&"+ngNuTauFromW+"==0"
##combined SubBkgs
#allHad = "(("+diHad+")||("+hTau_H+"))"
#allDiLep = ngNuEFromW+"+"+ngNuMuFromW+"==2&&"+ngNuTauFromW+"==0&&Sum$(genLep_pt>5)"


#'(singleLeptonic )&&( nLooseHardLeptons==1 )&&( nTightHardLeptons==1 )&&( nLooseSoftPt10Leptons==0 )&&( Jet_pt[1]>80 )&&( st>=150 )&&( st<250 )&&( htJet30j>=500 )&&( htJet30j<750 )&&( nJet30>=4 )&&( nJet30<=4 )&&( nBJetMediumCMVA30>=1 )&&( nBJetMediumCMVA30<=1 )&&( Sum$(abs(genPart_pdgId)==12 )&&( abs(genPart_motherId)==24)+Sum$(abs(genPart_pdgId)==14 )&&( abs(genPart_motherId)==24)==0 )&&( Sum$(abs(genPart_pdgId)==16 )&&( abs(genPart_motherId)==24)==1 )&&( Sum$(genTau_nNuE+genTau_nNuMu==1 )&&( genTau_nNuTau==1)==1 )&&( Jet_pt[2]>=80 )'


path=startpath
prepresel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80"
#prepresel = "singleLeptonic==1&&Jet_pt[1]>100&&Jet_pt[2]>80"
presel = prepresel

nothing='(1)'
subBkgTT=[
  ##[allHad, 'all hadronic', ROOT.kRed-7, 'all hadronic','placeholder'],
  [diHad,'two had.', ROOT.kRed-9,'diHad','dihadronic'],
  [diTau,'two #tau leptons', ROOT.kGreen+2,'diTau','di $\\tau$'],
  [hTau_H,'W#rightarrow#tau#nu#rightarrow had.+2#nu | W#rightarrow had.', ROOT.kRed-7, 'hadTau','$W\\rightarrow \\tau + \\nu \\rightarrow \\textrm{had.}+2\\nu ~|~ W \\rightarrow \\textrm{had.}$'],
  [hTau_l,'W#rightarrow#tau#nu#rightarrow had.+2#nu | W#rightarrow e/#mu+#nu', ROOT.kAzure+6,'hTau_l','$W\\rightarrow \\tau + \\nu \\rightarrow \\textrm{had.}+2\\nu ~|~ W \\rightarrow e/\\mu + \\nu$'],
  [lTau_l,'W#rightarrow#tau#nu#rightarrow e/#mu+3#nu | W#rightarrow e/#mu+#nu', ROOT.kOrange+1,'lTau_l','$W\\rightarrow \\tau + \\nu \\rightarrow e/\\mu+3\\nu ~|~ W \\rightarrow e/\\mu + \\nu$'],
  [lTau_H,'W#rightarrow#tau#nu#rightarrow e/#mu+3#nu | W#rightarrow had.', ROOT.kBlue-2, 'lepTau_H','$W\\rightarrow \\tau + \\nu \\rightarrow e/\\mu+3\\nu ~|~ W \\rightarrow \\textrm{had.}$'],
  [allDiLep,'dileptonic (e/#mu)',ROOT.kRed-3,'diLep','dileptonic'],
  #[diLepAcc,'dileptonic (e/#mu) Acc.',ROOT.kRed-3,'diLepAcc','placeholder'],
  #[diLepEff,'dileptonic (e/#mu) Eff.',ROOT.kRed-4,'diLepEff','placeholder'],
  #[jetFromW,'W#rightarrow#tau#rightarrow had./l | W#rightarrow h',ROOT.kBlue-2,'jetFromW','placeholder'],
  #[lepFromW,'W#rightarrow#tau#rightarrow had./l | W#rightarrow l',ROOT.kAzure+6,'lepFromW','placeholder'],
  [l_H, 'single lep. (e/#mu)',ROOT.kCyan+2,'singleLep','single lep. $(e/\\mu)$'],
  #[hadTau, 'W#rightarrow#tau#nu#rightarrow had.+2#nu | W#rightarrow had./lep',ROOT.kAzure+6, 'hadTau','placeholder'],
  #[lepTau, 'W#rightarrow#tau#nu#rightarrow e/#mu+3#nu | W#rightarrow had./lep',ROOT.kBlue-2, 'lepTau','placeholder']
  #[nothing,'tt Jets',ROOT.kBlue,'ttJets']
]

subBkgW=[
  [hTau_H,'W#rightarrow#tau#nu#rightarrow had.+2#nu', ROOT.kRed-7, 'hadTau','$W\\rightarrow \\tau + \\nu \\rightarrow \\textrm{had.}+2\\nu$'],#| W#rightarrow had.'
  [lTau_H,'W#rightarrow#tau#nu#rightarrow e/#mu+3#nu', ROOT.kBlue-2, 'lepTau_H','$W\\rightarrow \\tau + \\nu \\rightarrow e/\\mu+3\\nu$'],#| W#rightarrow had.'
  [l_H, 'single lep. (e/#mu)',ROOT.kCyan+2,'singleLep','single lep. $(e/\\mu)$']
]




#tot_lumi = 4000
#nevents = c.GetEntries()
#weight = "("+str(tot_lumi)+"*xsec)/"+str(nevents)
#print weight

#for i,bReg in enumerate(nBtagReg):
#  if i < len(nBtagReg)-1:
#    nbtagCutString='&&nBJetMediumCMVA30=='+str(bReg)
#    nbtagPath='nBtagEq'+str(bReg)+'/'
#  else:
#    nbtagCutString='&&nBJetMediumCMVA30>='+str(bReg)
#    nbtagPath='nBtagLEq'+str(bReg)+'/'
#  path+=nbtagPath
#  presel+=nbtagCutString
for hReg in htReg:
  if hReg[1]>0:
    htCutString='&&htJet30j>='+str(hReg[0])+'&&htJet30j<'+str(hReg[1])
    htPath=str(hReg[0])+'htJet30j'+str(hReg[1])+'/'
  else:
    htCutString='&&htJet30j>='+str(hReg[0])
    htPath=str(hReg[0])+'htJet30j/'
  for sReg in stReg:
    if sReg[1]>0:
      stCutString='&&st>='+str(sReg[0])+'&&st<'+str(sReg[1])
      stPath=str(sReg[0])+'st'+str(sReg[1])+'/'
    else:
      stCutString='&&st>='+str(sReg[0])
      stPath=str(sReg[0])+'st/'
    rcsHist0b=ROOT.TH1F('rcsh0b','rcsh0b',len(nJetReg),0,len(nJetReg))
    rcsHist1b=ROOT.TH1F('rcsh1b','rcsh1b',len(nJetReg),0,len(nJetReg))
    for ijReg,jReg in enumerate(nJetReg):
      if jReg[1]>0:
        njCutString='&&nJet30>='+str(jReg[0])+'&&nJet30<='+str(jReg[1])
        njPath=str(jReg[0])+'nJet30Eq'+str(jReg[1])+'/'
      else:
        njCutString='&&nJet30>='+str(jReg[0])
        njPath='nJet30LEq'+str(jReg[0])+'/'
      path=startpath+htPath+stPath+njPath
      if not os.path.exists(path):
        os.makedirs(path)

      prepresel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80"
      #prepresel = "singleLeptonic==1&&Jet_pt[1]>100&&Jet_pt[1]>80"
      presel = prepresel+htCutString+stCutString+njCutString#"htJet30j>=750&&htJet30j<=1000&&st>=450&&"+njetCutString+"&&"+nbtagCutString+'&&Jet_pt[1]>80'
      prefix= ''.join(presel.split('&&')[5:]).replace("&&","_").replace(">=","le_").replace("==","eq_")

      can1 = ROOT.TCanvas(varstring,varstring,1200,1000)
      
      h_Stack = ROOT.THStack('h_Stack',varstring)
      h_Stack_S = ROOT.THStack('h_Stack_S',varstring)
      
      yields=[]
      
      l = ROOT.TLegend(0.7,0.7,0.95,0.95)
      l.SetFillColor(ROOT.kWhite)
      l.SetShadowColor(ROOT.kWhite)
      l.SetBorderSize(1)
      totalh=ROOT.TH1F('total','Total 1b',*binning)
      totalh0b=ROOT.TH1F('total0b','Total 0b',*binning)
      totalh.Sumw2()
      totalh0b.Sumw2()
      c.Draw(varstring+'>>total','weight*('+presel+'&&nBJetMediumCMVA30==1)')
      c.Draw(varstring+'>>total0b','weight*('+presel+'&&nBJetMediumCMVA30==0)','goff')
      ##First Bin Normalisation
      #if totalh.GetBinContent(1)>0 and totalh0b.GetBinContent(1)>0:
      #  totalNorm=totalh.GetBinContent(1)/totalh0b.GetBinContent(1)
      #else:
      #  totalNorm=1.
      #First Bin Normalisation
      if totalh.GetSumOfWeights()>0 and totalh0b.GetSumOfWeights()>0:
        totalNorm=totalh.GetSumOfWeights()/totalh0b.GetSumOfWeights()
      else:
        totalNorm=1.
      c.Draw(varstring+'>>total0b',str(totalNorm)+'*weight*('+presel+'&&nBJetMediumCMVA30==0)')
      totalh.SetLineColor(ROOT.kBlue+3)
      totalh.SetLineWidth(2)
      totalh.SetMarkerSize(0)
      totalh.SetMarkerStyle(0)
      totalh.SetTitleSize(20)
      totalh.SetFillColor(0)
      totalh0b.SetLineColor(ROOT.kGreen+1)#kCyan+4
      totalh0b.SetLineWidth(2)
      totalh0b.SetMarkerSize(0)
      totalh0b.SetMarkerStyle(0)
      totalh0b.SetTitleSize(20)
      totalh0b.SetFillColor(0)
      l.AddEntry(totalh)
      l.AddEntry(totalh0b)
      for i, [cut,name,col,subname,texString] in enumerate(subBkgTT):
        histo = 'h'+str(i)
        histoname = histo
        print histoname
        histo = ROOT.TH1F(str(histo) ,str(histo),*binning)
        print histo
        print col
        wholeCut=presel+'&&nBJetMediumCMVA30==1&&'+cut
        print wholeCut
        c.Draw(varstring+'>>'+str(histoname),'weight*('+wholeCut+')')
        histo.SetLineColor(ROOT.kBlack)
        histo.SetLineWidth(1)
        histo.SetMarkerSize(0)
        histo.SetMarkerStyle(0)
        histo.SetTitleSize(20)
        histo.GetXaxis().SetTitle(varstring)
        histo.GetYaxis().SetTitle("Events / "+str( (binning[2] - binning[1])/binning[0]))
        histo.GetXaxis().SetLabelSize(0.04)
        histo.GetYaxis().SetLabelSize(0.04)
        histo.GetYaxis().SetTitleOffset(0.8)
        histo.GetYaxis().SetTitleSize(0.05)
        histo.SetFillColor(col)
        histo.SetFillStyle(1001)
        histo.SetMinimum(.08)
        h_Stack.Add(histo)
        l.AddEntry(histo, name)
        #RCS Backup calculation
        twoBin=[0,1,pi]
        rcsh=ROOT.TH1F('rcsh','rcsh',len(twoBin)-1, array('d', twoBin))
        c.Draw(varstring+'>>rcsh','weight*('+wholeCut+')','goff')
        rcsb=0
        if rcsh.GetBinContent(1)>0 and rcsh.GetBinContent(2)>0:
          rcsb=rcsh.GetBinContent(2)/rcsh.GetBinContent(1)
        
        can2=ROOT.TCanvas('sub','sub',800,600)
        histo.Draw()
        latex2 = ROOT.TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.035)
        latex2.SetTextAlign(11) # align right
        latex2.DrawLatex(0.7,0.96,str(rcsb))
        latex2.DrawLatex(0.16,0.96,name)
        can2.SetGrid()
        can2.SetLogy()
        can2.Print(path+varstring+subname+'_'+prefix+'notauRej.png')
        can2.Print(path+varstring+subname+'_'+prefix+'notauRej.root')
        
        canb = ROOT.TCanvas('canb','canb',800,600)
        histo1b = ROOT.TH1F('histo1b' ,'histo1b',*binning)
        histo0b = ROOT.TH1F('histo0b' ,'histo0b',*binning)
        histo1b.Sumw2()
        histo0b.Sumw2()
        histo1b.SetLineColor(ROOT.kBlack)
        histo1b.SetLineWidth(1)
        histo1b.SetMarkerSize(0)
        histo1b.SetMarkerStyle(0)
        histo1b.SetTitleSize(20)
        histo1b.GetXaxis().SetTitle(varstring)
        histo1b.GetYaxis().SetTitle("Events / "+str( (binning[2] - binning[1])/binning[0]))
        histo1b.GetXaxis().SetLabelSize(0.04)
        histo1b.GetYaxis().SetLabelSize(0.04)
        histo1b.GetYaxis().SetTitleOffset(0.8)
        histo1b.GetYaxis().SetTitleSize(0.05)
        histo1b.SetFillColor(col)
        histo1b.SetFillStyle(1001)
        histo1b.SetMinimum(.08)
        histo0b.SetLineColor(ROOT.kCyan+4)
        histo0b.SetLineWidth(2)
        histo0b.SetMarkerSize(0)
        histo0b.SetMarkerStyle(0)
        histo0b.SetTitleSize(20)
        histo0b.SetFillColor(0)
        wholeCut1 = wholeCut=presel+'&&nBJetMediumCMVA30==1&&'+cut
        #c.Draw(varstring+'>>histo1b','weight*('+wholeCut1+')')
        wholeCut0 = wholeCut=presel+'&&nBJetMediumCMVA30==0&&'+cut
        #c.Draw(varstring+'>>histo0b','weight*('+wholeCut0+')','goff')
        norm=1
        ##First Bin Normalisation
        #if histo1b.GetBinContent(1)>0 and histo0b.GetBinContent(1)>0:
        #  norm=histo1b.GetBinContent(1)/histo0b.GetBinContent(1)
        ##Area Normalisation
        #if histo1b.GetSumOfWeights()>0 and histo0b.GetSumOfWeights()>0:
        #  norm=histo1b.GetSumOfWeights()/histo0b.GetSumOfWeights()
        #
        #c.Draw(varstring+'>>histo0b',str(norm)+'*weight*('+wholeCut0+')')
        
        ##Calculation of RCS value, works only for cut at dPhi=1 atm
        #bins=1/(binning[2]/binning[0])
        #i=1+int(bins)
        #rcs0=0
        #rcsz0=0
        #rcsn0=0
        #rcs1=0
        #rcsz1=0
        #rcsn1=0
        #total0=histo0b.GetSumOfWeights()
        #total1=histo1b.GetSumOfWeights()
        #while i <= binning[0]:
        #  rcsz0+=histo0b.GetBinContent(i)
        #  rcsz1+=histo1b.GetBinContent(i)
        #  i+=1
        #i=1
        #while i<= int(bins):
        #  rcsn0+=histo0b.GetBinContent(i)
        #  rcsn1+=histo1b.GetBinContent(i)
        #  i+=1
        #if rcsn0>0:
        #  rcs0=rcsz0/rcsn0
        #else:
        #  rcs0=float('nan')
  
        #if rcsn1>0:
        #  rcs1=rcsz1/rcsn1
        #else:
        #  rcs1=float('nan')
        #rcsn0=rcsn0/norm
        #rcsz0=rcsz0/norm

        #RCS Backup calculation
        twoBin=[0,deltaPhiCut,pi]
        rcs0=ROOT.TH1F('rcs0','rcs0',len(twoBin)-1, array('d', twoBin))
        rcs1=ROOT.TH1F('rcs1','rcs1',len(twoBin)-1, array('d', twoBin))
        c.Draw(varstring+'>>rcs0','weight*('+wholeCut0+')','goff')
        c.Draw(varstring+'>>rcs1','weight*('+wholeCut1+')','goff')
        rcs0v=0
        rcs1v=0
        if rcs0.GetBinContent(1)>0:
          rcs0v=rcs0.GetBinContent(2)/rcs0.GetBinContent(1)
        else:
          rcs0v=float('nan')
        if rcs1.GetBinContent(1)>0:
          rcs1v=rcs1.GetBinContent(2)/rcs1.GetBinContent(1)
        else:
          rcs1v=float('nan')
        
        if rcs1.GetSumOfWeights()>0 and rcs0.GetSumOfWeights()>0:
          norm=rcs1.GetSumOfWeights()/rcs0.GetSumOfWeights()
        
        c.Draw(varstring+'>>histo1b','weight*('+wholeCut1+')')
        c.Draw(varstring+'>>histo0b',str(norm)+'*weight*('+wholeCut0+')')        


        histo1b.Draw('hist')
        histo1b.Draw('e1same')
        histo0b.Draw('hist same')
        histo0b.Draw('e1same')
        latex3 = ROOT.TLatex()
        latex3.SetNDC()
        latex3.SetTextSize(0.035)
        latex3.SetTextAlign(11) # align right
        #latex3.DrawLatex(0.45,0.91,'Y(0b,#Delta#Phi<1)='+str(round(rcsn0,2)))
        #latex3.DrawLatex(0.45,0.86,'Y(0b,#Delta#Phi>1)='+str(round(rcsz0,2)))
        #latex3.DrawLatex(0.45,0.81,'R(0b)='+str(round(rcs0,4)))
        #latex3.DrawLatex(0.7,0.91,'Y(1b,#Delta#Phi<1)='+str(round(rcsn1,2)))
        #latex3.DrawLatex(0.7,0.86,'Y(1b,#Delta#Phi>1)='+str(round(rcsz1,2)))
        #latex3.DrawLatex(0.7,0.81,'R(1b)='+str(round(rcs1,4)))
        #latex3.DrawLatex(0.45,0.76,'Norm 1b/0b='+str(round(norm,2)))
        latex3.DrawLatex(0.16,0.96,name)
        canb.SetLogy()
        canb.SetGrid()
        canb.Print(path+varstring+subname+'_'+prefix+'1bvs0b.png')
        canb.Print(path+varstring+subname+'_'+prefix+'1bvs0b.root')
        yields.append({'name':subname, 'title':texString, 'yield0bTotal':rcs0.GetSumOfWeights(),'yield1bTotal':rcs1.GetSumOfWeights(),'norm':norm,'rcs0b':rcs0v,'rcs1b':rcs1v,'yield0bC':rcs0.GetBinContent(1),'yield0bS':rcs0.GetBinContent(2),'yield1bC':rcs1.GetBinContent(1),'yield1bS':rcs1.GetBinContent(2)})
      can1.cd()
      can1.SetGrid()
      h_Stack.Draw()
      totalh.Draw('same')
      totalh.Draw('hist same')
      totalh0b.Draw('same')
      totalh0b.Draw('hist same')
      h_Stack.SetMinimum(0.08)
      l.Draw()
      
      #RCS Backup calculation
      twoBin=[0,deltaPhiCut,pi]
      rcs0=ROOT.TH1F('rcs0','rcs0',len(twoBin)-1, array('d', twoBin))
      rcs1=ROOT.TH1F('rcs1','rcs1',len(twoBin)-1, array('d', twoBin))
      rcs0.Sumw2()
      rcs1.Sumw2()
      c.Draw(varstring+'>>rcs0','weight*('+presel+'&&nBJetMediumCMVA30==0)','goff')
      c.Draw(varstring+'>>rcs1','weight*('+presel+'&&nBJetMediumCMVA30==1)','goff')
      rcs0v=0
      rcs1v=0
      if rcs0.GetBinContent(1)>0:
        rcs0v=rcs0.GetBinContent(2)/rcs0.GetBinContent(1)
      else:
        rcs0v=float('nan')
      if rcs1.GetBinContent(1)>0:
        rcs1v=rcs1.GetBinContent(2)/rcs1.GetBinContent(1)
      else:
        rcs1v=float('nan')
      rcsHist0b.SetBinContent(ijReg+1,rcs0v)
      
      if rcs0.GetBinContent(1)>0 and rcs0.GetBinContent(2)>0:
        rcsHist0b.SetBinError(ijReg+1, rcs0v*sqrt(rcs0.GetBinError(2)**2/rcs0.GetBinContent(2)**2 + rcs0.GetBinError(1)**2/rcs0.GetBinContent(1)**2))
      else:
        rcsHist0b.SetBinError(ijReg+1,0)
      rcsHist1b.SetBinContent(ijReg+1,rcs1v)
      if rcs1.GetBinContent(1)>0 and rcs1.GetBinContent(2)>0:
        rcsHist1b.SetBinError(ijReg+1, rcs1v*sqrt(rcs1.GetBinError(2)**2/rcs1.GetBinContent(2)**2 + rcs1.GetBinError(1)**2/rcs1.GetBinContent(1)**2))
      else:
        rcsHist1b.SetBinError(ijReg+1,0)
      rcsHist0b.GetXaxis().SetBinLabel(ijReg+1,str(jReg))
      ##Calculation of RCS value, works only for cut at dPhi=1 atm
      #bins=1/(binning[2]/binning[0])
      #i=1+int(bins)
      #rcsz1=0
      #rcsn1=0
      #rcsz0=0
      #rcsn0=0
      #total1=h_Stack.GetStack().Last().GetSumOfWeights()
      #total0=totalh0b.GetSumOfWeights()
      #while i <= binning[0]:
      #  rcsz1+=h_Stack.GetStack().Last().GetBinContent(i)
      #  rcsz0+=totalh0b.GetBinContent(i)
      #  i=i+1
      #i=1
      #while i<= int(bins):
      #  rcsn1+=h_Stack.GetStack().Last().GetBinContent(i)
      #  rcsn0+=totalh0b.GetBinContent(i)
      #  i=i+1
      #if rcsn1>0:
      #  rcs1=rcsz1/rcsn1
      #else:
      #  rcs1=float('nan')
      #print rcs1
      #if rcsn0>0:
      #  rcs0=rcsz0/rcsn0
      #else:
      #  rcs0=float('nan')
      #print rcs0
      latex1 = ROOT.TLatex()
      latex1.SetNDC()
      latex1.SetTextSize(0.035)
      latex1.SetTextAlign(11) # align right
      latex1.DrawLatex(0.16,0.96,"CMS simulation")
      latex1.DrawLatex(0.7,0.96,"L=4 fb^{-1} (13TeV)")
      
      #rcsz0=rcsz0/totalNorm
      #rcsn0=rcsn0/totalNorm
      yields.append({'name':'total', 'title':'total', 'yield0bTotal':rcs0.GetSumOfWeights(),'yield1bTotal':rcs1.GetSumOfWeights(),'norm':totalNorm,'rcs0b':rcs0v,'rcs1b':rcs1v,'yield0bC':rcs0.GetBinContent(1),'yield0bS':rcs0.GetBinContent(2),'yield1bC':rcs1.GetBinContent(1),'yield1bS':rcs1.GetBinContent(2)})
      #latexN = ROOT.TLatex()
      #latexN.SetNDC()
      #latexN.SetTextSize(0.025)
      #latexN.SetTextAlign(11) # align right
      #latexN.DrawLatex(0.5,0.91,"Y(0b,#Delta#Phi <1)="+str(round(rcsn0,2)))
      #latexN.DrawLatex(0.5,0.87,"Y(0b,#Delta#Phi >1)="+str(round(rcsz0,2)))
      #latexN.DrawLatex(0.5,0.83,"R_{CS}(0b)="+str(round(rcs0,4)))
      #latexN.DrawLatex(0.5,0.79,"Y(1b,#Delta#Phi <1)="+str(round(rcsn1,2)))
      #latexN.DrawLatex(0.5,0.75,"Y(1b,#Delta#Phi >1)="+str(round(rcsz1,2)))
      #latexN.DrawLatex(0.5,0.71,"R_{CS}(1b)="+str(round(rcs1,4)))
      #latexN.DrawLatex(0.5,0.67,"Norm 1b/0b ="+str(round(totalNorm,2)))
      can1.SetLogy()
      can1.Print(path+varstring+'_'+prefix+'notauRej.png')
      can1.Print(path+varstring+'_'+prefix+'notauRej.root')
      yieldFile=open(path+"yields.pkl","w")
      pickle.dump(yields,yieldFile)
      yieldFile.close()
    ROOT.gStyle.SetErrorX(0.5)
    canR=ROOT.TCanvas('RCS','RCS',800,600)
    rcsHist1b.SetMarkerSize(0)
    rcsHist0b.SetMarkerSize(0)
    rcsHist1b.SetLineColor(ROOT.kGreen+2)
    rcsHist0b.SetLineColor(ROOT.kBlue+1)
    rcsHist0b.SetLineWidth(1)
    rcsHist1b.SetLineWidth(1)
    rcsHist0b.SetMinimum(0.)
    rcsHist0b.SetMaximum(0.15)
    rcsHist0b.GetXaxis().SetTitle("n_jets")
    rcsHist0b.GetYaxis().SetTitle("Rcs")
    rcsHist0b.GetXaxis().SetLabelSize(0.07)
    rcsHist0b.GetYaxis().SetLabelSize(0.04)
    rcsHist0b.GetYaxis().SetTitleOffset(0.9)
    rcsHist0b.GetYaxis().SetTitleSize(0.05)
    rcsHist0b.Draw('e')
    rcsHist1b.Draw('e same')
    canR.Print(path+varstring+'_RCS.png')
