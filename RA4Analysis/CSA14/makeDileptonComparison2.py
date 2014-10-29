import ROOT
from Workspace.RA4Analysis.makeCompPlotDilep import DrawClosure
from localInfo import username

relIso=0.3
ptCut=15
deltaPhiCut = '>1' ##larger than 1
htCut     = 500
metCut    = 150
minNJets  =  3

leptonID = "muIsPF&&(muIsGlobal||muIsTracker)&&muPt>"+str(ptCut)+"&&abs(muEta)<2.5"\
          +"&&abs(muDxy)<0.2&&abs(muDz)<0.5"\
          +"&&muRelIso<"+str(relIso)

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

DrawClosure(hMT,hMTPred,hMTPredUp,hMTPredDown,'MT')

hHT = ROOT.TH1F('hHT', 'hHT',20,0,2000)
cLost.Draw('ht>>hHT','weightTruth*(htTruth>'+str(htCut)+'&&njetsTruth>='+str(minNJets)+'&&metTruth>'+str(metCut)+')','goff')
hHTPred = ROOT.TH1F('hHTPred', 'hHTPred',20,0,2000)
cPred.Draw('htPred>>hHTPred','weightPred*scaleLEff*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hHTPredUp = ROOT.TH1F('hHTPredUp', 'hHTPredUp',20,0,2000)
cPred.Draw('htPred>>hHTPredUp','weightPred*scaleLEffUp*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hHTPredDown = ROOT.TH1F('hHTPredDown', 'hHTPredDown',20,0,2000)
cPred.Draw('htPred>>hHTPredDown','weightPred*scaleLEffDown*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

DrawClosure(hHT,hHTPred,hHTPredUp,hHTPredDown,'HT')

hNJets = ROOT.TH1F('hNJets', 'hNJets',20,0,20)
cLost.Draw('njetsTruth>>hNJets','weightTruth*(htTruth>'+str(htCut)+'&&njetsTruth>='+str(minNJets)+'&&metTruth>'+str(metCut)+')','goff')
hNJetsPred = ROOT.TH1F('hNJetsPred', 'hNJetsPred',20,0,20)
cPred.Draw('njetsPred>>hNJetsPred','weightPred*scaleLEff*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hNJetsPredUp = ROOT.TH1F('hNJetsPredUp', 'hNJetsPredUp',20,0,20)
cPred.Draw('njetsPred>>hNJetsPredUp','weightPred*scaleLEffUp*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hNJetsPredDown = ROOT.TH1F('hNJetsPredDown', 'hNJetsPredDown',20,0,20)
cPred.Draw('njetsPred>>hNJetsPredDown','weightPred*scaleLEffDown*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

DrawClosure(hNJets,hNJetsPred,hNJetsPredUp,hNJetsPredDown,'NJets')

hMET = ROOT.TH1F('hMET', 'hMET',20,0,800)
cLost.Draw('metTruth>>hMET','weightTruth*(htTruth>'+str(htCut)+'&&njetsTruth>='+str(minNJets)+'&&metTruth>'+str(metCut)+')','goff')
hMETPred = ROOT.TH1F('hMETPred', 'hMETPred',20,0,800)
cPred.Draw('metPred>>hMETPred','weightPred*scaleLEff*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hMETPredUp = ROOT.TH1F('hMETPredUp', 'hMETPredUp',20,0,800)
cPred.Draw('metPred>>hMETPredUp','weightPred*scaleLEffUp*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hMETPredDown = ROOT.TH1F('hMETPredDown', 'hMETPredDown',20,0,800)
cPred.Draw('metPred>>hMETPredDown','weightPred*scaleLEffDown*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

DrawClosure(hMET,hMETPred,hMETPredUp,hMETPredDown,'MET')

hST = ROOT.TH1F('hST', 'hST',20,0,2000)
cLost.Draw('stTruth>>hST','weightTruth*(htTruth>'+str(htCut)+'&&njetsTruth>='+str(minNJets)+'&&metTruth>'+str(metCut)+')','goff')
hSTPred = ROOT.TH1F('hSTPred', 'hSTPred',20,0,2000)
cPred.Draw('stPred>>hSTPred','weightPred*scaleLEff*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hSTPredUp = ROOT.TH1F('hSTPredUp', 'hSTPredUp',20,0,2000)
cPred.Draw('stPred>>hSTPredUp','weightPred*scaleLEffUp*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hSTPredDown = ROOT.TH1F('hSTPredDown', 'hSTPredDown',20,0,2000)
cPred.Draw('stPred>>hSTPredDown','weightPred*scaleLEffDown*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

DrawClosure(hST,hSTPred,hSTPredUp,hSTPredDown,'ST')

hDeltaPhi = ROOT.TH1F('hDeltaPhi', 'hDeltaPhi',25,0,3.14)
cLost.Draw('deltaPhiTruth>>hDeltaPhi','weightTruth*(htTruth>'+str(htCut)+'&&njetsTruth>='+str(minNJets)+'&&metTruth>'+str(metCut)+')','goff')
hDeltaPhiPred = ROOT.TH1F('hDeltaPhiPred', 'hDeltaPhiPred',25,0,3.14)
cPred.Draw('deltaPhiPred>>hDeltaPhiPred','weightPred*scaleLEff*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hDeltaPhiPredUp = ROOT.TH1F('hDeltaPhiPredUp', 'hDeltaPhiPredUp',25,0,3.14)
cPred.Draw('deltaPhiPred>>hDeltaPhiPredUp','weightPred*scaleLEffUp*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hDeltaPhiPredDown = ROOT.TH1F('hDeltaPhiPredDown', 'hDeltaPhiPredDown',25,0,3.14)
cPred.Draw('deltaPhiPred>>hDeltaPhiPredDown','weightPred*scaleLEffDown*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

DrawClosure(hDeltaPhi,hDeltaPhiPred,hDeltaPhiPredUp,hDeltaPhiPredDown,'DeltaPhi')

##For Statistics##
hDeltaPhiStat = ROOT.TH1F('hDeltaPhiStat', 'hDeltaPhiStat',20,0,3.14)
hDeltaPhiStat.Sumw2() 
cLost.Draw('deltaPhiTruth>>hDeltaPhiStat','weightTruth*(deltaPhiTruth'+deltaPhiCut+'&&htTruth>'+str(htCut)+'&&njetsTruth>='+str(minNJets)+'&&metTruth>'+str(metCut)+')','goff')
hDeltaPhiPredStat = ROOT.TH1F('hDeltaPhiPredStat', 'hDeltaPhiPredStat',20,0,3.14)
hDeltaPhiPredStat.Sumw2()
cPred.Draw('deltaPhiPred>>hDeltaPhiPredStat','weightPred*scaleLEff*(deltaPhiPred'+deltaPhiCut+'&&htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hDeltaPhiPredUpStat = ROOT.TH1F('hDeltaPhiPredUpStat', 'hDeltaPhiPredUpStat',20,0,3.14)
hDeltaPhiPredUp.Sumw2()
cPred.Draw('deltaPhiPred>>hDeltaPhiPredUpStat','weightPred*scaleLEffUp*(deltaPhiPred'+deltaPhiCut+'&&htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

ePred = ROOT.Double()
eTruth = ROOT.Double()
predYield = hDeltaPhiPredStat.IntegralAndError(0,hDeltaPhiPredStat.GetNbinsX(),ePred)
truthYield = hDeltaPhiStat.IntegralAndError(0,hDeltaPhiStat.GetNbinsX(),eTruth)

print 'ht:', htCut,'met:',metCut,'njets:',minNJets
print 'deltaPhi>1:', 'Prediction yield:', predYield, 'ePred :', ePred, 'Truth yield:', truthYield,'eTruth:', eTruth, '%10Leff:', abs(hDeltaPhiPredUpStat.Integral()-predYield)


