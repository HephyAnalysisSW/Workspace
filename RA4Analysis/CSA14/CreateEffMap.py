import ROOT
from Workspace.RA4Analysis.stage2Tuples import ttJetsCSA1450ns
from localInfo import username
from objectSelection import tightPOGMuID , vetoMuID , getLooseMuStage2
from math import sqrt, cos, sin, atan2
from array import array
from getmuon import getMu

Lumi=2000 #pb-1
xsec=689.1 #pb ?
#nevents is later

ptBins  = array('d', [float(x) for x in range(10, 20)+range(20,50,3)+range(50,100,10)+range(100,300,30)])
#etaBins = array('d', [int(x)+30 for x in range(-30,32,2)])
etaBins = array('d', [float(x)/10. for x in range(-30,32,2)])

ptBinsCoarse  = array('d', [float(x) for x in range(10, 20)+range(20,50,5)+range(50,100,20)+range(100,310,50)])
etaBinsCoarse = array('d', [float(x)/10. for x in [-30,-25]+range(-21,22,6)+[25,30]])


File = ROOT.TFile('EffMapDiLep02OO.root','RECREATE')
NoIsoPtEff = ROOT.TH1F('NoIsoPtEff', 'NoIsoPtEff',len(ptBins)-1,ptBins)
#NoIsoPtEff = ROOT.TH1F('NoIsoPtEff', 'NoIsoPtEff',25,0,800)
NoIsoPtNum = ROOT.TH1F('NoIsoPtNum', 'NoIsoPtNum',len(ptBins)-1,ptBins)
NoIsoPtDen = ROOT.TH1F('NoIsoPtDen', 'NoIsoPtDen',len(ptBins)-1,ptBins)
#NoIsoPtDen = ROOT.TH1F('NoIsoPtDen', 'NoIsoPtDen',25,0,800)
NoIsoEtaEff = ROOT.TH1F('NoIsoEtaEff', 'NoIsoEtaEff',len(etaBins)-1,etaBins)
NoIsoEtaNum = ROOT.TH1F('NoIsoEtaNum', 'NoIsoEtaNum',len(etaBins)-1,etaBins)
NoIsoEtaDen = ROOT.TH1F('NoIsoEtaDen', 'NoIsoEtaDen',len(etaBins)-1,etaBins)

NoIsoPtDenDiLep = ROOT.TH1F('NoIsoPtDenDiLep', 'NoIsoPtDenDiLep',len(ptBins)-1,ptBins)
NoIsoEtaDenDiLep = ROOT.TH1F('NoIsoEtaDenDiLep', 'NoIsoEtaDenDiLep',len(etaBins)-1,etaBins) 


Iso01PtEff = ROOT.TH1F('Iso01PtEff', 'Iso01PtEff',len(ptBins)-1,ptBins)
Iso01PtNum = ROOT.TH1F('Iso01PtNum', 'Iso01PtNum',len(ptBins)-1,ptBins)
Iso01EtaEff = ROOT.TH1F('Iso01EtaEff', 'Iso01EtaEff',len(etaBins)-1,etaBins)
Iso01EtaNum = ROOT.TH1F('Iso01EtaNum', 'Iso01EtaNum',len(etaBins)-1,etaBins)

Iso02PtEff = ROOT.TH1F('Iso02PtEff', 'Iso02PtEff',len(ptBins)-1,ptBins)
Iso02PtNum = ROOT.TH1F('Iso02PtNum', 'Iso02PtNum',len(ptBins)-1,ptBins)
Iso02EtaEff = ROOT.TH1F('Iso02EtaEff', 'Iso02EtaEff',len(etaBins)-1,etaBins)
Iso02EtaNum = ROOT.TH1F('Iso02EtaNum', 'Iso02EtaNum',len(etaBins)-1,etaBins)

Iso03PtEff = ROOT.TH1F('Iso03PtEff', 'Iso03PtEff',len(ptBins)-1,ptBins)
Iso03PtNum = ROOT.TH1F('Iso03PtNum', 'Iso03PtNum',len(ptBins)-1,ptBins)
Iso03EtaEff = ROOT.TH1F('Iso03EtaEff', 'Iso03EtaEff',len(etaBins)-1,etaBins)
Iso03EtaNum = ROOT.TH1F('Iso03EtaNum', 'Iso03EtaNum',len(etaBins)-1,etaBins)

Iso03PtEffDiLep = ROOT.TH1F('Iso03PtEffDiLep', 'Iso03PtEffDiLep',len(ptBins)-1,ptBins)
Iso03PtNumDiLep = ROOT.TH1F('Iso03PtNumDiLep', 'Iso03PtNumDiLep',len(ptBins)-1,ptBins)

Iso03EtaEffDiLep = ROOT.TH1F('Iso03EtaEffDiLep', 'Iso03EtaEffDiLep',len(etaBins)-1,etaBins)
Iso03EtaNumDiLep = ROOT.TH1F('Iso03EtaNumDiLep', 'Iso03EtaNumDiLep',len(etaBins)-1,etaBins)


NoIsoPtEtaEff = ROOT.TH2F('NoIsoPtEtaEff', 'NoIsoPtEtaEff',len(ptBinsCoarse)-1,ptBinsCoarse,len(etaBinsCoarse)-1,etaBinsCoarse)
NoIsoPtEtaNum = ROOT.TH2F('NoIsoPtEtaNum', 'NoIsoPtEtaNum',len(ptBinsCoarse)-1,ptBinsCoarse,len(etaBinsCoarse)-1,etaBinsCoarse)
NoIsoPtEtaDen = ROOT.TH2F('NoIsoPtEtaDen', 'NoIsoPtEtaDen',len(ptBinsCoarse)-1,ptBinsCoarse,len(etaBinsCoarse)-1,etaBinsCoarse)
#NoIsoPtEtaDen = ROOT.TH2F('NoIsoPtEtaDenbin', 'NoIsoPtEtaDenbin',25,0,800,25,-3,3)
NoIsoPtEtaDenDiLep = ROOT.TH2F('NoIsoPtEtaDenDiLep', 'NoIsoPtEtaDenDiLep',len(ptBinsCoarse)-1,ptBinsCoarse,len(etaBinsCoarse)-1,etaBinsCoarse)

Iso01PtEtaEff = ROOT.TH2F('Iso01PtEtaEff', 'Iso01PtEtaEff',len(ptBinsCoarse)-1,ptBinsCoarse,len(etaBinsCoarse)-1,etaBinsCoarse)
Iso01PtEtaNum = ROOT.TH2F('Iso01PtEtaNum', 'Iso01PtEtaNum',len(ptBinsCoarse)-1,ptBinsCoarse,len(etaBinsCoarse)-1,etaBinsCoarse)

Iso02PtEtaEff = ROOT.TH2F('Iso02PtEtaEff', 'Iso02PtEtaEff',len(ptBinsCoarse)-1,ptBinsCoarse,len(etaBinsCoarse)-1,etaBinsCoarse)
Iso02PtEtaNum = ROOT.TH2F('Iso02PtEtaNum', 'Iso02PtEtaNum',len(ptBinsCoarse)-1,ptBinsCoarse,len(etaBinsCoarse)-1,etaBinsCoarse)

Iso03PtEtaEff = ROOT.TH2F('Iso03PtEtaEff', 'Iso03PtEtaEff',len(ptBinsCoarse)-1,ptBinsCoarse,len(etaBinsCoarse)-1,etaBinsCoarse)
Iso03PtEtaNum = ROOT.TH2F('Iso03PtEtaNum', 'Iso03PtEtaNum',len(ptBinsCoarse)-1,ptBinsCoarse,len(etaBinsCoarse)-1,etaBinsCoarse)

#Iso03PtEtaEff = ROOT.TH2F('Iso03PtEtaEff', 'Iso03PtEtaEff',25,0,800,25,-3,3)
#Iso03PtEtaNum = ROOT.TH2F('Iso03PtEtaNum', 'Iso03PtEtaNum',25,0,800,25,-3,3)

Iso03PtEtaEffDiLep = ROOT.TH2F('Iso03PtEtaEffDiLep', 'Iso03PtEtaEffDiLep',len(ptBinsCoarse)-1,ptBinsCoarse,len(etaBinsCoarse)-1,etaBinsCoarse)
Iso03PtEtaNumDiLep = ROOT.TH2F('Iso03PtEtaNumDiLep', 'Iso03PtEtaNumDiLep',len(ptBinsCoarse)-1,ptBinsCoarse,len(etaBinsCoarse)-1,etaBinsCoarse)
Iso03PtEtaEffFindDiLep = ROOT.TH2F('Iso03PtEtaEffFindDiLep', 'Iso03PtEtaEffFindDiLep',len(ptBinsCoarse)-1,ptBinsCoarse,len(etaBinsCoarse)-1,etaBinsCoarse)

EffCount = ROOT.TH1F('EffCount','Cuts',16,0,20)
EffCount.GetXaxis().SetBinLabel(1,'all')
EffCount.GetXaxis().SetBinLabel(2,'noIso')
EffCount.GetXaxis().SetBinLabel(3,'Iso01')
EffCount.GetXaxis().SetBinLabel(4,'Iso02')
EffCount.GetXaxis().SetBinLabel(5,'Iso03')


c50 = ROOT.TChain('Events')
#for b in ttJetsCSA1450ns['bins']:
#  c.Add(ttJetsCSA1450ns['dirname']+'/'+b+'/h*.root')
c50.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from0To10.root')
#c50.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/*')

number_events50 = c50.GetEntries()

#weight = Lumi*xsec/number_events50
weight = 0.436738650483
print 'weight is:', weight
print 'Total Number of Events is:', number_events50
print 'This is for from 0 to 10.....'

for i in range(number_events50):
#for i in range(3000):
  c50.GetEntry(i)
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
  relIso = 200  ##no Cut
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
  numerator = 0
  denominator = 0
  #print 'enter ngLep loop'
  for p in range(int(ngLep)):
    gLepPdg = c50.GetLeaf('gLepPdg').GetValue(p)
    gLepDR = c50.GetLeaf('gLepDR').GetValue(p)
    gLepPt = c50.GetLeaf('gLepPt').GetValue(p)
    gLepEta = c50.GetLeaf('gLepEta').GetValue(p)
    gLepInd = c50.GetLeaf('gLepInd').GetValue(p)
    gLepPhi = c50.GetLeaf('gLepPhi').GetValue(p)
    if gLepInd>=0:
      k=int(gLepInd)
      if abs(gLepPdg) == 13 and gLepPt>20 and abs(gLepEta)<2.1 and ht>300 and met>150 and njets>=3:
        EffCount.Fill(1) 
        denominator=ngLep
        NoIsoEtaDen.Fill(muons[k]['eta'])
        NoIsoPtDen.Fill(muons[k]['pt'])
        NoIsoPtEtaDen.Fill(muons[k]['pt'],muons[k]['eta'])
        if ngNuMuFromW==2 and ngNuEFromW==0 and ngoodMuons==1 and nvetoMuons==1 and nvetoElectrons==0:
          NoIsoPtEtaDenDiLep.Fill(muons[k]['pt'],muons[k]['eta'])
          NoIsoEtaDenDiLep.Fill(muons[k]['eta'])
          NoIsoPtDenDiLep.Fill(muons[k]['pt'])
        if muons[k]['isLoose'] == 1 and gLepDR<0.4 and abs(1-muons[k]['pt']/gLepPt)<0.9:
          numerator+=1
          EffCount.Fill(2)
          NoIsoPtNum.Fill(muons[k]['pt'])
          NoIsoEtaNum.Fill(muons[k]['eta'])
          NoIsoPtEtaNum.Fill(muons[k]['pt'],muons[k]['eta'])
          if muons[k]['relIso']<0.12:
             EffCount.Fill(3)
             Iso01PtNum.Fill(muons[k]['pt'])
             Iso01EtaNum.Fill(muons[k]['eta']) 
             Iso01PtEtaNum.Fill(muons[k]['pt'],muons[k]['eta'])
             #if ngNuMuFromW==2 and ngNuEFromW==0 and ngoodMuons==1 and nvetoMuons==1 and nvetoElectrons==0:
             #  Iso03PtEtaNumDiLep.Fill(muons[k]['pt'],muons[k]['eta'])
             #  Iso03EtaNumDiLep.Fill(muons[k]['eta'])
             #  Iso03PtNumDiLep.Fill(muons[k]['pt'])               
          if muons[k]['relIso']<0.2:
             EffCount.Fill(4)
             Iso02PtNum.Fill(muons[k]['pt'])
             Iso02EtaNum.Fill(muons[k]['eta']) 
             Iso02PtEtaNum.Fill(muons[k]['pt'],muons[k]['eta'])
             if ngNuMuFromW==2 and ngNuEFromW==0 and ngoodMuons==1 and nvetoMuons==1 and nvetoElectrons==0:
               Iso03PtEtaNumDiLep.Fill(muons[k]['pt'],muons[k]['eta'])
               Iso03EtaNumDiLep.Fill(muons[k]['eta'])
               Iso03PtNumDiLep.Fill(muons[k]['pt'])               
          if muons[k]['relIso']<0.3:
             Iso03PtNum.Fill(muons[k]['pt'])
             Iso03EtaNum.Fill(muons[k]['eta'])
             Iso03PtEtaNum.Fill(muons[k]['pt'],muons[k]['eta'])
             EffCount.Fill(5)
print 'Number of events passing only cuts for denominator:', EffCount.GetBinContent(1)
print 'Number of events passing cuts without Isolation for Numerator:', EffCount.GetBinContent(2)
print 'Number of events passing cuts with Isolation 0.1 for Numerator:', EffCount.GetBinContent(3)
print 'Number of events passing cuts with Isolation 0.2 for Numerator:', EffCount.GetBinContent(4)
print 'Number of events passing cuts with Isolation 0.3 for Numerator:', EffCount.GetBinContent(5)

Efftemp = EffCount.GetBinContent(5)/EffCount.GetBinContent(1)
print 'weight*(Iso0.3/denominatorevents) Supposed to be EigenEff for finding dimuon:', weight*(Efftemp)
print 'Supposed to be EigenEff for finding 1 lost lepton :', weight*(1-Efftemp)
###Eff Calculation
for j in range(len(ptBins)):
  denNoIsoPt = NoIsoPtDen.GetBinContent(j)
  numNoIsoPt = NoIsoPtNum.GetBinContent(j)
  numIso01Pt = Iso01PtNum.GetBinContent(j)
  numIso02Pt = Iso02PtNum.GetBinContent(j)
  numIso03Pt = Iso03PtNum.GetBinContent(j)
  denNoIsoPtDiLep = NoIsoPtDenDiLep.GetBinContent(j)
  numIso03PtDiLep = Iso03PtNumDiLep.GetBinContent(j)
  if denNoIsoPt != 0:
    effnoIsoPt=float(numNoIsoPt)/denNoIsoPt
    NoIsoPtEff.SetBinContent(j,effnoIsoPt)
    effIso01Pt=float(numIso01Pt)/denNoIsoPt
    Iso01PtEff.SetBinContent(j,effIso01Pt)
    effIso02Pt=float(numIso02Pt)/denNoIsoPt
    Iso02PtEff.SetBinContent(j,effIso02Pt)
    effIso03Pt=float(numIso03Pt)/denNoIsoPt
    Iso03PtEff.SetBinContent(j,effIso03Pt)
  if denNoIsoPtDiLep != 0:
    effIso03PtDiLep=float(numIso03PtDiLep)/denNoIsoPtDiLep
    Iso03PtEffDiLep.SetBinContent(j,effIso03PtDiLep)
for i in range(len(etaBins)):
  denNoIsoEta = NoIsoEtaDen.GetBinContent(i)
  numNoIsoEta = NoIsoEtaNum.GetBinContent(i)
  numIso01Eta = Iso01EtaNum.GetBinContent(i)
  numIso02Eta = Iso02EtaNum.GetBinContent(i)
  numIso03Eta = Iso03EtaNum.GetBinContent(i)
  denNoIsoEtaDiLep = NoIsoEtaDenDiLep.GetBinContent(i)
  numIso03EtaDiLep = Iso03EtaNumDiLep.GetBinContent(i)
  if denNoIsoEta != 0:
    effnoIsoEta=float(numNoIsoEta)/denNoIsoEta
    NoIsoEtaEff.SetBinContent(i,effnoIsoEta)
    effIso01Eta=float(numIso01Eta)/denNoIsoEta
    Iso01EtaEff.SetBinContent(i,effIso01Eta)
    effIso02Eta=float(numIso02Eta)/denNoIsoEta
    Iso02EtaEff.SetBinContent(i,effIso02Eta)
    effIso03Eta=float(numIso03Eta)/denNoIsoEta
    Iso03EtaEff.SetBinContent(i,effIso03Eta)
  if denNoIsoEtaDiLep !=0:
    effIso03EtaDiLep=float(numIso03EtaDiLep)/denNoIsoEtaDiLep
    Iso03EtaEffDiLep.SetBinContent(i,effIso03EtaDiLep)
##2Dcalculation
for p in range(len(ptBinsCoarse)):
  for k in range(len(etaBinsCoarse)):
    NoIsoPtEtanum = NoIsoPtEtaNum.GetBinContent(p,k)
    NoIsoPtEtaden = NoIsoPtEtaDen.GetBinContent(p,k)
    Iso01PtEtanum = Iso01PtEtaNum.GetBinContent(p,k)
    Iso02PtEtanum = Iso02PtEtaNum.GetBinContent(p,k)
    Iso03PtEtanum = Iso03PtEtaNum.GetBinContent(p,k)
    NoIsoPtEtadenDiLep = NoIsoPtEtaDenDiLep.GetBinContent(p,k)
    Iso03PtEtanumDiLep = Iso03PtEtaNumDiLep.GetBinContent(p,k)
    if NoIsoPtEtaden != 0:
      effnoIsoPtEta=float(NoIsoPtEtanum)/NoIsoPtEtaden
      NoIsoPtEtaEff.SetBinContent(p,k,effnoIsoPtEta)
      effIso01PtEta=float(Iso01PtEtanum)/NoIsoPtEtaden
      Iso01PtEtaEff.SetBinContent(p,k,effIso01PtEta)
      effIso02PtEta=float(Iso02PtEtanum)/NoIsoPtEtaden
      Iso02PtEtaEff.SetBinContent(p,k,effIso02PtEta)
      effIso03PtEta=float(Iso03PtEtanum)/NoIsoPtEtaden
      Iso03PtEtaEff.SetBinContent(p,k,effIso03PtEta)
      effIso03PtEtaFindDilep=float(Iso03PtEtanumDiLep)/NoIsoPtEtaden
      Iso03PtEtaEffFindDiLep.SetBinContent(p,k,effIso03PtEtaFindDilep)
    if NoIsoPtEtadenDiLep != 0:
      effIso03PtEtaDiLep=float(Iso03PtEtanumDiLep)/NoIsoPtEtadenDiLep
      Iso03PtEtaEffDiLep.SetBinContent(p,k,effIso03PtEtaDiLep)

File.cd() 
          
canPt = ROOT.TCanvas('Pt')
canPt.cd()
NoIsoPtEff.Draw('p')
canPt01 = ROOT.TCanvas('Pt')
canPt01.cd()
Iso01PtEff.Draw('p')

canEta = ROOT.TCanvas('Eta')
canEta.cd()
NoIsoEtaEff.Draw('p')

canEta01 = ROOT.TCanvas('Eta')
canEta01.cd()
Iso01EtaEff.Draw('p')

can2D = ROOT.TCanvas('2dNoIso')
can2D.cd()
NoIsoPtEtaEff.Draw('colz')
can2D.Write()

can2D1 = ROOT.TCanvas('2dIso01')
can2D1.cd()
Iso01PtEtaEff.Draw('colz')
can2D1.Write()

can2D2 = ROOT.TCanvas('2dIso02')
can2D2.cd()
Iso02PtEtaEff.Draw('colz')
can2D2.Write()

can2D3 = ROOT.TCanvas('2dIso03')
can2D3.cd()
Iso03PtEtaEff.Draw('colz')
can2D3.Write()


File.Write()
File.Close()

