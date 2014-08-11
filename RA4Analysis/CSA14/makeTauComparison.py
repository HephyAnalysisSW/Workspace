import ROOT
from stage2Tuples import ttJetsCSA14

htCut     = 300
metCut    = 150
minNJets  =   4

c = ROOT.TChain('Events')
for b in ttJetsCSA14['bins']:
  c.Add(ttJetsCSA14['dirname']+'/'+b+'/h*.root')
#Apply loose lepton selection to genTau selection for comparison
hMT = ROOT.TH1F('hMT', 'hMT',40,0,800)
oneHadTau="ngoodMuons==1&&nvetoMuons==1&&Sum$(gTauPt>15&&abs(gTauEta)<2.5&&gTauNENu+gTauNMuNu==0&&gTauNTauNu==1)==1"
c.Draw('sqrt(2.*met*leptonPt*(1-cos(leptonPhi-metphi)))>>hMT','weight*('+oneHadTau+'&&ht>'+str(htCut)+'&&njets>='+str(minNJets)+'&&met>'+str(metCut)+')')


cPred = ROOT.TChain('Events')
hMTPred = ROOT.TH1F('hMTPred', 'hMTPred',40,0,800)
cPred.Add('/data/schoef/results2014/tauTuples/CSA14_TTJets_genTau.root')
cPred.Draw('mTPred>>hMTPred','weight*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

hMT.Draw()
hMTPred.SetLineColor(ROOT.kRed)
hMTPred.Draw('same')
