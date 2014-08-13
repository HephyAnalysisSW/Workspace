import ROOT
from stage2Tuples import ttJetsCSA14

htCut     = 400
metCut    = 150
minNJets  =   4

c = ROOT.TChain('Events')
for b in ttJetsCSA14['bins']:
#  c.Add(ttJetsCSA14['dirname']+'/'+b+'/h*_from0To10.root')
  c.Add(ttJetsCSA14['dirname']+'/'+b+'/h*.root')
#Apply loose lepton selection to genTau selection for comparison
hMT = ROOT.TH1F('hMT', 'hMT',40,0,800)
oneHadTau="ngoodMuons==1&&nvetoMuons==1&&Sum$(gTauPt>15&&abs(gTauEta)<2.5&&gTauNENu+gTauNMuNu==0&&gTauNTauNu==1)==1"
c.Draw('sqrt(2.*met*leptonPt*(1-cos(leptonPhi-metphi)))>>hMT','weight*('+oneHadTau+'&&ht>'+str(htCut)+'&&njets>='+str(minNJets)+'&&met>'+str(metCut)+')','goff')

cPred = ROOT.TChain('Events')
hMTPred = ROOT.TH1F('hMTPred', 'hMTPred',40,0,800)
cPred.Add('/data/schoef/results2014/tauTuples/CSA14_TTJets_genTau.root')
cPred.Draw('mTPred>>hMTPred','weightPred*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

scaleF = (1-0.1741-0.1783)*0.1125/(0.1057+0.1075)

c1=ROOT.TCanvas()
hMTPred.SetLineColor(ROOT.kRed)
hMTPred.Scale(scaleF)
#hMTPred.Scale(hMT.Integral()/hMTPred.Integral())
hMTPred.Draw()
hMT.Draw('same')
c1.SetLogy()
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/comp.png')
