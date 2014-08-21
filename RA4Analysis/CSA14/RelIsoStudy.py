import ROOT
from stage2Tuples import ttJetsCSA1450ns , ttJetsCSA1425ns
from localInfo import username


def getMu(c,j):
  muIsGlobal = c.GetLeaf('muIsGlobal').GetValue(j)
  muIsTracker = c.GetLeaf('muIsTracker').GetValue(j)
  dz = c.GetLeaf('muDz').GetValue(j)
  pt = c.GetLeaf('muPt').GetValue(j)
  eta= c.GetLeaf('muEta').GetValue(j)
  phi= c.GetLeaf('muPhi').GetValue(j)
  Pdg= c.GetLeaf('gLepPdg').GetValue(j)
  gLepDR = c.GetLeaf('gLepDR').GetValue(j)
  RelIso = c.GetLeaf('muRelIso').GetValue(j)
  cand={'muIsGlobal':muIsGlobal, 'muIsTracker':muIsTracker, 'dz':dz, 'pt':pt, 'eta':eta, 'phi':phi, 'Pdg':Pdg, 'gLepDR':gLepDR, 'RelIso':RelIso}
  #if pt>5 and (muIsGlobal or  muIsTracker) and abs(eta)<2.5 and abs(dz)< 0.5 and gLepDR<0.5:
  if pt>5 and abs(eta)<2.5 and abs(dz)<0.5 and (muIsGlobal or  muIsTracker):
   return cand

h_RelIso50 = ROOT.TH1F('muRelIso', 'muRelIso',100,0,1)
h_RelIso25 = ROOT.TH1F('muRelIso', 'muRelIso',100,0,1)

c50 = ROOT.TChain('Events')
#for b in ttJetsCSA1450ns['bins']:
#  c.Add(ttJetsCSA1450ns['dirname']+'/'+b+'/h*.root')
c50.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from0To10.root')

c25 = ROOT.TChain('Events')
#for b in ttJetsCSA1425ns['bins']:
#  c2.Add(ttJetsCSA1425ns['dirname']+'/'+b+'/h*.root')
c25.Add('/data/schoef/convertedTuples_v23/copyMET/ttJetsCSA1425ns/histo_ttJetsCSA14_from0To10.root')


number_events50 = c50.GetEntries()
print number_events50
for i in range(number_events50):
  c50.GetEntry(i)
  nmuons = c50.GetLeaf('nmuCount').GetValue()
  for mu in range(int(nmuons)):
    muons50 = getMu(c50,mu)
    if muons50['gLepDR']<0.5:
      h_RelIso50.Fill(muons50['RelIso'])

number_events25 = c25.GetEntries()
print number_events25
for i in range(number_events25):
  c25.GetEntry(i)
  nmuons = c25.GetLeaf('nmuCount').GetValue()
  for mu in range(int(nmuons)):
    muons25 = getMu(c25,mu)
    if muons25['gLepDR']<0.5:
      h_RelIso25.Fill(muons25['RelIso'])


can = ROOT.TCanvas()
h_RelIso50.SetLineColor(ROOT.kRed)   ## 1:50ns  , 2:25ns
#h_RelIso50.Scale(1/h_RelIso50.Integral())
h_RelIso50.SetLineWidth(2)
h_RelIso50.Draw()
#h_RelIso25.Scale(h_RelIso50.Integral()/h_RelIso25.Integral())
h_RelIso25.SetLineColor(ROOT.kBlue)
h_RelIso25.SetLineWidth(2)
h_RelIso25.Draw('same')
#can.SetLogy()
can.Print('/afs/hephy.at/user/e/easilar/www/LastCSA14/MuonRelIsoComp.png')




