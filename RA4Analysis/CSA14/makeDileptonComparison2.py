import ROOT
from Workspace.RA4Analysis.makeCompPlotDilep import DrawClosure
from localInfo import username

relIso=0.3
ptCut=15
deltaPhiCut = '>1' ##larger than 1
htCut     = 150
metCut    = 150
minNJets  =  3

leptonID = "muIsPF&&(muIsGlobal||muIsTracker)&&muPt>"+str(ptCut)+"&&abs(muEta)<2.5"\
          +"&&abs(muDxy)<0.2&&abs(muDz)<0.5"\
          +"&&muRelIso<"+str(relIso)

plots = [
        {'varname':'MT',         'var':'mT',         'bin':25  ,   'lowlimit':0,  'limit':800},\
        {'varname':'ST',         'var':'st',         'bin':25  ,   'lowlimit':0,  'limit':1400},\
        {'varname':'NJets',      'var':'njets',      'bin':16  ,   'lowlimit':0,  'limit':16},\
        {'varname':'MET',        'var':'met',        'bin':25  ,   'lowlimit':0,  'limit':800},\
        {'varname':'HT',         'var':'ht',         'bin':25  ,   'lowlimit':0,  'limit':2000},\
        {'varname':'PT',         'var':'muPt',       'bin':25  ,   'lowlimit':0,  'limit':800},\
        {'varname':'DeltaPhi',   'var':'deltaPhi',   'bin':25  ,   'lowlimit':0,  'limit':3.14},\
        ]

truthSelection = 'weightTruth*(htTruth>'+str(htCut)+'&&njetsTruth>='+str(minNJets)+'&&metTruth>'+str(metCut)+')'
predSelection = 'weightPred*scaleLEff*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')'
predSelectionUp = 'weightPred*scaleLEffUp*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')'
predSelectionDown = 'weightPred*scaleLEffDown*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')'

cPred = ROOT.TChain('Events')
cPred.Add('/data/easilar/results2014/muonTuples/CSA14_TTJets_dilep_New_relIso'+str(relIso)+'.root')

cLost = ROOT.TChain('Events')
cLost.Add('/data/easilar/results2014/muonTuples/CSA14_TTJets_Lost_New_relIso'+str(relIso)+'.root')

for p in plots:
  histo = 'h'+p['varname']
  histoPred = 'h'+p['varname']+'Pred'
  histoPredUp = 'h'+p['varname']+'PredUp'
  histoPredDown = 'h'+p['varname']+'PredDown'
  histoname = histo
  histonamePred = histoPred
  histonamePredUp = histoPredUp
  histonamePredDown = histoPredDown

  histo = ROOT.TH1F(str(histo) ,str(histo),20,p['lowlimit'],p['limit'])
  cLost.Draw(p['var']+'Truth>>'+str(histoname),truthSelection,'goff')

  histoPred = ROOT.TH1F(str(histoPred) ,str(histoPred),20,p['lowlimit'],p['limit'])
  cPred.Draw(p['var']+'Pred>>'+str(histonamePred),predSelection,'goff')

  histoPredUp = ROOT.TH1F(str(histoPredUp) ,str(histoPredUp),20,p['lowlimit'],p['limit'])
  cPred.Draw(p['var']+'Pred>>'+str(histonamePredUp),predSelectionUp,'goff')

  histoPredDown = ROOT.TH1F(str(histoPredDown) ,str(histoPredDown),20,p['lowlimit'],p['limit'])
  cPred.Draw(p['var']+'Pred>>'+str(histonamePredDown),predSelectionDown,'goff')

  DrawClosure(histoPred,histo,histoPredUp,histoPredDown,p['varname'])


#
# hPTLost = ROOT.TH1F('hPTLost', 'hPTLost',25,0,1000)
# cLost.Draw('ptLostTruth>>hPTLost','weightTruth*(htTruth>'+str(htCut)+'&&njetsTruth>='+str(minNJets)+'&&metTruth>'+str(metCut)+')','goff')
# hPTLostPred = ROOT.TH1F('hPTLostPred', 'hPTLostPred',25,0,1000)
# cPred.Draw('muPtLoose>>hPTLostPred','weightPred*scaleLEff*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
# hPTLostPredUp = ROOT.TH1F('hPTLostPredUp', 'hPTLostPredUp',25,0,1000)
# cPred.Draw('muPtLoose>>hPTLostPredUp','weightPred*scaleLEffUp*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
# hPTLostPredDown = ROOT.TH1F('hPTLostPredDown', 'hPTLostPredDown',25,0,1000)
# cPred.Draw('muPtLoose>>hPTLostPredDown','weightPred*scaleLEffDown*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
#
# DrawClosure(hPTLostPred,hPTLost,hPTLostPredUp,hPTLostPredDown,'PTLost')
#
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


