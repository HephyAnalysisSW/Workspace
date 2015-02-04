import ROOT
from Workspace.RA4Analysis.stage2Tuples import ttJetsCSA1450ns
from Workspace.HEPHYPythonTools.helpers import findClosestObject, deltaR,getVarValue, getObjFromFile
from Workspace.RA4Analysis.objectSelection import getGoodJetsStage2
#from Workspace.RA4Analysis.makeCompPlotDilep import DrawClosure
from Workspace.RA4Analysis.makeNicePlot import DrawNicePlot
from math import *
from array import array
import os, sys
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v3 import *
from Workspace.HEPHYPythonTools.helpers import getChain

ROOT.gROOT.LoadMacro("../../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
ROOT.TH1F.SetDefaultSumw2()
#topMargin = 0.07

def DrawClosure(plot1,plot2,plot3,plot4,xaxis,path):

  #ROOT.setTDRStyle()
  can = ROOT.TCanvas("c",xaxis,600,600)
  can.cd()
  latex1 = ROOT.TLatex()
  latex1.SetNDC()
  latex1.SetTextSize(0.035)
  latex1.SetTextAlign(11) # align right
  latex2 = ROOT.TLatex()
  latex2.SetNDC()
  latex2.SetTextSize(0.035)
  latex2.SetTextAlign(11) # align left
  latex2.DrawLatex(0.16,0.9,"CMS Simulation")
  latex1.DrawLatex(0.7,0.9,"L=4 fb^{-1} (13 TeV)")
  Pad1 = ROOT.TPad("Pad1", "Pad1", 0, 0.35, 1, 0.9)
  Pad1.SetLogy()
  Pad1.SetTopMargin(0.02)
  Pad1.SetBottomMargin(0)
  Pad1.SetLeftMargin(0.16)
  Pad1.SetRightMargin(0.05)
  #Pad1.SetTickY(1)
  #Pad1.SetGridx()
  Pad1.Draw()
  Pad1.cd()
  #text = ROOT.TLatex()
  #text.DrawLatex(0.15,0.93, plot1name+" #sqrt{s} = 13 TeV")
  plot3.SetTitle("")
  plot3.SetAxisRange(0.0101,(plot1.GetMaximum())*(plot1.GetMaximum())*100,"Y")
  plot3.SetStats(0)
  plot3.SetLineColor(ROOT.kAzure)
  plot3.SetMarkerColor(ROOT.kAzure)
  plot3.SetLineWidth(3)
  plot3.GetXaxis().SetLabelSize(0.)
  plot3.Draw()
  plot4.SetStats(0)
  plot4.SetLineColor(ROOT.kAzure)
  plot4.SetMarkerColor(ROOT.kAzure)
  plot4.SetLineWidth(3)
  plot4.Draw('same')
  #plot1.SetTitleSize(5)
  plot1.SetStats(0)
  plot1.SetLineColor(ROOT.kBlack)
  plot1.SetMarkerColor(ROOT.kBlack)
  plot1.SetLineWidth(3)
  plot1.Draw('same')
  plot2.SetStats(0)
  plot2.SetLineColor(ROOT.kRed+1)
  plot2.SetMarkerColor(ROOT.kRed+1)
  plot2.SetLineWidth(3)
  plot2.Draw('same')
  #plot4.GetYaxis().SetLabelSize(0.)
  #plot3.GetYaxis().SetTitle("Number of Events / 50 GeV")
  plot3.GetYaxis().SetTitle("Number of Events / Bin ")
  plot3.GetYaxis().SetTitleSize(0.08)
  #plot1.GetYaxis().SetTitleFont(43)
  plot3.GetYaxis().SetTitleOffset(0.7)
  #plot3.GetYaxis().SetLabelFont(43)
  plot3.GetYaxis().SetLabelSize(0.08)
  leg = ROOT.TLegend(0.2,0.6,0.9,0.9)
  leg.AddEntry(plot2, "Prediction from MC","l")
  leg.AddEntry(plot1, "Hadronic Tau Expectation from MC","l")
  leg.AddEntry(plot3, "#pm 10% Efficiency","l")
  #leg.AddEntry(plot4, "0.9*(Eff) Pred","l")
  leg.SetTextSize(0.06)
  leg.SetFillColor(0)
  leg.SetShadowColor( ROOT.kWhite )
  leg.SetBorderSize( 0 )
  leg.SetBorderSize( 1 )
  leg.Draw()
  can.cd()
  Pad2 = ROOT.TPad("Pad2", "Pad2",  0, 0.05, 1, 0.35)
  Pad2.SetTopMargin(0)
  Pad2.SetBottomMargin(0.4)
  Pad2.SetLeftMargin(0.16)
  Pad2.SetRightMargin(0.05)
  #Pad2.SetTickX(1)
  #Pad2.SetTickY(1)
  #Pad2.SetGridx()
  Pad2.Draw()
  Pad2.cd()
  #ROOT.setTDRStyle()
  #ROOT.setTDRStyle()
  Func = ROOT.TF1('Func',"[0]",plot1.GetXaxis().GetXmin(),plot1.GetXaxis().GetXmax())
  Func.SetParameter(0,1)
  Func.SetLineColor(2)
  h_ratio = plot2.Clone("h_ratio")
  h_ratio.SetLineColor(ROOT.kBlack)
  h_ratio.SetLineWidth(2)
  h_ratio.SetMinimum(0.0)
  h_ratio.SetMaximum(1.99)
  h_ratio.Sumw2()
  h_ratio.SetStats(0)
  h_ratio.Divide(plot1)
  h_ratio.SetMarkerStyle(21)
  h_ratio.SetMarkerColor(ROOT.kBlack)
  #h_ratio.SetMarkerSize(0.5)
  #h_ratio.SetTitle(";;Truth/Pred;")
  h_ratio.SetTitle("")
  h_ratio.GetYaxis().SetTitle("Pred/Sim ")
  h_ratio.GetYaxis().SetNdivisions(505)
  h_ratio.GetYaxis().SetTitleSize(0.15)   #0.12
  h_ratio.GetYaxis().SetTitleFont(42)
  h_ratio.GetYaxis().SetTitleOffset(0.38)
  #h_ratio.GetYaxis().SetLabelFont(43)
  h_ratio.GetYaxis().SetLabelSize(0.15)
  print xaxis
  #h_ratio.GetXaxis().SetTitle(xaxis+"(GeV)")
  #h_ratio.GetXaxis().SetNdivisions(505)
  h_ratio.GetXaxis().SetTitle(xaxis)
  h_ratio.GetXaxis().SetTitleSize(0.2) #0.12
  h_ratio.GetXaxis().SetTitleFont(42)
  h_ratio.GetXaxis().SetTitleOffset(0.8)  # 0.9
  #h_ratio.GetXaxis().SetLabelFont(43)
  h_ratio.GetXaxis().SetLabelSize(0.17)
  h_ratio.Draw("ep")
  Func.Draw("same")
  #can.SetGridx()
  #Pad2.Update()
  #can.Update()
  #can.Draw()
  can.SaveAs(path)


c = ROOT.TChain('Events')
#c.Add('/data/schoef/convertedTuples_v26/copyInc/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*.root')
#c = getChain(hard_ttJetsCSA1450ns)
#c.Add('/data/schoef/cmgTuples/postProcessed_v5_Phys14V2/hard/TTJets/*.root')
c.Add('/data/schoef/cmgTuples/postProcessed_v5_Phys14V2//inc/hard/TTJets/*.root')
print c
cPred = ROOT.TChain('Events')
#cPred.Add('/data/easilar/results2014/tauTuples/CSA14_TTJets_hadGenTau_Nov24.root')
#cPred.Add('/data/easilar/results2014/tauTuples/CSA14_TTJets_hadGenTau_Nov24_NewTemp.root')
#cPred.Add('/data/easilar/results2014/tauTuples/CSA14_TTJets_hadTauEstimate_cmg_large_reduced_lepother.root')
#cPred.Add('/data/easilar/results2014/tauTuples/CSA14_TTJets_hadTauEstimate_cmg_large_reduced_lepother_PHYS14.root')
cPred.Add('/data/easilar/results2014/tauTuples/CSA14_TTJets_hadTauEstimate_cmg_large_PHYS14_inc.root')
#oneHadTau     ="ngoodMuons==1&&nvetoMuons==1&&nvetoElectrons==0&&Sum$(gTauPt>15&&abs(gTauEta)<2.1&&gTauNENu+gTauNMuNu==0&&gTauNTauNu==1)==1"
#oneHadTau     ="Sum$(abs(LepGood_pdgId)==13)==1&&Sum$(abs(LepGood_pdgId==13)&&LepGood_tightId==1)==1&&Sum$(abs(LepGood_pdgId)==11)==0&&Sum$(genTau_pt>15&&abs(genTau_eta)<2.1&&(genTau_nMuNu+genTau_nMuE==0)&&genTau_nMuTau==1"
oneHadTau     = "genTau_nNuE+genTau_nNuMu==0&&genTau_nNuTau==1\
        &&Sum$(abs(LepGood_pdgId)==13 && LepGood_tightId==1 && abs(LepGood_eta)<2.1 && LepGood_relIso03 < 0.12)==1" #&&Sum$(abs(LepGood_pdgId)==11)==0" #\
#&&Sum$(abs(LepGood_pdgId)==13 && abs(LepGood_eta)<2.4 && LepGood_relIso03 < 0.3)==1 \
#&&Sum$(abs(LepGood_pdgId)==11)==0"
# &&Sum$(abs(LepGood_pdgId)==11)==0"  #nLooseHardLeptons==1&&nTightHardLeptons==1)\
#oneHadTauOpen ="ngoodMuons==1&&nvetoMuons==1&&nvetoElectrons==0&&Sum$(gTauNENu+gTauNMuNu==0&&gTauNTauNu==1)==1"
#oneHadTau     ="ngNuMuFromW==1&&ngoodMuons==1&&nvetoMuons==1&&nvetoElectrons==0&&Sum$(gTauPt>15&&abs(gTauEta)<2.5&&gTauNENu+gTauNMuNu==0&&gTauNTauNu==1)==1"
#oneHadTauOpen ="ngNuMuFromW==1&&ngoodMuons==1&&nvetoMuons==1&&nvetoElectrons==0&&Sum$(gTauNENu+gTauNMuNu==0&&gTauNTauNu==1)==1"

##Fakerate calculation##
#ptBins  = array('d', [float(x) for x in range(10, 20)+range(20,50,3)+range(50,100,10)+range(100,310,30)])
#leptonID = 'gTauPt>15&&abs(gTauEta)<2.1&&(gTauNENu+gTauNMuNu)==0&&gTauNTauNu==1'
#
#fakeRatePre = ROOT.TProfile('fakeRatePre','fakeRatePre', len(ptBins)-1,ptBins,-2,2)
#c.Draw('gTauJetInd>=0:gTauPt>>fakeRatePre',oneHadTau, 'goff')
#fakeRate = ROOT.TProfile('fakeRate','fakeRate', len(ptBins)-1,ptBins,-2,2)
#c.Draw('gTauJetDR<0.4&&jetBTag[gTauJetInd]>0.679&&abs(jetEta[gTauJetInd])<2.4:gTauPt>>fakeRate',oneHadTau, 'goff')
#fakeRate=fakeRate.ProjectionX()
#fakeRate.Multiply(fakeRatePre.ProjectionX())
#path = '/afs/hephy.at/user/e/easilar/www/hadronicTau/'
#DrawNicePlot(fakeRate,'tau fake Rate','fake Rate','gen Tau Pt',path,'FakeRate.png')
####


#scaleF = (1-0.1741-0.1783)*0.1125/(0.1057+0.1095)
scaleF = (1-0.1741-0.1783)*0.1125/(0.1057)
#scaleF = 0.6476 #plus or minus 0.0024

hist_Title = "\#CMS \, Simulation \, L = 1 fb^{-1}, #sqrt{s} = 13 TeV"
mT = 'sqrt(2*LepGood_pt*met_pt*(1-cos(met_phi-LepGood_phi)))'


wX = 'met_pt*cos(met_phi)+LepGood_pt*cos(LepGood_phi)'
wY = 'met_pt*sin(met_phi)+LepGood_pt*sin(LepGood_phi)'
lX = 'LepGood_pt*cos(LepGood_phi)'
lY = 'LepGood_pt*sin(LepGood_phi)'
wPhi = 'atan2(('+wY+'),('+wX+'))'
wPT = 'sqrt(('+wX+')**2+('+wY+')**2)'
stLep = 'sqrt(('+wPT+')**2+('+mT+')**2)'
#stLep = '(LepGood_pt+(met_pt))'
stLepPred = 'sqrt(('+wPT+')**2+(mTPred)**2)'
#stLepPred = '(LepGood_pt+(metPred))'
num = '(('+wX+')*('+lX+'))+(('+wY+')*('+lY+'))'
den = '('+wPT+')*LepGood_pt'
cosDPhi = '('+num+')/('+den+')'
#dPhi = 'acos(('+cosDPhi+'))'
dPhi='acos((LepGood_pt+met_pt*cos(LepGood_phi-met_phi))/sqrt(LepGood_pt**2+met_pt**2+2*met_pt*LepGood_pt*cos(LepGood_phi-met_phi)))'
#c.Draw(dPhi)

minNJetCut = 2
maxNJetCut = 4
for htCut in [400]:
  for stCut in [150]:
    #for minNJets in [3]:
    for nbtagsCut in [0]: 
      print 'ht:', htCut, 'st:',stCut ,'njet:',minNJetCut,maxNJetCut-1 , 'nbtags >= ' , nbtagsCut
      #genSel= oneHadTau+'&&htJet40ja>'+str(htCut)+'&&nBJetMedium40>='+str(nbtagsCut)+'&&nJet40a>='+str(minNJetCut)+'&&nJet40a<'+str(maxNJetCut)+'&&'+stLep+'>'+str(stCut) 
      #predSel = 'htPred>'+str(htCut)+'&&nbtagsPred>='+str(nbtagsCut)+'&&njetsPred>='+str(minNJetCut)+'&&njetsPred<'+str(maxNJetCut)+'&&'+stLepPred+'>'+str(stCut)
      genSel= oneHadTau+'&&htJet40ja>'+str(htCut)+'&&nBJetMedium40>='+str(nbtagsCut)+'&&nJet40a>='+str(minNJetCut)+'&&nJet40a<'+str(maxNJetCut)+'&& st>'+str(stCut) 
      predSel = 'htPred>'+str(htCut)+'&&nbtagsPred>='+str(nbtagsCut)+'&&njetsPred>='+str(minNJetCut)+'&&njetsPred<'+str(maxNJetCut)+'&& st >'+str(stCut)
      #genSel = oneHadTau
      #predSel = 'htPred>'+str(htCut)
      Path='/afs/hephy.at/user/e/easilar/www/hadronicTau_PHYS14_inc/comparison_Results/ht_'+str(htCut)+'_st_'+str(stCut)+'_njet_'+str(minNJetCut)+'or'+str(maxNJetCut-1)+'_nbtag_lt_'+str(nbtagsCut)+'_DiffBin/' ##'+str(nbtagsCut)+'/'
      #Path='/afs/hephy.at/user/e/easilar/www/hadronicTau_28Jan/ht_'+str(htCut)+'_st_'+str(stCut)+'_njet_'+str(minNJetCut)+'or'+str(maxNJetCut-1)+'_nbtag_>_'+str(nbtagsCut)+'/' ##'+str(nbtagsCut)+'/'
      if not os.path.exists(Path):
        os.makedirs(Path)
      hMT = ROOT.TH1F('hMT', 'hMT',30,0,800)
      c.Draw('sqrt(2.*met_pt*LepGood_pt*(1-cos(LepGood_phi-met_phi)))>>hMT','weight*('+genSel+')','goff')
      #hMTOpen = ROOT.TH1F('hMTOpen', 'hMTOpen',30,0,800)
      #c.Draw('sqrt(2.*met_pt*LepGood_pt*(1-cos(LepGood_phi-met_phi)))>>hMTOpen','weight*('+oneHadTauOpen+'&&ht>'+str(htCut)+'&&nbtags=='+str(nbtagsCut)+'&&njets>='+str(minNJets)+'&&met_pt>'+str(metCut)+')','goff')
  
     #hMTPred = ROOT.TH1F('hMTPred', 'hMTPred',30,0,800)
     #cPred.Draw('mTPred>>hMTPred','weightPred*scaleLEff*('+str(scaleF)+')*('+predSel+')','goff')
     #hMTPred110 = ROOT.TH1F('hMTPred110', 'hMTPred110',30,0,800)
     #cPred.Draw('mTPred>>hMTPred110','weightPred*scaleLEffUp*('+str(scaleF)+')*('+predSel+')','goff')
     #hMTPred09 = ROOT.TH1F('hMTPred09', 'hMTPred09',30,0,800)
     #cPred.Draw('mTPred>>hMTPred09','weightPred*scaleLEffDown*('+str(scaleF)+')*('+predSel+')','goff')
  
     #DrawClosure(hMT,hMTPred,hMTPred110,hMTPred09,"M_{T}(GeV)",Path+'mT.png')
     #DrawClosure(hMT,hMTPred,hMTPred110,hMTPred09,"M_{T}(GeV)",Path+'mT.pdf')
     #DrawClosure(hMT,hMTPred,hMTPred110,hMTPred09,"M_{T}(GeV)",Path+'mT.root')

      hDeltaPhi = ROOT.TH1F('hDeltaPhi', 'hDeltaPhi',30,0,3.14)
      c.Draw(dPhi+'>>hDeltaPhi','weight*('+genSel+')','goff')
      #c.Draw(dPhi+'>>hDeltaPhi','weight*('+genSel+')','goff')

      hDeltaPhiPred = ROOT.TH1F('hDeltaPhiPred', 'hDeltaPhiPred',30,0,3.14)
      cPred.Draw('deltaPhiPred>>hDeltaPhiPred','weightPred*scaleLEff*('+str(scaleF)+')*('+predSel+')','goff')
      hDeltaPhiPred110 = ROOT.TH1F('hDeltaPhiPred110', 'hDeltaPhiPred110',30,0,3.14)
      cPred.Draw('deltaPhiPred>>hDeltaPhiPred110','weightPred*scaleLEffUp*('+str(scaleF)+')*('+predSel+')','goff')
      hDeltaPhiPred09 = ROOT.TH1F('hDeltaPhiPred09', 'hDeltaPhiPred09',30,0,3.14)
      cPred.Draw('deltaPhiPred>>hDeltaPhiPred09','weightPred*scaleLEffDown*('+str(scaleF)+')*('+predSel+')','goff')
  
      DrawClosure(hDeltaPhi,hDeltaPhiPred,hDeltaPhiPred110,hDeltaPhiPred09,'#Delta#phi(#mu,W)',Path+'deltaPhi.png')
      DrawClosure(hDeltaPhi,hDeltaPhiPred,hDeltaPhiPred110,hDeltaPhiPred09,'#Delta#phi(#mu,W)',Path+'deltaPhi.pdf')
      DrawClosure(hDeltaPhi,hDeltaPhiPred,hDeltaPhiPred110,hDeltaPhiPred09,'#Delta#phi(#mu,W)',Path+'deltaPhi.root')

      hHT = ROOT.TH1F('hHT', 'hHT',30,0,2000)
      c.Draw('htJet40ja>>hHT','weight*('+genSel+')','goff')
      hHTPred = ROOT.TH1F('hHTPred', 'hHTPred',30,0,2000)
      cPred.Draw('htPred>>hHTPred','weightPred*scaleLEff*('+str(scaleF)+')*('+predSel+')','goff')
      hHTPred110 = ROOT.TH1F('hHTPred110', 'hHTPred110',30,0,2000)
      cPred.Draw('htPred>>hHTPred110','weightPred*scaleLEffUp*('+str(scaleF)+')*('+predSel+')','goff')
      hHTPred09 = ROOT.TH1F('hHTPred09', 'hHTPred09',30,0,2000)
      cPred.Draw('htPred>>hHTPred09','weightPred*scaleLEffDown*('+str(scaleF)+')*('+predSel+')','goff')
  
      DrawClosure(hHT,hHTPred,hHTPred110,hHTPred09,'H_{T}(GeV)',Path+'ht.png')
      DrawClosure(hHT,hHTPred,hHTPred110,hHTPred09,'H_{T}(GeV)',Path+'ht.pdf')
      DrawClosure(hHT,hHTPred,hHTPred110,hHTPred09,'H_{T}(GeV)',Path+'ht.root')
  
      #hST = ROOT.TH1F('hST', 'hST',30,0,800)
      #c.Draw(stLep+'>>hST','weight*('+genSel+')','goff')
      #hSTPred = ROOT.TH1F('hSTPred', 'hSTPred',30,0,800)
      #cPred.Draw(stLepPred+'>>hSTPred','weightPred*scaleLEff*('+str(scaleF)+')*('+predSel+')','goff')
      #hSTPred110 = ROOT.TH1F('hSTPred110', 'hSTPred110',30,0,800)
      #cPred.Draw(stLepPred+'>>hSTPred110','weightPred*scaleLEffUp*('+str(scaleF)+')*('+predSel+')','goff')
      #hSTPred09 = ROOT.TH1F('hSTPred09', 'hSTPred09',30,0,800)
      #cPred.Draw(stLepPred+'>>hSTPred09','weightPred*scaleLEffDown*('+str(scaleF)+')*('+predSel+')','goff')
  
      hST = ROOT.TH1F('hST', 'hST',30,0,800)
      c.Draw('st>>hST','weight*('+genSel+')','goff')
      hSTPred = ROOT.TH1F('hSTPred', 'hSTPred',30,0,800)
      cPred.Draw('st>>hSTPred','weightPred*scaleLEff*('+str(scaleF)+')*('+predSel+')','goff')
      hSTPred110 = ROOT.TH1F('hSTPred110', 'hSTPred110',30,0,800)
      cPred.Draw('st>>hSTPred110','weightPred*scaleLEffUp*('+str(scaleF)+')*('+predSel+')','goff')
      hSTPred09 = ROOT.TH1F('hSTPred09', 'hSTPred09',30,0,800)
      cPred.Draw('st>>hSTPred09','weightPred*scaleLEffDown*('+str(scaleF)+')*('+predSel+')','goff')

      DrawClosure(hST,hSTPred,hSTPred110,hSTPred09,'S_{T}(GeV)',Path+'ST.png')
      DrawClosure(hST,hSTPred,hSTPred110,hSTPred09,'S_{T}(GeV)',Path+'ST.pdf')
      DrawClosure(hST,hSTPred,hSTPred110,hSTPred09,'S_{T}(GeV)',Path+'ST.root')

     #hMET = ROOT.TH1F('hMET', 'hMET',30,0,800)
     #c.Draw('met_pt>>hMET','weight*('+genSel+')','goff')
     #hMETPred = ROOT.TH1F('hMETPred', 'hMETPred',30,0,800)
     #cPred.Draw('metPred>>hMETPred','weightPred*scaleLEff*('+str(scaleF)+')*('+predSel+')','goff')
     #hMETPred110 = ROOT.TH1F('hMETPred110', 'hMETPred110',30,0,800)
     #cPred.Draw('metPred>>hMETPred110','weightPred*scaleLEffUp*('+str(scaleF)+')*('+predSel+')','goff')
     #hMETPred09 = ROOT.TH1F('hMETPred09', 'hMETPred09',30,0,800)
     #cPred.Draw('metPred>>hMETPred09','weightPred*scaleLEffDown*('+str(scaleF)+')*('+predSel+')','goff')
  
     #DrawClosure(hMET,hMETPred,hMETPred110,hMETPred09,'#slashE_{T}(GeV)',Path+'met.png')
     #DrawClosure(hMET,hMETPred,hMETPred110,hMETPred09,'#slashE_{T}(GeV)',Path+'met.pdf')
     #DrawClosure(hMET,hMETPred,hMETPred110,hMETPred09,'#slashE_{T}(GeV)',Path+'met.root')
  
      hNJet = ROOT.TH1F('hNJet', 'hNJet',10,0,10)
      c.Draw('nJet40a>>hNJet','weight*('+genSel+')','goff')
  
      hNJetPred = ROOT.TH1F('hNJetPred', 'hNJetPred',10,0,10)
      cPred.Draw('njetsPred>>hNJetPred','weightPred*scaleLEff*('+str(scaleF)+')*('+predSel+')','goff')
      hNJetPred110 = ROOT.TH1F('hNJetPred110', 'hNJetPred110',10,0,10)
      cPred.Draw('njetsPred>>hNJetPred110','weightPred*scaleLEffUp*('+str(scaleF)+')*('+predSel+')','goff')
      hNJetPred09 = ROOT.TH1F('hNJetPred09', 'hNJetPred09',10,0,10)
      cPred.Draw('njetsPred>>hNJetPred09','weightPred*scaleLEffDown*('+str(scaleF)+')*('+predSel+')','goff')
  
      DrawClosure(hNJet,hNJetPred,hNJetPred110,hNJetPred09,'N(JETS)',Path+'njets.png')
      DrawClosure(hNJet,hNJetPred,hNJetPred110,hNJetPred09,'N(JETS)',Path+'njets.pdf')
      DrawClosure(hNJet,hNJetPred,hNJetPred110,hNJetPred09,'N(JETS)',Path+'njets.root')
  
      hNBtag = ROOT.TH1F('hNBtag', 'hNBtag',10,0,10)
      c.Draw('nBJetMedium40>>hNBtag','weight*('+genSel+')','goff')
  
      hNBtagPred = ROOT.TH1F('hNBtagPred', 'hNBtagPred',10,0,10)
      cPred.Draw('nbtagsPred>>hNBtagPred','weightPred*scaleLEff*('+str(scaleF)+')*('+predSel+')','goff')
      hNBtagPred110 = ROOT.TH1F('hNBtagPred110', 'hNBtagPred110',10,0,10)
      cPred.Draw('nbtagsPred>>hNBtagPred110','weightPred*scaleLEffUp*('+str(scaleF)+')*('+predSel+')','goff')
      hNBtagPred09 = ROOT.TH1F('hNBtagPred09', 'hNBtagPred09',10,0,10)
      cPred.Draw('nbtagsPred>>hNBtagPred09','weightPred*scaleLEffDown*('+str(scaleF)+')*('+predSel+')','goff')
  
      DrawClosure(hNBtag,hNBtagPred,hNBtagPred110,hNBtagPred09,'N(Btags)',Path+'nbtags.png')
      DrawClosure(hNBtag,hNBtagPred,hNBtagPred110,hNBtagPred09,'N(Btags)',Path+'nbtags.pdf')
      DrawClosure(hNBtag,hNBtagPred,hNBtagPred110,hNBtagPred09,'N(Btags)',Path+'nbtags.root')
  


      print 'DELTA PHI >1: '
      ePred = ROOT.Double()
      eTruth = ROOT.Double()
      predYield = hDeltaPhiPred.IntegralAndError(hDeltaPhiPred.FindBin(1),hDeltaPhiPred.GetNbinsX(),ePred)
      truthYield = hDeltaPhi.IntegralAndError(hDeltaPhi.FindBin(1),hDeltaPhi.GetNbinsX(),eTruth)

      print '\documentclass{article}\usepackage[english]{babel}\usepackage[margin=0.5in]{geometry}\\begin{document}\\begin{center}\\begin{tabular}{| l | l | l | l |}\hline'
      print 'Hadronic Tau ($ \\triangle\phi>$',1,'  ) &Prediction & Truth  \\\ \hline'
      print 'ht$>$',htCut ,'and st$>$',stCut,'  and njet$=$',minNJetCut,'or',maxNJetCut-1,'  and nbtags$==$',nbtagsCut,'& $',format(predYield, '.2f'),'\pm',format(ePred, '.2f'),'(Stat)\pm',format(abs(hDeltaPhiPred110.Integral(hDeltaPhiPred110.FindBin(1),hDeltaPhiPred110.GetNbinsX())-predYield),'.2f'),'(\%10Leff)$ & $',format(truthYield,'.2f'),'\pm',format(eTruth,'.2f'),'(Stat)$ \\\ \hline '
      print '\end{tabular}\end{center}\end{document}'

      print 'DELTA PHI < 1: '
      ePredS = ROOT.Double()
      eTruthS = ROOT.Double()
      predYieldS = hDeltaPhiPred.IntegralAndError(0,hDeltaPhiPred.FindBin(1),ePredS)
      truthYieldS = hDeltaPhi.IntegralAndError(0,hDeltaPhi.FindBin(1),eTruthS)

      print '\documentclass{article}\usepackage[english]{babel}\usepackage[margin=0.5in]{geometry}\\begin{document}\\begin{center}\\begin{tabular}{| l | l | l | l |}\hline'
      print 'Hadronic Tau ($ \\triangle\phi<$',1,'  ) &Prediction & Truth  \\\ \hline'
      print 'ht$>$',htCut ,'and st$>$',stCut,'  and njet$=$',minNJetCut,'or',maxNJetCut-1,'  and nbtags$==$',nbtagsCut,'& $',format(predYieldS, '.2f'),'\pm',format(ePredS, '.2f'),'(Stat)\pm',format(abs(hDeltaPhiPred110.Integral(0,hDeltaPhiPred110.FindBin(1))-predYieldS),'.2f'),'(\%10Leff)$ & $',format(truthYieldS,'.2f'),'\pm',format(eTruthS,'.2f'),'(Stat)$ \\\ \hline '
      print '\end{tabular}\end{center}\end{document}'
