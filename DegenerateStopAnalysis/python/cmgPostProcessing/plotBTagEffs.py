## 
## Proudly stolen from Daniel Spitzbart
##

import ROOT, pickle, itertools

from Workspace.HEPHYPythonTools.helpers import *
#from Workspace.RA4Analysis.helpers import *

ROOT.gROOT.LoadMacro('../../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()

saveDir = "/afs/hephy.at/user/n/nrad/www/bTagEfficiency/8012_mAODv2_v0/"


def varBinHalfOpen(vb):
  if vb[0] < vb[1] : return '[' + str(vb[0]) + ',' +str(vb[1]) + ')'
  if vb[1]==-1 : return '#geq'+ str(vb[0])
  if vb[0]==vb[1] : return str(vb[0])

def getHistMCTruthEfficiencies(MCEff, histname, etaBin = (0,0.8), hadron='b'):
  nBins = len(MCEff)
  hist = ROOT.TH1F(histname,'MC truth b-tag efficiency',nBins,0,nBins)
  effs = []
  for a in sorted(MCEff):
    effs.append(MCEff[a][tuple(etaBin)][hadron])
  for b in range(1,nBins+1):
    hist.SetBinContent(b,effs[b-1])
    hist.GetXaxis().SetBinLabel(b,varBinHalfOpen(sorted(MCEff.keys())[b-1]))
  return hist

can = ROOT.TCanvas('can','can',600,600)
can.SetBottomMargin(0.22)

#effs = pickle.load(file('/data/dspitzbart/Spring16/btagEfficiency/effs_presel_JECv6_pkl'))
#bTagEffFile = '/data/dspitzbart/Spring16/btagEfficiency/signal_inclusive_pkl'
#bTagEffFile = "/afs/hephy.at/work/n/nrad/CMSSW/CMSSW_8_0_20/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/T2tt_allDM__presel_CSVv2L.pkl"
#effs = pickle.load(file(bTagEffFile))

#import copy
#new_effs = copy.deepcopy(effs)
#for ptBin, ptEff in effs.iteritems():
#    for etaBins in ptEff.keys()
#        effs.


#key = 'TTJets'
#key = 'T5qqqqVV_mGluino_1300To1375_mLSP_1to1250'


effs = {
        #'T2ttold_presel_CSVv2L' : pickle.load(file( "/afs/hephy.at/work/n/nrad/CMSSW/CMSSW_8_0_20/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/T2tt_allDM__presel_CSVv2L.pkl"   )),
        #'T2ttold_presel_CSVv2M' : pickle.load(file( "/afs/hephy.at/work/n/nrad/CMSSW/CMSSW_8_0_20/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/T2tt_allDM__presel_CSVv2M.pkl"   )),
        #'T2ttold_boosted_CSVv2L': pickle.load(file( "/afs/hephy.at/work/n/nrad/CMSSW/CMSSW_8_0_20/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/T2ttOld_allDM_boosted_CSVv2L.pkl"   )),
        #'T2ttold_boosted_CSVv2M': pickle.load(file( "/afs/hephy.at/work/n/nrad/CMSSW/CMSSW_8_0_20/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/T2ttOld_allDM_boosted_CSVv2M.pkl"   )),

        #'TTJets_presel_CSVv2M'  : pickle.load(file( "/afs/hephy.at/work/n/nrad/CMSSW/CMSSW_8_0_20/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/TTJets_2D_presel_CSVv2M.pkl" )),
        #'TTJets_presel_CSVv2L'  : pickle.load(file( "/afs/hephy.at/work/n/nrad/CMSSW/CMSSW_8_0_20/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/TTJets_2D_presel_CSVv2L.pkl" )),
        #'TTJets_boosted_CSVv2L' : pickle.load(file( "/afs/hephy.at/work/n/nrad/CMSSW/CMSSW_8_0_20/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/TTJets_2D_boosted_CSVv2L.pkl" )),
        #'TTJets_boosted_CSVv2M' : pickle.load(file( "/afs/hephy.at/work/n/nrad/CMSSW/CMSSW_8_0_20/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/TTJets_2D_boosted_CSVv2M.pkl" )),

        'T2ttold_OldJetClean_presel_CSVv2M' : pickle.load(file( "/afs/hephy.at/work/n/nrad/CMSSW/CMSSW_8_0_20/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/T2ttold_OldJetClean_allDM_presel_CSVv2M.pkl"   )),
        'T2ttold_OldJetClean_presel_cMVAv2M' : pickle.load(file( "/afs/hephy.at/work/n/nrad/CMSSW/CMSSW_8_0_20/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/T2ttold_OldJetClean_allDM_presel_cMVAv2M.pkl"   )),

       }



for key in effs.keys():
  
  h_b_1 = getHistMCTruthEfficiencies(effs[key], 'h_b_1', etaBin = (0,0.8), hadron='b')
  h_b_2 = getHistMCTruthEfficiencies(effs[key], 'h_b_2', etaBin = (0.8,1.6), hadron='b')
  h_b_3 = getHistMCTruthEfficiencies(effs[key], 'h_b_3', etaBin = (1.6,2.4), hadron='b')
  
  h_c_1 = getHistMCTruthEfficiencies(effs[key], 'h_c_1', etaBin = (0,0.8), hadron='c')
  h_c_2 = getHistMCTruthEfficiencies(effs[key], 'h_c_2', etaBin = (0.8,1.6), hadron='c')
  h_c_3 = getHistMCTruthEfficiencies(effs[key], 'h_c_3', etaBin = (1.6,2.4), hadron='c')
  
  h_l_1 = getHistMCTruthEfficiencies(effs[key], 'h_l_1', etaBin = (0,0.8), hadron='other')
  h_l_2 = getHistMCTruthEfficiencies(effs[key], 'h_l_2', etaBin = (0.8,1.6), hadron='other')
  h_l_3 = getHistMCTruthEfficiencies(effs[key], 'h_l_3', etaBin = (1.6,2.4), hadron='other')
  
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
  
  can.Print(saveDir+ "/" +key+'.png')
  can.Print(saveDir+ "/" +key+'.pdf')
  can.Print(saveDir+ "/" +key+'.root')
  
