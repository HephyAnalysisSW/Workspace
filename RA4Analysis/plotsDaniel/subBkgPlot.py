import ROOT
import os, sys, copy

import pickle

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
from array import array

from Workspace.HEPHYPythonTools.helpers import getVarValue, getChain, deltaPhi
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v1_Phys14V3_HT400ST200 import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400ST150_withDF import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2 import *
from Workspace.RA4Analysis.helpers import *

#ROOT.TH1F().SetDefaultSumw2()

#bVar = 'nBJetMediumCSV30'
bVar = 'nBJetMediumCMVA30'

deltaPhiCut=1.
varstring='deltaPhi_Wl'
vartex = '#Delta#Phi(W,l)'
binning=[16,0,3.2]
twoBin=[0,deltaPhiCut,3.2]
lepSel = 'hard'

nBtagReg=[(0,0),(1,1)]#,(2,-1)]
nJetReg=[(2,3),(4,5),(6,7),(8,-1)]#,(5,5),(6,-1)]#,(6,7),(8,-1)]#,(6,-1)]#,(3,3),(4,4),(5,5),(6,-1)]
stReg=[(350,-1)]#,(300,-1)]#,(350,450),(450,-1)]#,(250,-1)]#,(350,450),(450,-1)]
htReg=[(500,-1)]#,(1000,-1)]#,(1000,1250),(1250,-1)]#,(750,-1)]#,(750,1000),(1000,1250),(1250,-1)]

colorList=[ROOT.kBlack, ROOT.kMagenta+2, ROOT.kOrange+2,ROOT.kMagenta+2]

startpath = '/afs/hephy.at/user/d/dspitzbart/www/subBkgTThard/'


#Load the Background Chain
c = getChain(ttJets[lepSel],histname='')
#c = getChain(WJetsHTToLNu[lepSel],histname='')

#Sub Background Definitions #sometimes the variable is called genPart, sometimes GenPart, be aware of that
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

#mainHist = ROOT.TH1F('mainHist' ,'mainHist',*binning)
compHist = ROOT.TH1F('compHist','compHist',*binning)
normHist=ROOT.TH1F('normHist','normHist',len(twoBin)-1, array('d', twoBin))

rcsHist=ROOT.TH1F('rcsHist','rcsHist',len(nJetReg),0,len(nJetReg))

#mainHist.Sumw2()
compHist.Sumw2()
normHist.Sumw2()

#mainHist.SetLineColor(ROOT.kBlack)
#mainHist.SetLineWidth(1)
#mainHist.SetMarkerSize(0)
#mainHist.SetMarkerStyle(0)
#mainHist.SetTitleSize(20)
#mainHist.GetXaxis().SetTitle(varstring)
#mainHist.GetYaxis().SetTitle("Events")
#mainHist.GetXaxis().SetLabelSize(0.04)
#mainHist.GetYaxis().SetLabelSize(0.04)
#mainHist.GetYaxis().SetTitleOffset(0.8)
#mainHist.GetYaxis().SetTitleSize(0.05)
#mainHist.SetFillStyle(1001)
#mainHist.SetMinimum(.08)

compHist.SetLineWidth(2)
compHist.SetMarkerSize(0)
compHist.SetMarkerStyle(0)
compHist.SetFillColor(0)

rcsHist.SetMarkerStyle(2)
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

allYields = []


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
        njPath=str(jReg[0])+'nJet30'+str(jReg[1])+'/'
      else:
        njCutString='&&nJet30>='+str(jReg[0])
        njPath='nJet30LEq'+str(jReg[0])+'/'
      path=startpath+htPath+stPath+njPath

      if not os.path.exists(path):
        os.makedirs(path)
      print 'Processing nJets ' + str(jReg)
      print ' '
      
      h_Stack = ROOT.THStack('h_Stack',varstring)
      
      totalL = ROOT.TLegend(0.6,0.6,0.95,0.93)
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
        histo = ROOT.TH1F(str(histo) ,name,*binning)
        for bs in nBtagReg:
          #normHist.Reset()
          cutname,cut=nameAndCut(sReg, hReg, jReg, btb=bs, presel=prepresel, btagVar = bVar)
          wholecut = cut + '&&' + subcut
          #print wholecut
          c.Draw(varstring+'>>normHist','weight*('+wholecut+')','goff')
          totalYield=normHist.GetSumOfWeights()
          signalYield=normHist.GetBinContent(2)
          controlYield=normHist.GetBinContent(1)
          if controlYield>0:
            rcs=signalYield/controlYield
          else:
            rcs=0.
          if normHist.GetBinContent(1)>0 and normHist.GetBinContent(2)>0:
            rcsError = rcs*sqrt(normHist.GetBinError(2)**2/normHist.GetBinContent(2)**2 + normHist.GetBinError(1)**2/normHist.GetBinContent(1)**2)
            #rcsHist.SetBinError(ijReg+1, rcs*sqrt(normHist.GetBinError(2)**2/normHist.GetBinContent(2)**2 + normHist.GetBinError(1)**2/normHist.GetBinContent(1)**2))
          else:
            rcsError = 0.
            #rcsHist.SetBinError(ijReg+1,0)
          print jReg, bs, rcs, totalYield
          allYields.append({'name':subname, 'nbjets':bs,'st':sReg, 'ht':hReg, 'njets':jReg, 'totalYield':totalYield,'controlYield':controlYield,'signalYield':signalYield,'rcs':rcs, 'rcsError':rcsError, 'title':texString})
          subYields.append({'nbjets':bs,'totalYield':totalYield,'controlYield':controlYield,'signalYield':signalYield,'rcs':rcs})

        #make sub plots
        subCan.cd()
        
        pad1 = ROOT.TPad('pad1','pad1',0,0.3,1.,1.)
        pad1.SetBottomMargin(0)
        pad1.SetTopMargin(0.07)
        pad1.SetLeftMargin(0.12)
        pad1.SetGrid()
        pad1.SetLogy()
        pad1.Draw()
        pad1.cd()
        
        l = ROOT.TLegend(0.5,0.75,0.95,0.93)
        l.SetFillColor(ROOT.kWhite)
        l.SetShadowColor(ROOT.kWhite)
        l.SetBorderSize(1)

        cutname,cut=nameAndCut(sReg, hReg, jReg, btb=nBtagReg[0], presel=prepresel, btagVar = bVar)
        wholecut = cut + '&&' + subcut
        c.Draw(varstring+'>>'+str(histoname),'weight*('+wholecut+')')
        histo.SetFillColor(col)
        histo.SetLineColor(ROOT.kBlack)#was col+2
        histo.SetMarkerSize(0)
        histo.SetLineWidth(1)
        h_Stack.Add(histo)
        totalL.AddEntry(histo)
        compHists = []
        first = True
        
        for ibs,bs in enumerate(nBtagReg):
          namecut,cut=nameAndCut(sReg, hReg, jReg, btb=bs, presel=prepresel, btagVar = bVar)
          wholecut=cut+'&&'+subcut
          compHist = 'ch'+str(i)
          histoname = compHist
          compHist = ROOT.TH1F(str(histoname),str(bs) + ' b-tags',*binning)
          compHist.SetLineWidth(2)
          compHist.SetMarkerSize(0)
          compHist.SetMarkerStyle(0)
          compHist.SetFillColor(0)
          compHist.SetMinimum(0.08)
          compHist.SetLineWidth(3)
          compHist.Sumw2()
          if subYields[ibs]['totalYield']>0:
            norm=subYields[0]['totalYield']/subYields[ibs]['totalYield']
          else:
            norm=1
          c.Draw(varstring+'>>'+str(histoname),str(norm)+'*weight*('+wholecut+')')
          if first:
            compHist.SetLineColor(ROOT.kBlack)#was col+2
            first = False
          else:
            compHist.SetLineColor(colorList[ibs])
          compHists.append(compHist)
          print jReg, bs, norm
        
        l.AddEntry(histo)
        histo.GetYaxis().SetTitleOffset(1.)
        histo.GetYaxis().SetTitle('Events')
        histo.SetTitleSize(0.15)
        histo.GetYaxis().SetLabelSize(0.07)
        histo.SetMinimum(0.05)
        histo.Draw('hist')
        ks = []
        for hists in compHists:
          hists.Draw('hist same')
          hists.Draw('e1 same')
          l.AddEntry(hists)
          ks.append(compHists[0].KolmogorovTest(hists))
        l.Draw()
        
        ks.reverse()        
        for ik,k in enumerate(ks):
          allYields[-(ik+1)].update({'KS-Test': k})
        
        latex1 = ROOT.TLatex()
        latex1.SetNDC()
        latex1.SetTextSize(0.055)
        latex1.SetTextAlign(11) # align right
        latex1.DrawLatex(0.12,0.94,"CMS simulation")
        latex1.DrawLatex(0.7,0.94,"L=4 fb^{-1} (13TeV)")
        
        
        subCan.cd()
        
        pad2 = ROOT.TPad('pad2','pad2',0,0,1.,.3)
        pad2.SetTopMargin(0.)
        pad2.SetBottomMargin(0.3)
        pad2.SetLeftMargin(0.12)
        pad2.SetGrid()
        pad2.Draw()
        pad2.cd()
        
        ratio = compHists[0].Clone()
        ratio.Divide(compHists[1])
        ratio.SetMaximum(1.9)
        ratio.SetMinimum(0.1)
        ratio.SetMarkerStyle(9)
        ratio.SetMarkerSize(1)
        ratio.SetLineColor(ROOT.kBlack)
        ratio.GetYaxis().SetLabelSize(0.15)
        ratio.GetYaxis().SetTitleOffset(0.35)
        ratio.GetYaxis().SetTitleSize(0.15)
        ratio.GetYaxis().SetTitle('Ratio 0b/1b')
        ratio.GetYaxis().SetNdivisions(5)
        ratio.GetXaxis().SetLabelSize(0.15)
        ratio.GetXaxis().SetTitleSize(0.15)
        ratio.GetXaxis().SetTitleOffset(1.05)
        ratio.GetXaxis().SetTitle(vartex)
        
        ratio.Draw('e1p')
        
        subCan.Print(path+subname+cutname+'.pdf')
        subCan.Print(path+subname+cutname+'.png')
        subCan.Print(path+subname+cutname+'.root')        

        
               
      #RCS stuff
      rcsCan.cd()
      totalYields = []
      for bs in nBtagReg:
        cutname,cut=nameAndCut(sReg, hReg, jReg, btb=bs, presel=prepresel, btagVar = bVar)
        #print cut
        c.Draw(varstring+'>>normHist','weight*('+cut+')','goff')
        totalYield=normHist.GetSumOfWeights()
        signalYield=normHist.GetBinContent(2)
        controlYield=normHist.GetBinContent(1)
        
        if controlYield>0:
          rcs=signalYield/controlYield
        else:
          rcs=0.
        rcsHist.SetBinContent(ijReg+1,rcs)
        if normHist.GetBinContent(1)>0 and normHist.GetBinContent(2)>0:
          rcsError = rcs*sqrt(normHist.GetBinError(2)**2/normHist.GetBinContent(2)**2 + normHist.GetBinError(1)**2/normHist.GetBinContent(1)**2)
          rcsHist.SetBinError(ijReg+1, rcs*sqrt(normHist.GetBinError(2)**2/normHist.GetBinContent(2)**2 + normHist.GetBinError(1)**2/normHist.GetBinContent(1)**2))
        else:
          rcsError = 0.
          rcsHist.SetBinError(ijReg+1,0)
        rcsHist.GetXaxis().SetBinLabel(ijReg+1,str(jReg))
        if first:
          rcsHist.Draw('e')
          first = False
        else:
          rcsHist.Draw('e same')
        
        allYields.append({'name':'total', 'nbjets':bs,'st':sReg, 'ht':hReg, 'njets':jReg, 'totalYield':totalYield,'controlYield':controlYield,'signalYield':signalYield,'rcs':rcs, 'rcsError':rcsError, 'title':'total'})
        totalYields.append({'nbjets':bs,'totalYield':totalYield,'controlYield':controlYield,'signalYield':signalYield,'rcs':rcs})
        

      #Total plot
      totalCan.cd()
      totalCan.SetGrid()
      h_Stack.SetMinimum(0.08)
      pad3 = ROOT.TPad('pad1','pad1',0,0.3,1.,1.)
      pad3.SetBottomMargin(0)
      pad3.SetLeftMargin(0.12)
      pad3.SetTopMargin(0.07)
      pad3.SetGrid()
      pad3.SetLogy()
      pad3.Draw()
      pad3.cd()
      
      compHists = []
      for ibs,bs in enumerate(nBtagReg):
        cutname,cut=nameAndCut(sReg, hReg, jReg, btb=bs, presel=prepresel, btagVar = bVar)
        compHist = 'ch'+str(i)
        histoname = compHist
        binning = [16,0,3.2]
        compHist = ROOT.TH1F(str(histoname),str(bs) + ' b-tags',*binning)
        compHist.SetLineWidth(2)
        compHist.SetMarkerSize(0)
        compHist.SetMinimum(0.08)
        compHist.SetMarkerStyle(0)
        compHist.SetFillColor(0)
        compHist.SetLineWidth(3)
        compHist.Sumw2()
        if totalYields[ibs]['totalYield']>0:
          norm=totalYields[0]['totalYield']/totalYields[ibs]['totalYield']
        else:
          norm=1
        print norm
        c.Draw(varstring+'>>'+str(histoname),str(norm)+'*weight*('+cut+')')
        compHist.SetLineColor(colorList[ibs])
        compHists.append(compHist)
      ks = []
      h_Stack.Draw('hist')
      for hists in compHists:
        hists.Draw('hist same')
        hists.Draw('e1 same')
        hists.SetMinimum(0.08)
        totalL.AddEntry(hists)
        ks.append(compHists[0].KolmogorovTest(hists))
      
      ks.reverse()
      for ik,k in enumerate(ks):
          allYields[-(ik+1)].update({'KS-Test': k})

      h_Stack.GetYaxis().SetTitle("Events  ")
      h_Stack.GetYaxis().SetTitleSize(0.07)
      h_Stack.GetYaxis().SetTitleOffset(.8)
      h_Stack.GetYaxis().SetLabelSize(0.06)

      latex1.DrawLatex(0.12,0.94,"CMS simulation")
      latex1.DrawLatex(0.7,0.94,"L=4 fb^{-1} (13TeV)")
      
      totalL.Draw()
      
      totalCan.cd()
      
      pad4 = ROOT.TPad('pad2','pad2',0,0,1.,.3)
      pad4.SetTopMargin(0)
      pad4.SetBottomMargin(0.3)
      pad4.SetLeftMargin(0.12)
      pad4.SetGrid()
      pad4.Draw()
      pad4.cd()
      
      ratio = compHists[0].Clone()
      ratio.Divide(compHists[1])
      ratio.SetMaximum(1.9)
      ratio.SetMinimum(0.1)
      ratio.SetMarkerStyle(9)
      ratio.SetMarkerSize(1)
      ratio.SetLineColor(ROOT.kBlack)
      ratio.GetYaxis().SetLabelSize(0.15)
      ratio.GetYaxis().SetTitleOffset(0.4)
      ratio.GetYaxis().SetTitleSize(0.15)
      ratio.GetYaxis().SetTitle('Ratio 0b/1b')
      ratio.GetYaxis().SetNdivisions(5)
      ratio.GetXaxis().SetLabelSize(0.15)
      ratio.GetXaxis().SetTitleSize(0.15)
      ratio.GetXaxis().SetTitleOffset(1.05)
      ratio.GetXaxis().SetTitle(vartex)
      
      ratio.Draw('e1p')      
      totalCan.Print(path+cutname+'.pdf')
      totalCan.Print(path+cutname+'.png')
      totalCan.Print(path+cutname+'.root')
      
      #del h_Stack
    yieldFile = open(path+'yields.pkl','w')   
    rcsCan.Print(path+'RCS.png')
    rcsCan.Print(path+'RCS.root')
    pickle.dump(allYields,yieldFile)
    yieldFile.close()
    allYields = []

#maybe delete all kinds of stuff

