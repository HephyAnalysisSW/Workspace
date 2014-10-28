import ROOT
from Workspace.RA4Analysis.stage2Tuples import ttJetsCSA1450ns
from Workspace.RA4Analysis.helpers import deltaPhi
from math import *

htCut     = 500
metCut    = 200
minNJets  =   3
print 'ht:', htCut, 'met:',metCut
#htCut     = 0
#metCut    = 0
#minNJets  = 0

c = ROOT.TChain('Events')
for b in ttJetsCSA1450ns['bins']:
  c.Add(ttJetsCSA1450ns['dirname']+'/'+b+'/histo_ttJetsCSA1450ns_from*.root')
#c.Add('/data/easilar/results2014/tauTuples/CSA14_TTJets_Tau_reco.root')

cPred = ROOT.TChain('Events')
#cPred.Add('/data/schoef/results2014/tauTuples/CSA14_TTJets_hadGenTau.root')
cPred.Add('/data/easilar/results2014/tauTuples/CSA14_TTJets_hadGenTauTryBtag.root')

cPred110 = ROOT.TChain('Events')
cPred110.Add('/data/easilar/results2014/tauTuples/CSA14_TTJets_hadGenTauTryBtag110.root')

cPred09 = ROOT.TChain('Events')
cPred09.Add('/data/easilar/results2014/tauTuples/CSA14_TTJets_hadGenTauTryBtag09.root')

oneHadTau     ="ngoodMuons==1&&nvetoMuons==1&&nvetoElectrons==0&&Sum$(gTauPt>15&&abs(gTauEta)<2.5&&gTauNENu+gTauNMuNu==0&&gTauNTauNu==1)==1"
oneHadTauOpen ="ngoodMuons==1&&nvetoMuons==1&&nvetoElectrons==0&&Sum$(gTauNENu+gTauNMuNu==0&&gTauNTauNu==1)==1"
#oneHadTau     ="ngNuMuFromW==1&&ngoodMuons==1&&nvetoMuons==1&&nvetoElectrons==0&&Sum$(gTauPt>15&&abs(gTauEta)<2.5&&gTauNENu+gTauNMuNu==0&&gTauNTauNu==1)==1"
#oneHadTauOpen ="ngNuMuFromW==1&&ngoodMuons==1&&nvetoMuons==1&&nvetoElectrons==0&&Sum$(gTauNENu+gTauNMuNu==0&&gTauNTauNu==1)==1"

#scaleF = (1-0.1741-0.1783)*0.1125/(0.1057+0.1095)
scaleF = (1-0.1741-0.1783)*0.1125/(0.1057)

File = ROOT.TFile('/data/easilar/results2014/rootfiles/PhiSil.root','RECREATE')
File.cd()

hMT = ROOT.TH1F('hMT', 'hMT',20,0,800)
hMT.Sumw2()
c.Draw('sqrt(2.*met*leptonPt*(1-cos(leptonPhi-metPhi)))>>hMT','weight*('+oneHadTau+'&&ht>'+str(htCut)+'&&nbtags<100&&njets>='+str(minNJets)+'&&met>'+str(metCut)+')','goff')
hMTOpen = ROOT.TH1F('hMTOpen', 'hMTOpen',20,0,800)
c.Draw('sqrt(2.*met*leptonPt*(1-cos(leptonPhi-metPhi)))>>hMTOpen','weight*('+oneHadTauOpen+'&&ht>'+str(htCut)+'&&nbtags<100&&njets>='+str(minNJets)+'&&met>'+str(metCut)+')','goff')

hMTPred = ROOT.TH1F('hMTPred', 'hMTPred',20,0,800)
hMTPred.Sumw2()
cPred.Draw('mTPred>>hMTPred','weightPred*scaleLEff*('+str(scaleF)+')*(htPred>'+str(htCut)+'&&nbtags<100&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hMTPred110 = ROOT.TH1F('hMTPred110', 'hMTPred110',20,0,800)
hMTPred110.Sumw2()
cPred110.Draw('mTPred>>hMTPred110','weightPred*scaleLEff*('+str(scaleF)+')*(htPred>'+str(htCut)+'&&nbtags<100&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hMTPred09 = ROOT.TH1F('hMTPred09', 'hMTPred09',20,0,800)
cPred09.Draw('mTPred>>hMTPred09','weightPred*scaleLEff*('+str(scaleF)+')*(htPred>'+str(htCut)+'&&nbtags<100&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

# ePred = ROOT.Double()
# eTruth = ROOT.Double()
# ePred110 = ROOT.Double()
# Pred = hMTPred.IntegralAndError(0,hMTPred.GetNbinsX(),ePred)
# Truth = hMT.IntegralAndError(0,hMT.GetNbinsX(),eTruth)
# Pred110 = hMTPred110.IntegralAndError(0,hMTPred110.GetNbinsX(),eTruth)
# print 'Prediction yield:', Pred
# print 'Truth yield:', Truth
# print 'ePred :', ePred
# print 'eTruth:', eTruth
# print 'Pred:' , Pred, '+-',ePred,'(stat)+-', Pred110-Pred,'Leff'
# print 'Truth:' , Truth, '+-',eTruth,'(stat)+-'


Mt = 'sqrt(2*leptonPt*met*(1-cos(metPhi-leptonPhi)))'
Wx = 'met*cos(metPhi)+leptonPt*cos(leptonPhi)'
Wy = 'met*sin(metPhi)+leptonPt*sin(leptonPhi)'
Lx = 'leptonPt*cos(leptonPhi)'
Ly = 'leptonPt*sin(leptonPhi)'
WPhi = 'atan2(('+Wy+'),('+Wx+'))'
WPT = 'sqrt(('+Wx+')**2+('+Wy+')**2)'
StLep = 'sqrt(('+WPT+')**2+('+Mt+')**2)'
num = '(('+Wx+')*('+Lx+'))+(('+Wy+')*('+Ly+'))'
den = '('+WPT+')*leptonPt'
cosDPhi = '('+num+')/('+den+')'
DPhi = 'acos(('+cosDPhi+'))'

hDeltaPhi = ROOT.TH1F('hDeltaPhi', 'hDeltaPhi',25,0,3.14)
hDeltaPhi.Sumw2()
c.Draw(DPhi+'>>hDeltaPhi','weight*('+DPhi+'>1&&'+oneHadTau+'&&ht>'+str(htCut)+'&&nbtags<100&&njets>='+str(minNJets)+'&&met>'+str(metCut)+')','goff')

hDeltaPhiOpen = ROOT.TH1F('hDeltaPhiOpen', 'hWPhiOpen',25,0,3.14)
c.Draw(den+'>>hDeltaPhiOpen','weight*('+oneHadTauOpen+'&&ht>'+str(htCut)+'&&nbtags<100&&njets>='+str(minNJets)+'&&met>'+str(metCut)+')','goff')

hDeltaPhiPred = ROOT.TH1F('hDeltaPhiPred', 'hDeltaPhiPred',25,0,3.14)
hDeltaPhiPred.Sumw2()
cPred.Draw('DeltaPhi>>hDeltaPhiPred','weightPred*scaleLEff*('+str(scaleF)+')*(DeltaPhi>1&&htPred>'+str(htCut)+'&&nbtags<100&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hDeltaPhiPred110 = ROOT.TH1F('hDeltaPhiPred110', 'hDeltaPhiPred110',25,0,3.14)
hDeltaPhiPred110.Sumw2()
cPred110.Draw('DeltaPhi>>hDeltaPhiPred110','weightPred*scaleLEff*('+str(scaleF)+')*(DeltaPhi>1&&htPred>'+str(htCut)+'&&nbtags<100&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
hDeltaPhiPred09 = ROOT.TH1F('hDeltaPhiPred09', 'hDeltaPhiPred09',25,0,3.14)
hDeltaPhiPred09.Sumw2()
cPred09.Draw('DeltaPhi>>hDeltaPhiPred09','weightPred*scaleLEff*('+str(scaleF)+')*(DeltaPhi>1&&htPred>'+str(htCut)+'&&nbtags<100&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

ePred = ROOT.Double()
eTruth = ROOT.Double()
ePred110 = ROOT.Double()
Pred = hDeltaPhiPred.IntegralAndError(0,hDeltaPhiPred.GetNbinsX(),ePred)
Truth = hDeltaPhi.IntegralAndError(0,hDeltaPhi.GetNbinsX(),eTruth)
Pred110 = hDeltaPhiPred110.IntegralAndError(0,hDeltaPhiPred110.GetNbinsX(),eTruth)
print 'Prediction yield:', Pred
print 'Truth yield:', Truth
print 'ePred :', ePred
print 'eTruth:', eTruth
print 'Pred:' , Pred, '+-',ePred,'(stat)+-', Pred110-Pred,'Leff'
print 'Truth:' , Truth, '+-',eTruth,'(stat)+-'



c1=ROOT.TCanvas()
hMTPred.SetLineColor(ROOT.kRed)
hMTPred.Scale(scaleF)
#hMTPred.Scale(hMT.Integral()/hMTPred.Integral())
hMTPred.Draw()
hMTOpen.SetLineStyle(2)
hMTOpen.Draw('same')
hMT.Draw('same')
c1.SetLogy()
c1.Print('/afs/hephy.at/user/e/easilar/www/EcecompMT_hadTauNobtagCut.png')

cd=ROOT.TCanvas()
hDeltaPhiPred.SetLineColor(ROOT.kRed)
#hDeltaPhiPred.Scale(scaleF)
#hDeltaPhiPred.Scale(hDeltaPhi.Integral()/hDeltaPhiPred.Integral())
hDeltaPhiPred.Draw()
hDeltaPhiOpen.SetLineStyle(2)
hDeltaPhiOpen.Draw('same')
hDeltaPhi.Draw('same')
cd.SetLogy()
cd.Print('/afs/hephy.at/user/e/easilar/www/compDeltaPhi_hadTauNobtagCut.png')

hHT = ROOT.TH1F('hHT', 'hHT',25,0,2500)
c.Draw('ht>>hHT','weight*('+oneHadTau+'&&ht>'+str(htCut)+'&&nbtags<100&&njets>='+str(minNJets)+'&&met>'+str(metCut)+')','goff')

hHTPred = ROOT.TH1F('hHTPred', 'hHTPred',25,0,2500)
cPred.Draw('htPred>>hHTPred','weightPred*scaleLEff*(htPred>'+str(htCut)+'&&nbtags<100&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

hHTPred110 = ROOT.TH1F('hHTPred110', 'hHTPred110',25,0,2500)
cPred110.Draw('htPred>>hHTPred110','weightPred*scaleLEff*('+str(scaleF)+')*(htPred>'+str(htCut)+'&&nbtags<100&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

hHTPred09 = ROOT.TH1F('hHTPred09', 'hHTPred09',25,0,2500)
cPred09.Draw('htPred>>hHTPred09','weightPred*scaleLEff*('+str(scaleF)+')*(htPred>'+str(htCut)+'&&nbtags<100&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

c1=ROOT.TCanvas()
hHTPred.SetLineColor(ROOT.kRed)
hHTPred.Scale(scaleF)
#hHTPred.Scale(hHT.Integral()/hHTPred.Integral())
hHTPred.Draw()
hHT.Draw('same')
c1.SetLogy()
c1.Print('/afs/hephy.at/user/e/easilar/www/EcecompHT_hadTauNobtagCut.png')

hNJet = ROOT.TH1F('hNJet', 'hNJet',12,0,12)
c.Draw('njets>>hNJet','weight*('+oneHadTau+'&&ht>'+str(htCut)+'&&nbtags<100&&njets>='+str(minNJets)+'&&met>'+str(metCut)+')','goff')

hNJetPred = ROOT.TH1F('hNJetPred', 'hNJetPred',12,0,12)
cPred.Draw('njetsPred>>hNJetPred','weightPred*scaleLEff*(htPred>'+str(htCut)+'&&nbtags<100&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

hNJetPred110 = ROOT.TH1F('hNJetPred110', 'hNJetPred110',12,0,12)
cPred110.Draw('njetsPred>>hNJetPred110','weightPred*scaleLEff*('+str(scaleF)+')*(htPred>'+str(htCut)+'&&nbtags<100&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

hNJetPred09 = ROOT.TH1F('hNJetPred09', 'hNJetPred09',12,0,12)
cPred09.Draw('njetsPred>>hNJetPred09','weightPred*scaleLEff*('+str(scaleF)+')*(htPred>'+str(htCut)+'&&nbtags<100&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

c1=ROOT.TCanvas()
hNJetPred.SetLineColor(ROOT.kRed)
hNJetPred.Scale(scaleF)
#hNJetPred.Scale(hNJet.Integral()/hNJetPred.Integral())
hNJetPred.Draw()
hNJet.Draw('same')
c1.SetLogy()
c1.Print('/afs/hephy.at/user/e/easilar/www/EcecompNJet_hadTauNobtagCut.png')


File.Write()
File.Close()
