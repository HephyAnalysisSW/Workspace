import ROOT
from Workspace.RA4Analysis.makeCompPlotDilep import DrawClosure
from localInfo import username

relIso=0.3
ptCut=15
deltaPhiCut = '>1' ##larger than 1
htCut     = 0
metCut    = 0
minNJets  = 0
maxPt = 1000
lostminDeltaRCut = -1
leptonID = "muIsPF&&(muIsGlobal||muIsTracker)&&muPt>"+str(ptCut)+"&&abs(muEta)<2.5"\
          +"&&abs(muDxy)<0.2&&abs(muDz)<0.5"\
          +"&&muRelIso<"+str(relIso)

#diLep_File = '/data/easilar/results2014/muonTuples/CSA14_TTJets_diLep_metCut_relIso'+str(relIso)+'.root'
#lostLep_File = '/data/easilar/results2014/muonTuples/CSA14_TTJets_Lost_metCut_relIso'+str(relIso)+'.root'

diLep_File = '/data/easilar/results2014/muonTuples/CSA14_TTJets_diLep_v26_4_relIso'+str(relIso)+'.root'
#lostLep_File = '/data/easilar/results2014/muonTuples/CSA14_TTJets_Lost_v26_looseMatchedMuons_relIso'+str(relIso)+'.root'
lostLep_File = '/data/easilar/results2014/muonTuples/CSA14_TTJets_Lost_v26_relIso'+str(relIso)+'.root'


plots = [
    {'var':'mT',           'bin':100  ,   'lowlimit':0,  'limit':800},\
    {'var':'st',           'bin':100  ,   'lowlimit':0,  'limit':1400},\
    {'var':'njets',        'bin':16  ,    'lowlimit':0,  'limit':16},\
    {'var':'nbtags',       'bin':8  ,     'lowlimit':0,  'limit':8},\
    {'var':'met',          'bin':100  ,   'lowlimit':0,  'limit':800},\
    {'var':'ht',           'bin':100  ,   'lowlimit':0,  'limit':2000},\
    {'var':'pt',           'bin':100  ,   'lowlimit':0,  'limit':800},\
    {'var':'eta',          'bin':100  ,   'lowlimit':-3,  'limit':3},\
    {'var':'lostEta',      'bin':100  ,   'lowlimit':-3,  'limit':3},\
    {'var':'deltaPhi',     'bin':100  ,   'lowlimit':0,  'limit':3.14},\
    {'var':'phi',          'bin':100  ,   'lowlimit':-4,  'limit':4},\
    {'var':'lostPhi',      'bin':100  ,   'lowlimit':-4,  'limit':4},\
    {'var':'lostPt',       'bin':100  ,   'lowlimit':0,  'limit':800},\
    {'var':'wPt',          'bin':100  ,   'lowlimit':0,  'limit':1000},\
    {'var':'relIso',       'bin':100  ,   'lowlimit':0,  'limit':0.2},\
    {'var':'lostRelIso',   'bin':100  ,   'lowlimit':0,  'limit':0.4},\
        ]
minDeltaRplots = [
    {'var':'mindeltaRBM',        'bin':100  ,   'lowlimit':0,  'limit':10},\
    {'var':'mindeltaRBL',        'bin':100  ,   'lowlimit':0,  'limit':10},\
    {'var':'mindeltaRNonBM',     'bin':100  ,   'lowlimit':0,  'limit':10},\
    {'var':'mindeltaRNonBL',     'bin':100  ,   'lowlimit':0,  'limit':10},\
    {'var':'minlostdeltaRBM',    'bin':100  ,   'lowlimit':0,  'limit':10},\
    {'var':'minlostdeltaRBL',    'bin':100  ,   'lowlimit':0,  'limit':10},\
    {'var':'minlostdeltaRNonBM', 'bin':100  ,   'lowlimit':0,  'limit':10},\
    {'var':'minlostdeltaRNonBL', 'bin':100  ,   'lowlimit':0,  'limit':10},\
]
jetPlots = [
  {'var':'jetPt[0]', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
 # {'var':'jetPt[1]', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
 # {'var':'jetPt[2]', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
 # {'var':'jetPt[3]', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
  {'var':'jetEta[0]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'jetEta[1]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'jetEta[2]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'jetEta[3]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
  {'var':'jetPhi[0]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'jetPhi[1]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'jetPhi[2]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'jetPhi[3]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
  {'var':'jetPdg[0]', 'bin':100  ,   'lowlimit':-6,  'limit':30},\
 # {'var':'jetPdg[1]', 'bin':100  ,   'lowlimit':-6,  'limit':30},\
 # {'var':'jetPdg[2]', 'bin':100  ,   'lowlimit':-6,  'limit':30},\
 # {'var':'jetPdg[3]', 'bin':100  ,   'lowlimit':-6,  'limit':30},\
  {'var':'bJetCSVMPt[0]', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
 # {'var':'bJetCSVMPt[1]', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
 # {'var':'bJetCSVMPt[2]', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
 # {'var':'bJetCSVMPt[3]', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
  {'var':'bJetCSVLPt[0]', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
 # {'var':'bJetCSVLPt[1]', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
 # {'var':'bJetCSVLPt[2]', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
 # {'var':'bJetCSVLPt[3]', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
  {'var':'bJetCSVMPhi[0]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'bJetCSVMPhi[1]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'bJetCSVMPhi[2]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'bJetCSVMPhi[3]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
  {'var':'bJetCSVLPhi[0]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'bJetCSVLPhi[1]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'bJetCSVLPhi[2]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'bJetCSVLPhi[3]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
  {'var':'bJetCSVMEta[0]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'bJetCSVMEta[1]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'bJetCSVMEta[2]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'bJetCSVMEta[3]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
  {'var':'bJetCSVLEta[0]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'bJetCSVLEta[1]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'bJetCSVLEta[2]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'bJetCSVLEta[3]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
  {'var':'nonbJetCSVMPt[0]', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
 # {'var':'nonbJetCSVMPt[1]', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
 # {'var':'nonbJetCSVMPt[2]', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
 # {'var':'nonbJetCSVMPt[3]', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
  {'var':'nonbJetCSVLPt[0]', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
 # {'var':'nonbJetCSVLPt[1]', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
 # {'var':'nonbJetCSVLPt[2]', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
 # {'var':'nonbJetCSVLPt[3]', 'bin':100  ,   'lowlimit':0,  'limit':1000},\
  {'var':'nonbJetCSVMPhi[0]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'nonbJetCSVMPhi[1]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'nonbJetCSVMPhi[2]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'nonbJetCSVMPhi[3]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
  {'var':'nonbJetCSVLPhi[0]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'nonbJetCSVLPhi[1]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'nonbJetCSVLPhi[2]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'nonbJetCSVLPhi[3]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
  {'var':'nonbJetCSVMEta[0]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'nonbJetCSVMEta[1]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'nonbJetCSVMEta[2]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'nonbJetCSVMEta[3]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
  {'var':'nonbJetCSVLEta[0]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'nonbJetCSVLEta[1]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'nonbJetCSVLEta[2]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
 # {'var':'nonbJetCSVLEta[3]', 'bin':100  ,   'lowlimit':-5,  'limit':5},\
]

cPred = ROOT.TChain('Events')
cPred.Add(diLep_File)
print 'using:' , diLep_File                             
cLost = ROOT.TChain('Events')
cLost.Add(lostLep_File)
print 'using:', lostLep_File


variables = plots
#variables = minDeltaRplots
#variables = jetPlots

selectionT = '(minlostdeltaRBL>'+str(lostminDeltaRCut)+'&&minlostdeltaRNonBL>'+str(lostminDeltaRCut)+'&&lostPt<'+str(maxPt)+'&&ht>'+str(htCut)+'&&njets>='+str(minNJets)+'&&met>='+str(metCut)+')'
selectionP = '(minlostdeltaRBL>'+str(lostminDeltaRCut)+'&&minlostdeltaRNonBL>'+str(lostminDeltaRCut)+'&&lostPt<'+str(maxPt)+'&&htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>='+str(metCut)+')'

pdgIdCut = [0,1,2,3,4,5,21]

#for c in pdgIdCut:
#  print c
#  prefix = '_MatchedLoose_PdgID_'+str(c)+'relIso_'+str(relIso)+'_Cuts_ht'+str(htCut)+'_njets'+str(minNJets)+'_met'+str(metCut)+'minDelteR'+str(lostminDeltaRCut)+'_'
prefix = 'relIso_'+str(relIso)+'_Cuts_ht'+str(htCut)+'_njets'+str(minNJets)+'_met'+str(metCut)+'__'
# selectionT = '(abs(jetPdg[0])=='+str(c)+'&&lostPt<'+str(maxPt)+'&&ht>'+str(htCut)+'&&njets>='+str(minNJets)+'&&met>='+str(metCut)+')'
# selectionP = '(abs(jetPdg[0])=='+str(c)+'&&lostPt<'+str(maxPt)+'&&htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>='+str(metCut)+')'

truthSelection = 'weight*'+selectionT 
predSelection1     = 'weight*scaleLEff*'    +selectionT 
predSelectionUp1   = 'weight*scaleLEffUp*'  +selectionT 
predSelectionDown1 = 'weight*scaleLEffDown*'+selectionT

predSelection     = 'weight*scaleLEff*'    +selectionP 
predSelectionUp   = 'weight*scaleLEffUp*'  +selectionP 
predSelectionDown = 'weight*scaleLEffDown*'+selectionP

for p in variables:
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
  cPred.Draw(p['var']+'>>'+str(histonamePred),predSelection1,'goff')
  histoPredUp = ROOT.TH1F(str(histoPredUp) ,str(histoPredUp),p['bin'],p['lowlimit'],p['limit'])
  cPred.Draw(p['var']+'>>'+str(histonamePredUp),predSelectionUp1,'goff')
  histoPredDown = ROOT.TH1F(str(histoPredDown) ,str(histoPredDown),p['bin'],p['lowlimit'],p['limit'])
  cPred.Draw(p['var']+'>>'+str(histonamePredDown),predSelectionDown1,'goff')

  path = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/pngCSA14/ClosureTest/noDeltaRCut/'+prefix+p['var']+'.png'
  DrawClosure(histoPred,histo,histoPredUp,histoPredDown,p['var'],path)

##For met ###
hmetStat = ROOT.TH1F('hmetStat', 'hmetStat',100,0,800)
cLost.Draw('met>>hmetStat',truthSelection,'goff')
hmetPredStat = ROOT.TH1F('hmetPredStat', 'hmetPredStat',100,0,800)
cPred.Draw('metPred>>hmetPredStat',predSelection,'goff')
hmetPredUpStat = ROOT.TH1F('hmetPredUpStat', 'hmetPredUpStat',100,0,800)
cPred.Draw('metPred>>hmetPredUpStat',predSelectionUp,'goff')
hmetPredDownStat = ROOT.TH1F('hmetPredDownStat', 'hmetPredDownStat',100,0,800)
cPred.Draw('metPred>>hmetPredDownStat',predSelectionDown,'goff')

path = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/pngCSA14/ClosureTest/noDeltaRCut/'+prefix+'Correctedmet.png'
DrawClosure(hmetPredStat,hmetStat,hmetPredUpStat,hmetPredDownStat,'Corrected Met',path)

##For ht ###
hhtStat = ROOT.TH1F('hhtStat', 'hhtStat',100,0,2000)
cLost.Draw('ht>>hhtStat',truthSelection,'goff')
hhtPredStat = ROOT.TH1F('hhtPredStat', 'hhtPredStat',100,0,2000)
cPred.Draw('htPred>>hhtPredStat',predSelection,'goff')
hhtPredUpStat = ROOT.TH1F('hhtPredUpStat', 'hhtPredUpStat',100,0,2000)
cPred.Draw('htPred>>hhtPredUpStat',predSelectionUp,'goff')
hhtPredDownStat = ROOT.TH1F('hhtPredDownStat', 'hhtPredDownStat',100,0,2000)
cPred.Draw('htPred>>hhtPredDownStat',predSelectionDown,'goff')

path = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/pngCSA14/ClosureTest/noDeltaRCut/'+prefix+'Correctedht.png'
DrawClosure(hhtPredStat,hhtStat,hhtPredUpStat,hhtPredDownStat,'Corrected Ht',path)

###For njets ###
hnjetsStat = ROOT.TH1F('hnjetsStat', 'hnjetsStat',16,0,16)
cLost.Draw('njets>>hnjetsStat',truthSelection,'goff')
hnjetsPredStat = ROOT.TH1F('hnjetsPredStat', 'hnjetsPredStat',16,0,16)
cPred.Draw('njetsPred>>hnjetsPredStat',predSelection,'goff')
hnjetsPredUpStat = ROOT.TH1F('hnjetsPredUpStat', 'hnjetsPredUpStat',16,0,16)
cPred.Draw('njetsPred>>hnjetsPredUpStat',predSelectionUp,'goff')
hnjetsPredDownStat = ROOT.TH1F('hnjetsPredDownStat', 'hnjetsPredDownStat',16,0,16)
cPred.Draw('njetsPred>>hnjetsPredDownStat',predSelectionDown,'goff')

path = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/pngCSA14/ClosureTest/noDeltaRCut/'+prefix+'Correctednjets.png'
DrawClosure(hnjetsPredStat,hnjetsStat,hnjetsPredUpStat,hnjetsPredDownStat,'Corrected Njets',path)



##For Statistics##
hDeltaPhiStat = ROOT.TH1F('hDeltaPhiStat', 'hDeltaPhiStat',20,0,3.14)
hDeltaPhiStat.Sumw2() 
cLost.Draw('deltaPhi>>hDeltaPhiStat','weight*(deltaPhi'+deltaPhiCut+'&&ht>'+str(htCut)+'&&njets>='+str(minNJets)+'&&met>'+str(metCut)+')','goff')
hDeltaPhiPredStat = ROOT.TH1F('hDeltaPhiPredStat', 'hDeltaPhiPredStat',20,0,3.14)
hDeltaPhiPredStat.Sumw2()
cPred.Draw('deltaPhi>>hDeltaPhiPredStat','weight*scaleLEff*(deltaPhi'+deltaPhiCut+'&&htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hDeltaPhiPredUpStat = ROOT.TH1F('hDeltaPhiPredUpStat', 'hDeltaPhiPredUpStat',20,0,3.14)
hDeltaPhiPredUpStat.Sumw2()
cPred.Draw('deltaPhi>>hDeltaPhiPredUpStat','weight*scaleLEffUp*(deltaPhi'+deltaPhiCut+'&&htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

ePred = ROOT.Double()
eTruth = ROOT.Double()
predYield = hDeltaPhiPredStat.IntegralAndError(0,hDeltaPhiPredStat.GetNbinsX(),ePred)
truthYield = hDeltaPhiStat.IntegralAndError(0,hDeltaPhiStat.GetNbinsX(),eTruth)

print '\documentclass{article}\usepackage[english]{babel}\\begin{document}\\begin{center}\\begin{tabular}{| l | l | l | l |}\hline'
print ' Lost Lep ($ \\triangle\phi>1$ and njet>=3) &Prediction & Truth  \\\ \hline'
print 'ht$>$',htCut ,'and met$>$',metCut,' & $',format(predYield, '.2f'),'\pm',format(ePred, '.2f'),'(Stat)\pm',format(abs(hDeltaPhiPredUpStat.Integral()-predYield),'.2f'),'(\%10Leff)$ & $',format(truthYield,'.2f'),'\pm',format(eTruth,'.2f'),'(Stat)$ \\\ \hline '
print '\end{tabular}\end{center}\end{document}'




