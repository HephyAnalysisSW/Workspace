import ROOT, pickle, itertools

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()

def getHistMCTruthEfficiencies(MCEff, histname, etaBin = (0,0.8), hadron='b'):
  nBins = len(MCEff)
  hist = ROOT.TH1F(histname,'MC truth b-tag efficiency',nBins,0,nBins)
  effs = []
  for a in sorted(MCEff):
    effs.append(MCEff[a][etaBin][hadron])
  for b in range(1,nBins+1):
    hist.SetBinContent(b,effs[b-1])
    hist.GetXaxis().SetBinLabel(b,varBinHalfOpen(sorted(MCEff.keys())[b-1]))
  return hist

can = ROOT.TCanvas('can','can',600,600)
can.SetBottomMargin(0.22)

effs = pickle.load(file('/data/dspitzbart/Spring16/btagEfficiency/effs_presel_Spring15_for_check_pkl'))

h_b_1 = getHistMCTruthEfficiencies(effs['WJets'], 'h_b_1', etaBin = (0,0.8), hadron='b')
h_b_2 = getHistMCTruthEfficiencies(effs['WJets'], 'h_b_2', etaBin = (0.8,1.6), hadron='b')
h_b_3 = getHistMCTruthEfficiencies(effs['WJets'], 'h_b_3', etaBin = (1.6,2.4), hadron='b')

h_c_1 = getHistMCTruthEfficiencies(effs['WJets'], 'h_c_1', etaBin = (0,0.8), hadron='c')
h_c_2 = getHistMCTruthEfficiencies(effs['WJets'], 'h_c_2', etaBin = (0.8,1.6), hadron='c')
h_c_3 = getHistMCTruthEfficiencies(effs['WJets'], 'h_c_3', etaBin = (1.6,2.4), hadron='c')

h_l_1 = getHistMCTruthEfficiencies(effs['WJets'], 'h_l_1', etaBin = (0,0.8), hadron='other')
h_l_2 = getHistMCTruthEfficiencies(effs['WJets'], 'h_l_2', etaBin = (0.8,1.6), hadron='other')
h_l_3 = getHistMCTruthEfficiencies(effs['WJets'], 'h_l_3', etaBin = (1.6,2.4), hadron='other')

h_b_1.SetLineColor(ROOT.kAzure+12)
h_b_2.SetLineColor(ROOT.kAzure+9)
h_b_3.SetLineColor(ROOT.kAzure+6)

h_c_1.SetLineColor(ROOT.kGreen+3)
h_c_2.SetLineColor(ROOT.kGreen)
h_c_3.SetLineColor(ROOT.kGreen-3)

h_l_1.SetLineColor(ROOT.kRed+1)
h_l_2.SetLineColor(ROOT.kRed-1)
h_l_3.SetLineColor(ROOT.kRed-4)

hists = [h_b_2,h_b_3,h_c_1,h_c_2,h_c_3,h_l_1,h_l_2,h_l_3]

for h in hists+[h_b_1]:
  h.SetLineWidth(2)
  h.SetMarkerSize(0)
  h.SetMarkerColor(h.GetLineColor())

h_b_1.GetYaxis().SetTitle('Efficiency')
h_b_1.GetXaxis().SetTitle('p_{T} [GeV]')
h_b_1.GetXaxis().SetTitleSize(0.05)
h_b_1.GetXaxis().SetTitleOffset(2.3)

h_b_1.SetMaximum(1)
h_b_1.SetMinimum(0)
h_b_1.LabelsOption("v")



leg = ROOT.TLegend(0.16,0.78,0.44,0.95)
leg.SetFillColor(ROOT.kWhite)
leg.SetShadowColor(ROOT.kWhite)
leg.SetBorderSize(1)
leg.SetTextSize(0.035)

leg.AddEntry(None,'b hadrons','')
leg.AddEntry(h_b_1,'#bf{0.0 #leq |#eta| < 0.8}')
leg.AddEntry(h_b_2,'#bf{0.8 #leq |#eta| < 1.6}')
leg.AddEntry(h_b_3,'#bf{1.6 #leq |#eta| < 2.4}')

leg_2 = ROOT.TLegend(0.44,0.78,0.71,0.95)
leg_2.SetFillColor(ROOT.kWhite)
leg_2.SetShadowColor(ROOT.kWhite)
leg_2.SetBorderSize(1)
leg_2.SetTextSize(0.035)

leg_2.AddEntry(None,'c hadrons','')
leg_2.AddEntry(h_c_1,'#bf{0.0 #leq |#eta| < 0.8}')
leg_2.AddEntry(h_c_2,'#bf{0.8 #leq |#eta| < 1.6}')
leg_2.AddEntry(h_c_3,'#bf{1.6 #leq |#eta| < 2.4}')

leg_3 = ROOT.TLegend(0.71,0.78,0.98,0.95)
leg_3.SetFillColor(ROOT.kWhite)
leg_3.SetShadowColor(ROOT.kWhite)
leg_3.SetBorderSize(1)
leg_3.SetTextSize(0.035)

leg_3.AddEntry(None,'light/gluon','')
leg_3.AddEntry(h_l_1,'#bf{0.0 #leq |#eta| < 0.8}')
leg_3.AddEntry(h_l_2,'#bf{0.8 #leq |#eta| < 1.6}')
leg_3.AddEntry(h_l_3,'#bf{1.6 #leq |#eta| < 2.4}')

h_b_1.Draw('hist')
for h in hists:
  h.Draw('hist same')

leg.Draw()
leg_2.Draw()
leg_3.Draw()


latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.04)
latex1.SetTextAlign(11)

latex1.DrawLatex(0.16,0.96,'CMS #bf{#it{Simulation}}')
latex1.DrawLatex(0.85,0.96,'#bf{(13TeV)}')

can.Print('/afs/hephy.at/user/d/dspitzbart/www/Spring16/btagEfficiency/W_jets_Spring15_check.png')
can.Print('/afs/hephy.at/user/d/dspitzbart/www/Spring16/btagEfficiency/W_jets_Spring15_check.pdf')
can.Print('/afs/hephy.at/user/d/dspitzbart/www/Spring16/btagEfficiency/W_jets_Spring15_check.root')

