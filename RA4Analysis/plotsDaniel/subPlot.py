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

nBtagReg=[(0,0),(1,1)]#,(2,-1)]
nJetReg=[(4,5)]#,(3,3),(4,4),(5,5),(6,-1)]
stReg=[(250,-1)]#,(350,450),(450,-1)]
htReg=[(500,750)]#,(750,1000),(1000,1250),(1250,-1)]

startpath = '/afs/hephy.at/user/d/dspitzbart/www/subBkgttJetCorF/'

#Load the Background Chain
c = getChain(ttJets[lepSel],histname='')

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

path=startpath
prepresel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80"
presel = prepresel

nothing='(1)'
subBkgTT=[
  ##[allHad, 'all hadronic', ROOT.kRed-7, 'all hadronic'],
  [diHad,'two had.', ROOT.kRed-9,'diHad'],
  [hTau_H,'W#rightarrow#tau#nu#rightarrow had.+2#nu | W#rightarrow had.', ROOT.kRed-7, 'hadTau'],
  [lTau_H,'W#rightarrow#tau#nu#rightarrow e/#mu+3#nu | W#rightarrow had.', ROOT.kBlue-2, 'lepTau_H'],
  [diTau,'two #tau leptons', ROOT.kGreen+3,'diTau'],
  [lTau_l,'W#rightarrow#tau#nu#rightarrow e/#mu+3#nu | W#rightarrow e/#mu+#nu', ROOT.kOrange+1,'lTau_l'],
  [allDiLep,'dileptonic (e/#mu)',ROOT.kRed-3,'diLep'],
  #[diLepAcc,'dileptonic (e/#mu) Acc.',ROOT.kRed-3,'diLepAcc'],
  #[diLepEff,'dileptonic (e/#mu) Eff.',ROOT.kRed-4,'diLepEff'],
  [hTau_l,'W#rightarrow#tau#nu#rightarrow had.+2#nu | W#rightarrow e/#mu+#nu', ROOT.kAzure+6,'hTau_l'],
  #[jetFromW,'W#rightarrow#tau#rightarrow had./l | W#rightarrow h',ROOT.kBlue-2,'jetFromW'],
  #[lepFromW,'W#rightarrow#tau#rightarrow had./l | W#rightarrow l',ROOT.kAzure+6,'lepFromW'],
  [l_H, 'single lep. (e/#mu)',ROOT.kCyan+3,'singleLep'],
  #[nothing,'tt Jets',ROOT.kBlue,'ttJets']
]

subBkgW=[
  [hTau_H,'W#rightarrow#tau#nu#rightarrow had.+2#nu', ROOT.kRed-7, 'hadTau'],#| W#rightarrow had.'
  [lTau_H,'W#rightarrow#tau#nu#rightarrow e/#mu+3#nu', ROOT.kBlue-2, 'lepTau_H'],#| W#rightarrow had.'
  [l_H, 'single lep. (e/#mu)',ROOT.kCyan+3,'singleLep']
]

for nb in nBtagReg:
  if nb[1]>0:
    nbPath=str(nb[0])+'nb'+str(nb[1])+'/'
  else:
    nbPath='_'+str(nb[0])+'nb/'
  for hReg in htReg:
    if hReg[1]>0:
      htPath=str(hReg[0])+'htJet30j'+str(hReg[1])+'/'
    else:
      htPath='_'+str(hReg[0])+'htJet30j/'
    for sReg in stReg:
      if sReg[1]>0:
        stPath=str(sReg[0])+'st'+str(sReg[1])+'/'
      else:
        stPath='_'+str(sReg[0])+'st/'
      for nj in nJetReg:
        if nj[1]>0:
          njPath=str(nj[0])+'nj'+str(nj[1])+'/'
        else:
          njPath='_'+str(nj[0])+'nj/'
        path=startpath+nbPath+htPath+stPath+njPath
        if not os.path.exists(path):
          os.makedirs(path)
        

        cname, cut = nameAndCut(sReg,hReg,nj, btb=nb ,presel=presel) 
        print cut
        totalh=ROOT.TH1F('total','Total',*binning)
        c.Draw(varstring+'>>totalh',cut)
        h_Stack = ROOT.THStack('h_Stack',varstring)
        h_Stack_S = ROOT.THStack('h_Stack_S',varstring)
        l = ROOT.TLegend(0.7,0.7,0.95,0.95)
        l.SetFillColor(ROOT.kWhite)
        l.SetShadowColor(ROOT.kWhite)
        l.SetBorderSize(1)
        l.AddEntry(totalh)
        for i, [subcut,name,col,subname] in enumerate(subBkgTT):
          histo = 'h'+str(i)
          histoname = histo
          print histoname
          histo = ROOT.TH1F(str(histo) ,str(histo),*binning)
          print histo
          print col
          wholeCut=cut+'&&'+subcut
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
          can2.Print(path+varstring+subname+'_'+cname+'notauRej.png')
          can2.Print(path+varstring+subname+'_'+cname+'notauRej.root')

        can1.cd()
        can1.SetGrid()
        h_Stack.Draw()
        totalh.SetLineColor(ROOT.kBlue+3)
        totalh.SetLineWidth(2)
        totalh.SetMarkerSize(0)
        totalh.SetMarkerStyle(0)
        totalh.SetTitleSize(20)
        totalh.SetFillColor(0)

        totalh.Draw('same')
        h_Stack.SetMinimum(0.08)
        l.Draw()

        #Calculation of RCS value, works only for cut at dPhi=1 atm
        bins=1/(binning[2]/binning[0])
        i=1+int(bins)
        rcs=0
        rcsn=0
        total=h_Stack.GetStack().Last().GetSumOfWeights()
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
        latex1.DrawLatex(0.16,0.96,"Rcs="+str(round(rcs,40))+' T:'+str(round(total,2)))
        latex1.DrawLatex(0.7,0.96,"L=4 fb^{-1} (13TeV)")


        can1.SetLogy()
        can1.Print(path+varstring+'_'+cname+'notauRej.png')
        can1.Print(path+varstring+'_'+cname+'notauRej.root')

