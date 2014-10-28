import ROOT
from Workspace.RA4Analysis.stage2Tuples import *
from localInfo import username

relIso=0.3
ptCut = 15
leptonID = "muIsPF&&(muIsGlobal||muIsTracker)&&muPt>"+str(ptCut)+"&&abs(muEta)<2.5"\
          +"&&abs(muDxy)<0.2&&abs(muDz)<0.5"\
          +"&&muRelIso<"+str(relIso)
LostLepton = "nvetoMuons==1&&"
htCut     = 500
metCut    = 150
minNJets  =  3
print 'ht:', htCut,'met:',metCut,'njets:',minNJets
c = ROOT.TChain('Events')
for b in ttJetsCSA1450ns['bins']:
  c.Add(ttJetsCSA1450ns['dirname']+'/'+b+'/h*.root')

cPred = ROOT.TChain('Events')
cPred.Add('/data/easilar/results2014/muonTuples/CSA14_TTJets_dilep_relIso'+str(relIso)+'.root')

cLost = ROOT.TChain('Events')
cLost.Add('/data/easilar/results2014/muonTuples/CSA14_TTJets_Lost_relIso'+str(relIso)+'.root')

hMT = ROOT.TH1F('hMT', 'hMT',20,0,800)
cLost.Draw('mTTruth>>hMT','weightTruth*(htTruth>'+str(htCut)+'&&njetsTruth>='+str(minNJets)+'&&metTruth>'+str(metCut)+')','goff')
hMTPred = ROOT.TH1F('hMTPred', 'hMTPred',20,0,800)
cPred.Draw('mTPred>>hMTPred','weightPred*scaleLEff*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hMTPredUp = ROOT.TH1F('hMTPredUp', 'hMTPredUp',20,0,800)
cPred.Draw('mTPred>>hMTPredUp','weightPred*scaleLEffUp*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hMTPredDown = ROOT.TH1F('hMTPredDown', 'hMTPredDown',20,0,800)
cPred.Draw('mTPred>>hMTPredDown','weightPred*scaleLEffDown*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

c1=ROOT.TCanvas()
hMT.Draw()
hMTPred.SetLineColor(ROOT.kRed)
hMTPred.Draw('same')
hMTPredUp.SetLineColor(ROOT.kGreen)
hMTPredUp.Draw('same')
hMTPredDown.SetLineColor(ROOT.kYellow)
hMTPredDown.Draw('same')
c1.SetLogy()
c1.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/pngCSA14/compMT_diLep_relIso'+str(relIso)+'.png')

hHT = ROOT.TH1F('hHT', 'hHT',20,0,2000)
cLost.Draw('ht>>hHT','weightTruth*(htTruth>'+str(htCut)+'&&njetsTruth>='+str(minNJets)+'&&metTruth>'+str(metCut)+')','goff')
hHTPred = ROOT.TH1F('hHTPred', 'hHTPred',20,0,2000)
cPred.Draw('htPred>>hHTPred','weightPred*scaleLEff*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hHTPredUp = ROOT.TH1F('hHTPredUp', 'hHTPredUp',20,0,2000)
cPred.Draw('htPred>>hHTPredUp','weightPred*scaleLEffUp*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hHTPredDown = ROOT.TH1F('hHTPredDown', 'hHTPredDown',20,0,2000)
cPred.Draw('htPred>>hHTPredDown','weightPred*scaleLEffDown*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

c1=ROOT.TCanvas()
hHT.Draw()
hHTPred.SetLineColor(ROOT.kRed)
hHTPred.Draw('same')
hHTPredUp.SetLineColor(ROOT.kGreen)
hHTPredUp.Draw('same')
hHTPredDown.SetLineColor(ROOT.kYellow)
hHTPredDown.Draw('same')
c1.SetLogy()
c1.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/pngCSA14/compHT_diLep_relIso'+str(relIso)+'.png')


hNJets = ROOT.TH1F('hNJets', 'hNJets',20,0,20)
cLost.Draw('njetsTruth>>hNJets','weightTruth*(htTruth>'+str(htCut)+'&&njetsTruth>='+str(minNJets)+'&&metTruth>'+str(metCut)+')','goff')
hNJetsPred = ROOT.TH1F('hNJetsPred', 'hNJetsPred',20,0,20)
cPred.Draw('njetsPred>>hNJetsPred','weightPred*scaleLEff*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hNJetsPredUp = ROOT.TH1F('hNJetsPredUp', 'hNJetsPredUp',20,0,20)
cPred.Draw('njetsPred>>hNJetsPredUp','weightPred*scaleLEffUp*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hNJetsPredDown = ROOT.TH1F('hNJetsPredDown', 'hNJetsPredDown',20,0,20)
cPred.Draw('njetsPred>>hNJetsPredDown','weightPred*scaleLEffDown*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

c1=ROOT.TCanvas()
hNJets.Draw()
hNJetsPred.SetLineColor(ROOT.kRed)
hNJetsPred.Draw('same')
hNJetsPredUp.SetLineColor(ROOT.kGreen)
hNJetsPredUp.Draw('same')
hNJetsPredDown.SetLineColor(ROOT.kYellow)
hNJetsPredDown.Draw('same')
c1.SetLogy()
c1.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/pngCSA14/compNJets_diLep_relIso'+str(relIso)+'.png')

hMET = ROOT.TH1F('hMET', 'hMET',20,0,2000)
cLost.Draw('metTruth>>hMET','weightTruth*(htTruth>'+str(htCut)+'&&njetsTruth>='+str(minNJets)+'&&metTruth>'+str(metCut)+')','goff')
hMETPred = ROOT.TH1F('hMETPred', 'hMETPred',20,0,2000)
cPred.Draw('metPred>>hMETPred','weightPred*scaleLEff*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hMETPredUp = ROOT.TH1F('hMETPredUp', 'hMETPredUp',20,0,2000)
cPred.Draw('metPred>>hMETPredUp','weightPred*scaleLEffUp*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hMETPredDown = ROOT.TH1F('hMETPredDown', 'hMETPredDown',20,0,2000)
cPred.Draw('metPred>>hMETPredDown','weightPred*scaleLEffDown*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

c1=ROOT.TCanvas()
hMET.Draw()
hMETPred.SetLineColor(ROOT.kRed)
hMETPred.Draw('same')
hMETPredUp.SetLineColor(ROOT.kGreen)
hMETPredUp.Draw('same')
hMETPredDown.SetLineColor(ROOT.kYellow)
hMETPredDown.Draw('same')
c1.SetLogy()
c1.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/pngCSA14/compMET_diLep_relIso'+str(relIso)+'.png')


hST = ROOT.TH1F('hST', 'hST',20,0,2000)
cLost.Draw('stTruth>>hST','weightTruth*(htTruth>'+str(htCut)+'&&njetsTruth>='+str(minNJets)+'&&metTruth>'+str(metCut)+')','goff')
hSTPred = ROOT.TH1F('hSTPred', 'hSTPred',20,0,2000)
cPred.Draw('stPred>>hSTPred','weightPred*scaleLEff*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hSTPredUp = ROOT.TH1F('hSTPredUp', 'hSTPredUp',20,0,2000)
cPred.Draw('stPred>>hSTPredUp','weightPred*scaleLEffUp*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hSTPredDown = ROOT.TH1F('hSTPredDown', 'hSTPredDown',20,0,2000)
cPred.Draw('stPred>>hSTPredDown','weightPred*scaleLEffDown*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

c1=ROOT.TCanvas()
hST.Draw()
hSTPred.SetLineColor(ROOT.kRed)
hSTPred.Draw('same')
hSTPredUp.SetLineColor(ROOT.kGreen)
hSTPredUp.Draw('same')
hSTPredDown.SetLineColor(ROOT.kYellow)
hSTPredDown.Draw('same')
c1.SetLogy()
c1.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/pngCSA14/compST_diLep_relIso'+str(relIso)+'.png')


hDeltaPhi = ROOT.TH1F('hDeltaPhi', 'hDeltaPhi',20,0,3.14)
cLost.Draw('deltaPhiTruth>>hDeltaPhi','weightTruth*(htTruth>'+str(htCut)+'&&njetsTruth>='+str(minNJets)+'&&metTruth>'+str(metCut)+')','goff')
hDeltaPhiPred = ROOT.TH1F('hDeltaPhiPred', 'hDeltaPhiPred',20,0,3.14)
cPred.Draw('deltaPhiPred>>hDeltaPhiPred','weightPred*scaleLEff*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hDeltaPhiPredUp = ROOT.TH1F('hDeltaPhiPredUp', 'hDeltaPhiPredUp',20,0,3.14)
cPred.Draw('deltaPhiPred>>hDeltaPhiPredUp','weightPred*scaleLEffUp*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hDeltaPhiPredDown = ROOT.TH1F('hDeltaPhiPredDown', 'hDeltaPhiPredDown',20,0,3.14)
cPred.Draw('deltaPhiPred>>hDeltaPhiPredDown','weightPred*scaleLEffDown*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

c1=ROOT.TCanvas()
hDeltaPhi.Draw()
hDeltaPhiPred.SetLineColor(ROOT.kRed)
hDeltaPhiPred.Draw('same')
hDeltaPhiPredUp.SetLineColor(ROOT.kGreen)
hDeltaPhiPredUp.Draw('same')
hDeltaPhiPredDown.SetLineColor(ROOT.kYellow)
hDeltaPhiPredDown.Draw('same')
c1.SetLogy()
c1.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/pngCSA14/compDeltaPhi_diLep_relIso'+str(relIso)+'.png')

##For Statistics##
hDeltaPhiStat = ROOT.TH1F('hDeltaPhiStat', 'hDeltaPhiStat',20,0,3.14)
hDeltaPhiStat.Sumw2() 
cLost.Draw('deltaPhiTruth>>hDeltaPhiStat','weightTruth*(deltaPhiTruth>1&&htTruth>'+str(htCut)+'&&njetsTruth>='+str(minNJets)+'&&metTruth>'+str(metCut)+')','goff')
hDeltaPhiPredStat = ROOT.TH1F('hDeltaPhiPredStat', 'hDeltaPhiPredStat',20,0,3.14)
hDeltaPhiPredStat.Sumw2()
cPred.Draw('deltaPhiPred>>hDeltaPhiPredStat','weightPred*scaleLEff*(deltaPhiPred>1&&htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hDeltaPhiPredUpStat = ROOT.TH1F('hDeltaPhiPredUpStat', 'hDeltaPhiPredUpStat',20,0,3.14)
hDeltaPhiPredUp.Sumw2()
cPred.Draw('deltaPhiPred>>hDeltaPhiPredUpStat','weightPred*scaleLEffUp*(deltaPhiPred>1&&htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

ePred = ROOT.Double()
eTruth = ROOT.Double()
predYield = hDeltaPhiPredStat.IntegralAndError(0,hDeltaPhiPredStat.GetNbinsX(),ePred)
truthYield = hDeltaPhiStat.IntegralAndError(0,hDeltaPhiStat.GetNbinsX(),eTruth)
print 'deltaPhi>1:' 
print 'Prediction yield:', predYield
print 'ePred :', ePred
print 'Truth yield:', truthYield
print 'eTruth:', eTruth
print '%10Leff:', abs(hDeltaPhiPredUpStat.Integral()-predYield)


