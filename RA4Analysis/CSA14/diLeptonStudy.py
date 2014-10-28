import ROOT
from Workspace.RA4Analysis.stage2Tuples import ttJetsCSA1450ns
from localInfo import username
from objectSelection import tightPOGMuID , vetoMuID , getLooseMuStage2
from math import sqrt, cos, sin, atan2
from array import array
from getmuon import getMu , getGenLep
from Workspace.RA4Analysis.helpers import deltaPhi
ROOT.gROOT.Reset()

small = False
Lumi=2000 #pb-1
xsec=689.1 #pb ?
#nevents is later

c50 = ROOT.TChain('Events')
#for b in ttJetsCSA1450ns['bins']:
#  c50.Add(ttJetsCSA1450ns['dirname']+'/'+b+'/histo_ttJetsCSA1450ns_from*.root')
c50.Add('/data/schoef/convertedTuples_v24/copyInc/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*')
#c50.Add('/data/schoef/convertedTuples_v25/copyMET/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*')
#c50.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from0To10.root')
#c50.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/*')
#c50.Add('/data/schoef/convertedTuples_v25/copyMET/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*.root')
#number_events50 = c50.GetEntries()
#c50.Add('/data/schoef/convertedTuples_v24/copyMET/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*')
#weight = Lumi*xsec/number_events50
#weight = 0.436738650483
scale = 0.9
relIso = 0.3
metCut = 150
htCut = 150
njets = 3
deltaPhiCut = 0
preselection = "ht>"+str(htCut)+" && njets>="+str(njets)# && nbtags==0"
selection1="&&ngNuMuFromW==2&&ngNuEFromW==0"  ###gLepCount==2 always !checked!

c50.Draw(">>List",preselection+selection1)
List = ROOT.gDirectory.Get("List")
number_events = List.GetN()
#print 'number of events:', number_events
if small:
  number_events = min(number_events, 100)

Filetake = ROOT.TFile('/data/easilar/results2014/rootfiles/Eff03.root')
File = ROOT.TFile('/data/easilar/results2014/rootfiles/DiLepEff'+str(scale)+'ht'+str(htCut)+'met150njet3.root','RECREATE')
#File = ROOT.TFile('delete.root','RECREATE')
File.cd()
  #File = ROOT.TFile('/data/easilar/results2014/rootfiles/DiLepEff'+str(scale)+'ht'+str(htCut)+'_met'+str(metCut)+'njet3.root','RECREATE')
h_GenPt = ROOT.TH1F('h_GenPt', 'h_GenPt',25,0,800)
h_genMet = ROOT.TH1F('h_genMet', 'h_genMet',25,0,800)
h_GenMt = ROOT.TH1F('h_GenMt', 'h_GenMt',25,0,800)
h_GenDeltaPhi = ROOT.TH1F('h_GenDeltaPhi', 'h_GenDeltaPhi',25,0,3.14)
#h_GenDeltaPhi.Sumw2() 
h_Pt = ROOT.TH1F('h_Pt', 'h_Pt',25,0,800)
h_Met = ROOT.TH1F('h_Met', 'h_Met',25,0,800)
h_MtPred = ROOT.TH1F('h_MtPred', 'h_MtPred',25,0,800)
h_HtTruth = ROOT.TH1F('h_HtTruth', 'h_HtTruth',25,0,2000)
h_DeltaPhi = ROOT.TH1F('h_DeltaPhi', 'h_DeltaPhi',25,0,3.14)
#h_DeltaPhi.Sumw2()

h_GenPtLost = ROOT.TH1F('h_GenPtLost', 'h_GenPtLost',25,0,800)
h_PtLost = ROOT.TH1F('h_PtLost', 'h_PtLost',25,0,800)
h_PtLostNoReWeight = ROOT.TH1F('h_PtLostNoReWeight', 'h_PtLostNoReWeight',25,0,800)
h_Truthnjet = ROOT.TH1F('h_Truthnjet', 'h_Truthnjet',20,0,20)
h_TruthMuPhi = ROOT.TH1F('h_TruthMuPhi', 'h_TruthMuPhi',25,-5,5) 
h_metPhi = ROOT.TH1F('h_metPhi', 'h_metPhi',25,-5,5)
h_Phi = ROOT.TH1F('h_Phi', 'h_Phi',25,-5,5)
h_metPhiPred = ROOT.TH1F('h_metPhiPred', 'h_metPhiPred',25,-5,5)
h_MetDeltaPhiComp = ROOT.TH2F('h_MetDeltaPhiComp', 'h_MetDeltaPhiComp',100,-5,5,100,0,1800)
h_Ht= ROOT.TH1F('h_Ht', 'h_Ht',25,0,2000)
h_njets = ROOT.TH1F('h_njets', 'h_njets',20,0,20)
h_EffDiLep = ROOT.TH1F('h_EffDiLEp', 'h_EffDiLep',100,0,1)
h_EffLostLep = ROOT.TH1F('h_EffLostLEp', 'h_EffLostLep',100,0,1)
#for relIso in [0.12,0.2,0.3]:
#for scale in [1]:
print scale
h_EffinDiLep = Filetake.Get("2D"+str(relIso)) #Finding eff in DiLep Events
#print 'For relIso:',"2D"+str(relIso)
for i in range(number_events):
  weight = c50.GetLeaf('weight').GetValue()
  c50.GetEntry(List.GetEntry(i))
  #print i,'/',number_events
  nmuCount = int(c50.GetLeaf('nmuCount').GetValue())
  ngoodMuons = c50.GetLeaf('ngoodMuons').GetValue()
  nvetoMuons = c50.GetLeaf('nvetoMuons').GetValue()
  nvetoElectrons = c50.GetLeaf('nvetoElectrons').GetValue()
  njets = c50.GetLeaf('njets').GetValue()
  met = c50.GetLeaf('met').GetValue()
  genMet = c50.GetLeaf('genMet').GetValue()
  ht = c50.GetLeaf('ht').GetValue()
  metPhi = c50.GetLeaf('metphi').GetValue()
  genMetPhi = c50.GetLeaf('genMetPhi').GetValue()
  gLepCount = c50.GetLeaf('ngLep').GetValue()
  ngNuMuFromW = c50.GetLeaf('ngNuMuFromW').GetValue() 
  ngNuEFromW = c50.GetLeaf('ngNuEFromW').GetValue()
  ntmuons=0
  nlmuons=0
  muons=[]
  gLeps=[]
  #Get all genLeps
  for p in range(int(gLepCount)):
    genLep = getGenLep(c50,p)
    if genLep:
      gLeps.append(genLep)  
  for j in range(nmuCount):
    muon=getMu(c50,j)
    #muon=getLooseMuStage2(c50,j)
    if muon:
      isTight=tightPOGMuID(muon)
      isLoose=vetoMuID(muon,relIso)
      muon['isTight'] = isTight
      muon['isLoose'] = isLoose
      if isTight: ntmuons+=1
      if isLoose: nlmuons+=1
      hasMatch = False
      for gl in gLeps:
        if gl['gLepInd']==j and gl['gLepDR']<0.4: hasMatch=True
      muon['hasMatch']=hasMatch  
      muons.append(muon)
  #print 'nmuons:', len(muons)
  if met>metCut:
    lostGenLeps = filter(lambda gl:not(gl['gLepInd']>=0 and gl['gLepDR']<0.4) and gl['gLepPt']>15 and abs(gl['gLepEta'])<2.5, gLeps)
    lostnotloose = filter(lambda x:x['hasMatch'] and (not(x['isLoose'])), muons)
    tightMatchedMuons = filter(lambda x:x['hasMatch'] and x['isTight'], muons)
    #print 'number of lost muons because no reconstruction at all:',len(lostGenLeps)
    #print 'number of lost muons because there is reconstruction but the recomuons are not loose at all:', len(lostnotloose)
    nLostMuons = len(lostGenLeps) + len(lostnotloose) 
    #print 'nLostMuons:', nLostMuons
    if len(muons)==2 or len(muons)==1:
      if nlmuons==1 and ntmuons==1:
        if len(tightMatchedMuons)==1 and nLostMuons==1:
          if len(lostGenLeps)==1:
            lostGenMuon = lostGenLeps[0]
            h_GenPtLost.Fill(lostGenMuon['gLepPt'],weight)
          if len(lostnotloose)==1:
            lostGenMuon = lostnotloose[0]
            h_GenPtLost.Fill(lostGenMuon['pt'],weight)            
          if len(tightMatchedMuons) >1 : print "Warning"
          TightMatchedMuon = tightMatchedMuons[0]
          Mt = sqrt(2*met*TightMatchedMuon['pt']*(1-cos(TightMatchedMuon['phi']-metPhi)))
          Wx = met*cos(metPhi) + TightMatchedMuon['pt']*cos(TightMatchedMuon['phi'])
          Wy = met*sin(metPhi) + TightMatchedMuon['pt']*sin(TightMatchedMuon['phi'])
          WPhi = atan2(Wy,Wx)
          WPt = sqrt((Wx)**2+(Wy)**2)
          St = sqrt((WPt)**2+(Mt)**2) 
          #print 'St truth: ', St
          if deltaPhi(TightMatchedMuon['phi'],WPhi) >deltaPhiCut:# and St< 350:
            #h_GenDeltaPhi.Fill(cos(TightMatchedMuon['phi']-metPhi), weight)
            #print 'truth cos deltaphi:', cos(TightMatchedMuon['phi']-WPhi)
            h_HtTruth.Fill(ht,weight)
            h_Truthnjet.Fill(njets,weight)
            h_GenMt.Fill(Mt, weight)
            h_genMet.Fill(met, weight)
            h_GenPt.Fill(TightMatchedMuon['pt'], weight)
            h_TruthMuPhi.Fill(TightMatchedMuon['phi'],weight)
            h_metPhi.Fill(metPhi,weight)
            h_GenDeltaPhi.Fill(deltaPhi(TightMatchedMuon['phi'],WPhi), weight)
            h_MetDeltaPhiComp.Fill(TightMatchedMuon['phi']-metPhi,met)      
  if len(muons)<2: continue
  if len(muons)==2 and ntmuons>=1:
    #print 'tight muons:', ntmuons, 'loose muons:',nlmuons
    for perm in [muons, reversed(muons)]:
      m,m2 = perm
      if m2['isTight']==1:
        EffDiLepf = h_EffinDiLep.GetBinContent(h_EffinDiLep.FindBin(m['pt'],m['eta']))
        if EffDiLepf > 0.5 :
          if scale == 1: EffDiLep = EffDiLepf
          if scale == 1.1: EffDiLep = max((EffDiLepf*1.1)-0.1,0)
          if scale== 0.9:EffDiLep = min((EffDiLepf*0.9)+0.1,1)
          #print 'Eff: ', EffDiLep
          #h_EffDiLep.Fill(EffDiLep)
          #print 'm muon pt:', m['pt'], 'eta:',m['eta'] , 'phi:',m['phi'],'eff of muon:', EffDiLep
          #print 'm2 muon pt:',m2['pt'], 'eta:',m2['eta'] , 'phi:',m2['phi']
          metAdd=m['pt']
          Metx = met*cos(metPhi)+cos(m['phi'])*metAdd
          Mety = met*sin(metPhi)+sin(m['phi'])*metAdd
          WxPred= Metx+cos(m2['phi'])*m2['pt']
          WyPred= Mety+sin(m2['phi'])*m2['pt']
          WPhiPred = atan2(WyPred,WxPred)
          metPred = sqrt(Metx**2+Mety**2)
          metPhiPred = atan2(Mety,Metx)
          mtPred = sqrt(2*metPred*m2['pt']*(1-cos(m2['phi']-metPhiPred)))
          WPtPred = sqrt((WxPred)**2+(WyPred)**2) 
          StPred = sqrt((WPtPred)**2+(mtPred)**2) 
          #print 'StPred:' , StPred
          if metPred > metCut and deltaPhi(m2['phi'],WPhiPred)>deltaPhiCut:#StPred >250: #and StPred<350: ##metPred >150:
            h_PtLostNoReWeight.Fill(m['pt'],weight)
            if EffDiLep !=0: Seff = (1-EffDiLep)/EffDiLep
            if EffDiLep ==0: Seff = EffDiLep
            if Seff > 5 : print 'EffDiLep:',EffDiLep ,'Scale factor:', Seff
            #Seff =  (1-EffDiLep)/(EffDiLep)
            h_MtPred.Fill(mtPred,weight*Seff)
            h_Met.Fill(metPred,weight*Seff)
            h_Pt.Fill(m2['pt'],weight*Seff)
            h_Phi.Fill(m2['phi'],weight*Seff)
            h_metPhiPred.Fill(metPhiPred,weight*Seff) 
            #print 'pred cos deltaphi:', cos(m2['phi']-WPhiPred)
            #h_DeltaPhi.Fill(cos(m2['phi']-metPhiPred),weight*Seff)
            h_DeltaPhi.Fill(deltaPhi(m2['phi'],WPhiPred),weight*Seff)
            h_PtLost.Fill(m['pt'],weight*Seff)
            h_Ht.Fill(ht,weight*Seff)
            h_njets.Fill(njets,weight*Seff)
ePred = ROOT.Double()
eTruth = ROOT.Double() 
print 'Prediction yield:', h_DeltaPhi.IntegralAndError(0,h_DeltaPhi.GetNbinsX(),ePred)
print 'Truth yield:', h_GenDeltaPhi.IntegralAndError(0,h_GenDeltaPhi.GetNbinsX(),eTruth)
print 'ePred :', ePred
print 'eTruth:', eTruth

File.Write()
File.Close()


