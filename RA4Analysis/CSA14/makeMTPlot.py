import ROOT
import pickle
from stage2Tuples import ttJetsCSA14
from Workspace.HEPHYPythonTools.helpers import getPlotFromChain
from Workspace.RA4Analysis.simplePlotsCommon import ROOT_colors

c = ROOT.TChain('Events')
for b in ttJetsCSA14['bins']:
  c.Add(ttJetsCSA14['dirname']+'/'+b+'/h*.root')
#c.Add('histo_ttJetsCSA14_from0To10.root')

#lTau_H  = "ngNuEFromW+ngNuMuFromW==0&&ngNuTauFromW==1"
lTau_H  = "ngNuEFromW+ngNuMuFromW==0&&ngNuTauFromW==1&&Sum$(gTauNENu+gTauNMuNu==1&&gTauNTauNu==1)==1"
hTau_l  = "ngNuEFromW+ngNuMuFromW==1&&ngNuTauFromW==1&&Sum$(gTauNENu+gTauNMuNu==0&&gTauNTauNu==1)==1"

#diLep   = "ngNuEFromW+ngNuMuFromW==2&&ngNuTauFromW==0"
diLepEff   = "ngNuEFromW+ngNuMuFromW==2&&ngNuTauFromW==0&&Sum$(gLepPt>10&&(abs(gLepEta)<2.1&&abs(gLepPdg)==13||abs(gLepEta)<2.4&&abs(gLepPdg)==11))==2"
diLepAcc   = "ngNuEFromW+ngNuMuFromW==2&&ngNuTauFromW==0&&Sum$(gLepPt>10&&(abs(gLepEta)<2.1&&abs(gLepPdg)==13||abs(gLepEta)<2.4&&abs(gLepPdg)==11))!=2"

lTau_l  = "ngNuEFromW+ngNuMuFromW==1&&ngNuTauFromW==1&&Sum$(gTauNENu+gTauNMuNu==1&&gTauNTauNu==1)==1"
diTau   = "ngNuEFromW+ngNuMuFromW==0&&ngNuTauFromW==2"
l_H     = "ngNuEFromW+ngNuMuFromW==1&&ngNuTauFromW==0"

diHad   = "ngNuEFromW+ngNuMuFromW==0&&ngNuTauFromW==0"
hTau_H  = "ngNuEFromW+ngNuMuFromW==0&&ngNuTauFromW==1&&Sum$(gTauNENu+gTauNMuNu==0&&gTauNTauNu==1)==1"
allHad = '('+diHad+'||'+hTau_H+')'
prefix='EffAcc_nHybridMediumSel'
presel="ngoodMuons==1&&ngoodElectrons==0&&nHybridMediumMuons==1&&nvetoElectrons==0&&ht>400&&met>150"

c1 = ROOT.TCanvas()
hPresel = getPlotFromChain(c, 'sqrt(2*leptonPt*met*(1-cos(metphi-leptonPhi)))', [20,0,800], presel, 'weight')
hPresel.SetLineColor(ROOT.kBlack)
hPresel.Draw()

#hPresel_sum = getPlotFromChain(c, 'sqrt(2*leptonPt*met*(1-cos(metphi-leptonPhi)))', [20,0,800], 
#                presel+"&&("+"||".join([l_H, lTau_H, hTau_l, diLep, lTau_l, diTau, allHad])+")", 'weight')
#hPresel_sum.SetLineColor(ROOT.kMagenta)
#hPresel_sum.Draw('same')

l = ROOT.TLegend(0.5,0.7,1,1.0)
l.SetFillColor(ROOT.kWhite)
l.SetShadowColor(ROOT.kWhite)
l.SetBorderSize(1)

ROOT_colors = [ROOT.kBlack, ROOT.kRed-7, ROOT.kBlue-2, ROOT.kGreen+3, ROOT.kOrange+1,ROOT.kRed-3, ROOT.kAzure+6, ROOT.kCyan+3, ROOT.kOrange , ROOT.kRed-10]

histos=[]
l.AddEntry(hPresel, 'Total','l')
previous = None
for i, [cut,name,col] in enumerate([\
      [allHad, 'all hadronic', ROOT.kRed-7],
      [lTau_H,'W#rightarrow#tau#nu#rightarrow e/#mu+3#nu | W#rightarrow had.', ROOT.kBlue-2], 
      [diTau,'two #tau leptons', ROOT.kGreen+3], 
      [lTau_l,'W#rightarrow#tau#nu#rightarrow e/#mu+3#nu | W#rightarrow e/#mu+#nu', ROOT.kOrange+1], 
#      [diLep,'dileptonic (e/#mu)'], 
      [diLepAcc,'dileptonic (e/#mu) Acc.',ROOT.kRed-3], 
      [diLepEff,'dileptonic (e/#mu) Eff.',ROOT.kRed-4], 
      [hTau_l,'W#rightarrow#tau#nu#rightarrow had.+2#nu | W#rightarrow e/#mu+#nu', ROOT.kAzure+6], 
      [l_H, 'single lep. (e/#mu)',ROOT.kCyan+3],  
    ]):
  hPresel_cut = getPlotFromChain(c, 'sqrt(2*leptonPt*met*(1-cos(metphi-leptonPhi)))', [20,0,800], presel+"&&"+cut, 'weight')
  if previous:  
    hPresel_cut.Add(previous)
  previous=hPresel_cut.Clone()
  hPresel_cut.SetLineColor(ROOT.kBlack)
  hPresel_cut.SetLineStyle(0)
  hPresel_cut.SetLineWidth(0)
  hPresel_cut.SetFillColor(col)
  hPresel_cut.SetMarkerColor(ROOT.kBlack);
  hPresel_cut.SetMarkerStyle(0);
  hPresel_cut.SetMarkerColor(col)
  hPresel_cut.SetMarkerStyle(0);

  histos.append([hPresel_cut,name])

for h,n in reversed(histos):
  h.Draw('same')
  l.AddEntry(h, n)
  c1.SetLogy()
#hPresel.Draw('same')
c1.RedrawAxis()
l.Draw()
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/mt_'+prefix+'.png')

#hPresel_l_H = getPlotFromChain(c, 'sqrt(2*leptonPt*met*(1-cos(metphi-leptonPhi)))', [20,0,800], presel+"&&"+l_H, 'weight')
#hPresel_l_H.SetLineColor(ROOT.kRed)
#hPresel_l_H.Draw('same')
#
#hPresel_lTau_H = getPlotFromChain(c, 'sqrt(2*leptonPt*met*(1-cos(metphi-leptonPhi)))', [20,0,800], presel+"&&"+lTau_H, 'weight')
#hPresel_lTau_H.SetLineColor(ROOT.kBlue)
#hPresel_lTau_H.Draw('same')
#
#hPresel_hTau_l = getPlotFromChain(c, 'sqrt(2*leptonPt*met*(1-cos(metphi-leptonPhi)))', [20,0,800], presel+"&&"+hTau_l, 'weight')
#hPresel_hTau_l.SetLineColor(ROOT.kBlue)
#hPresel_hTau_l.Draw('same')
#
#hPresel_diLep = getPlotFromChain(c, 'sqrt(2*leptonPt*met*(1-cos(metphi-leptonPhi)))', [20,0,800], presel+"&&"+diLep, 'weight')
#hPresel_diLep.SetLineColor(ROOT.kGreen)
#hPresel_diLep.Draw('same')
#
#hPresel_lTau_l = getPlotFromChain(c, 'sqrt(2*leptonPt*met*(1-cos(metphi-leptonPhi)))', [20,0,800], presel+"&&"+lTau_l, 'weight')
#hPresel_lTau_l.SetLineColor(ROOT.kBlue)
#hPresel_lTau_l.Draw('same')
#
#hPresel_diTau = getPlotFromChain(c, 'sqrt(2*leptonPt*met*(1-cos(metphi-leptonPhi)))', [20,0,800], presel+"&&"+diTau, 'weight')
##hPresel_diTau.SetLineColor(ROOT.kGreen)
#hPresel_diTau.Draw('same')
#
#hPresel_diHad = getPlotFromChain(c, 'sqrt(2*leptonPt*met*(1-cos(metphi-leptonPhi)))', [20,0,800], presel+"&&"+diHad, 'weight')
##hPresel_diHad.SetLineColor(ROOT.kGreen)
#hPresel_diHad.Draw('same')
#
