import ROOT
from stage2Tuples import *

relIso=0.3
ptCut = 15
leptonID = "muIsPF&&(muIsGlobal||muIsTracker)&&muPt>"+str(ptCut)+"&&abs(muEta)<2.1"\
          +"&&abs(muDxy)<0.02&&abs(muDz)<0.5"\
          +"&&muRelIso<"+str(relIso)

htCut     = 300
metCut    = 150
minNJets  =   3

#htCut     = 0
#metCut    = 0
#minNJets  =   0

c = ROOT.TChain('Events')
for b in ttJetsCSA1450ns['bins']:
  c.Add(ttJetsCSA1450ns['dirname']+'/'+b+'/h*.root')

cPred = ROOT.TChain('Events')
cPred.Add('/data/schoef/results2014/tauTuples/CSA14_TTJets_dilep_relIso'+str(relIso)+'.root')

#diLep     ="ngoodMuons==1&&nvetoMuons==1&&nvetoElectrons==0&&Sum$(gTauPt>15&&abs(gTauEta)<2.5&&gTauNENu+gTauNMuNu==1&&gTauNTauNu==1)==1"
#diLepOpen ="ngoodMuons==1&&nvetoMuons==1&&nvetoElectrons==0&&Sum$(gTauNENu+gTauNMuNu==1&&gTauNTauNu==1)==1"
#diLep   = "ngNuEFromW+ngNuMuFromW==2&&ngNuTauFromW==0"

#Eff
#diLep   =  "ngNuEFromW==0&&ngNuMuFromW==2&&ngNuTauFromW==0&&ngoodMuons==1&&nvetoMuons==1&&nvetoElectrons==0&&Sum$(gLepPt>15&&(abs(gLepEta)<2.1&&abs(gLepPdg)==13||abs(gLepEta)<2.4&&abs(gLepPdg)==11))==2"
diLep   =  "ngNuEFromW==0&&ngNuMuFromW==2&&ngNuTauFromW==0&&ngoodMuons==1&&nvetoMuons==1&&nvetoElectrons==0&&Sum$(gLepPt>"+str(ptCut)+"&&abs(gLepEta)<2.1&&abs(gLepPdg)==13)==2"
#diLep   =  "ngNuEFromW==0&&ngNuMuFromW==2&&ngNuTauFromW==0&&ngoodMuons==1&&Sum$("+leptonID+")==1&&nvetoElectrons==0&&Sum$(gLepPt>"+str(ptCut)+"&&abs(gLepEta)<2.1&&abs(gLepPdg)==13)==2"
#Acc
#diLep   = "ngNuEFromW+ngNuMuFromW==2&&ngNuTauFromW==0&&Sum$(gLepPt>10&&(abs(gLepEta)<2.1&&abs(gLepPdg)==13||abs(gLepEta)<2.4&&abs(gLepPdg)==11))!=2"

#diLep     ="ngNuMuFromW==2&&ngNuEFromW==0&&ngNuTauFromW==0&&ngoodMuons==1&&nvetoMuons==1&&nvetoElectrons==0&&Sum$(abs(gLepPdg)==13&&gLepPt>15&&abs(gLepEta)<2.1)==2"
diLepOpen ="ngNuEFromW==0&&ngNuMuFromW==2&&ngNuTauFromW==0&&ngoodMuons==1&&nvetoMuons==1&&nvetoElectrons==0"

#scaleF = (1-0.1741-0.1783)*0.1125/(0.1057+0.1075)
#scaleF = (0.1741+0.1783)*0.1125/(0.1057)
scaleF = 1

hMT = ROOT.TH1F('hMT', 'hMT',20,120,800)
c.Draw('sqrt(2.*met*leptonPt*(1-cos(leptonPhi-metphi)))>>hMT','weight*('+diLep+'&&ht>'+str(htCut)+'&&njets>='+str(minNJets)+'&&met>'+str(metCut)+')','goff')

#hMTOpen = ROOT.TH1F('hMTOpen', 'hMTOpen',20,0,800)
#c.Draw('sqrt(2.*met*leptonPt*(1-cos(leptonPhi-metphi)))>>hMTOpen','weight*('+diLepOpen+'&&ht>'+str(htCut)+'&&njets>='+str(minNJets)+'&&met>'+str(metCut)+')','goff')

hMTPred = ROOT.TH1F('hMTPred', 'hMTPred',20,120,800)
cPred.Draw('mTPred>>hMTPred','weightPred*scaleLEff*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')

c1=ROOT.TCanvas()
hMT.Draw()
hMTPred.SetLineColor(ROOT.kRed)
hMTPred.Scale(scaleF)
hMTPred.Scale(hMT.Integral()/hMTPred.Integral())
hMTPred.Draw('same')
#hMTOpen.SetLineStyle(2)
#hMTOpen.Draw('same')
c1.SetLogy()
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/compMT_diLep_relIso'+str(relIso)+'.png')

#hHT = ROOT.TH1F('hHT', 'hHT',25,0,2500)
#c.Draw('ht>>hHT','weight*('+diLep+'&&ht>'+str(htCut)+'&&njets>='+str(minNJets)+'&&met>'+str(metCut)+')','goff')
#hHTPred = ROOT.TH1F('hHTPred', 'hHTPred',25,0,2500)
#cPred.Draw('htPred>>hHTPred','weightPred*scaleLEff*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
#c1=ROOT.TCanvas()
#hHTPred.SetLineColor(ROOT.kRed)
#hHTPred.Scale(scaleF)
##hHTPred.Scale(hHT.Integral()/hHTPred.Integral())
#hHTPred.Draw()
#hHT.Draw('same')
#c1.SetLogy()
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/compHT_diLep_relIso'+str(relIso)+'.png')
#
#hNJet = ROOT.TH1F('hNJet', 'hNJet',12,0,12)
#c.Draw('njets>>hNJet','weight*('+diLep+'&&ht>'+str(htCut)+'&&njets>='+str(minNJets)+'&&met>'+str(metCut)+')','goff')
#hNJetPred = ROOT.TH1F('hNJetPred', 'hNJetPred',12,0,12)
#cPred.Draw('njetsPred>>hNJetPred','weightPred*scaleLEff*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
#c1=ROOT.TCanvas()
#hNJetPred.SetLineColor(ROOT.kRed)
#hNJetPred.Scale(scaleF)
##hNJetPred.Scale(hNJet.Integral()/hNJetPred.Integral())
#hNJetPred.Draw()
#hNJet.Draw('same')
#c1.SetLogy()
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/compNJet_diLep_relIso'+str(relIso)+'.png')
