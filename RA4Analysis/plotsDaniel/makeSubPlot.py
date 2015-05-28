import ROOT
import os, sys, copy

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
from array import array

from Workspace.HEPHYPythonTools.helpers import getVarValue, getChain, deltaPhi
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400ST150_withDF import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2 import *
from Workspace.RA4Analysis.helpers import *

varstring='deltaPhi_Wl'
binning=[16,0,3.2]
lepSel = 'hard'
nbtagCut=0
njetCut=2

nBtagReg=[0,1,2]
nJetReg=[2,3,4,5,6]
stReg=[(150,-1)]#250),(250,350),(350,450),(450,-1)]
htReg=[(500,-1)]#750),(750,1000),(1000,1250),(1250,-1)]

startpath = '/afs/hephy.at/user/d/dspitzbart/www/subBkgInclusive/'

#Load the Background Chain
c = getChain(ttJets[lepSel],histname='')

#Sub Background Definitions
ngNuEFromW = "Sum$(abs(genPart_pdgId)==12&&abs(genPart_motherId)==24)"
ngNuMuFromW = "Sum$(abs(genPart_pdgId)==14&&abs(genPart_motherId)==24)"
ngNuTauFromW = "Sum$(abs(genPart_pdgId)==16&&abs(genPart_motherId)==24)"
lTau_H  = ngNuEFromW+"+"+ngNuMuFromW+"==0&&"+ngNuTauFromW+"==1"\
          +"&&Sum$(genTau_nNuE+genTau_nNuMu==1&&genTau_nNuTau==1)==1"
hTau_l=     "Sum$((abs(genPart_pdgId)==14||abs(genPart_pdgId)==12)&&abs(genPart_motherId)==24)==1"\
            +"&&Sum$(abs(genPart_pdgId)==16&&abs(genPart_motherId)==24)==1"\
            +"&&Sum$(genTau_nNuE+genTau_nNuMu==0&&genTau_nNuTau==1)==1"
diLepEff   = ngNuEFromW+"+"+ngNuMuFromW+"==2&&"+ngNuTauFromW+"==0&&Sum$(genLep_pt>10&&(abs(genLep_eta)<2.1&&abs(genLep_pdgId)==13||abs(genLep_eta)<2.4&&abs(genLep_pdgId)==11))==2"
diLepAcc   = ngNuEFromW+"+"+ngNuMuFromW+"==2&&"+ngNuTauFromW+"==0&&Sum$(genLep_pt>10&&(abs(genLep_eta)<2.1&&abs(genLep_pdgId)==13||abs(genLep_eta)<2.4&&abs(genLep_pdgId)==11))!=2"
lTau_l  = ngNuEFromW+"+"+ngNuMuFromW+"==1&&"+ngNuTauFromW+"==1&&Sum$(genTau_nNuE+genTau_nNuMu==1&&genTau_nNuTau==1)==1"
diTau   = ngNuEFromW+"+"+ngNuMuFromW+"==0&&"+ngNuTauFromW+"==2"
l_H     =  ngNuEFromW+"+"+ngNuMuFromW+"==1&&"+ngNuTauFromW+"==0"
diHad   = ngNuEFromW+"+"+ngNuMuFromW+"==0&&"+ngNuTauFromW+"==0"
hTau_H  = ngNuEFromW+"+"+ngNuMuFromW+"==0&&"+ngNuTauFromW+"==1&&Sum$(genTau_nNuE+genTau_nNuMu==0&&genTau_nNuTau==1)==1"
allHad = "(("+diHad+")||("+hTau_H+"))"


#tot_lumi = 4000
#nevents = c.GetEntries()
#weight = "("+str(tot_lumi)+"*xsec)/"+str(nevents)
#print weight

for i,bReg in enumerate(nBtagReg):
  if i < len(nBtagReg)-1:
    nbtagCutString='&&nBJetMediumCMVA30=='+str(bReg)
    nbtagPath='nBtagEq'+str(bReg)+'/'
  else:
    nbtagCutString='&&nBJetMediumCMVA30>='+str(bReg)
    nbtagPath='nBtagLEq'+str(bReg)+'/'
  for j, hReg in enumerate(htReg):
    if j < len(htReg)-1:
      htCutString='&&htJet30j>='+str(hReg[0])+'&&htJet30j<'+str(hReg[1])
      htPath=str(hReg[0])+'htJet30j'+str(hReg[1])+'/'
    else:
      htCutString='&&htJet30j>='+str(hReg[0])
      htPath='_'+str(hReg[0])+'htJet30j/'
    for k,sReg in enumerate(stReg):
      if k < len(stReg)-1:
        stCutString='&&st>='+str(sReg[0])+'&&st<'+str(sReg[1])
        stPath=str(sReg[0])+'st'+str(sReg[1])+'/'
      else:
        stCutString='&&st>='+str(sReg[0])
        stPath='_'+str(sReg[0])+'st/'  
      for l,jReg in enumerate(nJetReg):
        if l < len(nJetReg)-1:
          njCutString='&&nJet30=='+str(jReg)
          njPath='nJet30Eq'+str(jReg)+'/'
        else:
          njCutString='&&nJet30>='+str(jReg)
          njPath='nJet30LEq'+str(jReg)+'/'
        path=startpath+nbtagPath+htPath+stPath+njPath
        if not os.path.exists(path):
          os.makedirs(path)
        
        prepresel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80"
        presel = prepresel+nbtagCutString+htCutString+stCutString+njCutString#"htJet30j>=750&&htJet30j<=1000&&st>=450&&"+njetCutString+"&&"+nbtagCutString+'&&Jet_pt[1]>80'
        prefix= ''.join(presel.split('&&')[5:]).replace("&&","_").replace(">=","le_").replace("==","eq_")

        can1 = ROOT.TCanvas(varstring,varstring,1200,1000)
        
        h_Stack = ROOT.THStack('h_Stack',varstring)
        h_Stack_S = ROOT.THStack('h_Stack_S',varstring)
        
        l = ROOT.TLegend(0.7,0.7,0.95,0.95)
        l.SetFillColor(ROOT.kWhite)
        l.SetShadowColor(ROOT.kWhite)
        l.SetBorderSize(1)
        nothing='(1)'
        subBkg=[
          ##[allHad, 'all hadronic', ROOT.kRed-7, 'all hadronic'],
          [diHad,'two had.', ROOT.kRed-9,'diHad'],
          [hTau_H,'W#rightarrow#tau#nu#rightarrow had.+2#nu | W#rightarrow had.', ROOT.kRed-7, 'hadTau'],
          [lTau_H,'W#rightarrow#tau#nu#rightarrow e/#mu+3#nu | W#rightarrow had.', ROOT.kBlue-2, 'lepTau_H'],
          [diTau,'two #tau leptons', ROOT.kGreen+3,'diTau'],
          [lTau_l,'W#rightarrow#tau#nu#rightarrow e/#mu+3#nu | W#rightarrow e/#mu+#nu', ROOT.kOrange+1,'lTau_l'],
          [diLepAcc,'dileptonic (e/#mu) Acc.',ROOT.kRed-3,'diLepAcc'],
          [diLepEff,'dileptonic (e/#mu) Eff.',ROOT.kRed-4,'diLepEff'],
          [hTau_l,'W#rightarrow#tau#nu#rightarrow had.+2#nu | W#rightarrow e/#mu+#nu', ROOT.kAzure+6,'hTau_l'],
          [l_H, 'single lep. (e/#mu)',ROOT.kCyan+3,'singleLep']
          #[nothing,'tt Jets',ROOT.kBlue,'ttJets']
        ]
        totalh=ROOT.TH1F('total','Total',*binning)
        c.Draw(varstring+'>>total','weight*('+presel+')')
        totalh.SetLineColor(ROOT.kBlue+3)
        totalh.SetLineWidth(2)
        totalh.SetMarkerSize(0)
        totalh.SetMarkerStyle(0)
        totalh.SetTitleSize(20)
        totalh.SetFillColor(0)
        l.AddEntry(totalh)
        for i, [cut,name,col,subname] in enumerate(subBkg):
          histo = 'h'+str(i)
          histoname = histo
          print histoname
          histo = ROOT.TH1F(str(histo) ,str(histo),*binning)
          print histo
          print col
          wholeCut=presel+'&&'+cut
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
        
        can1.cd()
        can1.SetGrid()
        h_Stack.Draw()
        totalh.Draw('same')
        h_Stack.SetMinimum(0.08)
        l.Draw()

        #Calculation of RCS value, works only for cut at dPhi=1 atm
        bins=1/(binning[2]/binning[0])
        i=1+int(bins)
        rcs=0
        rcsn=0
        while i <= binning[0]:
          rcs=rcs+h_Stack.GetStack().Last().GetBinContent(i)
          i=i+1
        i=1
        while i<= int(bins):
          rcsn=rcsn+h_Stack.GetStack().Last().GetBinContent(i)
          i=i+1
        if rcsn>0:
          rcs=rcs/rcsn
        else:
          rcs=float('nan')
        print rcs
        latex1 = ROOT.TLatex()
        latex1.SetNDC()
        latex1.SetTextSize(0.035)
        latex1.SetTextAlign(11) # align right
        latex1.DrawLatex(0.16,0.96,"Rcs="+str(rcs))
        latex1.DrawLatex(0.72,0.96,"L=4 fb^{-1} (13TeV)")
        
        
        can1.SetLogy()
        can1.Print(path+varstring+'_'+prefix+'notauRej.png')
        can1.Print(path+varstring+'_'+prefix+'notauRej.root')

