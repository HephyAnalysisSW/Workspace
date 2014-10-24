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
#c50.Add('/data/schoef/convertedTuples_v25/copyMET/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*')
#c50.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from0To10.root')
#c50.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/*')
#c50.Add('/data/schoef/convertedTuples_v25/copyMET/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*.root')
#number_events50 = c50.GetEntries()
c50.Add('/data/schoef/convertedTuples_v24/copyMET/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*')
#weight = Lumi*xsec/number_events50
#weight = 0.436738650483
preselection = "ht>150 && njets>=3"
selection1="&&ngNuMuFromW==2&&ngNuEFromW==0"  ###ngLep==2 always !checked!
selection2="&&(nmuCount==2||nmuCount==1)"

c50.Draw(">>List",preselection+selection1)
List = ROOT.gDirectory.Get("List")
number_events = List.GetN()
print 'number of events:', number_events
if small:
  number_events = min(number_events, 100)

Filetake = ROOT.TFile('../rootfiles/Eff03.root')
File = ROOT.TFile('../rootfiles/Mt03.root','RECREATE')

h_GenPt = ROOT.TH1F('h_GenPt', 'h_GenPt',25,0,800)
h_GenMet = ROOT.TH1F('h_GenMet', 'h_GenMet',25,0,800)
h_GenMt = ROOT.TH1F('h_GenMt', 'h_GenMt',25,0,800)
h_GenDeltaPhi = ROOT.TH1F('h_GenDeltaPhi', 'h_GenDeltaPhi',20,0,5)

h_Pt = ROOT.TH1F('h_Pt', 'h_Pt',25,0,800)
h_Met = ROOT.TH1F('h_Met', 'h_Met',25,0,800)
h_MtPred = ROOT.TH1F('h_MtPred', 'h_MtPred',25,0,800)
h_DeltaPhi = ROOT.TH1F('h_DeltaPhi', 'h_DeltaPhi',20,0,5)

h_GenPtLost = ROOT.TH1F('h_GenPtLost', 'h_GenPtLost',25,0,800)
h_PtLost = ROOT.TH1F('h_PtLost', 'h_PtLost',25,0,800)
h_PtLostNoReWeight = ROOT.TH1F('h_PtLostNoReWeight', 'h_PtLostNoReWeight',25,0,800)

h_TruthMuPhi = ROOT.TH1F('h_TruthMuPhi', 'h_TruthMuPhi',25,-5,5) 
h_MetPhi = ROOT.TH1F('h_MetPhi', 'h_MetPhi',25,-5,5)
h_Phi = ROOT.TH1F('h_Phi', 'h_Phi',25,-5,5)
h_MetPhiPred = ROOT.TH1F('h_MetPhiPred', 'h_MetPhiPred',25,-5,5)
h_MetDeltaPhiComp = ROOT.TH2F('h_MetDeltaPhiComp', 'h_MetDeltaPhiComp',100,-5,5,100,0,1800)
h_Ht= ROOT.TH1F('h_Ht', 'h_Ht',100,0,1000)
h_njets = ROOT.TH1F('h_njets', 'h_njets',25,0,10)
h_EffDiLep = ROOT.TH1F('h_EffDiLEp', 'h_EffDiLep',100,0,1)
h_EffLostLep = ROOT.TH1F('h_EffLostLEp', 'h_EffLostLep',100,0,1)

#for relIso in [0.12,0.2,0.3]:
for relIso in [0.3]:
  h_EffinDiLep = Filetake.Get("2D"+str(relIso)) #Finding eff in DiLep Events
  #print 'For relIso:',"2D"+str(relIso)
  for i in range(number_events):
    weight = c50.GetLeaf('weight').GetValue()
    c50.GetEntry(List.GetEntry(i))
    print i,'/',number_events
    nmuCount = int(c50.GetLeaf('nmuCount').GetValue())
    ngoodMuons = c50.GetLeaf('ngoodMuons').GetValue()
    nvetoMuons = c50.GetLeaf('nvetoMuons').GetValue()
    nvetoElectrons = c50.GetLeaf('nvetoElectrons').GetValue()
    njets = c50.GetLeaf('njets').GetValue()
    met = c50.GetLeaf('met').GetValue()
    genMet = c50.GetLeaf('genMet').GetValue()
    ht = c50.GetLeaf('ht').GetValue()
    metphi = c50.GetLeaf('metphi').GetValue()
    genMetphi = c50.GetLeaf('genMetPhi').GetValue()
    ngLep = int(c50.GetLeaf('ngLep').GetValue())
    ngNuMuFromW = c50.GetLeaf('ngNuMuFromW').GetValue() 
    ngNuEFromW = c50.GetLeaf('ngNuEFromW').GetValue()
    ntmuons=0
    nlmuons=0
    muons=[]
    gLeps=[]
    #Get all genLeps
    for p in range(int(ngLep)):
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
    if met>150:
      h_Ht.Fill(ht)
      h_njets.Fill(njets)
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
            h_GenMt.Fill(sqrt(2*met*TightMatchedMuon['pt']*(1-cos(TightMatchedMuon['phi']-metphi))), weight)
            h_GenMet.Fill(met, weight)
            h_GenPt.Fill(TightMatchedMuon['pt'], weight)
            h_TruthMuPhi.Fill(TightMatchedMuon['phi'],weight)
            h_MetPhi.Fill(metphi,weight)
            Wx = met*cos(metphi) + TightMatchedMuon['pt']*cos(TightMatchedMuon['phi'])
            Wy = met*sin(metphi) + TightMatchedMuon['pt']*sin(TightMatchedMuon['phi'])
            WPhi = atan2(Wy,Wx)
            #h_GenDeltaPhi.Fill(cos(TightMatchedMuon['phi']-metphi), weight)
            print 'truth cos deltaphi:', cos(TightMatchedMuon['phi']-WPhi)
            h_GenDeltaPhi.Fill(deltaPhi(TightMatchedMuon['phi'],WPhi), weight)
            h_MetDeltaPhiComp.Fill(TightMatchedMuon['phi']-metphi,met)      
    if len(muons)<2: continue
    if len(muons)==2 and ntmuons>=1:
      #print 'tight muons:', ntmuons, 'loose muons:',nlmuons
      for perm in [muons, reversed(muons)]:
        m,m2 = perm
        if m2['isTight']==1:
          EffDiLep = h_EffinDiLep.GetBinContent(h_EffinDiLep.FindBin(m['pt'],m['eta']))
          #print 'Eff: ', EffDiLep
          h_EffDiLep.Fill(EffDiLep)
          #print 'm muon pt:', m['pt'], 'eta:',m['eta'] , 'phi:',m['phi'],'eff of muon:', EffDiLep
          #print 'm2 muon pt:',m2['pt'], 'eta:',m2['eta'] , 'phi:',m2['phi']
          metAdd=m['pt']
          Metx = met*cos(metphi)+cos(m['phi'])*metAdd
          Mety = met*sin(metphi)+sin(m['phi'])*metAdd
          WxPred= Metx+cos(m2['phi'])*m2['pt']
          WyPred= Mety+sin(m2['phi'])*m2['pt']
          WPhiPred = atan2(WyPred,WxPred)
          metPred = sqrt(Metx**2+Mety**2)
          metphiPred = atan2(Mety,Metx)
          mtPred = sqrt(2*metPred*m2['pt']*(1-cos(m2['phi']-metphiPred)))
          if metPred >150:
            h_PtLostNoReWeight.Fill(m['pt'],weight)
            if EffDiLep !=0: Seff = (1-EffDiLep)/EffDiLep
            if EffDiLep ==0: Seff = EffDiLep
            #print 'Scale factor:', Seff
            #Seff =  (1-EffDiLep)/(EffDiLep)
            h_MtPred.Fill(mtPred,weight*Seff)
            h_Met.Fill(metPred,weight*Seff)
            h_Pt.Fill(m2['pt'],weight*Seff)
            h_Phi.Fill(m2['phi'],weight*Seff)
            h_MetPhiPred.Fill(metphiPred,weight*Seff) 
            print 'pred cos deltaphi:', cos(m2['phi']-WPhiPred)
            #h_DeltaPhi.Fill(cos(m2['phi']-metphiPred),weight*Seff)
            h_DeltaPhi.Fill(deltaPhi(m2['phi'],WPhiPred),weight*Seff)
            h_PtLost.Fill(m['pt'],weight*Seff)
  
  print 'integral 2 reco muon:', h_EffDiLep.Integral()
  print 'integral 1 reco muon Eff hasmatch:', h_EffLostLep.Integral()
  print 'nevents:', number_events

File.Write()
File.Close()


