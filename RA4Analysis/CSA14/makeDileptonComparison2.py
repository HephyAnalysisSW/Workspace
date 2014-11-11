import ROOT
from Workspace.RA4Analysis.makeCompPlotDilep import DrawClosure
from localInfo import username

relIso=0.3
ptCut=15
deltaPhiCut = '>1' ##larger than 1
htCut     = 0
metCut    = 0
minNJets  = 3
maxPt = 1000
lostminDeltaRCut = -1

prefix = '_v26_relIso_'+str(relIso)+'_Cuts_ht'+str(htCut)+'_njets'+str(minNJets)+'_met'+str(metCut)+'minDelteR'+str(lostminDeltaRCut)+'_'
leptonID = "muIsPF&&(muIsGlobal||muIsTracker)&&muPt>"+str(ptCut)+"&&abs(muEta)<2.5"\
          +"&&abs(muDxy)<0.2&&abs(muDz)<0.5"\
          +"&&muRelIso<"+str(relIso)

#diLep_File = '/data/easilar/results2014/muonTuples/CSA14_TTJets_diLep_metCut_relIso'+str(relIso)+'.root'
#lostLep_File = '/data/easilar/results2014/muonTuples/CSA14_TTJets_Lost_metCut_relIso'+str(relIso)+'.root'

diLep_File = '/data/easilar/results2014/muonTuples/CSA14_TTJets_diLep_v26_2_relIso'+str(relIso)+'.root'
lostLep_File = '/data/easilar/results2014/muonTuples/CSA14_TTJets_Lost_v26_2_relIso'+str(relIso)+'.root'

plots = [
    {'var':'mT',           'bin':100  ,   'lowlimit':0,  'limit':800},\
    {'var':'st',           'bin':100  ,   'lowlimit':0,  'limit':1400},\
    {'var':'njets',        'bin':16  ,    'lowlimit':0,  'limit':16},\
    {'var':'nbtags',       'bin':8  ,     'lowlimit':0,  'limit':8},\
    {'var':'met',          'bin':100  ,   'lowlimit':0,  'limit':800},\
    {'var':'ht',           'bin':100  ,   'lowlimit':0,  'limit':2000},\
    {'var':'htCalc',       'bin':100  ,   'lowlimit':0,  'limit':2000},\
    {'var':'pt',           'bin':100  ,   'lowlimit':0,  'limit':800},\
    {'var':'eta',          'bin':100  ,   'lowlimit':-3,  'limit':3},\
    {'var':'lostEta',      'bin':100  ,   'lowlimit':-3,  'limit':3},\
    {'var':'deltaPhi',     'bin':100  ,   'lowlimit':0,  'limit':3.14},\
    {'var':'phi',          'bin':100  ,   'lowlimit':-4,  'limit':4},\
    {'var':'lostPhi',      'bin':100  ,   'lowlimit':-4,  'limit':4},\
    {'var':'lostPt',       'bin':100  ,   'lowlimit':0,  'limit':800},\
    {'var':'wPt',          'bin':100  ,   'lowlimit':0,  'limit':1000},\
    {'var':'hardestJetPt0', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
    {'var':'hardestJetPt1', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
    {'var':'hardestJetPt2', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
    {'var':'hardestJetPt3', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
    {'var':'hardestJetEta0', 'bin':100  ,   'lowlimit':-3,  'limit':3},\
    {'var':'hardestJetEta1', 'bin':100  ,   'lowlimit':-3,  'limit':3},\
    {'var':'hardestJetEta2', 'bin':100  ,   'lowlimit':-3,  'limit':3},\
    {'var':'hardestJetEta3', 'bin':100  ,   'lowlimit':-3,  'limit':3},\
    {'var':'hardestJetPhi0', 'bin':100  ,   'lowlimit':-4,  'limit':4},\
    {'var':'hardestJetPhi1', 'bin':100  ,   'lowlimit':-4,  'limit':4},\
    {'var':'hardestJetPhi2', 'bin':100  ,   'lowlimit':-4,  'limit':4},\
    {'var':'hardestJetPhi3', 'bin':100  ,   'lowlimit':-4,  'limit':4},\
    {'var':'hardestbJetPt0', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
    {'var':'hardestbJetPt1', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
    {'var':'hardestbJetPt2', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
    {'var':'hardestbJetPt3', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
    {'var':'minDeltaR',    'bin':100  ,   'lowlimit':0,  'limit':5},\
    {'var':'lostminDeltaR', 'bin':100  ,   'lowlimit':0,  'limit':5},\
    {'var':'relIso',       'bin':100  ,   'lowlimit':0,  'limit':0.2},\
    {'var':'lostRelIso',   'bin':100  ,   'lowlimit':0,  'limit':0.4},\
        ]


selectionT = '(lostminDeltaR>'+str(lostminDeltaRCut)+'&&lostPt<'+str(maxPt)+'&&ht>'+str(htCut)+'&&njets>='+str(minNJets)+'&&met>='+str(metCut)+')'
selectionP = '(lostminDeltaRPred>'+str(lostminDeltaRCut)+'&&lostPtPred<'+str(maxPt)+'&&htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>='+str(metCut)+')'

truthSelection = 'weight*'+selectionT 
predSelection     = 'weightPred*scaleLEff*'    +selectionP 
predSelectionUp   = 'weightPred*scaleLEffUp*'  +selectionP 
predSelectionDown = 'weightPred*scaleLEffDown*'+selectionP

cPred = ROOT.TChain('Events')
cPred.Add(diLep_File)

cLost = ROOT.TChain('Events')
cLost.Add(lostLep_File)
print 'using:', lostLep_File
for p in plots:
  histo = 'h'+p['var']
  histoPred = 'h'+p['var']+'Pred'
  histoPredUp = 'h'+p['var']+'PredUp'
  histoPredDown = 'h'+p['var']+'PredDown'
  histoname = histo
  histonamePred = histoPred
  histonamePredUp = histoPredUp
  histonamePredDown = histoPredDown

  histo = ROOT.TH1F(str(histo) ,str(histo),p['bin'],p['lowlimit'],p['limit'])
  cLost.Draw(p['var']+'>>'+str(histoname),truthSelection,'goff')
  histoPred = ROOT.TH1F(str(histoPred) ,str(histoPred),p['bin'],p['lowlimit'],p['limit'])
  cPred.Draw(p['var']+'Pred>>'+str(histonamePred),predSelection,'goff')
  histoPredUp = ROOT.TH1F(str(histoPredUp) ,str(histoPredUp),p['bin'],p['lowlimit'],p['limit'])
  cPred.Draw(p['var']+'Pred>>'+str(histonamePredUp),predSelectionUp,'goff')
  histoPredDown = ROOT.TH1F(str(histoPredDown) ,str(histoPredDown),p['bin'],p['lowlimit'],p['limit'])
  cPred.Draw(p['var']+'Pred>>'+str(histonamePredDown),predSelectionDown,'goff')

  path = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/pngCSA14/ClosureTest/'+prefix+p['var']+'.png'
  DrawClosure(histoPred,histo,histoPredUp,histoPredDown,p['var'],path)

##For met ###
hmetStat = ROOT.TH1F('hmetStat', 'hmetStat',100,0,800)
cLost.Draw('met>>hmetStat',truthSelection,'goff')
hmetPredStat = ROOT.TH1F('hmetPredStat', 'hmetPredStat',100,0,800)
cPred.Draw('met>>hmetPredStat',predSelection,'goff')
hmetPredUpStat = ROOT.TH1F('hmetPredUpStat', 'hmetPredUpStat',100,0,800)
cPred.Draw('met>>hmetPredUpStat',predSelectionUp,'goff')
hmetPredDownStat = ROOT.TH1F('hmetPredDownStat', 'hmetPredDownStat',100,0,800)
cPred.Draw('met>>hmetPredDownStat',predSelectionDown,'goff')

path = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/pngCSA14/ClosureTest/'+prefix+'metVsmet.png'
DrawClosure(hmetPredStat,hmetStat,hmetPredUpStat,hmetPredDownStat,'metVsmet',path)

##For ht ###
hhtStat = ROOT.TH1F('hhtStat', 'hhtStat',1000,0,2000)
cLost.Draw('ht>>hhtStat',truthSelection,'goff')
hhtPredStat = ROOT.TH1F('hhtPredStat', 'hhtPredStat',1000,0,2000)
cPred.Draw('ht>>hhtPredStat',predSelection,'goff')
hhtPredUpStat = ROOT.TH1F('hhtPredUpStat', 'hhtPredUpStat',1000,0,2000)
cPred.Draw('ht>>hhtPredUpStat',predSelectionUp,'goff')
hhtPredDownStat = ROOT.TH1F('hhtPredDownStat', 'hhtPredDownStat',1000,0,2000)
cPred.Draw('ht>>hhtPredDownStat',predSelectionDown,'goff')

path = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/pngCSA14/ClosureTest/'+prefix+'htVsht.png'
DrawClosure(hhtPredStat,hhtStat,hhtPredUpStat,hhtPredDownStat,'htVsht',path)

###For njets ###
hnjetsStat = ROOT.TH1F('hnjetsStat', 'hnjetsStat',16,0,16)
cLost.Draw('njets>>hnjetsStat',truthSelection,'goff')
hnjetsPredStat = ROOT.TH1F('hnjetsPredStat', 'hnjetsPredStat',16,0,16)
cPred.Draw('njets>>hnjetsPredStat',predSelection,'goff')
hnjetsPredUpStat = ROOT.TH1F('hnjetsPredUpStat', 'hnjetsPredUpStat',16,0,16)
cPred.Draw('njets>>hnjetsPredUpStat',predSelectionUp,'goff')
hnjetsPredDownStat = ROOT.TH1F('hnjetsPredDownStat', 'hnjetsPredDownStat',16,0,16)
cPred.Draw('njets>>hnjetsPredDownStat',predSelectionDown,'goff')

path = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/pngCSA14/ClosureTest/'+prefix+'njetsVsnjets.png'
DrawClosure(hnjetsPredStat,hnjetsStat,hnjetsPredUpStat,hnjetsPredDownStat,'njetsVsnjets',path)



##For Statistics##
hDeltaPhiStat = ROOT.TH1F('hDeltaPhiStat', 'hDeltaPhiStat',20,0,3.14)
hDeltaPhiStat.Sumw2() 
cLost.Draw('deltaPhi>>hDeltaPhiStat','weight*(deltaPhi'+deltaPhiCut+'&&ht>'+str(htCut)+'&&njets>='+str(minNJets)+'&&met>'+str(metCut)+')','goff')
hDeltaPhiPredStat = ROOT.TH1F('hDeltaPhiPredStat', 'hDeltaPhiPredStat',20,0,3.14)
hDeltaPhiPredStat.Sumw2()
cPred.Draw('deltaPhiPred>>hDeltaPhiPredStat','weightPred*scaleLEff*(deltaPhiPred'+deltaPhiCut+'&&htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hDeltaPhiPredUpStat = ROOT.TH1F('hDeltaPhiPredUpStat', 'hDeltaPhiPredUpStat',20,0,3.14)
hDeltaPhiPredUpStat.Sumw2()
cPred.Draw('deltaPhiPred>>hDeltaPhiPredUpStat','weightPred*scaleLEffUp*(deltaPhiPred'+deltaPhiCut+'&&htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

ePred = ROOT.Double()
eTruth = ROOT.Double()
predYield = hDeltaPhiPredStat.IntegralAndError(0,hDeltaPhiPredStat.GetNbinsX(),ePred)
truthYield = hDeltaPhiStat.IntegralAndError(0,hDeltaPhiStat.GetNbinsX(),eTruth)

print '\documentclass{article}\usepackage[english]{babel}\\begin{document}\\begin{center}\\begin{tabular}{| l | l | l | l |}\hline'
print ' Lost Lep ($ \\triangle\phi>1$ and njet>=3) &Prediction & Truth  \\\ \hline'
print 'ht$>$',htCut ,'and met$>$',metCut,' & $',format(predYield, '.2f'),'\pm',format(ePred, '.2f'),'(Stat)\pm',format(abs(hDeltaPhiPredUpStat.Integral()-predYield),'.2f'),'(\%10Leff)$ & $',format(truthYield,'.2f'),'\pm',format(eTruth,'.2f'),'(Stat)$ \\\ \hline '
print '\end{tabular}\end{center}\end{document}'




