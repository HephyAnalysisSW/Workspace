import ROOT
from stage2Tuples import ttJetsCSA1450ns , ttJetsCSA1425ns
from localInfo import username
from objectSelection import tightPOGMuID , vetoMuID
from math import sqrt, cos, sin, atan2
from array import array

def getMu(c,j):
  IsGlobal = c.GetLeaf('muIsGlobal').GetValue(j)
  IsPF = c.GetLeaf('muIsPF').GetValue(j)
  IsTracker = c.GetLeaf('muIsTracker').GetValue(j)
  Dz = c.GetLeaf('muDz').GetValue(j)
  pt = c.GetLeaf('muPt').GetValue(j)
  eta= c.GetLeaf('muEta').GetValue(j)
  phi= c.GetLeaf('muPhi').GetValue(j)
  relIso = c.GetLeaf('muRelIso').GetValue(j)
  NormChi2 = c.GetLeaf('muNormChi2').GetValue(j)
  NValMuonHits = c.GetLeaf('muNValMuonHits').GetValue(j)
  Dxy = c.GetLeaf('muDxy').GetValue(j)
  NumtrackerLayerWithMeasurement = c.GetLeaf('muNumtrackerLayerWithMeasurement').GetValue(j)
  ChargedHadronPt = c.GetLeaf('muIso03sumChargedHadronPt').GetValue(j)
  NeutralHadronEt = c.GetLeaf('muIso03sumNeutralHadronEt').GetValue(j)
  PixelHits = c.GetLeaf('muPixelHits').GetValue(j)
  NumMatchedStations = c.GetLeaf('muNumMatchedStations').GetValue(j)
  PhotonEt = c.GetLeaf('muIso03sumPhotonEt').GetValue(j)
  PUChargedHadronPt = c.GetLeaf('muIso03sumPUChargedHadronPt').GetValue(j)
  RelIsoPred = (ChargedHadronPt+max(0,(NeutralHadronEt+PhotonEt-(0.5*PUChargedHadronPt))))/pt
  isTight = None
  isLoose = None
  cand={'isLoose':isLoose, 'isTight':isTight, 'NumMatchedStations':NumMatchedStations,'PixelHits':PixelHits, 'NumtrackerLayerWithMeasurement':NumtrackerLayerWithMeasurement,'Dxy':Dxy, 'NValMuonHits':NValMuonHits ,'NormChi2':NormChi2, 'IsPF':IsPF, 'RelIsoPred':RelIsoPred, 'ChargedHadronPt':ChargedHadronPt,'NeutralHadronEt':NeutralHadronEt,'PhotonEt':PhotonEt,'PUChargedHadronPt':PUChargedHadronPt,'IsGlobal':IsGlobal, 'IsTracker':IsTracker, 'Dz':Dz, 'pt':pt, 'eta':eta, 'phi':phi, 'relIso':relIso}
  if pt>5 and abs(eta)<2.5 and abs(Dz)<0.5 and (IsGlobal or  IsTracker):
   return cand


diLep     ="ngoodMuons>=1&&nvetoMuons==2&&ngNuEFromW==0&&nvetoElectrons==0"

  
#def Get2Mu(c):
#  nmuCount = int(c.GetLeaf('nmuCount').GetValue())
#  ntmuons = 0
#  nlmuons = 0
#  temp=[]
#  for i in range(nmuCount):
#    lep=getMu(c,i)
#    isTight=tightPOGMuID(lep)
#    isLoose=vetoMuID(lep)
#    #print isTight
#    lep['isTight'] = isTight
#    #print lep['isTight']
#    lep['isLoose'] = isLoose
#    if isTight: ntmuons+=1
#    if isLoose:  nlmuons+=1
#    temp=lep
#    #print temp['isTight']
#  return temp

File = ROOT.TFile('DiLeptonMtnew.root','RECREATE')
h_MTDilepton = ROOT.TH1F('h_MTDilepton', 'h_MTDilepton',100,0,800)
h_MTGen = ROOT.TH1F('h_MTGen', 'h_MTGen',100,0,800)
ProfilePt = ROOT.TProfile('ProfilePt','muonID vs gen Lep Pt',100,0,800,0,1)
ProfileEta = ROOT.TProfile('ProfileEta','muonID vs gen Lep Eta',100,-5,5,0,1)
ProfilePt01 = ROOT.TProfile('ProfilePt01','muonID vs gen Lep Pt',100,0,800,0,1)
ProfilePt02 = ROOT.TProfile('ProfilePt02','muonID vs gen Lep Pt',100,0,800,0,1)
ProfileEta01 = ROOT.TProfile('ProfileEta01','muonID vs gen Lep Eta',100,-5,5,0,1)
ProfilePt03 = ROOT.TProfile('ProfilePt03','muonID vs gen Lep Pt',100,0,800,0,1)
ProfileEta02 = ROOT.TProfile('ProfileEta02','muonID vs gen Lep Eta',100,-5,5,0,1)
ProfileEta03 = ROOT.TProfile('ProfileEta03','muonID vs gen Lep Eta',100,-5,5,0,1)

c50 = ROOT.TChain('Events')
#for b in ttJetsCSA1450ns['bins']:
#  c.Add(ttJetsCSA1450ns['dirname']+'/'+b+'/h*.root')
c50.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from0To10.root')
#c50.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/*')


c25 = ROOT.TChain('Events')
#for b in ttJetsCSA1425ns['bins']:
#  c2.Add(ttJetsCSA1425ns['dirname']+'/'+b+'/h*.root')
c25.Add('/data/easilar/convertedTuples_v23/copyMET_DR0.4/ttJetsCSA1425ns/histo_ttJetsCSA1425ns_from0To10.root')

number_events50 = c50.GetEntries()
print number_events50
for i in range(1000):
  c50.GetEntry(i)
  nmuCount = int(c50.GetLeaf('nmuCount').GetValue())
  ntmuons = 0
  nlmuons = 0
  met = c50.GetLeaf('met').GetValue()
  metphi = c50.GetLeaf('metphi').GetValue()
  muons=[] 
  for j in range(nmuCount):
    muon=getMu(c50,j)
    muon['index'] = -1
    if muon:
      #print tightPOGMuID(muon)
      #if tightPOGMuID(muon)==0. or vetoMuID(muon)==0.: print 'Tight or loose is zero!'
      #if tightPOGMuID(muon)!=0:
      isTight=tightPOGMuID(muon)
      #if vetoMuID(muon)!=0:
      isLoose=vetoMuID(muon)
      #print isTight
      muon['isTight'] = isTight
      #print lep['isTight']
      muon['isLoose'] = isLoose
      if isTight: ntmuons+=1
      if isLoose: nlmuons+=1
      muons.append(muon)  
  
  ngLep = int(c50.GetLeaf('ngLep').GetValue()) 
  if len(muons)<2: continue
  if len(muons)==2 and ntmuons>=1:
    #print "Found two muons",len(muons),'muons'
    #print muons[0]['index']
    #print muons[1]['index']
    for perm in [muons, reversed(muons)]:
      m,m2 = perm
      if m2['isTight']:
        #if muons[0]['gLepDR']<0.5 and muons[1]['gLepDR']<0.5: 
        #if ntmuons>=1 and nlmuons==2 and ngNuMuFromW==2 and ngNuEFromW==0: ##For Dilepton
        #print 'Dilepton:)'
        metAdd=m['pt']
        Metx = met*cos(metphi)+cos(m['phi'])*metAdd
        Mety = met*sin(metphi)+sin(m['phi'])*metAdd
        metPred = sqrt(Metx**2+Mety**2)
        metphiPred = atan2(Mety,Metx)
        mtPred = sqrt(2*metPred*m2['pt']*(1-cos(m2['phi']-metphiPred)))
        h_MTDilepton.Fill(mtPred)
      ngLep = int(c50.GetLeaf('ngLep').GetValue()) 
      for j in range(int(ngLep)):
        gLepPt = c50.GetLeaf('gLepPt').GetValue(j)
        gLepEta = c50.GetLeaf('gLepEta').GetValue(j)
        #if m2['index']>=0:
        print int(m2['isLoose']) , gLepPt
        ProfilePt.Fill(gLepPt,m2['isLoose'],1)
        ProfileEta.Fill(gLepEta,m2['isLoose'],1)
        if m2['relIso']<0.1:
          ProfilePt01.Fill(gLepPt,m2['isLoose'],1)
          ProfileEta01.Fill(gLepEta,m2['isLoose'],1)
        if m2['relIso']<0.2:
          ProfilePt02.Fill(gLepPt,m2['isLoose'],1)
          ProfileEta02.Fill(gLepEta,m2['isLoose'],1)
        if m2['relIso']<0.3:
          ProfilePt03.Fill(gLepPt,m2['isLoose'],1)
          ProfileEta03.Fill(gLepEta,m2['isLoose'],1)

#c50.Draw('sqrt(2*genMet*gLepPt*(1-cos(gLepPhi-genMetphi)))>>h_MTGen', 'ngNuMuFromW==2&&gLepPdg==13&&gLepPt>20&&gLepEta<2.1&&gLepDR<0.4' )

#File.cd() 
          
canPt = ROOT.TCanvas('Iso')
canPt.cd()
#h_MTDilepton.SetLineColor(ROOT.kBlue)
#h_MTDilepton.Draw()
#h_MTGen.SetLineColor(ROOT.kRed)
#h_MTGen.Draw('same')
ProfilePt.SetLineColor(ROOT.kBlue)
ProfilePt.Draw()
ProfilePt01.SetLineColor(ROOT.kRed)
ProfilePt01.Draw('same')
ProfilePt02.SetLineColor(ROOT.kGreen)
ProfilePt02.Draw('same')
ProfilePt03.SetLineColor(ROOT.kYellow)
ProfilePt03.Draw('same')

leg = ROOT.TLegend(0.6,0.6,0.9,0.7)
leg.AddEntry(ProfilePt, "NoIso","l")
leg.AddEntry(ProfilePt01, "Iso:0.1","l")
leg.AddEntry(ProfilePt02, "Iso:0.2","l")
leg.AddEntry(ProfilePt03, "Iso:0.3","l")
leg.SetFillColor(0)
leg.Draw()
canPt.Update()
canPt.Print('/afs/hephy.at/user/e/easilar/www/LastCSA14/LooseIndexVsgLepPtIsoComp.png')

canEta = ROOT.TCanvas('iso02')
canEta.cd()
ProfileEta.SetLineColor(ROOT.kBlue)
#ProfileEta.SetLineWidth(1.8)
ProfileEta.Draw()
#ProfileEta01.SetLineWidth(1.8)
ProfileEta01.SetLineColor(ROOT.kRed)
ProfileEta01.Draw('same')
#ProfileEta02.SetLineWidth(1.8)
ProfileEta02.SetLineColor(ROOT.kGreen)
ProfileEta02.Draw('same')
#ProfileEta03.SetLineWidth(1.8)
ProfileEta03.SetLineColor(ROOT.kYellow)
ProfileEta03.Draw('same')

leg1 = ROOT.TLegend(0.8,0.6,0.9,0.7)
leg1.AddEntry(ProfileEta, "NoIso","l")
leg1.AddEntry(ProfileEta01, "Iso:0.1","l")
leg1.AddEntry(ProfileEta02, "Iso:0.2","l")
leg1.AddEntry(ProfileEta03, "Iso:0.3","l")
leg1.SetFillColor(0)
leg1.Draw()

canEta.Update()
canEta.Print('/afs/hephy.at/user/e/easilar/www/LastCSA14/LooseIndexVsgLepEtaIsoComp.png')

#leg = ROOT.TLegend(0.6,0.6,0.9,0.7)
#leg.AddEntry(h_MTDilepton, "Calculated","l")
#leg.AddEntry(h_MTGen, "MTGen","l")
#leg.SetFillColor(0)
#leg.Draw()
#can.SetLogy()
#can.Update()
#can.Print('/afs/hephy.at/user/e/easilar/www/LastCSA14/LooseIndexVsgLepEtaIso03.png')
#can.Write()

#File.Write()
#File.Close()
