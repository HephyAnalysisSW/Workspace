import ROOT
from Workspace.RA4Analysis.stage2Tuples import ttJetsCSA1450ns
from localInfo import username
from objectSelection import tightPOGMuID , vetoMuID , getLooseMuStage2
from math import sqrt, cos, sin, atan2
from array import array

ptBins  = array('d', [float(x) for x in range(10, 20)+range(20,50,3)+range(50,100,10)+range(100,300,30)])
#etaBins = array('d', [int(x)+30 for x in range(-30,32,2)])
etaBins = array('d', [float(x)/10. for x in range(-30,32,2)])

ptBins2D  = array('d', [float(x) for x in range(10, 20)+range(20,50,5)+range(50,100,20)+range(100,310,50)])
etaBins2D = array('d', [float(x)/10. for x in [-30,-25]+range(-21,22,6)+[25,30]])

File = ROOT.TFile('EffSmall.root','RECREATE')
File.cd()

PtDenDiLep = ROOT.TH1F('PtDenDiLep', 'PtDenDiLep',len(ptBins)-1,ptBins)
EtaDenDiLep = ROOT.TH1F('EtaDenDiLep', 'EtaDenDiLep',len(etaBins)-1,etaBins) 
PtEtaDenDiLep = ROOT.TH2F('PtEtaDenDiLep','PtEtaDenDiLep',len(ptBins2D)-1,ptBins2D,len(etaBins2D)-1,etaBins2D)

PtNumDiLep = ROOT.TH1F('PtNumDiLep', 'PtNumDiLep',len(ptBins)-1,ptBins)
EtaNumDiLep = ROOT.TH1F('EtaNumDiLep', 'EtaNumDiLep',len(etaBins)-1,etaBins) 
PtEtaNumDiLep = ROOT.TH2F('PtEtaNumDiLep','PtEtaNumDiLep',len(ptBins2D)-1,ptBins2D,len(etaBins2D)-1,etaBins2D)

EffPt = ROOT.TH1F('EffPt', 'EffPt',len(ptBins)-1,ptBins)
EffEta = ROOT.TH1F('EffEta', 'EffEta',len(etaBins)-1,etaBins) 
EffPtEta = ROOT.TH2F('EffPtEta','EffPtEta',len(ptBins2D)-1,ptBins2D,len(etaBins2D)-1,etaBins2D)

preselection = "ht>300 && met>150 && njets>=3"

c50 = ROOT.TChain('Events')
#for b in ttJetsCSA1450ns['bins']:
#  c.Add(ttJetsCSA1450ns['dirname']+'/'+b+'/h*.root')
c50.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from0To10.root')
#c50.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/*')

c50.Draw(">>List",preselection)
List = ROOT.gDirectory.Get("List")
number_events = List.GetN()
#number_events = c50.GetEntries()
for relIso in [0.12,0.2,0.3]:
  for i in range(number_events):
    c50.GetEntry(List.GetEntry(i))
    print number_events-i, 'events left'
    nmuCount = int(c50.GetLeaf('nmuCount').GetValue())
    ngoodMuons = c50.GetLeaf('ngoodMuons').GetValue()
    nvetoMuons = c50.GetLeaf('nvetoMuons').GetValue()
    nvetoElectrons = c50.GetLeaf('nvetoElectrons').GetValue()
    njets = c50.GetLeaf('njets').GetValue()
    met = c50.GetLeaf('met').GetValue()
    genMet = c50.GetLeaf('genMet').GetValue()
    ht = c50.GetLeaf('ht').GetValue()
    metphi = c50.GetLeaf('metphi').GetValue()
    genMetphi = c50.GetLeaf('genMetphi').GetValue()
    ngLep = int(c50.GetLeaf('ngLep').GetValue())
    ngNuMuFromW = c50.GetLeaf('ngNuMuFromW').GetValue() 
    ngNuEFromW = c50.GetLeaf('ngNuEFromW').GetValue()
    ntmuons=0
    nlmuons=0
    muons=[]
    for j in range(nmuCount):
      #muon=getMu(c50,j)
      muon=getLooseMuStage2(c50,j)
      if muon:
        isTight=tightPOGMuID(muon)
        isLoose=vetoMuID(muon,relIso)
        muon['isTight'] = isTight
        muon['isLoose'] = isLoose
        if isTight: ntmuons+=1
        if isLoose: nlmuons+=1
        muons.append(muon)
    for p in range(int(ngLep)):
      gLepPdg = c50.GetLeaf('gLepPdg').GetValue(p)
      gLepDR = c50.GetLeaf('gLepDR').GetValue(p)
      gLepPt = c50.GetLeaf('gLepPt').GetValue(p)
      gLepEta = c50.GetLeaf('gLepEta').GetValue(p)
      gLepInd = c50.GetLeaf('gLepInd').GetValue(p)
      gLepPhi = c50.GetLeaf('gLepPhi').GetValue(p)
      if abs(gLepPdg) == 13 and gLepPt>20 and abs(gLepEta)<2.1 and ngNuMuFromW==2 and ngNuEFromW==0:
        PtEtaDenDiLep.Fill(gLepPt,gLepEta)
        EtaDenDiLep.Fill(gLepEta)
        PtDenDiLep.Fill(gLepPt)
        if gLepInd>=0 and  gLepDR<0.4:
          k=int(gLepInd)
          if muons[k]['isLoose'] == 1 and abs(1-muons[k]['pt']/gLepPt)<0.9:
              PtEtaNumDiLep.Fill(gLepPt,gLepEta)
              EtaNumDiLep.Fill(gLepEta)
              PtNumDiLep.Fill(gLepPt)

  ###Eff Calculation
  EffPt = PtNumDiLep.Clone()
  EffPt.Divide(PtDenDiLep)
  EffPt.Write("Pt"+str(relIso))

  EffEta = EtaNumDiLep.Clone()
  EffEta.Divide(EtaDenDiLep)
  EffEta.Write("Eta"+str(relIso))

  EffPtEta = PtEtaNumDiLep.Clone()
  EffPtEta.Divide(PtEtaDenDiLep) 
  EffPtEta.Write("2D"+str(relIso))
  
  can2D3 = ROOT.TCanvas("2DCol"+str(relIso))
  can2D3.cd()
  EffPtEta.Draw('colz')
  can2D3.Write()


File.Write()
File.Close()

