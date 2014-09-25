import ROOT
from stage2Tuples import ttJetsCSA1450ns
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

##Take efficiency from root file
fEff = ROOT.TFile('IsolationBin5.root')
#effVec = []
h1 = fEff.Get('Iso03PtEtaEff')
#for i in range(h1.GetNbinsX()):
#  for j in range(h1.GetNbinsY()):
    #print h1.GetBinContent(i,j)
#    if h1.GetBinContent(i,j) != 0: effVec.append(h1.GetBinContent(i,j))
    #effVec.append(h1.GetBinContent(i,j))
#print 'lengt of eff vector:' , len(effVec)

#File = ROOT.TFile('DiLeptonMtScaled.root','RECREATE')
File = ROOT.TFile('deneme.root','RECREATE')
h_MTDilepton = ROOT.TH1F('h_MTDilepton', 'h_MTDilepton',100,0,800)
h_MTGen = ROOT.TH1F('h_MTGen', 'h_MTGen',100,0,800)
h_Eff = ROOT.TH1F('h_Eff', 'h_Eff',100,0,1)
t = ROOT.TTree( "Events", "Events", 1 )
 
c50 = ROOT.TChain('Events')
#for b in ttJetsCSA1450ns['bins']:
#  c.Add(ttJetsCSA1450ns['dirname']+'/'+b+'/h*.root')
c50.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from0To10.root')
#c50.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/*')


#c25 = ROOT.TChain('Events')
#for b in ttJetsCSA1425ns['bins']:
#  c2.Add(ttJetsCSA1425ns['dirname']+'/'+b+'/h*.root')
#c25.Add('/data/easilar/convertedTuples_v23/copyMET_DR0.4/ttJetsCSA1425ns/histo_ttJetsCSA1425ns_from0To10.root')


number_events50 = c50.GetEntries()
print number_events50
for i in range(number_events50):
  c50.GetEntry(i)
  nmuCount = int(c50.GetLeaf('nmuCount').GetValue())
  ntmuons = 0
  nlmuons = 0
  met = c50.GetLeaf('met').GetValue()
  metphi = c50.GetLeaf('metphi').GetValue()
  muons=[] 
  for j in range(nmuCount):
    muon=getMu(c50,j)
    if muon:
      #print tightPOGMuID(muon)
      #if tightPOGMuID(muon)==0. or vetoMuID(muon)==0.: print 'Tight or loose is zero!'
      #if tightPOGMuID(muon)!=0:
      isTight=tightPOGMuID(muon)
      #if vetoMuID(muon)!=0:
      isLoose=vetoMuID(muon,0.3)
      #print isTight
      muon['isTight'] = isTight
      #print lep['isTight']
      muon['isLoose'] = isLoose
      if isTight: ntmuons+=1
      if isLoose: nlmuons+=1
      muons.append(muon)  
  
  if len(muons)<2: continue
  if len(muons)==2 and ntmuons>=1:
    print "Found two muons",len(muons)
    for perm in [muons, reversed(muons)]:
      m,m2 = perm 
      Eff = h1.GetBinContent(h1.FindBin(m['pt'], m['eta']))
      if m2['isTight']:
        if Eff != 0:
          scaleEff = (1-Eff)/Eff
          #scaleEff = Eff
          #if muons[0]['gLepDR']<0.5 and muons[1]['gLepDR']<0.5: 
          #if ntmuons>=1 and nlmuons==2 and ngNuMuFromW==2 and ngNuEFromW==0: ##For Dilepton
          print 'Find one tight muon:)'
          metAdd=m['pt']
          Metx = met*cos(metphi)+cos(m['phi'])*metAdd
          Mety = met*sin(metphi)+sin(m['phi'])*metAdd
          metPred = sqrt(Metx**2+Mety**2)
          metphiPred = atan2(Mety,Metx)
          mtPred = sqrt(2*metPred*m2['pt']*(1-cos(m2['phi']-metphiPred)))
          h_MTDilepton.Fill(mtPred)
          h_Eff.Fill(scaleEff)

c50.Draw('sqrt(2*genMet*gLepPt*(1-cos(gLepPhi-genMetphi)))>>h_MTGen', 'ngNuMuFromW==2&&gLepPdg==13&&gLepPt>20&&gLepEta<2.1&&gLepDR<0.4' )

File.cd()
can = ROOT.TCanvas('Met')          
can.cd()
h_MTDilepton.SetLineColor(ROOT.kBlue)
#h_MTDilepton.Scale(h_MTGen.Integral()/h_MTDilepton.Integral())
#h_MTDilepton.Scale(1/h_MTDilepton.Integral())
h_MTDilepton.Draw()
h_MTGen.SetLineColor(ROOT.kRed)
#h_MTGen.Scale(1/h_MTGen.Integral())
h_MTGen.Draw('same')

leg = ROOT.TLegend(0.6,0.6,0.9,0.7)
leg.AddEntry(h_MTDilepton, "Calculated","l")
leg.AddEntry(h_MTGen, "MTGen","l")
leg.SetFillColor(0)
leg.Draw()
can.SetLogy()
can.Write()

File.Write()
File.Close()

