import ROOT
from Workspace.RA4Analysis.stage2Tuples import ttJetsCSA1450ns
from Workspace.RA4Analysis.helpers import deltaPhi
from math import *

htCut     = 750
metCut    = 150
minNJets  =   6

#htCut     = 0
#metCut    = 0
#minNJets  =   0

c = ROOT.TChain('Events')
for b in ttJetsCSA1450ns['bins']:
  c.Add(ttJetsCSA1450ns['dirname']+'/'+b+'/histo_ttJetsCSA1450ns_from*.root')
#c.Add('/data/easilar/results2014/tauTuples/CSA14_TTJets_Tau_reco.root')

cPred = ROOT.TChain('Events')
#cPred.Add('/data/schoef/results2014/tauTuples/CSA14_TTJets_hadGenTau.root')
cPred.Add('/data/easilar/results2014/tauTuples/CSA14_TTJets_hadGenTau.root')

oneHadTau     ="ngoodMuons==1&&nvetoMuons==1&&nvetoElectrons==0&&Sum$(gTauPt>15&&abs(gTauEta)<2.5&&gTauNENu+gTauNMuNu==0&&gTauNTauNu==1)==1"
oneHadTauOpen ="ngoodMuons==1&&nvetoMuons==1&&nvetoElectrons==0&&Sum$(gTauNENu+gTauNMuNu==0&&gTauNTauNu==1)==1"
#oneHadTau     ="ngNuMuFromW==1&&ngoodMuons==1&&nvetoMuons==1&&nvetoElectrons==0&&Sum$(gTauPt>15&&abs(gTauEta)<2.5&&gTauNENu+gTauNMuNu==0&&gTauNTauNu==1)==1"
#oneHadTauOpen ="ngNuMuFromW==1&&ngoodMuons==1&&nvetoMuons==1&&nvetoElectrons==0&&Sum$(gTauNENu+gTauNMuNu==0&&gTauNTauNu==1)==1"

#scaleF = (1-0.1741-0.1783)*0.1125/(0.1057+0.1075)
scaleF = (1-0.1741-0.1783)*0.1125/(0.1057)

File = ROOT.TFile('/afs/hephy.at/user/e/easilar/CMSSW_7_0_6_patch1/src/Workspace/RA4Analysis/rootfiles/Phi.root','RECREATE')
File.cd()

# hMT = ROOT.TH1F('hMT', 'hMT',20,0,800)
# c.Draw('sqrt(2.*met*leptonPt*(1-cos(leptonPhi-metphi)))>>hMT','weight*('+oneHadTau+'&&ht>'+str(htCut)+'&&njets>='+str(minNJets)+'&&met>'+str(metCut)+')','goff')
#
# hMTOpen = ROOT.TH1F('hMTOpen', 'hMTOpen',20,0,800)
# c.Draw('sqrt(2.*met*leptonPt*(1-cos(leptonPhi-metphi)))>>hMTOpen','weight*('+oneHadTauOpen+'&&ht>'+str(htCut)+'&&njets>='+str(minNJets)+'&&met>'+str(metCut)+')','goff')
#
# hMTPred = ROOT.TH1F('hMTPred', 'hMTPred',20,0,800)
# cPred.Draw('mTPred>>hMTPred','weightPred*scaleLEff*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

Mt = 'sqrt(2*leptonPt*met*(1-cos(metphi-leptonPhi)))'
Wx = '(met*cos(metphi)+leptonPt*cos(leptonPhi))'
Wy = '(met*sin(metphi)+leptonPt*sin(leptonPhi))'
Lx = 'leptonPt*cos(leptonPhi))'
Ly = 'leptonPt*sin(leptonPhi))'
WPhi = '(atan2('+Wy+','+Wx+'))'
WPT = 'sqrt('+Wx+'**2+'+Wy+'**2)'
#StLep = 'sqrt('+WPT+'**2+'+Mt+'**2)'
num = '(('+Wx+'*'+Lx+')+('+Wy+'*'+Ly+'))'
den = '('+WPT+'*leptonPt)'
DPhi = 'arccos('+num+'/'+den+')'

hDeltaPhi = ROOT.TH1F('hDeltaPhi', 'hDeltaPhi',25,0,10)
c.Draw(DPhi+'>>hDeltaPhi','weight*('+oneHadTau+'&&ht>'+str(htCut)+'&&njets>='+str(minNJets)+'&&met>'+str(metCut)+')','goff')

hDeltaPhiOpen = ROOT.TH1F('hDeltaPhiOpen', 'hWPhiOpen',25,0,10)
c.Draw(DPhi+'>>hDeltaPhiOpen','weight*('+oneHadTauOpen+'&&ht>'+str(htCut)+'&&njets>='+str(minNJets)+'&&met>'+str(metCut)+')','goff')

hDeltaPhiPred = ROOT.TH1F('hDeltaPhiPred', 'hDeltaPhiPred',25,0,10)
cPred.Draw('DeltaPhi>>hDeltaPhiPred','weightPred*scaleLEff*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

# c1=ROOT.TCanvas()
# hMTPred.SetLineColor(ROOT.kRed)
# hMTPred.Scale(scaleF)
# #hMTPred.Scale(hMT.Integral()/hMTPred.Integral())
# hMTPred.Draw()
# hMTOpen.SetLineStyle(2)
# hMTOpen.Draw('same')
# hMT.Draw('same')
# c1.SetLogy()
# c1.Print('/afs/hephy.at/user/e/easilar/www/EcecompMT_hadTau.png')

# cd=ROOT.TCanvas()
# hDeltaPhiPred.SetLineColor(ROOT.kRed)
# hDeltaPhiPred.Scale(scaleF)
# #hDeltaPhiPred.Scale(hDeltaPhi.Integral()/hDeltaPhiPred.Integral())
# hDeltaPhiPred.Draw()
# hDeltaPhiOpen.SetLineStyle(2)
# hDeltaPhiOpen.Draw('same')
# hDeltaPhi.Draw('same')
# cd.SetLogy()
# cd.Print('/afs/hephy.at/user/e/easilar/www/compDeltaPhi_hadTau.png')

# hHT = ROOT.TH1F('hHT', 'hHT',25,0,2500)
# c.Draw('ht>>hHT','weight*('+oneHadTau+'&&ht>'+str(htCut)+'&&njets>='+str(minNJets)+'&&met>'+str(metCut)+')','goff')
#
# hHTPred = ROOT.TH1F('hHTPred', 'hHTPred',25,0,2500)
# cPred.Draw('htPred>>hHTPred','weightPred*scaleLEff*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
#
# c1=ROOT.TCanvas()
# hHTPred.SetLineColor(ROOT.kRed)
# hHTPred.Scale(scaleF)
# #hHTPred.Scale(hHT.Integral()/hHTPred.Integral())
# hHTPred.Draw()
# hHT.Draw('same')
# c1.SetLogy()
# c1.Print('/afs/hephy.at/user/e/easilar/www/EcecompHT_hadTau.png')
#
# hNJet = ROOT.TH1F('hNJet', 'hNJet',12,0,12)
# c.Draw('njets>>hNJet','weight*('+oneHadTau+'&&ht>'+str(htCut)+'&&njets>='+str(minNJets)+'&&met>'+str(metCut)+')','goff')
#
# hNJetPred = ROOT.TH1F('hNJetPred', 'hNJetPred',12,0,12)
# cPred.Draw('njetsPred>>hNJetPred','weightPred*scaleLEff*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
#
# c1=ROOT.TCanvas()
# hNJetPred.SetLineColor(ROOT.kRed)
# hNJetPred.Scale(scaleF)
# #hNJetPred.Scale(hNJet.Integral()/hNJetPred.Integral())
# hNJetPred.Draw()
# hNJet.Draw('same')
# c1.SetLogy()
# c1.Print('/afs/hephy.at/user/e/easilar/www/EcecompNJet_hadTau.png')


File.Write()
File.Close()
