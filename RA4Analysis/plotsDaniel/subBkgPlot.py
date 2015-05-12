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
from Workspace.RA4Analysis.helpers import *

#ROOT.TH1F().SetDefaultSumw2()

deltaPhiCut=1.
varstring='deltaPhi_Wl'
binning=[16,0,3.2]
twoBin=[0,deltaPhiCut,3.2]
lepSel = 'hard'

nBtagReg=[(0,0),(1,1)]#,(2,-1)]
nJetReg=[(4,-1)]#,(3,3),(4,4),(5,5),(6,-1)]
stReg=[(250,-1)]#,(350,450),(450,-1)]
htReg=[(500,-1)]#,(750,1000),(1000,1250),(1250,-1)]

colorList=[ROOT.kCyan+2, ROOT.kMagenta+2, ROOT.kOrange+2,ROOT.kMagenta+2]

startpath = '/afs/hephy.at/user/d/dspitzbart/www/subBkgFinalCodeTest/'


#Load the Background Chain
c = getChain(ttJets[lepSel],histname='')
#c = getChain(WJetsHTToLNu[lepSel],histname='')

#Sub Background Definitions
ngNuEFromW = "(Sum$(abs(genPart_pdgId)==12&&abs(genPart_motherId)==24))"
ngNuMuFromW = "(Sum$(abs(genPart_pdgId)==14&&abs(genPart_motherId)==24))"
ngNuTauFromW = "(Sum$(abs(genPart_pdgId)==16&&abs(genPart_motherId)==24))"
lTau_H  = '('+ngNuEFromW+"+"+ngNuMuFromW+")==0&&"+ngNuTauFromW+"==1&&(Sum$(genTau_nNuE+genTau_nNuMu==1&&genTau_nNuTau==1))==1"
lTau_l  = '('+ngNuEFromW+"+"+ngNuMuFromW+")==1&&"+ngNuTauFromW+"==1&&(Sum$(genTau_nNuE+genTau_nNuMu==1&&genTau_nNuTau==1))==1"
hTau_H  = '('+ngNuEFromW+"+"+ngNuMuFromW+")==0&&"+ngNuTauFromW+"==1&&(Sum$(genTau_nNuE+genTau_nNuMu==0&&genTau_nNuTau==1))==1"
hTau_l  = '('+ngNuEFromW+'+'+ngNuMuFromW+")==1&&"+ngNuTauFromW+"==1&&(Sum$(genTau_nNuE+genTau_nNuMu==0&&genTau_nNuTau==1))==1"
diLepEff   = ngNuEFromW+"+"+ngNuMuFromW+"==2&&"+ngNuTauFromW+"==0&&(Sum$(genLep_pt>10&&(abs(genLep_eta)<2.1&&abs(genLep_pdgId)==13||abs(genLep_eta)<2.4&&abs(genLep_pdgId)==11)))==2"
diLepAcc   = ngNuEFromW+"+"+ngNuMuFromW+"==2&&"+ngNuTauFromW+"==0&&(Sum$(genLep_pt>10&&(abs(genLep_eta)<2.1&&abs(genLep_pdgId)==13||abs(genLep_eta)<2.4&&abs(genLep_pdgId)==11)))!=2"
diTau   = '('+ngNuEFromW+"+"+ngNuMuFromW+")==0&&"+ngNuTauFromW+"==2"
diHad   = '('+ngNuEFromW+"+"+ngNuMuFromW+")==0&&"+ngNuTauFromW+"==0"
l_H     = '('+ngNuEFromW+"+"+ngNuMuFromW+")==1&&"+ngNuTauFromW+"==0"
#combined SubBkgs
allHad = "(("+diHad+")||("+hTau_H+"))"
allDiLep = '('+ngNuEFromW+"+"+ngNuMuFromW+")==2&&"+ngNuTauFromW+"==0"#&&Sum$(genLep_pt>10)"#should not be necessary
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

totalCan = ROOT.TCanvas('total','total',1000,1000)
subCan = ROOT.TCanvas('sub','sub',800,800)
rcsCan = ROOT.TCanvas('rcs','rcs',800,800)

totalCan.SetLogy()
totalCan.SetGrid()
subCan.SetLogy()
subCan.SetGrid()

mainHist = ROOT.TH1F('mainHist' ,'mainHist',*binning)
compHist = ROOT.TH1F('compHist','compHist',*binning)
normHist=ROOT.TH1F('normHist','normHist',len(twoBin)-1, array('d', twoBin))

rcsHist=ROOT.TH1F('rcsHist','rcsHist',len(nJetReg),0,len(nJetReg))

mainHist.Sumw2()
compHist.Sumw2()
normHist.Sumw2()

mainHist.SetLineColor(ROOT.kBlack)
mainHist.SetLineWidth(1)
mainHist.SetMarkerSize(0)
mainHist.SetMarkerStyle(0)
mainHist.SetTitleSize(20)
mainHist.GetXaxis().SetTitle(varstring)
mainHist.GetYaxis().SetTitle("Events")
mainHist.GetXaxis().SetLabelSize(0.04)
mainHist.GetYaxis().SetLabelSize(0.04)
mainHist.GetYaxis().SetTitleOffset(0.8)
mainHist.GetYaxis().SetTitleSize(0.05)
mainHist.SetFillStyle(1001)
mainHist.SetMinimum(.08)

compHist.SetLineWidth(2)
compHist.SetMarkerSize(0)
compHist.SetMarkerStyle(0)
compHist.SetFillColor(0)

rcsHist.SetMarkerSize(0)
rcsHist.SetLineWidth(1)
rcsHist.SetMinimum(0.)
rcsHist.SetMaximum(0.15)
rcsHist.GetXaxis().SetTitle("n_jets")
rcsHist.GetYaxis().SetTitle("Rcs")
rcsHist.GetXaxis().SetLabelSize(0.07)
rcsHist.GetYaxis().SetLabelSize(0.04)
rcsHist.GetYaxis().SetTitleOffset(0.9)
rcsHist.GetYaxis().SetTitleSize(0.05)


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
    
    for ijReg,jReg in enumerate(nJetReg):
      first = True
      if jReg[1]>0:
        njCutString='&&nJet30>='+str(jReg[0])+'&&nJet30<='+str(jReg[1])
        njPath=str(jReg[0])+'nJet30Eq'+str(jReg[1])+'/'
      else:
        njCutString='&&nJet30>='+str(jReg[0])
        njPath='nJet30LEq'+str(jReg[0])+'/'
      path=startpath+htPath+stPath+njPath

      if not os.path.exists(path):
        os.makedirs(path)
      print 'Processing nJets ' + str(jReg)
      print ' '
      
      h_Stack = ROOT.THStack('h_Stack',varstring)
      
      totalL = ROOT.TLegend(0.7,0.7,0.95,0.95)
      totalL.SetFillColor(ROOT.kWhite)
      totalL.SetShadowColor(ROOT.kWhite)
      totalL.SetBorderSize(1)

      #Get yields for norm & rcs
      for i, [subcut,name,col,subname,texString] in enumerate(subBkgTT):
        print 'Processing ' + subname        
        subYields=[]
        histo = 'h'+str(i)
        histoname = histo
        #print histoname
        binning = [16,0,3.2]
        histo = ROOT.TH1F(str(histo) ,subname,*binning)
        for bs in nBtagReg:
          #normHist.Reset()
          cutname,cut=nameAndCut(sReg, hReg, jReg, btb=bs, presel=prepresel)
          wholecut = cut + '&&' + subcut
          print wholecut
          c.Draw(varstring+'>>normHist','weight*('+wholecut+')','goff')
          totalYield=normHist.GetSumOfWeights()
          signalYield=normHist.GetBinContent(2)
          controlYield=normHist.GetBinContent(1)
          if controlYield>0:
            rcs=signalYield/controlYield
          else:
            rcs=0.
          print jReg, bs, rcs, totalYield
          subYields.append({'nbjets':bs,'totalYield':totalYield,'controlYield':controlYield,'signalYield':signalYield,'rcs':rcs})
        
        #make sub plots
        subCan.cd()
        
        pad1 = ROOT.TPad('pad1','pad1',0,0.3,1.,1.)
        pad1.SetBottomMargin(0)
        pad1.SetLeftMargin(0.1)
        pad1.SetGrid()
        pad1.SetLogy()
        pad1.Draw()
        pad1.cd()
        
        l = ROOT.TLegend(0.7,0.8,0.95,0.95)
        l.SetFillColor(ROOT.kWhite)
        l.SetShadowColor(ROOT.kWhite)
        l.SetBorderSize(1)

        cutname,cut=nameAndCut(sReg, hReg, jReg, btb=nBtagReg[0], presel=prepresel)
        wholecut = cut + '&&' + subcut
        c.Draw(varstring+'>>'+str(histoname),'weight*('+wholecut+')')
        histo.SetFillColor(col)
        histo.SetLineColor(col+2)
        histo.SetMarkerSize(0)
        h_Stack.Add(histo)
        totalL.AddEntry(histo)
        compHists = []
        first = True
        
        for ibs,bs in enumerate(nBtagReg):
          namecut,cut=nameAndCut(sReg, hReg, jReg, btb=bs, presel=prepresel)
          wholecut=cut+'&&'+subcut
          compHist = 'ch'+str(i)
          histoname = compHist
          compHist = ROOT.TH1F(str(histoname),str(bs) + ' b-tags',*binning)
          compHist.SetLineWidth(2)
          compHist.SetMarkerSize(0)
          compHist.SetMarkerStyle(0)
          compHist.SetFillColor(0)
          compHist.Sumw2()
          if subYields[ibs]['totalYield']>0:
            norm=subYields[0]['totalYield']/subYields[ibs]['totalYield']
          else:
            norm=1
          c.Draw(varstring+'>>'+str(histoname),str(norm)+'*weight*('+wholecut+')')
          if first:
            compHist.SetLineColor(col+2)
            first = False
          else:
            compHist.SetLineColor(colorList[ibs])
          compHists.append(compHist)
          print jReg, bs, norm
        
        l.AddEntry(histo)
        histo.GetYaxis().SetTitleOffset(0.7)
        histo.GetYaxis().SetTitle('Events')
        histo.Draw('hist')
        for hists in compHists:
          hists.Draw('hist same')
          hists.Draw('e1 same')
          l.AddEntry(hists)
        l.Draw()

        latex2 = ROOT.TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.035)
        latex2.SetTextAlign(11) # align right
        latex2.DrawLatex(0.16,0.96,"CMS simulation")
        latex2.DrawLatex(0.7,0.96,"L=4 fb^{-1} (13TeV)")
        
        
        subCan.cd()
        
        pad2 = ROOT.TPad('pad2','pad2',0,0,1.,.3)
        pad2.SetTopMargin(0)
        pad2.SetBottomMargin(0.3)
        pad2.SetLeftMargin(0.1)
        pad2.SetGrid()
        pad2.Draw()
        pad2.cd()
        
        ratio = compHists[0].Clone()
        ratio.Divide(compHists[1])
        ratio.SetMaximum(2)
        ratio.SetMinimum(0)
        ratio.SetMarkerStyle(9)
        ratio.SetMarkerSize(1)
        ratio.SetLineColor(ROOT.kBlack)
        ratio.GetYaxis().SetLabelSize(0.1)
        ratio.GetYaxis().SetTitleOffset(0.4)
        ratio.GetYaxis().SetTitleSize(0.1)
        ratio.GetYaxis().SetTitle('Ratio')
        ratio.GetYaxis().SetNdivisions(5)
        ratio.GetXaxis().SetLabelSize(0.1)
        ratio.GetXaxis().SetTitleSize(0.1)
        ratio.GetXaxis().SetTitleOffset(1.1)
        ratio.GetXaxis().SetTitle(varstring)
        
        ratio.Draw('e1p')
        
        subCan.Print(path+subname+cutname+'.png')
        subCan.Print(path+subname+cutname+'.root')        

        #write yields to list for pickle
        
               
      #Total stuff
      rcsCan.cd()
      totalYields = []
      for bs in nBtagReg:
        cutname,cut=nameAndCut(sReg, hReg, jReg, btb=bs, presel=prepresel)
        print cut
        c.Draw(varstring+'>>normHist','weight*('+cut+')','goff')
        totalYield=normHist.GetSumOfWeights()
        signalYield=normHist.GetBinContent(2)
        controlYield=normHist.GetBinContent(1)
        
        if controlYield>0:
          rcs=signalYield/controlYield
        else:
          rcs=0.
        
        if normHist.GetBinContent(1)>0 and normHist.GetBinContent(2)>0:
          rcsHist.SetBinError(ijReg+1, rcs*sqrt(normHist.GetBinError(2)**2/normHist.GetBinContent(2)**2 + normHist.GetBinError(1)**2/normHist.GetBinContent(1)**2))
        else:
          rcsHist.SetBinError(ijReg+1,0)
        rcsHist.GetXaxis().SetBinLabel(ijReg+1,str(jReg))
        if first:
          rcsHist.Draw('e')
          first = False
        else:
          rcsHist.Draw('e same')
        
        totalYields.append({'nbjets':bs,'totalYield':totalYield,'controlYield':controlYield,'signalYield':signalYield,'rcs':rcs})
        

      
      totalCan.cd()
      totalCan.SetGrid()
      h_Stack.SetMinimum(0.08)
      
      pad3 = ROOT.TPad('pad1','pad1',0,0.3,1.,1.)
      pad3.SetBottomMargin(0)
      pad3.SetLeftMargin(0.1)
      pad3.SetGrid()
      pad3.SetLogy()
      pad3.Draw()
      pad3.cd()
      
      compHists = []
      for ibs,bs in enumerate(nBtagReg):
        cutname,cut=nameAndCut(sReg, hReg, jReg, btb=bs, presel=prepresel)
        compHist = 'ch'+str(i)
        histoname = compHist
        binning = [16,0,3.2]
        compHist = ROOT.TH1F(str(histoname),str(bs) + ' b-tags',*binning)
        compHist.SetLineWidth(2)
        compHist.SetMarkerSize(0)
        compHist.SetMarkerStyle(0)
        compHist.SetFillColor(0)
        if totalYields[ibs]['totalYield']>0:
          norm=totalYields[0]['totalYield']/totalYields[ibs]['totalYield']
        else:
          norm=1
        print norm
        c.Draw(varstring+'>>'+str(histoname),str(norm)+'*weight*('+cut+')')
        compHist.SetLineColor(colorList[ibs])
        compHists.append(compHist)
      
      h_Stack.Draw('hist same')
      for hists in compHists:
        hists.Draw('hist same')
        hists.SetMinimum(0.08)
      

      latex1 = ROOT.TLatex()
      latex1.SetNDC()
      latex1.SetTextSize(0.035)
      latex1.SetTextAlign(11) # align right
      latex1.DrawLatex(0.16,0.96,"CMS simulation")
      latex1.DrawLatex(0.7,0.96,"L=4 fb^{-1} (13TeV)")
      
      totalL.Draw()
      
      totalCan.cd()
      
      pad4 = ROOT.TPad('pad2','pad2',0,0,1.,.3)
      pad4.SetTopMargin(0)
      pad4.SetBottomMargin(0.3)
      pad4.SetLeftMargin(0.1)
      pad4.SetGrid()
      pad4.Draw()
      pad4.cd()
      
      ratio = compHists[0].Clone()
      ratio.Divide(compHists[1])
      ratio.SetMaximum(2)
      ratio.SetMinimum(0)
      ratio.SetMarkerStyle(9)
      ratio.SetMarkerSize(1)
      ratio.SetLineColor(ROOT.kBlack)
      ratio.GetYaxis().SetLabelSize(0.1)
      ratio.GetYaxis().SetTitleOffset(0.4)
      ratio.GetYaxis().SetTitleSize(0.1)
      ratio.GetYaxis().SetTitle('Ratio')
      ratio.GetYaxis().SetNdivisions(5)
      ratio.GetXaxis().SetLabelSize(0.1)
      ratio.GetXaxis().SetTitleSize(0.1)
      ratio.GetXaxis().SetTitleOffset(1.1)
      ratio.GetXaxis().SetTitle(varstring)
      
      ratio.Draw('e1p')      

      totalCan.Print(path+cutname+'.png')
      totalCan.Print(path+cutname+'.root')
      
      #del h_Stack
    
    rcsCan.Print(path+'RCS.png')
    rcsCan.Print(path+'RCS.root')

#maybe delete all kinds of stuff

#
#
#
#      #calculate total RCS, draw all total histograms
#      can1 = ROOT.TCanvas(varstring,varstring,1200,1000)
#      mainNormHist=ROOT.TH1F('mainNormHist','MainNormHist',len(twoBin)-1, array('d', twoBin))
#      totalHist=ROOT.TH1F('totalHist','totalHist',*binning)
#      totalHist.Sumw2()
#      c.Draw(varstring+'>>mainNormHist','weight*('+cut+')','goff')
#      c.Draw(varstring+'>>mainNormHist','weight*('+cut+')')
#      for cbReg in nBtagReg:
#        if cbReg!=bReg:
#          compcut,compcutname=nameAndCut(sReg, hReg, jReg, btb=cbReg, presel=prepresel)
#          
#      
#      #now draw sub backgrounds
#      h_Stack = ROOT.THStack('h_Stack',varstring)
#
#
#      
#      h_Stack_S = ROOT.THStack('h_Stack_S',varstring)
#      
#      yields=[]
#      
#      l = ROOT.TLegend(0.7,0.7,0.95,0.95)
#      l.SetFillColor(ROOT.kWhite)
#      l.SetShadowColor(ROOT.kWhite)
#      l.SetBorderSize(1)
#      totalh=ROOT.TH1F('total','Total 1b',*binning)
#      totalh0b=ROOT.TH1F('total0b','Total 0b',*binning)
#      totalh.Sumw2()
#      totalh0b.Sumw2()
#      c.Draw(varstring+'>>total','weight*('+presel+'&&nBJetMediumCMVA30==1)')
#      c.Draw(varstring+'>>total0b','weight*('+presel+'&&nBJetMediumCMVA30==0)','goff')
#      ##First Bin Normalisation
#      #if totalh.GetBinContent(1)>0 and totalh0b.GetBinContent(1)>0:
#      #  totalNorm=totalh.GetBinContent(1)/totalh0b.GetBinContent(1)
#      #else:
#      #  totalNorm=1.
#      #First Bin Normalisation
#      if totalh.GetSumOfWeights()>0 and totalh0b.GetSumOfWeights()>0:
#        totalNorm=totalh.GetSumOfWeights()/totalh0b.GetSumOfWeights()
#      else:
#        totalNorm=1.
#      c.Draw(varstring+'>>total0b',str(totalNorm)+'*weight*('+presel+'&&nBJetMediumCMVA30==0)')
#      totalh.SetLineColor(ROOT.kBlue+3)
#      totalh.SetLineWidth(2)
#      totalh.SetMarkerSize(0)
#      totalh.SetMarkerStyle(0)
#      totalh.SetTitleSize(20)
#      totalh.SetFillColor(0)
#      totalh0b.SetLineColor(ROOT.kGreen+1)#kCyan+4
#      totalh0b.SetLineWidth(2)
#      totalh0b.SetMarkerSize(0)
#      totalh0b.SetMarkerStyle(0)
#      totalh0b.SetTitleSize(20)
#      totalh0b.SetFillColor(0)
#      l.AddEntry(totalh)
#      l.AddEntry(totalh0b)
#      for i, [cut,name,col,subname,texString] in enumerate(subBkgTT):
#        histo = 'h'+str(i)
#        histoname = histo
#        print histoname
#        histo = ROOT.TH1F(str(histo) ,str(histo),*binning)
#        print histo
#        print col
#        wholeCut=presel+'&&nBJetMediumCMVA30==1&&'+cut
#        print wholeCut
#        c.Draw(varstring+'>>'+str(histoname),'weight*('+wholeCut+')')
#        histo.SetLineColor(ROOT.kBlack)
#        histo.SetLineWidth(1)
#        histo.SetMarkerSize(0)
#        histo.SetMarkerStyle(0)
#        histo.SetTitleSize(20)
#        histo.GetXaxis().SetTitle(varstring)
#        histo.GetYaxis().SetTitle("Events / "+str( (binning[2] - binning[1])/binning[0]))
#        histo.GetXaxis().SetLabelSize(0.04)
#        histo.GetYaxis().SetLabelSize(0.04)
#        histo.GetYaxis().SetTitleOffset(0.8)
#        histo.GetYaxis().SetTitleSize(0.05)
#        histo.SetFillColor(col)
#        histo.SetFillStyle(1001)
#        histo.SetMinimum(.08)
#        h_Stack.Add(histo)
#        l.AddEntry(histo, name)
#        #RCS Backup calculation
#        twoBin=[0,1,pi]
#        rcsh=ROOT.TH1F('rcsh','rcsh',len(twoBin)-1, array('d', twoBin))
#        c.Draw(varstring+'>>rcsh','weight*('+wholeCut+')','goff')
#        rcsb=0
#        if rcsh.GetBinContent(1)>0 and rcsh.GetBinContent(2)>0:
#          rcsb=rcsh.GetBinContent(2)/rcsh.GetBinContent(1)
#        
#        can2=ROOT.TCanvas('sub','sub',800,600)
#        histo.Draw()
#        latex2 = ROOT.TLatex()
#        latex2.SetNDC()
#        latex2.SetTextSize(0.035)
#        latex2.SetTextAlign(11) # align right
#        latex2.DrawLatex(0.7,0.96,str(rcsb))
#        latex2.DrawLatex(0.16,0.96,name)
#        can2.SetGrid()
#        can2.SetLogy()
#        can2.Print(path+varstring+subname+'_'+prefix+'notauRej.png')
#        can2.Print(path+varstring+subname+'_'+prefix+'notauRej.root')
#        
#        canb = ROOT.TCanvas('canb','canb',800,600)
#        histo1b = ROOT.TH1F('histo1b' ,'histo1b',*binning)
#        histo0b = ROOT.TH1F('histo0b' ,'histo0b',*binning)
#        histo1b.Sumw2()
#        histo0b.Sumw2()
#        histo1b.SetLineColor(ROOT.kBlack)
#        histo1b.SetLineWidth(1)
#        histo1b.SetMarkerSize(0)
#        histo1b.SetMarkerStyle(0)
#        histo1b.SetTitleSize(20)
#        histo1b.GetXaxis().SetTitle(varstring)
#        histo1b.GetYaxis().SetTitle("Events / "+str( (binning[2] - binning[1])/binning[0]))
#        histo1b.GetXaxis().SetLabelSize(0.04)
#        histo1b.GetYaxis().SetLabelSize(0.04)
#        histo1b.GetYaxis().SetTitleOffset(0.8)
#        histo1b.GetYaxis().SetTitleSize(0.05)
#        histo1b.SetFillColor(col)
#        histo1b.SetFillStyle(1001)
#        histo1b.SetMinimum(.08)
#        histo0b.SetLineColor(ROOT.kCyan+4)
#        histo0b.SetLineWidth(2)
#        histo0b.SetMarkerSize(0)
#        histo0b.SetMarkerStyle(0)
#        histo0b.SetTitleSize(20)
#        histo0b.SetFillColor(0)
#        wholeCut1 = wholeCut=presel+'&&nBJetMediumCMVA30==1&&'+cut
#        #c.Draw(varstring+'>>histo1b','weight*('+wholeCut1+')')
#        wholeCut0 = wholeCut=presel+'&&nBJetMediumCMVA30==0&&'+cut
#        #c.Draw(varstring+'>>histo0b','weight*('+wholeCut0+')','goff')
#        norm=1
#        ##First Bin Normalisation
#        #if histo1b.GetBinContent(1)>0 and histo0b.GetBinContent(1)>0:
#        #  norm=histo1b.GetBinContent(1)/histo0b.GetBinContent(1)
#        ##Area Normalisation
#        #if histo1b.GetSumOfWeights()>0 and histo0b.GetSumOfWeights()>0:
#        #  norm=histo1b.GetSumOfWeights()/histo0b.GetSumOfWeights()
#        #
#        #c.Draw(varstring+'>>histo0b',str(norm)+'*weight*('+wholeCut0+')')
#        
#        ##Calculation of RCS value, works only for cut at dPhi=1 atm
#        #bins=1/(binning[2]/binning[0])
#        #i=1+int(bins)
#        #rcs0=0
#        #rcsz0=0
#        #rcsn0=0
#        #rcs1=0
#        #rcsz1=0
#        #rcsn1=0
#        #total0=histo0b.GetSumOfWeights()
#        #total1=histo1b.GetSumOfWeights()
#        #while i <= binning[0]:
#        #  rcsz0+=histo0b.GetBinContent(i)
#        #  rcsz1+=histo1b.GetBinContent(i)
#        #  i+=1
#        #i=1
#        #while i<= int(bins):
#        #  rcsn0+=histo0b.GetBinContent(i)
#        #  rcsn1+=histo1b.GetBinContent(i)
#        #  i+=1
#        #if rcsn0>0:
#        #  rcs0=rcsz0/rcsn0
#        #else:
#        #  rcs0=float('nan')
#  
#        #if rcsn1>0:
#        #  rcs1=rcsz1/rcsn1
#        #else:
#        #  rcs1=float('nan')
#        #rcsn0=rcsn0/norm
#        #rcsz0=rcsz0/norm
#
#        #RCS Backup calculation
#        twoBin=[0,deltaPhiCut,pi]
#        rcs0=ROOT.TH1F('rcs0','rcs0',len(twoBin)-1, array('d', twoBin))
#        rcs1=ROOT.TH1F('rcs1','rcs1',len(twoBin)-1, array('d', twoBin))
#        c.Draw(varstring+'>>rcs0','weight*('+wholeCut0+')','goff')
#        c.Draw(varstring+'>>rcs1','weight*('+wholeCut1+')','goff')
#        rcs0v=0
#        rcs1v=0
#        if rcs0.GetBinContent(1)>0:
#          rcs0v=rcs0.GetBinContent(2)/rcs0.GetBinContent(1)
#        else:
#          rcs0v=float('nan')
#        if rcs1.GetBinContent(1)>0:
#          rcs1v=rcs1.GetBinContent(2)/rcs1.GetBinContent(1)
#        else:
#          rcs1v=float('nan')
#        
#        if rcs1.GetSumOfWeights()>0 and rcs0.GetSumOfWeights()>0:
#          norm=rcs1.GetSumOfWeights()/rcs0.GetSumOfWeights()
#               
#        c.Draw(varstring+'>>histo1b','weight*('+wholeCut1+')')
#        c.Draw(varstring+'>>histo0b',str(norm)+'*weight*('+wholeCut0+')')        
#
#
#        histo1b.Draw('hist')
#        histo1b.Draw('e1same')
#        histo0b.Draw('hist same')
#        histo0b.Draw('e1same')
#        latex3 = ROOT.TLatex()
#        latex3.SetNDC()
#        latex3.SetTextSize(0.035)
#        latex3.SetTextAlign(11) # align right
#        #latex3.DrawLatex(0.45,0.91,'Y(0b,#Delta#Phi<1)='+str(round(rcsn0,2)))
#        #latex3.DrawLatex(0.45,0.86,'Y(0b,#Delta#Phi>1)='+str(round(rcsz0,2)))
#        #latex3.DrawLatex(0.45,0.81,'R(0b)='+str(round(rcs0,4)))
#        #latex3.DrawLatex(0.7,0.91,'Y(1b,#Delta#Phi<1)='+str(round(rcsn1,2)))
#        #latex3.DrawLatex(0.7,0.86,'Y(1b,#Delta#Phi>1)='+str(round(rcsz1,2)))
#        #latex3.DrawLatex(0.7,0.81,'R(1b)='+str(round(rcs1,4)))
#        #latex3.DrawLatex(0.45,0.76,'Norm 1b/0b='+str(round(norm,2)))
#        latex3.DrawLatex(0.16,0.96,name)
#        canb.SetLogy()
#        canb.SetGrid()
#        canb.Print(path+varstring+subname+'_'+prefix+'1bvs0b.png')
#        canb.Print(path+varstring+subname+'_'+prefix+'1bvs0b.root')
#        yields.append({'name':subname, 'title':texString, 'yield0bTotal':rcs0.GetSumOfWeights(),'yield1bTotal':rcs1.GetSumOfWeights(),'norm':norm,'rcs0b':rcs0v,'rcs1b':rcs1v,'yield0bC':rcs0.GetBinContent(1),'yield0bS':rcs0.GetBinContent(2),'yield1bC':rcs1.GetBinContent(1),'yield1bS':rcs1.GetBinContent(2)})
#      can1.cd()
#      can1.SetGrid()
#      h_Stack.Draw()
#      totalh.Draw('same')
#      totalh.Draw('hist same')
#      totalh0b.Draw('same')
#      totalh0b.Draw('hist same')
#      h_Stack.SetMinimum(0.08)
#      l.Draw()
#      
#      #RCS Backup calculation
#      twoBin=[0,deltaPhiCut,pi]
#      rcs0=ROOT.TH1F('rcs0','rcs0',len(twoBin)-1, array('d', twoBin))
#      rcs1=ROOT.TH1F('rcs1','rcs1',len(twoBin)-1, array('d', twoBin))
#      rcs0.Sumw2()
#      rcs1.Sumw2()
#      c.Draw(varstring+'>>rcs0','weight*('+presel+'&&nBJetMediumCMVA30==0)','goff')
#      c.Draw(varstring+'>>rcs1','weight*('+presel+'&&nBJetMediumCMVA30==1)','goff')
#      rcs0v=0
#      rcs1v=0
#      if rcs0.GetBinContent(1)>0:
#        rcs0v=rcs0.GetBinContent(2)/rcs0.GetBinContent(1)
#      else:
#        rcs0v=float('nan')
#      if rcs1.GetBinContent(1)>0:
#        rcs1v=rcs1.GetBinContent(2)/rcs1.GetBinContent(1)
#      else:
#        rcs1v=float('nan')
#      rcsHist0b.SetBinContent(ijReg+1,rcs0v)
#      
#      if rcs0.GetBinContent(1)>0 and rcs0.GetBinContent(2)>0:
#        rcsHist0b.SetBinError(ijReg+1, rcs0v*sqrt(rcs0.GetBinError(2)**2/rcs0.GetBinContent(2)**2 + rcs0.GetBinError(1)**2/rcs0.GetBinContent(1)**2))
#      else:
#        rcsHist0b.SetBinError(ijReg+1,0)
#      rcsHist1b.SetBinContent(ijReg+1,rcs1v)
#      if rcs1.GetBinContent(1)>0 and rcs1.GetBinContent(2)>0:
#        rcsHist1b.SetBinError(ijReg+1, rcs1v*sqrt(rcs1.GetBinError(2)**2/rcs1.GetBinContent(2)**2 + rcs1.GetBinError(1)**2/rcs1.GetBinContent(1)**2))
#      else:
#        rcsHist1b.SetBinError(ijReg+1,0)
#      rcsHist0b.GetXaxis().SetBinLabel(ijReg+1,str(jReg))
#      ##Calculation of RCS value, works only for cut at dPhi=1 atm
#      #bins=1/(binning[2]/binning[0])
#      #i=1+int(bins)
#      #rcsz1=0
#      #rcsn1=0
#      #rcsz0=0
#      #rcsn0=0
#      #total1=h_Stack.GetStack().Last().GetSumOfWeights()
#      #total0=totalh0b.GetSumOfWeights()
#      #while i <= binning[0]:
#      #  rcsz1+=h_Stack.GetStack().Last().GetBinContent(i)
#      #  rcsz0+=totalh0b.GetBinContent(i)
#      #  i=i+1
#      #i=1
#      #while i<= int(bins):
#      #  rcsn1+=h_Stack.GetStack().Last().GetBinContent(i)
#      #  rcsn0+=totalh0b.GetBinContent(i)
#      #  i=i+1
#      #if rcsn1>0:
#      #  rcs1=rcsz1/rcsn1
#      #else:
#      #  rcs1=float('nan')
#      #print rcs1
#      #if rcsn0>0:
#      #  rcs0=rcsz0/rcsn0
#      #else:
#      #  rcs0=float('nan')
#      #print rcs0
#      latex1 = ROOT.TLatex()
#      latex1.SetNDC()
#      latex1.SetTextSize(0.035)
#      latex1.SetTextAlign(11) # align right
#      latex1.DrawLatex(0.16,0.96,"CMS simulation")
#      latex1.DrawLatex(0.7,0.96,"L=4 fb^{-1} (13TeV)")
#      
#      #rcsz0=rcsz0/totalNorm
#      #rcsn0=rcsn0/totalNorm
#      yields.append({'name':'total', 'title':'total', 'yield0bTotal':rcs0.GetSumOfWeights(),'yield1bTotal':rcs1.GetSumOfWeights(),'norm':totalNorm,'rcs0b':rcs0v,'rcs1b':rcs1v,'yield0bC':rcs0.GetBinContent(1),'yield0bS':rcs0.GetBinContent(2),'yield1bC':rcs1.GetBinContent(1),'yield1bS':rcs1.GetBinContent(2)})
#      #latexN = ROOT.TLatex()
#      #latexN.SetNDC()
#      #latexN.SetTextSize(0.025)
#      #latexN.SetTextAlign(11) # align right
#      #latexN.DrawLatex(0.5,0.91,"Y(0b,#Delta#Phi <1)="+str(round(rcsn0,2)))
#      #latexN.DrawLatex(0.5,0.87,"Y(0b,#Delta#Phi >1)="+str(round(rcsz0,2)))
#      #latexN.DrawLatex(0.5,0.83,"R_{CS}(0b)="+str(round(rcs0,4)))
#      #latexN.DrawLatex(0.5,0.79,"Y(1b,#Delta#Phi <1)="+str(round(rcsn1,2)))
#      #latexN.DrawLatex(0.5,0.75,"Y(1b,#Delta#Phi >1)="+str(round(rcsz1,2)))
#      #latexN.DrawLatex(0.5,0.71,"R_{CS}(1b)="+str(round(rcs1,4)))
#      #latexN.DrawLatex(0.5,0.67,"Norm 1b/0b ="+str(round(totalNorm,2)))
#      can1.SetLogy()
#      can1.Print(path+varstring+'_'+prefix+'notauRej.png')
#      can1.Print(path+varstring+'_'+prefix+'notauRej.root')
#      yieldFile=open(path+"yields.pkl","w")
#      pickle.dump(yields,yieldFile)
#      yieldFile.close()
#    ROOT.gStyle.SetErrorX(0.5)
#    canR=ROOT.TCanvas('RCS','RCS',800,600)
#    rcsHist1b.SetMarkerSize(0)
#    rcsHist0b.SetMarkerSize(0)
#    rcsHist1b.SetLineColor(ROOT.kGreen+2)
#    rcsHist0b.SetLineColor(ROOT.kBlue+1)
#    rcsHist0b.SetLineWidth(1)
#    rcsHist1b.SetLineWidth(1)
#    rcsHist0b.SetMinimum(0.)
#    rcsHist0b.SetMaximum(0.15)
#    rcsHist0b.GetXaxis().SetTitle("n_jets")
#    rcsHist0b.GetYaxis().SetTitle("Rcs")
#    rcsHist0b.GetXaxis().SetLabelSize(0.07)
#    rcsHist0b.GetYaxis().SetLabelSize(0.04)
#    rcsHist0b.GetYaxis().SetTitleOffset(0.9)
#    rcsHist0b.GetYaxis().SetTitleSize(0.05)
#    rcsHist0b.Draw('e')
#    rcsHist1b.Draw('e same')
#    canR.Print(path+varstring+'_RCS.png')
