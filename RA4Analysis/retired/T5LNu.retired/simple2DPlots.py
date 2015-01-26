import ROOT
from Workspace.RA4Analysis.simplePlotsCommon import *
ROOT.tdrStyle.SetPadRightMargin(0.16)
ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/useNiceColorPalette.C")
ROOT.useNiceColorPalette()

c = ROOT.TChain('Events')
c.Add('/data/schoef/convertedTuples_v22/copy/WJetsHT150v2/histo_WJetsHT150v2_from*')
d = ROOT.TChain('Events')
d.Add('/data/schoef/convertedTuples_v22/copy/T5LNu_1000_100/histo_T5LNu_1000_100.root')
e = ROOT.TChain('Events')
e.Add('/data/schoef/convertedTuples_v22/copy/TTJetsPowHeg/histo_TTJetsPowHeg_from*')

#commoncf = 'njets>=4&&ht>400&&nTightMuons+nTightElectrons==1&&nbtags==0&&(ht>750&&type1phiMet>350)'
commoncf = 'njets>=4&&ht>400&&nTightMuons+nTightElectrons==1&&nbtags==0&&(ht>400&&type1phiMet>150)'
#v1 = ['cosDeltaPhi', 'cosDeltaPhi']
#v2 = ['htThrustLepSideRatio', 'htThrustLepSideRatio']

#v1 = ['cos(leptonPhi-jetPhi[0])', 'cosLepPhiJet0']
#v2 = ['htThrustLepSideRatio', 'htThrustLepSideRatio']

#v1 = ['cos(leptonPhi-jetPhi[0])', 'cosLepPhiJet0']
#v2 = ['cosDeltaPhi', 'cosDeltaPhi']

#v1 = ['mT', 'mT', 'm_{T} (GeV)']
#v2 = ['Max$(gpM*(abs(gpPdg)==24))','mW', 'M_{W} (GeV)']

v1 = ['mT', 'mT', 'm_{T} (GeV)']
v2 = ['Max$(gpPt*(abs(gpPdg)==24))','pTW', 'p_{T,W} (GeV)']

c1 = ROOT.TCanvas()
c.Draw(v1[0]+':'+v2[0]+'>>hTMP', commoncf, 'COLZ')
c1.SetLogz()
ROOT.hTMP.GetXaxis().SetTitle(v2[2])
ROOT.hTMP.GetYaxis().SetTitle(v1[2])
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngT5LNu2D/'+v1[1]+'_'+v2[1]+'_WJetsHT150v2.png')
#c1 = ROOT.TCanvas()
#c1.SetLogz()
#d.Draw(v1[0]+':'+v2[0]+'>>hTMP', commoncf, 'COLZ')
#ROOT.hTMP.GetXaxis().SetTitle(v2[1])
#ROOT.hTMP.GetYaxis().SetTitle(v1[1])
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngT5LNu2D/'+v1[1]+'_'+v2[1]+'_T5LNu_1000_100.png')
c1 = ROOT.TCanvas()
c1.SetLogz()
e.Draw(v1[0]+':'+v2[0]+'>>hTMP', commoncf, 'COLZ')
ROOT.hTMP.GetXaxis().SetTitle(v2[2])
ROOT.hTMP.GetYaxis().SetTitle(v1[2])
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngT5LNu2D/'+v1[1]+'_'+v2[1]+'_TTJetsPowHeg.png')
