import ROOT
from stage2Tuples import ttJetsCSA1450ns , ttJetsCSA1425ns
from localInfo import username
from objectSelection import tightPOGMuID , vetoMuID
from math import sqrt, cos, sin, atan2

def getMu(c,j):
  IsGlobal = c.GetLeaf('muIsGlobal').GetValue(j)
  IsPF = c.GetLeaf('muIsPF').GetValue(j)
  IsTracker = c.GetLeaf('muIsTracker').GetValue(j)
  Dz = c.GetLeaf('muDz').GetValue(j)
  pt = c.GetLeaf('muPt').GetValue(j)
  eta= c.GetLeaf('muEta').GetValue(j)
  phi= c.GetLeaf('muPhi').GetValue(j)
  Pdg= c.GetLeaf('gLepPdg').GetValue(j)
  gLepDR = c.GetLeaf('gLepDR').GetValue(j)
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
  isTight = False
  isLoose = False
  cand={'isLoose':isLoose, 'isTight':isTight, 'NumMatchedStations':NumMatchedStations,'PixelHits':PixelHits, 'NumtrackerLayerWithMeasurement':NumtrackerLayerWithMeasurement,'Dxy':Dxy, 'NValMuonHits':NValMuonHits ,'NormChi2':NormChi2, 'IsPF':IsPF, 'IsGlobal':IsGlobal, 'RelIsoPred':RelIsoPred, 'ChargedHadronPt':ChargedHadronPt,'NeutralHadronEt':NeutralHadronEt,'PhotonEt':PhotonEt,'PUChargedHadronPt':PUChargedHadronPt,'IsGlobal':IsGlobal, 'IsTracker':IsTracker, 'Dz':Dz, 'pt':pt, 'eta':eta, 'phi':phi, 'Pdg':Pdg, 'gLepDR':gLepDR, 'relIso':relIso}
  #if pt>5 and (muIsGlobal or  muIsTracker) and abs(eta)<2.5 and abs(dz)< 0.5 and gLepDR<0.5:
  if pt>5 and abs(eta)<2.5 and abs(Dz)<0.5 and (IsGlobal or  IsTracker):
   return cand


diLep     ="ngoodMuons>=1&&nvetoMuons==2&&ngNuEFromW==0&&nvetoElectrons==0"

'''  
def Get2Mu(c):
  nmuCount = int(c.GetLeaf('nmuCount').GetValue())
  ntmuons = 0
  nlmuons = 0
  temp=[]
  for i in range(nmuCount):
    lep=getMu(c,i)
    isTight=tightPOGMuID(lep)
    isLoose=vetoMuID(lep)
    #print isTight
    lep['isTight'] = isTight
    #print lep['isTight']
    lep['isLoose'] = isLoose
    if isTight: ntmuons+=1
    if isLoose:  nlmuons+=1
    temp=lep
    #print temp['isTight']
  return temp
'''

File = ROOT.TFile('DiLeptonMt.root','RECREATE')
h_MTDilepton = ROOT.TH1F('MT', 'MT',100,0,800)

c50 = ROOT.TChain('Events')
#for b in ttJetsCSA1450ns['bins']:
#  c.Add(ttJetsCSA1450ns['dirname']+'/'+b+'/h*.root')
#c50.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from0To10.root')
c50.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/*')

c25 = ROOT.TChain('Events')
#for b in ttJetsCSA1425ns['bins']:
#  c2.Add(ttJetsCSA1425ns['dirname']+'/'+b+'/h*.root')
c25.Add('/data/easilar/convertedTuples_v23/copyMET_DR0.4/ttJetsCSA1425ns/histo_ttJetsCSA1425ns_from0To10.root')

number_events50 = c50.GetEntries()
print number_events50
for i in range(number_events50):
  c50.GetEntry(i)
  ngNuMuFromW = c50.GetLeaf('ngNuMuFromW').GetValue()
  ngNuEFromW = c50.GetLeaf('ngNuEFromW').GetValue()
  nmuCount = int(c50.GetLeaf('nmuCount').GetValue())
  ntmuons = 0
  nlmuons = 0
  for j in range(nmuCount):
    met = c50.GetLeaf('met').GetValue(j)
    metphi = c50.GetLeaf('metphi').GetValue(j)
    muons50=getMu(c50,j)
    isTight=tightPOGMuID(muons50)
    isLoose=vetoMuID(muons50)
    #print isTight
    muons50['isTight'] = isTight
    #print lep['isTight']
    muons50['isLoose'] = isLoose
    if isTight: ntmuons+=1
    if isLoose:  nlmuons+=1
  if ntmuons>=1 and nlmuons==2 and ngNuMuFromW==2 and ngNuEFromW==0:
    print 'Dilepton:)'
    if muons50['isLoose']:
      Lmuons=muons50
      metAdd=Lmuons['pt']
      Metx = met*cos(metphi)+cos(Lmuons['pt'])*metAdd
      Mety = met*sin(metphi)+sin(Lmuons['pt'])*metAdd
    if muons50['isTight']:
      Tmuons=muons50
      mtPred = sqrt(2*metPred*Tmuons['pt']*(1-cos(Tmuons['phi']-metphiPred)))
      if mtPred!=0: h_MTDilepton.Fill(mtPred)

File.cd() 
can = ROOT.TCanvas('MTPlotDiLepton')
can.cd()

h_MTDilepton.Draw()

#can.Update()
can.Write()

File.Write()
File.Close() 
