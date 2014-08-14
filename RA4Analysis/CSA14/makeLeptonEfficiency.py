import ROOT
import pickle
from stage2Tuples import ttJetsCSA14
from array import array
c = ROOT.TChain('Events')
for b in ttJetsCSA14['bins']:
  c.Add(ttJetsCSA14['dirname']+'/'+b+'/h*.root')

ROOT.gStyle.SetOptStat(0)

ptBins  = array('d', [float(x) for x in range(15, 20)+range(20,50,3)+range(50,100,10)+range(100,310,30)])
etaBins = array('d', [float(x)/10. for x in range(-21,22,2)])

ptBinsCoarse  = array('d', [float(x) for x in range(15, 20,2)+range(20,50,5)+range(50,100,20)+range(100,310,50)])
etaBinsCoarse = array('d', [float(x)/10. for x in [-30]+range(-21,22,6)+[30]])


muPresEff = ROOT.TH1F('muPresEff','muPresEff',2,0,2)
c.Draw('gLepInd>=0>>muPresEff','abs(gLepPdg)==13&&gLepPt>15','goff')

muPtIDEff = ROOT.TProfile('muPtIDEff','muPtIDEff', len(ptBins)-1,ptBins,-2,2)
c.Draw('gLepDR<0.4&&abs(1-muPt[gLepInd]/gLepPt)<0.9&&muIsPF[gLepInd]&&(muIsGlobal[gLepInd]||muIsTracker[gLepInd])&&muPt[gLepInd]>15&&abs(muEta[gLepInd])<2.5&&muRelIso[gLepInd]<2.5&&abs(muDxy[gLepInd])<0.02&&abs(muDz[gLepInd])<0.5:muPt[gLepInd]>>muPtIDEff','abs(gLepPdg)==13&&gLepPt>15&&gLepInd>=0', 'goff')
muPtIDEff.Scale(muPresEff.GetMean())

muEtaIDEff = ROOT.TProfile('muEtaIDEff','muEtaIDEff', len(etaBins)-1,etaBins,-2,2)
c.Draw('gLepDR<0.4&&abs(1-muPt[gLepInd]/gLepPt)<0.9&&muIsPF[gLepInd]&&(muIsGlobal[gLepInd]||muIsTracker[gLepInd])&&muPt[gLepInd]>15&&abs(muEta[gLepInd])<2.5&&muRelIso[gLepInd]<2.5&&abs(muDxy[gLepInd])<0.02&&abs(muDz[gLepInd])<0.5:muEta[gLepInd]>>muEtaIDEff','abs(gLepPdg)==13&&gLepPt>15&&gLepInd>=0', 'goff')
muEtaIDEff.Scale(muPresEff.GetMean())

muPtEta2DEff = ROOT.TProfile2D('muPtEta2DEff','muPtEta2DEff',len(ptBinsCoarse)-1,ptBinsCoarse, len(etaBinsCoarse)-1,etaBinsCoarse)
c.Draw('gLepDR<0.4&&abs(1-muPt[gLepInd]/gLepPt)<0.9&&muIsPF[gLepInd]&&(muIsGlobal[gLepInd]||muIsTracker[gLepInd])&&muPt[gLepInd]>15&&abs(muEta[gLepInd])<2.5&&muRelIso[gLepInd]<2.5&&abs(muDxy[gLepInd])<0.02&&abs(muDz[gLepInd])<0.5:muEta[gLepInd]:muPt[gLepInd]>>muPtEta2DEff','abs(gLepPdg)==13&&gLepPt>15&&gLepInd>=0', 'goff')
muPtEta2DEff.Scale(muPresEff.GetMean())

c1 = ROOT.TCanvas()
muPtIDEff.Draw()
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/muPtIDEff.png')
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/muPtIDEff.pdf')
muEtaIDEff.Draw()
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/muEtaIDEff.png')
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/muEtaIDEff.pdf')

muPtEta2DEff.Draw('COLZ')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/muPtEta2DEff.png')
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/muEtaIDEff.pdf')
pickle.dump(muPtEta2DEff, file('/data/schoef/results2014/tauTemplates/CSA14_TTJets_vetoLeptonEfficiencyMap.pkl','w'))
