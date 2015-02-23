import ROOT
from Workspace.RA4Analysis.stage2Tuples import ttJetsCSA1450ns
from Workspace.HEPHYPythonTools.helpers import findClosestObject, deltaR,getVarValue, getObjFromFile
from Workspace.RA4Analysis.objectSelection import getGoodJetsStage2
from Workspace.RA4Analysis.makeCompPlotDilep import DrawClosure
from Workspace.RA4Analysis.makeNicePlot import DrawNicePlot
from math import *
from array import array
import os, sys
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v3 import *
from Workspace.HEPHYPythonTools.helpers import getChain

ROOT.gROOT.Reset()
ROOT.gROOT.LoadMacro("/afs/hephy.at/scratch/e/easilar/newWorkDir/CMSSW_7_2_3/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
ROOT.TH1F.SetDefaultSumw2()


#c = ROOT.TChain('Events')
#c = getChain(hard_ttJetsCSA1450ns)
#c.Add('/data/schoef/cmgTuples/postProcessed_v5_Phys14V2//inc/hard/TTJets/*.root')
c = ROOT.TChain('tree')
c.Add('/data/schoef/cmgTuples/v5_Phys14V2_fromDPM_lateProcessingTauFix/TTJets/*.root')

cPred = ROOT.TChain('Events')
#cPred.Add('/data/easilar/results2014/tauTuples/CSA14_TTJets_hadTauEstimate_cmg_large_PHYS14_inc_new.root')
#cPred.Add('/data/easilar/results2014/tauTuples/PHYS14_TTJets_hadTauEstimate_cmg_large.root')
cPred.Add('/data/easilar/results2014/tauTuples/PHYS14_TTJets_hadTauEstimate_cmg_large_CMVA.root')
#oneHadTau     ="Sum$(abs(LepGood_pdgId)==13)==1&&Sum$(abs(LepGood_pdgId==13)&&LepGood_tightId==1)==1&&Sum$(abs(LepGood_pdgId)==11)==0&&Sum$(genTau_pt>15&&abs(genTau_eta)<2.1&&(genTau_nMuNu+genTau_nMuE==0)&&genTau_nMuTau==1"
#oneHadTau     = "genTau_nNuE+genTau_nNuMu==0&&genTau_nNuTau==1"
       # &&Sum$(abs(LepGood_pdgId)==13 && LepGood_tightId==1 && abs(LepGood_eta)<2.1 && LepGood_relIso03 < 0.12)==1" #&&Sum$(abs(LepGood_pdgId)==11)==0" #\
#kin_Cut = '&&genPart_pt>25&&abs(genPart_eta)<2.4'
oneHadTau = 'Sum$((abs(genPart_pdgId)==14)&&abs(genPart_motherId)==24)==1'\
            +'&&Sum$(abs(genPart_pdgId)==16&&abs(genPart_motherId)==24)==1'\
            +'&&Sum$(genTau_nNuE+genTau_nNuMu==0&&genTau_nNuTau==1)==1'\

#scaleF = (1-0.1741-0.1783)*0.1125/(0.1057+0.1095)
scaleF = (1-0.1741-0.1783)*0.1125/(0.1057)
#scaleF = 0.6476 #plus or minus 0.0024

#hist_Title = "\#CMS \, Simulation \, L = 1 fb^{-1}, #sqrt{s} = 13 TeV"
mT = 'sqrt(2*LepGood_pt*met_pt*(1-cos(met_phi-LepGood_phi)))'
tot_lumi = 4000
nevents = c.GetEntries()
#weight = "("+str(tot_lumi)+"*xsec)/"+str(nevents)
weight = str(float(4000*809)/float(nevents))
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
nbtagsCMVA = 'Sum$(Jet_id&&Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_btagCMVA>0.732)'
nJet30 = "Sum$(Jet_id&&Jet_pt>30&&abs(Jet_eta)<2.4)"
minNJetCut = 2
maxNJetCut = 4
minht = 500
maxht = 750
minst = 250
maxst = 350

#for htCut in [750]:
#  for stCut in [350]:
    #for minNJets in [3]:
for nbtagsCut in [0,1,2]: 
      print 'ht:', minht,maxht, 'st:',minst,maxst ,'njet:',minNJetCut,maxNJetCut-1 , 'nbtags == ' , nbtagsCut
      #genSel= oneHadTau+'&&htJet40ja>'+str(htCut)+'&&nBJetMedium40>='+str(nbtagsCut)+'&&nJet40a>='+str(minNJetCut)+'&&nJet40a<'+str(maxNJetCut)+'&&'+stLep+'>'+str(stCut) 
      #predSel = 'htPred>'+str(htCut)+'&&nbtagsPred>='+str(nbtagsCut)+'&&njetsPred>='+str(minNJetCut)+'&&njetsPred<'+str(maxNJetCut)+'&&'+stLepPred+'>'+str(stCut)
      ###genSel= oneHadTau+'&&htJet40ja>'+str(htCut)+'&&nBJetMedium40>='+str(nbtagsCut)+'&&nJet40a>='+str(minNJetCut)+'&&nJet40a<'+str(maxNJetCut)+'&& st>'+str(stCut) 
      ###predSel = 'htPred>'+str(htCut)+'&&nbtagsPred>='+str(nbtagsCut)+'&&njetsPred>='+str(minNJetCut)+'&&njetsPred<'+str(maxNJetCut)+'&& st >'+str(stCut)
      ###genSel= oneHadTau+'&&htJet40ja>'+str(htCut)+'&&nJet40a>='+str(minNJetCut)+'&&nJet40a<'+str(maxNJetCut)+'&& (met_pt+LepGood_pt)>'+str(stCut) 
      genSel = nbtagsCMVA+"=="+str(nbtagsCut)+"&&htJet40ja>="+str(minht)+"&&htJet40ja<"+str(maxht)+"&&met_pt+LepGood_pt>="+str(minst)+"&&met_pt+LepGood_pt<"+str(maxst)+"&&"+nJet30+">="+str(minNJetCut)+"&&"+nJet30+"<"+str(maxNJetCut)+"&&LepGood_pt>25&&abs(LepGood_eta)<2.1&&LepGood_relIso03<0.3&&"+oneHadTau
      predSel ='htPred>='+str(minht) +'&&htPred<'+str(maxht)+'&&nbtagsCMVAPred=='+str(nbtagsCut)+'&&njets30Pred>='+str(minNJetCut)+'&&njets30Pred<'+str(maxNJetCut)+'&& stPred >='+str(minst)+'&& stPred <'+str(maxst)
      #genSel = oneHadTau
      #predSel = 'htPred>'+str(htCut)
      Path='/afs/hephy.at/user/e/easilar/www/hadronicTau_PHYS14_inc_CMVA/comparison_Results/ht_'+str(htCut)+'_st_'+str(stCut)+'_njet_'+str(minNJetCut)+'or'+str(maxNJetCut-1)+'_nbtag_lt_'+str(nbtagsCut)+'/' ##'+str(nbtagsCut)+'/'
      #Path='/afs/hephy.at/user/e/easilar/www/hadronicTau_28Jan/ht_'+str(htCut)+'_st_'+str(stCut)+'_njet_'+str(minNJetCut)+'or'+str(maxNJetCut-1)+'_nbtag_>_'+str(nbtagsCut)+'/' ##'+str(nbtagsCut)+'/'
      if not os.path.exists(Path):
        os.makedirs(Path)
      hMT = ROOT.TH1F('hMT', 'hMT',30,0,800)
      c.Draw('sqrt(2.*met_pt*LepGood_pt*(1-cos(LepGood_phi-met_phi)))>>hMT',weight+'*('+genSel+')','goff')
      #hMTOpen = ROOT.TH1F('hMTOpen', 'hMTOpen',30,0,800)
      #c.Draw('sqrt(2.*met_pt*LepGood_pt*(1-cos(LepGood_phi-met_phi)))>>hMTOpen',weight+'*('+oneHadTauOpen+'&&ht>'+str(htCut)+'&&nbtags=='+str(nbtagsCut)+'&&njets>='+str(minNJets)+'&&met_pt>'+str(metCut)+')','goff')
   
      hMTPred = ROOT.TH1F('hMTPred', 'hMTPred',30,0,800)
      cPred.Draw('mTPred>>hMTPred','weightPred*scaleLEff*('+str(scaleF)+')*('+predSel+')','goff')
      hMTPred110 = ROOT.TH1F('hMTPred110', 'hMTPred110',30,0,800)
      cPred.Draw('mTPred>>hMTPred110','weightPred*scaleLEffUp*('+str(scaleF)+')*('+predSel+')','goff')
      #hMTPred09 = ROOT.TH1F('hMTPred09', 'hMTPred09',30,0,800)
      #cPred.Draw('mTPred>>hMTPred09','weightPred*scaleLEffDown*('+str(scaleF)+')*('+predSel+')','goff')
   
      DrawClosure(hMT,hMTPred,hMTPred110,"M_{T}(GeV)",Path+'mT.png')
      DrawClosure(hMT,hMTPred,hMTPred110,"M_{T}(GeV)",Path+'mT.pdf')
      DrawClosure(hMT,hMTPred,hMTPred110,"M_{T}(GeV)",Path+'mT.root')
 
      hDeltaPhi = ROOT.TH1F('hDeltaPhi', 'hDeltaPhi',30,0,3.14)
      c.Draw(dPhi+'>>hDeltaPhi',weight+'*('+genSel+')','goff')
      #c.Draw(dPhi+'>>hDeltaPhi',weight+'*('+genSel+')','goff')
 
      hDeltaPhiPred = ROOT.TH1F('hDeltaPhiPred', 'hDeltaPhiPred',30,0,3.14)
      cPred.Draw('deltaPhiPred>>hDeltaPhiPred','weightPred*scaleLEff*('+str(scaleF)+')*('+predSel+')','goff')
      hDeltaPhiPred110 = ROOT.TH1F('hDeltaPhiPred110', 'hDeltaPhiPred110',30,0,3.14)
      cPred.Draw('deltaPhiPred>>hDeltaPhiPred110','weightPred*scaleLEffUp*('+str(scaleF)+')*('+predSel+')','goff')
   
      DrawClosure(hDeltaPhi,hDeltaPhiPred,hDeltaPhiPred110,'#Delta#phi(#mu,W)',Path+'deltaPhi.png')
      DrawClosure(hDeltaPhi,hDeltaPhiPred,hDeltaPhiPred110,'#Delta#phi(#mu,W)',Path+'deltaPhi.pdf')
      DrawClosure(hDeltaPhi,hDeltaPhiPred,hDeltaPhiPred110,'#Delta#phi(#mu,W)',Path+'deltaPhi.root')
 
      hHT = ROOT.TH1F('hHT', 'hHT',40,300,2000)
      c.Draw('htJet40ja>>hHT',weight+'*('+genSel+')','goff')
      hHTPred = ROOT.TH1F('hHTPred', 'hHTPred',40,300,2000)
      cPred.Draw('htPred>>hHTPred','weightPred*scaleLEff*('+str(scaleF)+')*('+predSel+')','goff')
      hHTPred110 = ROOT.TH1F('hHTPred110', 'hHTPred110',40,300,2000)
      cPred.Draw('htPred>>hHTPred110','weightPred*scaleLEffUp*('+str(scaleF)+')*('+predSel+')','goff')
      #hHTPred09 = ROOT.TH1F('hHTPred09', 'hHTPred09',30,0,2000)
      #cPred.Draw('htPred>>hHTPred09','weightPred*scaleLEffDown*('+str(scaleF)+')*('+predSel+')','goff')
   
      DrawClosure(hHT,hHTPred,hHTPred110,'H_{T}(GeV)',Path+'ht.png')
      DrawClosure(hHT,hHTPred,hHTPred110,'H_{T}(GeV)',Path+'ht.pdf')
      DrawClosure(hHT,hHTPred,hHTPred110,'H_{T}(GeV)',Path+'ht.root')
   
      #hST = ROOT.TH1F('hST', 'hST',30,0,800)
      #c.Draw(stLep+'>>hST',weight+'*('+genSel+')','goff')
      #hSTPred = ROOT.TH1F('hSTPred', 'hSTPred',30,0,800)
      #cPred.Draw(stLepPred+'>>hSTPred','weightPred*scaleLEff*('+str(scaleF)+')*('+predSel+')','goff')
      #hSTPred110 = ROOT.TH1F('hSTPred110', 'hSTPred110',30,0,800)
      #cPred.Draw(stLepPred+'>>hSTPred110','weightPred*scaleLEffUp*('+str(scaleF)+')*('+predSel+')','goff')
      #hSTPred09 = ROOT.TH1F('hSTPred09', 'hSTPred09',30,0,800)
      #cPred.Draw(stLepPred+'>>hSTPred09','weightPred*scaleLEffDown*('+str(scaleF)+')*('+predSel+')','goff')
   
      hST = ROOT.TH1F('hST', 'hST',40,150,1000)
      c.Draw('(met_pt+LepGood_pt)>>hST',weight+'*('+genSel+')','goff')
      hSTPred = ROOT.TH1F('hSTPred', 'hSTPred',40,150,1000)
      cPred.Draw('stPred>>hSTPred','weightPred*scaleLEff*('+str(scaleF)+')*('+predSel+')','goff')
      hSTPred110 = ROOT.TH1F('hSTPred110', 'hSTPred110',40,150,1000)
      cPred.Draw('stPred>>hSTPred110','weightPred*scaleLEffUp*('+str(scaleF)+')*('+predSel+')','goff')
      #hSTPred09 = ROOT.TH1F('hSTPred09', 'hSTPred09',30,0,800)
      #cPred.Draw('stPred>>hSTPred09','weightPred*scaleLEffDown*('+str(scaleF)+')*('+predSel+')','goff')
 
      DrawClosure(hST,hSTPred,hSTPred110,'S_{T}(GeV)',Path+'ST.png')
      DrawClosure(hST,hSTPred,hSTPred110,'S_{T}(GeV)',Path+'ST.pdf')
      DrawClosure(hST,hSTPred,hSTPred110,'S_{T}(GeV)',Path+'ST.root')
 
      hMET = ROOT.TH1F('hMET', 'hMET',30,0,800)
      c.Draw('met_pt>>hMET',weight+'*('+genSel+')','goff')
      hMETPred = ROOT.TH1F('hMETPred', 'hMETPred',30,0,800)
      cPred.Draw('metPred>>hMETPred','weightPred*scaleLEff*('+str(scaleF)+')*('+predSel+')','goff')
      hMETPred110 = ROOT.TH1F('hMETPred110', 'hMETPred110',30,0,800)
      cPred.Draw('metPred>>hMETPred110','weightPred*scaleLEffUp*('+str(scaleF)+')*('+predSel+')','goff')
   
      DrawClosure(hMET,hMETPred,hMETPred110,'#slashE_{T}(GeV)',Path+'met.png')
      DrawClosure(hMET,hMETPred,hMETPred110,'#slashE_{T}(GeV)',Path+'met.pdf')
      DrawClosure(hMET,hMETPred,hMETPred110,'#slashE_{T}(GeV)',Path+'met.root')
   
      hNJet = ROOT.TH1F('hNJet', 'hNJet',9,2,11)
      c.Draw(nJet30+'>>hNJet',weight+'*('+genSel+')','goff')
  
      hNJetPred = ROOT.TH1F('hNJetPred', 'hNJetPred',9,2,11)
      cPred.Draw('njets30Pred>>hNJetPred','weightPred*scaleLEff*('+str(scaleF)+')*('+predSel+')','goff')
      hNJetPred110 = ROOT.TH1F('hNJetPred110', 'hNJetPred110',9,2,11)
      cPred.Draw('njets30Pred>>hNJetPred110','weightPred*scaleLEffUp*('+str(scaleF)+')*('+predSel+')','goff')
      #hNJetPred09 = ROOT.TH1F('hNJetPred09', 'hNJetPred09',10,0,10)
      #cPred.Draw('njetsPred>>hNJetPred09','weightPred*scaleLEffDown*('+str(scaleF)+')*('+predSel+')','goff')
  
      DrawClosure(hNJet,hNJetPred,hNJetPred110,'n_{jet}',Path+'njets.png')
      DrawClosure(hNJet,hNJetPred,hNJetPred110,'n_{jet}',Path+'njets.pdf')
      DrawClosure(hNJet,hNJetPred,hNJetPred110,'n_{jet}',Path+'njets.root')
  
      hNBtag = ROOT.TH1F('hNBtag', 'hNBtag',10,0,10)
      c.Draw('nBJetMedium40>>hNBtag',weight+'*('+genSel+')','goff')
  
      hNBtagPred = ROOT.TH1F('hNBtagPred', 'hNBtagPred',10,0,10)
      cPred.Draw('nbtagsPred>>hNBtagPred','weightPred*scaleLEff*('+str(scaleF)+')*('+predSel+')','goff')
      hNBtagPred110 = ROOT.TH1F('hNBtagPred110', 'hNBtagPred110',10,0,10)
      cPred.Draw('nbtagsPred>>hNBtagPred110','weightPred*scaleLEffUp*('+str(scaleF)+')*('+predSel+')','goff')
      #hNBtagPred09 = ROOT.TH1F('hNBtagPred09', 'hNBtagPred09',10,0,10)
      #cPred.Draw('nbtagsPred>>hNBtagPred09','weightPred*scaleLEffDown*('+str(scaleF)+')*('+predSel+')','goff')
  
      DrawClosure(hNBtag,hNBtagPred,hNBtagPred110,'n_{b-tag}',Path+'nbtags.png')
      DrawClosure(hNBtag,hNBtagPred,hNBtagPred110,'n_{b-tag}',Path+'nbtags.pdf')
      DrawClosure(hNBtag,hNBtagPred,hNBtagPred110,'n_{b-tag}',Path+'nbtags.root')
 
      hNBtag = ROOT.TH1F('hNBtag', 'hNBtag',10,0,10)
      c.Draw(nbtagsCMVA+'>>hNBtag',weight+'*('+genSel+')','goff')
  
      hNBtagPred = ROOT.TH1F('hNBtagPred', 'hNBtagPred',10,0,10)
      cPred.Draw('nbtagsCMVAPred>>hNBtagPred','weightPred*scaleLEff*('+str(scaleF)+')*('+predSel+')','goff')
      hNBtagPred110 = ROOT.TH1F('hNBtagPred110', 'hNBtagPred110',10,0,10)
      cPred.Draw('nbtagsCMVAPred>>hNBtagPred110','weightPred*scaleLEffUp*('+str(scaleF)+')*('+predSel+')','goff')
      #hNBtagPred09 = ROOT.TH1F('hNBtagPred09', 'hNBtagPred09',10,0,10)
      #cPred.Draw('nbtagsPred>>hNBtagPred09','weightPredOld*scaleLEffDown*('+str(scaleF)+')*('+predSel+')','goff')
  
      DrawClosure(hNBtag,hNBtagPred,hNBtagPred110,'n_{b-tag}',Path+'nbtags_CMVA.png')
      DrawClosure(hNBtag,hNBtagPred,hNBtagPred110,'n_{b-tag}',Path+'nbtags_CMVA.pdf')
      DrawClosure(hNBtag,hNBtagPred,hNBtagPred110,'n_{b-tag}',Path+'nbtags_CMVA.root')
 
 
      print 'DELTA PHI >1: '
      ePred = ROOT.Double()
      eTruth = ROOT.Double()
      predYield = hDeltaPhiPred.IntegralAndError(hDeltaPhiPred.FindBin(1),hDeltaPhiPred.GetNbinsX(),ePred)
      truthYield = hDeltaPhi.IntegralAndError(hDeltaPhi.FindBin(1),hDeltaPhi.GetNbinsX(),eTruth)
 
      print '& $',format(predYield, '.2f'),' $&$\pm$&$',format(ePred, '.2f'),'$(stat)&$\pm$&$',format(abs(hDeltaPhiPred110.Integral(hDeltaPhiPred110.FindBin(1),hDeltaPhiPred110.GetNbinsX())-predYield),'.2f'),'$(sys)& $ ',format(truthYield,'.2f'),' $&$\pm$&$',format(eTruth,'.2f'),'$(stat) \\'
    # print '\documentclass{article}\usepackage[english]{babel}\usepackage[margin=0.5in]{geometry}\\begin{document}\\begin{center}\\begin{tabular}{|c|ll|l|lllll|lll|}\hline'
    # print 'Hadronic Tau ($ \\triangle\phi>$',1,'  ) &Prediction & Truth  \\\ \hline'
    # print 'ht$>$',htCut ,'and st$>$',stCut,'  and njet$=$',minNJetCut,'or',maxNJetCut-1,'  and nbtags$==$',nbtagsCut,'& $',format(predYield, '.2f'),'\pm',format(ePred, '.2f'),'(Stat)\pm',format(abs(hDeltaPhiPred110.Integral(hDeltaPhiPred110.FindBin(1),hDeltaPhiPred110.GetNbinsX())-predYield),'.2f'),'(\%10Leff)$ & $',format(truthYield,'.2f'),'\pm',format(eTruth,'.2f'),'(Stat)$ \\\ \hline '
    # print '\end{tabular}\end{center}\end{document}'
 
      print 'DELTA PHI < 1: '
      ePredS = ROOT.Double()
      eTruthS = ROOT.Double()
      predYieldS = hDeltaPhiPred.IntegralAndError(0,hDeltaPhiPred.FindBin(1),ePredS)
      truthYieldS = hDeltaPhi.IntegralAndError(0,hDeltaPhi.FindBin(1),eTruthS)
      print '& $',format(predYieldS, '.2f'),' $&$\pm$&$',format(ePredS, '.2f'),'$(stat)&$\pm$&$',format(abs(hDeltaPhiPred110.Integral(0,hDeltaPhiPred110.FindBin(1))-predYieldS),'.2f'),'$(sys)& $ ',format(truthYieldS,'.2f'),' $&$\pm$&$',format(eTruthS,'.2f'),'$(stat) \\'
    # print '\documentclass{article}\usepackage[english]{babel}\usepackage[margin=0.5in]{geometry}\\begin{document}\\begin{center}\\begin{tabular}{|c|ll|l|lllll|lll|}\hline'
    # print 'Hadronic Tau ($ \\triangle\phi<$',1,'  ) &Prediction & Truth  \\\ \hline'
    # print 'ht$>$',htCut ,'and st$>$',stCut,'  and njet$=$',minNJetCut,'or',maxNJetCut-1,'  and nbtags$==$',nbtagsCut,'& $',format(predYieldS, '.2f'),'\pm',format(ePredS, '.2f'),'(Stat)\pm',format(abs(hDeltaPhiPred110.Integral(0,hDeltaPhiPred110.FindBin(1))-predYieldS),'.2f'),'(\%10Leff)$ & $',format(truthYieldS,'.2f'),'\pm',format(eTruthS,'.2f'),'(Stat)$ \\\ \hline '
    # print '\end{tabular}\end{center}\end{document}'
      del hDeltaPhiPred
      del hDeltaPhi
      del hDeltaPhiPred110 
